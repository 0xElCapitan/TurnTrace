#!/usr/bin/env python3
"""Runtime/offline import-direction check (Task 00.2/00.5; SDD §1.6, NFR-1).

Static (AST) enforcement of the dependency rule that keeps the per-move runtime
path fast and the offline analysis out of `cabt`:

  runtime   (agents/runtime/) → stdlib only — no sim/eval/analysis/cabt
  sim       (sim/)            → cabt + sim only
  eval      (eval/)           → sim + runtime + analysis + eval (NOT cabt directly)
  analysis  (analysis/)       → analysis only (reads run artifacts; no cabt/sim/runtime)

Run:  python tests/test_import_direction.py   (exit 0 ok / 1 violation)
stdlib only (NFR-7).
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ZONE_DIRS = {
    "runtime": REPO_ROOT / "agents" / "runtime",
    "sim": REPO_ROOT / "sim",
    "eval": REPO_ROOT / "eval",
    "analysis": REPO_ROOT / "analysis",
}

# allowed cross-zone import targets (intra-zone is always allowed and added below)
ALLOWED = {
    "runtime": set(),
    "sim": {"cabt"},
    "eval": {"sim", "runtime", "analysis"},
    "analysis": set(),
}


def _module_zone_map() -> dict:
    m = {"cg": "cabt"}
    for zone, d in ZONE_DIRS.items():
        if d.exists():
            for p in d.glob("*.py"):
                m[p.stem] = zone
    return m


def _top_imports(path: Path) -> "set[str]":
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                names.add(node.module.split(".")[0])
    return names


def check() -> "list[str]":
    module_zone = _module_zone_map()
    violations = []
    for zone, d in ZONE_DIRS.items():
        if not d.exists():
            continue
        allowed = ALLOWED[zone] | {zone}
        for src in sorted(d.glob("*.py")):
            for name in sorted(_top_imports(src)):
                tgt_zone = module_zone.get(name)
                if tgt_zone is None:
                    continue  # stdlib / unzoned — fine
                if tgt_zone not in allowed:
                    violations.append(
                        f"{src.relative_to(REPO_ROOT)} ({zone}) imports '{name}' "
                        f"({tgt_zone}) — forbidden; {zone} may import {sorted(allowed)}"
                    )
    return violations


def main() -> int:
    v = check()
    if v:
        for x in v:
            print(f"IMPORT-DIRECTION VIOLATION: {x}", file=sys.stderr)
        return 1
    print("import-direction: OK — runtime/offline separation intact", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
