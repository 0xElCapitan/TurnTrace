# Rung-2 Ledger-Row + Verdict Convention (Cycle-003 / Sprint 00 · S00-T3)

| Field | Value |
|---|---|
| **Type** | Docs-only format/spec convention (authorizes no code; opens no build gate; writes no ledger row) |
| **Status** | Authored — Cycle-003 Sprint 00 deliverable (S00-T3); convention authority for a *later* admission gate |
| **Date** | 2026-06-19 |
| **Lane / FR** | Lane C · C3-FR-3 · S00-T3 |
| **Scope** | Specifies, as format/spec only, the convention for a future deliverable Rung-2 ledger row and its verdict rule, and the separation between the ceiling-bearing row and the confidence-bearing evidence summary. **No row is written; `docs/ledger.md` is byte-unchanged.** |
| **Related** | `docs/ledger.md` (the only ceiling-bearing artifact; the existing schema this convention reuses verbatim), `docs/cycles/cycle-002/06-ledger-report-discipline.md` (the same-class precedent), `04-evidence-summary-schema-spec.md` (the summary a row would cite), `docs/claim-ceiling.md`, `docs/operator/turntrace-loop-contract.md` (§7-§8), `docs/cycles/cycle-003/01-prd.md` (C3-FR-3, §8), `docs/cycles/cycle-003/02-sdd.md` (§7) |

> Sanitized note. No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, or Competition Data appear here (CC-1/CC-2, ESP).
> **No dispersion metric values appear here.** Runs are referenced by `run_id`, content hashes, sanitized
> metric *names*, claim ceilings, and local path/status only. The forbidden agent claim words (*strong /
> competitive / optimal / calibrated / complete*) appear only as negated/forbidden language.

> **Boundary banner (binding).** This document opens **no build gate** and is **not** a Rung-2 admission. It
> specifies the *format/convention* for a future deliverable Rung-2 row and its verdict rule, so a later
> admission gate can write one against a settled design. It **writes no ledger row**, **edits no
> `docs/ledger.md`**, **advances no claim ceiling**, and **promotes no value**. Writing a Rung-2 row and
> advancing the ceiling are a separate later Rung-2 admission gate (`02-sdd.md:343-348`; NG1-NG3). The claim
> ceiling stays **Rung 1**.

## 1. The row reuses the existing ledger schema verbatim — adds no column

A future deliverable Rung-2 row follows the **existing append-only ledger schema verbatim, adding no new
column** (`docs/ledger.md:9`; `01-prd.md:203-211`; `02-sdd.md:316-322`). The columns, in order, are exactly
those of `docs/ledger.md:9`:

`date` · `run_id` · `regime_id` · `git_rev` · `sim_version` · `agent_version` · `opponent_pool_ref` ·
`seed_set_ref` · `games` (the sample size `n`) · `win_rate` · `illegal_action_rate` · `timeout_rate` ·
`error_rate` · `avg_turns` · `mode` · `hypothesis` · `claim_ceiling` · `notes`

- The ledger is **append-only; never edit a past row** (`docs/ledger.md:3-7`).
- `claim_ceiling` is **required and non-empty** (`eval/schemas.md:119`; `docs/ledger.md:3-4`). It is the
  field **where a Rung-2 ceiling would one day be recorded — by a separate operator decision, never by this
  cycle** (`01-prd.md:272-274`; `02-sdd.md:321-322`).
- The `hypothesis` column is the experiment-hypothesis **text field** (as in the two existing rows,
  `docs/ledger.md:11-12`), **not** an inferential hypothesis test. The convention reuses it verbatim and
  introduces no inferential semantics (OD-6).

Because the schema is reused verbatim, a Rung-2 row is **structurally indistinguishable in shape** from the
two existing Rung-1 `regime-v001` rows (`docs/ledger.md:11-12`); only its `claim_ceiling` text and its
same-regime comparison would differ — and both only at a separate later admission gate.

## 2. The verdict rule (no `verdict` column; the rule governs the existing narrative fields)

The existing ledger carries **no separate `verdict` column**; a better/worse verdict is expressed within the
row's existing narrative fields (`hypothesis` / `notes` / `claim_ceiling`), exactly as the existing
`run-0002` row records its comparison (`docs/ledger.md:12`). This convention specifies **when** such a
verdict may be written — it adds no column:

> A `verdict` of better/worse is written **only** for a **same-regime, agent-only** comparison carrying a
> **claim ceiling and an explicit `n`**, and **never across regimes** (`docs/ledger.md:5-8`;
> `06-ledger-report-discipline.md` §4; NFR-5).

The existing `run-0002` vs `run-0001` row demonstrates this shape at **Rung 1**: a *"same-regime agent-only
comparison: candidate `scripted-v001` vs baseline `run-0001`/`random_legal-v001` under `regime-v001`, n=12 …
NO strength claim (ladder Rung 1)"* (`docs/ledger.md:12`). A future Rung-2 row would have the **same
comparison shape** but a `claim_ceiling` advanced past Rung 1 — and that advance is a separate operator
decision (§4), never an automatic consequence of a number moving (`04-rung-2-readiness-criteria.md` §2.5).

Cross-regime verdicts are barred mechanically downstream: two numbers from two different regimes are not
comparable (`analysis/delta_report.py:128-143` `CrossRegimeRefusal`; `docs/claim-ceiling.md:62-65`), and the
evidence-summary validator enforces single-regime inputs (exit 2; `05-generator-validator-shape.md` §2.2).

## 3. Separation of concerns — the architectural heart of Lane C

The load-bearing distinction (`01-prd.md:208-211,276-279`; `02-sdd.md:331-341`):

- The **ledger row is the only future ceiling-bearing verdict artifact.** It carries the verdict, the claim
  ceiling, and the `n` (`docs/ledger.md:3-4`; `docs/claim-ceiling.md:5-6`).
- The **evidence summary (`04-evidence-summary-schema-spec.md`) is supporting confidence evidence only.** It
  carries the K-batch spread and **no ceiling of its own** (parity with `analysis/dispersion_report.py:36-37`,
  *"carries no ceiling of its own … the ledger is the only ceiling-bearing artifact"*).
- A future row would **cite a promoted evidence summary by reference + content hash, without embedding raw
  content** (`06-ledger-report-discipline.md` §6-§7; `docs/operator/turntrace-loop-contract.md:66-68`,
  *"Reference a run by `run_id` / hashes / sanitized metrics / local path — never embed raw contents"*). The
  citation would live in the row's existing `notes` field; it adds no column.

This keeps the **ceiling** (in the sparse, deliberate, append-only ledger) and the **confidence** (in the
sanitized summary) as two separate artifacts — so the ledger stays sparse (`06-ledger-report-discipline.md`
§2) and a summary can be richer without ever carrying a ceiling.

## 4. No row written; `docs/ledger.md` is byte-unchanged

`docs/ledger.md` **stays at its two Rung-1 `regime-v001` rows; this cycle changes nothing in it** (NG3;
`02-sdd.md:343-348`; `01-prd.md:280-281`). This convention is **format/spec only**:

- It **cross-references** `docs/ledger.md` but **does not edit it** — verified byte-unchanged by
  `git diff --exit-code -- docs/ledger.md` (sprint plan §12).
- No `run-v002` / Rung-2 row is written until a **separate later Rung-2 admission gate** — one of the four
  conjunctive operator decisions named in `07-od6-criterion-2-proposal.md` §5 (step 8d).
- Writing a row is a deliberate act tied to a non-empty `claim_ceiling` and its `n`/`games`
  (`06-ledger-report-discipline.md` §3-§4), **never** an automatic side effect.

## 5. Traceability

| Requirement (PRD) | This convention |
|---|---|
| C3-FR-3 row reuses existing columns verbatim, adds none | §1 |
| C3-FR-3 same-regime agent-only verdict rule, explicit `n`, explicit `claim_ceiling`, never cross-regime | §2 |
| C3-FR-3 separation: row carries the verdict, summary carries the confidence | §3 |
| C3-FR-3 row cites summary by reference + hash, no raw embed | §3 |
| C3-FR-3 "no row written; `docs/ledger.md` unchanged" | §4 |

> **Sources:** `docs/ledger.md:1-12` (the only ceiling-bearing artifact; the verbatim 18-column schema; the
> two Rung-1 rows; the `run-0002` vs `run-0001` same-regime agent-only shape); `eval/schemas.md:114-119`
> (`claim_ceiling` required non-empty); `docs/cycles/cycle-002/06-ledger-report-discipline.md` §2-§7
> (sparse-ledger discipline, SP-6 reference-not-embed, no raw content in tracked docs);
> `docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` §2.5 (ceiling advance is a separate operator
> decision); `docs/claim-ceiling.md:5-6,62-65`; `analysis/delta_report.py:128-143` (`CrossRegimeRefusal`);
> `docs/operator/turntrace-loop-contract.md:66-68` (reference-not-embed); `docs/cycles/cycle-003/01-prd.md`
> (C3-FR-3, §8); `docs/cycles/cycle-003/02-sdd.md` (§7). Claim ceiling: **Rung 1 (unchanged).** This
> convention opens no build gate, writes no ledger row, edits no `docs/ledger.md`, advances no ceiling, and
> promotes no value.
