# Rung 2 Readiness Criteria (Cycle-002 / Sprint 00 · S00-T1)

| Field | Value |
|---|---|
| **Type** | Docs-only criteria note (authorizes no code; opens no build gate) |
| **Status** | Active standing criteria for Cycle-002 |
| **Date** | 2026-06-18 |
| **Lane / FR** | Lane E · C2-FR-5 |
| **Scope** | Defines what a *future* Rung 2 consideration would minimally require. Cycle-002 defines these criteria; it does not meet or claim them. |
| **Related** | `docs/claim-ceiling.md`, `docs/ledger.md`, `docs/operator/turntrace-loop-contract.md`, `docs/cycles/cycle-002/00-research-and-planning.md` (RQ-4), `docs/cycles/cycle-002/01-prd.md` (C2-FR-5), `docs/cycles/cycle-002/02-sdd.md` (§9.1), `docs/cycles/cycle-002/03-sprint-plan.md` (S00-T1, OD-8), `docs/cycles/cycle-000-bootstrap/01-turntrace-prd.md:274-276` |

> Sanitized criteria note. No raw traces, card IDs/names, deck lists, hand contents, simulator
> logs, PDFs/CSVs, `deck.csv` rows, or Competition Data appear here (CC-1/CC-2, ESP). Runs are
> referenced by `run_id`, sanitized metrics, artifact names, and claim ceilings only.

## 1. Where Cycle-002 stands on the ladder

The maturity ladder's **Rung 1** is legal end-to-end play: the loop runs full games without
crashing or emitting a malformed selection (where detectable), and logs legality/throughput
honestly (`docs/claim-ceiling.md:8-19`). Every result to date — including the existing
same-regime `run-0001` vs `run-0002` pair under `regime-v001` at `n=12` — is held at **Rung 1**
because the sample is small and **no inferential design exists** (`docs/cycles/cycle-002/00-research-and-planning.md:159-161`).

**Rung 2** on the ladder is *"beats random-legal"* (`docs/cycles/cycle-000-bootstrap/01-turntrace-prd.md:274-276`).
The `run-0002` (`scripted-v001`) vs `run-0001` (`random_legal-v001`) pair has the *shape* of that
comparison, but a shape is not a Rung — the shape held at Rung 1 is a measurement, never a verdict
of agent quality.

## 2. What a future Rung 2 consideration would minimally require

A future Rung 2 **consideration** (not a claim) would minimally need **all five** of the following
(`docs/cycles/cycle-002/00-research-and-planning.md:161-168`; SDD §9.1):

1. **Same-regime baseline-vs-candidate comparison at a justified larger `n` under one regime.**
   Baseline and candidate both run under a single, frozen `regime-vNNN` (the seed-set is a regime
   component, so a larger `n` is a *new* regime, never an edit of an existing one). The larger `n`
   must be justified, not assumed.
2. **An explicitly designed and operator-approved inferential procedure.** The inferential design
   is authored and ratified *before* the comparison is read as evidence. Significance language
   without an explicit, approved design is forbidden (`docs/claim-ceiling.md`; the brief).
3. **The candidate exceeding the random-legal baseline by a pre-registered margin under that
   design.** The margin is fixed in advance (pre-registered) as part of the approved design, so the
   threshold cannot be chosen after seeing the numbers.
4. **Provenance and audit-trail intact.** Source-hash provenance, per-decision canonical traces,
   `trace_hash`, and the regime tuple stamp all remain verifiable for every run in the comparison.
5. **A deliberate, operator-authorized advance of `claim_ceiling` in the ledger.** The experiment
   ledger (`docs/ledger.md`) is **the only artifact that can carry a higher ceiling**
   (`docs/claim-ceiling.md:5-6`). Advancing it past Rung 1 is a separate, explicit operator
   decision — never an automatic consequence of a number moving.

These five are conjunctive: missing any one means a Rung 2 consideration is not yet on the table.

## 3. Cycle-002 does NOT claim Rung 2

Cycle-002 **defines** the criteria above and **does not meet or claim them** (OD-8, ratified —
`docs/cycles/cycle-002/03-sprint-plan.md:563`). Specifically:

- No artifact in Cycle-002 asserts that any agent "beats random-legal" as a Rung 2 verdict.
- The inferential design of §2.2 and the ceiling advance of §2.5 are a **separate operator
  decision** that this document does not make and does not pre-authorize.
- Larger-`n` work in Cycle-002 raises sampling *resolution* of the same unseeded distribution; a
  tighter view of the same distribution is **not** a higher rung
  (`docs/cycles/cycle-002/00-research-and-planning.md:155`).
- The ledger remains the only ceiling-bearing artifact, and no Cycle-002 row advances its ceiling.

## 4. What this document does NOT claim

This document is a criteria note. It makes **no agent-quality claim** of any kind. In particular it
does **not** assert that any agent is **strong, competitive, optimal, calibrated, or complete** —
those five words are forbidden as affirmative agent claims and appear here only as the forbidden
language they are (`docs/claim-ceiling.md:54-59`). It also makes no claim of statistical
significance, no leaderboard status, no calibration, no optimality, no completeness, and no
cross-regime uplift — a result is meaningful only relative to its own `regime_id`, and two rates
under different regimes are not comparable and their difference is not uplift (NFR-5;
`docs/claim-ceiling.md:62-65`).
