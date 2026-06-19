# FunSearch Forward-Compatibility Appendix (Cycle-003 / Sprint 00 · S00-T5)

| Field | Value |
|---|---|
| **Type** | Docs-only notes (authorizes no code; opens no build gate; adds no dependency/scaffold/interface) |
| **Status** | Authored — Cycle-003 Sprint 00 deliverable (S00-T5); forward-compatibility notes only |
| **Date** | 2026-06-19 |
| **Lane / FR** | Lane E · C3-FR-5 · S00-T5 |
| **Scope** | Records forward-compatibility guidance that keeps TurnTrace a clean scalar-per-candidate, regime-stamped evaluator, without adding any FunSearch dependency, interface, scaffold, integration, or runtime-agent heuristic surface. |
| **Related** | `04-evidence-summary-schema-spec.md` (§4 JSON-first), `docs/cycles/cycle-002/05-reproducibility-reality.md` (§3 unseeded noise floor), `docs/operator/deferred-lane-gate-after-sprint-01.md` (still-closed lanes), `docs/claim-ceiling.md`, `docs/cycles/cycle-003/01-prd.md` (C3-FR-5), `docs/cycles/cycle-003/02-sdd.md` (§10) |

> Sanitized note. No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, or Competition Data appear here (CC-1/CC-2, ESP).
> **No dispersion metric values appear here.** Runs are referenced by `run_id`, content hashes, sanitized
> metric *names*, claim ceilings, and local path/status only. The forbidden agent claim words (*strong /
> competitive / optimal / calibrated / complete*) appear only as negated/forbidden language.

> **Boundary banner (binding).** This document opens **no build gate** and is **notes-only.** Cycle-003 adds
> **no FunSearch dependency, no interface, no scaffold, no integration, no candidate-search code, and no
> runtime-agent heuristic surface** (NG10). It records forward-compatibility properties of the *existing*
> design; it builds nothing. The runtime-agent lane and broad optimization remain **closed**
> (`docs/operator/deferred-lane-gate-after-sprint-01.md`). The claim ceiling stays **Rung 1**.

## 1. Keep TurnTrace a clean scalar-per-candidate, regime-stamped evaluator

A future automated candidate-search consumer (FunSearch-style) wants one thing from an evaluator: a
**regime-stamped scalar signal per candidate** it can rank. TurnTrace already has the right shape for this
(`01-prd.md:224-231`; `02-sdd.md:424-426`):

- the evidence-summary JSON (`04-evidence-summary-schema-spec.md` §4) carries the `regime_id` stamp and
  per-metric scalars (the seven descriptive statistics per metric);
- every signal is **same-regime by construction** and never compared across regimes (NFR-5).

The forward-compatibility guidance is simply: **do not regress this shape.** Keep evaluator outputs
regime-stamped and reducible to a per-candidate scalar; do not introduce a cross-regime signal a downstream
ranker could misread as uplift.

## 2. Keep the schema JSON-first / machine-readable

The `04-evidence-summary-schema-spec.md` schema should stay **JSON-first / machine-readable** (its §4) so a
future automated consumer is not blocked by a human-only rendering. This is a **forward-compat property of an
existing-pattern choice** (`dispersion_report.py:243-255` already emits machine-readable JSON), **not a
FunSearch coupling** (`02-sdd.md:427-428`). No FunSearch-specific field, interface, or assumption is added to
the schema.

## 3. Two preconditions a future candidate-search loop would require — both currently closed

A future candidate-search loop is **out of scope and remains closed**; recording its preconditions is what
keeps the design honest about what it does *not* yet have (`01-prd.md:228-231`; `02-sdd.md:429-431`):

- **A runtime-agent heuristic surface first — currently closed.** A search loop needs candidates to vary,
  i.e. a runtime-agent heuristic surface to mutate. That lane is **closed**: agents are frozen, and the
  runtime-agent lane and broad optimization (RL, self-play, deck optimizer, value/win-probability model,
  search/lookahead/MCTS, ELO/tournament, leaderboard, dashboard) all remain on the still-closed list
  (`docs/operator/deferred-lane-gate-after-sprint-01.md:71-87`; NG7, NG8). Opening it requires a separate
  explicit operator decision.
- **An evaluator that clears the unseeded RNG noise floor.** Because runs are unseeded
  (`seed_controlled=false`), the observed dispersion of a metric is the spread of the **whole unseeded
  process** — it conflates agent behaviour with uncontrolled simulator RNG and cannot be separated into an
  isolated agent-only quantity (`05-reproducibility-reality.md` §3). A future evaluator signal would need to
  **average over enough matches/batches to clear that noise floor** before a per-candidate scalar is stable
  enough to rank on. This is a property of the measurement reality, recorded here as a forward note — not a
  task this cycle undertakes.

## 4. What this appendix deliberately does NOT do

- **No FunSearch dependency / interface / scaffold / integration / candidate-search code** is added (NG10).
  Any such surface here → HALT (AC-S00-5, AC-X9).
- **No runtime-agent heuristic surface** is opened; the lane stays closed (NG7;
  `docs/operator/deferred-lane-gate-after-sprint-01.md`).
- **No broad optimization, no Kaggle submission automation** (NG8, NG9).
- **No value promoted, no ceiling advanced.** Notes-only; Rung 1 held.

## 5. Traceability

| Requirement (PRD) | This appendix |
|---|---|
| C3-FR-5 keep a clean scalar-per-candidate, regime-stamped evaluator | §1 |
| C3-FR-5 schema stays JSON-first / machine-readable (forward-compat, not coupling) | §2 |
| C3-FR-5 future loop needs a (closed) heuristic surface + a noise-floor-clearing evaluator | §3 |
| C3-FR-5 notes-only; no dependency/scaffold/interface/heuristic surface added | §4 |

> **Sources:** `04-evidence-summary-schema-spec.md` §4 (JSON-first); `analysis/dispersion_report.py:243-255`
> (existing machine-readable JSON); `docs/cycles/cycle-002/05-reproducibility-reality.md` §3 (unseeded
> process / noise floor); `docs/operator/deferred-lane-gate-after-sprint-01.md:71-87` (still-closed lanes);
> `docs/claim-ceiling.md`; `docs/cycles/cycle-003/01-prd.md` (C3-FR-5); `docs/cycles/cycle-003/02-sdd.md`
> (§10). Claim ceiling: **Rung 1 (unchanged).** This appendix opens no build gate, adds no FunSearch surface,
> opens no runtime-agent lane, writes no ledger row, and promotes no value.
