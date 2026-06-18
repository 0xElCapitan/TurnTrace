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
from adapter import SimAdapter  # noqa: E402
from _env import load_config, read_deck, resolve_deck_file  # noqa: E402


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
        cls.res = run_eval.run_eval("run-test", cls.run_dir, ledger_path=cls.ledger)

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
    """O2: a non-deliverable run (write_ledger=False / --no-ledger) writes NO ledger."""

    def test_no_ledger_written(self):
        tmp = Path(tempfile.mkdtemp(prefix="tt-noledger-"))
        try:
            ledger = tmp / "ledger.md"
            res = run_eval.run_eval("run-noledger", tmp / "run-noledger",
                                    write_ledger=False, ledger_path=ledger)
            self.assertFalse(ledger.exists(), "no ledger file should be created")
            self.assertFalse(res["ledger_appended"])
            self.assertTrue((tmp / "run-noledger" / "summary.csv").exists())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_cli_no_ledger_flag(self):
        tmp = Path(tempfile.mkdtemp(prefix="tt-noledger-cli-"))
        try:
            ledger = tmp / "ledger.md"
            rc = run_eval.main(["--run-id", "run-cli", "--out-dir", str(tmp / "run-cli"),
                                "--no-ledger", "--ledger", str(ledger)])
            self.assertEqual(rc, 0)
            self.assertFalse(ledger.exists())
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
