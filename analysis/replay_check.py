#!/usr/bin/env python3
"""``analysis/replay_check.py`` — replay / reproducibility check (PR-15, Task 01.3).

Two reproducibility tiers, honestly degraded (NFR-3; SDD §5.6):

  1. **Audit-trail equality (always).** Recompute every match's ``trace_hash``
     from its on-disk sidecar and assert it equals the value stored in the
     match-summary. This proves the trace ↔ record join (AC-3) still holds and
     that no sidecar was silently altered — the reproducibility floor that holds
     even with no seed control.

  2. **Byte-identical determinism (gated).** Exercised **only if
     ``seed_controlled=true``**. When seeds are uncontrolled (the probed reality:
     ``sim/capabilities.json`` → ``seed_controlled=false``) the determinism path
     is **explicitly skipped** and ``mode=unseeded`` is recorded — never silently
     passed (AC-03). When seed control is later proven, pass a second run dir via
     ``--replay-run`` and the check asserts the two runs' traces are byte-identical
     per match.

Self-contained canonical hashing: ``analysis/`` may not import ``eval/`` (the
runtime/offline import rule; SDD §1.6). The serializer below is therefore a
stdlib copy of ``eval/canonical_json.py``; ``tests/test_smokes.py`` pins the two
to byte-parity so they cannot silently diverge.

`analysis/` reads run-dir artifacts only — no ``cabt``/``sim``/``runtime``/``eval``.
stdlib only (NFR-7).

CLI:  python analysis/replay_check.py runs/run-0001
      python analysis/replay_check.py runs/run-0002 --replay-run runs/run-0002b
Exit: 0 reproducible (audit-trail equality holds; determinism passed or skipped)
      · 1 a hash mismatch or input failure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


# ---- canonical hash (stdlib copy of eval/canonical_json.py; parity-tested) ----
def _canonical_dumps(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _hash_canonical(obj) -> str:
    return hashlib.sha256(_canonical_dumps(obj).encode("utf-8")).hexdigest()


def _read_trace_rows(trace_path: Path) -> "list[dict]":
    rows = []
    with open(trace_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _load_summaries(run_dir: Path) -> "list[dict]":
    mr = sorted((run_dir / "match_results").glob("*.json"))
    if not mr:
        raise FileNotFoundError(f"{run_dir}: no match_results to replay")
    return [json.loads(p.read_text(encoding="utf-8")) for p in mr]


def audit_trail_equality(run_dir: Path) -> dict:
    """Recompute every trace_hash from disk; assert == stored value."""
    summaries = _load_summaries(run_dir)
    checked, mismatches, skipped_no_trace = 0, [], 0
    for s in summaries:
        match_id = s.get("match_id")
        if not s.get("trace_present"):
            skipped_no_trace += 1
            continue
        tp = run_dir / "traces" / f"{match_id}.jsonl"
        if not tp.exists():
            mismatches.append((match_id, "stored", "sidecar-missing"))
            continue
        recomputed = _hash_canonical(_read_trace_rows(tp))
        stored = s.get("trace_hash")
        checked += 1
        if recomputed != stored:
            mismatches.append((match_id, stored, recomputed))
    return {"checked": checked, "mismatches": mismatches,
            "skipped_no_trace": skipped_no_trace, "n_summaries": len(summaries)}


def _seed_controlled(summaries: "list[dict]") -> bool:
    vals = {bool(s.get("seed_controlled")) for s in summaries}
    if len(vals) > 1:
        raise ValueError(f"inconsistent seed_controlled across records: {vals}")
    return vals.pop() if vals else False


def byte_identical(run_dir: Path, replay_run: Path) -> dict:
    """Determinism path: assert each match's trace bytes are identical between
    the two runs (only meaningful under seed control)."""
    a_ids = {p.stem for p in (run_dir / "traces").glob("*.jsonl")}
    b_ids = {p.stem for p in (replay_run / "traces").glob("*.jsonl")}
    common = sorted(a_ids & b_ids)
    diffs = []
    for mid in common:
        a = (run_dir / "traces" / f"{mid}.jsonl").read_bytes()
        b = (replay_run / "traces" / f"{mid}.jsonl").read_bytes()
        if a != b:
            diffs.append(mid)
    return {"compared": len(common), "diffs": diffs,
            "only_in_a": sorted(a_ids - b_ids), "only_in_b": sorted(b_ids - a_ids)}


def replay_check(run_dir: Path, replay_run: "Path | None" = None) -> dict:
    summaries = _load_summaries(run_dir)
    audit = audit_trail_equality(run_dir)
    seeded = _seed_controlled(summaries)
    mode = "seeded" if seeded else "unseeded"

    determinism = {"status": None, "detail": None}
    if not seeded:
        # AC-03: determinism path explicitly SKIPPED; mode=unseeded recorded.
        determinism = {"status": "skipped",
                       "detail": "seed_controlled=false → mode=unseeded; byte-identical "
                                 "replay not available (NFR-3 audit-trail posture)."}
    elif replay_run is None:
        determinism = {"status": "skipped",
                       "detail": "seed_controlled=true but no --replay-run reference "
                                 "provided; pass a second run dir to check byte-identity."}
    else:
        bi = byte_identical(run_dir, replay_run)
        ok = not bi["diffs"] and not bi["only_in_a"] and not bi["only_in_b"]
        determinism = {"status": "passed" if ok else "failed", "detail": bi}

    audit_ok = not audit["mismatches"]
    determ_ok = determinism["status"] in ("skipped", "passed")
    return {"run_dir": str(run_dir), "mode": mode, "seed_controlled": seeded,
            "audit": audit, "audit_ok": audit_ok,
            "determinism": determinism, "ok": audit_ok and determ_ok}


def render(rep: dict) -> str:
    a = rep["audit"]
    lines = [f"# Replay check — {rep['run_dir']} (mode={rep['mode']})", ""]
    lines.append(f"- audit-trail equality: {a['checked']}/{a['n_summaries']} traces "
                 f"recomputed; mismatches={len(a['mismatches'])}; "
                 f"no-trace={a['skipped_no_trace']}")
    for mid, stored, got in a["mismatches"]:
        lines.append(f"  MISMATCH {mid}: stored={stored[:16] if stored else stored}… "
                     f"recomputed={got[:16] if isinstance(got, str) else got}…")
    d = rep["determinism"]
    if rep["seed_controlled"]:
        lines.append(f"- determinism (byte-identical replay): {d['status']} — {d['detail']}")
    else:
        lines.append(f"- determinism (byte-identical replay): SKIPPED "
                     f"(seed_controlled=false; mode=unseeded recorded) — {d['detail']}")
    lines.append("")
    lines.append(f"verdict: {'REPRODUCIBLE' if rep['ok'] else 'FAILED'} "
                 f"(audit-trail equality {'held' if rep['audit_ok'] else 'BROKEN'}).")
    return "\n".join(lines)


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description="Replay / reproducibility check for a run dir.")
    ap.add_argument("run_dir", help="run dir to check (e.g. runs/run-0001)")
    ap.add_argument("--replay-run", default=None,
                    help="second run dir for byte-identical determinism (seed-controlled only)")
    args = ap.parse_args(argv)

    try:
        rep = replay_check(Path(args.run_dir),
                           Path(args.replay_run) if args.replay_run else None)
    except (FileNotFoundError, ValueError) as e:
        print(f"replay_check: input failure — {e}", file=sys.stderr)
        return 1

    print(render(rep))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
