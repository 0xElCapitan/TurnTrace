#!/usr/bin/env python3
"""``analysis/trace_diagnostic.py`` — offline, stdlib-only, single-regime
**descriptive** trace diagnostic (Cycle-008 S01; PRD C8-FR-1/2; SDD §2).

The first ``analysis/`` module to read ``traces/<match_id>.jsonl`` rows **for
content** (SDD §2.1; ``replay_check.py`` opens them only to recompute a hash).
It turns existing sealed run dirs into a sanitized, JSON-first, single-regime
diagnostic object bounded to the **five** authorized descriptive surfaces
(SDD §2.2). It reports **what occurred** — it never judges play quality, never
scores a decision, never recommends a move (OD-C8-2; NFR-3, NFR-10).

The module co-locates two cores in one file (SDD-C8-1, the ``evidence_summary.py``
pattern of record): the **generator** (``build_diagnostic`` — S01) and the
**fail-closed output sanitizer** (``validate_diagnostic`` + ``--validate`` — S02),
sharing the one ``SAFE_FIELDS`` allow-list so the doc<->code key-set cannot drift.

Reads (only), per ``run_id``, both read-only:
  * ``runs/<run_id>/manifest.json`` — read **first**, the ``regime_id`` authority
    (mirroring ``dispersion_report.py:126-141`` / ``evidence_summary.py:147-161``),
    so the single-regime guard fires before any content is touched.
  * ``runs/<run_id>/match_results/*.json`` — via ``aggregate.aggregate_run`` (the
    sanctioned per-run sanitized rollup + regime authority), **and** directly for
    per-match ``result`` / ``ending_cause`` / ``wall_clock_ms`` /
    ``invalid_action_count`` / ``timeout`` distributions.
  * ``runs/<run_id>/traces/<match_id>.jsonl`` — decision rows (for
    ``public_state_summary`` board counts and ``decision_latency_ms``) and the
    terminal row (for ``final_prize_counts``).

Safe aggregate output keys, never raw decision-body field names (RN-2): the raw
fields ``decision_latency_ms`` / ``public_state_summary`` are READ internally but
emitted only under safe derived keys (``latency_ms_stats`` / ``bench_count_stats``
/ ``active_present_rate`` / ``prize_trajectory_stats`` …). The ``SAFE_FIELDS``
allow-list below is the single source of truth for the output keys, and is
disjoint from ``evidence_summary._DECISION_BODY_MARKERS`` (asserted by a test).

Reuse, not recompute (SDD §2.3): ``descriptive_stats`` / ``STAT_COLUMNS`` are
imported from ``analysis.dispersion_report`` and ``aggregate_run`` from
``analysis.aggregate`` — so **no new statistic and no inferential statistic can
enter** through this module. No sample standard deviation, variance, confidence
interval, or p-value is computed anywhere; their absence is structural.

# loa:shortcut: _refuse_tracked_out is a self-contained parity copy of
# evidence_summary.py:451-476, keeping this module's dependency surface to
# aggregate + dispersion_report (the same two intra-analysis helpers the sibling
# diagnostics use). Upgrade trigger: none — the guard is small, stable, and
# security-relevant, so a single-file auditable copy is preferred over coupling
# to evidence_summary's evolving validator surface.

``analysis/`` imports run-dir artifacts + intra-zone helpers only — no ``cabt``,
``sim/``, ``agents/runtime/``, or ``eval/`` (the offline/runtime separation;
enforced by ``tests/test_import_direction.py``). stdlib only (NFR-1, NFR-2).

CLI:
  generate:  python analysis/trace_diagnostic.py <run_dir> [<run_dir> ...] [--json] [--out <local-path>]
  validate:  python analysis/trace_diagnostic.py --validate <diagnostic.json>
Exit: 0 diagnostic produced / valid · 1 input failure · 2 mixed-regime refusal ·
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

import aggregate  # noqa: E402  (analysis/ — intra-zone; per-run sanitized stats + authority)
import dispersion_report  # noqa: E402  (analysis/ — intra-zone; reused stat surface)

# ---- reuse the proven descriptive-stat surface (no recompute; SDD §2.3) ----
STAT_COLUMNS = dispersion_report.STAT_COLUMNS              # the seven descriptive stats
descriptive_stats = dispersion_report.descriptive_stats   # pure arithmetic; no inferential stat
MixedRegimeRefusal = dispersion_report.MixedRegimeRefusal  # exit-2 refusal type

# =====================================================================================
# Fixed sanitized enums (from eval/schemas.md:32-33). result is a non-nullable enum;
# ending_cause is nullable / may carry an unrecognized value -> bucketed as "<unmapped>"
# (the failure_report.py honesty pattern: counted, never silently dropped).
# =====================================================================================
_OUTCOME_ENUM_ORDER = ("win", "loss", "draw", "error")
_ENDING_CAUSE_ORDER = ("prize-out", "deck-out", "no-active", "card-effect", "error")
_UNMAPPED = "<unmapped>"

# =====================================================================================
# SAFE_FIELDS — the single source of truth for the diagnostic's output keys (SDD §2.4),
# mirroring evidence_summary.py:78-90. A test asserts the generated output key-set, at
# EVERY nesting depth, is a subset of this allow-list, that no key matches a
# quality/score/recommendation pattern, and that it is disjoint from the raw
# decision-body marker set. A future edit that adds a scorer field fails that test.
# =====================================================================================

# identity / provenance / framing field names.
_IDENTITY_FIELDS = frozenset({
    "regime_id", "n_runs", "run_ids", "n_matches", "n_decisions", "mode",
    "unseeded_caveat", "claim_ceiling",
})
# the five authorized descriptive surfaces, under safe aggregate names (RN-2).
_SURFACE_FIELDS = frozenset({
    "outcome_counts", "ending_cause_counts",                  # surface 1
    "bench_count_stats", "active_present_rate",               # surface 2
    "prize_trajectory_stats", "final_prize_counts_by_side",   # surface 3
    "latency_ms_stats", "wall_clock_ms_stats",                # surface 4
    "error_presence_count", "illegal_action_total",
    "illegal_action_excluded", "timeout",                     # surface 5
})
# per-side sub-keys for the two-sided board / prize surfaces.
_SIDE_FIELDS = frozenset({"p0", "p1"})
# the sanitized outcome / ending-cause vocabulary that appears as count-dict keys.
_OUTCOME_ENUM = frozenset(_OUTCOME_ENUM_ORDER)
_ENDING_CAUSE_ENUM = frozenset(_ENDING_CAUSE_ORDER) | {_UNMAPPED}

SAFE_FIELDS = frozenset(
    _IDENTITY_FIELDS
    | _SURFACE_FIELDS
    | _SIDE_FIELDS
    | _OUTCOME_ENUM
    | _ENDING_CAUSE_ENUM
    | set(STAT_COLUMNS)  # the seven statistic names appear inside every *_stats object
)

# ---- two framing strings (descriptive-only posture; no ceiling of its own). Worded to
# ----  pass the S02 co-located sanitizer: no affirmative forbidden agent word, no
# ----  inferential term, no cross-regime connective. ----
_UNSEEDED_CAVEAT = (
    "seed_controlled=false; these observed distributions reflect the whole unseeded "
    "process (agent behaviour together with uncontrolled simulator RNG), not an "
    "isolated agent-only quantity (docs/claim-ceiling.md:42-52)."
)
_RUNG1_FOOTER = (
    "Descriptive trace-safe diagnostic over one regime_id: reports what occurred. NO "
    "gameplay-strength claim and NO inferential claim; no per-decision quality, score, "
    "or recommendation. This diagnostic carries no ceiling of its own — the experiment "
    "ledger (docs/ledger.md) is the only ceiling-bearing artifact (NFR-5)."
)


# =====================================================================================
# Read helpers
# =====================================================================================

def _load_manifest(run_dir: Path) -> dict:
    mp = run_dir / "manifest.json"
    if not mp.exists():
        raise FileNotFoundError(f"{run_dir}: missing manifest.json")
    return json.loads(mp.read_text(encoding="utf-8"))


def _iter_trace_rows(trace_path: Path):
    """Yield each JSON object from a JSONL sidecar (one record per line)."""
    for line in trace_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            yield json.loads(line)


def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _collect_side_int(side_obj, acc: dict) -> None:
    """Append per-side integer counts from a ``{"p0": int, "p1": int}`` sub-object."""
    if isinstance(side_obj, dict):
        for s in ("p0", "p1"):
            v = side_obj.get(s)
            if _is_int(v):
                acc[s].append(v)


def _collect_side_bool(side_obj, acc: dict) -> None:
    """Append per-side booleans from a ``{"p0": bool, "p1": bool}`` sub-object."""
    if isinstance(side_obj, dict):
        for s in ("p0", "p1"):
            v = side_obj.get(s)
            if isinstance(v, bool):
                acc[s].append(v)


def _rate(bools: "list") -> "float | None":
    """Fraction True over the present booleans (descriptive presence rate). None if empty."""
    vals = [1.0 if b else 0.0 for b in bools if isinstance(b, bool)]
    if not vals:
        return None
    return round(sum(vals) / len(vals), 4)


# =====================================================================================
# Generator core (build_diagnostic). Read surface = SDD §2.1.
# =====================================================================================

def build_diagnostic(run_dirs: "list[Path]") -> dict:
    """Build the SDD §2.2 single-regime descriptive diagnostic over the run dirs.

    Reads each ``manifest.json`` FIRST (regime authority), hard-refuses mixed regimes
    (``MixedRegimeRefusal`` -> exit 2) before any aggregation, then aggregates the five
    authorized descriptive surfaces using only already-recorded fields and the reused
    ``descriptive_stats`` helper. Returns the JSON-first diagnostic dict (writing is the
    CLI's job). Runs no eval and creates no run dir."""
    if not run_dirs:
        raise ValueError("no run dirs given")

    # ---- read the authoritative regime_id from every manifest FIRST ----
    manifests = [(rd, _load_manifest(rd)) for rd in run_dirs]
    regimes = {man.get("regime_id") for _, man in manifests}

    # ---- HARD single-regime guard (exit 2) — before any aggregation (SDD §2.5) ----
    if len(regimes) != 1:
        raise MixedRegimeRefusal(
            f"refusing to diagnose across regimes: the input run dirs carry "
            f"{sorted(str(r) for r in regimes)}. A trace diagnostic covers ONE "
            f"regime_id only (NFR-5) — a v002 number is never aggregated beside a "
            f"v001 number. Re-run with run dirs that all share one regime_id."
        )
    regime_id = next(iter(regimes))

    # ---- accumulators ----
    run_ids: "list[str]" = []
    n_matches = 0
    n_decisions = 0
    mode = None
    outcome_counts = {k: 0 for k in _OUTCOME_ENUM_ORDER}
    ending_cause_counts = {k: 0 for k in (*_ENDING_CAUSE_ORDER, _UNMAPPED)}
    error_presence_count = 0
    illegal_action_total = 0
    illegal_action_excluded = 0
    wall_clocks: "list[int]" = []
    bench = {"p0": [], "p1": []}
    active = {"p0": [], "p1": []}
    prize = {"p0": [], "p1": []}
    final_prize = {"p0": [], "p1": []}
    latencies: "list[int]" = []

    for rd, man in manifests:
        # reuse the sanctioned per-run reader (outcome surface authority + regime cross-check)
        stats = aggregate.aggregate_run(rd)  # reads match_results/*.json only
        if stats.get("regime_id") != man.get("regime_id"):
            raise ValueError(
                f"{rd.name}: records regime '{stats.get('regime_id')}' != manifest "
                f"regime '{man.get('regime_id')}'")
        run_ids.append(stats.get("run_id") or man.get("run_id"))
        n_matches += stats.get("n_matches") or 0
        if mode is None:
            mode = man.get("mode") or "unseeded"

        # ---- surfaces 1 & 5: per-match read (result / ending_cause / errors / illegal / wall) ----
        for p in sorted((rd / "match_results").glob("*.json")):
            rec = json.loads(p.read_text(encoding="utf-8"))
            res = rec.get("result")
            if res in outcome_counts:
                outcome_counts[res] += 1
            ec = rec.get("ending_cause")
            ending_cause_counts[ec if ec in ending_cause_counts else _UNMAPPED] += 1
            # error surfaced as a PRESENCE flag only — the error string body is never read out.
            if res == "error" or rec.get("error") not in (None, ""):
                error_presence_count += 1
            # illegal-action total summed only where detectable; exclusion is counted, not dropped.
            if rec.get("invalid_action_detectable") is True:
                illegal_action_total += rec.get("invalid_action_count") or 0
            else:
                illegal_action_excluded += 1
            wc = rec.get("wall_clock_ms")
            if _is_int(wc):
                wall_clocks.append(wc)

        # ---- surfaces 2, 3 & 4: trace read (the structural first) ----
        traces_dir = rd / "traces"
        if traces_dir.is_dir():
            for tp in sorted(traces_dir.glob("*.jsonl")):
                for row in _iter_trace_rows(tp):
                    rt = row.get("record_type")
                    if rt == "decision":
                        n_decisions += 1
                        pss = row.get("public_state_summary")
                        if isinstance(pss, dict):
                            _collect_side_int(pss.get("bench_count"), bench)
                            _collect_side_bool(pss.get("active_present"), active)
                            _collect_side_int(pss.get("prize_count"), prize)
                        lat = row.get("decision_latency_ms")
                        if _is_int(lat):
                            latencies.append(lat)
                    elif rt == "terminal":
                        fpc = row.get("final_prize_counts")
                        if isinstance(fpc, list) and len(fpc) == 2:
                            if _is_int(fpc[0]):
                                final_prize["p0"].append(fpc[0])
                            if _is_int(fpc[1]):
                                final_prize["p1"].append(fpc[1])

    return {
        # identity / framing
        "regime_id": regime_id,
        "n_runs": len(run_dirs),
        "run_ids": sorted(r for r in run_ids if r is not None),
        "n_matches": n_matches,
        "n_decisions": n_decisions,
        "mode": mode or "unseeded",
        # surface 1 — outcome / ending-cause aggregates
        "outcome_counts": outcome_counts,
        "ending_cause_counts": ending_cause_counts,
        # surface 2 — board-shape distributions (safe aggregate names; RN-2)
        "bench_count_stats": {s: descriptive_stats(bench[s]) for s in ("p0", "p1")},
        "active_present_rate": {s: _rate(active[s]) for s in ("p0", "p1")},
        # surface 3 — prize trajectory
        "prize_trajectory_stats": {s: descriptive_stats(prize[s]) for s in ("p0", "p1")},
        "final_prize_counts_by_side": {s: descriptive_stats(final_prize[s]) for s in ("p0", "p1")},
        # surface 4 — latency / throughput (aggregate stats only — never raw rows)
        "latency_ms_stats": descriptive_stats(latencies),
        "wall_clock_ms_stats": descriptive_stats(wall_clocks),
        # surface 5 — error / illegal / timeout descriptive surfaces
        "error_presence_count": error_presence_count,
        "illegal_action_total": illegal_action_total,
        "illegal_action_excluded": illegal_action_excluded,
        "timeout": None,  # the soft, undetectable signal it is (eval/schemas.md:35)
        # framing
        "unseeded_caveat": _UNSEEDED_CAVEAT,
        "claim_ceiling": _RUNG1_FOOTER,
    }


def render_json(diag: dict) -> str:
    """JSON-first serialization (the primary form; mirror evidence_summary.py:219-221)."""
    return json.dumps(diag, indent=2, sort_keys=True)


# =====================================================================================
# S02 — Co-located fail-closed output sanitizer (validate_diagnostic + --validate).
#
# Pure, fail-closed, allow-list validator co-located in the SAME module as the
# generator and its SAFE_FIELDS allow-list (SDD-C8-1), so the doc<->code key-set
# cannot drift. Parity-or-stricter with analysis/evidence_summary.py's validator and
# eval/hygiene_check.py. The walk rejects any field outside SAFE_FIELDS at EVERY
# nesting depth with the MOST-SPECIFIC reason (decision-body marker > cross-regime >
# numeric-M > Rung-3 governance > quality/coaching > generic out-of-allow-list). The
# diagnostic reports WHAT OCCURRED; it never judges play quality, scores a decision, or
# recommends a move (OD-C8-2; NFR-3, NFR-10) — the sanitizer is the mechanical floor
# under that posture. One rejection class is genuinely new to Cycle-008: the
# numeric-`M`-shaped governance-threshold token (SDD-C8-5), riding the existing exit-3
# path (no new exit code).
#
# loa:shortcut: the rejection-class surface below (hygiene path rules, inferential /
# forbidden-word / cross-regime / SHA-256 rules, decision-body markers) is a parity-
# TESTED stdlib copy of evidence_summary.py:233-365 — NOT an eval/ import. The standing
# offline/runtime separation forbids analysis/ importing eval/ (test_import_direction),
# and the proven pattern is a single-file auditable copy (evidence_summary itself copies
# the hygiene rules from eval/hygiene_check.py the same way). Upgrade trigger: none —
# this is the import-direction rule (SDD §7), not a temporary shortcut. Parity is
# asserted by a test against eval/hygiene_check.find_violations and against
# evidence_summary._DECISION_BODY_MARKERS.
# =====================================================================================

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

# ---- copied parity-tested hygiene path rules (eval/hygiene_check.py:35-45). A test
# ----  asserts parity-or-stricter vs eval/hygiene_check.find_violations. ----
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

# ---- inferential-statistic vocabulary (NFR-3). Bare 'hypothesis' is allowed
# ----  (provenance text); only the compound 'hypothesis-test' is rejected. ----
_INFERENTIAL_RULES = [
    (re.compile(r"\bstd[\s\-]?dev\b", re.IGNORECASE), "inferential statistic: std-dev"),
    (re.compile(r"\bstandard\s+deviation\b", re.IGNORECASE), "inferential statistic: standard deviation"),
    (re.compile(r"\bvariance\b", re.IGNORECASE), "inferential statistic: variance"),
    (re.compile(r"\bconfidence\s+interval(s)?\b", re.IGNORECASE), "inferential statistic: confidence interval"),
    (re.compile(r"\bCI\b"), "inferential statistic: CI / confidence interval"),
    (re.compile(r"\bp[\s\-]?value(s)?\b", re.IGNORECASE), "inferential statistic: p-value"),
    (re.compile(r"\bsignifican(ce|t)\b", re.IGNORECASE), "inferential statistic: significance"),
    (re.compile(r"\bhypothesis[\s\-]?test(ing)?\b", re.IGNORECASE),
     "inferential statistic: hypothesis-test (bare 'hypothesis' provenance text is allowed)"),
    (re.compile(r"\berror[\s\-]?bar(s)?\b", re.IGNORECASE), "inferential statistic: error-bar"),
]

# ---- forbidden agent words (docs/claim-ceiling.md:93-98) — rejected only when
# ----  AFFIRMATIVE; suppressed ONLY by an IMMEDIATELY-preceding negation token. ----
_FORBIDDEN_AGENT_WORDS = ("strong", "competitive", "optimal", "calibrated", "complete")
_NEG_WINDOW = 36
_NEGATION_RE = re.compile(
    r"(?:\b(?:no|not|never|non|without|neither|nor)\b|n't)[\s\W]*\Z", re.IGNORECASE)

# ---- cross-regime field/value markers (NFR-5). Affirmative connectives only, so the
# ----  footer's "never compared / never aggregated" framing is not a false positive. ----
_CROSSREGIME_KEY_RE = re.compile(
    r"cross.?regime|regime.?(comparison|delta|diff|uplift|vs)|uplift|(^|_)vs.?regime", re.IGNORECASE)
_CROSSREGIME_VALUE_RE = re.compile(
    r"\buplift\b|regime-v\d+\s*-?\s*(vs\.?|versus)\s*-?\s*regime-v\d+", re.IGNORECASE)

# ---- raw per-decision body markers — the diagnostic emits only safe AGGREGATE keys
# ----  (RN-2), never these raw decision/terminal-row field names. Parity copy of
# ----  evidence_summary._DECISION_BODY_MARKERS (a test asserts equality / no drift). ----
_DECISION_BODY_MARKERS = frozenset({
    "record_type", "selected_action", "selected_action_type", "decision_index",
    "decision_rows", "private_state_summary", "public_state_summary",
    "last_decision_index", "post_decision_observation", "legal_actions_digest",
    "legal_actions_sample", "decision_latency_ms",
})

# ---- quality / scoring / recommendation / coaching key vocabulary (OD-C8-2; NFR-3,
# ----  NFR-10). KEY patterns ONLY — values are deliberately NOT scanned for these, so
# ----  the Rung-1 footer may say "no per-decision quality, score, or recommendation"
# ----  without self-rejecting. Mirrors tests/test_trace_diagnostic._QUALITY_PATTERNS. ----
_QUALITY_KEY_PATTERNS = (
    "quality", "score", "recommend", "should", "optimal", "best", "worse", "better",
    "mistake", "blunder", "rating", "grade", "coach", "advice", "advise", "suggest",
    "lethal", "missed", "wasted", "judge", "judgment", "improve", "policy",
)

# ---- numeric-`M`-shaped governance-threshold tokens (SDD-C8-5; NFR-7; the NEW class).
# ----  The diagnostic carries no ceiling and no margin; a numeric promotion-margin /
# ----  comparison-budget field (key + numeric value) or value token is a posture leak,
# ----  rejected fail-closed on the exit-3 path (no new exit code). ----
_NUMERIC_M_KEY_RE = re.compile(
    r"^M$|^K$|^n$|margin|comparison.?budget|(^|_)budget($|_)|threshold", re.IGNORECASE)
_NUMERIC_M_VALUE_RE = re.compile(
    r"\bM\s*[=:]\s*-?\d|\bpromotion\s+margin\b|\bcomparison\s+budget\b|"
    r"\bmargin\s*[=:]\s*-?\d|\bthreshold\s*[=:]\s*-?\d", re.IGNORECASE)

# ---- Rung-3 / promotion-governance semantics (the diagnostic selects/freezes nothing
# ----  and advances no ceiling). The bare ledger-citation "claim-ceiling" / "Rung 1/2"
# ----  framing in the footer is NOT matched (no 'rung 3', 'candidate', 'advance'). ----
_GOVERNANCE_KEY_RE = re.compile(
    r"rung.?3|candidate|pre.?registrat|fresh.?evidence|value.?promot|sp.?6|"
    r"claim.?advance|target.?regime|feature.?family", re.IGNORECASE)
_GOVERNANCE_VALUE_RE = re.compile(
    r"\brung[\s\-]?3\b|\bSP[\s\-]?6\b|pre[\s\-]?registrat|fresh[\s\-]?evidence|"
    r"value[\s\-]?promot|claim[\s\-]?advance|\bcandidate\b", re.IGNORECASE)

# ---- externally-sourced raw content (Discord screenshot / peer data / Kaggle /
# ----  Daily-Top-Episode / raw simulator log / run-dir dump). VALUE patterns scoped to
# ----  prose that never appears in the sanitized framing strings (e.g. 'simulator log',
# ----  not the footer's 'simulator RNG'). ----
_RAW_CONTENT_VALUE_RULES = [
    (re.compile(r"\bdiscord\b", re.IGNORECASE), "Discord content (peer / scouting data)"),
    (re.compile(r"\bkaggle\b", re.IGNORECASE), "Kaggle competition data"),
    (re.compile(r"daily[\s_-]?top[\s_-]?episode", re.IGNORECASE), "Daily-Top-Episode peer data"),
    (re.compile(r"\bpeer[\s_-]+(data|deck|episode|screenshot)\b", re.IGNORECASE), "peer data"),
    (re.compile(r"\bscreenshot\b", re.IGNORECASE), "screenshot (possible Competition Data)"),
    (re.compile(r"simulator[\s_-]?log", re.IGNORECASE), "raw simulator log"),
    (re.compile(r"\brun[\s_-]?dir[\s_-]?(dump|tree)\b", re.IGNORECASE), "run-dir dump"),
]


def _norm_path(p: str) -> str:
    return p.replace("\\", "/").lstrip("./")


def _hygiene_path_violation(value: str):
    """Parity-or-stricter with eval/hygiene_check.find_violations: first matching path
    rule (or None). Same rules, same order, so the parity test holds."""
    p = _norm_path(str(value))
    if not p:
        return None
    for rx, reason in _HYGIENE_PATH_RULES:
        if rx.search(p):
            return reason
    return None


def _is_number(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _affirmative_forbidden_words(text: str) -> "list[str]":
    low = text.lower()
    out = []
    for w in _FORBIDDEN_AGENT_WORDS:
        for m in re.finditer(r"\b" + re.escape(w) + r"\b", low):
            # suppress only when a negation token IMMEDIATELY precedes the word (bounded
            # look-behind) — a strict subset of any broad-window rule (conservative-only).
            pre = low[max(0, m.start() - _NEG_WINDOW):m.start()]
            if not _NEGATION_RE.search(pre):
                out.append(w)
    return out


def _quality_key_hit(key: str):
    low = str(key).lower()
    for pat in _QUALITY_KEY_PATTERNS:
        if pat in low:
            return pat
    return None


def _classify_unknown_key(key: str, value) -> str:
    """The most specific reason an out-of-allow-list field can carry (fail-closed).
    Specificity order: decision-body marker > cross-regime > numeric-M > Rung-3
    governance > quality/coaching > generic out-of-allow-list."""
    if key in _DECISION_BODY_MARKERS:
        return ("raw per-decision body content (forbidden; the diagnostic emits only "
                "safe aggregate keys, never raw decision rows — RN-2)")
    if _CROSSREGIME_KEY_RE.search(key):
        return "cross-regime field / comparison (forbidden; single-regime only, NFR-5)"
    if _NUMERIC_M_KEY_RE.search(key) and _is_number(value):
        return ("numeric-M-shaped governance threshold (promotion margin / comparison "
                "budget) — the diagnostic carries no ceiling and no margin (NFR-7; SDD-C8-5)")
    if _GOVERNANCE_KEY_RE.search(key):
        return ("Rung-3 / promotion-governance semantics (target / candidate / "
                "pre-registration / fresh-evidence / value-promotion / SP-6 / claim-advance) "
                "— the diagnostic selects nothing and advances no ceiling (OD-C8-2)")
    qh = _quality_key_hit(key)
    if qh is not None:
        return (f"quality / scoring / recommendation / coaching surface ('{qh}') — the "
                f"diagnostic reports what occurred, never judges play quality "
                f"(OD-C8-2; NFR-3, NFR-10)")
    return "field outside the safe allow-list (SDD §2.4 SAFE_FIELDS); fail-closed"


def _scan_string(field: str, s: str, out: "list[tuple[str, str]]") -> None:
    """Content checks a key allow-list cannot express: hygiene paths, inferential terms,
    affirmative forbidden words, cross-regime connectives, numeric-M tokens, Rung-3
    governance semantics, and externally-sourced raw content."""
    hp = _hygiene_path_violation(s)
    if hp is not None:
        out.append((field, f"Competition-Data path: {hp}"))
    for rx, reason in _INFERENTIAL_RULES:
        if rx.search(s):
            out.append((field, reason))
    for w in _affirmative_forbidden_words(s):
        out.append((field, f"affirmative forbidden agent word: '{w}' (docs/claim-ceiling.md:93-98)"))
    if _CROSSREGIME_VALUE_RE.search(s):
        out.append((field, "cross-regime comparison in value (forbidden; single-regime only, NFR-5)"))
    if _NUMERIC_M_VALUE_RE.search(s):
        out.append((field, "numeric-M-shaped governance threshold in value (promotion margin / "
                           "comparison budget) — the diagnostic carries no margin (NFR-7; SDD-C8-5)"))
    if _GOVERNANCE_VALUE_RE.search(s):
        out.append((field, "Rung-3 / promotion-governance semantics in value — the diagnostic "
                           "selects nothing and advances no ceiling (OD-C8-2)"))
    for rx, reason in _RAW_CONTENT_VALUE_RULES:
        if rx.search(s):
            out.append((field, f"externally-sourced raw content: {reason}"))


def _enforce_hashes_digest(field_path: str, hashes_dict: dict,
                           out: "list[tuple[str, str]]") -> None:
    """Every value in a 'hashes'-keyed dict — at ANY nesting depth — must be a SHA-256
    digest string, never raw content (a card-identity / Pokemon-Element leak vector;
    eval/schemas.md:13-15). Parity with evidence_summary._enforce_hashes_digest."""
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
                    out.append((kp, _classify_unknown_key(str(k), v)))
            else:
                # keys here are data (e.g. run_ids under 'hashes') — scan, don't allow-list.
                _scan_string(kp, str(k), out)
            # enforce digest-shape on EVERY 'hashes'-keyed dict, at any depth.
            if k == "hashes" and isinstance(v, dict):
                _enforce_hashes_digest(kp, v, out)
            # under 'hashes', the child dict's keys are data, not allow-listed fields.
            _walk(v, kp, keys_are_fields=(k != "hashes"), out=out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk(v, f"{path}[{i}]", keys_are_fields, out)
    elif isinstance(node, str):
        _scan_string(path, node, out)
    # int / float / bool / None: no string surface to scan.


def validate_diagnostic(obj) -> "list[tuple[str, str]]":
    """Pure, fail-closed allow-list validator for a diagnostic object. Returns (field,
    reason) violations; an empty list means valid (exit 0). No I/O, no global state —
    feed it a poisoned dict directly.

    SAFE_FIELDS (the generator's own allow-list, above) is the single source of truth;
    every field outside it is rejected at every nesting depth with the most-specific
    reason. The mixed-regime hard-refusal (exit 2) is handled by the --validate path
    (``_collect_regime_ids``), not here; this reports leak-class (exit 3) violations only."""
    out: "list[tuple[str, str]]" = []
    if not isinstance(obj, dict):
        return [("<root>", "diagnostic must be a JSON object")]
    _walk(obj, path="", keys_are_fields=True, out=out)
    return out


def _collect_regime_ids(obj) -> set:
    """Every distinct value carried under a 'regime_id' key, anywhere in the diagnostic.
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


def _run_validate(path_str: str) -> int:
    """Independent gate: re-read the named diagnostic file from disk and validate THAT
    file. Exit 0 valid · 1 input failure · 2 mixed-regime refusal · 3 forbidden leak."""
    p = Path(path_str)
    try:
        diag = json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        print(f"trace_diagnostic: input failure — cannot read {path_str}: {e}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError) as e:
        print(f"trace_diagnostic: input failure — {path_str} is not readable JSON: {e}", file=sys.stderr)
        return 1

    regimes = _collect_regime_ids(diag)
    if len(regimes) > 1:
        print(f"trace_diagnostic: REFUSED — diagnostic carries multiple regimes "
              f"{sorted(regimes)}; a trace diagnostic is single-regime only (NFR-5).",
              file=sys.stderr)
        return 2

    violations = validate_diagnostic(diag)
    if violations:
        print(f"trace_diagnostic: LEAK — refusing {len(violations)} forbidden "
              f"field/value/word(s) (fail-closed, exit 3):", file=sys.stderr)
        for field, reason in violations:
            print(f"  REJECT  {field}  — {reason}", file=sys.stderr)
        return 3

    print(f"trace_diagnostic: VALID — {path_str} is sanitized, single-regime, "
          f"allow-list-clean (exit 0).", file=sys.stderr)
    return 0


# =====================================================================================
# CLI dispatch (generate + --validate; exit 0/1/2/3).
# =====================================================================================

def _refuse_tracked_out(out_path: Path) -> None:
    """Generator is local-by-default (ESP-1): never write to docs/ or any ledger file.

    Parity copy of evidence_summary.py:451-476 (the proven guard pattern). Repo-root-
    resolves the candidate FIRST so an *absolute* path into the repo's tracked docs/
    tree is refused too; the relative-docs prefix check and the ledger basename guard
    are preserved verbatim — conservative-only (strictly more paths refused)."""
    resolved = Path(out_path).resolve()
    docs_root = (REPO_ROOT / "docs").resolve()
    if resolved == docs_root or docs_root in resolved.parents:
        raise ValueError(
            f"refusing to write to a tracked docs path '{out_path}' — diagnostic output "
            "is local-by-default (ESP-1); use a gitignored local path")
    norm = str(out_path).replace("\\", "/").lstrip("./")
    parts = norm.split("/")
    if parts and parts[0] == "docs":
        raise ValueError(
            f"refusing to write to a tracked docs path '{out_path}' — diagnostic output "
            "is local-by-default (ESP-1); use a gitignored local path")
    if Path(norm).name == "ledger.md":
        raise ValueError(
            f"refusing to write a ledger file '{out_path}' — the diagnostic never "
            "mutates docs/ledger.md")


def main(argv=None) -> int:
    try:  # robust output regardless of console codepage (Windows cp1252)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

    ap = argparse.ArgumentParser(
        description="Offline single-regime descriptive trace diagnostic over sealed "
                    "run dirs (reports what occurred; no quality judgment).")
    ap.add_argument("run_dirs", nargs="*",
                    help="sealed run dirs to diagnose (e.g. runs/run-v002-b-1 ...)")
    ap.add_argument("--validate", metavar="diagnostic.json", default=None,
                    help="independent fail-closed sanitizer: re-read this diagnostic file "
                         "and validate it (exit 0/1/2/3)")
    ap.add_argument("--json", action="store_true",
                    help="emit JSON explicitly (generate-mode is JSON-first regardless)")
    ap.add_argument("--out", default=None,
                    help="write the diagnostic to this LOCAL/gitignored path instead of "
                         "stdout; never a tracked path (ESP-1)")
    args = ap.parse_args(argv)

    # ---- validate mode (re-read + re-validate a diagnostic file; the co-located gate) ----
    if args.validate is not None:
        return _run_validate(args.validate)

    # ---- generate mode ----
    if not args.run_dirs:
        print("trace_diagnostic: no run dirs given (generate mode) — pass <run_dir> ... "
              "or use --validate <diagnostic.json>", file=sys.stderr)
        return 1
    try:
        diag = build_diagnostic([Path(p) for p in args.run_dirs])
    except MixedRegimeRefusal as e:
        print(f"trace_diagnostic: REFUSED — {e}", file=sys.stderr)
        return 2
    except (FileNotFoundError, ValueError) as e:
        print(f"trace_diagnostic: input failure — {e}", file=sys.stderr)
        return 1

    text = render_json(diag)  # JSON-first; --json is accepted but JSON is the default form
    if args.out:
        out_path = Path(args.out)
        try:
            _refuse_tracked_out(out_path)
        except ValueError as e:
            print(f"trace_diagnostic: {e}", file=sys.stderr)
            return 1
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
        print(f"trace_diagnostic: wrote {args.out}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
