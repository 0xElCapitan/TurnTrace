# Deferred-Lane Gate Decision — After Cycle-001 / Sprint 01

| Field | Value |
|---|---|
| **Type** | Operator decision note (docs-only; authorizes no code) |
| **Status** | Active standing decision |
| **Date** | 2026-06-18 |
| **Scope** | Governs what may be researched/planned after Sprint 01, before any Sprint 02 build gate |
| **Related** | `docs/operator/turntrace-loop-contract.md`, `docs/cycles/cycle-001-sprint-01/closeout.md`, PRD §11.3–§11.4 |

> Sanitized operator note. No raw traces, card IDs/names, deck lists, simulator logs, or
> Competition Data appear here (CC-1/CC-2, ESP). Runs are referenced by `run_id`, sanitized
> metrics, artifact names, and claim ceilings only.

## Current state

```
TurnTrace Cycle-001 / Sprint 01 is closed and integrated.
main = origin/main = f4f86c5 (or newer if housekeeping has landed).
Sprint 01 produced the first same-regime local comparison artifact.
Comparison: run-0001 vs run-0002 under regime-v001.
n = 12.
run-0001 = random_legal-v001.
run-0002 = scripted-v001.
```

## Observed metric movement (sanitized; run-0001 → run-0002, same regime-v001, n=12)

| metric | run-0001 | run-0002 |
|---|---|---|
| win_rate | 0.5 | 0.8333 |
| avg_turns | 13.42 | 7.67 |
| illegal_action_rate | 0.0 | 0.0 |
| timeout_rate | 0.0 | 0.0 |
| error_rate | 0.0 | 0.0 |

## What this movement is NOT

- This is **not** a gameplay-strength claim.
- This is **not** a statistical-significance claim.
- This is **not** a cross-regime claim.
- This is **not** evidence of leaderboard quality.
- This does **not** raise the claim ceiling above Rung 1.

The movement reflects a deterministic lowest-index policy played against the same random opponent
under the same frozen regime, at n=12. The forbidden agent claim words (*strong, competitive,
optimal, calibrated, complete*) remain forbidden. The ledger remains the only ceiling-bearing
artifact.

## Gate decision

```
Deferred-lane status after Sprint 01: NARROW PLANNING GATE OPENED.
Broad optimization remains closed.
```

A metric moved for an explainable, agent-only reason — enough to open a **narrow planning** lane
(per PRD §11.4), but **not** the broad-optimization lane. This note exists specifically to prevent
the Sprint 01 metric movement from being misread as permission for broad optimization.

## Allowed narrow planning

- explainability of the first delta
- failure-mode taxonomy
- comparison robustness
- trace-safe and Competition-Data-safe aggregate diagnostics
- provenance and ledger hardening
- delta_report hardening
- operator decision framing for a future improvement sprint

## Still closed

- RL
- self-play
- deck optimizer
- value model
- win-probability model
- dashboard
- ELO or tournament system
- search/lookahead/MCTS
- Kaggle upload automation
- leaderboard optimization
- agent tuning loops
- submission packaging
- two-direction ablation ledger
- SaaS/product surface

## Sprint 02 planning posture

```
Sprint 02 may be researched/planned as "Delta Explanation + Failure-Mode Taxonomy."
Sprint 02 must not directly optimize the agent unless a later operator decision explicitly opens that lane.
Sprint 02 should explain and harden the evidence loop before improving gameplay.
```

Data first, optimization second remains binding. Opening a broad-optimization lane (any item under
"Still closed") requires a **separate, explicit operator decision** that supersedes this note.
