"""``scripted_baseline`` runtime agent — PR-13, Task 01.4 (SDD §1.6, §5.2).

The frozen, **deterministic** baseline: a fixed priority policy that, holding
the selection *count* identical to ``random_legal``, replaces random choice with
a deterministic one. The priority is the simplest defensible one the in-process
contract can express — **lowest offered index first** — so the same offered
option set always yields the same selection (AC-04). A *pure function of the
offered-option shape* (no RNG, no cross-move state, no scoring, no network;
CC-3 / NFR-8); no imports from ``analysis/``, ``eval/``, or ``cabt`` (NFR-1).

This is **not** a tuned policy: there is no scoring, no win-probability, no
lookahead, and no per-option-type preference table (the in-process ``select``
contract carries only counts, not option types — by design, so no scoring can
leak onto the runtime path; SDD §1.6). It is the single deliberate, *trivial*,
one-variable change vs ``random_legal`` for the first comparison (run-0002 vs
run-0001 under the same ``regime-v001``): identical count, random → deterministic.

It earns NO gameplay-strength claim. The ledger ceiling bounds interpretation;
forbidden agent claim words (strong / competitive / optimal / calibrated /
complete) do not apply (PRD §9; loop contract §8).

Two entry points, mirroring ``random_legal``:
  * ``select(n_options, min_count, max_count, rng)`` — the in-process contract
    the local runner calls; takes only the legal-offer shape.
  * ``agent(obs_dict)`` — the Kaggle/cabt submission contract
    (``agent(obs_dict) -> list[int]``); used by mirror validation (PR-18).

stdlib only (NFR-7).
"""

from __future__ import annotations

AGENT_ID = "scripted_baseline"
AGENT_VERSION = "scripted-v001"


def select(n_options: int, min_count: int, max_count: int,
           rng=None) -> "list[int]":
    """Return the first ``max_count`` option indices: ``[0, 1, …, k-1]``.

    Deterministic by construction — no RNG is consulted (the ``rng`` parameter
    exists only for signature parity with ``random_legal``). ``max_count`` never
    exceeds ``n_options`` per the cabt contract; the clamp is belt-and-braces and
    matches ``random_legal`` exactly, so the *count* of the selection is identical
    and the only variable between the two agents is random vs deterministic choice.
    """
    k = max_count if max_count <= n_options else n_options
    if k <= 0:
        return []
    return list(range(k))


def agent(obs_dict: dict) -> "list[int]":
    """Kaggle/cabt submission contract: ``agent(obs_dict) -> list[int]``.

    Reads the obs dict's public ``select`` fields only. The initial
    deck-selection step (``select is None``) is owned by the host / runner, not
    this agent (same boundary as ``random_legal``).
    """
    sel = obs_dict.get("select")
    if sel is None:
        raise ValueError(
            "scripted_baseline.agent: select is None (deck-selection step is the "
            "runner's responsibility, not the agent's)"
        )
    options = sel.get("option") or []
    return select(len(options), sel.get("minCount", 0), sel.get("maxCount", 0))
