# Cycle-002 Sprint 01 — Scale Foundation — Implementation Report

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-002 · Sprint 01 (Scale Foundation) |
| **Gate** | Build-gated — landed under **OA-2 for Cycle-002 Sprint 01 only** |
| **Lanes / FR** | D (budget) + A (additive `regime-v002`) · C2-FR-1, C2-FR-2; G proofs for C2-FR-7 |
| **Date** | 2026-06-18 |
| **Status** | **Ready for `/review-sprint sprint-01`, NOT acceptance.** No COMPLETED marker created. |
| **Claim ceiling** | Rung 1 (unchanged; not raised) |

> Sanitized report. Timing (ms/s), byte sizes, content hashes, `run_id`s, artifact names, and proof
> outcomes only. No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, or Competition Data appear here (CC-1/CC-2, ESP). The forbidden agent claim words
> (*strong / competitive / optimal / calibrated / complete*) appear only as this negated/forbidden
> reference. No `regime-v002` metric is placed beside a v001 ledger row (NFR-5).

## 1. OA-2 scope confirmation

This work was performed under the operator's **OA-2 build gate opened for Cycle-002 Sprint 01 only**.
It does **not** open Sprint 02, does **not** create `analysis/dispersion_report.py` or
`eval/run_batch.py`, does **not** run any repeated 2K batch, does **not** change any runtime agent,
and does **not** raise the claim ceiling. Sprint 01 implements only Lane D (budget) and Lane A (the
two additive frozen files) plus the S01-T4/T5/T6 proofs (`03-sprint-plan.md:182-246`).

## 2. Files changed

**Tracked (the only files staged for this sprint):**

| File | Action | Task |
|---|---|---|
| [frozen/seeds/seed-set-v002.json](../../../frozen/seeds/seed-set-v002.json) | create (additive) | S01-T2 |
| [frozen/regimes/regime-v002.json](../../../frozen/regimes/regime-v002.json) | create (additive) | S01-T3 |
| [tests/test_smokes.py](../../../tests/test_smokes.py) | edit (3 new test classes appended) | S01-T4/T5/T6 |
| [docs/cycles/cycle-002/sprint-01-implementation-report.md](sprint-01-implementation-report.md) | create | report |

`tests/test_smokes.py` was used (not a new file) — it is the repo's existing stdlib `unittest` suite
and the sprint plan's designated home for these classes (`03-sprint-plan.md:360`). The change is
purely additive: one `import hashlib` and three appended classes (`tests/test_smokes.py:636-767`); no
existing test was modified.

**Local / git-ignored evidence (NOT staged, NOT tracked, NOT frozen evidence):** under
`grimoires/loa/a2a/cycle-002/sprint-01/` — `probe_budget.py` (throwaway probe), `gen_frozen.py` (local
generator for the two frozen files), `budget-note.md` (sanitized budget note). These live in the
gitignored State Zone (`.gitignore:17`) and were confirmed absent from `git status`.

## 3. S01-T1 — Dry-run budget, chosen `N`, storage ceiling

### 3.1 Method (existing harness only; no modification)

A bounded **local throwaway probe** (`grimoires/loa/a2a/cycle-002/sprint-01/probe_budget.py`) measured
per-match wall-clock and per-run disk using the **existing** harness:

- **Loop probe** — 120 matches per agent via `eval/run_match.py`'s `run_single` + `write_match`
  (a direct larger-sample per-match measurement that needs no seed-set file).
- **End-to-end probe** — one `eval/run_eval.py:run_eval(...)` per agent on `regime-v001` (n=12) with
  `write_ledger=False`, capturing fixed per-run overhead (`manifest.json` + `hashes.txt` +
  `summary.csv` + `notes.md` + aggregation).

The probe imported the harness as-is — **`eval/run_eval.py` was not modified** — wrote **no** ledger
row (`write_ledger=False`, the shipped default; `eval/run_eval.py:97,281-288`), built every run dir
inside `tempfile.mkdtemp()` and deleted it (no run dir or raw output left in the repo, nothing under
`runs/`), and authored **no** frozen interim seed-set. This resolves the D↔A ordering
(`03-sprint-plan.md:204-216`): `N` was chosen from the larger-sample loop measurement **before**
`seed-set-v002` was authored, so no frozen file was ever rewritten.

### 3.2 Sanitized results (conservative = worst-case agent, `random_legal`)

| Quantity | Measured (two probe runs) | Conservative |
|---|---|---|
| per-match wall-clock | 13.3–14.0 ms | **~14 ms** |
| per-match disk (traces dominate) | 43.8–45.3 KiB | **~45 KiB** |
| fixed files per run (manifest/hashes/summary/notes) | 3.0 KiB | **~3 KiB** |
| `run_eval` n=12 end-to-end `ledger_appended` | False | **no ledger** |

Throughput ≈ 70–87 matches/s — consistent with the `seed-set-v001` `n_note` (~80–190 matches/s) and
research RQ-5 ("throughput is not the bottleneck; storage/IO is the managed cost",
`00-research-and-planning.md:170-180`). Full numbers are in the local `budget-note.md` (sanitized:
timing + sizes only).

### 3.3 Chosen `N` = 500, storage ceiling = 3 GiB

- **`N` = 500.** A substantial sampling-resolution increase over the n=12 Sprint-00 set — a real scale
  foundation that tightens the view of the **same unseeded distribution**, not a higher rung
  (research RQ-3; `04-rung-2-readiness-criteria.md`). By the measured budget a single `regime-v002`
  run is ~7 s wall-clock and ~22 MiB. `match_indices` is the contiguous **neutral** list `1..500`
  (no index chosen to flatter an agent; risk R2), within the existing `M%04d` id format
  (`M0001`..`M0500`; `eval/run_eval.py:136`). `N` is an output of the dry-run (OD-4 / OD-B2), not
  fixed by any planning doc.
- **Storage ceiling = 3 GiB** for the combined **local** `runs/run-v002-*` footprint. Derivation:
  conservative per-run ≈ 22 MiB → round up to ≤ 25 MiB/run; 3 GiB ÷ 25 MiB ≈ 122 run dirs ≈ K ≤ ~60
  paired comparisons. **Rule carried to Sprint 02:** HALT the batch if the local footprint would
  exceed 3 GiB (risk R6). Even a generous K=50 (100 run dirs) stays ~11 min / ~2.1 GiB — bounded.
- **`K` is not chosen here** — it is a Sprint-02 decision (OD-4), informed by this budget.

## 4. S01-T2 / S01-T3 — additive frozen files

- **`seed-set-v002.json`** mirrors `seed-set-v001.json`'s schema exactly (SDD §5.2): `seed_set_id`,
  `mode`, `rationale`, `match_indices`, `seeds`, `n`, `n_note`. Values: `seed_set_id="seed-set-v002"`,
  `mode="unseeded"`, `seeds=null`, `match_indices=[1..500]`, `n=500`. The `n_note` records that `N`
  came from the Sprint-01 dry-run budget and that this is an additive Cycle-002 larger-n seed-set,
  **not** seed control.
- **`regime-v002.json`** mirrors `regime-v001.json` (SDD §5.3): `regime_id="regime-v002"`,
  `seed_set="seed-set-v002"`, and **reuse by reference** `opponent_pool="opponent-pool-v001"`,
  `deck_pool="deck-pool-v001"`, `metrics_spec="metrics-spec-v001"` (OD-3); `mode="unseeded"`. The
  `notes` field states: only the seed-set differs from `regime-v001`; `regime-v001` and its components
  remain byte-unchanged; **never** compare `regime-v002` numbers to v001 ledger rows (NFR-5); changing
  any component requires a **new** regime, never an edit; `seed_controlled=false` so reproducibility is
  distribution-stable + audit-trail (not byte-identical replay).

**Additivity proof.** `RegimeV002AdditiveSmoke` (`tests/test_smokes.py:667-703`) asserts the v002 files
conform and are additive: `seed-set-v002`'s field set equals `seed-set-v001`'s; `regime-v002`'s field
set equals `regime-v001`'s; the three reused component references are byte-identical strings to v001's;
and the **only** value that differs between the two regimes is `seed_set`. The harness records the three
reused components' content hashes into every run's `hashes.txt` (`eval/run_eval.py:239-243`), so reuse
is provable per run without re-minting. The two frozen files were generated by the local
`gen_frozen.py` (which self-validates schema on write); both are well-formed JSON, ASCII-only.

## 5. S01-T4 — `regime-v001` byte-unchanged proof

`V001ByteUnchangedSmoke` (`tests/test_smokes.py:636-664`) pins `regime-v001.json` and its four
component files against golden content hashes; it fails if any file's content differs.

**Line-ending note (faithful, not a loophole).** This repo runs `core.autocrlf=true` with no
`.gitattributes`, so raw working-tree bytes are CRLF on a Windows checkout and LF on Linux, while the
**committed** content is LF either way. The test therefore hashes the **LF-normalized content**
(universal-newline read → UTF-8 → SHA-256), which pins each file's content identity portably across
checkouts. Any real content edit changes the hash and fails the test. The golden LF-content hashes
(captured at Sprint 01):

| File | golden LF-content sha256 |
|---|---|
| `frozen/regimes/regime-v001.json` | `f99beee3…59153` |
| `frozen/seeds/seed-set-v001.json` | `d93f3692…83cd2` |
| `frozen/opponents/opponent-pool-v001.json` | `f785bb98…7958a` |
| `frozen/decks/deck-pool-v001.json` | `cf4b2cbf…7e694` |
| `frozen/metrics/metrics-spec-v001.json` | `0d2283ab…673e5c` |

Independently confirmed during implementation: `git status` shows none of the five v001 files modified,
and a direct hash check reported **ALL v001 BYTE-UNCHANGED**. No v001 file was edited to make any test
pass.

## 6. S01-T5 — no-ledger-by-default proof

`RegimeV002GuardsAndLedgerSmoke` (`tests/test_smokes.py:706-767`) runs a bare/non-deliverable
`run_eval` against **`regime-v002`** (n=500, `write_ledger` defaulted to False) into a tempdir with a
**redirected tmp ledger path** — never `docs/ledger.md`:

- `test_no_ledger_row_by_default_v002` (`:731`) — asserts `ledger_appended` is False and the redirected
  ledger file was **not created**.
- `test_summary_csv_still_written_v002` (`:736`) — asserts `summary.csv` **was** written and the run
  produced all `n=500` matches end-to-end (summary output without a ledger row).
- `test_redirected_ledger_is_not_the_tracked_ledger` (`:740`) — asserts the test's ledger path is not
  `docs/ledger.md`.

This is a real mechanical exercise of `run_eval` against `regime-v002` (not a stub). `docs/ledger.md`
was not mutated (it remains the two-row n=12 record; confirmed unmodified in `git status`).

## 7. S01-T6 — guards hold at scale

Same class, all under `regime-v002` at the larger `N`, with **no guard logic modified**:

- **Immutability (exit 3):** `test_immutability_guard_refuses_populated_v002` (`:745`) re-runs into the
  populated `regime-v002` run dir and asserts `ImmutabilityRefusal` is raised and the sealed
  `manifest.json` is untouched; `test_immutability_guard_exit_3_v002` (`:752`) asserts
  `run_eval.main(...)` returns **exit 3** on the populated dir and that the (redirected) ledger is not
  created (the guard fires before any ledger write).
- **Deck-drift:** `test_deck_drift_guard_refuses_v002` (`:759`) points `TURNTRACE_DECK_FILE` at a
  **synthetic 60-integer deck** (arbitrary integers — **not** Competition Data) whose content hash
  differs from the frozen `deck-pool-v001` hash, then asserts `run_eval` raises a `RuntimeError`
  containing "deck drift" and that `run_eval.main(...)` returns **exit 1**. The deck-drift guard
  precedes both the immutability guard and the match loop, so no run dir is created and no match is
  played; the env var is restored in a `finally`. Real sealed run dirs and v001 frozen files are never
  touched (tempdirs/synthetic inputs only).

## 8. Tests run and results

| Command | Result |
|---|---|
| `python tests/test_smokes.py` | **OK — Ran 58 tests** (49 prior + 9 new Sprint 01) |
| `python -m unittest -v` (the 3 new classes) | **OK — Ran 9 tests** |
| `python tests/test_import_direction.py` | **exit 0** — runtime/offline separation intact (tests/ is outside the lint's scanned zones; no new runtime/sim/eval/analysis import added) |

The 9 new tests: `V001ByteUnchangedSmoke` (1) + `RegimeV002AdditiveSmoke` (2) +
`RegimeV002GuardsAndLedgerSmoke` (6). The full suite's wall-clock rose because the `regime-v002`
no-ledger proof runs n=500 matches once (shared via `setUpClass`); this is the chosen larger `N`
exercised end-to-end.

## 9. Hygiene + forbidden-word / sanitization scan

- **`eval/hygiene_check.py --paths` (the three code/data tracked files):** `clean` (exit 0). The fourth
  tracked file (this report) is re-checked at staging; all four paths are clean (`docs/cycles/…`,
  `frozen/…`, `tests/…` match no Competition-Data rule; `eval/hygiene_check.py:35-45`).
- **Forbidden-word scan (`strong/competitive/optimal/calibrated/complete`) over changed tracked
  files:** the **word-boundary** scan found **no** whole-word forbidden term. The only substring hit is
  the **pre-existing** schema field name `"completed_at"` (`tests/test_smokes.py:180`, in the untouched
  `SchemaRejectionSmoke`) — a timestamp field, not an affirmative agent-quality claim. The frozen files'
  `notes`/`rationale`/`n_note` use no forbidden word affirmatively. This report uses them only as the
  negated/forbidden reference in the banner.
- **Sanitization:** no raw traces, card IDs/names, deck lists, simulator logs, PDFs/CSVs, or run-dir
  contents appear in any tracked file. The synthetic deck used by the deck-drift test is arbitrary
  integers in a tempfile (not Competition Data) and is never staged.

## 10. AC Verification

Every Sprint 01 and cross-cutting AC from `03-sprint-plan.md:404-436`, quoted verbatim (Validation
cell), with status and `file:line` evidence.

| AC | Verbatim validation criterion | Status | Evidence |
|---|---|---|---|
| **AC-S01-1** | "Sanitized **local** budget note records wall-clock + disk + a safe `N` + storage ceiling; dry-run wrote **no** ledger row; outputs local/ignored" | ✓ Met | `grimoires/loa/a2a/cycle-002/sprint-01/budget-note.md` (local) §2–§4; probe `…/probe_budget.py` uses `write_ledger=False` + tempdirs; §3 above |
| **AC-S01-2** | "`seed-set-v002` + `regime-v002` exist as **additive** files (`mode=unseeded`, `seeds=null`, `match_indices` len == `N`); only the seed-set differs; reuse opponent/deck/metrics by ref" | ✓ Met | [seed-set-v002.json](../../../frozen/seeds/seed-set-v002.json); [regime-v002.json](../../../frozen/regimes/regime-v002.json); `tests/test_smokes.py:678,689` |
| **AC-S01-3** | "Test asserts `regime-v001.json` + its 4 components byte-identical before/after" | ✓ Met | `tests/test_smokes.py:656` (`V001ByteUnchangedSmoke`); independent hash check reported ALL v001 byte-unchanged (§5) |
| **AC-S01-4** | "Bare/non-deliverable `run_eval` on `regime-v002` appends no row to a **redirected test** ledger; `summary.csv` still written" | ✓ Met | `tests/test_smokes.py:731,736` |
| **AC-S01-5** | "Deck-drift guard + immutability guard (exit 3) operate unchanged at the larger `N`" | ✓ Met | `tests/test_smokes.py:745,752` (immutability/exit 3); `:759` (deck-drift, exit 1) |
| **AC-S01-6** | "No `agents/runtime/` edit; `eval/run_eval.py` logic unchanged; hygiene clean on tracked frozen files" | ✓ Met | `git diff --name-only` over `agents/runtime`, `eval/`, `analysis/`, v001 frozen, `docs/ledger.md`, `.claude/` printed nothing (§11); hygiene clean (§9) |
| **AC-X1** | "No tracked artifact claims beyond Rung 1; `docs/ledger.md` stays the only ceiling-bearing artifact" | ✓ Met | Frozen `notes`/`n_note` state Rung-1 hold; this report carries no ceiling; `docs/ledger.md` unmodified |
| **AC-X2** | "No tracked artifact places a `regime-v002` number beside a v001 ledger row as a comparison" | ✓ Met | No `regime-v002` metric is reported anywhere; only sample-size scale (12→500) and budget timings/sizes appear |
| **AC-X3** | "S01 lands through `/implement → /review-sprint → /audit-sprint`; … no out-of-loop edits" | ✓ Met (implement stage) | Code written only in this `/implement` run; report ends here, ready for `/review-sprint sprint-01`; no COMPLETED marker |
| **AC-X4** | "The words *strong/competitive/optimal/calibrated/complete* appear only as negated/forbidden language across all changed tracked files" | ✓ Met | Word-boundary scan: no whole-word hit; only substring is pre-existing `completed_at` field name (§9) |
| **AC-X5** | "Review/audit/COMPLETED artifacts persist only to git-ignored `grimoires/loa/a2a/…`" | ✓ Met | No review/audit/COMPLETED artifact created by `/implement`; local evidence is under gitignored `grimoires/loa/a2a/cycle-002/sprint-01/` |

## 11. Required confirmations

- **No app code outside authorized tests changed.** Only `tests/test_smokes.py` (authorized) was edited
  among code files; the two frozen JSON files are additive data.
- **No runtime-agent changes.** `git diff --name-only -- agents/runtime` is empty; the
  import-direction lint passes.
- **No forbidden harness/app file changed.** `eval/run_eval.py`, `analysis/aggregate.py`,
  `eval/hygiene_check.py`, the other `analysis/` modules — all unchanged (empty diff).
- **No `regime-v001` or v001 component file changed** (byte-unchanged proof + hash check + empty diff).
- **No `docs/ledger.md` change** (unmodified; the two n=12 rows stand).
- **No `runs/` tracked change** (only `runs/.gitkeep` is tracked; probe run dirs were tempdirs).
- **No `.claude/` change.**
- **No Sprint 02 artifacts created** — no `analysis/dispersion_report.py`, no `eval/run_batch.py`, no
  2K batch output, no paired-delta report, no tracked sanitized cycle-close summary.
- **No COMPLETED marker created.** No OA-2 expansion occurred — scope stayed Sprint 01 only; the claim
  ceiling remains Rung 1.
- **State Zone artifacts are local/gitignored and not staged** (`grimoires/loa/a2a/…`); `.beads/*` and
  `grimoires/loa/NOTES.md` remain unstaged (pre-existing dirty state).

## 12. Known limitations

- Dispersion of the unseeded process is **not** measured in Sprint 01 — the cross-run dispersion
  report is Sprint-02 work (`analysis/dispersion_report.py`, out of scope here).
- `K` (batch count) is deliberately **not** chosen here; it is OD-4 for Sprint 02, informed by this
  budget.
- The byte-unchanged test pins **LF-normalized content** (not raw bytes) because the repo uses
  `core.autocrlf=true` with no `.gitattributes`; this is the portable, faithful notion of "byte-
  unchanged" for a committed artifact (§5). Adding a `.gitattributes` to force LF is out of Sprint-01
  scope.

## 13. Verification steps (for the reviewer)

```bash
python tests/test_smokes.py                                   # OK — 58 tests
python tests/test_import_direction.py                         # exit 0
python eval/hygiene_check.py --paths \
  frozen/seeds/seed-set-v002.json frozen/regimes/regime-v002.json \
  tests/test_smokes.py docs/cycles/cycle-002/sprint-01-implementation-report.md
git status --short                                            # only the 4 authorized tracked files
git diff --name-only -- agents/runtime eval/ analysis/ \
  frozen/regimes/regime-v001.json frozen/seeds/seed-set-v001.json \
  frozen/opponents/ frozen/decks/ frozen/metrics/ docs/ledger.md .claude/   # empty
```

**Sprint 01 is ready for `/review-sprint sprint-01` — not acceptance.** No COMPLETED marker has been
or should be created until explicit operator closeout authorization.
