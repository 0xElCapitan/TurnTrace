# Sprint 00 Closeout — Cycle-001 / "The Smallest Useful Loop"

| Field | Value |
|---|---|
| **Sprint** | Cycle-001 / Sprint 00 — The Smallest Useful Loop |
| **Status** | **CLOSED / ACCEPTED / INTEGRATED** |
| **Final commit** | `ffe16a880f89d41fb3dfba72d7de4f8871a31830` (`ffe16a8`) |
| **main** | `main = origin/main = ffe16a8` |
| **Base commit** | `2cf1f4f` — *docs: record TurnTrace loop contract* |
| **Branch** | `cycle-001-sprint-00-smallest-useful-loop` |
| **Integration method** | **fast-forward only** (no merge commit, no squash, no tag, no version bump) |
| **Date** | 2026-06-18 |

> Docs-only closeout note, written after the accepted fast-forward integration. Records
> sanitized evidence and Sprint 01 carry-forwards. No raw traces, card IDs/names, deck lists,
> simulator logs, or Competition Data appear here (CC-1/CC-2, ESP).

## The loop (governing contract: `docs/operator/turntrace-loop-contract.md`)

```
/implement sprint-00   → ACCEPTED  (10/10 tasks; probe-first; 9/9 acceptance checks)
/review-sprint sprint-00 → ACCEPT  (independent re-verification; 9/9; no patches)
/audit-sprint sprint-00  → ACCEPT  (final safety gate; 9/9 HIGH confidence)
operator acceptance      → committed + fast-forwarded to main; sprint branch pushed
```

Review/audit feedback never became ad-hoc patches; all corrective authority stayed with
`/implement` (none was needed). The sprint closed only after implementation + review + audit +
operator acceptance all held (contract §3).

## Sanitized evidence

| Field | Value |
|---|---|
| `run_id` | `run-0001` |
| status | **local / git-ignored, not committed** (ESP-1; only this sanitized note + the ledger row are tracked) |
| `n` | 12 |
| `regime_id` | `regime-v001` |
| claim ceiling | **Rung 1** — legality / throughput / audit-trail only; **no gameplay-strength claim** |
| `seed_controlled` | `false` |
| `mode` | unseeded / distribution-stable + audit-trail (NFR-3) |
| `timeout_detectable` | `false` (soft gate; `budget_source=assumed`) |

The experiment ledger (`docs/ledger.md`) holds the single ceiling-bearing `run-0001` row.
`win_rate` is recorded there for the run but is **explicitly not a quality signal** (the
opponent is a `random_legal` mirror; ladder Rung 1). The full `runs/run-0001/` tree (records,
traces, manifest, hashes) remains a local, git-ignored evidence artifact — referenced by
`run_id` and content hashes only, never embedded.

## What Sprint 00 delivered (sanitized scope)

- Probe-first simulator capability discovery (`sim/probe.py` → `sim/README.md`,
  `sim/capabilities.json`).
- Single-blast-radius `sim/` adapter; `random_legal` runtime agent (pure, no scoring);
  one-match and N-match runners; canonical trace hashing; stdlib schema validator;
  aggregation + one ceiling-bounded ledger row; Competition-Data hygiene check.
- Frozen `regime-v001` bundle stored as **references + hashes only** (no card lists).
- Sanitized operator docs (failure-modes, claim-ceiling, strategy-report skeleton).
- Runtime/offline import-direction enforced; 17 smoke checks; determinism smoke explicitly
  skipped (unseeded).

## Sprint 01 entry carry-forwards

These were accepted as **non-blocking for Sprint 00** at review and audit, and are recorded
here as explicit Sprint 01 entry concerns:

- **O1 — Agent provenance must be pinned before sealing `run-0002`.** Sprint 00 accepted
  `git_dirty=true` / static `agent_version` because **no comparison claim was made** (Rung 1).
  Sprint 01's delta report (`run-0001` vs `run-0002` under the same `regime-v001`) makes a
  same-regime, agent-only comparison, so its provenance **requires committed source or source
  hashing** before the comparison run is sealed. *Promote to a Sprint 01 entry criterion.*
- **O2 — `run_eval` default-ledger behavior can mutate `docs/ledger.md`** during
  non-deliverable (review/test) runs. The review avoided contamination by redirecting to a
  throwaway ledger, but this is a footgun. **Harden or require explicit review/test ledger
  handling** before Sprint 01 comparison work.
- **O3 — `decision_index` global-vs-SDD wording divergence.** The implementation uses a global
  monotonic `decision_index`; SDD §4.2 phrases it per-agent. It is internally consistent and
  validator-enforced (`total_decisions == agent decision rows`), so it is **not a code change**
  — it needs a **one-line documentation reconciliation** in the SDD.

## Binding posture carried into Sprint 01

- Data first, optimization second — **no rule/heuristic tuning until the first delta report
  exists** (PRD §11.3).
- The ledger is the only ceiling-bearing artifact; never compare across regimes (NFR-5).
- Competition Data never enters git (CC-1); generated run trees stay local/ignored by default
  (ESP-1).
- Forbidden agent claim words remain forbidden: *strong, competitive, optimal, calibrated,
  complete.*
