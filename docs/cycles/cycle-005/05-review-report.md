# Cycle-005 Review Report — Promotion-Gate Hardening (C1–C4)

> Senior-lead review artifact (output of `/review-sprint sprint-01`). **Pure review** — no source files
> were edited; nothing staged, committed, or pushed. This report reviews the working-tree implementation of
> Cycle-005 Sprint 01 against the accepted PRD/SDD/Sprint-Plan. Findings are grounded in independent
> behavioral probes of the actual module, not the implementation report alone.
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, simulator logs, Pokémon Elements, or
> Competition Data appear here. The forbidden agent words (*strong / competitive / optimal / calibrated /
> complete*) and inferential terms appear only as the negated/forbidden language they are — quoted from
> synthetic probe fixtures the validator is built to reject or suppress.

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-005 / Sprint 01 — Promotion-Gate Hardening C1–C4 |
| **Reviewer role** | Senior tech lead (adversarial) |
| **Build-time HEAD** | `6d1efbe7e0941d9c0b43a74f73563f9ef31b4b2a` (== `origin/main`; not behind) |
| **Date** | 2026-06-19 |
| **Verdict** | **PASS WITH NOTES** (all notes non-blocking) |
| **Ready for `/audit-sprint sprint-01`?** | **Yes.** |

---

## 1. Verdict

**PASS WITH NOTES.** All eight acceptance criteria (AC-1…AC-8) are met; the hardening-only posture is held
intact (Rung 1, ledger byte-unchanged, no value promoted, Rung 2 deferred); the validator is **empirically**
strictly more conservative (fuzz-verified, §5); and the one documented deviation (C4 comment wording) is
**acceptable**. The notes in §9 are non-blocking observations and carry-forwards — none requires a fix before
audit.

---

## 2. Command results (independently run at HEAD `6d1efbe`)

| Command | Exit | Expected | Verdict |
|---|---|---|---|
| `python tests/test_evidence_summary.py` | 0 | 0 (12 existing + 13a–13l) | ✓ |
| `python tests/test_import_direction.py` | 0 | 0 | ✓ |
| `python eval/hygiene_check.py --paths analysis/evidence_summary.py tests/test_evidence_summary.py docs/cycles/cycle-005/04-implementation-report.md` | 0 | 0 | ✓ |
| `git hash-object docs/ledger.md` | `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` | `2a2f1c2…` | ✓ |
| `git diff --exit-code -- docs/ledger.md` | 0 | 0 | ✓ |
| `git diff --exit-code -- docs/claim-ceiling.md` | 0 | 0 | ✓ |
| `git status --porcelain .claude/ frozen/ runs/ agents/ sim/` | (empty) | empty | ✓ |
| `git diff --cached --name-only` | (empty) | empty | ✓ |
| `git rev-parse HEAD` | `6d1efbe…` | `6d1efbe` or descendant | ✓ |
| `git ls-remote origin main` | `6d1efbe…` | not behind | ✓ |

**Posture guards (independently confirmed):** no `*.schema.json` in the change set; no
`analysis/evidence_summary_validate.py`; `grep -c "hashes.txt"` = **0** in the module; exit codes used are
exactly `0 1 2 3` (no new code); no `--promotion-check` / `promotion_check` token; no dependency/manifest
(`requirements*.txt`, `pyproject.toml`, `setup.cfg`, `setup.py`) change.

---

## 3. Changed-files verification

```
 M .beads/issues.jsonl          (pre-existing State-Zone dirt — untouched by this sprint)
 M analysis/evidence_summary.py (authorized; C1–C4)
 M grimoires/loa/NOTES.md       (pre-existing State-Zone dirt — untouched by this sprint)
 M tests/test_evidence_summary.py (authorized; block 13)
?? docs/cycles/cycle-005/04-implementation-report.md (authorized; new)
```

Exactly the authorized set. The two dirty State-Zone files were already `M` at preflight and carry no
sprint-related change. **Source-diff scope (8 hunks, all C1–C4):** C2 header/comment, `_NEGATION_RE` swap, C2
in-function comment, C1 `_enforce_hashes_digest` helper, C1 `_walk` wiring, C3 `_refuse_tracked_out`, C4 warning
in `main`. `SAFE_FIELDS` assignment and `_manifest_run_hash` body are **unchanged**. **Test-diff scope:** the
only deletion is the summary-line `print(...)` (the SDD-authorized OD-C5-4 update); all other lines are
additions — **the 12 existing checks are byte-unchanged.**

---

## 4. Code review — C1…C4

### C1 — nested-`hashes` digest-shape enforcement — ✓ PASS
- `_enforce_hashes_digest(field_path, hashes_dict, out)` exists at `analysis/evidence_summary.py:347`,
  mirroring the `out.append((field, reason))` contract and reusing the **same** reason message as the
  top-level block.
- `_walk` calls it for **every** `hashes`-keyed dict whose value is a dict, at any depth
  (`analysis/evidence_summary.py:380-381`). Independently verified at depth ≥2: a non-digest under
  `agents[0].metrics.hashes` was flagged at path `agents[0].metrics.hashes.r` with the SHA-256 reason —
  confirming enforcement is genuinely position-independent, not just one level deep.
- Nested clean non-digest → rejected (exit 3); nested valid digest → **no** violation (not falsely flagged).
- Top-level digest block preserved at `analysis/evidence_summary.py:408-419`; flat `SAFE_FIELDS` preserved
  (count 25, `hashes` ∈ set — matches existing check 9).
- No schema rewrite, no `.schema.json`, no dependency. **Conservative-only confirmed:** adds rejections,
  removes none; an empty `hashes` dict still validates clean (no false positive on `{}`).

### C2 — forbidden-word negation hardening — ✓ PASS (close-attention area)
- `_NEGATION_RE` is now end-anchored immediate-precedence:
  `(?:\b(?:no|not|never|non|without|neither|nor)\b|n't)[\s\W]*\Z` (`analysis/evidence_summary.py:271-272`);
  the token set is preserved. `_NEG_WINDOW = 36` is repurposed as the look-behind bound in
  `_affirmative_forbidden_words` (`analysis/evidence_summary.py:307`).
- **Required examples — independently driven through `_affirmative_forbidden_words`:**

  | Input | Result | Expected | Verdict |
  |---|---|---|---|
  | `"claim not made; agent strong"` | `['strong']` → rejected (exit 3) | reject | ✓ |
  | `"never strong"` | `[]` → clean | validate | ✓ |
  | `"NO strength claim"` | `[]` → clean | validate | ✓ (no `strong` token present; correct) |
  | `"agent is strong"` | `['strong']` → rejected (exit 3) | reject | ✓ |

- **Broad-window loophole probe — the key question.** The repurposed `_NEG_WINDOW` does **not** preserve a
  loophole: because the look-behind is bounded by the same window and the regex is end-anchored, a suppression
  under the new rule is necessarily a suppression under the Cycle-004 window. Adversarial cases confirm:
  `"not really, but the agent is strong"` → rejected; `"without question strong"` (content word between) →
  rejected; `"no, the deck is optimal"` → rejected. Immediate negation still suppresses across whitespace and
  punctuation (`"not strong"`, `"not  strong"`, `"not-strong"` → clean).
- **Conservative-only — fuzz-verified.** Ran 20,000 randomized strings over a token alphabet of negations,
  forbidden words, content words, and punctuation, comparing the new rule against a faithful re-implementation
  of the Cycle-004 broad-window rule. **Loosening cases (new drops a flag the old rule raised): 0.** The new
  suppression set is empirically a strict subset of the old → the validator flags a superset → strictly more
  conservative. **No input previously rejected now passes.**

### C3 — repo-root-resolved `--out` guard — ✓ PASS
- `_refuse_tracked_out` repo-root-resolves first (`analysis/evidence_summary.py:459`):
  `resolved == docs_root or docs_root in resolved.parents` raises; the original relative-`docs/` prefix check
  and the `ledger.md` basename guard are preserved **verbatim** below it.
- Independently verified: absolute repo `docs/` → refused; relative `docs/x.json` → refused; `a/b/ledger.md`
  basename → refused on any path; absolute repo `docs/ledger.md` → refused. **Adversarial bonus:** a
  `..`-traversal path (`sub/../docs/x.json`) now **also** refuses — `Path.resolve()` collapses the traversal
  into the repo `docs/` tree. A safe local temp path and a safe relative local path are both **allowed** (no
  raise). `docs/ledger.md` is byte-unchanged. **Conservative-only:** strictly more paths refused; none newly
  allowed.

### C4 — empty-`hashes` warning — ✓ PASS
- Manifest-only sourcing preserved (`_manifest_run_hash` body unchanged); **no** unauthorized hash-source file
  read (token absent from module).
- Generate mode emits the stderr `WARNING` on empty `hashes` (`analysis/evidence_summary.py:552`); message:
  `evidence_summary: WARNING — empty hashes (no manifest integrity stamp found); provenance is un-stamped and a
  future promotion gate must reject this.` — mentions both "empty hashes" and the missing integrity stamp.
- Independently verified: empty-`hashes` generate → exit **0**; **stdout is pure JSON** (parses; no `WARNING`
  leak — the JSON-first contract holds); non-empty generate → **no** warning, exit 0; `--validate` on a
  structurally-valid empty-`hashes` summary → exit **0**. No new exit code (an absolute-docs `--out` rides the
  existing exit-1 input-failure path). No `--promotion-check` mode.

---

## 5. Test review — block 13 (13a–13l) + the preserved 12

- **All 12 existing checks preserved unmodified** (diff confirms the only deletion is the summary line).
- New block `# --- 13. C1–C4 hardening ---` present (`tests/test_evidence_summary.py:256`); checks **13a–13l**
  all present, green, and meaningful:

  | Check | Asserts | Verdict |
  |---|---|---|
  | 13a | nested non-digest under `hashes` → violation at nested path, exit 3 | ✓ behavioral |
  | 13b | nested valid digest → validates clean (no false digest flag) | ✓ behavioral |
  | 13c | top-level non-digest still flagged + exit 3 | ✓ behavioral |
  | 13d | unrelated negation no longer suppresses `strong` → exit 3 | ✓ behavioral |
  | 13e | immediate negation still suppresses (legit example clean) | ✓ behavioral |
  | 13f | affirmative `strong` still flagged → exit 3 | ✓ behavioral |
  | 13g | absolute repo-docs path refused | ✓ behavioral |
  | 13h | relative `docs/` + `ledger.md` basename still refused | ✓ behavioral |
  | 13i | safe local path allowed | ✓ behavioral |
  | 13j | empty hashes warns on stderr, exit 0, ledger byte-unchanged | ✓ behavioral |
  | 13k | non-empty hashes → no warning, exit 0 | ✓ behavioral |
  | 13l | `"hashes.txt"` absent from module source | ✓ structural (read-surface) |

- Fixtures are **stdlib-only synthetic** (`make_run_dir`, `validate_file_exit`, `good`, `_HEX64`); the empty-
  hashes fixture reuses `make_run_dir(..., manifest_hash="")` — no local K-batch dependency, no raw data.
- **No tautological tests.** 13a–13k assert *behavior* (validator verdicts / exit codes / warning emission /
  ledger bytes). 13l is a *structural read-surface guarantee* (literal-string absence), directly parallel to
  the pre-existing check 4 (`"traces"`/`"trace"` absence) — a legitimate property test, not a tautology.

---

## 6. Posture review (hardening-only bright lines)

| Bright line | Status |
|---|---|
| Rung 1 held; no Rung-2 attempt/admission/verdict | ✓ held (no admission logic; validator only *rejects* inferential terms) |
| `docs/ledger.md` byte-unchanged (`2a2f1c2…`); no Rung-2 row | ✓ hash matches; diff clean |
| `docs/claim-ceiling.md` untouched | ✓ diff clean |
| No `M` / SP-6 / OD-6 relaxation | ✓ none present |
| No new eval / K=50 / runtime-agent / gameplay / FunSearch / Daily-Top-Episode work | ✓ none; tests are synthetic |
| No `--promotion-check` mode; no new exit code | ✓ exit set is `0/1/2/3` |
| No `.schema.json`; no second validator module; no dependency | ✓ confirmed |
| No `.claude/` edit; no State-Zone cleanup | ✓ protected paths clean; dirty State-Zone files untouched |
| No raw Competition Data / Pokémon Elements / traces / card/deck/sim logs | ✓ hygiene exit 0; synthetic fixtures only |
| No value promoted | ✓ summary carries no ceiling of its own (check 7 green) |

The implementation report contains all required sections and the **OD-C5-6 binding language verbatim** (C1–C4
"fixed/defined and tested as hardening, not admission"; "Rung 2 remains deferred"; "No value was promoted"; "No
`M`, SP-6, ledger row, or claim-ceiling advance"). The `## AC Verification` section walks all 8 ACs, each
`✓ Met` with file:line evidence; no AC is `✗ Not met` or `⚠ Partial`.

---

## 7. Explicit judgment — the C4 comment/token deviation

**Acceptable.** The C4 in-code comment was worded to avoid the literal token for the unauthorized hash-list
file because check 13l enforces literal-string absence over the module. Independently confirmed:
- **Behavior unchanged** — the empty-`hashes` warning fires correctly, exit 0 preserved, JSON-first stdout
  intact, `--validate` still accepts empty hashes; `_manifest_run_hash` body byte-unchanged.
- **Read-surface guarantee preserved** — `grep -c "hashes.txt" analysis/evidence_summary.py` = 0; no new read
  source was introduced.
- **Test remains meaningful** — 13l still pins the read-surface property (and is consistent with the existing
  check-4 absence-grep pattern).

This is the expected likely outcome: a documentation-wording nicety with zero behavioral or guarantee impact.

---

## 8. Required fixes

**None.** No blocking issues. No CHANGES_REQUIRED conditions triggered (AC Verification present and complete;
no AC Not-met/Partial; evidence is file:line-specific).

---

## 9. Adversarial Analysis

### Concerns identified (non-blocking)
1. **Top-level `hashes` is now validated twice.** With C1 traversal enforcement covering the top-level
   `hashes` *and* the preserved top-level block (`analysis/evidence_summary.py:380-381` + `:408-419`), a
   top-level non-digest produces **two** identical violation entries (verified: `count=2`). Harmless — both
   carry the correct reason, exit 3 is unaffected, and no test asserts an exact violation count — but
   `_run_validate` prints `len(violations)`, so the human-facing leak count for a *top-level* digest violation
   is inflated by 1. Cosmetic only; the SDD explicitly sanctioned the top-level block as "redundant-but-harmless."
2. **C3 `.resolve()` is CWD-relative for relative `--out` paths** (`analysis/evidence_summary.py:459`). The
   dual design mitigates this — the preserved string-prefix guard catches relative `docs/...` CWD-independently,
   and `REPO_ROOT` is derived from `__file__`, not CWD — so the absolute-docs coverage is stable. The residual
   assumption (the cycle runs from repo root) is acknowledged in SDD R8 and is satisfied by all tests.
3. **C2 keys on "no intervening *word*", not "no intervening character."** `[\s\W]*` permits arbitrary
   whitespace/punctuation between the negation and the forbidden word (`analysis/evidence_summary.py:271-272`),
   so `"not!!! strong"` suppresses. This is intentional and conservative-only-safe (still a strict subset of the
   old window, fuzz-confirmed), but a future maintainer should understand the rule is word-adjacency, not
   character-adjacency.

### Assumption challenged
- **Assumption:** the validator/generator runs from the repo root (C3 resolved-tree check + tests 13g/13i).
  **Risk if wrong:** a relative `--out docs/x.json` from a foreign CWD — still caught by the CWD-independent
  string-prefix guard, so the practical risk is nil; only the *absolute-docs* arm depends on `REPO_ROOT`, which
  is `__file__`-derived (stable). **Recommendation:** none required; the dual-guard design already neutralizes
  the assumption. Worth a one-line note for future maintainers.

### Alternative not considered
- **Alternative:** remove the now-redundant top-level digest block once `_walk` traversal covers it (would
  eliminate concern #1's double-report). **Tradeoff:** it would violate the SDD's explicit "preserve the
  top-level digest block for back-compat parity" directive and risk a regression for any consumer keyed on the
  exact top-level path/message. **Verdict:** the implemented approach (preserve + add) is correct and
  SDD-mandated; the duplicate is harmless. Keeping the block is the safer, conservative choice — do **not**
  change it in this hardening-only sprint.

---

## 10. Carry-forward recommendations (none blocking)

- **CF-1 (Cycle-006+ / audit to confirm deferred):** OD-C5-2 floor — a future promotion gate (e.g.
  `--promotion-check`) MUST treat empty `hashes` as a **hard failure**, not a warning. C4 correctly only
  *warns* this cycle; the audit should confirm this floor remains explicitly deferred (it is, in the SDD §16
  and the implementation report §9), not silently dropped.
- **CF-2 (optional, future):** if the `_run_validate` printed violation count is ever consumed
  programmatically, consider de-duplicating the top-level `hashes` double-report (concern #1). Not needed for
  any current consumer.
- **CF-3 (doc nicety):** record the C2 "word-adjacency, not character-adjacency" semantics (concern #3) in a
  future maintainer note if the negation rule is revisited.

---

## 11. Audit readiness

**Sprint 01 is ready for `/audit-sprint sprint-01`.** All acceptance criteria met; hardening-only posture
held; ledger and claim-ceiling untouched; conservative-only empirically verified; the documented deviation is
acceptable; no required fixes. The three carry-forwards are non-blocking and are explicitly future-scoped.

> **Sources:** `docs/cycles/cycle-005/01-prd.md`, `02-sdd.md`, `03-sprint-plan.md`,
> `04-implementation-report.md`; `analysis/evidence_summary.py` + `tests/test_evidence_summary.py`
> (build-time HEAD `6d1efbe`); `docs/claim-ceiling.md` (Rung 1); `docs/ledger.md` (hash `2a2f1c2…`).
> Findings grounded in independent behavioral probes of the actual module. This review edited no source files,
> mutated no ledger, advanced no ceiling, promoted no value, and edited no `.claude/`.
