#!/usr/bin/env python3
"""TurnTrace capability probe — Task 00.1 / PR-9 (the FIRST Sprint 00 executable).

Runs real match(es) through the local cabt (``cg/``) simulator and records,
from the *observed* environment, which capabilities are
**confirmed / unconfirmed / absent** — each with a fallback. It shapes the
harness against what the simulator actually exposes, never against assumptions
(OD-4; SDD §1.4, §8 Phase 1).

Outputs:
  sim/README.md          human-readable capability findings (PR-9)
  sim/capabilities.json  machine-readable flags + measured throughput
                         (consumed by sim/adapter.py:capabilities())

Exit codes:
  0  one match completed; findings written.
  1  one match could NOT complete (or cabt/deck unavailable). The failed probe
     IS the output (SDD §6.3 honesty rule): do not fake data, do not scaffold
     around a missing simulator surface.

``sim/`` is the single blast radius: this module and ``sim/adapter.py`` are the
only modules that import cabt directly. stdlib only (NFR-7).

Run:  python sim/probe.py
"""

from __future__ import annotations

import json
import random
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

# sim/ internal path resolution (no cabt import here).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _env import (  # noqa: E402
    REPO_ROOT,
    load_config,
    read_deck,
    resolve_cg_dir,
    resolve_deck_file,
)


def _relpath(p: "Path | None") -> "str | None":
    """Path relative to repo root when possible — keeps tracked artifacts free
    of absolute home-directory paths."""
    if p is None:
        return None
    try:
        return str(Path(p).resolve().relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)

SIM_DIR = Path(__file__).resolve().parent
README_PATH = SIM_DIR / "README.md"
CAPS_PATH = SIM_DIR / "capabilities.json"

MAX_DECISIONS = 20000      # safety cap: a non-terminating match can't hang the probe
THROUGHPUT_MATCHES = 5     # small N — we measure, we don't benchmark
RESULT_LOG_TYPE = 23       # LogType.RESULT (cg/api.py:L319-321)
PROBE_RNG_SEED = 0         # the probe's OWN selection RNG; the sim seed is NOT controllable


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _import_cabt(cg_dir: Path):
    """Import cabt. Triggers cg.sim: LoadLibrary(cg.dll/libcg.so) + GameInitialize()."""
    sys.path.insert(0, str(cg_dir))
    import cg.game as game  # noqa: E402
    import cg.api as api    # noqa: E402  (imported for provenance; probe works on raw dicts)
    return game, api


def _terminal(obs: dict):
    """Read terminal status from an observation dict.

    Returns (is_terminal, result, reason):
      result — winning player index (0/1) or 2 for draw; None if not finished.
      reason — cabt end reason (1 prize-out, 2 deck-out, 3 no-active, 4 effect).
    """
    cur = obs.get("current")
    result = None
    reason = None
    if cur is not None and cur.get("result", -1) != -1:
        result = cur.get("result")
    for log in obs.get("logs") or []:
        if log.get("type") == RESULT_LOG_TYPE:
            result = log.get("result", result)
            reason = log.get("reason", reason)
    return (result is not None), result, reason


def _choose(obs: dict, deck: "list[int]", rng: random.Random) -> "list[int]":
    """Random-legal selection over the offered options (mirrors cg sample main.py)."""
    sel = obs.get("select")
    if sel is None:
        # Initial deck-selection step — return the deck (cg main.py contract).
        return list(deck)
    options = sel.get("option") or []
    n = len(options)
    maxc = sel.get("maxCount", 0)
    k = maxc if maxc <= n else n
    if k <= 0:
        return []
    return rng.sample(range(n), k)


def run_one_match(game, deck, rng, capture=False) -> dict:
    """Drive one full mirror match (random-legal both sides). Returns a summary."""
    info = {
        "completed": False, "result": None, "reason": None, "decisions": 0,
        "select_none_steps": 0, "first_select_was_none": None,
        "sample_select": None, "own_hand_visible": None,
        "opponent_hand_hidden": None, "deck_contents_hidden": None,
        "error": None,
    }
    obs, start_data = game.battle_start(deck, deck)
    if obs is None:
        info["error"] = (
            "battle_start returned no battle "
            f"(errorPlayer={getattr(start_data, 'errorPlayer', None)}, "
            f"errorType={getattr(start_data, 'errorType', None)})"
        )
        return info
    try:
        for _ in range(MAX_DECISIONS):
            done, result, reason = _terminal(obs)
            if done:
                info["completed"] = True
                info["result"] = result
                info["reason"] = reason
                break
            sel = obs.get("select")
            if info["first_select_was_none"] is None:
                info["first_select_was_none"] = sel is None
            if sel is None:
                info["select_none_steps"] += 1
            elif capture and info["sample_select"] is None:
                info["sample_select"] = {
                    "type": sel.get("type"), "context": sel.get("context"),
                    "minCount": sel.get("minCount"), "maxCount": sel.get("maxCount"),
                    "n_options": len(sel.get("option") or []),
                }
            # capture hidden-state visibility from the first real state
            if capture and info["own_hand_visible"] is None:
                cur = obs.get("current")
                if cur is not None and cur.get("players"):
                    yi = cur.get("yourIndex", 0)
                    players = cur["players"]
                    if 0 <= yi < len(players):
                        me = players[yi]
                        opp = players[1 - yi] if len(players) > 1 else {}
                        info["own_hand_visible"] = me.get("hand") is not None
                        info["opponent_hand_hidden"] = opp.get("hand") is None
                        info["deck_contents_hidden"] = "deckCount" in me and "deck" not in me
            selection = _choose(obs, deck, rng)
            obs = game.battle_select(selection)
            info["decisions"] += 1
        else:
            info["error"] = f"match did not terminate within {MAX_DECISIONS} decisions"
    finally:
        try:
            game.battle_finish()
        except Exception:
            pass
    return info


def probe_invalid_action_detectable(game, deck) -> "bool | None":
    """On a throwaway battle, attempt an out-of-range selection and observe
    whether the sim rejects it. Returns True/False, or None if undetermined."""
    try:
        obs, start_data = game.battle_start(deck, deck)
        if obs is None:
            return None
        guard = 0
        while obs.get("select") is None and guard < 20:
            obs = game.battle_select(list(deck))
            guard += 1
        sel = obs.get("select")
        if sel is None or not (sel.get("option") or []):
            return None
        bad_index = len(sel["option"]) + 50  # unambiguously out of range
        try:
            game.battle_select([bad_index])
            return False   # accepted an illegal index → rejection NOT detectable
        except Exception:
            return True    # rejected → detectable
    except Exception:
        return None
    finally:
        try:
            game.battle_finish()
        except Exception:
            pass


def build_caps(cfg: dict) -> dict:
    """Conservative defaults; the probe overwrites what it can observe."""
    return {
        "schema": "turntrace/sim-capabilities/v1",
        "probed_at": _now(),
        "platform": sys.platform,
        "python": sys.version.split()[0],
        "sim_version": cfg.get("sim_version", "cabt (kaggle-environments 1.14.10)"),
        "sim_version_source": cfg.get("sim_version_source", "installed-pin"),
        "cg_dir": None,
        "deck_file": None,
        "flags": {
            "local_match_runnable": "absent",
            "legal_actions_observed": False,
            "seed_controlled": False,
            "invalid_action_detectable": None,
            "timeout_detectable": False,
            "own_hidden_state_observable": False,
        },
        "measured": {
            "match_throughput_per_sec": None,
            "match_throughput_per_hour": None,
            "throughput_matches": 0,
            "throughput_completed": 0,
            "avg_decisions_per_match": None,
            "example_match": None,
        },
        "budget": {
            "decision_budget_ms": cfg.get("decision_budget_ms"),
            "budget_source": cfg.get("budget_source", "assumed"),
        },
        "errors": [],
    }


# ---- capability fallbacks (the honest "what we do when it's missing") ----
FALLBACKS = {
    "local_match_runnable": "If one match cannot complete: HALT Sprint 00 and report the blocker (SDD §6.3). Do not fake data.",
    "legal_actions_observed": "If options are not enumerable: propose-and-retry on rejection; set legal_actions_* fields null; rely on selected_action + post-state (plan §10 contingency 2).",
    "seed_controlled": "No seed parameter is exposed by cg.game.battle_start(deck0, deck1). Posture: distribution-stable + audit-trail (NFR-3); records carry match_index, mode=unseeded; determinism smoke is skipped.",
    "invalid_action_detectable": "If rejection is undetectable: invalid_action_count=null + flag false; the §5.4 illegal-action gate downgrades to a soft warning (an undetectable rate is never a pass).",
    "timeout_detectable": "No per-move budget is published by the local surface. Measure our own decision wall-time vs a config budget (budget_source=assumed); timeout=null per record; the §5.4 timeout gate is a soft warning.",
    "own_hidden_state_observable": "Own hand/discard/prize/energy are observable and may populate private_state_summary; opponent hand and own deck order are hidden and are NEVER logged (no future-draw leakage).",
}

# raw observed facts captured by the probe (for the README), filled in main()
_OBSERVED: dict = {}


def render_readme(caps: dict, deck_present: bool) -> str:
    f = caps["flags"]
    m = caps["measured"]

    def mark(v):
        if v == "confirmed" or v is True:
            return "confirmed"
        if v == "absent" or v is False:
            return "absent"
        if v is None:
            return "unconfirmed"
        return str(v)

    tp_sec = m["match_throughput_per_sec"]
    tp_hr = m["match_throughput_per_hour"]
    tp_sec_s = f"{tp_sec:.3f}" if isinstance(tp_sec, (int, float)) else "unavailable"
    tp_hr_s = f"{tp_hr:,.0f}" if isinstance(tp_hr, (int, float)) else "unavailable"
    avg_dec = m["avg_decisions_per_match"]
    avg_dec_s = f"{avg_dec:.1f}" if isinstance(avg_dec, (int, float)) else "unavailable"
    ex = m.get("example_match") or {}

    rows = [
        ("Local match runnable", mark(f["local_match_runnable"]), FALLBACKS["local_match_runnable"]),
        ("Legal action enumeration", mark(f["legal_actions_observed"]), FALLBACKS["legal_actions_observed"]),
        ("Seed / RNG control", mark(f["seed_controlled"]), FALLBACKS["seed_controlled"]),
        ("Invalid-action detection", mark(f["invalid_action_detectable"]), FALLBACKS["invalid_action_detectable"]),
        ("Timeout / time-budget detection", mark(f["timeout_detectable"]), FALLBACKS["timeout_detectable"]),
        ("Own hidden-state observable", mark(f["own_hidden_state_observable"]), FALLBACKS["own_hidden_state_observable"]),
    ]
    table = "\n".join(f"| {n} | **{s}** | {fb} |" for n, s, fb in rows)

    obs_lines = []
    for k, v in _OBSERVED.items():
        obs_lines.append(f"- **{k}:** {v}")
    observed_block = "\n".join(obs_lines) if obs_lines else "- (none captured)"

    return f"""# `sim/` — Capability Findings (PR-9, Task 00.1)

> **Generated by `sim/probe.py`** — the first Sprint 00 executable. These are
> *observed* facts from the live local `cabt` (`cg/`) surface, not assumptions.
> Re-run `python sim/probe.py` to refresh. Machine-readable flags live in
> [`sim/capabilities.json`](capabilities.json), which `sim/adapter.py` consumes.
>
> No Competition Data (card IDs/names/deck lists) appears here — only outcome
> enums, counts, and capability facts (CC-1/CC-2, ESP-3).

- **Probed at:** {caps['probed_at']}
- **Platform / Python:** {caps['platform']} / {caps['python']}
- **Simulator version:** {caps['sim_version']} (`{caps['sim_version_source']}`)
- **`cg/` directory:** `{caps['cg_dir']}` *(local, git-ignored — CC-1)*
- **Deck present:** {deck_present} *(local, git-ignored — CC-1)*

## Capability matrix

| Capability | Status | Fallback (what we do if missing) |
|---|---|---|
{table}

## Measured throughput (Task 00.1 / U-2)

- **Matches timed:** {m['throughput_matches']} (completed {m['throughput_completed']})
- **Throughput:** {tp_sec_s} matches/sec  ·  ~{tp_hr_s} matches/hour
- **Avg decisions / match:** {avg_dec_s}
- **Example completed match:** result=`{ex.get('result')}` reason=`{ex.get('reason')}` decisions=`{ex.get('decisions')}`

Throughput unblocks N-sizing: `seed-set-v001` is sized so a full `run_eval`
stays well-bounded; raising N trades wall-clock for statistical power, never
correctness (plan §7.6).

## Raw observed surface facts

{observed_block}

## The `sim/` adapter contract (downstream of these findings)

`sim/adapter.py` is the **single blast radius** (SDD §1.4, §5.1): the only
module besides this probe that touches `cabt`. It exposes the harness-internal
port — `start_match` / `step` / `finish` / `legal_options` / `observe` /
`event_log` / `capabilities` — and returns every capability above as a flag,
defaulting conservative (e.g. `seed_controlled=false`) until proven here. If the
live API diverges from this report, only files **inside `sim/`** change.

## Maturity-ladder position

These findings place TurnTrace at **Rung 0 → Rung 1 territory**: the environment
can be invoked and (per the matrix above) a match completes legally. No
strength claim is licensed — see `docs/claim-ceiling.md`.
"""


def write_outputs(caps: dict, deck_present: bool) -> None:
    with open(CAPS_PATH, "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2, sort_keys=True)
        fh.write("\n")
    with open(README_PATH, "w", encoding="utf-8") as fh:
        fh.write(render_readme(caps, deck_present))


def main() -> int:
    cfg = load_config()
    caps = build_caps(cfg)

    # --- locate + import cabt ---
    cg_dir = None
    try:
        cg_dir = resolve_cg_dir(cfg)
        caps["cg_dir"] = _relpath(cg_dir)
    except Exception as e:  # noqa: BLE001
        caps["errors"].append(f"cg_dir resolution failed: {e}")

    game = api = None
    cg_loaded = False
    if cg_dir is not None and cg_dir.exists():
        try:
            game, api = _import_cabt(cg_dir)
            cg_loaded = True
        except Exception as e:  # noqa: BLE001
            caps["errors"].append(f"cabt import/load failed: {e} :: {traceback.format_exc()}")
    elif cg_dir is not None:
        caps["errors"].append(f"cg_dir does not exist: {cg_dir}")

    # --- locate deck ---
    deck = None
    try:
        deck_file = resolve_deck_file(cfg)
        caps["deck_file"] = _relpath(deck_file)
        deck = read_deck(deck_file)
    except Exception as e:  # noqa: BLE001
        caps["errors"].append(f"deck load failed: {e}")

    if not cg_loaded or deck is None:
        caps["flags"]["local_match_runnable"] = "absent"
        write_outputs(caps, deck_present=deck is not None)
        print("PROBE: cabt unavailable or deck missing — see sim/README.md", file=sys.stderr)
        return 1

    rng = random.Random(PROBE_RNG_SEED)

    # --- the gate: one full match must complete ---
    first = run_one_match(game, deck, rng, capture=True)
    _OBSERVED["battle_start"] = "returns (obs_dict, StartData); no seed parameter accepted"
    _OBSERVED["first_select_was_none"] = first.get("first_select_was_none")
    _OBSERVED["select_none_steps_in_match"] = first.get("select_none_steps")
    if first.get("sample_select"):
        ss = first["sample_select"]
        _OBSERVED["example_select"] = (
            f"type={ss['type']} context={ss['context']} "
            f"minCount={ss['minCount']} maxCount={ss['maxCount']} n_options={ss['n_options']}"
        )
    _OBSERVED["own_hand_visible"] = first.get("own_hand_visible")
    _OBSERVED["opponent_hand_hidden"] = first.get("opponent_hand_hidden")
    _OBSERVED["own_deck_contents_hidden"] = first.get("deck_contents_hidden")

    if not first["completed"]:
        caps["flags"]["local_match_runnable"] = "absent"
        caps["errors"].append(f"one match did not complete: {first.get('error')}")
        write_outputs(caps, deck_present=True)
        print(f"PROBE: one match did not complete — {first.get('error')}", file=sys.stderr)
        return 1

    caps["flags"]["local_match_runnable"] = "confirmed"
    caps["flags"]["legal_actions_observed"] = bool(first.get("sample_select"))
    caps["flags"]["own_hidden_state_observable"] = bool(first.get("own_hand_visible"))
    caps["measured"]["example_match"] = {
        "result": first.get("result"), "reason": first.get("reason"),
        "decisions": first.get("decisions"),
    }

    # --- invalid-action detectability (throwaway battle) ---
    caps["flags"]["invalid_action_detectable"] = probe_invalid_action_detectable(game, deck)

    # --- throughput (small N) ---
    t0 = perf_counter()
    completed = 0
    total_decisions = first.get("decisions", 0)
    for _ in range(THROUGHPUT_MATCHES):
        r = run_one_match(game, deck, rng)
        if r["completed"]:
            completed += 1
            total_decisions += r.get("decisions", 0)
    elapsed = perf_counter() - t0
    mps = (completed / elapsed) if (elapsed > 0 and completed > 0) else None
    caps["measured"].update({
        "match_throughput_per_sec": mps,
        "match_throughput_per_hour": (mps * 3600.0) if mps else None,
        "throughput_matches": THROUGHPUT_MATCHES,
        "throughput_completed": completed,
        "avg_decisions_per_match": (total_decisions / (completed + 1)) if completed else None,
    })

    write_outputs(caps, deck_present=True)
    print(
        f"PROBE: OK — match runnable; legal_actions_observed="
        f"{caps['flags']['legal_actions_observed']} seed_controlled=False "
        f"invalid_action_detectable={caps['flags']['invalid_action_detectable']} "
        f"throughput~{mps and round(mps, 3)} matches/s",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
