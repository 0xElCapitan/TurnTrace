#!/usr/bin/env python3
"""``eval/run_eval.py`` — N matches → one sealed, immutable run dir (PR-5/7, Task 00.8).

Drives ``random_legal`` over ``seed-set-v001`` against the single opponent under
``regime-v001`` into ONE append-only run directory, then writes the provenance
stamp and delegates aggregation. Responsibilities (SDD §1.4, §3.5):

  1. Allocate ``run_id`` + the expected ``match_id`` list and freeze them into
     ``manifest.json`` — the **authority** for ID allocation.
  2. **Immutability guard:** refuse to write into a populated run dir — a HARD
     error (exit 3), never a prompt (PR-5 / NFR-2). Validate every written
     ``match_id`` against the manifest (AC-9).
  3. Build ``hashes.txt`` (git_rev, sim_version, seed_list_hash, timestamp, +
     component hashes; AC-6) and ``notes.md`` (``mode``).
  4. Delegate ``summary.csv`` + the single ``ledger.md`` row to
     ``analysis/aggregate.py`` (offline; SDD lists it as a run_eval dependency).

Sprint 01 additions:
  * ``--agent`` selects the agent-under-test (player 0). Sprint 01 compares the
    frozen deterministic ``scripted_baseline`` (run-0002) against ``random_legal``
    (run-0001) under the SAME ``regime-v001`` — the single deliberate variable.
  * **O1 (provenance, Sprint 01 entry gate):** ``hashes.txt`` now records stable
    SHA-256 hashes of the runtime agent source(s) + the eval config — so a
    same-regime, agent-only comparison's provenance holds even with
    ``git_dirty=true`` (source-hash path; closeout O1 Option B).
  * **O2 (ledger footgun, Sprint 01 entry gate):** ``--no-ledger`` skips the
    ``docs/ledger.md`` append entirely (still writes ``summary.csv``). Review /
    test / non-deliverable runs MUST pass ``--no-ledger`` (or ``--ledger <tmp>``)
    so a stray run cannot contaminate the tracked ledger (closeout O2).

Exit codes: 0 ok · 1 env/input-load failure · 2 agent-init failure ·
3 immutability-guard refusal (populated dir). stdlib only (NFR-7).

CLI:  python eval/run_eval.py            # → runs/run-0001 (random_legal, deliverable)
      python eval/run_eval.py --run-id run-0002 --agent scripted_baseline
      python eval/run_eval.py --run-id run-x --no-ledger   # non-deliverable, no ledger row
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
for _sub in ("sim", "agents/runtime", "eval", "analysis"):
    sys.path.insert(0, str(REPO_ROOT / _sub))

import random  # noqa: E402
from adapter import SimAdapter  # noqa: E402  (sim/ — allowed)
from canonical_json import hash_canonical  # noqa: E402  (eval/)
from run_match import AGENTS, deck_hash as compute_deck_hash, run_single, write_match  # noqa: E402
from _env import load_config, read_deck, resolve_deck_file  # noqa: E402  (sim/_env)
import aggregate  # noqa: E402  (analysis/ — offline driver dependency; SDD §1.4)

FROZEN = REPO_ROOT / "frozen"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _git(args: "list[str]") -> str:
    try:
        out = subprocess.run(["git", *args], cwd=str(REPO_ROOT),
                             capture_output=True, text=True, timeout=15)
        return out.stdout.strip()
    except Exception:  # noqa: BLE001
        return ""


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _is_populated(run_dir: Path) -> bool:
    if (run_dir / "manifest.json").exists():
        return True
    mr = run_dir / "match_results"
    return mr.exists() and any(mr.glob("*.json"))


def run_eval(run_id: str, out_dir: Path, regime_id: str = "regime-v001",
             ledger_path: "Path | None" = None, agent_id: str = "random_legal",
             write_ledger: bool = True, ledger_notes: "str | None" = None) -> dict:
    """Returns a result dict. Raises SystemExit-like ints via RunEvalError-style
    exceptions mapped by main(). ``ledger_path`` defaults to docs/ledger.md;
    tests redirect it so they never touch the real ledger.

    ``agent_id`` selects the agent-under-test (player 0); the opponent stays the
    regime's frozen opponent. ``write_ledger=False`` (O2) skips the ledger append
    for non-deliverable runs. ``ledger_notes`` overrides the default ledger note
    (run-0002 uses it to record the same-regime, agent-only comparison framing)."""
    cfg = load_config()
    ledger_path = ledger_path if ledger_path is not None else (REPO_ROOT / "docs" / "ledger.md")
    if agent_id not in AGENTS:
        raise AgentInitError(f"unknown agent-under-test: {agent_id!r} (known: {sorted(AGENTS)})")

    # ---- load regime + components (env/input failures → exit 1) ----
    regime = _load_json(FROZEN / "regimes" / f"{regime_id}.json")
    seed_set = _load_json(FROZEN / "seeds" / f"{regime['seed_set']}.json")
    opp_pool = _load_json(FROZEN / "opponents" / f"{regime['opponent_pool']}.json")
    deck_pool = _load_json(FROZEN / "decks" / f"{regime['deck_pool']}.json")
    metrics = FROZEN / "metrics" / f"{regime['metrics_spec']}.json"

    match_indices = seed_set["match_indices"]
    opponent = opp_pool["opponents"][0]
    opponent_id = opponent["opponent_id"]
    deck_id = opponent["deck_ref"]

    deck = read_deck(resolve_deck_file(cfg))
    dh = compute_deck_hash(deck)
    # deck-drift guard: the live deck must match the frozen hash (G-4)
    frozen_dh = deck_pool["decks"][0]["deck_hash"]
    if dh != frozen_dh:
        raise RuntimeError(
            f"deck drift: live deck_hash {dh[:12]} != frozen {frozen_dh[:12]} "
            f"(deck-pool-v001). A changed deck requires a NEW regime, not a re-run."
        )

    expected_match_ids = [f"M{idx:04d}" for idx in match_indices]

    # ---- IMMUTABILITY GUARD (exit 3) — before any write ----
    if _is_populated(out_dir):
        # Validate that what is already there matches its own manifest (AC-9).
        existing = "no manifest"
        man_p = out_dir / "manifest.json"
        if man_p.exists():
            man = _load_json(man_p)
            written = sorted(p.stem for p in (out_dir / "match_results").glob("*.json"))
            unknown = [m for m in written if m not in set(man.get("expected_match_ids", []))]
            existing = (f"manifest run_id={man.get('run_id')} "
                        f"expected={len(man.get('expected_match_ids', []))} "
                        f"written={len(written)} unknown_ids={unknown}")
        raise ImmutabilityRefusal(
            f"run dir already populated: {out_dir} — refusing to overwrite "
            f"(immutability guard, exit 3). Existing: {existing}. "
            f"Re-running an evaluation goes to a NEW run_id."
        )

    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- O1 provenance (Sprint 01 entry gate): source-hash path (Option B) ----
    # Pin the runtime agent source(s) + eval config by stable SHA-256 so the
    # run-0001-vs-run-0002 same-regime, agent-only comparison has honest
    # provenance even when git_dirty=true (closeout O1; PRD §11.3).
    agent_src = REPO_ROOT / "agents" / "runtime" / f"{agent_id}.py"
    opp_ref = opponent.get("agent_ref") or f"agents/runtime/{opponent_id}.py"
    opp_src = REPO_ROOT / opp_ref
    config_path = REPO_ROOT / "config" / "eval_config.json"
    provenance = {
        "agent_source_file": f"agents/runtime/{agent_id}.py",
        "agent_source_hash": _file_hash(agent_src),
        "opponent_source_file": opp_ref,
        "opponent_source_hash": _file_hash(opp_src) if opp_src.exists() else "absent",
        "config_file": "config/eval_config.json",
        "config_hash": _file_hash(config_path) if config_path.exists() else "absent",
    }

    # ---- manifest FIRST (ID authority) ----
    agent_version = AGENTS[agent_id].AGENT_VERSION
    manifest = {
        "run_id": run_id,
        "regime_id": regime_id,
        "expected_match_ids": expected_match_ids,
        "match_indices": match_indices,
        "agent_id": agent_id,
        "opponent_id": opponent_id,
        "deck_a_id": deck_id,
        "deck_b_id": deck_id,
        "opponent_pool_id": opp_pool["opponent_pool_id"],
        "seed_set_id": seed_set["seed_set_id"],
        "deck_pool_id": deck_pool["deck_pool_id"],
        "metrics_spec_id": regime["metrics_spec"],
        "agent_version": agent_version,
        "agent_source_file": provenance["agent_source_file"],
        "agent_source_hash": provenance["agent_source_hash"],
        "opponent_source_hash": provenance["opponent_source_hash"],
        "mode": "unseeded",
        "sim_version": cfg.get("sim_version"),
        "created_at": _now(),
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    expected_set = set(expected_match_ids)

    # ---- play matches (agent-init failure → exit 2) ----
    rng = random.Random()  # unseeded: the sim RNG is uncontrolled anyway (audit-trail posture)
    caps_done = False
    for idx, match_id in zip(match_indices, expected_match_ids):
        if match_id not in expected_set:
            raise RuntimeError(f"allocated match_id {match_id} not in manifest expected list")
        inputs = {
            "agent_a_id": agent_id, "agent_b_id": opponent_id,
            "deck_a_id": deck_id, "deck_b_id": deck_id,
            "match_index": idx, "regime_id": regime_id,
            "run_id": run_id, "match_id": match_id,
            "opponent_id": opponent_id, "agent_version": agent_version,
            "deck_hash": dh,
        }
        try:
            result_obj = run_single(inputs, out_dir, cfg, deck, deck, rng)
        except KeyError as e:  # unknown agent id
            raise AgentInitError(f"agent init failed: {e}") from e
        # validate the written id against the manifest (AC-9)
        if result_obj["summary"]["match_id"] not in expected_set:
            raise RuntimeError(f"written match_id {match_id} not in manifest")
        write_match(out_dir, match_id, result_obj)
        caps_done = True

    # ---- provenance stamp: hashes.txt (AC-6) ----
    seed_list_hash = hash_canonical(match_indices)
    git_rev = _git(["rev-parse", "HEAD"]) or "unknown"
    git_dirty = "true" if _git(["status", "--porcelain"]) else "false"
    hashes = {
        "git_rev": git_rev,
        "git_dirty": git_dirty,
        "timestamp": _now(),
        "created_at": manifest["created_at"],
        "sim_version": cfg.get("sim_version") or "unknown",
        "sim_version_source": cfg.get("sim_version_source") or "installed-pin",
        "agent_version": agent_version,
        "seed_list_hash": seed_list_hash,
        "regime_hash": _file_hash(FROZEN / "regimes" / f"{regime_id}.json"),
        "seed_set_hash": _file_hash(FROZEN / "seeds" / f"{regime['seed_set']}.json"),
        "opponent_pool_hash": _file_hash(FROZEN / "opponents" / f"{regime['opponent_pool']}.json"),
        "deck_pool_hash": _file_hash(FROZEN / "decks" / f"{regime['deck_pool']}.json"),
        "metrics_spec_hash": _file_hash(metrics),
        "deck_hash": dh,
        # O1 source-hash provenance (Sprint 01 entry gate) — see manifest too.
        "agent_source_file": provenance["agent_source_file"],
        "agent_source_hash": provenance["agent_source_hash"],
        "opponent_source_file": provenance["opponent_source_file"],
        "opponent_source_hash": provenance["opponent_source_hash"],
        "config_hash": provenance["config_hash"],
    }
    with open(out_dir / "hashes.txt", "w", encoding="utf-8") as fh:
        fh.write("# Provenance stamp — flat SHA-256 strings; no signing, no hash chains (plan §7.3)\n")
        for k, v in hashes.items():
            fh.write(f"{k}={v}\n")

    # ---- notes.md ----
    (out_dir / "notes.md").write_text(
        f"# {run_id} — notes\n\n"
        f"- **What:** random_legal vs {opponent_id} (mirror) over {seed_set['seed_set_id']} "
        f"under {regime_id}, n={len(expected_match_ids)}.\n"
        f"- **mode:** unseeded (seed_controlled=false; the cabt local API exposes no RNG seed). "
        f"Reproducibility is distribution-stable + audit-trail (NFR-3); the determinism smoke is skipped.\n"
        f"- **Claim ceiling:** Rung 1 — legality/throughput only; NO strength claim (see docs/ledger.md, docs/claim-ceiling.md).\n",
        encoding="utf-8")

    # ---- summary.csv + (deliverable only) exactly one ledger row (AC-5, AC-7) ----
    default_notes = ("mode=unseeded; timeout undetectable (soft gate); "
                     "illegal-action gate hard (detectable=true).")
    if write_ledger:
        agg = aggregate.aggregate_and_ledger(
            out_dir, ledger_path,
            git_rev=git_rev, sim_version=hashes["sim_version"], mode="unseeded",
            opponent_pool_ref=opp_pool["opponent_pool_id"],
            seed_set_ref=seed_set["seed_set_id"],
            date=manifest["created_at"][:10],
            notes=ledger_notes or default_notes,
        )
        stats, ledger_appended, claim_ceiling = (
            agg["stats"], agg["ledger_appended"], agg["claim_ceiling"])
    else:
        # O2: non-deliverable (review/test/mirror) runs MUST NOT touch the tracked
        # ledger. Still write summary.csv; skip the ledger row entirely.
        stats = aggregate.aggregate_run(out_dir)
        aggregate.write_summary_csv(out_dir, stats)
        claim_ceiling = aggregate.build_claim_ceiling(stats, stats["regime_id"])
        ledger_appended = False

    # ---- final integrity check: written ids == manifest expected (AC-9) ----
    written = sorted(p.stem for p in (out_dir / "match_results").glob("*.json"))
    if set(written) != expected_set:
        raise RuntimeError(f"id integrity: written {written} != expected {sorted(expected_set)}")

    return {"run_dir": str(out_dir), "n": len(expected_match_ids),
            "stats": stats, "ledger_appended": ledger_appended,
            "claim_ceiling": claim_ceiling}


class ImmutabilityRefusal(Exception):
    pass


class AgentInitError(Exception):
    pass


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Drive N matches into one sealed run dir.")
    ap.add_argument("--run-id", default="run-0001")
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--regime-id", default="regime-v001")
    ap.add_argument("--agent", default="random_legal",
                    help="agent-under-test (player 0); e.g. scripted_baseline for run-0002")
    ap.add_argument("--ledger", default=None, help="ledger path (default: docs/ledger.md)")
    ap.add_argument("--no-ledger", action="store_true",
                    help="O2: do NOT append a ledger row (required for non-deliverable runs)")
    ap.add_argument("--ledger-note", default=None,
                    help="override the ledger row's notes (e.g. the comparison framing)")
    args = ap.parse_args(argv)

    cfg = load_config()
    runs_dir = REPO_ROOT / cfg.get("runs_dir", "runs")
    out_dir = Path(args.out_dir) if args.out_dir else (runs_dir / args.run_id)
    ledger_path = Path(args.ledger) if args.ledger else None

    try:
        res = run_eval(args.run_id, out_dir, regime_id=args.regime_id, ledger_path=ledger_path,
                       agent_id=args.agent, write_ledger=not args.no_ledger,
                       ledger_notes=args.ledger_note)
    except ImmutabilityRefusal as e:
        print(f"run_eval: REFUSED — {e}", file=sys.stderr)
        return 3
    except AgentInitError as e:
        print(f"run_eval: {e}", file=sys.stderr)
        return 2
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"run_eval: env/input failure — {e}", file=sys.stderr)
        return 1

    s = res["stats"]
    print(f"run_eval: OK — sealed {res['run_dir']} n={res['n']} "
          f"win_rate={s['win_rate']} error_rate={s['error_rate']} "
          f"illegal_rate={s['illegal_action_rate']} ledger_appended={res['ledger_appended']}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
