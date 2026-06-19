#!/usr/bin/env python3
"""``analysis/evidence_summary.py`` — offline sanitized K-batch evidence-summary
generator + independent fail-closed validator (Cycle-004 OA-2; C4-FR-1/2/3).

A new sibling of ``analysis/dispersion_report.py``. Two cores live in one module
(OD-C4-1): a **generator** (``build_summary``) that turns existing local sealed
run dirs into a sanitized, JSON-first, schema-conforming K-batch evidence summary,
and an **independent fail-closed validator** (``validate_summary`` + the
``--validate`` mode) that makes the ``04-evidence-summary-schema-spec.md`` §3
forbidden-field/content set *enforceable rather than advisory*. They share one
in-module allow-list constant (``SAFE_FIELDS``, §5 of the SDD). This cycle is
**build-only**: it promotes no value, writes no ledger row, advances no ceiling,
and chooses no margin — the summary carries **no ceiling of its own**.

Reads (only):
  * each run dir's ``manifest.json`` — read **first**, the authority for
    ``regime_id`` and ``agent_id`` (mirroring ``dispersion_report.py:126-141``).
  * each run dir's ``match_results/*.json`` — via ``aggregate.aggregate_run`` (the
    single source of per-run sanitized stats; ``aggregate.py:56-89``).
  * a summary ``.json`` file passed to ``--validate`` (re-read from disk).
It **never** opens the per-decision sidecar files (the raw decision rows). The
module contains **no reference to that sidecar directory** — the same structural
guarantee as ``dispersion_report.py:16-19``: there is no code path that names it,
so it *cannot* read raw decision rows. (Property asserted by a source-grep test.)

Reuse, not recompute: ``DISPERSION_METRICS`` / ``STAT_COLUMNS`` /
``descriptive_stats`` are imported from ``analysis.dispersion_report`` and
``aggregate_run`` from ``analysis.aggregate`` — so **no new metric and no new
statistic can enter through this module** (doc 04 §2.2-§2.3; OD-6). No sample
standard deviation, no variance, and no inferential statistic is computed
anywhere; their absence is structural.

# loa:shortcut: hygiene path rules are a parity-tested stdlib local copy of
# eval/hygiene_check.py:35-45 (asserted in tests), NOT an eval/ import — the
# standing offline/runtime separation forbids analysis/ importing eval/.
# Upgrade trigger: none — this is the import-direction rule (SDD §7), not a temp shortcut.

``analysis/`` imports run-dir artifacts + intra-zone helpers only — no ``cabt``,
``sim/``, ``agents/runtime/``, or ``eval/`` (the offline/runtime separation;
enforced by ``tests/test_import_direction.py:32-37,69``). stdlib only (NFR-5).

CLI:
  generate:  python analysis/evidence_summary.py <run_dir> [<run_dir> ...] [--json] [--out <local-path>]
  validate:  python analysis/evidence_summary.py --validate <summary.json>
Exit: 0 clean / valid · 1 input failure · 2 mixed-regime refusal ·
      3 forbidden-field/value/word leak (fail-closed; never 0 on a leak).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "analysis"))

import aggregate  # noqa: E402  (analysis/ — intra-zone; per-run sanitized stats)
import dispersion_report  # noqa: E402  (analysis/ — intra-zone; reused metric/stat surface)

# ---- reuse the proven sanitized surface (no recompute; doc 04 §2.2-§2.3, OD-6) ----
DISPERSION_METRICS = dispersion_report.DISPERSION_METRICS  # the six metric names (:69-72)
STAT_COLUMNS = dispersion_report.STAT_COLUMNS              # the seven descriptive stats (:76)
descriptive_stats = dispersion_report.descriptive_stats   # pure arithmetic (:94-114)
MixedRegimeRefusal = dispersion_report.MixedRegimeRefusal  # exit-2 refusal type (:79-80)

# =====================================================================================
# T3 — In-module machine-checkable allow-list (SAFE_FIELDS). Single source of truth in
# code; agrees with doc 04 §2 (+ the §4.1 JSON-first structural containers). The
# doc<->schema agreement is asserted by a test; a divergence fails the build.
# =====================================================================================

# doc 04 §2.1 — identity / provenance / framing field names.
_IDENTITY_FIELDS = frozenset({
    "regime_id", "n", "K", "agent_id", "agent_version", "run_ids",
    "hashes", "mode", "unseeded_caveat", "claim_ceiling",
})
# doc 04 §4.1 — the JSON-first structural containers the shape nests under.
_STRUCTURAL_FIELDS = frozenset({"agents", "metrics"})

SAFE_FIELDS = frozenset(
    _IDENTITY_FIELDS
    | _STRUCTURAL_FIELDS
    | set(DISPERSION_METRICS)   # doc 04 §2.3 — the six metric names
    | set(STAT_COLUMNS)         # doc 04 §2.2 — the seven statistic names
)

# ---- two mandatory framing strings (doc 04 §2.4); the summary carries no ceiling ----
_UNSEEDED_CAVEAT = (
    "seed_controlled=false; the observed dispersion reflects the whole unseeded "
    "process (agent behaviour together with uncontrolled simulator RNG), not an "
    "isolated agent-only quantity (docs/claim-ceiling.md:42-52)."
)
_RUNG1_FOOTER = (
    "Descriptive observed-spread diagnostic at Rung 1: NO gameplay-strength claim "
    "and NO inferential claim. This summary carries no ceiling of its own — the "
    "experiment ledger (docs/ledger.md) is the only ceiling-bearing artifact, and a "
    "regime-v002 number is never compared to a regime-v001 ledger row (NFR-5)."
)

# =====================================================================================
# T2 — Generator core (build_summary). Read surface = dispersion_report.py:11-19.
# =====================================================================================

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _load_manifest(run_dir: Path) -> dict:
    mp = run_dir / "manifest.json"
    if not mp.exists():
        raise FileNotFoundError(f"{run_dir}: missing manifest.json")
    return json.loads(mp.read_text(encoding="utf-8"))


def _manifest_run_hash(man: dict):
    """A single sanitized SHA-256 integrity stamp the manifest already carries.

    Card-identity signals are SHA-256 digests only (eval/schemas.md:13-15), so this
    stamp can never hold Competition Data. Sourced from the manifest alone — the
    generator's read surface is manifest.json + match_results/* only (SDD §3.1, §8)."""
    for key in ("config_hash", "regime_hash", "manifest_hash", "content_hash",
                "agent_source_hash", "opponent_source_hash"):
        v = man.get(key)
        if isinstance(v, str) and _SHA256_RE.match(v):
            return v
    for k in sorted(man):
        v = man.get(k)
        if "hash" in k.lower() and isinstance(v, str) and _SHA256_RE.match(v):
            return v
    return None


def build_summary(run_dirs: "list[Path]") -> dict:
    """Build the doc 04 §2/§4 sanitized K-batch evidence summary over the run dirs.

    Reads each manifest.json FIRST (regime authority), hard-refuses mixed regimes
    (MixedRegimeRefusal -> exit 2) before any aggregation, then reuses
    aggregate_run + descriptive_stats per agent. Returns the JSON-first summary
    dict; writing is the CLI's job. Runs no eval and creates no run dir (NG12)."""
    if not run_dirs:
        raise ValueError("no run dirs given")

    # ---- read the authoritative regime_id from every manifest FIRST ----
    manifests = []
    for rd in run_dirs:
        manifests.append((rd, _load_manifest(rd)))
    regimes = {man.get("regime_id") for _, man in manifests}

    # ---- HARD single-regime guard (exit 2) — before any aggregation ----
    if len(regimes) != 1:
        raise MixedRegimeRefusal(
            f"refusing to summarize across regimes: the input run dirs carry "
            f"{sorted(str(r) for r in regimes)}. An evidence summary covers ONE "
            f"regime_id only (NFR-5) — a v002 number is never aggregated beside a "
            f"v001 number. Re-run with run dirs that all share one regime_id."
        )
    regime_id = next(iter(regimes))

    # ---- per-run sanitized stats (manifest authority cross-check) + hashes ----
    by_agent: "dict[str, list[dict]]" = {}
    hashes: "dict[str, str]" = {}
    n_values = set()
    mode = None
    for rd, man in manifests:
        stats = aggregate.aggregate_run(rd)  # reads match_results/*.json only
        if stats.get("regime_id") != man.get("regime_id"):
            raise ValueError(
                f"{rd.name}: records regime '{stats.get('regime_id')}' != manifest "
                f"regime '{man.get('regime_id')}'")
        agent_id = man.get("agent_id") or stats.get("agent_version") or "<unknown-agent>"
        run_id = stats.get("run_id")
        by_agent.setdefault(agent_id, []).append({
            "run_id": run_id,
            "agent_version": stats.get("agent_version"),
            "n_matches": stats.get("n_matches"),
            "metrics": {m: stats.get(m) for m in DISPERSION_METRICS},
        })
        h = _manifest_run_hash(man)
        if run_id is not None and h is not None:
            hashes[run_id] = h
        if isinstance(stats.get("n_matches"), int):
            n_values.add(stats["n_matches"])
        if mode is None:
            mode = man.get("mode") or "unseeded"

    # ---- per-agent dispersion of each metric across its K runs (reused stats) ----
    agents = []
    for agent_id in sorted(by_agent):
        runs = by_agent[agent_id]
        agents.append({
            "agent_id": agent_id,
            "agent_version": runs[0].get("agent_version"),
            "K": len(runs),
            "run_ids": [r["run_id"] for r in runs],
            "metrics": {
                m: descriptive_stats([r["metrics"].get(m) for r in runs])
                for m in DISPERSION_METRICS
            },
        })

    n = next(iter(n_values)) if len(n_values) == 1 else sorted(n_values)
    k_values = {a["K"] for a in agents}
    return {
        "regime_id": regime_id,
        "n": n,
        "K": (next(iter(k_values)) if len(k_values) == 1 else None),
        "mode": mode or "unseeded",
        "agents": agents,
        "hashes": hashes,
        "unseeded_caveat": _UNSEEDED_CAVEAT,
        "claim_ceiling": _RUNG1_FOOTER,
    }


def render_json(summary: dict) -> str:
    """JSON-first serialization (the primary form; mirror dispersion_report.py:243-255)."""
    return json.dumps(summary, indent=2, sort_keys=True)


# =====================================================================================
# T4 — Validator core (validate_summary). Pure, fail-closed, allow-list. Returns a
# list of (field_or_token, reason) violations; an empty list means valid (exit 0).
# Per-class explicit reasons mirror hygiene_check.find_violations (hygiene_check.py:52-62).
# Mixed-regime is a SEPARATE hard refusal (exit 2), handled in the --validate path.
# =====================================================================================

# ---- copied parity-tested hygiene path rules (eval/hygiene_check.py:35-45); NOT an
# ----  eval/ import (import direction). Test asserts parity vs find_violations. ----
_HYGIENE_PATH_RULES = [
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

# ---- inferential-statistic vocabulary (OD-6). The bare word 'hypothesis' is ALLOWED
# ----  (the ledger hypothesis text-field context); only the compound 'hypothesis-test'
# ----  is rejected — the benign-exception allow-rule (doc 04 §3 note; SDD §4.4). ----
_INFERENTIAL_RULES = [
    (re.compile(r"\bstd[\s\-]?dev\b", re.IGNORECASE), "inferential statistic: std-dev (OD-6)"),
    (re.compile(r"\bstandard\s+deviation\b", re.IGNORECASE), "inferential statistic: standard deviation (OD-6)"),
    (re.compile(r"\bvariance\b", re.IGNORECASE), "inferential statistic: variance (OD-6)"),
    (re.compile(r"\bconfidence\s+interval(s)?\b", re.IGNORECASE), "inferential statistic: confidence interval (OD-6)"),
    (re.compile(r"\bCI\b"), "inferential statistic: CI / confidence interval (OD-6)"),
    (re.compile(r"\bp[\s\-]?value(s)?\b", re.IGNORECASE), "inferential statistic: p-value (OD-6)"),
    (re.compile(r"\bsignifican(ce|t)\b", re.IGNORECASE), "inferential statistic: significance (OD-6)"),
    (re.compile(r"\bhypothesis[\s\-]?test(ing)?\b", re.IGNORECASE),
     "inferential statistic: hypothesis-test (OD-6; bare 'hypothesis' provenance text is allowed)"),
    (re.compile(r"\berror[\s\-]?bar(s)?\b", re.IGNORECASE), "inferential statistic: error-bar (OD-6)"),
]

# ---- forbidden agent words (docs/claim-ceiling.md:54-59) — rejected only when
# ----  AFFIRMATIVE. C2 (Cycle-005): a forbidden word is suppressed ONLY when a
# ----  negation token is the IMMEDIATELY preceding token — whitespace/punctuation
# ----  may sit between it and the word, but no intervening content word. The
# ----  Cycle-004 broad fixed-window scan let an UNRELATED negation nearby suppress
# ----  an affirmative word; immediate-precedence suppresses a strict subset of that
# ----  window, so the validator now flags a SUPERSET of affirmative forbidden words
# ----  (conservative-only, NFR-1). The negation token set is preserved; `_NEG_WINDOW`
# ----  is repurposed as the look-behind bound that keeps suppression a strict subset
# ----  of the Cycle-004 rule (a negation matched here was in that window too). ----
_FORBIDDEN_AGENT_WORDS = ("strong", "competitive", "optimal", "calibrated", "complete")
_NEG_WINDOW = 36
_NEGATION_RE = re.compile(
    r"(?:\b(?:no|not|never|non|without|neither|nor)\b|n't)[\s\W]*\Z", re.IGNORECASE)

# ---- cross-regime field/value markers (NFR-5). Affirmative connectives only, so the
# ----  Rung-1 footer's "never compared to" framing is not a false positive. ----
_CROSSREGIME_KEY_RE = re.compile(
    r"cross.?regime|regime.?(comparison|delta|diff|uplift|vs)|uplift|(^|_)vs.?regime", re.IGNORECASE)
_CROSSREGIME_VALUE_RE = re.compile(
    r"\buplift\b|regime-v\d+\s*-?\s*(vs\.?|versus)\s*-?\s*regime-v\d+", re.IGNORECASE)

# ---- raw per-decision body markers (doc 04 §3; the trailing field names of decision /
# ----  terminal rows in eval/schemas.md). The summary never carries decision rows. ----
_DECISION_BODY_MARKERS = frozenset({
    "record_type", "selected_action", "selected_action_type", "decision_index",
    "decision_rows", "private_state_summary", "public_state_summary",
    "last_decision_index", "post_decision_observation", "legal_actions_digest",
    "legal_actions_sample", "decision_latency_ms",
})


def _norm_path(p: str) -> str:
    return p.replace("\\", "/").lstrip("./")


def _hygiene_path_violation(value: str):
    """Parity-or-stricter with eval/hygiene_check.find_violations: first matching
    path rule (or None). Same rules, same order, so the test's parity holds."""
    p = _norm_path(str(value))
    if not p:
        return None
    for rx, reason in _HYGIENE_PATH_RULES:
        if rx.search(p):
            return reason
    return None


def _affirmative_forbidden_words(text: str) -> "list[str]":
    low = text.lower()
    out = []
    for w in _FORBIDDEN_AGENT_WORDS:
        for m in re.finditer(r"\b" + re.escape(w) + r"\b", low):
            # C2: suppress only when a negation token IMMEDIATELY precedes the word
            # (no intervening content word). `_NEGATION_RE` is end-anchored, and the
            # look-behind is bounded by `_NEG_WINDOW`, so any suppression here was also
            # a suppression under the Cycle-004 broad window -> strict subset -> the
            # validator only ever flags MORE affirmative forbidden words, never fewer.
            pre = low[max(0, m.start() - _NEG_WINDOW):m.start()]
            if not _NEGATION_RE.search(pre):
                out.append(w)
    return out


def _classify_unknown_key(key: str) -> str:
    """The most specific reason an out-of-allow-list field can carry (fail-closed)."""
    if key in _DECISION_BODY_MARKERS:
        return "raw per-decision body content (forbidden; the summary carries no decision rows)"
    if _CROSSREGIME_KEY_RE.search(key):
        return "cross-regime field / comparison (forbidden; single-regime only, NFR-5)"
    return "field outside the safe allow-list (doc 04 §2); fail-closed"


def _scan_string(field: str, s: str, out: "list[tuple[str, str]]") -> None:
    """Content checks a path-based gate cannot express (SDD §4.5): hygiene paths,
    inferential terms, affirmative forbidden words, cross-regime connectives."""
    hp = _hygiene_path_violation(s)
    if hp is not None:
        out.append((field, f"Competition-Data path: {hp}"))
    for rx, reason in _INFERENTIAL_RULES:
        if rx.search(s):
            out.append((field, reason))
    for w in _affirmative_forbidden_words(s):
        out.append((field, f"affirmative forbidden agent word: '{w}' (docs/claim-ceiling.md:54-59)"))
    if _CROSSREGIME_VALUE_RE.search(s):
        out.append((field, "cross-regime comparison in value (forbidden; single-regime only, NFR-5)"))


def _enforce_hashes_digest(field_path: str, hashes_dict: dict,
                           out: "list[tuple[str, str]]") -> None:
    """C1 (Cycle-005): every value in a 'hashes'-keyed dict — at ANY nesting depth —
    must be a SHA-256 digest string, never raw content. The Cycle-004 validator
    enforced this on the TOP-LEVEL 'hashes' only (validate_summary's digest block),
    leaving a nested 'hashes' map (e.g. under an agent) a smuggling seam for a clean
    non-digest token. The reason message is identical to that top-level block, so
    assertions keyed on 'SHA-256 digest' / 'Pokemon-Element' match at any position.
    Adds rejections only — a valid nested digest still passes (conservative-only,
    NFR-1)."""
    for rid, hv in hashes_dict.items():
        if not (isinstance(hv, str) and _SHA256_RE.match(hv)):
            out.append((
                f"{field_path}.{rid}",
                "card-identity must be a SHA-256 digest, not raw content "
                "(Competition-Data / Pokemon-Element leak; eval/schemas.md:13-15)",
            ))


def _walk(node, path: str, keys_are_fields: bool, out: "list[tuple[str, str]]") -> None:
    if isinstance(node, dict):
        for k, v in node.items():
            kp = f"{path}.{k}" if path else str(k)
            if keys_are_fields:
                if k not in SAFE_FIELDS:
                    out.append((kp, _classify_unknown_key(str(k))))
            else:
                # keys here are data (run_ids under 'hashes') — scan, don't allow-list.
                _scan_string(kp, str(k), out)
            # C1 (Cycle-005): enforce digest-shape on EVERY 'hashes'-keyed dict, at any
            # depth — not just the top-level block in validate_summary. Closes the
            # nested-'hashes' smuggling seam (a clean non-digest token under, e.g., an
            # agent's 'hashes' map).
            if k == "hashes" and isinstance(v, dict):
                _enforce_hashes_digest(kp, v, out)
            # under 'hashes', the child dict's keys are data, not fields.
            _walk(v, kp, keys_are_fields=(k != "hashes"), out=out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk(v, f"{path}[{i}]", keys_are_fields, out)
    elif isinstance(node, str):
        _scan_string(path, node, out)
    # int / float / bool / None: no string surface to scan.


def validate_summary(obj) -> "list[tuple[str, str]]":
    """Pure, fail-closed allow-list validator. Returns (field, reason) violations;
    empty list => valid. No I/O, no global state — feed it a poisoned dict directly.

    NOTE: the mixed-regime hard-refusal (exit 2) is handled by the --validate path
    (``_collect_regime_ids``), not here; this function reports leak-class (exit 3)
    violations only."""
    out: "list[tuple[str, str]]" = []
    if not isinstance(obj, dict):
        return [("<root>", "summary must be a JSON object")]

    # 1. allow-list, fail-closed, at every nesting level (hashes' keys are data).
    _walk(obj, path="", keys_are_fields=True, out=out)

    # 2. card-identity shape: every 'hashes' value must be a SHA-256 digest, never raw
    #    content — the eval/schemas.md:13-15 mechanism that keeps Pokemon Elements out.
    h = obj.get("hashes")
    if isinstance(h, dict):
        for rid, hv in h.items():
            if not (isinstance(hv, str) and _SHA256_RE.match(hv)):
                out.append((
                    f"hashes.{rid}",
                    "card-identity must be a SHA-256 digest, not raw content "
                    "(Competition-Data / Pokemon-Element leak; eval/schemas.md:13-15)",
                ))
    elif h is not None and not isinstance(h, dict):
        out.append(("hashes", "hashes must be a map of run_id -> SHA-256 digest"))

    return out


def _collect_regime_ids(obj) -> set:
    """Every distinct value carried under a 'regime_id' key, anywhere in the summary.
    More than one => mixed-regime hard refusal (exit 2; NFR-5)."""
    ids = set()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "regime_id":
                    if isinstance(v, str):
                        ids.add(v)
                    elif isinstance(v, list):
                        ids.update(x for x in v if isinstance(x, str))
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(obj)
    return ids


# =====================================================================================
# T1 — CLI dispatch + exit-code contract (0/1/2/3). No --print-schema (OD-C4-5 DEFER).
# =====================================================================================

def _refuse_tracked_out(out_path: Path) -> None:
    """Generator is local-by-default (NG4): never write to docs/ or any ledger file.

    C3 (Cycle-005): repo-root-resolve the candidate path FIRST so an *absolute* path
    into the repo's tracked docs/ tree is refused too — the Cycle-004 guard only
    matched a relative 'docs/...' prefix (an absolute path into repo docs/ slipped it).
    The original relative-docs prefix check and the ledger basename guard are preserved
    verbatim below, so this is conservative-only: strictly more paths refused, none
    newly allowed (NFR-1)."""
    # (C3) absolute OR relative path that resolves inside the repo's tracked docs/ tree.
    resolved = Path(out_path).resolve()
    docs_root = (REPO_ROOT / "docs").resolve()
    if resolved == docs_root or docs_root in resolved.parents:
        raise ValueError(
            f"refusing to write to a tracked docs path '{out_path}' — generator output "
            "is local-by-default (NG4); use a gitignored local path")
    norm = _norm_path(str(out_path))
    parts = norm.split("/")
    if parts and parts[0] == "docs":
        raise ValueError(
            f"refusing to write to a tracked docs path '{out_path}' — generator output "
            "is local-by-default (NG4); use a gitignored local path")
    if Path(norm).name == "ledger.md":
        raise ValueError(
            f"refusing to write a ledger file '{out_path}' — the generator never "
            "mutates docs/ledger.md (NG3)")


def _run_validate(path_str: str) -> int:
    """Independent gate: re-read the named file from disk and validate THAT file."""
    p = Path(path_str)
    try:
        summary = json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        print(f"evidence_summary: input failure — cannot read {path_str}: {e}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError) as e:
        print(f"evidence_summary: input failure — {path_str} is not readable JSON: {e}", file=sys.stderr)
        return 1

    regimes = _collect_regime_ids(summary)
    if len(regimes) > 1:
        print(f"evidence_summary: REFUSED — summary carries multiple regimes "
              f"{sorted(regimes)}; an evidence summary is single-regime only (NFR-5).",
              file=sys.stderr)
        return 2

    violations = validate_summary(summary)
    if violations:
        print(f"evidence_summary: LEAK — refusing {len(violations)} forbidden "
              f"field/value/word(s) (fail-closed, exit 3):", file=sys.stderr)
        for field, reason in violations:
            print(f"  REJECT  {field}  — {reason}", file=sys.stderr)
        return 3

    print(f"evidence_summary: VALID — {path_str} is schema-conforming, sanitized, "
          f"single-regime (exit 0).", file=sys.stderr)
    return 0


def main(argv=None) -> int:
    try:  # robust output regardless of console codepage (Windows cp1252)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

    ap = argparse.ArgumentParser(
        description="Offline sanitized K-batch evidence-summary generator + "
                    "independent fail-closed validator (one regime_id; Rung 1).")
    ap.add_argument("run_dirs", nargs="*",
                    help="sealed run dirs to summarize (e.g. runs/run-v002-b-1 ...)")
    ap.add_argument("--validate", metavar="summary.json", default=None,
                    help="independent validator: re-read this summary file and validate it")
    ap.add_argument("--json", action="store_true",
                    help="emit JSON explicitly (generate-mode is JSON-first regardless)")
    ap.add_argument("--out", default=None,
                    help="write the summary to this LOCAL/gitignored path instead of "
                         "stdout; never a tracked path (NG4)")
    args = ap.parse_args(argv)

    # ---- validate mode ----
    if args.validate is not None:
        return _run_validate(args.validate)

    # ---- generate mode ----
    if not args.run_dirs:
        print("evidence_summary: no run dirs given (generate mode) — "
              "pass <run_dir> ... or use --validate <summary.json>", file=sys.stderr)
        return 1
    try:
        summary = build_summary([Path(p) for p in args.run_dirs])
    except MixedRegimeRefusal as e:
        print(f"evidence_summary: REFUSED — {e}", file=sys.stderr)
        return 2
    except (FileNotFoundError, ValueError) as e:
        print(f"evidence_summary: input failure — {e}", file=sys.stderr)
        return 1

    # C4 (Cycle-005): an empty `hashes` map means no manifest carried a SHA-256
    # integrity stamp for any run — provenance is un-stamped. Surface it on stderr
    # (exit stays 0; JSON-first stdout untouched) so it is never silently treated as
    # strong provenance. Manifest-only sourcing is unchanged — no new hash-source
    # file is read; a future promotion gate (Cycle-006+) MUST reject this.
    if not summary.get("hashes"):
        print("evidence_summary: WARNING — empty hashes (no manifest integrity stamp "
              "found); provenance is un-stamped and a future promotion gate must "
              "reject this.", file=sys.stderr)

    text = render_json(summary)  # JSON-first; --json is accepted but JSON is the default form
    if args.out:
        out_path = Path(args.out)
        try:
            _refuse_tracked_out(out_path)
        except ValueError as e:
            print(f"evidence_summary: {e}", file=sys.stderr)
            return 1
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
        print(f"evidence_summary: wrote {args.out}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
