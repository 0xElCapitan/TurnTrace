# Cycle-006 Review Report — Sprint 01: Promotion-Check Hardening (`--promotion-check`)

> Review artifact (written under `/review-sprint`). **Pure review — no code edited, no fix applied, nothing
> staged/committed/pushed, no audit/closeout artifact created, no `.claude/` mutation, no State-Zone file cleaned
> or staged.** Independent verification: every command was re-run fresh and every behavioural claim was
> reproduced from independently-derived synthetic fixtures rather than trusting the implementation report.

## Verdict: **PASS WITH NOTES**

Sprint 01 meets all eight acceptance criteria, all required commands pass, the ledger invariant holds
(`2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`), the claim ceiling is untouched, Rung 1 is held, no forbidden path
changed, no scope creep occurred, no State-Zone file was staged, and nothing was committed or pushed. The "NOTES"
are **non-blocking** advisory observations (test-coverage gaps for properties that are nonetheless verified
correct, and a cosmetic docstring realignment). None require a fix to proceed to `/audit-sprint`.

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-006 / Sprint 01 — Promotion-Check Hardening |
| **Reviewed at HEAD** | `082a953923e5fd8e4643171466cfcc23f413a8dd` (== `origin/main`); unstaged working tree |
| **Verdict** | **PASS WITH NOTES** |
| **Ledger invariant** | `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` — held (verified before & after every check) |
| **Claim ceiling** | Rung 1 held; `docs/claim-ceiling.md` untouched |
| **New review artifact** | this file only (`05-review-report.md`) |

---

## 1. Files reviewed

**Planning authorities (read, not changed):**
`docs/cycles/cycle-006/01-prd.md`, `02-sdd.md`, `03-sprint-plan.md`, `04-implementation-report.md`.

**Implementation under review (unstaged):**
`analysis/evidence_summary.py`, `tests/test_evidence_summary.py`, `docs/cycles/cycle-006/04-implementation-report.md`.

**Reference (read for parity/import checks):** `eval/hygiene_check.py`, `tests/test_import_direction.py`.

## 2. Diff summary

| File | Added / Deleted | Nature |
|---|---|---|
| `analysis/evidence_summary.py` | **+73 / −4** | Additive: new `_run_promotion_check` driver + `--promotion-check` argparse arg + dispatch branch + 1 docstring CLI-synopsis line. The 4 "deletions" are 3 reformatted docstring lines (CLI synopsis + exit-3 description) and 1 changed dispatch comment (`# ---- validate mode ----` → promotion-check/validate block). |
| `tests/test_evidence_summary.py` | **+77 / −1** | Additive: `promotion_check_file_exit` helper + block 14 (14a–14f). The 1 "deletion" is the `main()` summary line (now names block 14). |
| `docs/cycles/cycle-006/04-implementation-report.md` | new (268 lines, untracked) | Implementation report. |

**Behaviour-preservation confirmed by absence from the diff.** `validate_summary`, `_run_validate`,
`_refuse_tracked_out`, `build_summary`, `render_json`, the generate-mode empty-`hashes` WARNING block,
`_collect_regime_ids`, and `_enforce_hashes_digest` do **not** appear in the diff — they are byte-unchanged. The
existing checks 1–13 in the test file are likewise absent from the diff (unmodified). The new driver
(`analysis/evidence_summary.py:511-566`) *reuses* `_collect_regime_ids` (:532) and `validate_summary` (:540)
wholesale and adds exactly one rule (empty/absent-`hashes` precheck, :556-561).

## 3. Commands run and exit codes (independently re-run)

| # | Command | Result | Expected | ✓ |
|---|---|---|---|---|
| 1 | `python tests/test_evidence_summary.py` | **0** | 0 (12 + 13a–13l + 14a–14f green) | ✓ |
| 2 | `python tests/test_import_direction.py` | **0** | 0 | ✓ |
| 3 | `python eval/hygiene_check.py --paths analysis/evidence_summary.py tests/test_evidence_summary.py docs/cycles/cycle-006/04-implementation-report.md` | **0** | 0 | ✓ |
| 4 | `git hash-object docs/ledger.md` | `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` | identical | ✓ |
| 5 | `git diff --exit-code -- docs/ledger.md` | **0** | 0 | ✓ |
| 6 | `git diff --exit-code -- docs/claim-ceiling.md` | **0** | 0 | ✓ |
| 7 | `git status --porcelain .claude/ frozen/ runs/ agents/ sim/` | (empty) | empty | ✓ |
| 8 | `git diff --cached --name-only` | (empty) | empty | ✓ |

Forbidden-path diff sweep (`docs/ledger.md`, `docs/claim-ceiling.md`, `.claude`, `analysis/aggregate.py`,
`analysis/dispersion_report.py`, `eval`, `agents`, `sim`, `frozen`, `runs`): **all clean**.
`analysis/evidence_summary_validate.py` absent (no second module); no new/tracked `*.schema.json`; no
dependency/manifest change.

## 4. Independent behaviour checks (fresh synthetic fixtures, not the implementer's)

### 4.1 Exit-code contract & parity matrix (`--promotion-check` vs `--validate`)

| Input | `--promotion-check` | `--validate` | Relationship |
|---|---|---|---|
| clean, non-empty `hashes` | **0** | **0** | same |
| structurally-valid **empty** `hashes` `{}` | **3** | **0** | **intended delta** (stricter) |
| **absent** `hashes` (key missing) | **3** | **0** | **intended delta** (stricter) |
| leak — unknown/allow-list field | **3** | **3** | same |
| leak — inferential term | **3** | **3** | same |
| leak — affirmative forbidden word | **3** | **3** | same |
| leak — cross-regime field | **3** | **3** | same |
| leak — non-digest `hashes` value | **3** | **3** | same |
| mixed-regime | **2** | **2** | same |
| unreadable input path | **1** | (n/a) | reuses `_run_validate` read-fail block |

**Parity-or-stricter property holds.** Every input maps identically under both modes **except** empty/absent
`hashes` (validate `0` → promotion `3`). No input that `--validate` rejects (exit 2 or 3) is accepted (exit 0) by
`--promotion-check`. The accepted set of `--promotion-check` is a strict subset of `--validate`'s accepted set —
conservative-only confirmed across **all** rejection classes (not just the one the tests probe).

### 4.2 Behavioural focus questions

- **Wholesale `validate_summary`?** Yes — `analysis/evidence_summary.py:540` calls `validate_summary(summary)`
  unchanged; full hardened semantics inherited. Confirmed empirically: every leak class above rejects identically
  to `--validate`.
- **Empty/absent `hashes` hard-fails only in promotion mode?** Yes — precheck at :556-561 lives only in
  `_run_promotion_check`; `--validate` returns exit 0 for the same empty/absent input (§4.1).
- **`--validate` empty-`hashes` stayed exit 0?** Yes (§4.1; test 14b′).
- **Generate-mode empty-`hashes` warning stayed exit 0?** Yes — independently reproduced (generate from
  `manifest_hash=""` run dirs → exit 0 with stderr WARNING); the WARNING block is unchanged in the diff; tests 13j
  (preserved) and 14d (new) both green.
- **Exit-code contract stayed 0/1/2/3?** Yes — all five values observed (0,1,2,3 for promotion-check; 2/3 shared);
  no new code introduced.
- **Writes nothing / promotes nothing?** Yes — `_run_promotion_check` has no `open(...,'w')`/`write_text`/`mkdir`
  in the diff; independent run created no new file and left `docs/ledger.md` byte-identical in-process; never
  reaches `_refuse_tracked_out`.
- **Reads no `hashes.txt` / sidecar?** Yes — source-grep test 13l (`"hashes.txt" not in src`) green; test 4
  (`"trace"`/`"traces"` absent) green; the new code's only read is `p.read_text(...)` of the passed summary.

## 5. Acceptance criteria (AC-1 … AC-8)

| AC | Criterion (verbatim, sprint-plan §"Acceptance Criteria") | Status | Evidence |
|---|---|---|---|
| **AC-1** | "`--promotion-check` on a clean, non-empty-`hashes`, schema-conforming summary → exit 0." | ✓ Met | §4.1 (good→0); test 14a (`tests/test_evidence_summary.py:386`); driver pass `analysis/evidence_summary.py:563-566`. |
| **AC-2** | "`--promotion-check` on a structurally-valid but empty-`hashes` summary → exit 3 (non-zero, fail-closed; CF-1 / OD-C5-2 floor)." | ✓ Met | §4.1 (empty→3); test 14b (`:397`); precheck `analysis/evidence_summary.py:556-561`. |
| **AC-3** | "`--promotion-check` on a summary carrying any forbidden field/value/word → exit 3 (full validator re-run). A mixed-regime summary → exit 2." | ✓ Met | §4.1 (all leak classes→3; mixed→2); tests 14c (`:412`), 14f (`:443`); driver :540 / :532. |
| **AC-4** | "generate-mode still emits the empty-`hashes` WARNING at exit 0; `--validate` still accepts a structurally-valid empty `hashes` at exit 0; the 0/1/2/3 contract holds (no new exit code)." | ✓ Met | §4.2; tests 14d (`:420`), 14b′ (`:402`); generate WARNING + `_run_validate` unchanged in diff. |
| **AC-5** | "`--promotion-check` writes nothing; `docs/ledger.md` byte-unchanged before/after; no tracked `docs/` write." | ✓ Met | §4.2 (writes-nothing); test 14e (`:433-437`); `git diff --exit-code -- docs/ledger.md` = 0; hash unchanged. |
| **AC-6** | "each behaviour has ≥1 runnable regression check; all existing 12 + block-13 checks remain green; `test_import_direction` exit 0; `hygiene_check --paths …` exit 0." | ✓ Met | §3 cmds 1–3 all exit 0; block 14 runnable & green; checks 1–13 unmodified (diff). |
| **AC-7** | "posture held (hard): Rung 1; claim-ceiling untouched; no `M`; no SP-6; no value promotion; no Rung-2 row; no fresh evidence; no `.claude/` drift; State-Zone files unstaged; no second module; no `*.schema.json`; no dependency; no ledger write." | ✓ Met | §6; ledger/claim-ceiling clean; forbidden-path sweep clean; State-Zone unstaged. |
| **AC-8** | "lands only through `/implement → /review-sprint → /audit-sprint → operator acceptance`." | ⏸ In progress (by design) | `/implement` done; this is `/review-sprint`; `/audit-sprint` next. Nothing committed/pushed. |

The implementation report's own `## AC Verification` section (`04-implementation-report.md`) is present and walks
AC-1…AC-8 with file:line evidence — satisfying the cycle-057 AC-Verification gate. This review independently
re-derived each verdict above rather than copying the report's.

## 6. Posture / invariant verification (binding non-goals)

| Posture constraint | Result |
|---|---|
| Rung 1 held; ledger byte-unchanged (`2a2f1c2…`) | ✓ |
| `docs/claim-ceiling.md` untouched | ✓ |
| No numeric `M` anywhere in changed files | ✓ (no `M`-selection; fixtures are exit-code probes only) |
| No SP-6 / no value promoted to tracked status | ✓ (`--promotion-check` returns an exit code only; writes nothing) |
| No Rung-2 ledger row / no claim-ceiling advance | ✓ (ledger & claim-ceiling diffs clean) |
| No fresh evidence / no eval run / no K-batch / no run dir | ✓ (tests use synthetic `make_run_dir` temp fixtures only) |
| No PASS/FAIL/INCONCLUSIVE verdict applied | ✓ (no verdict logic added) |
| No runtime-agent / gameplay / FunSearch / RL / self-play / deck-optimizer / value-model / search / MCTS / tournament / dashboard | ✓ (none in diff; imports unchanged) |
| No Daily-Top-Episodes / Kaggle ingest | ✓ |
| No raw Competition Data / Pokémon Elements / traces / deck lists / simulator logs in tracked files | ✓ (hygiene exit 0; synthetic fixtures; only forbidden-looking string is the synthetic inferential probe in 14c, which tests *rejection*) |
| No second validator module / `*.schema.json` / dependency | ✓ |
| `.claude/` untouched; State-Zone (`.beads/issues.jsonl`, `NOTES.md`) pre-existing-dirty & unstaged | ✓ (State-Zone diffs contain only Cycle-003/earlier content; zero cycle-006/promotion-check references — the sprint and the retrospective postlude wrote nothing to them) |

## 7. Adversarial Analysis

### Concerns identified (non-blocking)

1. **Absent-`hashes` is not regression-tested** — block 14b covers empty `{}` only; the "absent key" branch of
   the precheck (`analysis/evidence_summary.py:556`, `not isinstance(h, dict)`) has no pinned test. The behaviour
   is **verified correct here** (§4.1 absent→3), and AC-2 as written specifies *empty*, so this is a robustness
   gap, not an AC miss. *Recommendation (advisory, Cycle-007):* add a 1-line `14b″` asserting a summary with no
   `hashes` key → exit 3, so the absent branch can't silently regress.
2. **No regression test for exit 1 (unreadable input) or the both-flags precedence** under `--promotion-check`.
   The exit-1 path is a verbatim copy of `_run_validate`'s read-failure block (also untested in-suite) and the
   precedence is documented in-code; both were verified manually (§4.1, and impl-session demo). Non-blocking.
3. **Cosmetic docstring realignment** — the `generate:`/`validate:` CLI-synopsis lines were re-indented for
   alignment (`analysis/evidence_summary.py:43-44`), slightly beyond the strictly-minimal diff (Karpathy
   "surgical changes"). Same file, documentation-only, improves the rendered CLI list; acceptable.
4. **Shallow "writes-nothing" assertion** — test 14e snapshots `tmp.iterdir()` (top-level, non-recursive). It is
   adequate *because* the driver has zero write surface (confirmed in the diff), but the assertion alone would
   miss a hypothetical write into a subdirectory. Non-blocking.

### Assumption challenged

- **Assumption:** a non-`dict` `hashes` value never reaches the promotion precheck (so the precheck need only
  assert non-emptiness). **Risk if wrong:** a non-dict `hashes` could slip the "non-empty" intent. **Finding:**
  the assumption is *defensively neutralised* — `validate_summary` already rejects a non-dict `hashes`
  (`:417-418`, exit 3 at step 3), **and** the precheck's `isinstance(h, dict)` guard fails closed even if that
  ever changed. No action required; the guard is correct fail-closed practice, not dead code.

### Alternative not considered

- **Alternative:** emit a stderr note when both `--promotion-check` and `--validate` are supplied (SDD §3.1: the
  impl "may note the redundancy on stderr"). The implementation silently prefers the stricter mode.
  **Tradeoff:** a note aids a user who passed both; silence is less noisy. **Verdict:** current approach
  justified — the SDD made the note optional, the precedence is documented in-code (`:591-594`), and stricter-wins
  is the correct default for a gate. Not a defect.

## 8. Issues / required fixes

- **Blocking issues:** none.
- **Required fixes:** none.
- **Advisory notes (optional, may defer to Cycle-007):** Concern 1 (absent-`hashes` regression test) is the
  highest-value follow-up; Concerns 2–4 are minor. None block audit or operator acceptance.

## 9. Accuracy of the implementation report

`04-implementation-report.md` is **accurate**: its file-change list, exit codes, line anchors (spot-checked:
`_run_promotion_check:511`, precheck `:556`, arg `:582`, dispatch `:597-598`), parity claim, and posture
confirmations all match independent reality. Its claim that empty *and absent* `hashes` both hard-fail is
correct (independently verified, §4.1), even though the shipped regression block tests only the empty case
(Concern 1). The report's binding "hardening/preparation, not admission" language is consistent with the diff.

## 10. New review artifact confirmation

This `docs/cycles/cycle-006/05-review-report.md` is the **only** new artifact created by the review. No code was
edited, no fix applied; `06-audit-report.md` and `07-closeout.md` were **not** created (those belong to
`/audit-sprint` and closeout). No `engineer-feedback.md` / `sprint.md` checkmark mutation (TurnTrace uses the
`docs/cycles/` artifact convention, not the default Loa `grimoires/loa/a2a/` paths).

## 11. Final git status summary

```
 M .beads/issues.jsonl                                  ← pre-existing State-Zone; unstaged, untouched by sprint
 M analysis/evidence_summary.py                          ← authorized; unstaged
 M grimoires/loa/NOTES.md                                ← pre-existing State-Zone; unstaged, untouched by sprint
 M tests/test_evidence_summary.py                        ← authorized; unstaged
?? docs/cycles/cycle-006/04-implementation-report.md     ← authorized (implementation report)
?? docs/cycles/cycle-006/05-review-report.md             ← this review report
```

Nothing staged (`git diff --cached --name-only` empty). Nothing committed or pushed.

---

> **Decision (binding):** **PASS WITH NOTES.** `--promotion-check` re-reads from disk, runs `validate_summary`
> wholesale, inherits mixed-regime exit 2, hard-fails empty/absent `hashes` at exit 3, and passes at exit 0 only
> when clean and non-empty-`hashes` — parity-or-stricter with `--validate` confirmed across all rejection classes.
> Generate-mode and `--validate` empty-`hashes` behaviour stayed exit 0; the 0/1/2/3 contract held; the gate
> writes nothing and promotes nothing; `docs/ledger.md` (`2a2f1c2…`) and `docs/claim-ceiling.md` are untouched;
> Rung 1 held; no `M`, no SP-6, no Rung-2 row, no fresh evidence, no forbidden-path change, no scope creep. The
> gate is hardening/preparation, not admission; the Rung-2 attempt remains deferred to Cycle-007 behind a separate
> explicit operator gate. **Cleared to proceed to `/audit-sprint`.** The four advisory notes are non-blocking and
> require no change to land this sprint.
