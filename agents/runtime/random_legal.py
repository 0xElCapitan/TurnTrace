"""``random_legal`` runtime agent — PR-2, Task 00.3 (SDD §1.4, §5.2).

The floor baseline: select uniformly among the offered legal options. A **pure
function of (observation, RNG)** — no cross-move state, no scoring, no network
(CC-3 / NFR-8), no imports from ``analysis/``, ``eval/``, or ``cabt``. This is
the runtime side (NFR-1): fast and dumb.

Two entry points:
  * ``select(n_options, min_count, max_count, rng)`` — the in-process contract
    the local runner calls; takes only the legal-offer shape, so the agent
    never parses a cabt observation.
  * ``agent(obs_dict)`` — the Kaggle/cabt submission contract
    (``agent(obs_dict) -> list[int]``; cg sample main.py). Reads the obs dict's
    public ``select`` fields only; used later for mirror validation (PR-18).

stdlib only (NFR-7).
"""

from __future__ import annotations

import random

AGENT_ID = "random_legal"
AGENT_VERSION = "random_legal-v001"


def select(n_options: int, min_count: int, max_count: int,
           rng: "random.Random | None" = None) -> "list[int]":
    """Return ``max_count`` distinct option indices in ``[0, n_options)``.

    Mirrors the cg sample (``random.sample(range(len(option)), maxCount)``),
    clamped so it is total over every offered option set. ``max_count`` never
    exceeds ``n_options`` per the cabt contract; the clamp is belt-and-braces.
    """
    rng = rng or random
    k = max_count if max_count <= n_options else n_options
    if k <= 0:
        return []
    return rng.sample(range(n_options), k)


def agent(obs_dict: dict) -> "list[int]":
    """Kaggle/cabt submission contract: ``agent(obs_dict) -> list[int]``.

    The local Sprint 00 harness drives matches via :func:`select`; this function
    exists for the hosted contract and Sprint 01's mirror validation (PR-18).
    The initial deck-selection step (``select is None``) is owned by the host /
    runner, not this agent.
    """
    sel = obs_dict.get("select")
    if sel is None:
        raise ValueError(
            "random_legal.agent: select is None (deck-selection step is the "
            "runner's responsibility, not the agent's)"
        )
    options = sel.get("option") or []
    return select(len(options), sel.get("minCount", 0), sel.get("maxCount", 0))
