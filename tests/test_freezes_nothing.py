#!/usr/bin/env python3
"""``tests/test_freezes_nothing.py`` — the SP-D checks for
``analysis/freezes_nothing_lint.py`` (Cycle-009 SP-D; PRD C9-FR-4; SDD §8–§9; gated
FEASIBLE by SP-C).

Stdlib plain-Python test module (``main()`` -> exit 0/1, mirroring
``tests/test_governance_gate.py`` / ``tests/test_ledger_validate.py``), so the module
is itself gate-child-eligible (``raise SystemExit(main())``). Offline, stdlib-only,
read-only. Synthetic poisoned/clean docs are written to a tempdir with **synthetic
placeholder tokens only** (``<M>``, ``<REGIME>``, …) — never a real candidate / M /
K / n / regime / threshold / feature-family value.

Covers FN1–FN5 (03-sprint-plan.md:417-426) + the SP-D operator test requirements:
  * FN1  each synthetic frozen-shape class (candidate/M/K/n/regime/threshold/feature-family,
         plus spaced and multi-param forms) -> exit 3;
  * FN2  synthetic negation-clause prose -> exit 0;
  * FN3  the real tracked 08d (and 08c, included per OD-C9-5) -> exit 0;
  * FN4  no-real-value guard — every synthetic string is placeholder-only (no hex /
         regime-vNNN / decimal margin);
  * FN5  no regex reuse — the discriminator is self-contained; the lint does not import
         trace_diagnostic (so there is no copy to parity-pin);
  * M1   the dropped bare-identifier VALUE branch — definitional "M = margin" /
         "n = number" pass (exit 0); only placeholder/number/quoted RHS are detected;
  * L1   the known false-negative class (prose-verb / spelled-out / table-row / delimited /
         HTML-entity) is documented AND verified non-detected (exit 0);
  * diagnostic names file/path + line; green prints the non-authorizing disclaimer;
  * read-only / writes-nothing source grep; stdlib-only; no sim/eval/agents.runtime/cabt
    import; no Competition-Data dependency; ledger/claim-ceiling byte-unchanged.

Run:  python tests/test_freezes_nothing.py     (exit 0 ok / 1 failure)
stdlib only (NFR-1).
"""

from __future__ import annotations

import contextlib
import io
import re
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "analysis"))
sys.path.insert(0, str(REPO_ROOT / "tests"))

import freezes_nothing_lint as fnl    # the module under test (analysis/)
import ledger_validate as lv          # analysis/ — reused for the pinned governance hashes
import test_import_direction as tid   # tests/ — import-direction / zone-map helpers

LINT_SRC = "analysis/freezes_nothing_lint.py"
D08D = "docs/cycles/cycle-008/08d-rung3-form-only-semantics.md"
D08C = "docs/cycles/cycle-008/08c-blocked-family-map.md"

_FAILURES: "list[str]" = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}  {detail}")
        _FAILURES.append(name)


# --------------------------------------------------------------------------------------
# Synthetic corpus — placeholder tokens ONLY (no real value anywhere). FN4 guards this.
# --------------------------------------------------------------------------------------

# One poisoned frozen-shape per governance-parameter class + the spaced/walrus/multi-param
# forms from the SP-C v1 threat model (08-sp-c-feasibility §5 Tier A). Each MUST be detected.
POISON = {
    "candidate":      "candidate=<VALUE>",
    "M":              "freeze M=<M>",
    "K":              "K=<K>",
    "n":              "n=<N>",
    "regime":         "regime := <REGIME>",                 # walrus / colon-equal
    "threshold":      "threshold=<THRESHOLD>",
    "feature-family": "feature family=<FEATURE_FAMILY>",
    "spaced":         "We pre-register M = <M>, K = <K>, n = <N>.",
    "multiparam":     "frozen comparison: M=<M>, regime=<REGIME>, threshold=<THRESHOLD>",
}

# Negation / form-only prose that names parameters but binds no value (08-sp-c-feasibility §4).
# Each MUST be accepted (exit 0) — these are the shapes a naive keyword/proximity lint trips on.
CLEAN = [
    "This document does not freeze M.",
    "freezes no parameter",
    "no parameter is frozen",
    "No regime id is selected.",
    "The margin M is left unset.",
    "It declines to freeze K, n, or the regime.",
    "No threshold of any kind is set.",
    "freezes nothing",
    "We freeze none of: M, K, n, regime, threshold, feature family.",
    "The form names M, K, n without choosing values.",
    "the full comparison tuple (candidate, incumbent, regime, margin) is fixed before any band exists",
    "candidate and incumbent compared under one frozen regime",
]

# M1 (SP-C review §Concerns.1): definitional '=' prose that the DROPPED bare-identifier
# branch would have false-positived on. With VALUE = {placeholder|number|quoted}, these pass.
M1_DEFINITIONAL = [
    "Let n = number of batches",
    "Define M = margin",
]

# L1 (SP-C review §Concerns.2): the documented v1 false-negative class — bindings without an
# '='/':=' operator. These PASS v1 (exit 0) by construction; the lint discloses them honestly.
FALSE_NEGATIVE = [
    "We set the regime to <REGIME>.",     # prose-verb "to"
    "Freeze the margin at <M>.",           # prose-verb "at"
    "The margin is hereby forty-two.",     # spelled-out value
    "| margin | <M> |",                    # table-row / delimited
    "regime\tis\t<REGIME>",                # tab-separated
    "M&#61;<M>",                            # HTML-entity equals
]

ALL_SYNTHETIC = list(POISON.values()) + CLEAN + M1_DEFINITIONAL + FALSE_NEGATIVE


def run_lint(*targets):
    """Call ``fnl.main`` in-process, capturing stdout+stderr. Returns ``(rc, out, err)``."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = fnl.main(list(targets))
    return rc, out.getvalue(), err.getvalue()


def _write(tmp: Path, name: str, content: str) -> str:
    p = tmp / name
    p.write_text(content, encoding="utf-8")
    return str(p)


# --------------------------------------------------------------------------------------
# FN1 — poisoned-fixture rejection (one per frozen-shape class) -> exit 3.
# --------------------------------------------------------------------------------------

def fn1_poison_rejected(tmp: Path) -> None:
    for cls, line in POISON.items():
        # surround the poison with clean negation prose so the doc is realistic.
        doc = f"This form-only doc freezes nothing.\n{line}\nNo other parameter is frozen.\n"
        path = _write(tmp, f"poison_{cls}.md", doc)
        rc, _out, err = run_lint(path)
        check(f"FN1 poison class {cls!r} -> exit 3", rc == fnl.EXIT_GOVERNANCE, f"got {rc}")
        check(f"FN1 poison class {cls!r} names a FREEZE diagnostic", "FREEZE" in err, err[-200:])


# --------------------------------------------------------------------------------------
# FN2 — clean negation-clause acceptance -> exit 0.
# --------------------------------------------------------------------------------------

def fn2_clean_accepted(tmp: Path) -> None:
    doc = "\n".join(CLEAN) + "\n"
    path = _write(tmp, "clean_negation.md", doc)
    rc, _out, err = run_lint(path)
    check("FN2 clean negation corpus -> exit 0", rc == fnl.EXIT_OK, f"got {rc}; err={err[-300:]}")
    # also each clean line individually
    for i, line in enumerate(CLEAN):
        p = _write(tmp, f"clean_{i}.md", line + "\n")
        rc_i, _o, _e = run_lint(p)
        check(f"FN2 clean line {i} -> exit 0", rc_i == fnl.EXIT_OK, f"{line!r} got {rc_i}")


# --------------------------------------------------------------------------------------
# FN3 — real tracked 08d (and 08c, included per OD-C9-5) -> exit 0 (no false positive).
# --------------------------------------------------------------------------------------

def fn3_real_docs_accepted() -> None:
    rc_d, _o, err_d = run_lint(str(REPO_ROOT / D08D))
    check("FN3 real tracked 08d -> exit 0 (no false positive)", rc_d == fnl.EXIT_OK,
          f"got {rc_d}; err={err_d[-300:]}")
    rc_c, _o2, err_c = run_lint(str(REPO_ROOT / D08C))
    check("FN3 real tracked 08c -> exit 0 (no false positive)", rc_c == fnl.EXIT_OK,
          f"got {rc_c}; err={err_c[-300:]}")
    # both together -> still 0 (max severity over a clean set is 0)
    rc_both, _o3, _e3 = run_lint(str(REPO_ROOT / D08D), str(REPO_ROOT / D08C))
    check("FN3 08d + 08c together -> exit 0", rc_both == fnl.EXIT_OK, f"got {rc_both}")


# --------------------------------------------------------------------------------------
# FN4 — no-real-value guard: every synthetic string is placeholder-only.
# --------------------------------------------------------------------------------------

_REAL_VALUE_SHAPES = [
    (re.compile(r"\b[0-9a-fA-F]{40}\b"), "40-hex (sha1-like commit id)"),
    (re.compile(r"\b[0-9a-fA-F]{64}\b"), "64-hex (sha256-like)"),
    (re.compile(r"regime-v\d+", re.IGNORECASE), "live regime-vNNN token"),
    (re.compile(r"\b\d+\.\d+\b"), "decimal margin/number"),
]


def fn4_no_real_value() -> None:
    for s in ALL_SYNTHETIC:
        for rx, why in _REAL_VALUE_SHAPES:
            check(f"FN4 synthetic string carries no real value ({why})", rx.search(s) is None,
                  f"{s!r} matched {why}")
    # every poison RHS is a <PLACEHOLDER> (the only real-looking token we ever bind)
    for cls, line in POISON.items():
        rhs_ok = ("<" in line and ">" in line)
        check(f"FN4 poison {cls!r} binds only a <PLACEHOLDER> RHS", rhs_ok, line)


# --------------------------------------------------------------------------------------
# FN5 — no regex reuse: the discriminator is self-contained; the lint does not import
# trace_diagnostic, so there is no copied pattern to parity-pin (D.4 / FN5 are N/A by design).
# --------------------------------------------------------------------------------------

def fn5_no_regex_reuse() -> None:
    imports = tid._top_imports(Path(fnl.__file__))
    check("FN5 lint does not import trace_diagnostic (no regex reuse to pin)",
          "trace_diagnostic" not in imports, str(sorted(imports)))
    check("FN5 lint imports no analysis-zone module (self-contained, stdlib-only)",
          all(n.split(".")[0] != "trace_diagnostic" for n in imports), str(sorted(imports)))
    # the discriminator parts exist as module-level regex source (self-contained).
    check("FN5 discriminator is defined in-module (_FREEZE_RE present)",
          hasattr(fnl, "_FREEZE_RE") and fnl._FREEZE_RE.pattern, "missing _FREEZE_RE")


# --------------------------------------------------------------------------------------
# M1 — dropped bare-identifier VALUE branch: definitional '=' prose passes; only
# placeholder/number/quoted RHS are detected.
# --------------------------------------------------------------------------------------

def m1_value_tightened(tmp: Path) -> None:
    for i, line in enumerate(M1_DEFINITIONAL):
        p = _write(tmp, f"defn_{i}.md", line + "\n")
        rc, _o, _e = run_lint(p)
        check(f"M1 definitional prose {line!r} -> exit 0 (bare-identifier dropped)",
              rc == fnl.EXIT_OK, f"got {rc}")
    # white-box: a bare-identifier RHS does NOT match; placeholder/number/quoted DO.
    check("M1 'M = margin' is not a match (bare identifier dropped)",
          fnl._FREEZE_RE.search("M = margin") is None)
    check("M1 'n = number' is not a match (bare identifier dropped)",
          fnl._FREEZE_RE.search("n = number") is None)
    check("M1 'M = <M>' IS a match (placeholder)", fnl._FREEZE_RE.search("M = <M>") is not None)
    check("M1 'M=42' IS a match (number)", fnl._FREEZE_RE.search("M=42") is not None)
    check('M1 \'regime="x"\' IS a match (quoted)', fnl._FREEZE_RE.search('regime="x"') is not None)


# --------------------------------------------------------------------------------------
# L1 — known false-negative class documented AND verified non-detected (exit 0).
# --------------------------------------------------------------------------------------

def l1_false_negative_class(tmp: Path) -> None:
    for i, line in enumerate(FALSE_NEGATIVE):
        p = _write(tmp, f"fn_{i}.md", line + "\n")
        rc, _o, _e = run_lint(p)
        check(f"L1 documented false-negative passes v1 (exit 0): {line!r}",
              rc == fnl.EXIT_OK, f"got {rc}")
    # the FN class is enumerated in the lint's surfaced framing (constraint #4 / #12).
    doc = fnl.KNOWN_FALSE_NEGATIVE_CLASS
    for needle in ("prose-verb", "spelled-out", "table-row", "delimited", "HTML-entity"):
        check(f"L1 FN-class enumeration documents {needle!r}", needle in doc, doc)
    check("L1 lint does not claim complete semantic protection",
          "not" in doc.lower() and "semantic" in doc.lower(), doc[:120])


# --------------------------------------------------------------------------------------
# Diagnostic content — failure names file/path + line (operator test #4).
# --------------------------------------------------------------------------------------

def t_diagnostic_path_and_line(tmp: Path) -> None:
    doc = "clean intro line\nanother clean line\nregime := <REGIME>\n"   # freeze on line 3
    p = _write(tmp, "located.md", doc)
    rc, _o, err = run_lint(p)
    check("diagnostic exit 3 for located poison", rc == fnl.EXIT_GOVERNANCE, f"got {rc}")
    check("diagnostic names the file path", p in err, err[-200:])
    check("diagnostic names the line number (line 3)", f"{p}:3:" in err, err[-200:])
    check("diagnostic shows the matched form", "regime := <REGIME>" in err, err[-200:])


# --------------------------------------------------------------------------------------
# Green output exposes the non-authorizing disclaimer (operator test #5).
# --------------------------------------------------------------------------------------

def t_green_disclaimer(tmp: Path) -> None:
    p = _write(tmp, "green.md", "This doc freezes nothing. No regime id is selected.\n")
    rc, _o, err = run_lint(p)
    check("green run -> exit 0", rc == fnl.EXIT_OK, f"got {rc}")
    low = err.lower()
    for needle in ("not authorization", "rung 3", "ledger", "no v1 assignment"):
        check(f"green output exposes disclaimer phrase {needle!r}", needle in low, err[-400:])
    # the constant itself is non-authorizing and names the ceiling-bearing artifact.
    dl = fnl.GREEN_DISCLAIMER.lower()
    check("GREEN_DISCLAIMER denies Rung-3/attempt/candidate/SP-6 authorization",
          all(k in dl for k in ("rung 3", "attempt", "candidate", "sp-6")), fnl.GREEN_DISCLAIMER)
    check("GREEN_DISCLAIMER names docs/ledger.md as the only ceiling-bearing artifact",
          "ledger.md" in dl and "only" in dl, fnl.GREEN_DISCLAIMER)


# --------------------------------------------------------------------------------------
# Read-only / writes-nothing source grep + stdlib-only (operator tests #7, #10).
# --------------------------------------------------------------------------------------

def t_read_only_stdlib_only() -> None:
    src = Path(fnl.__file__).read_text(encoding="utf-8")
    write_tokens = ("write_text", "write_bytes", "writelines", ".write(", "open(",
                    "shutil.", "os.remove", "os.unlink", "os.replace", ".mkdir(",
                    ".unlink(", ".touch(", ".rename(")
    for tok in write_tokens:
        check(f"lint names no '{tok}' write/mutation call", tok not in src, tok)
    for tok in ('"add"', '"commit"', '"push"', '"reset"', '"checkout"'):
        check(f"lint invokes no git {tok} subcommand", tok not in src, tok)
    # no subprocess / eval / run-dir machinery (read-only file scan only).
    for tok in ("subprocess", "os.system", "popen", "mkdir"):
        check(f"lint contains no '{tok}' (no child spawn / no run dir)", tok not in src, tok)
    # the read it DOES do is utf-8 pinned.
    check('lint pins encoding="utf-8" on its read', 'encoding="utf-8"' in src)
    # stdlib-only: no top-level import resolves to a project zone.
    zone_map = tid._module_zone_map()
    imports = tid._top_imports(Path(fnl.__file__))
    project_imports = sorted(n for n in imports if zone_map.get(n) is not None)
    check("lint imports stdlib only (no project-zone import)", project_imports == [],
          f"project imports: {project_imports}")


# --------------------------------------------------------------------------------------
# No forbidden imports: sim / eval / agents.runtime / cabt (operator test #8).
# --------------------------------------------------------------------------------------

def t_no_forbidden_imports() -> None:
    imports = tid._top_imports(Path(fnl.__file__))
    forbidden_roots = {"sim", "eval", "cabt", "agents"}
    bad = sorted(n for n in imports if n.split(".")[0] in forbidden_roots)
    check("lint imports none of sim/eval/cabt/agents(.runtime)", bad == [], f"forbidden: {bad}")


# --------------------------------------------------------------------------------------
# No Competition-Data dependency (operator test #9).
# --------------------------------------------------------------------------------------

def t_no_competition_data_dependency(tmp: Path) -> None:
    # runs on a plain temp doc with no deck.csv / cg/ / runs/ present.
    p = _write(tmp, "standalone.md", "freezes nothing\n")
    rc, _o, _e = run_lint(p)
    check("lint runs on a standalone temp doc (no Competition Data needed) -> exit 0",
          rc == fnl.EXIT_OK, f"got {rc}")
    src = Path(fnl.__file__).read_text(encoding="utf-8")
    for tok in ("deck.csv", "TURNTRACE_DECK_FILE", "cg/", "cg.dll", "runs/"):
        check(f"lint source references no Competition-Data token {tok!r}", tok not in src, tok)


# --------------------------------------------------------------------------------------
# Ledger / claim-ceiling byte-unchanged by a real lint run (operator test #10).
# --------------------------------------------------------------------------------------

def t_ledger_ceiling_unchanged() -> None:
    before_l = lv.git_hash_object(lv.DEFAULT_LEDGER)
    before_c = lv.git_hash_object(lv.DEFAULT_CLAIM_CEILING)
    with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
        fnl.main([str(REPO_ROOT / D08D), str(REPO_ROOT / D08C)])
    after_l = lv.git_hash_object(lv.DEFAULT_LEDGER)
    after_c = lv.git_hash_object(lv.DEFAULT_CLAIM_CEILING)
    check("docs/ledger.md byte-unchanged by a lint run",
          before_l == after_l == lv.LEDGER_HASH_S03_START, f"{before_l} -> {after_l}")
    check("docs/claim-ceiling.md byte-unchanged by a lint run",
          before_c == after_c == lv.CEILING_HASH_S03_START, f"{before_c} -> {after_c}")


# --------------------------------------------------------------------------------------
# CLI smoke — the real entrypoint over the tracked targets exits 0 (operator direct run).
# --------------------------------------------------------------------------------------

def t_cli_smoke_on_head() -> None:
    rc_missing, _o, err = run_lint(str(REPO_ROOT / "docs/cycles/cycle-008/does-not-exist.md"))
    check("missing target -> fail-closed exit 1", rc_missing == fnl.EXIT_INPUT, f"got {rc_missing}")
    check("missing target diagnostic mentions FAIL-CLOSED", "FAIL-CLOSED" in err, err[-200:])


def main() -> int:
    try:  # robust output regardless of console codepage (Windows cp1252)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    print("test_freezes_nothing:")
    # fast structural / source-grep / import / white-box checks first.
    fn4_no_real_value()
    fn5_no_regex_reuse()
    t_read_only_stdlib_only()
    t_no_forbidden_imports()
    fn3_real_docs_accepted()
    t_ledger_ceiling_unchanged()
    # behavioral checks over synthetic docs in a tempdir.
    with tempfile.TemporaryDirectory() as _d:
        tmp = Path(_d)
        fn1_poison_rejected(tmp)
        fn2_clean_accepted(tmp)
        m1_value_tightened(tmp)
        l1_false_negative_class(tmp)
        t_diagnostic_path_and_line(tmp)
        t_green_disclaimer(tmp)
        t_no_competition_data_dependency(tmp)
        t_cli_smoke_on_head()

    if _FAILURES:
        print(f"\nFAILED ({len(_FAILURES)}): {', '.join(_FAILURES)}", file=sys.stderr)
        return 1
    print("\nall freezes_nothing checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
