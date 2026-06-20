# Cycle-006 Implementation Report — Sprint 01: Promotion-Check Hardening (`--promotion-check`)

> Implementation artifact (written under `/implement`, OA-2-class build gate opened by the operator 2026-06-19,
> scoped to `analysis/evidence_summary.py` + `tests/test_evidence_summary.py` only). **This sprint promotes
> nothing, writes no ledger row, advances no claim ceiling, generates no fresh evidence, chooses no `M`, issues no
> SP-6, and applies no PASS/FAIL/INCONCLUSIVE verdict.** `--promotion-check` is a *gate* a future Cycle-007
> promotion must pass; building the gate is **not** admitting Rung 2. **Rung 1 held.** The Rung-2 *attempt* is
> deferred to Cycle-007 behind a separate explicit operator gate.
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, Daily-Top-Episode data, or Competition Data appear here or in
> any changed file. Test fixtures are stdlib-only synthetic. No dispersion metric *values* appear. No numeric
> margin `M` is chosen.

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-006 / Sprint 01 — Promotion-Check Hardening |
| **Type** | Implementation Report (Track B code sprint) |
| **Date** | 2026-06-19 |
| **Build-time HEAD** | `082a953` — *docs: plan TurnTrace Cycle-006* (== `origin/main`); a descendant of the SDD/sprint-plan citation anchor `561fb92` |
| **Authorities** | `docs/cycles/cycle-006/01-prd.md` (accepted; OD-C6-1 ratified), `02-sdd.md` (OD-C6-2…6 settled), `03-sprint-plan.md` (T1–T5) |
| **Claim ceiling** | **Rung 1** (held; not raised) |
| **Ledger invariant** | `docs/ledger.md` byte-unchanged; hash `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` (verified before *and* after) |
| **Files changed** | `analysis/evidence_summary.py`, `tests/test_evidence_summary.py`, `docs/cycles/cycle-006/04-implementation-report.md` (this file) |

---

## 1. Preflight / invariant verification

Run at build-time HEAD `082a953`, before any edit (T1):

| Check | Command | Result | Verdict |
|---|---|---|---|
| HEAD | `git rev-parse HEAD` | `082a953923e5fd8e4643171466cfcc23f413a8dd` | ✓ matches the operator-stated baseline |
| origin == HEAD | `git rev-parse origin/main` | `082a953923e5fd8e4643171466cfcc23f413a8dd` | ✓ not ahead/behind |
| Ledger hash | `git hash-object docs/ledger.md` | `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` | ✓ required invariant |
| Ledger diff | `git diff --exit-code -- docs/ledger.md` | exit 0 | ✓ clean |
| Claim ceiling | `git diff --exit-code -- docs/claim-ceiling.md` | exit 0 | ✓ clean |
| Protected-path drift | `git status --porcelain .claude/ frozen/ runs/ agents/ sim/` | empty | ✓ no drift |
| Staged files | `git diff --cached --name-only` | empty | ✓ nothing staged |
| State-Zone files | `git status --porcelain` | ` M .beads/issues.jsonl` · ` M grimoires/loa/NOTES.md` | ✓ only the two pre-existing dirty State-Zone files, unstaged — **left untouched** |

The two pre-existing dirty State-Zone files (`.beads/issues.jsonl`, `grimoires/loa/NOTES.md`) were **not** read for
edit, **not** staged, and **not** cleaned. They remain modified-but-unstaged exactly as found.

## 2. Anchor revalidation notes (NFR-9 / R6)

The SDD/sprint-plan line anchors are pinned to HEAD `561fb92`; build-time HEAD is `082a953`. I confirmed:

- `git merge-base --is-ancestor 561fb92 HEAD` → exit 0 (**`082a953` is a descendant of `561fb92`**).
- `git diff --name-only 561fb92 082a953` → only `docs/cycles/cycle-006/{01-prd,02-sdd,03-sprint-plan}.md`. The
  planning commit touched **no source file**; `analysis/evidence_summary.py` (574 lines) and
  `tests/test_evidence_summary.py` (404 lines) are byte-identical between `561fb92` and `082a953`, so every anchor
  carries over unchanged.

Every SDD §2 anchor re-validated against the build-time source (all confirmed exact):

| Anchor | SDD line | Confirmed at `082a953` |
|---|---|---|
| `main` | :509 | ✓ `def main` at :509 |
| `--validate` arg | :520-521 | ✓ |
| validate dispatch | :530-531 | ✓ |
| `_run_validate` (read-fail :482-487 / mixed :489-494 / validator :496-502 / clean :504-506) | :477-506 | ✓ all four blocks exact |
| `validate_summary` | :392-420 | ✓ |
| `_collect_regime_ids` | :423-442 | ✓ |
| `_enforce_hashes_digest` (+ wiring `_walk` :380-381) | :347-363 | ✓ |
| top-level digest block | :408-419 | ✓ |
| `_refuse_tracked_out` | :449-474 | ✓ |
| generate-mode empty-hashes WARNING | :552-555 | ✓ |
| exit set 0/1/2/3 | :45-46 | ✓ |
| `--promotion-check` token | absent | ✓ absent (only forward-reference WARNING *text* at :551,554) |
| test `check` / `make_run_dir` (`manifest_hash=""` :51,57) / `validate_file_exit` / `_HEX64` | :36 / :49-72 / :75-80 / :33 | ✓ |
| block 13 ends at 13l / 13j ledger byte-compare | :366-368 / :344-356 | ✓ |

**No anchor desync and no repo-reality contradiction.** No stop condition was triggered. Proceeded to code.

## 3. Exact files changed

Exactly the authorized set (App-Zone code + this Docs report):

| Path | Zone | Change | Size before → after |
|---|---|---|---|
| `analysis/evidence_summary.py` | App (tracked) | +`--promotion-check` CLI arg + `_run_promotion_check` driver + 1 docstring synopsis line | 574 → 643 lines |
| `tests/test_evidence_summary.py` | App (tracked) | +`promotion_check_file_exit` helper + block 14 (14a–14f) + summary-line text | 404 → 480 lines |
| `docs/cycles/cycle-006/04-implementation-report.md` | Docs/State | new (this report) | — |

No other tracked file was edited, staged, committed, or pushed. No second validator module, no `*.schema.json`, no
dependency/manifest change, no `.claude/` edit.

## 4. `--promotion-check` implementation summary

Implements the **OD-C6-2 wholesale-`validate_summary` + one empty/absent-`hashes` precheck** design (SDD §4):

- **CLI arg** (`analysis/evidence_summary.py:582-586`): `--promotion-check`, `metavar="summary.json"`,
  `default=None`, mirroring the `--validate` argument shape.
- **Dispatch** (`:596-598`): checked in the same block as `--validate`, **before** it — so if both are supplied the
  stricter promotion gate wins (a single documented precedence choice; neither existing mode's behaviour changes).
- **Driver `_run_promotion_check(path_str) -> int`** (`:511-566`), control flow:
  1. **Re-read from disk** (`:521-529`) — same try/except shape as `_run_validate`
     (`FileNotFoundError`/`OSError`/`json.JSONDecodeError` → stderr, **exit 1**). No new read source; no
     `hashes.txt`, no sidecar.
  2. **Mixed-regime guard** (`:532-538`) — `_collect_regime_ids`; `> 1` distinct regime → **exit 2**.
  3. **Full hardened validator** (`:540-546`) — `validate_summary(summary)` wholesale, **unchanged**; any
     violation → **exit 3**.
  4. **Empty/absent-`hashes` precheck** (`:556-561`, the only added rule) — `h = summary.get("hashes")`;
     `if not (isinstance(h, dict) and h):` → **exit 3** (rides the existing fail-closed class; CF-1 / OD-C5-2
     floor). Per-value digest shape of a non-empty map is already enforced by `validate_summary` above, so this
     asserts **non-emptiness only**.
  5. **Pass** (`:563-566`) — **exit 0** only when the summary is clean **and** `hashes` is a non-empty map. Writes
     nothing; promotes nothing.

**Conservative-only / parity-or-stricter proof (NFR-1).** Demonstrated empirically (§6, parity table): every
fixture maps to an identical exit under `--promotion-check` and `--validate` **except** the empty-`hashes` case
(promotion `3`, validate `0`). The set of inputs `--promotion-check` accepts is therefore a strict subset of what
`--validate` accepts (identical minus empty/absent-`hashes`); **no `--validate`-rejected input is
`--promotion-check`-accepted**. The property holds *by construction* because the driver calls the same
`validate_summary` and `_collect_regime_ids` and only **adds** one rejection.

**Behavior-unchanged (verified):** `validate_summary`, `_run_validate` (`--validate`), `build_summary`, generate
mode, and `_refuse_tracked_out` are untouched. No new exit code — the `0/1/2/3` contract is preserved. No new
import (import-direction stays green). The source-grep invariants hold: `evidence_summary.py` still contains no
`trace`/`traces` token (test 4) and no `hashes.txt` (test 13l).

## 5. Block-14 test summary

New block `# --- 14. promotion-check ---` added to `tests/test_evidence_summary.py` immediately after block 13
(13l), with a `promotion_check_file_exit` helper (`:83-91`) paralleling `validate_file_exit`. Fixtures are
stdlib-only synthetic, reusing `make_run_dir` / `build_summary` / the `good` fixture / `_HEX64` / `es.main`. **No
K-batch, no raw data, no run-dir dependency beyond the existing `make_run_dir` helper.**

| Check | Asserts | Lines | AC | Result |
|---|---|---|---|---|
| 14a | `--promotion-check` on a clean non-empty-`hashes` summary → exit 0 (+ non-empty precondition) | :384-387 | AC-1 | ✓ ok |
| 14b | `--promotion-check` on a structurally-valid empty-`hashes` summary → exit 3 | :389-398 | AC-2 | ✓ ok |
| 14b′ | the same empty-`hashes` summary under `--validate` still → exit 0 (asymmetry guard) | :400-403 | AC-4 | ✓ ok |
| 14c | `--promotion-check` on a forbidden-leak (non-empty-`hashes`) summary → exit 3 (full validator re-run) | :405-413 | AC-3 | ✓ ok |
| 14d | generate-mode empty-`hashes` still WARNS at exit 0 (under the new code) | :415-421 | AC-4 | ✓ ok |
| 14e | `--promotion-check` writes nothing; `docs/ledger.md` byte-unchanged; no new tmp file | :423-438 | AC-5 | ✓ ok |
| 14f | `--promotion-check` on a mixed-regime summary → exit 2 (single-regime guard inherited) | :440-444 | AC-3 / NFR-5 | ✓ ok |

All **12 existing + block-13 (13a–13l)** checks remain green and unmodified. The `main()` summary line
(`:474-475`) now reads `… block 13 (13a–13l) + promotion-check block 14 (14a–14f) pass`.

## 6. Exact commands run and exit codes

### Test-first evidence (block 14 written *before* the driver)

| Command | Exit | Note |
|---|---|---|
| `python analysis/evidence_summary.py --promotion-check nonexist.json` (pre-impl) | **2** | argparse: `unrecognized arguments: --promotion-check` — mode absent |
| `python tests/test_evidence_summary.py` (pre-impl) | **2** | blocks 1–13 + the 14a non-empty precondition pass; suite then crashes at the first `--promotion-check` call (argparse `SystemExit(2)`) — block 14 cannot pass without the driver |

### Required checks (post-impl)

| Command | Exit | Expected |
|---|---|---|
| `python tests/test_evidence_summary.py` | **0** | all 12 + 13a–13l + 14a–14f green |
| `python tests/test_import_direction.py` | **0** | no new import; analysis-only / stdlib-only preserved |
| `python eval/hygiene_check.py --paths analysis/evidence_summary.py tests/test_evidence_summary.py docs/cycles/cycle-006/04-implementation-report.md` | **0** | no Competition-Data path |
| `git hash-object docs/ledger.md` | `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` | byte-unchanged |
| `git diff --exit-code -- docs/ledger.md` | **0** | clean |
| `git diff --exit-code -- docs/claim-ceiling.md` | **0** | clean |
| `git status --porcelain .claude/ frozen/ runs/ agents/ sim/` | (empty) | no protected-path drift |
| `git diff --cached --name-only` | (empty) | nothing staged |

### CLI exit-code contract demonstration (synthetic fixtures, written to a temp dir **outside** the repo)

| Invocation | `--promotion-check` | `--validate` |
|---|---|---|
| clean, non-empty `hashes` | **0** | **0** |
| structurally-valid, **empty** `hashes` | **3** (hard-fail) | **0** (accepted — the asymmetry) |
| forbidden inferential leak (`p-value … significance`) | **3** (full validator) | **3** |
| mixed-regime (`regime-v002` + `regime-v099`) | **2** | **2** |
| unreadable path | **1** | (n/a) |
| both flags (`--promotion-check empty … --validate good …`) | **3** | — (promotion-check wins) |

The empty-`hashes` row is the **only** behavioural difference (3 vs 0); every other row is identical →
parity-or-stricter confirmed empirically.

## 7. Required confirmations

- **Exit-code contract stayed `0/1/2/3`.** ✓ No new exit code. The empty/absent-`hashes` promotion hard-fail
  rides the existing exit 3 (OD-C6-3). Demonstrated across all five exit values in §6.
- **`--validate` empty-`hashes` behaviour stayed exit 0.** ✓ (test 14b′; §6 parity table). `validate_summary` was
  not modified.
- **Generate-mode empty-`hashes` warning stayed exit 0.** ✓ (test 14d re-asserts 13j under the new code; the
  `:552-560` WARNING block is untouched).
- **`--promotion-check` empty-`hashes` behaviour exits 3.** ✓ (test 14b; §6).
- **`docs/ledger.md` untouched.** ✓ `git hash-object` = `2a2f1c2…` before and after; `git diff --exit-code` exit
  0; test 14e byte-compares the ledger across a promotion-check run.
- **`docs/claim-ceiling.md` untouched.** ✓ `git diff --exit-code` exit 0.
- **No raw data added.** ✓ Fixtures are stdlib-only synthetic (`regime-v00X`, `agentX`, `run-*`, `"a"*64`
  digests). No Competition Data, Pokémon Elements, traces, card names, deck lists, simulator logs, Daily-Top-Episode
  or Kaggle episode data in code, tests, or this report. `hygiene_check` exit 0 on all three artifacts.
- **No value promoted.** ✓ `--promotion-check` writes nothing and promotes nothing (it returns an exit code only);
  no dispersion value reaches tracked status; no SP-6.
- **Rung 2 remains deferred.** ✓ No numeric `M`; no Rung-2 ledger row; no claim-ceiling advance; no fresh evidence
  generated; no second validator module; no `*.schema.json`; no dependency; no ledger write. The verdict rule is
  pre-registered (PRD §16.3), **not applied**.
- **Rung 1 held.** ✓ The ledger remains the only ceiling-bearing artifact, byte-unchanged at its two Rung-1 rows.

## 8. AC Verification (PRD §16.2 / sprint-plan §"Acceptance Criteria", AC-1…AC-8)

- **AC-1** — *"`--promotion-check` on a clean, non-empty-`hashes`, schema-conforming summary → exit 0."*
  **✓ Met.** Test 14a (`tests/test_evidence_summary.py:386-387`); driver pass path
  `analysis/evidence_summary.py:563-566`; §6 CLI demo (good → 0).
- **AC-2** — *"`--promotion-check` on a structurally-valid but empty-`hashes` summary → exit 3 (non-zero,
  fail-closed; CF-1 / OD-C5-2 floor)."*
  **✓ Met.** Test 14b (`:397-398`); precheck `analysis/evidence_summary.py:556-561`; §6 (empty → 3).
- **AC-3** — *"`--promotion-check` on a summary carrying any forbidden field/value/word … → exit 3 (it re-runs the
  full hardened validator). A mixed-regime summary → exit 2."*
  **✓ Met.** Test 14c (`:412-413`, leak → 3 with non-empty hashes proving the validator ran) and test 14f
  (`:443-444`, mixed → 2); driver `:540-546` (validator) and `:532-538` (mixed-regime); §6.
- **AC-4** — *"generate-mode still emits the empty-`hashes` WARNING at exit 0; `--validate` still accepts a
  structurally-valid empty `hashes` at exit 0; the `0/1/2/3` contract holds (no new exit code)."*
  **✓ Met.** Tests 14d (`:420-421`) and 14b′ (`:402-403`); generate WARNING block `analysis/evidence_summary.py:552-560`
  unchanged; `--validate` driver `:479-507` unchanged; §6 contract demo.
- **AC-5** — *"`--promotion-check` writes nothing; `docs/ledger.md` byte-unchanged before/after; no tracked `docs/`
  write."*
  **✓ Met.** Test 14e (`:433-438`) byte-compares the ledger and asserts no new tmp file; driver has no write path;
  `git diff --exit-code -- docs/ledger.md` exit 0.
- **AC-6** — *"each behaviour has ≥1 runnable regression check; all existing 12 + block-13 checks remain green;
  `test_import_direction` exit 0; `hygiene_check --paths …` exit 0."*
  **✓ Met.** Block 14 14a–14f runnable and green; 12 + 13a–13l green (§5); `test_import_direction.py` exit 0;
  `hygiene_check.py --paths …` exit 0 (§6).
- **AC-7** — *"posture held (hard): Rung 1; claim-ceiling untouched; no `M`; no SP-6; no value promotion; no
  Rung-2 row; no fresh evidence; no `.claude/` drift; State-Zone files unstaged; no second module; no
  `*.schema.json`; no dependency; no ledger write."*
  **✓ Met.** §1, §7; `git status` (§9) shows only the two authorized code files + the two untouched State-Zone
  files; no forbidden artifact created.
- **AC-8** — *"lands only through `/implement → /review-sprint → /audit-sprint → operator acceptance`."*
  **⏸ In progress (by design).** `/implement` complete (this report); `/review-sprint` and `/audit-sprint` are the
  next cadence steps. No code is staged/committed/pushed; the sprint awaits review.

## 9. Final `git status --porcelain`

```
 M .beads/issues.jsonl          (pre-existing State-Zone; untouched, unstaged)
 M analysis/evidence_summary.py (authorized edit; unstaged)
 M grimoires/loa/NOTES.md       (pre-existing State-Zone; untouched, unstaged)
 M tests/test_evidence_summary.py (authorized edit; unstaged)
?? docs/cycles/cycle-006/04-implementation-report.md (this report; untracked)
```

Nothing staged (`git diff --cached --name-only` empty). Nothing committed or pushed.

## 10. Deviations / blockers

**None.** The sprint was implemented exactly as planned (T1→T5), test-first, within the two authorized code files
plus this report. No stop condition was encountered: ledger hash held, `.claude/` clean, no `M`, no SP-6, no value
promoted, no Rung-2 row, no ceiling advance, no fresh evidence, no Kaggle/episode ingest, no runtime-agent /
gameplay / FunSearch surface, and `--promotion-check` is parity-or-stricter with `--validate` by construction. The
existing 12 + block-13 checks remained green throughout.

One in-scope documentation touch beyond the driver itself: a single CLI-synopsis line was added to the module
docstring (`analysis/evidence_summary.py:45`) plus a one-line clarification of exit 3's promotion-mode case
(`:46-48`), to keep the module's own documented CLI list complete. This changes no behaviour and no exit code.

---

> **Reporting language (binding, per sprint-plan §"Implementation report requirements").** `--promotion-check`
> added and tested: it re-reads the summary from disk, runs `validate_summary` wholesale, hard-fails empty/absent
> `hashes` at exit 3, and passes at exit 0 only when the summary is clean **and** `hashes` is non-empty.
> Generate-mode empty-`hashes` warning stayed exit 0; `--validate` empty-`hashes` acceptance stayed exit 0; the
> `0/1/2/3` exit contract held; `--promotion-check` writes nothing and `docs/ledger.md` is byte-unchanged
> (`2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`); `docs/claim-ceiling.md` is untouched; no value promoted; no `M`;
> no SP-6; no Rung-2 row; no fresh evidence. **The gate is closed as hardening/preparation, not admission. Rung 1
> held. The Rung-2 attempt is deferred to Cycle-007 behind a separate explicit operator gate.**
