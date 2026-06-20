# Cycle-007 PRD — Gated Rung-2 Admission Attempt: Pre-Register, Generate Fresh Same-Regime Evidence, Apply the Verdict

> Planning artifact (PRD). Status: **DRAFT — awaiting operator acceptance.** This PRD specifies a **gated Rung-2
> admission-attempt** cycle (research Option A), but the PRD itself **opens no implementation gate and authorizes no
> irreversible act**: code lands only through `/architect → /sprint-plan → /implement → /review-sprint → /audit-sprint →
> operator acceptance` (`docs/operator/turntrace-loop-contract.md` §1, §6; OA-2-class build gate), and the Rung-2 *attempt*
> proceeds only behind the **separate explicit operator gate** the research and the Cycle-006 handoff require
> (`grimoires/loa/a2a/cycle-007/00-pre-prd-research.md` §15; `docs/cycles/cycle-006/01-prd.md` §19). **This PRD-drafting
> pass chooses no numeric margin `M`, generates no fresh evidence, runs no eval, applies no PASS/FAIL/INCONCLUSIVE verdict,
> issues no SP-6, promotes no value, writes no Rung-2 ledger row, and advances no claim ceiling.** It defines *what the
> Cycle-007 attempt must hold* at product/governance level; it does not design the SDD or sprint plan.
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs, `deck.csv`
> rows, run-dir dumps, Pokémon Elements, Daily-Top-Episode data, `cg/` SDK, or Competition Data appear here (CC-1/CC-2,
> ESP; SP-6/SP-9). **No dispersion metric values appear here.** **No numeric margin `M` is chosen or stated.** Runs are
> referenced by `run_id`/pattern, regimes by `regime_id`, metrics by sanitized *name* only, results by claim ceiling and
> local path/status only. The forbidden agent words (*strong / competitive / optimal / calibrated / complete*) and the
> inferential terms (*std-dev / variance / CI / p-value / significance / hypothesis-test / error-bar*) appear only as the
> negated/forbidden language they are.

## 0. State verified (2026-06-19, before drafting)

| Assumption to verify | Result |
|---|---|
| Current HEAD / branch | `main` @ `48a69fc` — *docs: close TurnTrace Cycle-006 Sprint 01* (== `origin/main`; no unexpected drift) |
| Local branch not behind `origin/main` | both at `48a69fcc04bd245dc62495536f8f1ce697969b27` — not behind |
| Cycle-006 status | **CLOSED — accepted, committed, pushed** (`docs/cycles/cycle-006/07-closeout.md`); `--promotion-check` live; Rung 1 held |
| `docs/ledger.md` byte-unchanged | **byte-unchanged**; `git diff --exit-code` clean; `hash-object = 2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` |
| `docs/claim-ceiling.md` unchanged | **unchanged**; `git diff --exit-code` clean; ceiling = **Rung 1** (`hash-object = b914ca1b…`) |
| Promotion gate present | `analysis/evidence_summary.py` `--promotion-check` live + audited at `48a69fc` (`a5cf339`); absent-`hashes` regression test **not yet pinned** (carry-forward 1) |
| `.claude/` untouched | **no drift**; `integrity_enforcement: strict` → no HALT |
| No staged files | **none staged** |
| `.beads/issues.jsonl`, `grimoires/loa/NOTES.md` dirty | both modified, **unstaged** (pre-existing State-Zone housekeeping); **must not be staged or cleaned** by this cycle |

**All assumptions hold. No finding forces a stop.** PRD acceptance, the build gate, fresh-evidence authorization, and the
Rung-2 attempt gate are **separate operator acts** this PRD does not self-authorize.

| Field | Value |
|---|---|
| **Cycle** | Cycle-007 |
| **Working title** | Gated Rung-2 Admission Attempt: Pre-Register, Generate Fresh Same-Regime Evidence, Apply the Verdict |
| **Type** | Product Requirements Document (planning artifact for a gated admission-attempt cycle) |
| **Status** | DRAFT — awaiting operator acceptance; next Golden-Path step is SDD / architecture |
| **Date** | 2026-06-19 |
| **Current main** | `48a69fc` — *docs: close TurnTrace Cycle-006 Sprint 01* |
| **Binding research input** | `grimoires/loa/a2a/cycle-007/00-pre-prd-research.md` (gitignored State-Zone research input; recommends **Option A**, accepted by operator for this pass) |
| **Posture** | **Gated Rung-2 admission attempt.** Rung 1 holds at open; Rung 2 is **unearned** and is earned **only** on a pre-registered fresh same-regime PASS followed by the separate PASS-gated terminal acts |
| **Claim ceiling (at open)** | **Rung 1** |

## Required posture (binding)

- **Cycle-007 is a gated Rung-2 admission *attempt*** — the first attempt in the project's history. It is **not** another
  preparation/evidence-repair cycle and **not** a split pre-registration/admission plan (research Options B and C are not
  taken). The reversible-safe seam half was completed and accepted in Cycle-006; Cycle-007 performs the gated *execution*
  acts (criteria 1, 3, 5) behind an explicit operator gate.
- **Rung 1 holds at cycle open** (`docs/claim-ceiling.md`). **Rung 2 is unearned** — not pending, not expected, not implied.
  An attempt is a question, not a foregone conclusion.
- **Rung 2 is earned only if and when** the pre-registered fresh same-regime comparison **PASSes** under the ratified 8a
  descriptive disjoint-bands rule and a pre-registered `M`, the promoted summary passes `--validate` **and**
  `--promotion-check`, provenance/audit-trail is intact, and the **separate PASS-gated terminal acts** (SP-6 → Rung-2 row →
  ceiling advance) are each taken as explicit operator decisions.
- **FAIL and INCONCLUSIVE are valid, non-regressive outcomes.** A FAIL or INCONCLUSIVE attempt **advances no ceiling,
  promotes no value, writes no Rung-2 row**, regresses nothing, stays at Rung 1, and **does not relax or re-pick `M` or the
  rule** to manufacture a PASS. An honest negative is a success of the harness, not a defect.
- **No numeric margin `M` is chosen in this drafting pass.** Cycle-007 records *that* `M` is fixed under the pre-registration
  procedure (`docs/cycles/cycle-006/02-sdd.md` §8); the value is set by the operator, recorded and dated, **before** any
  fresh band is generated/read, and **never** against the already-observed K=20+20 set (`01-prd.md` §10 contamination rule).
- **Fresh, never-observed same-regime evidence is required.** The existing K=20+20 evidence is **historical context only**;
  it may not be the verdict basis and may not be used to choose `M`. **No K=50 top-up and no expansion of any
  already-observed batch.**
- **Same-regime only.** A new frozen `regime-vNNN` is used for the fresh batch (a larger `n`/new seed-set is a **new** regime,
  never an edit of `regime-v001`; NFR-5). A `regime-v002` band is never compared to a `regime-v001` band.
- **The promotion gate gates, never promotes.** `--promotion-check` writes nothing and promotes nothing; it is the integrity
  precondition a promotion must pass, not a promoter.
- **Evidence-storage discipline holds.** Generated evidence is local/gitignored by default; only sanitized/operator-approved
  summaries may be promoted, and only by an explicit PASS-gated operator act; tracked artifacts reference runs by
  `run_id`/hashes/sanitized metric names/local path — never embed raw content (SP-6 / ESP).
- **The runtime-agent lane stays closed.** The candidate is an **existing frozen agent**; no new agent, gameplay heuristic,
  FunSearch, RL, self-play, deck optimizer, value/win-probability model, search/MCTS, tournament/leaderboard, or dashboard
  work enters Cycle-007 (NG7/NG8/NG10). Re-running a frozen agent to *generate evidence* is eval scope, not agent-building.
- **`.claude/` (System Zone) is never edited; no State-Zone cleanup is performed.** Pre-existing dirty State-Zone files stay
  unstaged and untouched.

**The bright line for the whole cycle:** *Cycle-006 built and audited the `--promotion-check` gate and pre-registered the
rule, then stopped at the seam. Cycle-007 opens the attempt behind a separate explicit operator gate, pre-registers the
single comparison (candidate, baseline, regime, `M`, `K`, justified `n`, stopping rule) before any fresh band exists,
generates the fresh same-regime evidence, applies the pre-registered verdict, and — only on PASS — takes the separate
terminal acts. Until that PASS, Rung 1 holds, `docs/ledger.md` stays byte-unchanged, and no value is promoted.*

## 1. Product / cycle overview

TurnTrace is a local, sanitized evaluation harness for a card-game simulator. Across five cycles it built Rung-2 *readiness*
without ever attempting Rung 2: Cycle-002 defined the five conjunctive readiness criteria; Cycle-003 specified the
evidence-summary schema, the generator/validator shape, the Rung-2 ledger convention, and the OD-6 / criterion-2
(disjoint-bands) resolution *in shape*; Cycle-004 built the offline evidence-summary generator + fail-closed validator and
stopped at the seam; Cycle-005 hardened that validator (C1–C4); Cycle-006 ratified the **8a** descriptive disjoint-bands
rule, recorded the `M` pre-registration *procedure* (no `M`), *designed* the fresh-evidence batch, *pre-registered* the
PASS/FAIL/INCONCLUSIVE verdict rule, and built/reviewed/audited the **`--promotion-check`** promotion gate
(`docs/cycles/cycle-006/07-closeout.md`).

The Cycle-007 pre-PRD research (`grimoires/loa/a2a/cycle-007/00-pre-prd-research.md`) audited the five readiness criteria —
**#2 MET** (8a ratified), **#4 PARTIALLY MET** (gate built; nothing fresh to verify yet), **#1, #3, #5 UNMET** — and found
that the three UNMET criteria are exactly the *gated execution acts of an attempt*, not further preparation. Every
reversible-safe blocker is cleared. The research recommends **Option A** — Cycle-007 as a gated Rung-2 admission attempt —
contingent on (i) the operator opening the attempt gate and (ii) the pre-registration being recorded and dated *before* any
fresh evidence is generated/read, with the irreversible terminal acts staying PASS-gated and separate. **The operator has
chosen Option A for this planning pass.**

**Mission (binding).** Run the first clean Rung-2 admission attempt under maximal contamination discipline: pre-register the
single comparison, generate fresh never-observed same-regime evidence, gate it on `--validate` + `--promotion-check`, apply
the pre-registered verdict, and advance the ceiling **only** on a PASS — or record an honest FAIL/INCONCLUSIVE at Rung 1.

**Who consumes this PRD.** The **operator** (accepts this PRD; opens the build gate and — separately — the Rung-2 attempt
gate; fixes `M`; authorizes fresh-evidence generation; is the only party who may issue SP-6, write the Rung-2 row, or advance
the ceiling, each on PASS only); the **architect/sprint-planner** (`/architect`, `/sprint-plan`, who resolve the SDD-level
and sprint-level decisions this PRD defers); the **implementer** (`/implement`, who lands the absent-`hashes` gate-pin and any
sanctioned harness wiring, and re-validates citations against the build-time HEAD); and the **reviewer/auditor**
(`/review-sprint`, `/audit-sprint`).

## 2. Problem statement

Cycle-006 left the loop *able* to attempt Rung 2 but holding at the seam. A clean attempt now requires the gated execution
acts, none of which has occurred:

1. **The single comparison is not yet pre-registered.** Criterion 3's pre-registered margin `M`, and the candidate /
   baseline / regime / `K` / justified-`n` / stopping-rule that scope it, are unfixed (`00-pre-prd-research.md` §3, §4, §6).
2. **No fresh same-regime evidence exists.** Criterion 1 requires a fresh, never-observed K≥20 same-regime batch under a new
   frozen `regime-vNNN` at a justified `n` that clears the unseeded RNG noise floor; the existing K=20+20 set is historical
   context only and contaminated for choosing `M` (`01-prd.md` §10; FM-11 analogue).
3. **The verdict has not been applied,** and the terminal ceiling advance (criterion 5) has not — and must not, except on a
   PASS — occurred.
4. **The promotion gate is not yet fully test-pinned for a real promotion.** The absent-`hashes` branch is structurally
   covered and was verified manually, but is not yet pinned by a dedicated regression test (Cycle-006 carry-forward 1) — and
   Cycle-007 is the first time the gate is relied on in a real promotion.

None of these is a *preparation* gap; each is an *execution* act gated behind the operator's explicit authorization.
Cycle-007 performs them under the contamination discipline below, or records an honest non-advancing outcome.

## 3. Posture statement (binding)

- **Cycle-007 is a gated Rung-2 admission attempt** (research Option A). **Rung 1 holds at cycle open.**
- **Rung 2 remains unearned** unless and until the pre-registered fresh same-regime comparison **PASSes** *and* the separate
  PASS-gated terminal acts (SP-6, Rung-2 row, ceiling advance) each occur as explicit operator decisions.
- **Rung 2 is not pending or expected.** The PRD makes **no** prediction about the outcome and applies **no** forbidden agent
  word to the candidate (*strong / competitive / optimal / calibrated / complete* appear only as forbidden language).
- **FAIL and INCONCLUSIVE are valid, non-regressive outcomes** that advance no ceiling, promote no value, write no Rung-2 row,
  and never relax or re-pick `M`/the rule.
- **This PRD authorizes nothing irreversible.** It opens no gate, chooses no `M`, generates no evidence, applies no verdict,
  and mutates neither `docs/ledger.md` nor `docs/claim-ceiling.md`.

## 4. Goals — what the Cycle-007 attempt must produce

Stated at product/governance level. **How** these are sprinted/architected is deferred to the SDD and sprint plan (§16);
this PRD states **what** must hold.

- **G1 — Pre-registration of the single comparison (before any fresh evidence).** The operator fixes and **dates**, in a
  committed record that **strictly precedes** any fresh-evidence generation/reading: the one frozen **candidate** identity,
  the **baseline** (`random_legal` under the new regime), the new frozen **`regime-vNNN`**, the numeric **`M`**, **`K` (≥20)**,
  a **justified `n`** with explicit noise-floor reasoning, and the **stopping rule**. Never fixed against the already-observed
  K=20+20 set.
- **G2 — Promotion-gate pinning precondition.** Before the gate is relied on in a real promotion, the **absent-`hashes`
  regression test** (Cycle-006 carry-forward 1) is added so the load-bearing gate is fully test-pinned; the promoted summary
  must pass **`--validate` and `--promotion-check`**.
- **G3 — Fresh same-regime evidence generated (gated, new eval scope).** A fresh, never-observed **K ≥ 20 same-regime** batch
  under the new frozen `regime-vNNN` at the justified `n`, baseline and candidate under the *same* regime, with
  provenance/audit-trail intact. Generated locally/gitignored, **only after** G1 is committed and the fresh-evidence gate is
  opened.
- **G4 — Verdict applied to the single pre-frozen tuple.** The pre-registered PASS/FAIL/INCONCLUSIVE rule
  (`docs/cycles/cycle-006/01-prd.md` §16.3) is applied to exactly the one pre-declared `(candidate, baseline, regime, M, K,
  n)` tuple — descriptive disjoint-bands, same-regime, no inferential statistic.
- **G5 — Terminal acts on PASS only (each a separate operator act).** On PASS: SP-6 (promote the sanitized summary), the
  Rung-2 ledger row (citing the summary by reference + content hash; 18-column schema verbatim; append-only), and the
  `docs/claim-ceiling.md` advance. **None before `--promotion-check` passes; none on FAIL/INCONCLUSIVE.**
- **G6 — Honest fail-state handling.** On FAIL/INCONCLUSIVE: no advance, no promotion, no Rung-2 row; record the descriptive
  result honestly at Rung 1; INCONCLUSIVE remediation generates a **new** pre-declared batch under the **same** `M`/rule —
  never an extension of the existing batch and never a post-hoc `M`.
- **G7 — Invariants held until PASS (hard).** Until a PASS terminal act, `docs/ledger.md` stays byte-unchanged
  (`2a2f1c2…`), `docs/claim-ceiling.md` is unchanged, no value reaches tracked status, and the ledger remains the only
  ceiling-bearing artifact.

## 5. Scope

**In scope (Cycle-007), behind the loop + the explicit operator gates.**
- Tracked planning/governance artifacts under `docs/cycles/cycle-007/` (this PRD; the SDD; the sprint plan; the dated
  pre-registration record per G1).
- The **absent-`hashes` regression test** (and, optionally, the exit-1 / both-flags-precedence tests) in
  `tests/test_evidence_summary.py`, plus any **sanctioned harness wiring** required to apply `--validate` /
  `--promotion-check` to the candidate summary — landing through `/implement → /review-sprint → /audit-sprint`.
- **Fresh same-regime evidence generation** (new eval scope) under the fresh-evidence gate (G3), local/gitignored.
- **Verdict application** (G4) and, **on PASS only**, the terminal acts (G5): SP-6, the Rung-2 ledger row, the
  `docs/claim-ceiling.md` advance.

**Out of scope (Cycle-007).**
- Any use of the already-observed K=20+20 set as a verdict basis or to choose `M`; any K=50 top-up or batch expansion.
- Choosing `M` against observed bands; optional stopping / batch-padding; candidate swapping; best-of-N candidate selection.
- Cross-regime comparison; OD-6 relaxation; any inferential statistic.
- Runtime-agent / gameplay-heuristic / FunSearch / RL / self-play / deck-optimizer / value-model / search-MCTS /
  tournament-leaderboard / dashboard work; any new agent.
- Daily-Top-Episodes or Kaggle episode ingest; any episode-derived improvement claim.
- Any second validator module, `*.schema.json`, third-party dependency, or promotion mode that writes a tracked path.
- Any `.claude/` edit; any State-Zone cleanup.

## 6. Non-goals (explicit)

Cycle-007 does **not**:

- **Predict or imply a PASS.** No claim that the candidate is *strong / competitive / optimal / calibrated / complete* or
  generally good; no implication that Rung 2 is pending or expected.
- **Use contaminated evidence.** No verdict on the already-observed K=20+20 bands; no `M` chosen against them; no top-up/
  expansion of an observed batch.
- **Choose `M` post-hoc**, relax the rule after the bands, swap candidates, or select the best of several candidates.
- **Compare across regimes**, edit `regime-v001`, or compute an inferential statistic; **OD-6 stays unrelaxed.**
- **Promote anything before the gate passes,** or on a FAIL/INCONCLUSIVE; **never** exit-0-accept an empty/absent `hashes`
  summary at promotion.
- **Ingest episodes** or treat Daily Top Episodes as proof; episodes remain local hypothesis input only (SP-9; FM-11).
- **Build or modify a runtime agent** or any gameplay/optimization surface (NG7/NG8/NG10).
- **Embed raw Competition Data / Pokémon Elements / traces / simulator logs / deck lists** in tracked docs; **edit
  `.claude/`;** or **clean State-Zone dirt.**

## 7. Functional requirements

The FRs state **what** the attempt must hold; **how** (sprint shape, internal design, task breakdown) is deferred to the SDD
and sprint plan (§16). Ordering requirements below are **governance constraints**, not a sprint design.

### C7-FR-1 — Pre-register the single comparison before any fresh evidence
1. The operator MUST fix and **date**, in a committed record, the full comparison tuple **before** any fresh band is
   generated or read: one frozen **candidate** `agent_version`; the **baseline** = `random_legal` under the new regime; the
   new frozen **`regime-vNNN`**; the numeric **`M`**; **`K` ≥ 20**; a **justified `n`** with explicit noise-floor reasoning;
   and the **stopping rule**.
2. The record's commit MUST **strictly precede** the fresh-evidence-generation commit, so "`M` before bands" is tamper-evident
   in git history. `M` MUST **not** be fixed against the already-observed K=20+20 set (`01-prd.md` §10; FM-11 analogue).
3. Exactly **one** candidate is pre-declared. **No candidate swapping** after the bands are seen, and **no best-of-N**
   candidate selection. The verdict is applied to this one tuple only.
4. **This PRD chooses no `M`** and declares no candidate; it states the requirement. The numeric `M` value lives only in the
   dated pre-registration record (a governance threshold, not a dispersion value), never in this PRD.

### C7-FR-2 — Pin and use the promotion gate
1. The **absent-`hashes` regression test** (Cycle-006 carry-forward 1) MUST be added to `tests/test_evidence_summary.py`
   (a dedicated check that a summary with the `hashes` key absent → the gate's fail-closed exit) **before** the gate is
   relied on in the real promotion. (Optionally the exit-1 / both-flags-precedence tests, carry-forward 2.)
2. The promoted candidate summary MUST pass **both `--validate` and `--promotion-check`** (non-empty integrity stamp + full
   hardened validator clean) before any Rung-2 row is written.
3. `--promotion-check` MUST remain a **gate only** — it writes nothing, promotes nothing, never writes `docs/ledger.md` or any
   tracked `docs/` path, and preserves the `0/1/2/3` exit contract and the `--validate` / generate-mode behaviour unchanged
   (`docs/cycles/cycle-006/07-closeout.md` §2).

### C7-FR-3 — Generate fresh same-regime evidence (gated; new eval scope)
1. A fresh, never-observed **K ≥ 20 same-regime** batch MUST be generated under the new frozen **`regime-vNNN`** at the
   justified `n`, with baseline and candidate under the **same** regime. Generation occurs **only after** C7-FR-1 is committed
   and **only** under the operator's explicit fresh-evidence authorization.
2. The batch MUST be **distinct** from the already-observed K=20+20 set; **no K=50 top-up; no expansion** of an observed batch;
   **no optional stopping / batch-padding** (read exactly the pre-declared `K` at the pre-declared `n`).
3. **Provenance/audit-trail MUST be intact** for every run — source-hash provenance, per-decision canonical traces,
   `trace_hash`, regime-tuple stamp — i.e. exactly what `--promotion-check` gates on.
4. Generated evidence is **local/gitignored by default** (SP-6 / ESP); no raw content enters tracked docs.

### C7-FR-4 — Apply the pre-registered verdict
1. The pre-registered **PASS / FAIL / INCONCLUSIVE** rule (`docs/cycles/cycle-006/01-prd.md` §16.3) MUST be applied to the
   single pre-frozen tuple, using the ratified **8a descriptive disjoint-bands** rule (*candidate `min` > baseline `max` by ≥
   `M` across the fresh K≥20 same-regime batch*) expressed in the allowed descriptive vocabulary only — **no inferential
   statistic, no cross-regime comparison** (NFR-2, NFR-3).
2. **PASS** requires *all* of: the margin met under the pre-registered `M`; the summary passes `--validate` **and**
   `--promotion-check`; provenance/audit-trail intact; the justified-`n` / noise-floor argument satisfied.
3. The verdict is recorded as a **same-regime TurnTrace descriptive delta**, never episode-derived (FM-11); no forbidden agent
   word is applied even on a PASS.

### C7-FR-5 — Terminal acts on PASS only (each a separate operator act)
1. **Only on PASS, and only after `--promotion-check` passes**, the operator MAY, as separate explicit acts and in order:
   (a) issue **SP-6** to promote the sanitized summary to tracked status (reference + hash + sanitized metric names; never raw
   content); (b) write the **Rung-2 ledger row** reusing the existing **18-column schema verbatim** (no new column; verdict in
   the existing narrative fields; citing the promoted summary **by reference + content hash** in `notes`; append-only; never
   edit a past row); (c) advance **`docs/claim-ceiling.md`** to Rung 2.
2. The **ledger remains the only ceiling-bearing artifact**; the evidence summary carries **no ceiling of its own**
   (`docs/cycles/cycle-003/04-evidence-summary-schema-spec.md` §1; `06-rung-2-ledger-convention.md` §3).
3. **None** of these acts may occur before the gate passes, and **none** on FAIL/INCONCLUSIVE.

### C7-FR-6 — Honest fail-state handling
1. A **FAIL** (margin not met) → no advance, no promotion, no Rung-2 row; record the descriptive result honestly at **Rung 1**;
   `M`/rule never re-picked.
2. An **INCONCLUSIVE** (a precondition unmet: `n` insufficient to clear the noise floor; incomplete provenance/hashes;
   `--promotion-check` fails) → no advance, no promotion; remediate by generating a **new** pre-declared batch under the
   **same** `M`/rule, never by extending the existing batch and never by relaxing `M`.
3. The fail-state outcome is recorded faithfully and is **not** a regression of Rung 1.

## 8. Non-functional / claim-ceiling requirements

- **NFR-1 — Contamination discipline (hard).** The §9 controls bind: one pre-frozen candidate; baseline `random_legal` under
  the new regime; new `regime-vNNN`; K=20+20 historical-only; no top-up/expansion; `M`/`K`/`n`/stopping-rule dated before
  evidence; no optional stopping/batch-padding; no candidate swap / best-of-N; no post-hoc `M`.
- **NFR-2 — Same-regime only.** The single-regime guard (exit 2) holds across the validator and `--promotion-check`; no
  cross-regime field or comparison anywhere; a larger `n` is a new regime, never an edit of `regime-v001`
  (`docs/cycles/cycle-003/05-generator-validator-shape.md` §2.2; `docs/claim-ceiling.md`).
- **NFR-3 — Claim safety.** Rung 1 at open; forbidden agent words negated-only; **no inferential result produced** (the
  validator *rejects* inferential terms; the ratified disjoint-bands rule is descriptive); OD-6 stays unrelaxed.
- **NFR-4 — Sanitization / data boundary.** Competition Data, Pokémon Elements, raw traces, simulator logs, deck lists,
  `deck.csv`, `cg/`, run-dir dumps, PDFs/CSVs, and Daily-Top-Episode data never enter tracked docs (CC-1/CC-2, ESP);
  `eval/hygiene_check.py` remains the staging gate; the validator + `--promotion-check` stay sanitization-parity-or-stricter;
  generated evidence stays local/gitignored; tracked artifacts use references/`run_id`/hashes/sanitized metric names/local
  path/status only (reference-not-embed; SP-6).
- **NFR-5 — Ledger / ceiling invariance until PASS (hard).** `docs/ledger.md` byte-unchanged at `2a2f1c2…` and
  `docs/claim-ceiling.md` unchanged until — and unless — a PASS terminal act; the Rung-2 row is append-only; no past row is
  edited.
- **NFR-6 — Simulator-authoritative (SP-8 / FM-10).** Any verdict-relevant logic follows the simulator-offered legal options
  and the simulator terminal result, never official-rule assumptions; record any divergence as a simulator-behaviour note,
  not an agent failure.
- **NFR-7 — No episode/Kaggle proof (SP-9 / FM-11).** No Daily-Top-Episodes or Kaggle episode ingest; episodes are
  hypothesis-only; the verdict must be a same-regime TurnTrace comparison, never episode-derived.
- **NFR-8 — Runtime-agent lane closed (NG7/NG8/NG10).** The candidate is an existing frozen agent; no new agent / heuristic /
  FunSearch / optimization surface; re-running a frozen agent to generate evidence is eval scope, not agent-building.
- **NFR-9 — Zone discipline.** Tracked code is App Zone (`analysis/`, `tests/`); planning artifacts are Docs/State Zone;
  `.claude/` is never touched; pre-existing dirty State-Zone files stay unstaged and uncleaned.
- **NFR-10 — Implement-time citation revalidation.** Any line anchors a later sprint relies on MUST be re-validated against the
  build-time HEAD before coding; anchors accurate now may desync if files move.

## 9. Contamination / fresh-evidence posture (binding)

Carried from the research (`00-pre-prd-research.md` §5, §6, §11) and the Cycle-006 contamination rule (`01-prd.md` §10):

- **The existing K=20+20 evidence is historical context only.** It may **not** be the verdict basis and may **not** be used to
  choose `M`. Fixing `M` against an already-observed set is post-hoc thresholding — the in-house analogue of **FM-11**.
- **A clean attempt requires fresh, never-observed same-regime evidence,** generated only **after** the pre-registration is
  committed, under a **justified `n`** that clears the unseeded RNG noise floor (`docs/cycles/cycle-003/08-funsearch-forward-compat.md`
  §3: runs are unseeded; observed dispersion conflates agent behaviour with simulator RNG; the evaluator must average over
  enough matches/batches to clear the noise floor before a per-candidate scalar is stable).
- **One pre-frozen candidate; `random_legal` baseline under the new regime; a new frozen `regime-vNNN`.** No candidate swap, no
  best-of-N, no cross-regime comparison, no edit of `regime-v001`.
- **`M`, `K`, justified `n`, and the stopping rule are recorded and dated before fresh evidence is generated/read.** No optional
  stopping; no batch-padding; read exactly the pre-declared `K` at the pre-declared `n`.

## 10. Promotion-gate requirements (product level)

At product/requirements level (architecture → SDD), the Cycle-007 use of the gate MUST:

1. **Pin the gate first.** Add the absent-`hashes` regression test (carry-forward 1) before the gate is relied on in the real
   promotion (C7-FR-2.1).
2. **Gate the promoted summary on both modes.** `--validate` and `--promotion-check` must pass (non-empty integrity stamp +
   full hardened validator clean) before any Rung-2 row is written (C7-FR-2.2). A silently empty/absent `hashes` is fatal at
   promotion (CF-1 / OD-C5-2 floor) precisely because the Rung-2 row cites the summary **by reference + content hash**.
3. **Keep the gate side-effect-free.** `--promotion-check` writes nothing and promotes nothing; it never writes
   `docs/ledger.md` or any tracked `docs/` path; the `0/1/2/3` contract and the `--validate` / generate-mode behaviour stay
   unchanged.

## 11. Pre-registered verdict rule (imported by reference)

The **PASS / FAIL / INCONCLUSIVE** criteria and **fail-state language** applied in Cycle-007 are the ones pre-registered in
`docs/cycles/cycle-006/01-prd.md` §16.3, imported here **by reference** to avoid divergence (no competing wording is authored
in this PRD). Its binding invariants: PASS requires the pre-registered margin met **and** `--validate` + `--promotion-check`
clean **and** provenance intact **and** the justified-`n` argument satisfied → the operator **may** take the separate terminal
acts; FAIL/INCONCLUSIVE **advance no ceiling, promote no value, write no Rung-2 row**, regress nothing, and **never** relax or
re-pick `M`/the rule.

The research recommends three **tightenings** to that rule before the attempt, carried here as requirements (C7-FR-1.3,
C7-FR-3.2, C7-FR-6.2): (a) freeze candidate/baseline/regime/`K`/`n`/stopping-rule into the pre-registration, not just `M`;
(b) no optional stopping / batch-padding; (c) scope INCONCLUSIVE to admissibility failures (noise floor not cleared,
incomplete provenance, failing gate), not band ambiguity. The **exact wording** of these tightenings is an SDD/pre-registration
deliverable (§16), not authored here.

## 12. Claim-ceiling posture

The loop sits at **ladder Rung 1**, and **Cycle-007 holds Rung 1 at open**:

```
Rung 0  env not trusted
Rung 1  legal completion                         ← current, held at cycle open
Rung 2  beats random-legal                       ← ATTEMPTED here behind a gate; earned ONLY on a pre-registered fresh same-regime PASS + the separate PASS-gated terminal acts
Rung 3  beats scripted / prior best, ablation-backed
Rung 4  stable, report-ready
```

**Allowed claim form** — relative, local, descriptive, carrying its `n`, `K`, and `regime_id`. **Forbidden claim forms**
(negated-only): gameplay strength; statistical significance; cross-regime uplift; leaderboard quality; calibration;
optimality; competitiveness. Only the ledger, advanced by a **separate explicit operator decision on PASS**, can carry Rung 2.
**A FAIL/INCONCLUSIVE leaves the ceiling at Rung 1 and is not a regression.**

## 13. Evidence-storage & data-boundary discipline

Carried verbatim-in-intent from the standing rules (`docs/operator/turntrace-loop-contract.md` §7-§8;
`docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` SP-6/SP-8/SP-9; `docs/failure-modes.md` FM-10/FM-11):

- **Raw Competition Data never enters git** (CC-1/CC-2): `cg/` SDK, card data, raw deck lists, `deck.csv`, PDFs/CSVs,
  run-dir dumps — local-only under gitignored `grimoires/loa/context/`.
- **Pokémon Elements never appear in tracked artifacts.**
- **Generated runs, dispersion values, and the generator's output stay local/gitignored;** tracked artifacts hold sanitized
  references only. **No `M` value** appears in any tracked artifact except the dated pre-registration record (a governance
  threshold).
- **Daily Top Episodes / raw episode datasets stay local/ignored (SP-9);** never tracked, never a runtime dependency, never
  Rung-2 proof without a same-regime TurnTrace comparison (FM-11).
- **Simulator behaviour is authoritative (SP-8 / CC-10);** official-rule assumptions must not override it (FM-10).
- **Only sanitized/operator-approved summaries may be promoted, and only by an explicit PASS-gated operator act** (SP-6).
  Tracked artifacts reference runs by `run_id` / hashes / sanitized metric names / local path/status — **never embed raw
  content.** `eval/hygiene_check.py` remains the mechanical staging gate.

## 14. Risks and mitigations

| ID | Risk | Mitigation |
|---|---|---|
| **R1** | **Post-hoc `M`** | C7-FR-1: `M` (+candidate/`K`/`n`/stopping rule) fixed in a committed, dated record that strictly precedes generation; never against K=20+20 (§9). |
| **R2** | **Candidate-selection contamination** (best-of-N / forking paths) | C7-FR-1.3: one pre-frozen candidate; runtime-agent lane closed (NFR-8) ⇒ candidate is an existing frozen agent; no swap/add after bands; no best-of-N. |
| **R3** | **Old-evidence contamination** | §9 / NFR-1: K=20+20 historical-only; never verdict basis, never used to choose `M`; no top-up/expansion (FM-11). |
| **R4** | **Unseeded noise / insufficient `n`** | C7-FR-1 justified `n` + noise-floor reasoning; C7-FR-3.2 no optional stopping; INCONCLUSIVE if floor not cleared (C7-FR-6.2). |
| **R5** | **Cross-regime comparison** | NFR-2: one frozen `regime-vNNN`; single-regime guard (exit 2); new `n` = new regime, never an edit of `regime-v001`. |
| **R6** | **Promotion before gate** | C7-FR-5 / NFR-5: SP-6 + row + ceiling advance only on PASS, only after `--validate` + `--promotion-check` pass; never on FAIL/INCONCLUSIVE. |
| **R7** | **Ledger / claim-ceiling drift** | NFR-5: `docs/ledger.md` byte-unchanged at `2a2f1c2…` until the PASS row (append-only; never edit a past row); `docs/claim-ceiling.md` unchanged until a PASS advance. |
| **R8** | **Raw Competition Data / Pokémon Elements leakage** | NFR-4 / §13: no raw data in tracked docs; `eval/hygiene_check.py` gate; validator + `--promotion-check` sanitization parity-or-stricter; evidence local/gitignored. |
| **R9** | **Simulator-vs-official-rules mismatch (FM-10)** | NFR-6 / SP-8: simulator-authoritative; record divergence as a simulator-behaviour note, not an agent failure. |
| **R10** | **Daily Top Episodes / Kaggle overfitting (FM-11)** | NFR-7 / SP-9: no episode/Kaggle ingest; episodes hypothesis-only; same-regime verdict only, never episode-derived. |
| **R11** | **Runtime-agent / FunSearch / gameplay scope creep** | NFR-8: lane closed (NG7/NG8/NG10); candidate is an existing frozen agent; Cycle-007 is admission, not agent-building. |
| **R12** | **Optional stopping / batch-padding** | C7-FR-3.2 / C7-FR-6.2: pre-register `K`/`n`/stopping rule; read exactly the pre-declared batch; remediation = a new pre-declared batch, not extension. |
| **R13** | **Gate-trust gap (absent-`hashes` untested)** | C7-FR-2.1: add the absent-`hashes` regression test before the gate gates the real promotion. |
| **R14** | **Premature execution** — `M` chosen, evidence generated, or a terminal act taken without the gate | §0/§3/§15: PRD acceptance, the build gate, the fresh-evidence gate, and the Rung-2 attempt gate are separate operator acts; HALT if any execution act is attempted out of order. |

## 15. Operator decisions still required (before and within the gated attempt)

This PRD identifies the decisions; it makes none of them. The numeric `M` is **not** chosen here.

| ID | Decision | When |
|---|---|---|
| **OD-C7-1 — Accept this PRD** | Accept the Cycle-007 gated-admission-attempt posture (Option A) and proceed to `/architect`. | Before SDD |
| **OD-C7-2 — Build gate (OA-2-class)** | Open the build gate for the sanctioned code work (absent-`hashes` gate-pin + any sanctioned harness wiring), scoped to `analysis/`/`tests/`. | After SDD/sprint-plan |
| **OD-C7-3 — Rung-2 attempt gate** | Open the **separate explicit operator gate** authorizing the Rung-2 attempt (`01-prd.md` §19.8). Without it, no fresh-evidence generation, verdict, or terminal act occurs. | Before evidence |
| **OD-C7-4 — Candidate identity** | Name the **one** frozen candidate `agent_version` (the runtime-agent lane is closed, so an existing frozen agent), and confirm baseline = `random_legal` under the new regime. | In pre-registration |
| **OD-C7-5 — New regime** | Fix the new frozen **`regime-vNNN`** for the fresh batch (a new `n`/seed-set is a new regime, never an edit of `regime-v001`). | In pre-registration |
| **OD-C7-6 — `M` mechanics & location** | Fix the numeric **`M`**, recorded and **dated**, committed **before** generation, **never** against K=20+20; and decide **where** it lives (dedicated dated pre-registration record and/or an operator-decision-register row). | In pre-registration |
| **OD-C7-7 — `K`, justified `n`, stopping rule** | Fix **`K` ≥ 20**, the **justified `n`** with explicit noise-floor reasoning, and the **stopping rule** (no optional stopping / batch-padding). | In pre-registration |
| **OD-C7-8 — Verdict-rule tightenings** | Confirm the §11 tightenings (freeze full tuple, not just `M`; no optional stopping; INCONCLUSIVE = admissibility failure). | Before evidence |
| **OD-C7-9 — Fresh-evidence authorization** | Authorize generating the fresh K≥20 same-regime batch as **new eval scope**, only after the pre-registration is committed. | Before generation |
| **OD-C7-10 — Terminal PASS-gated acts** | On PASS only, each as a separate explicit act: issue **SP-6**; write the **Rung-2 ledger row**; advance **`docs/claim-ceiling.md`**. None on FAIL/INCONCLUSIVE. | On PASS only |

## 16. Success criteria

### 16.1 Planning-cycle success (this PRD)
- Accepted by the operator (Option A) and proceeds to `/architect` (SDD), not directly to implementation or evidence.
- Grounded in the pre-PRD research and the tracked authorities; clearly a **gated attempt**, not prep and not a split plan;
  records the contamination controls, the promotion-gate requirements, and the pre-registered verdict rule by reference;
  **chooses no `M`; generates no evidence; applies no verdict; takes no terminal act.**
- **Rung 1 held;** `docs/ledger.md` byte-unchanged (`2a2f1c2…`); `docs/claim-ceiling.md` unchanged; no raw data embedded;
  `.claude/` untouched; State-Zone files unstaged and uncleaned.

### 16.2 Attempt outcome posture (when the gated attempt runs in later sprints)
- **PASS** — all C7-FR-4.2 conditions hold → the operator **may** take the separate terminal acts (C7-FR-5); recorded as a
  same-regime descriptive delta; no forbidden agent word applied.
- **FAIL** — margin not met → no advance, no promotion, no Rung-2 row; honest Rung-1 record; `M`/rule never re-picked.
- **INCONCLUSIVE** — an admissibility precondition unmet → no advance, no promotion; remediate with a new pre-declared batch
  under the same `M`/rule.
- **All three outcomes are valid.** FAIL/INCONCLUSIVE are non-regressive; the harness producing an honest negative is a
  success, not a defect.

### 16.3 Hard invariants (whole cycle, until a PASS terminal act)
- `docs/ledger.md` byte-unchanged at `2a2f1c2…`; `docs/claim-ceiling.md` unchanged; the ledger remains the only
  ceiling-bearing artifact; the summary carries no ceiling of its own; no value promoted; stdlib-only / analysis-only imports;
  no second module / `*.schema.json` / dependency / tracked-path-writing promotion mode; `.claude/` untouched; State-Zone
  dirt unstaged.

## 17. Sources and traceability

> **Local decision input (gitignored State Zone, not a tracked dependency):**
> `grimoires/loa/a2a/cycle-007/00-pre-prd-research.md` (the Cycle-007 pre-PRD research; recommends **Option A**, accepted by
> the operator for this pass; five-criteria audit; contamination controls; pre-registration / fresh-evidence / promotion-gate
> assessments; risk register).
> **Tracked Cycle-006 authorities:** `docs/cycles/cycle-006/07-closeout.md` (closed/accepted/pushed; `--promotion-check`
> live; Rung 1 held; carry-forwards; §9 Cycle-007 handoff gate); `06-audit-report.md` (PASS WITH NOTES — ACCEPTED; no
> findings; carry-forward 1 absent-`hashes` test); `01-prd.md` §9 (8a–8d seam), §10 (contamination rule), §16.3
> (pre-registered PASS/FAIL/INCONCLUSIVE rule — imported by reference), §19 (Cycle-007 handoff gate); `02-sdd.md` §8 (`M`
> pre-registration procedure), §9 (fresh-evidence batch design + verdict rule).
> **Tracked Cycle-003 design authorities:** `04-evidence-summary-schema-spec.md` (§1 summary carries no ceiling; §2 safe
> descriptive vocabulary); `05-generator-validator-shape.md` (§2 single-regime exit 2 / exit-code contract / hygiene parity;
> NG12 = no eval runs); `06-rung-2-ledger-convention.md` (§1 18-column schema verbatim; §2 same-regime agent-only verdict;
> §3 row cites summary by reference + content hash); `07-od6-criterion-2-proposal.md` (§2 disjoint-bands rule; §3
> pre-registration procedure; §5 seam 8a–8d — bundling is "the highest-consequence, hardest-to-walk-back path");
> `08-funsearch-forward-compat.md` (§3 unseeded noise floor / justified `n`; NG7/NG8/NG10 runtime-agent lane closed).
> **Tracked posture docs:** `docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` §2 (five conjunctive criteria);
> `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` (SP-6 evidence-storage / live-value promotion; SP-8 simulator
> authoritative; SP-9 episodes hypothesis-only; OA-2 build gate); `docs/failure-modes.md` (FM-10 official-rule mismatch;
> FM-11 contaminated evidence); `docs/claim-ceiling.md` (Rung 1; forbidden words; never compare across regimes); `docs/ledger.md`
> (two Rung-1 `regime-v001` rows: baseline `run-0001`/`random_legal-v001`, candidate `run-0002`/`scripted-v001`; hash
> `2a2f1c2…`); `docs/operator/turntrace-loop-contract.md` (§1 loop; §6 OA-2 build gate; §7-§8 hygiene/claim language).
> **Tracked code (the gate, at `48a69fc`):** `analysis/evidence_summary.py` (`--promotion-check` live; `0/1/2/3` exit
> contract; empty/absent-`hashes` → exit 3; writes nothing); `tests/test_evidence_summary.py` (12 + block-13 + block-14;
> absent-`hashes` regression test **not yet pinned** — carry-forward 1).
> Current main at authoring: `48a69fc`. Claim ceiling: **Rung 1 (unchanged).** This PRD opens no implementation gate, builds
> no code, generates no evidence, runs no eval, chooses no `M`, applies no admission verdict, issues no SP-6, promotes no
> value, writes no Rung-2 row, advances no ceiling, mutates no ledger, and edits no `.claude/`. **The Rung-2 attempt proceeds
> only behind a separate explicit operator gate.**

---

> **PRD statement (binding).** Cycle-007 is a **gated Rung-2 admission attempt** (research Option A). **Rung 1 holds at cycle
> open; Rung 2 is unearned** and is earned **only** on a pre-registered fresh same-regime **PASS** under the ratified 8a
> descriptive disjoint-bands rule and a pre-registered `M`, gated on `--validate` + `--promotion-check`, followed by the
> **separate PASS-gated terminal acts** (SP-6 → Rung-2 row → ceiling advance), each an explicit operator decision. **FAIL and
> INCONCLUSIVE are valid, non-regressive outcomes** that advance no ceiling, promote no value, write no Rung-2 row, and never
> relax or re-pick `M`. The single comparison — one frozen candidate, `random_legal` baseline under a new frozen
> `regime-vNNN`, `M`, `K`≥20, justified `n`, stopping rule — is **recorded and dated before any fresh evidence is
> generated/read**, never against the already-observed K=20+20 set. **This drafting pass chose no `M`, generated no evidence,
> ran no eval, applied no verdict, issued no SP-6, wrote no Rung-2 row, and advanced no ceiling.** `docs/ledger.md` remains
> byte-unchanged at `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`; `docs/claim-ceiling.md` is unchanged.
