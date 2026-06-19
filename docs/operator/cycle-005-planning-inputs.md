# Cycle-005 Planning Inputs — Pre-Planning Carry-Forward Index

| Field | Value |
|---|---|
| **Type** | Operator planning-input note (docs-only; authorizes no code, plans no cycle) |
| **Status** | Active standing note — consumed at Cycle-005 planning |
| **Date** | 2026-06-19 |
| **Scope** | Lists what Cycle-005 planning must consume. It does **not** plan Cycle-005, open a build gate, advance any claim ceiling, promote any value, or mutate the ledger. |
| **Related** | `docs/cycles/cycle-004/06-audit-report.md` §9, `docs/cycles/cycle-004/07-closeout.md` §8/§9; `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` (SP-8/SP-9); `docs/failure-modes.md` (FM-10/FM-11); `docs/operator/turntrace-loop-contract.md` |

> Sanitized operator note. No raw traces, card IDs/names, deck lists, simulator logs, episode
> datasets, or Competition Data appear here (CC-1/CC-2, ESP). This is a pointer index only — the
> authoritative text lives in the linked artifacts.

## What Cycle-005 planning must consume

1. **Cycle-004 audit carry-forwards C1–C4** (pre-promotion hardening of the evidence-summary
   validator) — from `docs/cycles/cycle-004/06-audit-report.md` §9 (also recorded in the closeout §8):
   - **C1 (priority)** — make the validator's digest-shape / allow-list **positional**, so a known
     field name in a non-schema position cannot bypass content checks.
   - **C2** — tighten the forbidden-word negation heuristic to immediate-precedence negation.
   - **C3** — repo-root-resolve the `--out` guard (`_refuse_tracked_out`).
   - **C4** — warn on empty `hashes`.

   These are non-blocking for build-only Cycle-004 (which promoted nothing) but **mandatory before
   the validator becomes load-bearing at a Cycle-005 value-promotion gate**.

2. **This competition-findings docs patch** (the patch that added this note) — operator decisions
   **SP-8** (simulator authoritative) and **SP-9** (Daily Top Episodes posture) in
   `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md`, plus failure modes **FM-10 / FM-11** in
   `docs/failure-modes.md`.

3. **Simulator-authoritative behavior (SP-8 / CC-10).** Runtime agents and offline analysis follow
   the simulator-offered legal options (`obs.select.option`) and the simulator terminal result/logs,
   not official-rule assumptions. The known sanitized divergences — selectability when an effect
   cannot resolve; automatic (left-to-right) multi-target ordering; simultaneous-Knock-Out prize
   ordering — are recorded as **simulator-behavior notes, not agent failures** (FM-10).

4. **Daily Top Episodes as local-only hypothesis-generation input (SP-9 / CC-6).** Offline
   scouting / training / report input only; raw datasets stay local/ignored by default; never proof
   of improvement without a same-regime TurnTrace comparison; never a runtime dependency. Justifying
   an agent change from top episodes alone is the FM-11 failure mode.

## What this note does NOT do

- It does **not** plan Cycle-005 (no PRD/SDD/sprint plan, no task breakdown, no scoping).
- It opens **no** build gate — the build gate still requires a separate explicit operator decision
  (OA-2 / the loop contract, `docs/operator/turntrace-loop-contract.md`).
- It advances **no** claim ceiling (Rung 1 holds) and mutates **no** ledger.
- It promotes **no** value and authorizes **no** runtime-agent, optimization, or Kaggle/episode-ingest
  work.

> When the operator opens Cycle-005, planning proceeds through the normal Loa path
> (`/plan` → PRD → SDD → sprint plan) and decides the open Rung-2 seam items (8a–8d, per
> `docs/cycles/cycle-003/07-od6-criterion-2-proposal.md` §5) and the C1–C4 hardening on their own
> merits. This note exists only so those inputs are not lost between cycles.
