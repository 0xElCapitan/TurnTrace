# TurnTrace — Loa-Native Loop Contract (Standing Operator Rule)

| Field | Value |
|---|---|
| **Status** | Standing operator rule (active) |
| **Scope** | TurnTrace sprint execution, every cycle from Cycle-001 / Sprint 00 onward |
| **Authority** | This document is the authoritative sprint-execution contract |
| **Last updated** | 2026-06-18 |
| **Related** | `docs/cycles/cycle-000-bootstrap/01-turntrace-prd.md`, `02-turntrace-sdd.md`, `03-turntrace-sprint-plan.md`, `04-operator-decisions.md` |

> **Docs-only standing rule.** This document records **how** sprints execute once the operator opens
> a build cycle. It does **not** open any build gate and authorizes no code.

## 1. The sprint control loop

Every sprint runs the same three-step Loa loop, in order:

```
/implement sprint-XX  →  /review-sprint sprint-XX  →  /audit-sprint sprint-XX
```

- **`/implement`** — the only authority that writes or patches sprint code/artifacts.
- **`/review-sprint`** — validates the implementation against acceptance criteria; emits review feedback.
- **`/audit-sprint`** — security/quality gate; emits the audit verdict and, on pass, the COMPLETED marker.

## 2. Feedback patches only through `/implement`

Review and audit findings are **not** fixed in place by the reviewer or auditor. Every corrective
change re-enters through **`/implement`**, which is the **single patch authority**. The loop iterates
`implement → review → audit` until both gates pass. No out-of-loop edits to sprint code.

## 3. A sprint closes only when ALL of these hold

1. Implementation complete — acceptance criteria met.
2. `/review-sprint` passed — one review artifact.
3. `/audit-sprint` passed — one audit artifact / COMPLETED marker.
4. **Operator acceptance.**

Missing any one → the sprint is **not** closed.

## 4. Sprint 00 — probe-first, mostly serial

Sprint 00 opens with the **capability probe** (Task 00.1, OD-4) and runs **mostly serially**: the
probe blocks the remaining tasks so the harness is shaped against the *observed* simulator surface,
never assumed. No parallel worktrees in Sprint 00.

## 5. Sprint 01 — limited internal worktrees, single review/audit

Sprint 01 **may** use limited internal worktrees for isolated parallel work, but it still closes
through exactly **one `/review-sprint` artifact and one `/audit-sprint` artifact**. Internal
parallelism does not multiply the gates.

## 6. Build-gate rule (preserved)

No implementation runs until the operator **explicitly opens Cycle-001 / Sprint 00**. Planning
artifacts and standing rules — including this one — never open the gate. Authorization is the operator
action **OA-2** (see `04-operator-decisions.md`).

## 7. Competition-Data & generated-run hygiene (preserved)

- **Competition Data** (the `cg/` simulator SDK, card data, starter files, `deck.csv`, raw deck lists,
  PDFs, CSVs) is local-only, **non-redistributable** (CC-1/CC-2), and **never committed**. It lives
  under the git-ignored `grimoires/loa/context/`.
- **Generated runs** — full `runs/<run_id>/` trees (raw traces, match logs, simulator outputs) stay
  local/ignored by default. Only **sanitized summaries, ledger rows, claim ceilings, failure-mode
  notes, planning docs, and operator-approved artifacts** are tracked. Reference a run by
  `run_id` / hashes / sanitized metrics / local path — **never embed raw contents** (Evidence-Storage
  Policy ESP-1…ESP-5 / SP-6).

## 8. Claim-ceiling language (preserved)

- Only **relative, local** claims, each carrying its sample size (`n`) and `regime_id`.
- The **experiment ledger is the only ceiling-bearing artifact**; per-match records and summaries
  carry no ceiling.
- **Never compare across regimes.**
- **Forbidden claim words** for the agent: *strong, competitive, optimal, calibrated, complete.*
  The loop measures and logs; humans make bounded claims from the evidence, with the sample size in view.

## 9. Loa zone discipline (preserved)

- **Never edit `.claude/`** (Loa System Zone). Use `.claude/overrides/` or `.loa.config.yaml`.
- App code lives in the **App Zone** (`agents/ sim/ eval/ analysis/ frozen/ runs/ config/`).
- **State Zone** (`grimoires/`, `.beads/`, `.run/`) is read/write working state.

## 10. Review/Audit Artifact Persistence Rule

`/review-sprint` and `/audit-sprint` are **pure-review skills**. If `Write`/`Edit` is disabled
inside those skills, that is **expected and correct, not a failure** — it mechanically enforces that
review and audit never patch implementation files. The review/audit *artifact* is the skill's output;
it is persisted by the **main loop / orchestrator after the skill returns**, not by the skill itself.

**For `/review-sprint sprint-N`:**

1. Run the pure review skill.
2. The review skill **must not** patch implementation files.
3. After the skill returns, persist the review artifact **verbatim** from the main loop/orchestrator to:
   `grimoires/loa/a2a/sprint-N/engineer-feedback.md`
4. This persistence is allowed because it writes **only the review artifact** in the git-ignored State Zone.
5. **Do not** create a `COMPLETED` marker during review.

**For `/audit-sprint sprint-N`:**

1. Run the pure audit skill.
2. The audit skill **must not** patch implementation files.
3. After the skill returns, persist the audit artifact **verbatim** from the main loop/orchestrator to:
   `grimoires/loa/a2a/sprint-N/auditor-sprint-feedback.md`
4. This persistence is allowed because it writes **only the audit artifact** in the git-ignored State Zone.
5. **Do not** create a `COMPLETED` marker during audit **unless the operator explicitly authorizes
   sprint closeout**.

This rule authorizes **only** the orchestrator's post-skill artifact persistence into git-ignored
State Zone paths (`grimoires/loa/a2a/sprint-N/`). It does **not** authorize review or audit to patch
implementation files or tracked source/docs by any path. All corrective changes still re-enter through
`/implement` (the single patch authority, §2).

---

*This contract is operational, not aspirational. If a build action conflicts with a step here, the
contract wins until the operator amends it.*
