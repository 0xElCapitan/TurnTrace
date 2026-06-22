# Cycle-009 PRD — Mechanical Governance Floor: Make the Existing Evidence Discipline Run as One Gate

> Planning artifact (PRD). Status: **ACCEPTED by operator.** This PRD specifies a **floor-hardening / mechanical-governance** cycle: it makes TurnTrace's already-written, already-tested governance controls **mechanically runnable as one read-only gate**, and (conditionally, behind a feasibility spike) mechanizes the explicitly-deferred S04.4 "freezes-nothing" lint. The PRD itself **opens no implementation gate and authorizes no irreversible act**: code lands only through `/architect → /sprint-plan → /implement → /review-sprint → /audit-sprint → operator acceptance` (`docs/operator/turntrace-loop-contract.md` §1, §6; an OD-C8-6-class build gate). **This drafting pass builds no code, generates no fresh evidence, runs no eval, chooses no candidate, pre-registers no Rung-3 attempt, chooses no numeric margin `M`, issues no SP-6, promotes no value, writes no ledger row, and advances no claim ceiling.** It defines *what Cycle-009 must hold*; it does not design the SDD or sprint plan.
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, hand contents, simulator logs, run-dir dumps, Pokémon Elements, Daily-Top-Episode data, Kaggle episode data, Discord/peer screenshots, `deck.csv` rows, `cg/` SDK, PDFs/CSVs, or Competition Data appear here. **No numeric margin `M` is chosen or stated.** The forbidden agent words (*strong / competitive / optimal / calibrated / complete*) and the inferential terms (*std-dev / variance / CI / p-value / significance / hypothesis-test / error-bar*) appear only as the negated/forbidden language they are. Any freezes-nothing-lint fixtures this cycle would produce use **synthetic tokens only** — never a real candidate, `M`, `K`/`n`, regime id, feature family, or threshold.
>
> **Cycle-009 posture (binding).** Cycle-009 does **not**: attempt Rung 3; select a Rung-3 target; select a candidate; freeze a numeric comparison budget; freeze `K`/`n`; freeze a regime id; freeze a feature family; freeze a threshold; create SP-6; write or modify a ledger row; or advance the claim ceiling. **The standing claim ceiling remains Rung 2 — "beats random-legal"** (`docs/claim-ceiling.md:10`), and `docs/ledger.md` remains the **only** ceiling-bearing artifact. The governance gate and the (conditional) freezes-nothing lint each carry **no ceiling of their own**; a green gate is **well-formedness, not authorization**.

## 0. State verified (2026-06-21, before drafting)

| Assumption to verify | Result |
|---|---|
| Current HEAD / branch | `main` @ `20aa6e2a9d6daad8f099448b4aba1f5c0ef07f6c` ("docs: close TurnTrace Cycle-008") |
| Local branch in sync with `origin/main` | both at `20aa6e2a9d6daad8f099448b4aba1f5c0ef07f6c` — not ahead, not behind |
| Cycle-008 status | **Closed** (tooling + governance landed; no terminal act; `docs/cycles/cycle-008/09-s05-closeout.md`); Rung 2 held |
| `docs/ledger.md` byte-unchanged | **byte-unchanged**; `git hash-object = 7da7e9a8dbed6561669d1569445eb9fe67a953fb` |
| `docs/claim-ceiling.md` unchanged | **unchanged**; ceiling = **Rung 2** (`git hash-object = 3d99759b919f7d75bc41ea81cd82e5f1fb974be7`) |
| `.claude/` untouched | **no drift**; `integrity_enforcement: strict` → no HALT |
| No staged files | **none staged** |
| `.beads/issues.jsonl`, `grimoires/loa/NOTES.md`, `grimoires/loa/README.draft.md` dirty | all modified/untracked, **unstaged** (pre-existing State-Zone housekeeping); **must not be staged or cleaned** by this cycle unless explicitly authorized as a separate operator decision |
| Binding research input present | `grimoires/loa/a2a/cycle-009/00-pre-prd-research.md` (gitignored State-Zone; recommends floor-hardening / mechanical-governance; accepted by operator) |

**All assumptions hold. No finding forces a stop.** PRD acceptance and the build gate are **separate operator acts** this PRD does not self-authorize.

| Field | Value |
|---|---|
| **Cycle** | Cycle-009 |
| **Working title** | Mechanical Governance Floor: Make the Existing Evidence Discipline Run as One Gate |
| **Type** | Product Requirements Document (planning artifact for a floor-hardening / mechanical-governance cycle) |
| **Status** | ACCEPTED by operator; next Golden-Path step is SDD / architecture |
| **Date** | 2026-06-21 |
| **Current main** | `20aa6e2` — "docs: close TurnTrace Cycle-008" |
| **Binding research input** | `grimoires/loa/a2a/cycle-009/00-pre-prd-research.md` (gitignored State-Zone research; recommends **C9-MG-1 governance-gate runner + the deferred S04.4 freezes-nothing lint, lint behind a feasibility spike**; accepted by operator) |
| **Posture** | **Floor-hardening. Make existing controls run; freeze nothing; advance nothing.** Rung 2 holds at open and is **preserved**; no ceiling movement this cycle. |
| **Claim ceiling (at open)** | **Rung 2 — "beats random-legal"** (narrowly bounded to `scripted-v001` over `random_legal-v001` under `regime-v003`) |

## Required posture (binding)

- **Cycle-009 is a floor-hardening / mechanical-governance cycle.** It is **not** a Rung-3 attempt, **not** a target-selection cycle, and **not** agent-building. It makes the *existing* discipline mechanical; it makes no new claim.
- **A green gate is well-formedness only, never authorization.** Mirroring the S03 validator posture (`08b-ledger-metric-column-convention.md` §6–§7): the gate reports whether the governance *mechanics* are valid; it blesses no rung, authorizes no act, and a green result is **not** permission to write a ledger row or advance a ceiling. Those remain separate, explicitly operator-gated terminal acts (the OD-C7-10 precedent).
- **The ledger remains the evidence-admission authority.** `docs/ledger.md` stays the **only** ceiling-bearing artifact; the gate and the conditional lint assert no ceiling of their own (`docs/claim-ceiling.md`; `docs/ledger.md` header).
- **Read-only by construction.** The gate and the lint **write nothing**: no `--fix`, no file writes, no `mkdir`, no run-dir creation, no ledger/claim-ceiling mutation, and no git `add`/`commit`/`push`/`reset`/`checkout`. Their only side effects are read-only reads (file reads; read-only `git show` / `git hash-object` where already used).
- **Rung 2 holds at cycle open and is preserved.** No ledger row is written; no claim-ceiling advance occurs; the standing claim stays narrowly bounded to `scripted-v001` beating `random_legal-v001` under `regime-v003` (`docs/claim-ceiling.md`).
- **Freeze nothing.** This cycle freezes no candidate, no numeric `M`, no `K`/`n`, no regime id, no feature family, and no threshold. The freezes-nothing lint, if it ships, *detects* freezes; it introduces none, and its fixtures are synthetic-token only.
- **`.claude/` (System Zone) is never edited; no State-Zone cleanup is performed.** Pre-existing dirty State-Zone files (`.beads/issues.jsonl`, `grimoires/loa/NOTES.md`, `grimoires/loa/README.draft.md`) stay unstaged and untouched unless a separate operator decision authorizes reconciliation. (Note: `.github/` is App/CI Zone, **not** System Zone, and is in scope for the CI invocation.)

**The bright line for the whole cycle:** *Cycle-008 wrote the controls and the conventions; nothing automatically runs them. Cycle-009 makes them run — one read-only gate over the validators and tests that already exist, and a conditional lint that mechanizes the one convention (08d "freezes-nothing") that Cycle-008 left as prose. It makes future work harder to accidentally corrupt. It makes no new strength claim, touches no runtime agent, and advances no ceiling.*

## 1. Product / cycle overview & problem statement

TurnTrace is a local, sanitized data-loop / evaluation harness for a simulator-based trading-card-game agent (`README.md`). Across eight cycles it built a strict evidence-and-claim-ceiling discipline. Cycle-007 earned the standing **Rung 2 — "beats random-legal."** Cycle-008 built **instruments and conventions** — a content-reading trace diagnostic + co-located fail-closed sanitizer (`analysis/trace_diagnostic.py`), a read-only ledger-row validator (`analysis/ledger_validate.py`), and four governance docs (`08a`–`08d`) — and took **no terminal act** (`docs/cycles/cycle-008/09-s05-closeout.md`).

**The problem (the prose-vs-mechanical gap).** The repo's strongest governance guarantees exist as scripts and tests, but **nothing automatically runs them as one gate**, and the new conventions are prose with no enforcing test or hook. Grounded in the accepted research (`grimoires/loa/a2a/cycle-009/00-pre-prd-research.md` §1, §4 CF-A/CF-B) and re-verified this pass:

1. **No runner invokes the controls.** `.github/workflows/` contains **only `post-merge.yml`**, which runs classify/semver/changelog/release and invokes **no** validator or test. There is **no** `pytest.ini` / `Makefile` / `conftest.py` / `tox.ini` / `setup.cfg` / `pyproject.toml`. The mechanical controls — append-only + Rung-2 anchoring (`analysis/ledger_validate.py`), the fail-closed diagnostic sanitizer (`analysis/trace_diagnostic.py::validate_diagnostic`), forbidden-word leak detection (`analysis/evidence_summary.py`), cross-regime exit-2 refusal, and the import-direction lint — run **only when an agent remembers to type the command** (`00-pre-prd-research.md` §1; verified live).
2. **The S04.4 "freezes-nothing" lint was deferred.** Cycle-008's own conventions are asserted in prose; the mechanical lint that would prove `08d` (and any future Rung-3 form doc) freezes nothing was explicitly deferred and is non-blocking (`docs/cycles/cycle-008/09-s05-closeout.md` §8.7, §8.9).

Neither gap is solved by building an agent or attempting a rung. Each is a **mechanization** gap: tested, read-only code that nothing yet runs as a gate. Cycle-009 closes the gap by wiring the existing controls into one mechanical check and (conditionally) mechanizing the deferred lint — and stops.

## 2. Product goal (mission)

**Make TurnTrace's existing evidence discipline mechanically runnable — as one read-only gate — before any future claim-bearing or optimization cycle.** Convert the project's strongest governance guarantees from "exists but optional" to "runs on every change," so that an outside reviewer asking "what stops a malformed ledger append, a cross-regime row, a forbidden-word leak, or an accidental ceiling edit?" gets a mechanical answer rather than "agent discipline." Build the floor; advance no claim.

**Who consumes this PRD.** The **operator** (accepts this PRD; opens the build gate; decides the CI mechanics and the lint-vs-defer question); the **architect / sprint-planner** (`/architect`, `/sprint-plan`, who resolve the SDD-level and sprint-level design this PRD defers — including the exact child-check list and the gate's placement); the **implementer** (`/implement`, who lands the gate, the conditional lint, the tests, and the CI invocation); and the **reviewer/auditor** (`/review-sprint`, `/audit-sprint`).

## 3. Scope

**In scope (Cycle-009), behind the loop + the build gate.**
- Tracked planning/governance artifacts under `docs/cycles/cycle-009/` (this PRD; the SDD; the sprint plan) — promoted from this State-Zone draft by the operator via the normal `docs:` path.
- A **single read-only governance-gate entrypoint** (likely under `analysis/`; exact placement an SDD decision) that runs the existing validators and stdlib test modules, aggregates their exits, and reports pass/fail — landing through `/implement → /review-sprint → /audit-sprint`.
- **Tests** for the gate (stdlib `unittest` / plain-assert, parity with the existing suite), including a forced-failure test and a writes-nothing / hashes-byte-unchanged test.
- A **CI and/or documented pre-commit invocation** of the gate (`.github/workflows/` is App/CI Zone, in scope), with advisory-vs-required mechanics surfaced as an operator decision.
- A **feasibility spike** for the S04.4 freezes-nothing lint (read-only investigation of the negation-clause discriminator), and — **only if the spike succeeds** — the lint itself plus its synthetic-token fixtures.

**Out of scope (Cycle-009).** See §6 Non-goals. In summary: any Rung-3 attempt/target/candidate/`M`/`K`/`n`/regime/feature-family/threshold freeze; any SP-6, ledger row, or ceiling advance; any fresh eval/evidence/run-dir; any runtime-agent / heuristic / FunSearch / RL / self-play / MCTS / value-model / deck-optimizer / tournament / dashboard / Kaggle-submission work; any pre-registration template or commit-order verifier build; any strategy-report evidence filling; any `.claude/` edit; any State-Zone cleanup unless separately authorized.

## 4. Functional requirements

The FRs state **what** Cycle-009 must hold; **how** (module shape, exact child list, placement, internal design, task breakdown) is deferred to the SDD and sprint plan (§9).

### C9-FR-1 — Single read-only governance-gate entrypoint
1. Cycle-009 MUST add **one** tracked governance-gate entrypoint (a single command an agent or CI job invokes) that runs the project's existing governance checks and **reports one pass/fail** outcome. Its likely home is `analysis/` (research §6); exact placement and name are an SDD decision.
2. The gate MUST be **stdlib-only** (no third-party runtime dependency), consistent with the whole App Zone (`README.md`; NFR-1).
3. The gate MUST be **read-only**: no `--fix` mode, no file writes, no `mkdir`, no run-dir creation, no mutation of `docs/ledger.md` / `docs/claim-ceiling.md` / any tracked `docs/` path / any run dir, and no git mutation (`add`/`commit`/`push`/`reset`/`checkout`). Permitted side effects are read-only reads only (file reads; the read-only `git show` / `git hash-object` already used by `analysis/ledger_validate.py`).
4. The gate MUST **aggregate child exits** into a single result and **name the failing check(s)** in its output. It MUST preserve the project's exit-code discipline — the existing `analysis/` validator family uses the `0/1/2/3` contract (`0` valid · `1` input/prerequisite failure, fail-closed · `2` structural refusal · `3` governance/leak refusal; `analysis/ledger_validate.py`, `analysis/trace_diagnostic.py`). The aggregate exit MUST be non-zero iff any included child is non-zero; the SDD decides whether the aggregate surfaces the max child severity or a dedicated aggregate code.
5. The gate MUST **fail closed** when a **required prerequisite for an included check is unreachable** (never a silent pass) — e.g. an unreachable committed ledger baseline yields `analysis/ledger_validate.py` exit `1` (fail-closed; `analysis/ledger_validate.py` append-only check), and the gate MUST propagate that as a failure, not swallow it.

### C9-FR-2 — Included checks (the child set)
1. The gate MUST include or support the project's existing read-only governance checks, drawn from: the **ledger-row + claim-ceiling validator** (`analysis/ledger_validate.py`), the **trace-diagnostic sanitizer** (`analysis/trace_diagnostic.py --validate`), and the **evidence-summary validator** (`analysis/evidence_summary.py`, where applicable), plus the current stdlib **test modules** — `tests/test_import_direction.py`, `tests/test_ledger_validate.py`, `tests/test_trace_diagnostic.py`, `tests/test_evidence_summary.py`, and `tests/test_smokes.py`.
2. The gate's child set MUST be **partitioned by prerequisite**, because the checks are **not** all simulator-free:
   - **CI-runnable subset (stdlib-only, simulator-free):** the validators above plus `tests/test_import_direction.py`, `tests/test_ledger_validate.py`, `tests/test_trace_diagnostic.py`, `tests/test_evidence_summary.py`. These run anywhere with no Competition Data present.
   - **Simulator-dependent subset (local-only):** `tests/test_smokes.py` **requires `cabt` + `TURNTRACE_DECK_FILE`** (`README.md` Tests section). `cabt` and the deck file are **Competition Data — local/gitignored, never in CI** (`docs/cycles/cycle-008/01-prd.md` §13; `grimoires/loa/NOTES.md` Competition-facing constraints). The gate MUST NOT require this subset in a CI context where the simulator is absent; it MAY include it in a local invocation.
   The **exact** final child list is an open operator decision (OD-C9-4); this FR fixes the partition principle, not the membership.
3. Each included child MUST be invoked in a way that **preserves the import-direction invariant** (`tests/test_import_direction.py`): if the gate lives in `analysis/`, it MUST NOT cause `analysis/` to import `sim` / `cabt` / `eval` / `agents.runtime` — child validators/tests are invoked as subprocesses or via intra-`analysis/` imports only. (Mechanism is an SDD decision; the invariant is binding.)

### C9-FR-3 — CI / pre-commit invocation
1. Cycle-009 MUST plan a **CI job and/or a documented pre-commit invocation** of the gate (`.github/workflows/` is App/CI Zone, in scope), so the controls run on change rather than on memory.
2. The PRD MUST distinguish **advisory vs required** check mechanics and surface the choice as an open operator decision (OD-C9-1); the SDD/sprint plan implements the chosen mechanic. A required check changes merge mechanics; an advisory check reports without blocking. The default recommendation (non-binding) is to **start advisory or path-scoped** and promote to required after it proves stable.
3. If CI is used, the PRD MUST account for **committed-baseline reachability**: `analysis/ledger_validate.py` reads the append-only baseline via `git show HEAD:docs/ledger.md`, which is **unreachable on a shallow/partial checkout** and would fail closed (exit `1`) on otherwise-legitimate runs. A CI invocation that includes the ledger validator MUST use a **full-history checkout** (e.g. `fetch-depth: 0`) — surfaced as an operator decision (OD-C9-2).
4. Any git subprocess the gate introduces or relies on MUST preserve **`encoding='utf-8'`** on its reads. Windows defaults to a legacy code page (cp1252) that mangles the ledger's UTF-8 em-dashes and breaks the byte-exact prefix comparison; the existing pin in `analysis/ledger_validate.py` (`git show` / `git hash-object` calls) MUST NOT be regressed, and any new git read MUST match it (`docs/cycles/cycle-008/09-s05-closeout.md` §8.6; `00-pre-prd-research.md` CF-D).

### C9-FR-4 — Freezes-nothing lint (conditional; behind a feasibility spike)
1. Cycle-009 MUST begin the freezes-nothing-lint track with a **feasibility spike** — a bounded, read-only investigation that tests whether a lint can **distinguish an actual parameter freeze from a negation clause that enumerates things explicitly NOT frozen.** `08c`/`08d` are saturated with freezes-nothing negation clauses that literally enumerate `M` / `K` / `n` / regime id / feature family / threshold as the things *not* frozen; a naive matcher would flag the very sentences asserting nothing is frozen (`docs/cycles/cycle-008/08d-rung3-form-only-semantics.md` §4; `00-pre-prd-research.md` §6 C9-MG-3, open question 1). The spike's outcome MUST be recorded.
2. The spike MUST also check whether `eval/hygiene_check.py` (or any existing validator) **already** asserts part of the freezes-nothing surface over `08d`, so the new lint targets only the delta and avoids redundancy (`00-pre-prd-research.md` open question 2).
3. **Decision gate (operator-visible):** if the discriminator is feasible — it rejects each synthetic frozen-shape poisoned fixture **and** produces zero false positives on the existing `08c`/`08d` freezes-nothing (negation-clause) text used as clean fixtures — Cycle-009 SHOULD build the lint. If the discriminator is **brittle**, Cycle-009 MUST be allowed to **ship the governance-gate runner alone and defer the lint** to a future cycle, with the runner as the **terminal deliverable** (§5 AC; OD-C9-3).
4. If built, the lint MUST be **read-only, stdlib-only**, and scoped **v1 to the Cycle-008 form-only Rung-3 semantics doc (`docs/cycles/cycle-008/08d-rung3-form-only-semantics.md`)** unless the PRD/spike justifies a wider target (e.g. `08c`); broadening to *future* docs is an open decision (OD-C9-5).
5. If built, the lint MUST **reject** a document that freezes a concrete **candidate identity / numeric `M` / `K`/`n` value / regime id / feature family / threshold**, and MUST **accept** the existing form-only `08d` (which freezes none of these).
6. The lint's fixtures MUST use **synthetic tokens only**. **No real candidate, real `M`, real `K`/`n`, real regime freeze, real feature-family selection, or real threshold may enter any tracked fixture** (NFR-7; required posture). A green freezes-nothing lint means only **"froze no parameter,"** never **"Rung 3 authorized."**
7. If the lint reuses any regex/marker family from `analysis/trace_diagnostic.py` (the existing `M`/governance patterns), it MUST do so under a **pinned parity test** so the copy cannot silently drift (`00-pre-prd-research.md` CF-H; C9-FR-4 risk).

### C9-FR-5 — Invariants held (hard)
1. Throughout Cycle-009, `docs/ledger.md` MUST stay byte-unchanged (`7da7e9a8dbed6561669d1569445eb9fe67a953fb`), `docs/claim-ceiling.md` MUST stay unchanged (`3d99759b919f7d75bc41ea81cd82e5f1fb974be7`; still **Rung 2**), **no** value is promoted, **no** SP-6 is issued, **no** ledger row is written, and **no** ceiling advance occurs.
2. The ledger remains the **only ceiling-bearing artifact**; the governance gate and the conditional lint carry **no ceiling of their own**, and a green result is **well-formedness, not authorization** (`08b-ledger-metric-column-convention.md` §6–§7).

## 5. Acceptance criteria

### 5.1 Planning-cycle success (this PRD)
- Accepted by the operator (floor-hardening / mechanical-governance direction) and proceeds to `/architect` (SDD), not directly to implementation.
- Grounded in the pre-PRD research (`00-pre-prd-research.md`) and the tracked Cycle-008 authorities; clearly a **floor-hardening** cycle, not a Rung-3 attempt and not agent-building.
- **Rung 2 held;** `docs/ledger.md` byte-unchanged (`7da7e9a8…`); `docs/claim-ceiling.md` unchanged (`3d99759b…`; Rung 2); `.claude/` untouched; State-Zone dirt unstaged and uncleaned.

### 5.2 Deliverable success (concrete, testable — when the cycle runs in later sprints)
- **Governance gate (C9-FR-1/2/3):**
  - Runs the included validators + stdlib test modules and reports a single pass/fail; **writes nothing**; **stdlib-only**.
  - **Has a test proving it returns non-zero when a child check fails** (e.g. a self-test that injects a failing child).
  - **Has a test (or closeout check) proving it writes nothing and leaves `docs/ledger.md` and `docs/claim-ceiling.md` byte-unchanged** (`git hash-object` identical before and after a run).
  - **Fails closed** when a required prerequisite for an included check is unreachable (e.g. unreachable ledger baseline → non-zero, never silent `0`).
  - Preserves `encoding='utf-8'` on any git subprocess; does not require `cabt`/Competition Data in the CI-runnable subset; a CI invocation including the ledger validator uses full-history checkout.
- **Freezes-nothing lint (C9-FR-4), if it ships:**
  - **Has poisoned synthetic fixtures** for the frozen-shape classes (candidate / `M` / `K`/`n` / regime id / feature family / threshold) that the lint **rejects**, and **clean fixtures** for valid negation-clause patterns (the existing `08d` freezes-nothing text) that the lint **accepts**.
  - Fixtures contain **no real** candidate / `M` / `K`/`n` / regime / feature-family / threshold.
  - Green output is documented as **"froze no parameter," not "Rung 3 authorized."**
- **If the freezes-nothing-lint feasibility spike fails:** PRD acceptance **explicitly allows deferral** of the lint to a future cycle while still accepting the **governance-gate runner as the terminal deliverable** (the cycle is complete and successful with the runner alone).

### 5.3 Hard invariants (whole cycle)
`docs/ledger.md` byte-unchanged at `7da7e9a8…`; `docs/claim-ceiling.md` unchanged (Rung 2); the ledger remains the only ceiling-bearing artifact; the gate/lint carry no ceiling of their own; **no** value promoted; **no** SP-6; **no** ledger row; **no** ceiling advance; **no** fresh eval / fresh evidence / run-dir creation; **no** runtime-agent / heuristic / FunSearch / RL / self-play / MCTS / value-model / deck-optimizer / tournament / dashboard / Kaggle-submission work; stdlib-only; `analysis/`-offline imports preserved; **no** numeric `M` in any tracked artifact; `.claude/` untouched; protected State-Zone dirt unstaged and uncleaned (unless separately authorized).

## 6. Non-goals (explicit)

Cycle-009 does **not**:

- **Attempt Rung 3**, choose a **Rung-3 target**, select a **candidate**, or freeze a **numeric comparison budget** / **`K`/`n`** / **regime id** / **feature family** / **threshold**.
- Create an **SP-6**, write or modify a **ledger row**, advance the **claim ceiling**, or introduce a numeric margin **`M`** into any tracked artifact.
- Run a **fresh eval**, generate **fresh evidence**, or create any **run dir**.
- Build a **pre-registration template** or a **commit-order ("M-before-bands") verifier** (both are separately-scoped future candidates per `00-pre-prd-research.md` §6 #10–#11).
- Fill the **strategy-report** with evidence-dependent content (`00-pre-prd-research.md` §10, blocked #19), or build any **per-decision quality detector** (FM-03/04/06/08 remain `detector: forbidden`).
- Do any **runtime-agent / heuristic / FunSearch / RL / self-play / MCTS / value-model / deck-optimizer / tournament / dashboard / Kaggle-submission** work (`docs/cycles/cycle-008/08c-blocked-family-map.md` §3; all lanes in `docs/operator/deferred-lane-gate-after-sprint-01.md` remain closed).
- Add any **simulator instrumentation** or per-Pokémon/card semantics.
- Edit **`.claude/`** (System Zone), or perform any **State-Zone cleanup** (`.beads/issues.jsonl`, `grimoires/loa/NOTES.md`, `grimoires/loa/README.draft.md` stay unstaged/untouched) **unless explicitly authorized as a separate operator decision** (OD-C9-6).

## 7. Risks and mitigations

| ID | Risk | Mitigation |
|---|---|---|
| **R1** | **Gate drifts into a writer / authorizer** (a "fix" mode or an auto-append creeps in) | C9-FR-1.3 / required posture: read-only by construction; no `--fix`; writes-nothing + hashes-byte-unchanged AC; a green gate is well-formedness, not authorization (08b §6–§7). |
| **R2** | **CI false-failure on shallow checkout** (`git show HEAD:docs/ledger.md` unreachable → exit 1) | C9-FR-3.3 / OD-C9-2: full-history checkout (`fetch-depth: 0`) for any CI invocation that includes the ledger validator. |
| **R3** | **Competition-Data leak into CI** (simulator-dependent `test_smokes` needs `cabt`) | C9-FR-2.2: partition the child set; the CI-runnable subset is stdlib-only and simulator-free; `cabt`/deck stay local/gitignored (cycle-008 PRD §13; NOTES.md). |
| **R4** | **Freezes-nothing lint false-positives on the freezes-nothing prose itself** | C9-FR-4.1/4.3: feasibility spike on the negation-clause discriminator first; build only if zero false positives on existing 08c/08d clauses; else defer (OD-C9-3). |
| **R5** | **Real frozen parameter leaks into a tracked lint fixture** | C9-FR-4.6 / NFR-7: synthetic tokens only; no real candidate/`M`/`K`/`n`/regime/feature-family/threshold in any tracked fixture. |
| **R6** | **Parity-copy drift** if the lint reuses sanitizer regexes | C9-FR-4.7: pinned parity test binds any reused regex/marker family to its source of truth. |
| **R7** | **Encoding regression** (Windows cp1252 mangles ledger em-dashes) | C9-FR-3.4: `encoding='utf-8'` preserved on all git subprocess reads. |
| **R8** | **Scope creep toward Rung 3** (a template / criteria / incumbent slips in) | §6 non-goals: no template, no commit-order build, no candidate/incumbent/`M`/`K`/`n`/regime/feature-family/threshold; the lint detects freezes, it introduces none. |
| **R9** | **Ledger / claim-ceiling drift** | C9-FR-5 / 5.3: hashes pinned (`7da7e9a8…` / `3d99759b…`); gate writes nothing; no row; no ceiling move. |
| **R10** | **Required CI check blocks legitimate merges before it is proven stable** | C9-FR-3.2 / OD-C9-1: advisory-vs-required surfaced; default recommendation is advisory/path-scoped first, promote later. |
| **R11** | **`.claude/` / State-Zone pollution** | Required posture / §6: System Zone untouched; protected dirt unstaged and uncleaned unless OD-C9-6 authorizes reconciliation. |
| **R12** | **Overclaim** — a green gate misread as a strength/admission signal | Required posture: green = well-formedness only; ledger remains the evidence-admission authority; ceiling bounded to the existing Rung-2 result; no forbidden agent word applied to the gate. |

## 8. Operator decisions

This PRD encodes the accepted direction; the following decisions are enumerated for the operator to take at the stated time. Several were surfaced by the pre-PRD research (`00-pre-prd-research.md` §9).

| ID | Decision | Status / When |
|---|---|---|
| **OD-C9-1 — CI invocation: advisory vs required** | Decide whether the gate's CI check is advisory (reports, does not block) or required (blocks merge), and any path-scoping. Default recommendation: start advisory/path-scoped, promote to required once stable. | Operator act, before/at SDD |
| **OD-C9-2 — CI full-history checkout** | Decide whether the CI invocation uses a full-history checkout (`fetch-depth: 0`) so `git show HEAD:docs/ledger.md` stays reachable (required if the ledger validator is in the CI subset). | Operator act, before/at SDD |
| **OD-C9-3 — Freezes-nothing lint: build vs defer** | After the feasibility spike: build the lint (if the negation-clause discriminator is feasible) or defer it (if brittle), accepting the governance-gate runner as the terminal deliverable. | Operator act, after the spike |
| **OD-C9-4 — Exact child-check list for v1** | Confirm the precise set of validators/tests the first gate includes, and how the simulator-dependent subset (`test_smokes`, needs `cabt`) is handled (local-only vs excluded from CI). | Operator act, before/at SDD |
| **OD-C9-5 — Freezes-nothing lint target breadth** | Decide whether the lint v1 stops at `08d` or also inspects `08c` and/or future Rung-3 form docs. | Operator act, before/at SDD (informed by the spike) |
| **OD-C9-6 — Protected State-Zone reconciliation** | Decide whether the stale beads issue (`turntrace-4by`), the orphaned `README.draft.md`, and the NOTES.md drift are reconciled later, **outside** this cycle (this PRD's default: out of scope; left unstaged/untouched). | Operator decision, separate from Cycle-009 |
| **OD-C9-7 — Build gate (OD-C8-6-class)** | Open the build gate for the sanctioned code work (governance gate + tests + CI invocation + conditional lint + fixtures), scoped to `analysis/` / `tests/` / `.github/`. | After SDD / sprint-plan |

## 9. Deferred to SDD / sprint plan (explicitly not decided here)

This PRD states **what** must hold; the following **how**-level questions are deferred:
- The gate's exact **module name, placement** (`analysis/` vs a dedicated location), and **child-invocation mechanism** (subprocess vs intra-`analysis/` import) — constrained by the import-direction invariant (C9-FR-2.3).
- The aggregate **exit-code shape** (max-child-severity vs a dedicated aggregate code) within the `0/1/2/3` family (C9-FR-1.4).
- The **CI workflow** structure and whether a pre-commit hook is added alongside (C9-FR-3).
- The freezes-nothing lint's **discriminator design** (the spike informs this) and fixture corpus layout (C9-FR-4).
- The sprint decomposition (e.g. a gate sprint, a CI-invocation sprint, a spike sprint, and a conditional lint sprint) — owned by `/sprint-plan`.

## 10. Success criteria (cycle)

### 10.1 Mechanical (verified at closeout, mirroring the Cycle-008 S05 pattern)
- `git hash-object docs/ledger.md` = `7da7e9a8dbed6561669d1569445eb9fe67a953fb`; `git hash-object docs/claim-ceiling.md` = `3d99759b919f7d75bc41ea81cd82e5f1fb974be7` (both byte-unchanged); `docs/claim-ceiling.md:10` still reads **Rung 2**; `.claude/` clean; protected State-Zone dirt unstaged — all asserted against actual command output.
- The governance gate exists, is read-only and stdlib-only, returns non-zero on a forced child failure (proven by test), and leaves both governance hashes byte-unchanged when run (proven by test or closeout check).
- The CI/pre-commit invocation is wired and green on HEAD (per the chosen advisory/required mechanic); the CI subset is simulator-free; the ledger-validator CI path uses full-history checkout.
- The freezes-nothing lint either ships with synthetic poisoned + clean fixtures (rejecting frozen shapes, accepting the form-only `08d`) **or** is explicitly deferred per OD-C9-3 with the runner accepted as terminal.

### 10.2 Posture (whole cycle)
A green gate is **well-formedness only, never authorization**; the ledger remains the evidence-admission authority; the claim ceiling remains bounded to the existing Rung-2 result; Cycle-009 makes future work **harder to accidentally corrupt** and makes **no new strength claim**.

## 11. Sources and traceability

> **Local decision input (gitignored State Zone, not a tracked dependency):**
> `grimoires/loa/a2a/cycle-009/00-pre-prd-research.md` (the accepted Cycle-009 pre-PRD research — recommends the governance-gate runner + the deferred S04.4 freezes-nothing lint behind a feasibility spike; CF-A/CF-B prose-vs-mechanical gap; §6 per-candidate detail for C9-MG-1 / C9-MG-3 / #5; §9 operator decisions; §11 acceptance posture).
> **Tracked governance authorities:** `docs/claim-ceiling.md:10` (standing ceiling Rung 2; forbidden words; never compare across regimes); `docs/ledger.md` (the only ceiling-bearing artifact; 18-column schema; the Rung-2 `regime-v003` row); `docs/cycles/cycle-008/09-s05-closeout.md` (Cycle-008 closeout; §8.6 UTF-8 pin; §8.7/§8.9 deferred freezes-nothing lint + conventions not mechanically enforced); `docs/cycles/cycle-008/08b-ledger-metric-column-convention.md` §6–§7 (the validator is a gate, not a writer or claim engine; green = well-formedness, not authorization); `docs/cycles/cycle-008/08c-blocked-family-map.md` §3 (blocked families); `docs/cycles/cycle-008/08d-rung3-form-only-semantics.md` (the form-only Rung-3 doc the lint targets; its freezes-nothing §4); `docs/cycles/cycle-008/01-prd.md` §13 (Competition-Data containment); `docs/operator/turntrace-loop-contract.md` (§1 loop; §6 build gate); `docs/operator/deferred-lane-gate-after-sprint-01.md` (closed broad-optimization lanes).
> **Tracked code (reality grounding, at `20aa6e2`):** `analysis/ledger_validate.py` (read-only ledger/ceiling gate; `encoding='utf-8'` git reads; hardcoded Rung-2 anchor; `0/1/2/3` exits); `analysis/trace_diagnostic.py` (`--validate` fail-closed sanitizer; `M`/governance regexes); `analysis/evidence_summary.py` (forbidden-word validator); `tests/test_import_direction.py`, `tests/test_ledger_validate.py`, `tests/test_trace_diagnostic.py`, `tests/test_evidence_summary.py`, `tests/test_smokes.py` (the five stdlib test modules; `test_smokes` needs `cabt` + `TURNTRACE_DECK_FILE` per `README.md`); `.github/workflows/post-merge.yml` (the only existing workflow; invokes no validator/test — verified).
> Current main at authoring: `20aa6e2` (== `origin/main`). Claim ceiling: **Rung 2 (unchanged).** This PRD opens no implementation gate, builds no code, generates no evidence, runs no eval, chooses no `M`, selects no candidate, opens no Rung-3 attempt, issues no SP-6, promotes no value, writes no ledger row, advances no ceiling, mutates no ledger, and edits no `.claude/`.

---

> **PRD statement (binding).** Cycle-009 is a **floor-hardening / mechanical-governance cycle.** It makes TurnTrace's existing evidence discipline **mechanically runnable as one read-only gate**: a single stdlib-only, read-only entrypoint that wires the existing validators (`analysis/ledger_validate.py`, `analysis/trace_diagnostic.py --validate`, `analysis/evidence_summary.py`) and the stdlib test modules into one pass/fail, aggregates their `0/1/2/3` exits, names the failing check, fails closed on an unreachable required prerequisite, and is invoked by CI and/or a documented pre-commit step — with the simulator-dependent subset partitioned out of CI and `encoding='utf-8'` preserved on every git read. It **conditionally** mechanizes the explicitly-deferred S04.4 **freezes-nothing lint** (v1 scoped to `08d`), but **only after a feasibility spike** proves the lint can distinguish an actual parameter freeze from the freezes-nothing negation clauses; if the discriminator is brittle, the runner ships **alone** as the terminal deliverable and the lint is deferred. The gate and the lint **write nothing**, **freeze nothing**, and **carry no ceiling** — a green gate is **well-formedness, not authorization.** **Cycle-009 attempts no Rung 3, selects no target/candidate, freezes no `M`/`K`/`n`/regime/feature-family/threshold, builds no runtime agent or optimization/search/learning surface, generates no evidence, issues no SP-6, writes no ledger row, advances no ceiling, edits no `.claude/`, and cleans no State-Zone dirt.** `docs/ledger.md` remains byte-unchanged at `7da7e9a8dbed6561669d1569445eb9fe67a953fb`; `docs/claim-ceiling.md` is unchanged at `3d99759b919f7d75bc41ea81cd82e5f1fb974be7`; the standing claim ceiling **remains Rung 2 — "beats random-legal."**
