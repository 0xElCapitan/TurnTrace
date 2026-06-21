# Cycle-008 — `NNa-` Document Numbering Convention (S04.1)

**Date:** 2026-06-21
**Cycle / sprint:** Cycle-008, Sprint **S04 — Governance & convention docs** (deliverable S04.1).
**Type:** governance / convention — formalize the per-cycle document numbering already in use, so future
cycles stop improvising filenames around the gates.
**Status:** Convention written. **This artifact carries no claim ceiling of its own and freezes nothing.**

> **Sanitization posture.** This is a governance/convention doc. It embeds **no** raw traces, simulator
> logs, deck lists, card IDs/names, Pokémon Elements, Competition Data, Daily-Top-Episodes, Kaggle
> episode data, Discord/peer screenshots, run-dir dumps, PDFs/CSVs, `deck.csv`, `cg/`, raw evidence rows,
> dispersion/band/win-rate values, or any inferential statistic. **No numeric governance margin `M` is
> chosen or stated** here. No forbidden agent word (*strong / competitive / optimal / calibrated /
> complete*) is used to describe agent evidence. The doc names filenames and sanitized artifact ids only.

> **Cycle-008 posture (binding for every S04 doc).** Cycle-008 does **not**: attempt Rung 3; select a
> Rung-3 target; select a candidate; freeze a numeric comparison budget; freeze `K`/`n`; freeze a regime
> id; freeze a feature family; create SP-6; write or modify a ledger row; or advance the claim ceiling.
> **The current standing claim ceiling remains Rung 2** ([`../../claim-ceiling.md`](../../claim-ceiling.md)),
> and [`../../ledger.md`](../../ledger.md) remains the **only** ceiling-bearing artifact. This convention
> doc asserts no ceiling.

---

## 1. What `NNa-` numbering is for

A cycle's `docs/cycles/cycle-NNN/` directory accumulates artifacts across the whole pipeline (PRD, SDD,
sprint plan, then per-sprint preflight / implementation / verdict / closeout artifacts). The filename
prefix is the artifact's **stable handle** — it is what other docs, ledger rows, and reviews cite. The
convention has three parts, each answering a different question:

| Part | Example | Answers |
|---|---|---|
| `NN-` (zero-padded ordinal) | `07-` | *In what order was this artifact added to the cycle?* |
| `-sXX-` (optional sprint infix) | `-s03-` | *Which sprint produced it?* (omitted for cycle-level docs) |
| `a`/`b`/`c` … (optional letter suffix) | `06a-` | *Is this a companion grouped under an existing ordinal?* |

`NNa-` (the letter-suffix form) exists so that **a companion artifact can be filed next to its base
artifact without consuming the next integer and without renaming anything already accepted**. It is an
*insertion / grouping* marker, not a new top-level step.

The precedent this convention formalizes is already in the tree:
[`../cycle-007/06a-sp6-promoted-summary.md`](../cycle-007/06a-sp6-promoted-summary.md) was filed as a
companion to the base ordinal `06`
([`../cycle-007/06-verdict-application.md`](../cycle-007/06-verdict-application.md)) — the promoted
summary belongs *with* the verdict it derives from, so it took `06a-`, not `07-`.

## 2. When `NNa-` is used (and when it is not)

**Use `NNa-` when:** a single base artifact (or a single sprint) produces more than one tracked doc and
the extra docs are companions that belong grouped under one ordinal. Letter the companions `a`, `b`,
`c`, … in authoring order under the shared base `NN`.

**Do not use `NNa-` for:** a genuinely new pipeline step. A new step that stands on its own takes the
**next integer** (`NN+1`), exactly as `01-prd → 02-sdd → 03-sprint-plan` and the per-sprint reports
`05-s01-… → 06-s02-… → 07-s03-…` already do.

**This cycle's S04 application (illustrating the convention).** Sprint S04 produced five tracked docs.
They are filed under one base ordinal `08`:

| Filename | Role |
|---|---|
| [`08-s04-implementation-report.md`](08-s04-implementation-report.md) | base `08` — the S04 sprint report (continues the `05-s01`/`06-s02`/`07-s03` report series) and indexes the four companions |
| `08a-numbering-convention.md` (this file) | companion — the convention doc whose own filename follows the convention it formalizes |
| [`08b-ledger-metric-column-convention.md`](08b-ledger-metric-column-convention.md) | companion — ledger metric-column "see cited summary" convention |
| [`08c-blocked-family-map.md`](08c-blocked-family-map.md) | companion — blocked-family map |
| [`08d-rung3-form-only-semantics.md`](08d-rung3-form-only-semantics.md) | companion — form-only Rung-3 ladder semantics |

A reader scanning the directory sees `08*` and knows: *that is all of S04.* The four conventions did not
each grab `08`, `09`, `10`, `11` — which would have scattered one sprint's output across four ordinals
and pushed the next sprint's report to `12`.

## 3. How it avoids ambiguity between three numbering axes

Three numbering axes coexist in a cycle directory. They are easy to conflate; the convention keeps them
separate:

1. **Cycle-document numbering** — the `NN-` ordinal. It is a **per-cycle monotonic document counter**,
   nothing more. It does **not** encode the sprint, the rung, or any semantic. `01-prd.md`,
   `02-sdd.md`, `03-sprint-plan.md` are ordinals 1–3 of *this cycle's* document stream.
2. **Sprint numbering** — the `sXX` infix (`s00`…`s05`). It binds an artifact to the sprint that
   produced it. It is **independent of `NN`**: sprint S03's report is the *seventh* document of the
   cycle, hence `07-s03-…`.
3. **Report numbering** — implementation reports are a *family* within the `NN-` stream, named
   `NN-sXX-implementation-report.md`. They are not a separate counter; they share the one `NN-` stream
   with every other doc.

The load-bearing rule: **`NN` is a document counter, not a sprint id.** Whenever you need to know "which
sprint," read the `-sXX-` infix, never the leading integer.

## 4. How future docs avoid confusing `04-s00-…` / `07-s03-…` filenames

The two real examples that *look* confusing are
[`04-s00-preflight.md`](04-s00-preflight.md) (ordinal 04, sprint **00**) and
[`07-s03-implementation-report.md`](07-s03-implementation-report.md) (ordinal 07, sprint **03**). The
mismatch (`04`≠`00`, `07`≠`03`) is **correct and intended**, not a bug: the leading number is the
document ordinal, and the planning docs (`01`–`03`) consumed the first three ordinals before any sprint
report existed, so sprint S00's report is the *fourth* document. Future authors should:

- **Read `NN` and `sXX` as orthogonal.** Do not "fix" `07-s03-…` to `03-s03-…`; that would collide with
  `03-sprint-plan.md` and destroy the stable ordinal handle.
- **Always carry the `-sXX-` infix on sprint artifacts**, so the sprint binding is explicit in the
  filename and never has to be inferred from the ordinal.
- **Group multi-doc sprints with `NNa-`** (§2) instead of spending several integers on one sprint —
  this is what keeps the `NN`/`sXX` gap from widening unnecessarily.
- **Keep cycle-level docs (`01-prd`, `02-sdd`, `03-sprint-plan`) infix-free**, so the absence of `-sXX-`
  itself signals "cycle-level, not a sprint artifact."

## 5. Preserving traceability without renaming accepted artifacts

Filenames are citation handles: the ledger, the claim ceiling, prior reports, and reviews all cite docs
by path. **Renaming an already-accepted artifact silently breaks every citation that points at it.**
Therefore:

- **Never renumber or rename an accepted/committed artifact** to "tidy" the sequence. Accepted ordinals
  are frozen. If a gap or an out-of-order insertion is needed, use the **next integer** (for a new step)
  or a **letter suffix** (for a companion) — both are additive and break nothing.
- **An insertion between accepted ordinals uses `NNa-`,** filed under the lower neighbour's ordinal,
  rather than shifting every later file up by one.
- **Renaming is allowed only under explicit operator authorization** (the same gate that governs any
  edit to accepted history), and when it happens, every inbound citation is updated in the same change.
- **The ledger and claim-ceiling artifacts are never renamed by a convention change.** They are
  byte-stable governance anchors (this cycle: ledger `7da7e9a8…`, ceiling `3d99759b…`); a numbering
  convention touches neither.

## 6. Sources / traceability

- **`NNa-` precedent in the tree:** [`../cycle-007/06a-sp6-promoted-summary.md`](../cycle-007/06a-sp6-promoted-summary.md)
  (companion to [`../cycle-007/06-verdict-application.md`](../cycle-007/06-verdict-application.md)).
- **S04 deliverable + "the doc's own filename follows the convention it formalizes":**
  [`03-sprint-plan.md`](03-sprint-plan.md) (S04 Deliverables; S04.1).
- **Carry-forward 1 (numbering convention) / C8-FR-5.1:** [`01-prd.md`](01-prd.md);
  [`02-sdd.md`](02-sdd.md) §6.1.
- **Ceiling posture (no doc carries a ceiling; ledger is the only ceiling-bearing artifact):**
  [`../../claim-ceiling.md`](../../claim-ceiling.md); [`../../ledger.md`](../../ledger.md).
