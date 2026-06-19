#!/usr/bin/env python3
"""``tests/test_evidence_summary.py`` — the twelve required checks for
``analysis/evidence_summary.py`` (Cycle-004 C4-FR-4; SDD §9).

Stdlib plain-Python test module (``main()`` -> exit 0/1, mirroring
``tests/test_import_direction.py:82-93``). Uses **synthetic temp-dir fixtures
only** (OD-C4-4) — it does NOT depend on the gitignored local K-batch run dirs.

Run:  python tests/test_evidence_summary.py     (exit 0 ok / 1 failure)
stdlib only (NFR-5).
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

import evidence_summary as es          # the module under test (analysis/)
import hygiene_check                   # eval/ — parity target (tests may reference both)
import test_import_direction as tid    # tests/ — import-direction checker

_FAILURES: "list[str]" = []
_HEX64 = "a" * 64  # a valid SHA-256-shaped digest for fixtures


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}  {detail}")
        _FAILURES.append(name)


# --------------------------------------------------------------------------------------
# Synthetic fixtures — minimal manifest.json + match_results/*.json (the fields
# aggregate_run reads). No Competition Data, no card/deck/decision content.
# --------------------------------------------------------------------------------------

def make_run_dir(base: Path, run_id: str, regime_id: str, agent_id: str,
                 agent_version: str, n_matches: int = 4, *,
                 manifest_hash: str = _HEX64) -> Path:
    rd = base / run_id
    (rd / "match_results").mkdir(parents=True, exist_ok=True)
    man = {
        "run_id": run_id, "regime_id": regime_id, "agent_id": agent_id,
        "agent_version": agent_version, "mode": "unseeded",
        "agent_source_hash": manifest_hash,
        "expected_match_ids": [f"M{i:04d}" for i in range(1, n_matches + 1)],
    }
    (rd / "manifest.json").write_text(json.dumps(man), encoding="utf-8")
    for i in range(1, n_matches + 1):
        result = "win" if i % 2 == 0 else "loss"
        rec = {
            "run_id": run_id, "match_id": f"M{i:04d}", "regime_id": regime_id,
            "agent_id": agent_id, "agent_version": agent_version,
            "opponent_id": "random_legal", "result": result,
            "invalid_action_count": 0, "invalid_action_detectable": True,
            "timeout": None, "turns": 5, "wall_clock_ms": 6, "error": None,
        }
        (rd / "match_results" / f"M{i:04d}.json").write_text(
            json.dumps(rec), encoding="utf-8")
    return rd


def validate_file_exit(summary_obj, tmp: Path, name: str = "v.json") -> int:
    """Write a summary to disk and run the independent --validate path; return exit."""
    p = tmp / name
    p.write_text(json.dumps(summary_obj), encoding="utf-8")
    with contextlib.redirect_stderr(io.StringIO()):
        return es.main(["--validate", str(p)])


# --------------------------------------------------------------------------------------
# The twelve checks.
# --------------------------------------------------------------------------------------

def run_checks(tmp: Path) -> None:
    # one clean, generator-produced single-regime summary to poison per check
    a1 = make_run_dir(tmp, "run-a1", "regime-v002", "agentX", "agentX-v001")
    a2 = make_run_dir(tmp, "run-a2", "regime-v002", "agentX", "agentX-v001")
    a3 = make_run_dir(tmp, "run-a3", "regime-v002", "agentX", "agentX-v001")
    other = make_run_dir(tmp, "run-z1", "regime-v099", "agentZ", "agentZ-v001")
    good = es.build_summary([a1, a2, a3])

    # --- 1. Allow-list fail-closed ---
    poisoned = copy.deepcopy(good)
    poisoned["sneaky_field"] = 1
    v1 = es.validate_summary(poisoned)
    check("1 allow-list: unknown field rejected with reason",
          any(f == "sneaky_field" for f, _ in v1), str(v1))
    check("1 allow-list: exit 3 (never 0) on unknown field",
          validate_file_exit(poisoned, tmp) == 3)

    # --- 2. Forbidden-content rejection (one case each) -> exit 3 ---
    def reject_case(label, mutate, reason_substr):
        s = copy.deepcopy(good)
        mutate(s)
        v = es.validate_summary(s)
        has_reason = any(reason_substr.lower() in r.lower() for _, r in v)
        check(f"2 reject {label} (reason)", has_reason, str(v))
        check(f"2 reject {label} (exit 3)", validate_file_exit(s, tmp, "c2.json") == 3)

    reject_case("raw decision/body content",
                lambda s: s.update({"record_type": "decision"}),
                "per-decision body")
    reject_case("Competition-Data token/path",
                lambda s: s["agents"][0].update({"agent_id": "cg/leaked"}),
                "Competition-Data path")
    reject_case("Pokemon-Element token (non-digest hash)",
                lambda s: s["hashes"].update({"run-a1": "raw-element-stand-in"}),
                "Pokemon-Element")
    reject_case("inferential statistic",
                lambda s: s.update({"claim_ceiling": "p-value 0.03 indicates significance"}),
                "inferential statistic")
    reject_case("cross-regime field",
                lambda s: s.update({"regime_uplift": 0.3}),
                "cross-regime")
    reject_case("affirmative forbidden agent word",
                lambda s: s.update({"claim_ceiling": "POISON probe (asserted-rejected): strong"}),
                "forbidden agent word")

    # --- 3. Mixed-regime refusal -> exit 2 (generator AND validator) ---
    with contextlib.redirect_stderr(io.StringIO()):
        gen_rc = es.main([str(a1), str(other)])           # two different regimes
    check("3 generator mixed-regime -> exit 2", gen_rc == 2)
    mixed = copy.deepcopy(good)
    mixed["agents"][0]["regime_id"] = "regime-v099"        # a 2nd regime appears
    check("3 validator mixed-regime -> exit 2",
          validate_file_exit(mixed, tmp, "mixed.json") == 2)
    check("3 _collect_regime_ids finds both",
          es._collect_regime_ids(mixed) == {"regime-v002", "regime-v099"})

    # --- 4. No-sidecar-read (structural source property) ---
    src = (REPO_ROOT / "analysis" / "evidence_summary.py").read_text(encoding="utf-8")
    check("4 module source has no sidecar-dir token ('traces')", "traces" not in src)
    check("4 module source references no per-decision sidecar ('trace')",
          "trace" not in src.lower())

    # --- 5. Hygiene parity (superset of eval/hygiene_check.find_violations) ---
    probes = ["cg/x", "deck.csv", "a/cg.dll", "lib/libcg.so", "report.pdf",
              "grimoires/loa/context/secret", "runs/run-x/match_results/M1.json",
              "cards_master.csv", "x/__MACOSX/y", "safe/path.txt", "run-v002-b-1"]
    parity_ok = True
    for p in probes:
        hygiene_refuses = bool(hygiene_check.find_violations([p]))
        mine_refuses = es._hygiene_path_violation(p) is not None
        if hygiene_refuses and not mine_refuses:        # parity-or-stricter
            parity_ok = False
    check("5 hygiene path parity (every refused path also refused)", parity_ok)
    # superset: a content leak a path-gate cannot express is still caught
    content_leak = copy.deepcopy(good)
    content_leak["claim_ceiling"] = "variance estimate attached"
    check("5 validator is a superset (content check the path gate can't express)",
          bool(es.validate_summary(content_leak))
          and not hygiene_check.find_violations(["variance estimate attached"]))

    # --- 6. No-ledger-mutation after a full generate run ---
    ledger = REPO_ROOT / "docs" / "ledger.md"
    before = ledger.read_bytes() if ledger.exists() else None
    with contextlib.redirect_stderr(io.StringIO()):
        es.main([str(a1), str(a2), str(a3), "--out", str(tmp / "gen-out.json")])
    after = ledger.read_bytes() if ledger.exists() else None
    check("6 docs/ledger.md byte-unchanged after generate", before == after)
    # the generator refuses to write into docs/ or any ledger file (local-by-default)
    refused_docs = refused_ledger = False
    try:
        es._refuse_tracked_out(Path("docs/x.json"))
    except ValueError:
        refused_docs = True
    try:
        es._refuse_tracked_out(Path("a/b/ledger.md"))
    except ValueError:
        refused_ledger = True
    check("6 generator refuses --out under docs/", refused_docs)
    check("6 generator refuses --out to a ledger.md", refused_ledger)

    # --- 7. No-value-promotion: framing strings present; no ceiling of its own ---
    check("7 unseeded-process caveat present",
          "seed_controlled=false" in good["unseeded_caveat"])
    check("7 Rung-1 footer present; carries no ceiling of its own",
          "Rung 1" in good["claim_ceiling"]
          and "no ceiling of its own" in good["claim_ceiling"])
    check("7 footer makes NO gameplay-strength / NO inferential claim",
          "NO gameplay-strength claim" in good["claim_ceiling"]
          and "NO inferential claim" in good["claim_ceiling"])

    # --- 8. Benign 'hypothesis' exception: accept column context, reject test ---
    benign = copy.deepcopy(good)
    benign["claim_ceiling"] = (
        "provenance: cites the ledger 'hypothesis' text-field (docs/ledger.md:9); "
        "descriptive Rung 1; carries no ceiling of its own.")
    check("8 benign 'hypothesis' text-field context accepted",
          es.validate_summary(benign) == [], str(es.validate_summary(benign)))
    infer = copy.deepcopy(good)
    infer["claim_ceiling"] = "a hypothesis-test was run on the result"
    v8 = es.validate_summary(infer)
    check("8 inferential 'hypothesis-test' rejected",
          any("hypothesis-test" in r for _, r in v8), str(v8))

    # --- 9. Doc<->schema agreement: SAFE_FIELDS == doc 04 §2 field list (+ §4.1 containers) ---
    doc04_section2_fields = {
        # §2.1 identity / provenance / framing
        "regime_id", "n", "K", "agent_id", "agent_version", "run_ids",
        "hashes", "mode", "unseeded_caveat", "claim_ceiling",
        # §2.2 the seven descriptive statistics
        "count", "min", "max", "range", "mean", "median", "spread",
        # §2.3 the six dispersed metric names
        "win_rate", "illegal_action_rate", "timeout_rate", "error_rate",
        "avg_turns", "avg_wall_clock_ms",
        # §4.1 JSON-first structural containers
        "agents", "metrics",
    }
    check("9 SAFE_FIELDS equals doc 04 §2 field list",
          set(es.SAFE_FIELDS) == doc04_section2_fields,
          f"diff={set(es.SAFE_FIELDS) ^ doc04_section2_fields}")

    # --- 10. JSON-first round-trip: generated output validates clean (exit 0) ---
    rt_out = tmp / "round-trip.json"
    with contextlib.redirect_stderr(io.StringIO()):
        gen_rc = es.main([str(a1), str(a2), str(a3), "--out", str(rt_out)])
        val_rc = es.main(["--validate", str(rt_out)])
    check("10 generate exit 0", gen_rc == 0)
    check("10 round-trip --validate exit 0 (any markdown derived from JSON)", val_rc == 0)
    check("10 render_json is the primary parseable form",
          json.loads(es.render_json(good))["regime_id"] == "regime-v002")

    # --- 11. Sanitization smoke: poisoned input refused, never surfaced ---
    smoke = copy.deepcopy(good)
    smoke["agents"][0]["agent_id"] = "cg/PLANTEDSECRET.json"
    smoke_path = tmp / "smoke.json"
    smoke_path.write_text(json.dumps(smoke), encoding="utf-8")
    out_buf, err_buf = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
        smoke_rc = es.main(["--validate", str(smoke_path)])
    surfaced = "PLANTEDSECRET" in out_buf.getvalue() or "PLANTEDSECRET" in err_buf.getvalue()
    check("11 poisoned input refused (exit 3)", smoke_rc == 3)
    check("11 planted token never surfaced in any output", not surfaced)

    # --- 12. Import-direction / stdlib-only ---
    check("12 import-direction clean (analysis-only / stdlib-only)", tid.check() == [])
    top_imports = es_top_imports()
    third_party = top_imports - _STDLIB - {"aggregate", "dispersion_report"}
    check("12 no third-party / cross-zone import in evidence_summary.py",
          third_party == set(), f"unexpected={third_party}")


_STDLIB = {
    "__future__", "argparse", "json", "re", "sys", "pathlib",
    "statistics", "contextlib", "io", "copy", "tempfile",
}


def es_top_imports() -> "set[str]":
    """Top-level import names of analysis/evidence_summary.py (stdlib AST)."""
    import ast
    src = (REPO_ROOT / "analysis" / "evidence_summary.py").read_text(encoding="utf-8")
    names: "set[str]" = set()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split(".")[0])
    return names


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        run_checks(Path(td))
    if _FAILURES:
        print(f"\ntest_evidence_summary: {len(_FAILURES)} FAILURE(S): {_FAILURES}",
              file=sys.stderr)
        return 1
    print("\ntest_evidence_summary: OK — all 12 required checks pass", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
