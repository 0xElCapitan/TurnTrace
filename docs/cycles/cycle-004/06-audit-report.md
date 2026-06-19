# Cycle-004 Sprint 01 — Security & Quality Audit Report

> Audit artifact (`/audit-sprint sprint-01`), authored by the Paranoid Cypherpunk Auditor — **final gate**.
> Findings are **independently reproduced**, not inherited from the review. `auditing-security` runs
> write-disabled (C-PROC-001 / skill-invariants); persisted at operator request after the pure-audit pass.
> Nothing was staged, committed, or pushed by the audit or this persistence step.
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, or Competition Data appear here. **No dispersion value
> from the local exercise output was read, printed, cited, or tracked.** Forbidden agent words and inferential
> terms appear only as the negated/forbidden language they are (e.g. validator-rejection examples). **Rung 1 held.**

| Field | Value |
|---|---|
| Cycle / Sprint | Cycle-004 · Sprint 01 (`C4-S01`) |
| Gate | `/audit-sprint sprint-01` (`auditing-security`, pure-audit / write-disabled) |
| Build-time HEAD | `8ac161d` — *docs: plan TurnTrace Cycle-004* |
| Prior gate | `/review-sprint` → PASS WITH NOTES |
| **Verdict** | **PASS WITH NOTES — Sprint 01 ACCEPTED; ready for operator commit/push** |

---

## Verdict: PASS WITH NOTES — ACCEPTED

No binding bright line was crossed; **no posture violation occurred**; every Sprint 01 acceptance criterion is
met; all gates are green. The four review concerns (C1–C4) were independently reproduced and adjudicated:
**all four are non-blocking for this build-only cycle** and are recorded here as **mandatory carry-forwards to
the Cycle-005 promotion gate**. This audit report, once persisted, is the tracked carry-forward record.

## 1. Command results (independently re-run)

| Command | Exit |
|---|---|
| `python tests/test_evidence_summary.py` | **0** (12 checks) |
| `python tests/test_import_direction.py` | **0** |
| `python eval/hygiene_check.py --paths analysis/evidence_summary.py tests/test_evidence_summary.py docs/cycles/cycle-004/04-implementation-report.md docs/cycles/cycle-004/05-review-report.md` | **0** |
| `git hash-object docs/ledger.md` | `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` |
| `git diff --exit-code -- docs/ledger.md` | **0** |
| `git status --porcelain .claude/ frozen/ runs/ agents/ sim/` | empty |
| `git diff --name-only` | `.beads/issues.jsonl`, `grimoires/loa/NOTES.md` (State-Zone, unstaged) |
| `git diff --cached --name-only` | empty (nothing staged) |
| `git check-ignore -v …evidence-summary-local.json` | `.gitignore:17` (ignored) |
| `git status --porcelain …evidence-summary-local.json` | empty (untracked/unstaged) |

Independent exit-code reachability (synthetic fixtures, in-process): generate→**0**, validate-clean→**0**,
missing-file→**1**, no-run-dirs→**1**, mixed-regime→**2**, leak→**3**. All four codes reachable as specified.

## 2. Authorized-files verification

| Path | Status | Authorized? |
|---|---|---|
| `analysis/evidence_summary.py` | `??` untracked/unstaged | ✓ (C4-FR-1/2/3) |
| `tests/test_evidence_summary.py` | `??` untracked/unstaged | ✓ (C4-FR-4) |
| `docs/cycles/cycle-004/04-implementation-report.md` | `??` untracked/unstaged | ✓ (cycle report) |
| `docs/cycles/cycle-004/05-review-report.md` | `??` untracked/unstaged | ✓ (review artifact) |
| `.beads/issues.jsonl`, `grimoires/loa/NOTES.md` | ` M` modified, **unstaged** | pre-existing State-Zone; **not** part of this sprint; must stay unstaged |

HEAD `8ac161d` (== baseline, == `origin/main`); `git merge-base --is-ancestor 8ac161d HEAD` → YES. No staged files.

## 3. Forbidden-path / forbidden-pattern verification (independent greps on module source)

| Probe | Count | Verdict |
|---|---|---|
| sidecar token (`trace`/`traces`) | 0 | ✓ no sidecar reference |
| `hashes.txt` read | 0 | ✓ confirms Deviation 2 (manifest-only) |
| `eval` import / `hygiene_check` import | 0 | ✓ no eval/ import (parity is a local copy) |
| `run_eval` / `run_match` / `aggregate_and_ledger` | 0 | ✓ no eval invocation, no ledger write path |
| third-party (`jsonschema`/`pydantic`/`numpy`/`pandas`/`requests`/`yaml`) | 0 | ✓ stdlib-only |
| `*.schema.json` / `evidence_summary_validate.py` on disk | none | ✓ no schema file, no second module |

**AST top-level imports** (independently computed): `['__future__', 'aggregate', 'argparse', 'dispersion_report', 'json', 'pathlib', 're', 'sys']` —
stdlib + intra-zone `analysis` siblings only. No `eval`/`cabt`/`sim`/`runtime`/third-party. ✓

## 4. Code audit findings (`analysis/evidence_summary.py`)

| Check | Verdict | Evidence |
|---|---|---|
| No sidecar reference | ✓ | grep `trace` = 0 |
| No eval invocation / no run-dir creation | ✓ | grep = 0; `build_summary` reads only; only `mkdir` is `--out` parent |
| No writes to `docs/` / no ledger mutation | ✓ | `_refuse_tracked_out` guard; ledger byte-unchanged (verified) |
| No `*.schema.json` / no `_validate.py` / no third-party dep | ✓ | absent (greps + `ls`) |
| No `eval/` import; stdlib + intra-zone only | ✓ | AST imports above |
| Generator read surface = `manifest.json` + `match_results/*` via `aggregate_run` | ✓ | re-read `build_summary` (`:146-167`): manifests first, then `aggregate.aggregate_run` (`:167`), manifest-vs-record cross-check (`:168-171`) |
| Generator never emits nested `hashes` (relevant to C1) | ✓ | `build_summary` return (`:205-214`) emits `hashes` top-level only; agents = {agent_id, agent_version, K, run_ids, metrics} (`:192-201`) — **no nested hashes** |
| Validator independent; `--validate` re-reads from disk | ✓ | `json.loads(p.read_text())` (`:428`) |
| Exit codes 0/1/2/3 | ✓ | all four reproduced (independent) |
| `SAFE_FIELDS` in-module, agrees with doc 04 §2 | ✓ | independently dumped: 25 fields = 10 identity/provenance + 7 stats + 6 metrics + 2 §4.1 containers (`agents`, `metrics`) |
| Validator rejects required forbidden classes | ✓ (canonical positions; see C1) | leak→exit 3 reproduced; T5 check 2 covers all 6 sub-cases |
| Benign `hypothesis` accepted / inferential `hypothesis-test` rejected | ✓ | independently reproduced: benign → `[]`; `hypothesis-test` → rejected |
| No inferential statistic computed | ✓ | reuses `descriptive_stats`; adds none |

**Security lens.** No hardcoded secrets (the only digest-shaped strings are SHA-256 integrity stamps —
non-sensitive). No injection surface: `json.loads` + arithmetic only; no `subprocess`/`eval`/`os.system` in the
module; no network. Input validation is the validator's purpose and is fail-closed (exit 3 on leak, never 0).
Info-disclosure: the sanitization smoke (T5 check 11) confirms a planted token is not surfaced to
stdout/stderr; exceptions map to exit codes without leaking stack traces to stdout. Read surface is
operator-pointed local files (offline tool) — no untrusted-input path. Acceptable.

## 5. Test audit findings (`tests/test_evidence_summary.py`)

| Check | Verdict |
|---|---|
| stdlib-only plain-Python; `main()`→0/1 | ✓ (imports: contextlib, copy, io, json, sys, tempfile, pathlib + intra-repo) |
| Synthetic temp-dir fixtures only | ✓ (`make_run_dir` + `tempfile.TemporaryDirectory`) |
| No dependency on gitignored K-batch runs | ✓ (only `runs/…` reference is a **string-literal probe** at `:151`, not a read) |
| No raw Competition Data / Pokémon Elements / sidecar content in fixtures | ✓ (generic synthetic fields; comment `:45-47` affirms; poisons are stand-ins: `cg/leaked`, `raw-element-stand-in`, `PLANTEDSECRET`) |
| All 12 sprint-plan checks present | ✓ (1–12, with check 2 spanning all six forbidden sub-cases) |
| Meaningful, not tautological | ✓ (check 5 vs **live** `hygiene_check.find_violations`; check 4 greps **live** module source; check 9 vs hard-coded doc-04 transcription; check 11 captures stdout+stderr) |

**Evidence-value leak scan (tracked artifacts).** No rate-like decimals in `04-implementation-report.md` or
`05-review-report.md`. The sole `0.NN` match repo-wide is `tests/test_evidence_summary.py:123`
`"p-value 0.03 indicates significance"` — a **synthetic inferential-rejection poison** (the validator's job is
to reject it), **not** an exercise value. Confirmed not a leak.

## 6. Posture audit findings (binding bright lines)

Every forbidden line **held**, independently verified: no Rung-2 admission, no "beats random-legal" verdict, no
claim-ceiling advance (Rung 1), **no `docs/ledger.md` mutation** (`2a2f1c2…`, diff clean), no Rung-2 row, no
SP-6/value promotion, no numeric `M`, no OD-6 relaxation, **no inferential statistic computed**, no new eval
run, no K=50 top-up, no paired-delta tooling, no runtime-agent work, no broad optimization, no Kaggle
automation, no FunSearch surface, no cross-regime comparison (mixed-regime → exit 2, reproduced), no regime
mutation, **no sidecar read**, no `.claude/` edit, **no tracked evidence-value artifact** (exercise output
gitignored/unstaged/uncited). State-Zone files unstaged. **Rung 1 held.**

## 7. Explicit judgment on C1–C4 (independently reproduced)

### C1 — Positional digest-shape gap (review: MEDIUM) → CONFIRMED real; NON-BLOCKING this cycle; MANDATORY carry-forward
**Reproduced:** a nested `hashes` map (e.g. inside an agent) carrying a clean non-digest token yields **no**
violation; the identical token at top-level `hashes` **is** caught. The gate has a positional blind spot
because `SAFE_FIELDS` is field-name-based (faithful to doc 04 §2, which is itself a flat field list) while the
digest-shape rule is applied top-level only (`:369`).
- **Fails a Sprint 01 AC?** No. AC-2 requires the validator to reject every doc 04 §3 class "with a reason" —
  which it does in the canonical schema positions (tested; leak→exit 3 reproduced). doc 04 §2 / SDD §4.2
  specify a flat allow-list, not positional digest enforcement.
- **Does the generator emit the problematic shape?** No — independently confirmed: `build_summary` emits
  `hashes` only at top-level. The validator this cycle gates only the generator's own clean output; the local
  exercise validated clean. **No leak occurred.**
- **Safe to defer to Cycle-005?** Yes for build-only Cycle-004 (promotes nothing). **But it must be hardened
  before the validator becomes load-bearing** at the Cycle-005 promotion gate, where it will gate a
  human-promoted (possibly hand-edited) summary.
- **Recommended fix (Cycle-005, pre-promotion):** apply the digest-shape check to **every** `hashes`-keyed dict
  during `_walk`, or convert the validator to a positional/structural schema. **Record as a hard carry-forward.**

### C2 — Forbidden-word negation-window evasion (review: LOW) → CONFIRMED real; NON-BLOCKING; carry-forward
**Reproduced:** `"claim not made; agent strong"` → not flagged (an unrelated `not` within the 36-char window
suppresses it); `"agent is strong"` → flagged `['strong']`.
- **Tracked claim leak now?** No. The generator's framing strings contain **none** of the five words
  (independently: generator output validates clean), so output does not rely on this heuristic; no tracked
  artifact carries an affirmative forbidden agent-quality claim.
- **Carry-forward:** tighten to immediate-precedence negation (or require human review of framing strings)
  before promotion. Non-blocking.

### C3 — Absolute-path guard gap (review: LOW) → CONFIRMED partial; NON-BLOCKING; carry-forward
**Reproduced:** abs path to repo `docs/` non-ledger → **not** refused (gap); abs `docs/ledger.md` → **refused**
(ledger still guarded); relative `docs/…` → refused.
- **Did the sprint mutate `docs/ledger.md`?** No — hash unchanged, diff clean. The **primary** control (git
  byte-unchanged) is independent of this guard and passed. `_refuse_tracked_out` is defense-in-depth; the
  ledger basename remains guarded on any path.
- **Carry-forward:** resolve `--out` against repo root before the prefix check. Non-blocking.

### C4 — Hash granularity / empty hashes (review: NOTE) → ACCEPTABLE for Cycle-004; minor carry-forward
- **Manifest-only sourcing acceptable under SDD §3.1/§8?** Yes — the read surface is `manifest.json` +
  `match_results/*`; `hashes.txt` is excluded. doc 04 §2.1 sanctions `manifest.json` as a hashes source.
- **Avoids unauthorized `hashes.txt` reads?** Yes — independently confirmed (grep `hashes.txt` = 0).
- **Note:** if a manifest carries no 64-hex `*_hash`, that run is omitted from `hashes` (degrades to `{}`
  silently). **Carry-forward:** have the generator warn on empty `hashes` before a promoted summary is
  produced. Non-blocking.

## 8. Required fixes
**None.** No blocking issue. No posture line crossed; no AC failed; all gates green; no actual leak or value
promotion occurred.

## 9. Carry-forward recommendations (Cycle-005 / pre-promotion)
1. **C1 (priority)** — make digest-shape (and ideally the whole schema) **positional**, so a known field name
   in a non-schema position cannot bypass content checks. This is the one to fix before the validator gates any
   real promotion.
2. **C2** — tighten the forbidden-word negation heuristic (immediate precedence) or gate framing strings
   through human review at promotion.
3. **C3** — repo-root-resolve `--out` in `_refuse_tracked_out`.
4. **C4** — warn when `hashes` is empty.

These should be ingested into the **Cycle-005 PRD/SDD as pre-promotion hardening requirements**. This persisted
audit report is their tracked record. No pre-Cycle-005 source patch is required for Cycle-004 acceptance (the
cycle is build-only and promotes nothing).

## 10. Acceptance
**Sprint 01 is ACCEPTED and ready for operator commit/push.** Implementation is faithful to the
PRD/SDD/sprint-plan and the Cycle-003 authorities, comprehensively and meaningfully tested, and holds every
bright line.

**Commit-hygiene instruction for the operator (binding posture):** stage **only** the authorized Cycle-004
artifacts —
```
git add analysis/evidence_summary.py \
        tests/test_evidence_summary.py \
        docs/cycles/cycle-004/04-implementation-report.md \
        docs/cycles/cycle-004/05-review-report.md \
        docs/cycles/cycle-004/06-audit-report.md
```
Do **not** `git add -A` — `.beads/issues.jsonl` and `grimoires/loa/NOTES.md` are pre-existing State-Zone
housekeeping and **must remain unstaged**. The gitignored local exercise output is unstageable by construction.
The optional `grimoires/loa/a2a/sprint-…/COMPLETED` marker, if created, is gitignored and does not affect the
tracked tree.

---

> **Provenance.** Audit run at HEAD `8ac161d`; `docs/ledger.md` byte-unchanged (`2a2f1c2…`); claim ceiling
> Rung 1; C1/C2/C3 independently reproduced; no dispersion value read or cited; nothing staged/committed/pushed.
> **Verdict: PASS WITH NOTES — ACCEPTED.** Next: operator commit/push of the five authorized Cycle-004
> artifacts; C1–C4 carried forward to Cycle-005.
