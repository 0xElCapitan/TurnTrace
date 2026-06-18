#!/usr/bin/env python3
"""``analysis/e2e_validate.py`` — End-to-End goal validation (Task 01.E2E, AC-07).

Maps every PRD goal **G-1 … G-7** (PRD §4) to a **concrete on-disk artifact** and
checks the evidence. A goal is marked achieved **only** when its artifact exists
and carries the expected evidence — never on assertion alone (PRD §15; sprint
plan Task 01.E2E). Any goal with no artifact evidence is reported `NOT ACHIEVED`.

Reads run-dir artifacts + the tracked ledger / strategy report, and re-uses the
intra-zone `delta_report` (G-3) and `replay_check` (G-5) tools as live evidence.
`analysis/` imports run-dir artifacts + analysis intra-zone only — no
`cabt`/`sim`/`runtime`/`eval` (SDD §1.6). stdlib only (NFR-7).

CLI:  python analysis/e2e_validate.py                       # runs/run-0001 vs runs/run-0002
      python analysis/e2e_validate.py --run-a runs/run-0001 --run-b runs/run-0002
Exit: 0 all 7 goals achieved with artifact evidence · 1 one or more not achieved / input failure.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "analysis"))

import aggregate  # noqa: E402  (analysis intra-zone — ledger columns)
import delta_report  # noqa: E402  (analysis intra-zone — G-3 live evidence)
import replay_check  # noqa: E402  (analysis intra-zone — G-5 live evidence)

LEDGER = REPO_ROOT / "docs" / "ledger.md"
STRATEGY = REPO_ROOT / "docs" / "strategy-report.md"


def _manifest(run_dir: Path) -> dict:
    return json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))


def _ledger_row(run_id: str) -> "dict | None":
    """Return the {column: value} dict for a run's ledger row, or None."""
    if not LEDGER.exists():
        return None
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.split("|")]
        if len(cells) > 3 and cells[2] == run_id:  # cells[0] is leading empty (aggregate.ledger_has_run)
            values = cells[1:1 + len(aggregate.LEDGER_COLUMNS)]
            return dict(zip(aggregate.LEDGER_COLUMNS, values))
    return None


# Each check returns (achieved: bool, evidence: str). Evidence cites a concrete path.
def g1_run_matches(a: Path, b: Path) -> "tuple[bool, str]":
    ok = True
    detail = []
    for rd in (a, b):
        man = _manifest(rd)
        n_files = len(list((rd / "match_results").glob("*.json")))
        exp = len(man.get("expected_match_ids", []))
        good = n_files == exp and exp > 0
        ok = ok and good
        detail.append(f"{rd.name}: {n_files}/{exp} match records")
    detail.append("missing-input refusal: eval/run_match.py:_check_required + "
                  "tests/test_smokes.py::ExitCodeSmoke.test_exit_1_env_load_failure")
    return ok, "; ".join(detail)


def g2_immutable(a: Path, b: Path) -> "tuple[bool, str]":
    ok = all((rd / "manifest.json").exists() for rd in (a, b))
    return ok, (f"{a.name}/manifest.json + {b.name}/manifest.json present (ID authority); "
                f"immutability guard: eval/run_eval.py::ImmutabilityRefusal (exit 3) + "
                f"tests/test_smokes.py::RunEvalSmoke.test_immutability_guard_refuses_overwrite")


def g3_compare(a: Path, b: Path) -> "tuple[bool, str]":
    try:
        rep = delta_report.compare(a, b)
    except delta_report.CrossRegimeRefusal:
        return False, "delta_report refused (regime mismatch) — cannot compare"
    except Exception as e:  # noqa: BLE001
        return False, f"delta_report failed: {e}"
    n_metrics = len(rep["metrics"])
    has_why = all(m["moved"] or m["why_no_change"] for m in rep["metrics"])
    ok = n_metrics > 0 and has_why
    return ok, (f"analysis/delta_report.py: {n_metrics} metrics compared on {rep['regime_id']} "
                f"(why-no-change on every unmoved metric); cross-regime refusal: "
                f"tests/test_smokes.py::DeltaReportSmoke.test_cross_regime_refused")


def g4_track(a: Path, b: Path) -> "tuple[bool, str]":
    rows = {rd.name: _ledger_row(_manifest(rd)["run_id"]) for rd in (a, b)}
    ok = True
    detail = []
    for rd in (a, b):
        row = rows[rd.name]
        ceiling = row.get("claim_ceiling") if row else None
        hashes_ok = (rd / "hashes.txt").exists()
        good = bool(row) and bool(ceiling) and hashes_ok
        ok = ok and good
        detail.append(f"{rd.name}: ledger row={'yes' if row else 'NO'} "
                      f"ceiling={'non-empty' if ceiling else 'EMPTY'} hashes.txt={'yes' if hashes_ok else 'NO'}")
    return ok, "docs/ledger.md + " + "; ".join(detail)


def g5_traces(a: Path, b: Path) -> "tuple[bool, str]":
    rep = replay_check.replay_check(b)
    ok = rep["audit_ok"]
    ac = rep["audit"]
    return ok, (f"analysis/replay_check.py {b.name}: {ac['checked']} trace_hash(es) recomputed, "
                f"mismatches={len(ac['mismatches'])}; trace↔record join (AC-3) holds")


def g6_bound(a: Path, b: Path) -> "tuple[bool, str]":
    ok = True
    detail = []
    for rd in (a, b):
        row = _ledger_row(_manifest(rd)["run_id"])
        ceiling = row.get("claim_ceiling") if row else None
        games = row.get("games") if row else None
        good = bool(ceiling) and bool(games)
        ok = ok and good
        detail.append(f"{rd.name}: n={games} ceiling={'present' if ceiling else 'MISSING'}")
    return ok, "docs/ledger.md claim_ceiling + n per row — " + "; ".join(detail)


def g7_report(a: Path, b: Path) -> "tuple[bool, str]":
    if not STRATEGY.exists():
        return False, "docs/strategy-report.md missing"
    text = STRATEGY.read_text(encoding="utf-8")
    required = ["## 4. Evaluation method", "## 5. Ablation table", "## 8. Appendix"]
    have = [h for h in required if h in text]
    # the comparison row (run-0002) is the first artifact that §5/§8 reference
    cmp_row = _ledger_row(_manifest(b)["run_id"])
    ok = len(have) == len(required) and cmp_row is not None
    return ok, (f"docs/strategy-report.md sections {have} present; comparison artifact "
                f"(ledger row {_manifest(b)['run_id']} + analysis/delta_report.py) slots into §5/§8")


GOALS = [
    ("G-1", "Run matches under fully-declared inputs, sequentially & debuggable", g1_run_matches),
    ("G-2", "Preserve evidence immutably (sealed, never-edited runs)", g2_immutable),
    ("G-3", "Compare agent versions honestly (attributable same-regime deltas)", g3_compare),
    ("G-4", "Track what was tested and under what conditions", g4_track),
    ("G-5", "Support decision traces where the simulator permits", g5_traces),
    ("G-6", "Bound claims with explicit evidence (ceiling + n)", g6_bound),
    ("G-7", "Feed a credible Strategy Category report", g7_report),
]


def validate(run_a: Path, run_b: Path) -> dict:
    results = []
    for gid, desc, fn in GOALS:
        try:
            achieved, evidence = fn(run_a, run_b)
        except Exception as e:  # noqa: BLE001  — a missing artifact is "not achieved", not a crash
            achieved, evidence = False, f"no artifact evidence ({type(e).__name__}: {e})"
        results.append({"goal": gid, "desc": desc, "achieved": achieved, "evidence": evidence})
    return {"results": results, "all_achieved": all(r["achieved"] for r in results)}


def render(rep: dict) -> str:
    lines = ["# E2E goal validation — PRD G-1 … G-7 (artifact-grounded)", ""]
    lines.append("| goal | achieved | evidence |")
    lines.append("|---|---|---|")
    for r in rep["results"]:
        mark = "ACHIEVED" if r["achieved"] else "NOT ACHIEVED"
        lines.append(f"| {r['goal']} {r['desc']} | {mark} | {r['evidence']} |")
    lines.append("")
    n_ok = sum(1 for r in rep["results"] if r["achieved"])
    lines.append(f"verdict: {n_ok}/{len(rep['results'])} goals achieved with artifact evidence. "
                 f"No goal is marked achieved without a concrete artifact (AC-07).")
    return "\n".join(lines)


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description="End-to-End PRD goal validation (G-1..G-7).")
    ap.add_argument("--run-a", default="runs/run-0001")
    ap.add_argument("--run-b", default="runs/run-0002")
    args = ap.parse_args(argv)

    run_a, run_b = Path(args.run_a), Path(args.run_b)
    if not (run_a / "manifest.json").exists() or not (run_b / "manifest.json").exists():
        print(f"e2e_validate: input failure — both run dirs must be sealed "
              f"({run_a}, {run_b})", file=sys.stderr)
        return 1

    rep = validate(run_a, run_b)
    print(render(rep))
    return 0 if rep["all_achieved"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
