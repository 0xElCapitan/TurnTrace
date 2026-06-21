# Cycle-008 Sprint S01 — Diagnostic Core + Synthetic Fixtures: Implementation Report

> Sprint artifact (S01 — Diagnostic core + synthetic fixtures). Status: **IMPLEMENTATION COMPLETE — awaiting
> `/review-sprint` → `/audit-sprint` → operator acceptance.** This S01 pass lands the offline, stdlib-only,
> single-regime **descriptive** trace diagnostic (`analysis/trace_diagnostic.py`, generator path only) plus
> committed synthetic sealed-run fixtures and a stdlib test suite. It implements **no** `validate_diagnostic()`,
> **no** `--validate` mode, **no** sanitizer rejection classes, **no** poisoned fixtures, and **no**
> `analysis/ledger_validate.py` — those are S02/S03. It runs no eval, creates no fresh evidence, writes no
> SP-6, writes/edits no ledger row, advances no claim ceiling, selects no Rung-3 target / candidate / numeric
> margin `M` / `K` / `n` / regime id / feature family, edits no `.claude/`, and cleans/stages no State-Zone dirt.
>
> **Sanitized note.** No raw traces, simulator logs, deck lists, card IDs/names, Pokémon Elements, Competition
> Data, Daily-Top-Episodes, Kaggle episode data, Discord/peer screenshots, run-dir dumps, PDFs/CSVs, `deck.csv`,
> `cg/`, raw evidence rows, dispersion/band/win-rate values, or any inferential statistic (no p-value, confidence
> interval, hypothesis test, std-dev, variance, or model estimate) appears here. **No numeric governance threshold
> `M` is chosen or stated.** No forbidden agent word (*strong / competitive / optimal / calibrated / complete*)
> applies. The committed fixtures carry only synthetic, schema-shaped counts/booleans/outcomes — no card data, no
> Pokémon Elements, no raw deck content.

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-008 / Sprint **S01 — Diagnostic core + synthetic fixtures** |
| **Type** | App-Zone code/test (behind the OD-C8-6 OA-2 build gate, scoped to `analysis/` + `tests/`) |
| **Date** | 2026-06-20 |
| **Status** | **IMPLEMENTATION COMPLETE** — review/audit/acceptance pending; **not committed or pushed** in this pass |
| **Build-time HEAD** | `0fd8c8d6a91ef60ba88961fc7d995696def4da79` — *docs: accept Cycle-008 Sprint S00 preflight* (== `origin/main`; not ahead/behind) |
| **Sprint-plan citation anchor** | `95d4811` — the plan's build-time HEAD; anchors relied on re-validated at the build-time HEAD (see §6) |
| **Operator gate** | **OD-C8-6 OPEN** — the operator explicitly opened the OA-2-class build gate for the Cycle-008 App-Zone code lane (diagnostic; scoped to `analysis/` + `tests/`); this S01 request is **S01 only** |
| **Claim ceiling (at S01)** | **Rung 2 — "beats random-legal"**; **held and preserved** (ceiling artifact byte-unchanged) |
| **Ledger invariant** | `docs/ledger.md` byte-unchanged; `git hash-object = 7da7e9a8dbed6561669d1569445eb9fe67a953fb` |
| **Ceiling invariant** | `docs/claim-ceiling.md` byte-unchanged; `git hash-object = 3d99759b919f7d75bc41ea81cd82e5f1fb974be7` |

---

## 1. Sprint goal & scope

**Goal (sprint plan `03-sprint-plan.md:396-399`).** "Land the offline, stdlib-only, single-regime descriptive
diagnostic `analysis/trace_diagnostic.py` (generator path only) that reads existing sealed run artifacts and emits
the five §2.2 descriptive surfaces under **safe aggregate key names** (RN-2), with the `SAFE_FIELDS` allow-list and
a **mechanical descriptive-only** key-set test — exercised against committed synthetic fixtures so it depends on no
local run dir."

**Scope.** MEDIUM (5 tasks: S01.1–S01.5, `03-sprint-plan.md:454-467`). **Type:** App-Zone code/test.
**Operator gate:** OD-C8-6 open. This pass implements the **generator path only**; the co-located sanitizer
(`validate_diagnostic` + `--validate` + rejection classes + poisoned fixtures) is explicitly deferred to S02.

---

## 2. What was built

### 2.1 `analysis/trace_diagnostic.py` (NEW; generator path only)

The first `analysis/` module to read `traces/<match_id>.jsonl` rows **for content** (SDD §2.1). It reads, per
`run_id`, both read-only:

- `manifest.json` — **first**, the `regime_id` authority; the single-regime guard fires before any aggregation.
- `match_results/*.json` — via `aggregate.aggregate_run` (the sanctioned per-run rollup + regime cross-check) and
  directly for per-match `result` / `ending_cause` / `wall_clock_ms` / `invalid_action_count` / `timeout`.
- `traces/<match_id>.jsonl` — decision rows (`public_state_summary` board counts, `decision_latency_ms`) and the
  terminal row (`final_prize_counts`).

It emits a single-regime JSON object bounded to the **five** authorized descriptive surfaces (SDD §2.2), under
**safe aggregate key names** — never raw decision-body field names (RN-2):

| # | Surface | Raw field READ internally | Safe aggregate output key(s) emitted |
|---|---|---|---|
| 1 | Outcome / ending-cause | `result`, `ending_cause` (match-summary enums) | `outcome_counts`, `ending_cause_counts` |
| 2 | Board shape | `public_state_summary.bench_count`/`.active_present` (**marker**) | `bench_count_stats` (per side), `active_present_rate` (per side) |
| 3 | Prize trajectory | `public_state_summary.prize_count` (per row), `final_prize_counts` (terminal) | `prize_trajectory_stats` (per side), `final_prize_counts_by_side` (per side) |
| 4 | Latency / throughput | `decision_latency_ms` (**marker**), `wall_clock_ms` (match) | `latency_ms_stats`, `wall_clock_ms_stats` |
| 5 | Error / illegal / timeout | `result==error`, `invalid_action_count`, `timeout` | `error_presence_count`, `illegal_action_total`, `illegal_action_excluded`, `timeout` (null) |

- **`SAFE_FIELDS`** ([analysis/trace_diagnostic.py:114](../../../analysis/trace_diagnostic.py)) — the single
  source of truth for the diagnostic's output keys (identity + the five surface containers + per-side `p0`/`p1` +
  the sanitized outcome/ending-cause enums + the seven `STAT_COLUMNS`). Disjoint from
  `evidence_summary._DECISION_BODY_MARKERS` by construction.
- **Reuse, not recompute** — `descriptive_stats` / `STAT_COLUMNS` are imported from `analysis.dispersion_report`
  and `aggregate_run` from `analysis.aggregate` ([analysis/trace_diagnostic.py:69-75](../../../analysis/trace_diagnostic.py)),
  so **no new statistic and no inferential statistic can enter** through this module.
- **Single-regime hard-refusal (exit 2)** — manifest-first; a mixed-regime invocation raises `MixedRegimeRefusal`
  before any aggregation ([analysis/trace_diagnostic.py:207-216](../../../analysis/trace_diagnostic.py)).
- **CLI** — `python analysis/trace_diagnostic.py <run_dir> [<run_dir> ...] [--json] [--out <local-path>]`;
  `--out` refuses any tracked `docs/` path via the `_refuse_tracked_out` guard (parity copy of
  `evidence_summary.py:451-476`); output is local/gitignored by default
  ([analysis/trace_diagnostic.py:386-393](../../../analysis/trace_diagnostic.py)). Generate-path exit contract:
  `0` produced · `1` input failure · `2` mixed-regime refusal. (Exit 3 / `--validate` arrives in S02.)

### 2.2 Committed synthetic sealed-run fixtures (`tests/fixtures/diagnostic/`)

Sanitized, schema-shaped, **no** card data / Pokémon Elements / raw deck content:

- `clean/run-syn-a-01/` — one single-regime run (`regime-syn-a`), 3 matches + per-match traces; exercises all five
  surfaces (win/loss/error outcomes; an illegal action; an error presence; a null `final_prize_counts`).
- `mixed/run-syn-a-01/` + `mixed/run-syn-b-01/` — two run dirs carrying **different** `regime_id`s, the
  mixed-regime exit-2 fixture.

### 2.3 `tests/test_trace_diagnostic.py` (NEW; stdlib, plain-assert)

42 checks driven off the committed fixtures (no dependence on local `runs/`).

---

## 3. Commands run & results

All run at build-time HEAD `0fd8c8d`. Smallest-sufficient first, then the relevant full checks.

| # | Command | Result |
|---|---|---|
| 1 | `python analysis/trace_diagnostic.py tests/fixtures/diagnostic/clean/run-syn-a-01` | exit **0**; emits all five surfaces under safe aggregate keys |
| 2 | `python analysis/trace_diagnostic.py tests/fixtures/diagnostic/mixed/run-syn-a-01 tests/fixtures/diagnostic/mixed/run-syn-b-01` | exit **2** (mixed-regime refusal, before aggregation) |
| 3 | `python tests/test_trace_diagnostic.py` | exit **0** — **all 42 checks pass** |
| 4 | `python tests/test_import_direction.py` | exit **0** — runtime/offline separation intact |
| 5 | `python tests/test_evidence_summary.py` | exit **0** — no regression (12 checks + hardening + promotion-check) |
| 6 | `python tests/test_smokes.py` | exit **0** — **72 tests OK** (no regression) |
| 7 | `python eval/hygiene_check.py --paths <15 new artifacts>` | exit **0** — clean; no Competition-Data paths |
| 8 | `git check-ignore` on the fixtures | not ignored — committed under `tests/`, independent of gitignored `runs/` |
| 9 | `git hash-object docs/ledger.md` | `7da7e9a8…` (byte-unchanged) |
| 10 | `git hash-object docs/claim-ceiling.md` | `3d99759b…` (byte-unchanged) |
| 11 | `git status --porcelain .claude/` | empty (System Zone clean) |

---

## 4. Acceptance-criteria verification

Each S01 acceptance criterion (`03-sprint-plan.md:426-452`) is quoted verbatim, with status and file:line evidence.

1. **Surfaces.** "given a committed synthetic sealed-run fixture, `build_diagnostic` emits all five §2.2 surfaces;
   each statistical surface uses `{count,min,max,range,mean,median,spread}`." — **✓ Met.**
   [analysis/trace_diagnostic.py:290-315](../../../analysis/trace_diagnostic.py) assembles the five surfaces;
   [tests/test_trace_diagnostic.py:93](../../../tests/test_trace_diagnostic.py) (`t_five_surfaces`) asserts
   each surface present and every `*_stats` object carries exactly the seven `STAT_COLUMNS`.

2. **Descriptive-only, mechanical.** "a test asserts the generated output's full key-set (at **every nesting
   depth**) is a **subset of `SAFE_FIELDS`**, and that **no key** matches a
   quality/score/recommendation/'should-have'/optimal-action pattern. **No quality/score/recommendation field is
   present (asserted absent).**" — **✓ Met.**
   [tests/test_trace_diagnostic.py:127](../../../tests/test_trace_diagnostic.py) (`t_keyset_subset_safe_fields`,
   recursive) + [:134](../../../tests/test_trace_diagnostic.py) (`t_no_quality_keys`).

3. **Safe aggregate names (RN-2).** "the output carries **none** of `_DECISION_BODY_MARKERS` as a key …; latency
   is emitted as `latency_ms_stats`, board shape as `bench_count_stats` / `active_present_rate`, etc. (A test
   asserts the marker set ∩ output-key-set = ∅.)" — **✓ Met.**
   [tests/test_trace_diagnostic.py:143](../../../tests/test_trace_diagnostic.py) (`t_marker_disjoint`) imports
   `evidence_summary._DECISION_BODY_MARKERS` and asserts disjointness (output keys and `SAFE_FIELDS` both).

4. **Single-regime.** "a mixed-regime synthetic fixture → **exit 2**, before any aggregation." — **✓ Met.**
   [analysis/trace_diagnostic.py:207-216](../../../analysis/trace_diagnostic.py) (guard before the per-run loop);
   [tests/test_trace_diagnostic.py:158](../../../tests/test_trace_diagnostic.py) asserts both the
   `MixedRegimeRefusal` raise and CLI exit 2.

5. **Import direction & stdlib.** "`python tests/test_import_direction.py` exits 0; an AST/source lint confirms
   `trace_diagnostic.py` imports **no** `sim`/`cabt`/`eval`/`agents.runtime` and is stdlib + intra-`analysis/`
   only." — **✓ Met.** Command #4 exits 0;
   [tests/test_trace_diagnostic.py:170](../../../tests/test_trace_diagnostic.py) (`t_import_direction`) runs the
   AST checker and asserts every zoned import is analysis-zone.

6. **Fixture independence.** "the diagnostic runs against the committed synthetic fixtures with **no local run dir
   present** (verified by running with only `tests/` fixtures on PATH)." — **✓ Met.**
   [tests/test_trace_diagnostic.py:184](../../../tests/test_trace_diagnostic.py) (`t_fixture_independence`)
   asserts the fixture is under `tests/fixtures` and not under `runs/`, and that the diagnostic was built from it;
   command #8 confirms the fixtures are git-trackable (not gitignored).

7. **No new statistic.** "a test confirms the statistical surface is exactly `STAT_COLUMNS` (no
   std-dev/variance/CI/p-value computed anywhere; their absence is structural via the reused helper)." — **✓ Met.**
   [tests/test_trace_diagnostic.py:195](../../../tests/test_trace_diagnostic.py) (`t_no_new_statistic`) asserts
   `td.descriptive_stats is dispersion_report.descriptive_stats`, `STAT_COLUMNS` equality, every stats object uses
   exactly those seven keys, and the generator imports no `statistics` module of its own.

8. **Local-by-default.** "`--out` to a tracked `docs/` path is refused; default output is local/gitignored;
   `git status --porcelain` shows no diagnostic output staged/tracked." — **✓ Met.**
   [analysis/trace_diagnostic.py:330](../../../analysis/trace_diagnostic.py) (`_refuse_tracked_out`);
   [tests/test_trace_diagnostic.py:218](../../../tests/test_trace_diagnostic.py) (`t_out_refuses_tracked_docs`)
   asserts relative/absolute `docs/` and `ledger.md` refused, local path accepted. `git status` (§5) shows no
   diagnostic output file.

9. **Hygiene.** "`eval/hygiene_check.py` clean on the tracked artifacts …; the fixtures embed no raw content." —
   **✓ Met.** Command #7 exits 0 over all 15 new artifacts.

10. **Non-occurrence.** "no `sim`/`cabt`/`eval` import; no new dependency; no new instrumentation; no quality
    scorer; no `M`; no fresh evidence; `git hash-object docs/ledger.md` unchanged (`7da7e9a8…`);
    `docs/claim-ceiling.md` unchanged." — **✓ Met.** See §3 commands #4, #9, #10; §6 below. Stdlib-only (imports:
    `argparse`, `json`, `sys`, `pathlib`, + intra-`analysis` `aggregate`/`dispersion_report`).

11. **`/review-sprint` + `/audit-sprint` both pass; operator accepts.** — **⏸ Pending** (downstream gates; not
    part of this `/implement` pass).

---

## 5. Changed files & final status

**New (untracked) — all under the sanctioned `analysis/` + `tests/` lane:**

- `analysis/trace_diagnostic.py`
- `tests/test_trace_diagnostic.py`
- `tests/fixtures/diagnostic/clean/run-syn-a-01/{manifest.json, match_results/M0001..M0003.json, traces/M0001..M0003.jsonl}`
- `tests/fixtures/diagnostic/mixed/run-syn-a-01/{manifest.json, match_results/M0001.json, traces/M0001.jsonl}`
- `tests/fixtures/diagnostic/mixed/run-syn-b-01/{manifest.json, match_results/M0001.json, traces/M0001.jsonl}`
- `docs/cycles/cycle-008/05-s01-implementation-report.md` (this file)

**Final `git status --porcelain`** (changes left unstaged; not committed or pushed):

```
 M .beads/issues.jsonl
 M grimoires/loa/NOTES.md
?? analysis/trace_diagnostic.py
?? docs/cycles/cycle-008/05-s01-implementation-report.md
?? grimoires/loa/README.draft.md
?? tests/fixtures/
?? tests/test_trace_diagnostic.py
```

`.beads/issues.jsonl`, `grimoires/loa/NOTES.md`, and `grimoires/loa/README.draft.md` remain the pre-existing
State-Zone dirt — **modified/untracked-unstaged, not edited, not staged, not cleaned** by this pass.

---

## 6. Invariant & citation-anchor verification

- **HEAD / origin parity:** `git rev-parse HEAD == origin/main == 0fd8c8d6a91ef60ba88961fc7d995696def4da79`.
- **Ledger invariant:** `git hash-object docs/ledger.md = 7da7e9a8dbed6561669d1569445eb9fe67a953fb` (byte-unchanged).
- **Ceiling invariant:** `git hash-object docs/claim-ceiling.md = 3d99759b919f7d75bc41ea81cd82e5f1fb974be7`
  (byte-unchanged); **claim ceiling remains Rung 2**.
- **System Zone:** `git status --porcelain .claude/` empty.
- **Citation anchors re-validated at build-time HEAD (NFR-12):** `evidence_summary.py` `SAFE_FIELDS` (:85),
  `_DECISION_BODY_MARKERS` (:285-290), `_refuse_tracked_out` (:451-476), exit set (:46-48);
  `dispersion_report.py` `STAT_COLUMNS` (:76), `descriptive_stats` (:94), `MixedRegimeRefusal` (:79);
  `aggregate.py` `aggregate_run` (:56); `eval/schemas.md` decision/terminal rows (:60-91) — all accurate at
  `0fd8c8d`.

---

## 7. Known limitations / handoff to S02

- **Generator path only.** `validate_diagnostic()`, the `--validate` mode, every rejection class, the numeric-`M`
  rule, and the poisoned fixtures are **out of scope for S01** and land in S02. The exit-3 leak code is therefore
  not yet exercised by this module (the generate path uses `0`/`1`/`2`).
- **RN-2 forward property.** The generator's output uses safe aggregate keys disjoint from
  `_DECISION_BODY_MARKERS`, so S02's co-located sanitizer will accept the clean diagnostic output (exit 0). S01
  asserts the disjointness; S02 asserts the round-trip acceptance + every rejection class.
- **`public_state_summary` shape.** The diagnostic reads board/prize counts from a per-side
  `{"p0":…, "p1":…}` sub-structure (`active_present`, `bench_count`, `prize_count`) — schema-consistent with
  `eval/schemas.md` ("counts both sides, no card IDs"). The committed synthetic fixtures define this shape.

**Stop point.** S01 implementation only. No review, audit, S02, S03, or S04 work performed.
