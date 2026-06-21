# Cycle-008 — Ledger Metric-Column "See Cited Summary" Convention (S04.2)

**Date:** 2026-06-21
**Cycle / sprint:** Cycle-008, Sprint **S04 — Governance & convention docs** (deliverable S04.2).
**Type:** governance / convention — formalize the by-reference + content-hash pattern the ledger's numeric
metric columns already use, and that the S03 ledger-row validator honors.
**Status:** Convention written. **This artifact carries no claim ceiling of its own and freezes nothing.**

> **Sanitization posture.** This is a governance/convention doc. It embeds **no** raw traces, simulator
> logs, deck lists, card IDs/names, Pokémon Elements, Competition Data, Daily-Top-Episodes, Kaggle
> episode data, Discord/peer screenshots, run-dir dumps, PDFs/CSVs, `deck.csv`, `cg/`, raw evidence rows,
> dispersion/band/win-rate values, or any inferential statistic. **No numeric governance margin `M` is
> chosen or stated** here. No forbidden agent word (*strong / competitive / optimal / calibrated /
> complete*) is used to describe agent evidence. Existing ledger evidence is referenced **by citation**,
> never re-embedded.

> **Cycle-008 posture (binding for every S04 doc).** Cycle-008 does **not**: attempt Rung 3; select a
> Rung-3 target; select a candidate; freeze a numeric comparison budget; freeze `K`/`n`; freeze a regime
> id; freeze a feature family; create SP-6; write or modify a ledger row; or advance the claim ceiling.
> **The current standing claim ceiling remains Rung 2** ([`../../claim-ceiling.md`](../../claim-ceiling.md)),
> and [`../../ledger.md`](../../ledger.md) remains the **only** ceiling-bearing artifact. This convention
> doc writes no ledger row and edits no ledger column.

---

## 1. The convention in one line

**A ledger row's numeric metric columns carry a by-reference placeholder — `see cited summary` — and the
actual numbers live in a separate, content-addressed summary artifact cited in the row's `notes`, never
embedded in the row itself.** The row says *where the evidence is and proves which bytes it is* (a
SHA-256 content hash); it does not paste the evidence.

This is not a new rule for S04 to invent — it is the pattern the standing **Rung-2 row already uses**
(the third data row of [`../../ledger.md`](../../ledger.md): its numeric metric cells read
`see cited summary`, and its `notes` cites the promoted summary by path **and** records the source
summary's `sha256` content hash). S04 only writes this down so future rows follow it deliberately.

## 2. Refer by reference, do not embed raw evidence

The 18-column ledger schema (header at [`../../ledger.md:9`](../../ledger.md), the schema authority — not
re-pasted here, per this very convention) has columns of three kinds:

| Column kind | What goes in the cell | Examples (by role) |
|---|---|---|
| **Identity / structure** | small, literal, sanitized tokens | run id, `regime_id`, `git_rev`, sim/agent versions, pool/seed refs, `games` count, `mode` |
| **Numeric metric** | the **by-reference placeholder `see cited summary`** when the values live in a cited summary | win-rate, illegal-action-rate, timeout-rate, error-rate, average-turns |
| **Governance / citation** | the bounded claim and the pointer to evidence | `claim_ceiling` (non-empty rung statement); `notes` (the cited-summary path + its `sha256`) |

The numeric-metric columns are exactly the ones that would otherwise tempt an author to paste per-batch
bands, win-rate values, or dispersion numbers directly into the ledger. **They must not.** Those values
are evidence; evidence is cited, not embedded.

## 3. What belongs in a metric/summary column vs. a cited artifact

| Belongs **in the row** (metric/summary + governance columns) | Belongs **only in the cited artifact** (referenced, content-hashed) |
|---|---|
| The placeholder `see cited summary` in numeric metric cells | Per-batch win-rate bands, `min`/`max`/`range`/`mean`/`median`/`spread` values |
| A non-empty `claim_ceiling` rung statement (the bounded claim) | Raw per-decision traces, simulator logs, run-dir dumps |
| `mode`, sample-size handle (`games`/`n`), sanitized ids and refs | The summary JSON body, its `hashes` integrity map, any per-batch table |
| In `notes`: the summary **path** + its **`sha256`** content hash + admissibility citations | The numeric governance margin `M` (lives **only** in the cycle's pre-registration doc) |

The dividing principle: **the row is a durable, append-only governance record; the cited artifact is the
evidence.** A reader follows the citation to get numbers; the row itself stays free of raw values, which
keeps the ceiling-bearing artifact sanitized and stable.

## 4. Sanitized hashes and cited summaries over raw traces or raw eval output

When a row needs to point at evidence, the preferred handle is, in order:

1. a **sanitized content hash** (`sha256`, 64-hex) of the summary artifact — tamper-evident and
   leak-free; it identifies the exact bytes without disclosing them;
2. a **cited summary path** to a tracked, sanitized summary artifact (e.g. an SP-6-style promoted
   summary) — which itself references, never embeds, the local/gitignored raw evidence;
3. **never** a raw trace, a raw evaluation output dump, a per-batch table, or a run-dir path treated as
   payload.

This mirrors the promoted-summary pattern in
[`../cycle-007/06a-sp6-promoted-summary.md`](../cycle-007/06a-sp6-promoted-summary.md): the source
summary stays local/gitignored and is promoted **by reference + content hash + a sanctioned descriptive
surface only**. A ledger row reuses that same content hash as its citation handle.

## 5. `docs/ledger.md` must remain append-only

- **One append-only row per run.** New evidence is added as a **new row appended at the end**; a prior
  committed row is **never edited** ([`../../ledger.md:3-7`](../../ledger.md), the ledger's own header
  rule).
- **The committed history is authoritative and is never re-judged.** Earlier rows legitimately reference
  prior governance terms (e.g. a past `SP-6`, a prior rung, a candidate, pre-registration); those are
  authorized history, not new movement.
- **An edit to a prior row, the header, or the separator is a violation,** not a correction. A genuine
  correction is itself an appended, operator-authorized act, not an in-place rewrite.
- **Append-only is checked, not just promised** — see §6.

## 6. `analysis/ledger_validate.py` is a gate, not a writer and not a claim engine

The S03 validator ([`../../../analysis/ledger_validate.py`](../../../analysis/ledger_validate.py);
report [`07-s03-implementation-report.md`](07-s03-implementation-report.md)) enforces this convention
**read-only**. Its role is precisely bounded:

- **It is a gate.** It content-checks the ledger against the 18-column schema verbatim, append-only
  discipline (LF-normalized byte-prefix against the committed `git show HEAD:docs/ledger.md` baseline),
  single-regime-per-row, and SHA-256-shaped digests; it **accepts** the `see cited summary`
  by-reference convention in the numeric metric columns (it requires no numeric values there); and it
  anchors [`../../claim-ceiling.md`](../../claim-ceiling.md) at **Rung 2**, failing closed on an
  unreadable baseline.
- **It is not a writer.** It performs **no** writes — no `write_text`/`open`/`mkdir`, and no git
  `add`/`commit`/`push`/`reset`/`checkout`; its only git reads are `show` + `hash-object`. Running it
  leaves `docs/ledger.md` byte-unchanged (proven by an unchanged `git hash-object` before and after).
- **It is not a claim engine.** It scores no agent, generates no evidence, computes no metric, and
  determines no Rung-3 readiness. It reports whether the ledger *mechanics* are valid; it blesses no
  rung and advances no ceiling.

## 7. Ledger edits and rows remain operator-governed

- **The validator decides admissibility, not authorization.** A green gate means a candidate row is
  *well-formed*; it is **not** permission to write it. Writing a ledger row, advancing a rung, or
  performing an SP-6 are **separate, explicitly operator-authorized terminal acts** (the OD-C7-10
  precedent: SP-6 → ledger row → claim-ceiling advance, each individually gated).
- **No automation appends rows.** A row enters the ledger only when an operator authorizes that specific
  act; the gate runs *before* the operator decides, never *instead of* the operator.
- **This convention doc changes nothing.** It writes no row, edits no column, and advances no ceiling;
  the standing ceiling remains **Rung 2** and the ledger remains byte-stable at `7da7e9a8…`.

## 8. Sources / traceability

- **Standing by-reference Rung-2 row (the pattern this convention names):**
  [`../../ledger.md`](../../ledger.md) (third data row; numeric metric cells = `see cited summary`;
  `notes` carries the cited-summary path + `sha256`).
- **Promoted-summary "reference + content hash, never raw content" precedent:**
  [`../cycle-007/06a-sp6-promoted-summary.md`](../cycle-007/06a-sp6-promoted-summary.md).
- **Validator honors the by-reference convention; gate-only, read-only, not a claim engine:**
  [`07-s03-implementation-report.md`](07-s03-implementation-report.md);
  [`../../../analysis/ledger_validate.py`](../../../analysis/ledger_validate.py);
  [`02-sdd.md`](02-sdd.md) §6.2 (SDD-C8-7).
- **Carry-forward 2 (metric-column convention) / C8-FR-5.2:** [`01-prd.md`](01-prd.md);
  [`03-sprint-plan.md`](03-sprint-plan.md) (S04.2).
- **Ceiling posture (ledger is the only ceiling-bearing artifact; acts are operator-gated):**
  [`../../claim-ceiling.md`](../../claim-ceiling.md).
