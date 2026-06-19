# Cycle-006 PRD — Rung-2 Admission-Seam Preparation: Pre-Register the Rule and Build the Promotion Gate

> Planning artifact (PRD). Status: **DRAFT — awaiting operator acceptance.** This PRD specifies a
> **preparation-and-hardening** cycle, but the PRD itself **opens no implementation gate**: code lands only
> through `/architect → /sprint-plan → /implement → /review-sprint → /audit-sprint → operator acceptance`
> (`docs/operator/turntrace-loop-contract.md` §6, the OA-2-class build-gate authorization). Cycle-006 resolves
> the **reversible-safe** half of the Rung-2 admission seam — ratifying the rule, recording the pre-registration
> procedure, designing fresh evidence, pre-registering the verdict rule, and preparing a promotion-mode gate — so
> that **Cycle-007** can become a clean, mechanical Rung-2 attempt *if the operator opens that gate*.
> **Cycle-006 attempts no Rung 2, produces no PASS/FAIL/INCONCLUSIVE verdict, promotes no value, generates no
> fresh evidence, writes no Rung-2 ledger row, and mutates neither the ledger nor the claim ceiling.**
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, Daily-Top-Episode data, or Competition Data appear here
> (CC-1/CC-2, ESP, SP-6/SP-9). **No dispersion metric values appear here** — evidence stays local/gitignored and
> is referenced qualitatively only. **No numeric margin `M` is chosen.** Runs are referenced by `run_id` pattern,
> count, hashes, sanitized metric *names*, claim ceilings, and local path/status only. The forbidden agent words
> (*strong / competitive / optimal / calibrated / complete*) and the inferential terms (*std-dev / variance / CI /
> p-value / significance / hypothesis-test / error-bar*) appear only as the negated/forbidden language they are.

## 0. State verified (2026-06-19, before drafting)

| Assumption to verify | Result |
|---|---|
| Current HEAD / branch | `main` @ `561fb92` — *docs: close TurnTrace Cycle-005 Sprint 01* (== `origin/main`) |
| Local branch not behind `origin/main` | `git ls-remote origin main` = `561fb92` — not behind |
| Cycle-005 status | **CLOSED — accepted, committed, pushed** (`docs/cycles/cycle-005/07-closeout.md`); hardening-only; Rung 1 held |
| `docs/ledger.md` byte-unchanged | **byte-unchanged**; `git diff --exit-code` clean; `hash-object = 2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` |
| `docs/claim-ceiling.md` unchanged | **unchanged**; `git diff --exit-code` clean; ceiling = **Rung 1** |
| Hardened gate present | `analysis/evidence_summary.py` (574 lines) + `tests/test_evidence_summary.py` (404 lines) tracked + accepted at `561fb92`; `--promotion-check` **absent** |
| No staged files | **none staged** |
| `.beads/issues.jsonl`, `grimoires/loa/NOTES.md` dirty | both modified, **unstaged** (pre-existing State-Zone housekeeping); **must not be staged** by this cycle |
| `.claude/` untouched | **no drift**; `integrity_enforcement: strict` → no HALT |
| `.claude/`/`frozen/`/`runs/`/`agents/`/`sim/`/`analysis/`/`tests/`/`eval/` drift | **none** (no tracked drift) |

**All assumptions hold. No finding forces a stop.** Implementation remains un-authorized until the operator
accepts this PRD and proceeds through `/architect → /sprint-plan → /implement`.

| Field | Value |
|---|---|
| **Cycle** | Cycle-006 |
| **Working title** | Rung-2 Admission-Seam Preparation: Pre-Register the Rule and Build the Promotion Gate |
| **Alt. framing** | Resolve the reversible-safe half of the Rung-2 admission seam — ratify 8a, record the `M` pre-registration procedure, design fresh evidence, pre-register the verdict rule, and prepare `--promotion-check` — **without** attempting Rung 2 |
| **Type** | Product Requirements Document (planning artifact for a preparation + one-sprint hardening cycle) |
| **Status** | DRAFT — awaiting operator acceptance; next Golden-Path step is SDD / architecture |
| **Date** | 2026-06-19 |
| **Current main** | `561fb92` — *docs: close TurnTrace Cycle-005 Sprint 01* |
| **Binding input** | local pre-PRD research pass (`grimoires/loa/a2a/cycle-006/00-pre-prd-research.md`, gitignored State Zone — research input, **not** authority; recommends **B — Admission-Seam Preparation**); the Cycle-005 closeout/audit + SDD §16 Cycle-006+ deferred items; the Cycle-003 design authorities (docs 04–08); the Cycle-002 readiness criteria; the competition-findings constraints (SP-8/SP-9, FM-10/FM-11) |
| **Posture** | **Preparation + one narrow hardening sprint.** Resolve the reversible-safe seam half in tracked planning artifacts; later authorize exactly one hardening-class code sprint (`--promotion-check`). Hold every other bright line |
| **Claim ceiling** | **Rung 1** (held for the whole cycle; not raised) |

## Required posture (binding)

- **Cycle-006 is preparation-only with respect to admission.** It resolves the reversible-safe half of the
  Rung-2 admission seam and, separately, authorizes one narrow hardening-class code sprint that builds a
  promotion-mode **gate** (`--promotion-check`). **Building a gate is not admitting Rung 2 and promotes nothing.**
- **Rung 1 remains held** for all of Cycle-006 (`docs/claim-ceiling.md:5-6`). **Rung 2 is unearned** — not
  pending approval, not claimed, not attempted. No "beats random-legal" verdict of any kind.
- **No Rung-2 admission attempt; no PASS/FAIL/INCONCLUSIVE verdict is applied** in Cycle-006. The verdict rule is
  *pre-registered for later use*, never *executed*.
- **No fresh evidence is generated.** Cycle-006 *designs* the Cycle-007 evidence batch; it runs no eval, no
  K-batch, no K=50 top-up, and reads no new runs.
- **No value promoted; no SP-6 issued.** No dispersion value reaches tracked status; the generator stays
  local-by-default; any exercise output stays gitignored.
- **No numeric margin `M` is chosen.** Cycle-006 records the `M` **pre-registration procedure**; it fixes no `M`,
  and it **must not** fix `M` against the already-observed K=20+20 bands (§10 contamination rule).
- **No Rung-2 ledger row.** `docs/ledger.md` stays **byte-unchanged** at its two Rung-1 `regime-v001` rows
  (`docs/ledger.md:11-12`; hash `2a2f1c2…`).
- **No claim-ceiling advance.** `docs/claim-ceiling.md` is unchanged; the ledger remains the only ceiling-bearing
  artifact.
- **OD-6 is not relaxed by execution.** Cycle-006 *ratifies the 8a posture* (recommended: the pre-registered
  descriptive disjoint-bands rule, which keeps OD-6 unrelaxed); it computes **no** inferential statistic.
- **The existing K=20+20 evidence is historical context only.** It may not be used as a verdict basis and may not
  be used to choose `M` (§10). A clean Rung-2 attempt requires **fresh, never-observed** same-regime evidence,
  generated only **after** `M` and the verdict rule are pre-registered.
- **No runtime-agent work; no gameplay-heuristic work; no broad optimization** (RL, self-play, deck optimizer,
  value/win-probability model, search/MCTS, ELO/tournament, dashboard, leaderboard); **no FunSearch surface;
  no cross-regime comparison; no regime mutation.**
- **No Kaggle / Daily Top Episodes ingest.** Daily Top Episodes remain **local-only hypothesis input, never
  proof of improvement** (SP-9).
- **Simulator behavior remains authoritative** over official-rule assumptions (SP-8): any verdict-relevant logic
  follows the simulator-offered legal options and the simulator terminal result.
- **No raw Competition Data / Pokémon Elements / traces / card names / deck lists / simulator logs** are
  committed or staged (CC-1/CC-2, ESP).
- **`.claude/` (System Zone) is never edited.** The promotion-check code is App Zone (`analysis/`, `tests/`);
  planning artifacts are State/Docs Zone. No State-Zone cleanup is performed by this cycle.

**The bright line for the whole cycle:** *Cycle-005 hardened the evidence-summary validator (C1–C4) so the gate
can be trusted in a load-bearing posture, and stopped before the admission seam. Cycle-006 resolves the
reversible-safe half of that seam — ratify the rule (8a), record the `M` pre-registration procedure (8b, no `M`),
design fresh evidence, pre-register the verdict rule and fail-state language, and prepare a promotion-mode gate
(`--promotion-check`) — while holding Rung 1, leaving `docs/ledger.md` byte-unchanged, promoting no value,
generating no evidence, and attempting no Rung 2. The Rung-2 attempt (8c/8d, fresh-evidence generation, verdict
application) is deferred to **Cycle-007 behind a separate explicit operator gate**.*

## 1. Product / cycle overview

TurnTrace is a local, sanitized evaluation harness for a card-game simulator. Across four cycles it has built
Rung-2 *readiness* without ever attempting Rung 2: Cycle-002 defined the five conjunctive readiness criteria;
Cycle-003 specified the evidence-summary schema, the generator/validator shape, the Rung-2 ledger convention,
and the OD-6 / criterion-2 (disjoint-bands) resolution *in shape*; Cycle-004 built the offline evidence-summary
generator + fail-closed validator (`analysis/evidence_summary.py`) and stopped at the seam; Cycle-005 hardened
that validator (C1–C4) and had it **reviewed and audited in a load-bearing-ready posture**
(`docs/cycles/cycle-005/06-audit-report.md`, PASS WITH NOTES — ACCEPTED).

The pre-PRD research for Cycle-006 (`grimoires/loa/a2a/cycle-006/00-pre-prd-research.md`) recommends **B —
Admission-Seam Preparation / Evidence Repair**: now that hardening has landed, the next disciplined step is to
resolve the *reversible-safe* governance/design half of the seam and prepare the promotion-mode tooling, leaving
the *irreversible* acts (first value promotion, first ceiling advance) and fresh-evidence generation to a
separate, explicit Cycle-007 gate. This honors the project's standing discipline — *"build readiness, then
advance as a separate explicit decision"* — and avoids the bundle the seam doc warns against
(`docs/cycles/cycle-003/07-od6-criterion-2-proposal.md` §5: *"Bundling them into one cycle is the
highest-consequence, hardest-to-walk-back path"*).

**Mission (binding).** Resolve the reversible-safe half of the Rung-2 admission seam so that Cycle-007 can become
a clean, mechanical Rung-2 attempt *if the operator opens that gate*. Concretely, Cycle-006 must: (a) ratify the
**8a posture** (recommended: the pre-registered descriptive disjoint-bands rule; alternative: OD-6 relaxation);
(b) record the **`M` pre-registration procedure** without choosing `M` and without reading the already-observed
bands; (c) **design** the Cycle-007 fresh-evidence batch (justified `n` / noise-floor reasoning, K≥20 same-regime
shape, never-observed-band requirement) **without generating it**; (d) **pre-register** the
PASS/FAIL/INCONCLUSIVE criteria and fail-state language for the later attempt; and (e) specify, at product level,
a hardened promotion-mode **gate** (`--promotion-check`) to be built in one narrow later sprint. Across all of it
**Rung 1 holds, `docs/ledger.md` stays byte-unchanged, no value is promoted, and no fresh evidence is
generated.**

**Who consumes this PRD.** The **operator** (accepts this PRD; ratifies the 8a posture; later opens both the
Cycle-006 build gate for the `--promotion-check` sprint and — separately — the Cycle-007 Rung-2 gate; the only
party who may ever issue SP-6, fix `M`, or advance the ceiling — none in Cycle-006); the
**architect/sprint-planner** (`/architect`, `/sprint-plan`, who resolve the SDD-level decisions named in §15);
the **implementer** (`/implement`, single patch authority, who lands `--promotion-check` and re-validates
citations against the build-time HEAD); and the **reviewer/auditor** (`/review-sprint`, `/audit-sprint`) who must
review and audit the promotion-mode gate **before** any Rung-2 attempt uses it.

## 2. Problem statement

Cycle-005 made the evidence-summary validator trustworthy, but a clean Rung-2 attempt is still not possible —
not for lack of machinery, but because the **reversible-safe half of the admission seam is unresolved** and one
piece of promotion-mode tooling is missing:

1. **The 8a posture is unratified.** Criterion 2 (an operator-approved *inferential* procedure) collides with
   OD-6 (which forbids inferential statistics). Cycle-003 resolved this *in shape* — recommending the
   pre-registered descriptive **disjoint-bands rule** *"candidate `min` > baseline `max` by ≥ `M` across `K ≥ 20`
   same-regime batches"* and presenting OD-6 relaxation as the alternative — but **decided nothing**
   (`docs/cycles/cycle-003/07-od6-criterion-2-proposal.md` §2/§4/§5). The rule a Cycle-007 attempt would apply is
   not yet ratified.
2. **The `M` pre-registration procedure is unrecorded, and the existing bands are contaminated for it.** `M` must
   be fixed **before** the comparison numbers are read as a verdict
   (`docs/cycles/cycle-003/07-od6-criterion-2-proposal.md` §3). The existing K=20+20 bands were **already locally
   generated** by the Cycle-004 exercise (`docs/cycles/cycle-005/01-prd.md` §8.3), so fixing `M` against that set
   would be post-hoc thresholding — *"the precise 'threshold chosen after seeing the numbers' failure that
   pre-registration exists to prevent."*
3. **No fresh-evidence design exists.** A clean attempt needs a fresh, never-observed same-regime K-batch under a
   **justified `n`** that clears the unseeded RNG noise floor
   (`docs/cycles/cycle-003/08-funsearch-forward-compat.md` §3); criterion 1's *"justified larger `n`"*
   (`docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` §2.1) is unestablished.
4. **The verdict rule and fail-state language are unwritten.** No PASS/FAIL/INCONCLUSIVE criteria are
   pre-registered, so a later attempt would risk defining success after the fact.
5. **The promotion-mode gate is absent.** The current module exposes `generate` and `--validate` only; there is
   **no `--promotion-check`** (grep at `561fb92`: 0 matches). The Cycle-005 audit recorded the binding floor that
   **a future promotion gate MUST hard-fail empty `hashes`** (CF-1; OD-C5-2 floor;
   `docs/cycles/cycle-005/06-audit-report.md` §11) — `--validate` correctly still accepts a structurally-valid
   empty `hashes` at exit 0, so a *separate* promotion-mode check is required.

None of these is itself a Rung-2 admission; all are **seam-preparation** problems. Cycle-006 resolves the
reversible-safe ones and prepares the gate; it does **not** cross the admission seam.

## 3. Accepted deferral statement (binding)

Cycle-006 **accepts** the pre-PRD research recommendation **B**. Explicitly and bindingly:

- **Rung 2 is unearned.** It is **not** pending approval; it is not claimed, implied, or attempted.
- **Cycle-006 produces no PASS / FAIL / INCONCLUSIVE admission verdict.** The verdict rule is *pre-registered for
  Cycle-007*, never *applied*.
- **Cycle-006 promotes no value** (no SP-6).
- **Cycle-006 writes no Rung-2 ledger row** (`docs/ledger.md` byte-unchanged).
- **Cycle-006 advances no claim ceiling** (`docs/claim-ceiling.md` unchanged; Rung 1 held).
- **Cycle-006 generates no fresh evidence batch** (no new eval runs).
- **The Rung-2 attempt is deferred to Cycle-007 behind a separate explicit operator gate.**

## 4. Goals — what Cycle-006 must produce

This is a **planning PRD**; the governance/design goals below are produced as tracked planning artifacts, and the
single code goal (G5) is specified for implementation under a later build gate — not implemented by this PRD.

- **G1 — 8a posture ratified.** Record the operator's ratification of the **8a** posture, with the
  **pre-registered descriptive disjoint-bands rule** as the recommended posture and OD-6 relaxation as the
  presented-not-recommended alternative. (Required operator decision for PRD acceptance — §18.)
- **G2 — `M` pre-registration procedure recorded (no `M`).** Specify the procedure by which `M` is fixed
  **before** any fresh band is read, recorded and dated, and **never** against the already-observed K=20+20 set.
  **No numeric `M` is chosen.**
- **G3 — Fresh-evidence batch designed (not generated).** Specify the Cycle-007 evidence batch: a **justified
  larger `n`** with explicit noise-floor reasoning, a **K ≥ 20 same-regime** shape, the **never-observed-band**
  requirement, and the provenance/audit-trail expectations (criterion 4). **No batch is generated; no eval runs.**
- **G4 — Verdict rule pre-registered.** Pre-register the **PASS / FAIL / INCONCLUSIVE** criteria and the
  **fail-state language** for the Cycle-007 attempt (§16.3), so success cannot be defined after the numbers.
- **G5 — Promotion-mode gate specified (one later sprint).** Specify, for one narrow hardening-class sprint to be
  implemented under a later build gate, a **`--promotion-check`** mode on `analysis/evidence_summary.py` that
  re-runs the full hardened validator and **hard-fails empty `hashes`**, with regression tests, preserving
  existing `generate`/`--validate` behaviour, and adding no schema file / second module / dependency / ledger
  write (§11, C6-FR-5). **No promotion is performed; the gate promotes nothing.**
- **G6 — Carry-forwards addressed.** CF-1 (promotion gate must hard-fail empty `hashes` — realised by G5);
  CF-2 (top-level duplicate-violation dedupe — only if the violation count becomes programmatic); CF-3 (document
  the C2 word-adjacency semantics if the negation rule is revisited) (§13).
- **G7 — Rung 1 held; ledger byte-unchanged; no value promoted; no fresh evidence (hard).** Across the whole
  cycle the ceiling stays Rung 1, `docs/ledger.md` stays byte-unchanged, `docs/claim-ceiling.md` is unchanged,
  no value reaches tracked status, and no fresh evidence batch is generated.

## 5. Scope

**In scope (Cycle-006).**
- Tracked planning/governance artifacts under `docs/cycles/cycle-006/` that ratify 8a, record the `M`
  pre-registration procedure, design the fresh-evidence batch, and pre-register the verdict rule + fail-state
  language (G1–G4).
- One narrow **hardening-class code sprint** (to be authorized through the loop contract after SDD/sprint-plan)
  that adds `--promotion-check` to `analysis/evidence_summary.py` and regression tests to
  `tests/test_evidence_summary.py` (G5). The only tracked code touched is those two files.
- Carry-forward bookkeeping CF-1/CF-2/CF-3 (G6).

**Out of scope (Cycle-006) — deferred to Cycle-007 behind a separate explicit operator gate.**
- Generating the fresh evidence batch (new eval runs).
- Fixing the numeric `M`.
- Issuing SP-6 (live-value promotion).
- Applying the verdict rule / producing a PASS·FAIL·INCONCLUSIVE result.
- Writing the Rung-2 ledger row / advancing the claim ceiling.

## 6. Non-goals (explicit)

Cycle-006 does **not** do any of the following:

- **No Rung-2 admission attempt;** **no "beats random-legal" verdict;** **no PASS/FAIL/INCONCLUSIVE verdict
  application.**
- **No numeric margin `M`** chosen — and in particular **no `M` chosen against the already-observed K=20+20
  bands.**
- **No SP-6** live-value promotion; no dispersion value promoted to tracked status.
- **No Rung-2 ledger row;** `docs/ledger.md` byte-unchanged. **No claim-ceiling advance;** `docs/claim-ceiling.md`
  unchanged.
- **No fresh-evidence generation; no new eval runs; no K=50 top-up; no K expansion.**
- **No cross-regime comparison; no inferential statistic computed; no OD-6 relaxation executed.**
- **No paired-delta tooling** except as a **future-only design note** for Cycle-007 (not built this cycle).
- **No runtime-agent implementation;** agents stay frozen. **No gameplay-heuristic work;** no broad optimization
  (RL, self-play, deck optimizer, value/win-probability model, search/MCTS, ELO/tournament, dashboard,
  leaderboard).
- **No FunSearch work** (no dependency, interface, scaffold, integration, or candidate-search surface).
- **No Daily Top Episodes ingestion; no Kaggle episode ingestion;** no Kaggle automation.
- **No raw Competition Data or Pokémon Elements in tracked docs;** no traces, simulator logs, deck lists, or
  Daily-Top-Episode data embedded.
- **No change to `.claude/`** (System Zone). **No State-Zone cleanup;** pre-existing dirty State-Zone files stay
  unstaged and untouched.
- **No new module** (`analysis/evidence_summary_validate.py`), **no `*.schema.json` file**, **no third-party
  dependency**, **no promotion mode that writes to `docs/ledger.md`** — the in-module constant, one-module, and
  stdlib-only posture are preserved.

## 7. Functional requirements

The FRs split into a **governance/design layer** (C6-FR-1…C6-FR-4, produced as tracked planning artifacts this
cycle) and a **hardening-class code layer** (C6-FR-5, specified now and implemented in one later sprint under the
build gate). Architecture-level choices are deferred to the SDD (§15); the FRs state **what** must hold.

### C6-FR-1 — Ratify the 8a posture (disjoint-bands rule vs OD-6 relaxation)

1. Cycle-006 MUST record the operator's ratification of the **8a** posture
   (`docs/cycles/cycle-003/07-od6-criterion-2-proposal.md` §5, seam decision 8a).
2. The **recommended** posture is the **pre-registered descriptive disjoint-bands rule**:
   *"candidate `min` > baseline `max` by ≥ `M` across `K ≥ 20` same-regime batches,"* expressed using **only** the
   allowed descriptive vocabulary (`count / min / max / range / mean / median / spread`), adding **no field and no
   statistic** to the schema, and keeping **OD-6 unrelaxed** (`07` §2).
3. The **alternative** — relax OD-6 for a genuine inferential test — MUST be presented as the
   presented-not-recommended, heavier-consequence path requiring its own explicit ratification (`07` §4). It is
   not adopted unless the operator chooses it.
4. This is a **required operator decision for PRD acceptance** (§18, OD-C6-1). Cycle-006 computes **no**
   inferential result and writes **no** verdict; it only ratifies which rule a Cycle-007 attempt would apply.

### C6-FR-2 — Record the `M` pre-registration procedure (no `M` chosen)

1. Cycle-006 MUST record the **procedure** by which the numeric margin `M` is fixed: the operator ratifies the
   rule and **fixes `M` in advance**, as part of the approved design, **before** any band is read as a verdict
   (`07` §3; `docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` §2.3).
2. The procedure MUST require `M` to be **recorded and dated** (and, for the Cycle-007 attempt, fixed **before**
   the fresh evidence is generated/read), so the threshold cannot be chosen after seeing the numbers.
3. Cycle-006 **MUST NOT choose `M`**, and **MUST NOT** fix `M` against the already-observed K=20+20 bands
   (§10 contamination rule). **No numeric `M` value appears in any Cycle-006 artifact.**

### C6-FR-3 — Design the Cycle-007 fresh-evidence batch (no generation)

1. Cycle-006 MUST specify the **design** of the Cycle-007 evidence batch as a tracked planning artifact, with
   **no batch generated and no eval run executed** (NG12).
2. The design MUST include: (a) a **justified larger `n`** with explicit **noise-floor reasoning** — the
   evaluator must average over enough matches/batches to clear the unseeded RNG noise floor before a
   per-candidate signal is stable (`08` §3; criterion 1, `04-rung-2-readiness-criteria.md` §2.1); (b) a **K ≥ 20
   same-regime** batch shape under a single frozen `regime-vNNN` (a larger `n` is a *new* regime, never an edit;
   `04-rung-2-readiness-criteria.md` §2.1; NFR-5); (c) the **never-observed-band requirement** — the batch is
   generated only **after** `M` and the verdict rule are pre-registered, and is distinct from the already-observed
   K=20+20 set; (d) the **provenance/audit-trail** expectations (source-hash provenance, per-decision canonical
   traces, `trace_hash`, regime tuple stamp; criterion 4).
3. The design MUST state that generating this batch is **new eval scope** (NG12) and a **separate operator
   decision** belonging to Cycle-007, never executed in Cycle-006.

### C6-FR-4 — Pre-register the PASS / FAIL / INCONCLUSIVE rule + fail-state language

1. Cycle-006 MUST pre-register, as a tracked planning artifact, the **PASS / FAIL / INCONCLUSIVE** criteria and
   the **fail-state language** to be **applied in Cycle-007**, never applied in Cycle-006 (§16.3).
2. The criteria MUST be expressed against the ratified 8a rule and the pre-registered `M`, on a **fresh,
   never-observed** same-regime batch, with the verdict honouring the contamination and fresh-evidence posture
   (§10) and the same-regime-only constraint (NFR-5).
3. The fail-state language MUST make explicit that a **FAIL or INCONCLUSIVE** attempt **advances no ceiling,
   promotes no value, writes no Rung-2 row**, regresses nothing, and is recorded honestly at Rung 1 — and that
   `M` or the rule is **never** re-picked after the bands to manufacture a PASS.

### C6-FR-5 — Promotion-mode gate `--promotion-check` (one later hardening sprint)

Specified now; implemented in one narrow hardening-class sprint under a later build gate. The only tracked code
touched is `analysis/evidence_summary.py` + `tests/test_evidence_summary.py`.

1. The module MUST gain a **`--promotion-check <summary.json>`** mode that **re-runs the full hardened validator**
   (`validate_summary` + the `--validate` re-read-from-disk semantics) over the candidate summary.
2. `--promotion-check` MUST **hard-fail an empty `hashes`** integrity stamp (the OD-C5-2 floor / CF-1;
   `docs/cycles/cycle-005/06-audit-report.md` §11) — i.e. an empty/absent integrity stamp is a non-zero,
   fail-closed exit, **not** the exit-0 acceptance `--validate` correctly retains.
3. `--promotion-check` MUST have **no promotion side effects**: it **promotes nothing**, writes **no** tracked
   artifact, and **never** writes to `docs/ledger.md` or any tracked `docs/` path (the C3 `--out` guard and the
   ledger byte-invariance continue to hold independently). It is a **gate**, not a promoter.
4. Existing behaviour MUST be **preserved**: generate-mode emits its empty-`hashes` **stderr WARNING at exit 0**
   (`analysis/evidence_summary.py:553`); `--validate` continues to **structurally accept** a valid empty `hashes`
   at exit 0; the `0/1/2/3` exit contract is preserved (a new exit code for the promotion hard-fail is permitted
   **only** if the SDD justifies it — OD-C6-3; the empty-`hashes` hard-fail most naturally rides the exit-3
   leak-class path).
5. The implementation MUST add **no `*.schema.json` file, no second validator module, no third-party
   dependency**, and **no promotion mode that writes to `docs/ledger.md`** — the in-module constant / one-module /
   stdlib-only / analysis-only-imports posture is preserved (`tests/test_import_direction.py` green).
6. Each behaviour MUST leave at least one **runnable regression check** in `tests/test_evidence_summary.py`
   (promotion-check passes a good summary at exit 0; hard-fails an empty-`hashes` summary; re-runs the full
   validator so a leak still fails; preserves generate-warning and `--validate` empty-`hashes` acceptance), with
   the existing 12 + block-13 checks remaining green. Fixtures are stdlib-only synthetic — **no K-batch
   dependency, no raw data.**

## 8. Non-functional / claim-ceiling requirements

- **NFR-1 — Conservative-only (code).** The `--promotion-check` sprint makes the gate **stricter or equal**,
  never looser: it adds a stricter mode and adds rejections (empty `hashes`); it removes none. No input the
  hardened `--validate` rejects becomes accepted.
- **NFR-2 — Compatibility.** Existing `generate` and `--validate` behaviour and emitted shape stay compatible;
  the **12 existing + block-13 checks remain green**; new behaviour is additive.
- **NFR-3 — Stdlib-only / analysis-only imports preserved.** No `cabt`/`cg`, `sim/`, `agents/runtime/`, or
  `eval/` import; no third-party dependency; the in-module allow-list stays the single source of truth (no
  `*.schema.json`, no second module). Enforced by `tests/test_import_direction.py`.
- **NFR-4 — Read/write surface unchanged.** Read surface stays `manifest.json` + `match_results/*` (via
  `aggregate_run`) + the `--validate`/`--promotion-check` file; **no `hashes.txt`** read; no sidecar/`traces/`
  reference. Write surface stays local-by-default; **never `docs/`, never a ledger row** — `--promotion-check`
  writes nothing.
- **NFR-5 — Same-regime only.** The single-regime guard (exit 2) is preserved; **no cross-regime field or
  comparison** is introduced anywhere (planning artifacts included); a `regime-v002` band is never compared to a
  `regime-v001` band.
- **NFR-6 — Claim-safety.** **Rung 1 held**; forbidden agent words negated-only; **no inferential result
  produced** — the validator *rejects* inferential terms, and the ratified disjoint-bands rule is descriptive, not
  inferential.
- **NFR-7 — Sanitization.** Competition Data and Pokémon Elements never enter git (CC-1/CC-2, ESP);
  `eval/hygiene_check.py` remains the staging gate; the validator (and `--promotion-check`) stay
  sanitization-parity-or-stricter.
- **NFR-8 — Simulator-authoritative (SP-8 / CC-10).** Any verdict-relevant logic follows simulator-offered legal
  options and the simulator terminal result, never official-rule assumptions. (No verdict logic is built this
  cycle; this is a standing constraint carried into the Cycle-007 design.)
- **NFR-9 — Implement-time citation revalidation.** The line anchors in this PRD are line-anchored to
  `analysis/evidence_summary.py` at HEAD `561fb92`. `/implement` MUST re-validate every anchor it relies on
  against the **build-time HEAD** before coding; anchors accurate now may desync if the file moves.
- **NFR-10 — Zone discipline.** Promotion-check code is tracked App Zone (`analysis/`, `tests/`); planning
  artifacts are Docs/State Zone; `.claude/` is never touched; State-Zone files stay unstaged.
- **NFR-11 — Claim-ceiling invariance (hard).** `docs/ledger.md` byte-unchanged (`2a2f1c2…`);
  `docs/claim-ceiling.md` unchanged; Rung 1 held for the whole cycle; the ledger remains the only ceiling-bearing
  artifact; the evidence summary continues to carry **no ceiling of its own**
  (`docs/cycles/cycle-003/04-evidence-summary-schema-spec.md` §1).

## 9. Admission-seam decisions (8a–8d)

The four conjunctive seam decisions (`docs/cycles/cycle-003/07-od6-criterion-2-proposal.md` §5), with what
Cycle-006 does for each:

| Seam | Decision | Cycle-006 action |
|---|---|---|
| **8a** | Descriptive disjoint-bands rule **vs** OD-6 relaxation | **Ratified (operator, 2026-06-19): the pre-registered descriptive disjoint-bands rule** (OD-C6-1); OD-6 relaxation not adopted. Computes no inferential result. |
| **8b** | Numeric margin `M` | **Procedure only — no `M`.** Record the pre-registration procedure; fix no `M`; never read the already-observed bands (§10). |
| **8c** | SP-6 live-value promotion | **Deferred to Cycle-007.** Not issued. The `--promotion-check` *gate* is prepared, but it promotes nothing. |
| **8d** | Rung-2 ledger row / claim-ceiling advance | **Deferred to Cycle-007.** Not written; ceiling stays Rung 1; `docs/ledger.md` byte-unchanged. |

**Reaffirmed (not done in Cycle-006):** `M` unset; SP-6 not issued; OD-6 not relaxed by execution; no Rung-2 row;
no ceiling advance; the irreversible acts (8c/8d) and fresh-evidence generation belong to **Cycle-007 behind a
separate explicit operator gate**.

## 10. Contamination / fresh-evidence posture (binding)

- **The existing K=20+20 evidence is historical context only.** The Cycle-004 local exercise generated the
  evidence summary over exactly those sealed run dirs, so the bands are **already locally accessible**
  (`docs/cycles/cycle-005/01-prd.md` §8.3; `docs/cycles/cycle-004/04-implementation-report.md` §4 T6). That set
  was sufficient to *exercise the machinery* and may serve as background context **only**.
- **It must not be the verdict basis, and must not be used to choose `M`.** Fixing `M` against an already-observed
  set is post-hoc thresholding — *"the precise 'threshold chosen after seeing the numbers' failure that
  pre-registration exists to prevent"* (`07` §3). This is the in-house analogue of **FM-11** (contaminated
  evidence): no improvement claim without a clean same-regime comparison.
- **A clean Rung-2 attempt requires fresh, never-observed same-regime evidence,** generated **only after** `M` and
  the verdict rule are pre-registered, under a **justified `n`** that clears the unseeded noise floor (`08` §3).
- **Operator-attestation fallback (non-preferred).** An explicit operator attestation accepting a weakened
  pre-registration against the already-observed set is *documentable* but strictly weaker, and is not recommended
  for the first-ever ceiling advance. Fresh evidence is the on-ethos choice. (This is a Cycle-007 operator
  decision, not a Cycle-006 action.)

## 11. Promotion-check requirement (product level)

At product/requirements level (architecture → SDD), the promotion-mode gate `--promotion-check` MUST:

1. **Re-run the full hardened validator** over the candidate summary (the same content checks as `--validate`,
   re-read from disk).
2. **Hard-fail empty `hashes`** — an empty/absent integrity stamp is a non-zero, fail-closed exit (CF-1 / OD-C5-2
   floor), because a Rung-2 row cites the promoted summary **by reference + content hash**
   (`docs/cycles/cycle-003/06-rung-2-ledger-convention.md` §3), so a silently-empty stamp is unacceptable at
   promotion.
3. **Have no promotion side effects** — it promotes nothing, writes no tracked artifact, and never writes to
   `docs/ledger.md` or any tracked `docs/` path. It is the gate a *future* promotion must pass, not a promoter.

It MUST also **preserve** the existing generate-mode empty-`hashes` **warning (exit 0)** and `--validate`
structural **acceptance of a valid empty `hashes` (exit 0)**, and add **no schema file, no second validator
module, no third-party dependency, and no ledger write.** *(`--promotion-check` does not promote anything; it
only gates a future promotion.)*

## 12. Claim-ceiling posture

The loop sits at **ladder Rung 1 — legal completion / throughput / audit-trail**, and **Cycle-006 keeps the
ceiling at Rung 1** for the whole cycle (`docs/claim-ceiling.md`):

```
Rung 0  env not trusted
Rung 1  legal completion                         ← current, and held for all of Cycle-006
Rung 2  beats random-legal                       ← admission machinery PREPARED here (rule ratified, gate built); UNEARNED; attempt = a separate gate (Cycle-007)
Rung 3  beats scripted / prior best, ablation-backed
Rung 4  stable, report-ready
```

**Allowed claim form** — relative, local, descriptive, carrying its `n`, `K`, and `regime_id`. **Forbidden claim
forms** (negated-only): gameplay strength; statistical significance; cross-regime uplift; leaderboard quality;
calibration; optimality; competitiveness. Only the ledger, advanced by a separate explicit later operator
decision, can carry a higher rung. **Cycle-006 advances nothing; it ratifies the rule and prepares the gate a
later attempt would use.**

## 13. Cycle-005 carry-forwards addressed

| CF | Carry-forward (`docs/cycles/cycle-005/06-audit-report.md` §11) | Cycle-006 disposition |
|---|---|---|
| **CF-1** | A future promotion gate MUST hard-fail empty `hashes`. | **Realised** by C6-FR-5 / §11 — `--promotion-check` hard-fails empty `hashes`. |
| **CF-2** | Optional top-level duplicate-violation dedupe — only if the printed violation count becomes programmatic. | **Conditional.** Dedupe **only if** `--promotion-check` consumes the violation count programmatically; if it keys solely on exit code, no dedupe is needed (SDD decides — OD-C6-4). |
| **CF-3** | Document the C2 word-adjacency ("no intervening content word") semantics if the negation rule is revisited. | **Documentation note.** Record the semantics in the SDD/implementation report **only if** C2 is touched; Cycle-006 does not otherwise revisit C2. |

## 14. Safety and sanitization constraints

Carried verbatim-in-intent from the standing rules (`docs/operator/turntrace-loop-contract.md` §7-§8;
`docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` SP-6/SP-8/SP-9):

- **Competition Data never enters git** (CC-1/CC-2): the `cg/` SDK, card data, raw deck lists, `deck.csv` —
  local-only under gitignored `grimoires/loa/context/`.
- **Pokémon Elements never appear in tracked artifacts.**
- **Generated runs, dispersion values, and the generator's output** stay local/gitignored; tracked artifacts hold
  sanitized code + specs only. **No `M` value** appears in any tracked artifact.
- **Daily Top Episodes / raw episode datasets** stay local/ignored (SP-9, same ESP discipline); never tracked,
  never a runtime dependency; **never Rung-2 proof** without a same-regime TurnTrace comparison (FM-11).
- **Simulator behavior is authoritative** (SP-8 / CC-10); official-rule assumptions must not override it (FM-10).
- **`eval/hygiene_check.py`** remains the mechanical staging gate; `--promotion-check` and the validator stay
  sanitization-parity-or-stricter.
- **Forbidden agent claim words** appear only as negated/forbidden language.

## 15. Open decisions deferred to SDD

Named here, **not** decided in this PRD:

- **OD-C6-2 — `--promotion-check` internal shape.** Whether it calls `validate_summary` wholesale and layers an
  empty-`hashes` precheck, or composes a single pass; the exact CLI surface and help text.
- **OD-C6-3 — exit-code behaviour for the promotion hard-fail.** Whether the empty-`hashes` hard-fail rides the
  existing **exit-3 leak-class** path (preferred; preserves the `0/1/2/3` contract per OD-C5-5 precedent) or a
  justified new code. Floor: a non-zero, fail-closed exit; never exit 0 on empty `hashes` in promotion mode.
- **OD-C6-4 — CF-2 dedupe.** Whether to de-duplicate the top-level duplicate-violation count — required **only**
  if `--promotion-check` exposes the violation count programmatically.
- **OD-C6-5 — test layout.** The exact placement of the new `--promotion-check` regression checks within
  `tests/test_evidence_summary.py` (e.g. a new block after block 13), reusing existing stdlib-only fixtures.
- **OD-C6-6 — artifact placement for the governance/design deliverables.** Where the ratified-8a record, the `M`
  pre-registration procedure, the fresh-evidence batch design, and the pre-registered verdict rule live under
  `docs/cycles/cycle-006/` (e.g. numbered companion docs), and the reporting language binding them to the
  prep-only posture.
- **Reaffirmed (not decided in Cycle-006):** `M` unset; SP-6 not issued; OD-6 not relaxed by execution; Rung-2
  attempt = a separate later gate — 8c/8d and fresh-evidence generation stay deferred to Cycle-007.

> **OD-C6-1 (8a posture)** is **not** an SDD decision — it was a **required operator decision for PRD acceptance**
> (§18), now **ratified: the pre-registered descriptive disjoint-bands rule** (operator, 2026-06-19). The SDD
> assumes this settled posture as input.

## 16. Success criteria

### 16.1 Planning-cycle success (this PRD)

- This PRD is accepted by the operator (with the **8a posture ratified** — OD-C6-1) and proceeds to `/architect`
  (SDD), not directly to implementation.
- It is **grounded** in the pre-PRD research and the tracked authorities; it is clearly **prep-only**; it records
  the `M` pre-registration procedure **without choosing `M`** from observed bands; it specifies the fresh-evidence
  batch design **without generating it**; it pre-registers the PASS/FAIL/INCONCLUSIVE criteria + fail-state
  language for later use; it specifies the `--promotion-check` requirement at product level (full validator
  re-run, empty-`hashes` hard-fail, no promotion side effects); and it addresses CF-1/CF-2/CF-3.
- **Rung 1 is held;** `docs/ledger.md` is byte-unchanged (`2a2f1c2…`); `docs/claim-ceiling.md` is unchanged; no
  value is promoted; no fresh evidence is generated; no raw Competition Data / Pokémon Elements / traces /
  simulator logs / deck lists / Daily-Top-Episode data are embedded; `.claude/` is untouched; State-Zone files
  stay unstaged; **the Rung-2 attempt is explicitly deferred to Cycle-007 behind a separate explicit operator
  gate.**

### 16.2 Build-cycle acceptance criteria — the `--promotion-check` sprint (when the code lands under `/implement`, a later gate)

- **AC-1 — promotion-check passes a good summary:** `--promotion-check` on a clean, non-empty-`hashes`,
  schema-conforming summary → exit 0.
- **AC-2 — empty-`hashes` hard-fail:** `--promotion-check` on a structurally-valid but **empty-`hashes`** summary
  → **non-zero, fail-closed** (CF-1 / OD-C5-2 floor).
- **AC-3 — full validator re-run:** a summary carrying any forbidden field/value/word still fails under
  `--promotion-check` (it re-runs the full hardened validator).
- **AC-4 — existing behaviour preserved:** generate-mode still emits the empty-`hashes` **WARNING at exit 0**;
  `--validate` still **accepts** a valid empty `hashes` at exit 0; the `0/1/2/3` contract holds (or a single
  SDD-justified addition per OD-C6-3).
- **AC-5 — no promotion side effects:** `--promotion-check` writes nothing; `docs/ledger.md` byte-unchanged
  (`2a2f1c2…`); no tracked `docs/` write.
- **AC-6 — tests:** each behaviour has at least one runnable regression check; **all existing 12 + block-13 checks
  remain green**; `tests/test_import_direction.py` green; `eval/hygiene_check.py --paths …` exit 0 on tracked
  artifacts.
- **AC-7 — posture held (hard):** Rung 1 held; `docs/claim-ceiling.md` unchanged; no value promoted; stdlib-only /
  analysis-only imports; no `M`/SP-6/Rung-2 row; no `.claude/` drift; State-Zone files unstaged; **no second
  module / `*.schema.json` / dependency / ledger write.**
- **AC-8 — cadence:** lands through `/implement → /review-sprint → /audit-sprint → operator acceptance`, so the
  promotion-mode gate is **reviewed and audited before any Rung-2 attempt uses it.**

### 16.3 Pre-registered verdict rule for Cycle-007 (recorded now; applied only in Cycle-007)

> Pre-registered here so success cannot be defined after the numbers. **Applied only in Cycle-007**, on a fresh,
> never-observed same-regime K≥20 batch, under the ratified 8a rule and a pre-registered `M`. Cycle-006 applies
> none of it.

- **PASS** — under the pre-registered disjoint-bands rule, with `M` fixed **before** the bands were read:
  *candidate `min` exceeds baseline `max` by ≥ `M`* across the fresh K≥20 same-regime batch; the promoted summary
  passes `--validate` **and** `--promotion-check` (non-empty integrity stamp, full validator clean);
  provenance/audit-trail intact; the justified-`n` / noise-floor argument satisfied. → the operator **may** issue
  SP-6 (8c), write the Rung-2 row citing the summary by reference + content hash (8d), and advance `claim_ceiling`
  to Rung 2. *(Even a PASS keeps the forbidden agent words forbidden — the verdict is "candidate beats the
  random-legal baseline by the pre-registered descriptive margin under this regime," nothing about being
  strong / competitive / optimal / calibrated / complete.)*
- **FAIL** — the pre-registered margin is **not** met (candidate `min` does not exceed baseline `max` by ≥ `M`).
  → **no** ceiling advance; **no** promotion; record the descriptive result honestly at **Rung 1**. A FAIL is an
  honest negative result, not a defect; it does not regress Rung 1; `M` and the rule are **never** re-picked after
  the bands to manufacture a PASS.
- **INCONCLUSIVE** — a precondition is unmet at attempt time: `n` insufficient to clear the noise floor; bands
  neither cleanly disjoint-by-`M` nor cleanly not, under unseeded noise; provenance/hashes incomplete; or
  `--promotion-check` fails on integrity. → **no** ceiling advance; **no** promotion; remediate the unmet
  precondition (more batches, fix provenance) and re-attempt under the **same** pre-registered `M`/rule. Never
  relax `M` or the rule post-hoc.
- **Fail-state language (Rung 2 not earned).** A FAIL or INCONCLUSIVE attempt **advances no ceiling, promotes no
  value, writes no Rung-2 row** (or writes only a Rung-1 descriptive note), and is recorded faithfully. The loop
  stays at Rung 1; the candidate is **not** shown to beat random-legal at the pre-registered margin under this
  regime; no forbidden agent word may be applied.

## 17. Risks and mitigations

| ID | Risk | Mitigation |
|---|---|---|
| **R1** | **Scope-creep into admission** — prep drifts into a verdict / `M` / promotion / ceiling advance. | §3 accepted deferral; §6 non-goals; §9 8c/8d deferred; no `M`, no SP-6, no row; `--promotion-check` promotes nothing (§11). |
| **R2** | **Pre-registration contamination** — `M` chosen against the already-observed K=20+20 bands. | §10 contamination rule; C6-FR-2.3 forbids it; **no `M` in any Cycle-006 artifact**; fresh never-observed evidence required for Cycle-007. |
| **R3** | **`--promotion-check` loosens or duplicates the gate.** | NFR-1 conservative-only; re-runs the full validator (C6-FR-5.1); existing 12 + block-13 checks green (AC-6); empty-`hashes` hard-fail regression (AC-2). |
| **R4** | **Ledger / docs mutation** via the promotion-check or `--out`. | `--promotion-check` writes nothing (C6-FR-5.3/§11); C3 `--out` guard preserved; `git diff --exit-code -- docs/ledger.md` byte-unchanged (AC-5). |
| **R5** | **Dependency / second-module / `.schema.json` creep** while adding `--promotion-check`. | NFR-3; §6 non-goals; import-direction test; in-module constant preserved (C6-FR-5.5). |
| **R6** | **Citation rot** — the line anchors desync from source before build. | NFR-9: `/implement` re-validates anchors at build-time HEAD. |
| **R7** | **8a left unratified** — the SDD proceeds against an unsettled rule. | OD-C6-1 is a required operator decision for PRD acceptance (§18); the SDD assumes the ratified posture. |
| **R8** | **FM-10 (official-rule assumption mismatch).** | NFR-8 simulator-authoritative; no verdict logic built; record any divergence as a simulator-behavior note, not an agent failure. |
| **R9** | **FM-11 (top-episode overfitting / contaminated evidence).** | §10/§14: no episode ingest; episodes are hypothesis-only; the in-house contamination rule forbids verdicts on already-observed bands; raw-data-in-git mechanically caught by `eval/hygiene_check.py` + validator hygiene parity. |
| **R10** | **Premature fresh-evidence generation** — a prep cycle runs an eval batch. | C6-FR-3.3: generation is NG12, new eval scope, a separate Cycle-007 operator decision; HALT if attempted. |

## 18. Operator decisions required before SDD (`/architect`)

| ID | Decision | Status |
|---|---|---|
| **OD-C6-1 — 8a posture** | Ratify the **8a** posture: the **pre-registered descriptive disjoint-bands rule** (recommended) **vs** OD-6 relaxation (presented, not recommended). | **Ratified (operator, 2026-06-19): the pre-registered descriptive disjoint-bands rule;** OD-6 relaxation not adopted. The SDD assumes this settled posture. |
| **Build gate (OA-2-class) — `--promotion-check` sprint** | The operator opens the later build gate for the Cycle-006 `--promotion-check` hardening sprint, scoped to `analysis/evidence_summary.py` + `tests/test_evidence_summary.py` only (`docs/operator/turntrace-loop-contract.md` §6). | **Required to proceed to `/implement`** — operator action after SDD/sprint-plan; this PRD does not self-authorize. |
| **D-1** | Cycle-006 = **preparation + one narrow hardening sprint**; admission deferred to Cycle-007. | **Decided** (this PRD). |
| **D-2** | `--promotion-check` makes the gate **stricter or equal**, never looser; existing `generate`/`--validate` behaviour preserved. | **Decided** (this PRD). |
| **D-3** | **In-module constant / stdlib-only / one-module** posture preserved (no `.schema.json`, no second module, no dependency, no ledger write). | **Decided** (this PRD). |
| **`M` / SP-6 / Rung-2 row / ceiling advance / fresh evidence** | Unset / not issued / not written / not advanced / not generated. | **Deferred** to the Cycle-007 gate — **none in Cycle-006.** |

## 19. Explicit Cycle-007 handoff gate

A Cycle-007 Rung-2 *attempt* may proceed **only** when **all** of the following hold, and only behind a **separate
explicit operator gate** (`docs/cycles/cycle-005/02-sdd.md` §16; `01-prd.md` §8.6 — *"only after Cycle-005 passes
review/audit and an explicit operator gate opens"*):

1. **Cycle-006 accepted** (this PRD, the governance/design artifacts, and the `--promotion-check` sprint —
   reviewed + audited + live).
2. **8a ratified** (OD-C6-1) — the rule a Cycle-007 attempt applies is settled.
3. **`M` pre-registered** under the recorded procedure (C6-FR-2), fixed **before** any fresh band is
   generated/read, and **never** against the already-observed K=20+20 set.
4. **A fresh, never-observed same-regime K≥20 batch generated** under a justified `n` that clears the noise floor
   (C6-FR-3) — new eval scope (NG12), a separate operator decision.
5. **`--promotion-check` live** — the promoted candidate summary passes `--validate` **and** `--promotion-check`
   (non-empty integrity stamp, full validator clean).
6. **Provenance/audit-trail intact** (criterion 4) and the verdict is a **same-regime** TurnTrace descriptive
   delta, never episode-derived (FM-11).
7. **The five conjunctive Rung-2 readiness criteria** all hold
   (`docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` §2).
8. **An explicit operator gate opens** the Cycle-007 Rung-2 attempt.

Only then is the pre-registered verdict rule (§16.3) **applied**; only on **PASS** do SP-6 (8c) + the Rung-2 row +
ceiling advance (8d) follow, each a separate operator act. **Any unmet item → the Rung-2 attempt defers again.**
**The Rung-2 attempt is deferred to Cycle-007 behind a separate explicit operator gate.**

## 20. Sources and traceability

> **Local decision input (gitignored State Zone, not a tracked dependency):**
> `grimoires/loa/a2a/cycle-006/00-pre-prd-research.md` (the pre-PRD research pass; recommends **B —
> Admission-Seam Preparation / Evidence Repair**; Rung-2 attempt deferred to Cycle-007).
> **Tracked Cycle-005 authorities:** `docs/cycles/cycle-005/07-closeout.md` (closed/accepted/pushed; Rung 1 held;
> §4 carry-forwards CF-1/CF-2/CF-3 and the Rung-2 admission seam); `06-audit-report.md` (§11 CF-1/CF-2/CF-3 —
> CF-1: promotion gate MUST hard-fail empty `hashes`); `02-sdd.md` (§6 OD-C5-1…6; §16 deferred Cycle-006+ items —
> `--promotion-check`, seam 8a–8d, defensible `M` pre-registration, five readiness criteria, "only after
> review/audit and an explicit operator gate"); `01-prd.md` (§8 why Rung 2 was deferred; §8.3 K=20+20 contamination).
> **Tracked code (the gate, anchors at `561fb92`):** `analysis/evidence_summary.py` (`SAFE_FIELDS` `:83`;
> `_SHA256_RE` `:107`; `_manifest_run_hash` `:117`; `build_summary` `:135`; `_NEG_WINDOW` `:270`;
> `_affirmative_forbidden_words` `:307`; `_enforce_hashes_digest` `:347`; `_walk` `:366` (wired `:381`);
> `validate_summary` `:392` (top-level digest block `:411`); `_refuse_tracked_out` `:449`; `_run_validate` `:477`;
> `main` `:509`; empty-`hashes` WARNING `:553`; exit set `0/1/2/3`; **no `--promotion-check` token**; **no
> `hashes.txt`**); `tests/test_evidence_summary.py` (12 + block-13 checks).
> **Tracked Cycle-003 design authorities:** `04-evidence-summary-schema-spec.md` (§2 safe fields, §3 forbidden
> classes, §4 JSON-first shape; summary carries no ceiling); `05-generator-validator-shape.md` (§2 allow-list /
> single-regime exit 2 / exit-code contract / hygiene parity; NG12); `06-rung-2-ledger-convention.md` (§1 row
> reuses 18-col schema verbatim; §2 same-regime agent-only verdict; §3 row cites summary by reference + hash);
> `07-od6-criterion-2-proposal.md` (§2 disjoint-bands rule; §3 pre-registration procedure; §4 OD-6-relaxation
> alternative; §5 seam 8a–8d — bundling is "the highest-consequence, hardest-to-walk-back path");
> `08-funsearch-forward-compat.md` (§3 unseeded noise floor; NG7/NG8/NG10 — runtime-agent lane closed).
> **Tracked posture docs:** `docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` §2 (five conjunctive
> criteria); `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` (SP-6/SP-8/SP-9); `docs/failure-modes.md`
> (FM-10/FM-11); `docs/claim-ceiling.md` (Rung 1; forbidden words; never compare across regimes);
> `docs/ledger.md` (two Rung-1 rows; hash `2a2f1c2…`); `docs/operator/turntrace-loop-contract.md` (§6 build gate;
> §7-§8 hygiene/claim language).
> Current main at authoring: `561fb92`. Claim ceiling: **Rung 1 (unchanged).** This PRD opens no implementation
> gate, builds no code, generates no evidence, mutates no ledger, advances no ceiling, promotes no value, applies
> no admission verdict, chooses no `M`, and edits no `.claude/`. **The Rung-2 attempt is deferred to Cycle-007
> behind a separate explicit operator gate.**
