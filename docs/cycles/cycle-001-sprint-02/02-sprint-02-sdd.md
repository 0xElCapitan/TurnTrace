# Cycle-001 / Sprint 02 SDD — Delta Explanation + Failure-Mode Taxonomy

> Planning artifact (SDD). Status: **DRAFT — research/planning only.** This document opens **NO build gate**.
> Implementation requires a separate, explicit operator build-gate action (OA-2 equivalent) per `docs/operator/turntrace-loop-contract.md` §6.
> Binding governance: `docs/operator/deferred-lane-gate-after-sprint-01.md` — **"NARROW PLANNING GATE OPENED. Broad optimization remains closed."**
> Binding input: `docs/cycles/cycle-001-sprint-02/01-sprint-02-prd.md` (the accepted Sprint 02 PRD). Where this SDD disagrees with the PRD, it is flagged inline as an **[SDD design question]**, never an implementation decision.

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-001 / Sprint 02 |
| **Working title** | Delta Explanation + Failure-Mode Taxonomy |
| **Type** | Software Design Document (planning artifact, not a build artifact) |
| **Status** | DRAFT — awaiting operator acceptance; next Golden Path step is Sprint Plan, not implementation |
| **Date** | 2026-06-18 |
| **Base commit** | `9c3d34e` — *docs: add TurnTrace Sprint 02 PRD* |
| **Posture** | EXPLAIN / AUDIT only — not an agent-improvement sprint |
| **Claim ceiling** | Rung 1 (unchanged; not raised) |

---

## 1. Design summary

Sprint 02 makes TurnTrace's first same-regime comparison (`run-0001` vs `run-0002`, `regime-v001`, n=12) **explainable** and makes future comparisons **auditable**, without touching the runtime agent. Six requirements (PR-1..PR-6) all land in the analysis/offline and provenance/docs layers:

- **PR-1 (docs):** a sanitized failure-mode taxonomy v001 — a category model with computable-now vs deferred status, gating capability flags, and an inline boundary forbidding per-decision quality detectors.
- **PR-2 (`analysis/`):** an aggregate failure-mode report over coarse match-summary fields from a local (git-ignored) run dir, emitting counts per `result`/`ending_cause` only — never raw trace rows.
- **PR-3 (`analysis/`):** harden `delta_report.py` for `None↔number` rendering and add a "why moved" line per MOVED metric, leaving the present numeric output byte-unchanged.
- **PR-4 (`eval/`):** close the ledger-contamination footgun (CF-01) so a default/non-deliverable `run_eval` invocation cannot append to `docs/ledger.md`.
- **PR-5 (`analysis/`, stretch):** mark/test the `replay_check.byte_identical()` dead path so byte-identical replay is never faked while `seed_controlled=false`.
- **PR-6 (docs):** update `docs/strategy-report.md` with a PERMITS/FORBIDS framing and per-sentence artifact traceability.

The design preserves every posture invariant in §2. **This SDD authorizes no code.** PR-2..PR-5 are App-Zone code and require an opened build gate (OA-2) before any patch; PR-1 and PR-6 are docs that open no gate but are still produced under the planning posture and only written through `/implement` once a gate is open.

### Resolved-during-SDD findings (binding for the Sprint Plan)

| Item | Resolution (this SDD) | Evidence |
|---|---|---|
| **OQ-1** import-direction: lint or convention? | **Executable lint.** `tests/test_import_direction.py` already enforces zone import rules via AST (exit 0/1). No prerequisite work needed; PR-2 inherits it. | `tests/test_import_direction.py:1-93` |
| **OQ-2** taxonomy location | **Recommend a sibling file** `docs/failure-mode-taxonomy-v001.md`, cross-linked from `docs/failure-modes.md`. See §6 (PR-1). | `docs/failure-modes.md:1-23` |
| **OQ-3** PR-4 CLI shape | **Recommend Option C** (`--ledger <path>` OR `--deliverable`; bare invocation writes no ledger). See §9 (PR-4). | `eval/run_eval.py:300-322` |
| **OQ-4** `run_eval` callers relying on deliverable-by-default | **None in tracked evidence.** Callers: `tests/test_smokes.py` (all pass `ledger_path=<tmp>` or `write_ledger=False`), the `run_eval.main` CLI, and the internal `aggregate.aggregate_and_ledger`. `analysis/e2e_validate.py` references `run_eval` only in a comment. See §9 + §16 (OQ-4). | `tests/test_smokes.py:102-273`, `eval/run_eval.py:300-338`, `analysis/e2e_validate.py:72` |
| **OQ-5** aggregate report location | **Recommend a new module** `analysis/failure_report.py`, not an extension of `analysis/aggregate.py`. See §10 (PR-2). | `analysis/aggregate.py:29-33` |

---

## 2. Architecture boundaries (posture — binding)

This SDD states and preserves, as design invariants:

1. **Analysis/offline code may read local ignored run artifacts read-only.** `analysis/` modules open `runs/<run_id>/...` files for read only; they create/mutate nothing under `runs/` (`analysis/aggregate.py:56-89` is the existing read-only pattern).
2. **Analysis/offline code must not import `cabt`** (`cg`) directly. Enforced by `tests/test_import_direction.py` (`analysis` allowed-set is intra-zone only; `cg→cabt` is forbidden for `analysis`).
3. **Analysis/offline code must not import `agents/runtime`** (nor `sim/`, nor `eval/`). Enforced by the same lint: `ALLOWED["analysis"] = set()` → `analysis` may import only `analysis`.
4. **Runtime agent code must not import analysis/eval/sim or any slow/offline code.** Enforced by the lint: `ALLOWED["runtime"] = set()`. No Sprint 02 requirement touches `agents/runtime/`.
5. **No changes to runtime agent playing behavior.** No `agents/runtime/*.py` edits in any PR. (NG1.)
6. **No edits to frozen / `regime-v001` components.** PR-3's `avg_match_length`↔`avg_turns` reconciliation is an in-code/in-report alias note only; `frozen/metrics/metrics-spec-v001.json` is not edited (a frozen change is a new regime — `docs/claim-ceiling.md:29-35`). (NG5.)
7. **No new run dirs generated by this planning step.** This SDD generates nothing; PR validation runs read-only against existing local `run-0001`/`run-0002` and against synthetic tempdir fixtures. `run-0001` and `run-0002` remain unmutated.
8. **No Competition Data in tracked artifacts.** All tracked outputs carry only `run_id`, hashes, sanitized metrics, claim ceilings, and aggregate categories — never raw traces, card IDs/names, deck lists, or simulator logs. (§13.)

**Import-direction coverage check (OQ-1 resolution).** The existing lint covers invariants 2–4 for any new or edited file under `agents/runtime/`, `sim/`, `eval/`, `analysis/` because it globs `*.py` per zone at run time (`tests/test_import_direction.py:40-79`). A new `analysis/failure_report.py` (PR-2) is therefore automatically covered. **Gap to close in-sprint:** the lint scans only the four zone directories' top-level `*.py`; it does not assert that a new module was added to the scan, and it does not lint `tests/`. Sprint 02 adds, as part of PR-2's acceptance, an assertion in `tests/test_smokes.py` (or `test_import_direction.py`) that `analysis/failure_report.py` is present in the scanned set and reports zero violations, so a new analysis module cannot silently escape the rule.

---

## 3. Module / file plan

| PR | Zone | Action | File(s) | Notes |
|---|---|---|---|---|
| PR-1 | docs (State/tracked) | **create** | `docs/failure-mode-taxonomy-v001.md` | sibling; cross-linked from `docs/failure-modes.md` (one-line pointer added) |
| PR-1 | docs | **edit (1 line)** | `docs/failure-modes.md` | add "See taxonomy v001: …" pointer near the header |
| PR-2 | App (`analysis/`) | **create** | `analysis/failure_report.py` | new module; stdlib only; intra-zone import of `aggregate` allowed |
| PR-2 | tests | **create / edit** | `tests/test_smokes.py` (new test class) | synthetic-fixture tests; no-raw-row assertion; lint-coverage assertion |
| PR-3 | App (`analysis/`) | **edit** | `analysis/delta_report.py` | `_delta`/`moved`/`render` None↔number branch + why-moved lines; alias note in docstring |
| PR-3 | tests | **edit** | `tests/test_smokes.py` (`DeltaReportSmoke`) | None↔number fixtures; why-moved coverage; numeric-output-unchanged guard |
| PR-4 | App (`eval/`) | **edit** | `eval/run_eval.py` | deliverable-intent gating (Option C); CLI flags; docstring update |
| PR-4 | tests | **edit** | `tests/test_smokes.py` (`NoLedgerGuardSmoke` + new) | default-no-write; explicit-deliverable-writes; idempotency |
| PR-5 (stretch) | App (`analysis/`) | **edit** | `analysis/replay_check.py` | `loa:shortcut` marker on `byte_identical`; no behavior change |
| PR-5 (stretch) | tests | **edit** | `tests/test_smokes.py` (`ReplayCheckSmoke`) | already covers skipped/unseeded; add an explicit "never 'passed' under unseeded" pin |
| PR-6 | docs (State/tracked) | **edit** | `docs/strategy-report.md` | sections 1, 4, 6, 7 + PERMITS/FORBIDS; section 5 stays DEFERRED |

No files outside this table are touched. No `.claude/`, no `frozen/`, no `agents/runtime/`, no `runs/`, no `.beads/`, no `grimoires/`.

---

## 4. Data contracts / schemas

### 4.1 Taxonomy v001 category model (PR-1)

A category is a YAML/markdown entry with these fields (extends the existing template at `docs/failure-modes.md:13-23` with explicit status/capability machinery):

| Field | Type | Required | Notes |
|---|---|---|---|
| `fm_id` | string (`FM-NN`) | yes | reuse existing FM-01..FM-09 ids |
| `name` | string | yes | short coarse-outcome/loss name |
| `axis` | enum `outcome` \| `loss-attribution` | yes | `outcome` = computable from `result`/`ending_cause`; `loss-attribution` = per-decision quality (name-only) |
| `compute_status` | enum `computable-now` \| `deferred` | yes | drives whether a detector may exist |
| `gating_capability` | enum `seed_controlled` \| `invalid_action_detectable` \| `timeout_detectable` \| `none` | yes | the flag from `sim/capabilities.json` that gates computability |
| `capability_value` | bool | yes | mirrors the probed flag value (e.g. `invalid_action_detectable=true`) |
| `signature` | string | yes | field-name reference only (`result==error`, `ending_cause=='deck-out'`); **never** row contents |
| `evidence_ref` | string \| null | yes | `run_id`+`match_id`+`decision_index` reference string only |
| `detector` | enum `present` \| `none-yet` \| `forbidden` | yes | FM-03/04/06/08 → `forbidden` |
| `status` | enum `open` \| `mitigated` \| `watched` \| `wont-fix` | yes | existing enum (`docs/failure-modes.md:15`) |

**Detector enum `forbidden` semantics (the binding boundary).** For `fm_id ∈ {FM-03, FM-04, FM-06, FM-08}`, `detector: forbidden` and `axis: loss-attribution`. The artifact states inline: *"Building any per-decision quality detector/scorer for this category is NOT covered by the narrow-planning gate and is a separate operator decision."* This makes NG3 mechanical in the doc itself.

### 4.2 Aggregate report input/output contract (PR-2)

**Input** — a local run-dir path. Reads **only** `runs/<run_id>/match_results/<match_id>.json` and `runs/<run_id>/manifest.json`. Allowed fields (all sanitized per `eval/schemas.md:17-52`):

`result`, `ending_cause`, `error` (presence-flag only, never the string body), `invalid_action_count`, `turns`, `total_decisions`, `trace_present`, plus `run_id`/`regime_id` and `n` (count). **Forbidden reads:** `traces/*.jsonl` row contents, `private_state_summary`, `legal_actions_sample`, `selected_action`, card-id digests, deck lists.

**Output** — markdown to stdout (default), or JSON via `--json`. Schema:

```
regime_id, run_id, n
result_counts:        { win: int, loss: int, draw: int, error: int }
ending_cause_counts:  { "prize-out": int, "deck-out": int, "no-active": int, "card-effect": int, "error": int, "<unmapped>": int }
error_present_count:  int            # count of records with error populated (no strings)
invalid_action_total: int           # sum of invalid_action_count where detectable
fm_links:             [ { fm_id, signature, evidence_ref } ]   # reference strings only
claim_ceiling_footer: string        # Rung-1 footer, no strength claim
```

Optional sanitized local output file is **off by default**; if `--out <path>` is given it writes there. **[SDD design question — defer to operator OD-8/§8]:** any such file must be local/git-ignored (it is a run-derived artifact under ESP-1) unless the operator explicitly approves tracking it. Default = no file, stdout only.

### 4.3 No schema changes elsewhere

PR-3, PR-4, PR-5 introduce no new persisted schema. PR-4 changes only `run_eval`'s CLI surface and the in-process `write_ledger` decision; `match-summary.json`, `manifest.json`, `hashes.txt`, and the ledger row columns (`analysis/aggregate.py:35-40`) are unchanged.

---

## 5. Per-requirement technical design

### 5.1 PR-1 — Failure-mode taxonomy v001 (Core, docs)

**Recommendation (OQ-2): create a sibling file `docs/failure-mode-taxonomy-v001.md`; do not rewrite `docs/failure-modes.md` in place.**

Justification:
- `docs/failure-modes.md` is declared an **append-only human registry** ("New modes are appended; status updated in place" — `docs/failure-modes.md:5-6`). A machine-aligned v001 taxonomy with the §4.1 field model is a different artifact shape (versioned schema vs append-only log); co-locating them would either bloat the registry or force a structural rewrite that the append-only rule discourages.
- A versioned filename (`-v001`) matches the regime/spec versioning convention used across the repo (`regime-v001`, `metrics-spec-v001`) and makes a future `v002` an additive file, not an edit — consistent with the "a change is a new version, never an edit" discipline (`docs/claim-ceiling.md:29-35`).
- The registry stays the canonical narrative catalogue; the taxonomy file is the sanitized, status-bearing schema. One-line cross-link from the registry header avoids drift.

**Content.** One §4.1 entry per FM-01..FM-09, reusing the existing computability findings (`docs/failure-modes.md:25-101`): FM-01 `computable-now` (`invalid_action_detectable=true`, detector `present`); FM-07 `computable-now` (`ending_cause` distribution + `avg_turns`, detector `none-yet`→`present` once PR-2 lands); FM-02 `deferred` (`timeout_detectable=false`); FM-03/04/06/08 `deferred`, `axis: loss-attribution`, `detector: forbidden`; FM-05/09 `deferred`, `detector: none-yet`.

**Sanitization constraints.** Signatures cite field names only; examples cite `run_id`+`match_id`+`decision_index` reference strings; no `result`/`ending_cause` distribution *values* are pasted (those live in ignored run dirs — `requires-raw-data: cannot-surface`). Claim-ceiling language: Rung 1, no forbidden words.

**Validation.** `eval/hygiene_check.py --paths docs/failure-mode-taxonomy-v001.md docs/failure-modes.md`; forbidden-word grep; cross-check every `gating_capability` value against `sim/capabilities.json`; assert FM-03/04/06/08 carry `detector: forbidden` + the inline boundary note; assert every `status` is in the allowed enum.

### 5.2 PR-2 — Aggregate failure-mode report (Core, `analysis/`)

**Recommendation (OQ-5): new module `analysis/failure_report.py`; do not extend `analysis/aggregate.py`.**

Justification:
- `aggregate.py` has a single, well-bounded responsibility (rollup → `summary.csv` + one ledger row) and is a **ledger-writing** module imported by `run_eval` and `delta_report` (`eval/run_eval.py:58`, `analysis/delta_report.py:35`). The aggregate failure report writes **no** ledger and emits a different output shape; folding it in would entangle a read-only diagnostic with the ceiling-bearing ledger path and widen `aggregate.py`'s blast radius.
- A separate module keeps PR-2's no-ledger, stdout-first contract obviously distinct from the ledger writer — easier to audit for the "emits categories only, never a ledger row, never a raw row" property.
- Import-direction stays clean either way; a new `analysis/` file is auto-covered by the lint (§2).

**Design.** `failure_report.py` exposes `aggregate_failures(run_dir: Path) -> dict` (pure read) and `render(rep: dict) -> str` / `render_json(rep) -> str`, plus `main(argv)`. It MAY `import aggregate` intra-zone to reuse `aggregate_run` for `n`/ids only — but reads `result`/`ending_cause` itself directly from `match_results/*.json` so it never depends on the ledger path. It MUST NOT touch `traces/`.

**Missing fields / empty runs.** If `match_results/` is empty → raise `ValueError` (exit 1), mirroring `aggregate.aggregate_run` (`analysis/aggregate.py:62-63`). If a record lacks `ending_cause` → bucket as `"<unmapped>"` and report the count (undetectable reported, never silently dropped). If `invalid_action_detectable=false` on a record → exclude from `invalid_action_total` and note the exclusion.

**CLI.** `python analysis/failure_report.py runs/run-0002 [--json] [--out <local-path>]`. Exit: `0` report produced · `1` input failure. Carries the claim-ceiling footer (pattern from `analysis/delta_report.py:166-170`).

**Import / runtime constraints.** stdlib only (NFR-7); `analysis/` zone only; no `cabt`/`sim`/`eval`/`agents/runtime`. The intra-zone `import aggregate` is the only cross-file import, mirroring `delta_report.py:35`.

### 5.3 PR-3 — `delta_report` hardening (Core, `analysis/`)

**Confirmed defect** (`analysis/delta_report.py`):
- `_delta(a,b)` returns `None` when either side is non-numeric (L73-78).
- `moved = (d is not None and d != 0) or (va != vb and d is None)` (L109) — fires `moved=True` on a `None↔number` transition with `delta=None`.
- In `render`, `direction = "up" if (m["delta"] or 0) > 0 else "down"` (L156) → `(None or 0) > 0` is `False` → a `None→number` transition is **always** rendered `down n/a`, regardless of the numeric value.
- No "why moved" line exists; only unmoved metrics get `WHY_NO_CHANGE` text (L145-151).

**Design.**
1. **Status taxonomy.** In `compare`, classify each metric into one of: `unchanged`, `moved` (both numeric, `d != 0`), `appeared` (`a is None`, `b` numeric), `disappeared` (`a` numeric, `b is None`). Add a `change_kind` field to each metric dict alongside `moved`.
2. **Honest rendering.** In `render`, branch on `change_kind`:
   - `moved` → existing `delta` text + new why-moved line.
   - `appeared` → `status="APPEARED"`, text `"n/a -> <b>"`, no direction; why line names the None→value transition.
   - `disappeared` → `status="DISAPPEARED"`, text `"<a> -> n/a"`, no direction.
   - Direction (`up`/`down`) is computed **only** when both sides are numeric — guard `isinstance(m["delta"], (int,float))` before the `> 0` test, eliminating the `(None or 0)` footgun.
3. **Why-moved lines.** Add a `WHY_MOVED` companion to `WHY_NO_CHANGE` (or a generic bounded sentence) so every MOVED/APPEARED/DISAPPEARED metric carries an explanation, symmetric with the existing unmoved coverage. Each line is bounded by the ledger ceiling and asserts no strength claim.
4. **`avg_match_length`↔`avg_turns` alias note.** The metrics-spec lists `avg_match_length` (`frozen/metrics/metrics-spec-v001.json` `"metrics"` array) while the code compares `avg_turns` (`analysis/delta_report.py:42`). Document the alias in the module docstring and (optionally) a one-line report footnote. **No `frozen/` edit** — already noted in code comment `avg_match_length=avg_turns` at L39; promote to an explicit docstring alias note.

**Preservation guarantees (must hold):**
- `COMPARE_METRICS` unchanged (5 metrics, `analysis/delta_report.py:41-43`).
- `avg_wall_clock_ms` stays excluded from comparison (reported separately, L162-164).
- Cross-regime `CrossRegimeRefusal` → exit 2 unchanged (L90-96, L186-188).
- **Present numeric output unchanged.** For `run-0001` vs `run-0002` all five metrics are numeric on both sides → only the `moved`/`unchanged` branches execute; the new `appeared`/`disappeared` branches are unreached. The added why-moved line is *new output* on the moved branch — **[SDD design question — see §16 DQ-1]:** the PRD AC-3 says "leaves the present numeric output unchanged," but adding a why-moved line for `win_rate`/`avg_turns` (which moved) necessarily adds lines to the live report. Recommended reading: "unchanged" means the **table rows and delta values** are unchanged; the additive why-moved prose is the intended new behavior (symmetric with existing why-no-change prose). The Sprint Plan/operator should confirm this reading; if strict byte-identity of the full report is required, gate the why-moved lines behind a flag or restrict them to the appeared/disappeared kinds.

**Validation.** Synthetic-stats fixtures (no Competition Data): `None→number` asserts `change_kind=="appeared"`, status not `down`, why-line present; `number→None` asserts `disappeared`; both-numeric-moved asserts a why-moved line; all-unmoved asserts existing why-no-change lines intact; run against local `run-0001`/`run-0002` and assert the **delta table values** are unchanged; cross-regime fixture asserts exit 2; forbidden-word grep.

### 5.4 PR-4 — Ledger contamination hardening / CF-01 (Core *[assumption: OD-2]*, `eval/`)

**Confirmed footgun.** `run_eval(..., write_ledger=True)` defaults True (`eval/run_eval.py:93`); `ledger_path` defaults to `docs/ledger.md` (L103); `main` wires `write_ledger = not args.no_ledger` (L321) → a bare `python eval/run_eval.py` appends to the tracked ledger. Opt-OUT design.

**Option comparison:**

| Option | Behavior | Pros | Cons |
|---|---|---|---|
| **A** — require explicit `--ledger <path>` for all ledger writes | No `--ledger` → no ledger write; `docs/ledger.md` only when explicitly named | Simplest mental model; the tracked path is never a default | Forces deliverable runs to always type the full path; easy to point at the wrong file |
| **B** — add `--deliverable` to allow default `docs/ledger.md` write | `--deliverable` → write `docs/ledger.md`; otherwise no write | One explicit intent flag; default stays `docs/ledger.md` when intent is declared | Two ways to mean "write" (`--deliverable` and `--ledger`) only if both kept; alone, can't redirect to a tmp ledger |
| **C** — require `--ledger <path>` OR `--deliverable`; bare invocation writes no ledger | Bare → no write; `--deliverable` → `docs/ledger.md`; `--ledger <p>` → `<p>` | Fail-safe default (no write); supports both "the real deliverable" and "a redirected tmp ledger"; matches existing test patterns that already pass `ledger_path=<tmp>` | Slightly larger CLI surface |

**Recommendation: Option C.** It is fail-safe (the dangerous tracked-ledger write is never a default), preserves the existing `ledger_path` redirection that all current tests rely on (`tests/test_smokes.py:110,257,269`), and gives deliverable runs a short, unambiguous `--deliverable`. Option A loses the ergonomic deliverable path; Option B can't redirect to a tmp ledger without re-adding `--ledger`, which is just Option C.

**Concrete shape.**
- `run_eval(...)` signature: change `write_ledger: bool = True` → `write_ledger: bool = False`. Add no new function params — `ledger_path` already distinguishes "where." Internally: write a ledger row iff `write_ledger is True` (i.e., caller declared deliverable intent) **and** `ledger_path` resolves.
- `main()`: replace `--no-ledger` semantics. Add `--deliverable` (action=store_true) and keep `--ledger <path>`. Compute: `write_ledger = bool(args.deliverable or args.ledger)`; `ledger_path = Path(args.ledger) if args.ledger else (REPO_ROOT/"docs"/"ledger.md")` (only consulted when `write_ledger`). Bare invocation → `write_ledger=False`.
- **[SDD design question — DQ-2/§16]:** removing `--no-ledger` is a CLI break. Recommend keeping `--no-ledger` as a deprecated no-op alias (it already means "don't write," which is now the default) to avoid breaking any unseen wrapper, with a one-line deprecation note. The operator confirms whether to drop it outright.

**Preservation guarantees:** `summary.csv` always written (the `else` branch at `eval/run_eval.py:274-280` becomes the default path); append-only ledger (`append_ledger_row` idempotency + non-empty `claim_ceiling`, `analysis/aggregate.py:125-140` unchanged); `run-0001`/`run-0002` rows never edited in place; exit codes 0/1/2/3 unchanged (`eval/run_eval.py:323-331`); immutability guard unchanged (L131-147).

**Caller audit (OQ-4 — must be done in the same `/implement`):**
- `tests/test_smokes.py::RunEvalSmoke` (L110) passes `ledger_path=cls.ledger` (a tmp) but relies on `write_ledger` defaulting True → **must add `write_ledger=True`** (or call via the new deliverable path) to keep asserting a row is written (L142-147).
- `tests/test_smokes.py::test_main_returns_3_on_populated_dir` (L156) passes `--ledger <tmp>` → under Option C this now implies deliverable; still exits 3 on populated dir (guard fires before ledger write) → behavior preserved.
- `tests/test_smokes.py::NoLedgerGuardSmoke` (L249) already asserts no-write with `write_ledger=False` / `--no-ledger` → passes under the new default; update the CLI test if `--no-ledger` is dropped.
- All Sprint 01 throwaway smokes use `write_ledger=False` → unaffected.
- `run_eval.main` CLI default (run-0001 deliverable) → now requires `--deliverable`; document in the docstring CLI examples (L34-36).

### 5.5 PR-5 — `replay_check` dead-path marker / CF-02 (Stretch *[assumption: OD-1]*, `analysis/`)

**[SDD recommendation: keep Stretch (OD-1 = Stretch).]** The code is already honest — `replay_check` skips the determinism branch under `seed_controlled=false` with `status="skipped"`, `mode="unseeded"` (`analysis/replay_check.py:114-133`), and `tests/test_smokes.py::ReplayCheckSmoke.test_determinism_skipped_unseeded` (L360-363) already pins `mode=='unseeded'` and `status=='skipped'`. The remaining value is regression-hardening + an explicit marker; low effort, low urgency.

**Design.**
1. **Marker.** Add to `byte_identical` (`analysis/replay_check.py:98`) a `loa:shortcut` line naming the ceiling + upgrade trigger, e.g. `# loa:shortcut: dead path — unreachable while seed_controlled=false; reachable only when seed control is proven (sim/capabilities.json seed_controlled=true) and --replay-run is supplied`.
2. **Test.** Strengthen `ReplayCheckSmoke` with an explicit assertion that `determinism["status"] != "passed"` under unseeded (in addition to `== "skipped"`), and a guard test that flips a fixture to assert the skip branch cannot silently become `passed`. **No fake seed injection** — fixtures keep `seed_controlled=false`; the test verifies the posture, never manufactures seed control.
3. **No byte-identical claim.** The always-on `audit_trail_equality` tier (L69-88) is unchanged; no code path asserts byte-identity while unseeded.

**Validation.** Run against local `run-0001`/`run-0002`: assert `mode=='unseeded'`, `status=='skipped'`, verdict driven by audit-trail equality only; run the new pin; confirm `sim/capabilities.json` still reports `seed_controlled=false` before asserting the dead path stays dead.

### 5.6 PR-6 — Strategy-report update (Core *[assumption: OD-3]*, docs)

**Sections to update** (`docs/strategy-report.md`):
- **§1 Claim ceiling** (L10-14): state Rung 1; cite `docs/claim-ceiling.md` + the ledger's per-row `claim_ceiling`.
- **§4 Evaluation method** (L27-33): the `run-0001` vs `run-0002` same-regime agent-only comparison, n=12, `mode=unseeded`; cite `regime-v001` + ledger rows.
- **§6 Failure-mode section** (L42-46, **Mandatory** under the Rung-4 honesty gate): link to `docs/failure-mode-taxonomy-v001.md` (PR-1) + `docs/failure-modes.md`; name the computable-now categories and the deferred/forbidden ones.
- **§7 Limitations** (L48-54): unseeded/no byte-replay, timeout undetectable, n=12 small, opponent = mirror.
- **§5 Ablation table** (L35-40): remains **DEFERRED** — unchanged.

**PERMITS / FORBIDS framing** (mirrors `docs/operator/deferred-lane-gate-after-sprint-01.md:37-69`):
- **PERMITS:** a recorded same-regime agent-only metric movement bounded by the Rung-1 ledger ceiling (the allowed claim form, PRD §9 / `01-sprint-02-prd.md:171-175`).
- **FORBIDS:** strength / significance / cross-regime / leaderboard claims, the five forbidden words, and every "Still closed" broad-optimization item (`deferred-lane-gate-after-sprint-01.md:71-87`).

**Traceability rule (binding).** Every claim sentence references a specific logged artifact (ledger row / match-summary / regime hash / `delta_report` output) per `docs/strategy-report.md:65-68`; runs by `run_id`+hashes; decks by `deck_id`+hash; **no raw metric values pasted beyond what the sanitized ledger already carries**; no forbidden claim words except as negated/forbidden language.

**Validation.** Manual traceability pass (each non-skeleton sentence cites an artifact path/reference); `eval/hygiene_check.py --paths docs/strategy-report.md`; forbidden-word + card/deck-token grep (expect none); cross-check PERMITS/FORBIDS against the deferred-lane note (every "Still closed" item present, nothing reframed as permitted); confirm §5 still reads DEFERRED.

---

## 6. Acceptance-criteria mapping

| AC | Source requirement | Implementation artifact(s) | Test / validation command | Review/audit evidence | Halt-the-sprint failure mode |
|---|---|---|---|---|---|
| **AC-1** taxonomy honesty | PR-1 | `docs/failure-mode-taxonomy-v001.md`; pointer in `docs/failure-modes.md` | `python eval/hygiene_check.py --paths docs/failure-mode-taxonomy-v001.md`; forbidden-word grep; manual capability-flag cross-check vs `sim/capabilities.json` | review confirms every category declares status+flag, FM-03/04/06/08 `detector: forbidden` + inline boundary | a per-decision quality detector appears, or a category claims a detector its capability forbids |
| **AC-2** aggregate-only diagnostics | PR-2 | `analysis/failure_report.py`; tests in `tests/test_smokes.py` | `python tests/test_import_direction.py`; `python tests/test_smokes.py`; `python eval/hygiene_check.py --paths analysis/failure_report.py`; run vs local `run-0002`, grep output for card/deck tokens (expect none) | review confirms no `traces/` read, no `cabt`/`sim`/`eval`/`runtime` import, output is counts only | the report reads or emits any raw trace row / card-adjacent token |
| **AC-3** delta correctness | PR-3 | `analysis/delta_report.py`; `DeltaReportSmoke` | `python tests/test_smokes.py`; None↔number fixtures; `run-0001` vs `run-0002` delta-table-unchanged assertion; cross-regime exit-2 check | review confirms `change_kind` branch, no fabricated `down`, why-moved symmetric, no `frozen/` edit | a `None↔number` transition still renders a fabricated direction, or `frozen/` is edited |
| **AC-4** ledger integrity | PR-4 | `eval/run_eval.py`; `NoLedgerGuardSmoke` + new tests | `python tests/test_smokes.py`; default-invocation-no-write fixture; explicit-deliverable-writes fixture; idempotency on re-run | review confirms default writes no ledger, `summary.csv` always written, two existing rows untouched, exit codes/guard intact | a default/non-deliverable invocation appends to `docs/ledger.md`, or an existing row is edited in place |
| **AC-5** replay honesty (stretch) | PR-5 | `analysis/replay_check.py`; `ReplayCheckSmoke` | `python tests/test_smokes.py`; assert `status != 'passed'` and `== 'skipped'` under unseeded | review confirms `loa:shortcut` marker + no fake seed | a fake seed is injected, or the skip branch can become `passed` while unseeded |
| **AC-6** report traceability | PR-6 | `docs/strategy-report.md` | manual traceability pass; `python eval/hygiene_check.py --paths docs/strategy-report.md`; forbidden-word + card/deck grep; §5-still-DEFERRED check | review confirms every non-skeleton sentence cites an artifact, PERMITS/FORBIDS complete | a claim sentence lacks an artifact ref, or a forbidden claim is made |
| **AC-7** loop discipline | all PRs | `/implement` patches; one review + one audit artifact | orchestrator persists `grimoires/loa/a2a/sprint-N/engineer-feedback.md` + `auditor-sprint-feedback.md` | exactly one review + one audit artifact; no out-of-loop edits | code lands outside `/implement`, or a COMPLETED marker appears without operator authorization |
| **AC-8** claim ceiling held | all PRs | every tracked Sprint 02 artifact | forbidden-word grep across all changed tracked files; ledger remains the only ceiling-bearing artifact | audit re-verifies claim-ceiling text vs `docs/claim-ceiling.md` | any artifact makes a claim beyond Rung 1, or a non-ledger artifact asserts a ceiling |

---

## 7. Validation / test plan

**Always-run gates (every PR):**
```bash
python tests/test_import_direction.py
python tests/test_smokes.py
python eval/hygiene_check.py --paths <changed tracked files>
```
- `test_import_direction.py` covers §2 invariants 2–4 for all `analysis/`/`eval/` changes (PR-2 new module auto-included).
- `test_smokes.py` is the stdlib `unittest` suite (NFR-7); new/edited test classes live here.
- `hygiene_check.py --paths` is run against each changed tracked doc/code file before staging.

**New / updated tests:**

| Area | Test | Location |
|---|---|---|
| taxonomy sanitization / status enum | (doc-level, validated via hygiene + grep + manual flag cross-check; no unit test for a markdown file) | n/a (PR-1 is docs) |
| aggregate report synthetic fixtures | counts per `result`/`ending_cause` from synthetic `match_results` tempdir | `tests/test_smokes.py` new `FailureReportSmoke` |
| aggregate report no raw row emission | assert rendered output contains no trace-row keys / card-adjacent tokens; assert no `traces/` read (e.g. fixture with a poisoned trace file that must be ignored) | `FailureReportSmoke` |
| import-direction coverage of new module | assert `analysis/failure_report.py` is in the lint's scanned set and reports zero violations | `tests/test_smokes.py` or `test_import_direction.py` |
| delta_report None↔number rendering | `appeared`/`disappeared` change_kind + no fabricated `down` | `DeltaReportSmoke` |
| why-moved coverage | every moved/appeared/disappeared metric has a why line; every unmoved keeps why-no-change | `DeltaReportSmoke` |
| delta_report numeric output unchanged | `run-0001` vs `run-0002` delta-table values byte-unchanged | `DeltaReportSmoke` (read-only against local runs) |
| default run_eval does not mutate `docs/ledger.md` | bare/default invocation → no ledger file/row | `NoLedgerGuardSmoke` + new default-mode test |
| explicit deliverable ledger write still works | `--deliverable` / `write_ledger=True, ledger_path=<tmp>` → exactly one row, idempotent | new `DeliverableLedgerSmoke` |
| replay_check unseeded skip posture (PR-5) | `status != 'passed'`, `== 'skipped'`, `mode=='unseeded'` | `ReplayCheckSmoke` |
| strategy-report forbidden-claim / traceability | hygiene + grep + manual traceability checklist | n/a (PR-6 is docs; checklist in §5.6) |

**No validation step may mutate `run-0001` or `run-0002`.** All run-dir tests either (a) read the sealed local runs read-only, or (b) build throwaway tempdirs via `run_eval(..., write_ledger=False)` and `shutil.copytree` (the existing pattern at `tests/test_smokes.py:307-327`). Tampering fixtures (e.g. `ReplayCheckSmoke.test_tamper_detected`, L370-376) copy into a tempdir first.

---

## 8. Import-direction & runtime/offline constraints

- **Lint is executable (OQ-1):** `tests/test_import_direction.py` (`analysis` → intra-zone only; `eval` → `sim`/`runtime`/`analysis`; `runtime`/`sim` constrained). Run on every PR.
- **PR-2** (`analysis/failure_report.py`): stdlib + intra-zone `import aggregate` only. Auto-covered; PR-2 adds an assertion that the new module is in the scanned set (§2 gap-closure).
- **PR-3/PR-5** (`analysis/`): no new imports; remain stdlib + intra-zone.
- **PR-4** (`eval/run_eval.py`): already imports `sim`/`runtime`/`analysis`/`eval` (allowed, `eval/run_eval.py:50-58`); PR-4 adds no imports.
- **Offline/runtime separation preserved:** no Sprint 02 file imports `cabt`/`cg`. No runtime file is edited. Runtime stays stdlib-only.
- **Runtime constraint:** all PR-2..PR-5 code is offline; none runs on the per-move path. No latency concern.

---

## 9. Evidence-storage & sanitization design

Per loop contract §7 / ESP-1..ESP-5 / SP-6 and `eval/schemas.md:13-15`:

- **Full runs remain local/git-ignored.** `runs/run-0001`, `runs/run-0002`, and any throwaway tempdir runs stay local; `hygiene_check.py` blocks `runs/<id>/...` paths (`eval/hygiene_check.py:43`). `run-0001` unmutated from Sprint 00.
- **Aggregate report output is stdout by default.** If `--out <path>` is used it writes a **local/git-ignored** file (a run-derived artifact under ESP-1); tracking it requires explicit operator approval (SP-6 / OD-8). Default = no file.
- **Tracked docs reference only** `run_id`, content hashes, sanitized metrics, claim ceilings, and aggregate categories — never embedded raw values. The taxonomy (PR-1) and strategy report (PR-6) cite categories and reference strings; the aggregate report (PR-2) emits counts, not rows.
- **Forbidden in any tracked artifact:** raw traces, card IDs/names, deck lists, simulator logs, PDFs/CSVs, `deck.csv` rows, Competition Data.
- **`hygiene_check.py` remains required** as a pre-commit guard and is run `--paths` on every changed file before staging.

---

## 10. Claim-ceiling enforcement design

- **Rung 1 remains the ceiling** for all Sprint 02 artifacts (`docs/claim-ceiling.md`; deferred-lane note L43). No PR raises it.
- **The ledger (`docs/ledger.md`) remains the only ceiling-bearing artifact** (`docs/claim-ceiling.md:5-7`). The taxonomy, aggregate report, delta report, and strategy report carry **no** ceiling — they carry a Rung-1 footer that asserts no strength claim (pattern: `analysis/delta_report.py:166-170`).
- **No gameplay-strength, statistical-significance, cross-regime, or leaderboard claim** appears in any tracked output. Cross-regime is additionally hard-refused by `delta_report` (exit 2), preserved by PR-3.
- **Forbidden words** (`strong, competitive, optimal, calibrated, complete`) checked by grep across every changed tracked file as an AC-8 gate; they may appear only as negated/forbidden language.

---

## 11. Migration / compatibility notes

- **PR-4 is the only behavior-changing migration.** Flipping `write_ledger` default to `False` (Option C) changes the bare-CLI contract: `python eval/run_eval.py` no longer writes `docs/ledger.md`. The same-`/implement` caller audit (§5.4) updates `tests/test_smokes.py::RunEvalSmoke` to declare deliverable intent. Recommend retaining `--no-ledger` as a deprecated no-op alias to avoid breaking unseen wrappers (DQ-2).
- **PR-3 is additive on the live path** (new why-moved prose; new `change_kind` field) and behavior-changing only on the previously-dead None↔number branch. Delta-table values for current runs are unchanged (DQ-1 caveat on "output unchanged" wording).
- **PR-1, PR-2, PR-5, PR-6 are non-breaking:** new file (PR-1, PR-2), in-place marker/test (PR-5), doc fill-in (PR-6). The ledger schema, match-summary schema, and run-dir layout are unchanged across all PRs.
- **No frozen / regime change** → no regime version bump; `regime-v001` stays authoritative.

---

## 12. Risks & mitigations

| # | Risk | Mitigation (design-level) |
|---|------|---------------------------|
| R1 | Scope creep into optimization (a "taxonomy"/"report" reinterpreted as a per-decision quality scorer or agent tuning). | PR-1 encodes `detector: forbidden` + inline boundary for FM-03/04/06/08; no `agents/runtime/` file in the module plan (§3); import-direction lint blocks reaching into runtime; review rejects any decision-logic touch. |
| R2 | Claim-ceiling inflation (n=12 `win_rate` move narrated as "better"). | AC-8 forbidden-word grep; Rung-1 footer on every non-ledger artifact; PERMITS/FORBIDS framing in PR-6; ledger stays sole ceiling-bearer. |
| R3 | Competition-Data / raw-trace leakage via PR-2. | PR-2 reads only match-summary aggregate fields (§4.2), never `traces/`; error captured as presence-flag not string; `hygiene_check` + a no-raw-row unit test (poisoned-trace-ignored fixture) gate it. |
| R4 | Ledger contamination persists if PR-4 deferred (OD-2). | Recommend PR-4 Core; until landed, any non-deliverable run must pass the no-write path. Option C makes no-write the *default*, removing the footgun entirely. |
| R5 | Acting on the CF-03 latent branch before PR-3 lands. | PR-3 adds runnable None↔number fixtures before the branch is relied on; explanation narrative (PR-6) cites only the live moved/unmoved output, not the dead branch. |
| R6 | Building before a gate is open. | This SDD opens no gate; PR-2..PR-5 explicitly require OA-2; Sprint Plan is the next step, not `/implement`. |
| R7 | `avg_match_length`/`avg_turns` "fixed" by editing a frozen artifact. | PR-3 documents the alias in-code/in-report only; `frozen/` edit is out of scope (a frozen change is a new regime). |
| R8 | False-honesty regression on CF-02. | PR-5 pins `status != 'passed'` under unseeded and forbids fake-seed injection; audit-trail tier unchanged. |
| R9 | "Output unchanged" (AC-3) read strictly → why-moved lines flagged as a violation. | DQ-1 surfaces the wording question to the operator/Sprint Plan; recommended reading + a flag-gated fallback documented in §5.3. |

---

## 13. Open design questions

| ID | Question | This SDD's position |
|---|---|---|
| **DQ-1** | AC-3 says PR-3 "leaves the present numeric output unchanged," but adding a why-moved line for the moved metrics (`win_rate`, `avg_turns`) adds prose to the live report. | Read "unchanged" as *delta-table rows + values unchanged*; the why-moved prose is intended additive behavior symmetric with why-no-change. **[SDD design question — confirm at Sprint Plan / operator.]** Fallback: gate why-moved lines behind a flag or restrict to appeared/disappeared. |
| **DQ-2** | PR-4 removes `--no-ledger`. Keep as deprecated no-op alias or drop? | Recommend keep as deprecated no-op (its meaning — "don't write" — is now the default) to avoid breaking unseen wrappers. **Operator/Sprint Plan confirms.** |
| **OQ-1** | Import-direction: lint or convention? | **Resolved: executable lint** (`tests/test_import_direction.py`). PR-2 adds a coverage assertion for the new module. |
| **OQ-2** | Taxonomy location? | **Resolved: sibling file** `docs/failure-mode-taxonomy-v001.md` (justified §5.1). |
| **OQ-3** | PR-4 CLI shape? | **Resolved: Option C** (justified §5.4). |
| **OQ-4** | `run_eval` callers relying on deliverable-by-default? | **Resolved: none external.** Caller audit in §5.4; `RunEvalSmoke` must declare intent. |
| **OQ-5** | Aggregate report: new module or extend `aggregate.py`? | **Resolved: new module** `analysis/failure_report.py` (justified §5.2). |

---

## 14. Operator decisions needed before Sprint Plan / implementation

These do not block this SDD; recommended dispositions are marked. None are silently decided here.

- **OD-1 — PR-5 core or stretch?** *[SDD: Stretch.]* Code already honest; marker/test is regression-hardening.
- **OD-2 — PR-4 mandatory?** *[SDD: Core.]* Option C removes the footgun by making no-write the default; protects the only ceiling-bearing artifact.
- **OD-3 — PR-6 in-sprint or closeout?** *[SDD: in-sprint Core.]* Fills the Mandatory §6 honesty section.
- **OD-4 — no per-decision quality detectors?** *[SDD: none allowed.]* Encoded as `detector: forbidden` in PR-1.
- **OD-5 — no runtime agent changes?** *[SDD: none.]* No `agents/runtime/` file in the module plan.
- **OD-6 — no build gate open yet?** *[SDD: none.]* PR-2..PR-5 require OA-2.
- **OD-8 — taxonomy/strategy docs tracked, no run-dir contents tracked?** *[SDD: taxonomy + strategy report are tracked sanitized docs; aggregate-report output stays local/ignored unless explicitly approved.]* SP-6 relaxation requires operator approval.
- **DQ-1 / DQ-2** (above) — confirm the "output unchanged" reading and the `--no-ledger` deprecation.
- **Build-gate (OA-2):** the single hard procedural gate. `/implement` runs only after explicit operator authorization.

---

## 15. Recommendation

**PROCEED to Sprint Plan** for Sprint 02 as "Delta Explanation + Failure-Mode Taxonomy," scoped to **PR-1, PR-2, PR-3, PR-4, PR-6 as Core** and **PR-5 as Stretch** (pending OD-1..OD-3 confirmation). All six requirements have a confirmed, well-scoped design confined to the analysis/offline and provenance/docs layers, with every open question from the PRD resolved (OQ-1..OQ-5) or carried as a clearly-scoped operator decision (DQ-1, DQ-2).

**Do NOT begin implementation.** This SDD opens no build gate. `/implement` may run only after a separate explicit operator build-gate action (OA-2) per loop contract §6. The next Golden Path step is the Sprint Plan.

> **Sources:** `docs/cycles/cycle-001-sprint-02/01-sprint-02-prd.md` (binding input); `docs/cycles/cycle-001-sprint-02/00-research-and-planning.md`; `docs/operator/deferred-lane-gate-after-sprint-01.md` (L37-97); `docs/operator/turntrace-loop-contract.md` (§1-§3, §6-§10); `docs/claim-ceiling.md` (L5-7, L20-64); `docs/cycles/cycle-001-sprint-01/closeout.md`; `docs/failure-modes.md` (L5-101); `docs/strategy-report.md` (L10-68); `eval/schemas.md` (L13-119); `docs/cycles/cycle-000-bootstrap/02-turntrace-sdd.md` (§1.6, L257-270); `analysis/delta_report.py` (L41-43, L73-78, L109, L156-170); `analysis/replay_check.py` (L98-133); `analysis/aggregate.py` (L29-40, L62-63, L125-140); `eval/run_eval.py` (L91-103, L263-338); `eval/hygiene_check.py` (L35-95); `tests/test_import_direction.py` (L24-79); `tests/test_smokes.py` (L102-393); `sim/capabilities.json`; `frozen/metrics/metrics-spec-v001.json`.
