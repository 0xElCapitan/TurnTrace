#!/usr/bin/env python3
"""``analysis/aggregate.py`` — run dir → summary.csv + one ledger row (PR-7/8, Task 00.9).

Offline analysis (NFR-1): reads a sealed run directory's match-summary records
(read-only) and rolls them up — purely from the single ``result`` enum (no
denormalized w/l/d booleans; FM-01) — into:
  * ``runs/<run_id>/summary.csv`` (per-run aggregate; AC-5)
  * exactly one appended row in ``docs/ledger.md`` — the **only**
    ceiling-bearing artifact, each row carrying a non-empty ``claim_ceiling``
    and its ``n`` (AC-7).

`analysis/` imports run-dir artifacts only — no `cabt`, no `sim/`, no
`agents/runtime/`, no harness internals (the offline/runtime separation; SDD
§1.6). stdlib only (NFR-7).

CLI:  python analysis/aggregate.py runs/run-0001 [--ledger docs/ledger.md]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SUMMARY_COLUMNS = [
    "regime_id", "run_id", "agent_version", "opponent_id", "n_matches",
    "win_rate", "illegal_action_rate", "timeout_rate", "error_rate",
    "avg_turns", "avg_wall_clock_ms",
]

LEDGER_COLUMNS = [
    "date", "run_id", "regime_id", "git_rev", "sim_version", "agent_version",
    "opponent_pool_ref", "seed_set_ref", "games", "win_rate",
    "illegal_action_rate", "timeout_rate", "error_rate", "avg_turns", "mode",
    "hypothesis", "claim_ceiling", "notes",
]

LEDGER_PREAMBLE = """# Experiment Ledger (PR-8)

> **The only ceiling-bearing artifact.** One append-only row per run; each row
> carries a non-empty `claim_ceiling` and its sample size `n`/`games`. Per-match
> records and `summary.csv` carry NO ceiling. A `verdict` of better/worse may be
> written ONLY for a same-regime, agent-only comparison with a ceiling + n —
> never across regimes (NFR-5). Rows are append-only; never edit a past row.
"""


def _round(x, n=4):
    return round(x, n) if isinstance(x, (int, float)) else x


def aggregate_run(run_dir: Path) -> dict:
    """Compute aggregate stats from a run dir's match-summary records."""
    records = []
    for p in sorted((run_dir / "match_results").glob("*.json")):
        records.append(json.loads(p.read_text(encoding="utf-8")))
    n = len(records)
    if n == 0:
        raise ValueError(f"aggregate: no match_results in {run_dir}")

    wins = sum(1 for r in records if r.get("result") == "win")
    errors = sum(1 for r in records if r.get("result") == "error")
    # illegal-action rate counted only where detectable (else not a pass; SDD §5.4)
    detectable = [r for r in records if r.get("invalid_action_detectable")]
    illegal = sum(1 for r in detectable if (r.get("invalid_action_count") or 0) > 0)
    illegal_rate = (illegal / len(detectable)) if detectable else None
    timeouts = sum(1 for r in records if r.get("timeout") is True)
    turns = [r.get("turns") for r in records if isinstance(r.get("turns"), int)]
    walls = [r.get("wall_clock_ms") for r in records if isinstance(r.get("wall_clock_ms"), int)]

    return {
        "n_matches": n,
        "wins": wins,
        "errors": errors,
        "win_rate": _round(wins / n),
        "illegal_action_rate": _round(illegal_rate) if illegal_rate is not None else None,
        "timeout_rate": _round(timeouts / n),
        "error_rate": _round(errors / n),
        "avg_turns": _round(sum(turns) / len(turns), 2) if turns else None,
        "avg_wall_clock_ms": _round(sum(walls) / len(walls), 1) if walls else None,
        "agent_version": records[0].get("agent_version"),
        "opponent_id": records[0].get("opponent_id"),
        "regime_id": records[0].get("regime_id"),
        "run_id": records[0].get("run_id"),
    }


def write_summary_csv(run_dir: Path, stats: dict) -> Path:
    """Write summary.csv (AC-5). n_matches == per-match file count by construction."""
    out = run_dir / "summary.csv"
    row = {
        "regime_id": stats["regime_id"], "run_id": stats["run_id"],
        "agent_version": stats["agent_version"], "opponent_id": stats["opponent_id"],
        "n_matches": stats["n_matches"], "win_rate": stats["win_rate"],
        "illegal_action_rate": stats["illegal_action_rate"],
        "timeout_rate": stats["timeout_rate"], "error_rate": stats["error_rate"],
        "avg_turns": stats["avg_turns"], "avg_wall_clock_ms": stats["avg_wall_clock_ms"],
    }
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=SUMMARY_COLUMNS)
        w.writeheader()
        w.writerow(row)
    return out


def ledger_has_run(ledger_path: Path, run_id: str) -> bool:
    if not ledger_path.exists():
        return False
    text = ledger_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        cells = [c.strip() for c in line.split("|")]
        if len(cells) > 3 and cells[2] == run_id:  # run_id is column 2 (after leading empty cell)
            return True
    return False


def _esc(v) -> str:
    return str("" if v is None else v).replace("|", "\\|").replace("\n", " ")


def append_ledger_row(ledger_path: Path, fields: dict) -> bool:
    """Append exactly one row to docs/ledger.md (idempotent per run_id). Returns
    True if a row was appended, False if a row for this run already existed."""
    if not fields.get("claim_ceiling"):
        raise ValueError("append_ledger_row: claim_ceiling is required and must be non-empty (AC-7)")
    if ledger_has_run(ledger_path, fields.get("run_id", "")):
        return False
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    new = not ledger_path.exists()
    with open(ledger_path, "a", encoding="utf-8") as fh:
        if new:
            fh.write(LEDGER_PREAMBLE)
            fh.write("\n| " + " | ".join(LEDGER_COLUMNS) + " |\n")
            fh.write("|" + "|".join(["---"] * len(LEDGER_COLUMNS)) + "|\n")
        fh.write("| " + " | ".join(_esc(fields.get(c)) for c in LEDGER_COLUMNS) + " |\n")
    return True


def build_claim_ceiling(stats: dict, regime_id: str) -> str:
    """Pre-written, trivial, Rung-1 ceiling (legality/throughput only; SDD §3.7)."""
    return (
        f"measures legality/throughput of {stats['agent_version']} on {regime_id} "
        f"at n={stats['n_matches']}; NO strength claim — win rate here is not "
        f"evidence of quality (ladder Rung 1)."
    )


def aggregate_and_ledger(run_dir: Path, ledger_path: Path, *, git_rev: str,
                         sim_version: str, mode: str, opponent_pool_ref: str,
                         seed_set_ref: str, date: str,
                         hypothesis: str = "Loop produces honest evidence regardless of win rate (Sprint 00 goal).",
                         claim_ceiling: "str | None" = None,
                         notes: str = "") -> dict:
    """Write summary.csv and append one ledger row. Used by run_eval and the CLI."""
    stats = aggregate_run(run_dir)
    summary_path = write_summary_csv(run_dir, stats)
    ceiling = claim_ceiling or build_claim_ceiling(stats, stats["regime_id"])
    fields = {
        "date": date, "run_id": stats["run_id"], "regime_id": stats["regime_id"],
        "git_rev": git_rev, "sim_version": sim_version,
        "agent_version": stats["agent_version"],
        "opponent_pool_ref": opponent_pool_ref, "seed_set_ref": seed_set_ref,
        "games": stats["n_matches"], "win_rate": stats["win_rate"],
        "illegal_action_rate": stats["illegal_action_rate"],
        "timeout_rate": stats["timeout_rate"], "error_rate": stats["error_rate"],
        "avg_turns": stats["avg_turns"], "mode": mode,
        "hypothesis": hypothesis, "claim_ceiling": ceiling, "notes": notes,
    }
    appended = append_ledger_row(ledger_path, fields)
    return {"stats": stats, "summary_csv": str(summary_path),
            "ledger_appended": appended, "claim_ceiling": ceiling}


def _read_hashes(run_dir: Path) -> dict:
    kv = {}
    hp = run_dir / "hashes.txt"
    if hp.exists():
        for line in hp.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                kv[k.strip()] = v.strip()
    return kv


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Aggregate a run dir → summary.csv + ledger row.")
    ap.add_argument("run_dir")
    ap.add_argument("--ledger", default=str(REPO_ROOT / "docs" / "ledger.md"))
    args = ap.parse_args(argv)
    run_dir = Path(args.run_dir)

    man = {}
    mp = run_dir / "manifest.json"
    if mp.exists():
        man = json.loads(mp.read_text(encoding="utf-8"))
    kv = _read_hashes(run_dir)

    res = aggregate_and_ledger(
        run_dir, Path(args.ledger),
        git_rev=kv.get("git_rev", "unknown"),
        sim_version=kv.get("sim_version", man.get("sim_version", "unknown")),
        mode=man.get("mode", "unseeded"),
        opponent_pool_ref=man.get("opponent_pool_id", "opponent-pool-v001"),
        seed_set_ref=man.get("seed_set_id", "seed-set-v001"),
        date=(kv.get("timestamp", "")[:10] or man.get("created_at", "")[:10] or "unknown"),
        notes="mode=unseeded; timeout undetectable (soft gate); illegal-action gate hard (detectable).",
    )
    print(f"aggregate: summary.csv written; ledger_appended={res['ledger_appended']} "
          f"n={res['stats']['n_matches']} win_rate={res['stats']['win_rate']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
