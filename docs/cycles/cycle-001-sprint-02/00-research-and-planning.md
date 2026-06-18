# TurnTrace Sprint 02 — Delta Explanation + Failure-Mode Taxonomy

> Planning artifact for TurnTrace Cycle-001 / Sprint 02. Status: research and planning only.
> This document opens NO build gate. Implementation requires a separate, explicit operator action (OA-2 equivalent) per `docs/operator/turntrace-loop-contract.md` §6.
> Binding governance: `docs/operator/deferred-lane-gate-after-sprint-01.md` — "NARROW PLANNING GATE OPENED. Broad optimization remains closed."

## 1. Executive summary

Sprint 01 closed/accepted/integrated on 2026-06-18 (final commit `3492e61`, fast-forward only), producing TurnTrace's first same-regime, agent-only comparison artifact: `run-0001` (baseline, `random_legal`) vs `run-0002` (candidate, frozen `scripted_baseline`) under `regime-v001` at n=12 (`docs/cycles/cycle-001-sprint-01/closeout.md` header + loop, lines 1-31). A metric moved (`win_rate`, `avg_turns`) for an explainable, agent-only reason while the correctness-gate rates stayed at the floor. On that basis the operator recorded the standing decision: **NARROW PLANNING GATE OPENED. Broad optimization remains closed.** (`docs/operator/deferred-lane-gate-after-sprint-01.md` §Gate decision, lines 51-59).

Sprint 02 — **"Delta Explanation + Failure-Mode Taxonomy"** — is proposed strictly inside that narrow lane. Its posture: improve TurnTrace's ability to **EXPLAIN and AUDIT** comparisons. It MUST NOT make the runtime agent stronger; "data first, optimization second" remains binding (deferred-lane note §Sprint 02 planning posture, lines 89-97).

Six candidate tasks are evaluated, all confined to the analysis/offline and provenance layers (SDD §1.6 directory-boundary + import-direction rule, reinforced by the code's own stated import rule): a sanitized failure-mode taxonomy v001 (S02-1), a Competition-Data-safe aggregate failure-mode report (S02-2), `delta_report` hardening for the recorded CF-03 None→number rendering defect (S02-3), ledger-contamination hardening for the CF-01 `run_eval` default footgun (S02-4), a `replay_check` dead-path marker for CF-02 (S02-5, stretch), and a strategy-report update recording what the first comparison permits/forbids (S02-6).

**Recommendation: PROCEED into research/planning only (PRD → SDD → sprint-plan), NOT into build.** Implementation begins only after the operator opens an explicit Sprint 02 build gate. This document opens no gate.

## 2. Sprint 01 evidence recap

Sprint 01 ran the standard loop — `/implement` (sole patch authority) → `/review-sprint` → `/audit-sprint` (both pure-review, Write/Edit disabled) — and was integrated fast-forward only with no merge/squash/tag/version bump (`docs/cycles/cycle-001-sprint-01/closeout.md` header table + loop, lines 1-31). The closeout records AC-01 through AC-08 passing at HIGH confidence, independently re-verified at review and audit.

What the comparison loop produced, mechanically:

- A second sealed, immutable run dir (`run-0002`) as candidate against the `run-0001` baseline; the ONLY changed variable was the agent-under-test (`random_legal` → `scripted_baseline`, a frozen deterministic priority policy, **not tuned**). Opponent, decks, seed-set, metrics-spec, and regime were held constant — `regime-v001`, n=12 (`docs/cycles/cycle-001-sprint-01/closeout.md` Sanitized evidence table, lines 36-48).
- A delta report (PR-14, `analysis/delta_report.py`) comparing the two runs on the same regime, emitting per-metric deltas plus a "why no change" line for every unmoved metric, and HARD-refusing cross-regime comparison (`CrossRegimeRefusal`, exit 2) — enforcing NFR-5 (`analysis/delta_report.py` docstring lines 1-23, cross-regime refusal lines 90-96).
- Sanitized metric movement `run-0001 → run-0002` across `win_rate`, `avg_turns`, `illegal_action_rate`, `timeout_rate`, `error_rate`: `win_rate` and `avg_turns` MOVED while the correctness-gate rates stayed at the floor (`docs/cycles/cycle-001-sprint-01/closeout.md` Sanitized metric movement + bounding callout, lines 55-70).
- Hardened provenance before sealing: `hashes.txt` + `manifest.json` record stable SHA-256 of runtime agent source(s) + eval config; all recompute to MATCH; `git_dirty=true` recorded honestly (entry-gate outcomes, lines 71-83).
- The audit-trail reproducibility floor exercised (PR-15, `replay_check.py`); a frozen scripted baseline (PR-13) and pre-submission mirror validation (PR-18) delivered.
- A second ceiling-bearing ledger row (`run-0002`); the ledger now holds exactly two deliverable rows, both `regime-v001`, both games=12, mode=unseeded (`docs/ledger.md` data rows, lines 11-12).

### 2.1 Research questions (RQ-1 .. RQ-7)

**RQ-1 — What exactly did Sprint 01 prove, and what did it not prove?**
Proved: the evidence loop can produce the first same-regime, agent-only comparison end-to-end, with provenance hardened, the audit-trail floor exercised, and a second ceiling-bearing ledger row appended. Did NOT prove: any gameplay-strength, statistical-significance, or cross-regime claim; it does not raise the claim ceiling above Rung 1; seed control was unavailable (`seed_controlled=false`) so byte-identical replay was not exercised (degraded to audit-trail equality; CF-02). Forbidden agent claim words remain forbidden. (`docs/cycles/cycle-001-sprint-01/closeout.md` lines 18-83; `docs/operator/deferred-lane-gate-after-sprint-01.md` §What this movement is NOT, lines 38-48.) **Gap:** the closeout cites AC-01..AC-08 but the sprint plan enumerates Sprint 01 ACs only as AC-01..AC-06 (`docs/cycles/cycle-000-bootstrap/03-turntrace-sprint-plan.md` lines 291-304); AC-07/AC-08 are referenced but not enumerated in the plan cluster — resolving them requires the Sprint 01 review/audit feedback artifacts, which are not in evidence.

**RQ-2 — What can be explained from current sanitized artifacts without raw card data?**
A substantial amount, because the schemas store card-identity signals only as SHA-256 digests or counts (CC-1/CC-2). From the ledger: two runs with coarse aggregate columns and provenance refs (`docs/ledger.md` lines 9-12). From the delta report: which of the five compared metrics moved vs stayed at the floor, with a per-metric why-line, and why the delta exists (the single deliberate variable was the agent) (`analysis/delta_report.py` lines 41-59, 106-164). For this specific comparison, note that `win_rate` MOVED (so the report's per-metric explanation for it is the why-moved path, not the WHY_NO_CHANGE path). From capability/schema artifacts: the reproducibility reality (`seed_controlled=false`, mode=unseeded) and the sanitization-safe match-summary roll-up fields (`result`, `ending_cause`, `error`, `invalid_action_count`, `turns`) (`docs/claim-ceiling.md` §Reproducibility posture, lines 43-52; `eval/schemas.md` lines 17-52). **Cannot surface:** the per-run distributions of `result`/`ending_cause` actually observed in these 24 matches live in git-ignored run dirs — requires-raw-data: cannot-surface.

**RQ-3 — What coarse failure-mode categories are possible without exposing Competition Data?**
Feasible entirely from sanitized aggregate fields. Two scaffolds exist: the nine seed failure modes FM-01..FM-09 with a fixed entry template and `open|mitigated|watched|wont-fix` status enum (`docs/failure-modes.md` lines 11-101), and the four coarse ledger rate categories (`win_rate`, `illegal_action_rate`, `timeout_rate`, `error_rate`, plus `avg_turns`). Computable now: FM-01 (gate `illegal_action_rate==0`, HARD because `invalid_action_detectable=true`) and FM-07 (track `ending_cause` distribution + `avg_turns`; deck-out maps to cabt reason=2). Capability-blocked/deferred: FM-02 (timeout undetectable), FM-06 (needs richer action decoding), FM-03/04/05/08/09 (regression check "none yet") (`docs/failure-modes.md` lines 25-30, 45-101). Note that FM-03 (bad prize trade), FM-04 (wasted resource), FM-06 (missed lethal), and FM-08 (bad search target) are per-decision "the agent played sub-optimally" loss-attribution judgments — adjacent to evaluating agent quality. They are carried as taxonomy *names* only; no detector is proposed for them in Sprint 02 (see S02-1 in-scope guard). **Gap:** no machine-readable failure-mode schema and no failure-mode aggregation module exist yet; "taxonomy v001" would be net-new.

**RQ-4 — What diagnostics can compare `run-0001` vs `run-0002` safely?**
Both runs share `regime-v001` and n=12, so comparison is permitted (NFR-5 satisfied). Existing/usable: `delta_report.py` per-metric deltas on the five COMPARE_METRICS; `replay_check.py` audit-trail equality (always runs; byte-identical tier skipped under `seed_controlled=false`, status='skipped', never silently passed); ledger-row better/worse verdict permitted ONLY for this same-regime agent-only case (`analysis/delta_report.py` lines 41-96; `analysis/replay_check.py` lines 69-133; `docs/ledger.md` verdict rule, lines 5-7). Additional safe diagnostics from schema fields: `result`-distribution and `ending_cause`-distribution counts, error-presence via the FM-01 invariant, game-length/decision-count comparison, correctness-gate floor comparison, and provenance/integrity comparison via `hashes.txt`/`manifest.json` (`eval/schemas.md` lines 17-119). Any such diagnostic stays in the offline zone: `analysis/` may read run-dir artifacts only and must NOT import `agents/runtime/` or `cabt` directly (SDD §1.6 directory-boundary + import-direction rule), and by the code's own stated rule (the docstrings of `delta_report.py` lines 17-18 and `replay_check.py` lines 20-25) must not import `sim/` or `eval/` either. **Hazard to harden (CF-03):** None→number metric transitions render delta `n/a` with direction always 'down' regardless of value, because `(None or 0) > 0` is False (`analysis/delta_report.py` lines 73-78, 109, 156-160).

**RQ-5 — What should Sprint 02 harden before any future optimization sprint?**
Inside the permitted lane, harden the evidence/audit loop — not the agent: (1) ledger-contamination guard (CF-01, highest priority — `run_eval` writes `docs/ledger.md` by default, opt-OUT design); (2) `delta_report` None→number rendering (CF-03), plus reconcile the `avg_match_length` (metrics-spec) vs `avg_turns` (code) naming; (3) reproducibility-floor/dead-path clarity (CF-02 — keep audit-trail equality, do not invest in byte-replay); (4) a coarse failure-mode/diagnostic aggregation layer; (5) preserve provenance/separation (O1 source-hashing, SDD §1.6 import-direction); (6) housekeeping (CF-04 `.beads/.br_history/` gitignore) (`docs/operator/deferred-lane-gate-after-sprint-01.md` lines 61-97; `docs/cycles/cycle-001-sprint-01/closeout.md` CF-01..CF-04, lines 86-95).

**RQ-6 — Which audit carry-forwards should be pulled into Sprint 02?**
The Sprint 00 entry carry-forwards (O1, O2, O3) were resolved during Sprint 01 — preserve, don't re-open. The live items are the four new Sprint 01 carry-forwards. Pull in (permitted): CF-01 (ledger contamination), CF-03 (delta_report None→number), CF-04 (housekeeping gitignore). Hold/conditional: CF-02 (byte-replay) — keep documented, do not build absent proven seed control (`docs/cycles/cycle-001-sprint-01/closeout.md` lines 71-95).

**RQ-7 — What should remain explicitly out of scope?**
The full "Still closed" broad-optimization list (RL, self-play, deck optimizer, value/win-probability model, dashboard, ELO, tournament/multi-agent comparisons, search/MCTS, Kaggle upload automation, leaderboard optimization, agent tuning loops, submission packaging, two-direction ablation ledger, SaaS); all claim/evidence boundary crossings (no ceiling upgrade, no statistical-significance, no cross-regime comparison, no strength claims, no agent strengthening); all sanitization/data exposure; and process boundaries (no out-of-loop edits, no premature COMPLETED marker, no build until OA-2) (`docs/operator/deferred-lane-gate-after-sprint-01.md` §Still closed, lines 71-87; `docs/claim-ceiling.md` lines 37-64; `docs/operator/turntrace-loop-contract.md` §2, §6, §7, §10).

## 3. What is proven / not proven

| Claim area | Status | Evidence |
|---|---|---|
| Evidence loop produces a first same-regime, agent-only comparison end-to-end | **Proven** | `docs/cycles/cycle-001-sprint-01/closeout.md` lines 18-48 |
| A metric moved (`win_rate`, `avg_turns`) for an explainable agent-only reason | **Proven** | closeout lines 55-70; `docs/operator/deferred-lane-gate-after-sprint-01.md` lines 27-36 |
| Correctness-gate rates (`illegal_action`, `timeout`, `error`) held at the floor | **Proven** | closeout lines 55-70 |
| Provenance hardened before sealing (source-hash, `git_dirty=true` honest) | **Proven** | closeout lines 71-83 |
| Audit-trail reproducibility floor exercised | **Proven** | `analysis/replay_check.py` lines 69-88 |
| Two ceiling-bearing ledger rows exist | **Proven** | `docs/ledger.md` lines 11-12 |
| Gameplay strength / quality | **NOT proven** (forbidden claim) | `docs/operator/deferred-lane-gate-after-sprint-01.md` lines 38-48; `docs/claim-ceiling.md` lines 20-23 |
| Statistical significance | **NOT proven** | closeout lines 65-70 |
| Cross-regime comparison / uplift | **NOT proven** (hard-refused by `delta_report`) | `analysis/delta_report.py` lines 90-96; `docs/claim-ceiling.md` lines 62-64 |
| Byte-identical reproducibility / determinism | **NOT proven** (`seed_controlled=false`; CF-02 path unreachable) | `analysis/replay_check.py` lines 98-133; closeout lines 86-95 |
| Claim ceiling above Rung 1 | **NOT raised** | `docs/operator/deferred-lane-gate-after-sprint-01.md` line 43 |
| Per-run `result`/`ending_cause` distributions actually observed | **requires-raw-data: cannot-surface** | git-ignored run dirs (ESP-1) |

> Note on CF-03 reachability: for the current numeric runs (`run-0001` vs `run-0002`) all five compared metrics carry numeric values on both sides — `win_rate` moved (e.g. it is not an unmoved metric for this pair), so the WHY_NO_CHANGE win_rate line is NOT rendered for this comparison and the None→number branch is NOT reached. CF-03 is therefore a latent/unreached path for these runs (closeout CF-03); S02-3 hardens that currently-unreached branch and must not be expected to change any live output for this comparison.

## 4. Deferred-lane interpretation

The binding status is **"NARROW PLANNING GATE OPENED. Broad optimization remains closed."** (`docs/operator/deferred-lane-gate-after-sprint-01.md` §Gate decision, lines 51-59). This is an operator decision **note** — docs-only, authorizes no code (header lines 5-8) — and it does **not** open a Sprint 02 build gate; that still requires a separate explicit operator action (OA-2 per `docs/operator/turntrace-loop-contract.md` §6 and `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` §3).

**ALLOWS** Sprint 02 to be researched and planned (not built) as "Delta Explanation + Failure-Mode Taxonomy" along exactly the seven narrow-planning lanes the note enumerates (lines 61-69):

1. Explainability of the first delta (`run-0001` → `run-0002`).
2. Failure-mode taxonomy (extending FM-01..FM-09 in `docs/failure-modes.md`).
3. Comparison robustness (`delta_report` edge-case correctness).
4. Trace-safe and Competition-Data-safe AGGREGATE diagnostics (coarse rollups over `result`/`ending_cause`/`error`, never raw trace contents).
5. Provenance and ledger hardening (CF-01 `run_eval` ledger-default footgun; source-hash provenance).
6. `delta_report` hardening (CF-03 None→number rendering).
7. Operator-decision framing for a FUTURE improvement sprint.

**DOES NOT ALLOW** any work touching the runtime agent's playing strength. The note is explicit: "Sprint 02 must not directly optimize the agent unless a later operator decision explicitly opens that lane" and "should explain and harden the evidence loop before improving gameplay" (lines 89-97). Work is confined to the analysis/offline and provenance layers: per SDD §1.6, `analysis/` may read run-dir artifacts (read-only) only and may NOT import `agents/runtime/` or `cabt` directly (directory-boundary + import-direction rule); by the code's own stated rule (the docstrings of `analysis/delta_report.py` and `analysis/replay_check.py`, expressing the NFR-1 offline/runtime separation intent) it also imports none of `sim/` or `eval/`. "Data first, optimization second" remains binding. Any "Still closed" item requires a separate operator decision that supersedes this note.

## 5. Proposed Sprint 02 mission

**Mission:** Strengthen TurnTrace's ability to EXPLAIN the first same-regime comparison and to AUDIT future comparisons, by (a) building a sanitized, coarse failure-mode taxonomy and aggregate diagnostic layer, and (b) hardening the comparison/provenance plumbing (`delta_report`, `run_eval` ledger writes) against the recorded carry-forwards — all without touching the runtime agent.

**Non-goal (binding):** No change to agent playing strength. No heuristic/rule tuning. No claim-ceiling movement. The mission is explanation and audit, not optimization (`docs/operator/deferred-lane-gate-after-sprint-01.md` lines 89-97).

**Framing label:** "Delta Explanation + Failure-Mode Taxonomy" — the operator-stated Sprint 02 framing (deferred-lane note lines 89-94).

## 6. Proposed in-scope tasks

All tasks cite the narrow-planning lane they serve. Tasks that write App-Zone code (`analysis/`, `eval/`) must land through `/implement` → `/review-sprint` → `/audit-sprint` and require an opened Sprint 02 build gate (OA-2) before any code is written; pure-docs tasks open no gate.

| ID | Refined title | Recommendation | Lane served |
|---|---|---|---|
| S02-1 | Failure-mode taxonomy v001 (tracked, sanitized coarse-outcome category schema) | **Include** (pure docs/schema) | Failure-mode taxonomy |
| S02-2 | Failure-mode report: read local IGNORED run summaries, emit sanitized AGGREGATE categories only | **Include** (App-Zone code; needs OA-2) | Trace-safe aggregate diagnostics |
| S02-3 | `delta_report` hardening: richer why-moved/why-no-change + correct None→number rendering (CF-03) | **Include** (App-Zone code; needs OA-2) | `delta_report` hardening / comparison robustness |
| S02-4 | Ledger hardening: non-deliverable `run_eval` calls cannot mutate `docs/ledger.md` by default (CF-01) | **Include** (App-Zone code; needs OA-2) | Provenance and ledger hardening |
| S02-5 | `replay_check` dead-path marker: mark/test `byte_identical()` unreachable under `seed_controlled=false` (CF-02) | **Include — stretch** (App-Zone code; needs OA-2) | Comparison robustness / audit honesty |
| S02-6 | Strategy-report update: record what the first comparison permits and forbids | **Include** (pure docs) | Operator-decision framing |

### S02-1 — Failure-mode taxonomy v001 (tracked, sanitized coarse-outcome category schema)

- **Recommendation:** Include. Squarely in the permitted "failure-mode taxonomy" lane; pure docs/schema, opens no build gate, no agent strengthening.
- **Rationale:** The deferred-lane note explicitly permits "failure-mode taxonomy" (`docs/operator/deferred-lane-gate-after-sprint-01.md` lines 61-69). A scaffold exists in `docs/failure-modes.md`: a fixed entry template (id, Status enum `open|mitigated|watched|wont-fix`, Signature, Description, "Why it costs games", Examples, Regression check, Notes — lines 11-23) and seed catalogue FM-01..FM-09 (lines 32-101). The taxonomy reuses only coarse, sanitization-safe signals already exposed — the `result` enum and `ending_cause` enum from match-summary (`eval/schemas.md` lines 17-52) and the four ledger rate columns (`docs/ledger.md` line 9) — never raw trace contents. This is EXPLAIN/AUDIT work: it names categories, it does not change the agent. The registry's own rule (`docs/failure-modes.md` lines 6-7) requires that an entry be kept only if its Signature is computable from fields the simulator provides; FM-03/04/05/08/09 have no regression check and FM-06 needs richer action decoding, so taxonomy v001 must mark those aspirational/deferred rather than implying detectors exist. FM-03 (bad prize trade), FM-04 (wasted resource), FM-06 (missed lethal), and FM-08 (bad search target) are specifically per-decision "agent played sub-optimally" loss-attribution categories; carrying them as names is EXPLAIN/AUDIT, but building any detector that *scores* per-decision quality for them would cross from aggregate diagnostics toward per-decision agent-quality evaluation (forbidden raw-trace/card inspection and strength-adjacent), so v001 keeps them detector-free.
- **Acceptance criteria:**
  - Taxonomy v001 is a tracked docs artifact (extends `docs/failure-modes.md` or a sibling docs file) containing NO Competition Data: categories reference signals by field name (`result`, `ending_cause`) and trace rows by `run_id`+`match_id`+`decision_index` only.
  - Each category declares computable-now vs deferred, naming the gating capability flag (`seed_controlled=false`, `invalid_action_detectable=true`, `timeout_detectable=false`), consistent with the existing Capability context block (`docs/failure-modes.md` lines 25-30).
  - Categories are coarse outcome/loss buckets only (per-`ending_cause` counts, per-`result` counts, FM-id mapping); no per-decision card/deck/hand content and no new agent behavior.
  - Every category lacking a computable detector today is explicitly marked aspirational (Status / Regression check "none yet").
  - **In-scope guard (per-decision quality):** FM-03/04/06/08 stay marked "aspirational / no detector / detect-and-describe only". Building any per-decision quality detector for these (e.g. a "missed lethal" or "bad prize trade" scorer) is NOT covered by the narrow-planning gate and is itself a separate operator decision; the taxonomy artifact must state this boundary inline so a future build cannot read v001 as license to implement such a detector.
  - Claim-ceiling language preserved: no forbidden words; bounded to Rung 1; asserts no strength claim.
- **Validation:** Run `eval/hygiene_check.py` against the new/edited doc (must pass); grep for forbidden claim words (`strong|competitive|optimal|calibrated|complete`) — zero in agent-claim context; cross-check every named Signature field against `eval/schemas.md` and `sim/capabilities.json`; confirm each Status uses only the allowed enum; confirm FM-03/04/06/08 carry no detector and the per-decision-detector boundary note is present.
- **Risk:** Drift toward agent-strengthening if a category is written as a "fix recipe" rather than a detection signature, or overstating coverage by listing detectors for capability-blocked categories, or a future build implementing a per-decision quality scorer for FM-03/04/06/08. Mitigate by keeping every entry detect-and-describe, marking non-computable categories aspirational, and recording inline that any per-decision quality detector is a separate operator decision outside this gate (R1).

### S02-2 — Failure-mode report: read local IGNORED run summaries, emit sanitized AGGREGATE categories only

- **Recommendation:** Include. Permitted "trace-safe and Competition-Data-safe aggregate diagnostics"; writes App-Zone code (`analysis/`), so it requires the `/implement` gate and an opened Sprint 02 build gate (OA-2).
- **Rationale:** Explicitly permitted (deferred-lane note lines 61-69). There is currently NO failure-mode aggregation module — `aggregate.py` emits only the 11-column `summary.csv` and one ledger row, with no `ending_cause`/`error`/`result`-distribution bucketing (`analysis/aggregate.py` SUMMARY_COLUMNS lines 29-33). The report reads ONLY already-aggregated, sanitization-safe fields from local IGNORED run dirs — `result`, `ending_cause`, error-populated flag, `invalid_action_count`, `turns` — which the schema designed to carry no card IDs (`eval/schemas.md` lines 13-16). It must emit AGGREGATE categories (counts per `ending_cause`, per `result`) and NEVER raw trace rows. Hard separation: `analysis/` may read run-dir artifacts (read-only) only and may NOT import `agents/runtime/` or `cabt` directly (SDD §1.6 directory-boundary + import-direction rule); by the code's stated rule (the `delta_report.py`/`replay_check.py` docstrings, NFR-1 separation intent) it also imports none of `sim/` or `eval/`. It must land through the loop (loop contract §1), and no Sprint 02 build gate is recorded yet, so OA-2 is a prerequisite.
- **Acceptance criteria:**
  - Reads only match-summary aggregate fields (`result`, `ending_cause`, error-flag, `invalid_action_count`, `turns`, `total_decisions`, `trace_present`) from a local run dir; MUST NOT read or emit `decision-trace.jsonl` row contents, card IDs, deck lists, or hand contents.
  - Output is coarse categories only: counts/rates per `ending_cause` and per `result`, plus FM-id linkage by reference string (`run_id`+`match_id`+`decision_index`) — never embedded raw rows.
  - Respects the offline/runtime separation: imports `agents/runtime/` and `cabt` not at all (SDD §1.6), and by the code's stated rule imports none of `sim/` or `eval/` either; analysis-zone only.
  - Output carries the claim-ceiling footer pattern (bounded by `regime_id` + n, no strength claim), consistent with `delta_report.render` (`analysis/delta_report.py` lines 166-170).
  - On a run dir with no matches / missing fields, degrades cleanly (undetectable reported, never silently passed).
- **Validation:** Run against local `run-0001`/`run-0002`; confirm output is aggregate counts only with zero card/deck/hand tokens; run `eval/hygiene_check.py` and the import-direction lint (both must pass); unit test with synthetic match-summary fixtures (no Competition Data) covering each `ending_cause`/`result` value, asserting category counts and that no raw row is present; confirm `/implement` was the writing authority and the change passed review+audit; confirm OA-2 build gate opened before any code is written.
- **Risk:** Highest sanitization-exposure task in the slate: a careless read of `traces/*.jsonl` or echoing an error string containing card text would leak Competition Data into a tracked output. Also drifts toward forbidden scope if it adds per-decision "quality" scoring (that is agent evaluation, not aggregate diagnostics). Mitigate by restricting inputs to match-summary aggregate fields and emitting counts only.

### S02-3 — `delta_report` hardening: richer why-moved/why-no-change lines + correct None→number rendering

- **Recommendation:** Include. Directly named permitted ("`delta_report` hardening", "comparison robustness") and maps to CF-03; App-Zone code, needs `/implement` gate + OA-2.
- **Rationale:** Both lanes are explicitly permitted (deferred-lane note lines 61-69), and this maps to CF-03 (`docs/cycles/cycle-001-sprint-01/closeout.md` lines 86-95). The code confirms the defect: when a metric is None on one side and numeric on the other, `_delta` returns None (lines 73-78), the moved test fires via `va != vb and d is None` (line 109), and direction is computed `(m['delta'] or 0) > 0` = `(None or 0) > 0` = False, so a None→number transition is ALWAYS rendered direction 'down' with delta 'n/a' regardless of actual values (lines 156-160). A "why moved" line is also absent — only unmoved metrics get an explanation (WHY_NO_CHANGE dict, render loop lines 145-151). This is a latent/unreached branch for the current numeric runs (all five metrics are numeric on both sides of `run-0001` vs `run-0002`; closeout CF-03), so the fix is regression-hardening of a currently-unreached path, not a live output change. Pure EXPLAIN hardening of the audit artifact; does not touch the agent. Secondary robustness item: the metrics-spec uses `avg_match_length` while `delta_report`/`aggregate` use `avg_turns` (`frozen/metrics/metrics-spec-v001.json` line 7 vs `analysis/delta_report.py` line 42); the report should make this alias explicit, but renaming frozen artifacts is OUT of scope (a frozen-component change is a new regime per NFR-5).
- **Acceptance criteria:**
  - A None→number (or number→None) transition renders honestly — not a spurious 'down': either an explicit "appeared/disappeared" status with no fabricated direction, or a "why moved" explanation naming the None side.
  - The fix is scoped to the currently-unreached None↔number branch; it MUST NOT alter rendering for the present numeric runs (`run-0001` vs `run-0002` output is unchanged for all five numeric metrics), so a reviewer should expect no live data change for this comparison — only new behavior on the previously-dead branch, covered by synthetic fixtures.
  - Each MOVED metric gets a "why moved" line (symmetric with existing WHY_NO_CHANGE coverage), bounded by the ledger claim ceiling, asserting no strength claim.
  - The five COMPARE_METRICS set and the cross-regime hard-refusal (exit 2) are unchanged; `avg_wall_clock_ms` stays excluded from comparison (`analysis/delta_report.py` lines 41-43, 90-96, 162-164).
  - The `avg_match_length` vs `avg_turns` relationship is documented in-code/in-report; no `frozen/` artifact is edited.
  - No forbidden claim words introduced; claim-ceiling footer preserved.
- **Validation:** Unit test with synthetic stats where one metric is None on side A and numeric on side B (and vice versa): assert honest status/direction (no false 'down') and a why-line present; unit test asserting every MOVED metric has a why-moved line and every unmoved metric still has its why-no-change line; run against local `run-0001` vs `run-0002` and assert the rendered output is byte-unchanged for the five numeric metrics (confirming the fix touches only the unreached branch); confirm cross-regime refusal still exits 2; grep for forbidden claim words; confirm change lands via `/implement` and passes review+audit.
- **Risk:** Scope creep into "fixing" the `avg_match_length`/`avg_turns` divergence by editing `frozen/metrics-spec-v001.json` — that mutates a frozen regime component (forbidden; any change is a new regime v002 per `docs/claim-ceiling.md` lines 29-35). Keep the fix to rendering + an in-code alias note. Lower risk: over-explaining moved metrics in a way that implies strength — bound every line to the ceiling.

### S02-4 — Ledger hardening: non-deliverable `run_eval` calls cannot mutate `docs/ledger.md` by default (CF-01)

- **Recommendation:** Include. Named permitted ("provenance and ledger hardening") and is the exact recorded residual CF-01; App-Zone code (`eval/run_eval.py`), needs `/implement` gate + OA-2.
- **Rationale:** Permitted lane (deferred-lane note lines 61-69); this is the precise recorded residual CF-01 (`docs/cycles/cycle-001-sprint-01/closeout.md` lines 86-95), the unresolved tail of the Sprint 00 O2 footgun. Code confirms the opt-OUT design: `write_ledger = not args.no_ledger`, `--no-ledger` defaults False, `ledger_path` defaults to `REPO_ROOT/docs/ledger.md`, so a bare `python eval/run_eval.py` mutates the tracked ledger by default; the only intent flag is the absence of `--no-ledger` (`eval/run_eval.py` lines 26-37, 263-280, 305-322). `aggregate.append_ledger_row` is already idempotent per `run_id` and requires a non-empty `claim_ceiling` (`analysis/aggregate.py` lines 110-140), so this is about making intent explicit, not row correctness. AUDIT hardening of evidence integrity — it makes a stray run unable to contaminate the only ceiling-bearing artifact; does not touch the agent.
- **Acceptance criteria:**
  - Writing a tracked ledger row requires explicit deliverable intent (explicit `--ledger` target or `--deliverable` flag) — a default/non-deliverable invocation does NOT append to `docs/ledger.md`.
  - `summary.csv` is still always written for every run (non-ledger path unchanged: `eval/run_eval.py` lines 274-280).
  - Idempotency and the non-empty `claim_ceiling` requirement preserved (`analysis/aggregate.py` lines 125-140 unchanged).
  - The two existing deliverable rows (`run-0001`, `run-0002`) in `docs/ledger.md` are not edited in place (append-only invariant; `docs/ledger.md` lines 3-7).
  - Exit-code contract (0/1/2/3) and the immutability guard unchanged (`eval/run_eval.py` lines 300-331).
- **Validation:** Invoke in the new non-deliverable/default mode against a throwaway run dir; assert `docs/ledger.md` unchanged (empty diff) and `summary.csv` exists; invoke with explicit deliverable intent against a throwaway ledger path; assert exactly one row appended and idempotent on re-run; run existing smoke/`run_eval` tests to confirm exit-code contract + immutability guard hold, and check whether any test/wrapper relied on deliverable-by-default (update those callers in the same `/implement`); confirm `docs/ledger.md` still has exactly the two run rows with no in-place edits; confirm change lands via `/implement` and passes review+audit.
- **Risk:** Flipping the default to opt-in could silently break an existing caller/test that relied on deliverable-by-default (callers not enumerated in evidence), causing a real run to skip its intended ledger row. Mitigate by auditing all `run_eval` callers in the same change and making deliverable intent loud/explicit. Secondary: must not edit existing ledger rows (append-only).

### S02-5 — `replay_check` dead-path marker: mark/test `byte_identical()` unreachable under `seed_controlled=false` (CF-02)

- **Recommendation:** Include — stretch. Permitted under "comparison robustness"/audit honesty and maps to CF-02; low value/low effort, App-Zone code, needs `/implement` gate + OA-2.
- **Rationale:** Maps directly to CF-02 (`docs/cycles/cycle-001-sprint-01/closeout.md` lines 86-95). Code confirms the dead path: `replay_check` only calls `byte_identical` when `seeded` is True AND `--replay-run` is provided; `_seed_controlled` derives `seeded` from records and `seed_controlled=false`, so the determinism branch is explicitly SKIPPED with status='skipped' (`analysis/replay_check.py` lines 114-133). The honest posture is already in place — the docstring states the two-tier degraded reality (lines 4-18) and never silently passes. Remaining value is small: a marker/test asserting the dead path STAYS dead under current reality (status='skipped', mode='unseeded'), plus an explicit unreachable/dead-path marker (e.g. `loa:shortcut` naming the upgrade trigger = seed control proven). AUDIT honesty, not a feature. Include-stretch because the current code is already honest — the task hardens against regression rather than fixing a live defect.
- **Acceptance criteria:**
  - A test asserts that under `seed_controlled=false`, `replay_check` returns mode='unseeded' and determinism.status='skipped' (never 'passed') (`analysis/replay_check.py` lines 117-125).
  - `byte_identical()` is annotated as a dead/unreachable path with an explicit upgrade trigger (reachable only if `seed_controlled` becomes true), per the `loa:shortcut` ceiling+trigger convention.
  - No code path fabricates or simulates byte-identical replay while `seed_controlled=false`.
  - The always-on audit-trail equality tier (`audit_trail_equality`, lines 69-88) is unchanged.
  - If a seeded test is added, it is gated/marked so it only becomes meaningful when seed control is proven (no fake seed injected to force the path green).
- **Validation:** Run against local `run-0001`/`run-0002`; assert mode='unseeded', determinism.status='skipped', verdict driven only by audit-trail equality; run the new test; confirm it fails if someone changes the skip branch to silently pass; confirm `sim/capabilities.json` still reports `seed_controlled=false` before asserting the dead path stays dead; confirm change lands via `/implement` and passes review+audit.
- **Risk:** Negative-value drift: "testing" a dead path by injecting a fake seed to make `byte_identical` run would pretend byte replay exists — the exact thing CF-02 forbids. Keep the test to asserting the skip/unseeded posture; do not manufacture seed control. Given the code is already honest, weigh whether this earns a slot vs deferring to whenever seed control is actually investigated.

### S02-6 — Strategy-report update: record what the first comparison permits and forbids

- **Recommendation:** Include. Named permitted ("operator decision framing for a future improvement sprint") and pure docs; fills mandatory honesty sections, opens no gate.
- **Rationale:** Explicitly permitted (deferred-lane note lines 61-69). `docs/strategy-report.md` is currently a SKELETON — seven of its eight sections are TODO (sections 1, 2, 3, 4, 6, 7, 8) and section 5 (ablation table) is DEFERRED (status lines 14, 19, 24-25, 32-33, 40, 46, 53-54, 61). Section 6 (failure-mode) is declared Mandatory and omitting known failures violates the Rung 4 honesty gate (lines 42-46), so updating the report to reflect the now-existing first comparison is honesty-driven, not optional polish. The update must state what the first same-regime comparison (`run-0001` vs `run-0002`, `regime-v001`, n=12) PERMITS (a recorded same-regime agent-only metric movement, bounded by the Rung-1 ledger ceiling) and FORBIDS (no strength/significance/cross-regime/leaderboard claim; broad-optimization lane remains closed) — mirroring the deferred-lane note's partition. Binding traceability: every claim sentence must point to a specific logged artifact or be deleted (lines 65-68). Pure docs in the State/docs zone; strengthens explanation, not the agent.
- **Acceptance criteria:**
  - Sections reflect the first comparison's reality: section 1 (claim ceiling = Rung 1), section 4 (evaluation method = the `run-0001` vs `run-0002` same-regime agent-only comparison, n=12, mode=unseeded), section 6 (failure-mode linkage), section 7 (limitations: unseeded/no byte-replay, timeout undetectable, n small, opponent=mirror).
  - A PERMITS/FORBIDS framing consistent with `docs/operator/deferred-lane-gate-after-sprint-01.md`: permitted = recorded same-regime agent-only movement bounded by ceiling; forbidden = strength/significance/cross-regime/leaderboard claims and all "Still closed" broad-optimization items.
  - Every claim sentence references a specific logged artifact (ledger row / match-summary / regime hash / `delta_report` output) per the traceability rule (lines 65-68); no unbacked sentence.
  - No Competition Data; decks referenced by `deck_id`+hash; runs by `run_id`+hashes; no raw metric values pasted as "evidence" beyond what the ledger already sanitizes.
  - No forbidden claim words; the ablation table (section 5) remains DEFERRED.
- **Validation:** Manual traceability pass (each non-skeleton sentence cites an existing artifact path/reference); run `eval/hygiene_check.py` against the edited report and grep for forbidden claim words and any card/deck token (expect none); cross-check the PERMITS/FORBIDS section against the deferred-lane note's §Still closed and §What this movement is NOT (every forbidden item present, nothing reframed as permitted); confirm section 5 still reads DEFERRED.
- **Risk:** Subtle drift: framing the recorded metric movement as evidence the agent is better, or implying the narrow-planning lane authorizes optimization. The deferred-lane note exists specifically to prevent the Sprint 01 movement being misread as permission for broad optimization (lines 51-59) — keep PERMITS strictly to "a metric moved for an explainable reason" and FORBIDS comprehensive. Also avoid pasting raw run-metric values as evidence; cite the sanitized ledger row instead.

## 7. Proposed out-of-scope list

The following remain out of scope for Sprint 02. Opening any of these requires a separate, explicit operator decision that supersedes the deferred-lane note.

**Broad-optimization items (still closed — `docs/operator/deferred-lane-gate-after-sprint-01.md` §Still closed, lines 71-87):**
- Reinforcement learning (RL); self-play; deck optimizer; value model; win-probability model.
- Dashboard; ELO / any rating system; tournament system; multi-agent tournament comparisons.
- Search / lookahead / MCTS.
- Kaggle upload automation; leaderboard optimization; submission packaging.
- Agent tuning loops (any rule/heuristic tuning of the runtime agent — "data first, optimization second" is binding).
- Two-direction ablation ledger; SaaS / product surface.

**Claim / evidence boundaries (`docs/claim-ceiling.md` lines 20-64):**
- Claim-ceiling upgrade above Rung 1.
- Statistical-significance claims.
- Cross-regime comparison (NFR-5; hard-refused by `delta_report`).
- Gameplay-strength claims; the words strong/competitive/optimal/calibrated/complete remain forbidden for the agent.
- Directly making the runtime agent stronger in any way.
- Per-decision agent-quality detectors/scorers (e.g. a "missed lethal" or "bad prize trade" quality scorer for FM-03/04/06/08) — these cross from aggregate diagnostics toward per-decision agent-quality evaluation and require a separate operator decision; not covered by the narrow-planning gate.
- Byte-identical determinism work (CF-02) — unreachable while `seed_controlled=false`; only add if a future seed-controlled regime is proven.

**Sanitization / data boundaries (`docs/operator/turntrace-loop-contract.md` §7; `eval/schemas.md` lines 13-15):**
- Committing or embedding Competition Data: card IDs/names, deck lists, hand contents, simulator step logs, raw trace contents, run-dir file dumps, PDFs/CSVs, `deck.csv` rows. Card-identity signals stay as SHA-256 digests/counts only.
- Raw trace/card/deck inspection or emission into tracked artifacts; full `runs/<run_id>/` trees stay local/git-ignored (ESP-1).

**Process / zone boundaries:**
- Editing the `.claude/` System Zone (use `.claude/overrides/` or `.loa.config.yaml`).
- Creating a new regime or editing `regime-v001` components (any component change is a new regime v002, never an edit; `docs/claim-ceiling.md` lines 29-35).
- Out-of-loop edits to sprint code; premature COMPLETED marker; any build before the operator opens the Sprint 02 build gate.

## 8. Acceptance criteria draft

Sprint-level acceptance criteria (per-task ACs are in §6). All criteria are bounded to Rung 1 and forbid agent strengthening.

- **AC-S02-1 (taxonomy honesty):** Failure-mode taxonomy v001 exists as a tracked, sanitized docs artifact; every category declares computable-now vs deferred with its gating capability flag; categories lacking a detector are marked aspirational; FM-03/04/06/08 carry no per-decision quality detector and the artifact records that any such detector is a separate operator decision outside the narrow-planning gate; no Competition Data; no forbidden claim words.
- **AC-S02-2 (aggregate-only diagnostics):** The failure-mode report reads only match-summary aggregate fields from local IGNORED run dirs and emits coarse counts per `result`/`ending_cause` only; it does not import `agents/runtime/` or `cabt` (SDD §1.6) and, by the code's stated import rule, imports none of `sim`/`eval` either; its output embeds no raw rows and passes `eval/hygiene_check.py`.
- **AC-S02-3 (delta correctness):** `delta_report` renders None→number (and number→None) transitions honestly (no fabricated 'down'), and every MOVED metric carries a why-moved line; the fix is confined to the currently-unreached None↔number branch and leaves the present numeric `run-0001` vs `run-0002` output unchanged; the five COMPARE_METRICS set and the cross-regime exit-2 refusal are unchanged; no `frozen/` artifact is edited.
- **AC-S02-4 (ledger integrity):** A default/non-deliverable `run_eval` invocation does not append to `docs/ledger.md`; deliverable intent is explicit; `summary.csv` is still always written; the two existing rows are untouched; the exit-code contract and immutability guard are unchanged.
- **AC-S02-5 (replay honesty, stretch):** A test pins that under `seed_controlled=false`, `replay_check` returns mode='unseeded' and determinism.status='skipped' (never 'passed'); `byte_identical()` is marked dead with an explicit upgrade trigger; no fake seed is injected.
- **AC-S02-6 (report traceability):** The strategy report reflects the first comparison with a PERMITS/FORBIDS framing; every non-skeleton sentence cites a logged artifact; section 5 remains DEFERRED; no Competition Data, no forbidden claim words.
- **AC-S02-7 (loop discipline):** All App-Zone code (S02-2..S02-5) lands through `/implement` → `/review-sprint` → `/audit-sprint` with one review artifact and one audit artifact; no out-of-loop edits; COMPLETED marker only on explicit operator authorization (`docs/operator/turntrace-loop-contract.md` §1-§3, §10).

**Note (carried gap):** the Sprint 01 closeout references AC-07/AC-08 not enumerated in the sprint-plan cluster; if Sprint 02 inherits any such criteria, resolving them requires the Sprint 01 review/audit feedback artifacts, which are not in evidence.

## 9. Validation plan draft

- **Hygiene gate (all docs + code outputs):** `eval/hygiene_check.py` must pass on every new/edited tracked artifact (refuses staged Competition-Data paths). Grep every tracked output for forbidden claim words and for card/deck tokens — expect none.
- **Separation lint (S02-2..S02-5):** Confirm the offline/runtime separation holds for all `analysis/` changes — no import of `agents/runtime/` or `cabt` directly (SDD §1.6 directory-boundary + import-direction rule), and by the code's stated rule (the `delta_report.py`/`replay_check.py` docstrings) no import of `sim/` or `eval/` either. **Gap:** whether this lint is an executable check vs a convention is not confirmed in evidence (SDD §1.6 notes it is added as a Sprint 00 smoke if trivial, otherwise a convention); a prerequisite is to verify/establish it as runnable.
- **Unit tests (S02-2, S02-3, S02-4, S02-5):** synthetic fixtures only (no Competition Data) — aggregate-category counts (S02-2), None↔number rendering and why-line coverage (S02-3), default-vs-deliverable ledger behavior + idempotency (S02-4), unseeded/skipped replay posture (S02-5).
- **Run-dir diagnostics (read-only, local):** run S02-2/S02-3/S02-5 against local `run-0001`/`run-0002`; confirm outputs are aggregate/honest only; never embed raw contents. For S02-3, additionally assert the rendered output is unchanged for the five numeric metrics (the None↔number fix touches only the currently-unreached branch). `run-0001` must remain unmutated from Sprint 00.
- **Regression on existing behavior:** `delta_report` numeric movers unchanged and cross-regime exit-2 preserved; `run_eval` exit-code contract (0/1/2/3) and immutability guard preserved; `summary.csv` always written.
- **Loop verification:** confirm `/implement` was sole patch authority; one `/review-sprint` artifact and one `/audit-sprint` artifact; review/audit ran pure-review (Write/Edit disabled is expected, not a failure).

## 10. Evidence-storage constraints

Per `docs/operator/turntrace-loop-contract.md` §7 / ESP-1..ESP-5 / SP-6 and `eval/schemas.md` lines 13-15:

- **Tracked in git (sanitized only):** the new failure-mode taxonomy / delta-explanation docs, sanitized aggregate summaries, ledger rows (`docs/ledger.md`), claim-ceiling text, failure-mode notes (`docs/failure-modes.md`), planning docs, operator-approved artifacts. App-Zone code is tracked; `frozen/` stores deck references + content hashes ONLY, never card lists.
- **Local-only / git-ignored, NEVER committed (CC-1/CC-2):** Competition Data — the `cg/` cabt simulator SDK, card data CSV/PDF, Kaggle starter `deck.csv`, raw deck card-lists, under git-ignored `grimoires/loa/context/`. Any later build must keep the `eval/hygiene_check.py` pre-commit guard active.
- **Run trees stay local:** full `runs/<run_id>/` trees (match results, traces, manifest, hashes, summary.csv) stay local/git-ignored by default (ESP-1). `run-0001` and `run-0002` remain local/ignored, and `run-0001` remains unmutated from Sprint 00. A sealed run is an evidence artifact, not automatically a tracked one.
- **Reference, never embed:** runs are referenced by `run_id`, content hashes, sanitized aggregate metrics, and local path + status (loop contract §7). Any new aggregate diagnostic derives from coarse fields (`result`, `ending_cause`, `error`, `turns`, `invalid_action_count`, counts/digests) and MUST NOT emit raw decision-trace rows.
- **Policy reversibility:** SP-6 / ESP can be relaxed ONLY by explicit operator approval to track a specific, confirmed-redistributable artifact (`docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` §2 SP-6). Sprint 02 must not assume any run-dir contents become trackable.
- **Review/audit artifacts:** persisted by the orchestrator (not by the pure-review skills) verbatim into git-ignored State Zone: `grimoires/loa/a2a/sprint-N/engineer-feedback.md` (review) and `grimoires/loa/a2a/sprint-N/auditor-sprint-feedback.md` (audit). No COMPLETED marker during review, and not during audit unless the operator explicitly authorizes closeout (loop contract §10).
- **requires-raw-data: cannot-surface** — the actual per-run `result`/`ending_cause` distributions and any run-dir file contents are not surfaced in any planning or tracked artifact.

## 11. Claim ceiling

Anchored to `docs/claim-ceiling.md` and the deferred-lane note's "What this movement is NOT" (lines 37-48). The first comparison sits at ladder **Rung 1** (legal completion / throughput / audit-trail), and Sprint 02 MUST NOT raise it (deferred-lane note line 43; claim-ceiling upgrade is forbidden).

**Sprint 02 MAY make** only RELATIVE, LOCAL claims about the first comparison, each carrying its sample size (n=12) and `regime_id` (`regime-v001`), of the form: "candidate (`run-0002` / scripted-v001) differs from baseline (`run-0001` / random_legal-v001) on metric M by delta under `regime-v001` at n=12." It may state that `win_rate` and `avg_turns` moved while the correctness-gate rates (`illegal_action_rate`, `timeout_rate`, `error_rate`) stayed at the floor, and may EXPLAIN that movement as the mechanical consequence of swapping a stateless `random_legal` policy for a deterministic lowest-index scripted policy against the same random opponent under the same frozen regime. The experiment ledger (`docs/ledger.md`) remains the ONLY ceiling-bearing artifact; per-match records, `summary.csv`, and any new taxonomy/explanation doc carry NO ceiling (`docs/claim-ceiling.md` lines 5-7; loop contract §8).

**Sprint 02 MUST NOT claim:** gameplay strength or quality (a `win_rate` vs a `random_legal` mirror is not evidence of quality — `docs/claim-ceiling.md` lines 22-23); statistical significance; any cross-regime comparison or "uplift" (NFR-5, lines 61-64); leaderboard/competitive quality; per-decision quality, probability reliability, generalization, or byte-identical reproducibility (lines 20-27). The forbidden agent claim words remain absolutely forbidden except as negated/forbidden language: **strong, competitive, optimal, calibrated, complete** (lines 54-59; deferred-lane note line 46).

## 12. Risk register

| # | Risk | Mitigation |
|---|------|------------|
| R1 | Scope creep from explanation into optimization: "explainability of the first delta" or "failure-mode taxonomy" reinterpreted as license to tune `scripted_baseline`, add heuristics, or build a per-decision quality detector for the loss-attribution categories (FM-03/04/06/08) that scores agent decisions. | Bind Sprint 02 to analysis/offline + provenance layers only; forbid edits under `agents/runtime/` or to agent scoring logic; enforce the SDD §1.6 import-direction rule (and the code's stated `sim`/`eval` exclusion); keep FM-03/04/06/08 detector-free and record that any per-decision quality detector is a separate operator decision outside this gate; require every task to cite which of the seven allowed lanes it serves; reject agent-decision-logic touches at review/audit. |
| R2 | Claim-ceiling inflation: the n=12 `win_rate` movement narrated as the scripted policy being "better"/"stronger", silently crossing Rung 1. | Make Rung-1 boundedness an explicit AC; ban the five forbidden words in tracked outputs; require any verdict language to carry n and `regime_id`; keep the ledger as the sole ceiling-bearing artifact; audit re-verifies claim-ceiling text against `docs/claim-ceiling.md`. |
| R3 | Competition-Data / raw-trace leakage: a new aggregate diagnostic or taxonomy detector reads `decision-trace.jsonl` rows and embeds card-adjacent signals or raw trace contents into a tracked doc. | Restrict diagnostics to coarse fields (`result`, `ending_cause`, `error`, `turns`, counts, SHA-256 digests) per `eval/schemas.md` lines 13-15; keep `eval/hygiene_check.py` pre-commit guard active; reference runs by `run_id` + hashes + sanitized metrics only; audit must confirm no raw contents embedded. |
| R4 | Ledger contamination via the `run_eval` default-to-tracked-ledger footgun (O2 / CF-01): a research/test/explanation run mutates `docs/ledger.md` by default because the caller forgot `--no-ledger` (`eval/run_eval.py` lines 300-322). | If Sprint 02 runs any re-runs, mandate `--no-ledger` / `--ledger <tmp>` for all non-deliverable runs; treat CF-01 (S02-4, flip to explicit opt-in) as in-scope hardening; per-`run_id` idempotency is a backstop, not a substitute. |
| R5 | Acting on the metric-rendering defect (CF-03): `delta_report` renders any None→number transition as direction 'down' with delta 'n/a' (`analysis/delta_report.py` lines 156-160), misleading the delta explanation. Note this branch is currently unreached for the numeric `run-0001`/`run-0002` pair (latent path). | Treat CF-03 (S02-3) as in-scope hardening of the currently-unreached branch; add a runnable synthetic-fixture check for the None→number branch before relying on its output; do not let the explanation narrative depend on the unhardened branch; keep the present numeric output unchanged. |
| R6 | Building before the operator opens a build gate: the narrow-planning note misread as authorization to `/implement`, bypassing OA-2 and the loop contract. | Reaffirm loop contract §6: planning artifacts and standing rules never open the gate; Sprint 02 stays in research/plan until the operator issues an explicit build gate; no `/implement` or `/run` until then. |
| R7 | Metrics naming inconsistency as a real defect: metrics-spec uses `avg_match_length` while `delta_report`/`aggregate` use `avg_turns` (`frozen/metrics/metrics-spec-v001.json` vs analysis code). | During comparison-robustness planning, confirm whether this is a documented alias or a latent inconsistency before any detector keys off metric names; if latent, scope a docs-only or one-line reconciliation rather than a behavior change, and verify against SDD §5.4. |

## 13. Operator decisions needed before implementation

1. **OA-1 / OA-2 equivalent:** explicitly approve the Sprint 02 plan and explicitly OPEN a Sprint 02 build gate before any `/implement` or `/run`. The deferred-lane note authorizes planning only; no record opens a build gate (`docs/operator/turntrace-loop-contract.md` §6; `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` §3).
2. **Framing confirmation:** confirm the binding Sprint 02 framing as "Delta Explanation + Failure-Mode Taxonomy" and confirm the agent-optimization lane stays CLOSED (no separate decision opening any "Still closed" item), including that no per-decision agent-quality detector for FM-03/04/06/08 is authorized under the narrow-planning gate.
3. **CF-01 disposition:** decide whether CF-01 (`run_eval` ledger default → explicit opt-in / require explicit `--ledger|--no-ledger`, S02-4) is in Sprint 02 scope as provenance/ledger hardening, or remains deferred.
4. **CF-03 disposition:** decide whether CF-03 (`delta_report` None→number direction / "MOVED n/a" rendering, S02-3) is in scope as `delta_report` hardening, or remains deferred — noting it is a currently-unreached branch for the present numeric runs (the fix is regression-hardening, not a live output change).
5. **CF-02 confirmation:** confirm CF-02 (`byte_identical` / determinism path, S02-5) stays DEFERRED/stretch — unreachable while `seed_controlled=false`; must not be built absent a proven seed-controlled regime.
6. **CF-04 disposition:** decide disposition of CF-04 (`.beads/.br_history/` untracked and not gitignored) — housekeeping; the git status shows `.beads/issues.jsonl` already modified, so confirm whether this is folded in or handled separately.
7. **OA-3 confirmation:** confirm OA-3 still holds for any Sprint 02 runs — local `cg/` Competition-Data lib present and gitignored on the build machine (CC-1).
8. **Artifact tracking:** decide whether the new failure-mode taxonomy / delta-explanation document(s) are tracked sanitized artifacts and confirm no run-dir contents are promoted to tracked status (SP-6 relaxation requires explicit operator approval).

## 14. Recommendation: whether Sprint 02 should proceed

**PROCEED — but only into research/planning (PRD → SDD → sprint-plan), NOT into build, and only after the operator opens an explicit Sprint 02 build gate (OA-2).**

Reasoning:

1. **The binding precondition for narrow planning is satisfied.** The first comparison (`run-0001` → `run-0002`, `regime-v001`, n=12) showed a metric move (`win_rate`, `avg_turns`) for an explainable, agent-only reason, and the operator recorded the standing decision "NARROW PLANNING GATE OPENED. Broad optimization remains closed" (`docs/operator/deferred-lane-gate-after-sprint-01.md` lines 50-59).
2. **The proposed charter maps exactly onto the seven allowed narrow-planning lanes** and is the operator-stated framing (lines 88-94).
3. **There is concrete, well-scoped, non-optimization work ready:** extend the FM-01..FM-09 catalogue into a sanitized taxonomy (S02-1), add Competition-Data-safe aggregate diagnostics over coarse fields (S02-2), harden `delta_report` (CF-03 / S02-3) and `run_eval` ledger provenance (CF-01 / S02-4), plus replay-honesty and strategy-report updates (S02-5/S02-6) — all confined to the analysis/offline and provenance layers, respecting the SDD §1.6 import-direction rule.
4. **Sprint 02 strengthens TurnTrace's ability to EXPLAIN and AUDIT comparisons** — the stated posture — without touching agent strength. The work is bounded by a clear claim ceiling (stay at Rung 1) and a clear forbidden list, with a known closeout path (implement → review → audit → operator acceptance).

The single hard gate is procedural: this note opens no build gate, so the operator must issue OA-2 before implementation begins. Until then, only planning may proceed.
