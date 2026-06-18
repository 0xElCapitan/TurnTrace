#!/usr/bin/env python3
"""``eval/mirror_validate.py`` — pre-submission mirror validation (PR-18, Task 01.5).

A local stand-in for Kaggle's hosted **Validation Episode**: play the candidate
agent against a copy of itself for one full match and confirm it completes with
**no error and no illegal action**, exercising the actual submission entry point
``agent(obs_dict) -> list[int]`` (the contract the host calls — cg sample
``main.py``), not the in-process ``select`` shim. Reports **pass/fail** before any
submission packaging (PRD §8.3).

No network call happens during the match (CC-3 / NFR-8); packaging
(``tar -czvf submission.tar.gz *`` with ``main.py`` + ``deck.csv``) stays an
operator action, not a harness one (CC-5; SDD §1.8). This validator writes **no
run dir and no ledger row** — it is a smoke, not a deliverable run.

`eval/` may import ``sim`` + ``agents/runtime`` (the import-direction rule;
SDD §1.6). stdlib only (NFR-7).

CLI:  python eval/mirror_validate.py                       # candidate = scripted_baseline
      python eval/mirror_validate.py --agent random_legal
Exit: 0 PASS · 1 FAIL (crash / illegal action / non-termination) · 2 env/agent setup failure.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
for _sub in ("sim", "agents/runtime", "eval"):
    sys.path.insert(0, str(REPO_ROOT / _sub))

from adapter import SimAdapter  # noqa: E402  (sim/ — allowed)
from run_match import AGENTS  # noqa: E402  (eval/ — intra-zone agent registry)
from _env import load_config, read_deck, resolve_deck_file  # noqa: E402  (sim/_env)

MAX_DECISIONS = 20000

# The submission candidate defaults to the Sprint 01 scripted baseline.
DEFAULT_AGENT = "scripted_baseline"


def play_mirror_match(adapter: SimAdapter, candidate, deck: "list[int]") -> dict:
    """Play candidate-vs-self for one full match via the ``agent(obs_dict)``
    submission contract. Returns a result dict (no files written)."""
    obs = adapter.start_match(deck, deck)
    decisions = 0
    invalid_action = False
    error = None
    result_int = None
    try:
        for _ in range(MAX_DECISIONS):
            done, result_int, _reason = adapter.terminal(obs)
            if done:
                break
            if adapter.is_deck_selection(obs):
                # Deck-selection step is the host/runner's job, never the agent's
                # (probe: select is never None locally; defensive parity with run_match).
                obs = adapter.step(list(deck))
                continue
            try:
                selection = candidate.agent(obs)  # the submission entry point
            except Exception as exc:  # noqa: BLE001  agent raised on a live obs
                error = f"agent raised: {type(exc).__name__}: {exc}"
                break
            decisions += 1
            try:
                obs = adapter.step(selection)
            except Exception as exc:  # noqa: BLE001  sim rejected the selection (illegal)
                invalid_action = True
                error = f"illegal selection: {type(exc).__name__}: {exc}"
                break
        else:
            error = f"match did not terminate within {MAX_DECISIONS} decisions"
    finally:
        adapter.finish()

    completed = error is None and result_int is not None
    return {
        "completed": completed,
        "decisions": decisions,
        "invalid_action": invalid_action,
        "result_int": result_int,
        "error": error,
        "passed": completed and not invalid_action,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Pre-submission mirror validation (candidate vs self).")
    ap.add_argument("--agent", default=DEFAULT_AGENT,
                    help=f"submission candidate agent (default: {DEFAULT_AGENT})")
    args = ap.parse_args(argv)

    # ---- env / agent setup (exit 2 on failure) ----
    try:
        if args.agent not in AGENTS:
            raise KeyError(f"unknown agent {args.agent!r} (known: {sorted(AGENTS)})")
        candidate = AGENTS[args.agent]
        cfg = load_config()
        deck = read_deck(resolve_deck_file(cfg))
        adapter = SimAdapter(cfg=cfg)
    except Exception as e:  # noqa: BLE001
        print(f"mirror_validate: setup failed: {e}", file=sys.stderr)
        return 2

    res = play_mirror_match(adapter, candidate, deck)
    verdict = "PASS" if res["passed"] else "FAIL"
    print(f"mirror_validate: {verdict} — agent={args.agent} candidate-vs-self "
          f"decisions={res['decisions']} invalid_action={res['invalid_action']} "
          f"completed={res['completed']}"
          + (f" error={res['error']}" if res["error"] else ""),
          file=sys.stderr)
    return 0 if res["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
