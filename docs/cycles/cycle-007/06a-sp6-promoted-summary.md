# Cycle-007 SP-6 — Promoted Sanitized Evidence Summary (OD-C7-10 terminal act 1)

**Date:** 2026-06-20
**Cycle / sprint:** Cycle-007, Sprint **S04** terminal acts — **SP-6** (the **first** OD-C7-10 act).
**Type:** governance / promotion — promote the sanitized evidence summary to tracked status by
**reference + content hash + sanctioned descriptive summary only**.
**Status:** SP-6 performed. **This artifact takes no further terminal act** — it writes **no** Rung-2
ledger row and advances **no** claim ceiling.

> Sanitization posture: this tracked artifact carries **references + a content hash + sanitized
> agent / regime / metric identifiers + the minimal descriptive verdict surface already disclosed in
> S04 only**. It embeds **no** raw traces, simulator logs, deck lists, card IDs/names, Pokémon
> Elements, Competition Data, Daily Top Episodes, run-dir dumps, PDFs/CSVs, `deck.csv`, `cg/`, raw
> evidence rows, the local summary JSON dump, per-batch tables, inferential statistics (no p-value,
> confidence interval, hypothesis test, std-dev, variance, or model estimate), the numeric governance
> threshold `M` (which lives **only** in `04-pre-registration.md` §2; a numeric `M` in any other
> tracked artifact is a posture violation), any forbidden agent word (*strong / competitive / optimal /
> calibrated / complete*), agent-strength marketing language, or any ceiling-bearing claim. **This
> SP-6 artifact carries no claim ceiling of its own.**

---

## 1. What this act is (and is not)

- **Is:** Cycle-007 **OD-C7-10 act 1 / SP-6** — the operator-authorized promotion of the sanitized
  Cycle-007 evidence summary from local/gitignored to **tracked** status, by **reference + content
  hash + a sanctioned descriptive summary** (`02-sdd.md` §6.1; `04-pre-registration.md` §9.1;
  `06-verdict-application.md` §9.1).
- **Is not:** a Rung-2 ledger row, a claim-ceiling advance, an evidence (re-)generation, an eval run, a
  re-run / top-up / candidate swap / threshold change / verdict change, or a promotion of any **raw**
  content. **None of those occur here** (§7, §8).
- **The promoted artifact is a sanitized summary / reference only.** The summary's bands, per-batch
  values, traces, and JSON body remain **local/gitignored**; only the reference, the content hash, the
  sanitized identifiers, and the descriptive surface already disclosed in S04 are tracked here.

---

## 2. Anchors (commit-order provenance — "`M` before bands")

| Anchor | Commit |
|---|---|
| **S02 pre-registration** (tuple incl. `M` fixed before any band existed) | `a27aef38db5cded5120c4eb923f6a7e8cd27a6e2` |
| **S03 admissibility / provenance** (fresh same-regime evidence + both gates) | `3f6dcd9bfdebe7dfb1c323266c99e14134006018` |
| **S04 PASS verdict** | `a1466ba133e133bf02e0845c4639f1c0aedd5b8a` |

The S02 anchor is strictly ancestral to the S03 anchor (`git merge-base --is-ancestor` → exit `0`;
`05-evidence-generation-report.md` §2; `06-verdict-application.md` §2), so the threshold was frozen
**before** the fresh `regime-v003` bands were generated — tamper-evident in history.

---

## 3. The one frozen tuple (sanitized identifiers)

SP-6 promotes the summary for **exactly** the one pre-registered tuple — no swap, no best-of-N.

| Field | Value |
|---|---|
| candidate | `scripted-v001` |
| baseline | `random_legal-v001` (under the new regime) |
| regime | `regime-v003` |
| `M` | the pre-registered governance threshold (numeric value recorded **only** in `04-pre-registration.md` §2) |
| `K` | `20` batches per side |
| `n` | `500` matches per batch per agent |
| stopping rule | read **exactly** the 20 pre-generated same-regime batches, then stop |

---

## 4. The promoted source summary (local → tracked-by-reference)

| Property | Value |
|---|---|
| **Local source summary path** | `.run/s03-gen/evidence-summary-regime-v003.json` |
| **Local status** | local / **gitignored** (`.gitignore` `.run/`) / **untracked** / **unstaged** — **not** promoted as raw content |
| **Full source summary content hash (sha256)** | `60d3c8afeba121e8884a5493989b8633fa6ae4116bf2a60b8537f15c2acb0ddf` |
| **Sanitized promoted-summary artifact (this file)** | `docs/cycles/cycle-007/06a-sp6-promoted-summary.md` |

The source summary stays local/gitignored; SP-6 promotes it **by reference + the content hash above**,
never by embedding its JSON body, its `hashes` integrity map, its bands, or any per-batch table. The
hash recorded here is the citation handle a later Rung-2 ledger row would reuse (§8).

---

## 5. Admissibility gate re-checks (gate-only — both exit 0)

Run on the local/gitignored source summary; both gates **write nothing and promote nothing**.

| Gate command | Exit code |
|---|---|
| `python analysis/evidence_summary.py --validate .run/s03-gen/evidence-summary-regime-v003.json` | `0` |
| `python analysis/evidence_summary.py --promotion-check .run/s03-gen/evidence-summary-regime-v003.json` | `0` |

`--validate` exit 0 → schema-conforming, sanitized, single-regime. `--promotion-check` exit 0 → the
full hardened validator is clean **and** the summary carries a non-empty `hashes` integrity stamp
(`05-evidence-generation-report.md` §7; `06-verdict-application.md` §4).

---

## 6. Authorized descriptive verdict surface (already disclosed in S04 §6)

For summary continuity only, the descriptive surface **already disclosed** in the tracked S04 verdict
report (`06-verdict-application.md` §6–§7) — allowed vocabulary (`count / min / max / range / mean /
median / spread`), per-batch win-rate across the `K = 20` same-regime batches:

| Quantity (per-batch win-rate, across `K = 20`) | Value |
|---|---|
| candidate `scripted-v001` win-rate **`min`** | `0.760` |
| baseline `random_legal-v001` win-rate **`max`** | `0.568` |
| descriptive separation (candidate `min` − baseline `max`) | `0.192` |

- The per-batch win-rate bands are **disjoint** (candidate `min` strictly greater than baseline `max`);
  the descriptive separation **exceeds** the pre-registered `M` (value in `04-pre-registration.md` §2).
- The sanctioned descriptive statement, carried verbatim-in-intent from `06-verdict-application.md` §7:
  under `regime-v003` at `n = 500` over `K = 20` batches, the candidate `scripted-v001` **beats** the
  `random_legal-v001` baseline by the pre-registered descriptive margin. It is a **same-regime
  TurnTrace descriptive delta**, never episode-derived; it asserts **nothing** beyond this regime and
  applies **no** forbidden agent word and **no** inferential statistic even though the verdict is PASS.

---

## 7. Ceiling posture (hard)

- **This SP-6 artifact carries no claim ceiling of its own.** Promoting the summary to tracked status
  asserts only that the summary exists, is sanitized, passes both gates, and is content-addressed by
  the hash in §4 — it advances nothing.
- **`docs/ledger.md` remains the only ceiling-bearing artifact** (`04-pre-registration.md` §0, §9;
  `06-rung-2-ledger-convention.md` §3). The standing posture is unchanged: **Rung 1 holds**;
  `docs/ledger.md` is byte-unchanged (`git hash-object` = `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`);
  `docs/claim-ceiling.md` is unchanged and **still states Rung 1**.
- **Rung 2 is still not earned.** It is earned **only** when the **Rung-2 ledger row** and the
  **claim-ceiling advance** are each **separately authorized under OD-C7-10** and applied. SP-6 alone
  does not earn it.

---

## 8. This is not the remaining terminal acts

This act is SP-6 **only**. Specifically, this artifact:

- writes **no** Rung-2 ledger row; **`docs/ledger.md` is not edited** (byte-unchanged at `2a2f1c2…`);
- advances **no** claim ceiling; **`docs/claim-ceiling.md` is not edited** (still Rung 1);
- issues **no** claim-ceiling update; starts **no** S05 closeout; generates **no** evidence.

The OD-C7-10 terminal acts remain **separate, ordered, and individually operator-gated**
(`06-verdict-application.md` §9; `02-sdd.md` §6.4):

```
SP-6 (this act)  →  Rung-2 ledger row  →  docs/claim-ceiling.md advance to Rung 2
```

**The next OD-C7-10 act is the Rung-2 ledger row (act 2) — not the claim-ceiling advance (act 3).**
Each remaining act requires its own separate explicit OD-C7-10 operator authorization and is not taken
here. A future Rung-2 ledger row, when separately authorized, would cite this promoted summary **by
reference + the §4 content hash** in its `notes` field, reusing the existing 18-column schema verbatim
with no new column (`06-rung-2-ledger-convention.md` §1–§3).

---

## 9. Sources / traceability

- **Pre-registration tuple + `M`/`K`/`n`/stopping rule + terminal-act order:**
  `docs/cycles/cycle-007/04-pre-registration.md` (§1, §9).
- **Admissibility / provenance / source-summary hash + gate exit codes:**
  `docs/cycles/cycle-007/05-evidence-generation-report.md` (§2, §6, §7).
- **PASS verdict + descriptive surface + OD-C7-10 separation:**
  `docs/cycles/cycle-007/06-verdict-application.md` (§6, §7, §9).
- **SP-6 design (reference + content hash + sanitized names; never raw content):**
  `docs/cycles/cycle-007/02-sdd.md` §6.1; `docs/cycles/cycle-007/01-prd.md` C7-FR-5.
- **Summary carries no ceiling; ledger is the only ceiling-bearing artifact; row cites summary by
  reference + hash:** `docs/cycles/cycle-003/04-evidence-summary-schema-spec.md` §1;
  `docs/cycles/cycle-003/06-rung-2-ledger-convention.md` §1–§4.
- **Gates / hygiene:** `analysis/evidence_summary.py` (`--validate`, `--promotion-check`);
  `eval/hygiene_check.py` (path-based staging guard). `docs/ledger.md` byte-unchanged at
  `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`; `docs/claim-ceiling.md` unchanged (Rung 1).
