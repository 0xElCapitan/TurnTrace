# Cycle-004 Sprint 01 — Senior Lead Review Report

> Review artifact (`/review-sprint sprint-01`). **Verdict: PASS WITH NOTES — ready for `/audit-sprint sprint-01`.**
> Persisted at operator request after the write-disabled `reviewing-code` pass (C-PROC-001 / skill-invariants).
> Nothing was staged, committed, or pushed by the review or this persistence step.
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, or Competition Data appear here (CC-1/CC-2, ESP).
> **No dispersion metric values appear here** — no evidence value from the local exercise output was read or
> cited. The forbidden agent words (*strong / competitive / optimal / calibrated / complete*) and the
> inferential terms (*std-dev / variance / CI / p-value / significance / hypothesis-test / error-bar*) appear
> only as the negated/forbidden language they are (e.g. as validator-rejection examples). **Rung 1 held.**

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-004 · Sprint 01 (`C4-S01`) |
| **Skill** | `/review-sprint sprint-01` (`reviewing-code`, pure-review / write-disabled) |
| **Build-time HEAD** | `8ac161d` — *docs: plan TurnTrace Cycle-004* |
| **Verdict** | **PASS WITH NOTES** — ready for `/audit-sprint sprint-01` |
| **Reviewed files** | `analysis/evidence_summary.py`, `tests/test_evidence_summary.py`, `docs/cycles/cycle-004/04-implementation-report.md` |

---

## Verdict: PASS WITH NOTES — ready for `/audit-sprint sprint-01`

All acceptance criteria are met, all 12 required tests pass, and **every binding bright line holds**. Three
non-blocking robustness gaps and several minor notes are documented below; none crosses a posture line or
fails an AC, and all concern hardening the validator for the *future* Cycle-005 promotion gate (where it
becomes load-bearing), not this build-only cycle (where it gates only the generator's own clean output).

---

## 1. Pre-review checks

| Check | Result |
|---|---|
| Branch / HEAD | `main` @ `8ac161d0a76e9b15056afaaf5b440766cc61e40d` ✓ |
| Started from baseline `8ac161d` (or descendant containing it) | HEAD **==** `8ac161d`; `git merge-base --is-ancestor 8ac161d HEAD` → YES ✓ |
| No staged files | `git diff --cached --name-only` → empty ✓ |
| State-Zone dirty files unstaged | `.beads/issues.jsonl`, `grimoires/loa/NOTES.md` → modified, **unstaged** (pre-existing; both were `M` at session start) ✓ |
| `.claude/` drift | `git status --porcelain .claude/` → empty ✓ |
| `docs/ledger.md` hash | `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` — **byte-unchanged** ✓ |
| `git diff --exit-code -- docs/ledger.md` | clean (exit 0) ✓ |
| Claim ceiling | **Rung 1** (`docs/claim-ceiling.md`) ✓ |
| Local exercise output gitignored + unstaged | `git check-ignore -v` → `.gitignore:17`; absent from tracked status ✓ |

**Changed tracked files** (exactly the three authorized, all untracked/unstaged):
- `?? analysis/evidence_summary.py`
- `?? tests/test_evidence_summary.py`
- `?? docs/cycles/cycle-004/04-implementation-report.md`

No `*.schema.json`, no `analysis/evidence_summary_validate.py`, no `requirements.txt`/`pyproject.toml`
(verified absent).

## 2. Command results

| Command | Exit |
|---|---|
| `python tests/test_evidence_summary.py` | **0** (12 checks / 37 assertions) |
| `python tests/test_import_direction.py` | **0** |
| `python eval/hygiene_check.py --paths analysis/evidence_summary.py tests/test_evidence_summary.py docs/cycles/cycle-004/04-implementation-report.md` | **0** |
| `git hash-object docs/ledger.md` | `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` |
| `git diff --exit-code -- docs/ledger.md` | **0** |
| `git status --porcelain .claude/ frozen/ runs/ agents/ sim/` | empty |
| `git diff --name-only` | `.beads/issues.jsonl`, `grimoires/loa/NOTES.md` (State-Zone, unstaged) |
| `git diff --cached --name-only` | empty |
| `git check-ignore -v …evidence-summary-local.json` | `.gitignore:17` (ignored) |

*(No evidence values from the exercise output were read or cited.)*

## 3. Code review — generator (`analysis/evidence_summary.py`)

| # | Requirement | Verdict | Evidence |
|---|---|---|---|
| 1 | Reads each `manifest.json` first | ✓ | manifests loaded before any aggregation (`:153-159`) |
| 2 | `manifest.json` is the `regime_id` authority | ✓ | `regimes = {man.get("regime_id") …}` (`:160`); record-vs-manifest cross-check (`:168-171`) |
| 3 | `match_results/*` only via `aggregate.aggregate_run` | ✓ | sole match read (`:167`); no manual `match_results` glob |
| 4 | Reuses `descriptive_stats` | ✓ | imported + applied (`:80`, `:200-203`) |
| 5 | Reuses `DISPERSION_METRICS` / `STAT_COLUMNS` | ✓ | imported, not redefined (`:78-79`) |
| 6 | No new metric / statistic | ✓ | only the reused 6 metrics × 7 stats; nothing computed locally |
| 7 | Mixed regimes → exit 2 | ✓ | `MixedRegimeRefusal` (`:161-166`) → `main` returns 2 (`:489`) |
| 8 | No eval invocation | ✓ | reads only; no `run_eval`/`aggregate_and_ledger` |
| 9 | No run-dir creation | ✓ | only `out_path.parent.mkdir` for `--out` (local output dir) |
| 10 | No sidecar-dir reference | ✓ | zero `trace` tokens in source (grep + T5 check 4) |
| 11 | JSON-first primary | ✓ | `render_json` is the only renderer; generate-mode always JSON |
| 12 | Unseeded-process caveat in output | ✓ | `_UNSEEDED_CAVEAT` in summary (`:91-95`, `:213`) |
| 13 | Rung-1 / no-ceiling-of-its-own framing | ✓ | `_RUNG1_FOOTER` (`:96-101`, `:214`) |
| 14 | Writes only stdout / explicit local `--out` | ✓ | `:507-515` |
| 15 | Never writes to `docs/` | ✓ (with note C3) | `_refuse_tracked_out` (`:410-421`) |
| 16 | Never mutates `docs/ledger.md` | ✓ | ledger byte-unchanged (verified); basename guard (`:418-421`) |

## 4. Code review — validator

| # | Requirement | Verdict | Evidence |
|---|---|---|---|
| 1 | `validate_summary(obj)` pure | ✓ | no I/O, reads only its arg (`:353-381`) |
| 2 | `--validate` re-reads from disk | ✓ | `json.loads(p.read_text())` (`:428`) — validates the file, not in-memory output |
| 3 | Unknown fields fail closed | ✓ | `_walk` allow-list (`:337-339`) |
| 4 | Leaks → exit 3 | ✓ | `:447-449` |
| 5 | Mixed-regime → exit 2 | ✓ | `_collect_regime_ids` checked first (`:437-441`) |
| 6 | Input failure → exit 1 | ✓ | `:429-435` |
| 7 | Clean → exit 0 | ✓ | `:451-454` |
| 8 | All doc 04 §3 classes rejected w/ reasons | ✓ (see C1 for a positional gap) | raw-body markers, hygiene paths, digest-shape, inferential, cross-regime, forbidden-word (`:262-330`) — all tested (T5 check 2) |
| 9 | Hygiene parity = local copy, not `eval/` import | ✓ | `_HYGIENE_PATH_RULES` is a **verbatim** copy of `hygiene_check._RULES` (same 9 rules, same order, same reasons; `_norm_path` == `_norm`); live parity asserted (T5 check 5). No `eval` import (T5 check 12) |
| 10 | Benign `hypothesis` text-field accepted | ✓ | compound-only rule `hypothesis[\s\-]?test(ing)?` (`:240-241`); T5 check 8 |
| 11 | Inferential `hypothesis-test` rejected | ✓ | same rule; T5 check 8 |
| 12 | No inferential statistic computed | ✓ | rejects terms; computes none (reuses `descriptive_stats`) |

## 5. Schema posture

| # | Requirement | Verdict |
|---|---|---|
| 1 | `SAFE_FIELDS` in-module | ✓ (`:83-89`) |
| 2 | No `evidence_summary_schema.json` | ✓ (absent) |
| 3 | No `*.schema.json` | ✓ (absent) |
| 4 | No `evidence_summary_validate.py` | ✓ (absent) |
| 5 | No third-party schema dependency | ✓ (stdlib + intra-zone only; T5 check 12) |
| 6 | `SAFE_FIELDS` agrees with doc 04 §2 | ✓ (T5 check 9 — literal transcription vs constant) |
| 7 | `--print-schema` deferred | ✓ (not implemented; documented OD-C4-5 DEFER) |

## 6. Test review (`tests/test_evidence_summary.py`)

- **stdlib-only plain-Python** module, `main()` → exit 0/1 ✓
- **synthetic temp-dir fixtures only** (`tempfile.TemporaryDirectory`, `make_run_dir`) ✓; the only `runs/…`
  reference is a **string-literal probe** in the hygiene-parity test, not a real read ✓
- **no dependency on gitignored K-batch runs** ✓
- **All 12 required checks present and meaningful** (not tautological): doc↔schema agreement compares the
  constant to a hard-coded doc-04 transcription; hygiene parity compares against *live*
  `hygiene_check.find_violations`; no-sidecar greps the *live* module source; sanitization smoke captures
  stdout+stderr and asserts the planted token never surfaces. ✓

Test quality is high. Minor note T1 below.

## 7. Posture review (binding bright lines)

Every forbidden line **held**: no Rung-2 admission, no "beats random-legal" verdict, no claim-ceiling advance,
no `docs/ledger.md` mutation, no Rung-2 row, no SP-6/value promotion, no numeric `M`, no OD-6 relaxation,
**no inferential statistic computed**, no new eval run, no K=50 top-up, no paired-delta tooling, no
runtime-agent work, no broad optimization, no Kaggle automation, no FunSearch surface, no cross-regime
comparison (single-regime guard, exit 2), no regime mutation, **no sidecar read** (zero `trace` tokens), no
`.claude/` edit, **no tracked evidence-value artifact** (exercise output gitignored/unstaged/uncited).
**Rung 1 held.**

## 8. Judgment on the two documented deviations

**Deviation 1 — Beads lifecycle not used → ACCEPTABLE.** The binding posture (sprint plan §0/§10, audit §8)
requires `.beads/issues.jsonl` to stay unstaged/untouched; running `br` would mutate it. Verified:
`.beads/issues.jsonl` is modified-but-**unstaged** and was already dirty at session start — consistent with
"pre-existing, untouched." `TaskCreate` was used only for session progress display, which CLAUDE.md explicitly
permits; it was **not** used as a beads substitute for lifecycle tracking. No NEVER-rule violation; nothing
material lost for the gate (the report + code + 12-check suite are the evidence). Correctly prioritizes the
explicit operator posture over the framework default.

**Deviation 2 — `hashes` from `manifest.json`, not `hashes.txt` → ACCEPTABLE.** Preserves the authorized read
surface: SDD §3.1/§8 define it as `manifest.json` + `match_results/*` (via `aggregate_run`) + the `--validate`
file; `hashes.txt` is **not** listed. `_manifest_run_hash` (`:117-133`) reads the already-loaded manifest dict
and never opens `hashes.txt`. doc 04 §2.1 explicitly sanctions `manifest.json` as a hashes source, so the
emitted shape conforms. Clearly documented (report §4/§8). See note C4 on the semantic granularity of the
chosen hash — non-blocking, forward-looking.

## 9. Adversarial Analysis

### Concerns identified

1. **C1 — Digest-shape enforcement is top-level only (positional gap). MEDIUM, non-blocking.**
   `validate_summary` enforces "`hashes` values must be SHA-256" against `obj.get("hashes")` only (`:369-377`),
   but the allow-list (`SAFE_FIELDS`) is **field-name-based, not positional** — `hashes` is an accepted key
   *anywhere*. A hostile summary nesting a `hashes` map inside an agent (e.g.
   `agents[0].hashes = {"x": "<clean-raw-token>"}`) has its value scanned only by `_scan_string`, which would
   **not** catch a clean token lacking path/inferential/forbidden-word characteristics. The enumerated classes
   are all rejected in their *canonical* positions (tested), and the generator never emits this shape, so this
   does not break any AC or posture line this cycle — but the validator's fail-closed guarantee is not airtight
   against nested smuggling. **Recommend: apply the digest-shape check to every `hashes`-keyed dict during the
   `_walk`, before the Cycle-005 promotion gate makes this validator load-bearing.**
2. **C2 — Forbidden-word negation window is evadable. LOW, non-blocking.** `_affirmative_forbidden_words`
   (`:298-306`) suppresses a flag if *any* negation token appears within 36 chars before the word — even an
   unrelated one (`"claim not made; agent strong"` would pass). Heuristic; legit generator output contains
   none of the five words. **Recommend: require immediate-precedence negation, or human-review framing strings
   at promotion.**
3. **C3 — `_refuse_tracked_out` is bypassable by absolute path. LOW, non-blocking.** The guard tests
   `parts[0] == "docs"` on a normalized-but-not-repo-resolved path (`:412-414`); an absolute path to the repo's
   `docs/` for a non-`ledger.md` file would slip the docs check (the `ledger.md` basename check still catches
   the ledger). The **primary** control — `git diff --exit-code -- docs/ledger.md` byte-unchanged — is
   unaffected and passed. **Recommend: resolve `--out` against repo root before the prefix check.**

### Assumptions challenged
- **Assumption:** a flat field-name allow-list fully captures doc 04 §2. **Risk if wrong:** positional
  smuggling (C1). **Note:** the implementation is *faithful* — doc 04 §2 genuinely is a flat field list — so
  the latent weakness is inherited from the spec's flatness, not introduced. **Recommendation:** flag for the
  audit and Cycle-005; consider a structural schema when the gate becomes load-bearing.
- **Assumption:** every manifest carries a 64-hex `*_hash` field. **Risk if wrong:** `_manifest_run_hash`
  returns `None` → `hashes` is silently `{}` (present-but-empty), which `validate_summary` accepts as clean.
  **Recommendation:** have the generator note/warn when `hashes` is empty so a missing integrity stamp isn't
  silent.

### Alternatives not considered
- **Structural (positional) validation** — validate top-down (top-level keys → `agents[]` → `metrics{}` →
  stats{}) instead of a flat-set walk. **Tradeoff:** more code, but closes C1. **Verdict:** the flat allow-list
  is justified for a build-only cycle that promotes nothing and is faithful to doc 04 §2; **reconsider at
  Cycle-005**.
- **`hashes.txt` (richer provenance) vs manifest-only.** **Tradeoff:** `hashes.txt` carries run-distinguishing
  content hashes (`regime_hash`, `deck_hash`, …); manifest-only yields an *agent-granular* stamp
  (`agent_source_hash` is identical across all runs of one agent — note **C4**). **Verdict:** manifest-only is
  the **correct** call — reading `hashes.txt` would exceed the SDD §8 read surface. The granularity limitation
  is a forward note for when a promoted summary's integrity stamp must distinguish runs (Cycle-005).

## 10. Minor notes (nits — non-blocking)
- **T1 — `--json` flag is vestigial.** Parsed but never branched on (`:500-502`); generate-mode is always JSON.
  Acceptable for CLI parity with `dispersion_report.py`, but consider removing or documenting as a no-op.
  `net: ~ -1 line possible` — otherwise lean.
- **C4 — `hashes` granularity** (see alternatives): per-run values are agent-identical; fine now, note for
  Cycle-005.
- **`\bCI\b`** (inferential rule) could false-positive on a future agent/run id containing "CI"; none present
  in current data.
- A top-level JSON **array** input maps to exit 3 (leak) rather than exit 1 (input failure) — defensible
  fail-closed direction, but a shape-not-content malformation arguably fits exit 1.
- **Complexity:** all functions within thresholds except `build_summary` (~60 logical lines) — borderline but
  justified (linear read→guard→aggregate→assemble pipeline mirroring `dispersion_report.disperse`; nesting ≤3,
  no duplication). Not blocking.

## 11. Required fixes before audit
**None blocking.** No posture line crossed; no AC failed; all gates green. Concerns C1–C4 are **carry-forward
hardening recommendations** for the Cycle-005 promotion gate (where the validator becomes load-bearing) and
should be **surfaced to `/audit-sprint sprint-01`** for the auditor's awareness — not fixed in this build-only
sprint.

## 12. Readiness
**Sprint 01 is READY for `/audit-sprint sprint-01`.** The implementation is faithful to the PRD/SDD/sprint-plan
and the Cycle-003 design authorities, well-tested (12 meaningful checks), and holds every bright line. The
documented concerns are robustness/forward notes, not defects of this cycle's scope.

---

### Reviewer's note on process
Three things I'd genuinely flag to the engineer if this weren't already solid work: the **positional smuggling
gap (C1)** is the one I'd most want addressed before any real promotion — it's the kind of thing that looks
airtight (six tested rejection classes) but has a seam where the allow-list's flatness and the shape-check's
top-level scope don't quite meet. The other carry-forwards (C2/C3) are heuristic edges. The sprint passes
because none of this is in-scope for a build-only cycle that promotes nothing — but all four notes belong in
the Cycle-005 planning input, not lost here.

---

> **Provenance.** Review run at HEAD `8ac161d`; `docs/ledger.md` byte-unchanged (`2a2f1c2…`); claim ceiling
> Rung 1; no file staged, committed, or pushed. This report contains no dispersion values and no affirmative
> forbidden agent-quality claim. Next Loa step: `/audit-sprint sprint-01`.
