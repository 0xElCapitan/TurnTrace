#!/usr/bin/env python3
"""``eval/run_match.py`` — one match → record + trace (PR-1/3/4, Task 00.5).

Plays a single match under a **fully declared** input set and emits one
``match-summary.json`` plus one ``decision-trace.jsonl`` sidecar. Refuses to run
if any required input is missing (PR-1). Computes ``trace_hash`` over the
canonical trace so the summary↔trace join (AC-3) holds. An in-match crash is
recorded as ``result="error"`` and is **never** counted as a loss (FM-01 guard;
SDD §6.1).

Capability-shaped by the probe (sim/capabilities.json): seeds are uncontrolled
(``seed=null``, ``match_index`` carries identity, ``mode=unseeded``); no time
budget is published (``timeout=null``); invalid actions are detectable.

Exit codes (CLI): 0 ok · 1 env/input-load failure · 2 agent-init failure
(SDD §5.3). stdlib only (NFR-7).

CLI (single-match smoke):
  python eval/run_match.py --match-index 1 --run-id run-smoke \\
      --match-id M0001 --out-dir runs/run-smoke
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

REPO_ROOT = Path(__file__).resolve().parent.parent
for _sub in ("sim", "agents/runtime", "eval"):
    sys.path.insert(0, str(REPO_ROOT / _sub))

from adapter import SimAdapter  # noqa: E402  (sim/ — allowed: eval may import sim)
import random_legal as random_legal_agent  # noqa: E402  (agents/runtime — allowed)
from canonical_json import canonical_dumps, hash_canonical, sha256_hex  # noqa: E402
from _env import load_config, read_deck, resolve_deck_file  # noqa: E402 (sim/_env)

MAX_DECISIONS = 20000
LEGAL_SAMPLE_K = 5

REQUIRED_INPUTS = (
    "agent_a_id", "agent_b_id", "deck_a_id", "deck_b_id",
    "match_index", "regime_id", "run_id", "match_id",
    "opponent_id", "agent_version",
)

# Agent registry — Sprint 00 ships only random_legal (both sides; mirror).
AGENTS = {"random_legal": random_legal_agent}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def deck_hash(deck: "list[int]") -> str:
    """Content hash of a deck's card-id list (drift detection). The hash, not
    the ids, is what may ever leave the local machine (CC-1/CC-2)."""
    return hash_canonical(deck)


def _check_required(inputs: dict) -> None:
    missing = [k for k in REQUIRED_INPUTS if inputs.get(k) in (None, "")]
    if missing:
        raise ValueError(f"run_match: missing required inputs: {missing}")


def play_match(adapter: SimAdapter, agents: dict, decks: "tuple[list, list]",
               inputs: dict, caps: dict, rng) -> dict:
    """Drive one match. Returns {"summary": {...}, "trace": [rows...]}.

    ``agents`` maps player index (0/1) → agent module. Player 0 is the agent
    under test (its perspective defines ``result``).
    """
    flags = caps.get("flags", {})
    invalid_detectable = bool(flags.get("invalid_action_detectable"))
    sim_version = caps.get("sim_version")
    sim_version_source = caps.get("sim_version_source")

    run_id, match_id, regime_id = inputs["run_id"], inputs["match_id"], inputs["regime_id"]
    trace: "list[dict]" = []
    invalid_action_count = 0
    agent_decision_count = 0
    last_turn = 0
    error_msg = None
    result_int = None
    reason_int = None

    started_at = _now()
    t0 = perf_counter()
    obs = adapter.start_match(decks[0], decks[1])
    try:
        for _ in range(MAX_DECISIONS):
            done, result_int, reason_int = adapter.terminal(obs)
            if done:
                break
            if adapter.is_deck_selection(obs):
                # Never observed locally (probe: select is never None); defensive only.
                obs = adapter.step(list(decks[adapter.your_index(obs) or 0]))
                continue

            yi = adapter.your_index(obs)
            player = "agent" if yi == 0 else "opponent"
            legal = adapter.legal_options(obs)
            last_turn = adapter.turn(obs) or last_turn

            agent_mod = agents[yi]
            d0 = perf_counter()
            selection = agent_mod.select(legal["n_options"], legal["min_count"],
                                         legal["max_count"], rng)
            latency_ms = int(round((perf_counter() - d0) * 1000))

            option_types = adapter.selected_action_view(obs, selection)["option_types"]
            row = {
                "record_type": "decision",
                "run_id": run_id, "match_id": match_id, "regime_id": regime_id,
                "decision_index": len(trace),
                "turn": adapter.turn(obs),
                "player": player,
                "phase": adapter.select_context(obs),
                "public_state_summary": adapter.public_summary(obs),
                # own observable state ONLY for the agent under test (no opponent leakage)
                "private_state_summary": adapter.private_summary(obs) if player == "agent" else None,
                "legal_actions_count": legal["n_options"],
                "legal_actions_digest": adapter.legal_digest(obs),
                "legal_actions_sample": legal["option_types"][:LEGAL_SAMPLE_K],
                "selected_action": {"indices": list(selection), "option_types": option_types},
                "selected_action_type": option_types[0] if option_types else None,
                "decision_latency_ms": latency_ms,
                "random_seed": None,            # seed_controlled=false → audit-trail posture
                "error": None,
                "post_decision_observation": None,  # reconstructable from next row / terminal
            }
            trace.append(row)
            if player == "agent":
                agent_decision_count += 1

            try:
                obs = adapter.step(selection)
            except Exception as exc:  # noqa: BLE001  invalid action / sim rejection
                if invalid_detectable:
                    invalid_action_count += 1
                row["error"] = f"{type(exc).__name__}: {exc}"
                error_msg = row["error"]
                result_int = None  # outcome is error, not a loss (FM-01)
                break
        else:
            error_msg = f"match did not terminate within {MAX_DECISIONS} decisions"
    finally:
        adapter.finish()

    wall_clock_ms = int(round((perf_counter() - t0) * 1000))
    completed_at = _now()

    # ---- outcome (FM-01: an error is an error, never a masqueraded loss) ----
    if error_msg is not None or result_int is None:
        result_str = "error"
        ending_cause = "error"
        if error_msg is None:
            error_msg = "no terminal result observed"
    else:
        result_str = adapter.outcome_for_player(result_int, 0)
        ending_cause = adapter.ending_cause(reason_int)

    final_prizes = None
    pub = adapter.public_summary(obs)
    if pub and pub.get("players"):
        final_prizes = [p.get("prize_count") for p in pub["players"]]

    trace.append({
        "record_type": "terminal",
        "run_id": run_id, "match_id": match_id, "regime_id": regime_id,
        "decision_index": len(trace),
        "result": result_str,
        "ending_cause": ending_cause,
        "turns": last_turn,
        "final_prize_counts": final_prizes,
        "last_decision_index": len(trace) - 1,
    })

    trace_hash = hash_canonical(trace)

    summary = {
        "run_id": run_id, "match_id": match_id, "regime_id": regime_id,
        "experiment_id": None,
        "agent_id": inputs["agent_a_id"],
        "agent_version": inputs["agent_version"],
        "opponent_id": inputs["opponent_id"],
        "deck_id": inputs["deck_a_id"],
        "opponent_deck_id": inputs["deck_b_id"],
        "seed": None,                       # seed_controlled=false (probe)
        "seed_controlled": False,
        "match_index": inputs["match_index"],
        "result": result_str,
        "ending_cause": ending_cause,
        "turns": last_turn,
        "timeout": None,                    # timeout_detectable=false (probe)
        "invalid_action_count": invalid_action_count if invalid_detectable else None,
        "invalid_action_detectable": invalid_detectable,
        "total_decisions": agent_decision_count,
        "trace_present": True,
        "trace_hash": trace_hash,
        "started_at": started_at,
        "completed_at": completed_at,
        "wall_clock_ms": wall_clock_ms,
        "simulator_version": sim_version,
        "sim_version_source": sim_version_source,
        "deck_hash": inputs.get("deck_hash"),
        "error": error_msg,
        "notes": "mode=unseeded; seed_controlled=false; timeout undetectable (budget_source=assumed)",
    }
    return {"summary": summary, "trace": trace}


def write_match(out_dir: Path, match_id: str, result_obj: dict) -> "tuple[Path, Path]":
    """Write match_results/<id>.json + traces/<id>.jsonl. Returns the two paths."""
    mr_dir = out_dir / "match_results"
    tr_dir = out_dir / "traces"
    mr_dir.mkdir(parents=True, exist_ok=True)
    tr_dir.mkdir(parents=True, exist_ok=True)
    summary_path = mr_dir / f"{match_id}.json"
    trace_path = tr_dir / f"{match_id}.jsonl"
    with open(summary_path, "w", encoding="utf-8") as fh:
        fh.write(canonical_dumps(result_obj["summary"]))
        fh.write("\n")
    with open(trace_path, "w", encoding="utf-8") as fh:
        for row in result_obj["trace"]:
            fh.write(canonical_dumps(row))
            fh.write("\n")
    return summary_path, trace_path


def recompute_trace_hash(trace_path: Path) -> str:
    """Re-hash a sidecar from disk (AC-3 join check / replay)."""
    rows = []
    with open(trace_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                import json
                rows.append(json.loads(line))
    return hash_canonical(rows)


def run_single(inputs: dict, out_dir: Path, cfg: dict, deck_a, deck_b, rng) -> dict:
    """Build the adapter + agents and play one match (no file writing)."""
    _check_required(inputs)
    adapter = SimAdapter(cfg=cfg)
    caps = adapter.capabilities()
    agents = {0: AGENTS[inputs["agent_a_id"]], 1: AGENTS[inputs["agent_b_id"]]}
    return play_match(adapter, agents, (deck_a, deck_b), inputs, caps, rng)


def main(argv=None) -> int:
    import random
    ap = argparse.ArgumentParser(description="Play one TurnTrace match → record + trace.")
    ap.add_argument("--match-index", type=int, required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--match-id", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--regime-id", default="regime-v001")
    ap.add_argument("--agent", default="random_legal")
    ap.add_argument("--opponent", default="random_legal")
    ap.add_argument("--deck-id", default="deck-starter-v001")
    args = ap.parse_args(argv)

    # ---- env / input load (exit 1 on failure) ----
    try:
        cfg = load_config()
        deck = read_deck(resolve_deck_file(cfg))
    except Exception as e:  # noqa: BLE001
        print(f"run_match: env/input load failed: {e}", file=sys.stderr)
        return 1

    # ---- agent init (exit 2 on failure) ----
    try:
        if args.agent not in AGENTS or args.opponent not in AGENTS:
            raise KeyError(f"unknown agent(s): {args.agent}/{args.opponent}")
    except Exception as e:  # noqa: BLE001
        print(f"run_match: agent init failed: {e}", file=sys.stderr)
        return 2

    inputs = {
        "agent_a_id": args.agent, "agent_b_id": args.opponent,
        "deck_a_id": args.deck_id, "deck_b_id": args.deck_id,
        "match_index": args.match_index,
        "regime_id": args.regime_id, "run_id": args.run_id, "match_id": args.match_id,
        "opponent_id": args.opponent, "agent_version": random_legal_agent.AGENT_VERSION,
        "deck_hash": deck_hash(deck),
    }
    try:
        result_obj = run_single(inputs, Path(args.out_dir), cfg, deck, deck, random.Random())
    except ValueError as e:  # missing required inputs
        print(f"run_match: {e}", file=sys.stderr)
        return 1
    summary_path, trace_path = write_match(Path(args.out_dir), args.match_id, result_obj)
    s = result_obj["summary"]
    print(f"run_match: {args.match_id} result={s['result']} turns={s['turns']} "
          f"decisions={s['total_decisions']} trace_hash={s['trace_hash'][:12]} "
          f"-> {summary_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
