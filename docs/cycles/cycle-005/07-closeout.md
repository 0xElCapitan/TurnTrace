# Cycle-005 Closeout — Promotion-Gate Hardening (C1–C4)

> Cycle closeout artifact. Status: **CLOSED — accepted, committed, pushed.** Cycle-005 hardened the Cycle-004
> evidence-summary generator/validator (`analysis/evidence_summary.py` + `tests/test_evidence_summary.py`) per
> the four pre-promotion carry-forwards C1–C4. **Cycle-005 was hardening-only:** it attempted no Rung 2,
> promoted no value, and mutated neither `docs/ledger.md` nor `docs/claim-ceiling.md`.
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, simulator logs, `deck.csv` rows, run-dir
> dumps, Pokémon Elements, Daily-Top-Episode data, or Competition Data appear here. **No dispersion metric
> values appear here.** The forbidden agent words (*strong / competitive / optimal / calibrated / complete*)
> and inferential terms (*std-dev / variance / CI / p-value / significance / hypothesis-test / error-bar*)
> appear only as the negated/forbidden language they are.

| Field | Value |
|---|---|
| **Cycle** | Cycle-005 |
| **Working title** | Promotion-Gate Hardening (C1–C4) |
| **Type** | Cycle Closeout |
| **Date** | 2026-06-19 |
| **Status** | **CLOSED — hardening-only; accepted, committed, pushed** |
| **Durable implementation commit** | `fd16cb5ac32ef6ebf7f57c8bd2dee482d715a191` — *feat: harden TurnTrace evidence-summary gate* |
| **Planning commit** | `6d1efbe7e0941d9c0b43a74f73563f9ef31b4b2a` — *docs: plan TurnTrace Cycle-005* |
| **Claim ceiling** | **Rung 1** (held for the whole cycle; not raised) |
| **Ledger** | `docs/ledger.md` byte-unchanged; hash `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` |

---

## 1. Outcome

Cycle-005 Sprint 01 — Promotion-Gate Hardening C1–C4 — completed the full
`/implement → /review-sprint → /audit-sprint` loop and was **accepted, committed, and pushed**:

- **Implementation** (`docs/cycles/cycle-005/04-implementation-report.md`) — landed C1–C4 exactly as the SDD
  designed (OD-C5-1…OD-C5-6); all 12 existing checks plus the new block-13 checks (13a–13l) green.
- **Review** (`docs/cycles/cycle-005/05-review-report.md`) — **PASS WITH NOTES**; conservative-only verified by
  a 20,000-string fuzz (zero loosening cases).
- **Audit** (`docs/cycles/cycle-005/06-audit-report.md`) — **PASS WITH NOTES — ACCEPTED**; C1–C4 independently
  re-verified through the real CLI exit path and a Cycle-004-vs-Cycle-005 comparison; no required fixes.

**Commit `fd16cb5` is the durable pushed implementation state** (`origin/main` == `fd16cb5`). It staged exactly
the five accepted Sprint 01 files (`analysis/evidence_summary.py`, `tests/test_evidence_summary.py`, and the
`04`/`05`/`06` cycle reports) and mutated neither the ledger nor the claim ceiling.

**Cycle-005 is closed as Promotion-Gate Hardening C1–C4.** The evidence-summary validator is now strictly more
conservative — the prerequisite hardening so a *future* Rung-2 attempt can run an admission gate through a
validator that has itself been reviewed and audited in a load-bearing posture.

---

## 2. The four hardenings (fixed and tested)

- **C1 — nested-`hashes` digest-shape enforcement (priority hard blocker).** Added `_enforce_hashes_digest`,
  invoked from `_walk` for **every** `hashes`-keyed dict at any depth (not just the top-level block). A nested
  clean non-digest token is now rejected (exit 3); a nested valid digest is not falsely flagged; the top-level
  digest block and flat `SAFE_FIELDS` are preserved. No schema rewrite, no `.schema.json`, no dependency.
  **Fixed and tested as hardening, not admission.**
- **C2 — immediate-precedence forbidden-word negation.** Repurposed `_NEGATION_RE` to an end-anchored
  immediate-precedence rule and `_NEG_WINDOW` to the look-behind bound (token set preserved). An unrelated
  negation no longer suppresses an affirmative forbidden word; legitimate negated/forbidden-language examples
  still validate; an affirmative quality claim is still rejected. The broad-window loophole is closed; the rule
  is a strict subset of Cycle-004's suppression (fuzz- and comparison-verified). **Fixed and tested as
  hardening, not admission.**
- **C3 — repo-root-resolved `--out` guard.** `_refuse_tracked_out` now repo-root-resolves the candidate path
  first, refusing an absolute path into the repo's tracked `docs/` (and a `..`-traversal path that collapses
  into it). The relative-`docs/` prefix check and the `ledger.md` basename guard are preserved verbatim; safe
  local/gitignored paths remain allowed; `docs/ledger.md` is byte-unchanged. **Fixed and tested as hardening,
  not admission.**
- **C4 — empty-`hashes` stderr warning.** Generate mode emits a stderr `WARNING` when assembled `hashes` is
  empty, mentioning the missing manifest integrity stamp; **exit 0 is preserved** and stdout stays JSON-first
  (no leak). `--validate` still accepts a structurally-valid empty `hashes` at exit 0. Manifest-only sourcing
  is preserved (no unauthorized hash-source file read); no new exit code; no `--promotion-check` mode.
  **Defined and tested as hardening, not admission.**

The validator became **strictly more conservative, not looser**: every change either rejects more inputs or
rejects the same set; no input the Cycle-004 validator rejected is now accepted.

---

## 3. Posture held (hardening-only bright lines)

- **Rung 1 held** for the whole cycle. No Rung-2 attempt, no Rung-2 admission, no same-regime admission verdict.
- **No value promoted.** No dispersion value reached tracked status; the generator stays local-by-default; the
  summary still carries no ceiling of its own.
- **No `M`** chosen. **No SP-6** issued. **No OD-6 relaxation;** no inferential statistic produced.
- **No Rung-2 ledger row.** `docs/ledger.md` byte-unchanged at hash `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`.
- **No claim-ceiling advance.** `docs/claim-ceiling.md` untouched.
- **No raw Competition Data / Pokémon Elements / Daily-Top-Episode data** added; tests use stdlib-only
  synthetic fixtures; `eval/hygiene_check.py` exit 0 on all committed artifacts.
- **No `.schema.json`, no second validator module, no third-party dependency, no `--promotion-check` mode, no
  new exit code** — the `0/1/2/3` contract and stdlib-only / in-module-constant / one-module posture are
  preserved.
- **No `.claude/` edit; no State-Zone cleanup.** The pre-existing dirty State-Zone files
  `.beads/issues.jsonl` and `grimoires/loa/NOTES.md` **remained unstaged and untouched** throughout the cycle
  (not part of commit `fd16cb5`).

---

## 4. Carry-forwards for Cycle-006+ (future-scoped, non-blocking)

From the audit (`06-audit-report.md` §11), recorded as non-blocking future work:

1. **CF-1 — a future promotion gate MUST hard-fail empty `hashes`.** C4 correctly only *warns* in Cycle-005
   (no promotion mode exists; no value promoted). The OD-C5-2 floor — *no promotion gate may trust silently-
   empty `hashes`* — becomes a hard failure when a promotion-check is introduced (Cycle-006+).
2. **CF-2 — optional top-level duplicate-violation dedupe.** A top-level non-digest is now reported twice (the
   preserved top-level block + the new traversal both catch it); the CLI exit code is unaffected (still 3).
   Only `_run_validate`'s printed `len(violations)` over-counts a top-level digest leak by 1 — cosmetic. Dedupe
   only if that printed count ever becomes programmatic.
3. **CF-3 — document C2 word-adjacency semantics.** Immediate-precedence keys on "no intervening *content
   word*", so whitespace/punctuation between a negation and a forbidden word still suppresses (e.g.
   `"not-strong"`). This matches SDD intent and does not loosen the validator versus Cycle-004 (that exact
   string was already suppressed). Record the semantics if the negation rule is revisited.

### Rung-2 admission seam — Cycle-006+ must handle explicitly

Cycle-005 deliberately **did not** cross the admission seam. A future Rung-2 attempt (Cycle-006 or a later
explicit operator gate) must resolve **all** of the following before any promotion:

- **OD-6 / disjoint-bands posture** — whether the criterion is disjoint observed bands or a relaxed OD-6
  (seam decision 8a).
- **Numeric margin `M`** — a chosen, defensible value (seam decision 8b); currently unset.
- **SP-6** — the operator-only live-value promotion decision (seam decision 8c); not issued.
- **Rung-2 ledger row / claim-ceiling advance procedure** — the row cites the promoted summary by reference +
  content hash; the ledger is the only ceiling-bearing artifact (seam decision 8d).
- **Defensible pre-registration of `M`** — chosen *before* seeing the bands, to avoid post-hoc thresholding
  (the already-generated K=20+20 bands risk post-hoc selection if reused).
- **Whether fresh, never-observed bands are needed** — i.e. whether a new same-regime batch must be generated
  so `M` is pre-registered against unseen evidence rather than the already-observed Cycle-004 exercise bands.

A Rung-2 attempt may proceed **only after** Cycle-005 hardening (now landed) **and** an explicit operator gate
opens, with the five conjunctive Rung-2 readiness criteria satisfied.

---

## 5. Provenance

| Artifact | Commit |
|---|---|
| Planning stack (PRD/SDD/Sprint-Plan) | `6d1efbe` — *docs: plan TurnTrace Cycle-005* |
| Implementation + review + audit (5 files) | `fd16cb5` — *feat: harden TurnTrace evidence-summary gate* |
| This closeout | *docs: close TurnTrace Cycle-005 Sprint 01* (this commit) |

> **Sources:** `docs/cycles/cycle-005/01-prd.md`, `02-sdd.md`, `03-sprint-plan.md`, `04-implementation-report.md`,
> `05-review-report.md`, `06-audit-report.md`; `analysis/evidence_summary.py` + `tests/test_evidence_summary.py`
> (at `fd16cb5`); `docs/claim-ceiling.md` (Rung 1); `docs/ledger.md` (hash `2a2f1c2…`). Cycle-005 closed
> hardening-only: it built no admission logic, mutated no ledger, advanced no ceiling, promoted no value, and
> edited no `.claude/`. **Rung 2 remains deferred to Cycle-006 or a later explicit operator gate.**
