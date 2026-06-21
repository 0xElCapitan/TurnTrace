# Cycle-008 Sprint S02 — Co-located Fail-Closed Sanitizer: Implementation Report

> Sprint artifact (S02 — Co-located fail-closed sanitizer). Status: **IMPLEMENTATION COMPLETE — awaiting
> `/review-sprint` → `/audit-sprint` → operator acceptance.** This S02 pass adds the **co-located** fail-closed
> output sanitizer to the S01 diagnostic module: a pure `validate_diagnostic(obj)` + a `--validate
> <diagnostic.json>` CLI mode, sharing the one `SAFE_FIELDS` allow-list with the generator (SDD-C8-1). It lands
> every PRD C8-FR-3 rejection class — including the **new numeric-`M`-shaped governance-threshold** rule
> (SDD-C8-5) — on the existing `0/1/2/3` exit contract, plus one committed synthetic poisoned fixture per class and
> a path-rule **parity** test against `eval/hygiene_check.find_violations`. It implements **no**
> `analysis/ledger_validate.py`, **no** S03 ledger-row validation, and **no** S04 governance docs. It runs no eval,
> creates no fresh evidence, writes no SP-6, writes/edits no ledger row, advances no claim ceiling, selects/freezes
> no Rung-3 target / candidate / numeric margin `M` / `K` / `n` / regime id / feature family, edits no `.claude/`,
> and cleans/stages no State-Zone dirt. The generator (`build_diagnostic`) is **byte-unchanged**.
>
> **Sanitized note.** No raw traces, simulator logs, deck lists, card IDs/names, Pokémon Elements, Competition
> Data, Daily-Top-Episodes, Kaggle episode data, Discord/peer screenshots, run-dir dumps, PDFs/CSVs, `deck.csv`,
> `cg/`, raw evidence rows, dispersion/band/win-rate values, or any inferential statistic (no p-value, confidence
> interval, hypothesis test, std-dev, variance, or model estimate) appears here. **No numeric governance threshold
> `M` is chosen or stated** — the symbol `M` appears only where the sanitizer *names the class it rejects* and as
> asserted-rejected poison probes. No forbidden agent word (*strong / competitive / optimal / calibrated /
> complete*) applies. The committed poisoned fixtures carry only minimal synthetic placeholder strings necessary to
> prove rejection — no real card data, no Pokémon Elements, no raw deck content.

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-008 / Sprint **S02 — Co-located fail-closed sanitizer** |
| **Type** | App-Zone code/test (behind the OD-C8-6 OA-2 build gate, scoped to `analysis/` + `tests/`) |
| **Date** | 2026-06-20 |
| **Status** | **IMPLEMENTATION COMPLETE** — review/audit/acceptance pending; **not committed or pushed** in this pass |
| **Build-time HEAD** | `a0f755065390e3cdef27a43b2a0392201ea2d11f` — *feat: add Cycle-008 S01 trace diagnostic core* (== `origin/main`; not ahead/behind) |
| **Sprint-plan citation anchor** | `f2330d1` — the plan's authoring commit; the S02 block (`03-sprint-plan.md:487-556`) and SDD §3 (`02-sdd.md:210-244`) anchors re-validated at build-time HEAD (see §6) |
| **Operator gate** | **OD-C8-6 OPEN** — the OA-2-class build gate for the Cycle-008 App-Zone code lane (diagnostic + sanitizer + ledger-row validator + tests; scoped to `analysis/` + `tests/`); this `/implement` request is **S02 only** |
| **Claim ceiling (at S02)** | **Rung 2 — "beats random-legal"**; **held and preserved** (ceiling artifact byte-unchanged) |
| **Ledger invariant** | `docs/ledger.md` byte-unchanged; `git hash-object = 7da7e9a8dbed6561669d1569445eb9fe67a953fb` |
| **Ceiling invariant** | `docs/claim-ceiling.md` byte-unchanged; `git hash-object = 3d99759b919f7d75bc41ea81cd82e5f1fb974be7` |

---

## 1. Sprint goal & scope

**Goal (sprint plan `03-sprint-plan.md:489-492`).** "Add the **co-located** fail-closed output sanitizer to
`analysis/trace_diagnostic.py` — a pure `validate_diagnostic(obj)` + a `--validate` mode — that is
parity-or-stricter with `evidence_summary.py` / `hygiene_check.py`, rejects every PRD C8-FR-3 class (including the
**new numeric-`M`** rule) with the `0/1/2/3` exit contract, and **accepts the clean diagnostic output** (proving
RN-2's safe-key discipline holds)."

**Scope.** MEDIUM (4 tasks: S02.1–S02.4, `03-sprint-plan.md:537-544`). **Type:** App-Zone code/test.
**Operator gate:** OD-C8-6 open. This pass implements the **sanitizer only** (validator + `--validate` mode +
rejection classes + poisoned fixtures + parity test). The ledger-row validator (`analysis/ledger_validate.py`, S03)
and the governance docs (S04) are explicitly out of scope.

---

## 2. What was built

### 2.1 `analysis/trace_diagnostic.py` — co-located sanitizer (additive; generator byte-unchanged)

The sanitizer is added to the **same module** as the generator (SDD-C8-1, the `evidence_summary.py` pattern of
record), sharing the one `SAFE_FIELDS` allow-list ([analysis/trace_diagnostic.py:116](../../../analysis/trace_diagnostic.py))
so the doc↔code key-set cannot drift. The diff is **additive** (343 insertions; the 8 deletions are docstring/comment
rewords + the no-args message) — `build_diagnostic` and `render_json` bodies are untouched.

- **`validate_diagnostic(obj)`** ([analysis/trace_diagnostic.py:581](../../../analysis/trace_diagnostic.py)) — a
  pure, fail-closed, allow-list validator returning a list of `(field, reason)` violations (empty ⇒ valid). No I/O,
  no global state. It walks the object at **every nesting depth** ([:558](../../../analysis/trace_diagnostic.py),
  `_walk`) and rejects any key outside `SAFE_FIELDS` with the **most-specific reason**
  ([:495](../../../analysis/trace_diagnostic.py), `_classify_unknown_key`): decision-body marker > cross-regime >
  numeric-`M` > Rung-3 governance > quality/coaching > generic out-of-allow-list. A non-dict root is rejected.
- **`--validate <diagnostic.json>`** ([analysis/trace_diagnostic.py:692](../../../analysis/trace_diagnostic.py),
  arg; [:619](../../../analysis/trace_diagnostic.py), `_run_validate`) — the independent gate: re-reads the named
  file from disk, runs the mixed-regime guard (exit 2) then the leak validator (exit 3), else exit 0.
- **Rejection classes** — a parity-tested stdlib **copy** of `evidence_summary.py:233-365` (NOT an `eval/` import;
  the offline/runtime separation forbids `analysis/`→`eval/`):
  - hygiene path rules ([:358](../../../analysis/trace_diagnostic.py), `_HYGIENE_PATH_RULES`) — `cg/`, `cg.dll`,
    `libcg.so`, `deck.csv`, `.pdf`, `__MACOSX/`, `grimoires/loa/context/`, `runs/…`, `card*.csv`;
  - inferential vocabulary (std-dev/variance/CI/p-value/significance/hypothesis-test/error-bar);
  - affirmative forbidden agent words (immediate-negation suppression);
  - cross-regime key/value markers;
  - raw decision-body markers ([:402](../../../analysis/trace_diagnostic.py), `_DECISION_BODY_MARKERS`) — a parity
    **copy** of `evidence_summary._DECISION_BODY_MARKERS` (a test asserts equality / no drift);
  - SHA-256-digest enforcement on every `hashes`-keyed value ([:544](../../../analysis/trace_diagnostic.py),
    `_enforce_hashes_digest`) — the card-identity / Pokémon-Element gate.
- **New for Cycle-008** — the **numeric-`M`-shaped governance-threshold** rule (SDD-C8-5):
  ([:423](../../../analysis/trace_diagnostic.py), `_NUMERIC_M_KEY_RE` for a key + numeric value;
  `_NUMERIC_M_VALUE_RE` for a `M=… / promotion margin / comparison budget / threshold=…` value token). Rides the
  existing **exit-3** path — **no new exit code**.
- **Defense-in-depth value/key classifiers** (the diagnostic emits string values for `regime_id`/`mode`/`run_ids`/
  `unseeded_caveat`/`claim_ceiling`, so a value-smuggling vector exists that a key allow-list cannot see):
  Rung-3/promotion-governance semantics ([:432](../../../analysis/trace_diagnostic.py), `_GOVERNANCE_*_RE`) and
  externally-sourced raw content ([:443](../../../analysis/trace_diagnostic.py), `_RAW_CONTENT_VALUE_RULES` —
  Discord / peer / Kaggle / Daily-Top-Episode / raw simulator log / run-dir dump). Quality/scoring/recommendation/
  coaching is a **KEY**-only classifier ([:413](../../../analysis/trace_diagnostic.py), `_QUALITY_KEY_PATTERNS`),
  so the Rung-1 footer may legitimately say "no per-decision quality, score, or recommendation" without
  self-rejecting.
- **`--out` tracked-docs refusal preserved** — the S01 `_refuse_tracked_out`
  ([analysis/trace_diagnostic.py:656](../../../analysis/trace_diagnostic.py)) is unchanged and still active on the
  generate path.
- **Exit contract** — `0` produced/valid · `1` input failure · `2` mixed-regime refusal · `3`
  forbidden-field/value/word leak (fail-closed; never 0 on a leak) — identical in shape to
  `evidence_summary.py:46-48`.

### 2.2 Committed synthetic poisoned fixtures (`tests/fixtures/diagnostic/poisoned/`)

One minimal, synthetic fixture per rejection class (no real card/deck/trace/peer/Kaggle/Competition Data — only
placeholder poison strings). Each is single-regime so it exercises the **exit-3 leak** path (not exit-2):

| Fixture | Rejection class | Synthetic poison |
|---|---|---|
| `unknown_key.json` | out-of-allow-list (generic) | a `smuggled_unknown_field` key |
| `decision_marker.json` | raw decision-body marker key | `decision_latency_ms` as a key |
| `quality_key.json` | quality / scoring / coaching key | `decision_quality_score` |
| `inferential_value.json` | inferential vocabulary | a `p-value … significance` value |
| `forbidden_word.json` | affirmative forbidden agent word | "the agent is **strong**" |
| `crossregime_key.json` | cross-regime field | `regime_uplift` |
| `nonsha_hash.json` | card-identity / non-SHA-256 hash | a non-digest token under `hashes` |
| `hygiene_path.json` | Competition-Data path | a bare `cg/poison.dll` value |
| `numeric_m.json` | numeric-`M` / comparison-budget | `comparison_budget: 20` |
| `governance_rung3.json` | Rung-3 / promotion governance | `rung3_target_candidate` key |
| `raw_external_content.json` | externally-sourced raw content | a `discord screenshot; kaggle daily-top-episode` value |

The fixture **filenames/paths** are themselves Competition-Data hygiene-clean (no `cg/`, `deck.csv`, `.pdf`,
`card*.csv`, or `runs/` path segment) — the poison lives only in the JSON **values**, which `hygiene_check` (a
path-rule scanner) does not read.

### 2.3 `tests/test_trace_diagnostic.py` — extended in place (stdlib, plain-assert)

The S01 test module is extended (not replaced) with a new S02 section
([tests/test_trace_diagnostic.py:302-448](../../../tests/test_trace_diagnostic.py)). House style preserved: a
clean fixture validated at exit 0; granular `validate_diagnostic` reject-class probes
([:315](../../../tests/test_trace_diagnostic.py), `t_s02_reject_classes`); the `0/1/2/3` exit contract
([:361](../../../tests/test_trace_diagnostic.py)); `SAFE_FIELDS`-as-source-of-truth
([:383](../../../tests/test_trace_diagnostic.py)); hygiene path **parity**-or-stricter vs
`hygiene_check.find_violations` + superset ([:399](../../../tests/test_trace_diagnostic.py)); decision-body marker
parity vs `evidence_summary` ([:414](../../../tests/test_trace_diagnostic.py)); and per-fixture `--validate` exit-3
+ per-file path-hygiene coverage ([:421](../../../tests/test_trace_diagnostic.py)). Total **173 checks** (S01's 42
preserved + S02 additions), all driven off `tests/` fixtures with **no dependence on the gitignored `runs/`**.

---

## 3. Commands run & results

All run at build-time HEAD `a0f7550`. Smallest-sufficient first, then the relevant regression checks.

| # | Command | Result |
|---|---|---|
| 1 | `python analysis/trace_diagnostic.py <clean-run-dir> --out <tmp>/clean-diag.json` then `--validate <tmp>/clean-diag.json` | gen exit **0**; validate exit **0** — the diagnostic's own output passes its own sanitizer (RN-2) |
| 2 | `python analysis/trace_diagnostic.py --validate tests/fixtures/diagnostic/poisoned/<each>.json` (×11) | exit **3** for every poisoned class (fail-closed) |
| 3 | `python tests/test_trace_diagnostic.py` | exit **0** — **173 checks pass, 0 FAIL** (S01 42 + S02) |
| 4 | `python tests/test_import_direction.py` | exit **0** — runtime/offline separation intact |
| 5 | `python tests/test_evidence_summary.py` | exit **0** — no regression (12 + hardening 13a–13l + promotion 14a–14f) |
| 6 | `python tests/test_smokes.py` | exit **0** — **72 tests OK** (no regression) |
| 7 | `python eval/hygiene_check.py --paths <13 touched artifacts, per-file>` | exit **0** — clean; no Competition-Data paths |
| 8 | `git diff --stat analysis/trace_diagnostic.py` | `343 insertions(+), 8 deletions(-)`; the 8 deletions are docstring/comment rewords + the no-args message — `build_diagnostic`/`render_json` bodies unchanged |
| 9 | `git hash-object docs/ledger.md` | `7da7e9a8…` (byte-unchanged) |
| 10 | `git hash-object docs/claim-ceiling.md` | `3d99759b…` (byte-unchanged) |
| 11 | `git status --porcelain .claude/` | empty (System Zone clean) |
| 12 | `git diff --cached --name-only` | empty (nothing staged; protected dirt + S02 changes left unstaged) |

---

## 4. Acceptance-criteria verification

Each S02 acceptance criterion (`03-sprint-plan.md:513-534`) is quoted verbatim, with status and file:line evidence.

1. **Each poisoned class rejected fail-closed.** "card name · raw decision-body field (e.g. `decision_latency_ms`
   as a key) · inferential term · affirmative forbidden agent word · cross-regime field · non-SHA-256 hash ·
   numeric-`M`-shaped token → **exit 3** (never exit 0 on a leak)." — **✓ Met.** One committed poisoned fixture per
   class (§2.2); [tests/test_trace_diagnostic.py:421](../../../tests/test_trace_diagnostic.py)
   (`t_s02_poisoned_fixtures`) asserts each `--validate` exits 3 with the class-specific reason, and
   [:315](../../../tests/test_trace_diagnostic.py) (`t_s02_reject_classes`) adds granular probes (every marker,
   every quality/coaching key, key + value forms of cross-regime / numeric-`M` / Rung-3). Command #2.

2. **Clean fixture accepted (C8-FR-3.3; RN-2).** "`python analysis/trace_diagnostic.py --validate
   <clean-diagnostic.json>` exits **0** — the diagnostic's own legitimate output (safe aggregate keys) passes its
   own sanitizer." — **✓ Met.** [analysis/trace_diagnostic.py:581](../../../analysis/trace_diagnostic.py)
   (`validate_diagnostic` returns `[]` on the generated output);
   [tests/test_trace_diagnostic.py:302](../../../tests/test_trace_diagnostic.py) (`t_s02_clean_validates`)
   generates the clean diagnostic from the committed clean run-dir fixture and asserts both `validate_diagnostic(diag)
   == []` and `--validate` exit 0. Command #1. (The "clean fixture" is the **actual S01 diagnostic output**,
   produced at test time from the existing `clean/run-syn-a-01/` fixture, so it can never drift from the generator.)

3. **Parity (C8-FR-3.1).** "a test mirrors the existing parity test — the path-rule surface matches
   `eval/hygiene_check.find_violations` for the path-rule class (parity-or-stricter), without importing `eval/`." —
   **✓ Met.** [tests/test_trace_diagnostic.py:399](../../../tests/test_trace_diagnostic.py) (`t_s02_hygiene_parity`)
   asserts every path `hygiene_check.find_violations` refuses is also refused by
   `td._hygiene_path_violation` (parity-or-stricter), plus a superset case (a content leak the path gate cannot
   express). The module imports no `eval/` (Criterion 5); the test references `hygiene_check` only as a parity
   target (tests are outside the import-direction zone).

4. **Exit-code contract.** "`0` clean/valid · `1` input failure · `2` mixed-regime refusal · `3`
   forbidden-field/value/word leak — identical in shape to `evidence_summary.py:46-48`; **no new exit code**." —
   **✓ Met.** [analysis/trace_diagnostic.py:619](../../../analysis/trace_diagnostic.py) (`_run_validate`);
   [tests/test_trace_diagnostic.py:361](../../../tests/test_trace_diagnostic.py) (`t_s02_exit_contract`) asserts
   exit 1 (missing file), exit 2 (a two-regime diagnostic, precedence over leak check), exit 3 (poison); exit 0 in
   `t_s02_clean_validates`. The module docstring exit set ([:56](../../../analysis/trace_diagnostic.py)) matches.

5. **Import direction & stdlib (NFR-1, NFR-2).** "`test_import_direction.py` exits 0; the sanitizer reuses the
   **copied** hygiene surface, not an `eval/` import." — **✓ Met.** Command #4 exits 0; the new code adds only
   `import re` (stdlib) — [analysis/trace_diagnostic.py:63](../../../analysis/trace_diagnostic.py) — and the
   rejection-class surface is a parity-tested copy ([:358](../../../analysis/trace_diagnostic.py),
   [:402](../../../analysis/trace_diagnostic.py)), not an `eval/`/`sim`/`cabt` import. The existing
   `t_import_direction` ([tests/test_trace_diagnostic.py:170](../../../tests/test_trace_diagnostic.py)) re-runs
   green within the suite.

6. **Generator behaviour unchanged.** "S01's `build_diagnostic` output is byte-identical for the existing fixtures
   (the new code is the validator + `--validate` mode, not a generator change) — verified by diff / re-running the
   S01 surfaces test green." — **✓ Met.** Command #8 shows the diff touches no `build_diagnostic`/`render_json`
   body line; the S01 surface checks (`t_five_surfaces`, `t_keyset_subset_safe_fields`, `t_marker_disjoint`,
   `t_no_new_statistic`, `t_json_roundtrip`) all re-run green inside the 173-check suite (Command #3).

7. **Hygiene.** "`eval/hygiene_check.py` clean on the touched tracked artifacts; poisoned fixtures live under
   `tests/` as test inputs (no raw real data — synthetic poison strings only)." — **✓ Met.** Command #7 exits 0
   over all 13 touched artifacts with **per-file** coverage (shallow directory handling);
   [tests/test_trace_diagnostic.py:421](../../../tests/test_trace_diagnostic.py) additionally asserts each fixture
   path is hygiene-clean and lives under `tests/`, not `runs/`. Poison is synthetic placeholder strings only (§2.2).

8. **Non-occurrence.** "no second validator module; no `*.schema.json`; no `eval/`/`sim`/`cabt` import; no new
   dependency; no new exit code; no `M` in any tracked artifact except as a rejected token in a poisoned fixture;
   `docs/ledger.md` unchanged (`7da7e9a8…`); `docs/claim-ceiling.md` unchanged." — **✓ Met.** The sanitizer is
   co-located in `trace_diagnostic.py` (no second module, no schema file); the only added import is stdlib `re`;
   the exit set stays `0/1/2/3`. No numeric governance margin is **stated** anywhere — the symbol `M` appears only
   where the sanitizer *names the class it rejects* (`_NUMERIC_M_*`) and as **asserted-rejected** poison probes
   (the `numeric_m.json` fixture carries the comparison-budget variant; the literal-`M` rejection is proven by an
   inline asserted-rejected probe, mirroring `evidence_summary`'s forbidden-word probes). Commands #9, #10 (§6).

9. **`/review-sprint` + `/audit-sprint` both pass; operator accepts.** — **⏸ Pending** (downstream gates; not part
   of this `/implement` pass).

**`/implement`-args criteria** map onto the above: clean-validates (AC2), poison-fails / unknown / decision-marker /
quality / forbidden-content / numeric-`M` (AC1), `SAFE_FIELDS` source-of-truth
([tests/test_trace_diagnostic.py:383](../../../tests/test_trace_diagnostic.py), `t_s02_safe_fields_source_of_truth`),
`--out` tracked-docs refusal still works (S01 `t_out_refuses_tracked_docs` re-runs green; the guard is unchanged),
and `runs/`-independence ([:447](../../../tests/test_trace_diagnostic.py), `t_s02_runs_independence`).

---

## 5. Changed files & final status

**Modified / new — all under the sanctioned `analysis/` + `tests/` + this cycle's `docs/` lane:**

- `analysis/trace_diagnostic.py` (M — additive sanitizer; generator byte-unchanged)
- `tests/test_trace_diagnostic.py` (M — extended with the S02 section)
- `tests/fixtures/diagnostic/poisoned/` (NEW — 11 synthetic poisoned fixtures)
- `docs/cycles/cycle-008/06-s02-implementation-report.md` (NEW — this file)

**Final `git status --porcelain`** (changes left unstaged; not committed or pushed):

```
 M .beads/issues.jsonl
 M analysis/trace_diagnostic.py
 M grimoires/loa/NOTES.md
 M tests/test_trace_diagnostic.py
?? docs/cycles/cycle-008/06-s02-implementation-report.md
?? grimoires/loa/README.draft.md
?? tests/fixtures/diagnostic/poisoned/
```

`.beads/issues.jsonl`, `grimoires/loa/NOTES.md`, and `grimoires/loa/README.draft.md` remain the pre-existing
State-Zone dirt — **modified/untracked-unstaged, not edited, not staged, not cleaned** by this pass.

---

## 6. Invariant & citation-anchor verification

- **HEAD / origin parity:** `git rev-parse HEAD == origin/main == a0f755065390e3cdef27a43b2a0392201ea2d11f`.
- **Ledger invariant:** `git hash-object docs/ledger.md = 7da7e9a8dbed6561669d1569445eb9fe67a953fb` (byte-unchanged).
- **Ceiling invariant:** `git hash-object docs/claim-ceiling.md = 3d99759b919f7d75bc41ea81cd82e5f1fb974be7`
  (byte-unchanged); **claim ceiling remains Rung 2** (`docs/claim-ceiling.md:11`).
- **System Zone:** `git status --porcelain .claude/` empty; **nothing staged** (`git diff --cached --name-only`
  empty).
- **Citation anchors re-validated at build-time HEAD (NFR-12):** sprint-plan S02 block (`03-sprint-plan.md:487-556`)
  and SDD §3 sanitizer design (`02-sdd.md:210-244`, rejection-class table `:216-227`); the parity-source surface
  `evidence_summary.py:233-365` (hygiene rules `:233-243`, inferential `:248-259`, forbidden words `:271-274`,
  cross-regime `:278-281`, markers `:285-290`, `_enforce_hashes_digest` `:349-365`, `validate_summary` `:394`,
  `_refuse_tracked_out` `:451-476`, exit set `:46-48`); `eval/hygiene_check.py` rules `:35-45` and
  `find_violations` `:52`; `eval/schemas.md` card-identity digest `:13-15` and decision/terminal rows `:60-91` —
  all accurate at `a0f7550`.

---

## 7. Known limitations / carry-forward

- **Sanitizer only.** `analysis/ledger_validate.py` (S03 ledger-row validation), the S04 governance docs, and S05
  closeout are **out of scope for S02** and are not present.
- **Player-scoping carry-forward — DEFERRED (recorded here, not in NOTES.md).** The S01 review/audit note observed
  that `build_diagnostic` aggregates the latency / board / prize decision-row surfaces over **all** decision rows
  rather than scoping to `player == "agent"` rows. This pass **defers** it as carry-forward, for these reasons:
  - It is a **generator** change, but S02's acceptance criteria require the generator output to be **byte-identical**
    for the existing fixtures and frame the new code as "the validator + `--validate` mode, **not a generator
    change**" (`03-sprint-plan.md:526-528`). Touching the decision-row loop would cross that sprint boundary.
  - All committed fixture decision rows carry `player == "agent"` (8/8), so a `player`-scoped guard would be
    byte-identical on them — meaning the scoping **could not be proven** without authoring a **new dual-player
    synthetic fixture**, which expands the fixture + review surface beyond "tiny/local."
  - It raises a non-trivial semantic question (whether `n_decisions` and each surface should also be agent-scoped)
    that properly belongs to a generator-class slice, not the sanitizer slice.
  - The board/prize surfaces are already two-sided (`p0`/`p1` split), so no side's data is conflated into a single
    misleading number; the `unseeded_caveat` framing already states the diagnostic reflects "the whole unseeded
    process," so whole-process latency is a defensible **descriptive** choice, not a correctness defect.

  **Fallback semantics (documented per the task).** When a future trace **omits** `player`, the diagnostic
  continues to aggregate all decision rows — the safe descriptive default (current behaviour, unchanged). When
  `player` is **present** and includes opponent rows, the current generator includes them; the carry-forward is to
  prefer `player == "agent"` (player-0) rows for the latency / board / prize surfaces when the field is present.
  Recommended home: a small generator-class follow-up sprint (S01-class), with a dual-player synthetic fixture to
  prove the scoping. *(NOTES.md is a protected State-Zone artifact this pass and must not be edited, so this
  deferral is recorded in this tracked implementation report instead.)*
- **RN-2 round-trip is the load-bearing property.** The generator emits safe aggregate keys disjoint from
  `_DECISION_BODY_MARKERS`, so its clean output validates at exit 0; any future regression that leaks a raw marker
  name as an output key fails the co-located sanitizer (exit 3) and the disjointness test.

**Stop point.** S02 implementation only. No review, audit, S03, S04, or S05 work performed; nothing committed or
pushed.
