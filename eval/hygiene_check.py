#!/usr/bin/env python3
"""``eval/hygiene_check.py`` — Competition-Data staging guard (Task 00.10; CC-1/CC-2).

The mechanical control behind the load-bearing safety rule: **no Competition
Data ever enters git** (SDD §4.5, Risk R1). It refuses any path that carries
Pokémon Elements or a raw generated run tree:

  * the `cg/` simulator lib (`cg/…`, `cg.dll`, `libcg.so`)
  * `deck.csv` / raw deck card-lists, card-data CSV/PDF
  * anything under `grimoires/loa/context/` (the local Competition-Data home)
  * raw run trees `runs/<run_id>/…` (ESP-1: local by default; only sanitized
    summaries/ledger rows are tracked, and only with operator approval)

Wire it as a pre-commit hook (the operator installs it; we don't touch
`.claude/`):

    ln -s ../../eval/hygiene_check.py .git/hooks/pre-commit   # or a wrapper

Modes:
  python eval/hygiene_check.py                 # scan git-staged files (pre-commit)
  python eval/hygiene_check.py --paths a b c   # check explicit paths (smoke/testing)
Exit: 0 clean · 1 a Competition-Data path was found. stdlib only (NFR-7).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# (compiled regex over the POSIX-style path, human reason)
_RULES = [
    (re.compile(r"(^|/)cg/"), "cg/ simulator lib (Competition Data)"),
    (re.compile(r"(^|/)cg\.dll$"), "cabt native lib"),
    (re.compile(r"(^|/)libcg\.so$"), "cabt native lib"),
    (re.compile(r"(^|/)deck\.csv$"), "raw deck list (Competition Data)"),
    (re.compile(r"\.pdf$", re.IGNORECASE), "PDF (possible card data / rulebook)"),
    (re.compile(r"(^|/)__MACOSX/"), "macOS archive cruft from the Competition bundle"),
    (re.compile(r"^grimoires/loa/context/"), "local Competition-Data home (CC-1)"),
    (re.compile(r"^runs/[^/]+/.+"), "raw generated run tree (ESP-1: local by default)"),
    (re.compile(r"card.*\.csv$", re.IGNORECASE), "possible card-data CSV"),
]


def _norm(p: str) -> str:
    return p.replace("\\", "/").lstrip("./")


def find_violations(paths) -> "list[tuple[str, str]]":
    out = []
    for raw in paths:
        p = _norm(str(raw))
        if not p:
            continue
        for rx, reason in _RULES:
            if rx.search(p):
                out.append((p, reason))
                break
    return out


def staged_paths() -> "list[str]":
    try:
        r = subprocess.run(["git", "diff", "--cached", "--name-only"],
                           cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=15)
        return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]
    except Exception:  # noqa: BLE001
        return []


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if argv and argv[0] == "--paths":
        paths = argv[1:]
        source = "explicit paths"
    else:
        paths = staged_paths()
        source = "git-staged files"

    violations = find_violations(paths)
    if violations:
        print("COMPETITION-DATA HYGIENE: refusing — these paths must NEVER be committed "
              "(CC-1/CC-2, ESP):", file=sys.stderr)
        for p, reason in violations:
            print(f"  BLOCKED  {p}  — {reason}", file=sys.stderr)
        print("If this is a sanitized, operator-approved artifact, the operator must "
              "stage it deliberately and update the policy. Default is: do not commit.",
              file=sys.stderr)
        return 1
    print(f"hygiene_check: clean — no Competition-Data paths in {source} "
          f"({len(paths)} checked)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
