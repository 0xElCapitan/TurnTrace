# OD-6 / Criterion-2 Resolution Proposal (Cycle-003 / Sprint 00 · S00-T4)

| Field | Value |
|---|---|
| **Type** | Docs-only proposal (resolves the tension *in shape*; decides nothing; authorizes no code; opens no build gate) |
| **Status** | Authored — Cycle-003 Sprint 00 deliverable (S00-T4); a proposal for a *later* operator decision |
| **Date** | 2026-06-19 |
| **Lane / FR** | Lane D · C3-FR-4 · S00-T4 |
| **Scope** | Resolves the Rung-2 criterion-2 ↔ OD-6 tension *in shape* by recommending a pre-registered descriptive disjoint-bands rule, presents the OD-6-relaxation alternative without deciding it, specifies the pre-registration procedure, and names the later operator seam. **`M` is left unset; OD-6 is not relaxed; no inferential result is produced.** |
| **Related** | `docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` (the five conjunctive criteria), `docs/cycles/cycle-002/07-operator-decision-register.md` (§1-§2, OD-6), `04-evidence-summary-schema-spec.md` (the `min`/`max`/`K` the rule consumes), `06-rung-2-ledger-convention.md` (the row a later advance would write), `docs/claim-ceiling.md`, `docs/cycles/cycle-003/01-prd.md` (C3-FR-4, §9), `docs/cycles/cycle-003/02-sdd.md` (§8) |

> Sanitized note. No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, or Competition Data appear here (CC-1/CC-2, ESP).
> **No dispersion metric values appear here**, and **no numeric margin `M` is chosen.** Runs are referenced
> by `run_id`, content hashes, sanitized metric *names*, claim ceilings, and local path/status only. The
> forbidden agent claim words (*strong / competitive / optimal / calibrated / complete*) appear only as
> negated/forbidden language. The inferential terms (*std-dev, variance, confidence interval, p-value,
> significance, hypothesis test, inferential error bar*) appear only as the enumerated-forbidden language
> they are.

> **Boundary banner (binding).** This document opens **no build gate** and **decides nothing.** It resolves
> the criterion-2 ↔ OD-6 tension *in shape* only: it recommends a procedure, presents the alternative, and
> names the later operator seam. It **chooses no numeric margin `M`**, **does not relax OD-6**, **computes
> and reports no inferential result**, **advances no claim ceiling**, and **writes no ledger row**. Choosing
> between the recommendation and the alternative, fixing `M`, issuing SP-6, and advancing the ceiling are all
> separate later operator decisions (§5). The claim ceiling stays **Rung 1**.

## 1. The tension

A future Rung-2 consideration is **conjunctive** — it requires **all five** criteria of
`04-rung-2-readiness-criteria.md` §2 (`:31-51`). Two of them collide as written:

- **Criterion 2** requires *"an explicitly designed and operator-approved **inferential** procedure"*
  (`04-rung-2-readiness-criteria.md` §2.2, `:38-40`).
- **OD-6** *forbids* inferential statistics — *"no confidence intervals, no p-values, no 'significant,' no
  hypothesis tests, no inferential error bars"* — as a deliberate bright line, allowing only the descriptive
  vocabulary `count / min / max / range / mean / median / spread` (`07-operator-decision-register.md` §2,
  `:39-45`; `:28` OD-6).

They **cannot both hold unchanged** (`01-prd.md:113-116,284-287`; `02-sdd.md:352-356`). A future admission
must therefore either reinterpret criterion 2 within OD-6, or relax OD-6 — a governance choice, not a data
question.

## 2. Recommended resolution — pre-registered descriptive disjoint-bands (shape only)

The recommendation is a **pre-registered descriptive disjoint-bands rule** of the shape
(`01-prd.md:213-222,288-293`; `02-sdd.md:358-370`):

> **"candidate `min` > baseline `max` by ≥ `M` across `K ≥ 20` same-regime batches"**

expressed using **only the allowed descriptive vocabulary** (`min`, `max`, `range`, `mean`, `median`,
`spread`, `count`) — **no `std-dev`, no `variance`, no inferential statistic** (OD-6 unrelaxed;
`07-operator-decision-register.md` §2).

Why this fits without crossing OD-6:

- **It consumes the schema with no new field.** The quantities it reads — `candidate min`, `baseline max`,
  and `K` — are all already in the `04-evidence-summary-schema-spec.md` safe set (§2.1-§2.2). The rule adds
  **no field** to the schema and **no statistic** beyond the seven descriptive ones (`02-sdd.md:366-368`).
- **It is descriptive, not inferential.** "The two observed `[min, max]` bands are disjoint by at least `M`"
  is a statement about observed extrema — arithmetic over values already computed, with no estimator of a
  population parameter, no interval, no p-value, and no test statistic.
- **It satisfies criterion 3 and reinterprets criterion 2's spirit.** A margin fixed in advance satisfies
  criterion 3's *pre-registered margin* (`04-rung-2-readiness-criteria.md` §2.3, `:41-43`), and a
  pre-registered, operator-approved, not-chosen-after-the-fact rule honours criterion 2's **spirit**
  (a designed, ratified-before-reading procedure) **without** the inferential machinery OD-6 forbids
  (`02-sdd.md:368-370`).

The rule carries the standing caveats: it is **same-regime only** (a `regime-v002` band is never compared to
a `regime-v001` band; NFR-5), and it operates on the **unseeded process** spread, which conflates agent
behaviour with uncontrolled simulator RNG and is never presented as isolated agent variance
(`05-reproducibility-reality.md` §3).

## 3. The pre-registration procedure (shape only; `M` unset)

The rule and its margin `M` are fixed **before** the comparison numbers are read as the verdict
(`01-prd.md:293`; `02-sdd.md:378-381`). The procedure shape:

1. The operator ratifies the disjoint-bands rule (or the §4 alternative) and fixes the numeric margin `M`
   **in advance**, as part of the approved design — so the threshold cannot be chosen after seeing the
   numbers (`04-rung-2-readiness-criteria.md` §2.3).
2. Only then are the K-batch `min`/`max` bands read and the rule applied.
3. The outcome is recorded only through the normal cadence, with any ceiling advance a **separate** explicit
   step (§5).

This proposal specifies the **procedure**; it **does not choose `M`** (NG6). No numeric margin value appears
in this document. Fixing `M` under the gravity of already-seen K-batch numbers is exactly the risk
pre-registration removes (`01-prd.md:390` R3; sprint plan §16 R4), so `M` is deferred to the later gate.

## 4. The alternative — relax OD-6 (presented, not recommended)

The operator may instead **relax OD-6** to permit a genuine inferential test (e.g. an explicitly designed and
approved inferential procedure with a pre-registered threshold). This is presented as **the alternative, not
the recommendation, and is not decided here** (`01-prd.md:294-295`; `02-sdd.md:372-376`). It is the
heavier-consequence path: it lifts a deliberate bright line, so it would need its own explicit operator
ratification. OD-6 **stays unrelaxed** unless and until that decision is made (`07-operator-decision-register.md`
§2).

## 5. The later operator seam (four conjunctive decisions — none in Cycle-003)

The resolution sits at a **single later seam** where an operator chooses, in order, four irreversible
governance/design (not data) acts (`01-prd.md:296-298,367-382`; `02-sdd.md:384-398`). **None happens in
Cycle-003:**

| Seam step | Operator decision | PRD ref | Cycle-003 status |
|---|---|---|---|
| **8a** | Descriptive disjoint-bands rule **vs** OD-6 relaxation | OD-C3-1 | proposed in shape (§2 recommended; §4 alternative); **not decided** |
| **8b** | Numeric margin `M` | OD-C3-2 | **deferred** — fixed before the numbers are read, at the later gate (§3) |
| **8c** | SP-6 live-value promotion | OD-C3-3 | **deferred** — schema designed (`04-…`); **no value promoted** |
| **8d** | Rung-2 ledger row / claim-ceiling advance | OD-C3-1 (criterion 5), OD-C3-7 | **deferred** — separate Rung-2 admission gate (`06-…` §4) |

These four are **conjunctive and all governance/design, not data** (`01-prd.md:103-107`). Bundling them into
one cycle is the highest-consequence, hardest-to-walk-back path; the project's discipline is to build
readiness, then advance as a separate explicit decision (`04-rung-2-readiness-criteria.md` §2.5).

## 6. What this proposal deliberately does NOT do

- **Decides nothing.** It recommends (§2) and presents the alternative (§4); the operator decides at the
  later seam (§5). Deciding the resolution here → HALT (AC-S00-4).
- **Chooses no `M`.** No numeric margin value appears in this document (§3; NG6). A numeric `M` appearing
  here → HALT (AC-S00-4, AC-X8).
- **Does not relax OD-6.** Descriptive vocabulary only; the inferential alternative is presented, not adopted
  (§4). Relaxing OD-6 here → HALT (AC-X8).
- **Produces no inferential result.** No confidence interval, p-value, significance statement, hypothesis
  test, or inferential error bar is computed or reported — these appear only as the enumerated-forbidden
  language they are (OD-6).
- **Advances no ceiling; writes no row.** The ceiling stays Rung 1; any advance is step 8d at the later gate
  (`06-rung-2-ledger-convention.md` §4; NG1-NG3).

## 7. Traceability

| Requirement (PRD) | This proposal |
|---|---|
| C3-FR-4 state the criterion-2 ↔ OD-6 tension | §1 |
| C3-FR-4 recommend pre-registered descriptive disjoint-bands (allowed vocabulary; no new field) | §2 |
| C3-FR-4 specify the pre-registration procedure in shape; `M` unset | §3 |
| C3-FR-4 present OD-6 relaxation as the alternative, not the recommendation | §4 |
| C3-FR-4 name the later operator seam (four conjunctive decisions) | §5 |
| C3-FR-4 "resolves in shape; decides nothing, chooses no `M`, no inferential result" | §6 |

> **Sources:** `docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` §2 (`:31-51`, the five conjunctive
> criteria; criterion 2 inferential, `:38-40`; criterion 3 pre-registered margin, `:41-43`; criterion 5
> ceiling advance, `:46-49`); `docs/cycles/cycle-002/07-operator-decision-register.md` §1-§2 (OD-6
> descriptive-only, `:28,39-45`); `docs/cycles/cycle-002/05-reproducibility-reality.md` §3 (unseeded
> process); `04-evidence-summary-schema-spec.md` §2 (the `min`/`max`/`K` the rule consumes); `docs/claim-ceiling.md`;
> `docs/cycles/cycle-003/01-prd.md` (C3-FR-4, §9, OD-C3-1/2/3/7); `docs/cycles/cycle-003/02-sdd.md` (§8).
> Claim ceiling: **Rung 1 (unchanged).** This proposal opens no build gate, decides nothing, chooses no `M`,
> does not relax OD-6, computes no inferential result, writes no ledger row, and promotes no value.
