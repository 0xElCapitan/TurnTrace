# Cycle-002 — Evaluation Scale + Comparison Confidence

> **Research and planning artifact only — Status: PRE-PRD / RESEARCH.**
> Alternative framing evaluated: *"From n=12 Toy Comparison to Stable Evaluation Harness."*
>
> This document opens **NO build gate** and authorizes no code. It is the pre-PRD
> research/planning pass for Cycle-002. Implementation requires a separate, explicit
> operator action (OA-2 equivalent) per `docs/operator/turntrace-loop-contract.md` §6.
> Governing standing rules: `docs/operator/turntrace-loop-contract.md`,
> `docs/operator/deferred-lane-gate-after-sprint-01.md`.
>
> Sanitized planning note. No raw traces, card IDs/names, deck lists, simulator logs,
> PDFs/CSVs, or Competition Data appear here (CC-1/CC-2, ESP). Runs are referenced by
> `run_id`, content hashes, sanitized metrics, claim ceilings, and local path/status only.
> The forbidden agent claim words (*strong / competitive / optimal / calibrated /
> complete*) appear only as negated/forbidden language.

| Field | Value |
|---|---|
| **Cycle** | Cycle-002 (planning) |
| **Working title** | Evaluation Scale + Comparison Confidence |
| **Status** | Research / planning only — no PRD yet, no build gate |
| **Authority** | `docs/cycles/cycle-001/closeout.md` (primary); Sprint 00/01/02 closeouts; `docs/operator/*`; `docs/claim-ceiling.md`; `docs/ledger.md`; `frozen/*` |
| **Expected main at authoring** | `beac070` — *docs: close TurnTrace Cycle 001* (Cycle-001 closeout landed) |
| **Claim ceiling** | Rung 1 (unchanged; this artifact does not raise it) |
| **Broad optimization** | **closed** |
| **Runtime-agent improvement lane** | **closed** |
| **Date** | 2026-06-18 |

## Binding posture (this whole artifact operates under these statements)

```
Cycle-002 planning opens no build gate.
Cycle-002 should improve evaluation scale and comparison confidence, not runtime-agent strength.
Broad optimization remains closed.
The runtime-agent improvement lane remains closed.
The claim ceiling remains Rung 1 until an explicit later artifact earns otherwise.
```

`Data first, optimization second` remains binding
(`docs/operator/deferred-lane-gate-after-sprint-01.md:96`). The bright line for the whole
cycle: **Cycle-001 held the regime fixed and varied the agent once; Cycle-002 holds the
agents frozen and varies only the *evaluation* (scale + repetition + reporting).** Any work
that makes the runtime agent play differently is out of scope and forbidden here.

## 1. Executive summary

Cycle-001 closed/accepted/integrated on 2026-06-18 as the "Evidence Foundation" cycle: it
proved TurnTrace can **produce, compare, explain, review, audit, and close** local simulator
evidence **without leaking Competition Data or overclaiming**
(`docs/cycles/cycle-001/closeout.md:23-24`). It earned a first same-regime, agent-only
comparison — `run-0001` (`random_legal-v001`) vs `run-0002` (`scripted-v001`) under
`regime-v001` at **n=12** — and two ceiling-bearing ledger rows, all bounded to **ladder
Rung 1** (`docs/ledger.md:11-12`; `docs/cycles/cycle-001/closeout.md:43-68`). It explicitly
did **not** earn any gameplay-strength, statistical-significance, cross-regime, leaderboard,
or calibration claim, and did not raise the ceiling (`docs/cycles/cycle-001/closeout.md:56-68`).

The Cycle-001 closeout recommends Cycle-002 as **"Evaluation Scale + Comparison Confidence,"**
asking: *"Can TurnTrace produce larger, repeatable same-regime comparisons that remain clean,
cheap, auditable, and claim-ceiling safe?"* (`docs/cycles/cycle-001/closeout.md:82-101`).

The decisive repo-grounded finding that shapes this entire plan: **raising `n` is not a free
parameter.** The evaluation harness derives `n` from the frozen seed-set
(`eval/run_eval.py:121` reads `seed_set["match_indices"]`), and the seed-set is one of the
four components of `regime-v001` (`frozen/regimes/regime-v001.json:4-7`). The frozen-regime
rule is explicit: *"A change to ANY component … requires a NEW file regime-v002 — never an
edit … Never compare results across regimes (NFR-5)"*
(`frozen/regimes/regime-v001.json:9`; `docs/claim-ceiling.md:29-35,62-64`). The seed-set's own
rationale already anticipates this: *"N=12 is a modest Sprint-00 set … Probe throughput
(~80-190 matches/s) leaves ample headroom to raise N in a future regime-v002 without touching
the loop"* (`frozen/seeds/seed-set-v001.json` `n_note`). **Therefore larger-n evaluation means
standing up `regime-v002`, re-establishing the same-regime comparison *inside* that new
regime, and never comparing v002 numbers to the v001 ledger rows.** "Same-regime" in Cycle-002
means *same `regime-v002` across a batch*, not an extension of the n=12 v001 result.

**Recommended narrow mission:** *Stand up a stable, sanitized, larger same-regime evaluation
harness under a new `regime-v002`, run repeated same-regime batches cheaply, and report
observed dispersion descriptively — all at Rung 1, agents frozen, ledger discipline preserved.*
Of the seven candidate lanes, the recommended in-scope spine is **D → A → C/B** (cost budget →
scale via regime-v002 → repeated batches + descriptive-variance reporting) with **G** (reporting
/ ledger discipline) as a cross-cutting constraint, and **E** (Rung 2 readiness criteria) and
**F** (reproducibility reality) as **planning/criteria-only** lanes that define and document but
build nothing claim-bearing.

**Recommendation: PROCEED to a Cycle-002 PRD** along this narrow scope, after the operator
accepts this artifact. This artifact opens no build gate; the PRD is the next Golden-Path step,
not implementation.

## 2. Cycle-001 recap

Cycle-001 ran three sprints, each through the standard Loa loop `/implement → /review-sprint →
/audit-sprint`, integrated fast-forward only with no merge/squash/tag/version bump
(`docs/operator/turntrace-loop-contract.md:14-39`; sprint closeouts).

| Sprint | Framing | Outcome | Final commit |
|---|---|---|---|
| 00 | Smallest Useful Loop | First local evidence run (`run-0001`) + ledger discipline | `ffe16a8` |
| 01 | The First Comparison | First same-regime, agent-only comparison `run-0001` vs `run-0002` | `3492e61` |
| 02 | Delta Explanation + Failure-Mode Taxonomy | Sanitized taxonomy v001, aggregate failure report, `delta_report`/ledger hardening, `replay_check` marker, strategy-report PERMITS/FORBIDS | `9771436` |

> Sources: `docs/cycles/cycle-001/closeout.md:26-54`; `docs/cycles/cycle-001-sprint-00/closeout.md`;
> `docs/cycles/cycle-001-sprint-01/closeout.md`; `docs/cycles/cycle-001-sprint-02/closeout.md`.

**The standing harness Cycle-002 inherits:**

- A sealed-run driver `eval/run_eval.py` — N matches → one immutable run dir, with an
  immutability guard (exit 3 on a populated dir; `eval/run_eval.py:138-154`) and source-hash
  provenance (`eval/run_eval.py:158-173`).
- Single-run aggregation `analysis/aggregate.py` — one `summary.csv` (11 columns) + at most one
  ledger row per run, idempotent per `run_id`, requiring a non-empty `claim_ceiling`
  (`analysis/aggregate.py:29-40,110-149`).
- A same-regime, two-run delta report `analysis/delta_report.py` that **hard-refuses**
  cross-regime comparison (`CrossRegimeRefusal` → exit 2; cited `docs/strategy-report.md:29-30`).
- A sanitized aggregate failure report `analysis/failure_report.py` — coarse counts only, no
  ledger row, Rung-1 footer, single run dir, `--out` local/ignored by policy
  (`analysis/failure_report.py:1-30`).
- A reproducibility floor `analysis/replay_check.py` — audit-trail equality always; byte-identical
  tier **skipped** under `seed_controlled=false` (never silently passed).
- The versioned `docs/failure-mode-taxonomy-v001.md` (FM-01..FM-09; FM-03/04/06/08
  `detector: forbidden`), additive-versioned (`-v002`, never in-place).
- A Competition-Data staging guard `eval/hygiene_check.py` (path-level pre-commit refusal).

### 2.1 Research questions (answered from repo evidence)

**RQ-1 — What did Cycle-001 prove, and what did it not prove?**
*Proved:* the evidence loop produces and seals immutable run dirs; computes a first same-regime,
agent-only comparison end-to-end with hardened provenance; emits sanitized aggregate diagnostics;
maintains an append-only ledger as the sole ceiling-bearing artifact; and runs the full
implement→review→audit→accept loop with fast-forward-only integration
(`docs/cycles/cycle-001/closeout.md:43-54`). *Did NOT prove:* gameplay strength/quality,
statistical significance, any cross-regime comparison, leaderboard quality, calibration, runtime-
agent improvement, or any claim above Rung 1 (`docs/cycles/cycle-001/closeout.md:56-68`). A
`win_rate` of 0.8333 for `run-0002` against the `random_legal` mirror at n=12 is **not** evidence
of quality — the opponent is a mirror and the rung is legal completion only
(`docs/claim-ceiling.md:22-23`; `docs/ledger.md:11-12`).

**RQ-2 — What are the safest next planning lanes for Cycle-002?**
The closeout's own enumerated lanes: increasing `n` safely; run cost / runtime budget; repeated
same-regime batches; variance/confidence language without overclaiming; seed/reproducibility
reality; larger-run report formats; claim-ceiling progression criteria; criteria for whether/when
Rung 2 becomes possible (`docs/cycles/cycle-001/closeout.md:92-101`). These map onto candidate
lanes A–G in §7. All are *evaluation-harness* work, none touch the agent — which is precisely why
they are the safe lanes.

**RQ-3 — What would scaling from n=12 to larger same-regime evaluations mean without overclaiming?**
It means a **new `regime-v002`**, not a bigger v001. `n` is the length of the frozen seed-set's
`match_indices` (`frozen/seeds/seed-set-v001.json`: `match_indices=[1..12]`, `n=12`), and the
seed-set is a regime component; any change to a component is a new regime, never an edit
(`frozen/regimes/regime-v001.json:9`). The design anticipates exactly this ("raise N in a future
regime-v002 without touching the loop," `frozen/seeds/seed-set-v001.json` `n_note`). Consequences:
(a) `regime-v002` results are **not comparable** to the v001 ledger rows (NFR-5;
`delta_report` exit-2 refusal); (b) "same-regime comparison" in Cycle-002 must be *baseline vs
candidate both under `regime-v002`*, a fresh internal pair; (c) the v001 rows remain the historical
Rung-1 record and are never edited or re-interpreted at the new `n`. Larger `n` buys **sampling
resolution** (a tighter view of the same unseeded distribution), not a higher rung.

**RQ-4 — What minimum evidence would a future Rung 2 claim even require?**
Rung 2 on the maturity ladder is *"beats random-legal"* (`docs/cycles/cycle-000-bootstrap/01-turntrace-prd.md:274-276`;
`docs/cycles/cycle-000-bootstrap/02-turntrace-sdd.md:840`). Today's `run-0002` vs `run-0001` is the
*shape* of that comparison (scripted vs random_legal mirror) but is held at Rung 1 because n=12 is
small and no inferential design exists. A future Rung 2 *consideration* (not a claim) would minimally
need: (1) a same-regime baseline-vs-candidate comparison at a justified, larger `n` under a single
`regime-vNNN`; (2) an explicitly *designed and operator-approved* inferential procedure (the brief and
`docs/claim-ceiling.md` forbid significance claims without explicit design); (3) the candidate exceeding
the random-legal baseline by a pre-registered margin under that design; (4) provenance + audit-trail
intact; (5) the ledger row's `claim_ceiling` deliberately advanced by an explicit operator decision —
the ledger is the only artifact that can carry a higher ceiling (`docs/claim-ceiling.md:5-6`). Cycle-002
**defines these criteria; it does not meet or claim them.**

**RQ-5 — What are the runtime/cost risks of larger runs?**
Simulator throughput is **not** the bottleneck: the probe recorded ~80-190 matches/s
(`frozen/seeds/seed-set-v001.json` `n_note`), so even n=1000 is on the order of seconds of match
time, and tens of repeated batches are minutes. The real cost risks are: (a) **disk/storage** — full
`runs/<run_id>/` trees (records, traces, manifest, hashes) grow with `n` × per-match trace size and
stay local/git-ignored (ESP-1), so many large batches consume local disk; (b) **trace I/O + canonical
hashing** time scaling with `n`; (c) **artifact-proliferation temptation** — more runs invites tracking
more reports, which the ledger/report discipline (Lane G) must resist; (d) **batch-count × n**
multiplies (a)–(c). All four are managed by a measured dry-run budget (Sprint 00), no-ledger-by-default
for non-deliverable runs (`eval/run_eval.py:270-288,333-336`), and keeping larger-run reports
local/ignored unless operator-approved.

**RQ-6 — What reporting changes are needed for larger same-regime batches?**
The current reporting surface is **single-run or single-pair**: `aggregate.py` emits one
`summary.csv` + one ledger row per run; `failure_report.py` reads one run dir; `delta_report.py`
compares exactly two runs. **There is no cross-run / cross-batch aggregator.** Repeated same-regime
batches therefore need a new *descriptive* roll-up that reads K sealed run dirs under the same
`regime-v002` and reports observed dispersion of the sanitized metrics (e.g. min/max/mean/median/spread
across the K runs), with a Rung-1 footer and no ceiling of its own — strictly counts/sanitized
aggregates, never raw rows, mirroring `failure_report.py`'s sanitization contract
(`analysis/failure_report.py:8-19`). This roll-up output stays local/ignored unless operator-approved
(Lane G).

**RQ-7 — What confidence/variance language is allowed without statistical-significance claims?**
*Allowed (descriptive only):* the observed dispersion of a sanitized metric across repeated same-regime
runs — its range, mean, median, and spread — each statement carrying its `n` and `regime_id`
(`docs/claim-ceiling.md:54-59` requires bounded, sample-sized claims; `docs/operator/turntrace-loop-contract.md:72-77`).
Example shape: *"across K repeated batches of n=N under `regime-v002`, the observed win_rate ranged
from X to Y (mean Z)"* — a description of what was observed. *Gated behind explicit design + operator
approval:* any **inferential** statement — confidence intervals, p-values, "significant," hypothesis
tests, or error bars presented as inference. The brief and `docs/claim-ceiling.md` treat significance
claims as requiring explicit design and approval; a confidence interval is inferential, so it is **not**
descriptive dispersion and stays gated. *Always forbidden:* the words *strong / competitive / optimal /
calibrated / complete* except as negated/forbidden language. The clean rule: **descriptive dispersion =
allowed; inferential statistics = gated.**

**RQ-8 — What seed/reproducibility limitations still constrain claims?**
`seed_controlled=false` (`sim/capabilities.json`, via `docs/claim-ceiling.md:42-52`): the local API
exposes no controllable RNG seed, so runs are `mode=unseeded`, records carry `match_index` not `seed`,
and there is **no byte-identical replay** (`frozen/seeds/seed-set-v001.json` `rationale`). The
consequence for variance work: repeated batches are **fresh draws from the same unseeded distribution,
not reproductions**, so observed dispersion conflates agent behavior with uncontrolled simulator RNG —
the two **cannot be separated** without seed control. Any variance language must therefore describe the
dispersion of the *whole unseeded process* under the regime, never be dressed up as an isolated "agent
variance" estimate. Byte-identical replay remains a future upgrade *only if* seed control is later proven
(`docs/claim-ceiling.md:51-52`); Cycle-002 must not manufacture or simulate seed control.

**RQ-9 — What must remain forbidden until a separate operator decision opens the lane?**
The full "Still closed" list and all claim/sanitization/process boundaries carried from Cycle-001
(`docs/operator/deferred-lane-gate-after-sprint-01.md:71-87`; `docs/cycles/cycle-001/closeout.md:103-119`).
Enumerated in §10. None of these is opened by this planning artifact; each requires a separate, explicit
operator decision.

**RQ-10 — What should Cycle-002 explicitly avoid so it does not become accidental agent optimization?**
The failure modes that turn "scale the evaluation" into "tune the agent": (1) changing any
`agents/runtime/` file or agent behavior — the agents (`random_legal`, `scripted_baseline`) stay
**frozen**; (2) **regime/seed-shopping** — choosing the `regime-v002` seed-set, opponent, or deck to
flatter a particular agent's numbers (hidden tuning); (3) adding any per-decision quality detector/scorer
(FM-03/04/06/08 stay `detector: forbidden`, `docs/failure-mode-taxonomy-v001.md:40-52`); (4) multi-agent
"find the best agent" comparisons — that is a tournament/optimization, not evaluation; (5) letting "Rung 2
readiness criteria" become a checklist someone satisfies by tuning rather than by evaluation design; (6)
narrating descriptive dispersion as the agent being "better." The bright line again: **the variable under
change in Cycle-002 is the evaluation harness, never the agent.**

## 3. What is proven / not proven

| Claim area | Status | Evidence |
|---|---|---|
| Evidence loop produces & seals immutable runs; runs the full implement→review→audit→accept loop | **Proven** | `docs/cycles/cycle-001/closeout.md:43-54` |
| First same-regime, agent-only comparison end-to-end (`run-0001` vs `run-0002`, `regime-v001`, n=12) | **Proven** | `docs/ledger.md:11-12`; `docs/cycles/cycle-001-sprint-01/closeout.md:33-53` |
| A metric moved (`win_rate`, `avg_turns`) for an explainable, agent-only reason; correctness-gate rates held at the floor | **Proven** | `docs/cycles/cycle-001-sprint-01/closeout.md:55-69` |
| Sanitized aggregate diagnostics + versioned failure-mode taxonomy v001 exist | **Proven** | `docs/failure-mode-taxonomy-v001.md`; `analysis/failure_report.py` |
| Ledger is the only ceiling-bearing artifact; append-only; idempotent per `run_id` | **Proven** | `analysis/aggregate.py:42-48,125-140`; `docs/ledger.md:3-7` |
| Larger-`n` evaluation = a new `regime-v002` (seed-set is a regime component) | **Proven (design constraint)** | `eval/run_eval.py:121`; `frozen/regimes/regime-v001.json:4-9`; `frozen/seeds/seed-set-v001.json` |
| Gameplay strength / quality | **NOT proven** (forbidden claim) | `docs/claim-ceiling.md:20-23`; `docs/operator/deferred-lane-gate-after-sprint-01.md:38-48` |
| Statistical significance | **NOT proven** (forbidden without explicit design) | `docs/cycles/cycle-001/closeout.md:60` |
| Cross-regime comparison / uplift | **NOT proven** (hard-refused, exit 2) | `docs/claim-ceiling.md:62-64`; `docs/strategy-report.md:29-30` |
| Byte-identical reproducibility / determinism | **NOT proven** (`seed_controlled=false`) | `docs/claim-ceiling.md:42-52` |
| Claim ceiling above Rung 1 | **NOT raised** | `docs/cycles/cycle-001/closeout.md:8,68` |
| Per-run `result`/`ending_cause` distributions actually observed | **requires-raw-data: cannot-surface** | git-ignored run dirs (ESP-1) |

## 4. Current claim ceiling

The loop sits at **ladder Rung 1 — legal completion / throughput / audit-trail**
(`docs/claim-ceiling.md:22-23`). The maturity ladder (`docs/cycles/cycle-000-bootstrap/01-turntrace-prd.md:274-276`;
`docs/cycles/cycle-000-bootstrap/02-turntrace-sdd.md:840`):

```
Rung 0  env not trusted
Rung 1  legal completion                         ← current
Rung 2  beats random-legal
Rung 3  beats scripted / prior best, ablation-backed
Rung 4  stable, report-ready
```

The **experiment ledger (`docs/ledger.md`) is the only ceiling-bearing artifact**; per-match records,
`summary.csv`, the failure report, the delta report, the taxonomy, and this planning doc carry **no
ceiling of their own** (`docs/claim-ceiling.md:5-6`; `docs/operator/turntrace-loop-contract.md:72-77`).
Only **relative, local** claims are permitted, each carrying its `n` and `regime_id`; **never compare
across regimes** (NFR-5). The forbidden agent claim words remain forbidden except as negated language:
*strong, competitive, optimal, calibrated, complete* (`docs/claim-ceiling.md:54-59`). **Cycle-002 keeps
the ceiling at Rung 1**; only the ledger, advanced by an explicit later operator decision, can ever carry
a higher rung.

## 5. Current safety and sanitization posture

Carried verbatim from Cycle-001 (`docs/operator/turntrace-loop-contract.md:59-77`;
`docs/cycles/cycle-001/closeout.md:70-80`):

- **Competition Data never enters git** (CC-1/CC-2): the `cg/` simulator SDK, card data CSV/PDF, Kaggle
  starter `deck.csv`, raw deck lists — all local-only under git-ignored `grimoires/loa/context/`, enforced
  by `eval/hygiene_check.py` (path-level pre-commit refusal; `eval/hygiene_check.py:35-45`).
- **Full `runs/<run_id>/` trees stay local/git-ignored by default** (ESP-1) — raw traces, match logs,
  simulator outputs. Only sanitized summaries, ledger rows, claim ceilings, failure-mode notes, planning
  docs, and operator-approved artifacts are tracked.
- **Reference, never embed**: runs by `run_id` + hashes + sanitized metrics + local path/status; never raw
  contents.
- **Frozen components store references + hashes only** — no card lists (`frozen/` decks are refs + content
  hashes).
- **Review/audit/COMPLETED artifacts** persist to git-ignored State Zone (`grimoires/loa/a2a/sprint-N/`),
  written by the orchestrator after the pure-review skills return — never by the skills, never patching
  implementation (`docs/operator/turntrace-loop-contract.md:85-114`).
- **`.claude/` (System Zone) is never edited.**

## 6. The regime-v002 constraint (the spine of Cycle-002)

Stated once, plainly, because it governs every lane:

1. `n` is the length of the frozen seed-set (`eval/run_eval.py:121`).
2. The seed-set is one of the four `regime-v001` components (`frozen/regimes/regime-v001.json:4-7`).
3. Any change to any component is a **new regime**, never an edit; never compare across regimes
   (`frozen/regimes/regime-v001.json:9`; `docs/claim-ceiling.md:29-35,62-64`; NFR-5).
4. Therefore **larger `n` ⇒ `regime-v002`** — explicitly the design's intended path
   (`frozen/seeds/seed-set-v001.json` `n_note`).
5. `regime-v002` numbers are **not** comparable to the v001 ledger rows. "Same-regime" in Cycle-002 means
   *same `regime-v002` across the batch* — a fresh baseline-vs-candidate pair under v002.
6. Creating `regime-v002` is an **additive** frozen artifact (a new file), mirroring the taxonomy's
   `-v002` convention — but writing it and running larger evals is a **build action** that needs the
   build gate (OA-2).

This is not a complication to be worked around; it is the correct, honest meaning of "scale" in this
design. Cycle-002 grows the evaluation by *adding* a regime, not by mutating the one that anchors the
historical record.

## 7. Candidate Cycle-002 lanes

The brief enumerates lanes A–G. Each is evaluated against the regime-v002 constraint, the Rung-1 ceiling,
and the "agents frozen, evaluation varies" bright line.

| Lane | Title | Recommendation | Why |
|---|---|---|---|
| **A** | Evaluation Scale | **In scope (core)** | Raise `n` via a new `regime-v002`; the headline capability of the cycle. Requires §6 framing so v002 is never compared to v001. |
| **B** | Comparison Confidence | **In scope (descriptive only)** | Descriptive dispersion language across repeated batches; inferential statistics stay gated (RQ-7). |
| **C** | Repeated Same-Regime Batches | **In scope (core)** | Repeated batches under one `regime-v002`, same frozen agents; the mechanism that makes B meaningful. |
| **D** | Run Cost + Runtime Budget | **In scope (prerequisite — do first)** | Measure wall-clock/disk at larger `n` before committing to a batch size; throughput is cheap but storage/IO is not free (RQ-5). |
| **E** | Claim-Ceiling Progression Criteria | **In scope (criteria/docs only)** | Define what a future Rung 2 *consideration* would require (RQ-4). Defines; never claims. |
| **F** | Reproducibility Reality | **In scope (document/confirm only)** | Confirm `seed_controlled=false` still holds; document what "stable" means without byte-replay and how it bounds B (RQ-8). No seed-control build. |
| **G** | Reporting / Ledger Discipline | **In scope (cross-cutting constraint)** | Decide how many runs are recorded, when a ledger row is allowed, and which reports stay local/ignored. Keeps the ledger from bloating with a row per batch. |

**Narrow recommended spine: D → A → C/B, with G binding throughout and E/F as planning/criteria-only.**
The artifact does **not** recommend all lanes as build work at once — A/C/B/D are the buildable core (behind
OA-2); E/F/G are docs/criteria/constraint work.

## 8. Recommended Cycle-002 mission

**Mission:** Stand up a stable, sanitized, larger same-regime evaluation harness under a new
`regime-v002`, capable of running repeated same-regime batches cheaply and reporting observed dispersion
descriptively — with the runtime agents frozen, every claim bounded to Rung 1, the ledger preserved as the
only ceiling-bearing artifact, and no cross-regime comparison.

**Framing label:** "Evaluation Scale + Comparison Confidence" (equivalently, "From n=12 Toy Comparison to
Stable Evaluation Harness").

**Non-goals (binding):** no runtime-agent change of any kind; no per-decision quality scoring; no inferential
significance machinery (descriptive dispersion only); no claim-ceiling movement; no cross-regime comparison;
no comparison of v002 numbers to v001 rows. The mission improves *how well TurnTrace evaluates*, not *how
well the agent plays* (`docs/operator/deferred-lane-gate-after-sprint-01.md:89-97`).

## 9. Recommended in-scope planning

Confined to the evaluation/offline/provenance layers. Tasks that write App-Zone code
(`eval/`, `analysis/`, `frozen/`) land only through `/implement → /review-sprint → /audit-sprint` and
require an opened Cycle-002 build gate (OA-2); pure-docs/criteria tasks open no gate.

1. **Cost + budget dry run (Lane D)** — measure wall-clock and disk for a single larger-`n` run before any
   batch commitment; record a safe batch size and a storage ceiling. Non-deliverable; `--no-ledger` /
   default no-ledger path (`eval/run_eval.py:333-336`); outputs local/ignored.
2. **`regime-v002` definition (Lane A)** — author a new frozen seed-set with a justified larger `n` (and a
   new `regime-v002.json` tuple), reusing the existing opponent-pool/deck-pool/metrics-spec *by reference and
   hash only*. Additive new files; never an edit of v001. The deck-drift and immutability guards
   (`eval/run_eval.py:128-154`) must hold unchanged.
3. **Repeated same-regime batches (Lane C)** — run baseline (`random_legal`) and candidate
   (`scripted_baseline`) *both under `regime-v002`*, repeated K times, frozen agents, into K sealed run dirs.
   Non-deliverable by default; the existing per-`run_id` immutability + idempotency carry the discipline.
4. **Descriptive dispersion report (Lanes B + G)** — a new cross-run roll-up reading K sealed run dirs under
   one regime and emitting sanitized observed dispersion (range/mean/median/spread per metric) with a Rung-1
   footer and no ceiling; counts/aggregates only, never raw rows (sanitization contract per
   `analysis/failure_report.py:8-19`). Output local/ignored unless operator-approved.
5. **Rung 2 readiness criteria (Lane E)** — a tracked criteria doc stating what artifacts/validations a future
   Rung 2 *consideration* would minimally require (RQ-4), explicitly **not** claiming Rung 2 and explicitly
   noting that any inferential design + ceiling advance is a separate operator decision.
6. **Reproducibility-reality note (Lane F)** — confirm/record `seed_controlled=false`, define "stable" as
   distribution-stable + audit-trail at the larger `n`, and document how unseeded draws bound the dispersion
   story (no agent-vs-RNG variance separation; RQ-8). Pure docs.
7. **Ledger/report discipline note (Lane G)** — record that non-deliverable scale/variance runs write **no**
   ledger row (default), that the ledger is not to grow a row per batch, and that larger-run reports stay
   local/ignored unless explicitly operator-approved.

## 10. Explicit out-of-scope list (forbidden / mention-only)

Opening any of these requires a separate, explicit operator decision that supersedes the standing notes.

**Broad-optimization (still closed — `docs/operator/deferred-lane-gate-after-sprint-01.md:71-87`;
`docs/cycles/cycle-001/closeout.md:103-115`):**
runtime-agent tuning; runtime-agent heuristic changes; RL; self-play; deck optimizer; value model;
win-probability model; search / lookahead / MCTS; ELO; tournament system; multi-agent tournament
comparisons; agent tuning loops; dashboard; Kaggle upload automation; leaderboard optimization; submission
packaging; two-direction ablation ledger; SaaS / product surface.

**Claim / evidence boundaries (`docs/claim-ceiling.md:20-64`):**
claim-ceiling upgrade above Rung 1; statistical-significance claims without explicit design and operator
approval; cross-regime comparison / uplift (hard-refused, exit 2); gameplay-strength claims; the forbidden
words *strong / competitive / optimal / calibrated / complete* except as negated language; directly making
the runtime agent stronger in any way; per-decision agent-quality detectors/scorers (FM-03/04/06/08 stay
`detector: forbidden`); byte-identical determinism work while `seed_controlled=false`.

**Sanitization / data boundaries (`docs/operator/turntrace-loop-contract.md:59-68`):**
committing or embedding Competition Data — card IDs, card names, deck lists, hand contents, simulator logs,
raw trace rows, run-dir file dumps, PDFs/CSVs, `deck.csv` rows; raw trace/card/deck inspection or emission
into tracked artifacts; full `runs/<run_id>/` trees becoming tracked (stay local/ignored, ESP-1).

**Process / regime boundaries:**
editing the `.claude/` System Zone; **editing `regime-v001` or any of its components** (a larger seed-set is
a *new* regime-v002 file, never an edit of v001); comparing `regime-v002` numbers to the v001 ledger rows;
out-of-loop edits to sprint code; premature COMPLETED marker; any build before the operator opens the
Cycle-002 build gate (OA-2).

## 11. Evidence-storage constraints

Per `docs/operator/turntrace-loop-contract.md:59-68` / ESP-1..ESP-5 / SP-6:

- **Full run dirs remain local/ignored** — at the larger `n`, the `runs/<run_id>/` trees (records, traces,
  manifest, hashes, summary.csv) stay git-ignored by default; only `runs/.gitkeep` is tracked.
- **Generated larger-run reports remain local/ignored unless operator-approved** — the descriptive dispersion
  report and any failure report `--out` artifact default to local/ignored (ESP-1 / OD-8;
  `analysis/failure_report.py:27-29`). Promotion to tracked status requires explicit operator approval (SP-6
  relaxation).
- **Tracked docs may reference only** `run_id`, content hashes, sanitized metrics, aggregate categories,
  claim ceilings, and local path/status.
- **No raw traces. No card IDs. No card names. No deck lists. No simulator logs. No Competition Data.**
- **`docs/ledger.md` remains the only ceiling-bearing artifact** — and is *not* to grow a row per scale/variance
  batch; non-deliverable runs write no ledger row by default (`eval/run_eval.py:281-288`). Only a deliberately
  designated deliverable run gets a row, by explicit intent (`--deliverable` / `--ledger`).
- **`requires-raw-data: cannot-surface`** — actual per-run distributions and run-dir file contents are never
  surfaced in any planning or tracked artifact.

## 12. Possible Cycle-002 sprint structure (to explore, not finalize)

Mirrors the brief's proposed structure, refined by the §6 regime-v002 constraint. This is a planning sketch;
the PRD/SDD/sprint-plan finalize it, and no sprint runs before OA-2.

**Sprint 00 — Scale Baseline / Dry Run (Lanes D + A-foundation + G):**
define `regime-v002` (new frozen seed-set at a justified larger `n`, tuple by reference + hash); measure
runtime/disk budget on a single larger-`n` dry run; confirm the immutability + deck-drift + hygiene guards hold
at scale; establish no-ledger-by-default mechanics and local/ignored sanitized outputs. Deliverable: a sanitized
budget/mechanics note + the additive `regime-v002` frozen files.

**Sprint 01 — Repeated Same-Regime Batch Comparison (Lanes C + B + reporting):**
run K repeated batches under `regime-v002` with the **frozen** agents; build the cross-run descriptive
dispersion roll-up (RQ-6); report observed spread with Rung-1 footer, descriptive language only, no inferential
statistics. Deliverable: a sanitized dispersion note (local/ignored unless operator-approved) + the roll-up tool
(behind OA-2).

**Sprint 02 — Claim-Ceiling Criteria / Rung 2 Readiness (Lanes E + F):**
write the Rung 2 *readiness criteria* doc (what a future consideration would require; RQ-4) and the
reproducibility-reality note (RQ-8). Pure docs/criteria; claims nothing above Rung 1; names the inferential-design
+ ceiling-advance decision as a separate, later operator decision. Deliverable: tracked criteria + reproducibility
docs.

> The artifact may be restructured by the PRD if evidence warrants (e.g. folding D into a single Sprint 00 task,
> or splitting the roll-up tool from the batch runs). The three-sprint shape above is the recommended starting
> point.

## 13. Open questions (for the PRD to resolve)

1. **Target `n` for `regime-v002`.** What larger `n` is justified — and on what basis (sampling resolution vs
   disk/time budget from the Sprint 00 dry run)? The brief and design leave `n` open; the dry run informs it.
2. **Batch count K.** How many repeated same-regime batches make the dispersion description meaningful while
   staying cheap and avoiding artifact proliferation?
3. **Reuse vs re-mint of non-seed components.** May `regime-v002` reuse `opponent-pool-v001` / `deck-pool-v001` /
   `metrics-spec-v001` by reference+hash (so only the seed-set differs), or does the operator want fresh
   components? Either way it is a new regime; the question is how much changes.
4. **Where does the descriptive dispersion report live?** Local/ignored by default is recommended; does the
   operator want a single sanitized, tracked summary at cycle close (SP-6 relaxation), or strictly local?
5. **Ledger row policy for scale runs.** Confirm that scale/variance batches write **no** ledger row, and that at
   most one deliberately designated deliverable run per regime may carry a row.
6. **Descriptive-statistics vocabulary.** Ratify the exact allowed dispersion vocabulary (range/mean/median/spread)
   and the explicit exclusion of CIs/p-values/"significant," so the reviewer/auditor has a bright line.
7. **Carry-forward CF-04.** `.beads/.br_history/` gitignore housekeeping remains open from Cycle-001; fold in or
   handle separately? (The live `.beads/issues.jsonl` dirty state is expected and stays unstaged.)

## 14. Risks

| # | Risk | Mitigation |
|---|------|------------|
| R1 | **Cross-regime contamination** — v002 numbers narrated as bigger/smaller than the v001 n=12 result, breaking NFR-5. | §6 framing front-and-center; `delta_report`'s exit-2 refusal stays intact; every v002 statement carries `regime-v002` + `n`; never place a v002 number beside a v001 row as a comparison. |
| R2 | **Accidental agent optimization** — "scale the evaluation" drifts into tuning, seed/regime-shopping, or a per-decision scorer. | Agents stay frozen (no `agents/runtime/` edit); the `regime-v002` seed-set is chosen on neutral grounds and hash-pinned before any agent runs; FM-03/04/06/08 stay `detector: forbidden`; reject agent-decision-logic touches at review/audit (RQ-10). |
| R3 | **Confidence-language overreach** — descriptive dispersion presented as inferential (CIs, "significant"), implicitly raising the rung. | Ratify the descriptive-only vocabulary (Q6); ban inferential terms in tracked outputs; Rung-1 footer on every non-ledger artifact; audit greps for forbidden words and inferential phrasing. |
| R4 | **Claim-ceiling inflation** — a larger-`n` win_rate movement read as the agent being "better," crossing Rung 1. | Keep the ceiling at Rung 1 as an explicit AC; the ledger stays the sole ceiling-bearer; Rung 2 is criteria-only (Lane E), never claimed; forbidden words banned except negated. |
| R5 | **Competition-Data / raw-trace leakage at scale** — more/larger runs increase the surface for a careless read of trace rows into a tracked report. | Restrict all roll-ups to coarse sanitized fields (counts/rates/dispersion); keep `eval/hygiene_check.py` active; reports local/ignored by default; audit confirms no raw contents embedded. |
| R6 | **Storage/cost surprise** — many large batches exhaust local disk or slow trace I/O. | Sprint 00 dry run measures wall-clock + disk and sets a safe batch size and storage ceiling *before* Sprint 01 commits to K (RQ-5). |
| R7 | **Building before the gate** — this planning artifact misread as authorization to `/implement`. | Reaffirm loop contract §6: planning never opens the gate; no `/implement` / `/run` until OA-2; PRD is the next step, not build. |
| R8 | **Unseeded variance misattribution** — dispersion across batches presented as the agent's variance when it conflates agent + uncontrolled RNG. | Document the `seed_controlled=false` constraint (Lane F) inline in any dispersion report; frame dispersion as the whole-process observation, never an isolated agent estimate (RQ-8). |

## 15. Operator decisions needed before the PRD

1. **Accept this research/planning artifact** and authorize moving to a **Cycle-002 PRD** (next Golden-Path
   step). This artifact opens no build gate; the PRD is planning, not build.
2. **Confirm the narrow mission and scope** — "Evaluation Scale + Comparison Confidence," in-scope spine
   D → A → C/B with G binding and E/F criteria-only; agent-optimization lane stays **closed**.
3. **Ratify the regime-v002 framing** — larger `n` is a new `regime-v002`; v002 is never compared to the v001
   ledger rows; `regime-v001` and its components are never edited.
4. **Confirm the descriptive-vs-inferential line** — descriptive dispersion allowed; CIs / p-values /
   significance gated behind a separate explicit design + approval decision.
5. **Confirm Rung-1 hold** — the ceiling stays Rung 1 for the whole cycle; Lane E defines Rung 2 *criteria* only
   and claims nothing.
6. **Confirm evidence-storage policy at scale** — full run trees and larger-run reports stay local/ignored;
   ledger gets no row per batch; any tracked sanitized summary requires explicit SP-6 relaxation.
7. **Note the open questions** in §13 (target `n`, batch count K, component reuse, report location, ledger
   policy, vocabulary, CF-04) to be resolved in the PRD.

## 16. Recommendation: whether to proceed to a Cycle-002 PRD

**PROCEED to a Cycle-002 PRD** — along the narrow scope in §8–§9, and **only** into PRD (planning), not build.
Implementation begins only after the operator opens an explicit Cycle-002 build gate (OA-2).

Reasoning:

1. **The next step is sanctioned and bounded.** The Cycle-001 closeout explicitly recommends Cycle-002 as
   "Evaluation Scale + Comparison Confidence" and lists exactly these lanes, while opening no build gate
   (`docs/cycles/cycle-001/closeout.md:82-119`). A PRD is the correct, low-risk next move.
2. **The scope is concrete, grounded, and non-optimization.** Raising `n` via an additive `regime-v002`,
   running repeated same-regime batches with frozen agents, and adding a descriptive cross-run roll-up are all
   evaluation-harness work — the design already anticipates the larger-`n`/regime-v002 path
   (`frozen/seeds/seed-set-v001.json` `n_note`), and the reporting gap (no cross-run aggregator) is real and
   well-scoped (RQ-6).
3. **The guardrails hold by construction.** Rung 1 stays the ceiling; the ledger stays the only ceiling-bearer;
   cross-regime comparison is hard-refused; descriptive-only language keeps significance gated; agents stay
   frozen; sanitization and the hygiene guard are unchanged. The cycle improves *evaluation confidence*, not
   *agent strength*.
4. **The single hard gate is procedural.** This artifact opens no build gate; the operator must accept it (and
   later issue OA-2) before any code. Until then, only the PRD may proceed.

---

> **Sources:** `docs/cycles/cycle-001/closeout.md`; `docs/cycles/cycle-001-sprint-00/closeout.md`;
> `docs/cycles/cycle-001-sprint-01/closeout.md`; `docs/cycles/cycle-001-sprint-02/{00-research-and-planning,closeout}.md`;
> `docs/operator/{turntrace-loop-contract,deferred-lane-gate-after-sprint-01}.md`; `docs/claim-ceiling.md`;
> `docs/ledger.md`; `docs/strategy-report.md`; `docs/failure-mode-taxonomy-v001.md`;
> `docs/cycles/cycle-000-bootstrap/{01-turntrace-prd,02-turntrace-sdd}.md`; `frozen/regimes/regime-v001.json`;
> `frozen/seeds/seed-set-v001.json`; `eval/run_eval.py`; `eval/hygiene_check.py`; `analysis/aggregate.py`;
> `analysis/failure_report.py`. Expected main at authoring: `beac070`.
