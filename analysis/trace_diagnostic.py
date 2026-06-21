#!/usr/bin/env python3
"""``analysis/trace_diagnostic.py`` — offline, stdlib-only, single-regime
**descriptive** trace diagnostic (Cycle-008 S01; PRD C8-FR-1/2; SDD §2).

The first ``analysis/`` module to read ``traces/<match_id>.jsonl`` rows **for
content** (SDD §2.1; ``replay_check.py`` opens them only to recompute a hash).
It turns existing sealed run dirs into a sanitized, JSON-first, single-regime
diagnostic object bounded to the **five** authorized descriptive surfaces
(SDD §2.2). It reports **what occurred** — it never judges play quality, never
scores a decision, never recommends a move (OD-C8-2; NFR-3, NFR-10).

This is the **generator path only** (S01). The co-located fail-closed sanitizer
(``validate_diagnostic`` + ``--validate``) lands in S02; it is deliberately not
present here.

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
Exit (S01 generate path): 0 diagnostic produced · 1 input failure ·
      2 mixed-regime refusal. (Exit 3 — forbidden-field leak — arrives with the
      co-located ``--validate`` sanitizer in S02.)
"""

from __future__ import annotations

import argparse
import json
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
# CLI dispatch (generate-only; exit 0/1/2). The co-located --validate sanitizer is S02.
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
    ap.add_argument("--json", action="store_true",
                    help="emit JSON explicitly (generate-mode is JSON-first regardless)")
    ap.add_argument("--out", default=None,
                    help="write the diagnostic to this LOCAL/gitignored path instead of "
                         "stdout; never a tracked path (ESP-1)")
    args = ap.parse_args(argv)

    if not args.run_dirs:
        print("trace_diagnostic: no run dirs given — pass <run_dir> ...", file=sys.stderr)
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
