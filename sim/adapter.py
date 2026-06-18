"""``sim/adapter.py`` — the single blast radius (PR-?, Task 00.2; SDD §1.4, §5.1).

The ONLY production module that knows ``cabt``. It wraps the local
``cg.game`` surface (``battle_start`` / ``battle_select`` / ``battle_finish``)
and exposes the harness-internal **port**: ``start_match`` / ``step`` /
``finish`` / ``legal_options`` / ``observe`` / ``event_log`` / ``capabilities``.

Two hard rules (SDD §5.1):
  1. No caller outside ``sim/`` references a ``cabt`` symbol — the rest of the
     harness depends on this contract, never on ``cabt`` internals.
  2. Every capability the harness reads is a flag from ``capabilities()``,
     defaulting conservative (e.g. ``seed_controlled=false``) until the probe
     (``sim/probe.py`` → ``sim/capabilities.json``) proves otherwise.

All *view* helpers below are deliberately **Competition-Data-free**: they emit
counts, OptionType enums, and SHA-256 digests of card-id lists — never raw card
IDs/names (CC-1/CC-2). Even though run traces are local/git-ignored (ESP-1),
keeping the adapter's output card-id-free means no downstream artifact can leak
Pokémon Elements.

stdlib only (NFR-7).
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _env import load_config, resolve_cg_dir  # noqa: E402

CAPS_PATH = Path(__file__).resolve().parent / "capabilities.json"
RESULT_LOG_TYPE = 23  # LogType.RESULT (cg/api.py:L319-321)

# cabt end-reason → ending_cause enum (cg/api.py:L319-321).
ENDING_CAUSE = {1: "prize-out", 2: "deck-out", 3: "no-active", 4: "card-effect"}

# Conservative capability defaults (used if sim/capabilities.json is absent).
_CONSERVATIVE_FLAGS = {
    "local_match_runnable": "unconfirmed",
    "legal_actions_observed": False,
    "seed_controlled": False,
    "invalid_action_detectable": None,
    "timeout_detectable": False,
    "own_hidden_state_observable": False,
}


def _digest(ids: "list[int]") -> str:
    """SHA-256 of a canonical card-id list — detects 'same hand' without storing
    raw card IDs (CC-1/CC-2 safe)."""
    return hashlib.sha256(json.dumps(ids, separators=(",", ":")).encode("ascii")).hexdigest()


class SimAdapter:
    """Stateful wrapper over the (single-battle, module-global) ``cg.game`` API.

    Sprint 00 runs matches sequentially, so one live battle at a time is
    sufficient (SDD §1.9). Construct once, then ``start_match`` / ``step`` /
    ``finish`` per match.
    """

    def __init__(self, cg_dir: "Path | None" = None, cfg: "dict | None" = None):
        cfg = cfg if cfg is not None else load_config()
        self._cfg = cfg
        cg_dir = cg_dir if cg_dir is not None else resolve_cg_dir(cfg)
        if not Path(cg_dir).exists():
            raise RuntimeError(f"cg_dir does not exist: {cg_dir}")
        sys.path.insert(0, str(cg_dir))
        try:
            import cg.game as game  # noqa: E402  loads cg.dll/libcg.so + GameInitialize()
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"failed to import/load cabt from {cg_dir}: {e}") from e
        self._game = game
        self._started = False

    # ---- drive ----------------------------------------------------------
    def start_match(self, deck0: "list[int]", deck1: "list[int]") -> dict:
        """Begin a match from two 60-card decks; return the first observation."""
        obs, start_data = self._game.battle_start(deck0, deck1)
        if obs is None:
            raise RuntimeError(
                "battle_start failed "
                f"(errorPlayer={getattr(start_data, 'errorPlayer', None)}, "
                f"errorType={getattr(start_data, 'errorType', None)})"
            )
        self._started = True
        return obs

    def step(self, selection: "list[int]") -> dict:
        """Apply a selection (indices into the offered options); return next obs.

        Raises (IndexError/ValueError from cabt) if the selection is illegal —
        this is what makes ``invalid_action_detectable`` true.
        """
        return self._game.battle_select(selection)

    def finish(self) -> None:
        """End the match and free cabt memory. Idempotent/safe to call once."""
        if self._started:
            try:
                self._game.battle_finish()
            finally:
                self._started = False

    # ---- capabilities ---------------------------------------------------
    def capabilities(self) -> dict:
        """Return capability flags + measured throughput from the probe output,
        or conservative defaults if ``sim/capabilities.json`` is missing."""
        if CAPS_PATH.exists():
            with open(CAPS_PATH, "r", encoding="utf-8") as fh:
                caps = json.load(fh)
            flags = dict(_CONSERVATIVE_FLAGS)
            flags.update(caps.get("flags", {}))
            return {
                "flags": flags,
                "measured": caps.get("measured", {}),
                "budget": caps.get("budget", {"decision_budget_ms": None, "budget_source": "assumed"}),
                "sim_version": caps.get("sim_version", self._cfg.get("sim_version")),
                "sim_version_source": caps.get("sim_version_source", self._cfg.get("sim_version_source")),
                "source": "sim/capabilities.json",
            }
        return {
            "flags": dict(_CONSERVATIVE_FLAGS),
            "measured": {},
            "budget": {"decision_budget_ms": self._cfg.get("decision_budget_ms"),
                       "budget_source": self._cfg.get("budget_source", "assumed")},
            "sim_version": self._cfg.get("sim_version"),
            "sim_version_source": self._cfg.get("sim_version_source"),
            "source": "conservative-defaults",
        }

    # ---- observation views (Competition-Data-free) ----------------------
    @staticmethod
    def terminal(obs: dict):
        """(is_terminal, result, reason). result: winner index 0/1, or 2 draw;
        None if not finished. reason: cabt end reason int (see ENDING_CAUSE)."""
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

    @staticmethod
    def your_index(obs: dict):
        cur = obs.get("current")
        return cur.get("yourIndex") if cur else None

    @staticmethod
    def turn(obs: dict):
        cur = obs.get("current")
        return cur.get("turn") if cur else None

    @staticmethod
    def select_context(obs: dict):
        sel = obs.get("select")
        return sel.get("context") if sel else None

    @staticmethod
    def is_deck_selection(obs: dict) -> bool:
        return obs.get("select") is None

    @staticmethod
    def legal_options(obs: dict) -> dict:
        """The legal-action view: counts, bounds, and OptionType tokens only."""
        sel = obs.get("select")
        if sel is None:
            return {"n_options": 0, "min_count": 0, "max_count": 0, "option_types": []}
        options = sel.get("option") or []
        return {
            "n_options": len(options),
            "min_count": sel.get("minCount", 0),
            "max_count": sel.get("maxCount", 0),
            "option_types": [o.get("type") for o in options],
        }

    @staticmethod
    def legal_digest(obs: dict) -> "str | None":
        sel = obs.get("select")
        if sel is None:
            return None
        types = [o.get("type") for o in (sel.get("option") or [])]
        return hashlib.sha256(json.dumps(types, separators=(",", ":")).encode("ascii")).hexdigest()

    @staticmethod
    def public_summary(obs: dict) -> "dict | None":
        """Counts visible to both players — no card IDs."""
        cur = obs.get("current")
        if cur is None or not cur.get("players"):
            return None
        players = cur["players"]

        def side(p):
            active = p.get("active") or []
            return {
                "active_present": bool(active) and active[0] is not None,
                "bench_count": len(p.get("bench") or []),
                "hand_count": p.get("handCount"),
                "deck_count": p.get("deckCount"),
                "discard_count": len(p.get("discard") or []),
                "prize_count": len(p.get("prize") or []),
            }

        return {
            "turn": cur.get("turn"),
            "your_index": cur.get("yourIndex"),
            "stadium_present": bool(cur.get("stadium")),
            "players": [side(p) for p in players],
        }

    @staticmethod
    def private_summary(obs: dict) -> "dict | None":
        """ONLY the deciding player's legitimately-observable hidden state:
        own hand size + a digest of own hand card IDs, discard/prize counts.
        Never the opponent hand or own deck order (no future-draw leakage)."""
        cur = obs.get("current")
        if cur is None or not cur.get("players"):
            return None
        yi = cur.get("yourIndex", 0)
        players = cur["players"]
        if not (0 <= yi < len(players)):
            return None
        me = players[yi]
        hand = me.get("hand")
        return {
            "hand_count": me.get("handCount"),
            "hand_card_ids_digest": _digest([c.get("id") for c in hand]) if hand else None,
            "discard_count": len(me.get("discard") or []),
            "prize_count": len(me.get("prize") or []),
            "deck_count": me.get("deckCount"),
        }

    @staticmethod
    def selected_action_view(obs: dict, selection: "list[int]") -> dict:
        """The chosen action as indices + OptionType tokens (no card IDs)."""
        sel = obs.get("select")
        options = (sel.get("option") or []) if sel else []
        types = []
        for i in selection:
            if isinstance(i, int) and 0 <= i < len(options):
                types.append(options[i].get("type"))
        return {"indices": list(selection), "option_types": types}

    @staticmethod
    def outcome_for_player(result, player_index: int) -> str:
        """Map cabt result (winner index / 2=draw) to win/loss/draw for a side."""
        if result == 2:
            return "draw"
        if result == player_index:
            return "win"
        return "loss"

    @staticmethod
    def ending_cause(reason) -> "str | None":
        return ENDING_CAUSE.get(reason)
