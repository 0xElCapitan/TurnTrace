# Cycle-004 PRD — OA-2 Build: Offline Evidence-Summary Generator + Validator

> Planning artifact (PRD). Status: **DRAFT — awaiting operator acceptance.** This PRD specifies a
> **build** cycle, but the PRD itself **opens no implementation gate**: building lands only through
> `/architect → /sprint-plan → /implement → /review-sprint → /audit-sprint → operator acceptance`
> (`docs/operator/turntrace-loop-contract.md` §6). Cycle-004 is the **OA-2 build** the Cycle-003 SDD
> deferred (`docs/cycles/cycle-003/02-sdd.md:485,505` OD-C3-6); the operator opening OA-2 authorizes
> relaxing **exactly one** Cycle-003 non-goal — **NG5** ("no code built", `docs/cycles/cycle-003/01-prd.md:151`).
> Every other Cycle-003 non-goal stays binding.
> Binding planning input: the local pre-PRD research pass (`grimoires/loa/a2a/cycle-004/pre-prd-research.md`,
> gitignored State Zone — research input, **not** authority) and the tracked Cycle-003 design authorities
> (docs 04–08). Substantive citations point to **tracked** artifacts so this PRD is self-grounded.
>
> Sanitized note. No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, or Competition Data appear here (CC-1/CC-2, ESP).
> **No dispersion metric values appear here** — local evidence is referenced qualitatively only and its
> values stay local/gitignored. Runs are referenced by `run_id`, hashes, sanitized metric *names*, claim
> ceilings, and local path/status only. The forbidden agent words (*strong / competitive / optimal /
> calibrated / complete*) and the inferential terms (*std-dev / variance / CI / p-value / significance /
> hypothesis-test / error-bar*) appear only as the negated/forbidden language they are.

## 0. State verified (2026-06-19, before drafting)

| Assumption to verify | Result |
|---|---|
| Current HEAD / branch | `main` @ `73c13ee` — *docs: complete TurnTrace Cycle-003 Sprint 00 specs* (Cycle-003 closed) |
| `docs/ledger.md` unchanged from Cycle-003 close | **byte-unchanged**; `git diff --exit-code` clean; `hash-object = 2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` (Cycle-003 baseline) |
| Claim ceiling still Rung 1 | **Rung 1** (`docs/claim-ceiling.md`) |
| No `analysis/evidence_summary*.py` / `.json` exists | **absent** — Cycle-003 built no code |
| No staged files | **none staged** |
| `.beads/issues.jsonl`, `grimoires/loa/NOTES.md` dirty | both modified, **unstaged** (pre-existing State-Zone housekeeping); not staged/committed by this cycle |
| `.claude/` untouched | **no drift**; `integrity_enforcement: strict` → no HALT |
| Local sealed K-batch run dirs present (for the §10 exercise) | **present** — `runs/run-v002-b-1..20` + `runs/run-v002-c-1..20` (40 dirs, gitignored) → the local end-to-end exercise is feasible this checkout |

**All assumptions hold. No finding forces a stop.** Implementation remains un-authorized until the
operator accepts this PRD and proceeds through `/architect → /sprint-plan → /implement`.

| Field | Value |
|---|---|
| **Cycle** | Cycle-004 |
| **Working title** | OA-2 Build: Offline Evidence-Summary Generator + Validator |
| **Alt. framing** | Build the bridge specified by Cycle-003 docs 04 + 05 — do **not** cross the admission seam |
| **Type** | Product Requirements Document (planning artifact for a build cycle) |
| **Status** | DRAFT — awaiting operator acceptance; next Golden-Path step is SDD / architecture |
| **Date** | 2026-06-19 |
| **Current main** | `73c13ee` — *docs: complete TurnTrace Cycle-003 Sprint 00 specs* |
| **Binding input** | local pre-PRD research pass (gitignored) + Cycle-003 docs 04–08 + Cycle-003 `01-prd.md`/`02-sdd.md` |
| **Posture** | **Build-only.** Relax NG5 only; build the generator/validator/tests; hold every other bright line |
| **Claim ceiling** | **Rung 1** (held for the whole cycle; not raised) |

## Required posture (binding)

- **Cycle-004 is build-only.** It builds the offline evidence-summary generator, its independent
  fail-closed validator, the in-module machine-checkable schema constant, the test suite, and runs a
  **local** end-to-end exercise. It builds **nothing else**.
- **NG5 is the only Cycle-003 non-goal relaxed.** Building the generator/validator/tests is sanctioned
  under OA-2 (`02-sdd.md:485,505`). NG1–NG4 and NG6–NG13 (`01-prd.md:145-171`) **all remain binding** —
  the build crosses no other line, because the generator writes **local-by-default** and the validator
  promotes nothing.
- **The claim ceiling remains Rung 1** for all of Cycle-004 (`docs/claim-ceiling.md:5-6`). No
  "beats random-legal" verdict; no Rung-2 claim.
- **No value is promoted to tracked status.** SP-6 is **not** issued (NG4); the generator's output and any
  evidence values stay local/gitignored. Promotion is a separate later operator decision.
- **`docs/ledger.md` is byte-unchanged.** No `run-v002` / Rung-2 row is written; the ledger remains the
  only ceiling-bearing artifact (NG3; `docs/ledger.md:1-8`).
- **No numeric margin `M` is chosen; OD-6 is not relaxed; no inferential statistic is computed** (NG6;
  `docs/cycles/cycle-002/07-operator-decision-register.md` §2). The validator *rejects* inferential terms;
  it does not produce them.
- **Rung-2 admission is a separate, later, explicit gate — expected Cycle-005.** Building the machinery
  does not admit Rung 2; the four conjunctive seam decisions (8a disjoint-bands-vs-OD-6, 8b `M`, 8c SP-6,
  8d Rung-2 row/ceiling-advance; `docs/cycles/cycle-003/07-od6-criterion-2-proposal.md` §5) remain open
  by design and are decided **only** at that later gate.
- **The runtime-agent lane and broad-optimization lane stay closed** (NG7, NG8); **no FunSearch**
  dependency/scaffold/surface (NG10); **no `regime` mutation, no cross-regime comparison** (NG11); **no
  evidence hardening** — no new eval runs, no K=50 top-up, no paired-delta tooling (NG12).
- **`.claude/` (System Zone) is never edited.** Build code is App Zone (`analysis/`, `tests/`); the PRD is
  State/Docs Zone.

**The bright line for the whole cycle:** *Cycle-003 specified the schema (doc 04) and the
generator/validator shape (doc 05) without building; Cycle-004 builds exactly those two — an
`analysis/`-class offline generator + independent fail-closed validator that turns existing local sealed
run dirs into a sanitized, JSON-first, schema-conforming K-batch evidence summary and validates it
mechanically — while holding Rung 1, leaving `docs/ledger.md` byte-unchanged, promoting no value, and
stopping short of the admission seam.*

## 1. Product / cycle overview

TurnTrace is a local, sanitized evaluation harness for a card-game simulator. Cycle-003 ("Rung-2
Admission Readiness", `01-prd.md`) produced five tracked design authorities at Rung 1 and built **no
code** (NG5): the evidence-summary **schema spec** (doc 04), the **generator/validator shape** (doc 05),
the **Rung-2 ledger-row + verdict convention** (doc 06), the **OD-6/criterion-2 resolution proposal**
(doc 07), and a **FunSearch forward-compat appendix** (doc 08). The Cycle-003 SDD placed the eventual
build behind a fresh OA-2 gate: *"Generator + validator code … Created only in the later build cycle"*
and *"Machine-readable schema artifact … `analysis/evidence_summary_schema.json` **or an in-module
constant** … Created only in the later build cycle"* (`02-sdd.md:170-172`).

**Cycle-004 is that later build cycle.** The confidence evidence behind any future Rung-2 verdict — the
cross-batch dispersion of sanitized aggregate metrics — currently lives **only** in local/gitignored
files (`01-prd.md:73-76`). Cycle-003 specified the safe shape for a tracked sanitized summary of that
evidence; Cycle-004 makes that specification real as runnable tooling, so that a future Rung-2 admission
becomes "fix `M`, run the built generator on existing local runs, validate, promote one cited summary,
append one ledger row" — a clean, pre-specified operator decision — without Cycle-004 itself taking any
of those irreversible steps.

**Mission (binding).** Build, under OA-2 and through the full `/implement → /review-sprint →
/audit-sprint` cadence: (a) an `analysis/`-class offline **generator** (`analysis/evidence_summary.py`)
that reads existing local sealed run dirs and emits a JSON-first, schema-conforming, sanitized K-batch
evidence summary; (b) an **independent, fail-closed validator** (a `--validate` mode over a re-read
summary file) that mechanically enforces doc 04 §3's forbidden-field/content classes; (c) the
**in-module machine-checkable allow-list constant** that is the schema artifact; (d) a **test suite** that
proves every required property; and (e) a **local end-to-end exercise** on the existing K=20+20 run dirs
that demonstrates the pair works and promotes nothing. Hold Rung 1; leave `docs/ledger.md` byte-unchanged;
choose no `M`; promote no value.

**Who consumes this PRD.** The **operator** (opens OA-2, accepts this PRD, decides whether to proceed to
SDD; the only party who may later issue SP-6, choose `M`, or advance the ceiling — none in Cycle-004); the
**implementer** (`/implement`, single patch authority, who builds the generator/validator/tests and
re-validates the doc 04/05 citations against the build-time HEAD); the **reviewer/auditor**
(`/review-sprint`, `/audit-sprint`); and a future **Rung-2 admission reviewer / evaluator consumer** who
will read summaries the built tooling produces.

## 2. Problem statement

The Rung-2 admission machinery is fully **specified** (Cycle-003) but does not yet **exist** as tooling:

1. **The schema is a spec, not a checker.** Doc 04 §3 enumerates seven forbidden field-classes "intended
   for mechanical validator enforcement, not mere documentation" (`04-evidence-summary-schema-spec.md`
   §3) — but no validator exists, so the forbidden set is presently advisory.
2. **No generator exists to produce a conforming summary.** Doc 05 §1 specifies the generator's read
   surface, import boundary, and JSON-first output, but the cross-batch evidence still lives only in
   ephemeral local dispersion files (`01-prd.md:73-76`); there is no tool that emits the sanitized,
   schema-conforming summary a future verdict would cite.
3. **The doc↔code contract is unrealized.** The project's settled pattern is "a plain field-list is the
   design authority, and the machine-checkable form pairs with it" (`eval/schemas.md:1-4`); doc 04 is the
   authority but its paired machine-checkable form has not been built.
4. **Carry-forward risks flagged at Cycle-003 close are unaddressed in code.** The Cycle-003 review/audit
   flagged, for the build cycle: re-validate line-anchored citations at build time; code the benign
   `hypothesis` text-field exception (allow the ledger column, reject inferential hypothesis-tests);
   guarantee no-sidecar-read structurally; keep the ledger byte-unchanged and promote no value
   (`grimoires/loa/a2a/cycle-003/sprint-00/auditor-sprint-feedback.md` §"Risks/carry-forward";
   `…/engineer-feedback.md` §"Adversarial Analysis"). These must be handled by the build.

None of these is an admission problem; all are build problems. Building the bridge does **not** require
crossing the seam — it requires writing offline tooling that, by construction, promotes nothing.

## 3. Goals — what Cycle-004 must produce

- **G1 — Generator built.** `analysis/evidence_summary.py` reads existing local sealed run dirs
  (`manifest.json` + `match_results/*` via `analysis/aggregate.py:aggregate_run`), reuses the
  descriptive-stat helper (`analysis/dispersion_report.py:descriptive_stats` `:94-114`), and emits a
  JSON-first sanitized summary conforming to doc 04 §2/§4, written **local-by-default** via `--out`.
- **G2 — Independent fail-closed validator built.** A `--validate <summary.json>` mode that re-reads a
  summary file and rejects, allow-list/fail-closed, every doc 04 §3 forbidden class with a clear
  per-class reason; single-regime guard (exit 2); hygiene-parity superset of `eval/hygiene_check.py`.
- **G3 — In-module machine-checkable schema constant.** The safe allow-list as an in-module Python
  constant (reusing `DISPERSION_METRICS`/`STAT_COLUMNS`), which **must agree with doc 04 §2** (the
  `eval/schemas.md ↔ eval/validate.py` contract).
- **G4 — Test suite proves every required property** (§9): allow-list rejection, forbidden-content
  rejection, mixed-regime refusal, no-sidecar-read (structural), hygiene parity, no-ledger-mutation,
  no-value-promotion, benign `hypothesis` exception, doc↔schema agreement, JSON-first round-trip,
  sanitization, import-direction/stdlib-only.
- **G5 — Local end-to-end exercise.** Run the generator on the existing local K=20+20 run dirs to produce
  a **gitignored** validated summary, demonstrating the pair end-to-end while promoting nothing.
- **G6 — Rung 1 held; ledger byte-unchanged; no value promoted (hard).** Across the whole cycle the
  ceiling stays Rung 1, `docs/ledger.md` stays byte-unchanged, and no dispersion value reaches tracked
  status.

## 4. Non-goals — Cycle-004 relaxes NG5 only; all other Cycle-003 non-goals remain binding

The single relaxation:

- **NG5 (RELAXED under OA-2).** Cycle-003 built no code; Cycle-004 **builds** the generator, validator,
  in-module schema constant, and tests. This is the **only** relaxation and is scoped to those artifacts.

All other Cycle-003 non-goals (`01-prd.md:145-171`) **carry forward unchanged**:

- **NG1 — No Rung-2 admission.** No artifact asserts a "beats random-legal" verdict or any Rung-2 claim.
- **NG2 — No claim-ceiling advance.** Ceiling stays Rung 1; only the ledger, advanced by a separate later
  operator decision, can ever carry a higher rung.
- **NG3 — No `docs/ledger.md` mutation.** No Rung-2 row; byte-unchanged.
- **NG4 — No SP-6 issuance for live values.** No dispersion value is promoted to tracked status; the
  generator writes local-by-default; the exercise output stays gitignored.
- **NG6 — No numeric margin `M`; no inferential results.** `M` stays unset; OD-6 unrelaxed; the validator
  *rejects* inferential statistics, it does not compute them.
- **NG7 — No runtime-agent work.** Agents stay frozen; no runtime implementation or planning.
- **NG8 — No broad optimization.** No RL, self-play, deck optimizer, value/win-probability model,
  search/MCTS, ELO/tournament, dashboard, leaderboard/tuning loop.
- **NG9 — No Kaggle submission automation.**
- **NG10 — No FunSearch implementation/scaffolding.** No dependency, no integration, no heuristic surface.
- **NG11 — No `regime-v001`/`regime-v002` mutation; no cross-regime comparison.** Single-regime by
  construction (NFR-5).
- **NG12 — No evidence hardening.** No new eval runs, no K=50 top-up, no paired-delta tooling; the
  generator reads **existing** local runs only and runs no eval.
- **NG13 — No forbidden claims.** No gameplay-strength, statistical-significance, calibration,
  leaderboard, optimality, completeness, competitiveness, or cross-regime-uplift claim; forbidden agent
  words appear only as negated/forbidden language.

**Additionally out of scope / forbidden** (verbatim from the operator brief and the standing rules): any
edit to `.claude/`; committing raw runs, raw traces, card data, Pokémon Elements, the `cg/` SDK, deck
lists, or any Competition Data; **sidecar trace reads** (`runs/<run_id>/traces/`).

## 5. Functional requirements

All five are **build** requirements, grounded in the Cycle-003 design authorities (docs 04, 05) and the
canonical offline sibling `analysis/dispersion_report.py`.

### C4-FR-1 — Evidence-summary generator (`analysis/evidence_summary.py`)

Build an offline `analysis/`-class generator that:

1. **Reads existing local sealed run dirs only** — each run dir's `manifest.json` (the `regime_id`/
   `agent_id` authority, read first) and `match_results/*` via `analysis/aggregate.py:aggregate_run`
   (`:75-89`) — **exactly the `dispersion_report.py` read surface** (`dispersion_report.py:11-19`). It
   runs **no eval** and creates **no run dir** (NG12).
2. **Never opens the per-decision sidecars** (`runs/<run_id>/traces/`) — *structurally*, by the module
   containing **no reference** to that sidecar directory, mirroring `dispersion_report.py:16-19`.
3. **Reuses** `aggregate_run` and `dispersion_report.descriptive_stats` (`:94-114`) rather than
   recomputing, inheriting the proven sanitized surface and the seven-statistic / six-metric boundary —
   so no new metric or statistic can enter through the generator (doc 04 §2.2-§2.3).
4. **Emits a doc 04 §2 safe-field, JSON-first summary** (`render_json` primary, any markdown derived —
   mirroring `dispersion_report.py:243-255` vs `:197-240`), carrying the two mandatory framing strings
   (unseeded-process caveat + Rung-1 footer, doc 04 §2.4).
5. **Writes local-by-default** via `--out` to a gitignored path (`dispersion_report.py:268-270`). Promotion
   to tracked status is never a generator side effect (NG4).

### C4-FR-2 — Independent fail-closed validator (`--validate` mode)

Build a validator that makes doc 04 §3's forbidden set **enforceable, not advisory**:

1. **Independent** — operates over an arbitrary summary dict **re-read from a file**, not the in-memory
   generator output, so it is a genuine gate (not a tautology that passes because the generator only
   emits safe fields).
2. **Allow-list, fail-closed** — accepts **only** the doc 04 §2 safe-field set; any field outside it
   fails closed (`05-generator-validator-shape.md` §2.1). Rejects with a clear per-class reason (mirroring
   `hygiene_check.find_violations` `(item, reason)` pairs, `hygiene_check.py:52-62`): any inferential
   statistic; any Competition-Data / Pokémon-Element token; any cross-regime field/comparison (NFR-5);
   any affirmative forbidden agent word.
3. **Single-regime guard → exit 2** — mirroring `MixedRegimeRefusal` (`dispersion_report.py:79-80,133-140`)
   and `delta_report.CrossRegimeRefusal` (`delta_report.py:128-143`); `regime_id` authority is each
   `manifest.json`, never keyed off the run-id string (`05-…` §2.2).
4. **Benign `hypothesis` exception** — the validator MUST allow the ledger `hypothesis` **text-field**
   context while rejecting an inferential **hypothesis-test** (doc 04 §3 note; doc 06 §1). Implemented as
   a benign-exception allow-rule, not a blanket token ban that would false-positive on the ledger column.
5. **Hygiene parity (superset of `eval/hygiene_check.py`)** — refuses the same carrying paths/tokens
   (`hygiene_check.py:35-45`) and adds the value-bearing/inferential/cross-regime/forbidden-word content
   checks a path gate cannot express (`05-…` §2.5, §3). The two compose; neither replaces the other.

### C4-FR-3 — In-module machine-checkable schema artifact (allow-list constant) [decision D-1]

The machine-readable schema artifact is an **in-module Python allow-list constant** (e.g. `SAFE_FIELDS`),
reusing the existing `DISPERSION_METRICS` (`dispersion_report.py:69-72`) and `STAT_COLUMNS` (`:76`) — **not**
a standalone hand-maintained `analysis/evidence_summary_schema.json`. This follows the settled project
idiom: *"No third-party schema library — overkill for this field set. A schema library is the ladder rung
to add only if the schemas outgrow this"* (`eval/validate.py:13`, whose field knowledge lives in the
in-module `_MATCH_SPEC`), and is explicitly sanctioned by the SDD (*"… or an in-module constant"*,
`02-sdd.md:170`). Doc 04 §2 is the plain authority the constant **must agree with** (the
`eval/schemas.md:1-4` spec↔validator contract). An optional `--print-schema` mode MAY emit the schema as a
**derived dump from the in-module constant** (single source of truth in code, no drift surface) — never a
hand-maintained file. "JSON-first" (doc 04 §4) governs the **emitted summary**, not the schema-definition
format.

### C4-FR-4 — Test suite (`tests/test_evidence_summary.py`)

Build a stdlib test module (plain-Python `main()` → exit 0/1, mirroring `tests/test_import_direction.py`)
proving every property enumerated in §9. Non-trivial logic (the allow-list, the refusals, the
single-regime guard, the benign exception) MUST each leave at least one runnable check that fails if the
logic breaks (Karpathy goal-driven principle; acceptance-criteria tests).

### C4-FR-5 — Local end-to-end exercise (no promotion) [decision D-3]

Run the built generator on the **existing local** K=20+20 sealed run dirs (`runs/run-v002-b-1..20`,
`runs/run-v002-c-1..20`) to emit a summary to a **gitignored** local path (default
`grimoires/loa/a2a/cycle-004/`, `.gitignore:17`; or a `runs/`-adjacent gitignored path), then validate it
clean (exit 0). This demonstrates the pair end-to-end. It **promotes no value**: the output is not
`git add`-ed, creates no tracked value artifact, and writes no ledger row. If the local run dirs are
unavailable in a given checkout, the exercise is deferred without blocking the build (the tests use
fixtures, per §9, and do not depend on gitignored data).

## 6. Non-functional requirements / technical posture

- **NFR-1 — Claim-safety.** Rung 1 held; forbidden agent words negated-only; no inferential result
  produced; no claim exceeds the ledger's `claim_ceiling` (`docs/claim-ceiling.md:54-65`).
- **NFR-2 — Sanitization.** Competition Data and Pokémon Elements never enter git (CC-1/CC-2, ESP);
  `eval/hygiene_check.py` remains the staging gate; the validator is sanitization-parity-or-stricter.
- **NFR-3 — Same-regime only.** No field, example, or comparison crosses `regime_id`; the validator
  enforces a single-regime guard (exit 2) (NFR-5; doc 05 §2.2).
- **NFR-4 — Descriptive vocabulary only.** Only `count/min/max/range/mean/median/spread`; `std-dev`,
  `variance`, and all inferential statistics are **rejected** by the validator, never computed (OD-6;
  `07-operator-decision-register.md` §2).
- **NFR-5 — Offline/runtime separation; stdlib-only [brief AC #8].** The generator/validator is
  `analysis/`-class: imports run-dir artifacts + intra-zone helpers only — **no `cabt`/`cg`, `sim/`,
  `agents/runtime/`, or `eval/` import** (`dispersion_report.py:44-46`; enforced by
  `tests/test_import_direction.py:32-37`, where `ALLOWED["analysis"] = set()`, which auto-globs
  `analysis/*.py` at `:69`). stdlib only — `json`, `statistics`, `pathlib`, `argparse`, `sys`. No
  third-party dependency (`eval/validate.py:13`; `02-sdd.md` "stdlib-only").
- **NFR-6 — Reproducibility posture.** `mode=unseeded`; the unseeded-process caveat travels with every
  summary (`docs/cycles/cycle-002/05-reproducibility-reality.md` §3; doc 04 §2.4).
- **NFR-7 — Zone discipline [brief AC #9].** Build code is tracked App Zone (`analysis/`, `tests/`); **all
  outputs that contain evidence values stay local/gitignored** (the generator's `--out`, the §10 exercise
  output) unless a separate operator promotion decision (SP-6) is issued. The PRD is Docs/State Zone.
  `.claude/` is never touched.
- **NFR-8 — Build-only-this-cycle.** NG5 is relaxed for the named artifacts only; the build crosses no
  other line; Rung-2 admission is deferred to a separate later gate (expected Cycle-005).
- **NFR-9 — Implement-time citation revalidation [brief AC #7].** Because docs 04/05/06/07 pair with
  source via line-anchored citations (e.g. `dispersion_report.py:69-72,76,94-114`; `delta_report.py:128-143`;
  `aggregate.py:75-89`; `hygiene_check.py:35-45`; `ledger.md:9`), `/implement` MUST re-validate those
  anchors against the **build-time HEAD** before relying on them, and make the in-module allow-list
  **agree** with doc 04 §2 (the `eval/schemas.md:1-4` contract). Citations accurate at Cycle-003 close may
  desync if source files moved since.

## 7. Generator / validator build detail (C4-FR-1 / C4-FR-2)

- **Command interface** (mirroring `dispersion_report.py` CLI `:48` + `hygiene_check.py` modes):
  ```
  # generate (default): existing sealed run dirs → JSON-first summary, local-by-default
  python analysis/evidence_summary.py <run_dir> [<run_dir> ...] [--json] [--out <local-path>]
  # validate an existing summary file (independent, fail-closed gate)
  python analysis/evidence_summary.py --validate <summary.json>
  # optional: print the in-module allow-list (derived; not a hand-maintained file)
  python analysis/evidence_summary.py --print-schema
  ```
- **Exit-code contract** (doc 05 §2.4; mirror `dispersion_report.py:48-49`): `0` clean/valid · `1` input
  failure (missing manifest, malformed run dir) · `2` mixed-regime refusal · **non-zero (never `0`)** on a
  forbidden-field/value/word leak — fail-closed. The exact leak code (e.g. `3`) is finalized by the SDD/
  sprint (OD-C4-2).
- **Module shape [decision D-2]:** **one** module `analysis/evidence_summary.py` exposing a `build_summary`
  (generator core) and a pure `validate_summary(obj) -> list[(field, reason)]` (validator core), sharing
  the in-module allow-list constant; CLI dispatches by flag. (A separate `…_validate.py` module is the
  noted alternative; SDD finalizes — OD-C4-1.)

## 8. Schema-shape decision detail (decision D-1)

Recorded as a PRD decision so the SDD does not relitigate it: the schema artifact is the **in-module
allow-list constant** (C4-FR-3). Rationale: (1) repo idiom — every TurnTrace validator carries field
knowledge in-module (`eval/validate.py:_MATCH_SPEC`; `dispersion_report.py:DISPERSION_METRICS`/`STAT_COLUMNS`)
and there is **no** standalone `*.schema.json` in the TurnTrace app (the only schema files + `jsonschema`
usage in the repo are under `.claude/`, the Loa framework); (2) stdlib-only (NFR-5) — a `.json` JSON-Schema
would force a `jsonschema`/`pydantic` dependency or hand-rolled Draft-07 interpretation, both contradicting
`eval/validate.py:13`; (3) DRY — the allow-list **is** `DISPERSION_METRICS + STAT_COLUMNS + identity/
provenance fields`, already in code. The "machine-readable schema artifact" requirement is satisfied by the
JSON-first emitted **summary** plus the in-module allow-list; `--print-schema` (if built) derives from the
constant.

## 9. Test & validation requirements (C4-FR-4 detail)

`tests/test_evidence_summary.py` MUST prove, each with a runnable check (use synthetic/fixture run dirs for
determinism — not gitignored real data):

1. **Allow-list fail-closed** — any field outside doc 04 §2 → rejected with a reason; unknown field → non-zero.
2. **Forbidden-content rejection** (one case each, doc 04 §3 / doc 05 §2.1): raw decision/trace body;
   Competition-Data token; Pokémon-Element token; **inferential statistic** (`std-dev`/`variance`/CI/
   p-value/`significance`/hypothesis-test/error-bar); **cross-regime** field; **affirmative forbidden agent
   word**.
3. **Mixed-regime refusal → exit 2** — inputs spanning two `regime_id`s hard-refused before aggregation.
4. **No-sidecar-read (structural) [brief AC #5]** — the module source contains **no reference** to the
   `traces/` sidecar directory (assert like the `dispersion_report.py:16-19` guarantee); reads only
   `manifest.json` + `match_results/*`.
5. **Hygiene parity (superset)** — every path/token `hygiene_check.find_violations` refuses is also refused
   by the validator, plus the content checks the path gate cannot express.
6. **No-ledger-mutation [brief AC #3]** — after a full generate run, `git diff --exit-code -- docs/ledger.md`
   is clean (generator writes local-by-default, never to `docs/`).
7. **No-value-promotion [brief AC #4]** — generator default output goes to local `--out`; the emitted
   summary carries the Rung-1 footer + unseeded-process caveat and **no ceiling of its own**.
8. **Benign `hypothesis` exception [brief AC #6]** — the validator **accepts** a summary whose provenance
   cites the ledger `hypothesis` text-field context, while **rejecting** an inferential hypothesis-test.
9. **Doc↔schema agreement** — the in-module allow-list equals doc 04 §2's field-list; a divergence fails.
10. **JSON-first round-trip** — generator output validates clean (exit 0) against its own validator; any
    markdown is derived from the JSON.
11. **Sanitization smoke** — a poisoned input (a planted forbidden token) is **refused**, never surfaced.
12. **Import-direction / stdlib-only [brief AC #8]** — auto-covered by `tests/test_import_direction.py`
    (globs `analysis/*.py`); no `cabt`/`sim`/`runtime`/`eval` import; no third-party dependency.

Operator hard-checks for the sprint (mirroring Cycle-003): `hygiene_check --paths` exit 0 on any tracked
artifact; `docs/ledger.md` byte-unchanged (`hash-object = 2a2f1c2…`); `frozen/`/`runs/`/`agents/`/`.claude/`
untouched; no forbidden agent word as an affirmative; no dispersion value in any tracked file.

## 10. Local end-to-end exercise (C4-FR-5 detail, decision D-3)

Demonstrate the built pair on the existing local evidence without promoting it: generate a summary from
`runs/run-v002-b-1..20` + `runs/run-v002-c-1..20` (single `regime-v002`, frozen `random_legal-v001` baseline
+ `scripted-v001` candidate) to a gitignored path under `grimoires/loa/a2a/cycle-004/`, then `--validate`
it to exit 0. **Promotes nothing:** the summary is gitignored (`.gitignore:17`; `hygiene_check.py:43`
mechanically refuses `runs/<id>/…` from staging), is not `git add`-ed, writes no ledger row, advances no
ceiling, and chooses no `M`. The exercise is evidence the machinery works — not a Rung-2 verdict.

## 11. Claim-ceiling posture

The loop sits at **ladder Rung 1 — legal completion / throughput / audit-trail**, and **Cycle-004 keeps
the ceiling at Rung 1** for the whole cycle (`docs/claim-ceiling.md`; ladder
`docs/cycles/cycle-000-bootstrap/01-turntrace-prd.md:274-276`):

```
Rung 0  env not trusted
Rung 1  legal completion                         ← current, and held for all of Cycle-004
Rung 2  beats random-legal                       ← machinery BUILT here; never claimed; admission = Cycle-005
Rung 3  beats scripted / prior best, ablation-backed
Rung 4  stable, report-ready
```

**Allowed claim form** — relative, local, descriptive, carrying its `n`, `K`, and `regime_id`. **Forbidden
claim forms** (negated-only): gameplay strength; statistical significance; cross-regime uplift; leaderboard
quality; calibration; optimality; competitiveness. Only the ledger, advanced by a separate explicit later
operator decision, can carry a higher rung. **Cycle-004 advances nothing; it builds the tool that a later
gate would use.**

## 12. Safety and sanitization constraints

Carried verbatim from the standing rules (`docs/operator/turntrace-loop-contract.md` §7-§8;
`docs/cycles/cycle-002/06-ledger-report-discipline.md` §5-§7):

- **Competition Data never enters git** (CC-1/CC-2): the `cg/` SDK, card data, raw deck lists, `deck.csv` —
  local-only under gitignored `grimoires/loa/context/`.
- **Pokémon Elements** never appear in tracked artifacts.
- **Generated runs, values, and the generator's output** stay local/gitignored; tracked artifacts hold
  sanitized code + specs only.
- **`eval/hygiene_check.py`** remains the mechanical staging gate; the built validator (C4-FR-2) is
  sanitization-parity-or-stricter with it.
- **Forbidden agent claim words** appear only as negated/forbidden language.

## 13. Operator / product decisions recorded

| ID | Decision | Status |
|---|---|---|
| **OA-2** | Operator opens the build gate for Cycle-004, scoped to relaxing **NG5 only** (`02-sdd.md:505` OD-C3-6). | **Required to proceed** — operator action at PRD acceptance; this PRD does not self-authorize. |
| **D-1** | Schema shape = **in-module machine-checkable allow-list constant**, not a standalone hand-maintained `.schema.json` (§8). | **Decided** (recorded; SDD honors). |
| **D-2** | Module shape = **one** `analysis/evidence_summary.py` with generation + `--validate` mode (§7). | **Decided** (one-vs-two finalized by SDD — OD-C4-1). |
| **D-3** | Local end-to-end exercise = **yes**, output **gitignored/local**, promotes nothing (§10). | **Decided.** |
| **D-4** | Cycle-004 = **build-only, no admission capstone**; Rung-2 admission deferred to a later gate (Cycle-005). | **Decided.** |
| **D-5** | **No** K=50 / paired-delta / evidence hardening in Cycle-004 (NG12). | **Decided.** |
| **D-6** | Local exercise output path **must be gitignored** and must not create a tracked value artifact (default `grimoires/loa/a2a/cycle-004/`). | **Decided** (exact path confirmable at SDD — OD-C4-3). |
| **M / SP-6 / Rung-2 row** | Numeric margin `M` unset; SP-6 not issued; no Rung-2 row. | **Deferred** to the later admission gate (seam 8b/8c/8d) — **none in Cycle-004**. |

## 14. Success criteria

### 14.1 Planning-cycle success (this PRD)

- This PRD is accepted by the operator (who opens OA-2) and proceeds to `/architect` (SDD), not directly
  to implementation.
- It specifies all five FRs (C4-FR-1…C4-FR-5) build-safely, records decisions OA-2 + D-1…D-6, and names
  the later Loa path.
- Rung 1 is held; `docs/ledger.md` is byte-unchanged; no value is promoted; `.claude/` is untouched; State-
  Zone files stay unstaged.

### 14.2 Build-cycle acceptance criteria (when the code lands under `/implement`)

- **AC-1 — Generator** conforms to C4-FR-1: reads `manifest.json` + `match_results/*` via `aggregate_run`
  only; never references the sidecar dir; emits JSON-first doc 04 §2 safe fields; writes local-by-default.
- **AC-2 — Validator** conforms to C4-FR-2: independent, allow-list/fail-closed; rejects every doc 04 §3
  class with a reason; single-regime exit 2; benign `hypothesis` exception; hygiene-parity superset.
- **AC-3 — Schema artifact** is the in-module allow-list constant agreeing with doc 04 §2 (C4-FR-3); no
  `.schema.json`; no third-party dependency.
- **AC-4 — Tests** (§9) all pass, including the structural no-sidecar-read, no-ledger-mutation,
  no-value-promotion, benign-`hypothesis`, and doc↔schema-agreement checks; meet
  `.loa.config.yaml: edd.min_test_scenarios`.
- **AC-5 — Local exercise** (§10) produces a gitignored validated summary; promotes nothing.
- **AC-6 — Citations re-validated** against build-time HEAD (NFR-9).
- **AC-7 — Posture held (hard):** Rung 1 held; `docs/ledger.md` byte-unchanged; no value promoted; stdlib-
  only / analysis-only imports; no `M`/SP-6/Rung-2 row.
- **AC-8 — Cadence:** lands through `/implement → /review-sprint → /audit-sprint → operator acceptance`.

> **Operator-brief PRD acceptance mapping (all satisfied):** (1) build-only + Rung 1 → Posture, NFR-8, §11;
> (2) admission later gate (Cycle-005) → Posture, D-4, §15; (3) ledger byte-unchanged HARD → §14.1/§14.2
> AC-7, §9.6; (4) no value promotion HARD → §14 AC-7, §9.7; (5) no-sidecar-read structural+tested →
> C4-FR-1.2, §9.4; (6) `hypothesis` text vs inferential distinction → C4-FR-2.4, §9.8; (7) implement-time
> citation revalidation → NFR-9, AC-6; (8) stdlib-only/analysis-only → NFR-5, §9.12; (9) value outputs
> local/gitignored unless separate promotion → NFR-7, §10; (10) names PRD→SDD→sprint→implement→review→audit→
> acceptance → Posture banner, §14, §15.

## 15. Open operator decisions for SDD / sprint planning

- **OD-C4-1 — Module shape finalization.** One module with `--validate` (recommended, D-2) vs. a separate
  `analysis/evidence_summary_validate.py`. SDD decides.
- **OD-C4-2 — Leak exit code.** The exact non-zero code for a forbidden-field/value/word leak (the contract
  is only "never 0 on a leak"; doc 05 §2.4). SDD/sprint decides.
- **OD-C4-3 — Exercise output path.** Confirm the gitignored local path for the §10 exercise (default
  `grimoires/loa/a2a/cycle-004/`).
- **OD-C4-4 — Test fixtures.** Synthetic fixture run dirs (recommended, for determinism) vs. the existing
  local K-batch dirs; the exercise uses the real local dirs, the tests use fixtures.
- **OD-C4-5 — `--print-schema`.** Whether to build the optional derived `--print-schema` mode now or defer
  it (derived-from-constant only; never a hand-maintained file).
- **Reaffirmed (not decided in Cycle-004):** `M` unset; SP-6 not issued; Rung-2 admission = a separate later
  gate (Cycle-005) — the four seam decisions (8a–8d) stay open.

## 16. Risks and mitigations

| ID | Risk | Mitigation |
|---|---|---|
| **R1** | **Value leak into a tracked artifact** during the exercise. | Fail-closed validator (C4-FR-2); `hygiene_check` parity; generator local-by-default; §10 output gitignored, never `git add`-ed (NG4). |
| **R2** | **Scope-creep into admission** — the build drifts into asserting Rung 2 / advancing the ceiling / writing a row. | NG1-NG3 held; no `M` chosen; admission deferred to Cycle-005 (D-4); seam 8a-8d untouched. |
| **R3** | **Citation rot** — docs 04/05 line anchors desync from source before build. | NFR-9: `/implement` re-validates anchors against build-time HEAD; allow-list made to agree with doc 04 §2. |
| **R4** | **`hypothesis` false-positive** — a naive inferential-term grep trips on the ledger column. | Benign-exception allow-rule (C4-FR-2.4); test §9.8 proves accept-column / reject-test. |
| **R5** | **Sidecar-read creep** — the generator reaches into `traces/`. | Structural no-reference guarantee (C4-FR-1.2); test §9.4. |
| **R6** | **Dependency creep** — a `jsonschema`/`pydantic` import sneaks in via a `.schema.json`. | In-module constant (D-1); stdlib-only (NFR-5); import-direction test §9.12; `eval/validate.py:13`. |
| **R7** | **Cross-regime contamination** — a v002 figure aggregated beside a v001 figure. | Single-regime guard exit 2 (C4-FR-2.3); `manifest.json` regime authority; test §9.3. |
| **R8** | **Value-promotion creep (SP-6)** — the exercise output gets tracked. | No SP-6 (NG4); local-by-default; §10 output gitignored; test §9.7. |
| **R9** | **Build beyond scope** — K=50 / paired-delta / FunSearch / runtime sneak in. | NG12/NG10/NG7 held (D-5); reads existing runs only; no eval invoked. |

## 17. Sources and traceability

> **Tracked design authorities (Cycle-003):** `docs/cycles/cycle-003/01-prd.md` (NG1-13 `:145-171`; OA-2/
> OD-C3-6 `:379`; ladder `:300-318`); `docs/cycles/cycle-003/02-sdd.md` (placement table `:165-175`;
> OA-2 `:485,505`; SP-6 `:405-413`); `04-evidence-summary-schema-spec.md` (§2 safe fields, §2.4 framing,
> §3 forbidden classes + `hypothesis` note, §4 JSON-first, §5 read surface/hygiene parity);
> `05-generator-validator-shape.md` (§1 generator, §2.1 allow-list, §2.2 single-regime exit 2, §2.3 import
> boundary/stdlib-only, §2.4 exit codes, §2.5/§3 hygiene parity); `06-rung-2-ledger-convention.md` (§1-§4
> ledger byte-unchanged, `hypothesis` text-field); `07-od6-criterion-2-proposal.md` (§5 seam 8a-8d).
> **Tracked code (canonical patterns):** `analysis/dispersion_report.py` (read surface `:11-19`; import
> boundary `:44-46`; exit codes `:48-49`; `DISPERSION_METRICS` `:69-72`; `STAT_COLUMNS` `:76`;
> `descriptive_stats` `:94-114`; `MixedRegimeRefusal` `:79-80,133-140`; `render_json` `:243-255`; local
> `--out` `:268-270`); `analysis/aggregate.py:75-89`; `analysis/delta_report.py:128-143`;
> `eval/hygiene_check.py:35-45,52-62`; `eval/validate.py:13` (+ in-module `_MATCH_SPEC`);
> `eval/schemas.md:1-4,114-119`; `tests/test_import_direction.py:32-37,69`; `docs/ledger.md:9,11-12`;
> `docs/claim-ceiling.md:5-6,54-65`; `.gitignore:17`.
> **Local decision input (gitignored State Zone, not a tracked dependency):**
> `grimoires/loa/a2a/cycle-004/pre-prd-research.md` (the pre-PRD research pass; recommends build-only,
> in-module constant, admission deferred).
> **Operator confirmations (this planning session):** build-only / NG5-only relaxation; OA-2 required to
> proceed; D-1…D-6 as recorded; `M`/SP-6/Rung-2-row deferred to Cycle-005.
> Current main at authoring: `73c13ee`. Claim ceiling: **Rung 1 (unchanged).** This PRD opens no
> implementation gate, builds no code, mutates no ledger, and promotes no value.
