# Cycle-008 Sprint S03 — Ledger-Row Validator (gate-only): Implementation Report

> Sprint artifact (S03 — Ledger-row validator). Status: **IMPLEMENTATION COMPLETE — awaiting
> `/review-sprint` → `/audit-sprint` → operator acceptance.** This S03 pass lands `analysis/ledger_validate.py`:
> a stdlib-only, offline, **read-only** governance gate that content-checks `docs/ledger.md` (18-column schema
> verbatim, append-only via the `git show HEAD:docs/ledger.md` baseline per RN-1, single-regime-per-row,
> SHA-256-shaped digests) and anchors `docs/claim-ceiling.md` at **Rung 2** — **accepting the current real
> artifacts**, **rejecting malformed rows and unauthorized governance movement**, and **writing nothing**. It
> implements **no** runtime agent / heuristic / value model / search loop, runs **no** eval, creates **no** fresh
> evidence, writes **no** SP-6 / ledger row, advances **no** claim ceiling, and selects/freezes **no** Rung-3
> target / candidate / numeric margin `M` / `K` / `n` / regime id / feature family. It edits **no** `.claude/` and
> cleans/stages **no** State-Zone dirt. S01/S02 diagnostic/sanitizer code is **untouched**.
>
> **Sanitized note.** No raw traces, simulator logs, deck lists, card IDs/names, Pokémon Elements, Competition
> Data, Daily-Top-Episodes, Kaggle episode data, Discord/peer screenshots, run-dir dumps, PDFs/CSVs, `deck.csv`,
> `cg/`, raw evidence rows, dispersion/band/win-rate values, or any inferential statistic appears here. **No
> numeric governance margin `M` is chosen or stated** — `M` appears only where the text *names a class the gate
> rejects*. No forbidden agent word (*strong / competitive / optimal / calibrated / complete*) is used to describe
> agent evidence. The committed synthetic fixtures carry only placeholder ids/hashes (`run-syn-*`, `regime-syn-a`,
> repeated-hex tokens) — no real run data, no card/deck content.

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-008 / Sprint **S03 — Ledger-row validator (gate-only)** |
| **Type** | App-Zone code/test (behind the OD-C8-6 OA-2 build gate, scoped to `analysis/` + `tests/`) |
| **Date** | 2026-06-21 |
| **Status** | **IMPLEMENTATION COMPLETE** — review/audit/acceptance pending; **not committed or pushed** in this pass |
| **Build-time HEAD** | `d6a7cf96c92a423134b67dc32b29966017157296` — *feat: add Cycle-008 S02 diagnostic sanitizer* (== `origin/main`; not ahead/behind) |
| **Sprint-plan citation anchor** | `f2330d1` (plan authoring commit); the S03 block (`03-sprint-plan.md:561-640`) + RN-1 (`:131-165`) re-validated at build-time HEAD (see §6) |
| **Operator gate** | **OD-C8-6 OPEN** — the OA-2-class build gate for the Cycle-008 App-Zone code lane; this `/implement` request is **S03 only** |
| **Claim ceiling (at S03)** | **Rung 2 — "beats random-legal"**; **held and preserved** (ceiling artifact byte-unchanged) |
| **Ledger invariant** | `docs/ledger.md` byte-unchanged; `git hash-object = 7da7e9a8dbed6561669d1569445eb9fe67a953fb` |
| **Ceiling invariant** | `docs/claim-ceiling.md` byte-unchanged; `git hash-object = 3d99759b919f7d75bc41ea81cd82e5f1fb974be7` |

---

## 1. Sprint goal & scope

**Goal (sprint plan `03-sprint-plan.md:563-566`).** "Land `analysis/ledger_validate.py` — a gate-only validator
that content-checks `docs/ledger.md` against the **18-column schema verbatim**, append-only discipline (via the
`git show HEAD:docs/ledger.md` baseline, RN-1), single-regime-per-row, and SHA-256-shaped hash references —
**accepting the current valid ledger**, **rejecting malformed rows**, and **writing nothing**."

The binding `/implement` request broadens S03's gate to also anchor `docs/claim-ceiling.md` at **Rung 2**, support
opt-in pinned-hash invariants, and reject unauthorized governance movement (Rung-3 / SP-6 / value-promotion) — all
consistent with the S03 goal of "a governance gate before any future ledger row or claim-ceiling movement is
trusted." **Scope.** MEDIUM (S03.1–S03.4, `03-sprint-plan.md:613-624`). App-Zone code/test only. The S04
governance docs and S05 closeout are out of scope and absent.

---

## 2. What was built

### 2.1 `analysis/ledger_validate.py` (NEW) — read-only ledger + claim-ceiling gate

A self-contained, stdlib-only module (only `argparse`, `re`, `subprocess`, `sys`, `pathlib`). It factors into
**pure functions** (no I/O — fed strings directly by tests) and a thin **read-only I/O layer**:

- **18-column schema pinned verbatim** ([analysis/ledger_validate.py:92](../../../analysis/ledger_validate.py),
  `LEDGER_COLUMNS`) from `docs/ledger.md:9` — the current tracked ledger **is** the schema authority (no new
  schema invented). `N_COLUMNS == 18`.
- **`validate_ledger_structure(text)`** ([:176](../../../analysis/ledger_validate.py)) — one consistent header
  matching the schema verbatim (header edit ⇒ exit 2); a separator row present and 18-wide; every data row exactly
  18 cells (wrong width ⇒ exit 2); non-empty `claim_ceiling` (empty ⇒ exit 3); exactly one regime per `regime_id`
  cell (two regimes ⇒ exit 2, cross-regime); `git_rev` is a git digest and any `sha256` citation is 64-hex
  (non-digest ⇒ exit 3). The **"see cited summary"** by-reference convention in the numeric metric columns is
  **accepted** (SDD-C8-7; the validator requires no numeric values there).
- **`classify_append(baseline, worktree)`** ([:249](../../../analysis/ledger_validate.py)) — LF-normalized
  byte-prefix check (RN-1): `equal` / `append` (committed content is a byte-identical prefix; returns the appended
  tail) / `edit` (a prior committed line changed ⇒ exit 3).
- **`scan_unauthorized_governance(text)`** ([:263](../../../analysis/ledger_validate.py)) — applied **only to the
  appended delta** (the committed history is the authorized truth and is never re-judged): an appended `Rung 3+` /
  `SP-6` / `value promotion` / `claim advance` token is rejected (exit 3). The authorized `Rung 1` / `Rung 2`
  framing is **not** matched.
- **`validate_claim_ceiling(text)`** ([:274](../../../analysis/ledger_validate.py)) — the standing ceiling must
  read **Rung 2** (anything else, or an unreadable posture ⇒ exit 3, fail-closed).
- **Read-only I/O layer** — `git_show` ([:303](../../../analysis/ledger_validate.py)) and `git_hash_object`
  ([:319](../../../analysis/ledger_validate.py)) are `subprocess` reads forced to `encoding="utf-8"` (load-bearing:
  the default locale decode mangles the ledger's UTF-8 em-dashes on Windows and breaks the byte-prefix check). If
  the committed baseline is unreachable, the append-only check **fails closed** (exit 1), never a silent exit 0.
- **`# loa:shortcut` (RN-1 baseline mechanism)** — the git-`HEAD` baseline is recorded in-code with its
  committed-manifest upgrade trigger ([analysis/ledger_validate.py:163](../../../analysis/ledger_validate.py), the
  escape-aware-split note; the git-baseline rationale is the RN-1 design itself, §4.2 of the module docstring).
- **CLI** ([:419](../../../analysis/ledger_validate.py), `main`) — supports both the sprint-plan positional shape
  `python analysis/ledger_validate.py [docs/ledger.md]` and the flag shape
  `--ledger … --claim-ceiling …`, plus `--baseline-ref` and opt-in `--expected-ledger-hash` /
  `--expected-ceiling-hash`. Exit set `0/1/2/3` (the max severity among triggered violations; every failure is
  printed).
- **Pinned S03-start invariants exported** ([:86](../../../analysis/ledger_validate.py)) — `LEDGER_HASH_S03_START`
  / `CEILING_HASH_S03_START`, off by default so the gate stays reusable for legitimate future appends.

### 2.2 Committed synthetic fixtures (`tests/fixtures/ledger_validate/`)

Two minimal, synthetic, safe fixtures (per the "synthetic, minimal" instruction):
`valid_ledger.md` (the 18-column house format, two rows — a concrete-numeric Rung-1 row and a "see cited summary"
by-reference Rung-2 row) and `valid_ceiling.md` (a Rung-2 standing posture). Ids/hashes are placeholder tokens
(`run-syn-*`, `regime-syn-a`, repeated-hex). Every reject class (header/separator/column edits, empty ceiling,
cross-regime, non-SHA-256 digest, non-digest `git_rev`, prior-row edit, Rung-3/SP-6/value-promotion appends,
claim-ceiling advance) is **derived in-test** from this single valid base by labeled one-cell mutation — the
`trace_diagnostic` `_reject` pattern — keeping the fixture subtree minimal while covering each class.

### 2.3 `tests/test_ledger_validate.py` (NEW) — stdlib plain-Python, 78 checks

House style preserved (`check()` / `_FAILURES` / `main()` -> exit 0/1, mirroring `tests/test_trace_diagnostic.py`).
The append-only baseline is **injected** (a sentinel parameter on `validate()`), so every append/edit/equal and
exit-code case is deterministic regardless of the fixtures' git commit-state. All 78 checks pass; nothing reads the
gitignored `runs/` tree.

---

## 3. Commands run & results

All run at build-time HEAD `d6a7cf9`. Smallest-sufficient first, then the relevant regression checks.

| # | Command | Result |
|---|---|---|
| 1 | `python analysis/ledger_validate.py docs/ledger.md` | exit **0** — current real ledger + claim ceiling valid |
| 2 | `python analysis/ledger_validate.py --ledger docs/ledger.md --claim-ceiling docs/claim-ceiling.md --expected-ledger-hash 7da7e9a8… --expected-ceiling-hash 3d99759b…` | exit **0** — pinned-hash invariants confirmed |
| 3 | `python tests/test_ledger_validate.py` | exit **0** — **78 checks pass, 0 FAIL** |
| 4 | `python tests/test_import_direction.py` | exit **0** — runtime/offline separation intact |
| 5 | `python tests/test_trace_diagnostic.py` | exit **0** — S01/S02 unchanged (no regression) |
| 6 | `python tests/test_evidence_summary.py` | exit **0** — no regression |
| 7 | `python tests/test_smokes.py` | exit **0** — **72 tests OK** (no regression) |
| 8 | `python eval/hygiene_check.py --paths <4 touched tracked artifacts, per-file>` | exit **0** — clean; no Competition-Data paths |
| 9 | `git hash-object docs/ledger.md` | `7da7e9a8…` (byte-unchanged, before and after a run — #1/#3 prove read-only) |
| 10 | `git hash-object docs/claim-ceiling.md` | `3d99759b…` (byte-unchanged) |
| 11 | `git status --porcelain .claude/` | empty (System Zone clean) |
| 12 | `git diff --cached --name-only` | empty (nothing staged; protected dirt + S03 changes left unstaged) |

---

## AC Verification

Each `/implement` acceptance criterion (the binding S03 contract) is quoted verbatim, with status and file:line
evidence. (Sprint-plan ACs `03-sprint-plan.md:587-611` map onto these.)

1. "`analysis/ledger_validate.py` exists." — **✓ Met.** [analysis/ledger_validate.py:1](../../../analysis/ledger_validate.py).
2. "It is stdlib-only and offline." — **✓ Met.** Imports `argparse`, `re`, `subprocess`, `sys`, `pathlib`
   ([:60-65](../../../analysis/ledger_validate.py)); `subprocess` git reads are local (no network);
   `test_import_direction` exits 0 and the module imports only stdlib + analysis-zone (Command #4;
   [tests/test_ledger_validate.py](../../../tests/test_ledger_validate.py) `t_import_direction`).
3. "It is read-only and performs no writes." — **✓ Met.** `t_writes_nothing`
   ([tests/test_ledger_validate.py](../../../tests/test_ledger_validate.py)) source-greps the module for **no**
   `write_text`/`write_bytes`/`.write(`/`open(`/`mkdir`/`unlink`/`rename`/`shutil`/`os.remove` call and **no** git
   `add`/`commit`/`push`/`reset`/`checkout`/`stash`/`rm`/`mv` subcommand; the only git reads are `show` +
   `hash-object`. Command #9 shows the ledger hash unchanged before/after a run.
4. "It validates the current real `docs/ledger.md`." — **✓ Met.** Command #1 exits 0;
   `t_real_ledger_validates` (positional, flag, and default CLI shapes all exit 0).
5. "It validates the current real `docs/claim-ceiling.md` and confirms Rung 2 remains held." — **✓ Met.**
   `validate_claim_ceiling` ([analysis/ledger_validate.py:274](../../../analysis/ledger_validate.py)) reads the
   standing ceiling at `docs/claim-ceiling.md:10`; `t_real_claim_ceiling_rung2` asserts no violations.
6. "It compares the working-tree ledger against `git show HEAD:docs/ledger.md` …" — **✓ Met.** `validate`
   ([:347](../../../analysis/ledger_validate.py)) fetches the baseline via `git_show`
   ([:303](../../../analysis/ledger_validate.py)); `classify_append` ([:249](../../../analysis/ledger_validate.py))
   does the LF-normalized byte-prefix comparison (RN-1).
7. "It allows equality." — **✓ Met.** `classify_append(BASE, BASE) == ("equal", "")` (`t_equality_passes`).
8. "It allows pure append-only additions only when prior committed content remains byte-identical as a prefix and
   the appended row is schema-valid." — **✓ Met.** `t_pure_append_passes`: a schema-valid appended row classifies
   `append`, the appended ledger stays structurally valid, the delta carries no unauthorized governance, and
   `validate()` exits 0.
9. "It rejects prior-row edits." — **✓ Met.** `t_prior_row_edit_fails`: an edited prior row classifies `edit` and
   `validate()` exits 3.
10. "It rejects header/separator edits." — **✓ Met.** `t_structural_rejections`: a header edit and a separator edit
    each yield an exit-2 structural violation; the header edit also fails `validate()` (it is additionally an
    append-only edit).
11. "It rejects malformed rows." — **✓ Met.** `t_structural_rejections`: a wrong-column-count row ⇒ exit 2; an
    empty `claim_ceiling` ⇒ exit 3; a non-SHA-256 digest citation ⇒ exit 3; a non-digest `git_rev` ⇒ exit 3.
12. "It rejects unauthorized claim-ceiling advance." — **✓ Met.** `t_claim_ceiling`: a standing ceiling reading
    Rung 3 ⇒ exit 3 (`validate_claim_ceiling`, [:274](../../../analysis/ledger_validate.py)).
13. "It rejects unauthorized Rung-3 / SP-6 / value-promotion semantics." — **✓ Met.** `t_unauthorized_governance`:
    `scan_unauthorized_governance` flags an appended Rung-3 advance, SP-6 promotion, and value promotion (and does
    **not** flag the authorized Rung-1/Rung-2 framing); each ⇒ `validate()` exit 3.
14. "It fails closed when the committed baseline cannot be read." — **✓ Met.** `t_unreachable_baseline_fails_closed`:
    an unreachable baseline ⇒ exit 1 (never 0), with the RN-1 input-failure reason.
15. "Synthetic tests cover valid and invalid cases." — **✓ Met.** §2.2/§2.3; 78 checks (Command #3).
16. "Tests are stdlib-only and independent of local gitignored `runs/`." — **✓ Met.** `t_runs_independence`:
    fixtures live under `tests/`, not `runs/`; per-file hygiene-clean. No test references `runs/`.
17. "`python tests/test_import_direction.py` passes." — **✓ Met.** Command #4 (exit 0).
18. "Relevant S03 unit tests pass." / "Relevant regression smoke tests pass." — **✓ Met.** Commands #3 (78 S03
    checks), #5 / #6 / #7 (S01/S02, evidence-summary, smokes — no regression).
19. "`eval/hygiene_check.py` is clean on touched tracked artifacts, with per-file coverage for fixture files." —
    **✓ Met.** Command #8 (4 files, per-file); `t_runs_independence` additionally asserts each fixture path is
    hygiene-clean.
20. "`docs/ledger.md` remains hash `7da7e9a8…` / `docs/claim-ceiling.md` remains `3d99759b…` / Claim ceiling
    remains Rung 2 / `.claude/` remains clean / protected State-Zone dirt remains unstaged." — **✓ Met.**
    Commands #9–#12 and §5.
21. "No S04/S05 work … No Rung-3 attempt/target/candidate/comparison-budget/K/n/regime/feature family …
    No SP-6, ledger row, value promotion, or claim-ceiling advance occurs." — **✓ Met (non-occurrence).** Only
    `analysis/ledger_validate.py` + `tests/` + this report were authored; the validator is read-only and the
    invariants in #20 hold. The module *names* the forbidden classes only to reject them.
22. "`/review-sprint` + `/audit-sprint` both pass; operator accepts." — **⏸ Pending** (downstream gates; not part
    of this `/implement` pass).

---

## 5. Changed files & final status

**New — all under the sanctioned `analysis/` + `tests/` + this cycle's `docs/` lane:**

- `analysis/ledger_validate.py` (NEW — read-only ledger + claim-ceiling gate)
- `tests/test_ledger_validate.py` (NEW — 78 stdlib checks)
- `tests/fixtures/ledger_validate/valid_ledger.md`, `tests/fixtures/ledger_validate/valid_ceiling.md` (NEW — synthetic)
- `docs/cycles/cycle-008/07-s03-implementation-report.md` (NEW — this file)

**Final `git status --porcelain`** (changes left unstaged; not committed or pushed):

```
 M .beads/issues.jsonl
 M grimoires/loa/NOTES.md
?? analysis/ledger_validate.py
?? docs/cycles/cycle-008/07-s03-implementation-report.md
?? grimoires/loa/README.draft.md
?? tests/fixtures/ledger_validate/
?? tests/test_ledger_validate.py
```

`.beads/issues.jsonl`, `grimoires/loa/NOTES.md`, and `grimoires/loa/README.draft.md` remain the pre-existing
State-Zone dirt — **modified/untracked-unstaged, not edited, not staged, not cleaned** by this pass.

---

## 6. Invariant & citation-anchor verification

- **HEAD / origin parity:** `git rev-parse HEAD == origin/main == d6a7cf96c92a423134b67dc32b29966017157296`.
- **Ledger invariant:** `git hash-object docs/ledger.md = 7da7e9a8dbed6561669d1569445eb9fe67a953fb` (byte-unchanged,
  before and after running the gate — the read-only proof).
- **Ceiling invariant:** `git hash-object docs/claim-ceiling.md = 3d99759b919f7d75bc41ea81cd82e5f1fb974be7`
  (byte-unchanged); **claim ceiling remains Rung 2** (`docs/claim-ceiling.md:10`).
- **System Zone:** `git status --porcelain .claude/` empty; **nothing staged** (`git diff --cached --name-only` empty).
- **Citation anchors re-validated at build-time HEAD (NFR-12):** sprint-plan S03 block (`03-sprint-plan.md:561-640`),
  RN-1 (`:131-165`), the 18-column schema list (`:574-577`); the schema authority `docs/ledger.md:9`; the standing
  ceiling line `docs/claim-ceiling.md:10`; the validator-family exit-set shape (`analysis/trace_diagnostic.py:56-57`)
  — all accurate at `d6a7cf9`.

---

## 7. Known limitations / carry-forward

- **Gate-only.** The validator reports whether the ledger *mechanics* are valid; it scores no agent, generates no
  evidence, determines no Rung-3 readiness, and blesses no rung (OD-C8-2). The S04 governance docs and S05 closeout
  are out of scope and absent.
- **Unauthorized-governance scope = the appended delta.** The scan deliberately exempts the committed history (the
  authorized truth): the real row 3 legitimately cites `SP-6` / `Rung 2` / `candidate` / `pre-registration`, so a
  whole-file scan would reject the real ledger. The gate rejects only *new* movement in an appended row. A future
  cycle that authorizes a new rung adjusts this posture (the markers are a small, auditable table at
  [analysis/ledger_validate.py:125](../../../analysis/ledger_validate.py)).
- **Pinned-hash invariants are opt-in.** `--expected-*-hash` is off by default so a legitimate future append (which
  changes the hash) still passes the structural/append-only gate; the S03-start pins are exported as constants and
  exercised by Command #2 / `t_pinned_hash_invariants`.
- **Markdown-cell parse shortcut.** `_split_cells` assumes no escaped `\|` inside a cell (the house ledger format
  uses none); the upgrade trigger is recorded in-code ([analysis/ledger_validate.py:162](../../../analysis/ledger_validate.py)).

**Stop point.** S03 implementation only. No review, audit, S04, or S05 work performed; nothing committed or pushed.
