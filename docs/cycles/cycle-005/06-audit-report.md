# Cycle-005 Audit Report — Promotion-Gate Hardening (C1–C4)

> Security/quality audit artifact (output of `/audit-sprint sprint-01`) — the final gate before operator
> acceptance. **Pure audit** — no source files were edited; nothing staged, committed, or pushed. Findings are
> grounded in **independent** behavioral verification of the actual module through the real CLI exit-code path,
> plus a direct Cycle-004-vs-Cycle-005 comparison — not trust in the implementation or review reports.
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, simulator logs, `deck.csv` rows, Pokémon
> Elements, Daily-Top-Episode data, or Competition Data appear here. The forbidden agent words
> (*strong / competitive / optimal / calibrated / complete*) and inferential terms appear only as the
> negated/forbidden language they are — quoted from synthetic probe fixtures the validator is built to reject
> or suppress. No dispersion metric values appear here.

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-005 / Sprint 01 — Promotion-Gate Hardening C1–C4 |
| **Auditor role** | Paranoid cypherpunk security/quality auditor (final gate) |
| **Build-time HEAD** | `6d1efbe7e0941d9c0b43a74f73563f9ef31b4b2a` (== `origin/main`; not behind) |
| **Date** | 2026-06-19 |
| **Upstream review** | `docs/cycles/cycle-005/05-review-report.md` — PASS WITH NOTES |
| **Verdict** | **PASS WITH NOTES — ACCEPTED** (all notes non-blocking, future-scoped) |
| **Ready for operator commit/push?** | **Yes.** |

---

## 1. Verdict

**PASS WITH NOTES — ACCEPTED.** All eight acceptance criteria (AC-1…AC-8) are independently confirmed met; the
hardening-only posture is held intact (Rung 1, ledger byte-unchanged, claim-ceiling unchanged, no value
promoted, Rung 2 deferred); the validator is verified **strictly more conservative** than Cycle-004 (every
"loosening" candidate the audit constructed was already suppressed by Cycle-004 or is now *more* strictly
flagged); and the documented C4 comment/token deviation is **acceptable**. **No required fixes.** The three
senior-review carry-forwards (CF-1/CF-2/CF-3) are independently confirmed **non-blocking** and properly
deferred. Sprint 01 is **accepted** and ready for operator commit/push.

---

## 2. Command results (independently run at HEAD `6d1efbe`)

| Command | Exit | Expected | Verdict |
|---|---|---|---|
| `python tests/test_evidence_summary.py` | 0 | 0 | ✓ |
| `python tests/test_import_direction.py` | 0 | 0 | ✓ |
| `python eval/hygiene_check.py --paths analysis/evidence_summary.py tests/test_evidence_summary.py docs/cycles/cycle-005/04-implementation-report.md docs/cycles/cycle-005/05-review-report.md` | 0 | 0 | ✓ |
| `git hash-object docs/ledger.md` | `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` | `2a2f1c2…` | ✓ |
| `git diff --exit-code -- docs/ledger.md` | 0 | 0 | ✓ |
| `git diff --exit-code -- docs/claim-ceiling.md` | 0 | 0 | ✓ |
| `git status --porcelain .claude/ frozen/ runs/ agents/ sim/` | (empty) | empty | ✓ |
| `git diff --cached --name-only` | (empty) | empty | ✓ |
| `git rev-parse HEAD` | `6d1efbe…` | `6d1efbe` or descendant | ✓ |
| `git ls-remote origin main` | `6d1efbe…` | not behind | ✓ |

**Posture guards (independently confirmed):** `grep -c "hashes.txt"` = **0** in the module; no `*.schema.json`
in the change set; no `analysis/evidence_summary_validate.py`; exit codes used are exactly `0 1 2 3` (no new
code); no `--promotion-check` / `promotion_check` token; no dependency/manifest change
(`requirements*.txt` / `pyproject.toml` / `setup.cfg` / `setup.py` / `Pipfile` / `poetry.lock`). **Imports** in
`analysis/evidence_summary.py` are stdlib (`argparse, json, re, sys, pathlib`) + intra-zone `analysis`
(`aggregate, dispersion_report`) only — **no `cg` / `sim` / `agents` / `eval`** import (offline/runtime
separation intact; `test_import_direction` green).

---

## 3. Changed-files verification

```
 M .beads/issues.jsonl          (pre-existing State-Zone dirt — untouched)
 M analysis/evidence_summary.py (authorized; C1–C4)
 M grimoires/loa/NOTES.md       (pre-existing State-Zone dirt — untouched)
 M tests/test_evidence_summary.py (authorized; block 13)
?? docs/cycles/cycle-005/04-implementation-report.md (authorized)
?? docs/cycles/cycle-005/05-review-report.md          (authorized)
```

Exactly the authorized set plus the two pre-existing dirty State-Zone files (already `M` at preflight; no
sprint-related change). **Review/audit did not edit source** — `analysis/evidence_summary.py` +
`tests/test_evidence_summary.py` show the identical implementation diffstat (`182 insertions(+), 4
deletions(-)`) before and after both review and audit. The 06-audit-report is the only new artifact this step.

---

## 4. Security / code audit — C1…C4 (independently verified via the real CLI exit path)

### C1 — nested-`hashes` digest-shape enforcement — ✓ PASS
`_enforce_hashes_digest` exists (`analysis/evidence_summary.py:347`) and is invoked from `_walk` for every
`hashes`-keyed dict at any depth (`:380-381`). Independently driven through `main(["--validate", …])`:

| Probe | Exit | Expected | Verdict |
|---|---|---|---|
| nested `agents[0].hashes = {"r":"clean-non-digest"}` | 3 | 3 | ✓ |
| **deeper** `agents[0].metrics.hashes = {"r":"clean-non-digest"}` | 3 | 3 | ✓ (depth-independent) |
| nested `agents[0].hashes = {"r": <64-hex>}` | 0 (0 false-digest flags) | 0 | ✓ |
| top-level `hashes = {"r":"clean-non-digest"}` | 3 | 3 | ✓ |

Top-level digest block preserved (`:408-419`); flat `SAFE_FIELDS` preserved (size **25**, `hashes` ∈ set —
matches existing check 9). No schema rewrite, no `.schema.json`, no dependency. **Conservative-only:** adds
rejections, removes none; an empty `hashes` dict still validates clean.

### C2 — forbidden-word negation hardening — ✓ PASS (audited closely; loophole closed)
`_NEGATION_RE` is end-anchored immediate-precedence
(`(?:\b(?:no|not|never|non|without|neither|nor)\b|n't)[\s\W]*\Z`, `:271-272`); `_NEG_WINDOW=36` is the
look-behind bound (`:307`). The audit drove each required probe through the **CLI `--validate` exit path** and,
critically, compared against a faithful re-implementation of the **Cycle-004 broad-window rule**:

| Probe | New (CLI) | Cycle-004 verdict | Verdict |
|---|---|---|---|
| `"claim not made; agent strong"` | **exit 3 (reject)** | *suppressed* (loophole) | ✓ now stricter |
| `"agent is strong"` | exit 3 (reject) | flagged | ✓ parity |
| `"never strong"` | exit 0 (clean) | clean | ✓ |
| `"not strong"` | exit 0 (clean) | clean | ✓ |
| `"not really, but the agent is strong"` | **exit 3 (reject)** | *suppressed* (loophole) | ✓ now stricter |
| `"without question strong"` | **exit 3 (reject)** | *suppressed* (loophole) | ✓ now stricter |
| `"not-strong"` | exit 0 (clean) | *suppressed* | ✓ unchanged (no loosening) |

**The broad-window loophole is closed.** Every probe where the new rule rejects but Cycle-004 suppressed is
exactly an unrelated/non-immediate negation the old window wrongly cleared — the new rule correctly flags it
(stricter). **No input previously rejected now passes:** the senior review's 20,000-string fuzz found **zero**
loosening cases, and this audit's per-probe Cycle-004 comparison corroborates it. The `_NEG_WINDOW`
repurposing does **not** preserve the old broad window in practice — because the bound caps the look-behind and
the regex is end-anchored, any new suppression was necessarily a Cycle-004 suppression (strict subset).

### C3 — repo-root-resolved `--out` guard — ✓ PASS
`_refuse_tracked_out` repo-root-resolves first (`:459`), preserving the relative-`docs/` prefix check and the
`ledger.md` basename guard verbatim below. Independently verified (corrected helper; True = refused):

| Probe | Refused | Expected |
|---|---|---|
| absolute repo `docs/x.json` | True | True |
| absolute repo `docs/ledger.md` | True | True |
| relative `docs/x.json` | True | True |
| relative `a/b/ledger.md` (basename) | True | True |
| **traversal** `sub/../docs/x.json` | True | True (collapses into repo `docs/`) |
| safe local temp path | False (allowed) | False |
| safe relative `local/out.json` | False (allowed) | False |

`docs/ledger.md` byte-unchanged (`git diff --exit-code` clean; hash `2a2f1c2…`). **Conservative-only:** strictly
more paths refused; none newly allowed.

### C4 — empty-`hashes` warning — ✓ PASS
`_manifest_run_hash` body unchanged (read-surface intent preserved); no unauthorized hash-source token in the
module; no new source read. Independently verified:

| Probe | Result | Expected |
|---|---|---|
| empty-`hashes` generate | exit **0**; stderr `WARNING` mentioning "empty hashes" + "no manifest integrity stamp"; **stdout pure JSON, no WARNING leak**; assembled `hashes == {}` | warn, exit 0, JSON-first |
| `--validate` empty-`hashes` summary | exit **0** | exit 0 |
| non-empty-`hashes` generate | exit **0**, **no** warning | exit 0, no warn |
| `--out` absolute repo `docs/` | exit **1** (existing input-failure path) | no new exit code |

No new exit code; no `--promotion-check` mode.

---

## 5. Test audit — block 13 (13a–13l) + preserved 12

- **All 12 existing checks preserved** — 27 `check()` calls across blocks 1–12 (unchanged); the only test-file
  deletion is the summary-line `print(...)` (SDD-authorized OD-C5-4 update).
- **Block 13 present** (`# --- 13. C1–C4 hardening ---`, `tests/test_evidence_summary.py:256`) with **21
  `check()` calls** spanning 13a–13l; every label 13a…13l confirmed present and behavioral (validator verdicts,
  CLI exit codes, warning emission, ledger-byte invariance).
- Fixtures are **stdlib-only synthetic** (`make_run_dir`, `validate_file_exit`, `good`, `_HEX64`; empty-hashes
  via `make_run_dir(..., manifest_hash="")`) — **no local K-batch dependency, no raw data.**
- **No tautological tests.** 13a–13k assert behavior. 13l is a structural read-surface guarantee
  (`"hashes.txt"` literal absence) — **acceptable**, directly parallel to the pre-existing check 4
  (`"traces"`/`"trace"` absence); it pins the read surface, not implementation prose.

---

## 6. Report audit

- **Implementation report** (`04-…`) — contains all required sections (preflight, anchor revalidation, files
  changed, C1–C4 summaries + conservative-only proofs, C4 warning/exit behaviour, 13a–13l test summary, 12
  green, exact commands + exit statuses, ledger/ceiling/protected-path proofs, no-raw-data / no-value-promotion
  / Rung-2-deferred proofs, final porcelain, deviations) and the **OD-C5-6 binding language verbatim**; the
  `## AC Verification` section walks all 8 ACs, each `✓ Met` with file:line evidence, none Not-met/Partial.
- **Review report** (`05-…`) — verdict **PASS WITH NOTES** with no blocking findings; review **did not edit
  source** (confirmed via diffstat).
- **No raw data / evidence values in report bodies** (hygiene is path-only, so the audit scanned content
  independently): the sole Competition-Data-token hit is the boilerplate **sanitized-note negative
  declaration** ("…`deck.csv` rows … or Competition Data appear here" preceded by "No raw…"); no run-tree or
  `grimoires/loa/context/` path; no dispersion values. Forbidden agent words appear **only** in the
  sanitized-note meta-declaration and quoted rejected/negated test fixtures — no affirmative quality claim.
- Both reports state **C1–C4 closed as hardening, not admission; Rung 2 remains deferred; no value promoted;
  no `M`, SP-6, ledger row, or claim-ceiling advance.**

---

## 7. Independent judgment — carry-forwards CF-1, CF-2, CF-3

- **CF-1 (future promotion gate must hard-fail empty `hashes`) — confirmed deferred and recorded; NO fix
  needed now.** The OD-C5-2 floor is explicitly documented in SDD §16 and implementation report §9. Cycle-005
  implements **no** promotion mode and promotes **no** value, so warning-only is the correct (and strictest
  non-breaking) Cycle-005 behaviour. Audit independently confirmed: empty `hashes` warns (visible, not silent)
  and `--validate` still accepts a structurally-valid empty `hashes`. **Non-blocking; carry to Cycle-006+.**
- **CF-2 (top-level double-report) — confirmed non-blocking.** Audit reproduced it: a top-level non-digest
  yields `violation_count == 2` (preserved top-level block + new traversal both catch it), but **the CLI exit
  code is still 3** — no exit-behaviour or safety impact, and no test asserts an exact count. The SDD
  explicitly preserved the top-level block ("redundant-but-harmless"). The only residual effect is that
  `_run_validate`'s human-facing `len(violations)` over-counts a *top-level* digest leak by 1 — cosmetic.
  **Non-blocking; optional future dedupe.**
- **CF-3 (C2 word-adjacency, not character-adjacency) — confirmed consistent with SDD intent and NOT a
  loosening.** SDD §4.2 specifies "allowing intervening whitespace/punctuation but no intervening content
  word", so `"not-strong"` suppressing is by design. Audit verified the exact string `"not-strong"` was
  **already suppressed under Cycle-004** (the old window also matched `"not"` before `"strong"`), so the new
  behaviour is identical for this case — **no loosening.** **Non-blocking; future maintainer doc note only.**

---

## 8. Independent judgment — C4 comment/token deviation

**Acceptable.** The C4 in-code comment was worded to avoid the literal hash-list-file token because check 13l
enforces literal-string absence over the module. Audit independently confirmed: (a) **behaviour unchanged** —
empty-`hashes` warning fires, exit 0 preserved, stdout JSON-first intact, `--validate` accepts empty hashes,
`_manifest_run_hash` body byte-unchanged; (b) **read-surface guarantee preserved** — `grep -c "hashes.txt"` =
0; no new read source; (c) **test 13l remains meaningful** (structural read-surface guard, consistent with
check 4). Zero behavioural or guarantee impact — a documentation-wording nicety.

---

## 9. Posture audit (hardening-only bright lines — all held)

| Bright line | Status |
|---|---|
| Rung 1 held; no Rung-2 attempt / admission / verdict / row | ✓ no admission logic; validator only *rejects* inferential terms; `validate_summary` emits no forbidden/inferential output |
| `docs/ledger.md` byte-unchanged (`2a2f1c2…`) | ✓ hash matches; diff clean |
| `docs/claim-ceiling.md` unchanged | ✓ diff clean |
| No `M` / SP-6 / OD-6 relaxation | ✓ none present |
| No new eval / K=50 / runtime-agent / gameplay / FunSearch / Daily-Top-Episode work | ✓ synthetic fixtures only |
| No `--promotion-check`; no new exit code | ✓ exit set `0/1/2/3`; no promotion token |
| No `.schema.json` / second module / dependency | ✓ confirmed |
| No `.claude/` edit; no State-Zone cleanup | ✓ protected paths clean; dirty State-Zone files untouched |
| No raw Competition Data / Pokémon Elements / traces / card/deck/sim logs | ✓ hygiene exit 0; content-scanned reports clean |
| No value promoted; no improvement claim | ✓ summary carries no ceiling of its own (check 7 green); reports frame as hardening only |

---

## 10. Required fixes

**None.** No CRITICAL/HIGH/MEDIUM/LOW security or quality finding. No blocking issue. No posture violation.

---

## 11. Carry-forward recommendations (all non-blocking, future-scoped)

- **CF-1 → Cycle-006+:** a future promotion gate MUST treat empty `hashes` as a hard failure (OD-C5-2 floor;
  already recorded). The audit should re-verify this at the Rung-2 attempt.
- **CF-2 → optional:** if `_run_validate`'s printed violation count is ever consumed programmatically,
  de-duplicate the top-level `hashes` double-report. Not needed for any current consumer.
- **CF-3 → doc nicety:** record the C2 "word-adjacency, not character-adjacency" semantics if the negation rule
  is revisited.

---

## 12. Acceptance

**Cycle-005 Sprint 01 is ACCEPTED.** All acceptance criteria met; hardening-only posture held; the validator is
verified strictly more conservative than Cycle-004; ledger and claim-ceiling byte-unchanged; no value promoted;
Rung 2 remains deferred; the documented deviation is acceptable; no required fixes. **Sprint 01 is ready for
operator commit/push.** Per the binding posture (no State-Zone cleanup; authorized artifact is this audit
report only), no separate `COMPLETED` marker is written — acceptance is recorded here, and commit/push is the
operator's explicit action.

> **Sources:** `docs/cycles/cycle-005/01-prd.md`, `02-sdd.md`, `03-sprint-plan.md`, `04-implementation-report.md`,
> `05-review-report.md`; `analysis/evidence_summary.py` + `tests/test_evidence_summary.py` (build-time HEAD
> `6d1efbe`); `docs/claim-ceiling.md` (Rung 1); `docs/ledger.md` (hash `2a2f1c2…`);
> `docs/cycles/cycle-004/06-audit-report.md` (C1–C4 origin). Findings grounded in independent behavioral probes
> through the real CLI exit path and a Cycle-004 comparison. This audit edited no source files, mutated no
> ledger, advanced no ceiling, promoted no value, and edited no `.claude/`.
