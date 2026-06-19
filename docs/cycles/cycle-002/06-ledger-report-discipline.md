# Ledger / Report-Discipline Note (Cycle-002 / Sprint 00 · S00-T3)

| Field | Value |
|---|---|
| **Type** | Docs-only policy note (codifies existing behavior; authorizes no code; opens no build gate) |
| **Status** | Active standing discipline for Cycle-002 |
| **Date** | 2026-06-18 |
| **Lane / FR** | Lane G · C2-FR-7 |
| **Scope** | Codifies how scale/batch runs relate to the ledger and where their reports live. No code change. |
| **Related** | `docs/ledger.md`, `docs/claim-ceiling.md:5-6`, `docs/operator/turntrace-loop-contract.md` (§7), `docs/cycles/cycle-002/02-sdd.md` (§8, §9.3), `docs/cycles/cycle-002/03-sprint-plan.md` (S00-T3, OD-5, OD-7), ESP-1..ESP-5 / SP-6 |

> Sanitized policy note. No raw traces, card IDs/names, deck lists, hand contents, simulator logs,
> PDFs/CSVs, `deck.csv` rows, run-dir dumps, or Competition Data appear here (CC-1/CC-2, ESP). Runs
> are referenced by `run_id`, sanitized metrics, and artifact names only.

## 1. Non-deliverable scale/batch runs write no ledger row

Scale and batch runs in Cycle-002 are **non-deliverable by default**, and a non-deliverable run
writes **no** ledger row. The run producer's shipped default is no-ledger-by-default for
non-deliverable runs (`eval/run_eval.py:281-288,333-336`; SDD §8.1): a bare invocation writes its
local `summary.csv` and sealed run dir only — it does not append to any ledger
(`docs/cycles/cycle-002/03-sprint-plan.md:159-161`). This is existing behavior; this note codifies
it, it does not change it.

## 2. The ledger does not grow one row per batch

The experiment ledger does **not** grow a row per batch. Running K repeated same-regime batches
(2K sealed run dirs) appends **zero** rows by default. The ledger is append-only and per-row
ceiling-bearing; flooding it with one row per batch would dilute exactly the artifact that is meant
to stay sparse and deliberate (`docs/ledger.md:1-8`; `docs/cycles/cycle-002/03-sprint-plan.md:376`).

## 3. Only explicitly designated deliverable runs may write ledger rows

A ledger row is written **only** when an operator explicitly designates a run as a deliverable. At
most one designated deliverable run per regime is contemplated (OD-5, ratified —
`docs/cycles/cycle-002/03-sprint-plan.md:560`), and none is in Cycle-002's current scope. Writing a
row is a deliberate act tied to a non-empty `claim_ceiling` and its sample size `n`/`games`
(`docs/ledger.md:5-9`), never an automatic side effect of a batch finishing.

## 4. `docs/ledger.md` remains the only ceiling-bearing artifact

`docs/ledger.md` remains **the only ceiling-bearing artifact** (`docs/claim-ceiling.md:5-6`).
Per-match records, `summary.csv`, dispersion reports, budget notes, and every other surface carry
**no** ceiling of their own. A `verdict` of better/worse may be written only for a same-regime,
agent-only comparison with a ceiling and an `n`, and never across regimes (`docs/ledger.md:5-8`;
NFR-5).

## 5. Full run dirs, budget notes, and dispersion reports stay local/git-ignored by default

By default, the following stay **local / git-ignored** and are never committed (ESP-1; SDD §4.1;
OD-7 ratified — `docs/cycles/cycle-002/03-sprint-plan.md:562`):

- **Full run dirs** — the `runs/<run_id>/` trees (records, traces, manifest, hashes). Only
  `runs/.gitkeep` is tracked.
- **Budget notes** — the sanitized dry-run time/size note from a future Sprint 01.
- **Dispersion reports** — the cross-run descriptive roll-up from a future Sprint 02.

A run is referenced by `run_id`, hashes, sanitized metrics, and local path — its raw contents are
never embedded in a tracked artifact (`docs/operator/turntrace-loop-contract.md:66-68`).

## 6. Tracked sanitized cycle-close summaries require explicit SP-6 relaxation

Promoting **any** sanitized summary from local/ignored to tracked status requires an **explicit
operator SP-6 relaxation** at cycle close (a Stretch item, not the default —
`docs/cycles/cycle-002/03-sprint-plan.md:489-491`). Even under an SP-6 relaxation, a promoted
summary carries **counts, aggregates, and dispersion only — never raw rows**.

## 7. No raw run content enters tracked docs

No raw run content enters any tracked document. Tracked artifacts hold sanitized summaries, ledger
rows, claim ceilings, failure-mode notes, planning docs, and operator-approved artifacts only
(`docs/operator/turntrace-loop-contract.md:66-68`). Raw traces, card IDs/names, deck lists, hand
contents, simulator logs, PDFs/CSVs, `deck.csv` rows, and run-dir dumps are **never** committed
(CC-1/CC-2, ESP), and the staging guard `eval/hygiene_check.py` mechanically refuses the paths that
carry them.
