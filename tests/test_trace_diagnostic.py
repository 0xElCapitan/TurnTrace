#!/usr/bin/env python3
"""``tests/test_trace_diagnostic.py`` — the S01 checks for
``analysis/trace_diagnostic.py`` (Cycle-008 S01; SDD §2, §7).

Stdlib plain-Python test module (``main()`` -> exit 0/1, mirroring
``tests/test_import_direction.py:82-93`` / ``tests/test_evidence_summary.py``).
Drives the **committed synthetic sealed-run fixtures** under
``tests/fixtures/diagnostic/`` — it does NOT depend on the gitignored local
``runs/`` dirs (C8-FR-1.5, R11).

Proves, against the synthetic fixtures:
  * all five §2.2 descriptive surfaces emit;
  * the generated output key-set (at every depth) is a subset of ``SAFE_FIELDS``;
  * no quality / score / recommendation / should-have / optimal-action key;
  * output keys are disjoint from the raw decision-body markers
    (``evidence_summary._DECISION_BODY_MARKERS``);
  * a mixed-regime fixture exits 2 before any aggregation;
  * import direction / stdlib-only stays green;
  * the fixtures are independent of any local gitignored run dir;
  * no new statistic enters (the stat surface is exactly ``STAT_COLUMNS``,
    via the reused ``descriptive_stats`` helper);
  * ``--out`` refuses a tracked ``docs/`` path.

Run:  python tests/test_trace_diagnostic.py     (exit 0 ok / 1 failure)
stdlib only (NFR-1).
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "analysis"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

import trace_diagnostic as td          # the module under test (analysis/)
import dispersion_report                # analysis/ — the reused stat-helper source
import evidence_summary as es           # analysis/ — _DECISION_BODY_MARKERS authority
import test_import_direction as tid     # tests/ — import-direction checker

FIX = REPO_ROOT / "tests" / "fixtures" / "diagnostic"
CLEAN_DIR = FIX / "clean" / "run-syn-a-01"
MIXED_A = FIX / "mixed" / "run-syn-a-01"
MIXED_B = FIX / "mixed" / "run-syn-b-01"

_FAILURES: "list[str]" = []

# Keys that would betray a quality/coaching/recommendation surface (must never appear).
_QUALITY_PATTERNS = (
    "quality", "score", "recommend", "should", "optimal", "best", "worse",
    "better", "mistake", "blunder", "rating", "grade", "coach", "advice",
    "advise", "suggest", "lethal", "missed", "wasted", "judge", "judgment",
)


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}  {detail}")
        _FAILURES.append(name)


def _all_keys(node, acc: set) -> set:
    """Every dict key appearing anywhere in the object, at every nesting depth."""
    if isinstance(node, dict):
        for k, v in node.items():
            acc.add(k)
            _all_keys(v, acc)
    elif isinstance(node, list):
        for v in node:
            _all_keys(v, acc)
    return acc


def _quality_hit(key: str) -> "str | None":
    low = str(key).lower()
    for pat in _QUALITY_PATTERNS:
        if pat in low:
            return pat
    return None


# --------------------------------------------------------------------------------------
# The checks
# --------------------------------------------------------------------------------------

def t_five_surfaces(diag: dict) -> None:
    """All five §2.2 descriptive surfaces emit from the synthetic fixture."""
    # surface 1 — outcome / ending-cause aggregates
    check("surface1.outcome_counts present",
          set(diag.get("outcome_counts", {})) == {"win", "loss", "draw", "error"})
    check("surface1.ending_cause_counts present",
          {"prize-out", "deck-out", "no-active", "card-effect", "error", "<unmapped>"}
          == set(diag.get("ending_cause_counts", {})))
    check("surface1.outcome_counts sum == n_matches",
          sum(diag["outcome_counts"].values()) == diag["n_matches"])
    # surface 2 — board-shape distributions
    check("surface2.bench_count_stats per side",
          set(diag.get("bench_count_stats", {})) == {"p0", "p1"})
    check("surface2.active_present_rate per side",
          set(diag.get("active_present_rate", {})) == {"p0", "p1"})
    # surface 3 — prize trajectory
    check("surface3.prize_trajectory_stats per side",
          set(diag.get("prize_trajectory_stats", {})) == {"p0", "p1"})
    check("surface3.final_prize_counts_by_side per side",
          set(diag.get("final_prize_counts_by_side", {})) == {"p0", "p1"})
    # surface 4 — latency / throughput
    check("surface4.latency_ms_stats has the seven stats",
          set(diag.get("latency_ms_stats", {})) == set(td.STAT_COLUMNS))
    check("surface4.wall_clock_ms_stats has the seven stats",
          set(diag.get("wall_clock_ms_stats", {})) == set(td.STAT_COLUMNS))
    # surface 5 — error / illegal / timeout
    check("surface5.error_presence_count is an int",
          isinstance(diag.get("error_presence_count"), int))
    check("surface5.illegal_action_total is an int",
          isinstance(diag.get("illegal_action_total"), int))
    check("surface5.timeout reported as null (soft signal)",
          "timeout" in diag and diag["timeout"] is None)


def t_keyset_subset_safe_fields(diag: dict) -> None:
    keys = _all_keys(diag, set())
    extra = keys - set(td.SAFE_FIELDS)
    check("output key-set subset of SAFE_FIELDS (every depth)", not extra,
          f"keys outside allow-list: {sorted(extra)}")


def t_no_quality_keys(diag: dict) -> None:
    keys = _all_keys(diag, set())
    hits = {k: _quality_hit(k) for k in keys if _quality_hit(k)}
    check("no quality/score/recommendation key in output", not hits, f"offenders: {hits}")
    # defense in depth: the allow-list itself carries no quality-shaped key.
    sf_hits = {k: _quality_hit(k) for k in td.SAFE_FIELDS if _quality_hit(k)}
    check("SAFE_FIELDS carries no quality-shaped key", not sf_hits, f"offenders: {sf_hits}")


def t_marker_disjoint(diag: dict) -> None:
    keys = _all_keys(diag, set())
    markers = es._DECISION_BODY_MARKERS
    overlap = keys & set(markers)
    check("output keys disjoint from _DECISION_BODY_MARKERS", not overlap,
          f"raw decision-body markers leaked as keys: {sorted(overlap)}")
    # the raw marker names the diagnostic READS internally must be absent as output keys.
    for raw in ("decision_latency_ms", "public_state_summary", "private_state_summary",
                "selected_action", "legal_actions_sample", "post_decision_observation"):
        check(f"raw marker '{raw}' not an output key", raw not in keys)
    # SAFE_FIELDS itself is disjoint from the marker set (single source of truth is clean).
    check("SAFE_FIELDS disjoint from _DECISION_BODY_MARKERS",
          not (set(td.SAFE_FIELDS) & set(markers)))


def t_mixed_regime_exit2() -> None:
    raised = False
    try:
        td.build_diagnostic([MIXED_A, MIXED_B])
    except td.MixedRegimeRefusal:
        raised = True
    check("mixed-regime build_diagnostic raises MixedRegimeRefusal", raised)
    with contextlib.redirect_stderr(io.StringIO()):
        rc = td.main([str(MIXED_A), str(MIXED_B)])
    check("mixed-regime CLI exits 2", rc == 2, f"got exit {rc}")


def t_import_direction() -> None:
    violations = tid.check()
    check("import-direction green (whole repo)", violations == [], f"{violations}")
    td_viol = [v for v in violations if "trace_diagnostic" in v]
    check("trace_diagnostic has no import-direction violation", not td_viol, f"{td_viol}")
    # precise (AST) stdlib-only / intra-analysis check — every zoned import is analysis-zone;
    # no sim / cabt / eval / agents.runtime. (Prose-grep would false-match doc citations.)
    imports = tid._top_imports(Path(td.__file__))
    zone_map = tid._module_zone_map()
    cross = sorted(n for n in imports if zone_map.get(n) not in (None, "analysis"))
    check("trace_diagnostic imports only stdlib + analysis-zone", not cross,
          f"cross-zone imports: {cross}")


def t_fixture_independence(diag: dict) -> None:
    # the fixture is committed under tests/, NOT under the gitignored runs/ tree.
    check("fixture lives under tests/fixtures", "fixtures" in CLEAN_DIR.parts
          and "tests" in CLEAN_DIR.parts)
    check("fixture is not under runs/", "runs" not in CLEAN_DIR.parts)
    # it produced a real diagnostic without any local run dir being present.
    check("diagnostic built from committed fixture", diag.get("n_matches", 0) > 0
          and diag.get("n_decisions", 0) > 0)
    check("regime read from the fixture manifest", diag.get("regime_id") == "regime-syn-a")


def t_no_new_statistic(diag: dict) -> None:
    # the reused helper IS dispersion_report's — not a re-implementation.
    check("descriptive_stats is the reused dispersion_report helper",
          td.descriptive_stats is dispersion_report.descriptive_stats)
    check("STAT_COLUMNS is the reused dispersion_report surface",
          td.STAT_COLUMNS == dispersion_report.STAT_COLUMNS)
    check("STAT_COLUMNS is exactly the seven descriptive stats",
          set(td.STAT_COLUMNS) == {"count", "min", "max", "range", "mean", "median", "spread"})
    # every emitted stats object uses EXACTLY those seven keys — no new statistic.
    stat_dicts = [
        diag["latency_ms_stats"], diag["wall_clock_ms_stats"],
        diag["bench_count_stats"]["p0"], diag["bench_count_stats"]["p1"],
        diag["prize_trajectory_stats"]["p0"], diag["prize_trajectory_stats"]["p1"],
        diag["final_prize_counts_by_side"]["p0"], diag["final_prize_counts_by_side"]["p1"],
    ]
    ok = all(set(sd.keys()) == set(td.STAT_COLUMNS) for sd in stat_dicts)
    check("every stats object uses exactly STAT_COLUMNS", ok)
    # structural: all stats delegate to the reused helper — the generator imports no
    # `statistics` module of its own, so no std-dev/variance/CI/p-value can be computed here.
    check("generator does not import statistics directly (delegates to reused helper)",
          "statistics" not in tid._top_imports(Path(td.__file__)))


def t_out_refuses_tracked_docs() -> None:
    def refused(p) -> bool:
        try:
            td._refuse_tracked_out(Path(p))
            return False
        except ValueError:
            return True
    check("--out refuses relative docs/ path", refused("docs/diag.json"))
    check("--out refuses absolute repo docs/ path", refused(REPO_ROOT / "docs" / "diag.json"))
    check("--out refuses a ledger.md basename", refused("ledger.md"))
    # a genuinely-local path is accepted (no raise).
    local_ok = True
    try:
        with tempfile.TemporaryDirectory() as d:
            td._refuse_tracked_out(Path(d) / "diag.json")
    except ValueError:
        local_ok = False
    check("--out accepts a local/gitignored path", local_ok)


def t_json_roundtrip(diag: dict) -> None:
    text = td.render_json(diag)
    check("render_json is sorted, deterministic, round-trips",
          json.loads(text) == diag and text == td.render_json(diag))


def main() -> int:
    try:  # robust output regardless of console codepage (Windows cp1252)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    print("test_trace_diagnostic:")
    diag = td.build_diagnostic([CLEAN_DIR])
    t_five_surfaces(diag)
    t_keyset_subset_safe_fields(diag)
    t_no_quality_keys(diag)
    t_marker_disjoint(diag)
    t_mixed_regime_exit2()
    t_import_direction()
    t_fixture_independence(diag)
    t_no_new_statistic(diag)
    t_out_refuses_tracked_docs()
    t_json_roundtrip(diag)

    if _FAILURES:
        print(f"\nFAILED ({len(_FAILURES)}): {', '.join(_FAILURES)}", file=sys.stderr)
        return 1
    print("\nall trace_diagnostic checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
