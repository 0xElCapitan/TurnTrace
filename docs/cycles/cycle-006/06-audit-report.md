# Cycle-006 Audit Report — Sprint 01: Promotion-Check Hardening (`--promotion-check`)

> Audit artifact (written under `/audit-sprint`; Paranoid Cypherpunk Auditor — final quality/security gate).
> **Pure audit — no code edited, no fix applied, nothing staged/committed/pushed, no closeout artifact created,
> no `.claude/` mutation, no State-Zone file cleaned or staged.** Every behavioural and posture claim below was
> re-derived independently (fresh synthetic fixtures, fresh command runs) rather than trusting the implementation
> report (`04`) or the review report (`05`).

## Verdict: **PASS WITH NOTES — ACCEPTED**

Sprint 01 is **accepted as the audited promotion gate**. All eight acceptance criteria are met, all required
commands pass, the ledger invariant holds (`2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`), the claim ceiling is
untouched, Rung 1 is held, no forbidden path changed, no scope creep occurred, no State-Zone file was staged, and
nothing was committed or pushed. The security audit surfaced **no new finding** at any severity. The review's four
advisory notes are independently confirmed **non-blocking** and are recorded as **Cycle-007 carry-forwards**.

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-006 / Sprint 01 — Promotion-Check Hardening |
| **Audited at HEAD** | `082a953923e5fd8e4643171466cfcc23f413a8dd` (== `origin/main`); unstaged working tree |
| **Verdict** | **PASS WITH NOTES — ACCEPTED** |
| **Security findings** | none (CRITICAL 0 · HIGH 0 · MEDIUM 0 · LOW 0) |
| **Ledger invariant** | `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` — held (verified before & after all audit runs) |
| **Claim ceiling** | Rung 1 held; `docs/claim-ceiling.md` untouched |
| **New audit artifact** | this file only (`06-audit-report.md`) |

---

## 1. Files audited

**Planning + record (read, not changed):** `docs/cycles/cycle-006/01-prd.md`, `02-sdd.md`, `03-sprint-plan.md`,
`04-implementation-report.md`, `05-review-report.md`.

**Implementation under audit (unstaged):** `analysis/evidence_summary.py`, `tests/test_evidence_summary.py`.

**Reference (parity/import targets):** `eval/hygiene_check.py`, `tests/test_import_direction.py`.

## 2. Diff summary

| File | Added / Deleted | Nature |
|---|---|---|
| `analysis/evidence_summary.py` | **+73 / −4** | Additive: `_run_promotion_check` driver (`:511-566`), `--promotion-check` arg (`:582`), dispatch branch (`:597-598`), 1 docstring CLI line. 4 "deletions" = 3 reformatted docstring lines + 1 changed dispatch comment. |
| `tests/test_evidence_summary.py` | **+77 / −1** | Additive: `promotion_check_file_exit` helper + block 14 (14a–14f). 1 "deletion" = the `main()` summary line. |
| `docs/cycles/cycle-006/04-implementation-report.md` | new (268 lines, untracked) | Implementation report. |
| `docs/cycles/cycle-006/05-review-report.md` | new (225 lines, untracked) | Review report. |

**Independently confirmed behaviour-unchanged:** a targeted diff grep finds **no** `def validate_summary` /
`_run_validate` / `_refuse_tracked_out` / `build_summary` / `render_json` lines and **no** generate-mode
`WARNING — empty hashes` line in the diff — those surfaces are byte-unchanged. The new driver *reuses*
`_collect_regime_ids` (`:532`) and `validate_summary` (`:540`) wholesale; the empty/absent-`hashes` precheck
(`:556`) is the only added rule. Existing test checks 1–13 are absent from the diff (unmodified).

## 3. Commands run and exit codes (independently re-run)

| # | Command | Result | ✓ |
|---|---|---|---|
| 1 | `python tests/test_evidence_summary.py` | **0** (12 + 13a–13l + 14a–14f green) | ✓ |
| 2 | `python tests/test_import_direction.py` | **0** | ✓ |
| 3 | `python eval/hygiene_check.py --paths analysis/evidence_summary.py tests/test_evidence_summary.py docs/cycles/cycle-006/04-implementation-report.md docs/cycles/cycle-006/05-review-report.md` | **0** | ✓ |
| 4 | `git hash-object docs/ledger.md` | `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` | ✓ |
| 5 | `git diff --exit-code -- docs/ledger.md` | **0** | ✓ |
| 6 | `git diff --exit-code -- docs/claim-ceiling.md` | **0** | ✓ |
| 7 | `git status --porcelain .claude/ frozen/ runs/ agents/ sim/` | (empty) | ✓ |
| 8 | `git diff --cached --name-only` | (empty) | ✓ |

Forbidden-path diff sweep (`docs/ledger.md`, `docs/claim-ceiling.md`, `.claude`, `analysis/aggregate.py`,
`analysis/dispersion_report.py`, `eval`, `agents`, `sim`, `frozen`, `runs`): **all clean**.
`analysis/evidence_summary_validate.py` absent (no second module); no new/tracked `*.schema.json`; no
dependency/manifest change.

## 4. Independent behaviour checks (fresh synthetic fixtures)

### 4.1 Exit-code contract & parity matrix (`--promotion-check` vs `--validate`)

| Input | `--promotion-check` | `--validate` | Relationship |
|---|---|---|---|
| clean, non-empty `hashes` | **0** | **0** | same |
| structurally-valid **empty** `hashes` `{}` | **3** | **0** | intended delta (stricter) |
| **absent** `hashes` (key missing) | **3** | **0** | intended delta (stricter) |
| leak — unknown/allow-list field | **3** | **3** | same |
| leak — inferential term | **3** | **3** | same |
| leak — affirmative forbidden word | **3** | **3** | same |
| leak — cross-regime field | **3** | **3** | same |
| leak — non-digest `hashes` value | **3** | **3** | same |
| mixed-regime | **2** | **2** | same |
| unreadable input path | **1** | (n/a) | reuses `_run_validate` read-fail block |

**Parity-or-stricter holds.** Every input is identical under both modes except empty/absent `hashes` (validate `0`
→ promotion `3`). No input that `--validate` rejects (exit 2/3) is accepted (exit 0) by `--promotion-check`. The
accepted set of `--promotion-check` is a strict subset of `--validate`'s.

### 4.2 Paranoid security probes (auditor value-add, beyond the review)

| Probe | Result |
|---|---|
| **No data leak** — planted Competition-Data token in an `agent_id` value → exit 3, and the token is **NOT surfaced** in stdout or stderr | ✓ (inherits the validator's field-path-only printing) |
| **stdout silence** — a clean promotion-check emits **nothing to stdout**; the `PROMOTION OK` decision goes only to stderr | ✓ (no data emission; JSON-first stdout reserved for generate mode) |
| **Un-bypassable precheck** — `hashes` as a list, a string, or `{"r": ""}` (empty-string digest) → exit 3 under both modes (validator catches before the precheck) | ✓ |
| **Idempotency** — promotion-check run twice on the same file → identical exit (3,3 and 0,0); pure read, no state | ✓ |
| **Writes nothing** — a promotion-check run creates no file and leaves `docs/ledger.md` byte-identical | ✓ |
| **Generate-mode empty-`hashes`** — still WARNS at exit 0 (unchanged) | ✓ |

### 4.3 Audit-focus questions (all answered ✓)

- Calls `validate_summary` wholesale / full hardened semantics preserved → **Yes** (`:540`; all leak classes reject
  identically to `--validate`).
- Empty/absent `hashes` hard-fails only in promotion mode → **Yes** (precheck lives only in `_run_promotion_check`;
  `--validate` returns 0 on the same input).
- `--validate` empty/absent-`hashes` stays exit 0 when otherwise structurally valid → **Yes** (matrix §4.1).
- Generate-mode empty-`hashes` warning stays exit 0 → **Yes** (§4.2; WARNING block unchanged in diff).
- Exit-code contract stayed 0/1/2/3 → **Yes** (all five values observed; no new code).
- Writes nothing / promotes nothing → **Yes** (§4.2; no write surface in diff).
- `docs/ledger.md` & `docs/claim-ceiling.md` untouched → **Yes** (cmds 4–6).
- Tests use only stdlib synthetic fixtures → **Yes** (`make_run_dir`/`copy`/`_HEX64`; no raw-data tokens in added
  test lines).
- No raw Competition Data / Pokémon Elements / traces / deck lists / simulator logs / Daily-Top-Episodes / Kaggle
  data in tracked files → **Yes** (hygiene exit 0; the only forbidden-looking strings are synthetic *rejection
  probes*).
- No runtime-agent / gameplay / FunSearch / RL / self-play / deck-optimizer / value-model / search / MCTS /
  tournament / dashboard scope → **Yes** (scope-token grep on added lines: none; imports unchanged).

## 5. Acceptance criteria (AC-1 … AC-8) — independently re-derived

| AC | Criterion (verbatim, sprint-plan §"Acceptance Criteria") | Status | Evidence |
|---|---|---|---|
| **AC-1** | "`--promotion-check` on a clean, non-empty-`hashes`, schema-conforming summary → exit 0." | ✓ Met | §4.1 good→0; test 14a; driver `:563-566`. |
| **AC-2** | "`--promotion-check` on a structurally-valid but empty-`hashes` summary → exit 3 (non-zero, fail-closed; CF-1 / OD-C5-2 floor)." | ✓ Met | §4.1 empty→3; test 14b; precheck `:556-561`. |
| **AC-3** | "`--promotion-check` on a summary carrying any forbidden field/value/word → exit 3 (full validator re-run). A mixed-regime summary → exit 2." | ✓ Met | §4.1 (all leak classes→3; mixed→2); tests 14c/14f; driver `:540`/`:532`. |
| **AC-4** | "generate-mode still emits the empty-`hashes` WARNING at exit 0; `--validate` still accepts a structurally-valid empty `hashes` at exit 0; the 0/1/2/3 contract holds (no new exit code)." | ✓ Met | §4.1/§4.2; tests 14d/14b′; generate WARNING + `_run_validate` unchanged. |
| **AC-5** | "`--promotion-check` writes nothing; `docs/ledger.md` byte-unchanged before/after; no tracked `docs/` write." | ✓ Met | §4.2; test 14e; ledger hash unchanged after all runs. |
| **AC-6** | "each behaviour has ≥1 runnable regression check; all existing 12 + block-13 checks remain green; `test_import_direction` exit 0; `hygiene_check --paths …` exit 0." | ✓ Met | §3 cmds 1–3 = 0; block 14 green; checks 1–13 unmodified. |
| **AC-7** | "posture held (hard): Rung 1; claim-ceiling untouched; no `M`; no SP-6; no value promotion; no Rung-2 row; no fresh evidence; no `.claude/` drift; State-Zone files unstaged; no second module; no `*.schema.json`; no dependency; no ledger write." | ✓ Met | §6. |
| **AC-8** | "lands only through `/implement → /review-sprint → /audit-sprint → operator acceptance`." | ✓ Met (audit step) | `/implement` (04) → `/review-sprint` (05) → `/audit-sprint` (this 06) completed; **operator acceptance** is the only remaining step. Nothing committed/pushed. |

## 6. Posture / invariant verification (binding non-goals)

| Constraint | Result |
|---|---|
| Rung 1 held; ledger byte-unchanged (`2a2f1c2…`) after all audit runs | ✓ |
| `docs/claim-ceiling.md` untouched | ✓ |
| No numeric `M` chosen | ✓ (added-line grep: none; one benign match — the 14e *no-write* comment) |
| No SP-6 / no value promoted | ✓ (gate returns an exit code only; writes nothing) |
| No Rung-2 ledger row / no claim-ceiling advance | ✓ |
| No fresh evidence / no eval run / no K-batch / no run dir | ✓ (synthetic temp fixtures only) |
| No PASS/FAIL/INCONCLUSIVE *verdict* applied | ✓ (the gate emits exit codes, not a Rung-2 admission verdict) |
| No runtime-agent / gameplay / FunSearch / RL / self-play / optimizer / value-model / search / MCTS / tournament / dashboard | ✓ |
| No Daily-Top-Episodes / Kaggle ingest | ✓ |
| No raw Competition Data / Pokémon Elements in tracked files | ✓ (hygiene exit 0) |
| No second validator module / `*.schema.json` / dependency | ✓ |
| `.claude/` untouched; State-Zone (`.beads/issues.jsonl`, `NOTES.md`) pre-existing-dirty & unstaged | ✓ (their diffs contain only Cycle-003/earlier content; zero cycle-006/promotion-check references) |
| Nothing staged / committed / pushed | ✓ |

## 7. Audit assessment of the review's four advisory notes

Each note independently re-verified; all confirmed **non-blocking**, recorded as **Cycle-007 carry-forwards**.

| # | Review note | Auditor assessment | Disposition |
|---|---|---|---|
| 1 | Absent-`hashes` branch verified manually but not regression-tested | **Confirmed correct & non-blocking.** AC-2 specifies *empty*, which **is** tested (14b). Absent is an additional robustness property; independently re-verified absent→3 (§4.1) and structurally covered by the `isinstance(h, dict)` guard (`:556`). | Carry-forward: add a 1-line absent-`hashes` regression check when Cycle-007 first exercises the gate. |
| 2 | exit-1 (unreadable) & both-flags precedence not regression-tested | **Confirmed non-blocking.** exit-1 is a verbatim copy of `_run_validate`'s read-fail block; independently re-verified exit 1 (§4.1). Precedence is documented in-code and verified (stricter wins). | Carry-forward (optional). |
| 3 | Cosmetic docstring realignment | **Confirmed non-blocking.** Documentation-only; no behaviour/exit-code change; keeps the CLI synopsis honest. | Accept as-is. |
| 4 | "writes-nothing" test is shallow (top-level `iterdir`) | **Confirmed non-blocking.** Adequate because the driver has **zero** write surface (diff-confirmed; §4.2 independently shows no new file + ledger byte-unchanged). | Accept as-is. |

The review's classification is accurate. No note rises to a blocking severity; none requires a fix to land.

## 8. Security assessment (Paranoid Cypherpunk Auditor)

- **Input handling.** `--promotion-check` parses the candidate with `json.loads` (stdlib; no `eval`, no code
  execution) and **re-reads from disk** (independent gate — never trusts an in-memory object). Read failures
  (`FileNotFoundError`/`OSError`/`json.JSONDecodeError`) are caught → exit 1.
- **Output handling / no data exfiltration.** All decisions go to **stderr**; stdout is silent for the gate
  (§4.2). The violation printer emits field **paths** and fixed reason strings only — a planted Competition-Data
  token in a value is **not** surfaced (§4.2), matching the audited `--validate` behaviour (test 11).
- **Fail-closed integrity.** Every non-clean path returns non-zero; the empty/absent-`hashes` precheck is
  un-bypassable (non-dict/empty-string/list `hashes` are caught by `validate_summary` *before* the precheck;
  §4.2). Exit 0 requires a clean validator pass **and** a non-empty all-digest `hashes` map.
- **No new attack surface.** No new read source (no `hashes.txt`, no sidecar — source-grep tests 13l & 4 green),
  no write path, no network, no subprocess, no new import or dependency (`test_import_direction` green).
- **Pre-existing, out-of-scope observation (NOT a finding, NOT a required fix).** `validate_summary` /
  `_collect_regime_ids` recurse over the parsed object; a maliciously deep JSON could raise an uncaught
  `RecursionError`. This exposure is **identical to the existing `--validate` path** (not introduced by this
  sprint), the threat model is an operator running the gate offline on their own candidate summary, and remediation
  is outside this narrow hardening sprint's authorized scope. Recorded here for completeness only; it does **not**
  affect the verdict and the auditor explicitly does **not** require a fix.

## 9. Accuracy of the implementation & review reports

- **`04-implementation-report.md`:** accurate — file-change list, exit codes, line anchors (`_run_promotion_check:511`,
  precheck `:556`, arg `:582`, dispatch `:597-598`), parity claim, and posture confirmations all match independent
  reality. Its claim that empty *and absent* `hashes` both hard-fail is correct (§4.1).
- **`05-review-report.md`:** accurate — verdict, parity matrix, AC table, and the four-note classification all
  reproduce under independent verification. The review correctly identified the absent-`hashes` test-coverage gap
  rather than overclaiming coverage.

Both reports are **accurate enough to land**.

## 10. Issues / required fixes

- **Blocking issues:** none.
- **Security findings:** none (CRITICAL/HIGH/MEDIUM/LOW all zero).
- **Required fixes:** none.
- **Carry-forwards to Cycle-007 (advisory, non-blocking):** review notes 1 & 2 (absent-`hashes` and exit-1 /
  both-flags regression checks) — best added when the gate is first wired into a real Cycle-007 promotion. Notes
  3 & 4 accepted as-is.

## 11. New audit artifact confirmation

This `docs/cycles/cycle-006/06-audit-report.md` is the **only** new artifact created by the audit. No code was
edited, no fix applied; **no `07-closeout.md`** and **no `grimoires/loa/a2a/.../COMPLETED` marker** were created
(closeout and operator acceptance are separate steps; the operator's instructions scoped this audit to the `06`
report only). No State-Zone file was cleaned or staged.

## 12. Final git status summary

```
 M .beads/issues.jsonl                                  ← pre-existing State-Zone; unstaged, untouched by sprint
 M analysis/evidence_summary.py                          ← authorized; unstaged
 M grimoires/loa/NOTES.md                                ← pre-existing State-Zone; unstaged, untouched by sprint
 M tests/test_evidence_summary.py                        ← authorized; unstaged
?? docs/cycles/cycle-006/04-implementation-report.md     ← implementation report
?? docs/cycles/cycle-006/05-review-report.md             ← review report
?? docs/cycles/cycle-006/06-audit-report.md              ← this audit report
```

Nothing staged (`git diff --cached --name-only` empty). Nothing committed or pushed.

---

> **Decision (binding):** **PASS WITH NOTES — ACCEPTED.** `--promotion-check` re-reads from disk, runs
> `validate_summary` wholesale, inherits mixed-regime exit 2, hard-fails empty/absent `hashes` at exit 3, and
> passes at exit 0 only when clean and non-empty-`hashes` — parity-or-stricter with `--validate` confirmed across
> all rejection classes, with no data-leak, no write surface, and an un-bypassable precheck. Generate-mode and
> `--validate` empty/absent-`hashes` behaviour stayed exit 0; the 0/1/2/3 contract held; `docs/ledger.md`
> (`2a2f1c2…`) and `docs/claim-ceiling.md` are untouched; Rung 1 held; no `M`, no SP-6, no Rung-2 row, no fresh
> evidence, no forbidden-path change, no scope creep, no State-Zone staging. Security audit: **no findings.** The
> gate is hardening/preparation, **not** admission; the Rung-2 attempt remains deferred to Cycle-007 behind a
> separate explicit operator gate. **Sprint 01 is cleared for operator acceptance / closeout.** The four advisory
> notes are non-blocking Cycle-007 carry-forwards and require no change to land this sprint.
