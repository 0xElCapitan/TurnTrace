# Cycle-006 Sprint Plan — Promotion-Check Hardening (`--promotion-check`)

> Planning artifact (Sprint Plan). Status: **DRAFT — awaiting operator acceptance + a separate build gate.** This
> sprint plan translates the accepted Cycle-006 PRD + SDD into **one focused, narrow hardening sprint** —
> Sprint 01, Promotion-Check Hardening — adding a `--promotion-check` mode to `analysis/evidence_summary.py`
> plus regression tests in `tests/test_evidence_summary.py`. It **opens no implementation gate**: code lands
> only through `/implement → /review-sprint → /audit-sprint → operator acceptance`
> (`docs/operator/turntrace-loop-contract.md` §1, §6, the OA-2-class build gate). **Cycle-006 attempts no
> Rung 2, applies no PASS/FAIL/INCONCLUSIVE verdict, promotes no value, generates no fresh evidence, chooses no
> `M`, issues no SP-6, writes no Rung-2 ledger row, and mutates neither `docs/ledger.md` nor
> `docs/claim-ceiling.md`.**
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, Daily-Top-Episode data, or Competition Data appear here
> (CC-1/CC-2, ESP, SP-6/SP-9). **No dispersion metric values appear here** — evidence stays local/gitignored and
> is referenced qualitatively only. **No numeric margin `M` is chosen.** Runs are referenced by `run_id`
> pattern, count, hashes, sanitized metric *names*, claim ceilings, and local path/status only. The forbidden
> agent words (*strong / competitive / optimal / calibrated / complete*) and the inferential terms (*std-dev /
> variance / CI / p-value / significance / hypothesis-test / error-bar*) appear only as the negated/forbidden
> language they are.

| Field | Value |
|---|---|
| **Cycle** | Cycle-006 |
| **Working title** | Rung-2 Admission-Seam Preparation: Pre-Register the Rule and Build the Promotion Gate |
| **Type** | Sprint Plan (implementation roadmap for one narrow hardening sprint) |
| **Status** | DRAFT — awaiting operator acceptance; next Golden-Path step is `/implement` (under a later build gate) |
| **Date** | 2026-06-19 |
| **Current main** | `561fb92` — *docs: close TurnTrace Cycle-005 Sprint 01* (== `origin/main`) |
| **Primary authorities** | `docs/cycles/cycle-006/01-prd.md` (accepted PRD; OD-C6-1 ratified); `docs/cycles/cycle-006/02-sdd.md` (accepted SDD — OD-C6-2…OD-C6-6, CF-3) |
| **Posture** | **Preparation + one narrow hardening sprint.** The governance/design (Track A) deliverables are complete in the SDD; this plan scopes only the code sprint (Track B). Modify exactly `analysis/evidence_summary.py` + `tests/test_evidence_summary.py`; hold every other bright line. |
| **Claim ceiling** | **Rung 1** (held for the whole cycle; not raised). |
| **Ledger** | `docs/ledger.md` byte-unchanged; hash `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`. |

---

## Preflight verification (recorded at authoring, HEAD `561fb92`)

| Check | Command | Result | Verdict |
|---|---|---|---|
| HEAD / branch | `git rev-parse HEAD` | `561fb92f6c398a53a381f9aff9056b1d85150a9e` | ✓ `561fb92` |
| Not behind origin | `git ls-remote origin main` | `561fb92…` | ✓ equal (not behind) |
| Working tree | `git status --porcelain` | ` M .beads/issues.jsonl` · ` M grimoires/loa/NOTES.md` · `?? docs/cycles/cycle-006/` | ✓ only pre-existing State-Zone + untracked Cycle-006 planning docs |
| Ledger byte-unchanged | `git hash-object docs/ledger.md` | `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` | ✓ |
| Ledger diff clean | `git diff --exit-code -- docs/ledger.md` | exit 0 | ✓ |
| Claim ceiling clean | `git diff --exit-code -- docs/claim-ceiling.md` | exit 0 | ✓ |
| Protected-path drift | `git status --porcelain .claude/ frozen/ runs/ agents/ sim/ analysis/ tests/ eval/` | empty | ✓ no tracked drift |
| No staged files | `git diff --cached --name-only` | empty | ✓ |
| Build target present | source read | `analysis/evidence_summary.py` (574 lines) + `tests/test_evidence_summary.py` (404 lines, 12 + block-13 checks) tracked + accepted | ✓ |
| `--promotion-check` absent | `grep -c "promotion-check\|promotion_check"` | 0 (only `:551,554` forward-reference WARNING *text*) | ✓ this sprint introduces the mode |

**All preflight expectations hold. No finding forces a stop.** Implementation remains un-authorized until the
operator accepts the PRD/SDD and opens the build gate. The pre-existing dirty State-Zone files
(`.beads/issues.jsonl`, `grimoires/loa/NOTES.md`) stay **unstaged and untouched** unless explicitly authorized.

---

## Executive summary

Across five cycles TurnTrace has built Rung-2 *readiness* without ever attempting Rung 2: Cycle-002 defined the
five conjunctive readiness criteria; Cycle-003 specified the evidence-summary schema, the generator/validator
shape, the Rung-2 ledger convention, and the OD-6 / disjoint-bands resolution *in shape*; Cycle-004 built the
offline generator + fail-closed validator (`analysis/evidence_summary.py`) and stopped at the seam; Cycle-005
hardened that validator (C1–C4) and had it **reviewed and audited in a load-bearing-ready posture**
(`docs/cycles/cycle-005/06-audit-report.md`, PASS WITH NOTES — ACCEPTED; `07-closeout.md`, CLOSED/accepted/pushed
at Rung 1). The Cycle-005 audit recorded the binding floor that **a future promotion gate MUST hard-fail empty
`hashes`** (CF-1; OD-C5-2 floor; `06-audit-report.md` §11), while `--validate` correctly still accepts a
structurally-valid empty `hashes` at exit 0 — so a *separate* promotion-mode check is required.

Cycle-006 resolves the **reversible-safe half** of the Rung-2 admission seam. Its governance/design work
(Track A — ratify 8a, record the `M` pre-registration procedure with no `M`, design the Cycle-007 fresh-evidence
batch, pre-register the verdict rule + fail-state language) is **already complete inside the SDD**
(`docs/cycles/cycle-006/02-sdd.md` §8–§10, importing the PRD §16.3 verdict rule by reference; OD-C6-6). **No
companion docs and no further planning artifact are required for Track A.** This sprint plan scopes **Track B
only**: one narrow hardening-class code sprint that builds the `--promotion-check` *gate*.

**Mission (binding).** Add a `--promotion-check` mode to `analysis/evidence_summary.py` and regression tests to
`tests/test_evidence_summary.py`, so a future Cycle-007 *promoted* evidence summary must pass the full hardened
validator **and** must carry a non-empty `hashes` integrity stamp. **The gate promotes nothing, writes nothing,
and does not mutate the ledger or the claim ceiling.** Building a gate is not admitting Rung 2.

**Sprint count: 1** (single focused, narrow sprint). The work touches one module + its test file; there is no
architectural seam that justifies a split (same single-sprint rationale as Cycle-004 and Cycle-005). **Do not
split into multiple implementation sprints unless a hard dependency is discovered at build time** — if so, the
implementer MUST stop and report rather than expand scope silently.

| Sprint | Title | Scope | Tasks |
|---|---|---|---|
| **Sprint 01** | Promotion-Check Hardening (`--promotion-check`) | **MEDIUM** | T1–T5 (5 tasks) |

> **Sizing rationale (MEDIUM, narrow).** SMALL would be defensible — the change is one new CLI arg + one new
> sibling driver + one test block. MEDIUM is chosen because the work is **test-first** (block-14 checks 14a–14f
> written failing before the driver), demands **strict CLI/behaviour preservation** of three existing modes
> (`generate`, `--validate`, `_refuse_tracked_out`) plus the `0/1/2/3` exit contract, and carries **invariant
> verification** (ledger byte-invariance, claim-ceiling untouched, `.claude/` clean, State-Zone unstaged) that
> the reviewer/auditor must independently confirm. It is MEDIUM in care, **narrow** in surface: still exactly two
> tracked code files, one new mode, one new driver, one new block.

---

## Binding posture (carried verbatim-in-intent from PRD §"Required posture" + SDD §13)

Cycle-006 is **preparation + one narrow hardening sprint.** Across the whole cycle the sprint preserves **all**
of:

- **No Rung-2 admission attempt.** No "beats random-legal" verdict of any kind.
- **No PASS / FAIL / INCONCLUSIVE verdict applied.** The verdict rule is *pre-registered* (PRD §16.3), never
  *executed* in Cycle-006.
- **No numeric margin `M`** chosen anywhere — and in particular **no `M` chosen against the already-observed
  K=20+20 bands** (PRD §10 contamination rule).
- **No SP-6** live-value promotion; no dispersion value reaches tracked status. `--promotion-check` **promotes
  nothing**.
- **No Rung-2 ledger row.** `docs/ledger.md` stays **byte-unchanged** at its two Rung-1 `regime-v001` rows
  (hash `2a2f1c2…`).
- **No claim-ceiling advance.** `docs/claim-ceiling.md` unchanged; the ledger remains the only ceiling-bearing
  artifact.
- **No fresh evidence generated; no new eval runs; no K=50 top-up; no K expansion.**
- **No OD-6 relaxation executed; no inferential statistic computed** (the validator *rejects* inferential terms;
  it does not produce them). OD-6 relaxation is **not adopted** (OD-C6-1 settled: descriptive disjoint-bands rule).
- **No cross-regime comparison** beyond preserving the existing mixed-regime refusal (exit 2).
- **No paired-delta tooling.**
- **No runtime-agent work;** agents stay frozen. **No gameplay-heuristic work;** no broad optimization (RL,
  self-play, deck optimizer, value/win-probability model, search/MCTS, ELO/tournament, dashboard, leaderboard).
- **No FunSearch work** (no dependency, interface, scaffold, integration, or candidate-search surface).
- **No Daily Top Episodes ingest; no Kaggle episode ingest;** no Kaggle automation. Daily Top Episodes remain
  local-only hypothesis input, never proof of improvement (SP-9).
- **No raw Competition Data / Pokémon Elements / traces / card names / deck lists / simulator logs** committed
  or staged.
- **No second validator module** (`analysis/evidence_summary_validate.py`), **no `*.schema.json` file**, **no
  third-party dependency**, **no promotion mode that writes to `docs/ledger.md`** — the in-module constant /
  one-module / stdlib-only / analysis-only-imports posture is preserved.
- **No edit to `analysis/aggregate.py` or `analysis/dispersion_report.py`** (import-only).
- **No edit to `eval/**`, `agents/**`, `sim/**`, `frozen/**`, `runs/**`.**
- **No `.claude/` (System Zone) edits.**
- **No State-Zone cleanup;** pre-existing dirty State-Zone files stay unstaged and untouched.
- **No new exit code** — the `0/1/2/3` contract is preserved verbatim (OD-C6-3).

**Rung 1 remains held for the whole cycle.**

The gate becomes **stricter or equal, never looser** (PRD NFR-1; SDD §4–§5). `--promotion-check` rejects a
*superset* of what `--validate` rejects — exactly `--validate`'s rejections **plus** empty/absent `hashes`. No
input the hardened `--validate` accepts that is also non-empty-`hashes`-and-clean is rejected; no input
`--validate` rejects becomes accepted. The **12 existing + block-13** checks remain green; new behaviour is
additive.

---

## Sprint 01 — Promotion-Check Hardening (`--promotion-check`)

### Sprint Goal

Add a `--promotion-check <summary.json>` mode to `analysis/evidence_summary.py` and a regression block (block 14)
to `tests/test_evidence_summary.py`, so a future Cycle-007 *promoted* evidence summary must pass the **full
hardened validator** and must carry a **non-empty `hashes` integrity stamp** — while holding Rung 1, leaving
`docs/ledger.md` byte-unchanged, promoting no value, generating no evidence, and preserving every existing
`generate` / `--validate` / exit-code behaviour. **The gate promotes nothing and writes nothing.**

### Scope: **MEDIUM** (5 tasks), narrow

Two tracked code files only. One new CLI mode (`--promotion-check`), one new sibling driver
(`_run_promotion_check` or equivalent), one new test block (14). `validate_summary`, `_run_validate`,
`build_summary`, generate mode, and `_refuse_tracked_out` are **behavior-unchanged**.

### The settled design (SDD §3–§7, grounded at HEAD `561fb92`)

- **OD-C6-2 — internal shape.** `--promotion-check` **re-reads the summary from disk**, calls **`validate_summary`
  wholesale** (the full hardened validator), and layers **exactly one promotion-only empty/absent-`hashes`
  precheck** on top. It does NOT compose a separate single pass and does NOT modify `validate_summary`. This
  guarantees parity-or-stricter with `--validate` by construction (SDD §4).
- **OD-C6-3 — exit-code behaviour.** The empty/absent-`hashes` promotion hard-fail **rides the existing exit 3**
  (fail-closed leak class). **No new exit code is introduced;** the `0/1/2/3` contract is preserved (SDD §3.2).
- **OD-C6-4 — CF-2 dedupe.** **Not required.** `--promotion-check` keys **solely on the exit code** and never
  consumes/emits the programmatic violation count, so the top-level duplicate-violation count (cosmetic,
  over-counts by 1 in the one top-level-digest-leak case) needs no dedupe (SDD §6).
- **OD-C6-5 — test layout.** The new regression checks live in a **new block 14** in
  `tests/test_evidence_summary.py`, immediately **after block 13** (which ends at 13l, the `"hashes.txt"`
  source-grep check). Fixtures are **stdlib-only synthetic**, reusing the existing harness — no K-batch, no raw
  data, no run-dir dependency beyond existing test helpers (SDD §7).
- **OD-C6-6 — governance/design placement.** Track-A deliverables live **inside the SDD** (§8–§10); **no
  companion docs.** The verdict rule is imported by reference to PRD §16.3 (SDD §10).
- **CF-3 — C2 word-adjacency note.** **Not required this cycle** — C2 is not revisited; `_affirmative_forbidden_words`
  / `_NEGATION_RE` are untouched (SDD §6).

### Source grounding at HEAD `561fb92` (the machinery the new mode reuses)

| Surface | Location (`561fb92`) | Promotion-check relevance |
|---|---|---|
| CLI dispatch + arg parsing | `main` `:509`; args `:518-527`; validate dispatch `:530-531` | `--promotion-check` is added here as a third dispatch branch (a new `argparse` arg mirroring `--validate` `:520-521`). |
| `--validate` driver (re-read + mixed-regime + validate) | `_run_validate` `:477-506` | The promotion path **reuses this shape**; the empty/absent-`hashes` precheck is the only delta. Read-failure block `:482-487` (exit 1); mixed-regime block `:489-494` (exit 2); validator block `:496-502` (exit 3); clean `:504-506` (exit 0). |
| Pure allow-list validator | `validate_summary` `:392-420` | **Re-run unchanged** by promotion-check (full hardened semantics). |
| Mixed-regime collector (exit 2) | `_collect_regime_ids` `:423-442`; used `:489-494` | Preserved; promotion-check inherits exit 2 for a mixed-regime summary. |
| Nested digest-shape enforcement (C1) | `_enforce_hashes_digest` `:347-363`; wired in `_walk` `:380-381` | Already runs inside `validate_summary`; a non-digest `hashes` value already exits 3 — the precheck need only assert **non-emptiness**. |
| Top-level `hashes` digest block | `validate_summary` `:408-419` | Existing top-level check; source of the cosmetic CF-2 double-report (not consumed; OD-C6-4). |
| Generate-mode empty-`hashes` WARNING (C4) | `:552-555` | **Preserved at exit 0** — promotion-check does not touch generate mode. |
| `--validate` empty-`hashes` acceptance | `validate_summary` returns `[]` for empty `hashes`; exit 0 | **Preserved** — the precheck is promotion-only, NOT in `validate_summary`. |
| Tracked-`--out` guard (C3) | `_refuse_tracked_out` `:449-474` | Untouched; promotion-check writes nothing, so it never reaches this guard. |
| Exit-code set | `0/1/2/3` (`:45-46`; `_run_validate` returns) | Preserved; the empty/absent-`hashes` hard-fail rides exit 3 (OD-C6-3). |
| `hashes.txt` absence | grep = 0 (`:551,554` are WARNING *text*, not a read) | Preserved; promotion-check reads no `hashes.txt`. |
| `--promotion-check` token | **absent** (only `:551,554` forward-reference WARNING text) | This sprint introduces the mode. |

**Test harness (reusable for the new block, all present at `561fb92`):** `check(name, cond, detail)` `:36`;
`make_run_dir(..., manifest_hash="")` for empty-hashes fixtures `:49-72` (used by 13j `:339-342`);
`validate_file_exit(obj, tmp, name)` `:75-80`; the clean `good` fixture and `_HEX64` digest `:33`; `es.main([...])`
CLI driver; the `REPO_ROOT/docs/ledger.md` byte-compare pattern (13j `:344-356`). Block 13 (C1–C4) ends at **13l**
(`:366-368`); a new block 14 fits immediately after it.

> **Anchor caveat (NFR-9 / SDD §2 / R6).** Every line anchor above is line-anchored to `analysis/evidence_summary.py`
> and `tests/test_evidence_summary.py` at HEAD `561fb92`. `/implement` MUST re-validate each anchor it relies on
> against the **build-time HEAD** before coding; anchors accurate now may desync if the files move. If any anchor
> has desynced or repo reality contradicts the SDD, **STOP and report** the concrete discrepancy before coding —
> do not silently adapt.

### Deliverables

- [ ] `--promotion-check <summary.json>` CLI arg added to `main` (a new `argparse` argument mirroring `--validate`'s
  shape; `metavar="summary.json"`, `default=None`), dispatched in the same block as `--validate`; documented
  precedence if both `--promotion-check` and `--validate` are supplied (prefer `--promotion-check`, the stricter
  mode). → **[G-5]**
- [ ] `_run_promotion_check(path_str) -> int` (or equivalent sibling driver) added beside `_run_validate`:
  re-reads JSON from disk; runs `_collect_regime_ids` (mixed-regime → exit 2); calls `validate_summary` wholesale
  (any violation → exit 3); after the validator is clean, hard-fails absent/empty `hashes` → exit 3; passes
  (exit 0) only when the summary is clean **and** `hashes` is a non-empty map. → **[G-5]**
- [ ] Empty/absent-`hashes` hard-fail rides **exit 3** (OD-C6-3); the `0/1/2/3` contract preserved; no new exit
  code. → **[G-5]**
- [ ] No promotion side effects: `--promotion-check` **writes nothing**, promotes nothing, reads no `hashes.txt`,
  reads no traces/sidecars, never writes to `docs/ledger.md` or any tracked `docs/` path. → **[G-5]**
- [ ] Existing behaviour preserved unchanged: `validate_summary`, `_run_validate` (`--validate`), `build_summary`,
  generate mode, and `_refuse_tracked_out` are **behavior-unchanged**. → **[G-6]**
- [ ] Regression block — new block `# --- 14. promotion-check ---` with checks 14a–14f (SDD §7) added to
  `tests/test_evidence_summary.py` after block 13 (13l); all 12 existing + block-13 checks preserved unmodified;
  stdlib-only synthetic fixtures; no K-batch dependency; no raw data. → **[G-5]**
- [ ] `docs/cycles/cycle-006/04-implementation-report.md` written with the full evidence set (see "Implementation
  report requirements"). → **[G-6]**

### Acceptance Criteria (PRD §16.2 / SDD §15, AC-1 … AC-8)

- [ ] **AC-1 — promotion-check passes a good summary:** `--promotion-check` on a clean, **non-empty-`hashes`**,
  schema-conforming summary → **exit 0**.
- [ ] **AC-2 — empty-`hashes` hard-fail:** `--promotion-check` on a **structurally-valid but empty-`hashes`**
  summary → **exit 3** (non-zero, fail-closed; CF-1 / OD-C5-2 floor).
- [ ] **AC-3 — full validator re-run:** `--promotion-check` on a summary carrying any forbidden field/value/word
  (affirmative `strong`, an inferential term, a cross-regime marker, a non-digest `hashes` value) → **exit 3** (it
  re-runs the full hardened validator). A **mixed-regime** summary → **exit 2** (single-regime guard inherited).
- [ ] **AC-4 — existing behaviour preserved:** generate-mode still emits the empty-`hashes` **WARNING at exit 0**;
  `--validate` still **accepts** a structurally-valid empty `hashes` at **exit 0**; the `0/1/2/3` contract holds
  (no new exit code).
- [ ] **AC-5 — no promotion side effects:** `--promotion-check` **writes nothing**; `docs/ledger.md` byte-unchanged
  (`2a2f1c2…`) before/after a promotion-check run; no tracked `docs/` write.
- [ ] **AC-6 — tests:** each behaviour has at least one runnable regression check; **all existing 12 + block-13
  checks remain green**; `python tests/test_import_direction.py` exit 0; `python eval/hygiene_check.py --paths …`
  exit 0 on the tracked artifacts.
- [ ] **AC-7 — posture held (hard):** Rung 1 held; `docs/claim-ceiling.md` untouched; **no `M`; no SP-6; no value
  promotion; no Rung-2 row; no fresh evidence generation; no `.claude/` drift; State-Zone files unstaged; no
  second module; no `*.schema.json`; no dependency; no ledger write.**
- [ ] **AC-8 — cadence:** lands only through `/implement → /review-sprint → /audit-sprint → operator acceptance`,
  so the promotion-mode gate is **reviewed and audited before any Rung-2 attempt uses it.**

### Technical Tasks (ordered)

> Each task lists its goal contribution `→ [G-N]`. T1 is preflight + anchor revalidation; T2 writes the **failing
> block-14 tests first**; T3 implements the `--promotion-check` mode to make them pass; T4 runs preservation and
> hygiene gates; T5 writes the implementation report. **Test-first is non-negotiable** (Goal-Driven Execution):
> the block-14 checks are the acceptance harness and map 1:1 to AC-1…AC-5.

#### T1 — Preflight / invariant verification + anchor revalidation → **[G-5, G-6]**

- [ ] Confirm build-time HEAD is `561fb92` or a descendant containing it; local branch not behind `origin/main`
  (`git rev-parse HEAD`; `git ls-remote origin main`).
- [ ] Confirm `git hash-object docs/ledger.md == 2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` and
  `git diff --exit-code -- docs/ledger.md` clean.
- [ ] Confirm `docs/claim-ceiling.md` clean (`git diff --exit-code -- docs/claim-ceiling.md`).
- [ ] Confirm `.claude/` clean and no code drift except the planned files:
  `git status --porcelain .claude/ frozen/ runs/ agents/ sim/ analysis/ tests/ eval/`.
- [ ] Confirm no staged files: `git diff --cached --name-only` empty.
- [ ] Confirm the pre-existing State-Zone files remain **unstaged and untouched** (`.beads/issues.jsonl`,
  `grimoires/loa/NOTES.md` modified-but-unstaged; do not stage, do not edit).
- [ ] **Revalidate every SDD source anchor** against build-time HEAD (NFR-9): in `analysis/evidence_summary.py` —
  `main` `:509`, args `:518-527`, validate dispatch `:530-531`, `_run_validate` `:477-506` (read-failure `:482-487`,
  mixed-regime `:489-494`, validator block `:496-502`, clean `:504-506`), `validate_summary` `:392-420`,
  `_collect_regime_ids` `:423-442`, `_enforce_hashes_digest` `:347-363`, top-level digest block `:408-419`,
  `_refuse_tracked_out` `:449-474`, empty-`hashes` WARNING `:552-555`, exit set `0/1/2/3` `:45-46`. In
  `tests/test_evidence_summary.py` — `check` `:36`, `make_run_dir` `:49-72` (with `manifest_hash=""` `:51,57`),
  `validate_file_exit` `:75-80`, `_HEX64` `:33`, block 13 end at 13l `:366-368`, the 13j ledger byte-compare
  pattern `:344-356`.
- [ ] Confirm no repo-reality contradiction. **If any anchor has desynced or repo reality contradicts the SDD,
  STOP and report** the concrete discrepancy before coding.

#### T2 — Add failing block-14 tests first → **[G-5]** (TEST-FIRST)

> Write these **before** the driver exists, so they fail (the mode is absent), then make them pass in T3. Fixtures
> are stdlib-only synthetic — reuse `check`, `make_run_dir` (incl. `manifest_hash=""` for empty-hashes summaries),
> `validate_file_exit`, the clean `good` fixture, `_HEX64`, and `es.main([...])`. Add a small
> `promotion_check_file_exit(obj, tmp, name)` helper that calls `es.main(["--promotion-check", path])`, paralleling
> `validate_file_exit` `:75-80`. **No K-batch, no raw data, no run-dir dependency beyond existing test helpers.**

- [ ] **Preserve all 12 existing + block-13 (13a–13l) checks** unmodified.
- [ ] Add a new block `# --- 14. promotion-check ---` inside `run_checks(tmp)` immediately after block 13 (after
  13l, `:366-368`); update `main()`'s summary line to include block 14.
- [ ] Add regression checks **14a–14f** as designed in SDD §7:

  | Check | Asserts | Maps to |
  |---|---|---|
  | **14a** promotion-check passes a good summary | `--promotion-check` on a clean **non-empty-`hashes`** `good` summary → **exit 0** | AC-1 |
  | **14b** empty-`hashes` hard-fail under promotion-check | `--promotion-check` on a structurally-valid **empty-`hashes`** summary (built via `make_run_dir(..., manifest_hash="")` → `build_summary`, `hashes == {}`) → **exit 3** | AC-2 |
  | **14b′** the same empty-`hashes` summary under `--validate` still passes | the identical empty-`hashes` summary under **`--validate`** → **exit 0** (preservation guard for the asymmetry) | AC-4 |
  | **14c** full validator re-run | `--promotion-check` on a summary carrying a forbidden field/value/word (affirmative `strong`, an inferential term, a cross-regime marker, or a non-digest `hashes` value) → **exit 3** (proves the full validator re-runs) | AC-3 |
  | **14d** generate-mode empty-`hashes` warning preserved | generate-mode empty-`hashes` still emits the stderr **WARNING at exit 0** (re-assert the 13j invariant under the new code) | AC-4 |
  | **14e** writes nothing; ledger byte-unchanged | `--promotion-check` writes nothing; `docs/ledger.md` **byte-unchanged before/after** a promotion-check run (byte-compare, mirroring 13j `:344-356`) | AC-5 |
  | **14f** mixed-regime inherited | `--promotion-check` on a **mixed-regime** summary → **exit 2** (single-regime guard inherited) | AC-3 / NFR-5 |

- [ ] **Keep stdlib-only synthetic fixtures.** No local K-batch dependency. No raw data. No run-dir dependency
  beyond the existing `make_run_dir` helper.

#### T3 — Implement `--promotion-check` in `analysis/evidence_summary.py` → **[G-5, G-6]**

> Implement the **OD-C6-2 wholesale-`validate_summary` + one empty/absent-`hashes` precheck** design (SDD §4),
> making the block-14 checks pass. Make `--promotion-check` parity-or-stricter with `--validate` by construction.

- [ ] Add the CLI arg `--promotion-check`, `metavar="summary.json"`, `default=None`, mirroring the existing
  `--validate` argument shape (`:520-521`). Help text (design-level): *"promotion gate: re-read this summary,
  re-run the full hardened validator, and additionally hard-fail empty/absent hashes; writes nothing, promotes
  nothing."*
- [ ] Dispatch `--promotion-check` in the same block as `--validate` (`:530-531`). If both `--promotion-check` and
  `--validate` are supplied, prefer `--promotion-check` (the stricter mode) — a single documented precedence
  choice, **not** a behaviour change to either existing mode.
- [ ] Add `_run_promotion_check(path_str) -> int` (or equivalent sibling driver) beside `_run_validate`
  (`:477-506`), with this control flow:
  1. **Re-read from disk** — load `path_str` as JSON with the *same* try/except shape as `_run_validate`
     (`:480-487`): `FileNotFoundError`/`OSError`/`json.JSONDecodeError` → stderr message, **exit 1**. (No new read
     surface; **no `hashes.txt`, no sidecar, no trace** — NFR-4.)
  2. **Mixed-regime guard** — `_collect_regime_ids(summary)`; `> 1` distinct regime → stderr REFUSED, **exit 2**
     (reuse `:489-494`). Preserve mixed-regime exit 2.
  3. **Full hardened validator** — `violations = validate_summary(summary)` (reuse **unchanged**, `:496`); any
     violation → print the same per-violation block as `_run_validate` (`:498-502`), **exit 3** (fail closed).
  4. **Empty/absent-`hashes` promotion precheck (the only added logic)** — after the validator is clean, evaluate
     `h = summary.get("hashes")`; hard-fail (**exit 3**) when `h` is empty or absent (`h is None`, `h == {}`, or
     `h` is not a non-empty dict), printing a fail-closed message naming CF-1 / OD-C5-2. The *per-value digest
     shape* of a non-empty map is already enforced by `validate_summary` (step 3, via `_enforce_hashes_digest`
     `:347-363` and the top-level block `:408-419`), so the precheck need only assert **non-emptiness**.
  5. **Pass** — if steps 1–4 all pass, print a VALID/gate-passed message and **exit 0**. **Write nothing. Promote
     nothing.**
- [ ] Pass at **exit 0 only** when the summary is clean **and** `hashes` is non-empty.
- [ ] **Use `_collect_regime_ids` and preserve mixed-regime exit 2.** **Call `validate_summary` wholesale.**
- [ ] **Read no `hashes.txt`; read no traces/sidecars.** Write nothing; promote nothing.
- [ ] **Do not modify `validate_summary` behaviour.** **Do not modify generate behaviour.** **Do not modify
  `--validate` behaviour.** **Do not modify `_refuse_tracked_out` behaviour.**
- [ ] **No `*.schema.json`, no second validator module, no third-party dependency** — the in-module constant /
  one-module / stdlib-only / analysis-only-imports posture is preserved (`tests/test_import_direction.py` green).
- [ ] Conservative-only proof obligation (NFR-1, for the reviewer/auditor): the set of inputs `--promotion-check`
  accepts is a **strict subset** of what `--validate` accepts — identical except the empty/absent-`hashes`
  summaries `--validate` accepts are *rejected* by `--promotion-check`. No `--validate`-rejected input is
  `--promotion-check`-accepted.

#### T4 — Preservation and hygiene checks → **[G-5, G-6]**

- [ ] `python tests/test_evidence_summary.py` → **exit 0** (all 12 existing + block-13 + block-14 14a–14f green).
- [ ] `python tests/test_import_direction.py` → **exit 0** (no new import; stdlib-only / analysis-only preserved).
- [ ] `python eval/hygiene_check.py --paths analysis/evidence_summary.py tests/test_evidence_summary.py
  docs/cycles/cycle-006/04-implementation-report.md` → **exit 0** on the tracked artifacts (the repo's established
  `--paths` invocation; `eval/hygiene_check.py:21,76`).
- [ ] `git hash-object docs/ledger.md` → `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` (byte-unchanged).
- [ ] `git diff --exit-code -- docs/ledger.md` → clean.
- [ ] `git diff --exit-code -- docs/claim-ceiling.md` → clean.
- [ ] `git status --porcelain .claude/` → empty (no `.claude/` drift); protected paths
  (`frozen/ runs/ agents/ sim/`) → no drift.
- [ ] `git diff --cached --name-only` → empty (nothing staged by the implementer).
- [ ] Confirm **no raw Competition Data, Pokémon Elements, traces, deck lists, simulator logs, Daily Top Episodes,
  or Kaggle episode data** is staged or embedded in any changed file (synthetic fixtures only; hygiene exit 0).

#### T5 — Implementation report → **[G-6]**

- [ ] Write `docs/cycles/cycle-006/04-implementation-report.md` with the full evidence set below (see
  "Implementation report requirements"). The later `/implement` output MUST report:
  - exact files changed;
  - exact tests run and exit codes;
  - whether the exit-code contract stayed `0/1/2/3`;
  - confirmation `--validate` empty-`hashes` behaviour stayed **exit 0**;
  - confirmation generate-mode empty-`hashes` warning stayed **exit 0**;
  - confirmation `--promotion-check` empty-`hashes` behaviour **exits 3**;
  - confirmation `docs/ledger.md` and `docs/claim-ceiling.md` were **untouched**;
  - confirmation **Rung 1 held**.

### Dependencies

- **Upstream:** accepted Cycle-006 PRD (`docs/cycles/cycle-006/01-prd.md`; OD-C6-1 ratified) + accepted SDD
  (`docs/cycles/cycle-006/02-sdd.md`; OD-C6-2…OD-C6-6 resolved); an explicit operator build gate (OA-2-class,
  `docs/operator/turntrace-loop-contract.md` §6; PRD §18), scoped to the two files only. This sprint plan
  self-authorizes nothing.
- **Task ordering:** T1 → T2 (failing tests first) → T3 (implement to pass) → T4 (gates) → T5 (report). T3 depends
  on T2; T4 depends on T2–T3; T5 depends on all prior tasks.
- **Read-only (import-only, never edited):** `analysis/aggregate.py`, `analysis/dispersion_report.py`,
  `eval/hygiene_check.py`.
- **External:** none. Stdlib-only; Python 3.14.0 local. No third-party dependency.
- **Track A (no dependency for this sprint):** the governance/design deliverables are **complete in the SDD**
  (§8–§10); no further planning artifact is required, and this sprint does not produce or modify them.

### Test plan

**Strategy (OD-C6-5).** New block 14 in `tests/test_evidence_summary.py`, immediately after block 13 (13l,
`:366-368`). Fixtures are **stdlib-only synthetic**, reusing the existing harness — no K-batch, no raw Competition
Data, no run-dir dependency beyond `make_run_dir`. The block-14 checks (14a–14f) are the acceptance harness and
map 1:1 to AC-1…AC-5.

| Check | Asserts | AC |
|---|---|---|
| 14a | `--promotion-check` on a clean **non-empty-`hashes`** `good` summary → exit 0 | AC-1 |
| 14b | `--promotion-check` on a structurally-valid **empty-`hashes`** summary → exit 3 (fail-closed) | AC-2 |
| 14b′ | the same empty-`hashes` summary under **`--validate`** still → exit 0 (asymmetry preservation guard) | AC-4 |
| 14c | `--promotion-check` on a forbidden field/value/word leak → exit 3 (full validator re-run) | AC-3 |
| 14d | generate-mode empty-`hashes` still emits the stderr **WARNING at exit 0** | AC-4 |
| 14e | `--promotion-check` writes nothing; `docs/ledger.md` byte-unchanged before/after (byte-compare) | AC-5 |
| 14f | `--promotion-check` on a **mixed-regime** summary → exit 2 (single-regime guard inherited) | AC-3 / NFR-5 |

**Preservation guards (must stay green).** All **12 existing + block-13 (13a–13l)** checks; `--validate`
empty-`hashes` exit 0; generate-mode empty-`hashes` WARNING exit 0; `_refuse_tracked_out` unchanged.

**Required test commands** (the implementer MUST run, and the report MUST record with exit statuses):

```bash
python tests/test_evidence_summary.py
python tests/test_import_direction.py
python eval/hygiene_check.py --paths analysis/evidence_summary.py tests/test_evidence_summary.py docs/cycles/cycle-006/04-implementation-report.md
git hash-object docs/ledger.md
git diff --exit-code -- docs/ledger.md
git diff --exit-code -- docs/claim-ceiling.md
git status --porcelain .claude/ frozen/ runs/ agents/ sim/
git diff --cached --name-only
```

**The ledger hash MUST equal `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`.** Any ledger-hash drift → HALT and
report.

### Risks & Mitigation (SDD §12 / PRD §17)

| ID | Risk | Mitigation |
|---|---|---|
| **R1** | **Scope-creep into admission** — the sprint drifts into a verdict / `M` / promotion / ceiling advance. | §"Binding posture" non-goals; `--promotion-check` promotes nothing and writes nothing (T3 step 5; AC-5); no `M`/SP-6/Rung-2 row; verdict rule pre-registered-not-applied (SDD §9). |
| **R2** | **Pre-registration contamination** — `M` chosen against the already-observed K=20+20 bands. | No `M` in any Cycle-006 artifact; the sprint touches no evidence and reads no bands (synthetic fixtures only); fresh never-observed evidence is a Cycle-007 act (PRD §10; SDD §8.3). |
| **R3** | **`--promotion-check` loosens or duplicates the gate.** | OD-C6-2 wholesale-`validate_summary` (parity-or-stricter by construction); conservative-only proof obligation (T3); 14a–14f + 12 + block-13 green (AC-6); empty-`hashes` hard-fail regression (14b/AC-2). |
| **R4** | **Ledger / docs mutation** via promotion-check or `--out`. | `--promotion-check` writes nothing (T3; §11/§10 SDD); C3 `_refuse_tracked_out` guard untouched and never reached; 14e byte-compare; `git diff --exit-code -- docs/ledger.md` clean (AC-5). |
| **R5** | **Dependency / second-module / `.schema.json` creep** while adding `--promotion-check`. | NFR-3; §"Forbidden files"; import-direction test green; one new sibling function, no new module; in-module constant preserved. |
| **R6** | **Citation rot** — anchors desync from source before build. | NFR-9 / T1: `/implement` re-validates every `:line` anchor at build-time HEAD; STOP-and-report on desync. |
| **R7** | **Exit-contract drift** — a new exit code expands `0/1/2/3`. | OD-C6-3: empty/absent-`hashes` rides exit 3; new code only on a strong sprint-surfaced reason (none found); 14a–14f pin `0/1/2/3`. |
| **R8** | **CF-2 over-count consumed programmatically.** | OD-C6-4: promotion-check keys on exit code only; violation count never consumed/emitted; no dedupe introduced. |
| **R9** | **FM-11 (contaminated evidence) / FM-10 (rule-assumption mismatch).** | No episode/Kaggle ingest; episodes hypothesis-only; simulator-authoritative; in-house contamination rule; hygiene parity; raw-data-in-git mechanically caught by `eval/hygiene_check.py` + validator hygiene parity. |
| **R10** | **Premature fresh-evidence generation** — a prep cycle runs an eval batch. | Generation is new eval scope, a separate Cycle-007 operator decision; the sprint runs no eval and creates no run dir (NG12); **HALT if attempted**. |

### Success Metrics (quantifiable)

- `python tests/test_evidence_summary.py` exit 0 — all 12 existing + block-13 (13a–13l) **plus** block-14 (14a–14f)
  green.
- `python tests/test_import_direction.py` exit 0.
- `python eval/hygiene_check.py --paths analysis/evidence_summary.py tests/test_evidence_summary.py
  docs/cycles/cycle-006/04-implementation-report.md` exit 0.
- `git hash-object docs/ledger.md` == `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`.
- `git diff --exit-code -- docs/ledger.md` exit 0 (byte-unchanged).
- `git diff --exit-code -- docs/claim-ceiling.md` exit 0 (untouched).
- `git status --porcelain .claude/ frozen/ runs/ agents/ sim/` empty (no protected-path drift).
- `git diff --cached --name-only` empty (nothing staged by the implementer).
- Exactly **two** App-Zone code files changed (`analysis/evidence_summary.py`, `tests/test_evidence_summary.py`)
  plus **one** Docs/State report (`docs/cycles/cycle-006/04-implementation-report.md`).
- Exit-code contract remains exactly `0/1/2/3` (no new code).

---

## Authorized implementation files

Only these paths are authorized for change in Sprint 01:

| Path | Zone | Authority |
|---|---|---|
| `analysis/evidence_summary.py` | App (tracked) | PRD §5, §7 C6-FR-5; SDD §3–§4, §13 |
| `tests/test_evidence_summary.py` | App (tracked) | PRD §7 C6-FR-5.6; SDD §7 |
| `docs/cycles/cycle-006/04-implementation-report.md` | Docs/State | loop contract (written under `/implement`) |

The standard later review/audit reports **may** be created by their own skills (not by the implementer's code
patch):

- `docs/cycles/cycle-006/05-review-report.md` (under `/review-sprint`)
- `docs/cycles/cycle-006/06-audit-report.md` (under `/audit-sprint`)

**No other tracked path is authorized.** If implementation appears to require another file, the implementer MUST
**stop and report** a concrete repo-reality reason before touching it; this sprint plan authorizes none. **No
second module** (`analysis/evidence_summary_validate.py`). **No `*.schema.json`.** **No third-party dependency.**

## Forbidden paths / stop conditions (no change authorized)

The implementer MUST NOT change any of:

- `docs/ledger.md`  ·  `docs/claim-ceiling.md`
- `.claude/**`
- `analysis/aggregate.py`  ·  `analysis/dispersion_report.py`  (import-only, read never edited)
- `eval/**`  (incl. `eval/hygiene_check.py` — import-only)  ·  `agents/**`  ·  `sim/**`  ·  `frozen/**`  ·  `runs/**`
- `grimoires/loa/context/**`  ·  `deck.csv`  ·  raw episode datasets / raw data paths
- dependency / manifest files (`requirements*.txt`, `pyproject.toml`, `setup.cfg`, etc.)
- any `*.schema.json`  ·  `analysis/evidence_summary_validate.py` (no second validator module)

No State-Zone cleanup: pre-existing dirty `.beads/issues.jsonl` + `grimoires/loa/NOTES.md` stay **unstaged and
untouched**.

**HALT and report** if any of the following is encountered or attempted:

- `git hash-object docs/ledger.md` ≠ `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` (ledger-hash drift).
- Any `.claude/` drift.
- Any value promoted / SP-6 issued / Rung-2 row written / ceiling advanced.
- Any numeric `M` chosen — and in particular any `M` chosen against the already-observed K=20+20 set.
- Any new eval run / K=50 top-up / fresh-evidence *generation*.
- Any Kaggle/episode ingest; any cross-regime comparison (beyond preserving the existing exit-2 refusal); any
  runtime-agent / gameplay-heuristic / FunSearch surface; any inferential statistic computed.
- A required existing check (12 + block-13) cannot stay green → **fix forward, never weaken a check.**
- A `--promotion-check` that cannot be made parity-or-stricter with `--validate`.
- Any source anchor desynced from the SDD, or any repo-reality contradiction → STOP and surface the concrete
  discrepancy before coding.

---

## Implementation report requirements

`docs/cycles/cycle-006/04-implementation-report.md` MUST include:

- **Preflight / invariant verification** (HEAD, ledger hash, claim-ceiling clean, `.claude/` clean, no code drift
  except the planned files, no staged files, State-Zone files unstaged/untouched).
- **Anchor revalidation notes** (each SDD anchor confirmed at build-time HEAD, or the concrete discrepancy that
  forced a stop).
- **Exact files changed** (exactly the authorized set: the two code files + this report).
- **`--promotion-check` implementation summary** (the new CLI arg + driver; the wholesale-`validate_summary` +
  empty/absent-`hashes` precheck design; conservative-only / parity-or-stricter proof).
- **Block-14 test summary** (14a–14f outcomes; the 12 existing + block-13 (13a–13l) checks remain green).
- **Exact commands run and exit codes** (the full Required-test-commands block).
- **Exit-code contract** — confirmation it stayed `0/1/2/3` (no new code).
- **`--validate` empty-`hashes` behaviour** — confirmation it stayed **exit 0**.
- **Generate-mode empty-`hashes` warning** — confirmation it stayed **exit 0**.
- **`--promotion-check` empty-`hashes` behaviour** — confirmation it **exits 3**.
- **Proof ledger hash unchanged** (`git hash-object docs/ledger.md` == `2a2f1c2…`; `git diff --exit-code` clean).
- **Proof claim ceiling untouched** (`docs/claim-ceiling.md` unchanged; `git diff --exit-code` clean).
- **Proof protected paths untouched** (`.claude/ frozen/ runs/ agents/ sim/` no drift; nothing staged).
- **Proof no raw data added** (no Competition Data / Pokémon Elements / traces / card names / deck lists /
  simulator logs / Daily-Top-Episode / Kaggle episode data; synthetic fixtures only; hygiene-check exit 0).
- **Proof no value promoted** (no dispersion value reaches tracked status; no SP-6).
- **Proof Rung 2 remains deferred** (no `M`; no Rung-2 row; no ceiling advance; no fresh evidence; no second
  module / `*.schema.json` / dependency / ledger write; `--promotion-check` is a **gate**, not a promoter).
- **Confirmation Rung 1 held.**
- **Final `git status --porcelain`.**
- **Any deviations or blockers.**

> **Reporting language (binding).** The report MUST state, verbatim in intent: *`--promotion-check` added and
> tested (re-reads the summary from disk, runs `validate_summary` wholesale, hard-fails empty/absent `hashes` at
> exit 3, passes at exit 0 only when clean and non-empty-`hashes`); generate-mode empty-`hashes` warning stayed
> exit 0; `--validate` empty-`hashes` acceptance stayed exit 0; the `0/1/2/3` exit contract held; `--promotion-check`
> writes nothing and `docs/ledger.md` is byte-unchanged; `docs/claim-ceiling.md` is untouched; no value promoted;
> no `M`; no SP-6; no Rung-2 row; no fresh evidence; the gate is closed as **hardening/preparation, not
> admission**; Rung 1 held; the Rung-2 attempt is deferred to Cycle-007 behind a separate explicit operator gate.*

---

## Review / audit focus notes

Reviewer (`/review-sprint`) and auditor (`/audit-sprint`) focus (SDD §4–§7, §12):

- [ ] **Independently test AC-1** — `--promotion-check` on a clean non-empty-`hashes` summary → exit 0.
- [ ] **Independently test AC-2** — `--promotion-check` on a structurally-valid empty-`hashes` summary → exit 3
  (fail-closed); confirm this is the *only* behavioural difference from `--validate` (which still → exit 0 on the
  same input).
- [ ] **Independently test AC-3** — a forbidden field/value/word leak under `--promotion-check` → exit 3 (full
  validator re-run); a mixed-regime summary → exit 2.
- [ ] **Confirm the conservative-only / parity-or-stricter property** — the inputs `--promotion-check` accepts are
  a strict subset of `--validate`'s accepted inputs (identical except empty/absent `hashes` is rejected); **no
  input `--validate` rejects is `--promotion-check`-accepted**; the 12 + block-13 checks remain green.
- [ ] **Confirm existing behaviour preserved** — generate-mode empty-`hashes` WARNING exit 0; `--validate`
  empty-`hashes` exit 0; `0/1/2/3` contract held (no new exit code); `validate_summary`, `_run_validate`,
  `build_summary`, `_refuse_tracked_out` byte-unchanged in behaviour.
- [ ] **Confirm no promotion side effects** — `--promotion-check` writes nothing; `git diff --exit-code --
  docs/ledger.md` clean (hash `2a2f1c2…`); no tracked `docs/` write; no `hashes.txt` / sidecar / trace read.
- [ ] **Confirm posture held** — Rung 1; claim-ceiling untouched; no `M`/SP-6/Rung-2 row/fresh evidence; no
  second module / `*.schema.json` / dependency; in-module constant / one-module / stdlib-only / analysis-only
  imports preserved (`test_import_direction` green).
- [ ] **Confirm sanitization** — no raw Competition Data / Pokémon Elements / traces / card names / deck lists /
  simulator logs / Daily-Top-Episode / Kaggle episode data in code, tests, or report; hygiene-check exit 0.
- [ ] **Confirm zone discipline** — only the two evidence-summary code files + standard `docs/cycles/cycle-006/`
  reports changed; forbidden paths untouched; State-Zone files unstaged; `.claude/` untouched.
- [ ] **Confirm the gate is closed as hardening/preparation, not admission** — the verdict rule is
  pre-registered-not-applied; Rung 2 deferred to Cycle-007; no value promoted.

---

## Operator gate reminder

- **This sprint plan opens no build gate.** Per `docs/operator/turntrace-loop-contract.md` §6 and PRD §18, the
  Cycle-006 `--promotion-check` sprint does **not** start until the operator **explicitly opens the OA-2-class
  build gate**, scoped to `analysis/evidence_summary.py` + `tests/test_evidence_summary.py` only. Planning
  artifacts never open the gate.
- **The sprint lands only through** `/implement → /review-sprint → /audit-sprint → operator acceptance` (AC-8), so
  the promotion-mode gate is **reviewed and audited before any Rung-2 attempt uses it.**
- **The Rung-2 *attempt* is deferred to Cycle-007 behind a separate explicit operator gate** (PRD §3, §19). A
  Cycle-007 attempt may proceed only when all of the PRD §19 conditions hold (Cycle-006 accepted; 8a ratified;
  `M` pre-registered against never-observed bands; a fresh, never-observed same-regime K≥20 batch generated under
  a justified `n`; `--promotion-check` live; provenance intact; the five readiness criteria; and an explicit
  operator gate). **Any unmet item → the Rung-2 attempt defers again.**

### Open operator decisions needed before `/implement`

| Decision | Status |
|---|---|
| **OD-C6-1 — 8a posture** (descriptive disjoint-bands rule vs OD-6 relaxation) | **Settled** — ratified by the operator (2026-06-19): the pre-registered descriptive disjoint-bands rule; OD-6 relaxation not adopted (PRD §18). No further action needed for this sprint. |
| **Build gate (OA-2-class) — `--promotion-check` sprint** | **REQUIRED before `/implement`.** The operator must explicitly open the build gate scoped to the two files. This sprint plan does not self-authorize. |
| OD-C6-2…OD-C6-6 (internal shape, exit code, CF-2 dedupe, test layout, artifact placement) | **Settled in the SDD** (§4, §3.2, §6, §7, §10). No further decision needed. |
| `M` / SP-6 / Rung-2 row / ceiling advance / fresh evidence | **Deferred to the Cycle-007 gate — none in Cycle-006.** |

**No other open operator decision blocks `/implement`** beyond the operator opening the build gate. With OD-C6-1
ratified and OD-C6-2…OD-C6-6 settled in the SDD, the sprint is mechanically ready once the gate opens.

---

## Goal traceability (Appendix C)

PRD goals (`docs/cycles/cycle-006/01-prd.md` §4) mapped to Sprint 01 tasks. Track-A goals (G1–G4) are **complete in
the SDD** (§8–§10) and produce no sprint code; Sprint 01 delivers **G5–G7** (the code goal + posture invariants).

| Goal | Description | Disposition / contributing tasks |
|---|---|---|
| **G1** | 8a posture ratified (descriptive disjoint-bands rule) | **Complete** — ratified (operator, 2026-06-19); recorded PRD §9/§18, SDD §9. No sprint code. |
| **G2** | `M` pre-registration procedure recorded (no `M`) | **Complete** — SDD §8. No sprint code; no `M`. |
| **G3** | Fresh-evidence batch designed (not generated) | **Complete** — SDD §9. No sprint code; no eval run. |
| **G4** | Verdict rule pre-registered (PASS/FAIL/INCONCLUSIVE + fail-state) | **Complete** — PRD §16.3, imported by SDD §9 by reference. No sprint code; never applied. |
| **G5** | Promotion-mode gate `--promotion-check` specified + implemented | **This sprint** — T1, T2, T3 (+ T4 gates). |
| **G6** | Carry-forwards addressed (CF-1 realised by G5; CF-2 not required; CF-3 not required) | **This sprint / settled** — CF-1 realised by T3; CF-2 not required (OD-C6-4); CF-3 not required (CF-3 / SDD §6). T2, T3. |
| **G7** | Rung 1 held; ledger byte-unchanged; no value promoted; no fresh evidence (hard) | **This sprint** — T1, T4 (verified end to end). |

**Goal-coverage check:** every PRD goal G1…G7 is accounted for — G1–G4 complete in the SDD, G5–G7 delivered by
Sprint 01. No sprint goal is orphaned.

**E2E posture-validation:** T4 is the cycle exit gate (single sprint). It runs the full Required-test-commands
block and proves the posture invariants (ledger byte-unchanged, claim ceiling untouched, protected paths
untouched, nothing staged, Rung 1 held, Rung 2 deferred). This is the P0 must-complete task. There is **no
separate same-regime E2E *evidence* task by design** — Cycle-006 promotes no value, generates no fresh evidence,
and applies no verdict; the E2E gate is the posture-and-hardening verification, not a verdict.

---

## Self-review checklist (sprint-plan QA)

- [x] The single code goal G5 (and the posture goals G6/G7) from the PRD are accounted for; G1–G4 are complete in
  the SDD (Track A) and produce no sprint code.
- [x] The single sprint is feasible as one iteration (one module + its test file).
- [x] All deliverables and acceptance criteria have checkboxes and are testable.
- [x] Technical tasks are specific and ordered (preflight → failing tests first → implement → gates → report).
- [x] Technical approach aligns with the SDD (OD-C6-2…OD-C6-6 + CF-3 honored verbatim).
- [x] Risks identified with mitigation (R1–R10).
- [x] Dependencies explicit (PRD/SDD + operator build gate; task ordering; import-only files; Track A complete).
- [x] All PRD goals mapped (Appendix C); none orphaned.
- [x] Tasks annotated with goal contributions.
- [x] Posture-validation gate (T4) included in the (single) final sprint.
- [x] Authorized files = 3 (two code + one report); forbidden files / stop conditions enumerated; stop-and-report
  rule stated.
- [x] Required test commands + ledger hash stated; operator gate reminder + open decisions recorded.
- [x] Sized SMALL/MEDIUM and narrow; not split into multiple implementation sprints.

---

## CLI / exit-code contract (preserved — SDD §3.2)

```
generate:        python analysis/evidence_summary.py <run_dir> [<run_dir> ...] [--json] [--out <local-path>]
validate:        python analysis/evidence_summary.py --validate <summary.json>
promotion-check: python analysis/evidence_summary.py --promotion-check <summary.json>   (NEW)

Exit codes (PRESERVED VERBATIM — no new code added):
  0  clean / valid / gate passed   (generate may carry a stderr WARNING for empty hashes — still exit 0;
                                     --validate accepts a structurally-valid empty hashes — exit 0;
                                     --promotion-check passes only when clean AND hashes non-empty)
  1  input failure (file unreadable / not JSON)
  2  mixed-regime refusal (single-regime guard)
  3  forbidden-field/value/word leak (fail-closed)  OR  (--promotion-check only) empty/absent hashes hard-fail
```

`--promotion-check` adds a stricter mode: it inherits exit 1/2/3 from `_run_validate`'s shape (re-read, mixed
regime, full validator) and additionally rides **exit 3** for an empty/absent `hashes` integrity stamp. **No exit
code changes meaning; none is added.** `generate` and `--validate` behaviour is byte-unchanged.

---

## Explicit non-goals (carried verbatim-in-intent from PRD §6 + SDD §13)

Sprint 01 does **none** of the following:

- No Rung-2 admission attempt; no "beats random-legal" verdict; **no PASS / FAIL / INCONCLUSIVE verdict applied**.
- **No numeric `M`** — and no `M` chosen against the already-observed K=20+20 bands.
- **No SP-6** live-value promotion; no value promoted to tracked status.
- **No Rung-2 ledger row;** `docs/ledger.md` byte-unchanged. **No claim-ceiling advance;** `docs/claim-ceiling.md`
  untouched.
- **No fresh-evidence generation; no new eval runs; no K=50 top-up; no K expansion.**
- **No cross-regime comparison** beyond preserving the existing mixed-regime refusal (exit 2). **No inferential
  statistic computed. No OD-6 relaxation executed.**
- **No paired-delta tooling.**
- **No runtime-agent work; no gameplay-heuristic work; no FunSearch.** No RL / self-play / deck optimizer / value
  model / search / MCTS / tournament / dashboard work.
- **No Daily Top Episodes ingest; no Kaggle episode ingest.** No raw Competition Data or Pokémon Elements.
- **No edits to `.claude/`.** **No edits to `docs/ledger.md` or `docs/claim-ceiling.md`.**
- **No edits to `analysis/aggregate.py` or `analysis/dispersion_report.py`.** **No edits to `eval/**`, `agents/**`,
  `sim/**`, `frozen/**`, `runs/**`.**
- **No second module; no `*.schema.json`; no third-party dependency; no new exit code; no promotion mode that
  writes any tracked path.**

---

## Sources and traceability

> **Primary authorities:** `docs/cycles/cycle-006/01-prd.md` (accepted PRD; OD-C6-1 ratified; FRs C6-FR-1…5; ACs
> §16.2; verdict rule §16.3; OD-C6-2…6 §15; non-goals §6; risks §17; operator decisions §18; Cycle-007 handoff §19);
> `docs/cycles/cycle-006/02-sdd.md` (accepted SDD — §3 CLI/exit, §4 validator flow, §5 empty-hashes hard-fail, §6
> CF-2/CF-3, §7 test strategy, §8–§10 Track A + artifact placement, §13 boundaries/non-goals, §14 decisions table,
> §15 sprint-plan handoff).
> **Supporting input (gitignored State Zone, not a tracked dependency):**
> `grimoires/loa/a2a/cycle-006/00-pre-prd-research.md` (recommends **B — Admission-Seam Preparation**; sprint
> shape: one sprint, Promotion-Mode Tooling; Rung-2 attempt deferred to Cycle-007).
> **Cycle-005 authorities:** `docs/cycles/cycle-005/07-closeout.md` (CLOSED/accepted/pushed; Rung 1 held; §4
> carry-forwards CF-1/CF-2/CF-3 + the Rung-2 admission seam); `06-audit-report.md` §11 (CF-1: promotion gate MUST
> hard-fail empty `hashes`; CF-2; CF-3); `02-sdd.md` §16 (Cycle-006+ deferred items — `--promotion-check`, seam
> 8a–8d, defensible `M` pre-registration, five readiness criteria, "only after review/audit and an explicit
> operator gate"); `03-sprint-plan.md` (the single-hardening-sprint structural precedent).
> **Tracked code (the gate, anchors at `561fb92`):** `analysis/evidence_summary.py` (`main` `:509`; args
> `:518-527`; `_run_validate` `:477-506`; `validate_summary` `:392-420`; `_collect_regime_ids` `:423-442`;
> `_enforce_hashes_digest` `:347-363`; top-level digest block `:408-419`; `_refuse_tracked_out` `:449-474`;
> empty-`hashes` WARNING `:552-555`; exit set `0/1/2/3` `:45-46`; **no `--promotion-check` token**; **no
> `hashes.txt`**); `tests/test_evidence_summary.py` (`check` `:36`; `make_run_dir` `:49-72` incl. `manifest_hash=""`
> `:51,57`; `validate_file_exit` `:75-80`; `_HEX64` `:33`; block 13 13a–13l ending at 13l `:366-368`; 13j ledger
> byte-compare `:344-356`).
> **Cycle-003 design authorities:** `04-evidence-summary-schema-spec.md` (§2 safe fields; §3 forbidden classes; §4
> JSON-first; summary carries no ceiling); `05-generator-validator-shape.md` (§2 allow-list / single-regime exit 2
> / exit-code contract / hygiene parity; NG12); `06-rung-2-ledger-convention.md` (§3 row cites summary by reference
> + hash — the empty-`hashes` hard-fail motivation); `07-od6-criterion-2-proposal.md` (§2 disjoint-bands rule; §3
> pre-registration procedure; §5 seam 8a–8d — bundling is "the highest-consequence, hardest-to-walk-back path").
> **Posture docs:** `docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` §2 (five conjunctive criteria);
> `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` (SP-6/SP-8/SP-9); `docs/failure-modes.md` (FM-10/FM-11);
> `docs/claim-ceiling.md` (Rung 1; forbidden words; never compare across regimes); `docs/ledger.md` (two Rung-1
> rows; hash `2a2f1c2…`); `docs/operator/turntrace-loop-contract.md` (§1 loop; §6 build gate; §7-§8 hygiene/claim
> language).
> Current main at authoring: `561fb92`. Claim ceiling: **Rung 1 (unchanged).** This sprint plan opens no
> implementation gate, builds no code, generates no evidence, mutates no ledger, advances no ceiling, promotes no
> value, applies no admission verdict, chooses no `M`, and edits no `.claude/`. **The Rung-2 attempt is deferred to
> Cycle-007 behind a separate explicit operator gate.**
