# Cycle-002 PRD — Evaluation Scale + Comparison Confidence

> Planning artifact (PRD). Status: **DRAFT — research/planning only.** This document opens **NO build gate**.
> Implementation requires a separate, explicit operator build-gate action (OA-2 equivalent) per
> `docs/operator/turntrace-loop-contract.md` §6.
> Binding planning input: `docs/cycles/cycle-002/00-research-and-planning.md` (the accepted Cycle-002
> research artifact; it too opens no build gate).
> Sanitized note. No raw traces, card IDs/names, deck lists, simulator logs, PDFs/CSVs, or Competition
> Data appear here (CC-1/CC-2, ESP). Runs are referenced by `run_id`, hashes, sanitized metrics, claim
> ceilings, and local path/status only. The forbidden agent claim words (*strong / competitive / optimal /
> calibrated / complete*) appear only as negated/forbidden language.

| Field | Value |
|---|---|
| **Cycle** | Cycle-002 |
| **Working title** | Evaluation Scale + Comparison Confidence |
| **Alt. framing** | From n=12 Toy Comparison to Stable Evaluation Harness |
| **Type** | Product Requirements Document (planning artifact, not a build artifact) |
| **Status** | DRAFT — awaiting operator acceptance; next Golden-Path step is SDD / architecture, not implementation |
| **Date** | 2026-06-18 |
| **Current main** | `beac070` — *docs: close TurnTrace Cycle 001* |
| **Binding input** | `docs/cycles/cycle-002/00-research-and-planning.md` (written + staged; commit pending operator decision) |
| **Posture** | Improve the EVALUATION HARNESS, not the agent |
| **Claim ceiling** | Rung 1 (unchanged; not raised) |

## Required posture (binding)

- **Cycle-002 planning opens no build gate.** This PRD authorizes no code.
- **Cycle-002 improves evaluation scale and comparison confidence, not runtime-agent strength.**
- **Broad optimization remains closed.** Every "Still closed" item
  (`docs/operator/deferred-lane-gate-after-sprint-01.md:71-87`) stays closed and requires a separate,
  explicit operator decision to open.
- **The runtime-agent improvement lane remains closed.** No change to agent behavior, rules, heuristics,
  or scoring.
- **The claim ceiling remains Rung 1** for all of Cycle-002 until an explicit later operator decision earns
  otherwise (`docs/claim-ceiling.md`; `docs/cycles/cycle-001/closeout.md:8`).
- **`regime-v001` and its components are never edited.** Larger `n` is an *additive* `regime-v002`, never a
  mutation of v001; `regime-v002` numbers are never compared to the v001 ledger rows (NFR-5;
  `frozen/regimes/regime-v001.json:9`).

The bright line for the whole cycle: **Cycle-001 held the regime fixed and varied the agent once;
Cycle-002 holds the agents frozen and varies only the *evaluation* (scale + repetition + reporting)**
(`docs/cycles/cycle-002/00-research-and-planning.md:42-44`).

## 1. Product / cycle overview

TurnTrace is a local, sanitized evaluation harness for a card-game simulator. Cycle-001 ("Evidence
Foundation") proved it can **produce, compare, explain, review, audit, and close** local simulator
evidence **without leaking Competition Data or overclaiming** (`docs/cycles/cycle-001/closeout.md:23-24`),
earning a first same-regime, agent-only comparison — `run-0001` (`random_legal-v001`) vs `run-0002`
(`scripted-v001`) under `regime-v001` at **n=12** — bounded to **ladder Rung 1**
(`docs/ledger.md:11-12`). The Cycle-001 closeout recommends Cycle-002 as "Evaluation Scale + Comparison
Confidence" (`docs/cycles/cycle-001/closeout.md:82-101`); the accepted research artifact translates that
into a narrow, repo-grounded plan (`docs/cycles/cycle-002/00-research-and-planning.md`).

**Mission (binding).** Stand up a stable, sanitized, larger same-regime evaluation harness under a new
`regime-v002`, capable of running repeated same-regime batches cheaply and reporting observed dispersion
descriptively — with runtime agents frozen, every claim bounded to Rung 1, the ledger preserved as the
only ceiling-bearing artifact, and no cross-regime comparison.

**Recommended spine (research artifact §7-§9):**

- **D** — run cost / runtime budget first.
- **A** — evaluation scale via additive `regime-v002`.
- **C/B** — repeated same-regime batches plus descriptive-dispersion reporting.
- **G** — ledger/report discipline as a cross-cutting constraint.
- **E/F** — criteria/docs only, not claim-bearing build work.

**Who consumes this PRD.** The **operator** (owns gate decisions; the only party who may open a "Still
closed" lane; decides whether to proceed to SDD); the future **implementer** (`/implement`, the single
patch authority once OA-2 opens); the **reviewer/auditor** (`/review-sprint`, `/audit-sprint`, pure-review
gates); and a **downstream evidence reader** who must understand the comparison from sanitized, tracked
artifacts alone (`docs/operator/turntrace-loop-contract.md` §1-§3, §6, §10).

## 2. Problem statement

The n=12 comparison is useful but **not enough for stable evaluation confidence**:

1. **n=12 is explicitly a small sample.** The strategy report names it a limitation
   (`docs/strategy-report.md:104`), and the seed-set rationale already frames n=12 as "a modest Sprint-00
   set … leaves ample headroom to raise N in a future regime-v002" (`frozen/seeds/seed-set-v001.json`
   `n_note`). At n=12 the harness cannot describe how much a metric *would move run-to-run* under the same
   conditions — the sampling dispersion is invisible.
2. **There is no repeated-batch capability.** Every artifact to date is a single sealed run; nothing runs
   the *same* regime repeatedly to observe spread.
3. **There is no cross-run reporting.** `analysis/aggregate.py` emits one `summary.csv` + at most one ledger
   row per run (`analysis/aggregate.py:29-40`); `analysis/failure_report.py` reads one run dir;
   `analysis/delta_report.py` compares exactly two runs. **No cross-run / cross-batch aggregator exists**
   (research artifact §2.1 RQ-6).
4. **Scaling `n` is not a free parameter.** `n` is the length of the frozen seed-set
   (`eval/run_eval.py:121`), and the seed-set is one of the four `regime-v001` components
   (`frozen/regimes/regime-v001.json:4-7`); any component change is a **new regime, never an edit**
   (`frozen/regimes/regime-v001.json:9`; `docs/claim-ceiling.md:29-35`). So "scale" has a precise,
   constrained meaning that the product requirements must encode (see §7).

None of these problems is about agent strength. All are about **evaluation scale and the confidence with
which the harness can describe what it observed.**

## 3. What Cycle-002 must prove (goals)

- **G1 — Scale safely via an additive regime.** Establish that a larger `n` can be run as an additive
  `regime-v002` without editing `regime-v001` and without comparing across regimes (NFR-5).
- **G2 — Know the cost before committing.** Measure wall-clock and disk for a single larger-`n` run and
  record a safe batch size and storage ceiling *before* committing to repeated batches.
- **G3 — Run repeated same-regime batches.** Run the **frozen** agents repeatedly under one `regime-v002`
  into K sealed run dirs, cheaply and reproducibly-by-policy (distribution-stable + audit-trail).
- **G4 — Report observed dispersion descriptively.** Produce a sanitized cross-run roll-up that reports the
  observed dispersion of each metric (range/mean/median/spread) with `n`, K, and `regime_id`, carrying a
  Rung-1 footer and no ceiling of its own.
- **G5 — Hold the line on claims.** Keep every Cycle-002 artifact at Rung 1; keep `docs/ledger.md` the only
  ceiling-bearing artifact; allow descriptive dispersion only, never inferential statistics.
- **G6 — Define (not claim) Rung 2 readiness.** Record what a future Rung 2 *consideration* would require,
  explicitly without claiming Rung 2.
- **G7 — Document reproducibility reality.** Record that `seed_controlled=false` still holds and what
  "stable" means without byte-identical replay, and how unseeded draws bound the dispersion story.
- **G8 — Preserve discipline.** Keep ledger/report/sanitization discipline intact at the larger scale (no
  row per batch; reports local/ignored by default; hygiene guard active).

## 4. What Cycle-002 must not prove or claim (non-goals)

- **NG1 — No runtime-agent change of any kind.** No tuning, heuristic change, rule change, or scoring change
  to `agents/runtime/`. The agents (`random_legal`, `scripted_baseline`) stay **frozen**
  (`docs/operator/deferred-lane-gate-after-sprint-01.md:89-97`).
- **NG2 — No claim above Rung 1.** No gameplay-strength, statistical-significance, cross-regime, leaderboard,
  or calibration claim; no claim-ceiling upgrade (`docs/claim-ceiling.md:20-64`).
- **NG3 — No inferential statistics without separate approval.** No confidence intervals, p-values,
  "significant," hypothesis tests, or inferential error bars. Descriptive dispersion only (§9).
- **NG4 — No cross-regime comparison.** `regime-v002` numbers are never placed beside v001 ledger rows as a
  comparison; cross-regime comparison stays hard-refused (`analysis/delta_report.py` exit 2;
  `docs/claim-ceiling.md:62-64`).
- **NG5 — No per-decision agent-quality scoring/detectors.** FM-03/04/06/08 stay `detector: forbidden`
  (`docs/failure-mode-taxonomy-v001.md:40-52`).
- **NG6 — No raw-data exposure.** No raw decision-trace rows, card IDs/names, deck lists, hand contents,
  simulator logs, PDFs/CSVs, or run-dir dumps in any tracked artifact.
- **NG7 — No regime-v001 mutation.** No edit to `regime-v001` or any of its frozen components (a component
  change is a new regime — `docs/claim-ceiling.md:29-35`).
- **NG8 — No byte-identical determinism work while `seed_controlled=false`.** No manufactured or simulated
  seed control (`docs/claim-ceiling.md:42-52`).
- **NG9 — No broad-optimization lane.** RL · self-play · deck optimizer · value model · win-probability
  model · search/lookahead/MCTS · ELO/tournament system · multi-agent tournament comparisons · leaderboard
  optimization · Kaggle upload automation · submission packaging · dashboard · SaaS/product surface ·
  two-direction ablation ledger (`docs/operator/deferred-lane-gate-after-sprint-01.md:71-87`).
- **NG10 — No build gate.** This PRD and the SDD that follows authorize no code.

## 5. Functional requirements

Each requirement cites the lane it serves (research artifact §7) and its class. **Build** = writes App-Zone
code (`eval/`, `analysis/`, `frozen/`) or runs evaluations → requires an opened build gate (OA-2) and lands
through `/implement → /review-sprint → /audit-sprint`. **Docs** = tracked sanitized documentation → opens no
gate. IDs are stable and namespaced `C2-FR-#`.

| ID | Title | Lane | Class |
|---|---|---|---|
| **C2-FR-1** | Runtime-budget / cost dry-run | D | Build |
| **C2-FR-2** | `regime-v002` definition (additive frozen seed-set + tuple) | A | Build |
| **C2-FR-3** | Repeated same-regime batches (frozen agents) | C | Build |
| **C2-FR-4** | Cross-run descriptive-dispersion report | B + reporting | Build |
| **C2-FR-5** | Rung 2 readiness criteria doc | E | Docs |
| **C2-FR-6** | Reproducibility-reality note | F | Docs |
| **C2-FR-7** | Ledger/report-discipline note | G | Docs |

### C2-FR-1 — Runtime-budget / cost dry-run (Build, Lane D)

**Requirement.** Before any repeated-batch commitment, run a single larger-`n` evaluation and produce a
sanitized budget note recording: measured wall-clock for the run, on-disk size of the sealed run tree, and a
derived **safe batch size** and **storage ceiling** for Cycle-002. The dry-run is **non-deliverable** — it
writes no ledger row (default no-ledger path; `eval/run_eval.py:333-336`) and its outputs stay local/ignored.

- **Rationale / source.** Lane D, "do first" (research artifact §7, §9.1). Simulator throughput is not the
  bottleneck (~80-190 matches/s; `frozen/seeds/seed-set-v001.json` `n_note`); the real cost risks are disk,
  trace I/O, and artifact proliferation (research artifact §2.1 RQ-5).
- **Constraint.** Non-deliverable; no ledger row; no tracked raw outputs. The budget note is sanitized
  (numbers about time/size only — no run contents).

### C2-FR-2 — `regime-v002` definition (Build, Lane A)

**Requirement.** Author an **additive** frozen seed-set at a justified larger `n` and a new `regime-v002.json`
tuple referencing its four components by id + content hash. Reuse of `opponent-pool-v001` / `deck-pool-v001` /
`metrics-spec-v001` by reference + hash vs re-minting is an open operator decision (OD-3). The new files are
**additive** (never an edit of v001); the deck-drift and immutability guards must hold unchanged
(`eval/run_eval.py:128-154`).

- **Rationale / source.** Lane A; the design's explicitly intended scale path
  (`frozen/seeds/seed-set-v001.json` `n_note`; research artifact §6).
- **Constraint.** `regime-v001` and its components are never edited (NG7). The seed-set / regime must be
  chosen on **neutral grounds and hash-pinned before any agent runs** — no regime/seed-shopping to flatter an
  agent (research artifact §2.1 RQ-10). Because the seed-set is unseeded match-indices, the larger seed-set is
  a larger *match-index list*, still `mode=unseeded` (`frozen/seeds/seed-set-v001.json`).

### C2-FR-3 — Repeated same-regime batches (Build, Lane C)

**Requirement.** Run the baseline (`random_legal`) and candidate (`scripted_baseline`) **both under
`regime-v002`**, repeated **K** times, into K sealed, immutable run dirs. The agents are **frozen**; the only
thing that repeats is the evaluation. Runs are **non-deliverable by default** (no ledger row). K is an open
operator decision (OD-4).

- **Rationale / source.** Lane C; the mechanism that makes dispersion reporting meaningful (research artifact
  §7, §9.3).
- **Constraint.** "Same-regime" means *same `regime-v002` across the batch*. The per-`run_id` immutability
  guard + idempotency carry the discipline (`eval/run_eval.py:138-154`). No `agents/runtime/` edit (NG1).
  Because runs are unseeded, repeated batches are **fresh draws from the same distribution, not
  reproductions** (§9, NG8).

### C2-FR-4 — Cross-run descriptive-dispersion report (Build, Lane B + reporting)

**Requirement.** Add an analysis-layer roll-up that reads **K sealed run dirs under a single `regime-v002`**
and emits the **observed dispersion** of each sanitized metric across the K runs — **range, mean, median,
spread** — each statement carrying `n`, `K`, and `regime_id`, with a Rung-1 footer and **no ceiling of its
own**. It emits **sanitized aggregates/counts only**, never raw rows, mirroring `analysis/failure_report.py`'s
sanitization contract (`analysis/failure_report.py:8-19`). Output is **local/ignored by default**.

- **Rationale / source.** Lanes B + reporting; fills the cross-run aggregator gap (research artifact §2.1
  RQ-6, §9.4).
- **Constraint (descriptive only).** **No inferential statistics** — no confidence intervals, p-values,
  "significant," hypothesis tests, or inferential error bars (NG3; §9). It must **refuse to mix regimes** (all
  K runs must share one `regime_id`), consistent with the never-cross-regime invariant (NFR-5). It does not
  import `agents/runtime/`, `cabt`, `sim/`, or `eval/` (offline/runtime separation, NFR-1).

### C2-FR-5 — Rung 2 readiness criteria doc (Docs, Lane E)

**Requirement.** Produce a tracked criteria document stating what a future Rung 2 *consideration* would
minimally require (research artifact §2.1 RQ-4): a same-regime baseline-vs-candidate comparison at a justified
larger `n` under one regime; an explicitly *designed and operator-approved* inferential procedure; the
candidate exceeding the random-legal baseline by a pre-registered margin under that design; provenance +
audit-trail intact; and a deliberate operator-authorized advance of the ledger row's `claim_ceiling`. The doc
**explicitly does not claim Rung 2** and records that the inferential design + ceiling advance is a separate
operator decision.

- **Rationale / source.** Lane E (criteria only); Rung 2 = "beats random-legal"
  (`docs/cycles/cycle-000-bootstrap/01-turntrace-prd.md:274-276`;
  `docs/cycles/cycle-000-bootstrap/02-turntrace-sdd.md:840`).
- **Constraint.** Criteria/docs only; no claim above Rung 1 (NG2); no forbidden claim words.

### C2-FR-6 — Reproducibility-reality note (Docs, Lane F)

**Requirement.** Produce a tracked note that (a) confirms/records `seed_controlled=false`
(`docs/claim-ceiling.md:42-52`), (b) defines "stable" at the larger `n` as **distribution-stable +
audit-trail** (not byte-identical), and (c) documents that, because runs are unseeded, observed dispersion
**conflates agent behavior with uncontrolled simulator RNG and cannot be separated** into an isolated
"agent variance" without seed control (research artifact §2.1 RQ-8).

- **Rationale / source.** Lane F (document/confirm only).
- **Constraint.** No manufactured or simulated seed control (NG8); byte-identical replay remains a future
  upgrade only if seed control is later proven.

### C2-FR-7 — Ledger/report-discipline note (Docs, Lane G — cross-cutting)

**Requirement.** Record the standing discipline for the larger scale: non-deliverable scale/variance runs
write **no** ledger row (the current default; `eval/run_eval.py:281-288`); the ledger **does not grow a row
per batch**; only an **explicitly designated deliverable run** may write a ledger row (explicit
`--deliverable` / `--ledger` intent); and larger-run reports stay **local/ignored unless operator-approved**
(SP-6 relaxation).

- **Rationale / source.** Lane G (cross-cutting constraint); research artifact §9.7, §11.
- **Constraint.** Docs/policy only — codifies existing behavior; requires no code change to the
  already-enforced no-ledger-by-default path.

## 6. Non-functional requirements / technical posture

PRD-local IDs `C2-NFR-#`. Where a requirement inherits a **global invariant**, that invariant is cited by its
established name (offline/runtime separation **NFR-1**; reproducibility posture **NFR-3**; never-cross-regime
**NFR-5**; stdlib-only **NFR-7**) — this PRD does not renumber the global invariants.

- **C2-NFR-1 — Claim ceiling stays Rung 1.** No Cycle-002 artifact asserts a claim above Rung 1; the ledger
  remains the only ceiling-bearing artifact (`docs/claim-ceiling.md:5-6`).
- **C2-NFR-2 — Agents frozen / offline-runtime separation preserved.** No `agents/runtime/` change; all new
  analysis code imports run-dir artifacts only, never `agents/runtime/`, `cabt`, `sim/`, or `eval/`
  (global NFR-1; `analysis/aggregate.py:12-14`).
- **C2-NFR-3 — Sanitization / Competition-Data hygiene.** Every tracked artifact passes
  `eval/hygiene_check.py`; no Competition Data path is ever staged (CC-1/CC-2; `eval/hygiene_check.py:35-45`).
- **C2-NFR-4 — Evidence storage local-by-default.** Full run dirs and larger-run reports stay
  local/git-ignored by default (ESP-1); promotion to tracked status requires explicit operator approval
  (SP-6).
- **C2-NFR-5 — Never compare across regimes.** Global **NFR-5** holds; the dispersion report and all narrative
  refuse to mix regimes; `regime-v002` is never compared to v001 rows.
- **C2-NFR-6 — Descriptive-only statistics.** Only descriptive dispersion (range/mean/median/spread) appears
  in any tracked output; inferential statistics are gated behind a separate explicit design + operator
  approval (§9).
- **C2-NFR-7 — Reproducibility posture preserved.** `mode=unseeded`; distribution-stable + audit-trail; the
  determinism tier stays skipped under `seed_controlled=false`, never silently passed (global NFR-3;
  `docs/claim-ceiling.md:42-52`).
- **C2-NFR-8 — stdlib-only + loop discipline.** New code is stdlib-only (global NFR-7); all App-Zone code lands
  through `/implement → /review-sprint → /audit-sprint`, integrated fast-forward only, one review + one audit
  artifact (`docs/operator/turntrace-loop-contract.md` §1-§3).
- **C2-NFR-9 — Immutability + provenance preserved.** The immutability guard (exit 3), deck-drift guard, and
  source-hash provenance hold unchanged at the larger `n` (`eval/run_eval.py:128-173`).

## 7. `regime-v002` requirements and constraints

The spine of the cycle (research artifact §6). Stated as requirements:

1. **Larger `n` ⇒ `regime-v002`.** `n` is the length of the frozen seed-set (`eval/run_eval.py:121`), and the
   seed-set is a regime component (`frozen/regimes/regime-v001.json:4-7`); any component change is a **new
   regime, never an edit** (`frozen/regimes/regime-v001.json:9`). A larger-`n` run **must** be a new
   `regime-v002`. *(Mapped to C2-FR-2.)*
2. **Additive, never a mutation.** `regime-v002` is authored as **new** frozen files (seed-set + tuple),
   mirroring the taxonomy's additive `-v002` convention (`docs/failure-mode-taxonomy-v001.md:6-9`).
   `regime-v001` and its four components are byte-unchanged (NG7).
3. **No cross-regime comparison.** `regime-v002` numbers are **never** placed beside the v001 ledger rows as a
   comparison; the v001 rows remain the historical Rung-1 record (NFR-5; `docs/claim-ceiling.md:62-64`).
4. **"Same-regime" = same `regime-v002` within a batch.** All runs in a batch share one `regime_id`; the
   baseline-vs-candidate pair is *internal to `regime-v002`* (research artifact §6.5).
5. **Neutral, pre-pinned regime choice.** The `regime-v002` seed-set/components are chosen on neutral grounds
   and hash-pinned **before any agent runs** — no regime/seed-shopping to flatter an agent (research artifact
   §2.1 RQ-10; risk R2).
6. **Mode stays unseeded.** The probe found no controllable RNG seed; `regime-v002` is `mode=unseeded`, a
   larger ordered list of match-indices, not seeds (`frozen/seeds/seed-set-v001.json` `rationale`; C2-NFR-7).
7. **Component reuse is an open decision (OD-3).** Whether `regime-v002` reuses opponent/deck/metrics by
   reference + hash (only the seed-set differs) or re-mints any of them is for the operator/SDD to decide;
   either way it is a new regime.

## 8. Repeated-batch and descriptive-dispersion requirements

Maps to C2-FR-3 and C2-FR-4. Stated as requirements:

1. **Repeated batches, frozen agents.** Run baseline (`random_legal`) and candidate (`scripted_baseline`)
   both under `regime-v002`, repeated K times, into K sealed immutable run dirs; the only thing that repeats
   is the evaluation (C2-FR-3).
2. **Descriptive dispersion, with context.** The cross-run report states, per metric, the observed **range,
   mean, median, and spread** across the K runs, each carrying `n`, `K`, and `regime_id` (C2-FR-4).
   Example shape (descriptive): *"across K batches of n=N under `regime-v002`, the observed win_rate ranged
   from X to Y (mean Z)."*
3. **No inferential statistics.** No confidence intervals, p-values, "significant," hypothesis tests, or
   inferential error bars in any tracked output. These are **gated** behind a separate explicit design +
   operator approval (NG3; C2-NFR-6).
4. **Unseeded-draw framing.** Any dispersion statement is framed as the dispersion of the *whole unseeded
   process* under the regime — never an isolated "agent variance" estimate, because agent behavior and
   uncontrolled simulator RNG cannot be separated without seed control (C2-FR-6; research artifact §2.1 RQ-8).
5. **Single-regime guard.** The report refuses to aggregate run dirs that do not all share one `regime_id`
   (NFR-5).
6. **Sanitized aggregates only.** The report emits counts/aggregates/dispersion only — never raw decision-
   trace rows, card IDs/names, deck lists, or hand contents (C2-NFR-3; sanitization contract per
   `analysis/failure_report.py:8-19`).
7. **Allowed descriptive vocabulary is ratified by the operator (OD-6).** The exact permitted dispersion
   vocabulary and the explicit exclusion of inferential terms are confirmed before build, so reviewer/auditor
   have a bright line.

## 9. Ledger / report / evidence-storage requirements

Maps to C2-FR-7 and C2-NFR-4 (per `docs/operator/turntrace-loop-contract.md:59-68` / ESP-1..ESP-5 / SP-6):

1. **Full run dirs stay local/ignored.** At the larger `n`, the `runs/<run_id>/` trees (records, traces,
   manifest, hashes, `summary.csv`) stay git-ignored by default; only `runs/.gitkeep` is tracked (ESP-1).
2. **Larger-run reports stay local/ignored unless operator-approved.** The dispersion report and any failure
   report `--out` artifact default to local/ignored; tracking requires explicit SP-6 relaxation
   (`analysis/failure_report.py:27-29`).
3. **Ledger does not grow a row per batch.** Non-deliverable scale/variance runs write **no** ledger row (the
   current default; `eval/run_eval.py:281-288`). The ledger stays small and ceiling-bearing.
4. **Only deliverable runs write ledger rows.** A ledger row is written **only** on explicit deliverable
   intent (`--deliverable` / `--ledger`); the exact policy — at most one designated deliverable run per
   regime — is confirmed by the operator (OD-5).
5. **`docs/ledger.md` remains the only ceiling-bearing artifact.** Per-match records, `summary.csv`, the
   dispersion report, the criteria doc, and this PRD carry no ceiling (`docs/claim-ceiling.md:5-6`).
6. **Reference, never embed.** Tracked docs reference runs by `run_id` + hashes + sanitized metrics +
   local path/status only.
7. **requires-raw-data: cannot-surface.** Actual per-run distributions and run-dir file contents are never
   surfaced in any tracked artifact.

## 10. Claim-ceiling posture

The loop sits at **ladder Rung 1 — legal completion / throughput / audit-trail** (`docs/claim-ceiling.md:22-23`).
**Cycle-002 keeps the ceiling at Rung 1** for the whole cycle (`docs/cycles/cycle-001/closeout.md:8`). The
maturity ladder (`docs/cycles/cycle-000-bootstrap/01-turntrace-prd.md:274-276`):

```
Rung 0  env not trusted
Rung 1  legal completion                         ← current, and held for all of Cycle-002
Rung 2  beats random-legal                       ← criteria defined (C2-FR-5), never claimed
Rung 3  beats scripted / prior best, ablation-backed
Rung 4  stable, report-ready
```

**Allowed claim form** — relative, local, descriptive, carrying its `n`, `K`, and `regime_id`:

> *"under `regime-v002` at n=N across K batches, the observed `<metric>` ranged from X to Y (mean Z)."*

**Forbidden claim forms** (never assert; the words may appear only as negated/forbidden language): gameplay
strength; statistical significance; cross-regime uplift; leaderboard quality; calibration; optimality;
competitiveness. The forbidden agent claim words remain absolutely forbidden: **strong, competitive, optimal,
calibrated, complete** (`docs/claim-ceiling.md:54-59`). Only the ledger, advanced by an explicit later
operator decision, can ever carry a higher rung.

## 11. Safety and sanitization constraints

Carried verbatim from Cycle-001 (`docs/operator/turntrace-loop-contract.md:59-77`;
`docs/cycles/cycle-001/closeout.md:70-80`):

- **Competition Data never enters git** (CC-1/CC-2): the `cg/` SDK, card data CSV/PDF, Kaggle starter
  `deck.csv`, raw deck lists — local-only under git-ignored `grimoires/loa/context/`, enforced by
  `eval/hygiene_check.py`.
- **No raw traces · no card IDs · no card names · no deck lists · no simulator logs · no PDFs/CSVs · no
  run-dir dumps** in any tracked artifact.
- **Frozen components store references + hashes only** — `regime-v002`'s deck reference carries a content hash,
  never a card list.
- **Review/audit/COMPLETED artifacts** persist to git-ignored State Zone (`grimoires/loa/a2a/sprint-N/`),
  written by the orchestrator after the pure-review skills return — never patching implementation
  (`docs/operator/turntrace-loop-contract.md:85-114`).
- **`.claude/` (System Zone) is never edited.**

## 12. Success criteria

### 12.1 Planning-cycle success (this PRD onward, no build)

- **SC-P1.** This PRD is accepted by the operator; the SDD and sprint plan are produced from it
  (Golden-Path: PRD → SDD → sprint-plan).
- **SC-P2.** The narrow mission, the D→A→C/B spine, the regime-v002 framing, the descriptive-vs-inferential
  line, and the Rung-1 hold are ratified (or amended) by the operator.
- **SC-P3.** No build gate is opened; no App-Zone code is written; `regime-v001` and `.claude/` are untouched.
- **SC-P4.** Every planning artifact is sanitized and passes `eval/hygiene_check.py`; no forbidden claim word
  appears except as negated language.

### 12.2 Later build-cycle success (only after OA-2; acceptance criteria)

Each maps to a functional requirement; all bounded to Rung 1, agents frozen.

- **AC-1 (C2-FR-1).** A larger-`n` dry-run produced a sanitized budget note with measured wall-clock, run-tree
  disk size, and a derived safe batch size + storage ceiling; the dry-run wrote **no** ledger row; outputs
  stayed local/ignored.
- **AC-2 (C2-FR-2).** `regime-v002` exists as **additive** frozen files (seed-set + tuple) at a justified
  larger `n`; `regime-v001` and its four components are byte-unchanged; the deck-drift + immutability guards
  hold; the regime was hash-pinned before any agent ran.
- **AC-3 (C2-FR-3).** K repeated batches ran under one `regime-v002` with the **frozen** agents into K sealed
  immutable run dirs; runs were non-deliverable (no ledger row); no `agents/runtime/` file changed.
- **AC-4 (C2-FR-4).** The cross-run report reads K same-`regime` run dirs and emits descriptive dispersion
  (range/mean/median/spread) per metric with `n`, `K`, `regime_id` and a Rung-1 footer; it contains **no**
  inferential statistics; it refuses mixed-regime input; it embeds no raw rows and passes
  `eval/hygiene_check.py`; it imports none of `agents/runtime/`/`cabt`/`sim/`/`eval/`.
- **AC-5 (C2-FR-5).** The Rung 2 readiness doc states the minimal criteria for a future Rung 2 *consideration*,
  explicitly does not claim Rung 2, and records that the inferential design + ceiling advance is a separate
  operator decision; no forbidden claim words.
- **AC-6 (C2-FR-6).** The reproducibility note confirms `seed_controlled=false`, defines "stable" as
  distribution-stable + audit-trail, and records that unseeded dispersion cannot be separated into an isolated
  agent-variance estimate; no manufactured seed control.
- **AC-7 (C2-FR-7).** The ledger/report-discipline note records: no ledger row per batch; only explicitly
  designated deliverable runs write rows; larger-run reports local/ignored unless operator-approved. The
  ledger still carries no row from non-deliverable Cycle-002 runs.
- **AC-8 (cross-cutting, claim ceiling held).** No tracked Cycle-002 artifact makes a claim beyond Rung 1; the
  ledger remains the only ceiling-bearing artifact; forbidden words appear only as negated language.
- **AC-9 (cross-cutting, no cross-regime + loop discipline).** No tracked artifact compares `regime-v002` to a
  v001 row; all App-Zone code landed through `/implement → /review-sprint → /audit-sprint`, fast-forward only,
  one review + one audit artifact; COMPLETED marker only on explicit operator authorization.

## 13. Open operator decisions for SDD / sprint planning

These do not block the PRD; recommended dispositions are marked `[ASSUMPTION]` and carried into the SDD.

- **OD-1 — Open the Cycle-002 build gate (OA-2) before any `/implement`/`/run`.** *[ASSUMPTION: not yet open.]*
  This PRD and the SDD authorize no code; C2-FR-1..4 need an explicit build gate.
- **OD-2 — Confirm the narrow scope and spine.** *[ASSUMPTION: D→A→C/B build core; E/F/G docs/criteria/
  constraint.]* Confirm the agent-optimization lane stays closed.
- **OD-3 — `regime-v002` component reuse vs re-mint.** *[ASSUMPTION: reuse opponent-pool-v001 / deck-pool-v001 /
   metrics-spec-v001 by reference + hash; only the seed-set differs.]* Either way it is a new regime; this fixes
  how much changes. *(Carry-forward §13 Q3 of the research artifact.)*
- **OD-4 — Target `n` and batch count K.** *[ASSUMPTION: chosen from the C2-FR-1 dry-run — `n` large enough to
  show dispersion, K small enough to stay cheap and avoid artifact proliferation.]* Final numbers are an SDD/
  sprint-plan input informed by the budget. *(Carry-forwards §13 Q1, Q2.)*
- **OD-5 — Ledger-row policy for scale/batch runs.** *[ASSUMPTION: scale/variance batches write no ledger row;
  at most one deliberately designated deliverable run per regime may write a row.]* *(Carry-forward §13 Q5.)*
- **OD-6 — Allowed descriptive-statistics vocabulary.** *[ASSUMPTION: range, mean, median, spread — with `n`,
  `K`, `regime_id`; CIs / p-values / "significant" / hypothesis tests / inferential error bars excluded.]*
  Ratify the bright line for reviewer/auditor. *(Carry-forward §13 Q6.)*
- **OD-7 — Where the dispersion report lives by default.** *[ASSUMPTION: local/git-ignored; a single sanitized
  tracked summary at cycle close only on explicit SP-6 relaxation.]* *(Carry-forward §13 Q4.)*
- **OD-8 — Rung 2 stays criteria-only.** *[ASSUMPTION: yes.]* C2-FR-5 defines criteria; Cycle-002 claims no
  Rung 2; the inferential design + ceiling advance is a separate later decision.
- **OD-9 — `.beads/.br_history/` gitignore housekeeping (CF-04).** *[ASSUMPTION: handled separately, not
  Cycle-002 build scope.]* Note `.beads/issues.jsonl` is already in the working tree's dirty set; decide fold-in
  vs separate. *(Carry-forward §13 Q7.)*

## 14. Risks and mitigations

| # | Risk | Mitigation |
|---|------|------------|
| R1 | **Cross-regime contamination** — v002 numbers narrated as bigger/smaller than the v001 n=12 result, breaking NFR-5. | §7 framing front-and-center; `delta_report` exit-2 refusal intact; the dispersion report refuses mixed-regime input; every v002 statement carries `regime-v002` + `n`; never place a v002 number beside a v001 row (AC-9). |
| R2 | **Accidental agent optimization** — "scale the evaluation" drifts into tuning, seed/regime-shopping, or a per-decision scorer. | Agents frozen (no `agents/runtime/` edit); `regime-v002` chosen on neutral grounds and hash-pinned before any agent runs; FM-03/04/06/08 stay `detector: forbidden`; reject agent-decision-logic touches at review/audit (NG1, NG5; OD-2). |
| R3 | **Confidence-language overreach** — descriptive dispersion presented as inferential (CIs, "significant"), implicitly raising the rung. | Ratify the descriptive-only vocabulary (OD-6); ban inferential terms in tracked outputs; Rung-1 footer on every non-ledger artifact; audit greps for forbidden words + inferential phrasing (NG3, C2-NFR-6). |
| R4 | **Claim-ceiling inflation** — a larger-`n` win_rate movement read as the agent being "better," crossing Rung 1. | Rung-1 hold as an explicit AC (AC-8); ledger stays the sole ceiling-bearer; Rung 2 is criteria-only (C2-FR-5), never claimed; forbidden words banned except negated. |
| R5 | **Competition-Data / raw-trace leakage at scale** — more/larger runs increase the surface for a careless read of trace rows into a tracked report. | Restrict roll-ups to coarse sanitized fields (counts/rates/dispersion); keep `eval/hygiene_check.py` active; reports local/ignored by default; audit confirms no raw contents embedded (C2-NFR-3; AC-4). |
| R6 | **Storage/cost surprise** — many large batches exhaust local disk or slow trace I/O. | C2-FR-1 dry-run measures wall-clock + disk and sets a safe batch size + storage ceiling **before** C2-FR-3 commits to K (research artifact §2.1 RQ-5). |
| R7 | **Building before the gate** — this PRD misread as authorization to `/implement`. | Reaffirm loop contract §6: planning never opens the gate; no `/implement`/`/run` until an explicit OA-2 (OD-1). |
| R8 | **Unseeded variance misattribution** — dispersion presented as the agent's variance when it conflates agent + uncontrolled RNG. | Document the `seed_controlled=false` bound (C2-FR-6) inline in any dispersion report; frame dispersion as the whole-process observation (NG8; research artifact §2.1 RQ-8). |
| R9 | **regime-v001 mutation** — a larger seed-set written by editing v001 instead of adding v002. | C2-FR-2 requires additive new files; AC-2 asserts v001's four components are byte-unchanged; review/audit verify no `frozen/regime-v001` diff (NG7). |

## 15. Sources and traceability

> **Binding input:** `docs/cycles/cycle-002/00-research-and-planning.md` (the accepted Cycle-002 research
> artifact, §§1-16).
>
> **Prior authorities:** `docs/cycles/cycle-001/closeout.md` (status, ladder lanes, still-forbidden list,
> lines 8, 23-24, 43-119); `docs/operator/turntrace-loop-contract.md` (§1-§3, §6, §7, §8, §10);
> `docs/operator/deferred-lane-gate-after-sprint-01.md` (data-first; still-closed list, lines 71-97);
> `docs/claim-ceiling.md` (Rung 1; regime rule; reproducibility posture; forbidden words; never-cross-regime,
> lines 5-6, 22-23, 29-35, 42-64); `docs/ledger.md` (only ceiling-bearing artifact; two n=12 rows, lines 3-12);
> `frozen/regimes/regime-v001.json` (four-component tuple; new-regime rule, lines 4-9);
> `frozen/seeds/seed-set-v001.json` (n=12 match-indices; throughput; raise-N-in-v002 rationale);
> `docs/cycles/cycle-001-sprint-00/closeout.md`; `docs/cycles/cycle-001-sprint-01/closeout.md`;
> `docs/cycles/cycle-001-sprint-02/{00-research-and-planning,01-sprint-02-prd,closeout}.md`;
> `docs/strategy-report.md` (limitations: n=12 small sample, mode=unseeded, opponent=mirror, lines 94-107);
> `docs/failure-mode-taxonomy-v001.md` (additive `-v002` convention; FM-03/04/06/08 detector-forbidden,
> lines 6-9, 40-52); `docs/cycles/cycle-000-bootstrap/{01-turntrace-prd,02-turntrace-sdd}.md` (maturity ladder,
> PRD lines 274-276 / SDD line 840); `eval/run_eval.py` (n from seed-set line 121; immutability/deck-drift
> guards 128-154; source-hash provenance 158-173; no-ledger default 281-288, 333-336);
> `analysis/aggregate.py` (single-run aggregation, lines 29-40, 125-149); `analysis/failure_report.py`
> (sanitization contract; local `--out`, lines 8-30); `eval/hygiene_check.py` (path-level guard, lines 35-45).
>
> **Traceability rule:** every functional requirement (C2-FR-#) cites its lane (research artifact §7) and its
> source; every assumption is tagged `[ASSUMPTION]` and carried as an operator decision (§13). The PRD
> introduces no new evidence and reuses only sanitized, already-tracked artifacts.
