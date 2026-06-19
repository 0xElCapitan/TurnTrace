# Cycle-004 Sprint 01 — Implementation Report (OA-2 Build: Offline Evidence-Summary Generator + Validator)

> Implementation artifact. Status: **IMPLEMENTED — ready for `/review-sprint sprint-01`.** This report records
> the build of `analysis/evidence_summary.py` + `tests/test_evidence_summary.py` under the accepted Cycle-004
> planning stack, through `/implement`. Cycle-004 is **build-only**: NG5 relaxed, every other Cycle-003 bright
> line held. **Rung 1 held throughout.**
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, or Competition Data appear here (CC-1/CC-2, ESP).
> **No dispersion metric values appear here** — the local exercise output stays local/gitignored and its
> values are not cited. Runs are referenced by `run_id`, sanitized metric *names*, claim ceilings, and local
> path/status only. The forbidden agent words (*strong / competitive / optimal / calibrated / complete*) and
> the inferential terms (*std-dev / variance / CI / p-value / significance / hypothesis-test / error-bar*)
> appear only as the negated/forbidden language they are.

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-004 · Sprint 01 (`C4-S01`) |
| **Skill** | `/implement sprint-01` |
| **Build-time HEAD** | `8ac161d` — *docs: plan TurnTrace Cycle-004* (the committed planning baseline) |
| **Posture** | Build-only; NG5 relaxed only; **Rung 1 held**; ledger byte-unchanged; no value promoted |
| **Result** | All 7 task groups (T1–T7) complete; all gates green; **ready for `/review-sprint sprint-01`** |

---

## 1. Preflight verification

All checks recorded **before** coding. Every assumption held; none contradicted the accepted PRD/SDD/sprint
plan; none forced a stop.

| Assumption to verify | Command | Result |
|---|---|---|
| Current branch | `git branch --show-current` | `main` ✓ |
| Current HEAD | `git rev-parse HEAD` | `8ac161d0a76e9b15056afaaf5b440766cc61e40d` ✓ |
| `origin/main` at/descends `8ac161d` | `git ls-remote origin main` | `8ac161d0a76e9b15056afaaf5b440766cc61e40d  refs/heads/main` — exact match ✓ |
| HEAD contains `8ac161d` | `git merge-base --is-ancestor 8ac161d HEAD` | yes (HEAD **==** `8ac161d`) ✓ |
| Local branch not behind `origin/main` | (HEAD == origin/main == `8ac161d`) | not behind ✓ |
| Planning docs present | `ls docs/cycles/cycle-004/0{1,2,3}-*.md` | `01-prd.md` · `02-sdd.md` · `03-sprint-plan.md` all present ✓ |
| No staged files | `git diff --cached --name-only` | empty ✓ |
| `docs/ledger.md` hash | `git hash-object docs/ledger.md` | **`2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`** — matches baseline exactly ✓ |
| `docs/ledger.md` clean | `git diff --exit-code -- docs/ledger.md` | clean (exit 0) ✓ |
| Claim ceiling still Rung 1 | read `docs/claim-ceiling.md` | **Rung 1** (ladder unchanged; `:5-6`) ✓ |
| `.claude/` (System Zone) drift | `git status --porcelain .claude/` | empty — no drift ✓ |
| `frozen/`/`runs/`/`agents/`/`sim/` drift | `git status --porcelain frozen/ runs/ agents/ sim/` | empty ✓ |
| `analysis/evidence_summary*` absent | `git ls-files "analysis/evidence_summary*"` + `ls` | absent (untracked, not on disk) ✓ |
| `tests/test_evidence_summary*` absent | `git ls-files "tests/test_evidence_summary*"` + `ls` | absent ✓ |
| State-Zone dirty files unstaged | `git status --porcelain` | `.beads/issues.jsonl` + `grimoires/loa/NOTES.md` modified, **unstaged** (pre-existing housekeeping) — **not staged or touched by this cycle** ✓ |
| Local K=20+20 run dirs present | `ls -d runs/run-v002-b-* runs/run-v002-c-*` | 20 `b` + 20 `c` = 40 dirs present (all `regime-v002`) — exercise feasible ✓ |

**Confirmation of baseline.** Implementation started from the committed planning baseline
**`8ac161d docs: plan TurnTrace Cycle-004`** — HEAD is exactly `8ac161d`, which is also `origin/main`. That
commit contains only the three planning docs (`01-prd.md`, `02-sdd.md`, `03-sprint-plan.md`); no code, no
State-Zone files, no ledger/claim-ceiling mutation. The build proceeded from that baseline.

---

## 2. Citation revalidation notes (NFR-9)

The PRD/SDD/sprint-plan were authored at `73c13ee`; the build-time HEAD is **`8ac161d`**, a descendant of
`73c13ee` that adds **only** `docs/cycles/cycle-004/` planning docs. The source files the citations anchor to
(`analysis/`, `eval/`, `tests/`) are therefore byte-identical between `73c13ee` and `8ac161d`. Every anchor
relied on for the build was re-validated directly against the build-time HEAD:

| Citation (used in the build) | Verified at HEAD `8ac161d` |
|---|---|
| `dispersion_report.py` read surface (manifest + `match_results/*`, never sidecar) | docstring **`:11-19`** ✓ |
| `dispersion_report.py` import boundary | sentence **`:44-46`**; full statement spans **`:39-46`** (shortcut block `:39-42` + boundary `:44-46`) ✓ — **the flagged minor drift confirmed exactly as the SDD §0 note predicted** |
| `DISPERSION_METRICS` (six metric names) | **`:69-72`** ✓ |
| `STAT_COLUMNS` (seven descriptive statistics) | **`:76`** ✓ |
| `descriptive_stats` helper | **`:94-114`** ✓ |
| `MixedRegimeRefusal` (exit 2) | class **`:79-80`**, raised **`:133-140`**, mapped to exit 2 **`:275-277`** ✓ |
| `render_json` (JSON-first) vs `render` (Markdown) | `render_json` **`:243-255`** / `render` **`:197-240`** ✓ |
| local-by-default `--out` | **`:268-270`** (+ write logic **`:283-287`**) ✓ |
| sibling-import pattern | **`:60-63`** ✓ |
| `aggregate.aggregate_run` (reads `match_results/*` only) | **`:56-89`** ✓ |
| `aggregate.LEDGER_COLUMNS` incl. `hypothesis` | **`:35-40`** (the `hypothesis` text column at `:39`) ✓ |
| `eval/hygiene_check.py` path rules `_RULES` | **`:35-45`** ✓ |
| `eval/hygiene_check.find_violations` returns `(path, reason)` | **`:52-62`** ✓ |
| `eval/validate.py` "no third-party schema library" idiom + `_MATCH_SPEC` | idiom **`:11-12`**; `_MATCH_SPEC` **`:27`** ✓ |
| `eval/schemas.md` spec↔validator contract; card-identity = SHA-256/counts only | **`:1-5`**; sanitization rule **`:13-15`** ✓ |
| `tests/test_import_direction.py` `ALLOWED["analysis"]=set()`; auto-glob `analysis/*.py` | `ALLOWED` **`:32-37`**; glob **`:69`** ✓ |
| `.gitignore` gitignores `grimoires/loa/a2a/` | line **`:17`** ✓ |

The in-module allow-list (`SAFE_FIELDS`) was made to **agree with doc 04 §2** (asserted by test check 9; §6
below). No anchor desynced; no citation rot found.

---

## 3. Files changed

**Authorized tracked files created (only these):**

| Path | Operation | Lines | Authority |
|---|---|---|---|
| `analysis/evidence_summary.py` | **create** | 511 | C4-FR-1/2/3; SDD §2-§7; sprint plan §3 |
| `tests/test_evidence_summary.py` | **create** | 289 | C4-FR-4; SDD §9; sprint plan §3 |
| `docs/cycles/cycle-004/04-implementation-report.md` | **create** | this file | sprint plan §3 (authorized cycle report) |

**Local/gitignored output created (never staged):**

| Path | Operation | Authority |
|---|---|---|
| `grimoires/loa/a2a/cycle-004/evidence-summary-local.json` | create (local only) | T6 exercise output; OD-C4-3; gitignored (`.gitignore:17`); **never `git add`-ed** |

**Existing helper files: NOT edited.** `analysis/aggregate.py`, `analysis/dispersion_report.py`,
`analysis/delta_report.py`, `eval/hygiene_check.py`, `eval/validate.py`, `eval/schemas.md`, and
`tests/test_import_direction.py` were **imported/referenced only** — no edits. No concrete blocker requiring
an edit was discovered.

---

## 4. Implementation summary by task (T1–T7)

### T1 — Module skeleton + CLI dispatch  [G1, G2]
`analysis/evidence_summary.py` created with a module docstring stating the read surface, import boundary,
exit-code contract, and the **structural no-sidecar guarantee** (mirroring `dispersion_report.py:11-49`). The
public surface — `SAFE_FIELDS`, `build_summary`, `validate_summary`, `render_json`, `main` — is exposed in
**one module** (OD-C4-1); the `argparse` CLI dispatches by flag. **No `analysis/evidence_summary_validate.py`**
second module. **No `--print-schema`** — recorded **deferred** (OD-C4-5 DEFER), not omitted-by-oversight; if a
future consumer needs it, add a one-line derived dump from the constant then. Exit codes `0`/`1`/`2`/`3` are
reachable (proven by T5 checks 1–3, 10).

### T2 — Generator core (`build_summary`)  [G1]
Reads each run dir's `manifest.json` **first** (the `regime_id`/`agent_id` authority), then `match_results/*`
**only via `analysis.aggregate.aggregate_run`**. Reuses `dispersion_report.descriptive_stats` and the
`DISPERSION_METRICS` / `STAT_COLUMNS` constants — **reuse, not recompute**, so no new metric or statistic can
enter (OD-6). Hard-refuses mixed regimes (`MixedRegimeRefusal` → exit 2) **before** aggregation. Runs no eval
and creates no run dir. Emits the doc 04 §4.1 JSON-first shape (`regime_id`, `n`, `K`, `mode`, per-agent
`metrics` of the seven statistics over the six metric names, `hashes`, `unseeded_caveat`, `claim_ceiling`),
carrying both mandatory framing strings (unseeded-process caveat **and** the Rung-1 footer that states the
summary "carries no ceiling of its own"). Writes **local-by-default** via `--out`; stdout otherwise; a guard
(`_refuse_tracked_out`) refuses any `--out` under `docs/` or to a `ledger.md`. **The module source contains no
reference to the per-decision sidecar directory** (verified: zero `trace` tokens; T5 check 4).

> **`hashes` source note (within the SDD read surface).** The SDD §3.1/§8 read surface is `manifest.json` +
> `match_results/*` only. The `hashes` integrity stamp is therefore sourced from the **manifest** (a
> prioritized search for a SHA-256-shaped `*_hash` field; the local manifests carry `agent_source_hash`),
> **not** from `hashes.txt` — staying strictly within the authorized read surface. Values are SHA-256 digests
> only (sanitized; `eval/schemas.md:13-15`).

### T3 — In-module schema / allow-list (`SAFE_FIELDS`)  [G3]
`SAFE_FIELDS` is the in-module machine-checkable allow-list — the single source of truth in code — composed
from the reused `DISPERSION_METRICS` (six metric names) + `STAT_COLUMNS` (seven statistic names) + the doc 04
§2.1 identity/provenance/framing field names + the doc 04 §4.1 JSON-first structural containers
(`agents`, `metrics`). **No standalone `.schema.json`. No `jsonschema`/`pydantic`/third-party dependency.** It
**agrees with doc 04 §2** — asserted by T5 check 9 (a divergence fails the build).

### T4 — Validator core (`validate_summary`)  [G2]
A **pure, fail-closed** function `validate_summary(obj) -> list[(field, reason)]` (no I/O, no global state).
`--validate <summary.json>` **re-reads the named file from disk** and validates **that** file (not the
in-memory generator output) — a genuine, independent gate. It rejects with per-class reasons and exit `3`:

- **field outside `SAFE_FIELDS`** (allow-list fail-closed, at every nesting level; `hashes` keys are treated
  as data, not fields);
- **raw per-decision body content** (decision/terminal row field markers);
- **Competition-Data tokens/paths** and **file-form Competition Data** (PDF/CSV/`deck.csv`/run-dir dump) —
  via the **parity-tested stdlib-local copy** of the hygiene path rules (**not** an `eval/` import);
- **Pokémon-Element / Competition-Data leak** — card-identity must be a SHA-256 digest, never raw content
  (the `eval/schemas.md:13-15` mechanism);
- **inferential statistic terms** (`std-dev`/`variance`/CI/`p-value`/`significance`/`hypothesis-test`/`error-bar`);
- **cross-regime fields / comparisons** (field-name + affirmative-connective markers);
- **affirmative forbidden agent words** (rejected only when not negated).

It **hard-refuses mixed-regime summaries with exit 2** (`_collect_regime_ids` over the `--validate` path,
checked before leak classification). It implements **hygiene parity-or-stricter** via the local copy (T5 check
5 asserts parity against `eval/hygiene_check.find_violations`). It distinguishes the **benign `hypothesis`
text-field context** (allowed — the inferential rule matches only the compound `hypothesis[\s\-]?test(ing)?`)
from an **inferential hypothesis-test** (rejected) — T5 check 8.

### T5 — Synthetic fixtures + 12-check test suite  [G4, G6]
`tests/test_evidence_summary.py` — a stdlib plain-Python module (`main()` → exit 0/1) using **synthetic
temp-dir fixtures only** (no dependency on the gitignored K-batch runs). All 12 required checks present and
green (1 allow-list fail-closed; 2 forbidden-content rejection — six sub-cases; 3 mixed-regime → exit 2;
4 structural no-sidecar source property; 5 hygiene parity superset; 6 no-ledger-mutation; 7 no-value-promotion
+ framing strings; 8 benign-`hypothesis` exception; 9 doc↔schema agreement; 10 JSON-first round-trip;
11 sanitization smoke; 12 import-direction/stdlib-only). The suite also runs `test_import_direction.check()`.

### T6 — Local end-to-end exercise (no promotion)  [G5]
**COMPLETED.** Local `runs/run-v002-b-1..20` + `runs/run-v002-c-1..20` (40 dirs, single `regime-v002`) were
present, so the exercise ran:
- **Generate** → `grimoires/loa/a2a/cycle-004/evidence-summary-local.json` (gitignored), **exit 0**.
- **Validate** that file → **exit 0** (VALID — schema-conforming, sanitized, single-regime).

The output is **gitignored and unstaged** (proof in §7). It **promotes nothing**: not `git add`-ed, no ledger
row, no ceiling advance, no `M`, and **its values are not cited in any tracked artifact** (including this
report).

### T7 — Final posture / hygiene checks  [G6]
All closing checks pass (full command/exit table in §5; posture proofs in §7). `docs/ledger.md` is
byte-unchanged; `.claude/`/`frozen/`/`runs/`/`agents/`/`sim/` show no tracked drift; no inferential statistic
is computed anywhere in the module (it reuses `descriptive_stats` and adds none); no third-party dependency;
stdlib + intra-zone (`analysis`) imports only.

---

## 5. Exact commands run and exit statuses

| # | Command | Exit / Result |
|---|---|---|
| 1 | `python analysis/evidence_summary.py --help` | 0 (CLI loads) |
| 2 | `python tests/test_evidence_summary.py` | **0** (all 12 checks / 37 assertions) |
| 3 | `python tests/test_import_direction.py` | **0** |
| 4 | `python eval/hygiene_check.py --paths analysis/evidence_summary.py tests/test_evidence_summary.py` | **0** (clean) |
| 5 | `python analysis/evidence_summary.py runs/run-v002-b-1 … runs/run-v002-c-20 --out grimoires/loa/a2a/cycle-004/evidence-summary-local.json` | **0** (generate; wrote local) |
| 6 | `python analysis/evidence_summary.py --validate grimoires/loa/a2a/cycle-004/evidence-summary-local.json` | **0** (VALID) |
| 7 | `git hash-object docs/ledger.md` | **`2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`** (unchanged) |
| 8 | `git diff --exit-code -- docs/ledger.md` | **0** (clean) |
| 9 | `git status --porcelain .claude/ frozen/ runs/ agents/ sim/` | empty (clean) |
| 10 | `git status --porcelain` | only the 4 expected lines (§7) |
| 11 | `git diff --cached --name-only` | empty (nothing staged) |
| 12 | `git check-ignore grimoires/loa/a2a/cycle-004/evidence-summary-local.json` | match (gitignored) |

---

## 6. AC Verification (sprint plan §5)

Every acceptance criterion from `docs/cycles/cycle-004/03-sprint-plan.md` §5, walked verbatim.

**AC-1 — Generator** — *"Generator conforms to C4-FR-1 / SDD §3: reads `manifest.json` + `match_results/*` via
`aggregate_run` only; never references the sidecar dir; emits JSON-first doc 04 §2 safe fields; carries the
two framing strings; writes local-by-default."*
✓ **Met** — `build_summary` ([analysis/evidence_summary.py:135](analysis/evidence_summary.py:135)) reads manifest first then `aggregate.aggregate_run` ([analysis/evidence_summary.py:167](analysis/evidence_summary.py:167)); no sidecar reference (zero `trace` tokens, T5 check 4); JSON-first doc 04 shape ([analysis/evidence_summary.py:205-216](analysis/evidence_summary.py:205)); both framing strings ([analysis/evidence_summary.py:91-101](analysis/evidence_summary.py:91)); local-by-default `--out` with tracked-path guard ([analysis/evidence_summary.py:410](analysis/evidence_summary.py:410)).

**AC-2 — Validator** — *"pure `validate_summary`; independent `--validate` re-read; allow-list/fail-closed;
rejects every doc 04 §3 class with a reason; single-regime exit 2; leak exit 3; benign `hypothesis` exception
(accept column / reject test); hygiene-parity-or-stricter."*
✓ **Met** — pure `validate_summary` ([analysis/evidence_summary.py:353](analysis/evidence_summary.py:353)); independent disk re-read ([analysis/evidence_summary.py:424-432](analysis/evidence_summary.py:424)); allow-list fail-closed via `_walk` ([analysis/evidence_summary.py:365](analysis/evidence_summary.py:365)); all forbidden classes with reasons (T5 check 2, six sub-cases); single-regime exit 2 ([analysis/evidence_summary.py:437-441](analysis/evidence_summary.py:437)); leak exit 3 ([analysis/evidence_summary.py:443-449](analysis/evidence_summary.py:443)); benign-`hypothesis` split (T5 check 8); hygiene parity (T5 check 5).

**AC-3 — Schema artifact** — *"in-module `SAFE_FIELDS` constant agreeing with doc 04 §2; no `.schema.json`; no
third-party dependency."*
✓ **Met** — `SAFE_FIELDS` ([analysis/evidence_summary.py:83-89](analysis/evidence_summary.py:83)); doc↔schema agreement (T5 check 9); no `.schema.json` and stdlib-only (T5 check 12; `git status` shows no schema file).

**AC-4 — Tests** — *"§T5 all 12 pass, including structural no-sidecar-read (4), no-ledger-mutation (6),
no-value-promotion (7), benign-`hypothesis` (8), doc↔schema-agreement (9); count ≥ 3."*
✓ **Met** — `python tests/test_evidence_summary.py` exit 0; 12 checks (≥ `edd.min_test_scenarios: 3`).

**AC-5 — Local exercise** — *"produces a gitignored validated summary (exit 0), or is recorded deferred;
promotes nothing."*
✓ **Met** — completed; generate + `--validate` both exit 0; output gitignored/unstaged (§7); no value cited.

**AC-6 — Citations re-validated** — *"against build-time HEAD (NFR-9); the in-module allow-list made to agree
with doc 04 §2."*
✓ **Met** — §2 above (all anchors re-validated at `8ac161d`; flagged `:39-46` drift confirmed); allow-list agrees with doc 04 §2 (T5 check 9).

**AC-7 — Posture held (hard)** — *"Rung 1 held; `docs/ledger.md` byte-unchanged (`2a2f1c2…`); no value
promoted; stdlib-only / analysis-only imports; no `M` / SP-6 / Rung-2 row; no `.claude/` drift; State-Zone
files unstaged."*
✓ **Met** — ledger hash `2a2f1c2…` unchanged (§5 #7-8); no value promoted (exercise gitignored, no values in tracked docs); stdlib/analysis-only (T5 check 12); no `M`/SP-6/Rung-2 row written; `.claude/` clean; State-Zone files unstaged (§7).

**AC-8 — Cadence** — *"lands through `/implement → /review-sprint → /audit-sprint → operator acceptance`."*
✓ **Met (in progress)** — `/implement` complete; nothing staged/committed; ready for `/review-sprint sprint-01`.

---

## 7. Posture proofs

**Ledger byte-unchanged (HARD).** `git hash-object docs/ledger.md` = `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`
(matches the baseline exactly); `git diff --exit-code -- docs/ledger.md` clean. No Rung-2 row written.

**`.claude/` unchanged.** `git status --porcelain .claude/` → empty. System Zone untouched.

**No forbidden paths touched.** `git status --porcelain frozen/ runs/ agents/ sim/` → empty. No
`docs/claim-ceiling.md` change; no `eval/run_eval.py` / `eval/run_match.py` change; no `*.schema.json`; no
`analysis/evidence_summary_validate.py`; no dependency file change. The only new tracked files are the two
authorized source files (plus this report).

**Exercise output gitignored and unstaged.** `git check-ignore grimoires/loa/a2a/cycle-004/evidence-summary-local.json`
returns the path (it is ignored); `git status --porcelain` does **not** list it. Never `git add`-ed.

**No value promotion / no inferential statistic.** No dispersion value appears in any tracked artifact
(including this report); the module computes no inferential statistic (it reuses `descriptive_stats` and adds
none). Forbidden agent words and inferential terms appear in the tracked artifacts **only** as negated/
forbidden language (comments/docstrings) or as deliberate **test-poison inputs that the suite asserts are
rejected** — never as an affirmative claim about the agent's evidence.

**Final `git status --porcelain`:**

```
 M .beads/issues.jsonl          # pre-existing State-Zone housekeeping — unstaged, untouched by this cycle
 M grimoires/loa/NOTES.md       # pre-existing State-Zone housekeeping — unstaged, untouched by this cycle
?? analysis/evidence_summary.py # authorized new file (untracked, unstaged)
?? tests/test_evidence_summary.py # authorized new file (untracked, unstaged)
```

(`docs/cycles/cycle-004/04-implementation-report.md` appears as `??` once written. The exercise output under
`grimoires/loa/a2a/` is gitignored and does not appear.) **Nothing is staged; nothing is committed.**

---

## 8. Deviations and blockers

- **No code-affecting deviations.** No existing helper file required editing; scope stayed within the
  authorized file-touch matrix (sprint plan §3). No forbidden path (sprint plan §4) was touched.
- **Beads not used for task lifecycle (deliberate posture choice).** The framework default is to track sprint
  tasks via `br` (beads), which mutates `.beads/issues.jsonl`. The binding sprint posture requires the
  pre-existing dirty State-Zone files — explicitly including `.beads/issues.jsonl` — to **remain unstaged and
  untouched** (sprint plan §0, §10; audit checklist §8). To honor that, this cycle did **not** run `br`
  mutations and did **not** modify `.beads/issues.jsonl` or `grimoires/loa/NOTES.md`; session progress was
  tracked with the session-display task list only. The State-Zone files are byte-unchanged from their
  pre-existing state.
- **`hashes` sourced from `manifest.json`, not `hashes.txt`** — a deliberate read-surface choice to stay
  strictly within the SDD §3.1/§8 allowed read surface (manifest + `match_results/*`). Documented in §4 (T2).
- **`--print-schema` deferred** — OD-C4-5 DEFER, recorded as deferred (not omitted-by-oversight).
- **No blockers encountered.**

---

## 9. Readiness

**Sprint 01 is READY for `/review-sprint sprint-01`.**

- Both authorized source files build and pass all gates; the 12-check suite, the import-direction test, and
  the hygiene gate are green.
- The local end-to-end exercise completed (generate + validate exit 0); its output is gitignored, unstaged,
  and uncited.
- `docs/ledger.md` is byte-unchanged (`2a2f1c2…`); Rung 1 is held; no value is promoted; no `M`/SP-6/Rung-2
  row exists; `.claude/` and all forbidden paths are untouched; State-Zone files remain unstaged.
- Nothing is staged or committed. The working tree holds exactly the authorized changes plus this report.
