# Generator / Validator Shape Spec (Cycle-003 / Sprint 00 · S00-T2)

| Field | Value |
|---|---|
| **Type** | Docs-only shape spec (authorizes no code; opens no build gate; builds no generator/validator) |
| **Status** | Authored — Cycle-003 Sprint 00 deliverable (S00-T2); shape authority for a *later* build cycle |
| **Date** | 2026-06-19 |
| **Lane / FR** | Lane B · C3-FR-2 · S00-T2 |
| **Scope** | Specifies the *shape* (inputs, outputs, import boundary, refusals, exit codes, hygiene parity) of a future offline `analysis/`-class evidence-summary generator and its validator. It specifies the shape; it builds no code. |
| **Related** | `04-evidence-summary-schema-spec.md` (the schema this shape produces/enforces), `analysis/dispersion_report.py` (read surface, import boundary, exit-code discipline, single-regime guard), `analysis/delta_report.py` (`CrossRegimeRefusal`), `analysis/aggregate.py` (`aggregate_run`), `eval/hygiene_check.py` (parity target), `eval/schemas.md` (spec-pairs-with-validator precedent), `docs/cycles/cycle-003/01-prd.md` (C3-FR-2), `docs/cycles/cycle-003/02-sdd.md` (§4.3, §5, §6) |

> Sanitized note. No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, or Competition Data appear here (CC-1/CC-2, ESP).
> **No dispersion metric values appear here.** Runs are referenced by `run_id`, content hashes, sanitized
> metric *names*, claim ceilings, and local path/status only. The forbidden agent claim words (*strong /
> competitive / optimal / calibrated / complete*) appear only as negated/forbidden language.

> **Boundary banner (binding).** This document opens **no build gate** and is **not** an implementation
> authorization. It specifies the *shape* of a future offline generator + validator — inputs, outputs,
> import boundary, refusals, exit codes, hygiene parity — so the later build cycle can implement them
> against a settled design. It **writes no `analysis/` code**, **creates no schema file**, and **promotes no
> value**. The generator/validator **code** is a separate later build cycle behind a fresh operator OA-2 gate
> (`02-sdd.md:171`, §5-§6; OD-C3-6). The claim ceiling stays **Rung 1**.

## 1. Generator shape

The generator is an offline `analysis/`-class component (a future sibling of `dispersion_report.py` /
`delta_report.py` / `aggregate.py`). Its shape (`01-prd.md:191-199`; `02-sdd.md:243-267`):

1. **Reads** existing local sealed run dirs — `manifest.json` + `match_results/*` via
   `aggregate.aggregate_run` — and the local dispersion output, **exactly the `dispersion_report.py` read
   surface** (`dispersion_report.py:11-19`). It reads only **existing** local outputs; it runs no eval and
   creates no run dir (NG12).
2. **Emits** a summary conforming to the `04-evidence-summary-schema-spec.md` safe-field set, in the
   JSON-first form of that spec §4.
3. **Never opens** the per-decision sidecars — *structurally*, by containing no reference to that directory,
   mirroring `dispersion_report.py:16-19` (*"The module contains no reference to that sidecar directory, so
   it cannot read raw decision rows"*).
4. **Reuses** `aggregate.aggregate_run` and the descriptive-stat helpers (`dispersion_report.py:63,147`,
   `descriptive_stats` `:94-114`) rather than recomputing them — inheriting the proven sanitized surface and
   the seven-statistic descriptive boundary, so no new metric or statistic can enter through the generator.
5. **Writes local by default.** The generator writes to a **local/git-ignored path by default**, mirroring
   `dispersion_report.py --out` (`dispersion_report.py:268-270`, *"local/git-ignored by default"*). Promotion
   to tracked status is a separate later SP-6 operator decision (`06-rung-2-ledger-convention.md` §4;
   `02-sdd.md:392`), **never a generator side effect**.

## 2. Validator shape

The validator is the mechanical barrier that makes the `04-evidence-summary-schema-spec.md` forbidden-field
set **enforceable rather than advisory** (`01-prd.md:191-199,262-263`; `02-sdd.md:269-311`). It runs **before
any summary could ever be promoted**.

### 2.1 Allow-list, fail-closed

The validator accepts **only** the §2 safe-field set of `04-evidence-summary-schema-spec.md` (an
**allow-list**, not a deny-list — unknown fields **fail closed**). It additionally rejects, with a clear
reason per class (`02-sdd.md:275-283`):

- any field outside the safe allow-list;
- any **inferential statistic** name or value (`std-dev`, `variance`, confidence interval, p-value,
  "significance", hypothesis test, inferential error bar) — OD-6;
- any **Competition-Data / Pokémon-Element** token (reaching parity with `eval/hygiene_check.py`);
- any **cross-regime** field or comparison (NFR-5);
- any **affirmative forbidden agent word** (*strong / competitive / optimal / calibrated / complete*).

### 2.2 Single-regime guard (mirrors existing exit-code discipline)

The generator and validator **hard-refuse mixed `regime_id` inputs — exit 2** (`01-prd.md:198`;
`02-sdd.md:285-292`). This mirrors `dispersion_report.py`'s `MixedRegimeRefusal`
(`dispersion_report.py:79-80,133-140,275-277`, *"refusing to disperse across regimes … exit 2"*) and
`delta_report.py`'s `CrossRegimeRefusal` (`delta_report.py:128-143`). The `regime_id` authority is each run
dir's **`manifest.json`, read first, before any aggregation** (`dispersion_report.py:126-141`); **no logic
keys off the run-id string** in place of the manifest (`07-operator-decision-register.md` §2, *"ID
authority: `manifest.json`"*). A `regime-v002` number can therefore never be aggregated beside a
`regime-v001` number.

### 2.3 Import boundary

The generator/validator is **`analysis/`-class**: it imports run-dir artifacts and intra-zone helpers only —
**no `cabt`, no `sim/`, no `agents/runtime/`, no `eval/` import** (the standing offline/runtime separation;
`dispersion_report.py:44-46`). It is **stdlib-only** (`json`, `statistics`, `pathlib`), exactly as
`dispersion_report.py` is (`dispersion_report.py:52-58`): the read surface is JSON + arithmetic, which the
stdlib covers. The SDD **finds no justification to deviate** (`02-sdd.md:257-260`); any future dependency is
a separate operator decision, not assumed here.

### 2.4 Exit-code contract (design level)

Mirroring `dispersion_report.py:48-49` and `delta_report.py` (`02-sdd.md:294-303`):

| Exit | Meaning |
|---|---|
| `0` | summary validates clean (schema-conforming, sanitized, single-regime) |
| `1` | input failure (missing manifest, malformed run dir) |
| `2` | **mixed-regime refusal** (the hard single-regime guard of §2.2) |
| (leak) | a forbidden field/value/word found → **non-zero, fail-closed** — the build cycle fixes the exact code; the contract is **never exit 0 on a leak** |

### 2.5 Hygiene parity (superset of `eval/hygiene_check.py`)

The validator's sanitization checks are a **superset-parity** with `eval/hygiene_check.py`: it refuses the
same carrying paths/tokens (`hygiene_check.py:35-45`) and additionally enforces the value-bearing,
inferential, cross-regime, and forbidden-word checks that a path-based staging gate cannot express
(`02-sdd.md:305-311`). The two gates **compose**: `eval/hygiene_check.py` guards the *staging boundary* (what
may be committed); the validator guards the *summary content* (what a summary may contain) before it is ever
a promotion candidate.

## 3. Why the validator is a superset, not a duplicate

`eval/hygiene_check.py` is a **path-based** staging guard: it refuses paths such as `cg/`, `deck.csv`,
`*.pdf`, `grimoires/loa/context/`, and `runs/<run_id>/…` (`hygiene_check.py:35-45`), and exits `0`/`1`
(`hygiene_check.py:22`). It cannot inspect *content* — it cannot tell that a JSON field carries an
inferential statistic, a promoted dispersion value, a cross-regime comparison, or an affirmative forbidden
word. The evidence-summary validator closes exactly that gap: it is **content-aware** over the summary's
fields, while remaining **parity-or-stricter** on the paths/tokens the staging gate already refuses
(`02-sdd.md:305-311`). Neither replaces the other.

## 4. What this spec deliberately does NOT do

- **No code.** No `analysis/evidence_summary.py`, no validator module, no schema file is written; the build
  is a later cycle behind a fresh OA-2 (NG5; `02-sdd.md:171`). Writing any `analysis/` code here → HALT
  (AC-S00-2, AC-X5).
- **No eval run / no new run dir.** The generator reads *existing* local outputs only; this cycle runs no
  eval, no K=50 top-up, no batch (NG12).
- **No value promotion.** Local-by-default output; tracking is a separate later SP-6 operator decision (NG4).
- **No dependency added.** stdlib-only; any dependency proposal is a separate operator decision
  (`02-sdd.md:257-260`).

## 5. Traceability

| Requirement (PRD) | This spec |
|---|---|
| C3-FR-2 generator reads existing local outputs, emits schema-conforming summary, never opens sidecars | §1 |
| C3-FR-2 validator rejects forbidden content (allow-list, fail-closed) | §2.1 |
| C3-FR-2 import boundary (`analysis/`-class, stdlib-only) | §2.3 |
| C3-FR-2 single-regime guard (exit 2) | §2.2 |
| C3-FR-2 exit-code contract | §2.4 |
| C3-FR-2 hygiene parity (superset) | §2.5, §3 |
| C3-FR-2 "specifies the shape; builds no code" | §4 |

> **Sources:** `analysis/dispersion_report.py` (read surface `:11-19`; import boundary `:44-46`; exit codes
> `:48-49`; `MixedRegimeRefusal` `:79-80,133-140,275-277`; local-by-default `--out` `:268-270`; descriptive
> helpers `:94-114`); `analysis/delta_report.py:128-143` (`CrossRegimeRefusal`); `analysis/aggregate.py:75-89`
> (`aggregate_run`); `eval/hygiene_check.py:22,35-45` (path-based staging gate / parity target);
> `eval/schemas.md:1-4` (spec-pairs-with-validator precedent); `docs/cycles/cycle-002/07-operator-decision-register.md`
> §2 (ID authority, OD-6); `docs/cycles/cycle-003/01-prd.md` (C3-FR-2); `docs/cycles/cycle-003/02-sdd.md`
> (§4.3, §5, §6). Claim ceiling: **Rung 1 (unchanged).** This spec opens no build gate, builds no code,
> creates no schema file, writes no ledger row, and promotes no value.
