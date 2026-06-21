#!/usr/bin/env python3
"""``analysis/ledger_validate.py`` — offline, stdlib-only, **read-only** ledger-row
+ claim-ceiling governance gate (Cycle-008 S03; PRD C8-FR-4; SDD §4; RN-1).

A gate-only validator that content-checks the tracked governance artifacts
**before any future ledger row or claim-ceiling movement is trusted**. It says
whether the ledger *mechanics* are valid; it never scores an agent, never
generates evidence, never determines Rung-3 readiness, and **blesses no new
rung** (OD-C8-2; the validator is a gate, not a scoring system).

**Read-only by construction.** This module never writes, stages, commits, or
mutates anything. Its only side effects are two *read-only* ``git`` reads —
``git show <ref>:docs/ledger.md`` (the append-only baseline, RN-1) and
``git hash-object`` (the optional pinned-hash check) — both via ``subprocess``
(stdlib; NFR-1). A source-grep test (``tests/test_ledger_validate.py``) asserts
the module names no write/append/open-for-write call against ``docs/``.

What it checks (each a rejection class with a synthetic poisoned fixture under
``tests/fixtures/ledger_validate/``):

  1. **Table discipline (exit 2).** One consistent 18-column header matching the
     house schema **verbatim** (``docs/ledger.md:9``; PRD C8-FR-4.1); a separator
     row present and 18-wide; every data row exactly 18 cells. A header or
     separator edit, or a wrong-width row, is a structural refusal.
  2. **Required fields (exit 2/3).** ``regime_id`` names exactly one regime
     (a two-regime row is a cross-regime structural refusal, exit 2); the
     ``claim_ceiling`` cell is non-empty (empty ⇒ exit 3); ``git_rev`` is a
     git digest; a ``sha256`` citation is a 64-hex SHA-256 digest (non-digest
     ⇒ exit 3). The **"see cited summary"** by-reference convention is
     explicitly **allowed** in the numeric metric columns (SDD-C8-7; the
     validator requires no numeric values there).
  3. **Append-only (exit 1/3; RN-1).** The working-tree ledger is compared
     against its committed baseline read read-only via ``git show <ref>:<path>``.
     Exact equality and *pure appends* (the committed content remains a
     byte-identical prefix) pass; an edited prior row/header/separator/historical
     line is rejected (exit 3). If no committed baseline is reachable (git
     unavailable, or the ledger absent at the ref) the append-only check
     **fails closed** (exit 1) — never a silent exit 0.
  4. **Unauthorized governance movement (exit 3).** Applied **only to the
     appended delta** (rows beyond the committed baseline — the committed
     history is the authorized truth and is never re-judged): an appended row
     that advances the ceiling (``Rung 3+``), creates an ``SP-6`` promotion, or
     promotes a value is unauthorized in this posture and is rejected. S03
     authorizes no ledger row, no SP-6, no value promotion, no claim-ceiling
     advance, and no Rung-3 target/candidate/pre-registration/fresh-evidence.
  5. **Claim-ceiling anchoring (exit 1/3).** ``docs/claim-ceiling.md`` must
     exist (missing ⇒ exit 1) and its standing ceiling must read **Rung 2**
     (anything else, or unreadable posture, ⇒ exit 3 — fail-closed).
  6. **Pinned-hash invariants (opt-in; exit 1/3).** ``--expected-ledger-hash`` /
     ``--expected-ceiling-hash`` compare ``git hash-object`` against a pinned
     value (a point-in-time integrity assertion). Off by default so the gate
     stays reusable for legitimate future appends (which change the hash). The
     S03-start pins are exported as module constants for the verification test.

``analysis/`` imports stdlib only — no ``cabt``, ``sim/``, ``agents/runtime/``,
or ``eval/`` (the offline/runtime separation; enforced by
``tests/test_import_direction.py``). NFR-1, NFR-2.

CLI:
  python analysis/ledger_validate.py [docs/ledger.md]
  python analysis/ledger_validate.py --ledger docs/ledger.md --claim-ceiling docs/claim-ceiling.md
Exit: 0 valid · 1 input failure / baseline unreachable (fail-closed) ·
      2 table-shape / cross-regime structural refusal ·
      3 append-only edit / empty ceiling / bad digest / unauthorized movement.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---- default tracked governance artifacts (read-only) ----
DEFAULT_LEDGER = "docs/ledger.md"
DEFAULT_CLAIM_CEILING = "docs/claim-ceiling.md"

# ---- S03-start pinned invariants (git hash-object; LF-normalized content identity).
# ----  These are the byte-state at S03 start, exported for the verification test and
# ----  for an opt-in `--expected-*-hash` integrity assertion. They are NOT a default
# ----  gate (a legitimate future append changes the hash) — see the docstring §6 and
# ----  the V001 LF-normalization note in tests/test_smokes.py. ----
LEDGER_HASH_S03_START = "7da7e9a8dbed6561669d1569445eb9fe67a953fb"
CEILING_HASH_S03_START = "3d99759b919f7d75bc41ea81cd82e5f1fb974be7"

# ---- the 18-column ledger schema, pinned VERBATIM from docs/ledger.md:9 (the house
# ----  format; PRD C8-FR-4.1; eval/schemas.md / aggregate.LEDGER_COLUMNS). The current
# ----  tracked ledger IS the schema authority — this is its header, not a new schema. ----
LEDGER_COLUMNS = (
    "date", "run_id", "regime_id", "git_rev", "sim_version", "agent_version",
    "opponent_pool_ref", "seed_set_ref", "games", "win_rate", "illegal_action_rate",
    "timeout_rate", "error_rate", "avg_turns", "mode", "hypothesis", "claim_ceiling",
    "notes",
)
N_COLUMNS = len(LEDGER_COLUMNS)                       # 18
REGIME_COL = LEDGER_COLUMNS.index("regime_id")        # 2
GIT_REV_COL = LEDGER_COLUMNS.index("git_rev")         # 3
CLAIM_CEILING_COL = LEDGER_COLUMNS.index("claim_ceiling")  # 16

# ---- exit codes (parity-in-shape with the analysis/ validator family —
# ----  evidence_summary.py:46-48 / trace_diagnostic.py:56-57). ----
EXIT_OK = 0          # valid
EXIT_INPUT = 1       # input failure / committed baseline unreachable (fail-closed)
EXIT_STRUCTURE = 2   # table-shape / column-count / cross-regime structural refusal
EXIT_GOVERNANCE = 3  # append-only edit / empty ceiling / non-digest / unauthorized movement

# ---- digest shapes ----
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$", re.IGNORECASE)
_GIT_REV_RE = re.compile(r"^[0-9a-f]{40}$|^[0-9a-f]{64}$", re.IGNORECASE)  # SHA-1 or SHA-256 git rev
_SHA256_CITATION_RE = re.compile(r"sha-?256[\s:=]+([0-9a-zA-Z]+)", re.IGNORECASE)
_REGIME_TOKEN_RE = re.compile(r"regime-", re.IGNORECASE)
_SEPARATOR_CELL_RE = re.compile(r"^:?-+:?$")  # markdown table separator cell (dashes, opt. colons)

# ---- claim-ceiling standing-posture anchor (docs/claim-ceiling.md:10). The bold ``**``
# ----  markdown around the line is tolerated. ----
_STANDING_CEILING_RE = re.compile(
    r"current\s+standing\s+ceiling:\s*\**\s*rung\s+(\d+)", re.IGNORECASE)

# ---- unauthorized governance-movement markers, applied ONLY to the appended delta
# ----  (committed history is the authorized truth and is never re-judged). S03 opens no
# ----  rung beyond 2, mints no SP-6, and promotes no value (OD-C8-2; PRD §6; SDD §10). ----
_UNAUTHORIZED_GOVERNANCE_RULES = [
    (re.compile(r"\brung[\s-]*(?:[3-9]|[1-9][0-9]+)\b", re.IGNORECASE),
     "Rung-3+ claim advance (S03 authorizes no rung beyond Rung 2)"),
    (re.compile(r"\bsp[\s-]?6\b", re.IGNORECASE),
     "SP-6 promotion (S03 mints no SP-6)"),
    (re.compile(r"\bvalue[\s-]*promot\w*", re.IGNORECASE),
     "value promotion (S03 promotes no value)"),
    (re.compile(r"\bpromot\w*[\s-]*value\b", re.IGNORECASE),
     "value promotion (S03 promotes no value)"),
    (re.compile(r"\bclaim[\s-]*(?:ceiling[\s-]*)?advance\w*", re.IGNORECASE),
     "claim-ceiling advance (S03 advances no ceiling)"),
]


# =====================================================================================
# Pure helpers — no I/O, no git, no global state. Tests feed these strings directly so
# every check is exercisable without a git baseline or the gitignored runs/ tree.
# =====================================================================================

def _normalize_lf(text: str) -> str:
    """LF-normalize content for a portable byte comparison.

    The repo runs ``core.autocrlf=true`` with no ``.gitattributes``: the working-tree
    bytes are CRLF on a Windows checkout and LF on Linux, but the COMMITTED blob (what
    ``git show`` yields) is LF either way. Normalizing both sides to LF makes the
    append-only "byte-identical prefix" check a portable CONTENT-prefix check — the same
    rationale as the V001 byte-unchanged smoke (``tests/test_smokes.py``)."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _table_rows(text: str) -> "list[str]":
    """The markdown table lines (those starting with ``|``), in order. The ledger holds
    exactly one table; the first row is the header, the second the separator, the rest
    data rows."""
    return [ln.strip() for ln in text.splitlines() if ln.strip().startswith("|")]


def _split_cells(row: str):
    """Split a ``| a | b | ... |`` markdown row into stripped cell values, or None if the
    line is not a bounded table row.

    # loa:shortcut: assumes no escaped ``\\|`` inside a cell — the house ledger format
    # uses none (a pipe cannot appear unescaped in a markdown cell). Upgrade trigger: if
    # a future legitimate ledger cell needs a literal pipe, switch to an escape-aware
    # split; until then a plain split is the smallest correct parser."""
    s = row.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return None
    return [c.strip() for c in s.split("|")[1:-1]]


def validate_ledger_structure(text: str) -> "list[tuple[int, str]]":
    """Table-discipline + per-row schema checks (no baseline needed). Returns a list of
    ``(exit_code, reason)`` violations; empty ⇒ structurally valid."""
    out: "list[tuple[int, str]]" = []
    rows = _table_rows(text)
    if len(rows) < 2:
        out.append((EXIT_STRUCTURE,
                    "no ledger table found (need a header row and a separator row)"))
        return out

    header = _split_cells(rows[0])
    separator = _split_cells(rows[1])
    data_rows = [(_split_cells(r), r) for r in rows[2:]]

    # ---- one consistent header, matching the house schema verbatim (header edit ⇒ reject) ----
    if header != list(LEDGER_COLUMNS):
        out.append((EXIT_STRUCTURE,
                    f"header does not match the {N_COLUMNS}-column house schema verbatim "
                    f"(edited/reordered/renamed header). Expected {list(LEDGER_COLUMNS)}, "
                    f"got {header}"))

    # ---- separator row present, 18-wide, every cell a dash-run ----
    if separator is None:
        out.append((EXIT_STRUCTURE, "missing markdown separator row after the header"))
    else:
        if len(separator) != N_COLUMNS:
            out.append((EXIT_STRUCTURE,
                        f"separator row has {len(separator)} columns, expected {N_COLUMNS}"))
        bad_sep = [c for c in separator if not _SEPARATOR_CELL_RE.match(c)]
        if bad_sep:
            out.append((EXIT_STRUCTURE,
                        f"malformed separator cells (expected dash-runs like '---'): {bad_sep}"))

    if not data_rows:
        out.append((EXIT_STRUCTURE, "ledger has a header/separator but no data rows"))

    # ---- per data-row checks ----
    for cells, raw in data_rows:
        ref = (raw[:48] + "…") if len(raw) > 49 else raw
        if cells is None:
            out.append((EXIT_STRUCTURE, f"malformed table row (not pipe-bounded): {ref}"))
            continue
        if len(cells) != N_COLUMNS:
            out.append((EXIT_STRUCTURE,
                        f"row has {len(cells)} cells, expected {N_COLUMNS}: {ref}"))
            continue  # column-shape unknown ⇒ skip cell-position checks for this row

        # claim_ceiling must be non-empty (the only ceiling-bearing column; docs/ledger.md:3-6)
        if not cells[CLAIM_CEILING_COL]:
            out.append((EXIT_GOVERNANCE, f"empty claim_ceiling cell (required non-empty): {ref}"))

        # single regime per row (a two-regime row is a cross-regime structural refusal, NFR-5)
        n_regime = len(_REGIME_TOKEN_RE.findall(cells[REGIME_COL]))
        if n_regime != 1:
            out.append((EXIT_STRUCTURE,
                        f"regime_id cell names {n_regime} regimes, expected exactly 1 "
                        f"(no cross-regime row; NFR-5): '{cells[REGIME_COL]}'"))

        # git_rev must be a git digest (40-hex SHA-1 or 64-hex SHA-256)
        if not _GIT_REV_RE.match(cells[GIT_REV_COL]):
            out.append((EXIT_GOVERNANCE,
                        f"git_rev is not a git digest (40/64-hex): '{cells[GIT_REV_COL]}'"))

        # any 'sha256 <token>' citation, in any cell, must be a 64-hex SHA-256 digest
        for cell in cells:
            for m in _SHA256_CITATION_RE.finditer(cell):
                token = m.group(1)
                if not _SHA256_RE.match(token):
                    out.append((EXIT_GOVERNANCE,
                                f"non-SHA-256 digest where one is cited ('sha256 {token}'): {ref}"))
    return out


def classify_append(baseline_text: str, worktree_text: str) -> "tuple[str, str]":
    """Append-only classification on LF-normalized content (RN-1). Returns:
      ("equal", "")            — working tree == committed baseline;
      ("append", delta_text)   — baseline is a byte-identical prefix; delta is the appended tail;
      ("edit", "")             — a prior committed line was changed (prefix broken)."""
    b = _normalize_lf(baseline_text)
    w = _normalize_lf(worktree_text)
    if w == b:
        return ("equal", "")
    if w.startswith(b):
        return ("append", w[len(b):])
    return ("edit", "")


def scan_unauthorized_governance(text: str) -> "list[tuple[int, str]]":
    """Scan a chunk of (appended) ledger text for unauthorized governance-movement
    markers. Returns ``(EXIT_GOVERNANCE, reason)`` violations."""
    out: "list[tuple[int, str]]" = []
    for rx, reason in _UNAUTHORIZED_GOVERNANCE_RULES:
        if rx.search(text):
            out.append((EXIT_GOVERNANCE,
                        f"unauthorized governance movement in appended ledger content: {reason}"))
    return out


def validate_claim_ceiling(text: str) -> "list[tuple[int, str]]":
    """Confirm the standing claim ceiling reads **Rung 2** (no advance/regression). Returns
    ``(exit_code, reason)`` violations; empty ⇒ Rung 2 held."""
    m = _STANDING_CEILING_RE.search(text)
    if not m:
        return [(EXIT_GOVERNANCE,
                 "claim-ceiling: cannot find 'Current standing ceiling: Rung N' — "
                 "cannot confirm Rung 2 is held (fail-closed)")]
    rung = int(m.group(1))
    if rung != 2:
        return [(EXIT_GOVERNANCE,
                 f"claim-ceiling advance/regression: standing ceiling reads Rung {rung}, "
                 f"expected Rung 2 (S03 authorizes no advance)")]
    return []


# =====================================================================================
# Read-only I/O layer — file reads + read-only git reads (subprocess; stdlib).
# =====================================================================================

def _repo_rel_posix(path) -> str:
    """Repo-relative POSIX path for ``git show <ref>:<path>``; falls back to a
    slash-normalized string for a path outside the repo."""
    try:
        return Path(path).resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path).replace("\\", "/").lstrip("./")


def git_show(ref: str, repo_rel_path: str) -> "str | None":
    """Read-only ``git show <ref>:<repo_rel_path>``; None if git is unavailable or the
    object does not exist at the ref (baseline unreachable ⇒ caller fails closed)."""
    try:
        # encoding="utf-8" is load-bearing: the default text mode decodes git's stdout
        # with the system locale (cp1252 on Windows), which mangles the ledger's UTF-8
        # em-dashes and breaks the byte-prefix comparison. The blob is UTF-8.
        r = subprocess.run(["git", "show", f"{ref}:{repo_rel_path}"], cwd=str(REPO_ROOT),
                           capture_output=True, text=True, encoding="utf-8", timeout=15)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    return r.stdout


def git_hash_object(path) -> "str | None":
    """Read-only ``git hash-object <path>`` (the LF-normalized governance hash); None on
    error. Stdlib subprocess; no network."""
    try:
        r = subprocess.run(["git", "hash-object", str(path)], cwd=str(REPO_ROOT),
                           capture_output=True, text=True, encoding="utf-8", timeout=15)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    return (r.stdout.strip() or None)


def _read_text(path) -> "str | None":
    """Read a file as text (universal-newline ⇒ LF-normalized); None if missing/unreadable."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


# =====================================================================================
# Orchestration + CLI (exit 0/1/2/3; read-only).
# =====================================================================================

_UNSET = object()  # sentinel: distinguish "fetch baseline from git" from "baseline is None"


def validate(ledger_path: str, claim_ceiling_path: str, *, baseline_ref: str = "HEAD",
             baseline_text=_UNSET, expected_ledger_hash: "str | None" = None,
             expected_ceiling_hash: "str | None" = None) -> "tuple[int, list[tuple[int, str]]]":
    """Run the full read-only gate. Returns ``(exit_code, violations)`` where exit_code is
    the max severity among triggered violations (3 > 2 > 1 > 0) and violations is the full
    ``(code, reason)`` list (nothing is hidden — every failure is reported).

    ``baseline_text`` is the append-only committed baseline. Left unset (the default,
    used by the CLI), it is fetched read-only via ``git show <baseline_ref>:<ledger>``;
    a test may inject a string (to exercise append/edit/equal deterministically) or
    ``None`` (to exercise the fail-closed unreachable-baseline path)."""
    violations: "list[tuple[int, str]]" = []

    # ---- ledger ----
    ledger_text = _read_text(ledger_path)
    if ledger_text is None:
        violations.append((EXIT_INPUT, f"cannot read ledger '{ledger_path}' (input failure)"))
    else:
        violations.extend(validate_ledger_structure(ledger_text))

        # append-only via the committed baseline (RN-1); fail-closed if unreachable.
        baseline = (git_show(baseline_ref, _repo_rel_posix(ledger_path))
                    if baseline_text is _UNSET else baseline_text)
        if baseline is None:
            violations.append((EXIT_INPUT,
                               f"append-only: committed baseline 'git show {baseline_ref}:"
                               f"{_repo_rel_posix(ledger_path)}' is unreachable — fail-closed "
                               f"(RN-1; never a silent pass)"))
        else:
            status, delta = classify_append(baseline, ledger_text)
            if status == "edit":
                violations.append((EXIT_GOVERNANCE,
                                   "append-only violation: the committed baseline is not a "
                                   "byte-identical prefix — a prior row / header / separator / "
                                   "historical line was edited (RN-1)"))
            elif status == "append":
                violations.extend(scan_unauthorized_governance(delta))

        # opt-in pinned-hash integrity assertion.
        if expected_ledger_hash:
            got = git_hash_object(ledger_path)
            if got is None:
                violations.append((EXIT_INPUT,
                                   f"cannot compute git hash-object of '{ledger_path}' to check "
                                   f"the pinned hash (fail-closed)"))
            elif got != expected_ledger_hash:
                violations.append((EXIT_GOVERNANCE,
                                   f"ledger hash mismatch: git hash-object = {got}, expected "
                                   f"{expected_ledger_hash} (file is not at the pinned bytes)"))

    # ---- claim ceiling ----
    ceiling_text = _read_text(claim_ceiling_path)
    if ceiling_text is None:
        violations.append((EXIT_INPUT,
                           f"cannot read claim-ceiling '{claim_ceiling_path}' (input failure)"))
    else:
        violations.extend(validate_claim_ceiling(ceiling_text))
        if expected_ceiling_hash:
            got = git_hash_object(claim_ceiling_path)
            if got is None:
                violations.append((EXIT_INPUT,
                                   f"cannot compute git hash-object of '{claim_ceiling_path}' to "
                                   f"check the pinned hash (fail-closed)"))
            elif got != expected_ceiling_hash:
                violations.append((EXIT_GOVERNANCE,
                                   f"claim-ceiling hash mismatch: git hash-object = {got}, "
                                   f"expected {expected_ceiling_hash} (file is not at the pinned bytes)"))

    code = max((c for c, _ in violations), default=EXIT_OK)
    return code, violations


def main(argv=None) -> int:
    try:  # robust output regardless of console codepage (Windows cp1252)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

    ap = argparse.ArgumentParser(
        description="Offline, read-only ledger-row + claim-ceiling governance gate "
                    "(reports whether ledger mechanics are valid; blesses no rung).")
    ap.add_argument("ledger_pos", nargs="?", default=None,
                    help=f"path to the ledger (positional; default {DEFAULT_LEDGER})")
    ap.add_argument("--ledger", default=DEFAULT_LEDGER,
                    help=f"path to the ledger (default {DEFAULT_LEDGER})")
    ap.add_argument("--claim-ceiling", default=DEFAULT_CLAIM_CEILING,
                    help=f"path to the claim-ceiling doc (default {DEFAULT_CLAIM_CEILING})")
    ap.add_argument("--baseline-ref", default="HEAD",
                    help="git ref for the append-only committed baseline (default HEAD)")
    ap.add_argument("--expected-ledger-hash", default=None,
                    help="assert git hash-object of the ledger equals this pinned value")
    ap.add_argument("--expected-ceiling-hash", default=None,
                    help="assert git hash-object of the claim-ceiling equals this pinned value")
    args = ap.parse_args(argv)

    ledger_path = args.ledger_pos or args.ledger
    code, violations = validate(
        ledger_path, args.claim_ceiling,
        baseline_ref=args.baseline_ref,
        expected_ledger_hash=args.expected_ledger_hash,
        expected_ceiling_hash=args.expected_ceiling_hash,
    )

    if violations:
        print(f"ledger_validate: INVALID — {len(violations)} issue(s) "
              f"(exit {code}; fail-closed):", file=sys.stderr)
        for c, reason in violations:
            print(f"  REJECT[{c}]  {reason}", file=sys.stderr)
        return code

    print(f"ledger_validate: VALID — '{ledger_path}' is schema/append-only/regime/digest "
          f"clean and '{args.claim_ceiling}' holds Rung 2 (exit 0). Wrote nothing.",
          file=sys.stderr)
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
