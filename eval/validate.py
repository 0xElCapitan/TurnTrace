#!/usr/bin/env python3
"""``eval/validate.py`` — tiny stdlib schema validator (Task 00.6; SDD §3.1, §7.3).

Validates the Sprint 00 flat-file artifacts against the field lists in
``eval/schemas.md``. The governing rule (NFR-6, capability-tolerance): a
capability-uncertain field may be ``null`` **iff** its capability flag says the
capability is absent — never silently. The validator also enforces the FM-01
masquerade guard: ``result == "error"`` **iff** ``error`` is populated, so a
mishandled error can never pass as a win/loss/draw.

No third-party schema library — overkill for this field set (SDD §2.2). A
schema library is the ladder rung to add only if the schemas outgrow this.

CLI:  python eval/validate.py runs/run-0001     # validate a whole run dir
Exit: 0 all valid · 1 one or more validation errors. stdlib only (NFR-7).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

RESULT_ENUM = {"win", "loss", "draw", "error"}

# (field, accepted python types, nullable?) — bool must precede int (bool is int subclass).
_MATCH_SPEC = [
    ("run_id", (str,), False), ("match_id", (str,), False), ("regime_id", (str,), False),
    ("experiment_id", (str,), True),
    ("agent_id", (str,), False), ("agent_version", (str,), False),
    ("opponent_id", (str,), False), ("deck_id", (str,), False),
    ("opponent_deck_id", (str,), True),
    ("seed", (int,), True), ("seed_controlled", (bool,), False),
    ("match_index", (int,), False),
    ("result", (str,), False), ("ending_cause", (str,), True),
    ("turns", (int,), False), ("timeout", (bool,), True),
    ("invalid_action_count", (int,), True), ("invalid_action_detectable", (bool,), False),
    ("total_decisions", (int,), True), ("trace_present", (bool,), False),
    ("trace_hash", (str,), True),
    ("started_at", (str,), False), ("completed_at", (str,), False),
    ("wall_clock_ms", (int,), False),
    ("simulator_version", (str,), False), ("sim_version_source", (str,), False),
    ("deck_hash", (str,), False),
    ("error", (str,), True), ("notes", (str,), False),
]


def _type_ok(value, types) -> bool:
    # Reject bool where a non-bool int is expected, and vice versa.
    if bool in types:
        return isinstance(value, bool)
    if int in types:
        return isinstance(value, int) and not isinstance(value, bool)
    return isinstance(value, types)


def _check_fields(rec: dict, spec, label: str) -> "list[str]":
    errs = []
    for name, types, nullable in spec:
        if name not in rec:
            errs.append(f"{label}: missing field '{name}'")
            continue
        v = rec[name]
        if v is None:
            if not nullable:
                errs.append(f"{label}: field '{name}' is null but not nullable")
        elif not _type_ok(v, types):
            errs.append(f"{label}: field '{name}' has type {type(v).__name__}, expected {types}")
    return errs


def validate_match_summary(rec: dict, label: str = "match-summary") -> "list[str]":
    errs = _check_fields(rec, _MATCH_SPEC, label)
    if rec.get("result") not in RESULT_ENUM:
        errs.append(f"{label}: result '{rec.get('result')}' not in {sorted(RESULT_ENUM)}")

    # FM-01 masquerade guard: result==error  <=>  error populated.
    is_error = rec.get("result") == "error"
    has_err = rec.get("error") not in (None, "")
    if is_error and not has_err:
        errs.append(f"{label}: result==error but 'error' is empty (mishandled error)")
    if has_err and not is_error:
        errs.append(f"{label}: 'error' populated but result is '{rec.get('result')}' (error masquerading as outcome)")

    # capability-tolerance nullability (NFR-6)
    if rec.get("seed") is None and rec.get("seed_controlled") is True:
        errs.append(f"{label}: seed is null but seed_controlled=true")
    if rec.get("seed_controlled") is True and not isinstance(rec.get("seed"), int):
        errs.append(f"{label}: seed_controlled=true requires an integer seed")
    if rec.get("invalid_action_count") is None and rec.get("invalid_action_detectable") is True:
        errs.append(f"{label}: invalid_action_count is null but invalid_action_detectable=true")
    if rec.get("invalid_action_detectable") is True and not isinstance(rec.get("invalid_action_count"), int):
        errs.append(f"{label}: invalid_action_detectable=true requires an integer invalid_action_count")

    # trace linkage
    if rec.get("trace_present") is True:
        if not isinstance(rec.get("trace_hash"), str):
            errs.append(f"{label}: trace_present=true requires a string trace_hash")
        if not isinstance(rec.get("total_decisions"), int):
            errs.append(f"{label}: trace_present=true requires an integer total_decisions")
    return errs


def validate_trace(rows: "list[dict]", label: str = "trace") -> "list[str]":
    errs = []
    if not rows:
        return [f"{label}: empty trace"]
    terminals = [r for r in rows if r.get("record_type") == "terminal"]
    if len(terminals) != 1:
        errs.append(f"{label}: expected exactly 1 terminal record, found {len(terminals)}")
    if rows[-1].get("record_type") != "terminal":
        errs.append(f"{label}: last record is not the terminal record")
    for i, r in enumerate(rows):
        rt = r.get("record_type")
        if rt == "decision":
            for f, ts in (("decision_index", int), ("turn", int),
                          ("decision_latency_ms", int)):
                if not isinstance(r.get(f), ts) or isinstance(r.get(f), bool):
                    errs.append(f"{label}[{i}]: decision field '{f}' bad/missing")
            if r.get("player") not in ("agent", "opponent"):
                errs.append(f"{label}[{i}]: player '{r.get('player')}' invalid")
            if not isinstance(r.get("selected_action"), dict):
                errs.append(f"{label}[{i}]: selected_action missing")
            # never leak opponent private state
            if r.get("player") == "opponent" and r.get("private_state_summary") is not None:
                errs.append(f"{label}[{i}]: opponent row carries private_state_summary (leakage)")
        elif rt == "terminal":
            if r.get("result") not in RESULT_ENUM:
                errs.append(f"{label}[{i}]: terminal result '{r.get('result')}' invalid")
            for f in ("turns", "decision_index", "last_decision_index"):
                if not isinstance(r.get(f), int) or isinstance(r.get(f), bool):
                    errs.append(f"{label}[{i}]: terminal field '{f}' bad/missing")
        else:
            errs.append(f"{label}[{i}]: unknown record_type '{rt}'")
    return errs


def validate_trace_self_consistency(summary: dict, rows: "list[dict]", label: str) -> "list[str]":
    """total_decisions must equal the count of agent decision rows (plan §4.1)."""
    agent_rows = sum(1 for r in rows if r.get("record_type") == "decision" and r.get("player") == "agent")
    td = summary.get("total_decisions")
    if isinstance(td, int) and td != agent_rows:
        return [f"{label}: total_decisions={td} != agent decision rows={agent_rows}"]
    return []


def validate_manifest(man: dict) -> "list[str]":
    errs = []
    for f in ("run_id", "regime_id", "expected_match_ids", "created_at"):
        if f not in man or man[f] in (None, ""):
            errs.append(f"manifest: missing/empty '{f}'")
    if not isinstance(man.get("expected_match_ids"), list) or not man.get("expected_match_ids"):
        errs.append("manifest: expected_match_ids must be a non-empty list")
    return errs


def validate_hashes(txt: str) -> "list[str]":
    """hashes.txt: KEY=VALUE lines; AC-6 requires these non-empty."""
    kv = {}
    for line in txt.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        kv[k.strip()] = v.strip()
    errs = []
    for req in ("git_rev", "sim_version", "seed_list_hash", "timestamp"):
        if not kv.get(req):
            errs.append(f"hashes.txt: missing/empty '{req}'")
    return errs


def validate_run_dir(run_dir: Path) -> "list[str]":
    errs = []
    mr = sorted((run_dir / "match_results").glob("*.json"))
    if not mr:
        errs.append(f"{run_dir}: no match_results")
    man_path = run_dir / "manifest.json"
    expected = None
    if man_path.exists():
        man = json.loads(man_path.read_text(encoding="utf-8"))
        errs += validate_manifest(man)
        expected = set(man.get("expected_match_ids") or [])
    else:
        errs.append(f"{run_dir}: missing manifest.json")
    for p in mr:
        rec = json.loads(p.read_text(encoding="utf-8"))
        errs += validate_match_summary(rec, label=p.name)
        if expected is not None and rec.get("match_id") not in expected:
            errs.append(f"{p.name}: match_id '{rec.get('match_id')}' not in manifest expected list")
        tp = run_dir / "traces" / f"{rec.get('match_id')}.jsonl"
        if rec.get("trace_present"):
            if not tp.exists():
                errs.append(f"{p.name}: trace_present but sidecar {tp.name} missing")
            else:
                rows = [json.loads(ln) for ln in tp.read_text(encoding="utf-8").splitlines() if ln.strip()]
                errs += validate_trace(rows, label=tp.name)
                errs += validate_trace_self_consistency(rec, rows, label=p.name)
    hp = run_dir / "hashes.txt"
    if hp.exists():
        errs += validate_hashes(hp.read_text(encoding="utf-8"))
    else:
        errs.append(f"{run_dir}: missing hashes.txt")
    return errs


def main(argv=None) -> int:
    ap_args = argv if argv is not None else sys.argv[1:]
    if not ap_args:
        print("usage: python eval/validate.py <run_dir>", file=sys.stderr)
        return 1
    run_dir = Path(ap_args[0])
    errs = validate_run_dir(run_dir)
    if errs:
        for e in errs:
            print(f"INVALID: {e}", file=sys.stderr)
        print(f"validate: {len(errs)} error(s) in {run_dir}", file=sys.stderr)
        return 1
    print(f"validate: OK — {run_dir} conforms to schemas.md", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
