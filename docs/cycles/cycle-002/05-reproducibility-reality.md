# Reproducibility-Reality Note (Cycle-002 / Sprint 00 · S00-T2)

| Field | Value |
|---|---|
| **Type** | Docs-only posture note (authorizes no code; opens no build gate) |
| **Status** | Active standing posture for Cycle-002 |
| **Date** | 2026-06-18 |
| **Lane / FR** | Lane F · C2-FR-6 |
| **Scope** | Records the honest reproducibility posture that bounds every Cycle-002 run, especially at a larger `n`. |
| **Related** | `docs/claim-ceiling.md` (§ "Reproducibility posture"), `frozen/seeds/seed-set-v001.json`, `frozen/regimes/regime-v001.json`, `docs/cycles/cycle-002/00-research-and-planning.md` (RQ-8), `docs/cycles/cycle-002/02-sdd.md` (§9.2), `docs/cycles/cycle-002/03-sprint-plan.md` (S00-T2) |

> Sanitized posture note. No raw traces, card IDs/names, deck lists, hand contents, simulator
> logs, PDFs/CSVs, `deck.csv` rows, or Competition Data appear here (CC-1/CC-2, ESP). Runs are
> referenced by `run_id`, sanitized metrics, and artifact names only.

## 1. `seed_controlled=false`

The capability probe found **no controllable RNG seed**: `sim/capabilities.json` records
`seed_controlled=false`, and the simulator's match-start entry point accepts no seed
(`frozen/seeds/seed-set-v001.json` `rationale`; `docs/claim-ceiling.md:42-52`). This is a recorded
property of the local simulator surface, not a choice and not a defect we may paper over. Every
Cycle-002 run inherits it: runs are `mode=unseeded`, and records carry `match_index`, **not**
`seed` (`frozen/regimes/regime-v001.json:8-9`).

## 2. "Stable" means distribution-stable + audit-trail — not byte-identical replay

Because there is no controllable seed, "stable" in this project is defined honestly as
**distribution-stable plus an audit trail**, and **not** byte-identical replay
(`docs/claim-ceiling.md:42-52`; NFR-3):

- **Distribution-stable** — re-running yields a *new* run dir whose sanitized metric distribution
  matches, not a byte-identical reproduction of prior traces.
- **Audit-trail** — per-decision canonical traces, `trace_hash`, and the recorded RNG events
  (`obs.logs`) make each run verifiable and tamper-evident on its own terms.

The determinism smoke is therefore **explicitly skipped** and recorded as `mode=unseeded`. This
posture does not weaken at a larger `n`: more matches sharpen the observed distribution, but they
do not introduce a seed and do not convert distribution-stability into replay.

## 3. Unseeded dispersion conflates agent behavior with simulator RNG

Under unseeded runs, the observed dispersion of a metric across repeated same-regime batches is the
spread of the **whole unseeded process**. It **conflates agent behavior with uncontrolled simulator
RNG and cannot be separated** into an isolated "agent variance"
(`docs/cycles/cycle-002/00-research-and-planning.md:206-208`; research RQ-8;
`docs/cycles/cycle-002/03-sprint-plan.md:152-156`). Two consequences bind every Cycle-002 report:

- Any cross-run dispersion figure describes the agent *and* the simulator's uncontrolled randomness
  together. It is never presented as an isolated agent-variance estimate.
- Each dispersion statement carries its `n` and `regime_id` and is framed as *observed* spread of
  the unseeded process — a description of what happened, not an inference about the agent alone.

## 4. Cycle-002 cannot isolate "agent variance" without seed control

It follows directly from §3 that **Cycle-002 cannot isolate "agent variance"** while
`seed_controlled=false`. Separating agent-driven variation from simulator RNG would require a
controllable seed the local surface does not expose. Until seed control is proven, "agent variance"
is not a quantity this loop can measure, and no Cycle-002 artifact reports one.

## 5. No manufactured seed control; byte-identical determinism stays out of scope

- **No manufactured seed control.** Cycle-002 does **not** invent, simulate, or assert a seed the
  simulator does not provide. Any fixed seed used inside a *test harness* (for test determinism
  only) does not manufacture simulator seed control: `sim/capabilities.json: seed_controlled=false`
  is unchanged, and real-run reproducibility stays `mode=unseeded` / distribution-stable +
  audit-trail (`docs/cycles/cycle-002/03-sprint-plan.md:527-530`).
- **Byte-identical determinism remains out of scope while seed control is false.** Byte-identical
  replay is a future upgrade *only if* seed control is later proven
  (`docs/claim-ceiling.md:50-52`). It is explicitly not pursued in Cycle-002, and its absence is
  recorded honestly rather than worked around.
