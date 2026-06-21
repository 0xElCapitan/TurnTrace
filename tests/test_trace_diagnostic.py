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

S02 — the co-located fail-closed sanitizer (``validate_diagnostic`` + ``--validate``):
  * the clean S01 diagnostic output passes its own sanitizer (RN-2; exit 0);
  * every rejection class fails closed (exit 3): unknown key · raw decision-body
    marker key · quality/scoring/recommendation/coaching key · inferential term ·
    affirmative forbidden agent word · cross-regime field/value · non-SHA-256 hash
    (card-identity) · Competition-Data path · numeric-`M`/comparison-budget ·
    Rung-3 governance · externally-sourced raw content;
  * the ``0/1/2/3`` exit contract (1 input failure · 2 mixed-regime · 3 leak);
  * ``SAFE_FIELDS`` is the single source of truth (the validator's allow-list);
  * path-rule parity-or-stricter vs ``eval/hygiene_check.find_violations`` and
    decision-body-marker parity vs ``evidence_summary._DECISION_BODY_MARKERS``;
  * the committed poisoned fixtures live under ``tests/fixtures/diagnostic/poisoned/``
    only, are independent of the gitignored ``runs/`` tree, and each fixture path is
    itself Competition-Data hygiene-clean.

Run:  python tests/test_trace_diagnostic.py     (exit 0 ok / 1 failure)
stdlib only (NFR-1).
"""

from __future__ import annotations

import contextlib
import copy
import io
import json
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "analysis"))
sys.path.insert(0, str(REPO_ROOT / "eval"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

import trace_diagnostic as td          # the module under test (analysis/)
import dispersion_report                # analysis/ — the reused stat-helper source
import evidence_summary as es           # analysis/ — _DECISION_BODY_MARKERS authority
import hygiene_check                     # eval/ — path-rule parity target (tests may use both)
import test_import_direction as tid     # tests/ — import-direction checker

FIX = REPO_ROOT / "tests" / "fixtures" / "diagnostic"
CLEAN_DIR = FIX / "clean" / "run-syn-a-01"
MIXED_A = FIX / "mixed" / "run-syn-a-01"
MIXED_B = FIX / "mixed" / "run-syn-b-01"
POISONED = FIX / "poisoned"

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


# ======================================================================================
# S02 — the co-located fail-closed sanitizer (validate_diagnostic + --validate).
# ======================================================================================

# (fixture filename, expected --validate exit, a reason substring that must appear)
_POISON_EXPECT = [
    ("unknown_key.json", 3, "outside the safe allow-list"),
    ("decision_marker.json", 3, "raw per-decision body"),
    ("quality_key.json", 3, "quality / scoring"),
    ("inferential_value.json", 3, "inferential statistic"),
    ("forbidden_word.json", 3, "forbidden agent word"),
    ("crossregime_key.json", 3, "cross-regime"),
    ("nonsha_hash.json", 3, "SHA-256 digest"),
    ("hygiene_path.json", 3, "Competition-Data path"),
    ("numeric_m.json", 3, "numeric-M-shaped governance threshold"),
    ("governance_rung3.json", 3, "Rung-3 / promotion-governance"),
    ("raw_external_content.json", 3, "externally-sourced raw content"),
]


def _validate_obj_exit(obj, tmp: Path, name: str = "v.json") -> int:
    """Write a diagnostic object to disk and run the independent --validate path."""
    p = tmp / name
    p.write_text(json.dumps(obj), encoding="utf-8")
    with contextlib.redirect_stderr(io.StringIO()):
        return td.main(["--validate", str(p)])


def _reject(diag: dict, mutate, reason_substr: str, label: str, tmp: Path) -> None:
    """A clean diagnostic + one injected poison -> a (field, reason) match + exit 3."""
    s = copy.deepcopy(diag)
    mutate(s)
    v = td.validate_diagnostic(s)
    check(f"reject {label} (reason '{reason_substr}')",
          any(reason_substr.lower() in r.lower() for _, r in v), str(v)[:240])
    check(f"reject {label} (exit 3, fail-closed)",
          _validate_obj_exit(s, tmp, "reject.json") == 3)


def t_s02_clean_validates(diag: dict, tmp: Path) -> None:
    # RN-2: the diagnostic's own legitimate output (safe aggregate keys) passes its
    # own co-located sanitizer — proving the safe-key discipline holds end to end.
    v = td.validate_diagnostic(diag)
    check("S02 clean S01 diagnostic validates (no violations)", v == [], str(v)[:240])
    out = tmp / "clean-diag.json"
    with contextlib.redirect_stderr(io.StringIO()):
        gen_rc = td.main([str(CLEAN_DIR), "--out", str(out)])
        val_rc = td.main(["--validate", str(out)])
    check("S02 generate clean diagnostic exit 0", gen_rc == 0, f"got {gen_rc}")
    check("S02 --validate clean diagnostic exit 0 (C8-FR-3.3)", val_rc == 0, f"got {val_rc}")


def t_s02_reject_classes(diag: dict, tmp: Path) -> None:
    # raw decision-body markers as output keys (raw rows + public/private state)
    for marker in ("decision_latency_ms", "public_state_summary", "private_state_summary",
                   "selected_action", "legal_actions_sample", "record_type", "decision_rows"):
        _reject(diag, lambda s, m=marker: s.update({m: "x"}),
                "raw per-decision body", f"decision marker '{marker}'", tmp)
    # quality / scoring / recommendation / should-have / optimal-action / coaching / policy
    for qk in ("decision_quality_score", "recommended_action", "should_have_played",
               "optimal_action", "coaching_note", "policy_improvement", "blunder_rate"):
        _reject(diag, lambda s, k=qk: s.update({k: 1}),
                "quality / scoring", f"quality key '{qk}'", tmp)
    # inferential vocabulary in a value
    _reject(diag, lambda s: s.update({"claim_ceiling": "a hypothesis-test gave p-value 0.01"}),
            "inferential statistic", "inferential value", tmp)
    # affirmative forbidden agent word in a value
    _reject(diag, lambda s: s.update({"claim_ceiling": "the agent is optimal"}),
            "forbidden agent word", "affirmative forbidden word", tmp)
    # cross-regime: a field name AND a value connective
    _reject(diag, lambda s: s.update({"regime_uplift": 0.2}), "cross-regime", "cross-regime key", tmp)
    _reject(diag, lambda s: s.update({"mode": "regime-v001 vs regime-v002"}),
            "cross-regime", "cross-regime value", tmp)
    # card-identity / non-SHA-256 hash (Pokemon-Element leak vector)
    _reject(diag, lambda s: s.update({"hashes": {"r": "raw-token-not-a-digest"}}),
            "SHA-256 digest", "non-digest hash", tmp)
    # Competition-Data path values (bare paths; the anchored hygiene rules)
    _reject(diag, lambda s: s.update({"mode": "cg/leaked.dll"}), "Competition-Data path", "cg/ path", tmp)
    _reject(diag, lambda s: s.update({"mode": "deck.csv"}), "Competition-Data path", "deck.csv path", tmp)
    _reject(diag, lambda s: s.update({"mode": "rulebook.pdf"}), "Competition-Data path", "pdf path", tmp)
    # numeric-`M` / comparison-budget — key (with numeric value) AND value form (the NEW class)
    _reject(diag, lambda s: s.update({"M": 0.05}), "numeric-M", "bare 'M' key", tmp)
    _reject(diag, lambda s: s.update({"comparison_budget": 20}), "numeric-M", "comparison_budget key", tmp)
    _reject(diag, lambda s: s.update({"claim_ceiling": "promotion margin M=0.05"}),
            "numeric-M", "numeric-M value", tmp)
    # Rung-3 / promotion-governance semantics — key AND value
    _reject(diag, lambda s: s.update({"rung3_candidate": "x"}), "Rung-3", "rung3 key", tmp)
    _reject(diag, lambda s: s.update({"claim_ceiling": "advancing to Rung 3 via SP-6 candidate"}),
            "Rung-3", "rung3 value", tmp)
    # externally-sourced raw content (Discord / Kaggle / Daily-Top-Episode / sim log)
    _reject(diag, lambda s: s.update({"mode": "discord screenshot"}),
            "externally-sourced raw content", "discord value", tmp)
    _reject(diag, lambda s: s.update({"mode": "kaggle daily-top-episode"}),
            "externally-sourced raw content", "kaggle value", tmp)
    _reject(diag, lambda s: s.update({"mode": "raw simulator log dump"}),
            "externally-sourced raw content", "simulator-log value", tmp)


def t_s02_exit_contract(diag: dict, tmp: Path) -> None:
    # exit 1 — a missing / unreadable file
    with contextlib.redirect_stderr(io.StringIO()):
        rc1 = td.main(["--validate", str(tmp / "does-not-exist.json")])
    check("S02 --validate missing file -> exit 1", rc1 == 1, f"got {rc1}")
    # exit 2 — a diagnostic carrying two regime_ids (mixed-regime refusal, before leak check)
    two_regime = tmp / "two-regime.json"
    two_regime.write_text(json.dumps(
        {"regime_id": "regime-syn-a", "nested": {"regime_id": "regime-syn-b"}}), encoding="utf-8")
    with contextlib.redirect_stderr(io.StringIO()):
        rc2 = td.main(["--validate", str(two_regime)])
    check("S02 --validate multi-regime -> exit 2 (precedes leak check)", rc2 == 2, f"got {rc2}")
    check("S02 _collect_regime_ids finds both regimes",
          td._collect_regime_ids({"regime_id": "a", "x": {"regime_id": "b"}}) == {"a", "b"})
    # exit 3 — a poisoned file; exit 0 is asserted in t_s02_clean_validates
    with contextlib.redirect_stderr(io.StringIO()):
        rc3 = td.main(["--validate", str(POISONED / "unknown_key.json")])
    check("S02 --validate poisoned -> exit 3", rc3 == 3, f"got {rc3}")
    # the validator rejects a non-dict root, fail-closed
    check("S02 non-dict root rejected", td.validate_diagnostic([1, 2]) != [])


def t_s02_safe_fields_source_of_truth(diag: dict) -> None:
    # every key the generator emits is within SAFE_FIELDS -> the clean output validates.
    keys = _all_keys(diag, set())
    check("S02 generator output keys all within SAFE_FIELDS",
          keys <= set(td.SAFE_FIELDS), f"outside={sorted(keys - set(td.SAFE_FIELDS))}")
    # membership in SAFE_FIELDS is literally the allow-list gate: a safe key validates
    # clean, a non-safe key fails — and a near-miss of an allowed key is rejected.
    check("S02 a SAFE_FIELDS key validates clean; a non-safe key fails",
          td.validate_diagnostic({"regime_id": "r"}) == []
          and bool(td.validate_diagnostic({"not_a_safe_field": 1})))
    near = copy.deepcopy(diag)
    near["regime_idx"] = "x"   # one char off the allow-listed 'regime_id'
    check("S02 near-miss key outside SAFE_FIELDS rejected",
          any(f == "regime_idx" for f, _ in td.validate_diagnostic(near)))


def t_s02_hygiene_parity(diag: dict) -> None:
    probes = ["cg/x", "deck.csv", "a/cg.dll", "lib/libcg.so", "report.pdf",
              "grimoires/loa/context/secret", "runs/run-x/match_results/M1.json",
              "cards_master.csv", "x/__MACOSX/y", "safe/path.txt", "run-v002-b-1"]
    parity_ok = all(td._hygiene_path_violation(p) is not None
                    for p in probes if hygiene_check.find_violations([p]))
    check("S02 hygiene path parity (every hygiene-refused path also refused here)", parity_ok)
    # superset: a content leak a path gate cannot express is still caught by the validator.
    leak = copy.deepcopy(diag)
    leak["claim_ceiling"] = "variance estimate attached"
    check("S02 validator is a superset (content the path gate can't express)",
          bool(td.validate_diagnostic(leak))
          and not hygiene_check.find_violations(["variance estimate attached"]))


def t_s02_marker_parity() -> None:
    # the copied marker set agrees with the evidence_summary authority (no drift).
    check("S02 decision-body markers parity vs evidence_summary (no drift)",
          set(td._DECISION_BODY_MARKERS) == set(es._DECISION_BODY_MARKERS),
          f"diff={set(td._DECISION_BODY_MARKERS) ^ set(es._DECISION_BODY_MARKERS)}")


def t_s02_poisoned_fixtures() -> None:
    for fname, want_exit, want_reason in _POISON_EXPECT:
        fp = POISONED / fname
        check(f"S02 poisoned fixture present: {fname}", fp.is_file())
        if not fp.is_file():
            continue
        obj = json.loads(fp.read_text(encoding="utf-8"))
        v = td.validate_diagnostic(obj)
        check(f"S02 poisoned {fname}: reason '{want_reason}'",
              any(want_reason.lower() in r.lower() for _, r in v), str(v)[:240])
        with contextlib.redirect_stderr(io.StringIO()):
            rc = td.main(["--validate", str(fp)])
        check(f"S02 poisoned {fname}: --validate exit {want_exit}", rc == want_exit, f"got {rc}")
        # the fixture lives under tests/, NEVER the gitignored runs/ tree (R11)
        check(f"S02 poisoned {fname}: under tests/, not runs/",
              "tests" in fp.parts and "runs" not in fp.parts)
        # per-file hygiene coverage: the fixture PATH itself is Competition-Data-clean
        rel = fp.relative_to(REPO_ROOT).as_posix()
        check(f"S02 poisoned {fname}: fixture path hygiene-clean",
              hygiene_check.find_violations([rel]) == [], rel)
    # all poisoned fixtures committed under the intended subtree only
    present = sorted(p.name for p in POISONED.glob("*.json"))
    check("S02 poisoned fixtures committed under tests/fixtures/diagnostic/poisoned/",
          present == sorted(n for n, _, _ in _POISON_EXPECT), str(present))


def t_s02_runs_independence() -> None:
    # the entire S02 validation surface is driven from tests/ fixtures + generated temp
    # files; nothing reads the gitignored runs/ tree.
    check("S02 poisoned subtree is under tests/, not runs/",
          "tests" in POISONED.parts and "runs" not in POISONED.parts)


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

    # ---- S02 — co-located fail-closed sanitizer ----
    print("test_trace_diagnostic (S02 sanitizer):")
    with tempfile.TemporaryDirectory() as _td:
        tmp = Path(_td)
        t_s02_clean_validates(diag, tmp)
        t_s02_reject_classes(diag, tmp)
        t_s02_exit_contract(diag, tmp)
    t_s02_safe_fields_source_of_truth(diag)
    t_s02_hygiene_parity(diag)
    t_s02_marker_parity()
    t_s02_poisoned_fixtures()
    t_s02_runs_independence()

    if _FAILURES:
        print(f"\nFAILED ({len(_FAILURES)}): {', '.join(_FAILURES)}", file=sys.stderr)
        return 1
    print("\nall trace_diagnostic checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
