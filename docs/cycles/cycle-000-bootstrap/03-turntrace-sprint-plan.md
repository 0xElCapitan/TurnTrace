# Sprint Plan: TurnTrace

| Field | Value |
|---|---|
| **Version** | 1.0 |
| **Date** | 2026-06-17 |
| **Author** | Sprint Planner Agent |
| **Status** | Draft for review |
| **Cycle** | `cycle-000-bootstrap` |
| **Artifact** | `grimoires/loa/a2a/cycle-000-bootstrap/03-turntrace-sprint-plan.md` |
| **PRD Reference** | `grimoires/loa/a2a/cycle-000-bootstrap/01-turntrace-prd.md` |
| **SDD Reference** | `grimoires/loa/a2a/cycle-000-bootstrap/02-turntrace-sdd.md` |
| **Operator decisions** | `grimoires/loa/a2a/cycle-000-bootstrap/04-operator-decisions.md` |

> **Scope of this cycle (binding).** `cycle-000-bootstrap` produces **planning artifacts only** —
> PRD → SDD → this sprint plan. This document **plans** the build; it does **not** authorize it. No
> application code is written, no dependencies are added, and no Kaggle/Competition-Data files are
> committed in this cycle (operator hard rules; PRD §11.1, CC-1; SDD scope note). The sprints below
> (Sprint 00, Sprint 01) execute in the **next** cycle, after the operator opens the build gate
> (see §"Recommended Next Operator Gate").
>
> **Grounding.** Tasks cite the PRD (`PR-n` / `NFR-n` / `CC-n` / `G-n`), the SDD (`sdd §N`), or the
> Data Loop Plan (`plan §N`). The 9 Sprint 00 acceptance checks mirror **sdd §7.2** verbatim. Goal
> IDs G-1…G-7 map to the PRD's "G1…G7" (PRD §4) — see Appendix C.

---

## Executive Summary

TurnTrace's build is split into **two sprints** that establish the evidence loop before any gameplay
work begins. The ordering is the product's central discipline: **data first, optimization second,
inside the machine** (PRD §2, §11; plan §7.7).

- **Sprint 00 — "The smallest useful loop."** Stand up the data loop end-to-end: capability probe →
  random-legal agent → one-match runner → sealed immutable run directory → aggregate → exactly one
  ceiling-bounded ledger row. Delivers **PR-1…PR-9** + stubs **PR-10/11/12**. Success is *the loop
  works and is honest*, **regardless of win rate** (PRD §11.2, §15; plan §7.4).
- **Sprint 01 — "The first comparison."** Produce the first run-vs-run delta report (PR-14) under the
  *same* frozen regime, plus the audit-trail replay check (PR-15), a scripted heuristic baseline
  (PR-13), and pre-submission mirror validation (PR-18). The **deferred-lane gate** (RL, self-play,
  deck optimizer, value model, dashboards, tournaments — PR-17) does **not** open until this delta
  report shows a metric moved for an explainable reason (PRD §11.3–§11.4; plan §8).

**Hard rule across both sprints:** **no rule/heuristic tuning until the first delta report exists**
(PRD §11.3; plan §7.7). Sprint 00 ships *only* `random_legal`; the scripted baseline (PR-13) is a
frozen, deterministic priority policy, not a tuned one, and arrives in Sprint 01.

| | Value |
|---|---|
| **Total build sprints** | 2 (Sprint 00, Sprint 01) |
| **Sprint sizing** | Sprint 00 = **LARGE** (10 tasks); Sprint 01 = **MEDIUM** (6 tasks) |
| **Build arc target** | Per plan's 72-hour arc for Sprint 00 (plan §11); both sprints comfortably inside the ~2-month runway to **Final Submission 2026-08-16** (PRD §8.3, CC-9) |
| **Dependencies added this cycle** | None (cycle-000 is planning only) |

> **Dates are intentionally relative.** cycle-000 is planning-only and the build cycle has not been
> opened, so calendar dates for Sprint 00/01 are assigned when the operator opens the build gate.
> The binding *deadline* constraint is unchanged: both sprints must complete with ample margin
> before the **Final Submission Deadline 2026-08-16** (CC-9, PRD §11.5). Sequencing — not calendar —
> is what this plan fixes.

---

## Sprint Overview

| Sprint | Theme | Scope | Key Deliverables (PR IDs) | Dependencies |
|--------|-------|-------|---------------------------|--------------|
| **00** | The smallest useful loop | LARGE (10 tasks) | PR-9, PR-2, PR-1, PR-3, PR-4, PR-5, PR-6, PR-7, PR-8, PR-10/11/12 (stubs) | Build gate open; local `cg/` lib present (gitignored) |
| **01** | The first comparison | MEDIUM (6 tasks) | PR-14, PR-15, PR-13, PR-18 + Sprint-00 E2E goal validation | Sprint 00 complete (sealed `run-0001/` + ledger row) |

---

## Evidence-Storage Policy (binding, both sprints)

> Extends **CC-1/CC-2** (Competition-Data redistribution; Pokémon Elements) and **NFR-2/NFR-4** to all
> *generated* evidence. Binding across Sprint 00 and Sprint 01; mechanically enforced by the Task 00.10
> `.gitignore` entries + build-time pre-commit Competition-Data hygiene check. The governing idea: a
> sealed run is an **evidence** artifact, not automatically a **tracked** artifact — immutability
> (NFR-2) is a filesystem property, not a git property.

- **ESP-1 — Generated runs are local by default.** Full `runs/<run_id>/` trees — `match_results/`,
  `traces/`, `manifest.json`, `hashes.txt`, and the raw inputs behind `summary.csv` — are
  **local / git-ignored by default**. A sealed run directory can exist locally **without ever being
  committed**.
- **ESP-2 — Never commit raw or Competition-Data-bearing artifacts.** Raw traces, match logs,
  simulator outputs, deck files, card IDs, card names, `cg/`, starter files, PDFs, CSVs, and raw deck
  lists **must not be committed** unless explicitly confirmed **redistributable AND operator-approved**
  (CC-1/CC-2). Absent that confirmation, the default is *do not commit*.
- **ESP-3 — Tracked evidence is sanitized only.** What may be tracked in git is limited to: **sanitized
  summaries, ledger rows, claim ceilings, failure-mode notes, planning docs, and other
  operator-approved artifacts.** Anything carrying Pokémon Elements or raw run contents is excluded.
- **ESP-4 — Reference runs, don't embed them.** When a run must be cited in a tracked document,
  reference its **`run_id`, content hashes, sanitized metrics, and the local artifact path + status**
  — never embed raw trace contents or card-level data.
- **ESP-5 — Enforcement.** The Task 00.10 `.gitignore` + pre-commit hygiene check is the mechanical
  control; this policy is the rule it enforces. The same boundary applies to `run-0002` and all later
  runs (Sprint 01 §"Security Considerations").

---

## Sprint 00: The Smallest Useful Loop

**Scope:** LARGE (10 tasks)
**Duration:** ~3 working days (the plan's 72-hour arc; plan §11)
**Dates:** TBD — assigned when the operator opens the build cycle (see Executive Summary note)

### Sprint Goal

Run the random-legal agent over `seed-set-v001` against one fixed opponent under `regime-v001`,
capture per-match records and traces on disk, aggregate them, and seal exactly one immutable
`run-0001/` with a hash stamp and one ceiling-bounded ledger row — **regardless of win rate**.

> From Data Loop Plan §7 (PRD §11.2): "Sprint 00 is about the data loop, not about playing well…
> Win rate is irrelevant this sprint."

### Deliverables

- [ ] **PR-9 — Capability probe** report (`sim/README.md`): each capability marked
  confirmed / unconfirmed / absent with a fallback (run-locally, legal-action enumeration, seed
  control, time budget/timeout detection, match throughput, submission interface). *(sdd §1.4, §5.1)*
- [ ] **PR-2 — `random_legal` runtime agent**: selects uniformly among offered legal options,
  count within `[minCount, maxCount]`; pure function of (observation, RNG), no cross-move state,
  no network. *(sdd §1.4, §5.2)*
- [ ] **PR-1 — `run_match.py`**: plays one match under a fully declared input set; refuses to run if
  any required input is missing. *(sdd §1.4, §5.3)*
- [ ] **PR-3 — `match-summary.json`** per match: all Sprint-00 fields populated; `result` is the
  single outcome source of truth; carries no claim ceiling. *(sdd §3.2)*
- [ ] **PR-4 — `decision-trace.jsonl`** per match (optional per match; loop runs on records alone if
  tracing impossible): observable state only, never leaks opponent hand / own deck order; terminal
  record mandatory when a trace exists. *(sdd §3.3)*
- [ ] **PR-5 — Immutable `run-0001/`**: `manifest.json` (ID authority) + `hashes.txt` + `summary.csv`
  + `notes.md` + `match_results/` + `traces/`; immutability guard is a **hard error**. *(sdd §3.5)*
- [ ] **PR-6 — `frozen/regime-v001`**: the four-component tuple (seed-set + opponent-pool + deck-pool
  + metrics-spec); deck-pool stores **references + hashes only**, never card lists (CC-1/CC-2).
  *(sdd §3.6, §4.5)*
- [ ] **PR-7 — `summary.csv`** aggregate: win/draw/error/timeout rates + game-length stats, per-matchup
  breakdown, computed from the single `result` enum. *(sdd §3.4)*
- [ ] **PR-8 — One `ledger.md` row** for run-0001 with a **mandatory, non-empty `claim_ceiling`**
  (pre-written, trivial, Rung-1: legality/throughput only, no strength claim). *(sdd §3.7)*
- [ ] **PR-10/11/12 — Stub docs**: `failure-modes.md` (seeded FM-01…FM-09, incl. the malformed-
  selection reframe), `claim-ceiling.md` (zero-modeling invariant + distribution-stable posture),
  `strategy-report.md` (eight-section skeleton, placeholders only). *(sdd §3.8)*

### Acceptance Criteria (mirrors sdd §7.2 verbatim — the definition of done)

- [ ] **AC-1.** `run_eval` runs random-legal over `seed-set-v001` vs one opponent under `regime-v001`,
  exits 0.
- [ ] **AC-2.** `match_results/` has exactly one JSON per seed (count == seed-list length).
- [ ] **AC-3.** `traces/` has one sidecar per match; each record's `trace_hash` matches its sidecar
  (**trace-hash join exercised**).
- [ ] **AC-4.** Every record validates against `schemas.md` (capability-uncertain fields accepted
  `null` with the matching capability flag set; NFR-6).
- [ ] **AC-5.** `summary.csv` exists; its `n_matches` == per-match file count.
- [ ] **AC-6.** `hashes.txt` has non-empty `git_rev`, `sim_version`, `seed_list_hash`, `timestamp`.
- [ ] **AC-7.** Exactly one new `ledger.md` row for run-0001, tagged `regime-v001`, with a **non-empty
  `claim_ceiling`**.
- [ ] **AC-8.** `invalid_action_count` + `invalid_action_detectable` populated on every record (count
  may be > 0).
- [ ] **AC-9.** Re-running into `run-0001` **refuses to overwrite** (immutability guard) and validates
  written ids against `manifest.json`.

### Technical Tasks

> Karpathy goal-driven note: every non-trivial task below names its verifiable check (the AC it
> earns). The capability probe runs **first** (OD-4) so the harness is shaped against the *observed*
> surface, never assumed (PRD §13; sdd §8 Phase 1).

- [ ] **Task 00.1 — Capability probe (FIRST).** Run one match through the live `cg/` lib; dump the
  exposed surface; write `sim/README.md` marking each capability confirmed/unconfirmed/absent with a
  fallback; record measured `match_throughput`. Exit 1 (escalate) if one match cannot complete.
  *Verify: probe report exists with every U-1…U-4 capability flagged.* → **[G-1, G-5]**
  *(PR-9; OD-4; sdd §5.3, §5.1 `capabilities()`)*
- [ ] **Task 00.2 — `sim/adapter.py` (the single blast radius).** Wrap `cabt`
  `battle_start`/`battle_select`/`battle_finish`; expose the §5.1 internal port
  (`start_match`/`step`/`finish`/`legal_options`/`observe`/`event_log`/`capabilities`); no caller
  outside `sim/` references a `cabt` symbol; all capability facts returned as flags, defaulting
  conservative (`seed_controlled=false`). *Verify: import-direction check + single-match smoke.*
  → **[G-1, G-5]** *(sdd §1.4, §5.1; plan §3)*
- [ ] **Task 00.3 — `random_legal` agent.** Implement `select(observation) -> selection` =
  `random.sample(range(len(option)), maxCount)` within `[minCount, maxCount]`; no scoring fields, no
  cross-move state, no network (CC-3). *Verify: agent returns a valid selection on every offered
  option set in a smoke match.* → **[G-1]** *(PR-2; sdd §1.4, §5.2)*
- [ ] **Task 00.4 — `eval/canonical_json.py`.** Sorted-key, stable-number, no-incidental-whitespace
  serializer used for `trace_hash`. *Verify: re-serializing a trace twice yields byte-identical
  output; AC-3 join depends on it.* → **[G-2, G-5]** *(sdd §1.4 canonical serializer, §3.3)*
- [ ] **Task 00.5 — `eval/run_match.py` (one match → record + trace).** Refuse to start on any
  missing required input (PR-1); resolve output path up front; drive the adapter; capture per-decision
  trace rows + terminal record; compute `trace_hash`; write `match-summary.json` + `decision-trace.jsonl`.
  Never count an in-match error as a loss (FM-01 guard). *Verify: AC-2, AC-3, AC-8, exit-code smoke
  (0/1/2).* → **[G-1, G-3, G-5]** *(PR-1/3/4; sdd §1.4, §3.2, §3.3, §6.1)*
- [ ] **Task 00.6 — `eval/schemas.md` + hand-written validator.** Plain field lists for
  match-summary / decision-trace / summary.csv / manifest / hashes; tiny stdlib validator that
  accepts `null` on a capability-uncertain field iff its flag says the capability is absent (NFR-6).
  *Verify: AC-4; schema smoke runs with no flags so it cannot be skipped; rejects a mishandled
  `result==error`.* → **[G-2, G-6]** *(sdd §2.2, §3.1, §7.3)*
- [ ] **Task 00.7 — `frozen/regime-v001` bundle.** Author `regimes/regime-v001.json`,
  `seeds/seed-set-v001.json`, `opponents/opponent-pool-v001.json`,
  `decks/deck-pool-v001.json` (**references + content hashes only — no card lists, CC-1/CC-2**),
  `metrics/metrics-spec-v001.json` (minimal: `vs-random` category, worst-case composite verdict,
  capability-aware soft gates). *Verify: regime hashes into the run; AC-1 runs under `regime-v001`.*
  → **[G-3, G-4]** *(PR-6; sdd §3.6, §4.5, §5.4)*
- [ ] **Task 00.8 — `eval/run_eval.py` (N matches → sealed run dir).** Allocate `run_id` + expected
  `match_id` list, freeze into `manifest.json` (ID authority); **immutability guard** (refuse to write
  into a populated run dir — hard error, exit 3); build `hashes.txt` + `notes.md` (`mode = seeded |
  unseeded`). *Verify: AC-1, AC-6, AC-9 (overwrite refused + id check vs manifest).* → **[G-2, G-4]**
  *(PR-5; sdd §1.4, §3.5, §6.1)*
- [ ] **Task 00.9 — `analysis/aggregate.py` → `summary.csv` + one `ledger.md` row.** Roll records up
  by the single `result` enum into the §3.4 columns; append **exactly one** ledger row with a
  pre-written non-empty `claim_ceiling` (Rung-1, no strength claim) and `n`. *Verify: AC-5, AC-7.*
  → **[G-3, G-4, G-6, G-7]** *(PR-7/8; sdd §3.4, §3.7)*
- [ ] **Task 00.10 — Seed stub docs + `.gitignore`/pre-commit hygiene.** Seed `docs/failure-modes.md`
  (FM-01…FM-09 incl. malformed-selection reframe), `docs/claim-ceiling.md` (zero-modeling invariant +
  distribution-stable + audit-trail posture), `docs/strategy-report.md` (eight-section skeleton).
  Add `.gitignore` entries for `cg/`, card data, starter `deck.csv`, raw deck lists; add the
  build-time pre-commit Competition-Data hygiene check. *Verify: stubs exist with required sections;
  hygiene check refuses to stage any gitignored Competition-Data path.* → **[G-6, G-7]** *(PR-10/11/12;
  sdd §3.8, §4.5; CC-1)*

### Dependencies

- **Build gate must be open** — Sprint 00 executes only after the operator authorizes the build cycle
  (cycle-000 is planning-only).
- **Local `cg/` Competition-Data lib present** on the build machine (gitignored; never committed, CC-1).
- **Capability probe (Task 00.1) blocks Tasks 00.2–00.9** — the harness is shaped against the observed
  surface (OD-4).
- No dependency on Sprint 01 (Sprint 00 is the foundation).

### Security Considerations

- **Trust boundaries.** The only external input is the local `cg/` lib + Competition Data. There is
  no network surface, no auth, no secrets, no PII (sdd §1.10). The *compliance* boundary, not infosec,
  is binding.
- **Competition-Data redistribution (CC-1/CC-2 — highest-impact, rules-breach risk).** `cg/`, card
  data, starter `deck.csv`, and raw deck card-lists are gitignored and never committed; `frozen/`
  stores references + hashes only; a build-time pre-commit hygiene check fences accidental commits
  (Task 00.10). This is the load-bearing safety control of the whole sprint.
- **No ingress/egress on the runtime path (CC-3 / NFR-8).** `random_legal` imports nothing networked;
  the runtime/offline directory + import-direction rule (sdd §1.6) keeps the per-move path self-contained.
- **Plain-language framing (CC-8).** No FORGE/Echelon/CORONA in file names, field names, schemas, or
  any competition-facing artifact; "TurnTrace" stays out of submission bundles.

### Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Accidental commit of Competition Data | Med | **High (rules breach)** | `.gitignore` + `frozen/` refs-and-hashes-only + pre-commit hygiene check (Task 00.10); `sim/` imports `cg/` locally (sdd §4.5) |
| Live `cabt` API differs from inspected starter kit | Med | Med | Probe-first (Task 00.1); all sim facts behind `sim/` (Task 00.2) so divergence changes only the adapter (sdd §5.1) |
| Seed uncontrollable → no byte-replay | High | Med | Distribution-stable + audit-trail posture (NFR-3); `mode=unseeded` in notes; event-log RNG trail; determinism smoke skipped if seeds uncontrolled (sdd §7.3) |
| Low local throughput limits N | Unknown | Med | Measured in probe (Task 00.1); shrink N (power, not correctness); RL/self-play stays blocked (sdd §1.9) |
| Time budget undetectable | Med | Low–Med | Measure own decision wall-time vs config budget (`budget_source=assumed`); `timeout=null` + soft gate if none published (sdd §5.4) |
| Runtime/offline coupling creeps in | Med | Med | Directory boundary + import-direction check (Task 00.2/00.5; sdd §1.6) |

### Success Metrics

- All **9 acceptance checks (AC-1…AC-9)** pass — *regardless of win rate* (PRD §15 bounded build success).
- Exactly **1** sealed `run-0001/` directory; the immutability guard demonstrably refuses a second write (AC-9).
- Exactly **1** `ledger.md` row, with a non-empty `claim_ceiling` at Rung 1 (AC-7).
- `match_throughput` is a **measured number**, not an assumption (Task 00.1) — unblocks N-sizing decisions.
- **0** Competition-Data paths committed to git (CC-1 hygiene check green).

---

## Sprint 01 (Final): The First Comparison

**Scope:** MEDIUM (6 tasks)
**Duration:** ~2.5 days
**Dates:** TBD — assigned at build-cycle planning; sequenced strictly after Sprint 00

### Sprint Goal

Produce the first run-vs-run delta report — run-0001 (baseline) vs run-0002 (one deliberate trivial
change) under the **same** `regime-v001` — establishing the comparison artifact that gates all
deferred-lane work, plus the audit-trail replay check, a frozen scripted baseline, and pre-submission
mirror validation.

> No rule tuning and no deferred lane starts until this delta report exists (PRD §11.3; plan §7.7, §8).

### Deliverables

- [ ] **PR-14 — Delta report** (`analysis/delta_report.py`): compares two run dirs on the same
  `regime_id`; emits per-metric deltas + a "why no change" line for every unmoved metric; refuses to
  compare across regimes. *(sdd §1.4, §3.4)*
- [ ] **PR-15 — Replay / reproducibility check** (`analysis/replay_check.py`): re-hash traces for
  **audit-trail equality**; byte-identical replay only if seed control was proven by the probe (NFR-3).
- [ ] **PR-13 — Scripted heuristic baseline** (`agents/runtime/scripted_*.py`): a small, **frozen,
  deterministic** priority policy — the "better than a sensible first script" bar. Not a tuned policy.
- [ ] **PR-18 — Pre-submission mirror validation**: locally play the candidate agent vs a copy of
  itself, confirm a full match completes with no error before submission (mirrors Kaggle's Validation
  Episode). *(PRD §8.3, PR-18)*

### Acceptance Criteria

- [ ] **AC-01.** `delta_report.py` produces per-metric deltas for run-0001 vs run-0002 under the same
  `regime-v001`, with a "why no change" line on each unmoved metric.
- [ ] **AC-02.** `delta_report.py` **refuses** (non-zero exit / explicit error) when the two runs carry
  different `regime_id`s (no cross-regime comparison; NFR-5).
- [ ] **AC-03.** `replay_check.py` recomputes every trace's `trace_hash` and asserts audit-trail
  equality; the determinism path is exercised only if `seed_controlled=true`, else explicitly skipped
  with `mode=unseeded` recorded.
- [ ] **AC-04.** The scripted baseline (PR-13) is deterministic: the same observation yields the same
  selection across two runs (no hidden state).
- [ ] **AC-05.** PR-18 mirror validation reports pass/fail for a candidate-vs-self full match before
  any submission packaging.
- [ ] **AC-06.** A second `ledger.md` row exists for run-0002 with its own non-empty `claim_ceiling`;
  the delta is recorded only via a same-regime, agent-only comparison with a ceiling + `n`.

### Technical Tasks

- [ ] **Task 01.1 — Generate run-0002** with one deliberate *trivial* non-tuning change vs run-0001
  under `regime-v001`; seal it as a second immutable run dir; append its ledger row. *Verify: AC-06.*
  → **[G-3, G-4]** *(PRD §11.3; sdd §8 Phase 2)*
- [ ] **Task 01.2 — `analysis/delta_report.py`** (PR-14): per-metric deltas + "why no change" lines;
  hard-refuse cross-`regime_id` comparisons. *Verify: AC-01, AC-02.* → **[G-3, G-6]** *(sdd §1.4, §3.4)*
- [ ] **Task 01.3 — `analysis/replay_check.py`** (PR-15): re-hash traces (audit-trail equality);
  determinism path gated on `seed_controlled`. *Verify: AC-03.* → **[G-2, G-5]** *(sdd §1.4; NFR-3)*
- [ ] **Task 01.4 — Scripted heuristic baseline** (PR-13): frozen deterministic priority policy in
  `agents/runtime/`; no tuning, no scoring leakage onto the runtime path. *Verify: AC-04.* → **[G-1]**
  *(PR-13; sdd §1.6)*
- [ ] **Task 01.5 — Pre-submission mirror validation** (PR-18): candidate vs copy-of-self full-match
  smoke; reports pass/fail mirroring the hosted Validation Episode. *Verify: AC-05.* → **[G-1, G-7]**
  *(PR-18; PRD §8.3)*
- [ ] **Task 01.E2E — End-to-End Goal Validation** (see dedicated section below). → **[All goals]**

### Task 01.E2E: End-to-End Goal Validation

**Priority:** P0 (Must Complete)
**Goal Contribution:** All goals (G-1 … G-7)

**Description:** Validate that every PRD goal is demonstrably achieved by the complete two-sprint
build, with each claim tied to an immutable on-disk artifact (PRD §15).

| Goal ID | Goal (PRD §4) | Validation Action | Expected Result |
|---------|---------------|-------------------|-----------------|
| G-1 | Run matches when simulator available, fully-declared inputs, sequential, debuggable | Inspect `run-0001/` + `run-0002/`: matches ran via `run_eval`; `run_match` refuses on missing input | Both runs sealed; missing-input refusal demonstrated (Sprint 00 AC-1, PR-1) |
| G-2 | Preserve evidence immutably | Attempt a second write into `run-0001/` | Immutability guard refuses (hard error); no edit to a written run (AC-9) |
| G-3 | Compare agent versions honestly | Run `delta_report.py` on run-0001 vs run-0002, same regime | Per-metric deltas + "why no change"; cross-regime compare refused (AC-01, AC-02) |
| G-4 | Track what was tested + under what conditions | Read `ledger.md` + each `manifest.json`/`hashes.txt` | One ceiling-bounded row per run; every number traces to a frozen regime (AC-07, AC-06) |
| G-5 | Decision traces where simulator permits | Open a `traces/<match_id>.jsonl`; recompute its `trace_hash` | Trace decomposes the match from observable signals; hash matches record (AC-3) |
| G-6 | Bound claims with explicit evidence | Inspect each ledger `claim_ceiling` + `n` | No claim exceeds its N/regime; ceiling non-empty on every row (AC-7) |
| G-7 | Feed a credible Strategy/Hackathon report | Open `docs/strategy-report.md` skeleton; confirm run artifacts slot into its sections | Report sections populate directly from run dirs + ledger (PR-12) |

**Acceptance Criteria:**
- [ ] Each goal validated with documented evidence pointing at a specific artifact path.
- [ ] Integration points verified (records → summary → ledger → delta report flow end-to-end).
- [ ] No goal marked "not achieved" without explicit justification recorded in `notes.md`.

### Dependencies

- **Sprint 00 complete** — requires a sealed `run-0001/`, its ledger row, and a frozen `regime-v001`
  to compare against.
- **`seed_controlled` capability fact** from the Sprint 00 probe — determines whether AC-03's
  determinism path runs or is skipped.

### Security Considerations

- Same CC-1/CC-2 Competition-Data boundary as Sprint 00 — run-0002's `frozen/` references stay
  refs-and-hashes-only; the pre-commit hygiene check remains active.
- **PR-18 (mirror validation) touches the submission flow** but performs **no network call** during
  the match itself (CC-3); packaging (`tar -czvf submission.tar.gz *`, `main.py` at top level + `deck.csv`)
  is an operator action, not a harness action (CC-5; sdd §1.8).

### Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Comparing across regimes (false uplift) | Med | Med | `regime_id` first-class on every row; `delta_report.py` hard-refuses mismatched regimes (AC-02; NFR-5) |
| Premature optimization temptation (Hackathon rewards strength) | Med | Med | Deferred-lane gate stays closed until this delta report shows an explainable move; PR-13 is frozen, not tuned (PRD §11.4) |
| Determinism check unavailable (seeds uncontrolled) | High | Low | Replay degrades to audit-trail equality; determinism path explicitly skipped + `mode=unseeded` recorded (NFR-3) |
| run-0002 change too large to attribute | Low | Med | The change is deliberately *trivial* and non-tuning; one variable only (PRD §11.3) |

### Success Metrics

- **1** delta report comparing run-0001 vs run-0002 on `regime-v001`, with a "why no change" line on
  every unmoved metric (AC-01).
- Cross-regime comparison **refused** in a test (AC-02) — the false-uplift guard is proven, not assumed.
- **2** ledger rows total, each ceiling-bounded (AC-06).
- E2E validation: **7/7** PRD goals each tied to a concrete artifact path (Task 01.E2E).
- **Deferred-lane gate decision recorded** in `ledger.md`/`notes.md`: open the gate only if a metric
  moved for an explainable reason (PRD §11.4).

---

## Risk Register

| ID | Risk | Sprint | Probability | Impact | Mitigation | Owner |
|----|------|--------|-------------|--------|------------|-------|
| R1 | Accidental commit of Competition Data | 00–01 | Med | **High (rules breach)** | `.gitignore` + refs-and-hashes-only `frozen/` + pre-commit hygiene check (Task 00.10) | Agent engineer |
| R2 | Live `cabt` API differs from starter kit | 00 | Med | Med | Probe-first (Task 00.1); single blast radius in `sim/` (Task 00.2) | Agent engineer |
| R3 | Seed uncontrollable → no byte-replay | 00–01 | High | Med | Distribution-stable + audit-trail (NFR-3); `mode=unseeded`; determinism path skipped if needed | Agent engineer |
| R4 | Low local throughput limits N | 00 | Unknown | Med | Measure in probe; shrink N; RL/self-play blocked until a number exists | Operator |
| R5 | Time budget undetectable | 00 | Med | Low–Med | Measure own wall-time vs config budget; `timeout=null` + soft gate | Agent engineer |
| R6 | Comparing across regimes (false uplift) | 01 | Med | Med | `regime_id` first-class; delta report refuses mismatched regimes | Agent engineer |
| R7 | Premature optimization before the delta report | 01 | Med | Med | Deferred-lane gate + data→optimize ordering binding regardless of deadline | Operator |
| R8 | `cabt` ≠ official Pokémon TCG rules | 00–01 | Med | Med | Analysis/heuristics follow cabt behavior; rules-differences page is build-phase analyst reading | Analyst |
| R9 | Deadline pressure erodes evidence-first ordering | 00–01 | Med | Med | ~2-month runway; ordering/claim-ceilings/checklist stay binding (PRD §11.5) | Operator |

---

## Success Metrics Summary

| Metric | Target | Measurement Method | Sprint |
|--------|--------|--------------------|--------|
| Sprint 00 acceptance checks pass | 9/9 (AC-1…AC-9) | Run smokes; inspect `run-0001/` | 00 |
| Sealed immutable run dirs | 1 (Sprint 00), 2 (Sprint 01) | Filesystem inspection; overwrite refusal | 00–01 |
| Ceiling-bounded ledger rows | 1 → 2 | `ledger.md`; every row has non-empty `claim_ceiling` + n | 00–01 |
| Measured match throughput | A real number | Probe wall-clock over N matches (Task 00.1) | 00 |
| Competition-Data paths committed | 0 | Pre-commit hygiene check + `git status` | 00–01 |
| First delta report | 1, same-regime, with "why no change" lines | `delta_report.py` output (AC-01) | 01 |
| Cross-regime comparison guard | Refused in test | `delta_report.py` exit on mismatched regime (AC-02) | 01 |
| PRD goals validated E2E | 7/7 tied to artifacts | Task 01.E2E table | 01 |

---

## Dependencies Map

```
[Operator: open build cycle gate]
            │
            ▼
Sprint 00 ───────────────────────────────▶ Sprint 01
   │  The smallest useful loop                │  The first comparison
   │  (probe → loop → sealed run-0001)         │  (run-0002 → delta report → E2E)
   │                                           │
   └─ Task 00.1 (probe) blocks 00.2–00.9       └─ requires run-0001 + regime-v001
                                                  └─ [Deferred-lane gate: opens only
                                                      after delta shows explainable move]
```

---

## Appendix

### A. PRD Functional-Requirement Mapping

| PRD FR | Capability | Priority | Sprint | Status |
|--------|------------|----------|--------|--------|
| PR-1 | Local match runner | P0 | 00 | Planned |
| PR-2 | Random-legal baseline agent | P0 | 00 | Planned |
| PR-3 | Per-match record | P0 | 00 | Planned |
| PR-4 | Decision trace | P0 | 00 | Planned |
| PR-5 | Immutable run directory | P0 | 00 | Planned |
| PR-6 | Frozen regime | P0 | 00 | Planned |
| PR-7 | Run aggregation | P0 | 00 | Planned |
| PR-8 | Experiment ledger | P0 | 00 | Planned |
| PR-9 | Capability probe | P0 | 00 | Planned (FIRST task) |
| PR-10 | Failure-mode registry | P0 (stub) | 00 | Planned (seeded) |
| PR-11 | Claim-ceiling document | P0 (stub) | 00 | Planned (seeded) |
| PR-12 | Strategy-report skeleton | P0 (stub) | 00 | Planned (seeded) |
| PR-13 | Scripted heuristic baseline | P1 | 01 | Planned |
| PR-14 | Delta report | P1 | 01 | Planned |
| PR-15 | Replay / reproducibility check | P1 | 01 | Planned |
| PR-18 | Pre-submission mirror validation | P1 | 01 | Planned |
| PR-16 | Two-direction ablation ledger | P2 | Deferred | Not in cycle |
| PR-17 | Scoring agent / search / RL / dashboards / etc. | Deferred lane | Gated | Not until delta-report gate opens |

### B. SDD Component Mapping

| SDD Component | PR | Sprint | Status |
|---------------|----|--------|--------|
| `sim/adapter.py` (blast radius) | — | 00 | Planned (Task 00.2) |
| `sim/README.md` (capability findings) | PR-9 | 00 | Planned (Task 00.1) |
| `agents/runtime/random_legal.py` | PR-2 | 00 | Planned (Task 00.3) |
| `eval/canonical_json.py` | — | 00 | Planned (Task 00.4) |
| `eval/run_match.py` | PR-1/3/4 | 00 | Planned (Task 00.5) |
| `eval/schemas.md` + validator | — | 00 | Planned (Task 00.6) |
| `frozen/regime-v001` bundle | PR-6 | 00 | Planned (Task 00.7) |
| `eval/run_eval.py` | PR-5/7 | 00 | Planned (Task 00.8) |
| `analysis/aggregate.py` + `ledger.md` | PR-7/8 | 00 | Planned (Task 00.9) |
| Stub docs + `.gitignore`/hygiene | PR-10/11/12 | 00 | Planned (Task 00.10) |
| `analysis/delta_report.py` | PR-14 | 01 | Planned (Task 01.2) |
| `analysis/replay_check.py` | PR-15 | 01 | Planned (Task 01.3) |
| `agents/runtime/scripted_*.py` | PR-13 | 01 | Planned (Task 01.4) |
| Mirror validation | PR-18 | 01 | Planned (Task 01.5) |

### C. PRD Goal Mapping

> PRD §4 names goals "G1…G7"; mapped here to the template's `G-1…G-7`.

| Goal ID | Goal Description (PRD §4) | Contributing Tasks | Validation Task |
|---------|--------------------------|--------------------|-----------------|
| G-1 | Run matches when simulator available | 00.1, 00.2, 00.3, 00.5; 01.4, 01.5 | 01.E2E |
| G-2 | Preserve evidence immutably | 00.4, 00.6, 00.8; 01.3 | 01.E2E |
| G-3 | Compare agent versions honestly | 00.5, 00.7, 00.9; 01.1, 01.2 | 01.E2E |
| G-4 | Track what was tested + conditions | 00.7, 00.8, 00.9; 01.1 | 01.E2E |
| G-5 | Decision traces where simulator permits | 00.1, 00.2, 00.4, 00.5; 01.3 | 01.E2E |
| G-6 | Bound claims with explicit evidence | 00.6, 00.9, 00.10; 01.2 | 01.E2E |
| G-7 | Feed a credible Strategy/Hackathon report | 00.9, 00.10; 01.5 | 01.E2E |

**Goal Coverage Check:**
- [x] All 7 PRD goals have at least one contributing task.
- [x] All goals have a validation step in the final sprint (Task 01.E2E).
- [x] No orphan tasks — every task in §"Technical Tasks" carries a `→ [G-n]` annotation.

**Per-Sprint Goal Contribution:**

- **Sprint 00:** G-1 (foundation: run matches), G-2 (immutability + canonical hashing), G-3 (partial:
  single-version records + regime), G-4 (ledger + manifest + hashes), G-5 (traces), G-6 (claim
  ceiling + validator), G-7 (report skeleton).
- **Sprint 01:** G-3 (complete: cross-version delta), G-5 (replay), G-1 (scripted baseline + mirror
  validation), then E2E validation of all seven goals.

### D. Build Posture Reminders (binding regardless of deadline)

- **Data first, optimization second.** No rule/heuristic tuning until the first delta report exists
  (PRD §11.3; plan §7.7).
- **Capability probe is the first build task** (OD-4, confirmed in this plan).
- **Stdlib only** in Sprint 00 — no third-party dependencies (NFR-7; PRD §14).
- **Immutability is a hard error**, never a prompt (NFR-2).
- **The ledger is the only ceiling-bearing artifact** — records and summaries carry no ceiling (PRD §9).
- **Never compare across regimes** (NFR-5).
- **Competition Data never enters git** (CC-1) — the single highest-impact risk.
- **Generated runs stay local; only sanitized evidence is tracked.** Full `runs/<run_id>/` trees and
  any raw/Competition-Data artifacts are git-ignored by default; tracked evidence is limited to
  sanitized summaries, ledger rows, claim ceilings, failure-mode notes, and planning/operator-approved
  docs (see §"Evidence-Storage Policy"; CC-1/CC-2, NFR-2/NFR-4).

---

*Generated by Sprint Planner Agent. cycle-000-bootstrap is planning-only: this plan defines what the
build does and proves; it does not authorize execution. The next gate is operator approval to open
the build cycle (Sprint 00). No application code, dependencies, or Kaggle/Competition-Data files were
created by this artifact.*
