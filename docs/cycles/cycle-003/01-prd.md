# Cycle-003 PRD — Rung-2 Admission Readiness: Tracked Evidence Summary + Ledger Plumbing

> Planning artifact (PRD). Status: **DRAFT — research/planning only.** This document opens **NO build gate**
> and is **NOT an implementation authorization**. It **specifies requirements**; it builds nothing.
> Implementation of any specified artifact (schema file, generator/validator code, finalized ledger-row
> convention) requires a separate, explicit operator build-gate action (OA-2 equivalent) per
> `docs/operator/turntrace-loop-contract.md` §6, and lands only through `/architect → /sprint-plan →
> /implement → /review-sprint → /audit-sprint → operator acceptance`.
> Binding planning input: the local pre-PRD research/decision pass
> (`grimoires/loa/a2a/cycle-003/pre-prd-research.md`, gitignored State Zone) and the tracked Cycle-002
> closeout + readiness docs. Substantive grounding citations below point to **tracked** artifacts so this
> PRD is self-grounded on durable sources.
> Sanitized note. No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, Pokémon Elements, or Competition Data appear here (CC-1/CC-2, ESP). **No dispersion
> metric values appear here** — local evidence is referenced qualitatively only and its values stay
> local/gitignored. Runs are referenced by `run_id`, hashes, sanitized metric *names*, claim ceilings, and
> local path/status only. The forbidden agent claim words (*strong / competitive / optimal / calibrated /
> complete*) appear only as negated/forbidden language.

| Field | Value |
|---|---|
| **Cycle** | Cycle-003 |
| **Working title** | Rung-2 Admission Readiness: Tracked Evidence Summary + Ledger Plumbing |
| **Alt. framing** | Make a future Rung-2 admission a single, pre-specified, low-risk operator decision |
| **Type** | Product Requirements Document (planning artifact, not a build artifact) |
| **Status** | DRAFT — awaiting operator acceptance; next Golden-Path step is SDD / architecture, not implementation |
| **Date** | 2026-06-18 |
| **Current main** | `37d7851` — *docs: close TurnTrace Cycle-002* |
| **Binding input** | local pre-PRD research/decision pass (gitignored) + `docs/cycles/cycle-002/closeout.md` |
| **Posture** | Specify/design the admission **plumbing** (specs/conventions/proposal), **not** the admission |
| **Claim ceiling** | Rung 1 (held for the whole cycle; not raised) |

## Required posture (binding)

- **Cycle-003 planning opens no build gate.** This PRD authorizes no code and creates no schema file,
  generator/validator code, tracked metric summary, or ledger row. It **specifies**; it does not build.
- **Cycle-003 specifies/designs Rung-2 admission *readiness plumbing*, not a Rung-2 admission.** It does **not** assert
  any "beats random-legal" verdict and does **not** advance any claim ceiling.
- **The claim ceiling remains Rung 1** for all of Cycle-003 until a separate, explicit later operator
  decision earns otherwise (`docs/claim-ceiling.md`; `docs/cycles/cycle-002/closeout.md:8`).
- **No live dispersion values are promoted to tracked status.** SP-6 is **not** issued here; only the
  *schema* (the safe shape) is specified. Values stay local/gitignored (ESP-1;
  `docs/cycles/cycle-002/06-ledger-report-discipline.md` §5-§6).
- **`docs/ledger.md` is not changed.** No `run-v002` / Rung-2 row is written; the ledger remains the **only
  ceiling-bearing artifact** (`docs/claim-ceiling.md:5-6`; `docs/ledger.md:1-8`).
- **The runtime-agent improvement lane remains closed; broad optimization remains closed.** Every "Still
  closed" item (`docs/operator/deferred-lane-gate-after-sprint-01.md:71-87`) stays closed and requires a
  separate, explicit operator decision to open.
- **FunSearch is future-loop architecture only.** Cycle-003 adds no FunSearch dependency, scaffold,
  integration, or runtime-agent heuristic surface — forward-compatibility *notes* only.
- **`regime-v001` / `regime-v002` and their components are never edited; never compare across regimes**
  (NFR-5; `frozen/regimes/regime-v001.json:9`).
- **The OD-6 and SP-6 bright lines stay in force.** The OD-6 ↔ Rung-2-criterion-2 resolution is **proposed**
  here, not decided; OD-6 (descriptive-only) is not relaxed by this PRD
  (`docs/cycles/cycle-002/07-operator-decision-register.md` §1-§2).

The bright line for the whole cycle: **Cycle-002 produced the larger-`n` data and the descriptive-dispersion
*machinery*; Cycle-003 specifies/designs the *tracked sanitized evidence-summary schema*, the *Rung-2 ledger-row +
verdict convention*, and the *OD-6/criterion-2 resolution proposal* — so a future Rung-2 admission becomes a
single pre-specified operator decision — and Cycle-003 stops short of that decision.**

## 1. Product / cycle overview

TurnTrace is a local, sanitized evaluation harness for a card-game simulator. Cycle-002 ("Evaluation Scale +
Comparison Confidence") earned the **Rung-2-readiness infrastructure** at Rung 1: an additive `regime-v002`
(reusing the three v001 components by ref+hash; `frozen/regimes/regime-v002.json`), a `seed-set-v002` at
N=500 (`frozen/seeds/seed-set-v002.json`), a dry-run budget procedure + 3 GiB ceiling, a repeated
same-regime batch capability, K=20 → 40 local sealed run dirs, an offline descriptive
`analysis/dispersion_report.py`, and supporting tests — all without advancing the ceiling
(`docs/cycles/cycle-002/closeout.md` §3). It did **not** earn a Rung-2 claim, a ceiling advance, a ledger
row, any tracked dispersion values, or any runtime/optimization change (`closeout.md` §4).

Two facts set up this cycle. First, the **confidence evidence** behind any future Rung-2 verdict — the
cross-batch dispersion — lives **only** in local/gitignored files; the tracked Cycle-002 closeout is
**narrative-only** and carries no values (`closeout.md` §8). Second, the Rung-2 admission gate is
**conjunctive** and three of its five criteria are unmet, **all governance/design, not data**: an
operator-approved inferential procedure (criterion 2), a pre-registered margin (criterion 3), and an
operator-authorized ceiling advance (criterion 5) (`docs/cycles/cycle-002/04-rung-2-readiness-criteria.md`
§2). Worse, criterion 2 ("inferential procedure") directly conflicts with the deliberate Cycle-002 bright
line OD-6 ("no inferential statistics"). Admitting Rung 2 today would therefore bundle two bright-line
relaxations (OD-6, SP-6) + a pre-registered margin + an irreversible append-only ledger row into one cycle —
against the project's gate-by-gate discipline.

**Mission (binding).** Specify — claim-safely and without building — (a) a **tracked sanitized
evidence-summary schema** for K-batch dispersion evidence, (b) a **generator/validator shape** that produces
hygiene-passing summaries from existing local outputs, (c) the **Rung-2 ledger-row + verdict convention**
(format/spec only, no row written), and (d) an **OD-6 / criterion-2 resolution proposal** (a pre-registered
descriptive disjoint-bands rule preferred), plus (e) a **FunSearch forward-compatibility appendix**. The goal
is to convert the remaining Rung-2 gap into a **single, pre-specified operator decision** — while holding the
ceiling at Rung 1, promoting no values, writing no ledger row, and building no artifact or code.

**Who consumes this PRD.** The **operator** (owns gate decisions; the only party who may resolve OD-6/SP-6,
choose the margin, or advance the ceiling; decides whether to proceed to SDD); the future **implementer**
(`/implement`, the single patch authority once a build gate opens) who will build the specified schema and
generator/validator; the future **reviewer/auditor** (`/review-sprint`, `/audit-sprint`); a future **Rung-2
admission reviewer** who must read the comparison from sanitized, tracked artifacts alone; and a future
**evaluator consumer** (the FunSearch forward-compat reader).

## 2. Problem statement

The Rung-2-readiness infrastructure exists, but admission is **not yet a clean, low-risk operator decision**:

1. **The Rung-2 gate is conjunctive and three of five criteria are unmet — all governance/design.** Satisfied:
   the same-regime baseline-vs-candidate *data shape* (criterion 1) and provenance/audit-trail (criterion 4).
   Unmet: an operator-approved inferential procedure (2), a pre-registered margin (3), and an
   operator-authorized ceiling advance (5) (`04-rung-2-readiness-criteria.md` §2). **None of these is a data
   problem.**
2. **No tracked sanitized evidence-summary *format* exists.** The cross-batch dispersion that would justify a
   Rung-2 verdict's confidence is local/gitignored only; the tracked closeout is narrative-only (no values)
   (`closeout.md` §8; `06-ledger-report-discipline.md` §5-§6). A ledger *row* carries a single run's
   `win_rate` by schema (`docs/ledger.md:9`), but the *confidence* (the K-batch spread) has no tracked,
   sanitized, hygiene-passing home.
3. **Criterion 2 conflicts with OD-6 — unresolved.** Criterion 2 demands an *inferential* procedure; OD-6
   *forbids* inferential statistics (no std-dev/variance, no CIs, no p-values, no "significance") as a
   deliberate bright line (`07-operator-decision-register.md` §1-§2). An admission cycle that did not resolve
   this first would stumble into it mid-flight.
4. **No Rung-2 ledger-row / verdict convention is specified.** `docs/ledger.md` holds only the two Rung-1
   `regime-v001` n=12 rows (`run-0001`, `run-0002`); the shape of a deliverable Rung-2 row and its
   same-regime, agent-only `verdict` are not yet written down (`docs/ledger.md:9-12`).
5. **Doing admission now bundles too many irreversible acts.** Two bright-line relaxations + a pre-registered
   margin + an append-only ceiling row, all at once, is the highest-consequence, hardest-to-walk-back path.
   The project's discipline is to build readiness, then advance as a separate explicit decision
   (`04-rung-2-readiness-criteria.md` §2.5; `closeout.md` §10).

## 3. What Cycle-003 must prove (goals)

- **G1 — Tracked evidence-summary schema is specified.** A complete requirement set for a sanitized K-batch
  evidence-summary schema: enumerated **safe** fields and enumerated **forbidden** fields.
- **G2 — Generator/validator shape is specified.** A complete requirement set for an offline tool shape that
  produces hygiene-passing, schema-conforming summaries from existing local sealed run dirs + dispersion
  outputs, and a validator that refuses forbidden content.
- **G3 — Rung-2 ledger-row + verdict convention is specified.** Format/spec only: the row's columns and
  semantics, and the same-regime agent-only `verdict` rule with explicit `n` and explicit claim ceiling — **no
  row written.**
- **G4 — OD-6 / criterion-2 resolution proposal is authored.** A proposal that resolves the criterion-2 ↔ OD-6
  tension, recommending a pre-registered descriptive **disjoint-bands** rule, with the relax-OD-6 alternative
  presented — both left as explicit operator decisions for a later gate.
- **G5 — FunSearch forward-compatibility appendix is provided.** Notes-only guidance that keeps TurnTrace a
  clean scalar-per-candidate, regime-stamped evaluator, with no FunSearch dependency/scaffold/integration.
- **G6 — Rung 1 is held; the ledger is untouched.** No claim-ceiling advance, no ledger row, no values
  promoted to tracked status, across the whole cycle.

## 4. What Cycle-003 must not prove or claim (non-goals)

- **NG1 — No Rung-2 admission.** No artifact asserts a "beats random-legal" verdict or any Rung-2 claim.
- **NG2 — No claim-ceiling advance.** The ceiling stays Rung 1; only the ledger, advanced by a separate
  explicit operator decision, can ever carry a higher rung (`docs/claim-ceiling.md:5-6`).
- **NG3 — No `docs/ledger.md` mutation.** No `run-v002` / Rung-2 row; the convention is format/spec only.
- **NG4 — No SP-6 issuance for live values.** No promotion of any dispersion value to tracked status; the
  schema is specified, the values stay local/gitignored (`06-ledger-report-discipline.md` §5-§6).
- **NG5 — No artifacts or code built.** No schema file, no generator/validator code, no application code of
  any kind. The PRD specifies requirements; building them needs a separate later `/implement`.
- **NG6 — No numeric margin chosen; no inferential results.** The disjoint-bands rule's margin `M` is left
  unset; OD-6 is not relaxed; no inferential statistic is computed or reported.
- **NG7 — No runtime-agent work.** No runtime-agent implementation, and no runtime-agent planning beyond
  "the lane is closed"; baseline and candidate agents stay frozen (`regime-v002` reuses frozen agents).
- **NG8 — No broad optimization.** No RL, self-play, deck optimizer, value/win-probability model,
  search/lookahead/MCTS, ELO/tournament, dashboard, leaderboard/tuning loop
  (`deferred-lane-gate-after-sprint-01.md:71-87`).
- **NG9 — No Kaggle submission automation** (upload, packaging, submission tooling).
- **NG10 — No FunSearch implementation/scaffolding.** No dependency, no integration, no heuristic surface;
  appendix is notes-only.
- **NG11 — No `regime-v001`/`regime-v002` mutation; no cross-regime comparison.** A result is meaningful only
  relative to its own `regime_id` (NFR-5; `frozen/regimes/regime-v001.json:9`).
- **NG12 — No evidence hardening in scope.** A K=50 confidence top-up, any new eval runs, and the S02-T4
  paired-delta tooling are **Non-Goals** for Cycle-003 (they are Option-B evidence hardening, require running
  eval, and exceed pure schema/ledger readiness). They MAY be **mentioned** as future optional follow-ups
  only (§13 OD-C3-5).
- **NG13 — No forbidden claims.** No gameplay-strength, statistical-significance, calibration, leaderboard,
  optimality, completeness, competitiveness, or cross-regime-uplift claim; the forbidden agent words appear
  only as negated/forbidden language.

## 5. Functional requirements

Five lanes, all **specification/proposal** (planning artifacts), none a build. The actual schema file,
generator/validator code, and finalized ledger-row convention are produced in a **later** authorized cycle.

### C3-FR-1 — Tracked sanitized evidence-summary schema (Spec, Lane A)

Specify a schema for a tracked, sanitized K-batch evidence summary. **Required safe fields:** `regime_id`,
`n`, `K`, `agent_id` / `agent_version`, per-metric descriptive vocabulary only
(`count` / `min` / `max` / `range` / `mean` / `median` / `spread`), the `run_id` list, the per-run / batch
content `hashes`, `mode=unseeded`, the unseeded-process caveat string, and a Rung-1 footer. **Forbidden
fields** (enumerated and validator-enforced): raw decision rows / trace bodies; any Competition Data (card
IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs, `deck.csv` rows, run-dir dumps); Pokémon
Elements; `std-dev` / `variance` / any inferential statistic (OD-6); any cross-regime field or comparison
(NFR-5); the forbidden agent words as affirmatives. Sanitization parity with `eval/hygiene_check.py` and the
`analysis/dispersion_report.py` read surface (manifest + `match_results/*` only; never the decision
sidecars). **Specifies the schema; creates no schema file and promotes no values.**

### C3-FR-2 — Generator / validator shape (Spec, Lane B)

Specify the *shape* of an offline tool that (a) reads existing local sealed run dirs and the local
dispersion outputs, (b) emits a **schema-conforming** (C3-FR-1) sanitized summary, and (c) a **validator**
that rejects any forbidden field or value-bearing leak before a summary could ever be promoted. Required
properties: offline/`analysis/` import boundary (no `cabt`, `sim/`, `agents/runtime/`, or `eval/` import;
the standing offline/runtime separation), stdlib-only, a single-regime guard (hard-refuse / exit 2 on mixed
`regime_id`, mirroring `dispersion_report.py` / `delta_report.py`), and never opening the per-decision
sidecars. **Specifies the shape; builds no code.**

### C3-FR-3 — Rung-2 ledger-row + verdict convention (Spec, Lane C, format-only)

Specify, as format/spec only, the convention for a future deliverable Rung-2 ledger row and its verdict:
the required columns and their semantics (consistent with the existing ledger schema — `date`, `run_id`,
`regime_id`, `git_rev`, `sim_version`, `agent_version`, `opponent_pool_ref`, `seed_set_ref`, `games`/`n`,
`win_rate`, `illegal_action_rate`, `timeout_rate`, `error_rate`, `avg_turns`, `mode`, `hypothesis`,
`claim_ceiling`, `notes`); the **same-regime, agent-only** `verdict` rule (a better/worse verdict only with a
ceiling + `n`, **never** across regimes — NFR-5); explicit `n`; explicit `claim_ceiling`. State the
relationship to C3-FR-1: the **row** carries the ceiling-bearing verdict; the **evidence summary** carries
the confidence behind it (the two are separate artifacts). **No row is written; `docs/ledger.md` is
unchanged.**

### C3-FR-4 — OD-6 / Rung-2 criterion-2 resolution proposal (Proposal, Lane D)

Author a proposal (PRD content) resolving the criterion-2 ↔ OD-6 tension (§9). **Recommended:** a
pre-registered descriptive **disjoint-bands** rule of the shape *"candidate `min` > baseline `max` by ≥ M
across K ≥ 20 same-regime batches"*, expressed using only the allowed descriptive vocabulary (no
`std-dev`/`variance`, no inferential statistic), with the **pre-registration procedure** specified in shape
(the margin is fixed before the numbers are read) but the numeric margin `M` **left unset**. **Alternative:**
the operator relaxes OD-6 to permit a genuine inferential test. Both are explicit **operator decisions for a
later gate**; this PRD recommends disjoint-bands, **does not decide**, **does not choose `M`**, and **produces
no inferential result.**

### C3-FR-5 — FunSearch forward-compatibility appendix (Docs, Lane E, notes-only)

Provide an appendix stating that TurnTrace should remain a clean **scalar-per-candidate, regime-stamped**
evaluator; the C3-FR-1 schema should stay **JSON-first** / machine-readable and avoid assumptions that would
block a future automated evaluator from consuming it; a future candidate-search loop would require a
**runtime-agent heuristic surface first** (currently closed) and an evaluator that **averages over enough
matches/batches to clear the unseeded RNG noise floor** (`05-reproducibility-reality.md` §3-§4). Cycle-003
adds **no** FunSearch dependency, scaffold, integration, or heuristic surface (NG10).

## 6. Non-functional requirements / technical posture

- **NFR-1 — Claim-safety.** Rung 1 held; forbidden agent words negated-only; no inferential results; no claim
  exceeds the ledger row's `claim_ceiling` (`docs/claim-ceiling.md:54-65`).
- **NFR-2 — Sanitization.** Competition Data and Pokémon Elements never enter git (CC-1/CC-2, ESP); the
  staging guard `eval/hygiene_check.py` mechanically refuses the carrying paths; tracked artifacts hold
  sanitized specs only (`turntrace-loop-contract.md` §7).
- **NFR-3 — Same-regime only.** No field, example, or comparison crosses `regime_id` (NFR-5); the specified
  generator/validator enforces a single-regime guard.
- **NFR-4 — Descriptive vocabulary only.** Only `count/min/max/range/mean/median/spread`; `std-dev`,
  `variance`, and all inferential statistics are excluded unless and until the operator relaxes OD-6 at a
  later gate (`07-operator-decision-register.md` §2).
- **NFR-5 — Offline/runtime separation.** Any specified generator/validator is `analysis/`-class: stdlib-only,
  no `cabt`/`sim`/`agents/runtime`/`eval` import, never reads decision sidecars (matching
  `analysis/dispersion_report.py`).
- **NFR-6 — Reproducibility posture.** `mode=unseeded`; reproducibility is distribution-stable + audit-trail,
  not byte-identical replay; the unseeded-process caveat travels with every evidence summary
  (`05-reproducibility-reality.md`).
- **NFR-7 — Zone discipline.** Tracked specs/PRD live under `docs/`; local evidence, values, run dirs, and the
  pre-PRD research stay gitignored State Zone (ESP-1; `.gitignore`).
- **NFR-8 — Spec-only.** This cycle produces no artifact or code; every FR is a requirement/proposal, built
  later under a separate authorization (NG5).

## 7. Evidence-summary schema requirements and constraints (C3-FR-1 / C3-FR-2 detail)

- **Safe-field set** is exactly the descriptive surface already produced by `analysis/dispersion_report.py`
  plus identity/provenance fields (`regime_id`, `n`, `K`, `agent_id`/`agent_version`, `run_id` list,
  `hashes`, `mode`, caveat, Rung footer). The schema adds **no** new metric and **no** new statistic.
- **Forbidden-field set** is enumerated and **validator-enforced**, not merely documented: raw rows/traces,
  Competition Data, Pokémon Elements, inferential statistics, cross-regime fields, affirmative forbidden
  words. A summary that would carry any of these fails validation and can never be promoted.
- **JSON-first.** The summary's machine-readable form is primary (FunSearch forward-compat, C3-FR-5); a
  human-readable rendering is derived, never the source of truth.
- **Value-promotion gate (SP-6).** Defining the **schema** is in scope; **promoting live values** into a
  tracked summary is **not** (NG4). The schema specifies *what a promoted summary may contain*; issuing SP-6
  to actually promote values is a separate later operator decision (§13 OD-C3-3).

## 8. Ledger-row / verdict convention requirements (C3-FR-3 detail)

- **Row semantics.** A Rung-2 deliverable row follows the existing append-only ledger schema
  (`docs/ledger.md:9`), adding no column; its `claim_ceiling` field is where a Rung-2 ceiling would one day be
  recorded — by a separate operator decision, never by this PRD.
- **Verdict rule.** A `verdict` of better/worse is written **only** for a same-regime, agent-only comparison
  carrying a ceiling and an `n`, and **never** across regimes (`06-ledger-report-discipline.md` §4; NFR-5).
- **Separation of concerns.** The **ledger row** is the ceiling-bearing verdict; the **evidence summary**
  (§7) is the sanitized confidence behind it. The convention specifies how a future row would *cite* a
  promoted evidence summary without embedding raw content.
- **No row written.** `docs/ledger.md` stays at its two Rung-1 `regime-v001` rows; this cycle changes nothing
  in it (NG3). Per the operator constraint, `docs/ledger.md` is **not edited** by this planning cycle.

## 9. OD-6 / criterion-2 resolution proposal requirements (C3-FR-4 detail)

- **The tension.** Rung-2 criterion 2 requires "an explicitly designed and operator-approved **inferential**
  procedure" (`04-rung-2-readiness-criteria.md` §2.2); OD-6 **forbids** inferential statistics
  (`07-operator-decision-register.md` §2). They cannot both hold unchanged.
- **Recommended resolution — pre-registered descriptive disjoint-bands.** Define the Rung-2 decision rule as
  *"candidate `min` > baseline `max` by ≥ M across K ≥ 20 same-regime batches"*, using only allowed
  descriptive vocabulary. This satisfies criterion 3's *pre-registered margin* and reinterprets criterion 2's
  spirit ("pre-registered, operator-approved, not chosen after the fact") **without** crossing OD-6.
- **Pre-registration procedure.** The rule and its margin `M` are fixed **before** the comparison numbers are
  read as the verdict. The PRD specifies the *procedure*; it does **not** choose `M` (NG6).
- **Alternative — relax OD-6.** The operator may instead relax OD-6 to permit a genuine inferential test. The
  proposal presents this as the alternative, not the recommendation.
- **Decision deferral.** Choosing between disjoint-bands and OD-6-relaxation, and fixing `M`, are explicit
  operator decisions at a **later** gate (§13 OD-C3-1, OD-C3-2). This proposal resolves criteria 2 and 3 *in
  shape*; criterion 5 (the ceiling advance) remains a separate, later, explicit decision.

## 10. Claim-ceiling posture

The loop sits at **ladder Rung 1 — legal completion / throughput / audit-trail**, and **Cycle-003 keeps the
ceiling at Rung 1** for the whole cycle. The maturity ladder
(`docs/cycles/cycle-000-bootstrap/01-turntrace-prd.md:274-276`):

```
Rung 0  env not trusted
Rung 1  legal completion                         ← current, and held for all of Cycle-003
Rung 2  beats random-legal                       ← admission PLUMBING specified here; never claimed
Rung 3  beats scripted / prior best, ablation-backed
Rung 4  stable, report-ready
```

**Allowed claim form** — relative, local, descriptive, carrying its `n`, `K`, and `regime_id` (e.g. *"under
`regime-v002` at n=N across K batches, the observed `<metric>` ranged from X to Y (mean Z)"*). **Forbidden
claim forms** (negated-only): gameplay strength; statistical significance; cross-regime uplift; leaderboard
quality; calibration; optimality; competitiveness. Only the ledger, advanced by a separate explicit later
operator decision, can ever carry a higher rung (`docs/claim-ceiling.md:54-65`). **This PRD advances
nothing.**

## 11. Safety and sanitization constraints

Carried verbatim from the standing rules (`turntrace-loop-contract.md` §7-§8;
`06-ledger-report-discipline.md` §5-§7):

- **Competition Data never enters git** (CC-1/CC-2): the `cg/` SDK, card data, raw deck lists, `deck.csv` —
  local-only under gitignored `grimoires/loa/context/`.
- **Pokémon Elements** (names, rules, type matchups, deck recipes) never appear in tracked artifacts.
- **Generated runs, values, and dispersion outputs** stay local/gitignored; tracked artifacts hold sanitized
  specs, ledger rows, claim ceilings, failure-mode notes, planning docs, and operator-approved artifacts only.
- **`eval/hygiene_check.py`** is the mechanical staging gate; the specified validator (C3-FR-2) is
  sanitization-parity with it.
- **Forbidden agent claim words** (*strong / competitive / optimal / calibrated / complete*) appear only as
  negated/forbidden language.

## 12. Success criteria

### 12.1 Planning-cycle success (this PRD onward, no build)

- This PRD is accepted by the operator and proceeds to `/architect` (SDD), not implementation.
- It specifies all five FRs (C3-FR-1…C3-FR-5) claim-safely, with safe/forbidden field sets enumerated and the
  OD-6/criterion-2 proposal authored.
- Rung 1 is held; `docs/ledger.md` is unchanged; no dispersion value is promoted to tracked status; no schema
  file or code is created.
- Every requirement traces to a tracked source (file:line) or an operator confirmation.

### 12.2 Later build-cycle success (only after a separate build authorization; acceptance criteria)

When the specified artifacts are later built under an explicit `/implement` authorization, acceptance requires:

- **AC-1** — A schema (file/spec) conforms to C3-FR-1: safe fields only; forbidden fields rejected by the
  validator; sanitization parity with `hygiene_check`.
- **AC-2** — A generator/validator behaves per C3-FR-2: hygiene-passing output; offline/`analysis/` import
  boundary; stdlib-only; single-regime guard (exit 2 on mixed regime); never reads decision sidecars.
- **AC-3** — The Rung-2 ledger-row + verdict convention is documented per C3-FR-3; **no row is written** until
  a separate Rung-2 admission decision.
- **AC-4** — The OD-6/criterion-2 resolution proposal is authored per C3-FR-4: disjoint-bands recommended; `M`
  unset; no inferential result.
- **AC-5** — The FunSearch forward-compat appendix is present per C3-FR-5 (notes-only; no dependency/scaffold).
- **AC-6** — Rung 1 held; `docs/ledger.md` unchanged; no value promoted to tracked status.
- **AC-7** — The work lands through the full `/implement → /review-sprint → /audit-sprint → operator
  acceptance` cadence; EDD test scenarios (schema/validator lint + hygiene checks) meet the configured
  minimum (`.loa.config.yaml: edd.min_test_scenarios`).

## 13. Open operator decisions for SDD / sprint planning

- **OD-C3-1 — OD-6 / criterion-2 resolution.** Ratify the pre-registered descriptive disjoint-bands rule
  (recommended) **or** relax OD-6 for a genuine inferential test. Operator decision, later gate (C3-FR-4).
- **OD-C3-2 — Margin `M`.** The numeric margin for the disjoint-bands rule. **Deferred** — fixed before the
  numbers are read, at a later admission gate; not chosen in this PRD (NG6).
- **OD-C3-3 — SP-6 schema authorization.** Authorize defining the tracked evidence-summary *schema* now
  (recommended), with live-value promotion deferred to admission (NG4).
- **OD-C3-4 — Artifact placement.** Where the eventual schema file and convention doc live (e.g.
  `docs/cycles/cycle-003/` for specs; a `docs/`-tracked or `frozen/`-adjacent path for the schema file). SDD
  decides.
- **OD-C3-5 — Optional future evidence hardening.** Whether a later, separately-authorized cycle runs a K=50
  confidence top-up and/or builds the S02-T4 paired-delta tooling. **Out of Cycle-003** (NG12); recorded as a
  future option only.
- **OD-C3-6 — Build authorization (OA-2 equivalent).** A separate, explicit gate to implement the C3-FR-1/2/3
  specs. This PRD opens no gate.
- **OD-C3-7 — Admission timing.** Whether the eventual Rung-2 admission is a gated capstone of a later cycle or
  a standalone cycle. Not decided here.

## 14. Risks and mitigations

| ID | Risk | Mitigation |
|---|---|---|
| **R1** | **Value leak into tracked docs** — a dispersion value reaches a tracked artifact. | Schema enumerates forbidden fields + validator (C3-FR-1/2); `hygiene_check` parity; this PRD carries no values; NG4. |
| **R2** | **Scope-creep into admission** — the cycle drifts into asserting Rung 2 or advancing the ceiling. | NG1-NG3; ceiling held (§10); no row written (§8); the OD-6/criterion-2 output is a *proposal*, not a decision (§9). |
| **R3** | **Mis-resolved margin** — a procedure/margin chosen under the gravity of already-seen K=20 numbers. | Pre-registration procedure (margin fixed before numbers read); `M` deferred to a later gate; operator decides (OD-C3-1/2). |
| **R4** | **Scope-creep into evidence hardening** — K=50 / new eval runs / paired-delta tooling sneak in. | NG12; pure Option C; no eval run and no tooling build authorized; follow-ups recorded as future options only (OD-C3-5). |
| **R5** | **FunSearch creep** — a dependency/scaffold/heuristic surface is added. | NG10; appendix is notes-only (C3-FR-5). |
| **R6** | **Premature implementation** — schema/code built inside a planning cycle. | NG5; spec-only (NFR-8); building needs a separate `/implement` (OD-C3-6). |
| **R7** | **Cross-regime contamination** — a v002 figure compared to a v001 row. | NFR-3/NFR-5; specified single-regime guard; never compare across regimes. |
| **R8** | **Runtime-agent creep** — agent tuning/planning beyond "closed lane." | NG7; lane closed; agents frozen. |

## 15. Sources and traceability

> **Tracked sources (durable grounding):** `docs/cycles/cycle-002/closeout.md`;
> `docs/cycles/cycle-002/04-rung-2-readiness-criteria.md`; `docs/cycles/cycle-002/05-reproducibility-reality.md`;
> `docs/cycles/cycle-002/06-ledger-report-discipline.md`; `docs/cycles/cycle-002/07-operator-decision-register.md`;
> `docs/claim-ceiling.md`; `docs/ledger.md`; `docs/operator/turntrace-loop-contract.md`;
> `docs/operator/deferred-lane-gate-after-sprint-01.md`; `docs/cycles/cycle-000-bootstrap/01-turntrace-prd.md`
> (maturity ladder); `frozen/regimes/regime-v00{1,2}.json`; `frozen/seeds/seed-set-v002.json`;
> `analysis/dispersion_report.py`, `analysis/delta_report.py`.
> **Local decision input (gitignored State Zone, not a tracked dependency):**
> `grimoires/loa/a2a/cycle-003/pre-prd-research.md` (the pre-PRD research/decision pass; recommends
> Option C = Summary / Ledger Readiness).
> **Operator confirmations (this planning session):** PRD specifies-only (no artifacts/code); margin rule shape
> + procedure with the numeric `M` deferred; pure Option C with K=50 / paired-delta as Non-Goals.
> Current main at authoring: `37d7851`. Claim ceiling: **Rung 1 (unchanged).** This PRD opens no build gate.
