#!/usr/bin/env python3
"""``analysis/freezes_nothing_lint.py`` — offline, stdlib-only, **read-only**
freezes-nothing lint (Cycle-009 SP-D; PRD C9-FR-4; SDD §8–§9; gated FEASIBLE by SP-C).

A *form-only* governance doc (e.g. ``docs/cycles/cycle-008/08d-rung3-form-only-semantics.md``)
names every Rung-3 governance parameter — ``M`` / ``K`` / ``n`` / regime / threshold /
candidate / feature-family — while **binding a value to none of them**. This lint detects
the one shape that would break that contract: a governance parameter **bound to a value via
an explicit assignment operator** (``PARAM = VALUE`` / ``PARAM := VALUE``). It reads the
target doc, writes nothing, and exits non-zero if any such assignment/value-binding form is
present.

**v1 discriminator (assignment/value-binding only).** This is the narrow v1 discriminator
validated by the SP-C feasibility spike (``grimoires/loa/a2a/cycle-009/08-sp-c-feasibility.md``
§6), with the SP-C **review M1** refinement applied: the ``VALUE`` right-hand side is
``{placeholder | number | quoted}`` — the loose bare-identifier branch (``[A-Za-z_]\\w*``) is
**dropped** so definitional prose like ``"Let n = number of batches"`` no longer false-positives,
while every assignment-form poison example still carries a placeholder/number/quoted RHS and is
still detected. There is **no** broad freeze-word parser, **no** negation-scope parser, **no**
semantic/prose-intent parser, and **no** Rung-3 authorization logic. The clean form-only corpus
saturates *negated* mentions of every freeze token; keying on the value-binding form (not on
negation proximity) is exactly why a narrow lint is feasible without being brittle.

**Known v1 false-negative class (SP-C review L1 — honest disclosure).** This lint detects a
syntactic FORM, not semantics, and does **not** claim complete semantic protection. The
following bind a parameter without an ``=`` / ``:=`` operator and therefore **pass v1**
(``exit 0``):

  * prose-verb bindings — ``"set the regime to <REGIME>"``, ``"freeze the margin at <M>"``
  * spelled-out values  — ``"the margin is hereby forty-two"``
  * table-row / delimited bindings — ``"| margin | <M> |"``, tab-separated ``"regime<TAB>is<TAB><REGIME>"``
  * non-``=`` separators / HTML-entity equals — ``"M&#61;<M>"``

Closing these is a careful v2 candidate (it risks re-introducing false positives on the clean
``08d`` form table); v1 deliberately stays assignment-only.

**Green is well-formedness only, never authorization.** A green result means *only* "no v1
assignment/value-binding freeze detected under v1 rules." It does **not** authorize Rung 3, an
attempt, a candidate, a metric, ``M``, ``K``/``n``, a regime, a threshold, a feature family,
SP-6, a promotion, a ledger row, or a claim-ceiling advance. ``docs/ledger.md`` remains the
**only** ceiling-bearing artifact; this lint carries no ceiling of its own (mirrors
``governance_gate.py``'s "well-formedness only, never authorization" framing).

**Read-only by construction.** No ``--fix``/``--write`` mode, no file writes, no directory
creation, no run-dir creation, no git mutation, no eval, no simulator import, no Competition-Data
dependency. It opens each target read-only with ``encoding="utf-8"`` pinned (Windows defaults to
cp1252, which mangles the docs' UTF-8 em-dashes/backticked tokens).

CLI::

    python analysis/freezes_nothing_lint.py docs/cycles/cycle-008/08d-rung3-form-only-semantics.md
    python analysis/freezes_nothing_lint.py docs/cycles/cycle-008/08c-blocked-family-map.md

Exit (max severity across targets, the existing ``analysis/`` family —
governance_gate.py:73-76 / ledger_validate.py):
  0 froze nothing under v1 rules (well-formedness only) ·
  1 a target was missing/unreadable (fail-closed) ·
  3 a v1 assignment/value-binding freeze form was detected (governance refusal).
stdlib only (NFR-1).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---- exit codes — parity-in-shape with the analysis/ validator family
# ----  (governance_gate.py:73-76; ledger_validate.py:86-... EXIT_INPUT/EXIT_GOVERNANCE).
# ----  This matches the ACCEPTED sprint plan D.1 / tests FN1-FN3
# ----  (docs/cycles/cycle-009/03-sprint-plan.md:400-402,421-423): clean=0, unreadable=1,
# ----  freeze-detected=3. (The SP-C feasibility §6 prose transcribed this mapping inverted;
# ----  the accepted plan + the analysis/ convention — EXIT_GOVERNANCE=3, EXIT_INPUT=1 — govern.)
EXIT_OK = 0          # froze nothing under v1 rules (well-formedness only)
EXIT_INPUT = 1       # missing / unreadable target (fail-closed)
EXIT_GOVERNANCE = 3  # a v1 assignment/value-binding freeze form was detected

# =====================================================================================
# v1 assignment/value-binding discriminator (SP-C feasibility §6 + review M1).
# Match shape:  \bPARAM\b  \s*  (= | :=)  \s*  VALUE      (assignment-only; value REQUIRED)
# No negation parsing, no freeze-word parsing, no semantic parsing.
# =====================================================================================

# governance parameters named by the Rung-3 form (08d §3 / 08c §3). "feature family" allows
# an optional space/underscore/hyphen between the two words.
_PARAM = r"(?:feature[\s_-]*family|regime|threshold|margin|candidate|M|K|n)"

# v1 is assignment-only: the narrowest, highest-precision binding operator family.
_BIND = r"(?:=|:=)"

# M1 (SP-C review §Concerns.1 / audit constraint #3): VALUE = {placeholder | number | quoted}.
# The bare-identifier branch ([A-Za-z_]\w*) is intentionally DROPPED — it made the lint match
# definitional prose ("Let n = number of batches"); poison detection is unchanged (every
# assignment-form poison binds a placeholder/number/quoted RHS).
_VALUE = (
    r"(?:"
    r"<[A-Za-z0-9_]+>"        # <PLACEHOLDER>  (the synthetic-token form)
    r"|[-+]?\d[\w.%+\-]*"     # number         (e.g. 42, -0.5, 1.5%)
    r'|"[^"]+"'               # "quoted value"
    r"|'[^']+'"               # 'quoted value'
    r")"
)

_FREEZE_RE = re.compile(r"\b" + _PARAM + r"\b\s*" + _BIND + r"\s*" + _VALUE)

# ---- surfaced framing (green disclaimer + honest FN-class). Exposed in output AND in --help
# ----  so green can never be silently misread as authorization. ----
GREEN_DISCLAIMER = (
    'green means only "no v1 assignment/value-binding freeze detected under v1 rules" — '
    "NOT authorization. It does NOT authorize Rung 3, an attempt, a candidate, a metric, M, "
    "K/n, a regime, a threshold, a feature family, SP-6, a promotion, a ledger row, or a "
    "claim-ceiling advance. docs/ledger.md remains the only ceiling-bearing artifact."
)

KNOWN_FALSE_NEGATIVE_CLASS = (
    "Known v1 false-negative class (this lint detects FORM, not semantics, and does NOT claim "
    "complete semantic protection). These bind a parameter WITHOUT an '='/':=' operator and "
    "PASS v1 (exit 0):\n"
    "  - prose-verb bindings: 'set the regime to <REGIME>', 'freeze the margin at <M>'\n"
    "  - spelled-out values:  'the margin is hereby forty-two'\n"
    "  - table-row / delimited bindings: '| margin | <M> |', tab-separated 'regime<TAB>is<TAB><REGIME>'\n"
    "  - non-'=' separators / HTML-entity equals: 'M&#61;<M>'"
)


def scan_text(text):
    """Return ``[(lineno, col, snippet), ...]`` for every v1 assignment/value-binding freeze
    form in ``text``. Line numbers are 1-based; ``col`` is the 1-based column of the match.
    Scanning per line keeps ``\\s*`` from spanning lines (an assignment is one line) and yields
    natural line context for the diagnostic."""
    hits = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in _FREEZE_RE.finditer(line):
            hits.append((lineno, m.start() + 1, m.group(0)))
    return hits


def read_target(path):
    """Read ``path`` read-only with ``encoding="utf-8"`` pinned. Raises ``OSError`` on a
    missing/unreadable target (mapped to EXIT_INPUT by ``main`` — fail-closed)."""
    return Path(path).read_text(encoding="utf-8")


_EPILOG = (
    "green = well-formedness only, never authorization:\n"
    "  " + GREEN_DISCLAIMER + "\n\n"
    + KNOWN_FALSE_NEGATIVE_CLASS + "\n\n"
    "This lint freezes nothing, writes nothing, runs no eval, and reads no Competition Data."
)


def main(argv=None) -> int:
    try:  # robust utf-8 on both streams regardless of console codepage (Windows cp1252)
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

    ap = argparse.ArgumentParser(
        prog="freezes_nothing_lint",
        description="Offline, read-only freezes-nothing lint: detects a governance parameter "
                    "bound to a value via an explicit '='/':=' assignment (v1 assignment/"
                    "value-binding discriminator) in a form-only governance doc. Writes nothing.",
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("targets", nargs="+",
                    help="target doc path(s) to lint (read-only; e.g. "
                         "docs/cycles/cycle-008/08d-rung3-form-only-semantics.md)")
    args = ap.parse_args(argv)

    any_freeze = False
    any_unreadable = False

    for target in args.targets:
        try:
            text = read_target(target)
        except OSError as exc:
            any_unreadable = True
            print(f"freezes_nothing_lint: FAIL-CLOSED (exit {EXIT_INPUT}) — cannot read "
                  f"{target!r}: {exc}", file=sys.stderr)
            continue
        hits = scan_text(text)
        if hits:
            any_freeze = True
            for lineno, col, snippet in hits:
                print(f"FREEZE  {target}:{lineno}:{col}  v1 assignment/value-binding form "
                      f"detected: {snippet!r}", file=sys.stderr)

    # max severity across targets: freeze (3) > unreadable (1) > clean (0).
    if any_freeze:
        print(f"freezes_nothing_lint: FAIL (exit {EXIT_GOVERNANCE}) — a v1 assignment/"
              f"value-binding freeze form was detected (governance refusal). This is "
              f"FORM-detection only; {KNOWN_FALSE_NEGATIVE_CLASS.splitlines()[0]}",
              file=sys.stderr)
        return EXIT_GOVERNANCE
    if any_unreadable:
        print(f"freezes_nothing_lint: FAIL-CLOSED (exit {EXIT_INPUT}) — a target was "
              f"missing/unreadable; refusing to report green on an unread target.",
              file=sys.stderr)
        return EXIT_INPUT

    print(f"freezes_nothing_lint: PASS (exit {EXIT_OK}) — no v1 assignment/value-binding "
          f"freeze detected in {', '.join(args.targets)}.", file=sys.stderr)
    print(f"  {GREEN_DISCLAIMER}", file=sys.stderr)
    print(f"  {KNOWN_FALSE_NEGATIVE_CLASS}", file=sys.stderr)
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
