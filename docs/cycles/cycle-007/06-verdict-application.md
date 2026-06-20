# Cycle-007 S04 — Verdict Application (§16.3 disjoint-bands rule, one frozen tuple)

**Date:** 2026-06-19
**Cycle / sprint:** Cycle-007, Sprint **S04** — Verdict application.
**Type:** governance — apply the pre-registered §16.3 rule to exactly the one frozen tuple.
**Status:** verdict applied. **This report takes no terminal act** (no SP-6, no promotion, no
Rung-2 ledger row, no claim-ceiling advance).

> Sanitization posture: this tracked artifact carries **references + sanitized agent / regime /
> metric names + the minimal descriptive verdict surface (allowed vocabulary: per-batch `min` /
> `max` and their descriptive difference) + gate exit codes + the single verdict word**. It
> embeds **no** raw traces, simulator logs, deck lists, card IDs/names, Pokémon Elements,
> Competition Data, Daily Top Episodes, run-dir dumps, PDFs/CSVs, raw evidence rows, the local
> summary JSON, inferential statistics, the numeric governance threshold `M` (which lives **only**
> in `04-pre-registration.md` §2; a numeric `M` in any other tracked artifact is a posture
> violation), any forbidden agent word (see `docs/claim-ceiling.md`), or any ceiling-bearing
> claim beyond the explicit verdict. The claim ceiling is **not** advanced by this report.

---

## 1. Inputs (by reference only)

| Input | Reference | Read posture |
|---|---|---|
| Pre-registration record (binding tuple + rule by reference) | `docs/cycles/cycle-007/04-pre-registration.md` | committed; the binding artifact |
| Verdict rule (imported by reference) | `docs/cycles/cycle-006/01-prd.md` §16.3 | committed |
| S03 admissibility report | `docs/cycles/cycle-007/05-evidence-generation-report.md` | committed |
| Evidence summary | `.run/s03-gen/evidence-summary-regime-v003.json` | **local / gitignored / untracked**; read-only here |

The verdict reads **only** the local/gitignored evidence summary and the committed
pre-registration record. No historical K=20+20 evidence, no `regime-v001` / `regime-v002`
evidence, no alternate candidate, no best-of-N is consulted.

## 2. Anchors (commit-order — "`M` before bands")

- **S02 O1 pre-registration anchor** (the tuple, including `M`, fixed before any band existed):
  `a27aef38db5cded5120c4eb923f6a7e8cd27a6e2`
- **S03 admissibility / provenance anchor** (current HEAD):
  `3f6dcd9bfdebe7dfb1c323266c99e14134006018`
- Ancestry holds: `git merge-base --is-ancestor a27aef38… 3f6dcd9…` → exit `0`. The threshold
  was frozen strictly **before** the fresh `regime-v003` bands were generated; the
  "`M` before bands" property is tamper-evident in history.

## 3. The one frozen tuple (sanitized identifiers)

The verdict binds to **exactly** this tuple (§16.3 tightening 1: freeze the full tuple).

| Field | Value |
|---|---|
| candidate | `scripted-v001` |
| baseline | `random_legal-v001` (under the new regime) |
| regime | `regime-v003` |
| `M` | the pre-registered governance threshold (numeric value recorded **only** in `04-pre-registration.md` §2) |
| `K` | 20 batches per side |
| `n` | 500 matches per batch per agent |
| stopping rule | read exactly the 20 pre-generated same-regime batches, then stop |

No candidate swap, no best-of-N, no alternate baseline/regime, no threshold/`K`/`n`/stopping-rule
change occurred in applying the verdict.

## 4. Gate re-checks (admissibility precondition — both exit 0)

Run on the local/gitignored summary before the verdict was applied:

| Gate command | Exit code |
|---|---|
| `python analysis/evidence_summary.py --validate .run/s03-gen/evidence-summary-regime-v003.json` | `0` |
| `python analysis/evidence_summary.py --promotion-check .run/s03-gen/evidence-summary-regime-v003.json` | `0` |

`--validate` exit 0 → schema-conforming, sanitized, single-regime. `--promotion-check` exit 0 →
the full hardened validator is clean **and** the summary carries a non-empty `hashes` integrity
stamp; it writes nothing and promotes nothing. Both passing establishes **admissibility** — a
**precondition** of a PASS, never a substitute for the margin. (Either gate nonzero → exit 3 →
INCONCLUSIVE, never a PASS; that branch did not occur.)

## 5. The §16.3 rule applied (concise)

The ratified **8a descriptive disjoint-bands** rule (`docs/cycles/cycle-006/01-prd.md` §16.3,
imported by reference; `01-prd.md` C7-FR-4):

- **PASS** — the candidate's per-batch win-rate **`min`** exceeds the baseline's per-batch
  win-rate **`max`** by at least the pre-registered `M` across the fresh `K = 20` same-regime
  batch, **and** the summary passes `--validate` + `--promotion-check` (non-empty integrity
  stamp, full validator clean), **and** provenance/audit-trail is intact, **and** the
  justified-`n` / noise-floor argument is satisfied.
- **FAIL** — the margin is not met.
- **INCONCLUSIVE** — an admissibility precondition is unmet (noise floor not cleared; bands
  neither cleanly disjoint-by-`M` nor cleanly not; provenance/hashes incomplete; `--promotion-check`
  fails on integrity).

Applied to exactly the one tuple (§3), using only the allowed descriptive vocabulary
(`count / min / max / range / mean / median / spread`). **No inferential statistic** is computed
(no p-value, confidence interval, hypothesis test, std-dev, variance, value model). **No forbidden
agent word** is applied even on PASS.

## 6. Authorized descriptive verdict surface (allowed vocabulary only)

Read from the local/gitignored summary — single regime `regime-v003`, `K = 20`, `n = 500`,
per-batch win-rate across the 20 batches:

| Quantity (per-batch win-rate, across `K = 20`) | Value |
|---|---|
| candidate `scripted-v001` win-rate **`min`** | `0.760` |
| baseline `random_legal-v001` win-rate **`max`** | `0.568` |
| descriptive separation (candidate `min` − baseline `max`) | `0.192` |

- The per-batch win-rate bands are **disjoint**: candidate `min` (`0.760`) is strictly greater
  than baseline `max` (`0.568`); the two bands do not overlap.
- The descriptive separation (`0.192`) **exceeds** the pre-registered `M` → the bands are
  **cleanly disjoint-by-`M`**. This is the cleanly-disjoint branch, **not** the INCONCLUSIVE
  "neither cleanly disjoint nor cleanly not under unseeded noise" case (the separation is several
  times `M` and larger than either band's own per-batch dispersion).
- **Provenance/audit-trail intact** — the summary's `hashes` integrity stamp is non-empty
  (40 entries, every value a 64-hex SHA-256 digest); `--promotion-check` exit 0 confirms it.
- **Justified-`n` / noise-floor satisfied** — `n = 500` per the pre-registration; the band
  separation is large relative to the per-batch dispersion, so the floor is cleared for this
  comparison.

These four conditions are the §16.3 PASS conjunction, all holding together.

## 7. Verdict

### **PASS**

All §16.3 PASS conditions hold conjointly: the margin is met under the pre-registered `M`
(candidate `min` `0.760` exceeds baseline `max` `0.568` by `0.192`); `--validate` exit 0;
`--promotion-check` exit 0 with a non-empty integrity stamp; provenance/audit-trail intact;
justified-`n` / noise-floor satisfied.

The verdict is the **same-regime TurnTrace descriptive statement** that, under `regime-v003` at
`n = 500` over `K = 20` batches, the candidate `scripted-v001` beats the `random_legal-v001`
baseline by the pre-registered descriptive margin. It is **never** episode-derived. It asserts
**nothing** beyond this regime and **no** forbidden agent word (see `docs/claim-ceiling.md`):
the candidate is not described in any agent-strength terms, only as beating the random-legal
baseline by the pre-registered descriptive margin under this one regime.

## 8. This is not a terminal act

This report **applies the verdict only**. It is **not** a terminal act and changes no
ceiling-bearing artifact. Specifically, this report:

- issues **no** SP-6;
- promotes **no** value (the evidence summary stays local/gitignored / untracked);
- writes **no** Rung-2 ledger row;
- advances **no** claim ceiling — `docs/claim-ceiling.md` is unchanged and **still states Rung 1**;
- does **not** modify `docs/ledger.md` (byte-unchanged at
  `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`).

The experiment ledger (`docs/ledger.md`) remains the **only** ceiling-bearing artifact, and this
verdict carries no ceiling of its own. The claim ceiling has **not** advanced.

## 9. PASS ⇒ OD-C7-10 required for each terminal act (none taken here)

Because the verdict is **PASS**, the three terminal acts become *possible* but **none is taken in
this report**. Each requires its **own separate explicit operator authorization under OD-C7-10**,
in order, and only after the gate passed (`01-prd.md` C7-FR-5; `02-sdd.md` §6):

1. issue **SP-6** to promote the sanitized summary to tracked status (reference + content hash +
   sanitized metric names; never raw content);
2. write the **Rung-2 ledger row** (existing 18-column schema verbatim; append-only; cites the
   promoted summary by reference + content hash; no `verdict` column);
3. advance **`docs/claim-ceiling.md`** to Rung 2.

Until each OD-C7-10 act is separately authorized and taken, the loop's standing posture is
unchanged: **Rung 1 holds**, `docs/ledger.md` is byte-unchanged, and Rung 2 is **not yet earned**.
**OD-C7-10 operator authorization is now required for the terminal acts.**

## 10. Sources / traceability

- **Frozen tuple + `M` / `K` / `n` / stopping rule + verdict rule (by reference):**
  `docs/cycles/cycle-007/04-pre-registration.md` (§1–§7, §11).
- **Verdict rule (imported by reference):** `docs/cycles/cycle-006/01-prd.md` §16.3.
- **S04 contract / goals:** `docs/cycles/cycle-007/03-sprint-plan.md` (Sprint S04; G4/G5/G6).
- **Verdict + terminal-act sections:** `docs/cycles/cycle-007/02-sdd.md` (§5 verdict application;
  §6 terminal PASS-gated acts).
- **Functional requirements:** `docs/cycles/cycle-007/01-prd.md` (C7-FR-4 verdict; C7-FR-5
  terminal acts; C7-FR-6 fail-state; §16.3 hard invariants).
- **Admissibility / fresh evidence:** `docs/cycles/cycle-007/05-evidence-generation-report.md`.
- **Gates:** `analysis/evidence_summary.py` (`--validate`, `--promotion-check`); staging guard
  `eval/hygiene_check.py`.
