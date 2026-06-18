# Sprint 01 Closeout — Cycle-001 / "The First Comparison"

| Field | Value |
|---|---|
| **Sprint** | Cycle-001 / Sprint 01 — The First Comparison |
| **Status** | **CLOSED / ACCEPTED / INTEGRATED** |
| **Final commit** | `3492e615267549c2a15c09f75c72b86d039af616` (`3492e61`) |
| **main** | `main = origin/main = 3492e61` |
| **Base commit** | `d881837` — *docs: close TurnTrace Sprint 00* |
| **Branch** | `cycle-001-sprint-01-first-comparison` |
| **Integration method** | **fast-forward only** (no merge commit, no squash, no tag, no version bump) |
| **Date** | 2026-06-18 |

> Docs-only closeout note, written after the accepted fast-forward integration. Records
> sanitized evidence and Sprint 01 carry-forwards. No raw traces, card IDs/names, deck lists,
> simulator logs, or Competition Data appear here (CC-1/CC-2, ESP).

## The loop (governing contract: `docs/operator/turntrace-loop-contract.md`)

```
/implement sprint-01    → IMPLEMENTED  (grimoires/loa/a2a/sprint-01/reviewer.md)
/review-sprint sprint-01 → ACCEPT       (grimoires/loa/a2a/sprint-01/engineer-feedback.md)
/audit-sprint sprint-01  → ACCEPT       (grimoires/loa/a2a/sprint-01/auditor-sprint-feedback.md)
operator acceptance      → committed, pushed, and fast-forwarded to main
```

`/implement` held sole patch authority throughout; review and audit ran as pure-review skills
(Write/Edit disabled inside them by design — see the loop contract's Review/Audit Artifact
Persistence Rule). The sprint closed only after implementation + review + audit + operator
acceptance all held (contract §3). AC-01…AC-08 passed at HIGH confidence, independently
re-verified at both review and audit.

## Sanitized evidence

| Field | Value |
|---|---|
| `run_id` | `run-0002` |
| status | **local / git-ignored, not committed** (ESP-1; only this sanitized note + the ledger row are tracked) |
| comparison | `run-0001` (baseline) vs `run-0002` (candidate) |
| `regime_id` | `regime-v001` |
| `n` | 12 |
| baseline | `run-0001` / `random_legal-v001` |
| candidate | `run-0002` / `scripted-v001` |
| one-variable change | the agent-under-test changed from `random_legal` to the deterministic `scripted_baseline`; opponent, decks, seed-set, metrics, and regime are unchanged |
| claim ceiling | **same-regime, local, n=12 metric movement only; Rung 1 ceiling; no gameplay-strength claim** |
| `seed_controlled` | `false` |
| `mode` | unseeded / distribution-stable + audit-trail (NFR-3) |
| `timeout_detectable` | `false` (soft gate; `budget_source=assumed`) |

The experiment ledger (`docs/ledger.md`) holds the two ceiling-bearing rows (`run-0001`, `run-0002`).
The full `runs/run-0002/` tree (records, traces, manifest, hashes) remains a local, git-ignored
evidence artifact — referenced by `run_id` and content hashes only, never embedded. `run-0001`
remains local/ignored and **unmutated** from Sprint 00.

## Sanitized metric movement (run-0001 → run-0002, same regime-v001, n=12)

| metric | run-0001 | run-0002 |
|---|---|---|
| win_rate | 0.5 | 0.8333 |
| avg_turns | 13.42 | 7.67 |
| illegal_action_rate | 0.0 | 0.0 |
| timeout_rate | 0.0 | 0.0 |
| error_rate | 0.0 | 0.0 |

> **This is not a strength claim, not a statistical-significance claim, not a cross-regime claim,
> and not evidence of leaderboard quality. It is the first same-regime local comparison artifact.**
> The movement reflects a deterministic lowest-index policy played against the same random opponent
> under the same frozen regime; interpretation is bounded by the Rung-1 ledger claim ceiling. The
> forbidden agent claim words (*strong, competitive, optimal, calibrated, complete*) remain forbidden.

## Sprint 01 entry-gate outcomes

- **O1 — provenance.** Satisfied by the **source-hash path** before sealing `run-0002`: `hashes.txt`
  and `manifest.json` record stable SHA-256 of the runtime agent source(s) + eval config; all
  recompute to MATCH the sealed values; `git_dirty=true` recorded honestly. Strong enough for a
  same-regime, agent-only delta despite no commit having been made at seal time.
- **O2 — ledger footgun.** Controlled by `--no-ledger` / `write_ledger=False` for non-deliverable
  (review / test / mirror / temp / cross-regime) runs, used throughout; `docs/ledger.md` carries
  exactly the two deliverable rows. The residual CLI default-to-tracked-ledger for deliverable runs
  remains **future hardening** (CF-01).
- **O3 — decision_index.** SDD §3.3 wording **reconciled docs-only** (one clarifying bullet): a
  global per-match monotonic index over all trace rows, distinct from `total_decisions` (agent rows).
  No behavior change; code and schema were already consistent.

## Carry-forwards

- **CF-01:** consider hardening `run_eval` so non-deliverable runs cannot write `docs/ledger.md` by
  default (e.g., require an explicit `--ledger`/`--no-ledger` choice).
- **CF-02:** `byte_identical()` (the determinism path in `analysis/replay_check.py`) remains
  unreachable/untested while `seed_controlled=false`; add a seeded test only if seed control becomes
  real (a future seed-controlled regime).
- **CF-03:** `analysis/delta_report.py` `None → number` metric rendering ("MOVED / n/a", no why-line)
  can be hardened later; not reachable for the current numeric runs.
- **CF-04:** `.beads/.br_history/` is untracked and not gitignored; consider separate housekeeping
  (add to `.beads/.gitignore`), not part of Sprint 01.

## Binding posture carried forward

- Data first, optimization second — the deferred-lane gate decision remains the operator's (PRD §11.4);
  this closeout opens no gate.
- The ledger is the only ceiling-bearing artifact; never compare across regimes (NFR-5).
- Competition Data never enters git (CC-1); generated run trees stay local/ignored by default (ESP-1).
- Forbidden agent claim words remain forbidden: *strong, competitive, optimal, calibrated, complete.*
