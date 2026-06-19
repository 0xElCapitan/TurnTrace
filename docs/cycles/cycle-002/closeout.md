# Cycle-002 Closeout — "Evaluation Scale + Comparison Confidence"

| Field | Value |
|---|---|
| **Cycle** | Cycle-002 |
| **Status** | **CLOSED / ACCEPTED / INTEGRATED** |
| **Final main** | `7ed156a` (this closeout commit follows) |
| **Claim ceiling** | Rung 1 (unchanged across the whole cycle; not advanced) |
| **Broad optimization** | **closed** |
| **Runtime-agent improvement lane** | **closed** |
| **Date** | 2026-06-18 |

> Docs-only historical boundary artifact. It closes Cycle-002 at Rung 1 and records what
> the cycle did and did not establish. **Sanitized narrative only:** no dispersion metric
> values, no win-rate values, no baseline/candidate performance table, no raw traces, no
> card IDs/names, deck lists, hand contents, opponent data, simulator logs, PDFs/CSVs,
> `deck.csv` rows, or Competition Data appear here (CC-1/CC-2, ESP). Runs are referenced by
> id pattern, count, and sanitized artifact names only. The forbidden agent claim words
> (*strong / competitive / optimal / calibrated / complete*) appear only as negated/forbidden
> language, as here.

## 1. Cycle title and date

**Cycle-002 — Evaluation Scale + Comparison Confidence** (alt. framing: "From n=12 Toy
Comparison to Stable Evaluation Harness"). Closed 2026-06-18.

## 2. Final durable state

- `origin/main` is at **`7ed156a`** (`feat: add TurnTrace Cycle-002 dispersion reporting`).
- **Sprint 00 — accepted / closed / pushed** (criteria / reproducibility / ledger-discipline docs).
- **Sprint 01 — accepted / closed / pushed** (scale foundation: additive `regime-v002` + `seed-set-v002`, dry-run budget, proofs).
- **Sprint 02 — accepted / closed / pushed** (repeated batch + descriptive-dispersion reporting; review PASS WITH NITS, audit PASS).
- **Cycle-002 is closed at Rung 1.**

## 3. What Cycle-002 earned

The cycle improved the **evaluation harness**, not the agent. It earned:

- Rung-2-**readiness** criteria/posture docs (criteria defined, not claimed).
- An **additive `regime-v002`** (the existing `regime-v001` and its four components stayed byte-unchanged).
- An **additive `seed-set-v002` at `N = 500`** (`mode=unseeded`; a larger ordered match-index list).
- A **dry-run budget procedure** that chose `N` and a **3 GiB storage ceiling** before any batch.
- A **repeated same-regime batch capability** under one `regime-v002`, frozen agents.
- **K = 20 → 40 local sealed run dirs** (baseline `run-v002-b-<i>` / candidate `run-v002-c-<i>`,
  i ∈ 1..20), described here by **count and id pattern only** (kept local/gitignored).
- An **offline descriptive `analysis/dispersion_report.py`** reporting only the ratified
  descriptive vocabulary (`count / min / max / range / mean / median / spread`), with a
  Rung-1 footer, an unseeded-process caveat, a single-regime guard, and sanitized reads.
- **Tests** proving dispersion behavior, sanitization (poison not surfaced), the import
  boundary, the single-regime refusal, and missing-input handling.
- Preserved **no-ledger-by-default** and **frozen-file** protections at the larger scale.

## 4. What Cycle-002 did NOT earn

Cycle-002 did **not** earn:

- a Rung-2 claim (no "beats random-legal" verdict);
- any claim-ceiling advancement;
- any tracked dispersion metric values (none promoted to tracked status);
- any ledger update or new ledger row;
- any runtime-agent change;
- any broad-optimization lane;
- the paired-delta stretch (S02-T4, not built);
- an `eval/run_batch.py` batch runner (S02-T5, not built);
- a gameplay-strength, cross-regime, leaderboard, calibration, or statistical-significance claim.

The forbidden agent claim words remain forbidden: no artifact describes any agent as
*strong, competitive, optimal, calibrated,* or *complete.*

## 5. Claim-ceiling decision

**Hold at Rung 1.** No Cycle-002 artifact carries a ceiling of its own; `docs/ledger.md`
remains the **only** ceiling-bearing artifact. No row was advanced past Rung 1.

## 6. Why Rung 2 was not earned

The Rung-2 admission gate (`docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` §2) is
**conjunctive** — all five conditions must hold. Cycle-002:

- performed **no operator-approved inferential design** (the design must be authored and
  ratified before any comparison is read as evidence);
- had **no pre-registered margin** approved in advance;
- took **no operator-authorized advance** of the ledger's claim ceiling;
- and produced larger-`n`, **unseeded** data, which is a finer **resolution** of the same
  distribution — explicitly **not** a higher rung.

Because three of the five conditions were not met (by design, per OD-6/OD-8), a Rung-2
consideration is not on the table. Cycle-002 built the *readiness infrastructure* a future
cycle could use, and stopped there.

## 7. Ledger decision

- `docs/ledger.md` is **unchanged** — it still holds only the two Rung-1 `regime-v001`
  rows from Cycle-001.
- There are **no `run-v002` rows**.
- The local Sprint 02 batch was **non-deliverable** (no `--deliverable` / `--ledger`); per
  OD-5 the ledger does not grow a row per batch, and no deliverable run was designated.

## 8. Local evidence policy

- The local run dirs and the local dispersion reports remain **gitignored State Zone /
  evidence** (ESP-1); only `runs/.gitkeep` is tracked.
- **No metric values were promoted to tracked status.** This tracked closeout is **narrative
  only** and carries no dispersion numbers.
- Review / audit / acceptance markers and the dispersion outputs live under gitignored
  `grimoires/loa/a2a/cycle-002/...` and are never staged.

## 9. Carry-forward items (none authorized here)

- A future **Rung-2 admission cycle** — only if the operator later authorizes the full
  conjunctive gate (an explicit inferential design + a pre-registered margin + a ceiling
  advance).
- An optional **SP-6 tracked sanitized dispersion summary** — only with explicit operator
  authorization; even then, counts/aggregates/dispersion only, never raw rows.
- Optional **evidence hardening at a larger K** (e.g. K=50 / K=100) under the same ceiling.
- The optional **S02-T4 paired-delta** stretch and **S02-T5 `eval/run_batch.py`** wrapper.
- **OD-9 `.beads/` gitignore housekeeping** (handled separately; not Cycle-002 build scope).
- The **runtime-agent improvement lane remains separate and closed.**

## 10. Final statement

**Cycle-002 is closed at Rung 1.** No additional work is authorized. Opening any build gate,
any still-closed broad-optimization lane, a Rung-2 admission, an SP-6 tracked summary, or any
runtime-agent change each requires a separate, explicit operator decision
(`docs/operator/turntrace-loop-contract.md`,
`docs/operator/deferred-lane-gate-after-sprint-01.md`).

---

> **Sources:** `docs/cycles/cycle-002/{00-research-and-planning,01-prd,02-sdd,03-sprint-plan}.md`;
> `docs/cycles/cycle-002/{04-rung-2-readiness-criteria,05-reproducibility-reality,06-ledger-report-discipline,07-operator-decision-register}.md`;
> `docs/cycles/cycle-002/sprint-0{0,1,2}-implementation-report.md`; `docs/claim-ceiling.md`;
> `docs/ledger.md`; the cycle-001 convention `docs/cycles/cycle-001/closeout.md`. Final main at
> closeout authoring: `7ed156a`. Claim ceiling: Rung 1 (unchanged).
