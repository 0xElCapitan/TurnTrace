# Cycle-008 — Rung-3 Ladder Semantics: Form Only, Freezes Nothing (S04.4)

**Date:** 2026-06-21
**Cycle / sprint:** Cycle-008, Sprint **S04 — Governance & convention docs** (deliverable S04.4).
**Type:** governance / convention — a docs-only definition of the Rung-3 comparison **form**, and only
the form. Its sole purpose is governance clarity for a future cycle.
**Status:** Form written. **This artifact carries no claim ceiling of its own, opens no attempt, and
freezes nothing.**

> **Sanitization posture.** This doc embeds **no** raw traces, simulator logs, deck lists, card IDs/names,
> Pokémon Elements, Competition Data, Daily-Top-Episodes, Kaggle episode data, Discord/peer screenshots,
> run-dir dumps, PDFs/CSVs, `deck.csv`, `cg/`, raw evidence rows, dispersion/band/win-rate values, or any
> inferential statistic. **It states no numeric governance margin (`M`), no batch/sample sizes (`K`/`n`)
> values, no regime id, no candidate identity, no target feature family, and no threshold.** No forbidden
> agent word (*strong / competitive / optimal / calibrated / complete*) is used to describe agent
> evidence. The symbols `M` / `K` / `n` appear **only** in the list of quantities this doc declines to
> freeze.

> **Cycle-008 posture (binding for every S04 doc).** Cycle-008 does **not**: attempt Rung 3; select a
> Rung-3 target; select a candidate; freeze a numeric comparison budget; freeze `K`/`n`; freeze a regime
> id; freeze a feature family; create SP-6; write or modify a ledger row; or advance the claim ceiling.
> **The current standing claim ceiling remains Rung 2** ([`../../claim-ceiling.md`](../../claim-ceiling.md)),
> and [`../../ledger.md`](../../ledger.md) remains the **only** ceiling-bearing artifact.

---

## 1. Why this doc exists

The claim ladder needs a *definition* of what Rung 3 would mean **before** anyone proposes how to reach
it, so that a future cycle does not conflate two very different questions:

- *"What does Rung 3 mean?"* — a governance question, answered here, **form only**.
- *"What candidate should we try, and how?"* — an attempt-design question, deliberately **left open**.

This doc answers only the first. It is the analogue, one rung up, of the standing claim-ceiling posture
that bounds Rung 2 ([`../../claim-ceiling.md`](../../claim-ceiling.md)). It exists to keep Cycle-009+ from
sleepwalking into an attempt while merely trying to understand the ladder.

## 2. Rung 3 is future-only and form-only

- **Future-only.** Rung 3 is **not** earned, attempted, or in progress. The standing ceiling is **Rung 2
  — "beats random-legal."** Nothing in Cycle-008 moves toward Rung 3; this doc opens **no** attempt.
- **Form-only.** What is written here is the *shape* a Rung-3 comparison must take if one is ever
  pre-registered. It is **not** a plan, a target, or a selection. Naming the shape authorizes nothing.

## 3. The Rung-3 comparison form

> **A future candidate must beat the current non-trivial incumbent under a same-regime, fresh-evidence,
> pre-registered comparison.**

Unpacking each load-bearing term — as *form*, with no value attached:

| Form element | What it requires (no value frozen) |
|---|---|
| **future candidate** | some agent of record proposed *at that future time*; **no candidate is named or selected now** |
| **beats** | a same-regime descriptive separation in the candidate's favor, under a rule pre-registered before evidence exists; **no numeric margin (`M`) and no threshold is set now** |
| **the current non-trivial incumbent** | the standing baseline of record at the time of the future pre-registration — by construction something **better than the trivial `random_legal` baseline** that Rung 2 cleared. Naming the incumbent in the *form* is descriptive context only; it **freezes no baseline** and authorizes no attempt |
| **same-regime** | candidate and incumbent compared under **one frozen regime**, never across regimes (the standing no-cross-regime invariant); **no regime id is selected now** |
| **fresh-evidence** | evidence generated *for that future comparison*, under the pre-registered design — not a re-reading or re-labeling of existing Rung-1/Rung-2 evidence; **no eval is run and no evidence is generated now** |
| **pre-registered** | the full comparison tuple (candidate, incumbent, regime, margin, batch/sample sizes, stopping rule, feature family) is fixed **before** any band exists, in its own future pre-registration artifact under that future cycle's gates; **none of that tuple is fixed now** |

The form deliberately raises the bar above Rung 2: Rung 2 is "beats the *trivial* baseline
(`random_legal`)"; Rung 3's form is "beats the current *non-trivial* incumbent." That difference is the
entire semantic content of this doc.

## 4. What this doc explicitly does NOT freeze or do

Stated plainly so the absence is checkable (success-criterion 16.2; this is the freezes-nothing
contract):

- **No candidate identity** is selected.
- **No numeric governance margin (`M`)** is chosen or stated.
- **No `K`/`n` values** (batch count / per-batch sample size) are chosen or stated.
- **No regime id** is selected.
- **No target feature family** is selected.
- **No threshold** of any kind is set.
- **No attempt is opened**, scheduled, or implied.
- **No SP-6** is created; **no ledger row** is written; **no claim-ceiling movement** occurs.
- **No fresh evidence** is generated and **no eval** is run.

The only thing this doc fixes is the **English meaning** of a future Rung-3 comparison. Every concrete
parameter is left to a future, separately gated cycle.

## 5. Claim-ceiling posture (hard)

- **The standing ceiling remains Rung 2 — "beats random-legal."** This doc neither asserts nor advances a
  ceiling; defining what a *higher* rung would mean is not the same as claiming it.
- **[`../../ledger.md`](../../ledger.md) remains the only ceiling-bearing artifact.** A future Rung-3
  result — if one is ever pre-registered, generated, and operator-authorized — would be recorded there as
  its own append-only row, under its own terminal acts, never by editing this doc.
- **Rung 3 is earned only by the future evidence + the operator-gated terminal acts**, exactly as Rung 2
  was (the SP-6 → ledger-row → ceiling-advance sequence, each separately authorized). This doc is none of
  those acts.

## 6. Sources / traceability

- **Rung-3 form-only definition (freezes nothing; OD-C8-3 resolved):** [`02-sdd.md`](02-sdd.md) §6.4;
  [`01-prd.md`](01-prd.md) (C8-FR-6); [`03-sprint-plan.md`](03-sprint-plan.md) (S04.4; freezes-nothing AC).
- **Standing Rung-2 ceiling and "beats random-legal" scope (the rung below the form):**
  [`../../claim-ceiling.md`](../../claim-ceiling.md).
- **Same-regime / no-cross-regime invariant and the pre-registration → ledger-row → ceiling-advance
  terminal-act order (the precedent the form points at):**
  [`../cycle-007/06a-sp6-promoted-summary.md`](../cycle-007/06a-sp6-promoted-summary.md);
  [`../../ledger.md`](../../ledger.md).
- **By-reference, no-embed evidence handling a future row would reuse:**
  [`08b-ledger-metric-column-convention.md`](08b-ledger-metric-column-convention.md).
