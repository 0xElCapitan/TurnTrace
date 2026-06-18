# Cycle-001 / Sprint 02 PRD — Delta Explanation + Failure-Mode Taxonomy

> Planning artifact (PRD). Status: **DRAFT — research/planning only.** This document opens **NO build gate**.
> Implementation requires a separate, explicit operator build-gate action (OA-2 equivalent) per `docs/operator/turntrace-loop-contract.md` §6.
> Binding governance: `docs/operator/deferred-lane-gate-after-sprint-01.md` — **"NARROW PLANNING GATE OPENED. Broad optimization remains closed."**
> Binding planning input: `docs/cycles/cycle-001-sprint-02/00-research-and-planning.md` (the Sprint 02 research artifact; it too opens no build gate).

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-001 / Sprint 02 |
| **Working title** | Delta Explanation + Failure-Mode Taxonomy |
| **Type** | Product Requirements Document (planning artifact, not a build artifact) |
| **Status** | DRAFT — awaiting operator acceptance; next Golden Path step is SDD planning, not implementation |
| **Date** | 2026-06-18 |
| **Base commit** | `d6b9915` — *docs: plan TurnTrace Sprint 02* |
| **Posture** | EXPLAIN / AUDIT only — not an agent-improvement sprint |
| **Claim ceiling** | Rung 1 (unchanged; not raised) |

## Required posture (binding)

- **Sprint 02 is EXPLAIN/AUDIT work** — it improves TurnTrace's ability to explain and audit the first same-regime comparison from Sprint 01.
- **Sprint 02 is not an agent-improvement sprint** — no change to the runtime agent's playing behavior, rules, heuristics, or scoring.
- **Sprint 02 does not open broad optimization** — every "Still closed" item (`docs/operator/deferred-lane-gate-after-sprint-01.md` lines 71-87) remains closed and requires a separate explicit operator decision to open.
- **Sprint 02 does not raise the claim ceiling above Rung 1** (`docs/operator/deferred-lane-gate-after-sprint-01.md` line 43; `docs/claim-ceiling.md`).
- **Sprint 02 implementation requires a later explicit operator build gate** (OA-2 equivalent; `docs/operator/turntrace-loop-contract.md` §6, `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` §3). This PRD authorizes no code.

## 1. Background / context

Sprint 01 closed/accepted/integrated on 2026-06-18 (final commit `3492e61`, fast-forward only) and produced TurnTrace's first same-regime, agent-only comparison artifact: `run-0001` (baseline, `random_legal`) vs `run-0002` (candidate, frozen `scripted_baseline`) under `regime-v001` at n=12 (`docs/cycles/cycle-001-sprint-01/closeout.md` lines 1-48). The only changed variable was the agent-under-test; opponent, decks, seed-set, metrics-spec, and regime were held constant (closeout lines 36-48). `win_rate` and `avg_turns` moved while the correctness-gate rates (`illegal_action_rate`, `timeout_rate`, `error_rate`) stayed at the floor (closeout lines 55-70).

On that basis the operator recorded a standing decision: **"NARROW PLANNING GATE OPENED. Broad optimization remains closed."** (`docs/operator/deferred-lane-gate-after-sprint-01.md` lines 50-59). The note permits research/planning along seven narrow lanes — explainability of the first delta, failure-mode taxonomy, comparison robustness, trace-safe/Competition-Data-safe aggregate diagnostics, provenance and ledger hardening, `delta_report` hardening, and operator-decision framing for a future improvement sprint (lines 61-69) — and explicitly holds that "Sprint 02 must not directly optimize the agent unless a later operator decision explicitly opens that lane" and "should explain and harden the evidence loop before improving gameplay" (lines 89-97).

The Sprint 02 research artifact (`docs/cycles/cycle-001-sprint-02/00-research-and-planning.md`) evaluated six candidate tasks against repo evidence and recommended **PROCEED into research/planning only** (research artifact §14). This PRD turns that research into product requirements. It introduces no new evidence and reuses only sanitized artifacts.

Sprint 01 also recorded four carry-forwards that anchor most of this PRD's scope (`docs/cycles/cycle-001-sprint-01/closeout.md` lines 86-95):

- **CF-01** — harden `run_eval` so non-deliverable runs cannot write `docs/ledger.md` by default (the residual tail of the Sprint 00 "O2" ledger footgun).
- **CF-02** — `byte_identical()` in `analysis/replay_check.py` is unreachable/untested while `seed_controlled=false`; add a seeded test only if seed control becomes real.
- **CF-03** — `analysis/delta_report.py` `None → number` metric rendering ("MOVED / n/a", no why-line) can be hardened later; not reachable for the current numeric runs.
- **CF-04** — `.beads/.br_history/` housekeeping (gitignore); explicitly not Sprint 02 implementation scope but surfaced as an operator decision.

## 2. Problem statement

The first comparison exists, but TurnTrace's ability to **explain why it moved** and to **audit future comparisons safely** is thin:

1. **No coarse failure-mode taxonomy/schema exists** for outcome and loss categories. `docs/failure-modes.md` holds a prose seed catalogue (FM-01…FM-09) with a fixed entry template, but there is no sanitized, machine-aligned taxonomy v001 that maps coarse outcomes to computable-now vs deferred signatures (`docs/failure-modes.md` lines 11-101).
2. **No aggregate failure-mode report exists.** `analysis/aggregate.py` emits only `summary.csv` columns + one ledger row; there is no Competition-Data-safe rollup over `result`/`ending_cause` that could explain outcomes without exposing raw traces (research artifact §6 S02-2; `docs/cycles/cycle-001-sprint-01/closeout.md`).
3. **`delta_report` has a latent rendering defect (CF-03).** A `None→number` metric transition renders direction always 'down' with delta `n/a`, because `(None or 0) > 0` is False, and moved metrics get no "why moved" line (`analysis/delta_report.py` lines 73-78, 109, 156-160). It is unreached for the current all-numeric runs but is a correctness hazard for the explanation artifact.
4. **The ledger has a contamination footgun (CF-01 / O2).** `run_eval` writes `docs/ledger.md` by default (`write_ledger=True`, `ledger_path` defaults to `docs/ledger.md`); a non-deliverable run must remember `--no-ledger` or it mutates the only ceiling-bearing artifact (`eval/run_eval.py` lines 26-29, 93, 103, 305-322).
5. **The reproducibility dead path is honest but unmarked (CF-02).** `byte_identical()` is unreachable while `seed_controlled=false`; without a marker/regression test a future change could silently "revive" it and pretend byte replay exists (`analysis/replay_check.py` lines 98-133).
6. **The strategy report is a skeleton.** `docs/strategy-report.md` has seven of eight sections TODO (section 5 DEFERRED) and does not yet record what the first comparison permits and forbids, despite section 6 (failure-mode) being declared mandatory under the Rung-4 honesty gate (`docs/strategy-report.md` lines 42-46; section statuses at lines 14, 19, 24-25, 32-33, 40, 46, 53-54, 61).

None of these problems are about agent strength. All are about explanation and audit integrity.

## 3. Goals

- **G1 — Explain the first delta.** Make the `run-0001` → `run-0002` movement explainable from sanitized artifacts alone, bounded by the Rung-1 claim ceiling.
- **G2 — A sanitized failure-mode taxonomy.** Establish taxonomy v001 of coarse outcome/loss categories, each declaring computable-now vs deferred with its gating capability flag.
- **G3 — Competition-Data-safe aggregate diagnostics.** Provide an analysis-layer report that aggregates coarse fields from local (ignored) run summaries and emits categories/counts only — never raw trace contents.
- **G4 — Harden the comparison/provenance plumbing.** Fix the `delta_report` None→number rendering (CF-03) and close the `run_eval` ledger-contamination footgun (CF-01), preserving append-only ledger integrity.
- **G5 — Keep the audit honest.** Mark/test the `replay_check` dead path (CF-02) so byte-identical replay is never faked while `seed_controlled=false`.
- **G6 — Record what the comparison permits/forbids.** Update the strategy report to state, with traceability, what Sprint 01's first comparison permits and forbids.
- **G7 — Stay inside the gate.** Produce all of the above without touching the runtime agent, without raising the claim ceiling, and without opening any build gate.

## 4. Non-goals

- **NG1** — Improving, tuning, optimizing, or strengthening the runtime agent in any way (no rule/heuristic/scoring changes; "data first, optimization second" is binding — `docs/operator/deferred-lane-gate-after-sprint-01.md` lines 89-97).
- **NG2** — Raising the claim ceiling above Rung 1, or making any gameplay-strength / statistical-significance / cross-regime / leaderboard claim.
- **NG3** — Building any per-decision agent-quality detector or scorer (e.g. a "missed lethal" or "bad prize trade" quality scorer for FM-03/04/06/08). Carrying these as taxonomy *names* is allowed; *scoring* per-decision quality is forbidden and is a separate operator decision (research artifact §6 S02-1 guard, §7).
- **NG4** — Reading or emitting raw decision-trace rows, card IDs/names, deck lists, hand contents, or simulator logs into any tracked artifact.
- **NG5** — Creating or mutating run dirs, generating new runs, or editing any `regime-v001` / `frozen/` component (a component change is a new regime v002, never an edit — `docs/claim-ceiling.md` lines 29-35).
- **NG6** — Opening a build gate. This PRD and the SDD that follows authorize no code.

## 5. Users / operators

- **Operator (primary).** Owns gate decisions (OA-2 build gate), accepts/*rejects* planning artifacts, and is the only party that may open any "Still closed" lane. Consumes this PRD to decide whether to proceed to SDD. (`docs/operator/turntrace-loop-contract.md` §3, §6; `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md`.)
- **Implementer (`/implement`, future).** The single patch authority once a build gate is open; writes the App-Zone code (PR-2..PR-5) and docs (PR-1, PR-6) under the implement → review → audit loop (`docs/operator/turntrace-loop-contract.md` §1-§2).
- **Reviewer / Auditor (`/review-sprint`, `/audit-sprint`, future).** Pure-review gates; validate acceptance criteria and sanitization/claim-ceiling compliance; Write/Edit disabled inside them is expected, not a failure (`docs/operator/turntrace-loop-contract.md` §10).
- **Downstream evidence reader.** A human (or future-us) who must be able to understand and verify the comparison from sanitized, tracked artifacts (ledger row, taxonomy, strategy report) without access to Competition Data.

## 6. Product requirements

Each requirement cites the narrow-planning lane it serves and its source. **Core** = required for Sprint 02 to deliver its EXPLAIN/AUDIT value. **Stretch** = include only if capacity allows; droppable without failing the sprint. App-Zone code requirements (PR-2..PR-5) require an opened build gate (OA-2) before any code is written; pure-docs requirements (PR-1, PR-6) open no gate but are still produced under the planning posture.

| ID | Maps to | Title | Class | Zone | Lane served |
|---|---|---|---|---|---|
| PR-1 | S02-1 | Failure-mode taxonomy v001 (tracked, sanitized) | **Core** | docs | Failure-mode taxonomy |
| PR-2 | S02-2 | Aggregate failure-mode report (sanitized categories only) | **Core** | App (`analysis/`) | Trace-safe aggregate diagnostics |
| PR-3 | S02-3 | `delta_report` hardening (why-lines + None→number) | **Core** | App (`analysis/`) | `delta_report` hardening / comparison robustness |
| PR-4 | S02-4 | Ledger contamination hardening (CF-01) | **Core** *(assumption — see OD-2)* | App (`eval/`) | Provenance & ledger hardening |
| PR-5 | S02-5 | `replay_check` dead-path marker/test (CF-02) | **Stretch** *(assumption — see OD-1)* | App (`analysis/`) | Comparison robustness / audit honesty |
| PR-6 | S02-6 | Strategy-report update (permits/forbids) | **Core** *(assumption — see OD-3)* | docs | Operator-decision framing |

### PR-1 — Failure-mode taxonomy v001 (Core, docs)

**Requirement.** Produce a tracked, sanitized failure-mode taxonomy v001 (extending `docs/failure-modes.md` or a sibling docs file) that organizes coarse outcome and loss categories. Each category declares (a) computable-now vs deferred and (b) the gating capability flag (`seed_controlled=false`, `invalid_action_detectable=true`, `timeout_detectable=false`), reusing only sanitization-safe signals already exposed — the `result` enum and `ending_cause` enum and the four ledger rate columns — and referencing trace rows by `run_id`+`match_id`+`decision_index` only (a reference string, never row contents).

- **Rationale / source.** Explicitly permitted lane (`docs/operator/deferred-lane-gate-after-sprint-01.md` lines 61-69). Scaffold exists: entry template + status enum `open|mitigated|watched|wont-fix` and seed catalogue FM-01…FM-09 (`docs/failure-modes.md` lines 11-101); the registry rule requires a category be kept only if its Signature is computable from fields the simulator provides (lines 6-7).
- **Constraint.** FM-03 (bad prize trade), FM-04 (wasted resource), FM-06 (missed lethal), FM-08 (bad search target) are per-decision "agent played sub-optimally" categories. They are carried as **names only**; **no detector that scores per-decision quality may be built** (NG3). The taxonomy must state this boundary inline so a future build cannot read v001 as license to implement such a detector.

### PR-2 — Aggregate failure-mode report (Core, App-Zone `analysis/`)

**Requirement.** Add an analysis-layer report that reads **only already-aggregated, sanitization-safe fields** (`result`, `ending_cause`, error-flag, `invalid_action_count`, `turns`, `total_decisions`, `trace_present`) from a **local, git-ignored** run dir and emits **coarse categories only**: counts/rates per `ending_cause` and per `result`, plus FM-id linkage by reference string. It MUST NOT read or emit `decision-trace.jsonl` row contents, card IDs, deck lists, or hand contents.

- **Rationale / source.** Permitted "trace-safe and Competition-Data-safe aggregate diagnostics" lane (`docs/operator/deferred-lane-gate-after-sprint-01.md` lines 61-69). No such aggregation module exists today (`analysis/aggregate.py` emits `summary.csv` + one ledger row only).
- **Separation constraint.** `analysis/` may read run-dir artifacts (read-only) and MUST NOT import `agents/runtime/` or `cabt` directly (SDD §1.6 directory-boundary + import-direction rule); by the code's own stated rule (the docstrings of `analysis/delta_report.py` and `analysis/replay_check.py`) it imports none of `sim/` or `eval/` either.
- **Output constraint.** Carry the claim-ceiling footer pattern (bounded by `regime_id` + n, no strength claim), consistent with `analysis/delta_report.py` `render` (lines 166-170). Degrade cleanly on a run dir with no matches / missing fields (undetectable reported, never silently passed).

### PR-3 — `delta_report` hardening (Core, App-Zone `analysis/`)

**Requirement.** Harden `analysis/delta_report.py` so that (a) a `None→number` (and `number→None`) metric transition renders **honestly** — an explicit "appeared/disappeared" status with no fabricated 'down' direction — and (b) every **MOVED** metric carries a "why moved" line, symmetric with the existing `WHY_NO_CHANGE` coverage for unmoved metrics.

- **Rationale / source.** Permitted "`delta_report` hardening" / "comparison robustness" lanes; maps to CF-03 (`docs/cycles/cycle-001-sprint-01/closeout.md` lines 92-93). The defect is confirmed: `_delta` returns None when either side is non-numeric (lines 73-78), `moved` fires via `va != vb and d is None` (line 109), and direction `(None or 0) > 0` = False forces 'down' regardless of value (lines 156-160).
- **Scope constraint.** The fix is confined to the currently-unreached None↔number branch and MUST NOT alter rendering for the present numeric runs (`run-0001` vs `run-0002` output unchanged for all five numeric metrics). The five `COMPARE_METRICS` and the cross-regime hard-refusal (exit 2) are unchanged (lines 41-43, 90-96).
- **Secondary item.** The `avg_match_length` (metrics-spec) vs `avg_turns` (code) naming relationship should be documented in-code/in-report as an alias; **no `frozen/` artifact may be edited** (a frozen-component change is a new regime — `docs/claim-ceiling.md` lines 29-35).

### PR-4 — Ledger contamination hardening / CF-01 (Core *(assumption, OD-2)*, App-Zone `eval/`)

**Requirement.** Change `eval/run_eval.py` so that writing a tracked row to `docs/ledger.md` requires **explicit deliverable intent** (an explicit `--ledger` target or a `--deliverable` flag) — a default/non-deliverable invocation MUST NOT append to `docs/ledger.md`. `summary.csv` is still always written. Idempotency and the non-empty `claim_ceiling` requirement are preserved; the two existing rows (`run-0001`, `run-0002`) are not edited in place (append-only).

- **Rationale / source.** Permitted "provenance and ledger hardening" lane; the precise recorded residual CF-01 (`docs/cycles/cycle-001-sprint-01/closeout.md` lines 87-88). Code confirms opt-OUT design: `write_ledger` defaults to `True` (function signature, line 93) and `ledger_path` defaults to `docs/ledger.md` (line 103); `main()` wires `write_ledger=not args.no_ledger` at the call site (line 321), so a bare invocation appends to the tracked ledger (`eval/run_eval.py` lines 93, 103, 305-322).
- **Migration constraint.** Flipping the default to opt-in may break a caller/test that relied on deliverable-by-default; all `run_eval` callers must be audited and updated in the same change. The exit-code contract (0/1/2/3) and immutability guard are unchanged.

### PR-5 — `replay_check` dead-path marker / CF-02 (Stretch *(assumption, OD-1)*, App-Zone `analysis/`)

**Requirement.** Mark `byte_identical()` in `analysis/replay_check.py` as a dead/unreachable path with an explicit upgrade trigger (reachable only if `seed_controlled` becomes true), per the `loa:shortcut` ceiling+trigger convention, and add a test pinning that under `seed_controlled=false`, `replay_check` returns `mode='unseeded'` and `determinism.status='skipped'` (never `'passed'`). No fake seed may be injected to force the path green.

- **Rationale / source.** Maps to CF-02 (`docs/cycles/cycle-001-sprint-01/closeout.md` lines 89-91). The code is already honest (docstring states the degraded reality; gating at lines 114-133 skips the determinism branch under `seed_controlled=false`). The remaining value is regression-hardening against a future silent revival; hence **Stretch**.
- **Constraint.** The always-on audit-trail equality tier (`audit_trail_equality`, lines 69-88) is unchanged. Do not manufacture seed control (NG2 reproducibility boundary; `docs/claim-ceiling.md` lines 43-52).

### PR-6 — Strategy-report update (Core *(assumption, OD-3)*, docs)

**Requirement.** Update `docs/strategy-report.md` to reflect the first comparison with a **PERMITS / FORBIDS** framing mirroring the deferred-lane note's partition: PERMITS = a recorded same-regime agent-only metric movement bounded by the Rung-1 ledger ceiling; FORBIDS = strength/significance/cross-regime/leaderboard claims and all "Still closed" broad-optimization items. Fill the now-answerable sections (1 claim ceiling, 4 evaluation method, 6 failure-mode linkage, 7 limitations); section 5 (ablation table) remains **DEFERRED**.

- **Rationale / source.** Permitted "operator-decision framing for a future improvement sprint" lane; section 6 is declared Mandatory under the Rung-4 honesty gate (`docs/strategy-report.md` lines 42-46). The report is currently a skeleton (lines 14, 19, 24-25, 32-33, 40, 53-54, 61).
- **Constraint.** Every claim sentence must reference a specific logged artifact (ledger row / match-summary / regime hash / `delta_report` output) per the traceability rule (lines 65-68); decks referenced by `deck_id`+hash; runs by `run_id`+hashes; no raw metric values pasted as "evidence" beyond what the ledger already sanitizes; no forbidden claim words.

## 7. Acceptance criteria

Sprint-level acceptance criteria. All criteria are bounded to Rung 1 and forbid agent strengthening. (Per-requirement detail aligns with research artifact §6 and §8.)

- **AC-1 (PR-1, taxonomy honesty).** Taxonomy v001 is a tracked, sanitized docs artifact; every category declares computable-now vs deferred with its gating capability flag; categories lacking a detector are marked aspirational; FM-03/04/06/08 carry no per-decision quality detector and the artifact records inline that any such detector is a separate operator decision outside the gate; no Competition Data; no forbidden claim words.
- **AC-2 (PR-2, aggregate-only diagnostics).** The report reads only match-summary aggregate fields from local ignored run dirs and emits coarse counts per `result`/`ending_cause` only; it does not import `agents/runtime/` or `cabt`, and by the code's stated rule imports none of `sim`/`eval`; its output embeds no raw rows and passes `eval/hygiene_check.py`.
- **AC-3 (PR-3, delta correctness).** `delta_report` renders None→number (and number→None) honestly (no fabricated 'down'); every MOVED metric carries a why-moved line; the fix is confined to the currently-unreached None↔number branch and leaves the present numeric output unchanged; the five `COMPARE_METRICS` and the cross-regime exit-2 refusal are unchanged; no `frozen/` artifact is edited.
- **AC-4 (PR-4, ledger integrity).** A default/non-deliverable `run_eval` invocation does not append to `docs/ledger.md`; deliverable intent is explicit; `summary.csv` is still always written; the two existing rows are untouched (append-only); the exit-code contract and immutability guard are unchanged.
- **AC-5 (PR-5, replay honesty — stretch).** A test pins that under `seed_controlled=false`, `replay_check` returns `mode='unseeded'` and `determinism.status='skipped'` (never `'passed'`); `byte_identical()` is marked dead with an explicit upgrade trigger; no fake seed is injected.
- **AC-6 (PR-6, report traceability).** The strategy report reflects the first comparison with a PERMITS/FORBIDS framing; every non-skeleton sentence cites a logged artifact; section 5 remains DEFERRED; no Competition Data, no forbidden claim words.
- **AC-7 (loop discipline).** All App-Zone code (PR-2..PR-5) lands through `/implement` → `/review-sprint` → `/audit-sprint` with one review artifact and one audit artifact; no out-of-loop edits; COMPLETED marker only on explicit operator authorization (`docs/operator/turntrace-loop-contract.md` §1-§3, §10).
- **AC-8 (claim ceiling held).** No tracked Sprint 02 artifact makes a claim beyond Rung 1; the experiment ledger remains the only ceiling-bearing artifact; the forbidden claim words never appear except as negated/forbidden language.

> **Carried gap.** The Sprint 01 closeout cites AC-01..AC-08 while the sprint plan enumerates Sprint 01 ACs only as AC-01..AC-06 (research artifact §2.1 RQ-1). If Sprint 02 inherits any such criteria, resolving them requires the Sprint 01 review/audit feedback artifacts, which are not in tracked evidence.

## 8. Evidence-storage constraints

Per `docs/operator/turntrace-loop-contract.md` §7 / ESP-1..ESP-5 / SP-6, `eval/schemas.md` lines 13-15, and `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` §2 (SP-6):

- **Full run dirs stay local/git-ignored.** The full `runs/<run_id>/` trees (match results, traces, manifest, hashes, `summary.csv`) stay local by default (ESP-1). `run-0001` and `run-0002` remain local/ignored; `run-0001` remains unmutated from Sprint 00. A sealed run is an evidence artifact, not automatically a tracked one.
- **No raw traces committed.** No `decision-trace.jsonl` row contents enter any tracked artifact.
- **No card IDs or card names.** Card-identity signals stay as SHA-256 digests / counts only.
- **No deck lists.** Decks referenced by `deck_id` + hash; `frozen/` stores deck references + content hashes only, never card lists.
- **No simulator logs.** Raw simulator/match logs stay local/ignored.
- **No Competition Data.** The `cg/` cabt SDK, card data CSV/PDF, Kaggle starter `deck.csv`, and raw deck card-lists live under git-ignored `grimoires/loa/context/` and are never committed (CC-1/CC-2).
- **Tracked docs may use only** `run_id`, content hashes, sanitized metrics, claim ceilings, and aggregate categories — referenced, never embedded.
- **Enforcement.** Any later build must keep the `eval/hygiene_check.py` pre-commit guard active. SP-6 / ESP can be relaxed ONLY by explicit operator approval to track a specific, confirmed-redistributable artifact; Sprint 02 must not assume any run-dir contents become trackable.
- **requires-raw-data: cannot-surface** — the actual per-run `result`/`ending_cause` distributions and any run-dir file contents are not surfaced in this PRD or any tracked artifact.

## 9. Claim ceiling

The first comparison sits at ladder **Rung 1** (legal completion / throughput / audit-trail), and **Sprint 02 MUST NOT raise it** (`docs/operator/deferred-lane-gate-after-sprint-01.md` line 43; `docs/claim-ceiling.md`). The experiment ledger (`docs/ledger.md`) remains the **only ceiling-bearing artifact**; per-match records, `summary.csv`, the taxonomy, the aggregate report, and the strategy report carry **no** ceiling (`docs/claim-ceiling.md` lines 5-7; loop contract §8).

**Allowed claim form** — relative, local, carrying its sample size and regime:

> *same-regime local comparison/explanation under `regime-v001` at n=12*

i.e. "candidate (`run-0002`) differs from baseline (`run-0001`) on metric M by delta under `regime-v001` at n=12," explained as the mechanical consequence of the single agent-under-test change.

**Forbidden claim forms** (never assert; the words may appear only as negated/forbidden language):

- gameplay strength
- statistical significance
- cross-regime uplift
- leaderboard quality
- calibration
- optimality
- competitiveness

The forbidden agent claim words remain absolutely forbidden: **strong, competitive, optimal, calibrated, complete** (`docs/claim-ceiling.md` lines 54-59; deferred-lane note line 46).

## 10. Out-of-scope / forbidden list

The following are out of scope for Sprint 02 and are mentioned here only as forbidden. Opening any of these requires a separate, explicit operator decision that supersedes the deferred-lane note (`docs/operator/deferred-lane-gate-after-sprint-01.md` lines 71-87).

**Broad optimization (still closed):**
RL · self-play · deck optimizer · value model · win-probability model · dashboard · ELO / any rating system · tournament system · multi-agent tournament comparisons · search / lookahead / MCTS · Kaggle upload automation · leaderboard optimization · submission packaging · agent tuning loops · two-direction ablation ledger · SaaS / product surface.

**Claim / evidence boundaries:**
claim-ceiling upgrade above Rung 1 · statistical-significance claim · cross-regime comparison (NFR-5; hard-refused by `delta_report`) · runtime agent strengthening (any rule/heuristic/scoring change) · per-decision agent-quality scoring (e.g. a "missed lethal" / "bad prize trade" detector for FM-03/04/06/08).

**Data / sanitization boundaries:**
raw trace/card/deck inspection or emission · committing card IDs/names, deck lists, hand contents, simulator logs, raw trace contents, run-dir file dumps, PDFs/CSVs, `deck.csv` rows.

**Process / zone boundaries:**
editing the `.claude/` System Zone · creating a new regime or editing `regime-v001` / `frozen/` components · creating or mutating run dirs / generating new runs · out-of-loop edits to sprint code · premature COMPLETED marker · any build before the operator opens the Sprint 02 build gate (OA-2).

## 11. Operator decisions needed before SDD / implementation

These do not block the PRD; recommended dispositions are marked and carried as assumptions in §6/§13.

- **OD-1 — PR-5 (replay_check dead-path marker) core or stretch?** *[ASSUMPTION: Stretch.]* The code is already honest; the marker/test is regression-hardening. If the operator wants it guaranteed, promote to Core. If wrong, the only consequence is whether PR-5 is droppable under capacity pressure.
- **OD-2 — PR-4 (ledger hardening / CF-01) mandatory for Sprint 02?** *[ASSUMPTION: Core/mandatory.]* It protects the only ceiling-bearing artifact and is a recorded residual. If the operator defers it, the contamination footgun persists and all Sprint 02 runs (if any) must manually pass `--no-ledger`.
- **OD-3 — Strategy-report update (PR-6) in Sprint 02 or left as closeout docs?** *[ASSUMPTION: in Sprint 02 as Core.]* It fills a mandatory honesty section. If the operator prefers, it can be moved to the Sprint 02 closeout as docs-only. If wrong, the only consequence is which artifact carries the permits/forbids framing.
- **OD-4 — Confirm no per-decision agent-quality detectors are allowed.** *[ASSUMPTION: not allowed.]* FM-03/04/06/08 stay name-only (NG3). Operator confirmation closes the R1 scope-creep risk at the gate.
- **OD-5 — Confirm no runtime agent changes are allowed.** *[ASSUMPTION: none allowed.]* No `agents/runtime/` edits; EXPLAIN/AUDIT only.
- **OD-6 — Confirm no build gate is open yet.** *[ASSUMPTION: none open.]* Implementation begins only after an explicit OA-2. This PRD and the SDD authorize no code.
- **OD-7 — CF-04 housekeeping disposition.** *[ASSUMPTION: handled separately, not Sprint 02 implementation scope.]* `.beads/.br_history/` gitignore; note `.beads/issues.jsonl` is already in the working tree's dirty set. Decide whether this is folded into Sprint 02 or handled as separate housekeeping.
- **OD-8 — Artifact tracking.** *[ASSUMPTION: the taxonomy and strategy-report updates are tracked sanitized artifacts; no run-dir contents are promoted to tracked status.]* SP-6 relaxation requires explicit operator approval.

## 12. Risks

| # | Risk | Mitigation |
|---|------|------------|
| R1 | **Scope creep into optimization** — "explainability"/"taxonomy" reinterpreted as license to tune the agent or build a per-decision quality scorer for FM-03/04/06/08. | Bind Sprint 02 to analysis/offline + provenance layers; forbid `agents/runtime/` edits; keep FM-03/04/06/08 detector-free with an inline boundary note; require each requirement to cite its lane; reject agent-decision-logic touches at review/audit (OD-4, OD-5). |
| R2 | **Claim-ceiling inflation** — the n=12 `win_rate` movement narrated as the agent being "better"/"stronger". | Make Rung-1 boundedness an explicit AC (AC-8); ban the five forbidden words in tracked outputs; require verdict language to carry n + `regime_id`; ledger stays the sole ceiling-bearing artifact. |
| R3 | **Competition-Data / raw-trace leakage** — a new diagnostic or taxonomy reads trace rows and embeds card-adjacent signals into a tracked doc. | Restrict diagnostics to coarse fields (`result`, `ending_cause`, `error`, `turns`, counts, digests); keep `eval/hygiene_check.py` guard active; reference runs by `run_id`+hashes; audit confirms no raw contents embedded (AC-2). |
| R4 | **Ledger contamination (CF-01 / O2)** — a research/test run mutates `docs/ledger.md` by default because `--no-ledger` was forgotten. | Treat PR-4 as in-scope hardening (OD-2); until then mandate `--no-ledger`/`--ledger <tmp>` for any non-deliverable run; per-`run_id` idempotency is a backstop, not a substitute. |
| R5 | **Acting on the CF-03 latent defect** — the None→number 'down n/a' misrender misleads the explanation if relied upon before PR-3 lands. | Add a runnable synthetic-fixture check for the None→number branch before relying on it; keep the explanation narrative off the unhardened branch; keep present numeric output unchanged (AC-3). |
| R6 | **Building before a gate is open** — the narrow-planning note misread as authorization to `/implement`. | Reaffirm loop contract §6: planning artifacts never open the gate; stay in research/plan until an explicit OA-2 (OD-6). |
| R7 | **Metrics naming inconsistency** — metrics-spec `avg_match_length` vs code `avg_turns` mistaken for a defect or "fixed" by editing a frozen component. | During PR-3, confirm whether this is a documented alias; if latent, scope a docs-only/in-code alias note, never a `frozen/` edit (a frozen change is a new regime). |
| R8 | **False-honesty regression on CF-02** — a future change revives `byte_identical()` and pretends byte replay exists. | PR-5 marker/test pins `mode='unseeded'`/`status='skipped'`; never inject a fake seed (OD-1, AC-5). |

## 13. Open questions

- **OQ-1.** Is the SDD §1.6 offline/runtime separation check an executable lint or a convention? The SDD notes it is "added as a Sprint 00 smoke if trivial, otherwise a convention" (research artifact §9 gap). PR-2's validation presumes a runnable lint; if it is convention-only, a prerequisite is to verify/establish it as runnable. *(Resolve during SDD.)*
- **OQ-2.** What is the canonical home for taxonomy v001 — extend `docs/failure-modes.md` in place, or a sibling file under `docs/`? *(SDD decision; either keeps it tracked + sanitized.)*
- **OQ-3.** For PR-4, which deliverable-intent shape is preferred — require an explicit `--ledger <path>` target, or add a `--deliverable` flag, or both? *(SDD decision; AC-4 is shape-agnostic.)*
- **OQ-4.** Are there `run_eval` callers/tests beyond those in evidence that rely on deliverable-by-default? *(Must be enumerated during SDD/implement; affects PR-4 migration — R-related to R4.)*
- **OQ-5.** Does the aggregate report (PR-2) belong in a new `analysis/` module or as an extension of `analysis/aggregate.py`? *(SDD decision; must preserve the import-direction rule either way.)*

## 14. Recommendation

**PROCEED to SDD planning** for Sprint 02 as "Delta Explanation + Failure-Mode Taxonomy," scoped to PR-1, PR-2, PR-3, PR-4, and PR-6 as **Core** and PR-5 as **Stretch** (pending OD-1..OD-3 confirmation). **Do NOT begin implementation:** this PRD opens no build gate, and `/implement` may run only after a separate explicit operator build-gate action (OA-2).

Reasoning:

1. The binding precondition for narrow planning is satisfied and recorded (`docs/operator/deferred-lane-gate-after-sprint-01.md` lines 50-59); the proposed charter maps exactly onto the seven allowed lanes (lines 61-69).
2. There is concrete, well-scoped, non-optimization work ready — a sanitized taxonomy and aggregate diagnostics, plus `delta_report`/`run_eval` hardening of recorded carry-forwards — all confined to the analysis/offline and provenance layers.
3. Sprint 02 strengthens TurnTrace's ability to **explain and audit** comparisons without touching agent strength, bounded by a Rung-1 claim ceiling and a clear forbidden list, under a known implement → review → audit → operator-acceptance closeout path.

The single hard gate is procedural: the operator must accept this PRD and (later) issue OA-2 before any code is written. Until then, only planning proceeds.

> **Sources:** `docs/cycles/cycle-001-sprint-02/00-research-and-planning.md` (binding research input, §§1-14); `docs/operator/deferred-lane-gate-after-sprint-01.md` (lines 37-97); `docs/operator/turntrace-loop-contract.md` (§1-§3, §6, §7, §8, §10); `docs/claim-ceiling.md` (lines 5-7, 20-35, 43-64); `docs/cycles/cycle-001-sprint-01/closeout.md` (lines 1-95); `docs/ledger.md` (lines 5-12); `docs/failure-modes.md` (lines 6-101); `docs/strategy-report.md` (lines 14-68); `docs/cycles/cycle-000-bootstrap/02-turntrace-sdd.md` (§1.6); `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` (§2 SP-6, §3 OA-2); `analysis/delta_report.py` (lines 41-96, 109, 156-170); `analysis/replay_check.py` (lines 69-133); `eval/run_eval.py` (lines 26-29, 93, 103, 305-322).
