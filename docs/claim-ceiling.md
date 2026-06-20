# Claim Ceiling (PR-11)

> A blunt, code-factual statement of exactly what this loop does and does **not**
> establish, so no one (including future-us) overstates the evidence (plan §1, §2).
> The **experiment ledger (`docs/ledger.md`) is the only ceiling-bearing artifact**;
> this document states the standing posture that bounds every ledger row.

## Standing claim ceiling

**Current standing ceiling: Rung 2 — "beats random-legal."** Earned for **Cycle-007**, and
only to this narrow, ledgered extent:

- **Basis (same-regime, descriptive).** One ledgered result: the candidate `scripted-v001`
  beats the `random_legal-v001` baseline under the frozen `regime-v003`, with the candidate's
  per-batch win-rate band strictly above the baseline's by at least the pre-registered
  descriptive margin across the pre-registered `K = 20` same-regime batches at `n = 500` (the
  ratified descriptive disjoint-bands rule). It is a **same-regime delta only** — no
  inferential statistic, and no forbidden agent word (below) applies even on this PASS.
- **Authority.** The committed **Rung-2 ledger row** in `docs/ledger.md` (ledger commit
  `399bbf01308dfa2fbd982b6f3b4f71730af53472`). `docs/ledger.md` stays the **only
  ceiling-bearing artifact**; this document only states the standing posture and points at
  that ledgered basis.
- **Supporting chain.** S04 PASS verdict
  (`docs/cycles/cycle-007/06-verdict-application.md` @ `a1466ba133e133bf02e0845c4639f1c0aedd5b8a`)
  → SP-6 promoted sanitized summary
  (`docs/cycles/cycle-007/06a-sp6-promoted-summary.md` @ `d445141b5f60c458a78f6e6891082ce70bf252f2`)
  → the Rung-2 ledger row (ledger commit `399bbf01…`).

**What Rung 2 does NOT grant** (the advance is bounded to the ledgered "beats random-legal"
scope — nothing more):

- **No Rung 3**, and no claim beyond "beats random-legal" under `regime-v003`.
- **No calibration** improvement, no win-probability reliability, no value model.
- **No tournament or meta strength**, no leaderboard standing, no absolute strength.
- **No runtime-agent maturity** — `scripted-v001` is an existing frozen agent re-run to
  generate evidence; no agent, heuristic, search, or learning system was built or tuned.
- **No FunSearch / RL / self-play / deck-optimization outcome** of any kind.
- **No general Pokémon TCG strength** beyond this ledgered Rung-2 scope.

A FAIL or INCONCLUSIVE would have advanced nothing; this Rung-2 standing holds **only**
because the pre-registered same-regime comparison PASSed and the separate ledgered terminal
acts (SP-6 → Rung-2 row → this advance) were each taken under OD-C7-10.

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
  **not** evidence of quality. Sprint 00's `regime-v001` mirror is a **ladder Rung 1** result
  (legal completion); the standing ceiling has since advanced to **Rung 2** (see *Standing
  claim ceiling* above) — a same-regime descriptive "beats random-legal" result, still not
  absolute strength.
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
