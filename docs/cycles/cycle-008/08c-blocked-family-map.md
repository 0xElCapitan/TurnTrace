# Cycle-008 — Blocked-Family Map (S04.3)

**Date:** 2026-06-21
**Cycle / sprint:** Cycle-008, Sprint **S04 — Governance & convention docs** (deliverable S04.3).
**Type:** governance / convention — a tracked, sanitized map of which families of work are *measurable
now*, which are *documented but not built*, and which are *blocked in Cycle-008 and why*.
**Status:** Map written. **This artifact carries no claim ceiling of its own and freezes nothing. It
builds nothing it documents.**

> **Sanitization posture.** This map embeds **no** raw traces, simulator logs, deck lists, card IDs/names,
> Pokémon Elements, Competition Data, Daily-Top-Episodes, Kaggle episode data, Discord/peer screenshots,
> run-dir dumps, PDFs/CSVs, `deck.csv`, `cg/`, raw evidence rows, dispersion/band/win-rate values, or any
> inferential statistic. **No numeric governance margin `M` is chosen or stated.** No forbidden agent word
> (*strong / competitive / optimal / calibrated / complete*) is used to describe agent evidence. Every
> family is named in **sanitized terms only**; failure modes are cited by id, never by embedding their
> detector logic or any card data.

> **Cycle-008 posture (binding for every S04 doc).** Cycle-008 does **not**: attempt Rung 3; select a
> Rung-3 target; select a candidate; freeze a numeric comparison budget; freeze `K`/`n`; freeze a regime
> id; freeze a feature family; create SP-6; write or modify a ledger row; or advance the claim ceiling.
> **The current standing claim ceiling remains Rung 2** ([`../../claim-ceiling.md`](../../claim-ceiling.md)),
> and [`../../ledger.md`](../../ledger.md) remains the **only** ceiling-bearing artifact.

---

## 1. Purpose

Scouting and review surface many *ideas* for what to measure or build. Most of them are **not** in scope
for Cycle-008 — some because the simulator does not record the needed signal, some because they require a
separate operator authorization, and some because the whole governance posture blocks them this cycle.
This map records each family and **why it is blocked**, so a future run does not improvise its way around
a gate by mistaking "interesting" for "authorized." **Documenting a family here is not a step toward
building it** — the map builds nothing.

## 2. The three-class surface taxonomy (SDD §6.3)

Each scouting-inspired *measurement surface* falls into exactly one of three classes.

### 2.1 Measurable now — built this cycle (S01 diagnostic)

These are the five descriptive surfaces the S01 trace diagnostic actually emits, each computed from
**already-recorded** fields (no new instrumentation), named here in sanitized form (full definitions:
[`02-sdd.md`](02-sdd.md) §2.2):

| Surface (measurable now) | Descriptive form (sanitized) |
|---|---|
| Outcome / ending-cause aggregates | counts/rates over the result and ending-cause enums |
| Board-shape distributions | per-side active-present rate and bench-count `min/max/range/mean/median/spread` |
| Prize trajectory | the prize-count trajectory's `min/max/range/mean/median/spread`; terminal counts per side |
| Decision-latency distribution | aggregate latency `min/max/range/mean/median/spread` (never raw rows) |
| Error / illegal / malformed-selection regression | error-presence count; illegal total; timeout reported as the soft, undetectable signal it is |

Every one of these is **descriptive of what occurred** — none is framed as a mistake, fault, or quality
score, and none requires energy, per-Pokémon state, card identity, retreat cost, or decoded option
semantics. This class is the only class **built** in Cycle-008 (S01).

### 2.2 Needs future sim instrumentation — documented, NOT built

These families would require the simulator to record signals it does not record today (no energy field,
no per-Pokémon state; only raw option tokens are available). They are named so a future cycle can scope
them deliberately — **they are not built in Cycle-008** (OD-C8-5; [`02-sdd.md`](02-sdd.md) §6.3; NFR-9):

- backup-attacker readiness
- attach / energy tempo
- attack-vs-setup timing
- contextual-retreat semantics

Status for all four: **documented, not built.** No new simulator instrumentation, no per-Pokémon state
extraction, and no option-token decoding is added this cycle.

### 2.3 Requires separate operator authorization — documented, NOT built

These are **per-decision quality** judgments. They are flagged `detector: forbidden` in the failure-mode
taxonomy ([`../../failure-mode-taxonomy-v001.md`](../../failure-mode-taxonomy-v001.md)), meaning no
detector may be built for them without a separate, explicit operator authorization. They are cited by id
and sanitized label only — their detector logic and any card data are **not** reproduced here:

| Failure-mode id | Sanitized label | Status |
|---|---|---|
| FM-03 | per-decision quality of prize trades | `detector: forbidden` — documented, **not built** |
| FM-04 | wasted resources | `detector: forbidden` — documented, **not built** |
| FM-06 | missed lethals | `detector: forbidden` — documented, **not built** |
| FM-08 | bad search targets | `detector: forbidden` — documented, **not built** |

Cycle-008 adds **no per-decision quality scoring** and **no per-Pokémon/card/deck semantic
instrumentation** for any of these (NFR-10).

## 3. Families blocked at the governance level in Cycle-008

Beyond the surface taxonomy, the following families are blocked for the **whole** cycle. Each is listed
with the reason it is out of scope. Cycle-008 documents them; **no sprint builds them.**

| Blocked family | Why it is blocked in Cycle-008 |
|---|---|
| **Rung-3 attempts** | The cycle is bounded to diagnostics + governance docs; Rung 3 is future-only and **form-only** this cycle (see [`08d-rung3-form-only-semantics.md`](08d-rung3-form-only-semantics.md)). No attempt is opened. |
| **Target / candidate selection** | Selecting a Rung-3 target or candidate would freeze a comparison this cycle deliberately leaves open. None is selected. |
| **Numeric comparison budget / `K`/`n` / regime id / feature family** | Freezing any of these is choosing a comparison; Cycle-008 freezes none, and **no numeric margin `M` appears in any tracked artifact**. |
| **Fresh evidence / eval promotion** | No eval is run, no fresh evidence is generated, and no summary is promoted (no SP-6). The standing evidence is referenced, never regenerated. |
| **Runtime agent changes** | No runtime agent, heuristic, or value model is implemented or modified; the standing frozen agent is not tuned. |
| **Heuristic / candidate / search-loop / FunSearch / RL / self-play / MCTS / tournament / deck-optimizer / dashboard work** | This entire search-and-learning family is out of scope; none is built, tuned, or scaffolded. |
| **Per-decision quality scoring** | Blocked per §2.3 (FM-03/04/06/08 `detector: forbidden`); no scorer is added. |
| **Per-Pokémon / card / deck semantic instrumentation** | Blocked per §2.2 (needs instrumentation that does not exist) and the no-embed rule below; none is added. |
| **Raw data of any kind in tracked artifacts** | Raw Competition Data, Pokémon Elements, deck lists, card IDs/names, raw traces, simulator logs, run-dir dumps, `deck.csv`, `cg/`, PDFs/CSVs, Discord screenshots, peer data, and Kaggle/Daily-Top-Episode content **may not enter** any tracked artifact. Evidence is referenced by sanitized hash + cited summary only (see [`08b-ledger-metric-column-convention.md`](08b-ledger-metric-column-convention.md)). |

## 4. How to move a blocked family (future cycles)

A blocked family becomes buildable only by the appropriate gate, not by reclassification in this map:

- A **"needs instrumentation"** family (§2.2) becomes measurable only after a future cycle adds the
  recording capability through its own PRD/SDD/sprint pipeline — never as a "while we're here" addition.
- A **"requires authorization"** family (§2.3) becomes buildable only after a **separate explicit
  operator authorization** lifts its `detector: forbidden` status.
- A **governance-blocked** family (§3) becomes reachable only when a future cycle's PRD/SDD authorizes it
  and (for any ceiling movement) the operator-gated terminal acts are taken.

Until then, these families remain **Cycle-009+ candidates, documented and not built.**

## 5. Sources / traceability

- **Three-class surface taxonomy:** [`02-sdd.md`](02-sdd.md) §6.3; [`01-prd.md`](01-prd.md) (C8-FR-5.3);
  [`03-sprint-plan.md`](03-sprint-plan.md) (S04.3 deliverable; OD-C8-5).
- **Measurable-now surfaces (the S01 diagnostic output shape):** [`02-sdd.md`](02-sdd.md) §2.2;
  [`05-s01-implementation-report.md`](05-s01-implementation-report.md).
- **Failure modes FM-03/04/06/08 (`detector: forbidden`), cited by id only:**
  [`../../failure-mode-taxonomy-v001.md`](../../failure-mode-taxonomy-v001.md).
- **No-embed / sanitized-reference rule:** [`08b-ledger-metric-column-convention.md`](08b-ledger-metric-column-convention.md);
  [`03-sprint-plan.md`](03-sprint-plan.md) (§9 surface scope).
- **Ceiling posture (no doc carries a ceiling; ledger is the only ceiling-bearing artifact):**
  [`../../claim-ceiling.md`](../../claim-ceiling.md); [`../../ledger.md`](../../ledger.md).
