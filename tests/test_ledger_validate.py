#!/usr/bin/env python3
"""``tests/test_ledger_validate.py`` — the S03 checks for
``analysis/ledger_validate.py`` (Cycle-008 S03; PRD C8-FR-4; SDD §4; RN-1).

Stdlib plain-Python test module (``main()`` -> exit 0/1, mirroring
``tests/test_trace_diagnostic.py`` / ``tests/test_import_direction.py``). Drives the
committed synthetic fixtures under ``tests/fixtures/ledger_validate/`` plus the real
tracked ``docs/ledger.md`` / ``docs/claim-ceiling.md`` (read-only). It does NOT depend
on the gitignored ``runs/`` tree.

Proves:
  * the current REAL ledger validates (exit 0) and the REAL claim ceiling holds Rung 2;
  * exact baseline equality passes; a pure schema-valid append passes;
  * an edited prior row is rejected (append-only, via the injected baseline; RN-1);
  * header / separator / table-shape edits are rejected (structural, exit 2);
  * a malformed row, empty ``claim_ceiling``, cross-regime row, non-SHA-256 digest, and
    non-digest ``git_rev`` are rejected;
  * the "see cited summary" by-reference convention is ACCEPTED (SDD-C8-7);
  * a missing claim-ceiling file fails (exit 1); a claim-ceiling advance fails (exit 3);
  * unauthorized Rung-3 / SP-6 / value-promotion semantics in an appended row fail (exit 3);
  * an unreachable committed baseline fails closed (exit 1), never a silent exit 0;
  * the CLI returns the 0/1/2/3 exit contract;
  * the module writes nothing (source-grep) and the real ledger hash is unchanged by a run;
  * the pinned S03-start hash invariants hold;
  * import-direction / stdlib-only stays green and the module is in the scanned set.

Run:  python tests/test_ledger_validate.py     (exit 0 ok / 1 failure)
stdlib only (NFR-1).
"""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "analysis"))
sys.path.insert(0, str(REPO_ROOT / "eval"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

import ledger_validate as lv          # the module under test (analysis/)
import hygiene_check                  # eval/ — path-rule scanner (tests may reference it)
import test_import_direction as tid   # tests/ — import-direction checker

FIX = REPO_ROOT / "tests" / "fixtures" / "ledger_validate"
VALID_LEDGER = FIX / "valid_ledger.md"
VALID_CEILING = FIX / "valid_ceiling.md"
REAL_LEDGER = "docs/ledger.md"
REAL_CEILING = "docs/claim-ceiling.md"

_FAILURES: "list[str]" = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}  {detail}")
        _FAILURES.append(name)


# --------------------------------------------------------------------------------------
# Fixture-derivation helpers — build every reject class from the one committed synthetic
# valid ledger (mirrors trace_diagnostic's `_reject` mutate pattern; keeps the fixture
# subtree minimal per the "synthetic, minimal" instruction).
# --------------------------------------------------------------------------------------

def _read(p) -> str:
    return Path(p).read_text(encoding="utf-8")


def _lines(text: str) -> "list[str]":
    return text.splitlines()


def _join(lines: "list[str]") -> str:
    return "\n".join(lines) + "\n"


def _table_idx(lines: "list[str]") -> "list[int]":
    return [i for i, l in enumerate(lines) if l.strip().startswith("|")]


def _row(cells: "list[str]") -> str:
    return "| " + " | ".join(cells) + " |"


def _clone_cells(text: str, data_i: int = 0) -> "list[str]":
    lines = _lines(text)
    ti = _table_idx(lines)
    return lv._split_cells(lines[ti[2 + data_i]])


def _mutate_row(text: str, data_i: int, fn) -> str:
    lines = _lines(text)
    ti = _table_idx(lines)
    li = ti[2 + data_i]
    cells = lv._split_cells(lines[li])
    fn(cells)
    lines[li] = _row(cells)
    return _join(lines)


def _mutate_line(text: str, which: int, fn) -> str:
    """which: 0 header, 1 separator (table-line index)."""
    lines = _lines(text)
    ti = _table_idx(lines)
    lines[ti[which]] = fn(lines[ti[which]])
    return _join(lines)


def _append_cells(text: str, cells: "list[str]") -> str:
    return text.rstrip("\n") + "\n" + _row(cells) + "\n"


def _tmp(tmp: Path, name: str, text: str) -> str:
    p = tmp / name
    p.write_text(text, encoding="utf-8")
    return str(p)


# normalized base used as the injected append-only baseline everywhere (so derived
# variants and the baseline are constructed identically — no trailing-newline skew).
BASE = _join(_lines(_read(VALID_LEDGER)))


# --------------------------------------------------------------------------------------
# Real-artifact acceptance (the load-bearing "current ledger validates" checks).
# --------------------------------------------------------------------------------------

def t_real_ledger_validates() -> None:
    with contextlib.redirect_stderr(io.StringIO()):
        rc_pos = lv.main([REAL_LEDGER])                       # sprint-plan positional shape
        rc_flag = lv.main(["--ledger", REAL_LEDGER, "--claim-ceiling", REAL_CEILING])
    check("real ledger validates via positional CLI (exit 0)", rc_pos == 0, f"got {rc_pos}")
    check("real ledger+ceiling validates via flag CLI (exit 0)", rc_flag == 0, f"got {rc_flag}")
    # default (no args) targets the tracked governance artifacts and validates.
    with contextlib.redirect_stderr(io.StringIO()):
        rc_default = lv.main([])
    check("real ledger validates via default CLI (exit 0)", rc_default == 0, f"got {rc_default}")


def t_real_claim_ceiling_rung2() -> None:
    v = lv.validate_claim_ceiling(_read(REAL_CEILING))
    check("real claim ceiling holds Rung 2 (no violations)", v == [], str(v)[:200])


def t_pinned_hash_invariants() -> None:
    check("real ledger git hash == S03-start pin",
          lv.git_hash_object(REAL_LEDGER) == lv.LEDGER_HASH_S03_START,
          f"got {lv.git_hash_object(REAL_LEDGER)}")
    check("real claim-ceiling git hash == S03-start pin",
          lv.git_hash_object(REAL_CEILING) == lv.CEILING_HASH_S03_START,
          f"got {lv.git_hash_object(REAL_CEILING)}")
    # the opt-in pinned-hash CLI assertion passes for the real files and fails on a wrong pin.
    with contextlib.redirect_stderr(io.StringIO()):
        rc_ok = lv.main(["--ledger", REAL_LEDGER, "--claim-ceiling", REAL_CEILING,
                         "--expected-ledger-hash", lv.LEDGER_HASH_S03_START,
                         "--expected-ceiling-hash", lv.CEILING_HASH_S03_START])
        rc_bad = lv.main(["--ledger", REAL_LEDGER, "--expected-ledger-hash", "0" * 40])
    check("CLI --expected-*-hash matches real files (exit 0)", rc_ok == 0, f"got {rc_ok}")
    check("CLI --expected-ledger-hash mismatch rejected (exit 3)", rc_bad == 3, f"got {rc_bad}")


def t_ledger_unchanged_by_run() -> None:
    before = lv.git_hash_object(REAL_LEDGER)
    with contextlib.redirect_stderr(io.StringIO()):
        lv.main([REAL_LEDGER])                                # run the gate over the real ledger
    after = lv.git_hash_object(REAL_LEDGER)
    check("real ledger byte-unchanged before/after a run (read-only)",
          before == after == lv.LEDGER_HASH_S03_START, f"{before} -> {after}")


# --------------------------------------------------------------------------------------
# Append-only discipline (RN-1) — via the injected baseline (deterministic, no git).
# --------------------------------------------------------------------------------------

def t_equality_passes(tmp: Path) -> None:
    check("exact baseline equality classifies 'equal'", lv.classify_append(BASE, BASE) == ("equal", ""))
    code, v = lv.validate(str(VALID_LEDGER), str(VALID_CEILING), baseline_text=BASE)
    check("validate() of equal ledger+valid ceiling exits 0", code == 0, str(v)[:200])


def t_pure_append_passes(tmp: Path) -> None:
    cells = _clone_cells(BASE, 0)                # clone the schema-valid Rung-1 row
    cells[1] = "run-syn-3"
    cells[3] = "3" * 40                          # a fresh 40-hex git_rev
    appended = _append_cells(BASE, cells)
    status, delta = lv.classify_append(BASE, appended)
    check("schema-valid append classifies 'append'", status == "append")
    check("appended ledger is still structurally valid", lv.validate_ledger_structure(appended) == [])
    check("appended delta carries no unauthorized governance",
          lv.scan_unauthorized_governance(delta) == [])
    code, v = lv.validate(_tmp(tmp, "appended_ok.md", appended), str(VALID_CEILING), baseline_text=BASE)
    check("validate() of a pure schema-valid append exits 0", code == 0, str(v)[:200])


def t_prior_row_edit_fails(tmp: Path) -> None:
    edited = _mutate_row(BASE, 0, lambda c: c.__setitem__(9, "0.9"))   # win_rate 0.5 -> 0.9
    check("edited prior row classifies 'edit'", lv.classify_append(BASE, edited)[0] == "edit")
    code, v = lv.validate(_tmp(tmp, "edited_prior.md", edited), str(VALID_CEILING), baseline_text=BASE)
    check("validate() of an edited prior row exits 3", code == 3, str(v)[:200])


def t_unreachable_baseline_fails_closed() -> None:
    # None baseline simulates 'git show' failing (git unavailable, or ledger absent at ref).
    code, v = lv.validate(str(VALID_LEDGER), str(VALID_CEILING), baseline_text=None)
    check("unreachable baseline fails closed (exit 1)", code == 1, str(v)[:200])
    check("unreachable baseline never a silent exit 0", code != 0)
    check("unreachable baseline reports the RN-1 input failure",
          any(c == 1 and "baseline" in r.lower() for c, r in v), str(v)[:200])


# --------------------------------------------------------------------------------------
# Structural / field rejection classes — demonstrated as a single appended bad row over
# the valid baseline, so each yields one clean, single-cause exit code via validate().
# --------------------------------------------------------------------------------------

def _validate_appended(tmp: Path, name: str, mutate_cells) -> "tuple[int, list]":
    cells = _clone_cells(BASE, 0)
    cells[1] = "run-syn-bad"
    mutate_cells(cells)
    text = _append_cells(BASE, cells)
    return lv.validate(_tmp(tmp, name, text), str(VALID_CEILING), baseline_text=BASE)


def t_structural_rejections(tmp: Path) -> None:
    # header edit — both a schema mismatch (exit 2, pure) and an append-only edit (exit 3).
    hdr = _mutate_line(BASE, 0, lambda l: l.replace("| win_rate |", "| winrate |"))
    sv = lv.validate_ledger_structure(hdr)
    check("header edit -> structural violation (exit 2)", any(c == 2 for c, _ in sv), str(sv)[:200])
    code_h, _ = lv.validate(_tmp(tmp, "hdr.md", hdr), str(VALID_CEILING), baseline_text=BASE)
    check("validate() of a header edit fails (non-zero)", code_h != 0, f"got {code_h}")

    # separator edit -> structural violation (exit 2).
    sep = _mutate_line(BASE, 1, lambda l: "| x | x | x |")
    sv2 = lv.validate_ledger_structure(sep)
    check("separator/table-shape edit -> structural violation (exit 2)",
          any(c == 2 for c, _ in sv2), str(sv2)[:200])

    # wrong column count (appended row missing a cell) -> exit 2.
    code_wc, vwc = _validate_appended(tmp, "wrongcols.md", lambda c: c.__delitem__(5))
    check("malformed row (wrong column count) -> exit 2", code_wc == 2, str(vwc)[:200])

    # empty claim_ceiling -> exit 3.
    code_ec, vec = _validate_appended(tmp, "emptyceil.md", lambda c: c.__setitem__(16, ""))
    check("empty claim_ceiling -> exit 3", code_ec == 3, str(vec)[:200])

    # two regimes in one row -> cross-regime structural refusal (exit 2).
    code_xr, vxr = _validate_appended(
        tmp, "xregime.md", lambda c: c.__setitem__(2, "regime-syn-a vs regime-syn-b"))
    check("cross-regime row -> exit 2", code_xr == 2, str(vxr)[:200])

    # non-SHA-256 digest where one is cited -> exit 3.
    code_nh, vnh = _validate_appended(
        tmp, "nonsha.md", lambda c: c.__setitem__(17, "synthetic notes; sha256 deadbeef (too short)"))
    check("non-SHA-256 digest citation -> exit 3", code_nh == 3, str(vnh)[:200])

    # non-digest git_rev -> exit 3.
    code_gr, vgr = _validate_appended(
        tmp, "badrev.md", lambda c: c.__setitem__(3, "not-a-git-digest"))
    check("non-digest git_rev -> exit 3", code_gr == 3, str(vgr)[:200])


def t_by_reference_accepted() -> None:
    # SDD-C8-7: the "see cited summary" convention in the numeric columns is ACCEPTED.
    row2 = _clone_cells(BASE, 1)
    check("by-reference 'see cited summary' present in the numeric columns",
          all(row2[i] == "see cited summary" for i in (9, 10, 11, 12, 13)))
    check("a 'see cited summary' ledger is structurally valid (not rejected)",
          lv.validate_ledger_structure(BASE) == [])


# --------------------------------------------------------------------------------------
# Unauthorized governance movement (appended-delta only) + claim-ceiling anchoring.
# --------------------------------------------------------------------------------------

def t_unauthorized_governance(tmp: Path) -> None:
    # pure scan: movement markers fire; the authorized Rung-1/Rung-2 framing does NOT.
    check("scan flags an appended Rung-3 advance",
          lv.scan_unauthorized_governance("| ... | Rung 3 (advance) | ... |") != [])
    check("scan flags an appended SP-6 promotion",
          lv.scan_unauthorized_governance("notes: SP-6 promotion of a new value") != [])
    check("scan flags an appended value promotion",
          lv.scan_unauthorized_governance("notes: value promotion to a new rung") != [])
    check("scan does NOT flag a clean Rung-1 row", lv.scan_unauthorized_governance(
          "Rung 1 (legal completion): synthetic descriptive row") == [])
    check("scan does NOT flag a Rung-2 row (the authorized ceiling)",
          lv.scan_unauthorized_governance("Rung 2 (beats random-legal): descriptive") == [])

    # via validate(): each is a structurally-valid append rejected solely by the delta scan.
    code_r3, vr3 = _validate_appended(
        tmp, "rung3.md", lambda c: c.__setitem__(16, "Rung 3 (synthetic unauthorized advance)"))
    check("appended Rung-3 row -> exit 3 (unauthorized)", code_r3 == 3, str(vr3)[:200])
    code_sp, vsp = _validate_appended(
        tmp, "sp6.md", lambda c: c.__setitem__(17, "synthetic; SP-6 promotion (unauthorized)"))
    check("appended SP-6 row -> exit 3 (unauthorized)", code_sp == 3, str(vsp)[:200])
    code_vp, vvp = _validate_appended(
        tmp, "valpromo.md", lambda c: c.__setitem__(16, "value promotion (synthetic unauthorized)"))
    check("appended value-promotion row -> exit 3 (unauthorized)", code_vp == 3, str(vvp)[:200])


def t_claim_ceiling(tmp: Path) -> None:
    # valid synthetic ceiling holds Rung 2.
    check("synthetic valid ceiling holds Rung 2", lv.validate_claim_ceiling(_read(VALID_CEILING)) == [])
    # an advance to Rung 3 is rejected (exit 3).
    advanced = _read(VALID_CEILING).replace("standing ceiling: Rung 2", "standing ceiling: Rung 3")
    va = lv.validate_claim_ceiling(advanced)
    check("claim-ceiling advance to Rung 3 -> violation", any(c == 3 for c, _ in va), str(va)[:200])
    code_adv, vadv = lv.validate(str(VALID_LEDGER), _tmp(tmp, "adv_ceiling.md", advanced),
                                 baseline_text=BASE)
    check("validate() with an advanced claim ceiling exits 3", code_adv == 3, str(vadv)[:200])
    # a ceiling with no standing-posture line fails closed.
    check("unparseable claim ceiling fails closed",
          any(c == 3 for c, _ in lv.validate_claim_ceiling("# no standing ceiling line here")))
    # a missing claim-ceiling file is an input failure (exit 1).
    code_miss, vmiss = lv.validate(str(VALID_LEDGER), str(FIX / "does-not-exist.md"), baseline_text=BASE)
    check("missing claim-ceiling file -> exit 1", code_miss == 1, str(vmiss)[:200])


# --------------------------------------------------------------------------------------
# CLI exit contract, writes-nothing, import-direction, runs/-independence.
# --------------------------------------------------------------------------------------

def t_cli_exit_contract(tmp: Path) -> None:
    with contextlib.redirect_stderr(io.StringIO()):
        rc0 = lv.main([REAL_LEDGER])                                       # valid (baseline reachable)
        rc1 = lv.main(["--ledger", str(FIX / "nope.md"), "--claim-ceiling", REAL_CEILING])
        # a temp ledger is never in git, so its baseline is unreachable (exit 1) and the
        # structural/governance code (2/3) dominates via the max-severity rule.
        cells2 = _clone_cells(BASE, 0)
        del cells2[5]                                          # drop a cell -> wrong column count
        bad2 = _tmp(tmp, "cli_wrongcols.md", _append_cells(BASE, cells2))
        rc2 = lv.main(["--ledger", bad2, "--claim-ceiling", REAL_CEILING])
        cells3 = _clone_cells(BASE, 0)
        cells3[16] = ""                                        # empty claim_ceiling
        bad3 = _tmp(tmp, "cli_emptyceil.md", _append_cells(BASE, cells3))
        rc3 = lv.main(["--ledger", bad3, "--claim-ceiling", REAL_CEILING])
    check("CLI exit 0 (valid real ledger)", rc0 == 0, f"got {rc0}")
    check("CLI exit 1 (missing ledger file)", rc1 == 1, f"got {rc1}")
    check("CLI exit 2 (structural: wrong column count)", rc2 == 2, f"got {rc2}")
    check("CLI exit 3 (governance: empty claim_ceiling)", rc3 == 3, f"got {rc3}")


def t_writes_nothing() -> None:
    src = Path(lv.__file__).read_text(encoding="utf-8")
    # no file-write / filesystem-mutation call shapes anywhere in the module.
    write_tokens = ("write_text", "write_bytes", "writelines", ".write(", "open(",
                    "shutil.", "os.remove", "os.unlink", "os.replace", ".mkdir(",
                    ".unlink(", ".touch(", ".rename(")
    for tok in write_tokens:
        check(f"module names no '{tok}' write/mutation call", tok not in src)
    # subprocess git usage is read-only: only 'show' and 'hash-object'; no mutating subcommand.
    for tok in ('"add"', '"commit"', '"push"', '"reset"', '"checkout"', '"stash"', '"rm"', '"mv"'):
        check(f"module invokes no git {tok} subcommand", tok not in src)
    check("module uses only read-only git reads (show + hash-object)",
          '"show"' in src and '"hash-object"' in src)


def t_import_direction() -> None:
    violations = tid.check()
    check("import-direction green (whole repo)", violations == [], f"{violations}")
    lv_viol = [v for v in violations if "ledger_validate" in v]
    check("ledger_validate has no import-direction violation", not lv_viol, f"{lv_viol}")
    zone_map = tid._module_zone_map()
    check("ledger_validate is in the import-direction scanned set",
          zone_map.get("ledger_validate") == "analysis")
    imports = tid._top_imports(Path(lv.__file__))
    cross = sorted(n for n in imports if zone_map.get(n) not in (None, "analysis"))
    check("ledger_validate imports only stdlib + analysis-zone", not cross, f"cross-zone: {cross}")


def t_runs_independence() -> None:
    # the fixtures live under tests/, never the gitignored runs/ tree (R11).
    check("fixtures under tests/, not runs/",
          "tests" in VALID_LEDGER.parts and "fixtures" in VALID_LEDGER.parts
          and "runs" not in VALID_LEDGER.parts)
    # per-file hygiene: each committed fixture path is Competition-Data-clean.
    for fp in sorted(FIX.glob("*.md")):
        rel = fp.relative_to(REPO_ROOT).as_posix()
        check(f"fixture path hygiene-clean: {fp.name}", hygiene_check.find_violations([rel]) == [], rel)


def main() -> int:
    try:  # robust output regardless of console codepage (Windows cp1252)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    print("test_ledger_validate:")
    t_real_ledger_validates()
    t_real_claim_ceiling_rung2()
    t_pinned_hash_invariants()
    t_ledger_unchanged_by_run()
    t_unreachable_baseline_fails_closed()
    t_by_reference_accepted()
    t_import_direction()
    t_writes_nothing()
    t_runs_independence()
    with tempfile.TemporaryDirectory() as _d:
        tmp = Path(_d)
        t_equality_passes(tmp)
        t_pure_append_passes(tmp)
        t_prior_row_edit_fails(tmp)
        t_structural_rejections(tmp)
        t_unauthorized_governance(tmp)
        t_claim_ceiling(tmp)
        t_cli_exit_contract(tmp)

    if _FAILURES:
        print(f"\nFAILED ({len(_FAILURES)}): {', '.join(_FAILURES)}", file=sys.stderr)
        return 1
    print("\nall ledger_validate checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
