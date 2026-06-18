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
import failure_report  # noqa: E402  (analysis/, Sprint 02 PR-2)
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
