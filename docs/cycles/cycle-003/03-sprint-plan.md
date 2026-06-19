# Cycle-003 Sprint Plan — Rung-2 Admission Readiness: Tracked Evidence Summary + Ledger Plumbing

> Planning artifact (Sprint Plan). Status: **DRAFT — research/planning only.** This document opens **NO build gate**
> and is **NOT an implementation authorization.** It plans the *design/spec* deliverables of Cycle-003; it builds
> nothing and creates no `/implement` prompt.
> Implementation of any specified artifact (schema file, generator/validator code, finalized ledger-row convention)
> is **out of Cycle-003** and requires a **separate, explicit operator build-gate action (OA-2 equivalent)** per
> `docs/operator/turntrace-loop-contract.md` §6, landing only through `/architect → /sprint-plan → /implement →
> /review-sprint → /audit-sprint → operator acceptance` in a later cycle.
> Binding inputs: `docs/cycles/cycle-003/01-prd.md` (accepted-for-architecture PRD) and `docs/cycles/cycle-003/02-sdd.md`
> (reviewed SDD). The SDD resolved artifact placement (OD-C3-4, SDD §3) and the A→B→C/D/E design spine (SDD §1.2).
> Sanitized note. No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs, `deck.csv` rows,
> run-dir dumps, Pokémon Elements, or Competition Data appear here (CC-1/CC-2, ESP). **No dispersion metric values
> appear here** — local evidence is referenced qualitatively only and its values stay local/gitignored. Runs are
> referenced by `run_id`, hashes, sanitized metric *names*, claim ceilings, and local path/status only. The forbidden
> agent claim words (*strong / competitive / optimal / calibrated / complete*) appear only as negated/forbidden language.

| Field | Value |
|---|---|
| **Cycle** | Cycle-003 |
| **Working title** | Rung-2 Admission Readiness: Tracked Evidence Summary + Ledger Plumbing |
| **Type** | Sprint Plan (planning artifact, not a build artifact) |
| **Status** | DRAFT — awaiting operator acceptance; next Golden-Path step is **operator acceptance/commit of the plan**, not implementation |
| **Date** | 2026-06-19 |
| **Current main** | `3014c07` — *docs: add TurnTrace Cycle-003 SDD* |
| **Binding inputs** | `docs/cycles/cycle-003/01-prd.md`; `docs/cycles/cycle-003/02-sdd.md` |
| **Posture** | Plan the design/spec deliverables of the Rung-2 admission **plumbing**, **not** the admission, **not** the build |
| **Claim ceiling** | Rung 1 (held for the whole cycle; not raised) |
| **Shape** | **1 sprint** (docs-only, all Core, **no OA-2 build gate**) — the smallest safe structure the PRD/SDD admit |

## 1. Sprint-cycle objective

Translate the accepted PRD (C3-FR-1…C3-FR-5) and the reviewed SDD into an **operator-acceptable set of tracked
planning/design documents** that convert the remaining Rung-2 gap into a **single, pre-specified future operator
decision** — while holding the ceiling at **Rung 1**, promoting **no values**, writing **no ledger row**, and building
**no artifact or code** (`01-prd.md:84-90`; `02-sdd.md:31-50`).

The bright line governs the whole cycle, restated from the SDD (`02-sdd.md:42-45`): **Cycle-002 produced the larger-`n`
data and the descriptive-dispersion *machinery*; Cycle-003 specifies/designs the *tracked sanitized evidence-summary
schema*, the *Rung-2 ledger-row + verdict convention*, and the *OD-6/criterion-2 resolution proposal* — so a future
Rung-2 admission becomes a single pre-specified operator decision — and Cycle-003 stops short of that decision.**

## 2. Why one sprint (the smallest safe structure)

The SDD establishes that **the entire Cycle-003 deliverable surface is tracked design/spec documents** — the net-new
*code* (the generator/validator and the machine-readable schema file) is **explicitly deferred to a separate later
build cycle** (`02-sdd.md:64-68`, `02-sdd.md:482-489`). Within Cycle-003 there is therefore **no build-gated work to
sequence**: every lane lands as a sanitized tracked doc under `docs/cycles/cycle-003/` (or as a section of those docs),
all in the same zone, all under the same docs-cadence, none touching `frozen/`, `analysis/`, `eval/`, `runs/`, or
`docs/ledger.md`.

- **One docs-only sprint is the right size.** Five design/spec deliverables (C3-FR-1…C3-FR-5), all Core, all tracked
  docs, no code, no build gate → a single MEDIUM sprint of 6 tasks (5 deliverable tasks + 1 end-to-end goal-validation
  sweep). This is within the SMALL/MEDIUM/LARGE sizing rule (`planning-sprints` constraints: MEDIUM = 4–6 tasks).
- **Multiple sprints would be artificial.** Cycle-002 used three sprints because it had a **docs lane plus two
  build-gated lanes** with a real D→A→C/B ordering and an OA-2 firebreak (`docs/cycles/cycle-002/03-sprint-plan.md`
  §3). Cycle-003 has **no build lane at all** — splitting five co-located docs across sprints would invent ordering
  that the design does not require and would imply build phases that this cycle explicitly forbids (NG5;
  `02-sdd.md:151`).
- **The procedural firebreak is the cycle boundary itself.** The build (schema file + `analysis/evidence_summary.py` +
  tests) is a *different cycle* behind a fresh operator build-gate (OA-2 equivalent), not a later sprint of this one
  (`02-sdd.md:485`, OD-C3-6). Cycle-003 closes at "specs accepted"; it does not roll forward into implementation.

| Lane (PRD/SDD) | Task | C3-FR | Deliverable (tracked design/spec doc) | Net-new code? |
|---|---|---|---|---|
| **A** — evidence-summary schema | S00-T1 | C3-FR-1 | `04-evidence-summary-schema-spec.md` (safe/forbidden fields; JSON-first) | **None** (spec only; schema FILE is later) |
| **B** — generator/validator shape | S00-T2 | C3-FR-2 | `05-generator-validator-shape.md` (inputs/outputs/import boundary/refusals/exit codes/hygiene parity) | **None** (shape spec only; CODE is later) |
| **C** — Rung-2 ledger-row + verdict convention | S00-T3 | C3-FR-3 | `06-rung-2-ledger-convention.md` (columns/semantics/verdict rule; **no row written**) | **None** |
| **D** — OD-6 / criterion-2 resolution proposal | S00-T4 | C3-FR-4 | `07-od6-criterion-2-proposal.md` (disjoint-bands shape; `M` unset; OD-6 unrelaxed) | **None** |
| **E** — FunSearch forward-compat appendix | S00-T5 | C3-FR-5 | `08-funsearch-forward-compat.md` (notes-only) | **None** |
| (validation) | S00-T6 | all goals | `sprint-00-implementation-report.md` (E2E goal sweep) | **None** |

**The entire net-new surface of Cycle-003 is tracked documents.** Everything references existing, unchanged repo
mechanics (`analysis/dispersion_report.py`, `analysis/aggregate.py`, `eval/hygiene_check.py`, `eval/schemas.md`,
`docs/ledger.md`) by file:line; nothing is built or promoted.

## 3. Posture and gates (binding)

```
This Sprint Plan opens no build gate.
Cycle-003 builds nothing: no schema file, no generator/validator code, no tracked metric summary, no ledger row.
Implementation of the specified artifacts is OUT OF Cycle-003 and requires a separate later operator OA-2 / build gate.
Cycle-003 specifies/designs Rung-2 admission readiness PLUMBING. It is NOT a Rung-2 admission.
The runtime-agent improvement lane remains closed; broad optimization remains closed.
The claim ceiling remains Rung 1 until a separate explicit later operator decision earns otherwise.
```

- **Specify/design the plumbing, not the admission, not the build.** No artifact asserts a "beats random-legal" verdict;
  no task advances the claim ceiling; no task builds a schema file or generator/validator code (NG1, NG2, NG5;
  `02-sdd.md:148-151`).
- **`docs/ledger.md` is not touched.** No `run-v002` / Rung-2 row is written; the ledger remains the **only
  ceiling-bearing artifact** at its two Rung-1 `regime-v001` rows (NG3; `docs/ledger.md:9-12`; `02-sdd.md:343-348`).
- **No SP-6 / no live-value promotion.** Only the *schema* (the safe shape) is specified; dispersion **values** stay
  local/gitignored. Issuing SP-6 to promote values is a separate later operator decision (NG4; `02-sdd.md:392`,
  `02-sdd.md:410-413`).
- **OD-6 stays unrelaxed; no numeric margin `M`.** The disjoint-bands rule is proposed *in shape* with `M` left unset;
  no inferential statistic is computed or reported (NG6; `02-sdd.md:372-381`).
- **Build gate (OA-2) is a future-cycle gate, not a Cycle-003 sprint gate.** This Sprint Plan never opens it
  (loop contract §6; `02-sdd.md:485`, OD-C3-6).

### 3.1 Docs-only cadence (no OA-2)

Sprint 00 is **docs-only** and opens **no OA-2 build gate** — but it still runs the **normal Loa sprint cadence** for
quality: `/implement → /review-sprint → /audit-sprint → explicit operator acceptance/closeout`. Its deliverables are
sanitized **tracked docs only** (no app code, no `frozen/` files, no `analysis/`/`eval/` code, no runs, no ledger
change), so no OA-2 is required; the cadence runs because prior cycles' review caught sensitive/token issues before
task completion (precedent: `docs/cycles/cycle-002/03-sprint-plan.md` §2.1). Review/audit MUST verify the docs-only
gate checks of §11.

> **Process note (carried from cycle-002).** `/review-sprint` and `/audit-sprint` are **pure-review skills**:
> `Write`/`Edit` disabled inside them is **expected, not a failure**. Review/audit artifacts and the COMPLETED marker
> are persisted by the orchestrator into **gitignored** `grimoires/loa/a2a/...` after the skill returns — never tracked,
> never by `/implement`. The COMPLETED marker is created only after explicit operator closeout authorization.

## 4. Core vs Stretch

- **Core (all six tasks):** evidence-summary schema spec (S00-T1) · generator/validator shape spec (S00-T2) · Rung-2
  ledger-row + verdict convention (S00-T3) · OD-6/criterion-2 proposal (S00-T4) · FunSearch forward-compat appendix
  (S00-T5) · end-to-end goal-validation sweep + sprint report (S00-T6).
- **Stretch:** **none.** Every deliverable is a required PRD FR (C3-FR-1…C3-FR-5) and is Core. Deliberately no Stretch
  lane — adding speculative scope to a spec-only cycle is exactly the scope-creep the PRD forbids (R2/R4; NG12).

## 5. Defaults carried from the SDD (ratified inputs)

All resolved in the PRD/SDD and carried verbatim into this plan:

| Default | Value | Source |
|---|---|---|
| Allowed descriptive vocabulary | `count, min, max, range, mean, median, spread` only | `02-sdd.md:196`; `01-prd.md:181-182` |
| Std-dev / variance / inferential | **Forbidden** (OD-6 unrelaxed) — no CIs, p-values, "significance", hypothesis tests, inferential error bars | `02-sdd.md:219`; `01-prd.md:153-154` |
| Dispersed metrics (names only) | `win_rate, illegal_action_rate, timeout_rate, error_rate, avg_turns, avg_wall_clock_ms` (the last reported, never a comparison metric) | `02-sdd.md:203-206` |
| Schema spec placement | `docs/cycles/cycle-003/` (tracked field-list design authority, same class as `eval/schemas.md`) | `02-sdd.md:169` (OD-C3-4 resolved) |
| Machine-readable schema **file** | App-Zone, paired with the validator under `analysis/` — **created only in the later build cycle** | `02-sdd.md:170` |
| Generator/validator **code** | `analysis/` (e.g. `analysis/evidence_summary.py`), stdlib-only, single-regime guard, no sidecar reads — **created only in the later build cycle** | `02-sdd.md:171`, §5–§6 |
| Read surface | `manifest.json` + `match_results/*` only; **never** the per-decision sidecars | `02-sdd.md:225-229` |
| Import boundary (future code) | `analysis/`-class — no `cabt`, `sim/`, `agents/runtime/`, or `eval/` import | `02-sdd.md:255-256` |
| Exit-code discipline (future code) | `0` clean · `1` input failure · `2` mixed-regime refusal · non-zero on forbidden-field leak | `02-sdd.md:298-303` |
| Verdict rule | same-regime, agent-only, carrying a ceiling + `n`, **never** cross-regime | `02-sdd.md:326-330`; `docs/ledger.md:5-8` |
| Numeric margin `M` | **Unset** — fixed before the numbers are read, at the later admission gate | `02-sdd.md:380-381` (NG6) |
| Reproducibility posture | `mode=unseeded`; distribution-stable + audit-trail; unseeded caveat travels with every summary | `02-sdd.md:199-200`; `01-prd.md:248-250` |
| Ledger | `docs/ledger.md` unchanged; no row written; only ceiling-bearing artifact | `02-sdd.md:343-348` (NG3) |
| Values | All dispersion values stay local/gitignored; SP-6 deferred | `02-sdd.md:410-413` (NG4) |

## 6. Sprint 00 — Rung-2 Admission Readiness Specs (docs-only, NO build gate)

**Posture:** docs-only; opens **no OA-2 build gate**; touches **tracked docs only** (no app code, no `frozen/` files, no
`analysis/`/`eval/` code, no run dirs, no ledger changes, no build-gated paths). Runs the normal Loa sprint cadence —
`/implement → /review-sprint → /audit-sprint → explicit operator acceptance/closeout` — for quality, not because BUILD
work is authorized. Single sprint; tasks may be authored in any order except S00-T6 (the closing sweep) which runs last.

| Task | C3-FR / Lane | Title | Output (tracked) |
|---|---|---|---|
| **S00-T1** | C3-FR-1 / A | Evidence-summary schema spec (safe + forbidden field sets; JSON-first) | `docs/cycles/cycle-003/04-evidence-summary-schema-spec.md` |
| **S00-T2** | C3-FR-2 / B | Generator/validator **shape** spec (inputs, outputs, import boundary, refusals, exit codes, hygiene parity) | `docs/cycles/cycle-003/05-generator-validator-shape.md` |
| **S00-T3** | C3-FR-3 / C | Rung-2 ledger-row + verdict **convention** (format/spec only; **no row written**) | `docs/cycles/cycle-003/06-rung-2-ledger-convention.md` |
| **S00-T4** | C3-FR-4 / D | OD-6 / criterion-2 resolution **proposal** (disjoint-bands shape; `M` unset; OD-6 unrelaxed) | `docs/cycles/cycle-003/07-od6-criterion-2-proposal.md` |
| **S00-T5** | C3-FR-5 / E | FunSearch forward-compatibility appendix (notes-only) | `docs/cycles/cycle-003/08-funsearch-forward-compat.md` |
| **S00-T6** | all goals | End-to-end goal-validation sweep + sprint report | `docs/cycles/cycle-003/sprint-00-implementation-report.md` |

### S00-T1 — Evidence-summary schema spec (Core, docs) → **[G1]**
Author a tracked **field-list design authority** for the sanitized K-batch evidence summary, mirroring the
`eval/schemas.md` precedent (a plain spec that the future validator must agree with; `02-sdd.md:163-165`). It MUST
enumerate, per SDD §4:
- **Safe fields** (exactly the descriptive surface already produced by `analysis/dispersion_report.py` plus
  identity/provenance — **no new metric, no new statistic**, `02-sdd.md:186-202`): `regime_id`, `n`, `K`,
  `agent_id`/`agent_version`, the seven descriptive statistics (`count`, `min`, `max`, `range`, `mean`, `median`,
  `spread`) per metric, the `run_id` list, per-run/batch content `hashes`, `mode=unseeded`, the unseeded-process caveat
  string, and a Rung-1 footer (the summary "carries no ceiling of its own").
- **Forbidden fields** (enumerated and intended for mechanical validator enforcement, not mere documentation,
  `02-sdd.md:208-221`): raw decision rows / trace bodies; Competition Data (card IDs/names, deck lists, hand contents,
  simulator logs); file-form Competition Data (PDFs/CSVs, `deck.csv` rows, run-dir dumps); Pokémon Elements; inferential
  statistics (`std-dev`, `variance`, CIs, p-values, "significance", hypothesis tests, inferential error bars — OD-6);
  cross-regime fields/comparisons (NFR-5); affirmative forbidden agent words.
- **JSON-first** (`02-sdd.md:231-239`): the machine-readable form is primary; any human rendering is derived. Note this
  is an existing-pattern choice (`dispersion_report.py` `render_json` vs `render`), **not** a FunSearch coupling.
- **Sanitization parity** with `eval/hygiene_check.py` and the `dispersion_report.py` read surface (manifest +
  `match_results/*` only; never the decision sidecars; `02-sdd.md:225-229`).

**Specifies the schema; creates no schema FILE and promotes no values** (`01-prd.md:189`; NG4/NG5).

### S00-T2 — Generator/validator shape spec (Core, docs) → **[G2]**
Author a tracked spec describing the **shape** (not the code) of the future offline `analysis/`-class generator + its
validator, per SDD §5–§6. It MUST specify:
- **Generator** (`02-sdd.md:243-267`): reads existing local sealed run dirs (`manifest.json` + `match_results/*` via
  `aggregate.aggregate_run`) and the local dispersion output; emits a schema-conforming (S00-T1) sanitized JSON summary;
  **never opens** the per-decision sidecars (structural); writes to a **local path by default** (promotion is a separate
  SP-6 decision, never a side effect); reuses the existing descriptive-stat helpers rather than recomputing.
- **Validator** (`02-sdd.md:269-311`): an **allow-list, fail-closed** barrier rejecting any field outside the S00-T1
  safe set, any inferential statistic name/value, any Competition-Data/Pokémon-Element token, any cross-regime field,
  and any affirmative forbidden agent word — reaching **sanitization parity with `eval/hygiene_check.py`** plus the
  value/inferential/cross-regime/forbidden-word checks a path-based gate cannot express (superset parity).
- **Import boundary** (`02-sdd.md:255-256`): `analysis/`-class — no `cabt`, `sim/`, `agents/runtime/`, or `eval/`
  import; stdlib-only (the SDD finds no justification to deviate; any dependency is a separate operator decision).
- **Single-regime guard** (`02-sdd.md:285-292`): hard-refuse mixed `regime_id` → **exit 2**, mirroring
  `dispersion_report.py`'s `MixedRegimeRefusal` / `delta_report.py`'s `CrossRegimeRefusal`; `regime_id` authority is each
  run dir's `manifest.json`, read first.
- **Exit-code contract** (`02-sdd.md:298-303`): `0` clean · `1` input failure · `2` mixed-regime refusal · non-zero,
  fail-closed on a forbidden-field leak (the exact leak code is fixed by the later build cycle; the contract is "never
  exit 0 on a leak").

**Specifies the shape; builds no code** (`01-prd.md:199`; NG5).

### S00-T3 — Rung-2 ledger-row + verdict convention (Core, docs) → **[G3]**
Author a tracked **format/spec** convention doc (same class as `06-ledger-report-discipline.md`), per SDD §7. It MUST
specify:
- **Row schema** (`02-sdd.md:316-322`): a future deliverable Rung-2 row follows the **existing append-only ledger
  schema verbatim, adding no column** (`docs/ledger.md:9`): `date`, `run_id`, `regime_id`, `git_rev`, `sim_version`,
  `agent_version`, `opponent_pool_ref`, `seed_set_ref`, `games`/`n`, `win_rate`, `illegal_action_rate`, `timeout_rate`,
  `error_rate`, `avg_turns`, `mode`, `hypothesis`, `claim_ceiling`, `notes`. The `claim_ceiling` field is where a Rung-2
  ceiling would one day be recorded — by a separate operator decision, never by this cycle.
- **Verdict rule** (`02-sdd.md:324-330`): a `verdict` of better/worse is written **only** for a same-regime, agent-only
  comparison carrying a ceiling and an `n`, and **never** across regimes (NFR-5; the existing `run-0002` vs `run-0001`
  row demonstrates the Rung-1 shape, `docs/ledger.md:12`).
- **Separation of concerns** (`02-sdd.md:331-341`, the architectural heart of Lane C): the **ledger row is the only
  future ceiling-bearing verdict artifact**; the **evidence summary (S00-T1) is supporting confidence evidence only**
  (no ceiling of its own); the convention specifies how a future row would **cite a promoted evidence summary by
  reference + hash without embedding raw content**.

**No row is written; `docs/ledger.md` is unchanged** (`02-sdd.md:343-348`; NG3). The convention doc cross-references
`docs/ledger.md` but does not edit it.

### S00-T4 — OD-6 / criterion-2 resolution proposal (Core, docs) → **[G4]**
Author a tracked proposal resolving the criterion-2 ↔ OD-6 tension, per SDD §8. It MUST:
- **State the tension** (`02-sdd.md:352-356`): Rung-2 criterion 2 requires an *inferential* procedure; OD-6 *forbids*
  inferential statistics; they cannot both hold unchanged.
- **Recommend the pre-registered descriptive disjoint-bands rule** (`02-sdd.md:358-370`), of the shape *"candidate
  `min` > baseline `max` by ≥ M across K ≥ 20 same-regime batches"*, expressed using only the allowed descriptive
  vocabulary (no `std-dev`/`variance`, no inferential statistic). Note the quantities (`candidate min`, `baseline max`,
  `K`) are already in the S00-T1 safe set, so the procedure consumes the schema with **no new field**. This satisfies
  criterion 3's *pre-registered margin* and reinterprets criterion 2's spirit (pre-registered, operator-approved, not
  chosen after the fact) **without crossing OD-6**.
- **Specify the pre-registration procedure in shape** (`02-sdd.md:378-381`): the rule and its margin `M` are fixed
  **before** the comparison numbers are read; the proposal specifies the *procedure* and **does not choose `M`** (NG6).
- **Keep OD-6 unrelaxed and present the alternative, not recommend it** (`02-sdd.md:372-376`): relaxing OD-6 for a
  genuine inferential test is presented as the alternative, not decided here.
- **Name the later operator seam** (`02-sdd.md:384-398`): the four conjunctive, governance/design (not data) decisions —
  (8a) disjoint-bands vs OD-6 relaxation, (8b) numeric `M`, (8c) SP-6 live-value promotion, (8d) Rung-2 ledger row /
  ceiling advance — are a single later seam, **none in Cycle-003**.

**A proposal that resolves criteria 2 and 3 *in shape*; it decides nothing, chooses no `M`, and produces no inferential
result** (`01-prd.md:213-222`; NG6).

### S00-T5 — FunSearch forward-compatibility appendix (Core, docs) → **[G5]**
Author a tracked **notes-only** appendix, per SDD §10. It MUST state that TurnTrace should remain a clean
**scalar-per-candidate, regime-stamped** evaluator; that the S00-T1 schema should stay **JSON-first / machine-readable**
to avoid blocking a future automated consumer (a forward-compat property, not a FunSearch coupling); and that a future
candidate-search loop would require a **runtime-agent heuristic surface first (currently closed)** and an evaluator that
**averages over enough matches/batches to clear the unseeded RNG noise floor** (`05-reproducibility-reality.md` §3).
Cycle-003 adds **no** FunSearch dependency, interface, scaffold, integration, or heuristic surface (NG10;
`02-sdd.md:419-431`).

### S00-T6 — End-to-end goal-validation sweep + sprint report (Core, docs) → **[all goals]**
After S00-T1…T5 land, sweep the cycle's goals (G1–G6) and acceptance criteria and record evidence in the tracked
**sprint-scoped** report `docs/cycles/cycle-003/sprint-00-implementation-report.md` (no generic
`implementation-report.md`, no overwrite-prone generic path). No new code. No goal marked achieved without a file:line
citation to the produced doc. MUST re-verify: Rung 1 held; `docs/ledger.md` byte-unchanged; no value promoted; no schema
file or code created; OD-6 unrelaxed and `M` unset; hygiene clean on every produced doc; no cross-regime comparison
anywhere; the design-level later-build acceptance matrix (SDD §12) recorded as **planning-only** (no test/code written
now).

**Sprint 00 acceptance:** see §11.

## 7. Goal traceability (Appendix C)

PRD goals (`01-prd.md:125-141`, IDs present as G1–G6) → contributing tasks:

| Goal | Statement (abridged) | Contributing task(s) |
|---|---|---|
| **G1** | Tracked evidence-summary schema is specified (safe + forbidden fields) | S00-T1 |
| **G2** | Generator/validator shape is specified | S00-T2 |
| **G3** | Rung-2 ledger-row + verdict convention is specified (no row written) | S00-T3 |
| **G4** | OD-6 / criterion-2 resolution proposal authored (disjoint-bands; `M` deferred) | S00-T4 |
| **G5** | FunSearch forward-compatibility appendix provided (notes-only) | S00-T5 |
| **G6** | Rung 1 held; ledger untouched; no values promoted | **All tasks** (cross-cutting); re-verified by S00-T6 |

- Every goal has at least one contributing task — **no orphan goals.**
- **E2E validation task present:** S00-T6 is the final-sprint end-to-end goal-validation sweep (P0, must complete).
  Because Cycle-003 is spec-only, the E2E sweep validates **doc deliverables and boundary preservation**, not running
  code (the runnable later-build checks land only inside a future `/implement`, SDD §12).

## 8. Task ordering / dependency graph

```
Sprint 00 (docs-only, NO build gate) — single sprint, lands on operator acceptance
   S00-T1 (schema spec, A) ───┐
   S00-T2 (gen/val shape, B) ─┤  (T2 references T1's safe/forbidden field sets)
   S00-T3 (ledger convention, C) ─┤  (T3 references T1: row CITES summary, separation of concerns)
   S00-T4 (OD-6 proposal, D) ─┤  (T4 consumes T1's min/max/K — no new field)
   S00-T5 (FunSearch appendix, E) ─┘  (T5 references T1's JSON-first property)
        │  all five design/spec docs authored
        ▼
   S00-T6 (E2E goal sweep + sprint report) ── LAST
```

- **S00-T1 is the natural anchor** — T2 (validator allow-list), T3 (row-cites-summary), T4 (consumes `min`/`max`/`K`),
  and T5 (JSON-first) all reference the schema's field sets. Authoring T1 first reduces rework, but all five are
  co-located tracked docs and may be authored in any order; **only S00-T6 is strictly last** (it sweeps the others).
- **No build-gated dependency exists** — there is no `frozen/` authoring, no batch run, no `analysis/` code to sequence.
- **No `agents/runtime/` change, no eval run, no value promotion** appears anywhere in the graph.

## 9. File authorization matrix

**Authorized for a future docs-cadence `/implement` ONLY (per task; no other path may be touched):**

| Path | Task | Action | Zone |
|---|---|---|---|
| `docs/cycles/cycle-003/04-evidence-summary-schema-spec.md` | S00-T1 | create | docs (tracked) |
| `docs/cycles/cycle-003/05-generator-validator-shape.md` | S00-T2 | create | docs (tracked) |
| `docs/cycles/cycle-003/06-rung-2-ledger-convention.md` | S00-T3 | create | docs (tracked) |
| `docs/cycles/cycle-003/07-od6-criterion-2-proposal.md` | S00-T4 | create | docs (tracked) |
| `docs/cycles/cycle-003/08-funsearch-forward-compat.md` | S00-T5 | create | docs (tracked) |
| `docs/cycles/cycle-003/sprint-00-implementation-report.md` | S00-T6 / closeout | create | docs (tracked) |

> The exact filenames above follow the SDD's placement (`02-sdd.md:169-174`) and the `docs/cycles/cycle-00N/NN-*.md`
> numbering precedent (PRD = `01-`, SDD = `02-`, this plan = `03-`). The implementer MAY consolidate D (S00-T4) and E
> (S00-T5) as sections rather than separate files **only if** the operator prefers it (SDD §3 allows the proposal/appendix
> to live as SDD sections); the default here is one file per lane for traceability. No other consolidation is authorized.

**Explicitly FORBIDDEN to touch (any task) — the hard exclusions:**

| Path | Why |
|---|---|
| `docs/ledger.md` | **No row written; byte-unchanged.** No `run-v002` / Rung-2 row. The only ceiling-bearing artifact (NG3; `02-sdd.md:343-348`). |
| `frozen/regimes/regime-v00{1,2}.json` + their components; `frozen/seeds/seed-set-v00{1,2}.json` | **Never edited; never compared across regimes** (NG11; `02-sdd.md:155`). Cycle-003 authors no `frozen/` file. |
| `analysis/evidence_summary.py` (and any new `analysis/` code) | The generator/validator **CODE is a later build cycle**, not Cycle-003 (NG5; `02-sdd.md:171`, §5–§6). Cycle-003 specifies its *shape* only. |
| `analysis/evidence_summary_schema.json` (or any machine-readable schema FILE) | The schema **FILE is a later build cycle** (NG5; `02-sdd.md:170`). Cycle-003 specifies the *field-list* only. |
| `analysis/dispersion_report.py`, `analysis/aggregate.py`, `analysis/delta_report.py`, `analysis/failure_report.py`, `analysis/replay_check.py`, `analysis/e2e_validate.py`, `eval/*` | Reused **unchanged** as design references; no edit designed in Cycle-003. |
| `agents/runtime/` | **No runtime-agent work** (NG7); lane closed; agents frozen. |
| `runs/` | No eval run; no run dir authored or read into a tracked artifact. Live evidence stays local/gitignored (ESP-1). |
| local dispersion outputs / dispersion VALUES | **No live-value promotion** (NG4; `02-sdd.md:410-413`). Values stay local/gitignored; SP-6 not issued. |
| `cg/`, `deck.csv`, `grimoires/loa/context/` | Competition Data — never committed/read into tracked artifacts (CC-1/CC-2). |
| `grimoires/loa/a2a/` | Review/audit/COMPLETED markers persist here (gitignored), orchestrator-written after the pure-review skills return — never tracked, never by `/implement`. |
| `grimoires/loa/NOTES.md`, `grimoires/loa/ledger.json`, `.beads/` | **State Zone — kept OUT of tracked docs commits** unless explicitly authorized; `.beads/issues.jsonl` stays unstaged (OD-9; operator constraint; `02-sdd.md:176`). |
| `.claude/` | **System Zone — never read, suggested, or edited** (zone-system rule; operator constraint; `02-sdd.md:178-180`). |

**Implementation-report path rule (binding).** The sprint's implementation report uses the explicit **sprint-scoped,
cycle-scoped** tracked path `docs/cycles/cycle-003/sprint-00-implementation-report.md`. **No generic
`implementation-report.md`** and no overwrite-prone generic path. Review/audit artifacts and the COMPLETED marker live
**only** in gitignored `grimoires/loa/a2a/...` and are never tracked; the COMPLETED marker is created only after explicit
operator closeout authorization.

## 10. The designed-now → later-build handoff (explicit, binding)

This Sprint Plan plans **only the "designed now" row** of the SDD's admission chain (`02-sdd.md:468-489`). The full chain,
with each step's Cycle-003 status:

```
sanitized evidence-summary SCHEMA SPEC     ← PLANNED & AUTHORED THIS CYCLE (S00-T1, tracked spec doc only)
generator/validator SHAPE SPEC             ← PLANNED & AUTHORED THIS CYCLE (S00-T2, tracked spec doc only)
Rung-2 ledger-row + verdict CONVENTION     ← PLANNED & AUTHORED THIS CYCLE (S00-T3, tracked spec doc only)
OD-6 / criterion-2 PROPOSAL (shape)        ← PLANNED & AUTHORED THIS CYCLE (S00-T4, M unset, OD-6 unrelaxed)
FunSearch forward-compat APPENDIX          ← PLANNED & AUTHORED THIS CYCLE (S00-T5, notes-only)
  → schema FILE + generator/validator CODE ← LATER, separate /implement under a fresh OA-2 (OD-C3-6)
    → generated/validated summary          ← LATER (built under OA-2, B)
      → promoted evidence summary           ← LATER, separate SP-6 operator decision (8c)
        → Rung-2 ledger ROW                 ← LATER, separate Rung-2 admission gate (8d)
          → Rung-2 admission DECISION        ← LATER, operator; NEVER in Cycle-003
```

| Phase | Status in Cycle-003 |
|---|---|
| Five design/spec docs (S00-T1…T5) | **Authored this cycle** (tracked docs only — no file, no code, no row, no value) |
| Schema FILE + generator/validator CODE | **Later** — separate `/implement` under a fresh OA-2 (OD-C3-6) in a future cycle |
| Live-value promotion (SP-6) | **Later** — separate operator decision (NG4) |
| Numeric margin `M`; disjoint-bands vs OD-6-relaxation choice | **Later** — operator at the admission gate (NG6) |
| Rung-2 ledger row + claim-ceiling advance + Rung-2 admission | **Later** — separate Rung-2 admission gate (NG1–NG3) |
| K=50 confidence top-up / S02-T4 paired-delta tooling / new eval runs | **Out of scope** — future option only (NG12; `02-sdd.md:489`) |

**Rung 1 remains held. `docs/ledger.md` is unchanged. No value is promoted. No build gate is opened by this Sprint Plan.**

## 11. Acceptance criteria

All bounded to Rung 1; all forbid agent strengthening; all forbid cross-regime comparison and inferential statistics.
These are **planning-cycle** acceptance criteria for the docs deliverables (`01-prd.md:338-345`). The **later build-cycle**
acceptance criteria (AC-1…AC-7, `01-prd.md:347-363`) and the SDD's design-level check matrix (SDD §12) apply only when the
specified artifacts are later built under a fresh OA-2 — **no test or code is written now**.

| AC | Theme | Task | Validation | Stop condition |
|---|---|---|---|---|
| **AC-S00-1** | Schema completeness | S00-T1 | The schema spec enumerates the full safe set (the 7 descriptive stats + identity/provenance) AND the full forbidden set (raw/Competition-Data/Pokémon/inferential/cross-regime/forbidden-words); JSON-first stated; read-surface + hygiene parity stated; **no schema FILE created** | A safe or forbidden class is missing, the doc creates a `.json` schema file, or it promotes a value → HALT |
| **AC-S00-2** | Generator/validator shape | S00-T2 | The shape spec states inputs (sealed run dirs + dispersion output), JSON output, the `analysis/`-class import boundary, stdlib-only, single-regime guard (exit 2), the exit-code contract, allow-list/fail-closed validation, and superset hygiene parity; **no code written** | The doc omits the import boundary / single-regime guard / fail-closed rule, or writes any `analysis/` code → HALT |
| **AC-S00-3** | Ledger convention | S00-T3 | The convention states the existing ledger columns verbatim (adds none), the same-regime agent-only verdict rule, the row-vs-summary separation of concerns, and row-cites-summary-by-ref+hash; **`docs/ledger.md` byte-unchanged; no row written** | The doc adds a ledger column, writes a row, edits `docs/ledger.md`, or permits a cross-regime verdict → HALT |
| **AC-S00-4** | OD-6 proposal honesty | S00-T4 | Disjoint-bands recommended (shape only, allowed vocabulary); OD-6-relaxation presented as alternative, **not decided**; pre-registration procedure specified; **`M` unset**; **no inferential statistic** computed or reported; the later operator seam named | The proposal decides the resolution, chooses `M`, relaxes OD-6, or reports an inferential result → HALT |
| **AC-S00-5** | FunSearch notes-only | S00-T5 | Appendix is notes-only: scalar-per-candidate / regime-stamped / JSON-first / heuristic-surface-first-and-closed / noise-floor; **no dependency, interface, scaffold, integration, or heuristic surface added** | The appendix adds a FunSearch dependency/scaffold/interface or any runtime-agent surface → HALT |
| **AC-S00-6** | Goals met | S00-T6 | The sprint report records a file:line citation of evidence for every goal G1–G6; Rung-1 re-verified; `docs/ledger.md` byte-unchanged; no value promoted; no schema file/code created; OD-6 unrelaxed and `M` unset; hygiene clean | A goal is marked achieved without evidence, or a claim exceeds Rung 1, or any boundary above is crossed → HALT |
| **AC-S00-7** | Docs hygiene | all S00 | `eval/hygiene_check.py` passes on each produced doc; forbidden agent words appear only as negated/forbidden language; no app code / `frozen/` / run dir / ledger change; no Competition-Data or Pokémon-Element token | Any Competition-Data/Pokémon token, forbidden affirmative claim word, or non-docs change → HALT |

### Cross-cutting (the hard exclusions, as ACs)

| AC | Theme | Validation | Stop condition |
|---|---|---|---|
| **AC-X1** | Claim ceiling held | No tracked artifact claims beyond Rung 1; `docs/ledger.md` stays the only ceiling-bearing artifact | Any artifact claims beyond Rung 1, or a non-ledger artifact asserts a ceiling → HALT |
| **AC-X2** | No Rung-2 admission / no ceiling advance | No artifact asserts a "beats random-legal" verdict or advances the claim ceiling | Any Rung-2 assertion or ceiling advance → HALT |
| **AC-X3** | No ledger mutation / no row | `docs/ledger.md` byte-unchanged; no `run-v002` / Rung-2 row written | Any `docs/ledger.md` diff or written row → HALT |
| **AC-X4** | No values / no SP-6 | No dispersion value promoted to tracked status; SP-6 not issued | Any value in a tracked artifact, or SP-6 issued → HALT |
| **AC-X5** | No build / no code | No schema file, no generator/validator code, no application code of any kind created | Any `.json` schema file, `analysis/` code, or app code created → HALT |
| **AC-X6** | No eval / no hardening | No new eval run, no K=50 top-up, no paired-delta tooling, no Kaggle submission automation | Any eval run, hardening, or submission tooling → HALT |
| **AC-X7** | No cross-regime / no regime mutation | No `regime-v002` figure compared to a v001 row; no `frozen/` regime/component edited | Any cross-regime comparison or `frozen/` edit → HALT |
| **AC-X8** | OD-6 unrelaxed / `M` unset / no inference | OD-6 stays descriptive-only; `M` unset; no inferential statistic computed or reported | OD-6 relaxed, `M` chosen, or an inferential result reported → HALT |
| **AC-X9** | No FunSearch implementation | No FunSearch dependency, scaffold, interface, integration, or heuristic surface | Any FunSearch implementation surface → HALT |
| **AC-X10** | Loop discipline | Sprint 00 lands through `/implement → /review-sprint → /audit-sprint` (docs cadence, **no OA-2**); one review + one audit artifact; no out-of-loop edits | Code lands outside `/implement`, or a COMPLETED marker appears without operator authorization → HALT |
| **AC-X11** | Forbidden words | `strong / competitive / optimal / calibrated / complete` appear only as negated/forbidden language across all changed tracked files | Any affirmative use → HALT |
| **AC-X12** | Zone discipline | Nothing under `.claude/` touched; State Zone (`grimoires/loa/NOTES.md`, `ledger.json`, `.beads/`) kept out of tracked docs commits | Any `.claude/` edit, or a State Zone file staged into a docs commit → HALT |

## 12. Validation commands

**Always-run gate (every docs task, before staging):**

```bash
python eval/hygiene_check.py --paths <changed tracked docs>   # sanitization staging gate; must exit 0
git diff --exit-code -- docs/ledger.md                        # ledger byte-unchanged (must report no diff)
```

**Planned targeted checks (docs-only; grep-level, no code):**

- Forbidden affirmative claim words absent (only negated): grep `strong|competitive|optimal|calibrated|complete` across
  each produced doc → only negated/forbidden uses.
- Inferential-statistic terms absent as affirmatives: grep `std.?dev|variance|confidence interval|p-value|significant|
  hypothesis|error bar` → present only as enumerated-forbidden language.
- No machine-readable schema file created: `ls analysis/evidence_summary_schema.json` → absent.
- No generator/validator code created: `ls analysis/evidence_summary.py` → absent.
- `M` unset in the OD-6 proposal: the proposal states `M` is deferred / unchosen (no numeric margin value present).
- No `frozen/` diff, no `analysis/`/`eval/` code diff, no `runs/` addition.

> **No validation step may mutate `docs/ledger.md`, any `frozen/` regime/component, any sealed run dir, or any
> `analysis/`/`eval/` source.** This is a docs-only cycle; the only created files are the six tracked docs of §9.

## 13. Review / audit expectations

Per the loop contract (§1–§3, §10), Sprint 00 closes through exactly **one `/review-sprint` artifact and one
`/audit-sprint` artifact**; corrective changes re-enter only through `/implement`. **Sprint 00 runs this cadence with no
OA-2 build gate** (docs-only). Future review/audit MUST verify:

- implementation touched **only** the six authorized docs paths (§9); no forbidden path edited
- **no schema file, no generator/validator code, no app code** created (the build is a later cycle; NG5)
- **`docs/ledger.md` byte-unchanged**; no row written; no ceiling advance (NG3, NG1–NG2)
- **no value promoted** to tracked status; SP-6 not issued (NG4)
- **OD-6 unrelaxed**; **`M` unset**; no inferential statistic computed or reported (NG6)
- **no cross-regime comparison**; **no `frozen/` regime/component edit** (NG11)
- **no FunSearch dependency/scaffold/interface/heuristic surface**; appendix notes-only (NG10)
- **no eval run / no evidence hardening / no Kaggle submission automation** (NG12, NG9, NG8)
- **no Competition Data or Pokémon Elements** in any tracked file (hygiene clean)
- **claim ceiling remains Rung 1**; the ledger remains the only ceiling-bearing artifact
- nothing under `.claude/`, and no State Zone file (`grimoires/loa/NOTES.md`, `ledger.json`, `.beads/`) staged into a
  docs commit
- **no COMPLETED marker** until explicit operator closeout authorization

> Review/audit are pure-review skills: `Write`/`Edit` disabled inside them is **expected, not a failure.** The
> review/audit artifact is persisted by the orchestrator into gitignored `grimoires/loa/a2a/...` after the skill returns.

## 14. Evidence-storage and sanitization rules

Per loop contract §7 / ESP-1..ESP-5 / SP-6 and SDD §3, §9:

- **All local run evidence, dispersion outputs, and dispersion VALUES stay local/git-ignored** and are **never**
  surfaced in any tracked artifact, including this plan and the six docs it authorizes (`02-sdd.md:175`; `requires-raw-data:
  cannot-surface`).
- **Promotion of any sanitized value to tracked status requires a separate later operator SP-6 decision** — out of
  Cycle-003 (NG4; `02-sdd.md:410-413`).
- **Tracked docs reference only** `run_id`, content hashes, sanitized metric *names*, claim ceilings, and local
  path/status — never embedded raw values.
- **Forbidden in any tracked artifact:** raw traces, card IDs/names, deck lists, hand contents, simulator logs,
  PDFs/CSVs, `deck.csv` rows, run-dir dumps, Pokémon Elements, Competition Data.
- **`eval/hygiene_check.py`** is the mechanical staging gate run on each produced doc.

## 15. Claim-ceiling rules

- **Rung 1 remains the ceiling** for all Cycle-003 artifacts. No task raises it (NG2; `docs/claim-ceiling.md:5-6`).
- **`docs/ledger.md` remains the only ceiling-bearing artifact.** The six docs carry **no** ceiling — only a Rung-1
  footer where relevant (`02-sdd.md:335-339`).
- **Allowed claim form** (descriptive, local, with `n`/`K`/`regime_id`): *"under `regime-v002` at n=N across K batches,
  the observed `<metric>` ranged from X to Y (mean Z)"* — and this cycle states such forms only as **schema examples
  without values** (`01-prd.md:314-316`).
- **No gameplay-strength, statistical-significance, cross-regime-uplift, leaderboard, calibration, optimality, or
  competitiveness claim** in any tracked output (NG13).
- **Forbidden words** (`strong, competitive, optimal, calibrated, complete`) checked by grep across every changed tracked
  file (AC-X11); they may appear only as negated/forbidden language.

## 16. Risks / stop conditions

Carried and sharpened from `01-prd.md:384-396` (R1–R8) and `02-sdd.md:435-447` (R1–R9), specialized to a docs-only cycle.

| # | Risk | Mitigation (plan-level) | Stop condition |
|---|------|---|---|
| R1 | **Value leak into tracked docs** — a dispersion value reaches a produced doc. | Docs carry no values; the schema enumerates forbidden fields; `hygiene_check` run on each doc; this plan carries no values (AC-S00-1, AC-X4, §14). | Any dispersion value in a tracked doc → HALT. |
| R2 | **Scope-creep into admission** — a doc drifts into asserting Rung 2 / advancing the ceiling. | Rung 1 held (§15); the OD-6 output is a *proposal*, not a decision (S00-T4); no row written (S00-T3); NG1–NG3 (AC-X1/X2/X3). | Any Rung-2 assertion or ceiling advance → HALT. |
| R3 | **Premature implementation** — a schema file or generator/validator code is built inside this planning cycle. | Spec/shape only; the build is a later cycle behind a fresh OA-2 (§10, OD-C3-6); FORBIDDEN paths include `analysis/evidence_summary.py` and any schema `.json` (§9); NG5 (AC-X5). | Any schema file or `analysis/` code created → HALT. |
| R4 | **Mis-resolved margin** — `M` chosen under the gravity of already-seen K-batch numbers. | Pre-registration procedure (margin fixed *before* numbers read); `M` deferred to a later gate; the proposal does not choose `M` (S00-T4; NG6, AC-S00-4, AC-X8). | A numeric `M` appears in the proposal → HALT. |
| R5 | **OD-6 relaxation by stealth** — an inferential statistic slips into the schema/proposal. | OD-6 stays descriptive-only; inferential terms enumerated as forbidden (S00-T1); grep gate (§12); the proposal presents OD-6-relaxation as alternative only (AC-X8). | Any inferential statistic computed/reported, or OD-6 relaxed → HALT. |
| R6 | **Cross-regime contamination** — a v002 figure placed beside a v001 row. | Forbidden-field set bars cross-regime fields; the future generator/validator's single-regime guard (exit 2) is specified; no `frozen/` touched (NG11, AC-X7). | Any cross-regime comparison appears → HALT. |
| R7 | **Evidence-hardening / eval creep** — K=50 / new eval runs / paired-delta tooling / Kaggle automation sneak in. | Pure spec cycle; no eval run, no tooling build, no submission automation authorized; follow-ups recorded as future options only (NG8/NG9/NG12, AC-X6). | Any eval run, hardening, or submission tooling → HALT. |
| R8 | **FunSearch creep** — a dependency/scaffold/interface/heuristic surface is added. | Appendix is notes-only; JSON-first is an existing-pattern choice; no runtime-agent surface (S00-T5; NG10, AC-X9). | Any FunSearch implementation surface → HALT. |
| R9 | **Runtime-agent creep** — agent tuning/planning beyond "closed lane." | `agents/runtime/` FORBIDDEN to touch (§9); agents frozen; lane closed (NG7). | Any `agents/runtime/` edit or tuning plan → HALT. |
| R10 | **Building before the gate** — this plan misread as authorization. | This plan opens no build gate and creates no `/implement` prompt; the build is a later cycle behind a fresh OA-2 (§3, §10). | Any code patch / schema file before a fresh OA-2 → HALT (out-of-loop edit). |
| R11 | **State Zone leak into a docs commit** — `NOTES.md` / `ledger.json` / `.beads/` staged with the docs. | State Zone FORBIDDEN to stage (§9; operator constraint; OD-9); review verifies the staged set is the six docs only (AC-X12). | Any State Zone file staged into a docs commit → HALT. |

## 17. Explicit out-of-scope (forbidden — mention only)

Opening any of these requires a separate, explicit operator decision that supersedes the standing notes:

**Admission / claim / ledger boundaries:** Rung-2 admission · claim-ceiling advance · `docs/ledger.md` mutation ·
`run-v002` / Rung-2 ledger row · SP-6 issuance / live-value promotion · statistical-significance claims · cross-regime
uplift · gameplay-strength / leaderboard / calibration / optimality / completeness / competitiveness claims · any
inferential statistic (CIs, p-values, "significant", hypothesis tests, inferential error bars) · choosing the numeric
margin `M` · relaxing OD-6.

**Build / code boundaries:** the machine-readable schema **file** · the generator/validator **code**
(`analysis/evidence_summary.py`) · any application code of any kind · editing `analysis/dispersion_report.py` /
`aggregate.py` / `delta_report.py` / `eval/*` · opening a build gate (OA-2) · generating an `/implement` prompt.

**Evidence / eval boundaries:** new eval runs · K=50 confidence top-up · paired-delta tooling (S02-T4) · running the
harness · authoring or reading `runs/` into a tracked artifact · raw trace/card/deck/simulator-log exposure into tracked
artifacts.

**Optimization / agent boundaries:** runtime-agent work / tuning / heuristic changes · any `agents/runtime/` behavior
change · RL · self-play · deck optimizer · value/win-probability model · search/lookahead/MCTS · ELO / tournament ·
leaderboard tuning · dashboard · Kaggle upload / submission packaging automation · broad optimization.

**FunSearch boundaries:** FunSearch implementation · dependency · scaffold · interface · integration · candidate-search
code · runtime-agent heuristic surface (appendix is notes-only).

**Regime / process / zone boundaries:** editing `regime-v001`/`regime-v002` or any component · regime mutation ·
comparing `regime-v002` numbers to v001 rows · editing `.claude/` (System Zone) · staging State Zone
(`grimoires/loa/NOTES.md`, `ledger.json`, `.beads/`) into a docs commit · out-of-loop edits · premature COMPLETED marker.

## 18. Open decisions carried forward

Carried from `01-prd.md:365-382` (OD-C3-1…OD-C3-7) and the SDD's disposition (`02-sdd.md:496-506`), with this plan's
disposition. **None is opened or decided by this plan.**

| ID | Decision | Disposition |
|---|---|---|
| **OD-C3-1** | OD-6 / criterion-2 resolution (disjoint-bands vs OD-6 relaxation) | **Proposed in shape** by S00-T4; decision left to the operator at the later admission seam. This plan does not decide. |
| **OD-C3-2** | Numeric margin `M` | **Deferred.** Pre-registration procedure designed (S00-T4); `M` unset. Fixed before the numbers are read, at the later gate. |
| **OD-C3-3** | SP-6 schema authorization | Schema **specified** (S00-T1); **live-value promotion deferred** to admission (NG4). Whether to author the schema spec now is the operator's acceptance of this plan. |
| **OD-C3-4** | Artifact placement | **Resolved by the SDD** (§3) and carried into §9 (the six `docs/cycles/cycle-003/` paths). |
| **OD-C3-5** | Optional future evidence hardening (K=50 / paired-delta) | **Out of Cycle-003** (NG12); recorded as a future option only. |
| **OD-C3-6** | Build authorization (OA-2 equivalent) for the schema file + generator/validator code | A **separate later operator gate in a future cycle**. This plan opens no gate. |
| **OD-C3-7** | Admission timing (gated capstone vs standalone cycle) | Not decided here; carried to the later Rung-2 admission gate. |

## 19. Build-gate statement

```
This Sprint Plan opens no build gate.
Sprint 00 is docs-only (tracked docs only) and runs the normal /implement -> /review-sprint -> /audit-sprint ->
  acceptance cadence, opening no OA-2 build gate.
The schema FILE + generator/validator CODE are a SEPARATE LATER CYCLE behind a fresh operator OA-2 / build gate.
No Rung-2 admission. No claim-ceiling advance. No docs/ledger.md mutation. No Rung-2 row. No SP-6 / no live values.
No eval run. No numeric margin M. OD-6 unrelaxed. No FunSearch implementation. No runtime-agent work. No cross-regime.
The claim ceiling remains Rung 1.
```

The single hard procedural gate for build is OA-2 (loop contract §6; `02-sdd.md:485`, OD-C3-6), and it lives in a
**later cycle**, not in a later sprint of this one. `/implement` may run for **Sprint 00 only** (docs-only, no OA-2) to
author the six tracked docs through the normal review/audit cadence. This plan creates no `/implement` prompt and writes
no app code.

## 20. Recommendation

**Sprint Plan is ready for operator acceptance** — **1 docs-only sprint, all Core, no OA-2 build gate**: Sprint 00
authors five tracked design/spec docs (C3-FR-1…C3-FR-5) plus an end-to-end goal-validation sweep, converting the
remaining Rung-2 gap into a single pre-specified future operator decision. Every task is confined to tracked
`docs/cycles/cycle-003/` paths; nothing under `frozen/`, `analysis/`, `eval/`, `runs/`, `agents/runtime/`,
`docs/ledger.md`, or `.claude/` is touched; no value is promoted; Rung 1 is held.

**Do NOT begin implementation from this plan alone, and do NOT build the schema file or generator/validator code.** This
plan opens no build gate and creates no `/implement` prompt. After operator acceptance, the next steps are one of:

1. **commit the Sprint Plan** (planning artifact lands on `main` via the normal `docs:` path), and/or run **Sprint 00**
   (docs-only; normal `/implement → /review-sprint → /audit-sprint → acceptance` cadence; **no OA-2 gate**); then
2. in a **later cycle**, the operator opens an explicit build gate (**OA-2**) to implement the schema file +
   generator/validator code specified by Sprint 00's docs.

Neither the build nor any Rung-2 admission is performed by this Sprint Plan. It creates the planning artifact and reports
status only.

> **Sources:** `docs/cycles/cycle-003/02-sdd.md` (binding input; §1.2 spine, §3 placement, §4 schema, §5 generator,
> §6 validator, §7 ledger convention, §8 OD-6 proposal + later seam, §9 no-values protections, §10 FunSearch, §12
> design-level acceptance, §13 designed-now-vs-later, §15 traceability); `docs/cycles/cycle-003/01-prd.md` (C3-FR-1…5,
> G1–G6, NG1–NG13, OD-C3-1…7, AC-1…7); `docs/cycles/cycle-002/03-sprint-plan.md` (format/cadence/firebreak precedent);
> `docs/cycles/cycle-002/closeout.md`, `04-rung-2-readiness-criteria.md`, `05-reproducibility-reality.md`,
> `06-ledger-report-discipline.md`, `07-operator-decision-register.md`; `docs/claim-ceiling.md` (Rung 1; only
> ceiling-bearing artifact); `docs/ledger.md` (two Rung-1 rows; schema; verdict rule); `docs/operator/turntrace-loop-contract.md`
> (§1-§3, §6-§10); `docs/operator/deferred-lane-gate-after-sprint-01.md` (still-closed list); `eval/schemas.md`
> (spec-pairs-with-validator placement precedent); `eval/hygiene_check.py` (sanitization staging gate);
> `analysis/dispersion_report.py` (read surface + exit-code discipline + descriptive vocabulary);
> `analysis/delta_report.py` (`CrossRegimeRefusal`); `analysis/aggregate.py` (per-run sanitized stats);
> `frozen/regimes/regime-v00{1,2}.json`; `frozen/seeds/seed-set-v00{1,2}.json`.
> Current main at authoring: `3014c07`. Claim ceiling: **Rung 1 (unchanged).** This Sprint Plan opens no build gate,
> designs no runtime-agent change, builds no schema file or code, writes no ledger row, promotes no value, and creates
> no `/implement` prompt.
