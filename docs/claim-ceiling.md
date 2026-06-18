# Claim Ceiling (PR-11)

> A blunt, code-factual statement of exactly what this loop does and does **not**
> establish, so no one (including future-us) overstates the evidence (plan §1, §2).
> The **experiment ledger (`docs/ledger.md`) is the only ceiling-bearing artifact**;
> this document states the standing posture that bounds every ledger row.

## What the loop measures

For a frozen regime (`regime-v001` = seed-set + opponent-pool + deck-pool +
metrics-spec), at a stated sample size `n`:

- **Legal completion** — whether `random_legal` plays full games end-to-end without
  crashing or emitting a malformed selection (where detectable).
- **Win / loss / draw / error rate** — from the single `result` enum, agent-under-test
  (player 0) perspective, against the frozen opponent.
- **Throughput & game length** — `wall_clock_ms`, `turns`, `avg_*`.
- **An audit trail** — per-decision traces (observable signals only) hashed for integrity.

## What the loop does NOT measure (yet)

- **Strength in any absolute sense.** A win rate vs `random_legal` (here, a mirror) is
  **not** evidence of quality. Sprint 00 sits at **ladder Rung 1** (legal completion).
- **Skill against the real meta**, probability reliability, or per-decision quality.
- **Generalization** beyond this frozen pool and deck. A rate is a statement about *this
  regime*.
- **Reproducibility by byte-identical replay** — see posture below.

## Fixed inputs (the regime)

`regime-v001`: `seed-set-v001` (unseeded — match indices), `opponent-pool-v001`
(one opponent: `random_legal`, mirror), `deck-pool-v001` (refs + hashes only — no card
lists), `metrics-spec-v001` (correctness gates, no strength gate). A change to any
component, or a new sim version, is a **new** regime (`v002`), never an edit.

## Zero-modeling invariant

There are **no learned components** in this loop. `random_legal` is fixed and stateless;
`agent_meta` scores (none emitted) would be uncalibrated heuristics, never
win-probabilities. Nothing here is trained, tuned, or fit.

## Reproducibility posture: distribution-stable + audit-trail

The capability probe found **no controllable RNG seed** (`sim/capabilities.json:
seed_controlled=false`). Therefore (NFR-3):

- Records carry `match_index`, not `seed`; runs are `mode=unseeded`.
- Reproducibility is **distribution-stable** (re-running yields a *new* run dir with a
  matching distribution, not byte-identical traces) **plus an audit trail** (per-decision
  canonical traces, `trace_hash`, and `obs.logs` RNG events).
- The determinism smoke is **explicitly skipped** and recorded as `mode=unseeded`.
  Byte-identical replay is a future upgrade only if seed control is later proven.

## Forbidden claim language (for the agent)

The agent's evidence must **never** be described with: **strong, competitive, optimal,
calibrated, complete.** These words may appear only as forbidden/negated language (as
here). The loop measures and logs; a human makes bounded claims from the evidence, with
the sample size in view, never exceeding the ledger row's `claim_ceiling`.

## Never compare across regimes

A result is meaningful only relative to its own `regime_id` (NFR-5). Two rates under
different regimes are not comparable and their difference is not uplift.
