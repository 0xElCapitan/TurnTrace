#!/usr/bin/env python3
"""``analysis/governance_gate.py`` — offline, stdlib-only, **read-only** governance
gate that runs TurnTrace's existing validators + stdlib test modules as ONE check
(Cycle-009 SP-A; PRD C9-FR-1/2/3; SDD §1–§7).

Cycle-008 wrote the governance controls (``analysis/ledger_validate.py``,
``analysis/trace_diagnostic.py``, ``analysis/evidence_summary.py``) and their
stdlib test modules, but nothing runs them as one gate. This module is that one
orchestration layer: it **subprocess-invokes** each child, reads its ``0/1/2/3``
exit code, aggregates the children as **max severity**, names every failing
child, **fails closed** on an unreachable required prerequisite, and **writes
nothing**.

**Pure orchestration.** The gate adds no validation logic — no new rule, regex,
or allow-list. Each child runs in its own interpreter as a subprocess, so the
gate's own import graph stays stdlib-only and the ``analysis/`` import-direction
invariant (``tests/test_import_direction.py``: ``analysis`` may import
``analysis`` only) holds for this module exactly as it does for the other
``analysis/`` modules. Subprocess isolation also makes "writes nothing" a
structural property: the gate only reads each child's ``returncode`` + captured
stdout/stderr; it never imports a child and cannot leak a child's state into its
own process.

**Read-only by construction.** No ``--fix``/``--write`` mode, no file writes, no
directory creation, no run-dir creation, no git mutation. The gate's only side
effects are subprocess spawns of read-only children and reading their captured
output. A source-grep test (``tests/test_governance_gate.py`` TG4) asserts this
module names no write/mutation call and imports stdlib only.

**Child registry (data, not branches).** Each child is a record
``(name, argv, subset, required)`` with ``subset ∈ {ci, local}``. The CI subset is
simulator-free; ``tests/test_smokes.py`` (L1) needs ``cabt`` +
``TURNTRACE_DECK_FILE`` (Competition Data — local/gitignored) and is therefore
**excluded from ``--mode ci``**. ``trace_diagnostic --validate`` /
``evidence_summary --validate`` are already exercised over their fixture corpora
by C4/C5's test modules, so the v1 registry adds no redundant direct
``--validate <file>`` child (SDD §4.1/§4.3).

CLI / documented local invocation (run before landing governance changes)::

    python analysis/governance_gate.py              # default: --mode ci (simulator-free)
    python analysis/governance_gate.py --mode ci    # the CI subset (C1–C5); no cabt/deck
    python analysis/governance_gate.py --mode local # CI subset + L1 test_smokes (needs cabt+deck)
    python analysis/governance_gate.py --mode ci --json   # machine-readable report on stdout

A green gate is **well-formedness only, never authorization**: it reports that
the governance *mechanics* are valid; it blesses no rung, advances no ceiling, and
is **not** permission to write a ledger row. ``docs/ledger.md`` remains the only
ceiling-bearing artifact; this gate carries no ceiling of its own.

Exit (max child severity, the existing ``analysis/`` family):
  0 every required child in the active mode exited 0 (well-formedness only) ·
  1 a required child reported an input/prerequisite failure (fail-closed) ·
  2 a required child reported a structural refusal ·
  3 a required child reported a governance/leak refusal, OR a child could not be
    run/verified (spawn failure / timeout / out-of-family exit) — fail-closed.
stdlib only (NFR-1).
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---- exit codes (parity-in-shape with the analysis/ validator family —
# ----  ledger_validate.py:105-108 / trace_diagnostic.py / evidence_summary.py). ----
EXIT_OK = 0          # every required child exited 0 (well-formedness only)
EXIT_INPUT = 1       # input / prerequisite failure (fail-closed)
EXIT_STRUCTURE = 2   # structural refusal
EXIT_GOVERNANCE = 3  # governance/leak refusal, or could-not-run/verify (fail-closed)

_EXIT_FAMILY = (EXIT_OK, EXIT_INPUT, EXIT_STRUCTURE, EXIT_GOVERNANCE)

# ---- per-child subprocess timeout (seconds). A hung child fails closed (SDD §6.3). ----
PER_CHILD_TIMEOUT_S = 120.0

# ---- invocation modes -> the child subsets they run. Data, not branches: --mode ci
# ----  runs the simulator-free CI subset only; --mode local adds the local-only subset
# ----  (test_smokes, which needs cabt + TURNTRACE_DECK_FILE). Bare invocation defaults
# ----  to ci (OD-C9-D-default): the safest default is Competition-Data-free. ----
MODE_SUBSETS = {
    "ci": frozenset({"ci"}),
    "local": frozenset({"ci", "local"}),
}
DEFAULT_MODE = "ci"


@dataclasses.dataclass(frozen=True)
class Child:
    """A registry record: the child's display ``name``; its ``argv`` (passed after
    ``sys.executable``; ``argv[0]`` is the child script path, REPO_ROOT-relative or
    absolute); the ``subset`` it belongs to (``ci`` | ``local``); and whether a
    non-zero exit counts toward the aggregate (``required``) or is a non-counted
    WARN (``required=False``)."""
    name: str
    argv: tuple
    subset: str
    required: bool = True


@dataclasses.dataclass(frozen=True)
class ChildResult:
    """The outcome of running one child: the record, the raw process ``exit_code``
    (``None`` if the child never produced one), captured ``stdout``/``stderr``, and a
    ``run_error`` cause string when the child could not be run/verified (spawn
    failure / timeout)."""
    child: Child
    exit_code: "int | None"
    stdout: str
    stderr: str
    run_error: "str | None" = None


# ---- the v1 child registry (OD-C9-4; SDD §4). CI subset = C1–C5 (simulator-free,
# ----  required); local-only subset = L1 test_smokes (required in --mode local,
# ----  excluded from --mode ci). argv[0] is the child path relative to REPO_ROOT
# ----  (resolved by cwd=REPO_ROOT at spawn). ----
REGISTRY = (
    Child("C1:ledger_validate", ("analysis/ledger_validate.py",), "ci"),
    Child("C2:test_import_direction", ("tests/test_import_direction.py",), "ci"),
    Child("C3:test_ledger_validate", ("tests/test_ledger_validate.py",), "ci"),
    Child("C4:test_trace_diagnostic", ("tests/test_trace_diagnostic.py",), "ci"),
    Child("C5:test_evidence_summary", ("tests/test_evidence_summary.py",), "ci"),
    Child("L1:test_smokes", ("tests/test_smokes.py",), "local"),
)


def active_children(mode, registry=REGISTRY):
    """The children that run in ``mode``, filtered by subset (data-driven). An unknown
    mode is a fail-closed ``ValueError`` (the CLI also constrains ``--mode`` via
    argparse ``choices``)."""
    subsets = MODE_SUBSETS.get(mode)
    if subsets is None:
        raise ValueError(f"unknown mode {mode!r}; expected one of {sorted(MODE_SUBSETS)}")
    return [c for c in registry if c.subset in subsets]


# =====================================================================================
# Child invocation — subprocess only (SDD §3). The gate imports no child; each runs in
# its own interpreter, preserving the analysis/ import-direction invariant by construction.
# =====================================================================================

def run_child(child, *, timeout=PER_CHILD_TIMEOUT_S):
    """Run one child as ``[sys.executable, *child.argv]`` from REPO_ROOT, read-only.

    ``encoding="utf-8"`` is load-bearing on every subprocess: Windows defaults to
    cp1252, which mangles the ledger's UTF-8 em-dashes and would corrupt a child's
    captured diagnostic (mirrors ``ledger_validate.py``'s git-read pin). ``errors=
    "replace"`` keeps that utf-8 pin while staying robust: a child that emits a stray
    cp1252 byte on its (non-reconfigured) stderr must never crash the gate's capture
    thread — the gate reads exit codes, and captured text is diagnostic-only. A
    timeout or a spawn failure is surfaced as a ``run_error`` (fail-closed; SDD §6.3)
    rather than a silent pass."""
    cmd = [sys.executable, *child.argv]
    try:
        proc = subprocess.run(
            cmd, cwd=str(REPO_ROOT),
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout if isinstance(exc.stdout, str) else ""
        err = exc.stderr if isinstance(exc.stderr, str) else ""
        return ChildResult(child, None, out, err, run_error=f"timeout after {timeout:g}s")
    except (OSError, subprocess.SubprocessError) as exc:
        return ChildResult(child, None, "", "", run_error=f"spawn failed: {exc}")
    return ChildResult(child, proc.returncode, proc.stdout or "", proc.stderr or "")


def run_children(children, *, timeout=PER_CHILD_TIMEOUT_S):
    """Run each child in order, returning one ChildResult per child."""
    return [run_child(c, timeout=timeout) for c in children]


# =====================================================================================
# Aggregation — max severity in the 0/1/2/3 family; non-zero iff any REQUIRED child is
# non-zero. A child that could not be run/verified (run_error) or returned an exit code
# outside the family is clamped to EXIT_GOVERNANCE (the worst severity) — fail-closed,
# never a silent 0 (SDD §5). The raw cause is preserved on the result for the report.
# =====================================================================================

def severity(result):
    """The in-family severity (0/1/2/3) a child contributes to the aggregate. A
    ``run_error`` or an out-of-family exit code clamps to EXIT_GOVERNANCE: the gate
    cannot prove the child well-formed, so it fails closed to the worst severity
    (the raw code/cause is still reported)."""
    if result.run_error is not None:
        return EXIT_GOVERNANCE
    rc = result.exit_code
    if rc in _EXIT_FAMILY:
        return rc
    return EXIT_GOVERNANCE


def aggregate_exit(results):
    """Max severity among the REQUIRED children (non-required failures are WARN, not
    counted). 0 only when every required child exited 0."""
    return max((severity(r) for r in results if r.child.required), default=EXIT_OK)


# =====================================================================================
# Reporting — human-readable summary to stderr, optional --json to stdout. Reads only
# what was already captured; writes no file.
# =====================================================================================

def _raw_code(result):
    """The raw cause to show for a failing child: the process exit code, or the
    ``run_error`` string when the child never produced an exit code."""
    return result.run_error if result.run_error is not None else result.exit_code


def _argv_str(child):
    return " ".join(child.argv)


def _stderr_tail(text, max_lines=20):
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return lines[-max_lines:]


def render_summary(mode, results, aggregate, *, stream=None):
    """Print the human-readable gate summary: each failing child named with its argv
    and a stderr tail, then a final PASS/FAIL line. Required failures are ``FAIL``;
    non-required failures are ``WARN`` (not counted in the aggregate)."""
    if stream is None:
        stream = sys.stderr
    failing_required = []
    for r in results:
        if severity(r) == EXIT_OK:
            continue
        label = "FAIL" if r.child.required else "WARN"
        print(f"{label}[{_raw_code(r)}] {r.child.name} — {_argv_str(r.child)}", file=stream)
        for ln in _stderr_tail(r.stderr):
            print(f"      {ln}", file=stream)
        if r.child.required:
            failing_required.append(r.child.name)
    if aggregate == EXIT_OK:
        print(f"gate: PASS (exit 0) — mode={mode}; {len(results)} child(ren) ran; "
              f"wrote nothing. Well-formedness only, never authorization.", file=stream)
    else:
        print(f"gate: FAIL (exit {aggregate}) — mode={mode}; "
              f"failing: {', '.join(failing_required)}", file=stream)


def json_report(mode, results, aggregate):
    """A machine-readable report (stdlib ``json``): the ``aggregate``, the ``mode``, and
    a row per child ``{name, argv, exit, severity, required, subset[, error]}``."""
    children = []
    for r in results:
        row = {
            "name": r.child.name,
            "argv": list(r.child.argv),
            "exit": r.exit_code,
            "severity": severity(r),
            "required": r.child.required,
            "subset": r.child.subset,
        }
        if r.run_error is not None:
            row["error"] = r.run_error
        children.append(row)
    return {"aggregate": aggregate, "mode": mode, "children": children}


_EPILOG = (
    "documented local invocation (run before landing governance changes):\n"
    "  python analysis/governance_gate.py --mode local   # CI subset + test_smokes (needs cabt+deck)\n"
    "  python analysis/governance_gate.py --mode ci       # the simulator-free CI subset\n"
    "\n"
    "CI green = well-formedness only, never authorization. The ledger remains the only\n"
    "ceiling-bearing artifact; this gate writes nothing and carries no ceiling of its own."
)


def main(argv=None) -> int:
    try:  # robust utf-8 output on both streams regardless of console codepage (Windows cp1252)
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

    ap = argparse.ArgumentParser(
        prog="governance_gate",
        description="Offline, read-only governance gate: runs the existing validators "
                    "+ stdlib test modules as one check, aggregates their 0/1/2/3 exits "
                    "as max severity, names failing children, fails closed, writes nothing.",
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--mode", choices=tuple(MODE_SUBSETS), default=DEFAULT_MODE,
                    help=f"which child subset to run (default {DEFAULT_MODE}: the "
                         f"simulator-free CI subset; 'local' adds test_smokes)")
    ap.add_argument("--json", action="store_true",
                    help="emit a machine-readable JSON report on stdout instead of the "
                         "human-readable summary on stderr")
    ap.add_argument("--timeout", type=float, default=PER_CHILD_TIMEOUT_S,
                    help=f"per-child subprocess timeout in seconds (default "
                         f"{PER_CHILD_TIMEOUT_S:g}; a hung child fails closed)")
    args = ap.parse_args(argv)

    results = run_children(active_children(args.mode), timeout=args.timeout)
    aggregate = aggregate_exit(results)

    if args.json:
        print(json.dumps(json_report(args.mode, results, aggregate), indent=2))
    else:
        render_summary(args.mode, results, aggregate)
    return aggregate


if __name__ == "__main__":
    raise SystemExit(main())
