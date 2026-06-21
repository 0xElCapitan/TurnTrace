# Cycle-008 Sprint S04 — Governance & Convention Docs: Implementation Report

> Sprint artifact (S04 — Governance & convention docs). Status: **IMPLEMENTATION COMPLETE — awaiting
> `/review-sprint` → `/audit-sprint` → operator acceptance.** This S04 pass lands the four tracked,
> sanitized governance/convention docs under `docs/cycles/cycle-008/` — the `NNa-` numbering convention
> ([`08a-numbering-convention.md`](08a-numbering-convention.md)), the ledger metric-column "see cited
> summary" convention ([`08b-ledger-metric-column-convention.md`](08b-ledger-metric-column-convention.md)),
> the blocked-family map ([`08c-blocked-family-map.md`](08c-blocked-family-map.md)), and the form-only
> Rung-3 ladder-semantics doc ([`08d-rung3-form-only-semantics.md`](08d-rung3-form-only-semantics.md)) —
> plus this report. It is **documentation-only**: it writes **no** application code, runs **no** eval,
> creates **no** fresh evidence, and selects/freezes **no** Rung-3 target / candidate / numeric margin
> `M` / `K` / `n` / regime id / feature family. It creates **no** SP-6, writes **no** ledger row, advances
> **no** claim ceiling, edits **no** `.claude/`, and cleans/stages **no** State-Zone dirt. S01/S02/S03
> code is **untouched**.
>
> **Sanitized note.** No raw traces, simulator logs, deck lists, card IDs/names, Pokémon Elements,
> Competition Data, Daily-Top-Episodes, Kaggle episode data, Discord/peer screenshots, run-dir dumps,
> PDFs/CSVs, `deck.csv`, `cg/`, raw evidence rows, dispersion/band/win-rate values, or any inferential
> statistic appears here or in any of the four docs. **No numeric governance margin `M` is chosen or
> stated** — `M`/`K`/`n` appear only where the text *names a quantity the cycle declines to freeze*. No
> forbidden agent word (*strong / competitive / optimal / calibrated / complete*) is used to describe
> agent evidence. Existing evidence is referenced by citation/hash, never re-embedded.

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-008 / Sprint **S04 — Governance & convention docs** |
| **Type** | **Docs Zone** (no App-Zone code; no test; no eval; no fixture) |
| **Date** | 2026-06-21 |
| **Status** | **IMPLEMENTATION COMPLETE** — review/audit/acceptance pending; **not committed or pushed** in this pass |
| **Build-time HEAD** | `04bbf7ba7b53f15a9c8cbe8dba603c369bab76b7` — *feat: add Cycle-008 S03 ledger validator* (== `origin/main`; not ahead/behind) |
| **Sprint-plan citation anchor** | the S04 block ([`03-sprint-plan.md:644-715`](03-sprint-plan.md)) + SDD §2.2 / §6.1–§6.4 ([`02-sdd.md`](02-sdd.md)) re-read at build-time HEAD (see §6) |
| **Operator gate** | **OD-C8-6 OPEN** for the sanctioned Cycle-008 lane; this `/implement` request is **S04 only** (Docs Zone — needs no new gate) |
| **Claim ceiling (at S04)** | **Rung 2 — "beats random-legal"**; **held and preserved** (ceiling artifact byte-unchanged) |
| **Ledger invariant** | `docs/ledger.md` byte-unchanged; `git hash-object = 7da7e9a8dbed6561669d1569445eb9fe67a953fb` |
| **Ceiling invariant** | `docs/claim-ceiling.md` byte-unchanged; `git hash-object = 3d99759b919f7d75bc41ea81cd82e5f1fb974be7` |

---

## 1. Sprint goal & scope

**Goal (sprint plan [`03-sprint-plan.md:644-649`](03-sprint-plan.md)).** "Author the four tracked,
sanitized governance/convention docs under `docs/` — the SP-6/promoted-summary `NNa-` numbering
convention, the ledger metric-column 'see cited summary' convention, the blocked-family map, and the
**bounded docs-only Rung-3 ladder-semantics** definition (comparison **form only**, freezing nothing) —
each carrying **no ceiling of its own** and embedding **no raw content**."

**Scope.** MEDIUM (S04.1–S04.4). **Type:** Docs Zone only. The binding `/implement` request scopes this
pass to **S04 documentation only** and instructs "**Prefer no code/test changes**", listing only the
existing, non-mutating checks to run. S05 closeout is out of scope and absent.

---

## 2. What was built (five tracked docs, applying the `NNa-` convention)

All five S04 artifacts are filed under base ordinal `08`, demonstrating the very numbering convention
S04.1 formalizes (the four convention docs are `08a`–`08d` companions to the base `08` report):

### 2.1 [`08a-numbering-convention.md`](08a-numbering-convention.md) — `NNa-` numbering convention (S04.1)

Formalizes the per-cycle document numbering already in the tree (precedent:
[`../cycle-007/06a-sp6-promoted-summary.md`](../cycle-007/06a-sp6-promoted-summary.md)): what `NNa-` is
for (insertion/grouping without consuming the next integer or renaming accepted files); when it is used
vs. when a new integer is used; how it keeps the three numbering axes — **cycle-document ordinal `NN`**,
**sprint infix `sXX`**, **report family `NN-sXX-implementation-report`** — unambiguous (`NN` is a document
counter, never a sprint id); why `04-s00-…` / `07-s03-…` look mismatched but are correct; and how to
preserve traceability **without renaming already-accepted artifacts** unless explicitly authorized. The
doc's own filename (`08a-…`) follows the convention it formalizes.

### 2.2 [`08b-ledger-metric-column-convention.md`](08b-ledger-metric-column-convention.md) — ledger metric-column "see cited summary" convention (S04.2)

Documents the by-reference + content-hash pattern the standing Rung-2 row already uses (the numeric
metric cells read `see cited summary`; the actual numbers live in a cited, content-hashed summary). Covers
what belongs in a metric/summary column vs. a cited artifact; that sanitized hashes + cited summaries are
preferred over raw traces or raw eval output; that [`../../ledger.md`](../../ledger.md) is **append-only**;
that [`../../../analysis/ledger_validate.py`](../../../analysis/ledger_validate.py) is a **read-only gate,
not a writer and not a claim engine**; and that ledger edits/rows remain **operator-governed**.

### 2.3 [`08c-blocked-family-map.md`](08c-blocked-family-map.md) — blocked-family map (S04.3)

A tracked, sanitized map with all three classes: **measurable now** (the five §2.2 surfaces the S01
diagnostic emits, named); **needs future sim instrumentation** (backup-attacker readiness, attach/energy
tempo, attack-vs-setup timing, contextual-retreat semantics — documented, **not built**); **requires
separate operator authorization** (per-decision quality of prize trades FM-03, wasted resources FM-04,
missed lethals FM-06, bad search targets FM-08 — `detector: forbidden`, documented, **not built**). It
adds a governance-level blocked list (Rung-3 attempts; target/candidate selection; numeric comparison
budget / `K`/`n` / regime / feature family; fresh evidence / eval promotion; runtime-agent changes; the
heuristic/search/FunSearch/RL/self-play/MCTS/tournament/deck-optimizer/dashboard family; per-decision
quality scoring; per-Pokémon/card/deck semantic instrumentation; and raw data of any kind). Names no card
data; embeds no raw content; builds nothing it documents.

### 2.4 [`08d-rung3-form-only-semantics.md`](08d-rung3-form-only-semantics.md) — form-only Rung-3 ladder semantics (S04.4)

A docs-only definition of the Rung-3 comparison **form only**: *a future candidate must beat the current
non-trivial incumbent under a same-regime, fresh-evidence, pre-registered comparison.* It explicitly
freezes **no** candidate identity, **no** numeric margin `M`, **no** `K`/`n` values, **no** regime id,
**no** target feature family, **no** threshold, and opens **no** attempt; it creates **no** SP-6, writes
**no** ledger row, and asserts **no** ceiling movement — the standing ceiling remains **Rung 2**. (The
*executable* freezes-nothing lint named in sprint-plan task S04.4 is deferred this pass per the
documentation-only instruction — see §7.)

---

## 3. Commands run & results

All run at build-time HEAD `04bbf7b`. Smallest-sufficient, non-mutating checks only (Docs-Zone sprint).

| # | Command | Result |
|---|---|---|
| 1 | `python analysis/ledger_validate.py docs/ledger.md --expected-ledger-hash 7da7e9a8… --expected-ceiling-hash 3d99759b…` | exit **0** — VALID; ledger schema/append-only/regime/digest clean; claim-ceiling holds **Rung 2**; "Wrote nothing." |
| 2 | `python eval/hygiene_check.py --paths 08a 08b 08c 08d` (four governance docs) | exit **0** — clean; no Competition-Data paths (4 checked) |
| 3 | `python eval/hygiene_check.py --paths 08-s04-implementation-report.md 08a 08b 08c 08d` (all five S04 docs incl. this report) | exit **0** — clean (5 checked) |
| 4 | `git hash-object docs/ledger.md` | `7da7e9a8…` (byte-unchanged, before and after check #1 — the read-only proof) |
| 5 | `git hash-object docs/claim-ceiling.md` | `3d99759b…` (byte-unchanged) |
| 6 | `git status --porcelain .claude/` | empty (System Zone clean) |
| 7 | `git diff --cached --name-only` | empty (nothing staged; new docs + protected dirt left unstaged) |

---

## AC Verification

Each binding `/implement` acceptance criterion is quoted verbatim, with status and evidence. (Sprint-plan
S04 ACs [`03-sprint-plan.md:674-692`](03-sprint-plan.md) are mapped in §4.1.)

1. "S04 governance/convention docs exist under `docs/cycles/cycle-008/`." — **✓ Met.**
   [`08a`](08a-numbering-convention.md)/[`08b`](08b-ledger-metric-column-convention.md)/[`08c`](08c-blocked-family-map.md)/[`08d`](08d-rung3-form-only-semantics.md) (§2; status #3 lists them present).
2. "Required documentation families are covered: `NNa-` numbering convention; ledger metric-column
   convention; blocked-family map; form-only Rung-3 semantics." — **✓ Met.** §2.1 / §2.2 / §2.3 / §2.4
   respectively.
3. "A S04 implementation report exists under `docs/cycles/cycle-008/`." — **✓ Met.** This file,
   [`08-s04-implementation-report.md`](08-s04-implementation-report.md).
4. "Docs are sanitized and contain no raw forbidden data." — **✓ Met.** Each doc carries the sanitized
   posture blockquote; hygiene clean on all five (Commands #2, #3).
5. "Docs do not select/freeze Rung-3 target/candidate/comparison-budget/`K`/`n`/regime/feature family." —
   **✓ Met.** [`08d` §4](08d-rung3-form-only-semantics.md) enumerates the absence; the binding posture
   blockquote in all four docs repeats it; hygiene clean (no numeric `M`).
6. "Docs do not create SP-6." — **✓ Met.** Non-occurrence; §5 explicit non-acts; no SP-6 artifact written.
7. "Docs do not write or modify a ledger row." — **✓ Met.** `docs/ledger.md` byte-unchanged
   (`7da7e9a8…`, Commands #1/#4); ledger_validate reports "Wrote nothing."
8. "Docs do not advance the claim ceiling." — **✓ Met.** `docs/claim-ceiling.md` byte-unchanged
   (`3d99759b…`, Command #5); ceiling reads **Rung 2** ([`../../claim-ceiling.md:10`](../../claim-ceiling.md)).
9. "Docs correctly state current claim ceiling remains Rung 2." — **✓ Met.** Each doc's posture
   blockquote states Rung 2 held; [`08d` §2/§5](08d-rung3-form-only-semantics.md).
10. "Docs correctly frame `analysis/ledger_validate.py` as a read-only gate, not a writer or claim
    engine." — **✓ Met.** [`08b` §6](08b-ledger-metric-column-convention.md) ("It is a gate. … It is not
    a writer. … It is not a claim engine.").
11. "Docs correctly carry forward S01/S02/S03 non-blocking notes without changing code." — **✓ Met.** §4.2
    (six carried-forward governance notes); no S01/S02/S03 code touched (status #3 shows `analysis/` /
    `tests/` unchanged).
12. "`docs/ledger.md` remains hash `7da7e9a8…`." — **✓ Met.** Command #4.
13. "`docs/claim-ceiling.md` remains hash `3d99759b…`." — **✓ Met.** Command #5.
14. "Claim ceiling remains Rung 2." — **✓ Met.** Command #1 + [`../../claim-ceiling.md:10`](../../claim-ceiling.md).
15. "`.claude/` remains clean." — **✓ Met.** Command #6 (empty).
16. "Protected State-Zone dirt remains unstaged and uncleaned." — **✓ Met.** §5; final status shows
    `.beads/issues.jsonl`, `grimoires/loa/NOTES.md`, `grimoires/loa/README.draft.md` modified/untracked-
    unstaged; Command #7 (nothing staged).
17. "No S05 closeout work is accidentally included." — **✓ Met.** No closeout artifact authored; §1 scope;
    no invariant-closeout doc exists (the S05 closeout `09-…` is absent).
18. "No code/test/fixture change is included unless explicitly justified by the sprint plan." — **✓ Met.**
    Only the five `docs/` artifacts were authored; no `analysis/` / `tests/` / `eval/` / `sim/` path was
    touched. The one sprint-plan-named test (the S04.4 freezes-nothing lint) is **deferred** per the
    documentation-only instruction, not added (§7).

---

## 4. Sprint-plan AC mapping & carried-forward notes

### 4.1 Sprint-plan S04 acceptance criteria

| Sprint-plan AC ([`03-sprint-plan.md:674-692`](03-sprint-plan.md)) | Status |
|---|---|
| **Rung-3 form-only, freezes nothing** (a lint/test asserts the doc contains no candidate / `M` / `K`/`n` / regime / feature family / threshold; opens no attempt) | **✓ Property met; ⏸ executable lint deferred.** [`08d`](08d-rung3-form-only-semantics.md) is form-only and §4 enumerates the absence; hygiene clean. The *executable* lint is deferred this pass (§7). |
| **Blocked-family map present + classified** (all three classes; "measurable now" names the §2.2 surfaces; others documented-not-built; no card data; no raw content) | **✓ Met.** [`08c` §2](08c-blocked-family-map.md). |
| **Conventions written down** (`NNa-` numbering + ledger metric-column "see cited summary"; metric-column doc matches what S03 honors) | **✓ Met.** [`08a`](08a-numbering-convention.md), [`08b`](08b-ledger-metric-column-convention.md) (S03 parity: [`08b` §6](08b-ledger-metric-column-convention.md)). |
| **No ceiling of their own** (none of the four asserts/advances a ceiling; ledger remains the only ceiling-bearing artifact) | **✓ Met.** Each posture blockquote; Commands #1/#5. |
| **Hygiene / no-embed** (`eval/hygiene_check.py` clean; no raw content; no numeric `M`; no inferential term; no affirmative forbidden agent word) | **✓ Met.** Commands #2/#3. |
| **Non-occurrence** (no Rung-3 target; nothing frozen; no ledger row; no ceiling advance; no `.claude/` edit; ledger/ceiling byte-unchanged) | **✓ Met.** §5; Commands #1/#4/#5/#6. |
| `/review-sprint` + `/audit-sprint` verify; operator accepts | **⏸ Pending** (downstream gates; not part of this pass). |

### 4.2 Carried-forward governance notes (S01/S02/S03 — non-blocking, no code changed)

Per `/implement` scope item 9, the following standing notes are carried forward as governance notes; **no
code is changed by recording them here**:

- **S01 player-scoping note** remains **deferred to S05/follow-up** unless a later sprint explicitly
  authorizes generator hardening.
- **S02 empty-object sanitizer acceptance** is a **leak allow-list behavior**, not a completeness
  guarantee.
- **S02 free-text value coverage** is **parity-bounded**; arbitrary card-name prose is **not** closed,
  because closing it would require card dictionaries / Competition Data (out of scope, blocked).
- **S03 governance-scan keyword coverage** is **heuristic**; the **append-only discipline** and
  **claim-ceiling anchoring** are the load-bearing controls.
- **S03 delta-only governance scanning** is **correct and necessary**: authorized historical ledger
  content legitimately contains prior SP-6 / Rung / candidate references, so only the appended delta is
  scanned (a whole-file scan would reject the real ledger).
- **S03 UTF-8 subprocess decoding** must remain **preserved** (the default locale decode mangles the
  ledger's UTF-8 em-dashes on Windows and breaks the byte-prefix check).

---

## 5. Explicit non-acts (this S04 pass)

This pass: wrote **no** application code and touched **no** App-Zone path (`analysis/`, `eval/`, `sim/`,
`cabt/`, `agents/`); created **no** test and **no** fixture; ran **no** eval and **no** diagnostic;
generated **no** fresh evidence and read **no** trace row for content; selected **no** Rung-3
target/attempt and froze **no** candidate / numeric margin `M` / `K` / `n` / regime id / feature family;
issued **no** SP-6 and promoted **no** value; made **no** `docs/ledger.md` edit (byte-unchanged at
`7da7e9a8…`) and appended **no** ledger row; made **no** `docs/claim-ceiling.md` edit (byte-unchanged at
`3d99759b…`; still Rung 2) and advanced **no** ceiling; made **no** `.claude/` edit; staged, cleaned,
edited, or deleted **no** State-Zone dirt (`.beads/issues.jsonl`, `grimoires/loa/NOTES.md`,
`grimoires/loa/README.draft.md` remain modified/untracked-unstaged); and staged, committed, or pushed
**nothing**.

---

## 6. Invariant & citation-anchor verification

- **HEAD / origin parity:** `git rev-parse HEAD == origin/main == 04bbf7ba7b53f15a9c8cbe8dba603c369bab76b7`.
- **Ledger invariant:** `git hash-object docs/ledger.md = 7da7e9a8dbed6561669d1569445eb9fe67a953fb`
  (byte-unchanged, before and after running the gate — the read-only proof).
- **Ceiling invariant:** `git hash-object docs/claim-ceiling.md = 3d99759b919f7d75bc41ea81cd82e5f1fb974be7`
  (byte-unchanged); **claim ceiling remains Rung 2** ([`../../claim-ceiling.md:10`](../../claim-ceiling.md)).
- **System Zone:** `git status --porcelain .claude/` empty; **nothing staged**.
- **Citation anchors re-read at build-time HEAD (NFR-12):** the sprint-plan S04 block
  ([`03-sprint-plan.md:644-715`](03-sprint-plan.md)), SDD §2.2 (surfaces), §6.1–§6.4 (conventions /
  blocked families / Rung-3 form) ([`02-sdd.md`](02-sdd.md)); the `NNa-` precedent
  ([`../cycle-007/06a-sp6-promoted-summary.md`](../cycle-007/06a-sp6-promoted-summary.md)); the standing
  Rung-2 row and ceiling line ([`../../ledger.md`](../../ledger.md);
  [`../../claim-ceiling.md:10`](../../claim-ceiling.md)); FM-03/04/06/08 `detector: forbidden`
  ([`../../failure-mode-taxonomy-v001.md`](../../failure-mode-taxonomy-v001.md)) — all accurate at
  `04bbf7b` (the planning docs are committed and clean).

---

## 7. Known limitations / carry-forward

- **Executable freezes-nothing lint (sprint-plan S04.4) deferred this pass.** The sprint plan's S04.4
  names "add the freezes-nothing lint/test." This `/implement` request is **documentation-only**
  ("**Prefer no code/test changes**"; in-scope items are docs; the listed checks are existing,
  non-mutating ones), and a new `tests/` lint would land in the OD-C8-6 App-Zone lane this request scopes
  out. The freezes-nothing **property** is nonetheless satisfied and demonstrated:
  [`08d` §4](08d-rung3-form-only-semantics.md) enumerates every quantity left unfrozen, and
  `eval/hygiene_check.py` is clean on `08d` (no numeric `M`, no inferential term, no raw content). **The
  executable lint is recommended for the S04 `/review-sprint` → `/audit-sprint` cycle or a follow-up
  micro-sprint, under explicit authorization.** This deferral is recorded here (the binding S04 artifact)
  rather than in `grimoires/loa/NOTES.md`, because this request forbids editing the protected State-Zone
  `NOTES.md`.
- **Docs-only.** These four docs write down rules and conventions; they make no new empirical claim,
  build none of the families they document, and carry no ceiling. They move TurnTrace **no** rung; Rung 2
  holds.
- **Conventions formalize existing practice.** The `NNa-` and metric-column conventions describe patterns
  already in the tree (cycle-007 `06a-…`; the standing Rung-2 row); they introduce no new artifact format
  and rename nothing.

---

## 8. Changed files & final status

**New — all under this cycle's `docs/` lane (Docs Zone):**

- `docs/cycles/cycle-008/08-s04-implementation-report.md` (NEW — this file)
- `docs/cycles/cycle-008/08a-numbering-convention.md` (NEW)
- `docs/cycles/cycle-008/08b-ledger-metric-column-convention.md` (NEW)
- `docs/cycles/cycle-008/08c-blocked-family-map.md` (NEW)
- `docs/cycles/cycle-008/08d-rung3-form-only-semantics.md` (NEW)

**Final `git status --porcelain`** (changes left unstaged; not committed or pushed):

```
 M .beads/issues.jsonl
 M grimoires/loa/NOTES.md
?? docs/cycles/cycle-008/08-s04-implementation-report.md
?? docs/cycles/cycle-008/08a-numbering-convention.md
?? docs/cycles/cycle-008/08b-ledger-metric-column-convention.md
?? docs/cycles/cycle-008/08c-blocked-family-map.md
?? docs/cycles/cycle-008/08d-rung3-form-only-semantics.md
?? grimoires/loa/README.draft.md
```

`.beads/issues.jsonl`, `grimoires/loa/NOTES.md`, and `grimoires/loa/README.draft.md` remain the
pre-existing State-Zone dirt — **modified/untracked-unstaged, not edited, not staged, not cleaned** by
this pass.

---

> **S04 statement (binding).** The four Cycle-008 governance/convention docs are authored and sanitized:
> the `NNa-` numbering convention, the ledger metric-column "see cited summary" convention, the
> blocked-family map (three classes, "measurable now" grounded in the S01 surfaces), and the form-only
> Rung-3 ladder-semantics doc (freezes nothing, opens no attempt). Hygiene is clean on all five docs;
> `docs/ledger.md` = `7da7e9a8…` and `docs/claim-ceiling.md` = `3d99759b…` are byte-unchanged; the claim
> ceiling remains **Rung 2** and the ledger remains the only ceiling-bearing artifact; `.claude/` is
> clean; State-Zone dirt is preserved and unstaged. **No code/test/fixture was changed, no eval run, no
> evidence generated, no Rung-3 target/candidate/`M`/`K`/`n`/regime/feature-family frozen, no SP-6, no
> ledger row, no value promotion, and no ceiling advance occurred.** Nothing was committed or pushed.
> **Stop point:** S04 implementation only — no review, audit, S05, or closeout performed.
