# Cycle-007 Pre-Registration Record — The Single Rung-2 Comparison Tuple

**Date:** 2026-06-19
**Cycle / sprint:** Cycle-007, Sprint **S02** (Pre-registration record).
**Status:** binding pre-registration. **No evidence is generated, read, or applied in this record.**

> This is the **Cycle-007 Sprint S02 pre-registration record**. It freezes the one
> frozen comparison tuple the operator fixes, **before any fresh band exists**, so that
> "**`M` before bands**" is tamper-evident in git history. This record is the binding
> artifact; the PRD/SDD/sprint-plan may only *reference* it (`02-sdd.md` §2.1). The
> load-bearing integrity property is **the commit order, not this prose** — see §10.
> This record **chooses the tuple below and generates no evidence** (no eval run, no
> band read, no verdict). The full non-occurrence statement is §11.

---

## 0. What this record is (and is not)

- **Is:** the dated, tracked, to-be-committed record of the single comparison tuple for
  the Cycle-007 gated Rung-2 admission attempt (PRD `01-prd.md` C7-FR-1; `02-sdd.md` §2.1).
- **Is not:** an evidence artifact, an eval run, a band reading, a verdict, a promotion,
  a ledger row, or a claim-ceiling advance. None of those occur here (§11).
- **Standing posture (unchanged by this record):** the loop sits at **ladder Rung 1**;
  Cycle-007 holds Rung 1 at open (`docs/claim-ceiling.md`; `01-prd.md` §12). Rung 2 is
  *attempted* behind operator gate **OD-C7-3** and is earned **only** on a pre-registered
  fresh same-regime **PASS** plus the separate PASS-gated terminal acts (§9).
- **The `docs/ledger.md` experiment ledger remains the only ceiling-bearing artifact**
  (`01-prd.md` C7-FR-5.2; `docs/claim-ceiling.md`).

---

## 1. The frozen comparison tuple (the seven fields)

Exactly **one** candidate, **one** baseline, **one** regime. No list, no "best-of"
(`02-sdd.md` §2.2.2; sprint-plan O6).

| Field | Value |
|---|---|
| **candidate** | `scripted-v001` |
| **baseline** | `random_legal` (under the new regime) |
| **regime** | `regime-v003` |
| **`M`** | `0.05` win-rate units |
| **`K`** | `20` batches |
| **`n`** | `500` matches per batch per agent |
| **stopping rule** | Generate/read **exactly** `K = 20` fresh same-regime batches at `n = 500`; then stop. *(Full text below.)* |

**Tuple, compactly:** `(candidate = scripted-v001, baseline = random_legal, regime = regime-v003, M = 0.05, K = 20, n = 500, stopping-rule = read-exactly-20-batches-at-n-500-then-stop)`.

**Provenance of the agents (existing frozen agents; NFR-8 — runtime-agent lane closed):**
- `scripted-v001` is an **existing frozen agent** (it appears as a prior frozen
  `agent_version` in `docs/ledger.md`). Re-running a frozen agent to *generate evidence*
  is eval scope, not agent-building (`01-prd.md` NFR-8). No new agent/heuristic is built.
- `random_legal` is the **existing frozen random-legal baseline** (ledgered previously as
  `random_legal-v001`). Rung 2 is defined as *"beats random-legal"* (`docs/claim-ceiling.md`;
  `02-sdd.md` §2.1, baseline row). For this attempt it runs **under `regime-v003`**.

**Stopping rule (full, binding):** Generate/read **exactly 20** fresh same-regime batches
at `n = 500`; **no** interim verdict, **no** peeking-based changes, **no** top-up, **no**
expansion, **no** replacement, **no** optional stopping, **no** batch-padding, **no**
candidate swap, **no** best-of-N, **no** `M` change. A **FAIL** or **INCONCLUSIVE**
advances **no** ceiling, promotes **no** value, writes **no** Rung-2 row, and **never**
relaxes or re-picks `M` (see §7).

---

## 2. `M` — units and interpretation

- **`M = 0.05` win-rate units.** This is a **governance threshold**, not a dispersion
  value; it lives **only** in this record and nowhere else tracked (`02-sdd.md` §2.2.3;
  `01-prd.md` §13). A numeric `M` in any other tracked artifact is a posture violation → HALT.
- **PASS margin:** PASS requires the candidate's per-batch win-rate **`min`** to **exceed**
  the baseline's per-batch win-rate **`max`** by **at least `0.05`** across the fresh
  `K = 20` same-regime batches (the ratified **8a descriptive disjoint-bands** rule;
  `docs/cycles/cycle-006/01-prd.md` §16.3; `01-prd.md` C7-FR-4.1) — **in addition to** all
  gate, provenance, and noise-floor requirements (§7).
- The margin is **descriptive only**: no inferential statistic is computed, and no
  forbidden agent word (strong / competitive / optimal / calibrated / complete) is applied
  even on a PASS (`docs/claim-ceiling.md`; `01-prd.md` NFR-3).

---

## 3. `n = 500` — justification (the noise-floor argument)

The justification is **explicit, not assumed** (`02-sdd.md` §2.2.5; sprint-plan AC "`n`
justification"):

- **Runs are unseeded.** The capability probe found no controllable RNG seed
  (`docs/claim-ceiling.md`, reproducibility posture; `sim/capabilities.json:
  seed_controlled=false`); records carry `match_index`, not `seed`.
- **Observed dispersion conflates agent behaviour with simulator RNG**
  (`docs/cycles/cycle-003/08-funsearch-forward-compat.md` §3, carried at `01-prd.md` §9):
  the evaluator must average over enough matches/batches to clear the noise floor before a
  per-candidate scalar is stable.
- **`n = 500` per batch per agent** is chosen as a **practical, serious attempt** to
  average over simulator noise without making the first Rung-2 attempt unnecessarily huge.
- **If the justified-`n` / noise-floor requirement is not satisfied at verdict time, the
  result is INCONCLUSIVE — not a reason to change `n` post-hoc** (`01-prd.md` C7-FR-6.2;
  see §7). `n` is frozen here with the rest of the tuple.

---

## 4. The three §11 verdict-rule tightenings (binding for this attempt)

Confirmed as binding (OD-C7-8; `01-prd.md` §11; research §7):

1. **Freeze the full tuple, not just `M`.** The pre-registration freezes
   `candidate / baseline / regime / M / K / n / stopping-rule` — all seven fields (§1) —
   not `M` alone. The verdict (S04) binds to **exactly this one tuple**.
2. **No optional stopping or batch-padding.** Read **exactly** the pre-declared `K = 20`
   batches at the pre-declared `n = 500`; no appending batches until a margin appears; no
   early stop. INCONCLUSIVE remediation is a **new** pre-declared batch, never an extension
   of this one.
3. **INCONCLUSIVE means admissibility failure, not band ambiguity.** INCONCLUSIVE is
   scoped to admissibility preconditions (noise floor not cleared, incomplete
   provenance/hashes, failing `--promotion-check`), **not** to "the bands looked close."

---

## 5. Old-evidence exclusion (the existing K=20+20 is historical context only)

The existing **K=20+20** evidence (the prior `regime-v002` batches, local/gitignored under
`runs/`) is **historical context only** (`01-prd.md` §9, NFR-1; `02-sdd.md` §4.4;
sprint-plan O4):

- It is **not** the verdict basis.
- It is **not** used to choose `M` (fixing `M` against an already-observed set is post-hoc
  thresholding — the in-house analogue of FM-11).
- **No K=50 top-up.**
- **No expansion** of an observed batch.

Because the fresh batch runs under a **new** `regime-v003`, the old `regime-v002` bands are
not even same-regime-comparable (§6; `02-sdd.md` §2.4 "old-evidence reuse").

---

## 6. Same-regime requirement (one new frozen `regime-v003`)

- **Baseline and candidate both run under the one new frozen `regime-v003`** (`01-prd.md`
  C7-FR-3.1, NFR-2; `02-sdd.md` §4.1; sprint-plan O3).
- **No cross-regime comparison.** The validator and `--promotion-check` hard-refuse mixed
  regimes (exit 2); a `regime-v002` number is never compared beside a `regime-v003` number
  (`02-sdd.md` §3.1, §2.4; `analysis/dispersion_report.py`).
- **A new `n` / new seed-set means a new regime, not an edit of `regime-v001`** (or of
  `regime-v002`). `regime-v003` is a *new* version id, never an edit of a prior regime
  (`02-sdd.md` §2.2.4; `01-prd.md` NFR-2/NFR-5).

**Regime resolution (why `regime-v003`):** the repo's frozen regime authority
`frozen/regimes/` already defines `regime-v001.json` and `regime-v002.json` (both tracked);
`regime-v002` is additionally **observed** (the historical K=20+20 batches in `runs/`,
§5). No `regime-v003` definition and no `regime-v003` run dirs exist. The next free,
never-observed regime id is therefore **`regime-v003`**.

---

## 7. The verdict rule (imported by reference) — PASS / FAIL / INCONCLUSIVE

The PASS / FAIL / INCONCLUSIVE criteria and fail-state language are the ones
**pre-registered in `docs/cycles/cycle-006/01-prd.md` §16.3**, imported here **by
reference** to avoid divergence (`01-prd.md` §11; C7-FR-4). They are applied to **exactly
the one tuple** in §1. In summary (the cited source governs on any wording question):

- **PASS** — the §2 margin is met under the pre-registered `M = 0.05` **and** the promoted
  summary passes **`--validate` and `--promotion-check`** (non-empty integrity stamp, full
  hardened validator clean) **and** provenance/audit-trail is intact **and** the
  justified-`n` / noise-floor argument is satisfied → the operator **may** take the
  separate terminal acts (§9).
- **FAIL** — the margin is **not** met → **no** ceiling advance, **no** promotion, **no**
  Rung-2 row; recorded honestly at **Rung 1**; not a regression; `M` and the rule are
  **never** re-picked after the bands to manufacture a PASS.
- **INCONCLUSIVE** — an admissibility precondition is unmet (§4 tightening 3) → **no**
  advance, **no** promotion; remediate by generating a **new** pre-declared batch under the
  **same** `M`/rule, never by extending this batch and never by relaxing `M`.

---

## 8. Gate requirements (S01 already landed; S03/S04 must use both modes)

- The **S01 absent-`hashes` gate-pin** is already landed on `main` at **`ceb6f67`**
  (`test: pin promotion-check absent hashes`).
- **S03/S04 must require both `--validate` and `--promotion-check`** on the promoted
  candidate summary before any Rung-2 row is written (`01-prd.md` C7-FR-2.2, §10.2).
- **`--promotion-check` gates only — it writes nothing, promotes nothing**, never writes
  `docs/ledger.md` or any tracked `docs/` path, and preserves the `0/1/2/3` exit contract
  (`01-prd.md` C7-FR-2.3; `docs/cycles/cycle-006/07-closeout.md` §2). Any behaviour change
  to these modes is a posture violation → HALT.

---

## 9. Terminal-act requirements (PASS only; each a separate operator act)

On **PASS only**, and **only after `--promotion-check` passes**, the operator MAY take, as
**separate explicit acts in order** (`01-prd.md` C7-FR-5; OD-C7-10; `02-sdd.md` §6):

1. issue **SP-6** to promote the sanitized summary to tracked status (reference + content
   hash + sanitized metric names; never raw content);
2. write the **Rung-2 ledger row** (existing 18-column schema verbatim; append-only; cites
   the promoted summary by reference + content hash; never edit a past row);
3. advance **`docs/claim-ceiling.md`** to Rung 2.

- **None** of these occur on **FAIL** or **INCONCLUSIVE**.
- **None** occur in S02 or S03.
- The **`docs/ledger.md` ledger remains the only ceiling-bearing artifact**; the evidence
  **summary carries no ceiling of its own** (`01-prd.md` C7-FR-5.2).

---

## 10. Commit-order requirement (the load-bearing "`M` before bands" property)

- **This pre-registration record MUST be committed and pushed before any S03 fresh-evidence
  generation or band observation** (`01-prd.md` C7-FR-1.2; `02-sdd.md` §2.3; sprint-plan
  O1). The precedence is tamper-evident in history: this record's commit hash and date are
  earlier than the generation commit's.
- **S03 MUST verify the S02 commit is strictly ancestral to the generation commit before
  generating evidence** — confirm `git log --oneline` shows the pre-registration commit
  ancestral to (strictly before) the generation commit, and confirm the generation surface
  was untouched at the pre-registration commit (`git show <pre-reg-commit> --stat` lists
  **no** run-dir / evidence path) (`02-sdd.md` §2.3; sprint-plan O1, S02 AC "Commit-order").

---

## 11. Non-occurrence statement (this S02 implementation pass)

This S02 implementation pass:

- generated **no** evidence;
- ran **no** eval;
- read **no** bands;
- issued **no** SP-6;
- promoted **no** value;
- wrote **no** Rung-2 ledger row;
- advanced **no** claim ceiling;
- applied **no** PASS / FAIL / INCONCLUSIVE verdict.

`docs/ledger.md` is byte-unchanged (`2a2f1c2…`) and `docs/claim-ceiling.md` is unchanged
(still Rung 1) (`01-prd.md` §16.3, NFR-5). The only tracked change introduced by S02 is
**this record**.

---

## 12. Sources / traceability

- **Pre-registration requirement & shape:** `01-prd.md` C7-FR-1, §9, §11, §13, §15;
  `02-sdd.md` §2.1 (record representation), §2.2 (validity conditions), §2.3 (commit-order),
  §2.4 (anti-contamination).
- **Verdict rule (imported by reference):** `docs/cycles/cycle-006/01-prd.md` §16.3.
- **Promotion gate:** `01-prd.md` C7-FR-2, §10; `docs/cycles/cycle-006/07-closeout.md` §2.
- **Terminal acts / ledger / ceiling:** `01-prd.md` C7-FR-5, §12; `docs/ledger.md`;
  `docs/claim-ceiling.md`.
- **Sprint contract & gates:** `03-sprint-plan.md` §2 (O1–O7), §3 (OD-C7-1…10), Sprint S02.
- **Noise-floor / `n`:** `docs/cycles/cycle-003/08-funsearch-forward-compat.md` §3
  (carried at `01-prd.md` §9).
- **Regime authority:** `frozen/regimes/regime-v001.json`, `frozen/regimes/regime-v002.json`
  (tracked); next free id = `regime-v003`.
