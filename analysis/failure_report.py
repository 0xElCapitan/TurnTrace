#!/usr/bin/env python3
"""``analysis/failure_report.py`` — aggregate failure-mode report (PR-2 / S02-2).

Reads a sealed run directory's **match-summary records** (read-only) and emits
**coarse counts only** — result/ending-cause distributions, an error-presence
count, and a legality (invalid-action) total — tied back to the sanitized
failure-mode taxonomy (`docs/failure-mode-taxonomy-v001.md`) by reference string.

**What it reads (only):** ``runs/<run_id>/match_results/*.json`` and
``runs/<run_id>/manifest.json``. It never opens the per-decision sidecar
(``*.jsonl``) files, and it never emits raw rows, card ids, card names, deck
lists, hand contents, selected actions, simulator logs, or any Competition Data
(SDD §4.2; ESP/CC-1/CC-2). The error field is surfaced as a **presence flag
only** — the error string body is never read into the output.

This is a *sanitized aggregate diagnostic*. It writes **no ledger row** and
carries **no claim ceiling of its own** — only a Rung-1 footer asserting no
gameplay-strength claim (the experiment ledger remains the only ceiling-bearing
artifact; pattern from `analysis/delta_report.py`).

`analysis/` imports run-dir artifacts only — no `cabt`, `sim/`, `eval/`, or
`agents/runtime/` (the offline/runtime separation; SDD §1.6). stdlib only (NFR-7).

CLI:  python analysis/failure_report.py runs/run-0002 [--json] [--out <local-path>]
Exit: 0 report produced · 1 input failure.

Note: ``--out`` writes a run-derived artifact and is **local/git-ignored by
policy** (ESP-1 / OD-8); tracking such a file requires explicit operator
approval. The default is stdout, no file.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Fixed enums (from eval/schemas.md). result is a non-nullable enum; ending_cause
# is nullable / may carry an unrecognized value → bucketed as "<unmapped>".
RESULT_KEYS = ["win", "loss", "draw", "error"]
ENDING_CAUSE_KEYS = ["prize-out", "deck-out", "no-active", "card-effect", "error"]
UNMAPPED = "<unmapped>"

# Sanitized links back to the taxonomy's computable-now categories. Reference
# strings only: fm_id + a field-NAME signature + evidence_ref (null — specific
# evidence lives in local, git-ignored run dirs; requires-raw-data: cannot-surface).
FM_LINKS = [
    {"fm_id": "FM-01",
     "signature": "match-summary invalid_action_count > 0, or result == 'error'",
     "evidence_ref": None},
    {"fm_id": "FM-07",
     "signature": "match-summary ending_cause 'deck-out' bucket plus avg_turns",
     "evidence_ref": None},
]


def _load_manifest(run_dir: Path) -> dict:
    """Run_id/regime_id authority. Optional — falls back to the records if absent."""
    mp = run_dir / "manifest.json"
    return json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else {}


def _load_summaries(run_dir: Path) -> "list[dict]":
    recs = sorted((run_dir / "match_results").glob("*.json"))
    if not recs:
        raise ValueError(f"failure_report: no match_results in {run_dir}")
    return [json.loads(p.read_text(encoding="utf-8")) for p in recs]


def _claim_ceiling_footer(regime_id, n) -> str:
    return (f"Sanitized aggregate counts over {regime_id} at n={n}. NO "
            f"gameplay-strength claim — these are legality/outcome diagnostics, not "
            f"evidence of agent quality (ladder Rung 1). The experiment ledger "
            f"(docs/ledger.md) is the only ceiling-bearing artifact.")


def aggregate_failures(run_dir: Path) -> dict:
    """Pure read → sanitized counts. Raises ValueError on an empty run dir."""
    man = _load_manifest(run_dir)
    summaries = _load_summaries(run_dir)
    n = len(summaries)

    result_counts = {k: 0 for k in RESULT_KEYS}
    ending_cause_counts = {k: 0 for k in (*ENDING_CAUSE_KEYS, UNMAPPED)}
    error_present_count = 0
    invalid_action_total = 0
    invalid_action_excluded = 0  # records where invalid_action_detectable != true

    for s in summaries:
        res = s.get("result")
        if res in result_counts:
            result_counts[res] += 1
        # (result is a non-nullable enum per eval/validate.py; an out-of-enum value
        #  would leave sum(result_counts) < n — a visible signal, never a silent drop.)

        ec = s.get("ending_cause")
        ending_cause_counts[ec if ec in ending_cause_counts else UNMAPPED] += 1

        # error surfaced as a PRESENCE FLAG only — the string body is never read out.
        if s.get("error") not in (None, ""):
            error_present_count += 1

        # invalid-action count summed only where detectable; exclusion is noted, not dropped.
        if s.get("invalid_action_detectable") is True:
            invalid_action_total += s.get("invalid_action_count") or 0
        else:
            invalid_action_excluded += 1

    return {
        "run_id": man.get("run_id") or summaries[0].get("run_id"),
        "regime_id": man.get("regime_id") or summaries[0].get("regime_id"),
        "n": n,
        "result_counts": result_counts,
        "ending_cause_counts": ending_cause_counts,
        "error_present_count": error_present_count,
        "invalid_action_total": invalid_action_total,
        "invalid_action_excluded": invalid_action_excluded,
        "fm_links": FM_LINKS,
        "claim_ceiling_footer": _claim_ceiling_footer(
            man.get("regime_id") or summaries[0].get("regime_id"), n),
    }


def render(rep: dict) -> str:
    lines = [f"# Failure-mode report — {rep['run_id']} (regime {rep['regime_id']}), "
             f"n={rep['n']}", ""]

    lines.append("## Result counts")
    lines.append("| result | count |")
    lines.append("|---|---|")
    for k in RESULT_KEYS:
        lines.append(f"| {k} | {rep['result_counts'][k]} |")
    lines.append("")

    lines.append("## Ending-cause counts")
    lines.append("| ending_cause | count |")
    lines.append("|---|---|")
    for k in (*ENDING_CAUSE_KEYS, UNMAPPED):
        lines.append(f"| {k} | {rep['ending_cause_counts'][k]} |")
    lines.append("")
    lines.append(f"_The `{UNMAPPED}` bucket counts records with a null or unrecognized "
                 f"ending_cause — reported, never silently dropped._")
    lines.append("")

    lines.append("## Legality / errors")
    lines.append(f"- invalid_action_total: {rep['invalid_action_total']} "
                 f"(summed only over records where invalid_action_detectable=true)")
    lines.append(f"- records excluded from invalid_action_total "
                 f"(invalid_action_detectable != true): {rep['invalid_action_excluded']}")
    lines.append(f"- error_present_count: {rep['error_present_count']} "
                 f"(presence only — error strings are never surfaced)")
    lines.append("")

    lines.append("## Failure-mode links (reference strings only)")
    for link in rep["fm_links"]:
        lines.append(f"- **{link['fm_id']}** — signature: {link['signature']}; "
                     f"evidence_ref: {link['evidence_ref']}")
    lines.append("")

    lines.append(f"**Claim ceiling.** {rep['claim_ceiling_footer']}")
    return "\n".join(lines)


def render_json(rep: dict) -> str:
    return json.dumps(rep, indent=2, sort_keys=True)


def main(argv=None) -> int:
    try:  # robust output regardless of console codepage (Windows cp1252)
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(
        description="Sanitized aggregate failure-mode report (counts only) for a run dir.")
    ap.add_argument("run_dir", help="run dir to summarize (e.g. runs/run-0002)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    ap.add_argument("--out", default=None,
                    help="write the report to a LOCAL/git-ignored path (ESP-1/OD-8); "
                         "default is stdout, no file")
    args = ap.parse_args(argv)

    try:
        rep = aggregate_failures(Path(args.run_dir))
    except (FileNotFoundError, ValueError) as e:
        print(f"failure_report: input failure — {e}", file=sys.stderr)
        return 1

    text = render_json(rep) if args.json else render(rep)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"failure_report: wrote {args.out} (local/git-ignored by policy — ESP-1/OD-8)",
              file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
