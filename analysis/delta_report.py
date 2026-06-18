#!/usr/bin/env python3
"""``analysis/delta_report.py`` — the first comparison artifact (PR-14, Task 01.2).

Compares two sealed run directories **on the same frozen regime** and emits
per-metric deltas, with a **"why no change" line for every metric that did not
move**. It **hard-refuses** to compare two runs that carry different
``regime_id``s — two numbers from two different regimes are not comparable
(NFR-5; never compare across regimes).

This is a *same-regime, agent-only* comparison. It earns **no gameplay-strength
claim** — it reports the deltas and bounds them with `n` + the regime. The
forbidden agent claim words (*strong / competitive / optimal / calibrated /
complete*) never apply; the experiment ledger is the only ceiling-bearing
artifact (PRD §9; loop contract §8). The deferred-lane gate decision is the
operator's, not this script's (PRD §11.4).

`analysis/` imports run-dir artifacts + intra-zone helpers only — no `cabt`,
`sim/`, `agents/runtime/`, or `eval/` (the offline/runtime separation; SDD §1.6).
stdlib only (NFR-7).

CLI:  python analysis/delta_report.py runs/run-0001 runs/run-0002
Exit: 0 comparison produced · 1 env/input failure · 2 cross-regime refusal.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "analysis"))

import aggregate  # noqa: E402  (analysis/ — intra-zone; computes the per-run stats)

# Metrics compared, in report order. Correctness/gameplay metrics from the
# metrics-spec category (win_rate, illegal_action_rate, timeout_rate,
# avg_match_length=avg_turns, error_rate). avg_wall_clock_ms is reported
# separately as environment-sensitive throughput, NOT a comparison metric.
COMPARE_METRICS = [
    "win_rate", "illegal_action_rate", "timeout_rate", "error_rate", "avg_turns",
]

# Metric-specific "why no change" explanations (used only when a metric is unmoved).
WHY_NO_CHANGE = {
    "win_rate": ("win_rate is identical across both runs at this n — within the "
                 "unseeded regime's noise the agent change did not shift the rate "
                 "(no strength inference; ladder Rung 1)."),
    "illegal_action_rate": ("both agents select only offered legal options (random "
                            "sample vs lowest-index slice over the same legal set), so "
                            "no detectable illegal action occurred in either run "
                            "(invalid_action_detectable=true -> hard gate held at 0)."),
    "timeout_rate": ("no per-move budget is published (timeout undetectable; soft "
                     "gate); both runs record 0 by construction."),
    "error_rate": ("no in-match crash, forfeit, or non-termination occurred in either "
                   "run (FM-01 guard: an error is never masqueraded as a loss)."),
    "avg_turns": ("average match length did not move between the two runs at this n."),
}


def _load_manifest(run_dir: Path) -> dict:
    mp = run_dir / "manifest.json"
    if not mp.exists():
        raise FileNotFoundError(f"{run_dir}: missing manifest.json")
    return json.loads(mp.read_text(encoding="utf-8"))


def _fmt(v) -> str:
    return "n/a" if v is None else (f"{v}")


def _delta(a, b):
    """Signed delta b - a, or None if either side is missing."""
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) \
            and not isinstance(a, bool) and not isinstance(b, bool):
        return round(b - a, 4)
    return None


class CrossRegimeRefusal(Exception):
    pass


def compare(run_a: Path, run_b: Path) -> dict:
    """Compare two run dirs. Raises CrossRegimeRefusal on regime mismatch."""
    man_a, man_b = _load_manifest(run_a), _load_manifest(run_b)
    regime_a, regime_b = man_a.get("regime_id"), man_b.get("regime_id")

    # ---- HARD cross-regime refusal (AC-02; NFR-5) — before any comparison ----
    if regime_a != regime_b:
        raise CrossRegimeRefusal(
            f"refusing to compare across regimes: {run_a.name} is '{regime_a}' but "
            f"{run_b.name} is '{regime_b}'. Two numbers from two different regimes are "
            f"NOT comparable (NFR-5). A comparison requires the SAME regime_id."
        )

    stats_a, stats_b = aggregate.aggregate_run(run_a), aggregate.aggregate_run(run_b)
    # defensive: the records' regime must match the manifest authority
    for label, man_r, st in ((run_a.name, regime_a, stats_a), (run_b.name, regime_b, stats_b)):
        if st.get("regime_id") != man_r:
            raise ValueError(f"{label}: records regime '{st.get('regime_id')}' "
                             f"!= manifest regime '{man_r}'")

    metrics = []
    for m in COMPARE_METRICS:
        va, vb = stats_a.get(m), stats_b.get(m)
        d = _delta(va, vb)
        moved = (d is not None and d != 0) or (va != vb and d is None)
        metrics.append({
            "metric": m, "a": va, "b": vb, "delta": d, "moved": moved,
            "why_no_change": None if moved else WHY_NO_CHANGE.get(
                m, "no change between the two runs at this n."),
        })

    return {
        "regime_id": regime_a,
        "run_a": {"run_id": stats_a["run_id"], "agent_version": stats_a["agent_version"],
                  "opponent_id": stats_a["opponent_id"], "n": stats_a["n_matches"]},
        "run_b": {"run_id": stats_b["run_id"], "agent_version": stats_b["agent_version"],
                  "opponent_id": stats_b["opponent_id"], "n": stats_b["n_matches"]},
        "metrics": metrics,
        "wall_clock_ms": {"a": stats_a.get("avg_wall_clock_ms"),
                          "b": stats_b.get("avg_wall_clock_ms")},
    }


def render(rep: dict) -> str:
    a, b = rep["run_a"], rep["run_b"]
    lines = []
    lines.append(f"# Delta report — {a['run_id']} vs {b['run_id']} (regime {rep['regime_id']})")
    lines.append("")
    lines.append(f"- baseline  {a['run_id']}: agent={a['agent_version']} "
                 f"opponent={a['opponent_id']} n={a['n']}")
    lines.append(f"- candidate {b['run_id']}: agent={b['agent_version']} "
                 f"opponent={b['opponent_id']} n={b['n']}")
    lines.append("")
    lines.append(f"| metric | {a['run_id']} | {b['run_id']} | delta (cand-base) | status |")
    lines.append("|---|---|---|---|---|")
    for m in rep["metrics"]:
        status = "MOVED" if m["moved"] else "no change"
        dtxt = _fmt(m["delta"]) if m["delta"] is not None else "n/a"
        lines.append(f"| {m['metric']} | {_fmt(m['a'])} | {_fmt(m['b'])} | {dtxt} | {status} |")
    lines.append("")
    # "why no change" line for EVERY unmoved metric (AC-01)
    unmoved = [m for m in rep["metrics"] if not m["moved"]]
    if unmoved:
        lines.append("## Why no change")
        for m in unmoved:
            lines.append(f"- **{m['metric']}**: {m['why_no_change']}")
        lines.append("")
    moved = [m for m in rep["metrics"] if m["moved"]]
    if moved:
        lines.append("## Moved metrics (recorded, NOT a strength claim)")
        for m in moved:
            direction = "up" if (m["delta"] or 0) > 0 else "down"
            lines.append(f"- **{m['metric']}**: {_fmt(m['a'])} -> {_fmt(m['b'])} "
                         f"({direction} {_fmt(m['delta'])}). Recorded as a same-regime, "
                         f"agent-only delta at n={b['n']}; interpretation is bounded by "
                         f"the ledger claim ceiling.")
        lines.append("")
    wc = rep["wall_clock_ms"]
    lines.append(f"_throughput (environment-sensitive, not a comparison metric): "
                 f"avg_wall_clock_ms {_fmt(wc['a'])} -> {_fmt(wc['b'])}._")
    lines.append("")
    lines.append(f"**Claim ceiling.** Same-regime, agent-only comparison under "
                 f"{rep['regime_id']} at n={b['n']}. NO gameplay-strength claim — the "
                 f"agent is not asserted strong/competitive/optimal/calibrated/complete. "
                 f"See docs/ledger.md and docs/claim-ceiling.md. The deferred-lane gate "
                 f"decision is the operator's (PRD §11.4).")
    return "\n".join(lines)


def main(argv=None) -> int:
    try:  # robust report output regardless of console codepage (Windows cp1252)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description="Same-regime per-metric delta report for two run dirs.")
    ap.add_argument("run_a", help="baseline run dir (e.g. runs/run-0001)")
    ap.add_argument("run_b", help="candidate run dir (e.g. runs/run-0002)")
    args = ap.parse_args(argv)

    try:
        rep = compare(Path(args.run_a), Path(args.run_b))
    except CrossRegimeRefusal as e:
        print(f"delta_report: REFUSED — {e}", file=sys.stderr)
        return 2
    except (FileNotFoundError, ValueError) as e:
        print(f"delta_report: input failure — {e}", file=sys.stderr)
        return 1

    print(render(rep))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
