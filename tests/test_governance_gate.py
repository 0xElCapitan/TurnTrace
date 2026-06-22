#!/usr/bin/env python3
"""``tests/test_governance_gate.py`` — the SP-A checks for
``analysis/governance_gate.py`` (Cycle-009 SP-A; PRD C9-FR-1/2/3; SDD §3–§7, §10).

Stdlib plain-Python test module (``main()`` -> exit 0/1, mirroring
``tests/test_ledger_validate.py`` / ``tests/test_import_direction.py``), so the
module is itself gate-child-eligible (``raise SystemExit(main())``). It is offline,
stdlib-only, and injects failures via **synthetic throwaway child scripts** in a
tempdir (each ``sys.exit(N)``) — it never mutates a real child validator/test to
force a failure.

Covers TG1–TG10:
  * TG1  a synthetic child exiting 1/2/3 makes the aggregate non-zero;
  * TG2  max-severity aggregation ({0,1,3}->3, {0,2}->2, {0,0}->0, 127/timeout clamped);
  * TG3  the summary names each failing child + its argv; passing children are not
         named as failures; a non-required failure is WARN and is not counted;
  * TG4  source-grep writes-nothing guard + stdlib-only import check;
  * TG5  docs/ledger.md + docs/claim-ceiling.md byte-unchanged before/after a real run;
  * TG6  an unreachable required prerequisite (exit 1) is propagated, not swallowed;
  * TG7  --mode ci excludes L1 test_smokes; --mode local includes it; CI is sim-free;
  * TG8  the gate pins encoding="utf-8" (and the SDD §3 invocation shape) on every
         subprocess (source grep);
  * TG9  import-direction stays green with governance_gate present (analysis+stdlib only);
  * TG10 `python analysis/governance_gate.py --mode ci` is green on HEAD (CLI + --json).

Run:  python tests/test_governance_gate.py     (exit 0 ok / 1 failure)
stdlib only (NFR-1).
"""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "analysis"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

import governance_gate as gg        # the module under test (analysis/)
import ledger_validate as lv        # analysis/ — reused for the pinned governance hashes
import test_import_direction as tid  # tests/ — import-direction checker (TG9)

GATE_SRC = "analysis/governance_gate.py"

_FAILURES: "list[str]" = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}  {detail}")
        _FAILURES.append(name)


# --------------------------------------------------------------------------------------
# Synthetic child injection — tiny throwaway scripts that sys.exit(N) (optionally sleep
# or emit a stderr line). Never a real child mutated to fail (SDD §10; review focus).
# --------------------------------------------------------------------------------------

def _synth(tmp: Path, name: str, exit_code: int, *, required: bool = True,
           subset: str = "ci", stderr_msg=None, sleep=None) -> "gg.Child":
    body = ["import sys"]
    if sleep is not None:
        body.append("import time")
        body.append(f"time.sleep({sleep})")
    if stderr_msg is not None:
        body.append(f"print({stderr_msg!r}, file=sys.stderr)")
    body.append(f"sys.exit({exit_code})")
    script = tmp / f"{name}.py"
    script.write_text("\n".join(body) + "\n", encoding="utf-8")
    return gg.Child(name=name, argv=(str(script),), subset=subset, required=required)


# --------------------------------------------------------------------------------------
# TG1 — child failure injection.
# --------------------------------------------------------------------------------------

def tg1_child_failure_injection(tmp: Path) -> None:
    for code in (1, 2, 3):
        res = gg.run_children([_synth(tmp, f"fail{code}", code)])
        agg = gg.aggregate_exit(res)
        check(f"TG1 synthetic child exit {code} -> aggregate non-zero", agg != 0, f"got {agg}")
        check(f"TG1 synthetic child exit {code} -> aggregate == {code}", agg == code, f"got {agg}")
    res_ok = gg.run_children([_synth(tmp, "ok0", 0)])
    check("TG1 passing child -> aggregate 0", gg.aggregate_exit(res_ok) == 0,
          str(gg.aggregate_exit(res_ok)))


# --------------------------------------------------------------------------------------
# TG2 — nonzero aggregation = max severity (incl. out-of-family + timeout clamp).
# --------------------------------------------------------------------------------------

def tg2_max_severity(tmp: Path) -> None:
    mixed = gg.run_children([_synth(tmp, "m0", 0), _synth(tmp, "m1", 1), _synth(tmp, "m3", 3)])
    check("TG2 mixed {0,1,3} -> aggregate 3", gg.aggregate_exit(mixed) == 3, str(gg.aggregate_exit(mixed)))
    two = gg.run_children([_synth(tmp, "a0", 0), _synth(tmp, "b2", 2)])
    check("TG2 {0,2} -> aggregate 2", gg.aggregate_exit(two) == 2, str(gg.aggregate_exit(two)))
    zeros = gg.run_children([_synth(tmp, "z0a", 0), _synth(tmp, "z0b", 0)])
    check("TG2 {0,0} -> aggregate 0", gg.aggregate_exit(zeros) == 0, str(gg.aggregate_exit(zeros)))
    # out-of-family exit 127 -> clamped to EXIT_GOVERNANCE (fail-closed), raw code kept.
    odd = gg.run_children([_synth(tmp, "odd127", 127)])
    check("TG2 exit 127 -> clamped non-zero", gg.aggregate_exit(odd) != 0, str(gg.aggregate_exit(odd)))
    check("TG2 exit 127 -> clamped to EXIT_GOVERNANCE (3)",
          gg.aggregate_exit(odd) == gg.EXIT_GOVERNANCE, str(gg.aggregate_exit(odd)))
    check("TG2 exit 127 raw code preserved on the result", odd[0].exit_code == 127, str(odd[0].exit_code))
    # timeout -> run_error -> clamped to failure (never a silent 0).
    slow = gg.run_children([_synth(tmp, "slow", 0, sleep=30)], timeout=0.5)
    check("TG2 timeout -> run_error set", slow[0].run_error is not None, str(slow[0].run_error))
    check("TG2 timeout -> clamped to EXIT_GOVERNANCE (fail-closed)",
          gg.aggregate_exit(slow) == gg.EXIT_GOVERNANCE, str(gg.aggregate_exit(slow)))


# --------------------------------------------------------------------------------------
# TG3 — failed-check naming (FAIL/WARN; passing not named; non-required not counted).
# --------------------------------------------------------------------------------------

def tg3_failed_check_naming(tmp: Path) -> None:
    passing = _synth(tmp, "C-pass", 0)
    failing = _synth(tmp, "C-fail", 3, stderr_msg="synthetic child diagnostic line")
    warn = _synth(tmp, "C-warn", 1, required=False)
    results = gg.run_children([passing, failing, warn])
    agg = gg.aggregate_exit(results)
    buf = io.StringIO()
    gg.render_summary("ci", results, agg, stream=buf)
    out = buf.getvalue()
    check("TG3 failing child name is reported", "C-fail" in out, out)
    check("TG3 failing child argv is reported", str(tmp / "C-fail.py") in out, out)
    check("TG3 failing child stderr tail surfaced", "synthetic child diagnostic line" in out, out)
    check("TG3 passing child not named (only failures are listed)", "C-pass" not in out, out)
    check("TG3 non-required failing child shown as WARN", "WARN[1] C-warn" in out, out)
    check("TG3 non-required child not counted in aggregate (required-only == 3)", agg == 3, f"got {agg}")
    tail = out.split("failing:")[-1]
    check("TG3 WARN child excluded from the final failing list",
          "C-fail" in tail and "C-warn" not in tail, tail)


# --------------------------------------------------------------------------------------
# TG4 — writes-nothing source grep + stdlib-only imports (mirror test_ledger_validate).
# --------------------------------------------------------------------------------------

def tg4_writes_nothing_and_stdlib_only() -> None:
    src = Path(gg.__file__).read_text(encoding="utf-8")
    write_tokens = ("write_text", "write_bytes", "writelines", ".write(", "open(",
                    "shutil.", "os.remove", "os.unlink", "os.replace", ".mkdir(",
                    ".unlink(", ".touch(", ".rename(")
    for tok in write_tokens:
        check(f"TG4 gate names no '{tok}' write/mutation call", tok not in src, tok)
    for tok in ('"add"', '"commit"', '"push"', '"reset"', '"checkout"', '"stash"', '"rm"', '"mv"'):
        check(f"TG4 gate invokes no git {tok} subcommand", tok not in src, tok)
    # stdlib-only: no top-level import resolves to a project zone (analysis/sim/eval/runtime/cabt).
    zone_map = tid._module_zone_map()
    imports = tid._top_imports(Path(gg.__file__))
    project_imports = sorted(n for n in imports if zone_map.get(n) is not None)
    check("TG4 gate imports stdlib only (no project-zone import)", project_imports == [],
          f"project imports: {project_imports}")


# --------------------------------------------------------------------------------------
# TG5 — ledger/claim-ceiling hash preservation before/after a real gate run.
# --------------------------------------------------------------------------------------

def tg5_hash_preservation() -> None:
    before_l = lv.git_hash_object(lv.DEFAULT_LEDGER)
    before_c = lv.git_hash_object(lv.DEFAULT_CLAIM_CEILING)
    with contextlib.redirect_stderr(io.StringIO()):
        rc = gg.main(["--mode", "ci"])
    after_l = lv.git_hash_object(lv.DEFAULT_LEDGER)
    after_c = lv.git_hash_object(lv.DEFAULT_CLAIM_CEILING)
    check("TG5 gate --mode ci is green on HEAD (exit 0)", rc == 0, f"got {rc}")
    check("TG5 docs/ledger.md byte-unchanged by a gate run",
          before_l == after_l == lv.LEDGER_HASH_S03_START, f"{before_l} -> {after_l}")
    check("TG5 docs/claim-ceiling.md byte-unchanged by a gate run",
          before_c == after_c == lv.CEILING_HASH_S03_START, f"{before_c} -> {after_c}")


# --------------------------------------------------------------------------------------
# TG6 — fail-closed on an unreachable required prerequisite.
# --------------------------------------------------------------------------------------

def tg6_fail_closed(tmp: Path) -> None:
    # synthetic required child reporting an input/prerequisite failure (exit 1).
    res = gg.run_children([_synth(tmp, "prereq-unreachable", 1,
                                  stderr_msg="baseline unreachable (synthetic)")])
    agg = gg.aggregate_exit(res)
    check("TG6 required exit-1 child propagated, not swallowed (aggregate == 1)", agg == 1, f"got {agg}")
    check("TG6 fail-closed is never a silent 0", agg != 0)
    # real fail-closed: ledger_validate over an unreachable committed baseline (bogus ref) -> exit 1.
    bogus = gg.Child("C1:ledger_validate@bogus-ref",
                     ("analysis/ledger_validate.py", "--baseline-ref", "0" * 40), "ci")
    rres = gg.run_children([bogus])
    check("TG6 real ledger_validate fails closed on unreachable baseline (exit 1)",
          rres[0].exit_code == 1, f"got {rres[0].exit_code}; stderr={rres[0].stderr[-200:]}")
    check("TG6 real unreachable baseline propagated to aggregate (== 1)",
          gg.aggregate_exit(rres) == 1, str(gg.aggregate_exit(rres)))


# --------------------------------------------------------------------------------------
# TG7 — CI/local partition (test_smokes is local-only).
# --------------------------------------------------------------------------------------

def tg7_ci_local_partition() -> None:
    ci = gg.active_children("ci")
    local = gg.active_children("local")
    ci_names = [c.name for c in ci]
    local_names = [c.name for c in local]
    check("TG7 --mode ci excludes L1 test_smokes", not any("smokes" in n for n in ci_names), str(ci_names))
    check("TG7 --mode ci has only ci-subset children", all(c.subset == "ci" for c in ci), str(ci_names))
    check("TG7 --mode ci is exactly C1–C5",
          ci_names == ["C1:ledger_validate", "C2:test_import_direction", "C3:test_ledger_validate",
                       "C4:test_trace_diagnostic", "C5:test_evidence_summary"], str(ci_names))
    check("TG7 CI subset is simulator-free (no test_smokes argv)",
          all("test_smokes" not in " ".join(c.argv) for c in ci), str(ci_names))
    check("TG7 --mode local includes L1 test_smokes", any("smokes" in n for n in local_names), str(local_names))
    check("TG7 --mode local is a superset of --mode ci", set(ci_names).issubset(set(local_names)))
    check("TG7 L1 test_smokes is required in local mode",
          all(c.required for c in local if "smokes" in c.name))
    check("TG7 bare/default mode is ci", gg.DEFAULT_MODE == "ci", gg.DEFAULT_MODE)


# --------------------------------------------------------------------------------------
# TG8 — encoding="utf-8" pin (and the SDD §3 invocation shape) on every subprocess.
# --------------------------------------------------------------------------------------

def tg8_encoding_pin() -> None:
    src = Path(gg.__file__).read_text(encoding="utf-8")
    n_run = src.count("subprocess.run(")
    n_enc = src.count('encoding="utf-8"')
    check("TG8 gate uses subprocess.run", n_run >= 1, f"count={n_run}")
    check('TG8 gate pins encoding="utf-8"', n_enc >= 1, f"count={n_enc}")
    # one subprocess.run call site -> each is pinned (n_enc also counts the stdout reconfigure pin).
    check("TG8 every subprocess.run carries an encoding pin", n_enc >= n_run, f"{n_enc} enc vs {n_run} run")
    for tok in ("sys.executable", "cwd=", "capture_output=True", "text=True", "timeout="):
        check(f"TG8 gate subprocess pins {tok}", tok in src, tok)


# --------------------------------------------------------------------------------------
# TG9 — import-direction preserved with governance_gate present.
# --------------------------------------------------------------------------------------

def tg9_import_direction() -> None:
    violations = tid.check()
    check("TG9 import-direction green (whole repo, gate present)", violations == [], f"{violations}")
    gate_viol = [v for v in violations if "governance_gate" in v]
    check("TG9 governance_gate has no import-direction violation", not gate_viol, f"{gate_viol}")
    zone_map = tid._module_zone_map()
    check("TG9 governance_gate is in the import-direction scanned set",
          zone_map.get("governance_gate") == "analysis", str(zone_map.get("governance_gate")))
    imports = tid._top_imports(Path(gg.__file__))
    cross = sorted(n for n in imports if zone_map.get(n) not in (None, "analysis"))
    check("TG9 governance_gate imports only stdlib + analysis-zone", not cross, f"cross-zone: {cross}")


# --------------------------------------------------------------------------------------
# TG10 — green-on-HEAD smoke for the real CLI (and --json).
# --------------------------------------------------------------------------------------

def tg10_green_on_head() -> None:
    gate = str(REPO_ROOT / "analysis" / "governance_gate.py")
    bare = subprocess.run([sys.executable, gate], cwd=str(REPO_ROOT),
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=600)
    check("TG10 bare `python analysis/governance_gate.py` exits 0 on HEAD (default ci)",
          bare.returncode == 0, f"rc={bare.returncode}; stderr tail={bare.stderr[-400:]}")
    js = subprocess.run([sys.executable, gate, "--mode", "ci", "--json"], cwd=str(REPO_ROOT),
                        capture_output=True, text=True, encoding="utf-8",
                        errors="replace", timeout=600)
    check("TG10 `--mode ci --json` exits 0 on HEAD", js.returncode == 0,
          f"rc={js.returncode}; stderr={js.stderr[-300:]}")
    try:
        report = json.loads(js.stdout)
    except Exception as exc:  # noqa: BLE001
        check("TG10 --json stdout parses", False, f"{exc}; stdout={js.stdout[:200]}")
        return
    check("TG10 --json reports aggregate 0", report.get("aggregate") == 0, str(report)[:300])
    children = report.get("children", [])
    check("TG10 --json lists exactly the 5 CI children", len(children) == 5, str(report)[:300])
    check("TG10 --json every child exits 0", all(c.get("exit") == 0 for c in children), str(children)[:400])


def main() -> int:
    try:  # robust output regardless of console codepage (Windows cp1252)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    print("test_governance_gate:")
    # fast structural / source-grep / import checks first.
    tg4_writes_nothing_and_stdlib_only()
    tg7_ci_local_partition()
    tg8_encoding_pin()
    tg9_import_direction()
    # real end-to-end runs over the live C1–C5 (slower; spawn subprocesses).
    tg5_hash_preservation()
    tg10_green_on_head()
    # synthetic-child injection in a tempdir.
    with tempfile.TemporaryDirectory() as _d:
        tmp = Path(_d)
        tg1_child_failure_injection(tmp)
        tg2_max_severity(tmp)
        tg3_failed_check_naming(tmp)
        tg6_fail_closed(tmp)

    if _FAILURES:
        print(f"\nFAILED ({len(_FAILURES)}): {', '.join(_FAILURES)}", file=sys.stderr)
        return 1
    print("\nall governance_gate checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
