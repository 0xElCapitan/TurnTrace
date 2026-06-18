"""Internal sim/ helpers — path + config resolution and deck loading.

Lives inside ``sim/`` (the single blast radius; SDD §1.4). It does **not**
import cabt itself: it only resolves the local, git-ignored Competition-Data
paths (CC-1/CC-2) that ``sim/adapter.py`` and ``sim/probe.py`` use to import
``cg`` and read the deck. Keeping this here avoids any cross-zone import (the
runtime/offline import rule; SDD §1.6).

stdlib only (NFR-7).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

# Repo root = the directory two levels up from this file (``<root>/sim/_env.py``).
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "config" / "eval_config.json"


def load_config(path: "Path | None" = None) -> dict:
    """Load ``config/eval_config.json`` if present; return {} otherwise."""
    cfg_path = path or DEFAULT_CONFIG
    if cfg_path.exists():
        with open(cfg_path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def _resolve(p: str) -> Path:
    pp = Path(p)
    return pp if pp.is_absolute() else (REPO_ROOT / pp)


def resolve_cg_dir(cfg: "dict | None" = None) -> Path:
    """Directory that contains the ``cg`` package (env > config)."""
    cfg = cfg if cfg is not None else load_config()
    val = os.environ.get("TURNTRACE_CG_DIR") or cfg.get("cg_dir")
    if not val:
        raise RuntimeError(
            "cg_dir not configured — set TURNTRACE_CG_DIR or config/eval_config.json:cg_dir"
        )
    return _resolve(val)


def resolve_deck_file(cfg: "dict | None" = None) -> Path:
    """Path to the local (git-ignored) starter deck CSV (env > config)."""
    cfg = cfg if cfg is not None else load_config()
    val = os.environ.get("TURNTRACE_DECK_FILE") or cfg.get("deck_file")
    if not val:
        raise RuntimeError(
            "deck_file not configured — set TURNTRACE_DECK_FILE or config/eval_config.json:deck_file"
        )
    return _resolve(val)


def read_deck(deck_file: Path) -> "list[int]":
    """Read the first 60 card IDs (one int per line) from a deck CSV.

    The returned IDs are Competition Data (CC-1/CC-2): callers MUST NOT write
    them into any tracked artifact. They exist only to drive a match and to
    compute a deck content hash.
    """
    with open(deck_file, "r", encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    return [int(lines[i]) for i in range(60)]
