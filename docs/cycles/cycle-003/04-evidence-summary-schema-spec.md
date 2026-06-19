# Evidence-Summary Schema Spec (Cycle-003 / Sprint 00 · S00-T1)

| Field | Value |
|---|---|
| **Type** | Docs-only field-list design authority (authorizes no code; opens no build gate; creates no schema file) |
| **Status** | Authored — Cycle-003 Sprint 00 deliverable (S00-T1); design authority for a *later* build cycle |
| **Date** | 2026-06-19 |
| **Lane / FR** | Lane A · C3-FR-1 · S00-T1 |
| **Scope** | Specifies the safe + forbidden field sets, the JSON-first shape, and the read-surface/hygiene parity for a sanitized K-batch evidence summary. It specifies the schema; it creates no machine-readable schema FILE and promotes no value. |
| **Related** | `eval/schemas.md` (placement precedent: spec pairs with a validator), `analysis/dispersion_report.py` (the read surface + descriptive vocabulary), `analysis/aggregate.py` (per-run sanitized stats), `eval/hygiene_check.py` (sanitization staging gate / parity target), `docs/ledger.md` (the only ceiling-bearing artifact), `docs/claim-ceiling.md`, `docs/cycles/cycle-003/01-prd.md` (C3-FR-1, §7), `docs/cycles/cycle-003/02-sdd.md` (§3, §4), `docs/cycles/cycle-003/05-generator-validator-shape.md` (the validator that must agree with this spec) |

> Sanitized note. No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, or Competition Data appear here (CC-1/CC-2, ESP).
> **No dispersion metric values appear here** — values stay local/gitignored; this spec carries field
> *names*, types, and placeholders only. Runs are referenced by `run_id`, content hashes, sanitized metric
> *names*, claim ceilings, and local path/status only. The forbidden agent claim words (*strong /
> competitive / optimal / calibrated / complete*) appear only as negated/forbidden language.

> **Boundary banner (binding).** This document opens **no build gate** and is **not** an implementation
> authorization. It is the tracked *field-list design authority* for a sanitized K-batch evidence summary —
> the plain spec that a future validator (`05-generator-validator-shape.md`) must agree with, mirroring
> `eval/schemas.md:1-4`. It **creates no machine-readable schema file**, **builds no generator/validator
> code**, and **promotes no dispersion value** to tracked status. The schema *file* and the
> generator/validator *code* are a separate later build cycle behind a fresh operator OA-2 gate
> (`02-sdd.md:170-171`; OD-C3-6). The claim ceiling stays **Rung 1**.

## 1. Purpose and relationship to the loop

The confidence evidence behind any future Rung-2 verdict — the cross-batch dispersion of sanitized aggregate
metrics — currently lives **only** in local/gitignored files; the tracked Cycle-002 closeout is
narrative-only and carries no values (`01-prd.md:73-76`). This spec defines the **shape a sanitized K-batch
evidence summary must take** so that, in a later cycle, such confidence evidence *could* be generated and
validated without ever leaking a forbidden field — while this cycle promotes nothing.

The summary is **supporting confidence evidence only**. It carries **no ceiling of its own**; the experiment
ledger (`docs/ledger.md`) remains the only ceiling-bearing artifact (`docs/claim-ceiling.md:5-6`;
`analysis/dispersion_report.py:36-37`). The separation of the ceiling-bearing ledger row from the
confidence-bearing summary is specified in `06-rung-2-ledger-convention.md` §3.

This spec follows the existing project convention established by `eval/schemas.md`: a **tracked plain
field-list is the design authority, and the machine-checkable form pairs with it**
(`eval/schemas.md:1-4` — *"The machine-checkable form lives in `eval/validate.py`; this doc and that
validator must agree"*). The evidence-summary schema mirrors that split: this doc is the authority; the
later validator (`05-generator-validator-shape.md`) is the machine-checkable form, and the two must agree.

## 2. Safe fields (the full allow-list)

The safe surface is **exactly** the descriptive surface already produced by `analysis/dispersion_report.py`
plus identity/provenance fields (`01-prd.md:180-189`; `02-sdd.md:184-206`). The schema **adds no new metric
and no new statistic** (`01-prd.md:259-260`). It is an **allow-list**: a field outside this set is rejected
by the validator (fail-closed; `05-generator-validator-shape.md` §2.1).

### 2.1 Identity and provenance fields

| Field | Type | Source / authority | Notes |
|---|---|---|---|
| `regime_id` | string | each run dir `manifest.json` (`dispersion_report.py:126-141`) | single value; the single-regime guard guarantees one regime per summary |
| `n` | int \| list[int] | per-run `n_matches` (`aggregate.py:76`) | the sample size; explicit, always present (a list only if runs differ, mirroring `dispersion_report.py:179`) |
| `K` | int | count of runs per agent (`dispersion_report.py:184`) | the batch count (e.g. K ≥ 20 same-regime batches) |
| `agent_id` / `agent_version` | string | manifest authority + per-run stats (`dispersion_report.py:153,173`) | identity only; never a quality descriptor |
| `run_id` list | list[string] | `dispersion_report.py:175` | provenance; references runs, embeds **no** run content |
| per-run / batch content `hashes` | map[string→string] | run-dir `hashes.txt` / `manifest.json` (`eval/schemas.md:106-112`) | integrity stamp; SHA-256 strings only, **no raw content** |
| `mode` | string (`= unseeded`) | reproducibility posture (`05-reproducibility-reality.md` §1) | always `unseeded` for this loop |
| unseeded-process caveat | string | `dispersion_report.py:226-231,251-254` | the caveat string travels with every summary (NFR-6); see §2.4 |
| Rung-1 footer | string | `dispersion_report.py:233-239` | states the summary "carries no ceiling of its own"; see §2.4 |

### 2.2 Per-metric descriptive statistics

For each dispersed metric, the summary carries **exactly** the seven descriptive statistics produced by
`analysis/dispersion_report.py:76` (`STAT_COLUMNS`) — and **nothing else** (OD-6;
`07-operator-decision-register.md` §1 OD-6):

`count` · `min` · `max` · `range` (the pair `[min, max]`) · `mean` · `median` · `spread` (`max − min`)

These are pure arithmetic over the K per-run metric values (`dispersion_report.py:94-114`). **No sample
standard deviation, no variance, and no inferential statistic** is carried — their absence is structural in
the existing report and is preserved as a forbidden-field rule here (§3; OD-6).

### 2.3 Dispersed metrics (names only)

The metrics dispersed are **exactly** `analysis/dispersion_report.py:69-72` (`DISPERSION_METRICS`):

`win_rate` · `illegal_action_rate` · `timeout_rate` · `error_rate` · `avg_turns` · `avg_wall_clock_ms`

`avg_wall_clock_ms` is environment-sensitive throughput: it is **reported but is never a comparison metric**
(`dispersion_report.py:67-68`). The schema carries these as sanitized metric **names** with their seven
descriptive statistics; the underlying dispersion **values** stay local/gitignored and are not promoted by
this cycle (NG4).

### 2.4 Two mandatory framing strings

Every conforming summary MUST carry both framing strings verbatim-in-intent from the existing report
(`dispersion_report.py:226-239,251-254`):

- **Unseeded-process caveat** — that runs are unseeded (`seed_controlled=false`; the local simulator API
  exposes no RNG seed), so the observed dispersion reflects the **whole unseeded process** (agent behaviour
  together with uncontrolled simulator RNG) and is **not** an isolated agent-only quantity
  (`05-reproducibility-reality.md` §3; `docs/claim-ceiling.md:42-52`).
- **Rung-1 footer** — that the summary is a descriptive, observed-spread diagnostic at **Rung 1**, makes
  **no** gameplay-strength claim and **no** inferential claim, and **carries no ceiling of its own**; the
  experiment ledger (`docs/ledger.md`) is the only ceiling-bearing artifact, and a `regime-v002` number is
  never compared to a `regime-v001` ledger row (NFR-5).

## 3. Forbidden fields (enumerated, validator-enforced)

The forbidden set is **enumerated and intended for mechanical validator enforcement**, not mere
documentation (`01-prd.md:262-263`; `02-sdd.md:208-221`). A summary carrying any of these **fails validation
and can never be promoted** (`05-generator-validator-shape.md` §2). Because the safe set (§2) is an
allow-list, *anything not in §2 is already rejected*; the table below names the classes the validator must
recognize explicitly so that a near-miss leak is refused with a clear reason.

| Forbidden class | Examples | Rule basis |
|---|---|---|
| Raw decision rows / trace bodies | per-decision sidecar contents, decision-trace JSONL bodies | CC-1/CC-2; `dispersion_report.py:16-19` (never opens sidecars) |
| Competition Data | card IDs/names, deck lists, hand contents, simulator logs | CC-1/CC-2; `hygiene_check.py:36-44` |
| File-form Competition Data | PDFs/CSVs, `deck.csv` rows, run-dir dumps | `hygiene_check.py:39-44` |
| Pokémon Elements | type matchups, deck recipes, names | ESP; `eval/schemas.md:13-15` |
| Inferential statistics | `std-dev`, `variance`, confidence intervals, p-values, "significance", hypothesis tests, inferential error bars | OD-6 (`07-operator-decision-register.md` §2); `dispersion_report.py:31-34` |
| Cross-regime fields / comparisons | any field comparing two `regime_id`s; any `regime-v002`-vs-`regime-v001` figure | NFR-5; `frozen/regimes/regime-v001.json:9`; `docs/claim-ceiling.md:62-65` |
| Affirmative forbidden agent words | *strong / competitive / optimal / calibrated / complete* used as affirmative agent-quality descriptors | `docs/claim-ceiling.md:54-59` |

> The `hypothesis` token is **not** in either set above as an inferential term: where it appears in the
> ledger row schema (`06-rung-2-ledger-convention.md` §2) it is the experiment-hypothesis **text field**,
> not an inferential hypothesis test. The evidence summary itself carries no `hypothesis` field.

## 4. JSON-first shape

The summary's machine-readable JSON form is **primary**; any human-readable rendering is **derived, never
the source of truth** (`01-prd.md:264-265`; `02-sdd.md:231-239`). This mirrors `dispersion_report.py`'s
existing `render_json` (machine-readable; `dispersion_report.py:243-255`) versus `render` (Markdown;
`dispersion_report.py:197-240`) split. JSON-first is an **existing-pattern choice** that keeps the summary
consumable by a future automated reader (`08-funsearch-forward-compat.md`); it is **not** a FunSearch
coupling, and **no FunSearch dependency, interface, or scaffold is introduced** (NG10).

### 4.1 Illustrative shape — field names and placeholders only (no values)

The following is a **schema example carrying no dispersion values** — every leaf is a type placeholder, not
a measured number (`docs/cycles/cycle-003/03-sprint-plan.md:471-473`; `01-prd.md:314-316`). It shows the
JSON-first structure only.

```jsonc
{
  "regime_id": "<regime-vNNN>",
  "n": "<int | [int, ...]>",
  "K": "<int>",
  "mode": "unseeded",
  "agents": [
    {
      "agent_id": "<string>",
      "agent_version": "<string>",
      "K": "<int>",
      "run_ids": ["<run_id>", "..."],
      "metrics": {
        "win_rate":            { "count": "<int>", "min": "<num>", "max": "<num>", "range": ["<num>", "<num>"], "mean": "<num>", "median": "<num>", "spread": "<num>" },
        "illegal_action_rate": { "count": "<int>", "min": "<num>", "max": "<num>", "range": ["<num>", "<num>"], "mean": "<num>", "median": "<num>", "spread": "<num>" },
        "timeout_rate":        { "...": "(same seven descriptive statistics)" },
        "error_rate":          { "...": "(same seven descriptive statistics)" },
        "avg_turns":           { "...": "(same seven descriptive statistics)" },
        "avg_wall_clock_ms":   { "...": "(reported; never a comparison metric)" }
      }
    }
  ],
  "hashes": { "<run_id>": "<sha256>", "...": "..." },
  "unseeded_caveat": "<the §2.4 caveat string>",
  "claim_ceiling": "<the §2.4 Rung-1 footer string; this summary carries no ceiling of its own>"
}
```

The allowed *narrative* form a future summary may render is equally value-free here — e.g. *"under
`regime-vNNN` at n=N across K batches, the observed `<metric>` ranged from X to Y (mean Z)"* — stated as a
**form** with symbolic placeholders, never instantiated with a measured value in this cycle
(`01-prd.md:314-316`; `dispersion_report.py:220-223`).

## 5. Sanitization parity and read surface

- **Read surface (identical to `dispersion_report.py`).** A future generator that emits a conforming
  summary reads **`manifest.json` + `match_results/*` only, never the per-decision sidecars**
  (`dispersion_report.py:11-19`; `01-prd.md:188-189`). The schema therefore can only be populated from
  already-sanitized aggregate stats (`analysis/aggregate.py:75-89`).
- **Hygiene parity (superset of `eval/hygiene_check.py`).** The validator that enforces this schema reaches
  **sanitization parity with `eval/hygiene_check.py`** (`hygiene_check.py:35-45`) and adds the
  value-bearing, inferential, cross-regime, and forbidden-word checks that a path-based staging gate cannot
  express (`02-sdd.md:223-229`; detailed in `05-generator-validator-shape.md` §3). `eval/hygiene_check.py`
  guards the *staging boundary* (which paths may be committed); the validator guards the *summary content*
  (what a summary may contain) before it could ever be a promotion candidate.

## 6. What this spec deliberately does NOT do

- **No machine-readable schema file.** This cycle authors the field-list authority only; the
  `analysis/evidence_summary_schema.json` (or in-module constant) is created **only in the later build
  cycle** (`02-sdd.md:170`; NG5). Creating a `.json` schema file here → HALT (AC-S00-1, AC-X5).
- **No values promoted.** Only the safe *shape* is specified; dispersion **values** stay local/gitignored.
  Promoting any value to tracked status requires a separate later operator SP-6 decision (NG4;
  `02-sdd.md:410-413`).
- **No inferential statistic; OD-6 unrelaxed.** The seven descriptive statistics are the entire statistical
  surface; inferential statistics are enumerated as forbidden (§3), not computed or reported (OD-6).
- **No cross-regime field.** Every summary is single-regime by construction (§2.1, `regime_id` single value;
  the generator/validator single-regime guard is specified in `05-generator-validator-shape.md` §2.2).

## 7. Traceability

| Requirement (PRD) | This spec |
|---|---|
| C3-FR-1 safe fields enumerated | §2 (identity/provenance, seven statistics, metric names, two framing strings) |
| C3-FR-1 forbidden fields enumerated + validator-enforced | §3 (seven forbidden classes, allow-list fail-closed) |
| C3-FR-1 JSON-first | §4 (machine-readable primary; value-free example) |
| C3-FR-1 read-surface + hygiene parity | §5 (manifest + `match_results/*` only; superset parity) |
| C3-FR-1 "specifies the schema; creates no file, promotes no value" | §6 (explicit non-actions) |

> **Sources:** `analysis/dispersion_report.py` (read surface, `DISPERSION_METRICS`, `STAT_COLUMNS`,
> framing strings, JSON-first split); `analysis/aggregate.py:75-89` (per-run sanitized stats);
> `eval/hygiene_check.py:35-45` (parity target); `eval/schemas.md:1-4,99-119` (placement precedent + manifest
> /hashes fields); `docs/ledger.md:1-9` (only ceiling-bearing artifact); `docs/claim-ceiling.md:5-6,42-65`;
> `docs/cycles/cycle-002/05-reproducibility-reality.md` §3 (unseeded process); `docs/cycles/cycle-002/07-operator-decision-register.md`
> §1-§2 (OD-6); `docs/cycles/cycle-003/01-prd.md` (C3-FR-1, §7); `docs/cycles/cycle-003/02-sdd.md` (§3, §4).
> Claim ceiling: **Rung 1 (unchanged).** This spec opens no build gate, creates no schema file, builds no
> code, writes no ledger row, and promotes no value.
