# Operator-Decision Register + OA-2 Readiness Checklist (Cycle-002 / Sprint 00 · S00-T4)

| Field | Value |
|---|---|
| **Type** | Docs-only register + checklist (records decisions; authorizes no code; opens no build gate) |
| **Status** | Active standing register for Cycle-002 |
| **Date** | 2026-06-18 |
| **Lane / FR** | Readiness (covers Lanes A–G) |
| **Scope** | Records the ratified Cycle-002 build assumptions and their dispositions, and the checklist of what must hold before the operator opens OA-2 for Sprint 01/02. It records; it does not authorize. |
| **Related** | `docs/cycles/cycle-002/00-research-and-planning.md`, `01-prd.md`, `02-sdd.md` (§14), `03-sprint-plan.md` (§5, §18, OD-1..OD-9 + OD-B1/OD-B3), `docs/operator/turntrace-loop-contract.md` (§6), `docs/operator/deferred-lane-gate-after-sprint-01.md`, `docs/claim-ceiling.md`, `docs/ledger.md` |

> Sanitized register. No raw traces, card IDs/names, deck lists, hand contents, simulator logs,
> PDFs/CSVs, `deck.csv` rows, run-dir dumps, or Competition Data appear here (CC-1/CC-2, ESP).
> No decision is silently opened by this register; it records ratified dispositions only.

## 1. Ratified decision register

The following Cycle-002 decisions are ratified (operator review 2026-06-18, carried from
`docs/cycles/cycle-002/02-sdd.md` §14 and `03-sprint-plan.md` §18). Dispositions are recorded
verbatim in intent; this register does not re-decide them.

| ID | Decision | Disposition |
|---|---|---|
| **OD-1** | Open OA-2 for Sprint 01/02 | Required before any `/implement` or `/run`; **no plan or note authorizes it**. Sprint 01/02 build work stays unauthorized until OA-2. |
| **OD-3** | `regime-v002` component reuse vs re-mint | **Ratified:** `regime-v002` reuses `opponent-pool-v001`, `deck-pool-v001`, and `metrics-spec-v001` **by reference + hash**; **only the seed-set changes** (SDD §5.4). |
| **OD-4** | Target `N` and batch count `K` | **Ratified:** an **output of the Sprint-01 dry-run** — schema fixed, the numbers are data; **not fixed by any planning doc**. |
| **OD-5** | Ledger-row policy for scale runs | **Ratified:** **no row per batch**; scale/batch runs are non-deliverable by default and write no ledger row; at most one explicitly designated deliverable run per regime may write a row (SDD §8.1). |
| **OD-6** | Allowed descriptive-statistics vocabulary | **Ratified:** `min`, `max`, `range`, `mean`, `median`, `spread`, `count` only; sample standard deviation / variance and all inferential statistics are excluded (SDD §7.4). |
| **OD-7** | Where the dispersion report lives | **Ratified:** full run dirs and dispersion reports are **local / git-ignored by default**; a tracked sanitized summary only on explicit **SP-6 relaxation** (SDD §4.1). |
| **OD-8** | Rung 2 stays criteria-only | **Ratified:** S00-T1 defines the Rung 2 criteria; **Cycle-002 claims no Rung 2** (SDD §9.1; see `04-rung-2-readiness-criteria.md`). |
| **OD-B1** | Batch runner C-i vs C-ii | **Ratified:** **C-i (manual `run_eval`) is the Core default**; a thin `eval/run_batch.py` wrapper stays **Stretch only** — not Core unless the operator amends scope after K is chosen, and only if K makes 2K manual runs a meaningful risk; the wrapper is loop-only and adds no eval semantics (SDD §3.3). |
| **OD-B3** | Run-id naming | **Ratified:** descriptive `run-v002-b-<i>` (baseline) / `run-v002-c-<i>` (candidate); `manifest.json` stays the authority (SDD §6.1). |
| **OD-9** | `.beads/` gitignore housekeeping | Handled separately, **not Cycle-002 build scope**; `.beads/issues.jsonl` stays unstaged. |

## 2. Ratified defaults (explicit, for unambiguous reference)

Carried verbatim from `docs/cycles/cycle-002/03-sprint-plan.md:113-126` (SDD §14 / §7.4 / §6.1):

- **Allowed statistics:** `min`, `max`, `range`, `mean`, `median`, `spread`, `count` — and nothing
  else.
- **Sample standard deviation and variance:** **excluded** in Cycle-002 reports. They are
  descriptive, but deliberately omitted to hold a bright line.
- **Inferential statistics:** **forbidden** — no confidence intervals, no p-values, no
  "significant," no hypothesis tests, no inferential error bars. (These inferential terms appear
  here only as the forbidden language they are.)
- **Batch model:** K paired comparisons = **2K** sealed run dirs (one baseline + one candidate per
  pair, all under one `regime-v002`).
- **Run IDs:** `run-v002-b-<i>` (baseline) / `run-v002-c-<i>` (candidate) — human-readable
  convenience only.
- **ID authority:** `manifest.json` is the authority for `regime_id` / `agent_id` / run metadata;
  **no logic may key off the run-id string** in place of the manifest.
- **Batch runner:** **C-i** (manual `run_eval` ×2K) is the Core default; **C-ii** (`run_batch.py`)
  is **Stretch only**, authorized only if K justifies it and the operator amends scope.
- **Component reuse:** `regime-v002` reuses opponent / deck / metrics-v001 **by reference + hash**;
  **only the seed-set changes**.
- **`regime-v001`:** stays **byte-unchanged**, with all of its components; `regime-v002` is
  **additive** future build work, not an edit and not something that already exists.
- **Ledger:** scale/batch runs are **non-deliverable by default → no ledger row**; `docs/ledger.md`
  is the only ceiling-bearing artifact.
- **Storage:** full run dirs and dispersion reports are **local / git-ignored by default**.
- **Sample size `N`:** **not fixed by any planning doc** — an output of the Sprint-01 dry-run; the
  schema is fixed, the number is data.

## 3. OA-2 readiness checklist (Sprint 01/02 build is NOT authorized yet)

> **Authorization status: Sprint 01 and Sprint 02 implementation is NOT authorized.** Both are
> build-gated and require an **explicit operator OA-2** action before any `/implement` or `/run`
> touches code, `frozen/`, or run dirs (`docs/operator/turntrace-loop-contract.md:53-57`; OD-1).
> This checklist records *readiness*; it does **not** open the gate and must not be read as opening
> it.

What must hold before the operator opens OA-2 for Sprint 01/02:

- [ ] **Scope confirmed** — Sprint 01 (scale foundation) and Sprint 02 (descriptive dispersion)
      scope is confirmed and unchanged from `03-sprint-plan.md`; no broad-optimization lane is in
      scope (`docs/operator/deferred-lane-gate-after-sprint-01.md`).
- [ ] **Agents frozen** — no `agents/runtime/` behavior change is contemplated; baseline and
      candidate agents stay frozen (risk R2).
- [ ] **Sanitization gate active** — `eval/hygiene_check.py` is wired and passing; no card
      IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs, `deck.csv` rows, or run-dir
      dumps enter tracked artifacts (CC-1/CC-2, ESP).
- [ ] **`N` and `K` set from the dry-run** — the target `N` and batch count `K` come from the
      Sprint-01 dry-run (OD-4), not from a planning doc; any interim probe file stays local/ignored
      and is never staged.
- [ ] **`regime-v001` byte-unchanged** — the larger-`n` work is an additive `regime-v002`
      (`seed-set-v002.json` + `regime-v002.json`), reusing the other three components by reference +
      hash; `regime-v001` and its components are not edited.
- [ ] **Ledger discipline preserved** — scale/batch runs stay non-deliverable (no ledger row); the
      ledger stays the only ceiling-bearing artifact; no row per batch.
- [ ] **Storage discipline preserved** — full run dirs and dispersion reports stay local/ignored by
      default; any tracked summary requires an explicit SP-6 relaxation.
- [ ] **Rung-1 hold** — Cycle-002 claims no Rung 2 (OD-8); no artifact asserts gameplay strength,
      statistical significance, leaderboard status, calibration, optimality, completeness, or
      cross-regime uplift.
- [ ] **Cadence intact** — Sprint 01/02 land only through `/implement → /review-sprint →
      /audit-sprint → explicit operator acceptance`, each closing through exactly one review and one
      audit artifact (`docs/operator/turntrace-loop-contract.md`).
- [ ] **Explicit OA-2 issued** — the operator has performed the OA-2 build-gate action for the
      specific sprint about to run. Until this box is checked, no build work begins.

## 4. This register records; it does not authorize

No decision in this document is silently opened by recording it here. The ratified dispositions in
§1–§2 describe what was decided; the checklist in §3 describes what must hold *before* OA-2. None of
it opens OA-2, authorizes `/implement`, or advances any claim ceiling. Opening a build gate, or
opening any broad-optimization lane still listed as closed
(`docs/operator/deferred-lane-gate-after-sprint-01.md`), requires a separate, explicit operator
decision that supersedes the standing notes. This document makes **no agent-quality claim** and does
not describe any agent as strong, competitive, optimal, calibrated, or complete — those five words
appear here only as the forbidden language they are.
