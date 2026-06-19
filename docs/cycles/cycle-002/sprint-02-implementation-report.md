# Cycle-002 Sprint 02 — Implementation Report (Repeated Batch + Dispersion Report)

> Sprint-scoped, cycle-scoped tracked report (build-gate OA-2, Sprint 02 only). Status:
> **ready for `/review-sprint sprint-02`, NOT acceptance.** Sanitized: no raw traces, card
> IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs, or Competition Data
> appear here. Runs are referenced by run-id pattern, counts, byte footprint, and local
> path/status only. **This tracked report deliberately contains NO dispersion metric
> values** — the observed per-agent dispersion numbers live only in the local/git-ignored
> dispersion report and are not promoted to tracked status (an SP-6 relaxation would be a
> separate operator decision). The forbidden affirmative claim words
> (*strong / competitive / optimal / calibrated / complete*) appear only as negated/forbidden
> language. Claim ceiling: **Rung 1** (unchanged).

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-002 / Sprint 02 — Repeated Batch + Dispersion Report |
| **Gate** | Build-gated; OA-2 opened for **Sprint 02 only** |
| **Date** | 2026-06-18 |
| **Base commit** | `a8ce2db` — *feat: add TurnTrace Cycle-002 regime v002 foundation* |
| **Claim ceiling** | **Rung 1** (not raised; `docs/ledger.md` remains the only ceiling-bearing artifact) |
| **Posture** | Improve the EVALUATION HARNESS, not the agent (agents frozen) |

## OA-2 scope confirmation

This work was performed under an OA-2 build gate scoped to **Cycle-002 Sprint 02 only**.
It did **not** reopen Sprint 00 or Sprint 01, did **not** change any runtime agent, did
**not** perform broad optimization, did **not** raise the claim ceiling, did **not**
perform cross-regime comparison, did **not** add inferential statistics, and did **not**
produce a tracked dispersion-output summary. Only the authorized Core tasks were
implemented: **S02-T1, S02-T2, S02-T3, S02-T6**. No Stretch task (S02-T4 paired-delta,
S02-T5 `eval/run_batch.py`) was implemented.

## Executive summary

Sprint 02 stood up a repeated same-regime batch and an offline descriptive-dispersion
report, both bounded to Rung 1:

1. **S02-T1** — chose **K = 20** and ran **2K = 40** sealed, immutable, local/git-ignored
   run dirs under `regime-v002` (`N = 500`), all **non-deliverable** (no ledger row),
   via repeated invocation of the **unchanged** `eval/run_eval.py` (mechanism C-i).
2. **S02-T2** — added one new offline module, `analysis/dispersion_report.py`, that reads
   only sealed run-dir `manifest.json` + `match_results/*.json` (per-run stats via
   `aggregate.aggregate_run()`), refuses mixed regimes with exit 2, and emits **descriptive
   statistics only** (`count / min / max / range / mean / median / spread`) with a Rung-1
   footer and the unseeded-process caveat.
3. **S02-T3** — added 14 synthetic-fixture tests proving the single-regime guard,
   descriptive-only output, import boundary, and sanitization.
4. **S02-T6** — this report; end-to-end AC sweep below.

## Files changed

### Tracked (authorized matrix)

| File | Action | Notes |
|---|---|---|
| `analysis/dispersion_report.py` | **create** | New offline descriptive-dispersion module (S02-T2). |
| `tests/test_smokes.py` | **edit** | +`import dispersion_report`; +1 synthetic-run helper; +5 test classes / 14 tests (S02-T3). |
| `docs/cycles/cycle-002/sprint-02-implementation-report.md` | **create** | This report (S02-T6). |

**`tests/test_import_direction.py` was NOT modified** (justification, per the prompt's
allowance to adjust the test surface). The import-direction lint already auto-scans every
`analysis/*.py` file via `_module_zone_map()` (`tests/test_import_direction.py:40-46`), so
the new module is covered with **no edit** to the lint. The lint-coverage guarantee
required by AC-S02-4/AC-S02-7 (the module is in the scanned set and reports zero
violations) is asserted from `tests/test_smokes.py` —
`DispersionImportBoundary.test_module_scanned_and_clean`
(`tests/test_smokes.py:939`) — mirroring the existing `FailureReportImportCoverage`
pattern. Keeping the change in `tests/test_smokes.py` keeps scope narrow and adds no broad
new test infrastructure.

### Local / git-ignored evidence (NOT staged, NOT committed)

- `grimoires/loa/a2a/cycle-002/sprint-02/k-decision.md` — K-decision note.
- `grimoires/loa/a2a/cycle-002/sprint-02/run-transcript.md` — 2K batch command transcript.
- `grimoires/loa/a2a/cycle-002/sprint-02/dispersion-report.md` — local descriptive report.
- `grimoires/loa/a2a/cycle-002/sprint-02/dispersion-report.json` — local report (JSON).
- `runs/run-v002-b-1` … `run-v002-b-20`, `runs/run-v002-c-1` … `run-v002-c-20` — 40 sealed run dirs.

## S02-T1 — K decision and the 2K batch

### K chosen and rationale

**K = 20** → **2K = 40** sealed local run dirs (20 baseline + 20 candidate). Rationale
(full note: local `k-decision.md`):

- **Footprint is dominated by per-decision sidecars**, which scale with matches. Measured
  from the existing sealed runs: `random_legal` ≈ 45,038 B/match, `scripted_baseline`
  ≈ 30,507 B/match.
- **Estimate at N=500, 2K=40 runs:** realistic ≈ 0.70 GiB; conservative (50,000 B/match
  applied to *both* agents) ≈ 0.93 GiB; very conservative (×1.5 tail margin) ≈ 1.40 GiB —
  all safely below the 3 GiB ceiling.
- **K ≤ 50**, so no operator halt was required; **20 runs/agent** gives a meaningful set of
  per-run data points for *descriptive* dispersion while keeping operator/runtime risk low.
- **Disk:** ≈ 119 GiB free at start — abundant.

### Confirmation K stayed under the 3 GiB ceiling

**Actual measured footprint of the 40 run dirs: 821,109,783 bytes = 783.1 MiB = 0.765 GiB**
— under the 3 GiB ceiling with **≈ 3.9× headroom**. Disk free after the batch: ≈ 117.9 GiB.

### Command method used for the 2K runs

Mechanism **C-i**: a **local shell loop** over the **unchanged** `eval/run_eval.py`, once
per run id, `--regime-id regime-v002`, `--agent {random_legal|scripted_baseline}`, with
**no** `--deliverable` and **no** `--ledger` (so `write_ledger` stays `False`). No tracked
`eval/run_batch.py` was created (that is Stretch S02-T5, not authorized). The full
transcript is the local `run-transcript.md`; every line reported `[rc=0] … n=500 …
ledger_appended=False`.

### Local run IDs created (pattern)

- baseline (`random_legal`): `run-v002-b-1` … `run-v002-b-20`
- candidate (`scripted_baseline`): `run-v002-c-1` … `run-v002-c-20`

40 dirs total (20 + 20), verified by directory count and by reading each
`manifest.json`.

### Confirmations (S02-T1)

- **All run dirs are local/git-ignored and unstaged.** `git check-ignore` reports each
  `runs/run-v002-*` path (and files within) ignored; `git status --porcelain runs/` is
  empty. Only `runs/.gitkeep` is tracked.
- **All runs are `regime-v002`.** Every `manifest.json` (the ID authority) carries
  `regime_id = regime-v002`; the 20 baseline dirs carry `agent_id = random_legal`, the 20
  candidate dirs `agent_id = scripted_baseline`; each has exactly 500 `match_results`.
- **All runs are non-deliverable.** Each invocation reported `ledger_appended=False`.
- **No ledger row was written.** `grep -c run-v002 docs/ledger.md` → 0.
- **`docs/ledger.md` unchanged.** `git diff --quiet docs/ledger.md` is clean (exit 0).

## S02-T2 — `analysis/dispersion_report.py`

New offline module (SDD §7). Summary:

- **Reads only** each run dir's `manifest.json` (the `regime_id` / `agent_id` authority;
  `analysis/dispersion_report.py:83,129`) and `match_results/*.json` **via**
  `aggregate.aggregate_run()` (`:147`) — the single source of per-run sanitized stats. It
  **never** references the per-decision sidecar directory and never reads error-string
  bodies (the source contains no such reference; same sanitization surface as
  `failure_report.py`).
- **Single-regime guard** (`MixedRegimeRefusal`, `:79`; raised at `:135`): if the input run
  dirs do not all share one `regime_id`, it hard-refuses with **exit 2** — structurally
  identical to `delta_report.py`'s `CrossRegimeRefusal`. Cross-regime aggregation is
  mechanically impossible.
- **Descriptive statistics only** (`descriptive_stats`, `:94`; `STAT_COLUMNS`, `:76`):
  `count`, `min`, `max`, `range` (the pair min..max), `mean`, `median`, `spread` (max − min)
  — pure arithmetic over the per-run metric values (`min`/`max`/`sum` + `statistics.median`).
  The module computes **no** sample standard deviation, **no** variance, and **no**
  inferential statistic; their absence is structural (there is no code path to compute
  them).
- **Metrics dispersed** (`DISPERSION_METRICS`, `:69`): the already-sanitized aggregate set
  `win_rate`, `illegal_action_rate`, `timeout_rate`, `error_rate`, `avg_turns`,
  `avg_wall_clock_ms`.
- **Every report carries** `regime_id`, `n`, `K`, the agent id, the unseeded-process
  caveat, and a Rung-1 footer; it carries **no ceiling of its own**.
- **Imports:** stdlib (`argparse`, `json`, `statistics`, `sys`, `pathlib`) + intra-`analysis/`
  `import aggregate` only — no `eval`, `sim`, `cabt`, or `agents/runtime`.
- **CLI:** `dispersion_report.py <run_dir>... [--json] [--out <local-path>]`; exit `0`
  produced · `1` input failure · `2` mixed-regime refusal. Output is local/git-ignored by
  default (`--out` is a local path).

## S02-T3 — dispersion-report tests

14 tests across 5 classes in `tests/test_smokes.py`, **synthetic fixtures only** (each
builds `manifest.json` + `match_results/*.json` directly via `_write_synth_run`,
`tests/test_smokes.py:804`; no simulator, no Competition Data; metric values set
explicitly, so no RNG and no implied simulator seed control):

| Class (line) | Proves |
|---|---|
| `DispersionSingleRegimeGuard` (`:841`) | uniform `regime-v002` → exit 0; mixed regime → `MixedRegimeRefusal` / exit 2. |
| `DispersionDescriptiveOnly` (`:874`) | output includes `count/min/max/range/mean/median/spread`; excludes every inferential/overreach term; `descriptive_stats` keys are exactly the seven; no `statistics.stdev/variance/...` code path. |
| `DispersionImportBoundary` (`:934`) | module is in the import-direction lint's scanned set with zero violations; imports no `eval/sim/runtime/cabt` zone; intra-`analysis/` `import aggregate` present. |
| `DispersionSanitization` (`:955`) | poison written into sidecars + error fields is never surfaced; clean/poisoned stats are identical (sidecars never read); source has no sidecar-dir reference; rendered output passes `hygiene_check`. |
| `DispersionMissingInput` (`:1006`) | missing run dir → exit 1; missing/empty `match_results` → exit 1. |

## Local dispersion output

The descriptive report was generated over the 40 batch dirs to two **local/git-ignored**
paths (both pass `hygiene_check`):

- `grimoires/loa/a2a/cycle-002/sprint-02/dispersion-report.md`
- `grimoires/loa/a2a/cycle-002/sprint-02/dispersion-report.json`

**This tracked report does not reproduce the dispersion metric values.** The per-agent
observed dispersion (`count/min/max/range/mean/median/spread` per metric, with `regime_id`,
`n`, `K`, and the Rung-1 footer) is recorded only in the local report above. Promotion of
any sanitized dispersion summary to tracked status is a separate operator decision (SP-6)
and is **not** done here.

## Validation — tests, hygiene, scans

### Tests run and results

- `python tests/test_smokes.py` → **72 tests OK** (58 pre-existing + 14 new dispersion
  tests). Includes the pre-existing real `regime-v002` n=500 run path.
- `python tests/test_import_direction.py` → **OK** (runtime/offline separation intact; the
  new module is auto-scanned and clean).

### Hygiene result

- `python eval/hygiene_check.py --paths analysis/dispersion_report.py tests/test_smokes.py
  tests/test_import_direction.py docs/cycles/cycle-002/sprint-02-implementation-report.md`
  → **clean**.
- `hygiene_check` on both local dispersion outputs → **clean**.

### Forbidden-word / sanitization scan result

- **Changed tracked files + local outputs** scanned for the forbidden affirmative
  (*strong/competitive/optimal/calibrated/complete*) and inferential/overreach terms
  (*significant, confidence interval, p-value, hypothesis, standard deviation, variance,
  statistically, beats, better, worse, uplift, improvement*).
- **`analysis/dispersion_report.py`:** the only hits are **negated policy language** in the
  module docstring/comments (e.g. "computes **no** … variance … **no** inferential
  statistic") — the same negated framing the SDD §7.4 uses and that `delta_report.py`
  applies to the affirmative words. No affirmative claim word appears.
- **Local `dispersion-report.md` / `.json`:** **zero** forbidden-word hits.
- **Raw/sensitive indicators** (`deck.csv`, card ids, deck lists, `hand=`, simulator logs,
  raw trace rows, PDFs/CSVs, Competition Data): **none** in the module or local outputs.
- **Within `tests/test_smokes.py`**, the forbidden terms appear only as (a) the test's
  *exclusion* assertion list and (b) synthetic poison fixtures asserted to be **absent**
  from output — acceptable test-fixture / negated usage.

## AC Verification

Acceptance criteria quoted verbatim from the OA-2 prompt. Evidence cites `file:line`,
manifest facts, or test results — never dispersion values.

| AC | Verbatim criterion | Status | Evidence |
|---|---|---|---|
| **AC-S02-1** | "K chosen safely under the 3 GiB ceiling" | ✓ Met | K=20; actual footprint 0.765 GiB (≈3.9× headroom); local `k-decision.md`. |
| **AC-S02-2** | "2K sealed same-regime local run dirs exist" | ✓ Met | 40 dirs `run-v002-b/c-{1..20}`; each `manifest.json` `regime_id=regime-v002`, 500 `match_results`; immutable (sealed via the unchanged `run_eval` immutability guard). |
| **AC-S02-3** | "all 2K runs are non-deliverable and no ledger row is written" | ✓ Met | every run `ledger_appended=False` (`run-transcript.md`); `grep -c run-v002 docs/ledger.md`→0; `git diff --quiet docs/ledger.md` clean. |
| **AC-S02-4** | "`analysis/dispersion_report.py` reads only sanitized sealed run-dir artifacts" | ✓ Met | reads `manifest.json` (`analysis/dispersion_report.py:83,129`) + `aggregate.aggregate_run` (`:147`); no sidecar reference; `DispersionSanitization` (`tests/test_smokes.py:955`). |
| **AC-S02-5** | "dispersion report refuses mixed regimes with exit 2" | ✓ Met | `MixedRegimeRefusal` (`analysis/dispersion_report.py:79`, raised `:135`, mapped to exit 2 `:277`); `DispersionSingleRegimeGuard.test_mixed_regime_refused_exit_2` (`tests/test_smokes.py:867`). |
| **AC-S02-6** | "dispersion output is descriptive-only" | ✓ Met | `descriptive_stats` (`:94`) + `STAT_COLUMNS` (`:76`) compute only the seven; `DispersionDescriptiveOnly` (`tests/test_smokes.py:874`) asserts allowed-present / inferential-absent and no inferential code path. |
| **AC-S02-7** | "tests prove import boundary and sanitization" | ✓ Met | `DispersionImportBoundary` (`:934`) + `DispersionSanitization` (`:955`). |
| **AC-S02-8** | "no runtime-agent or forbidden harness mutation" | ✓ Met | `git diff --name-only` lists only the 2 authorized tracked code/test files; no `agents/runtime/`, `eval/run_eval.py`, `analysis/aggregate.py`, frozen, or ledger change (see scope confirmation below). |
| **AC-X1** | "claim ceiling held at Rung 1" | ✓ Met | every artifact carries a Rung-1 footer and no ceiling of its own; `docs/ledger.md` unchanged (only ceiling-bearer). |
| **AC-X2** | "no cross-regime comparison" | ✓ Met | the report groups per agent under one `regime_id`; the single-regime guard hard-refuses mixed input (exit 2); no `regime-v002` number is placed beside a v001 row. |
| **AC-X3** | "loop discipline" | ✓ Met | code landed only via `/implement`; ready for `/review-sprint` → `/audit-sprint`; no COMPLETED marker created. |
| **AC-X4** | "forbidden words only negated/forbidden" | ✓ Met | scan above: affirmative words absent; inferential terms only negated (module) / as test exclusion+poison (tests); zero hits in local outputs. |
| **AC-X5** | "review/audit storage discipline" | ✓ Met | all evidence under git-ignored `grimoires/loa/a2a/...`; no review/audit/COMPLETED artifact tracked. |

## Scope confirmations (final)

- **No runtime-agent changes** — `agents/runtime/` untouched; agents are frozen inputs.
- **No broad optimization** — no tuning, scoring, search, or heuristic change anywhere.
- **No Sprint 02 stretch tasks** — S02-T4 and S02-T5 were not implemented.
- **No `eval/run_batch.py`** — the 2K batch used a local shell loop over the unchanged
  `run_eval.py`; no tracked batch runner was created.
- **No paired-delta dispersion** — the module reports per-agent dispersion only.
- **No tracked dispersion-output summary** — values stay in the local report.
- **No claim-ceiling advance** — Rung 1 throughout.
- **Cycle-002 remains Rung 1.**
- **No forbidden file changed** — no `eval/run_eval.py`, `analysis/aggregate.py`,
  `analysis/delta_report.py`, `analysis/failure_report.py`, `analysis/replay_check.py`,
  `eval/hygiene_check.py`, no v001/v002 frozen file, no `docs/ledger.md`, no tracked
  `runs/` content, no `.claude/`.
- **State Zone artifacts** (`grimoires/loa/a2a/...`) are local/git-ignored and not
  staged/tracked; `.beads/*` is not staged/tracked.

## Known limitations / honest boundaries

- **Unseeded process.** `seed_controlled=false`; observed dispersion reflects the whole
  process (agent behaviour together with uncontrolled simulator RNG) and is **not** an
  isolated agent-only quantity. The dispersion report embeds this caveat inline.
- **Descriptive only, Rung 1.** No strength, comparison, or inferential claim is made or
  supported; the report carries no ceiling.
- **Dispersion values are local.** They are intentionally absent from every tracked
  artifact pending a separate operator decision.

## Verification steps for the reviewer

```bash
git status -sb
git diff --name-only
python tests/test_smokes.py
python tests/test_import_direction.py
python eval/hygiene_check.py --paths \
  analysis/dispersion_report.py \
  tests/test_smokes.py \
  tests/test_import_direction.py \
  docs/cycles/cycle-002/sprint-02-implementation-report.md
# local report (over the local, git-ignored batch dirs):
python analysis/dispersion_report.py runs/run-v002-b-* runs/run-v002-c-* \
  --out grimoires/loa/a2a/cycle-002/sprint-02/dispersion-report.md
```

## Status

**Sprint 02 is ready for `/review-sprint sprint-02`, NOT acceptance.** No COMPLETED marker
has been created; acceptance and any cycle-close summary remain explicit later operator
decisions.
