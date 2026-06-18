# Cycle-001 / Sprint 02 Sprint Plan — Delta Explanation + Failure-Mode Taxonomy

> Planning artifact (Sprint Plan). Status: **DRAFT — research/planning only.** This document opens **NO build gate.**
> Implementation requires a separate, explicit operator build-gate action (OA-2 equivalent) per `docs/operator/turntrace-loop-contract.md` §6.
> Binding governance: `docs/operator/deferred-lane-gate-after-sprint-01.md` — **"NARROW PLANNING GATE OPENED. Broad optimization remains closed."**
> Binding input: `docs/cycles/cycle-001-sprint-02/02-sprint-02-sdd.md` (the accepted Sprint 02 SDD). Where this Sprint Plan disagrees with the SDD, it is flagged inline as a **[Sprint Plan question]**, never an implementation decision.

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-001 / Sprint 02 |
| **Working title** | Delta Explanation + Failure-Mode Taxonomy |
| **Type** | Sprint Plan (planning artifact, not a build artifact) |
| **Status** | DRAFT — awaiting operator acceptance; next Golden Path step is the build gate (OA-2 → `/implement sprint-02`), not implementation now |
| **Date** | 2026-06-18 |
| **Base commit** | `072f1b7` — *docs: add TurnTrace Sprint 02 SDD* |
| **Posture** | EXPLAIN / AUDIT only — not an agent-improvement sprint |
| **Claim ceiling** | Rung 1 (unchanged; not raised) |
| **Scope size** | LARGE (7 tasks: 5 Core + 1 Core E2E + 1 Stretch) |

---

## 1. Sprint objective

Translate the accepted PRD (`01-sprint-02-prd.md`) and SDD (`02-sprint-02-sdd.md`) into an implementation-ready task plan that, **when a build gate is later opened**, makes TurnTrace's first same-regime comparison (`run-0001` vs `run-0002`, `regime-v001`, n=12) **explainable** and makes future comparisons **auditable** — without touching the runtime agent, without raising the claim ceiling, and without opening broad optimization.

The objective is bounded to the analysis/offline and provenance/docs layers. Six requirements (PR-1..PR-6) plus an end-to-end goal-validation task land across `docs/` and `analysis/` + `eval/`. No `agents/runtime/` file is touched by any task.

---

## 2. Posture and gates (binding)

This Sprint Plan states, as binding posture:

```
This Sprint Plan opens no build gate.
Implementation requires a later explicit operator OA-2 / build-gate action.
Broad optimization remains closed.
Runtime agent changes remain forbidden.
Claim ceiling remains Rung 1.
```

- **EXPLAIN / AUDIT only.** Sprint 02 improves TurnTrace's ability to explain and audit the first comparison. It is **not** an agent-improvement sprint (no rule/heuristic/scoring change to `agents/runtime/`). (PRD §Required posture; `deferred-lane-gate-after-sprint-01.md:89-97`.)
- **Broad optimization stays closed.** Every "Still closed" item (`deferred-lane-gate-after-sprint-01.md:71-87`) remains closed and requires a **separate, explicit operator decision** that supersedes the deferred-lane note. This Sprint Plan opens none of them.
- **Claim ceiling held at Rung 1.** No task raises it (`docs/claim-ceiling.md`; deferred-lane note L43). The experiment ledger (`docs/ledger.md`) remains the only ceiling-bearing artifact.
- **Build gate (OA-2) is the single hard procedural gate.** Planning artifacts — including this Sprint Plan — never open the gate (loop contract §6). `/implement sprint-02` may run only after a separate, explicit operator authorization.

---

## 3. Scope summary

| Task | Maps to | Title | Class | Zone |
|---|---|---|---|---|
| **T1** | PR-1 / S02-1 | Failure-mode taxonomy v001 (tracked, sanitized) | **Core** | docs |
| **T2** | PR-2 / S02-2 | Aggregate failure-mode report (sanitized categories only) | **Core** | App (`analysis/`) |
| **T3** | PR-3 / S02-3 | `delta_report` hardening (why-lines + None↔number) | **Core** | App (`analysis/`) |
| **T4** | PR-4 / S02-4 | Ledger contamination hardening (CF-01, Option C) | **Core** | App (`eval/`) |
| **T5** | PR-5 / S02-5 | `replay_check` dead-path marker/test (CF-02) | **Stretch** | App (`analysis/`) |
| **T6** | PR-6 / S02-6 | Strategy-report update (PERMITS/FORBIDS, §1/4/6/7) | **Core** | docs |
| **T7** | all ACs | End-to-end goal validation (AC sweep, no new code) | **Core** | docs |

**In scope:** the six PRs above (T1–T6) plus a final E2E goal-validation pass (T7). All confined to analysis/offline + provenance/docs layers.

**Out of scope (mentioned only as forbidden):** all "Still closed" broad-optimization items (`deferred-lane-gate-after-sprint-01.md:71-87`); any per-decision agent-quality detector/scorer (NG3); any runtime agent change (NG1); any claim above Rung 1 (NG2); any raw trace/card/deck emission (NG4); any new/mutated run dir or `frozen/`/`regime-v001` edit (NG5); opening a build gate (NG6).

> The seven tasks map exactly onto the seven allowed narrow-planning lanes (`deferred-lane-gate-after-sprint-01.md:61-69`): explainability of the first delta (T3, T6), failure-mode taxonomy (T1), comparison robustness (T3, T5), trace-safe/Competition-Data-safe aggregate diagnostics (T2), provenance & ledger hardening (T4), `delta_report` hardening (T3), operator-decision framing (T6).

---

## 4. Explicit operator decisions carried forward

The SDD's recommended dispositions are carried as the Sprint Plan's recommended defaults. **None is silently opened.** Each remains an operator decision confirmable at the build gate.

| ID | Decision | Sprint-Plan default (recommended) | Source |
|---|---|---|---|
| **OD-1 / PR-5** | PR-5 (replay_check marker) Core or Stretch? | **Stretch.** Include only if capacity remains after T1–T4 + T6 + T7. Droppable without failing the sprint. | SDD §14 OD-1; PRD §11 OD-1 |
| **OD-2 / PR-4** | PR-4 (ledger hardening) mandatory? | **Core / Mandatory.** Protects the only ceiling-bearing artifact; closes recorded residual CF-01. | SDD §14 OD-2 |
| **OD-3 / PR-6** | PR-6 (strategy report) in-sprint or closeout-only? | **In-sprint Core**, not closeout-only. Fills the Mandatory §6 honesty section. | SDD §14 OD-3 |
| **OD-4** | Per-decision quality detectors allowed? | **No.** FM-03/04/06/08 stay name-only; encoded as `detector: forbidden` in T1. | SDD §14 OD-4; PRD §11 OD-4 |
| **OD-5** | Runtime agent changes allowed? | **No.** No `agents/runtime/` file in the module plan. | SDD §14 OD-5; PRD §11 OD-5 |
| **OD-6** | Build gate open yet? | **No.** T2–T5 (App-Zone code) require OA-2; this Sprint Plan opens nothing. | SDD §14 OD-6; PRD §11 OD-6 |
| **OD-8** | Artifact tracking | **Taxonomy (T1) + strategy report (T6) are tracked sanitized docs.** Aggregate-report output (T2) is **local/git-ignored unless explicitly operator-approved** (SP-6 relaxation). Default = stdout, no file. | SDD §14 OD-8; PRD §11 OD-8 |
| **DQ-1** | "Present numeric output unchanged" reading (T3) | **Read as: delta-table values unchanged.** Additive why-moved prose IS allowed and intended (symmetric with existing why-no-change prose). | SDD §13 DQ-1 |
| **DQ-2** | `--no-ledger` removed or kept? (T4) | **Keep `--no-ledger` as a deprecated no-op alias** under PR-4 Option C (its meaning "don't write" is now the default). Do not drop it outright. | SDD §13 DQ-2 |

> **Not silently opened.** OD-7 (CF-04 `.beads/.br_history/` housekeeping) is explicitly **not** Sprint 02 implementation scope (PRD §11 OD-7); this Sprint Plan does not fold it in and does not touch `.beads/`. Any "Still closed" lane stays closed.

---

## 5. Task breakdown

Each task records: requirement mapping, class, target files (authorized; see §7), the design it implements (per SDD §5), and per-task verification. **No task is executed by this Sprint Plan** — they are specifications for a future `/implement sprint-02` once a gate is open.

### T1 / PR-1 — Failure-mode taxonomy v001 (Core, docs) → **[G2, G7]**

**Requirement.** Produce a tracked, sanitized failure-mode taxonomy v001 organizing coarse outcome/loss categories, each declaring (a) computable-now vs deferred and (b) its gating capability flag, with a detector enum and an inline boundary forbidding per-decision quality detectors. (PRD PR-1; SDD §5.1.)

**Design (SDD §5.1, §4.1).**
- **Create** `docs/failure-mode-taxonomy-v001.md` (sibling file; OQ-2 resolved — do **not** rewrite the append-only `docs/failure-modes.md` in place).
- **Edit (1 line)** `docs/failure-modes.md` — add a one-line pointer near the header ("See taxonomy v001: `docs/failure-mode-taxonomy-v001.md`").
- One §4.1 entry per FM-01..FM-09 with fields: `fm_id`, `name`, `axis` (`outcome` | `loss-attribution`), `compute_status` (`computable-now` | `deferred`), `gating_capability` (`seed_controlled` | `invalid_action_detectable` | `timeout_detectable` | `none`), `capability_value` (bool, mirroring `sim/capabilities.json`), `signature` (field-name reference only — never row contents), `evidence_ref` (`run_id`+`match_id`+`decision_index` reference string only, or null), `detector` (`present` | `none-yet` | `forbidden`), `status` (`open` | `mitigated` | `watched` | `wont-fix`).
- **Detector-forbidden boundary (binding).** For `fm_id ∈ {FM-03, FM-04, FM-06, FM-08}`: `detector: forbidden` + `axis: loss-attribution`, with the inline note: *"Building any per-decision quality detector/scorer for this category is NOT covered by the narrow-planning gate and is a separate operator decision."* (Encodes NG3 / OD-4 mechanically in the doc.)
- **Computability per existing probe** (`docs/failure-modes.md:25-101`): FM-01 `computable-now` (`invalid_action_detectable=true`, detector `present`); FM-07 `computable-now` (`ending_cause` distribution + `avg_turns`, detector `none-yet` → `present` once T2 lands); FM-02 `deferred` (`timeout_detectable=false`); FM-05/09 `deferred`, detector `none-yet`.
- **Sanitization.** Signatures cite field names only; no `result`/`ending_cause` distribution **values** pasted (`requires-raw-data: cannot-surface`); Rung-1 language, no forbidden words.

**Verification.** `python eval/hygiene_check.py --paths docs/failure-mode-taxonomy-v001.md docs/failure-modes.md`; forbidden-word grep (expect none except negated); manual cross-check of every `gating_capability` value against `sim/capabilities.json`; assert FM-03/04/06/08 carry `detector: forbidden` + the inline boundary; assert every `status` is in the allowed enum. (Doc-level; no unit test for a markdown file.)

### T2 / PR-2 — Aggregate failure-mode report (Core, `analysis/`) → **[G3, G1, G7]**

**Requirement.** Add an analysis-layer report that reads **only** already-aggregated, sanitization-safe fields from a **local, git-ignored** run dir and emits **coarse counts only** — never raw trace rows, card IDs, deck lists, or hand contents. (PRD PR-2; SDD §5.2, §4.2.)

**Design (SDD §5.2, §4.2; OQ-5 resolved — new module, not an `aggregate.py` extension).**
- **Create** `analysis/failure_report.py`: `aggregate_failures(run_dir: Path) -> dict` (pure read), `render(rep) -> str`, `render_json(rep) -> str`, `main(argv)`.
- Reads **only** `runs/<run_id>/match_results/<match_id>.json` and `runs/<run_id>/manifest.json`. Allowed fields: `result`, `ending_cause`, `error` (presence-flag only, never the string body), `invalid_action_count`, `turns`, `total_decisions`, `trace_present`, `run_id`/`regime_id`, `n`. **Forbidden reads:** `traces/*.jsonl` row contents, `private_state_summary`, `legal_actions_sample`, `selected_action`, card-id digests, deck lists.
- **Output** (SDD §4.2 schema): `result_counts`, `ending_cause_counts` (incl. `<unmapped>`), `error_present_count`, `invalid_action_total`, `fm_links` (reference strings only), `claim_ceiling_footer` (Rung-1, no strength claim). Markdown to stdout default; `--json`; `--out <local-path>` writes a **local/git-ignored** file only (OD-8 — tracking requires explicit operator approval; default = no file).
- **Degrade cleanly.** Empty `match_results/` → raise `ValueError` (exit 1). Record lacking `ending_cause` → bucket `<unmapped>` and report count (undetectable reported, never silently dropped). `invalid_action_detectable=false` → exclude from `invalid_action_total` + note exclusion.
- **Imports.** stdlib only (NFR-7); `analysis/` zone only; MAY `import aggregate` intra-zone (for `n`/ids), mirroring `delta_report.py:35`. MUST NOT import `cabt`/`sim`/`eval`/`agents/runtime`.
- **Lint-coverage gap-closure (SDD §2, §8).** As part of T2 acceptance, add an assertion (in `tests/test_smokes.py` or `tests/test_import_direction.py`) that `analysis/failure_report.py` is present in the lint's scanned set and reports zero violations — so a new analysis module cannot silently escape the import-direction rule.

**Verification.** `python tests/test_import_direction.py`; `python tests/test_smokes.py` (new `FailureReportSmoke`); `python eval/hygiene_check.py --paths analysis/failure_report.py`; run read-only vs local `run-0002`, grep output for card/deck tokens (expect none); synthetic-fixture count test; a poisoned-trace fixture that MUST be ignored (no `traces/` read, no raw-row emission); missing-field / empty-run test. **Synthetic fixtures use a fixed seed** for any randomized record generation (see §13).

### T3 / PR-3 — `delta_report` hardening (Core, `analysis/`) → **[G1, G4, G7]**

**Requirement.** Harden `analysis/delta_report.py` so a `None↔number` transition renders honestly (no fabricated `down`), and every MOVED metric carries a why-moved line — preserving the present numeric delta-table values and the cross-regime exit-2 refusal. (PRD PR-3; SDD §5.3.)

**Confirmed defect (grounded against code).** `_delta` returns `None` when either side is non-numeric (`delta_report.py:73-78`); `moved` fires on a `None↔number` transition via `va != vb and d is None` (`:109`); `direction = "up" if (m["delta"] or 0) > 0 else "down"` (`:156`) → `(None or 0) > 0` is `False` → a `None→number` transition always renders `down`, regardless of value. No why-moved line exists (only `WHY_NO_CHANGE`, `:46-59`, `:145-151`).

**Design (SDD §5.3).**
- Add a `change_kind` field per metric in `compare`: `unchanged`, `moved` (both numeric, `d != 0`), `appeared` (`a is None`, `b` numeric), `disappeared` (`a` numeric, `b is None`).
- In `render`, branch on `change_kind`: `appeared` → status `APPEARED`, text `"n/a -> <b>"`, no direction; `disappeared` → status `DISAPPEARED`, text `"<a> -> n/a"`, no direction. Compute `up`/`down` **only** when both sides numeric — guard `isinstance(m["delta"], (int,float))` before the `> 0` test (removes the `(None or 0)` footgun).
- Add `WHY_MOVED` companion to `WHY_NO_CHANGE` so every moved/appeared/disappeared metric carries an explanation, symmetric with the existing unmoved coverage; each line bounded by the Rung-1 ceiling, asserting no strength claim.
- **`avg_match_length`↔`avg_turns` alias** documented in the module docstring (and optionally a one-line report footnote). **No `frozen/` edit** — promote the existing in-code comment (`delta_report.py:39`) to an explicit docstring alias note.

**Preservation guarantees (must hold).** `COMPARE_METRICS` unchanged (`:41-43`); `avg_wall_clock_ms` stays excluded (`:162-164`); cross-regime `CrossRegimeRefusal` → exit 2 unchanged (`:90-96`, `:186-188`); **present numeric delta-table values unchanged** for `run-0001` vs `run-0002` (all five metrics numeric on both sides → only `moved`/`unchanged` branches execute; the why-moved line is the intended additive output per DQ-1).

**Verification.** `python tests/test_smokes.py` (`DeltaReportSmoke`): `None→number` asserts `change_kind=="appeared"`, status not `down`, why-line present; `number→None` asserts `disappeared`; both-numeric-moved asserts a why-moved line; all-unmoved asserts existing why-no-change lines intact; read-only run vs local `run-0001`/`run-0002` asserts **delta-table values unchanged**; cross-regime fixture asserts exit 2; forbidden-word grep. **Synthetic stat fixtures only — no Competition Data; any randomized fixture sets a fixed seed (§13).**

### T4 / PR-4 — Ledger contamination hardening / CF-01 (Core, `eval/`) → **[G4, G7]**

**Requirement.** Change `eval/run_eval.py` so writing a tracked row to `docs/ledger.md` requires **explicit deliverable intent** — a default/non-deliverable invocation MUST NOT append to `docs/ledger.md`. `summary.csv` is still always written; append-only ledger + the two existing rows preserved. (PRD PR-4; SDD §5.4.)

**Confirmed footgun (grounded against code).** `run_eval(..., write_ledger=True)` defaults `True` (`run_eval.py:93`); `ledger_path` resolves to `docs/ledger.md` when `None` (`:103`); `main` wires `write_ledger = not args.no_ledger` (`:321`). A bare `python eval/run_eval.py` → `write_ledger=True` + `ledger_path → docs/ledger.md` → appends to the tracked ledger. Opt-OUT design.

**Design — Option C (SDD §5.4; OQ-3 resolved).** Require `--ledger <path>` OR `--deliverable`; bare invocation writes no ledger.
- `run_eval(...)` signature: change `write_ledger: bool = True` → `write_ledger: bool = False`. Keep `ledger_path` as "where." Write a ledger row iff `write_ledger is True` **and** `ledger_path` resolves.
- `main()`: add `--deliverable` (`action=store_true`); keep `--ledger <path>`. Compute `write_ledger = bool(args.deliverable or args.ledger)`; `ledger_path = Path(args.ledger) if args.ledger else (REPO_ROOT/"docs"/"ledger.md")` (consulted only when `write_ledger`). Bare invocation → `write_ledger=False`.
- **DQ-2:** keep `--no-ledger` as a **deprecated no-op alias** (its meaning "don't write" is now the default) with a one-line deprecation note. Do not drop it outright.
- **Caller audit (OQ-4 — same `/implement`):** update `tests/test_smokes.py::RunEvalSmoke` (`:110`) to declare deliverable intent (`write_ledger=True` / new deliverable path) so it keeps asserting a row is written (`:142-147`). `test_main_returns_3_on_populated_dir` (`:156`, passes `--ledger <tmp>`) — guard fires before any ledger write, still exits 3, behavior preserved. `NoLedgerGuardSmoke` (`:249`) passes under the new default. CLI docstring examples (`:34-36`) updated to require `--deliverable` for the deliverable run.

**Preservation guarantees.** `summary.csv` always written (the `else` branch at `run_eval.py:274-280` becomes the default path); append-only ledger + non-empty `claim_ceiling` (`analysis/aggregate.py` idempotency) unchanged; `run-0001`/`run-0002` rows never edited in place; exit codes 0/1/2/3 (`run_eval.py:323-331`) + immutability guard (`:131-147`) unchanged.

**Verification.** `python tests/test_smokes.py` (`NoLedgerGuardSmoke` + new `DeliverableLedgerSmoke`): bare/default invocation writes no ledger row/file; `--deliverable` / `write_ledger=True, ledger_path=<tmp>` writes exactly one row, idempotent on re-run; `--no-ledger` deprecated no-op compatibility check. **All ledger-write tests MUST use a temporary ledger path (`tmp_path`), never the tracked `docs/ledger.md`** (§7, §9).

### T5 / PR-5 — `replay_check` dead-path marker/test (Stretch, `analysis/`) → **[G5, G7]**

**Requirement.** Mark `byte_identical()` in `analysis/replay_check.py` as a dead/unreachable path with an explicit upgrade trigger, and strengthen the test so `seed_controlled=false` returns unseeded/skipped and **never `passed`**. No fake seed injected. (PRD PR-5; SDD §5.5.) **Stretch (OD-1): only if capacity remains after T1–T4 + T6 + T7.**

**Design (SDD §5.5).**
- **Marker.** Add a `loa:shortcut` line on `byte_identical` (`replay_check.py:98`) naming the ceiling + upgrade trigger, e.g. `# loa:shortcut: dead path — unreachable while seed_controlled=false; reachable only when seed control is proven (sim/capabilities.json seed_controlled=true) and --replay-run is supplied`.
- **Test.** Strengthen `ReplayCheckSmoke` with an explicit assertion that `determinism["status"] != "passed"` under unseeded (in addition to `== "skipped"`), plus a guard test that flips a fixture to assert the skip branch cannot silently become `passed`. **No fake seed injection** — fixtures keep `seed_controlled=false`; the test verifies posture, never manufactures seed control (NG2 reproducibility boundary).
- **No byte-identical claim.** The always-on `audit_trail_equality` tier (`:69-88`) is unchanged.

**Verification.** `python tests/test_smokes.py` (`ReplayCheckSmoke`): assert `mode=='unseeded'`, `status=='skipped'`, `status != 'passed'`; confirm `sim/capabilities.json` still reports `seed_controlled=false` before asserting the dead path stays dead. **Tamper/flip fixtures copy into a tempdir first — never mutate `run-0001`/`run-0002`. No seed is fabricated (§13).**

### T6 / PR-6 — Strategy-report update (Core, docs) → **[G6, G1, G7]**

**Requirement.** Update `docs/strategy-report.md` with a PERMITS/FORBIDS framing and per-sentence artifact traceability; fill §1, §4, §6, §7; keep §5 DEFERRED. (PRD PR-6; SDD §5.6.)

**Design (SDD §5.6).**
- **§1 Claim ceiling** (`strategy-report.md:10-14`): state Rung 1; cite `docs/claim-ceiling.md` + the ledger's per-row `claim_ceiling`.
- **§4 Evaluation method** (`:27-33`): `run-0001` vs `run-0002` same-regime agent-only comparison, n=12, `mode=unseeded`; cite `regime-v001` + ledger rows.
- **§6 Failure-mode section** (`:42-46`, **Mandatory** under the Rung-4 honesty gate): link `docs/failure-mode-taxonomy-v001.md` (T1) + `docs/failure-modes.md`; name computable-now vs deferred/forbidden categories.
- **§7 Limitations** (`:48-54`): unseeded/no byte-replay, timeout undetectable, n=12 small, opponent = mirror.
- **§5 Ablation table** (`:35-40`): remains **DEFERRED** — unchanged.
- **PERMITS / FORBIDS** (mirrors `deferred-lane-gate-after-sprint-01.md:37-69`): PERMITS = a recorded same-regime agent-only metric movement bounded by the Rung-1 ledger ceiling (PRD §9, `01-sprint-02-prd.md:171-175`); FORBIDS = strength/significance/cross-regime/leaderboard claims, the five forbidden words, and every "Still closed" item (`deferred-lane-gate-after-sprint-01.md:71-87`).
- **Traceability rule (binding).** Every claim sentence references a specific logged artifact (ledger row / match-summary / regime hash / `delta_report` output) per `strategy-report.md:65-68`; runs by `run_id`+hashes; decks by `deck_id`+hash; **no raw metric values pasted beyond what the sanitized ledger already carries**; no forbidden claim words except as negated/forbidden language.

**Verification.** Manual traceability pass (each non-skeleton sentence cites an artifact path/reference); `python eval/hygiene_check.py --paths docs/strategy-report.md`; forbidden-word + card/deck-token grep (expect none); cross-check PERMITS/FORBIDS against the deferred-lane note (every "Still closed" item present, nothing reframed as permitted); confirm §5 still reads DEFERRED.

### T7 — End-to-End Goal Validation (Core, docs) → **[all goals]**

**Priority:** P0 (Must Complete). **Goal contribution:** G1–G7. **No new code** — an acceptance sweep run after T1–T6 land.

**Description.** Validate that all PRD goals (G1–G7) and ACs (AC-1..AC-8) are achieved through the implemented tasks, before the implementation report is written. See the validation matrix in §10 and the AC mapping in §9.

**Validation steps.**

| Goal | Validation action | Expected result |
|---|---|---|
| G1 — Explain the first delta | T3 + T6 landed: `delta_report` renders honestly; strategy-report explains the move from sanitized artifacts | delta-table values unchanged; every moved metric has a why-line; report cites artifacts |
| G2 — Sanitized taxonomy | T1 landed: every FM category declares status + capability flag + detector enum | `docs/failure-mode-taxonomy-v001.md` present, hygiene-clean, FM-03/04/06/08 `detector: forbidden` |
| G3 — Competition-Data-safe aggregate diagnostics | T2 landed: report emits counts only, reads no traces | output is counts only; no card/deck tokens; no `traces/` read |
| G4 — Harden comparison/provenance | T3 + T4 landed | None↔number honest; default `run_eval` writes no ledger; existing rows untouched |
| G5 — Keep the audit honest | T5 landed (if included) | `byte_identical` marked dead; unseeded never `passed`; no fake seed |
| G6 — Record permits/forbids | T6 landed | PERMITS/FORBIDS complete; §5 DEFERRED; every sentence cites an artifact |
| G7 — Stay inside the gate | all tasks | no `agents/runtime/` change; Rung 1 held; no build gate opened; no broad-optimization item touched |

**Acceptance.** Each goal validated with documented evidence in `docs/cycles/cycle-001-sprint-02/implementation-report.md`; no goal marked "not achieved" without explicit justification; all §10 validation commands pass; claim ceiling re-verified Rung 1.

---

## 6. Task ordering / dependency graph

Recommended safe order (matches SDD module dependencies; no agent/runtime change appears anywhere):

```
T1 (taxonomy doc boundary)
   │  defines categories/capability flags the report consumes
   ▼
T2 (aggregate report) ──────────────┐
                                     │  T2 categories + T3 semantics feed the report narrative
T3 (delta_report hardening) ─────────┤
   (independent of T1/T2; explanation-facing)
                                     │
T4 (ledger hardening) ───────────────┤
   (independent; gates any future deliverable run before it could contaminate the ledger)
                                     ▼
T6 (strategy report) ◀───────────────┘  written after taxonomy/report/delta semantics are defined
   │
   ▼
T5 (replay_check marker) — Stretch, only if capacity remains after T1–T4 + T6 + T7
   │
   ▼
T7 (E2E goal validation) — last; sweeps all ACs after code/docs land
```

| Order | Task | Depends on | Rationale |
|---|---|---|---|
| 1 | **T1** | — | Taxonomy doc boundary must exist before the report implementation references its categories. |
| 2 | **T2** | T1 | Aggregate report uses taxonomy categories/capability flags. |
| 3 | **T3** | — | `delta_report` hardening is independent but explanation-facing; lands before T6 narrates the delta. |
| 4 | **T4** | — | Ledger hardening lands before any future deliverable run could contaminate the ledger. |
| 5 | **T6** | T1, T2, T3 | Strategy report is written after taxonomy/report/delta semantics are defined. |
| 6 | **T5** | (none; Stretch) | `replay_check` marker only if time remains after Core + T7. |
| 7 | **T7** | T1–T6 | E2E goal-validation sweep runs last, after all tasks land. |

> Each task is small enough to land and be verified independently. T2, T3, T4 are mutually independent (only T2 depends on T1). The Sprint Plan may reorder T3/T4 with justification, **but must never place any agent/runtime change anywhere — there is none.**

---

## 7. File authorization matrix

**Authorized for a future `/implement sprint-02` ONLY (no other path may be touched):**

| Path | Task(s) | Action | Zone |
|---|---|---|---|
| `docs/failure-mode-taxonomy-v001.md` | T1 | create | docs (tracked) |
| `docs/failure-modes.md` | T1 | edit (1-line pointer only) | docs (tracked) |
| `analysis/failure_report.py` | T2 | create | App (`analysis/`) |
| `analysis/delta_report.py` | T3 | edit | App (`analysis/`) |
| `analysis/replay_check.py` | T5 (Stretch) | edit (marker + no behavior change) | App (`analysis/`) |
| `eval/run_eval.py` | T4 | edit | App (`eval/`) |
| `tests/test_smokes.py` | T2, T3, T4, T5 | create/edit test classes | tests |
| `tests/test_import_direction.py` | T2 | edit (optional — lint-coverage assertion may live here or in `test_smokes.py`) | tests |
| `docs/strategy-report.md` | T6 | edit (§1/4/6/7 + PERMITS/FORBIDS; §5 stays DEFERRED) | docs (tracked) |
| `docs/cycles/cycle-001-sprint-02/implementation-report.md` | T7 | create | docs (tracked) |

**Explicitly FORBIDDEN to touch (any task, any path):**

| Path | Why |
|---|---|
| `agents/runtime/` | No runtime agent behavior change (NG1, OD-5). |
| `frozen/` (incl. `regime-v001` components, `frozen/metrics/metrics-spec-v001.json`) | A frozen-component change is a new regime v002, never an edit (NG5; `docs/claim-ceiling.md:29-35`). |
| `runs/` | No new/mutated run dirs; `run-0001`/`run-0002` stay sealed/local (NG5, ESP-1). |
| `cg/`, `deck.csv` | Competition Data — never committed/read into tracked artifacts (CC-1/CC-2, NG4). |
| `grimoires/loa/context/` | Local Competition-Data home (CC-1). |
| `grimoires/loa/a2a/` | **Except** review/audit artifacts and the COMPLETED marker **when authorized** (loop contract §10; orchestrator-persisted, never by `/implement`). |
| `.claude/` | System Zone — never edited (loop contract §9; zone-system rule). |
| `.beads/` | State Zone task store; not Sprint 02 implementation scope (OD-7). Not staged/committed by this work. |
| `docs/ledger.md` | **Except** controlled operator-approved deliverable rows, which Sprint 02 must **not** produce. **PR-4 (T4) tests MUST write to a temporary ledger path, never the tracked `docs/ledger.md`.** |

> **PR-4 test constraint (binding).** Every T4 ledger-write test uses a temporary ledger path (`tmp_path` / `shutil.copytree` tempdir), exactly as the existing tests do (`tests/test_smokes.py` redirects `ledger_path` to a tmp). No test edits tracked `docs/ledger.md`.

---

## 8. Acceptance criteria

Sprint-level acceptance criteria, mapped to the SDD ACs (SDD §6) and PRD ACs (PRD §7). All bounded to Rung 1; all forbid agent strengthening.

| AC | Theme | Task(s) | Expected artifact | Validation command/check | Stop condition |
|---|---|---|---|---|---|
| **AC-1** | Taxonomy honesty | T1 | `docs/failure-mode-taxonomy-v001.md`; pointer in `docs/failure-modes.md` | `python eval/hygiene_check.py --paths docs/failure-mode-taxonomy-v001.md`; forbidden-word grep; manual capability-flag cross-check vs `sim/capabilities.json` | A per-decision quality detector appears, or a category claims a detector its capability forbids. |
| **AC-2** | Aggregate-only diagnostics | T2 | `analysis/failure_report.py`; tests | `python tests/test_import_direction.py`; `python tests/test_smokes.py`; `python eval/hygiene_check.py --paths analysis/failure_report.py`; run vs local `run-0002`, grep for card/deck tokens (expect none) | The report reads or emits any raw trace row / card-adjacent token, or imports `cabt`/`sim`/`eval`/`runtime`. |
| **AC-3** | Delta correctness | T3 | `analysis/delta_report.py`; `DeltaReportSmoke` | `python tests/test_smokes.py`; None↔number fixtures; `run-0001` vs `run-0002` delta-table-unchanged assertion; cross-regime exit-2 check | A None↔number transition still renders a fabricated `down`, or `frozen/` is edited, or a delta-table value changes for the current runs. |
| **AC-4** | Ledger integrity | T4 | `eval/run_eval.py`; `NoLedgerGuardSmoke` + `DeliverableLedgerSmoke` | `python tests/test_smokes.py`; default-no-write fixture; explicit-deliverable-write fixture (tmp ledger); idempotency; `--no-ledger` no-op check | A default/non-deliverable invocation appends to `docs/ledger.md`, or an existing row is edited in place. |
| **AC-5** | Replay honesty (Stretch) | T5 | `analysis/replay_check.py`; `ReplayCheckSmoke` | `python tests/test_smokes.py`; assert `status != 'passed'` and `== 'skipped'` under unseeded | A fake seed is injected, or the skip branch can become `passed` while unseeded. |
| **AC-6** | Report traceability | T6 | `docs/strategy-report.md` | manual traceability pass; `python eval/hygiene_check.py --paths docs/strategy-report.md`; forbidden-word + card/deck grep; §5-still-DEFERRED check | A claim sentence lacks an artifact ref, or a forbidden claim is made, or §5 is filled. |
| **AC-7** | Loop discipline | all (T7 verifies) | `/implement` patches; one review + one audit artifact | orchestrator persists `grimoires/loa/a2a/sprint-02/engineer-feedback.md` + `auditor-sprint-feedback.md` | Code lands outside `/implement`, or a COMPLETED marker appears without operator authorization. |
| **AC-8** | Claim ceiling held | all (T7 verifies) | every tracked Sprint 02 artifact | forbidden-word grep across all changed tracked files; ledger remains the only ceiling-bearing artifact | Any artifact makes a claim beyond Rung 1, or a non-ledger artifact asserts a ceiling. |

> **Carried gap (PRD §7).** The Sprint 01 closeout cites AC-01..AC-08 while the Sprint 01 plan enumerates AC-01..AC-06; resolving any inherited criterion requires the Sprint 01 review/audit feedback artifacts, which are not in tracked evidence. Sprint 02 inherits no such criterion — its ACs are self-contained above.

---

## 9. Validation commands

**Always-run gates (every task, before staging):**

```bash
python tests/test_import_direction.py
python tests/test_smokes.py
python eval/hygiene_check.py --paths <changed tracked files>
```

- `test_import_direction.py` covers the offline/runtime separation for all `analysis/`/`eval/` changes; the new `analysis/failure_report.py` is auto-included (it globs `analysis/*.py`), and T2 adds an assertion that the module is in the scanned set with zero violations.
- `test_smokes.py` is the stdlib `unittest` suite (NFR-7); new/edited test classes live here.
- `hygiene_check.py --paths` is run against each changed tracked doc/code file before staging (blocks `runs/<id>/`, `cg/`, `deck.csv`, PDFs, `card*.csv`, `grimoires/loa/context/`).

**Planned targeted checks:**

- taxonomy status enum / capability flag manual check (vs `sim/capabilities.json`)
- FM-03/04/06/08 detector: `forbidden` check + inline boundary note present
- `failure_report` synthetic fixture counts (per `result`/`ending_cause`)
- poisoned-trace-ignored / no-raw-row-emission test (`failure_report` must not read `traces/`)
- `failure_report` missing-field / empty-run behavior (`<unmapped>` bucket; `ValueError` on empty)
- `delta_report` None↔number `appeared`/`disappeared` tests (no fabricated `down`)
- why-moved / why-no-change coverage tests (every metric carries the right line)
- `delta_report` cross-regime refusal exit 2 unchanged
- `delta_report` delta-table values unchanged for `run-0001` vs `run-0002` (read-only)
- default `run_eval` does NOT write `docs/ledger.md` (bare invocation → no row/file)
- `--deliverable` / `--ledger <tmp>` explicit-write tests using a **temporary ledger path** (exactly one row, idempotent)
- `--no-ledger` deprecated no-op compatibility check
- `replay_check` unseeded/skipped, never `passed` (if T5 included)
- strategy-report traceability pass + forbidden-word grep + §5-DEFERRED check

> **No validation step may mutate `run-0001`, `run-0002`, or the tracked `docs/ledger.md`.** Run-dir tests either read the sealed local runs read-only or build throwaway tempdirs (the existing `shutil.copytree` + `write_ledger=False` pattern). Tamper/flip fixtures copy into a tempdir first.

---

## 10. Review / audit expectations

Per the loop contract (`docs/operator/turntrace-loop-contract.md` §1-§3, §10), Sprint 02 closes through exactly **one `/review-sprint sprint-02` artifact and one `/audit-sprint sprint-02` artifact**; corrective changes re-enter only through `/implement` (single patch authority). Future review/audit MUST verify:

- implementation touched **only** the authorized paths (§7); no forbidden path edited
- **no runtime agent behavior change** (no `agents/runtime/` edit; import-direction lint intact)
- **no Competition Data or raw run data** in any tracked file (hygiene clean; no card/deck/trace tokens)
- **no `docs/ledger.md` mutation** except explicit operator-approved deliverable rows — which **Sprint 02 must not produce** (no deliverable run is in scope)
- **PR-4 Option C works**: bare invocation writes no ledger; `--deliverable` and `--ledger <path>` write; `--no-ledger` deprecated no-op compatibility is documented
- **DQ-1 / DQ-2 carried correctly**: delta-table values unchanged + additive why-moved prose allowed (DQ-1); `--no-ledger` kept as deprecated no-op (DQ-2)
- **all validation commands pass** (§9)
- **claim ceiling remains Rung 1**; the ledger remains the only ceiling-bearing artifact
- **no COMPLETED marker** until explicit operator closeout authorization (loop contract §10)

> Review/audit are pure-review skills: `Write`/`Edit` disabled inside them is **expected, not a failure** (loop contract §10). The review/audit artifact is persisted by the orchestrator into `grimoires/loa/a2a/sprint-02/` after the skill returns.

---

## 11. Evidence-storage and sanitization rules

Per loop contract §7 / ESP-1..ESP-5 / SP-6 and `eval/schemas.md`:

- **Full run dirs stay local/git-ignored.** `runs/run-0001`, `runs/run-0002`, and any throwaway tempdir runs stay local; `hygiene_check.py` blocks `runs/<id>/...` paths. `run-0001` remains unmutated from Sprint 00.
- **Aggregate report output (T2) is stdout by default.** `--out <path>` writes a **local/git-ignored** file (a run-derived artifact under ESP-1); tracking it requires explicit operator approval (SP-6 / OD-8). Default = no file.
- **Tracked docs reference only** `run_id`, content hashes, sanitized metrics, claim ceilings, and aggregate categories — never embedded raw values. The taxonomy (T1) and strategy report (T6) cite categories and reference strings; the aggregate report (T2) emits counts, not rows.
- **Forbidden in any tracked artifact:** raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs, `deck.csv` rows, Competition Data.
- **`hygiene_check.py` remains required** as a pre-commit guard and is run `--paths` on every changed file before staging.
- **requires-raw-data: cannot-surface** — actual per-run `result`/`ending_cause` distributions and run-dir file contents are not surfaced in any tracked artifact, including this Sprint Plan.

---

## 12. Claim-ceiling rules

- **Rung 1 remains the ceiling** for all Sprint 02 artifacts (`docs/claim-ceiling.md`; deferred-lane note L43). No task raises it.
- **The ledger (`docs/ledger.md`) remains the only ceiling-bearing artifact** (`docs/claim-ceiling.md:5-7`). The taxonomy, aggregate report, delta report, and strategy report carry **no** ceiling — only a Rung-1 footer asserting no strength claim (pattern: `delta_report.py:166-170`).
- **No gameplay-strength, statistical-significance, cross-regime, or leaderboard claim** appears in any tracked output. Cross-regime is additionally hard-refused by `delta_report` (exit 2), preserved by T3.
- **Allowed claim form** (PRD §9): *"candidate (`run-0002`) differs from baseline (`run-0001`) on metric M by delta under `regime-v001` at n=12,"* explained as the mechanical consequence of the single agent-under-test change.
- **Forbidden words** (`strong, competitive, optimal, calibrated, complete`) checked by grep across every changed tracked file as the AC-8 gate; they may appear only as negated/forbidden language.

---

## 13. Risks / stop conditions

| # | Risk | Mitigation (plan-level) | Stop condition |
|---|------|---|---|
| R1 | Scope creep into optimization (a "taxonomy"/"report" reinterpreted as a per-decision quality scorer or agent tuning). | T1 encodes `detector: forbidden` + inline boundary for FM-03/04/06/08; no `agents/runtime/` path authorized (§7); import-direction lint blocks reaching into runtime; review rejects any decision-logic touch. | A per-decision quality scorer or any `agents/runtime/` edit appears → HALT. |
| R2 | Claim-ceiling inflation (n=12 `win_rate` move narrated as "better"/"stronger"). | AC-8 forbidden-word grep; Rung-1 footer on every non-ledger artifact; PERMITS/FORBIDS framing in T6; ledger stays sole ceiling-bearer. | Any artifact makes a claim beyond Rung 1 → HALT. |
| R3 | Competition-Data / raw-trace leakage via T2. | T2 reads only match-summary aggregate fields (§5), never `traces/`; error captured as presence-flag; `hygiene_check` + a poisoned-trace-ignored unit test gate it. | Any card/deck/trace token in tracked output, or a `traces/` read → HALT. |
| R4 | Ledger contamination persists if T4 deferred. | T4 is Core (OD-2); Option C makes no-write the *default*, removing the footgun. Until landed, any non-deliverable run must pass `--no-ledger`/`--ledger <tmp>`. | A default/non-deliverable run appends to `docs/ledger.md` → HALT. |
| R5 | Acting on the CF-03 latent branch before T3 lands. | T3 adds runnable None↔number fixtures before the branch is relied on; the explanation narrative (T6) cites only the live moved/unmoved output, not the dead branch. | The explanation relies on the unhardened None↔number render → HALT until T3 lands. |
| R6 | Building before a gate is open. | This Sprint Plan opens no gate; T2–T5 explicitly require OA-2; the next Golden Path step is the build gate, not `/implement`. | Any code patch before OA-2 → HALT (out-of-loop edit). |
| R7 | `avg_match_length`/`avg_turns` "fixed" by editing a frozen artifact. | T3 documents the alias in-code/in-report only; `frozen/` edit is out of scope (a frozen change is a new regime). | Any `frozen/` edit → HALT. |
| R8 | False-honesty regression on CF-02. | T5 pins `status != 'passed'` under unseeded and forbids fake-seed injection; audit-trail tier unchanged. | A fake seed is injected, or the skip branch becomes `passed` → HALT. |
| R9 | "Output unchanged" (AC-3) read strictly → why-moved lines flagged as a violation. | DQ-1 resolved here: "unchanged" = delta-table values; additive why-moved prose is intended. Fallback documented (SDD §5.3): gate why-moved behind a flag or restrict to appeared/disappeared. | Operator rejects the DQ-1 reading → re-scope T3 to the flag-gated fallback. |
| R10 | A new `analysis/` module silently escapes the import-direction lint. | T2 acceptance adds an explicit assertion that `analysis/failure_report.py` is in the scanned set with zero violations (SDD §2 gap-closure). | The lint does not cover the new module → HALT until the assertion is added. |

**Reproducibility / seeding (binding for tests).** Any test fixture that generates randomized records (synthetic `match_results`, sampled stats) MUST explicitly set and surface its random seed (e.g. `random.seed(<fixed>)` / `numpy` seed). This is a determinism requirement for the *test harness only* — it does **not** manufacture simulator seed control (`sim/capabilities.json: seed_controlled=false` is unchanged; T5 forbids fake-seed injection). Real-run reproducibility stays `mode=unseeded` / distribution-stable + audit-trail per `docs/claim-ceiling.md:42-52`.

---

## 14. Implementation branch / commit guidance

For a future `/implement sprint-02` **once a build gate is open**:

- **Recommended branch:** `cycle-001-sprint-02-delta-explanation`
- **Recommended implementation commit message:** `feat: implement TurnTrace Sprint 02 explanation loop`

> **No branch creation, code editing, implementation commit, or push is authorized by this Sprint Plan.** Those require a later explicit operator build-gate prompt. This Sprint Plan creates only the planning artifact and reports status.

Integration posture (from Sprint 01 precedent, `cycle-001-sprint-01/closeout.md`): fast-forward only, no merge commit, no squash, no tag, no version bump — confirmed at operator closeout, not by this plan.

---

## 15. Build-gate statement

```
This Sprint Plan opens no build gate.
Implementation requires a later explicit operator OA-2 / build-gate action.
Broad optimization remains closed.
Runtime agent changes remain forbidden.
Claim ceiling remains Rung 1.
```

The single hard procedural gate is OA-2 (`docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` §3; loop contract §6). `/implement sprint-02` may run only after the operator explicitly opens the Sprint 02 build gate. Until then, only planning proceeds. T2–T5 (App-Zone code) and the docs tasks T1/T6 are written **only inside `/implement`** once the gate is open — this plan authorizes none of them to be written now.

---

## 16. Recommendation

**Sprint Plan is ready for operator acceptance**, scoped to **T1, T2, T3, T4, T6 as Core**, **T7 (E2E goal validation) as Core/P0**, and **T5 as Stretch** (per OD-1). Every task is confined to the analysis/offline and provenance/docs layers; every open question from the PRD is resolved in the SDD (OQ-1..OQ-5) or carried as a clearly-scoped operator decision (DQ-1, DQ-2) with a recommended default here.

**Do NOT begin implementation.** This Sprint Plan opens no build gate. After operator acceptance, the next step is one of:

1. **commit the Sprint Plan** (planning artifact lands on `main`), or
2. the operator later opens an explicit build gate with **`/implement sprint-02`** (OA-2).

Neither is performed by this Sprint Plan. It creates the artifact and reports status only.

> **Sources:** `docs/cycles/cycle-001-sprint-02/02-sprint-02-sdd.md` (binding input); `docs/cycles/cycle-001-sprint-02/01-sprint-02-prd.md`; `docs/cycles/cycle-001-sprint-02/00-research-and-planning.md`; `docs/operator/deferred-lane-gate-after-sprint-01.md` (L37-97); `docs/operator/turntrace-loop-contract.md` (§1-§3, §6-§10); `docs/claim-ceiling.md` (L5-7, L29-35, L42-64); `docs/cycles/cycle-001-sprint-01/closeout.md` (L1-95); `docs/ledger.md` (L9-12); `docs/failure-modes.md` (L5-101); `docs/strategy-report.md` (L10-68); `analysis/delta_report.py` (L41-43, L73-78, L109, L156-170); `analysis/replay_check.py` (L69-133); `eval/run_eval.py` (L91-103, L260-338); `eval/hygiene_check.py` (L34-95); `tests/test_import_direction.py` (L24-79); `tests/test_smokes.py`; `sim/capabilities.json`; `frozen/metrics/metrics-spec-v001.json`.
