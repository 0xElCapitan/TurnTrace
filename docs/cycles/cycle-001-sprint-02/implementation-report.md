# Cycle-001 / Sprint 02 — Implementation Report

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-001 / Sprint 02 |
| **Working title** | Delta Explanation + Failure-Mode Taxonomy |
| **Posture** | EXPLAIN / AUDIT only — not an agent-improvement sprint |
| **Claim ceiling** | Rung 1 (unchanged; not raised) |
| **Branch** | `cycle-001-sprint-02-delta-explanation` |
| **Base commit** | `c77a362` (`main = origin/main`) |
| **Build gate** | OA-2 (operator-authorized for Sprint 02 only) |
| **Date** | 2026-06-18 |
| **Commit state** | Not committed / not pushed / not tagged — no COMPLETED marker (per operator posture) |

> Sanitized report. No raw traces, card IDs/names, deck lists, simulator logs, or
> Competition Data appear here. Runs are referenced by `run_id` + sanitized metrics only.

---

## 1. Executive summary

Sprint 02 made the first same-regime comparison (`run-0001` vs `run-0002`, `regime-v001`,
n=12) **explainable** and future comparisons **auditable**, entirely within the
analysis/offline + provenance/docs layers. **No `agents/runtime/` file was touched, the
claim ceiling stays at Rung 1, broad optimization stays closed, and no build gate beyond
Sprint 02 was opened.**

All six Core tasks (T1–T4, T6, T7) landed and are green; the **T5 Stretch was included**
(it is a behavior-neutral dead-path marker + test hardening, low-risk and within safe
scope after Core + validation were green). All three required gates pass:
`tests/test_import_direction.py` (exit 0), `tests/test_smokes.py` (exit 0, **49 tests**),
`eval/hygiene_check.py --paths <changed>` (exit 0).

---

## 2. AC Verification

ACs quoted from the Sprint Plan §8 (`docs/cycles/cycle-001-sprint-02/03-sprint-02-sprint-plan.md`).

### AC-1 — Taxonomy honesty
> "`docs/failure-mode-taxonomy-v001.md`; pointer in `docs/failure-modes.md` … forbidden-word grep; manual capability-flag cross-check vs `sim/capabilities.json` … Stop: A per-decision quality detector appears, or a category claims a detector its capability forbids."

**Status: ✓ Met.** `docs/failure-mode-taxonomy-v001.md` encodes FM-01..FM-09 with
`axis`/`compute_status`/`gating_capability`/`capability_value`/`signature`/`evidence_ref`/
`detector`/`status`. FM-03/FM-04/FM-06/FM-08 carry `detector: forbidden` + the inline
boundary note (taxonomy "Detector boundary (binding)" section and each forbidden FM block).
One-line pointer added at `docs/failure-modes.md:12`. Capability cross-check PASS: FM-01
`invalid_action_detectable=true`, FM-02 `timeout_detectable=false` both mirror
`sim/capabilities.json`. No forbidden claim word appears in the taxonomy.

### AC-2 — Aggregate-only diagnostics
> "`analysis/failure_report.py`; tests … run vs local `run-0002`, grep output for card/deck tokens (expect none) … Stop: The report reads or emits any raw trace row / card-adjacent token, or imports `cabt`/`sim`/`eval`/`runtime`."

**Status: ✓ Met.** `analysis/failure_report.py` (`aggregate_failures`) reads only
`match_results/*.json` + `manifest.json` and emits counts only (`result_counts`,
`ending_cause_counts` incl. `<unmapped>`, `error_present_count` [presence flag only],
`invalid_action_total`, `fm_links` reference strings, Rung-1 footer). It contains **no
reference to the trace-sidecar directory** (static test `test_no_sidecar_reference_in_source`)
and stdlib-only imports (no `cabt`/`sim`/`eval`/`runtime`). `FailureReportSmoke.test_poisoned_sidecar_ignored`
proves poisoned sidecar contents never reach output and counts are identical to the clean
run. `FailureReportImportCoverage` asserts the module is in the import-direction lint's
scanned set with zero violations.

### AC-3 — Delta correctness
> "`analysis/delta_report.py`; `DeltaReportSmoke` … None↔number fixtures; `run-0001` vs `run-0002` delta-table-unchanged assertion; cross-regime exit-2 check … Stop: A None↔number transition still renders a fabricated `down`, or `frozen/` is edited, or a delta-table value changes."

**Status: ✓ Met.** `analysis/delta_report.py` adds `change_kind` (`_change_kind`) with
`unchanged`/`moved`/`appeared`/`disappeared`; direction (`up`/`down`) is computed **only**
when the delta is numeric (`_is_num` guard in the moved-section render), eliminating the
`(None or 0) > 0` footgun. `_why_moved` adds a why-line to every moved/appeared/disappeared
metric, symmetric with `WHY_NO_CHANGE`. Read-only run of `runs/run-0001` vs `runs/run-0002`
shows the delta-table values unchanged (`win_rate 0.5→0.8333 MOVED`, `avg_turns 13.42→7.67
MOVED` rendering a correct `down -5.75`, three `no change` at delta `0.0`). Cross-regime
`CrossRegimeRefusal` → exit 2 preserved. No `frozen/` edit (alias documented in the module
docstring only). Tests: `test_change_kind_classifier`, `test_appeared_not_fabricated_down`,
`test_disappeared_renders_na`, `test_moved_metric_has_why_line`, `test_per_metric_deltas_with_why_no_change`,
`test_cross_regime_refused`.

### AC-4 — Ledger integrity
> "`eval/run_eval.py`; `NoLedgerGuardSmoke` + `DeliverableLedgerSmoke` … default-no-write fixture; explicit-deliverable-write fixture (tmp ledger); idempotency; `--no-ledger` no-op check … Stop: A default/non-deliverable invocation appends to `docs/ledger.md`, or an existing row is edited in place."

**Status: ✓ Met.** `run_eval(..., write_ledger: bool = False)` — a row is written only on
explicit intent. `main()` computes `write_ledger = bool(args.deliverable or args.ledger) and
not args.no_ledger`; `--deliverable` and `--ledger <path>` are added; `--no-ledger` is a
deprecated, still-suppressing fail-safe (with a stderr deprecation note). `summary.csv` is
always written. Tests: `NoLedgerGuardSmoke.test_no_ledger_written` (default writes nothing),
`DeliverableLedgerSmoke.test_deliverable_writes_one_row_idempotent` (one row, idempotent,
byte-identical on re-aggregate), `test_cli_ledger_path_implies_deliverable`,
`test_cli_deliverable_flag_with_redirected_ledger`, `test_cli_no_ledger_flag` (suppressor).
**All ledger-write tests use a temporary ledger path** — `docs/ledger.md` SHA verified
identical before/after the full suite and git status clean.

### AC-5 — Replay honesty (Stretch)
> "`analysis/replay_check.py`; `ReplayCheckSmoke` … assert `status != 'passed'` and `== 'skipped'` under unseeded … Stop: A fake seed is injected, or the skip branch can become `passed` while unseeded."

**Status: ✓ Met (Stretch included).** `byte_identical` carries a `loa:shortcut` dead-path
marker naming the ceiling (unreachable while `seed_controlled=false`) and the upgrade
trigger (`seed_controlled=true` proven + `--replay-run`). `ReplayCheckSmoke` strengthened:
`test_determinism_skipped_unseeded` now also asserts `status != "passed"` and
`seed_controlled is False`; `test_byte_identical_copy_still_skipped_not_passed` passes a
**byte-identical copy** as `--replay-run` and asserts the result stays `skipped` (the seed
gate short-circuits before `byte_identical`); `test_seed_controlled_still_false` pins the
gate. **No fake seed injected; no sealed run mutated** (fixtures copy into tempdirs).

### AC-6 — Report traceability
> "`docs/strategy-report.md` … manual traceability pass; forbidden-word + card/deck grep; §5-still-DEFERRED check … Stop: A claim sentence lacks an artifact ref, or a forbidden claim is made, or §5 is filled."

**Status: ✓ Met.** §1/§4/§6/§7 filled with artifact-cited Rung-1 prose; PERMITS/FORBIDS
boundary added (mirrors `deferred-lane-gate-after-sprint-01.md:37-87`; all 14 still-closed
items present). §5 remains DEFERRED (`docs/strategy-report.md:76`); §2/§3/§8 remain TODO
skeletons. Every non-skeleton sentence cites a concrete artifact path. Forbidden words
appear only in the negated FORBIDS list; no card/deck tokens; hygiene clean.

### AC-7 — Loop discipline
> "`/implement` patches; one review + one audit artifact … Stop: Code lands outside `/implement`, or a COMPLETED marker appears without operator authorization."

**Status: ⚠ Partial — implement-side met; review/audit is the next phase.** All code/docs
were authored inside this `/implement sprint-02` invocation only; no out-of-loop edit; **no
COMPLETED marker written**; nothing committed/pushed/tagged. The single `/review-sprint
sprint-02` + `/audit-sprint sprint-02` artifacts are produced by the orchestrator in the
**next** Golden Path step and are out of scope for `/implement`. No scope-split needed —
this is sequencing, not unmet work.

### AC-8 — Claim ceiling held
> "every tracked Sprint 02 artifact … forbidden-word grep across all changed tracked files; ledger remains the only ceiling-bearing artifact … Stop: Any artifact makes a claim beyond Rung 1, or a non-ledger artifact asserts a ceiling."

**Status: ✓ Met.** Forbidden-word grep across all 8 changed files returns only
negated/forbidden-language usages (the pre-existing `delta_report.py` claim-ceiling footer
and the strategy-report FORBIDS list). No artifact asserts a ceiling — the taxonomy,
failure_report, and delta_report carry only a Rung-1 footer; `docs/ledger.md` remains the
sole ceiling-bearing artifact and was not mutated.

---

## 3. Tasks completed

| Task | Title | Class | Status | Primary artifact |
|---|---|---|---|---|
| T1 | Failure-mode taxonomy v001 | Core | ✓ | `docs/failure-mode-taxonomy-v001.md` (new) + `docs/failure-modes.md:12` pointer |
| T2 | Aggregate failure-mode report | Core | ✓ | `analysis/failure_report.py` (new) + tests |
| T3 | `delta_report` hardening | Core | ✓ | `analysis/delta_report.py` |
| T4 | Ledger contamination hardening | Core | ✓ | `eval/run_eval.py` |
| T5 | `replay_check` dead-path marker/test | **Stretch (INCLUDED)** | ✓ | `analysis/replay_check.py` |
| T6 | Strategy-report update | Core | ✓ | `docs/strategy-report.md` |
| T7 | E2E goal validation + this report | Core | ✓ | this file |

**T5 disposition:** INCLUDED. Core (T1–T4, T6) + T7 validation were finished and green
before T5 was started; T5 is a comment marker + test strengthening with no behavior change,
within safe scope (OD-1 condition satisfied).

---

## 4. Files changed

**New (3):**
- `analysis/failure_report.py` (200 lines)
- `docs/failure-mode-taxonomy-v001.md` (248 lines)
- `docs/cycles/cycle-001-sprint-02/implementation-report.md` (this file)

**Modified (6):** `analysis/delta_report.py` (+77/-…), `analysis/replay_check.py` (+7),
`eval/run_eval.py` (+53/-…), `tests/test_smokes.py` (+243), `docs/failure-modes.md` (+2),
`docs/strategy-report.md` (+79/-…). Diffstat: `6 files changed, 419 insertions(+), 42 deletions(-)`.

Every path is in the Sprint Plan §7 authorization matrix. No other path was touched.

---

## 5. Validation

| Command | Exit | Result |
|---|---|---|
| `python tests/test_import_direction.py` | 0 | runtime/offline separation intact |
| `python tests/test_smokes.py` | 0 | Ran 49 tests, OK |
| `python eval/hygiene_check.py --paths <8 changed files>` | 0 | clean — no Competition-Data paths |

**Targeted Sprint-Plan checks (all pass):**
- taxonomy enum + capability-flag cross-check vs `sim/capabilities.json` — PASS (FM-01 true, FM-02 false; rest `none`/`n/a`)
- FM-03/04/06/08 `detector: forbidden` + inline boundary — present (exactly those four)
- `failure_report` emits counts only; poisoned sidecar contents ignored; no trace-dir reference in source — PASS
- `delta_report` None↔number → `appeared`/`disappeared`, no fabricated `down` — PASS
- `delta_report` why-moved / why-no-change coverage — PASS
- `delta_report` cross-regime refusal → exit 2 — PASS
- `delta_report` delta-table values unchanged for `run-0001` vs `run-0002` (read-only) — PASS
- `run_eval` default writes no ledger; `--deliverable`/`--ledger <tmp>` write; `--no-ledger` deprecated fail-safe — PASS
- `replay_check` unseeded `status=='skipped'`, never `'passed'`; no fake seed — PASS
- strategy-report traceability pass; §5 DEFERRED; PERMITS/FORBIDS present, 14/14 still-closed items — PASS
- forbidden-claim-word grep across changed files — only negated usages
- hygiene clean across changed files — PASS

---

## 6. Posture & hygiene confirmations

- **No build gate beyond Sprint 02 was opened.** This `/implement` consumed the OA-2 build
  gate for Sprint 02 only; it opened nothing further.
- **Broad optimization remains closed.** No still-closed lane was touched; the strategy
  report's FORBIDS section re-states all 14.
- **Runtime-agent changes remain forbidden — and none occurred.** No `agents/runtime/` file
  was edited; the import-direction lint passes (offline/runtime separation intact).
- **Claim ceiling remains Rung 1.** No artifact raises it; `docs/ledger.md` remains the only
  ceiling-bearing artifact and was not mutated.
- **No Competition Data leakage.** Hygiene clean; no card/deck/trace tokens in any tracked file.
- **No forbidden-path mutation:** `frozen/`, `runs/`, `cg/`, `deck.csv`, `.claude/`,
  `.beads/`, `grimoires/loa/context/`, `grimoires/loa/a2a/`, `regime-v001`, and
  `docs/ledger.md` are all unmodified (verified via `git status`).
- **No new or mutated run directories;** the sealed local `run-0001`/`run-0002` were read
  read-only and remain byte-unchanged.

---

## 7. Known limitations / residual risks

- **AC-7 review/audit artifacts pending.** The `/review-sprint` + `/audit-sprint` artifacts
  are produced in the next Golden Path step, not by `/implement`. Until then the loop's
  review/audit half is unverified by definition.
- **`--no-ledger` semantics are a suppressor, not a literal no-op.** Per Sprint-Plan DQ-2
  ("deprecated no-op alias") read together with the SDD caller-audit note ("`NoLedgerGuardSmoke`
  … passes under the new default"), `--no-ledger` is retained as a fail-safe that still
  suppresses any ledger write (it can only ever *prevent* a write). This keeps the existing
  CLI compatibility test passing unchanged and is the conservative reading for a
  contamination-hardening sprint; a reviewer may prefer a literal no-op, which would require
  editing `test_cli_no_ledger_flag`.
- **FM-05/FM-09 are `detector: none-yet`, not `forbidden`** (per SDD §5.1). They are
  `axis: loss-attribution`; the taxonomy notes explicitly that `none-yet` records absence
  only and does not authorize a per-decision quality scorer (which remains the separate
  operator decision the forbidden boundary names).
- **`avg_match_length`↔`avg_turns` alias** is documented in `analysis/delta_report.py`'s
  docstring only — no `frozen/` edit (a frozen change is a new regime).
- **Delta-table "unchanged" reading (DQ-1):** "unchanged" = the table rows and delta values;
  additive why-moved prose is the intended new output. Confirmed via the read-only
  `run-0001` vs `run-0002` run (delta column values identical to prior behavior).

---

## 8. Remaining unstaged / pre-existing dirty files

These were dirty at session start and were **not** staged, committed, or modified by this work:
- `.beads/issues.jsonl`
- `grimoires/loa/NOTES.md`

---

## 9. Next recommended Golden Path command

```
/review-sprint sprint-02
```
