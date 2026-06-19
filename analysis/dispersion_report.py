#!/usr/bin/env python3
"""``analysis/dispersion_report.py`` — cross-run descriptive-dispersion report
(Cycle-002 S02-T2, C2-FR-4; SDD §7).

Offline analysis over K (or 2K) sealed run dirs that share **one** ``regime_id``.
For each agent, across its K runs, it reports the observed **dispersion** of each
sanitized aggregate metric — and nothing more. It answers "how much did the
observed metric move from batch to batch?" purely descriptively; it makes **no**
strength claim and **no** inferential claim.

Reads (only):
  * each run dir's ``manifest.json`` — the authority for ``regime_id`` and
    ``agent_id`` (SDD §6.1).
  * each run dir's ``match_results/*.json`` — via ``aggregate.aggregate_run`` (the
    single source of per-run sanitized stats; SDD §7.1).
It **never** opens the per-decision sidecar files (the raw decision rows) and
never reads error-string bodies — the same sanitization surface as
``failure_report.py`` (``analysis/failure_report.py:11-19``). The module contains
no reference to that sidecar directory, so it *cannot* read raw decision rows.

Single-regime guard (SDD §7.3): before any aggregation it asserts every input run
dir shares one ``regime_id`` (read from each ``manifest.json``); on mismatch it
**hard-refuses with exit 2** — structurally identical to ``delta_report.py``'s
``CrossRegimeRefusal`` (``analysis/delta_report.py:128-143``). A v002 number can
therefore never be aggregated beside a v001 number (NFR-5); cross-regime
comparison is mechanically impossible here.

Descriptive-vs-inferential boundary (SDD §7.4): the only statistics computed are
``count``, ``min``, ``max``, ``range`` (the pair min..max), ``mean``, ``median``,
and ``spread`` (max − min) — pure arithmetic over the K per-run metric values.
The module computes **no** sample standard deviation, **no** variance, and **no**
inferential statistic (no confidence intervals, no p-values, no "significance,"
no hypothesis tests, no inferential error bars). Their absence is **structural**:
there is no code path that computes them. Every report carries ``regime_id``,
``n``, ``K``, the agent id, the unseeded-process caveat, and a Rung-1 footer; it
carries **no** ceiling of its own (``docs/ledger.md`` is the only ceiling-bearing
artifact; ``docs/claim-ceiling.md:5-6``).

# loa:shortcut: dispersion_report reuses analysis/aggregate.aggregate_run() (intra-zone)
# and copies any eval-shared helper as a parity-tested stdlib local; no eval/ import.
# Upgrade trigger: none — this is the standing offline/runtime separation (SDD §6.3),
# not a temporary shortcut.

`analysis/` imports run-dir artifacts + intra-zone helpers only — no ``cabt``,
``sim/``, ``agents/runtime/``, or ``eval/`` (the offline/runtime separation; SDD
§1.6, §6.3). stdlib only (NFR-7).

CLI:  python analysis/dispersion_report.py <run_dir> [<run_dir> ...] [--json] [--out <local-path>]
Exit: 0 report produced · 1 input failure · 2 mixed-regime refusal.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "analysis"))

import aggregate  # noqa: E402  (analysis/ — intra-zone; the per-run sanitized stats)

# The sanitized aggregate metrics dispersed across the K runs of an agent. Exactly
# the metric set defined in analysis/aggregate.py:75-89 — no other field is read or
# emitted. avg_wall_clock_ms is environment-sensitive throughput — like everywhere
# in the harness, it is reported but is never a comparison metric.
DISPERSION_METRICS = [
    "win_rate", "illegal_action_rate", "timeout_rate", "error_rate",
    "avg_turns", "avg_wall_clock_ms",
]

# The seven (and only) descriptive statistics. Pure arithmetic; no std dev /
# variance / inferential statistic is computed anywhere (SDD §7.4).
STAT_COLUMNS = ["count", "min", "max", "range", "mean", "median", "spread"]


class MixedRegimeRefusal(Exception):
    """Raised when input run dirs do not all share one regime_id (exit 2)."""


def _load_manifest(run_dir: Path) -> dict:
    mp = run_dir / "manifest.json"
    if not mp.exists():
        raise FileNotFoundError(f"{run_dir}: missing manifest.json")
    return json.loads(mp.read_text(encoding="utf-8"))


def _round(x, n=4):
    return round(x, n) if isinstance(x, (int, float)) and not isinstance(x, bool) else x


def descriptive_stats(values: "list") -> dict:
    """The seven descriptive statistics over the non-None metric values.

    ``range`` is the pair ``[min, max]``; ``spread`` is ``max − min`` (SDD §7.2).
    Pure arithmetic — ``min``/``max``/``sum`` and ``statistics.median`` only. No
    sample standard deviation, no variance, no inferential statistic is computed
    (SDD §7.4). When no value is present, ``count`` is 0 and the rest are None."""
    vals = [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]
    if not vals:
        return {"count": 0, "min": None, "max": None, "range": None,
                "mean": None, "median": None, "spread": None}
    mn, mx = min(vals), max(vals)
    return {
        "count": len(vals),
        "min": _round(mn),
        "max": _round(mx),
        "range": [_round(mn), _round(mx)],
        "mean": _round(sum(vals) / len(vals)),
        "median": _round(statistics.median(vals)),
        "spread": _round(mx - mn),
    }


def disperse(run_dirs: "list[Path]") -> dict:
    """Build the per-agent descriptive-dispersion report over the run dirs.

    Raises ``MixedRegimeRefusal`` if the run dirs do not all share one
    ``regime_id`` (exit 2). Raises ``FileNotFoundError``/``ValueError`` on input
    failure (exit 1)."""
    if not run_dirs:
        raise ValueError("no run dirs given")

    # ---- read the authoritative regime_id from every manifest FIRST ----
    manifests = []
    for rd in run_dirs:
        man = _load_manifest(rd)
        manifests.append((rd, man))
    regimes = {man.get("regime_id") for _, man in manifests}

    # ---- HARD single-regime guard (exit 2) — before any aggregation ----
    if len(regimes) != 1:
        raise MixedRegimeRefusal(
            f"refusing to disperse across regimes: the input run dirs carry "
            f"{sorted(str(r) for r in regimes)}. A dispersion report covers ONE "
            f"regime_id only (NFR-5) — a v002 number is never aggregated beside a "
            f"v001 number. Re-run with run dirs that all share one regime_id."
        )
    regime_id = next(iter(regimes))

    # ---- per-run sanitized stats + defensive manifest/records cross-check ----
    by_agent: "dict[str, list[dict]]" = {}
    n_values = set()
    for rd, man in manifests:
        stats = aggregate.aggregate_run(rd)  # reads match_results/*.json only
        # the records' regime must match the manifest authority (mirror delta_report)
        if stats.get("regime_id") != man.get("regime_id"):
            raise ValueError(
                f"{rd.name}: records regime '{stats.get('regime_id')}' != manifest "
                f"regime '{man.get('regime_id')}'")
        agent_id = man.get("agent_id") or stats.get("agent_version") or "<unknown-agent>"
        by_agent.setdefault(agent_id, []).append({
            "run_id": stats.get("run_id"),
            "agent_version": stats.get("agent_version"),
            "n_matches": stats.get("n_matches"),
            "metrics": {m: stats.get(m) for m in DISPERSION_METRICS},
        })
        if isinstance(stats.get("n_matches"), int):
            n_values.add(stats["n_matches"])

    # ---- compute per-agent dispersion of each metric across its K runs ----
    agents = []
    for agent_id in sorted(by_agent):
        runs = by_agent[agent_id]
        metric_stats = {
            m: descriptive_stats([r["metrics"].get(m) for r in runs])
            for m in DISPERSION_METRICS
        }
        agents.append({
            "agent_id": agent_id,
            "agent_version": runs[0].get("agent_version"),
            "K": len(runs),
            "run_ids": [r["run_id"] for r in runs],
            "metrics": metric_stats,
        })

    n = next(iter(n_values)) if len(n_values) == 1 else sorted(n_values)
    k_values = {a["K"] for a in agents}
    return {
        "regime_id": regime_id,
        "n": n,
        "K": (next(iter(k_values)) if len(k_values) == 1 else None),
        "agents": agents,
    }


def _fmt(v) -> str:
    if v is None:
        return "n/a"
    if isinstance(v, list) and len(v) == 2:  # range pair → min..max
        return f"{_fmt(v[0])}..{_fmt(v[1])}"
    return f"{v}"


def render(rep: dict) -> str:
    """Render the report as descriptive-only Markdown. Output contains ONLY the
    seven allowed statistics and a Rung-1 footer — no inferential term appears."""
    n_txt = _fmt(rep["n"]) if not isinstance(rep["n"], list) else ",".join(str(x) for x in rep["n"])
    k_txt = f", K={rep['K']}" if rep["K"] is not None else " (K per agent below)"
    lines = [f"# Dispersion report — {rep['regime_id']}, n={n_txt}{k_txt}", ""]
    lines.append(f"Per-agent observed dispersion across the runs of each agent under "
                 f"{rep['regime_id']}. Descriptive only.")
    lines.append("")
    for a in rep["agents"]:
        lines.append(f"## {a['agent_id']} (across K={a['K']} runs; agent={a['agent_version']})")
        lines.append("")
        lines.append("| metric | count | min | max | range | mean | median | spread |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for m in DISPERSION_METRICS:
            s = a["metrics"][m]
            lines.append(
                f"| {m} | {_fmt(s['count'])} | {_fmt(s['min'])} | {_fmt(s['max'])} | "
                f"{_fmt(s['range'])} | {_fmt(s['mean'])} | {_fmt(s['median'])} | "
                f"{_fmt(s['spread'])} |")
        lines.append("")
        wr = a["metrics"]["win_rate"]
        if wr["count"]:
            lines.append(
                f"Observed: across K={a['K']} batches of n={n_txt} under "
                f"{rep['regime_id']}, the observed win_rate ranged from {_fmt(wr['min'])} "
                f"to {_fmt(wr['max'])} (mean {_fmt(wr['mean'])}, spread {_fmt(wr['spread'])}).")
            lines.append("")
    lines.append("---")
    lines.append(
        "**Unseeded-process caveat.** Runs are unseeded (seed_controlled=false; the "
        "cabt local API exposes no RNG seed). The observed dispersion reflects the "
        "whole process — agent behaviour together with uncontrolled simulator RNG — "
        "and is NOT an isolated agent-only quantity; it cannot be separated into an "
        "agent-only figure without seed control (docs/claim-ceiling.md:42-52).")
    lines.append("")
    lines.append(
        f"**Claim ceiling.** Descriptive dispersion over {rep['regime_id']} at "
        f"n={n_txt}. NO gameplay-strength claim and NO inferential claim — these are "
        f"observed-spread diagnostics of the whole unseeded process (Rung 1). This "
        f"report carries no ceiling of its own; the experiment ledger (docs/ledger.md) "
        f"is the only ceiling-bearing artifact. A regime-v002 number is never compared "
        f"to a regime-v001 ledger row (NFR-5).")
    return "\n".join(lines)


def render_json(rep: dict) -> str:
    """JSON rendering — the same sanitized structured stats, machine-readable. Carries
    the same Rung-1 framing fields; emits only counts/rates/dispersion, never raw rows."""
    out = dict(rep)
    out["claim_ceiling"] = (
        f"Descriptive dispersion over {rep['regime_id']} at n={rep['n']}; Rung 1; "
        f"NO gameplay-strength claim, NO inferential claim; this report carries no "
        f"ceiling of its own (docs/ledger.md is the only ceiling-bearing artifact).")
    out["unseeded_caveat"] = (
        "seed_controlled=false; observed dispersion reflects the whole unseeded "
        "process (agent behaviour with uncontrolled simulator RNG), not an isolated "
        "agent-only quantity.")
    return json.dumps(out, indent=2, sort_keys=True)


def main(argv=None) -> int:
    try:  # robust report output regardless of console codepage (Windows cp1252)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(
        description="Cross-run descriptive-dispersion report over sealed run dirs "
                    "(one regime_id; descriptive-only).")
    ap.add_argument("run_dirs", nargs="+", help="sealed run dirs (e.g. runs/run-v002-b-1 ...)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    ap.add_argument("--out", default=None,
                    help="write the report to this LOCAL path instead of stdout "
                         "(local/git-ignored by default; ESP-1/OD-7)")
    args = ap.parse_args(argv)

    try:
        rep = disperse([Path(p) for p in args.run_dirs])
    except MixedRegimeRefusal as e:
        print(f"dispersion_report: REFUSED — {e}", file=sys.stderr)
        return 2
    except (FileNotFoundError, ValueError) as e:
        print(f"dispersion_report: input failure — {e}", file=sys.stderr)
        return 1

    text = render_json(rep) if args.json else render(rep)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
        print(f"dispersion_report: wrote {args.out}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
