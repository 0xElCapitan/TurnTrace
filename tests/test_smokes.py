#!/usr/bin/env python3
"""Sprint 00 smoke tests (plan §7.5, SDD §7.3) — stdlib ``unittest`` only (NFR-7).

Covers: single-match · trace-join · exit codes (0/1/2) · schema validation +
FM-01 rejection · immutability overwrite refusal (exit 3) · id-vs-manifest ·
Competition-Data hygiene · determinism smoke (explicitly SKIPPED when unseeded).

These tests build a throwaway run dir and a throwaway ledger — they never touch
runs/run-0001 or docs/ledger.md.

Run:  python tests/test_smokes.py
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import shutil
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
for _sub in ("sim", "agents/runtime", "eval", "analysis"):
    import sys
    sys.path.insert(0, str(REPO_ROOT / _sub))

import run_match  # noqa: E402
import run_eval  # noqa: E402
import validate  # noqa: E402
import hygiene_check  # noqa: E402
import mirror_validate  # noqa: E402  (eval/, Sprint 01 PR-18)
import canonical_json  # noqa: E402  (eval/, parity check)
import delta_report  # noqa: E402  (analysis/, Sprint 01 PR-14)
import replay_check  # noqa: E402  (analysis/, Sprint 01 PR-15)
import scripted_baseline  # noqa: E402  (agents/runtime, Sprint 01 PR-13)
import failure_report  # noqa: E402  (analysis/, Sprint 02 PR-2)
import dispersion_report  # noqa: E402  (analysis/, Cycle-002 S02-T2)
from adapter import SimAdapter  # noqa: E402
from _env import load_config, read_deck, resolve_deck_file  # noqa: E402

sys.path.insert(0, str(REPO_ROOT / "tests"))
import test_import_direction  # noqa: E402  (Sprint 02 PR-2 lint-coverage assertion)


class SingleMatchSmoke(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="tt-match-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_single_match_and_trace_join(self):
        cfg = load_config()
        deck = read_deck(resolve_deck_file(cfg))
        inputs = {
            "agent_a_id": "random_legal", "agent_b_id": "random_legal",
            "deck_a_id": "deck-starter-v001", "deck_b_id": "deck-starter-v001",
            "match_index": 1, "regime_id": "regime-v001",
            "run_id": "run-test", "match_id": "M0001",
            "opponent_id": "random_legal", "agent_version": "random_legal-v001",
            "deck_hash": run_match.deck_hash(deck),
        }
        obj = run_match.run_single(inputs, self.tmp, cfg, deck, deck, random.Random(1))
        self.assertEqual(validate.validate_match_summary(obj["summary"]), [])
        self.assertEqual(validate.validate_trace(obj["trace"]), [])
        self.assertGreater(obj["summary"]["total_decisions"], 0)
        # trace-join: recompute from the written sidecar
        run_match.write_match(self.tmp, "M0001", obj)
        recomputed = run_match.recompute_trace_hash(self.tmp / "traces" / "M0001.jsonl")
        self.assertEqual(obj["summary"]["trace_hash"], recomputed)


class ExitCodeSmoke(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="tt-exit-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_exit_0_ok(self):
        rc = run_match.main(["--match-index", "1", "--run-id", "run-test",
                             "--match-id", "M0001", "--out-dir", str(self.tmp)])
        self.assertEqual(rc, 0)

    def test_exit_1_env_load_failure(self):
        prev = os.environ.get("TURNTRACE_DECK_FILE")
        os.environ["TURNTRACE_DECK_FILE"] = str(self.tmp / "no-such-deck.csv")
        try:
            rc = run_match.main(["--match-index", "1", "--run-id", "run-test",
                                 "--match-id", "M0001", "--out-dir", str(self.tmp)])
            self.assertEqual(rc, 1)
        finally:
            if prev is None:
                os.environ.pop("TURNTRACE_DECK_FILE", None)
            else:
                os.environ["TURNTRACE_DECK_FILE"] = prev

    def test_exit_2_agent_init_failure(self):
        rc = run_match.main(["--match-index", "1", "--run-id", "run-test",
                             "--match-id", "M0001", "--out-dir", str(self.tmp),
                             "--agent", "does_not_exist"])
        self.assertEqual(rc, 2)


class RunEvalSmoke(unittest.TestCase):
    """One sealed run shared across schema / id / immutability checks."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="tt-eval-"))
        cls.run_dir = cls.tmp / "run-test"
        cls.ledger = cls.tmp / "ledger.md"
        # PR-4 caller audit: write_ledger now defaults False, so a deliverable test
        # that asserts a ledger row MUST declare intent explicitly (to a tmp ledger).
        cls.res = run_eval.run_eval("run-test", cls.run_dir, ledger_path=cls.ledger,
                                    write_ledger=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_run_dir_validates(self):
        self.assertEqual(validate.validate_run_dir(self.run_dir), [])

    def test_summary_csv_matches_count(self):
        import csv
        man = json.loads((self.run_dir / "manifest.json").read_text())
        n_files = len(list((self.run_dir / "match_results").glob("*.json")))
        self.assertEqual(n_files, len(man["expected_match_ids"]))
        with open(self.run_dir / "summary.csv") as fh:
            rows = list(csv.DictReader(fh))
        self.assertEqual(int(rows[0]["n_matches"]), n_files)

    def test_ids_match_manifest(self):
        man = json.loads((self.run_dir / "manifest.json").read_text())
        written = {p.stem for p in (self.run_dir / "match_results").glob("*.json")}
        self.assertEqual(written, set(man["expected_match_ids"]))

    def test_hashes_present(self):
        kv = {}
        for line in (self.run_dir / "hashes.txt").read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                kv[k.strip()] = v.strip()
        for req in ("git_rev", "sim_version", "seed_list_hash", "timestamp"):
            self.assertTrue(kv.get(req), f"hashes.txt missing {req}")

    def test_one_ledger_row_with_ceiling(self):
        text = self.ledger.read_text()
        data_rows = [l for l in text.splitlines()
                     if l.startswith("| run-test ") or " | run-test | " in l]
        self.assertEqual(len(data_rows), 1, "expected exactly one ledger row")
        self.assertIn("Rung 1", text)  # claim_ceiling present & non-empty

    def test_immutability_guard_refuses_overwrite(self):
        before = (self.run_dir / "manifest.json").read_text()
        with self.assertRaises(run_eval.ImmutabilityRefusal):
            run_eval.run_eval("run-test", self.run_dir, ledger_path=self.ledger)
        # the sealed dir is untouched
        self.assertEqual((self.run_dir / "manifest.json").read_text(), before)

    def test_main_returns_3_on_populated_dir(self):
        rc = run_eval.main(["--run-id", "run-test", "--out-dir", str(self.run_dir),
                            "--ledger", str(self.ledger)])
        self.assertEqual(rc, 3)


class SchemaRejectionSmoke(unittest.TestCase):
    def test_fm01_masquerade_rejected(self):
        base = {
            "run_id": "r", "match_id": "M0001", "regime_id": "regime-v001",
            "experiment_id": None, "agent_id": "a", "agent_version": "v",
            "opponent_id": "o", "deck_id": "d", "opponent_deck_id": "d",
            "seed": None, "seed_controlled": False, "match_index": 1,
            "result": "loss", "ending_cause": "error", "turns": 3, "timeout": None,
            "invalid_action_count": 0, "invalid_action_detectable": True,
            "total_decisions": 2, "trace_present": True, "trace_hash": "x",
            "started_at": "t", "completed_at": "t", "wall_clock_ms": 1,
            "simulator_version": "s", "sim_version_source": "installed-pin",
            "deck_hash": "h", "error": "boom", "notes": "n",
        }
        errs = validate.validate_match_summary(base)
        self.assertTrue(any("masquerading" in e for e in errs))

    def test_error_without_message_rejected(self):
        base = {"result": "error", "error": None}
        # minimal record will also flag missing fields; we only assert the FM-01 rule fires
        errs = validate.validate_match_summary(base)
        self.assertTrue(any("mishandled error" in e for e in errs))


class HygieneSmoke(unittest.TestCase):
    def test_competition_data_paths_blocked(self):
        bad = [
            "grimoires/loa/context/Planning/sample_submission/cg/api.py",
            "deck.csv", "runs/run-0001/traces/M0001.jsonl", "cards.pdf",
        ]
        v = hygiene_check.find_violations(bad)
        self.assertEqual(len(v), len(bad), f"all should be blocked: {v}")

    def test_sanitized_paths_clean(self):
        ok = [
            "frozen/decks/deck-pool-v001.json", "docs/ledger.md",
            "sim/capabilities.json", "eval/run_match.py", "runs/.gitkeep",
        ]
        self.assertEqual(hygiene_check.find_violations(ok), [])

    def test_main_paths_mode_refuses(self):
        rc = hygiene_check.main(["--paths",
                                 "grimoires/loa/context/Planning/sample_submission/deck.csv"])
        self.assertEqual(rc, 1)


class DeterminismSmoke(unittest.TestCase):
    def test_determinism_smoke_skipped_when_unseeded(self):
        caps = SimAdapter(cfg=load_config()).capabilities()
        seed_controlled = caps["flags"].get("seed_controlled")
        if seed_controlled:
            self.skipTest("seed_controlled=true — determinism smoke would run (not this env)")
        # Unseeded: the determinism smoke is EXPLICITLY skipped (NFR-3); record that.
        self.assertFalse(seed_controlled)
        print("determinism smoke: SKIPPED (seed_controlled=false; mode=unseeded)")


# ====================== Sprint 01 smokes ======================
# All throwaway runs below use write_ledger=False (O2) — they NEVER touch
# docs/ledger.md, and build into tempdirs so they never touch runs/run-000{1,2}.


class ScriptedBaselineSmoke(unittest.TestCase):
    """PR-13 / AC-04: the scripted baseline is deterministic (no hidden state)."""

    def test_select_deterministic(self):
        a = scripted_baseline.select(5, 1, 2, None)
        b = scripted_baseline.select(5, 1, 2, random.Random(1))
        c = scripted_baseline.select(5, 1, 2, random.Random(99999))
        self.assertEqual(a, [0, 1])
        self.assertEqual(a, b)   # RNG must not influence selection
        self.assertEqual(a, c)

    def test_select_count_matches_random_legal_clamp(self):
        # identical count behaviour to random_legal (the single-variable guarantee)
        for n, lo, hi in [(3, 1, 1), (2, 1, 5), (0, 0, 0), (4, 2, 3)]:
            k = hi if hi <= n else n
            self.assertEqual(scripted_baseline.select(n, lo, hi), list(range(max(k, 0))))

    def test_agent_contract(self):
        obs = {"select": {"option": [{"type": 1}, {"type": 2}, {"type": 3}],
                          "minCount": 1, "maxCount": 2}}
        self.assertEqual(scripted_baseline.agent(obs), [0, 1])
        with self.assertRaises(ValueError):
            scripted_baseline.agent({"select": None})


class NoLedgerGuardSmoke(unittest.TestCase):
    """O2 / PR-4 Option C: a non-deliverable run writes NO ledger. With the new
    fail-safe default (write_ledger=False) a bare run never appends; --no-ledger
    remains a deprecated, still-suppressing fail-safe."""

    def test_no_ledger_written(self):
        tmp = Path(tempfile.mkdtemp(prefix="tt-noledger-"))
        try:
            ledger = tmp / "ledger.md"
            # rely on the NEW DEFAULT (write_ledger omitted → False): no ledger write.
            res = run_eval.run_eval("run-noledger", tmp / "run-noledger",
                                    ledger_path=ledger)
            self.assertFalse(ledger.exists(), "no ledger file should be created by default")
            self.assertFalse(res["ledger_appended"])
            self.assertTrue((tmp / "run-noledger" / "summary.csv").exists())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_cli_no_ledger_flag(self):
        # deprecated --no-ledger still SUPPRESSES even alongside an explicit --ledger
        # (fail-safe: the contamination flag can only ever prevent a write).
        tmp = Path(tempfile.mkdtemp(prefix="tt-noledger-cli-"))
        try:
            ledger = tmp / "ledger.md"
            rc = run_eval.main(["--run-id", "run-cli", "--out-dir", str(tmp / "run-cli"),
                                "--no-ledger", "--ledger", str(ledger)])
            self.assertEqual(rc, 0)
            self.assertFalse(ledger.exists())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class DeliverableLedgerSmoke(unittest.TestCase):
    """PR-4 / AC-4: an EXPLICIT deliverable run writes exactly one ledger row,
    idempotently, to a redirected (tmp) path — never the tracked docs/ledger.md."""

    def test_deliverable_writes_one_row_idempotent(self):
        import aggregate  # noqa: E402  (analysis/, intra-zone)
        tmp = Path(tempfile.mkdtemp(prefix="tt-deliv-"))
        try:
            ledger = tmp / "ledger.md"
            rd = tmp / "run-deliv"
            res = run_eval.run_eval("run-deliv", rd, write_ledger=True, ledger_path=ledger)
            self.assertTrue(res["ledger_appended"])
            self.assertTrue(ledger.exists())
            text = ledger.read_text()
            rows = [l for l in text.splitlines()
                    if l.startswith("| run-deliv ") or " | run-deliv | " in l]
            self.assertEqual(len(rows), 1, "exactly one deliverable row")
            self.assertIn("Rung 1", text)  # claim ceiling present & non-empty
            # idempotent: re-aggregating the same run into the same ledger adds no row
            again = aggregate.aggregate_and_ledger(
                rd, ledger, git_rev="x", sim_version="s", mode="unseeded",
                opponent_pool_ref="opponent-pool-v001", seed_set_ref="seed-set-v001",
                date="2026-06-18")
            self.assertFalse(again["ledger_appended"])
            self.assertEqual(ledger.read_text(), text)  # byte-identical: no second row
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_cli_ledger_path_implies_deliverable(self):
        # --ledger <tmp> alone implies deliverable intent → writes the redirected ledger.
        tmp = Path(tempfile.mkdtemp(prefix="tt-deliv-cli-"))
        try:
            ledger = tmp / "ledger.md"
            rc = run_eval.main(["--run-id", "run-dcli", "--out-dir", str(tmp / "run-dcli"),
                                "--ledger", str(ledger)])
            self.assertEqual(rc, 0)
            self.assertTrue(ledger.exists())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_cli_deliverable_flag_with_redirected_ledger(self):
        # --deliverable declares intent; --ledger keeps the write off the tracked ledger.
        tmp = Path(tempfile.mkdtemp(prefix="tt-deliv-flag-"))
        try:
            ledger = tmp / "ledger.md"
            rc = run_eval.main(["--run-id", "run-df", "--out-dir", str(tmp / "run-df"),
                                "--deliverable", "--ledger", str(ledger)])
            self.assertEqual(rc, 0)
            self.assertTrue(ledger.exists())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class ProvenanceSmoke(unittest.TestCase):
    """O1: hashes.txt + manifest pin the runtime agent source (source-hash path)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="tt-prov-"))
        cls.rd = cls.tmp / "run-prov"
        run_eval.run_eval("run-prov", cls.rd, agent_id="scripted_baseline", write_ledger=False)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_hashes_has_agent_source(self):
        kv = {}
        for line in (self.rd / "hashes.txt").read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                kv[k.strip()] = v.strip()
        self.assertEqual(kv.get("agent_source_file"), "agents/runtime/scripted_baseline.py")
        self.assertEqual(len(kv.get("agent_source_hash", "")), 64)  # sha256 hex
        self.assertEqual(len(kv.get("config_hash", "")), 64)
        self.assertIn("git_dirty", kv)  # honestly recorded

    def test_manifest_has_agent_source(self):
        man = json.loads((self.rd / "manifest.json").read_text())
        self.assertEqual(man["agent_id"], "scripted_baseline")
        self.assertEqual(man["agent_version"], "scripted-v001")
        self.assertEqual(len(man["agent_source_hash"]), 64)


class DeltaReportSmoke(unittest.TestCase):
    """PR-14 / AC-01, AC-02."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="tt-delta-"))
        cls.base = cls.tmp / "run-a"   # NB: not 'run' — that shadows TestCase.run
        run_eval.run_eval("run-a", cls.base, write_ledger=False)
        # same-regime copy → every metric unmoved (exercises "why no change" on all)
        cls.same = cls.tmp / "run-a-copy"
        shutil.copytree(cls.base, cls.same)
        # cross-regime copy → tamper ONLY the copy's manifest regime_id
        cls.xreg = cls.tmp / "run-a-xregime"
        shutil.copytree(cls.base, cls.xreg)
        man = json.loads((cls.xreg / "manifest.json").read_text())
        man["regime_id"] = "regime-v999"
        (cls.xreg / "manifest.json").write_text(json.dumps(man, indent=2))
        # None-producing copy: force illegal_action_rate -> None (no detectable records),
        # so base<->none exercises the appeared/disappeared (None<->number) branches.
        cls.noneb = cls.tmp / "run-a-none"
        shutil.copytree(cls.base, cls.noneb)
        for p in (cls.noneb / "match_results").glob("*.json"):
            r = json.loads(p.read_text(encoding="utf-8"))
            r["invalid_action_detectable"] = False
            r["invalid_action_count"] = None
            p.write_text(json.dumps(r), encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_per_metric_deltas_with_why_no_change(self):
        rep = delta_report.compare(self.base, self.same)
        self.assertGreater(len(rep["metrics"]), 0)
        for m in rep["metrics"]:           # identical runs → all unmoved → all explained (AC-01)
            self.assertFalse(m["moved"])
            self.assertTrue(m["why_no_change"])

    def test_cross_regime_refused(self):
        with self.assertRaises(delta_report.CrossRegimeRefusal):
            delta_report.compare(self.base, self.xreg)
        self.assertEqual(delta_report.main([str(self.base), str(self.xreg)]), 2)  # AC-02

    def test_change_kind_classifier(self):  # PR-3: None<->number is never a fabricated move
        self.assertEqual(delta_report._change_kind(None, 0.5, None), "appeared")
        self.assertEqual(delta_report._change_kind(0.5, None, None), "disappeared")
        self.assertEqual(delta_report._change_kind(0.1, 0.3, 0.2), "moved")
        self.assertEqual(delta_report._change_kind(0.2, 0.2, 0.0), "unchanged")
        self.assertEqual(delta_report._change_kind(None, None, None), "unchanged")

    def test_appeared_not_fabricated_down(self):
        # baseline n/a, candidate numeric → APPEARED, never the old fabricated 'down'
        rep = delta_report.compare(self.noneb, self.base)
        iar = next(m for m in rep["metrics"] if m["metric"] == "illegal_action_rate")
        self.assertEqual(iar["change_kind"], "appeared")
        self.assertIsNone(iar["delta"])
        self.assertTrue(iar["why_moved"])
        out = delta_report.render(rep)
        line = next(l for l in out.splitlines()
                    if l.startswith("- **illegal_action_rate**") and "APPEARED" in l)
        self.assertNotIn("down", line)
        self.assertNotIn("up ", line)

    def test_disappeared_renders_na(self):
        # baseline numeric, candidate n/a → DISAPPEARED, "<a> -> n/a", no direction
        rep = delta_report.compare(self.base, self.noneb)
        iar = next(m for m in rep["metrics"] if m["metric"] == "illegal_action_rate")
        self.assertEqual(iar["change_kind"], "disappeared")
        out = delta_report.render(rep)
        line = next(l for l in out.splitlines()
                    if l.startswith("- **illegal_action_rate**") and "DISAPPEARED" in l)
        self.assertIn("-> n/a", line)
        self.assertNotIn("down", line)

    def test_moved_metric_has_why_line(self):  # symmetric with why-no-change; numeric delta preserved
        rep = {
            "regime_id": "regime-v001",
            "run_a": {"run_id": "x", "agent_version": "v", "opponent_id": "o", "n": 12},
            "run_b": {"run_id": "y", "agent_version": "v", "opponent_id": "o", "n": 12},
            "metrics": [{"metric": "win_rate", "a": 0.4, "b": 0.6, "delta": 0.2,
                         "change_kind": "moved", "moved": True, "why_no_change": None,
                         "why_moved": delta_report._why_moved("win_rate", "moved", 0.4, 0.6)}],
            "wall_clock_ms": {"a": 1, "b": 2},
        }
        out = delta_report.render(rep)
        self.assertIn("| win_rate | 0.4 | 0.6 | 0.2 | MOVED |", out)  # delta-table value preserved
        self.assertIn("up 0.2", out)
        self.assertTrue(any("win_rate" in l and "Rung 1" in l for l in out.splitlines()))


class ReplayCheckSmoke(unittest.TestCase):
    """PR-15 / AC-03 + canonical-hash parity with eval/canonical_json.py."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="tt-replay-"))
        cls.rd = cls.tmp / "run-r"
        run_eval.run_eval("run-r", cls.rd, write_ledger=False)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_audit_trail_equality(self):
        rep = replay_check.replay_check(self.rd)
        self.assertTrue(rep["audit_ok"])
        self.assertEqual(len(rep["audit"]["mismatches"]), 0)

    def test_determinism_skipped_unseeded(self):
        rep = replay_check.replay_check(self.rd)
        self.assertEqual(rep["mode"], "unseeded")
        self.assertEqual(rep["determinism"]["status"], "skipped")
        self.assertNotEqual(rep["determinism"]["status"], "passed")  # PR-5: never 'passed'
        self.assertFalse(rep["seed_controlled"])  # probed reality: seed_controlled=false

    def test_byte_identical_copy_still_skipped_not_passed(self):
        # PR-5 dead-path guard: a byte-identical COPY as --replay-run WOULD make
        # byte_identical() pass — but unseeded short-circuits to 'skipped' before reaching
        # it, so the skip branch can NOT silently become 'passed'. No seed is fabricated;
        # seed_controlled stays false (NG2 reproducibility boundary).
        copy = self.tmp / "run-r-copy"
        shutil.copytree(self.rd, copy)
        rep = replay_check.replay_check(self.rd, replay_run=copy)
        self.assertFalse(rep["seed_controlled"])
        self.assertEqual(rep["determinism"]["status"], "skipped")
        self.assertNotEqual(rep["determinism"]["status"], "passed")

    def test_seed_controlled_still_false(self):
        # Confirm the gate that keeps the dead path dead: records report seed_controlled=false.
        self.assertFalse(replay_check._seed_controlled(replay_check._load_summaries(self.rd)))

    def test_canonical_parity_with_eval(self):
        for s in ({"b": 2, "a": 1}, [1, {"z": 9, "y": [3, 2, 1]}], {"n": None, "t": True}):
            self.assertEqual(replay_check._hash_canonical(s), canonical_json.hash_canonical(s))
            self.assertEqual(replay_check._canonical_dumps(s), canonical_json.canonical_dumps(s))

    def test_tamper_detected(self):
        tampered = self.tmp / "run-tampered"
        shutil.copytree(self.rd, tampered)
        a_trace = next(iter((tampered / "traces").glob("*.jsonl")))
        a_trace.write_text(a_trace.read_text() + '{"record_type":"decision"}\n')
        rep = replay_check.replay_check(tampered)
        self.assertFalse(rep["audit_ok"])


class MirrorValidateSmoke(unittest.TestCase):
    """PR-18 / AC-05: candidate-vs-self full match reports pass/fail."""

    def test_scripted_baseline_passes(self):
        self.assertEqual(mirror_validate.main(["--agent", "scripted_baseline"]), 0)

    def test_random_legal_passes(self):
        self.assertEqual(mirror_validate.main(["--agent", "random_legal"]), 0)

    def test_unknown_agent_setup_fails(self):
        self.assertEqual(mirror_validate.main(["--agent", "does_not_exist"]), 2)


# ====================== Sprint 02 smokes ======================
# All throwaway runs below build into tempdirs (write_ledger=False) — they NEVER
# touch runs/run-000{1,2} or docs/ledger.md.


class FailureReportSmoke(unittest.TestCase):
    """PR-2 / AC-2: aggregate report emits COUNTS ONLY and never reads the
    per-decision sidecars (poisoned-sidecar contents must be ignored)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="tt-failrep-"))
        cls.rd = cls.tmp / "run-fr"
        run_eval.run_eval("run-fr", cls.rd, write_ledger=False)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_counts_sum_to_n(self):
        rep = failure_report.aggregate_failures(self.rd)
        n = rep["n"]
        self.assertGreater(n, 0)
        self.assertEqual(sum(rep["result_counts"].values()), n)        # nothing dropped
        self.assertEqual(sum(rep["ending_cause_counts"].values()), n)  # incl. <unmapped>
        self.assertGreaterEqual(rep["invalid_action_total"], 0)
        self.assertIsInstance(rep["error_present_count"], int)

    def test_no_sidecar_reference_in_source(self):
        # static guarantee: the module contains no reference to the trace sidecar
        # directory, so it CANNOT read raw decision rows.
        src = Path(failure_report.__file__).read_text(encoding="utf-8")
        self.assertNotIn("traces", src)

    def test_poisoned_sidecar_ignored(self):
        poisoned = self.tmp / "run-poison"
        shutil.copytree(self.rd, poisoned)
        poison = "NOT_A_REAL_CARD DROP-TABLE deck.csv CARD_ID_0xDEADBEEF hand=[A,B,C]"
        sidecar_dir = poisoned / "traces"
        sidecar_dir.mkdir(exist_ok=True)
        (sidecar_dir / "ZZZZ.jsonl").write_text(poison + "\n", encoding="utf-8")
        for jf in sidecar_dir.glob("*.jsonl"):
            jf.write_text(poison + "\n", encoding="utf-8")
        # match_results + manifest are identical to the clean run → counts identical,
        # which proves the sidecars were never consulted.
        clean = failure_report.aggregate_failures(self.rd)
        pois = failure_report.aggregate_failures(poisoned)
        self.assertEqual(pois["result_counts"], clean["result_counts"])
        self.assertEqual(pois["ending_cause_counts"], clean["ending_cause_counts"])
        out = failure_report.render(pois) + "\n" + failure_report.render_json(pois)
        for tok in ("NOT_A_REAL_CARD", "DROP-TABLE", "deck.csv", "0xDEADBEEF", "hand="):
            self.assertNotIn(tok, out)

    def test_unmapped_bucket_and_invalid_exclusion(self):
        tampered = self.tmp / "run-tamper"
        shutil.copytree(self.rd, tampered)
        recs = sorted((tampered / "match_results").glob("*.json"))
        self.assertGreaterEqual(len(recs), 2)
        r0 = json.loads(recs[0].read_text(encoding="utf-8"))
        r0["ending_cause"] = None              # null → <unmapped>, reported not dropped
        r0["invalid_action_detectable"] = False  # → excluded from invalid_action_total
        recs[0].write_text(json.dumps(r0), encoding="utf-8")
        r1 = json.loads(recs[1].read_text(encoding="utf-8"))
        r1["ending_cause"] = "totally-new-cause"  # unrecognized → <unmapped>
        recs[1].write_text(json.dumps(r1), encoding="utf-8")
        rep = failure_report.aggregate_failures(tampered)
        self.assertGreaterEqual(rep["ending_cause_counts"]["<unmapped>"], 2)
        self.assertGreaterEqual(rep["invalid_action_excluded"], 1)
        self.assertEqual(sum(rep["ending_cause_counts"].values()), rep["n"])

    def test_empty_run_raises(self):
        empty = self.tmp / "run-empty"
        (empty / "match_results").mkdir(parents=True)
        with self.assertRaises(ValueError):
            failure_report.aggregate_failures(empty)

    def test_cli_exit_codes_and_out(self):
        self.assertEqual(failure_report.main([str(self.rd)]), 0)            # stdout default
        self.assertEqual(failure_report.main([str(self.rd), "--json"]), 0)  # json
        self.assertEqual(failure_report.main([str(self.tmp / "no-such-run")]), 1)  # input fail
        out = self.tmp / "fr-out.md"
        self.assertEqual(failure_report.main([str(self.rd), "--out", str(out)]), 0)
        self.assertTrue(out.exists())


class FailureReportImportCoverage(unittest.TestCase):
    """PR-2 / SDD §2 gap-closure: the new analysis module is in the import-direction
    lint's scanned set and reports zero violations — a new analysis module cannot
    silently escape the runtime/offline separation rule."""

    def test_module_scanned_and_clean(self):
        zone_map = test_import_direction._module_zone_map()
        self.assertEqual(zone_map.get("failure_report"), "analysis")
        offending = [v for v in test_import_direction.check() if "failure_report" in v]
        self.assertEqual(offending, [], f"failure_report import violations: {offending}")


# ====================== Cycle-002 Sprint 01 smokes ======================
# Scale Foundation (OA-2 Sprint 01). Every throwaway run below uses the shipped
# write_ledger=False default and builds into a tempdir with a REDIRECTED (tmp)
# ledger — they NEVER touch runs/run-000{1,2}, the sealed run dirs, or
# docs/ledger.md, and they mutate no v001 frozen file. No guard logic is changed;
# these tests only exercise the existing run_eval guards at the larger regime-v002 N.


class V001ByteUnchangedSmoke(unittest.TestCase):
    """S01-T4 / AC-S01-3: regime-v001 + its four components are byte-unchanged.

    Golden = LF-normalized content sha256 captured at Sprint 01. Line endings are
    normalized on read (universal-newline) because the repo runs core.autocrlf=true
    with no .gitattributes: raw working-tree bytes are CRLF on a Windows checkout and
    LF on Linux, but the COMMITTED content is LF either way. Hashing the LF-normalized
    content pins each file's CONTENT identity portably — any real content edit changes
    the hash and fails here. Do NOT update these goldens to silence a failure: a v001
    change is a NEW regime (regime-v002), never an edit (NG7; frozen/README.md).
    """

    GOLDEN_LF_SHA256 = {
        "frozen/regimes/regime-v001.json": "f99beee320dae9af0b653073d75ba1c4bafaa92d2813aeecabc14c02e6b59153",
        "frozen/seeds/seed-set-v001.json": "d93f3692020ba044e5183b03d3cd279b39b816b3765d728e3b54404c69e83cd2",
        "frozen/opponents/opponent-pool-v001.json": "f785bb98f80060c7289a40162c8a0ff514f624caa901e905994fe93e3e67958a",
        "frozen/decks/deck-pool-v001.json": "cf4b2cbf6ba2459f26d2f81cef2ee27976e7e0ae4df65419affb8fc75ea7e694",
        "frozen/metrics/metrics-spec-v001.json": "0d2283abc88d6bd0d62adbc1387c026c567443d356adaf7e65e32ee023673e5c",
    }

    def test_v001_components_byte_unchanged(self):
        for rel, want in self.GOLDEN_LF_SHA256.items():
            p = REPO_ROOT / rel
            self.assertTrue(p.exists(), f"missing frozen v001 file: {rel}")
            got = hashlib.sha256(p.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
            self.assertEqual(
                got, want,
                f"{rel} CONTENT changed — v001 must be byte-unchanged (NG7). A larger-n "
                f"seed-set is a NEW regime (regime-v002), never an edit of v001.")


class RegimeV002AdditiveSmoke(unittest.TestCase):
    """S01-T2/T3 / AC-S01-2: seed-set-v002 + regime-v002 are additive and conform.

    The schema mirrors v001 exactly, changing only the scale; regime-v002 reuses the
    other three regime-v001 components by reference (OD-3) — only the seed-set differs.
    Structural conformance only; no strength claim, no cross-regime comparison.
    """

    def _load(self, rel):
        return json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))

    def test_seed_set_v002_schema(self):
        ss = self._load("frozen/seeds/seed-set-v002.json")
        self.assertEqual(ss["seed_set_id"], "seed-set-v002")
        self.assertEqual(ss["mode"], "unseeded")
        self.assertIsNone(ss["seeds"])
        self.assertEqual(ss["match_indices"], list(range(1, ss["n"] + 1)))  # contiguous neutral 1..N
        self.assertEqual(len(ss["match_indices"]), ss["n"])
        self.assertGreater(ss["n"], 12)  # a larger-n set than seed-set-v001 (n=12)
        # additive: mirrors v001's field set exactly (same schema, only the scale differs)
        self.assertEqual(set(ss), set(self._load("frozen/seeds/seed-set-v001.json")))

    def test_regime_v002_reuses_v001_components_by_reference(self):
        r2 = self._load("frozen/regimes/regime-v002.json")
        r1 = self._load("frozen/regimes/regime-v001.json")
        self.assertEqual(r2["regime_id"], "regime-v002")
        self.assertEqual(r2["seed_set"], "seed-set-v002")            # the single deliberate difference
        self.assertEqual(r2["opponent_pool"], "opponent-pool-v001")  # reused by reference (OD-3)
        self.assertEqual(r2["deck_pool"], "deck-pool-v001")
        self.assertEqual(r2["metrics_spec"], "metrics-spec-v001")
        self.assertEqual(r2["mode"], "unseeded")
        # additive: same field set as regime-v001; the three reused components are byte-identical refs
        self.assertEqual(set(r2), set(r1))
        self.assertEqual(r2["opponent_pool"], r1["opponent_pool"])
        self.assertEqual(r2["deck_pool"], r1["deck_pool"])
        self.assertEqual(r2["metrics_spec"], r1["metrics_spec"])
        self.assertNotEqual(r2["seed_set"], r1["seed_set"])          # only the seed-set changed


class RegimeV002GuardsAndLedgerSmoke(unittest.TestCase):
    """S01-T5 + S01-T6 / AC-S01-4, AC-S01-5: at the larger N under regime-v002 the
    no-ledger-by-default behavior and the deck-drift + immutability guards hold,
    with no guard logic modified.

    One sealed regime-v002 run (n=500, write_ledger=False) is built once into a
    tempdir and shared across the checks. The ledger path is a REDIRECTED tmp file
    that must never be created; docs/ledger.md, runs/, and the v001 frozen files are
    never touched.
    """

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="tt-v002-"))
        cls.run_dir = cls.tmp / "run-v002-noledger"
        cls.ledger = cls.tmp / "ledger.md"   # redirected; must NOT be created
        # bare / non-deliverable run against regime-v002 (write_ledger defaults to False)
        cls.res = run_eval.run_eval("run-v002-noledger", cls.run_dir,
                                    regime_id="regime-v002", ledger_path=cls.ledger)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    # ---- S01-T5: no ledger by default at scale (AC-S01-4) ----
    def test_no_ledger_row_by_default_v002(self):
        self.assertFalse(self.res["ledger_appended"])
        self.assertFalse(self.ledger.exists(),
                         "a non-deliverable regime-v002 run must append NO ledger row by default")

    def test_summary_csv_still_written_v002(self):
        self.assertTrue((self.run_dir / "summary.csv").exists())  # summary output still produced
        self.assertEqual(self.res["n"], 500)                      # the chosen larger N ran end-to-end

    def test_redirected_ledger_is_not_the_tracked_ledger(self):
        # the test never targets the tracked ledger — redirected tmp path only
        self.assertNotEqual(self.ledger.resolve(), (REPO_ROOT / "docs" / "ledger.md").resolve())

    # ---- S01-T6: immutability guard holds at scale (AC-S01-5) ----
    def test_immutability_guard_refuses_populated_v002(self):
        before = (self.run_dir / "manifest.json").read_text(encoding="utf-8")
        with self.assertRaises(run_eval.ImmutabilityRefusal):
            run_eval.run_eval("run-v002-noledger", self.run_dir, regime_id="regime-v002",
                              ledger_path=self.ledger)
        self.assertEqual((self.run_dir / "manifest.json").read_text(encoding="utf-8"), before)

    def test_immutability_guard_exit_3_v002(self):
        rc = run_eval.main(["--run-id", "run-v002-noledger", "--out-dir", str(self.run_dir),
                            "--regime-id", "regime-v002", "--ledger", str(self.ledger)])
        self.assertEqual(rc, 3)                 # populated dir → exit 3, unchanged guard
        self.assertFalse(self.ledger.exists())  # the guard fires before any ledger write

    # ---- S01-T6: deck-drift guard holds at scale (AC-S01-5) ----
    def test_deck_drift_guard_refuses_v002(self):
        # A SYNTHETIC 60-int deck (arbitrary integers — NOT Competition Data) whose
        # content hash differs from the frozen deck-pool-v001 hash. The deck-drift
        # guard precedes both the immutability guard and the match loop, so it fires
        # first and no run dir is created and no match is played.
        synth = self.tmp / "synthetic-deck.csv"
        synth.write_text("\n".join(str(i) for i in range(1, 61)) + "\n", encoding="utf-8")
        drift_dir = self.tmp / "run-v002-drift"
        prev = os.environ.get("TURNTRACE_DECK_FILE")
        os.environ["TURNTRACE_DECK_FILE"] = str(synth)
        try:
            with self.assertRaises(RuntimeError) as ctx:
                run_eval.run_eval("run-v002-drift", drift_dir, regime_id="regime-v002",
                                  ledger_path=self.ledger)
            self.assertIn("deck drift", str(ctx.exception).lower())
            rc = run_eval.main(["--run-id", "run-v002-drift2", "--regime-id", "regime-v002",
                                "--out-dir", str(self.tmp / "run-v002-drift2")])
            self.assertEqual(rc, 1)  # deck-drift RuntimeError → env/input failure exit 1
        finally:
            if prev is None:
                os.environ.pop("TURNTRACE_DECK_FILE", None)
            else:
                os.environ["TURNTRACE_DECK_FILE"] = prev
        self.assertFalse(drift_dir.exists())     # guard fired before any dir/match write
        self.assertFalse(self.ledger.exists())   # and never any ledger write


# ============== Cycle-002 Sprint 02 — dispersion report smokes ==============
# S02-T3 / AC-S02-2..5, AC-S02-7. SYNTHETIC fixtures ONLY: these classes build run
# dirs directly (manifest.json + match_results/*.json) — they invoke NO simulator,
# read NO Competition Data, and touch neither runs/run-000{1,2} nor docs/ledger.md.
# Fixture metric values are set explicitly (deterministic by construction; no RNG is
# used, so no random seed is needed — and nothing here implies simulator seed
# control: sim/capabilities.json seed_controlled=false is unchanged).

# A synthetic poison string: tokens that look like Competition Data / raw gameplay.
# It is written into the per-decision sidecars and the per-match error field; the
# dispersion module must never surface any of these tokens.
_DISP_POISON = ("NOT_A_REAL_CARD CARD_ID_0xDEADBEEF deck.csv hand=[A,B,C] "
                "DROP-TABLE card_list.pdf decklist.csv raw-trace-row")
_DISP_POISON_TOKENS = ("NOT_A_REAL_CARD", "0xDEADBEEF", "deck.csv", "hand=[",
                       "DROP-TABLE", "card_list.pdf", "decklist.csv", "raw-trace-row")


def _write_synth_run(run_dir, *, run_id, agent_id, agent_version, regime_id,
                     n=10, wins=5, turns=8, wall_ms=10,
                     poison_sidecar=None, poison_error=None):
    """Build a synthetic sealed-run-dir shape: manifest.json (the regime/agent
    authority) + ``n`` match_results records carrying exactly the fields
    ``aggregate_run`` reads. No simulator, no Competition Data. Optionally poison the
    per-decision sidecars and/or the per-match error field to prove they are never
    surfaced by the dispersion report."""
    mr = run_dir / "match_results"
    mr.mkdir(parents=True)
    manifest = {
        "run_id": run_id, "regime_id": regime_id, "agent_id": agent_id,
        "agent_version": agent_version, "opponent_id": "synthetic-opponent",
        "mode": "unseeded", "expected_match_ids": [f"M{i:04d}" for i in range(1, n + 1)],
    }
    (run_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    for i in range(1, n + 1):
        rec = {
            "match_id": f"M{i:04d}", "match_index": i,
            "result": "win" if i <= wins else "loss",
            "turns": turns, "wall_clock_ms": wall_ms,
            "invalid_action_detectable": True, "invalid_action_count": 0,
            "timeout": None, "error": poison_error,
            "agent_id": agent_id, "agent_version": agent_version,
            "opponent_id": "synthetic-opponent", "regime_id": regime_id,
            "run_id": run_id,
        }
        (mr / f"M{i:04d}.json").write_text(json.dumps(rec), encoding="utf-8")
    if poison_sidecar is not None:
        sd = run_dir / "traces"   # the per-decision sidecar dir the module must ignore
        sd.mkdir(exist_ok=True)
        for i in range(1, n + 1):
            (sd / f"M{i:04d}.jsonl").write_text(poison_sidecar + "\n", encoding="utf-8")
    return run_dir


class DispersionSingleRegimeGuard(unittest.TestCase):
    """S02-T3 #1 / AC-S02-3: uniform regime → exit 0; mixed regime → exit 2."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="tt-disp-guard-"))
        cls.v002 = [
            _write_synth_run(cls.tmp / f"run-v002-b-{i}", run_id=f"run-v002-b-{i}",
                             agent_id="random_legal", agent_version="random_legal-v001",
                             regime_id="regime-v002", n=10, wins=3 + i)
            for i in range(1, 4)
        ]
        cls.v001 = _write_synth_run(
            cls.tmp / "run-v001-x", run_id="run-v001-x", agent_id="random_legal",
            agent_version="random_legal-v001", regime_id="regime-v001", n=10, wins=5)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_uniform_regime_v002_exit_0(self):
        rep = dispersion_report.disperse(self.v002)
        self.assertEqual(rep["regime_id"], "regime-v002")
        self.assertEqual(rep["agents"][0]["K"], 3)
        self.assertEqual(dispersion_report.main([str(p) for p in self.v002]), 0)

    def test_mixed_regime_refused_exit_2(self):
        with self.assertRaises(dispersion_report.MixedRegimeRefusal):
            dispersion_report.disperse([self.v002[0], self.v001])
        self.assertEqual(
            dispersion_report.main([str(self.v002[0]), str(self.v001)]), 2)


class DispersionDescriptiveOnly(unittest.TestCase):
    """S02-T3 #2 / AC-S02-2: output carries the seven allowed statistics and NONE of
    the inferential / overreach terms; the module computes no std dev / variance."""

    ALLOWED = ("count", "min", "max", "range", "mean", "median", "spread")
    FORBIDDEN = ("standard deviation", "variance", "confidence interval", "p-value",
                 "significant", "hypothesis", "error bar", "better", "worse",
                 "uplift", "improvement")

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="tt-disp-desc-"))
        # Three runs with deliberately DIFFERENT win counts → non-zero spread.
        cls.runs = [
            _write_synth_run(cls.tmp / f"run-v002-c-{i}", run_id=f"run-v002-c-{i}",
                             agent_id="scripted_baseline", agent_version="scripted-v001",
                             regime_id="regime-v002", n=10, wins=w)
            for i, w in enumerate((3, 5, 7), start=1)
        ]
        cls.rep = dispersion_report.disperse(cls.runs)
        cls.md = dispersion_report.render(cls.rep)
        cls.js = dispersion_report.render_json(cls.rep)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_descriptive_stats_values(self):
        s = dispersion_report.descriptive_stats([0.3, 0.5, 0.7])
        self.assertEqual(set(s), set(self.ALLOWED))          # exactly the 7 allowed keys
        self.assertEqual(s["count"], 3)
        self.assertEqual(s["min"], 0.3)
        self.assertEqual(s["max"], 0.7)
        self.assertEqual(s["range"], [0.3, 0.7])
        self.assertEqual(s["mean"], 0.5)
        self.assertEqual(s["median"], 0.5)
        self.assertEqual(s["spread"], 0.4)                   # max - min, not std dev/variance
        empty = dispersion_report.descriptive_stats([None, None])
        self.assertEqual(empty["count"], 0)
        self.assertIsNone(empty["spread"])

    def test_output_includes_allowed_terms(self):
        for term in self.ALLOWED:
            self.assertIn(term, self.md, f"descriptive term missing from report: {term}")

    def test_output_excludes_inferential_terms(self):
        low_md, low_js = self.md.lower(), self.js.lower()
        for term in self.FORBIDDEN:
            self.assertNotIn(term, low_md, f"forbidden term leaked into Markdown: {term}")
            self.assertNotIn(term, low_js, f"forbidden term leaked into JSON: {term}")

    def test_no_inferential_code_path(self):
        # Structural: the module computes none of std dev / variance — there is no call
        # to the inferential statistics functions (only statistics.median is used).
        src = Path(dispersion_report.__file__).read_text(encoding="utf-8")
        for call in ("statistics.stdev", "statistics.pstdev",
                     "statistics.variance", "statistics.pvariance"):
            self.assertNotIn(call, src, f"inferential/variance code path present: {call}")


class DispersionImportBoundary(unittest.TestCase):
    """S02-T3 #3 / AC-S02-4: dispersion_report is in the import-direction lint's
    scanned set, reports zero violations, and imports no eval/sim/cabt/runtime
    module (intra-analysis ``import aggregate`` is allowed)."""

    def test_module_scanned_and_clean(self):
        zone_map = test_import_direction._module_zone_map()
        self.assertEqual(zone_map.get("dispersion_report"), "analysis")
        offending = [v for v in test_import_direction.check() if "dispersion_report" in v]
        self.assertEqual(offending, [], f"dispersion_report import violations: {offending}")

    def test_no_forbidden_zone_imports(self):
        src = REPO_ROOT / "analysis" / "dispersion_report.py"
        zone_map = test_import_direction._module_zone_map()
        imported_zones = {zone_map.get(name) for name in test_import_direction._top_imports(src)}
        for forbidden in ("eval", "sim", "runtime", "cabt"):
            self.assertNotIn(forbidden, imported_zones,
                             f"dispersion_report must not import zone {forbidden}")
        self.assertIn("aggregate", test_import_direction._top_imports(src))  # intra-analysis reuse


class DispersionSanitization(unittest.TestCase):
    """S02-T3 #4 / AC-S02-5: the report reads only manifest.json + match_results/*.json.
    Poison written into the per-decision sidecars and the per-match error field is
    never surfaced; the output passes hygiene_check; no sidecar dir is referenced."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="tt-disp-sanit-"))
        cls.clean = [
            _write_synth_run(cls.tmp / f"clean-{i}", run_id=f"run-v002-c-{i}",
                             agent_id="scripted_baseline", agent_version="scripted-v001",
                             regime_id="regime-v002", n=10, wins=w)
            for i, w in enumerate((4, 6), start=1)
        ]
        # identical metrics, but every sidecar AND every error field is poisoned
        cls.poisoned = [
            _write_synth_run(cls.tmp / f"poison-{i}", run_id=f"run-v002-c-{i}",
                             agent_id="scripted_baseline", agent_version="scripted-v001",
                             regime_id="regime-v002", n=10, wins=w,
                             poison_sidecar=_DISP_POISON, poison_error=_DISP_POISON)
            for i, w in enumerate((4, 6), start=1)
        ]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_poison_never_surfaced(self):
        rep = dispersion_report.disperse(self.poisoned)
        out = dispersion_report.render(rep) + "\n" + dispersion_report.render_json(rep)
        for tok in _DISP_POISON_TOKENS:
            self.assertNotIn(tok, out, f"poison token surfaced in dispersion output: {tok}")

    def test_clean_and_poisoned_stats_identical(self):
        # match_results + manifest are identical across clean/poisoned; only the
        # sidecars + error bodies differ. Identical stats prove they were never read.
        clean_stats = dispersion_report.disperse(self.clean)["agents"][0]["metrics"]
        pois_stats = dispersion_report.disperse(self.poisoned)["agents"][0]["metrics"]
        self.assertEqual(clean_stats, pois_stats)

    def test_no_sidecar_reference_in_source(self):
        src = Path(dispersion_report.__file__).read_text(encoding="utf-8")
        self.assertNotIn("traces", src)  # cannot construct a sidecar path → cannot read rows

    def test_output_passes_hygiene(self):
        rep = dispersion_report.disperse(self.clean)
        out = self.tmp / "disp.md"
        out.write_text(dispersion_report.render(rep), encoding="utf-8")
        self.assertEqual(hygiene_check.main(["--paths", str(out)]), 0)


class DispersionMissingInput(unittest.TestCase):
    """S02-T3 #5 / AC-S02-3: missing run dir or missing match_results → exit 1."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="tt-disp-missing-"))
        # a dir with a manifest but an EMPTY match_results/ (no records)
        cls.no_records = cls.tmp / "run-empty"
        (cls.no_records / "match_results").mkdir(parents=True)
        (cls.no_records / "manifest.json").write_text(
            json.dumps({"run_id": "run-empty", "regime_id": "regime-v002",
                        "agent_id": "random_legal"}), encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_missing_run_dir_exit_1(self):
        with self.assertRaises(FileNotFoundError):
            dispersion_report.disperse([self.tmp / "does-not-exist"])
        self.assertEqual(dispersion_report.main([str(self.tmp / "does-not-exist")]), 1)

    def test_missing_match_results_exit_1(self):
        with self.assertRaises(ValueError):
            dispersion_report.disperse([self.no_records])
        self.assertEqual(dispersion_report.main([str(self.no_records)]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
