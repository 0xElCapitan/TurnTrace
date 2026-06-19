# Cycle-005 PRD — Promotion-Gate Hardening

> Planning artifact (PRD). Status: **DRAFT — awaiting operator acceptance.** This PRD specifies a **hardening
> build** cycle, but the PRD itself **opens no implementation gate**: code lands only through
> `/architect → /sprint-plan → /implement → /review-sprint → /audit-sprint → operator acceptance`
> (`docs/operator/turntrace-loop-contract.md` §6, the OA-2-class build-gate authorization). Cycle-005 hardens
> the Cycle-004 evidence-summary generator/validator (`analysis/evidence_summary.py` +
> `tests/test_evidence_summary.py`) so the gate can **later** be trusted as part of a value-promotion gate.
> **Cycle-005 attempts no Rung 2, promotes no value, and mutates neither the ledger nor the claim ceiling.**
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, Daily-Top-Episode data, or Competition Data appear here
> (CC-1/CC-2, ESP, SP-6/SP-9). **No dispersion metric values appear here** — evidence stays local/gitignored and
> is referenced qualitatively only. Runs are referenced by `run_id` pattern, count, hashes, sanitized metric
> *names*, claim ceilings, and local path/status only. The forbidden agent words (*strong / competitive /
> optimal / calibrated / complete*) and the inferential terms (*std-dev / variance / CI / p-value /
> significance / hypothesis-test / error-bar*) appear only as the negated/forbidden language they are.

## 0. State verified (2026-06-19, before drafting)

| Assumption to verify | Result |
|---|---|
| Current HEAD / branch | `main` @ `337fc4f` — *docs: record TurnTrace competition findings* (== `origin/main`) |
| Local branch not behind `origin/main` | `git ls-remote origin main` = `337fc4f` — not behind |
| `docs/ledger.md` byte-unchanged | **byte-unchanged**; `git diff --exit-code` clean; `hash-object = 2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` |
| Claim ceiling still Rung 1 | **Rung 1** (`docs/claim-ceiling.md`) |
| Cycle-004 build artifacts present | `analysis/evidence_summary.py` (511 lines) + `tests/test_evidence_summary.py` (289 lines) present, tracked, accepted |
| No staged files | **none staged** |
| `.beads/issues.jsonl`, `grimoires/loa/NOTES.md` dirty | both modified, **unstaged** (pre-existing State-Zone housekeeping); not staged/committed by this cycle |
| `.claude/` untouched | **no drift**; `integrity_enforcement: strict` → no HALT |
| `.claude/`/`frozen/`/`runs/`/`agents/`/`sim/`/`analysis/`/`tests/` drift | **none** (no tracked drift) |

**All assumptions hold. No finding forces a stop.** Implementation remains un-authorized until the operator
accepts this PRD and proceeds through `/architect → /sprint-plan → /implement`.

| Field | Value |
|---|---|
| **Cycle** | Cycle-005 |
| **Working title** | Promotion-Gate Hardening |
| **Alt. framing** | Make the Cycle-004 evidence-summary validator/promotion machinery airtight **before** it ever gates a value promotion — without attempting Rung 2 |
| **Type** | Product Requirements Document (planning artifact for a hardening build cycle) |
| **Status** | DRAFT — awaiting operator acceptance; next Golden-Path step is SDD / architecture |
| **Date** | 2026-06-19 |
| **Current main** | `337fc4f` — *docs: record TurnTrace competition findings* |
| **Binding input** | local pre-PRD research pass (`grimoires/loa/a2a/cycle-005/00-pre-prd-research.md`, gitignored State Zone — research input, **not** authority); the Cycle-004 audit carry-forwards C1–C4; the Cycle-003 design authorities (docs 04–08); the competition-findings patch (SP-8/SP-9, FM-10/FM-11) |
| **Posture** | **Hardening-only.** Modify exactly the two Cycle-004 evidence-summary artifacts for C1–C4; hold every other bright line |
| **Claim ceiling** | **Rung 1** (held for the whole cycle; not raised) |

## Required posture (binding)

- **Cycle-005 is hardening-only.** It hardens the Cycle-004 evidence-summary generator/validator (C1–C4 below),
  its tests, and nothing else. The only tracked code it touches is `analysis/evidence_summary.py` and
  `tests/test_evidence_summary.py`.
- **Rung 1 remains held** for all of Cycle-005 (`docs/claim-ceiling.md:5-6`). No "beats random-legal" verdict;
  no Rung-2 claim.
- **No Rung-2 admission** in Cycle-005; **no same-regime admission verdict** is written or implied.
- **No Rung-2 ledger row.** `docs/ledger.md` stays **byte-unchanged** at its two Rung-1 `regime-v001` rows
  (`docs/ledger.md:11-12`; hash `2a2f1c2…`).
- **No claim-ceiling advance.** `docs/claim-ceiling.md` is unchanged; the ledger remains the only
  ceiling-bearing artifact.
- **No numeric margin `M` is chosen; OD-6 is not relaxed; no inferential statistic is computed.** The validator
  *rejects* inferential terms; it does not produce them.
- **No SP-6 live-value promotion.** No dispersion value reaches tracked status; the generator stays
  local-by-default; any exercise output stays gitignored.
- **No new eval runs; no K=50 top-up; no paired-delta tooling** (NG12 carried). The cycle reads no new runs and
  produces no new evidence.
- **No runtime-agent work; no broad optimization; no FunSearch implementation/scaffold/surface; no
  cross-regime comparison; no regime mutation.**
- **No Kaggle / Daily Top Episodes ingest.** Daily Top Episodes remain **local-only hypothesis input, never
  proof of improvement** (SP-9); raw episode datasets stay local/ignored.
- **Simulator behavior remains authoritative** over official-rule assumptions (SP-8): offline analysis and any
  verdict logic follow the simulator-offered legal options and the simulator terminal result, never
  official-rule assumptions.
- **No raw Competition Data / Pokémon Elements / traces / card names / deck lists / simulator logs** are
  committed or staged (CC-1/CC-2, ESP).
- **`.claude/` (System Zone) is never edited.** Build code is App Zone (`analysis/`, `tests/`); the PRD is
  State/Docs Zone. No State-Zone cleanup is performed by this cycle.

**The bright line for the whole cycle:** *Cycle-004 built the evidence-summary generator + independent
fail-closed validator and stopped before the admission seam; the Cycle-004 audit recorded four pre-promotion
hardening carry-forwards (C1–C4) as mandatory before the validator becomes load-bearing at any value-promotion
gate. Cycle-005 implements exactly those four hardenings — making the validator strictly more conservative,
never looser — while holding Rung 1, leaving `docs/ledger.md` byte-unchanged, promoting no value, attempting no
Rung 2, and deferring the Rung-2 admission seam (8a–8d) to a separate later gate (expected Cycle-006 or later).*

## 1. Product / cycle overview

TurnTrace is a local, sanitized evaluation harness for a card-game simulator. Cycle-004 ("OA-2 Build")
delivered `analysis/evidence_summary.py` — an offline generator (`build_summary`) plus an independent,
fail-closed validator (`validate_summary` + the `--validate` re-read mode) sharing one in-module allow-list
constant (`SAFE_FIELDS`) — and `tests/test_evidence_summary.py` (12 stdlib checks). The cycle closed
**accepted, pushed, at Rung 1**, promoting nothing (`docs/cycles/cycle-004/07-closeout.md`).

The Cycle-004 review and audit independently reproduced four robustness gaps and recorded them as
**non-blocking for the build-only cycle** (which gated only the generator's own clean output) but **mandatory
hardening before the validator becomes load-bearing at a value-promotion gate**
(`docs/cycles/cycle-004/06-audit-report.md` §7, §9; `docs/cycles/cycle-004/05-review-report.md` §9):

- **C1 (priority)** — make the validator's digest-shape / allow-list **positional**, so a known field name in a
  non-schema position cannot bypass content checks.
- **C2** — tighten the forbidden-word negation heuristic to immediate-precedence negation.
- **C3** — repo-root-resolve the `--out` guard (`_refuse_tracked_out`).
- **C4** — warn (or fail appropriately) on empty `hashes`.

**Cycle-005 is the cycle that lands C1–C4.** It is the prerequisite hardening so that a *future* Rung-2 attempt
(expected Cycle-006 or later) can run an admission gate through a validator that has itself been reviewed and
audited in a load-bearing posture.

**Mission (binding).** Specify, for one focused hardening sprint to be implemented under a later build gate,
the C1–C4 hardenings of `analysis/evidence_summary.py` and their regression tests in
`tests/test_evidence_summary.py`, so that: (a) a nested `hashes` map cannot smuggle a non-digest token past the
validator (C1); (b) the forbidden-word negation heuristic no longer suppresses unrelated affirmative use (C2);
(c) the `--out` tracked-path guard is repo-root-resolved (C3); (d) an empty `hashes` integrity stamp is no
longer silently treated as strong provenance (C4). The validator becomes **strictly more conservative, not
looser**; existing generator behaviour stays compatible unless the SDD explicitly justifies a change; the 12
existing checks remain green; and **Rung 1 holds, `docs/ledger.md` stays byte-unchanged, and no value is
promoted.**

**Who consumes this PRD.** The **operator** (accepts this PRD; opens the later build gate; the only party who
may ever issue SP-6, choose `M`, or advance the ceiling — none in Cycle-005); the **architect/sprint-planner**
(`/architect`, `/sprint-plan`, who resolve the SDD-level decisions named in §12); the **implementer**
(`/implement`, single patch authority, who lands C1–C4 and re-validates citations against the build-time HEAD);
and the **reviewer/auditor** (`/review-sprint`, `/audit-sprint`) who must be able to review and audit the
hardened gate **before** any Rung-2 attempt.

## 2. Problem statement

The evidence-summary validator exists (Cycle-004) but is **not yet trustworthy as a load-bearing promotion
gate**. Four reproduced gaps, grounded in the current module source, are open:

1. **Positional smuggling (C1).** `validate_summary` applies the SHA-256 digest-shape check **only to the
   top-level `hashes`** (`analysis/evidence_summary.py:369-379`), while `SAFE_FIELDS` is a **flat field-name
   allow-list** (`:83-88`) and `_walk` treats keys under any `hashes` key as *data* at any nesting depth
   (`:333-350`, esp. `:344`). A nested `hashes` map (e.g. under an agent) carrying a clean, non-digest token is
   scanned only by `_scan_string` (`:318-330`) — which catches path/inferential/forbidden-word/cross-regime
   tokens but **not** a clean non-digest token — so it passes. Reproduced by the audit
   (`docs/cycles/cycle-004/06-audit-report.md` §7 C1).
2. **Negation-window evasion (C2).** `_affirmative_forbidden_words` (`:298-306`) suppresses a forbidden word if
   **any** negation token appears within a 36-char window before it (`_NEG_WINDOW = 36`, `:263`) — even an
   unrelated one. An affirmative forbidden agent-quality word can therefore slip past in a hand-edited summary.
3. **Absolute-path guard gap (C3).** `_refuse_tracked_out` tests a normalized-but-not-repo-resolved path
   (`:410-421`; `_norm_path` `:282-283`); an **absolute** path into the repo's `docs/` for a non-`ledger.md`
   file slips the docs check (the `ledger.md` basename check still catches the ledger on any path).
4. **Silent empty hashes (C4).** `_manifest_run_hash` returns `None` when no SHA-256-shaped `*_hash` is present
   (`:117-132`); `hashes[run_id]` is then never set (`:181-182`), so `hashes` degrades to `{}` **silently**,
   which `validate_summary` accepts as clean (`:369-370`). A missing integrity stamp is invisible — yet a future
   Rung-2 row cites a promoted summary **by reference + content hash**
   (`docs/cycles/cycle-003/06-rung-2-ledger-convention.md` §3).

None of these is an admission problem; all are **gate-trust problems**. Until C1 in particular is fixed,
reviewed, and audited, the validator cannot be trusted to gate a human-promoted (possibly hand-edited) summary.
Cycle-005 closes these gaps; it does **not** cross the admission seam.

## 3. Goals — what Cycle-005 must produce

This is a **planning PRD for one hardening sprint**; the goals below are specified for implementation under a
later build gate, not implemented by this PRD.

- **G1 — C1 positional hardening specified (priority).** The validator must enforce the digest-shape rule on
  **every** `hashes`-keyed dict regardless of nesting position, or move to a stricter positional/structural
  schema (either is acceptable; the SDD decides — §12). This is the hard blocker for any future promotion.
- **G2 — C2 negation hardening specified.** The forbidden-word negation heuristic is tightened
  (immediate-precedence negation, or an equivalently tighter rule) so an unrelated negation no longer suppresses
  an affirmative forbidden word — while legitimate negated/forbidden-language examples in reports remain valid.
- **G3 — C3 `--out` guard specified.** The `--out` tracked-path guard resolves against the repo root before the
  `docs/` prefix check; `docs/ledger.md` remains independently protected and byte-unchanged.
- **G4 — C4 empty-hashes handling specified.** An empty `hashes` is no longer silently accepted as strong
  provenance; manifest-only sourcing remains the authorized read surface (no `hashes.txt` read).
- **G5 — Regression tests specified.** Each of C1–C4 leaves at least one runnable check that fails if the
  hardening regresses; the 12 existing checks remain green.
- **G6 — Conservative-only, compatible.** The validator becomes **strictly more conservative, not looser**;
  existing generator behaviour stays compatible unless the SDD explicitly justifies a change.
- **G7 — Rung 1 held; ledger byte-unchanged; no value promoted (hard).** Across the whole cycle the ceiling
  stays Rung 1, `docs/ledger.md` stays byte-unchanged, `docs/claim-ceiling.md` is unchanged, and no value
  reaches tracked status.

## 4. Non-goals (explicit)

Cycle-005 does **not** do any of the following:

- **No Rung-2 attempt** and **no Rung-2 admission**; **no "beats random-legal" verdict.**
- **No Rung-2 ledger row;** `docs/ledger.md` byte-unchanged.
- **No claim-ceiling advance;** `docs/claim-ceiling.md` unchanged.
- **No numeric margin `M`** chosen anywhere.
- **No SP-6** live-value promotion; no dispersion value promoted to tracked status.
- **No OD-6 decision / relaxation;** no inferential statistic computed.
- **No same-regime evidence verdict** of any kind.
- **No new eval runs; no K=50 top-up; no K expansion; no paired-delta tooling.**
- **No runtime-agent implementation;** agents stay frozen.
- **No gameplay-heuristic work;** no broad optimization (RL, self-play, deck optimizer, value/win-probability
  model, search/MCTS, ELO/tournament, dashboard, leaderboard).
- **No Daily Top Episodes ingestion;** no Kaggle automation.
- **No FunSearch work** (no dependency, interface, scaffold, integration, or candidate-search surface).
- **No report-track narrative expansion** beyond the risk/constraint references this PRD requires.
- **No broad refactor of TurnTrace;** the only tracked code touched is the two evidence-summary artifacts.
- **No change to `.claude/`** (System Zone).
- **No State-Zone cleanup;** pre-existing dirty State-Zone files stay unstaged and untouched.
- **No new module** (`analysis/evidence_summary_validate.py`), **no `*.schema.json` file**, **no third-party
  dependency** — the in-module constant and stdlib-only posture are preserved.

## 5. Functional requirements

All four are **hardening** requirements against the current `analysis/evidence_summary.py`, grounded in the
Cycle-004 audit carry-forwards (`docs/cycles/cycle-004/06-audit-report.md` §9) and the Cycle-003 design
authorities (docs 04, 05). Architecture-level choices are deferred to the SDD (§12); the FRs state **what** must
hold, not the exact mechanism.

### C5-FR-1 — Positional digest-shape / allow-list hardening (C1) — **PRIORITY hard blocker**

The validator MUST close the positional smuggling gap so a known field name in a non-schema position cannot
bypass content checks:

1. The current **flat field-name allow-list** (`SAFE_FIELDS`, `:83-88`) admits `hashes` as an accepted key at
   any nesting depth, while the digest-shape rule runs **top-level only** (`:369-379`) — a positional blind
   spot. A nested `hashes` map carrying a clean, non-digest token currently passes.
2. The hardened validator MUST ensure **nested `hashes` maps cannot bypass digest-shape checks**: every
   `hashes`-keyed dict, regardless of position, has its values enforced to SHA-256 digest shape (or fails
   closed, exit 3).
3. The fix MAY be either (a) **apply digest-shape validation to every `hashes`-keyed dict during traversal**, or
   (b) **move toward a stricter positional/structural schema**. Both are acceptable; the **exact architecture is
   for the SDD, not this PRD** (§12).
4. This requirement **blocks any future value promotion until it is fixed, reviewed, and audited** — it is the
   hard prerequisite for the validator becoming load-bearing.

### C5-FR-2 — Forbidden-word negation hardening (C2)

The validator MUST tighten the forbidden-word negation heuristic:

1. The current broad negation window (`_NEG_WINDOW = 36`, `:263`; `_affirmative_forbidden_words`, `:298-306`)
   can suppress an affirmative forbidden-word flag because of an **unrelated** negation token nearby.
2. The hardened rule SHOULD prefer **immediate-precedence negation** (or an equivalently tighter rule) so only a
   genuine negation of the word suppresses the flag.
3. It MUST **preserve legitimate negated/forbidden-language examples** in reports (e.g. "NO strength claim",
   validator-rejection examples) — these remain valid.
4. It MUST **never admit an affirmative agent-quality claim** using any of the five forbidden words
   (*strong / competitive / optimal / calibrated / complete*; `docs/claim-ceiling.md:54-59`).

### C5-FR-3 — `--out` repo-root guard (C3)

The generator MUST harden its tracked-path write guard:

1. Relative `docs/` writes are guarded now; an **absolute** path into the repo's `docs/` (for a non-`ledger.md`
   file) has a defense-in-depth gap (`_refuse_tracked_out`, `:410-421`; `_norm_path`, `:282-283`).
2. The hardened guard MUST **repo-root-resolve `--out` before the tracked-docs prefix check**, so generated
   outputs cannot be written into tracked docs locations by absolute-path trickery.
3. `docs/ledger.md` remains **independently protected** (the basename guard) and MUST remain **byte-unchanged**.
   The primary control — `git diff --exit-code -- docs/ledger.md` byte-unchanged — is independent of this guard
   and continues to hold.

### C5-FR-4 — Empty-hashes handling (C4)

The generator/validator MUST stop treating a silently-empty integrity stamp as strong provenance:

1. **Manifest-only hash sourcing remains the authorized read surface** (`_manifest_run_hash`, `:117-132`); the
   cycle MUST **not** read an unauthorized `hashes.txt` (SDD §3.1/§8 read surface).
2. An **empty `hashes` MUST NOT silently pass** as if provenance were strong: the generator warns (and/or a
   future promotion mode fails) when `hashes` is empty.
3. The **exact behaviour — warning-only in normal validate mode vs. a stricter promotion-mode failure — is
   resolved in the SDD** (§12). The binding floor: **no promotion mode may trust a summary with silently empty
   hashes.**

## 6. Non-functional requirements / technical posture

- **NFR-1 — Conservative-only.** Every change makes the validator **stricter or equal**, never looser. A change
  that would accept something the current validator rejects is out of scope unless the SDD explicitly justifies
  it as required by a C1–C4 fix.
- **NFR-2 — Compatibility.** Existing generator behaviour and emitted shape stay compatible; the **12 existing
  checks remain green**. New behaviour is additive (new regression checks + stricter rejections).
- **NFR-3 — Stdlib-only / analysis-only imports preserved.** No `cabt`/`cg`, `sim/`, `agents/runtime/`, or
  `eval/` import; no third-party dependency; the in-module allow-list stays the single source of truth (no
  `*.schema.json`, no second module). Enforced by `tests/test_import_direction.py`.
- **NFR-4 — Read/write surface unchanged.** Read surface stays `manifest.json` + `match_results/*` (via
  `aggregate_run`) + the `--validate` file; no sidecar/`traces/` reference is introduced; the structural
  no-sidecar guarantee holds. Write surface stays local-by-default; never `docs/`, never a ledger row.
- **NFR-5 — Same-regime only.** The single-regime guard (exit 2) is preserved; no cross-regime field or
  comparison is introduced.
- **NFR-6 — Claim-safety.** Rung 1 held; forbidden agent words negated-only; no inferential result produced (the
  validator *rejects* inferential terms; C2 strengthens, never weakens, this).
- **NFR-7 — Sanitization.** Competition Data and Pokémon Elements never enter git (CC-1/CC-2, ESP);
  `eval/hygiene_check.py` remains the staging gate; the validator stays sanitization-parity-or-stricter (C1–C4
  only strengthen it).
- **NFR-8 — Simulator-authoritative (SP-8 / CC-10).** Any verdict-relevant logic follows simulator-offered
  legal options and the simulator terminal result, never official-rule assumptions. (No verdict logic is built
  this cycle; this is a standing constraint carried into the design.)
- **NFR-9 — Implement-time citation revalidation.** The C1–C4 anchors in this PRD are line-anchored to
  `analysis/evidence_summary.py` at HEAD `337fc4f`. `/implement` MUST re-validate every anchor it relies on
  against the **build-time HEAD** before coding; anchors accurate now may desync if the file moves.
- **NFR-10 — Zone discipline.** Build code is tracked App Zone (`analysis/`, `tests/`); the PRD is Docs/State
  Zone; `.claude/` is never touched; State-Zone files stay unstaged.

## 7. Hardening detail (C5-FR-1 … C5-FR-4)

> This section restates the four hardenings as the binding framing the SDD must honour. It introduces no new
> requirement beyond §5; it fixes the language so the SDD does not relitigate the intent.

- **C1 — positional digest-shape (priority).** Today the allow-list is flat and the digest-shape check is
  top-level only, so a nested `hashes` map is a smuggling seam. The hardened validator treats digest-shape as a
  property of **every** `hashes`-keyed dict (traversal-based enforcement) **or** adopts a positional/structural
  schema. Exact architecture → SDD. **Blocks promotion until fixed, reviewed, audited.**
- **C2 — negation hardening.** Today a broad 36-char window lets an unrelated negation suppress an affirmative
  forbidden word. The hardened rule uses immediate-precedence (or tighter) negation, preserves legitimate
  negated/forbidden-language examples, and never admits an affirmative quality claim.
- **C3 — `--out` repo-root guard.** Today an absolute path into repo `docs/` slips the docs prefix check. The
  hardened guard repo-root-resolves `--out` first; the ledger stays independently protected and byte-unchanged.
- **C4 — empty-hashes.** Today an empty `hashes` passes silently. The hardened behaviour warns (and/or fails in
  a future promotion mode); manifest-only sourcing is preserved; no `hashes.txt` read; no promotion mode trusts
  silently-empty hashes. Warning-vs-failure split → SDD.

## 8. Why Rung 2 is deferred

Cycle-005 deliberately does **not** attempt Rung 2. The reasons (from the pre-PRD research,
`grimoires/loa/a2a/cycle-005/00-pre-prd-research.md` T3/T5, and the tracked authorities):

1. **The validator has known hardening gaps from the Cycle-004 audit** (C1–C4); it has never been reviewed or
   audited in a load-bearing posture.
2. **C1 is a hard blocker before any promotion.** Running an admission gate through a validator with an open
   positional smuggling seam is exactly backwards; the hardening must land, be reviewed, and be audited first.
3. **The existing K=20+20 summary has already been locally generated** (the Cycle-004 local exercise ran the
   generator over exactly those sealed run dirs; `docs/cycles/cycle-004/04-implementation-report.md` §4 T6). The
   bands are therefore already locally accessible, so **using that set to choose `M` now risks post-hoc
   thresholding** — the precise "threshold chosen after seeing the numbers" failure that pre-registration exists
   to prevent (`docs/cycles/cycle-003/07-od6-criterion-2-proposal.md` §3).
4. **The Rung-2 seam decisions 8a–8d remain governance decisions** the operator owns (8a disjoint-bands-vs-OD-6,
   8b numeric `M`, 8c SP-6, 8d Rung-2 row / ceiling-advance; `docs/cycles/cycle-003/07-od6-criterion-2-proposal.md`
   §5), and a Rung-2 *consideration* requires **all five** conjunctive readiness criteria
   (`docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` §2).
5. **Cycle-005 should make the gate trustworthy first** — build readiness, then advance as a separate explicit
   decision.
6. **Cycle-006 or later may attempt Rung 2 only after** Cycle-005 passes review/audit **and** an explicit
   operator gate opens (and the seam decisions 8a–8d are resolved with a defensible pre-registration of `M`).

## 9. Competition-findings integration (the `337fc4f` docs-only patch)

Cycle-005 consumes the pushed competition-findings patch (operator decisions SP-8/SP-9; failure modes
FM-10/FM-11; `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md`; `docs/failure-modes.md`) as **planning
constraints and active risks** — it does **not** expand Cycle-005 scope:

- **Simulator legal options and simulator terminal results are authoritative** (SP-8 / CC-10). Official-rule
  assumptions **must not** override simulator behavior in any analysis or future verdict logic.
- **Daily Top Episodes are local-only scouting / training / report input** (SP-9 / CC-6). **Raw top episodes
  stay ignored/local;** they **generate hypotheses only** and are **never Rung-2 proof** without a same-regime
  TurnTrace comparison.
- **FM-10 (official-rule assumption mismatch)** and **FM-11 (top-episode overfitting / contaminated evidence)**
  are **active risks** carried into §15. FM-11's raw-data-in-git leg is already mechanically caught by
  `eval/hygiene_check.py` and the validator's hygiene-parity path rules (`analysis/evidence_summary.py:231-241`)
  — C1–C4 only strengthen the content gate.
- **No scope expansion because of Daily Top Episodes.** Cycle-005 ingests none and builds nothing for them.

## 10. Claim-ceiling posture

The loop sits at **ladder Rung 1 — legal completion / throughput / audit-trail**, and **Cycle-005 keeps the
ceiling at Rung 1** for the whole cycle (`docs/claim-ceiling.md`):

```
Rung 0  env not trusted
Rung 1  legal completion                         ← current, and held for all of Cycle-005
Rung 2  beats random-legal                       ← gate HARDENED here; never claimed; admission = a later gate (Cycle-006+)
Rung 3  beats scripted / prior best, ablation-backed
Rung 4  stable, report-ready
```

**Allowed claim form** — relative, local, descriptive, carrying its `n`, `K`, and `regime_id`. **Forbidden
claim forms** (negated-only): gameplay strength; statistical significance; cross-regime uplift; leaderboard
quality; calibration; optimality; competitiveness. Only the ledger, advanced by a separate explicit later
operator decision, can carry a higher rung. **Cycle-005 advances nothing; it hardens the tool a later gate
would use.**

## 11. Safety and sanitization constraints

Carried verbatim-in-intent from the standing rules (`docs/operator/turntrace-loop-contract.md` §7-§8;
`docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` SP-6/SP-8/SP-9):

- **Competition Data never enters git** (CC-1/CC-2): the `cg/` SDK, card data, raw deck lists, `deck.csv` —
  local-only under gitignored `grimoires/loa/context/`.
- **Pokémon Elements never appear in tracked artifacts.**
- **Generated runs, dispersion values, and the generator's output** stay local/gitignored; tracked artifacts
  hold sanitized code + specs only.
- **Daily Top Episodes / raw episode datasets** stay local/ignored (SP-9, same ESP discipline); never tracked,
  never a runtime dependency.
- **`eval/hygiene_check.py`** remains the mechanical staging gate; the built validator stays
  sanitization-parity-or-stricter with it (C1–C4 only strengthen it).
- **Forbidden agent claim words** appear only as negated/forbidden language.

## 12. Open decisions deferred to SDD

Named here, **not** decided in this PRD:

- **OD-C5-1 — C1 mechanism.** Whether C1 is implemented as a **full positional/structural schema** or as
  **traversal-based nested-`hashes` digest-shape enforcement**. Both satisfy C5-FR-1; the SDD chooses.
- **OD-C5-2 — empty-hashes severity.** Whether empty `hashes` is **warning-only in normal `--validate` mode but
  blocking in a future promotion mode**, or stricter. The SDD decides the split (floor: no promotion mode trusts
  silently-empty hashes).
- **OD-C5-3 — promotion-mode shape.** Whether a future **`--promotion-check` mode** is introduced, or whether
  the existing **`--validate` should simply become stricter**. (No promotion is performed this cycle; this names
  the eventual shape only.)
- **OD-C5-4 — test layout.** The exact layout/placement of the new C1–C4 regression checks within
  `tests/test_evidence_summary.py`.
- **OD-C5-5 — CLI exit behaviour for warnings.** The exact exit-code behaviour for warning cases (e.g.
  empty-hashes warning) vs. the existing `0/1/2/3` contract.
- **OD-C5-6 — carry-forward documentation language.** The exact documentation/reporting language for the C1–C4
  carry-forwards in the implementation/review/audit artifacts.
- **Reaffirmed (not decided in Cycle-005):** `M` unset; SP-6 not issued; OD-6 not relaxed; Rung-2 admission =
  a separate later gate — the four seam decisions 8a–8d stay open.

## 13. Operator / product decisions recorded

| ID | Decision | Status |
|---|---|---|
| **Build gate (OA-2-class)** | The operator opens the later build gate for Cycle-005 implementation, scoped to the C1–C4 hardening of the two evidence-summary artifacts only (`docs/operator/turntrace-loop-contract.md` §6). | **Required to proceed to `/implement`** — operator action after SDD/sprint-plan; this PRD does not self-authorize. |
| **D-1** | Cycle-005 = **hardening-only**; the only tracked code touched is `analysis/evidence_summary.py` + `tests/test_evidence_summary.py`. | **Decided.** |
| **D-2** | The validator becomes **strictly more conservative, not looser**; existing behaviour stays compatible unless the SDD explicitly justifies a change. | **Decided.** |
| **D-3** | **Rung-2 admission deferred** to a later explicit gate (expected Cycle-006 or later); seam 8a–8d untouched. | **Decided.** |
| **D-4** | **In-module constant / stdlib-only / one-module** posture preserved (no `.schema.json`, no second module, no dependency). | **Decided.** |
| **`M` / SP-6 / Rung-2 row / OD-6** | Unset / not issued / not written / not relaxed. | **Deferred** to the later admission gate — **none in Cycle-005**. |

## 14. Success criteria

### 14.1 Planning-cycle success (this PRD)

- This PRD is accepted by the operator and proceeds to `/architect` (SDD), not directly to implementation.
- It specifies C1–C4 (C5-FR-1…C5-FR-4) as a small, testable hardening scope, records decisions D-1…D-4, names
  the SDD-deferred decisions (OD-C5-1…6), and states the Rung-2 deferral and competition-findings integration.
- Rung 1 is held; `docs/ledger.md` is byte-unchanged; `docs/claim-ceiling.md` is unchanged; no value is
  promoted; no raw data is committed; `.claude/` is untouched; State-Zone files stay unstaged.

### 14.2 Build-cycle acceptance criteria (when the code lands under `/implement`, a later gate)

- **AC-1 — C1 (priority):** a **nested** `hashes` map carrying a clean non-digest token is **rejected**
  (fail-closed, exit 3); digest-shape is enforced at every position (or via a positional/structural schema).
- **AC-2 — C2:** an unrelated negation no longer suppresses an affirmative forbidden word; a genuine negation
  (and legitimate negated/forbidden-language examples) still validate; no affirmative quality claim is admitted.
- **AC-3 — C3:** an absolute path into repo `docs/` (non-ledger) is **refused**; `docs/ledger.md` byte-unchanged.
- **AC-4 — C4:** an empty `hashes` is **not silently accepted** (warns, and/or fails in promotion mode per the
  SDD); manifest-only sourcing preserved; no `hashes.txt` read.
- **AC-5 — Tests:** each of C1–C4 has at least one runnable regression check; **all existing 12 checks remain
  green**; `tests/test_import_direction.py` green; `eval/hygiene_check.py --paths …` exit 0 on tracked artifacts.
- **AC-6 — Conservative-only / compatible:** the validator is strictly stricter-or-equal; generator behaviour
  stays compatible unless the SDD justified a change.
- **AC-7 — Posture held (hard):** Rung 1 held; `docs/ledger.md` byte-unchanged (`2a2f1c2…`);
  `docs/claim-ceiling.md` unchanged; no value promoted; stdlib-only / analysis-only imports; no `M`/SP-6/Rung-2
  row; no `.claude/` drift; State-Zone files unstaged; no second module / `.schema.json` / dependency.
- **AC-8 — Cadence:** lands through `/implement → /review-sprint → /audit-sprint → operator acceptance`, so the
  hardened gate is **reviewed and audited before any Rung-2 attempt**.

## 15. Risks and mitigations

| ID | Risk | Mitigation |
|---|---|---|
| **R1** | **C1 fix loosens the gate** (a restructure accidentally accepts something previously rejected). | NFR-1 conservative-only; keep the 12 existing checks green (AC-5); add the nested-`hashes` rejection check (AC-1). |
| **R2** | **Scope-creep into admission** — hardening drifts into a verdict / `M` / promotion. | §4 non-goals; §8 deferral; no `M`/SP-6/Rung-2 row; seam 8a–8d untouched. |
| **R3** | **Citation rot** — the C1–C4 line anchors desync from source before build. | NFR-9: `/implement` re-validates anchors at build-time HEAD. |
| **R4** | **C2 over-tightening** — a legitimate negated/forbidden-language example in a report is wrongly flagged. | C5-FR-2.3 preserves legitimate examples; regression check for "NO strength claim" and validator-rejection examples. |
| **R5** | **Ledger / docs mutation** via the generator's `--out`. | C5-FR-3 repo-root guard; ledger basename guard; `git diff --exit-code -- docs/ledger.md` byte-unchanged (AC-3/AC-7). |
| **R6** | **Dependency / second-module / `.schema.json` creep** during the C1 restructure. | NFR-3; §4 non-goals; import-direction test; in-module constant preserved. |
| **R7** | **FM-10 (official-rule assumption mismatch).** | NFR-8 simulator-authoritative; no verdict logic built; record any divergence as a simulator-behavior note, not an agent failure. |
| **R8** | **FM-11 (top-episode overfitting / contaminated evidence).** | §9/§11: no episode ingest; episodes are hypothesis-only; raw-data-in-git mechanically caught by `eval/hygiene_check.py` + validator hygiene parity. |
| **R9** | **Pre-registration contamination** if a later cycle reuses the already-generated K=20+20 bands to choose `M`. | §8.3 flags it; deferral to Cycle-006+ with a defensible pre-registration is the mitigation (out of scope here). |

## 16. Sources and traceability

> **Local decision input (gitignored State Zone, not a tracked dependency):**
> `grimoires/loa/a2a/cycle-005/00-pre-prd-research.md` (the pre-PRD research pass; recommends hardening-only,
> Rung-2 deferred).
> **Tracked Cycle-004 carry-forwards:** `docs/cycles/cycle-004/06-audit-report.md` (§7 C1–C4 reproduced, §9
> carry-forwards); `docs/cycles/cycle-004/05-review-report.md` (§9 C1–C3, §10 minor notes);
> `docs/cycles/cycle-004/07-closeout.md` (§8 carry-forwards, Rung 1 held);
> `docs/cycles/cycle-004/04-implementation-report.md` (§4 T6 local exercise on the K=20+20 dirs);
> `docs/cycles/cycle-004/01-prd.md`, `02-sdd.md`, `03-sprint-plan.md` (the build this cycle hardens).
> **Tracked code (the hardening target, anchors at `337fc4f`):** `analysis/evidence_summary.py`
> (`SAFE_FIELDS` `:83-88`; `_manifest_run_hash` `:117-132`; `build_summary` hashes set `:181-182`;
> `_norm_path` `:282-283`; `_affirmative_forbidden_words` `:298-306` + `_NEG_WINDOW` `:263`; `_walk` `:333-350`;
> `validate_summary` digest-shape `:369-379`; `_refuse_tracked_out` `:410-421`; hygiene path rules `:231-241`);
> `tests/test_evidence_summary.py` (the 12 checks).
> **Tracked Cycle-003 design authorities:** `04-evidence-summary-schema-spec.md` (§2 safe fields, §3 forbidden
> classes); `05-generator-validator-shape.md` (§2 allow-list / single-regime / exit codes / hygiene parity);
> `06-rung-2-ledger-convention.md` (§3 row cites summary by reference + hash); `07-od6-criterion-2-proposal.md`
> (§3 pre-registration, §5 seam 8a–8d); `08-funsearch-forward-compat.md` (NG10).
> **Tracked posture docs:** `docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` §2 (five conjunctive
> criteria); `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` (SP-6/SP-8/SP-9);
> `docs/failure-modes.md` (FM-10/FM-11); `docs/claim-ceiling.md` (Rung 1; forbidden words);
> `docs/ledger.md` (two Rung-1 rows; hash `2a2f1c2…`); `docs/operator/turntrace-loop-contract.md`
> (§6 build gate; §7-§8 hygiene/claim language); `docs/operator/cycle-005-planning-inputs.md` (carry-forward
> index).
> Current main at authoring: `337fc4f`. Claim ceiling: **Rung 1 (unchanged).** This PRD opens no implementation
> gate, builds no code, mutates no ledger, advances no ceiling, promotes no value, and edits no `.claude/`.
