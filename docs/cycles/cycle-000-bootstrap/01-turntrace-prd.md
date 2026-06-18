# TurnTrace — Product Requirements Document

| Field | Value |
|---|---|
| **Product** | TurnTrace — a data-loop and evaluation harness for simulator-based trading card game agents |
| **Initial target** | Kaggle "The Pokémon Company — PTCG AI Battle Challenge Simulation" |
| **Competition structure** | Two tracks: this **Simulation** competition (skill-rated leaderboard, **no monetary prize**) + a separate, optional **Hackathon** track (report-based, **prize-eligible**). TurnTrace serves the Simulation track and feeds the Hackathon report. (Operator-supplied Overview, 2026-06-17) |
| **Key deadlines** | Start 2026-06-16 11:00 UTC; Entry & Team-Merger **2026-08-09**; **Final Submission 2026-08-16**; final evaluation through ~2026-08-31 (all 23:59 UTC unless noted). ~2 months runway from this PRD. |
| **Simulator engine** | `cabt` (Matsuo Institute), built for `kaggle-environments` **1.14.10**; same logic as the hosted environment; suitable for local debug/RL. Docs: matsuoinstitute.github.io/cabt |
| **Cycle** | `cycle-000-bootstrap` |
| **Artifact** | `grimoires/loa/a2a/cycle-000-bootstrap/01-turntrace-prd.md` |
| **Status** | Draft for review |
| **Date** | 2026-06-17 |
| **Scope of this cycle** | Planning artifacts only (PRD → SDD → sprint plan). No implementation. (Operator decision, 2026-06-17) |
| **Primary source** | Research spike: `grimoires/loa/context/Planning/Pokemon TCG AI Battle - Data Loop Plan.md` (the "Data Loop Plan", cited as §N below) |

> **Grounding note.** This PRD is grounded in three evidence sources: the Data Loop Plan
> research spike (design-level), the official competition docs the operator downloaded
> (`Competition Rules.md`, `Competition Dataset Description.md`), and direct inspection of the
> Kaggle starter kit (`grimoires/loa/context/Planning/sample_submission/`). Code citations use
> `file:Lnn`. Ungrounded statements are tagged `[ASSUMPTION]`. Open items are tagged `[UNKNOWN]`
> with a fallback. This document is product-level: it defines *what* TurnTrace must be and prove,
> not *how* it is implemented (that is the SDD's job).

---

## 1. What TurnTrace Is

TurnTrace is an **evidence machine** for simulator-based card-game agents. It runs matches when
the simulator is available, preserves what happened as immutable artifacts, and lets us compare
two agent versions and *believe the difference*. It exists to produce **trustworthy evidence about
an agent — not to produce a strong agent**.

> From Data Loop Plan §1: "This data loop exists to produce **trustworthy evidence about a Pokemon
> TCG agent**, not to produce a strong agent… a clever bot with no reproducible evidence is worth
> less to the Strategy Category report than a mediocre bot whose every behavior is logged,
> replayable, and honestly framed."

TurnTrace is the **internal name of the harness**. It is distinct from the agent(s) it evaluates
and from any competition submission. In competition-facing materials the work is described in plain
Kaggle/ML-agent terms (see §11); the names "FORGE", "Echelon", and "CORONA" must not appear in
competition-facing docs (Hard rule, operator brief).

The harness has two physically and conceptually separate halves, a rule that colors the entire
product:

- **Runtime side** — the code that picks a move inside the per-move budget. Fast, simple,
  self-contained, no mandatory scoring machinery.
- **Offline side** — the analysis that reads run outputs *between* submissions. Slow and thorough
  is fine here.

> From Data Loop Plan §2: "the runtime agent… and the offline analysis… must never share code or
> assumptions. The runtime side must be fast and dumb. The offline side can be slow and thorough."

---

## 2. The Problem It Solves

Optimizing an agent before an evidence loop exists is "building on sand" (§1c). Concretely, without
TurnTrace:

- **"Improvement" is unmeasurable.** Without a frozen baseline pool and a fixed evaluation set, a
  real gain cannot be told apart from opponent-pool drift or lucky variance (§1c).
- **Losses cannot be debugged.** A loss you cannot reproduce (or audit) is a loss you cannot fix
  (§1c).
- **Ablations are guesswork.** "Did changing rule X help?" needs per-match artifacts you can
  re-slice, not an aggregate win rate (§1c).
- **The Strategy Category report has nothing to stand on.** The report is graded on evidence and
  honesty; every claim must point back to a logged artifact (§1c, §9).

TurnTrace solves this by enforcing a hard ordering — **data first, optimization second, inside the
machine** — and by making every result carry the evidence and the ceiling that bound it.

---

## 3. Who It Serves

| Stakeholder | Role | What they need from TurnTrace |
|---|---|---|
| **Agent engineer (primary user)** | Builds/iterates the runtime agent | A trustworthy way to tell whether a change helped, on which matchups, by how much — without re-running history or fooling themselves. |
| **Analyst / report author** | Writes the Strategy Category report | Logged, traceable artifacts (per-match records, traces, ledger rows, failure modes) that every report sentence can cite. |
| **Operator / decision-maker** | Decides what to submit and when | Honest, ceiling-bounded comparisons between agent versions and a clear record of what was tested under what conditions. |
| **External verifier** *(future)* | Reproduces or audits a claim | Run artifacts (hashes, manifests, logs) sufficient to re-run or audit-verify a result. Deferred (§12). |

> The product optimizes for the **agent engineer** first: the loop must be small enough that one
> engineer can stand it up and trust its output before any modeling work (§2). Per Data Loop Plan §2.

---

## 4. Goals (this product)

**G1 — Run matches when the simulator is available**, under fully declared inputs, sequentially and
debuggably (§2 "Local match runner").

**G2 — Preserve evidence immutably.** Every run is a sealed artifact; written runs are never edited;
new runs go to new directories (§2 "Immutable run directories").

**G3 — Compare agent versions honestly.** Produce attributable deltas between versions on a fixed
test definition, bounded by sample size and a claim ceiling (§1a, §4.3, §5.5).

**G4 — Track what was tested and under what conditions.** A human-readable ledger and a frozen
"regime" make every number traceable to its inputs (§2 "Experiment ledger", §5.2).

**G5 — Support decision traces where the simulator permits**, so a loss is decomposable from
observable signals without re-running it by hand (§4.2).

**G6 — Bound claims with explicit evidence.** No claim exceeds what its sample size and test
definition support (§4 preamble, claim ceilings throughout).

**G7 — Feed a credible Strategy Category report.** The run artifacts directly populate the report
rather than requiring a separate effort (§9, §12 checklist item). The report is the separate,
prize-eligible **Hackathon** track (§8.3); Hackathon ranking weighs **both** leaderboard performance
**and** report quality — TurnTrace supplies the evidence half. Competitive leaderboard standing is
the agent's job (pursued later, inside the machine, §11.3–§11.4), not a claim of this harness.

---

## 5. What the System Must Prove vs. Must Not Prove

### 5.1 What it MUST prove (when working)

Grounded in §1a, and re-scoped to the **resolved** simulator surface (see §8):

- **The agent runs legally and completes games** — full games end-to-end against a fixed opponent
  pool with zero crashes, at a measured rate over a stated N (§1a, ladder Rung 1 §6). Because the
  engine only ever offers legal options (§8.3), an illegal *game* move is impossible by
  construction; the residual, detectable failure is a **malformed selection** (wrong count /
  duplicate / out-of-range index). That — not "did it pick a legal move" — is what "runs legally"
  measures here, and it anchors the FM-01 reframe.
- **Reproducibility evidence exists** — at the **distribution-stable + audit-trail** level (see §7,
  Operator decision 2026-06-17): run artifacts preserve logs, visible state transitions, action
  choices, timing, and simulator metadata so a divergence can be diagnosed, not guessed.
- **Measured performance against a frozen baseline pool** — win/draw/error rate and game-length
  statistics versus a fixed opponent set on a fixed evaluation set, so two submissions are
  comparable (§1a).
- **Attributable deltas between agent versions** — when v2 differs from v1, *by how much, on which
  matchups*, tied to a specific changed decision rule (§1a). (The two-direction ablation discipline
  that fully earns this is later-cycle, §4.4 / §12.)
- **Provenance of every tuning knob** — where each threshold came from and how confident we are
  (§1a).

### 5.2 What it MUST NOT prove / claim

> From Data Loop Plan §1b: "The loop measures and logs. It does not bless."

- That the agent is good in any absolute sense, or would win the competition (§1b).
- That results generalize beyond the frozen opponent pool and deck list used (§1b).
- That the agent plays the "objectively correct" line — only that it beats the specific baselines
  measured (§1b).
- Anything about matchups/decks/rule interactions absent from the evaluation set (§1b).
- Statistical significance beyond what the (often small) sample supports — every number carries its
  N (§1b).

Per the operator brief and §1b, TurnTrace must **never claim the agent is strong, competitive,
optimal, calibrated, or complete.** Any "the agent is strong" statement is a human reading the
evidence with the sample size in view — not an output of the loop.

---

## 6. Functional Requirements (product-level)

These describe product *capabilities*, not implementation. IDs are stable for SDD/sprint traceability.
Priority: **P0** = required for the first build (Sprint 00); **P1** = next; **P2+** = deferred lane.

| ID | Capability | Priority | Source |
|---|---|---|---|
| **PR-1** | **Local match runner** — play one match under a fully declared input set (which agents, which decks, which test definition, which run/match identity) and refuse to run if any input is missing. | P0 | §2 "Local match runner" |
| **PR-2** | **Random-legal baseline agent** — a runtime agent that selects uniformly among the simulator-offered legal options. The floor opponent and harness stress test. | P0 | §2 "Baseline agent(s)", §5.1 |
| **PR-3** | **Per-match record** — one compact machine-readable record per match (outcome, turns, error, timing, capability flags, trace linkage). The row-level analysis unit. Carries no claim ceiling. | P0 | §2 "Match summary", §4.1 |
| **PR-4** | **Decision trace** — an ordered, per-decision log of one match (observed state, chosen action, outcome of the move, optional free-form agent metadata) sufficient to decompose a loss from observable signals. Optional per match; the loop still runs on records alone if tracing is impossible. | P0 | §2 "Decision trace", §4.2 |
| **PR-5** | **Immutable run directory** — one sealed, append-only directory per run holding records, traces, an aggregate summary, a manifest (the authority for run/match identity), and a hash stamp. Writing into a populated run directory is a hard error. | P0 | §2 "Immutable run directories", §4 |
| **PR-6** | **Frozen regime** — an immutable bundle (seed/index set + opponent pool + deck pool + metrics spec) that defines a comparison. A new version is a new file, never an edit. Cited in every result row. | P0 | §5.2 |
| **PR-7** | **Run aggregation** — roll per-match records up into win/draw/error/timeout rates and game-length stats, broken down by matchup. | P0 | §2 "Match summary", §4.1 |
| **PR-8** | **Experiment ledger** — one human-readable, append-only row per run: what it was, against what, the result, the sample size, and a mandatory `claim_ceiling`. The only artifact that binds a number to a ceiling. | P0 | §2 "Experiment ledger", §4.3 |
| **PR-9** | **Capability probe** — a first-task report stating, from the *actual* environment, what the simulator does and does not expose (run-locally, legal-action enumeration, seed control, time budget/timeout detection, match throughput, submission interface), each marked confirmed / unconfirmed / absent with a fallback. | P0 | §10, §11 Day 1 |
| **PR-10** | **Failure-mode registry** — a living, human-maintained catalogue of ways the loop/agent produces wrong or untrustworthy output, each with a detection signature computable from available fields. Seeded with the known unknowns. | P0 (stub) | §2 "Failure-mode registry", §4.5 |
| **PR-11** | **Claim-ceiling document** — a short, code-factual statement of exactly what the loop does and does not measure, including the zero-modeling invariant. | P0 (stub) | §2 "Claim ceiling document" |
| **PR-12** | **Strategy-report skeleton** — the standing report structure (headings + placeholders) so later runs slot in cleanly. | P0 (stub) | §2 "Strategy report skeleton", §9 |
| **PR-13** | **Scripted heuristic baseline** — a small, frozen, deterministic priority policy: the "better than a sensible first script" bar. | P1 | §2, §5.1 |
| **PR-14** | **Delta report** — compare two run directories on the same frozen regime and emit per-metric deltas with a "why no change" line for metrics that didn't move. *First comparison artifact; owned by the first build's successor sprint.* | P1 | §7.7, §11 |
| **PR-15** | **Replay / reproducibility check** — re-hash traces (audit-trail equality) or, if seed control is later proven, byte-identical replay. | P1 | §4.2, §5.6 |
| **PR-16** | **Two-direction ablation ledger** — baseline → modified → reverted discipline with a revert check; the artifact that fully earns "this change caused the delta." | P2 | §4.4 |
| **PR-17** | **Candidate action-scoring agent**, search/lookahead, value/win-probability model, deck optimizer, RL/self-play, dashboards, signed receipts. | Deferred lane | §6, §8 |
| **PR-18** | **Pre-submission mirror validation** — locally play a candidate agent against a copy of itself to confirm it completes a full match with no error before submitting, mirroring Kaggle's hosted Validation Episode (which runs the submission vs copies of itself and marks it `Error` on failure). | P1 | §8.3; Overview (Evaluation) |

> **Anti-inference note.** The feature set above is taken from the research spike and operator brief;
> it is deliberately *not* expanded with speculative additions. Items the brief explicitly excludes
> are listed as Non-Goals (§13), not silently added.

---

## 7. Non-Functional / Technical Posture (product-level)

| ID | Requirement | Source |
|---|---|---|
| **NFR-1 — Runtime/offline separation** | The per-move runtime agent (fast, simple, no mandatory scoring fields, no slow code) is cleanly separated from offline analysis. They share no code or assumptions. | §2, §12 |
| **NFR-2 — Immutability** | Generated run directories are append-only and never hand-edited; re-running writes a new directory. The immutability guard is a hard error, not a prompt. | §2, §7.4(9) |
| **NFR-3 — Reproducibility posture = distribution-stable + audit trail (baseline)** | Byte-identical replay is a *desired upgrade, not a current requirement.* Baseline evidence uses larger-N distribution-stable comparisons. Run artifacts preserve logs, visible state transitions, action choices, timing, and simulator metadata. If seed control is later discovered, the architecture **may** upgrade to deterministic replay checks. Until then, claims are framed as statistical/distribution-level, not replay-perfect. | Operator decision 2026-06-17; §5.6, §10 |
| **NFR-4 — Provenance on every run** | Every run records code revision, dependency/simulator version (with whether it was *reported* by the sim or *pinned* by us), and content hashes of decks/opponents/metrics, so a divergence can be diagnosed instead of guessed. | §4.1, §10 |
| **NFR-5 — Claim-bounded outputs** | Every reported metric carries its sample size; no comparison is asserted across two different regimes; "better/worse" requires a same-regime, agent-only comparison plus a ceiling and an N. | §4.3, §5.5 |
| **NFR-6 — Schema tolerance to capability gaps** | No schema requires a field the simulator cannot provide. Capability-dependent fields are nullable and paired with a capability flag; a missing capability is logged once, never blocks the loop. | §4 preamble |
| **NFR-7 — Flat-files-first simplicity** | One entrypoint, one config, env-var-driven output directory, flat JSON/CSV/Markdown. The default answer to any new abstraction is "no, not yet." No new services. | §3, §10 "Overengineering" |
| **NFR-8 — Self-contained runtime** | The submitted agent performs no external network calls during episode evaluation (competition no-ingress/no-egress rule, §11). | Competition Rules:L119-120 |

---

## 8. Simulator Capability Findings & Remaining Unknowns

The Data Loop Plan was written before the simulator was inspected and treated nearly everything as
UNKNOWN. Inspecting the starter kit (`sample_submission/cg/`) **resolves most of these**. This
section records the *resolved* surface and the *genuinely remaining* unknowns. The Capability Probe
(PR-9) must still confirm these against the live environment before the build relies on them.

### 8.1 Resolved from the starter kit (high confidence)

| Question | Finding | Evidence |
|---|---|---|
| Simulator language/runtime | **Python** (3.10+) over a compiled native lib loaded via `ctypes` — `cg/cg.dll` (Windows) / `cg/libcg.so` (else). One language for the repo: Python. | `cg/sim.py:L19-23` |
| Can local matches be run? | **Yes, in-process.** `battle_start(deck0, deck1)` → first observation; `battle_select(list[int])` → next observation; `battle_finish()`. A full match is driven by alternating selections. | `cg/game.py:L19-66` |
| Can agents/decks be controlled locally? | **Yes.** `battle_start` takes *both* 60-card decks; both sides' move selection is ours to drive. | `cg/game.py:L19-35` |
| Are legal actions enumerable? | **Yes.** `obs.select.option` is the full legal-option list; the agent returns indices into it, bounded by `obs.select.minCount`/`maxCount`. Random-legal = `random.sample(range(len(option)), maxCount)`. | `main.py:L31-38`; `cg/api.py:L398-409` |
| Are invalid actions detectable? | **Yes, and largely structurally prevented.** The agent can only choose offered options; `Select` returns error codes for out-of-range / wrong-count / duplicate selections. Illegal *game* moves are essentially impossible by construction; the residual detectable failure is malformed selection. | `cg/game.py:L60-65`; `cg/api.py:L609-625` |
| Is observable state sufficient for decision traces? | **Yes.** `obs.current` (`State`) exposes the full visible board for both players; own hand is visible, opponent hand is `None`, own deck *contents* are hidden (only `deckCount`) — so traces cannot leak future-draw state. `obs.logs` is the event stream since the last selection (draws, moves, attacks, HP changes, coin flips, KOs, result). | `cg/api.py:L350-379`, `L411-445` |
| Is the ending cause reported? | **Yes.** `LogType.RESULT` carries `result` (0/1 winner, 2 draw) and `reason` (1 = prize-out, 2 = deck-out, 3 = no Active Pokémon, 4 = card effect). | `cg/api.py:L318-321` |
| Official submission interface | **Kaggle simulation competition.** Submit `submission.tar.gz` = `main.py` (defines `agent(obs_dict) -> list[int]`) + `deck.csv` (60 card IDs) + the `cg/` lib. Episode replays via `kaggle competitions replay <id>`; per-agent logs via `kaggle competitions logs <id> <idx>`. No private leaderboard. | `main.py`; `simulation_competitions.md`; Competition Rules:L114 |
| Optional built-in lookahead | A `search_begin/step/end/release` API exists for forward simulation by *predicting* opponent hidden cards, with `manual_coin` to fix coin flips during search. **Noted as a capability; deferred lane (MCTS/planning), not built now.** | `cg/api.py:L517-639` |

### 8.2 Genuinely remaining unknowns (probe before relying)

| ID | Unknown | Current evidence | Assumption + fallback |
|---|---|---|---|
| **U-1 — Seed / RNG control** | `BattleStart` accepts only the concatenated decks (120 ints); **no seed parameter is exposed** on the local surface. | `cg/sim.py:L27-28`, `cg/game.py:L33-35` | `[ASSUMPTION]` seeds are **not controllable**. **Baseline:** distribution-stable evidence + log-based RNG audit trail (the sim's shuffles/draws/coin flips are observable in `obs.logs`). If a seed path is later found, upgrade to deterministic replay (NFR-3). Recorded as an explicit capability unknown. |
| **U-2 — Match throughput** | In-process `ctypes` calls into a compiled lib suggest high throughput, but no number is measured. | `cg/sim.py`, `cg/game.py` | `[ASSUMPTION]` tens–hundreds/hour at least; **fallback:** measure wall-clock for N matches in the probe; if slow, shrink the evaluation set N (reduces statistical power, not correctness). RL/self-play stays blocked until a number exists. |
| **U-3 — Time budget / timeout** | No per-move or per-game budget is visible in the starter code; the agent function is a plain callable. | `main.py`, `cg/api.py` | `[ASSUMPTION]` a per-move budget exists in the hosted environment. **Fallback:** measure our own decision wall-time against a config-constant budget (`budget_source=assumed`); if none is published, set timeout fields null and soften the timeout gate. |
| **U-4 — Local vs hosted parity** | Local `cg` lib plays full matches, but whether local outcomes match hosted episode scoring is unverified. | — | `[ASSUMPTION]` local results are representative. **Fallback:** track local win% and leaderboard rank as *separate* metrics; treat divergence as a finding (§10). |
| **U-5, U-6** *(was: Strategy track & timeline)* | **RESOLVED** by operator-supplied competition Overview (2026-06-17). Two-track structure (Simulation vs Hackathon) and pinned deadlines confirmed — see §8.3. | `competition-overview.md` | Moved to §8.3 (resolved). No longer open. |

### 8.3 Resolved by operator-supplied competition Overview (2026-06-17)

Recorded verbatim in `grimoires/loa/context/Planning/competition-overview.md` (the live page is
JS-rendered and could not be fetched). These resolve U-5/U-6 and refine several constraints.

| Fact | Detail | Implication for TurnTrace |
|---|---|---|
| **Two competitions** | This is the **Simulation** competition (agent vs ladder; skill-rated leaderboard; **no monetary prize**). A separate, optional **Hackathon** track is report-based and **prize-eligible**; Hackathon final ranking uses **both** Simulation-leaderboard performance **and** report evaluation. | Resolves U-5. The "Strategy Category report" (G7, §9) = the **Hackathon report**. TurnTrace produces the *evidence backbone* of that report; competitive standing is the agent's job (pursued later, inside the machine — §11.3/§11.4), not a claim of this harness. |
| **Timeline** (23:59 UTC unless noted) | Start **2026-06-16 11:00 UTC**; Entry Deadline **2026-08-09**; Team-Merger Deadline **2026-08-09**; **Final Submission Deadline 2026-08-16**; final evaluation **2026-08-17 → ~2026-08-31** (games run to convergence, then leaderboard final). | Resolves U-6. ~2 months of runway from this PRD to 2026-08-16. Bounds cycle cadence (§11.5). |
| **Simulator engine = `cabt`** | The `cg` lib is the **cabt** engine (Matsuo Institute), "built for kaggle-environments," "uses the same logic as the Kaggle competition environment," "suitable for local debugging and reinforcement learning." Pinned at **kaggle-environments 1.14.10**. Docs: `https://matsuoinstitute.github.io/cabt/`. A documented list of **differences between official Pokémon TCG rules and simulator behavior** exists. | Softens U-4 (official local↔hosted parity intent) and confirms the SDK officially supports local RL (context for the RL deferred lane; the stance is unchanged — no premature RL, §12). Engine + env version are provenance fields (NFR-4). Analysis must follow **cabt behavior, not the official rulebook** (§14 risk). |
| **"The engine only ever presents legal moves."** | Official confirmation: each turn the agent chooses only from the offered legal options. | Confirms §8.1: illegal *game* moves are structurally impossible. The legality gate reduces to "0 malformed-selection errors." Strengthens the FM-01 reframe. |
| **Scoring = TrueSkill-style rating** | Each submission has a rating **N(μ, σ²)**, initialized **μ₀ = 600**; wins raise μ, losses lower it, draws converge; σ shrinks with information. **The victory margin does NOT affect rating** — only win/loss/draw. Matchmaking pairs similar ratings; newer agents play more often. | The metrics-spec treats the outcome as **W/L/D only** (margin-irrelevant) — aligns with the existing `result` enum (§4.1). The harness must not optimize for, nor report, victory margin as if it affected ranking (refines NFR-5). |
| **Validation episode (mirror self-play)** | On upload, a submission first plays a **Validation Episode against copies of itself**; on failure it is marked **Error** (download agent logs). | Motivates **PR-18** (local mirror-match validation) as a pre-submission smoke that catches what the hosted validation would. |
| **Submission mechanics** | `.tar.gz` with **`main.py` at the top level (not nested)** + **`deck.csv`**; built via `tar -czvf submission.tar.gz *`. **5 submissions/day**; only the **latest 2** are tracked/used for final; leaderboard shows only your best agent; all submitted agents keep playing to the end. | Refines CC-5/CC-6; informs submission cadence and the "latest-2" selection discipline (§11.5). |

---

## 9. Claim Ceiling Posture

Claim ceilings are the first of the four core disciplines (§intro). The posture, binding on every
output:

1. **Only relative, local claims.** The strongest sayable form is "candidate-vNNN beat
   baseline-vMMM by X points over regime-vKKK at n=N." Never "strong", "optimal", "solved", or
   "calibrated" (§5.1).
2. **The ledger is the only ceiling-bearing artifact.** Per-match records and aggregate summaries
   carry *no* ceiling; any strength/comparison claim is made via an experiment-ledger row that binds
   the number to a ceiling and a sample size (§4 preamble, §4.3).
3. **A row may only raise its ceiling to what its N and regime support** — a flattering win rate at
   small N or against a narrow pool stays modest (§4.3).
4. **Never compare across regimes.** Two numbers from two different regimes are not comparable and
   their difference is not uplift (§5.5).
5. **Honesty about reproducibility.** Until seed control is proven, every report states "measured at
   distribution level; exact replay unavailable" rather than implying replay-perfect results
   (NFR-3, §5.6).
6. **The maturity ladder gates claims (§6).** A claim may not exceed the rung whose required
   artifacts exist in an immutable run directory: Rung 0 (environment not trusted) → Rung 1 (legal
   completion) → Rung 2 (beats random-legal) → Rung 3 (beats scripted/prior best, ablation-backed)
   → Rung 4 (stable, report-ready).

---

## 10. Competition-Facing Constraints

Grounded in the official `Competition Rules.md` and `Competition Dataset Description.md`.

| ID | Constraint | Source |
|---|---|---|
| **CC-1 — Competition Data is non-redistributable and Competition-Use-Only.** The `cg/` simulator lib, card data (CSVs/PDFs), and any starter code/`deck.csv` provided on Kaggle must not be transmitted, duplicated, published, or redistributed to non-participants, and must be deleted at competition end. **→ These files must never be committed to the repo; keep them local/gitignored.** (Validates the operator "no Kaggle files" rule.) | Competition Rules:L52-54, L60-62 |
| **CC-2 — Pokémon Elements belong to Pokémon.** Card names, rules, game logic, type matchups, deck recipes, etc. are owned by Pokémon and may not be published. Competition-facing artifacts must avoid embedding redistribution-sensitive Pokémon Elements. | Competition Rules:L245-257 |
| **CC-3 — No ingress/egress during episode evaluation.** The submitted agent may not pull in or send out any information external to the submission and environment during an episode. The runtime agent must be fully self-contained (NFR-8). | Competition Rules:L119-120 |
| **CC-4 — Winner obligations / licensing.** A winning submission's source code is licensed under an OSI-approved license (competition winner license type: **MIT**), with a reproducibility description; this excludes Competition Data and Pokémon Elements. | Competition Rules:L27-28, L63-72, L95-100 |
| **CC-5 — Submission limits & format.** Max 5 submissions/day; up to 2 final submissions for judging — only the **latest 2** are tracked and used for final; max team size 5; mergers permitted within submission-count limits. Submission is a `.tar.gz` with **`main.py` at the top level** + `deck.csv` (`tar -czvf submission.tar.gz *`). | Competition Rules:L36-44; Overview |
| **CC-6 — Scoring = TrueSkill-style rating; public leaderboard only.** Per-episode results update a rating N(μ,σ²), μ₀=600, where **only W/L/D matters — victory margin does not affect the rating**; leaderboard shows your best agent; no private leaderboard. Episode replays may be public/downloadable; a daily top-episode export exists (*offline* scouting input only). | Competition Rules:L113-117; Dataset Description:L3-5; Overview (Evaluation) |
| **CC-7 — External data/tools must be publicly and equally accessible at minimal cost.** Any external data used must satisfy the Reasonableness Standard. | Competition Rules:L78-85 |
| **CC-8 — Plain-language framing.** No borrowed private-product vocabulary (FORGE/Echelon/CORONA) in competition-facing schemas, file names, field names, or docs. | Operator brief; §12 checklist |
| **CC-9 — Hard deadlines.** Entry & team-merger **2026-08-09**; **final submission 2026-08-16** (submissions lock); final evaluation runs through ~2026-08-31. | Overview (Timeline) |
| **CC-10 — Simulator ≠ official rules 1:1.** Battles run on the `cabt` engine (kaggle-environments 1.14.10); a documented set of differences from official Pokémon TCG rules applies. Analysis and any heuristics must follow **cabt behavior**, not the published rulebook. (The cabt rules-differences page is a known reference — required reading for the SDD/build; see §17.) | Overview (Simulator API) |

---

## 11. Scope & Prioritization

### 11.1 This cycle (`cycle-000-bootstrap`) — planning only

cycle-000 produces **planning artifacts only**: this PRD → SDD → sprint plan. **No code, no Kaggle
files, no dependencies.** (Operator decision, 2026-06-17.) The first *build* (Sprint 00) is the
immediately-following cycle and is bounded by this PRD.

### 11.2 First build (Sprint 00, next cycle) — the smallest useful loop

Defined here at the product level so the PRD bounds the build:

> From Data Loop Plan §7: "Sprint 00 is about the data loop, not about playing well. Success is: we
> can run the random-legal agent against a fixed opponent, capture a per-match record and trace on
> disk, summarize it, and write one immutable run directory with a hash stamp. Win rate is
> irrelevant this sprint."

Sprint 00 delivers PR-1, PR-2, PR-3, PR-4, PR-5, PR-6, PR-7, PR-8, PR-9, and the stubs PR-10/11/12.
It explicitly excludes any gameplay-quality work.

### 11.3 First comparison (Sprint 01) — the first delta report

The first run-vs-run delta report (PR-14): run-0001 (baseline) vs run-0002 (one deliberate trivial
change) under the *same* frozen regime. **No rule tuning and no deferred lane starts until this delta
report exists** (§7.7, §8 cross-cutting rule).

### 11.4 Deferred lanes (each with an evidence trigger, §8 of the plan)

Deep RL, heavyweight self-play, LLM in-loop play, deck optimizer, value/win-probability model,
signed receipts/crypto provenance, dashboards/live UI, multi-agent tournament/ELO. None start before
the loop has produced at least one delta report showing a metric moved for an explainable reason
(§8). The optional built-in `search_*` lookahead (§8.1) belongs to this deferred set.

### 11.5 Competition runway & cadence

~2 months from this PRD to the **Final Submission Deadline (2026-08-16)**; entry and team-merger
close **2026-08-09**; final evaluation runs to ~2026-08-31 (§8.3, CC-9). This bounds cadence: the
planning cycle (cycle-000) and the first build/comparison cycles must leave ample margin before
2026-08-16. Submission economics (CC-5): 5/day and only the **latest 2** are tracked for final — so
submissions are cheap to iterate, but the final two must be chosen deliberately from ledger evidence,
not reflexively. None of this relaxes the data→optimize ordering (§14).

---

## 12. Non-Goals (explicit)

Per the operator brief and §7.3 / §8 of the plan, TurnTrace in its first cycles is **not**:

- A strong, competitive, optimal, calibrated, or complete agent — and makes no such claim.
- A reinforcement-learning system (no premature RL).
- A deck optimizer (deck is a frozen *input*, not a tuned output — no premature deck optimizer).
- A dashboard or live UI (flat git-diffable files instead).
- An overbuilt receipt/signature or cryptographic-provenance system (flat SHA-256 in a text file).
- A self-play training rig.
- A multi-agent tournament / ELO ladder.
- A consumer of Kaggle starter files into version control (CC-1).
- A vehicle for FORGE/Echelon/CORONA branding in competition-facing docs (CC-8).

---

## 13. Key Unknowns & Assumptions

Resolved simulator facts are in §8.1; facts resolved by the operator-supplied Overview are in §8.3.
The remaining unknowns (U-1…U-4, §8.2) carry assumptions and fallbacks and must be confirmed by the
Capability Probe (PR-9) before the build relies on them. Cross-cutting assumptions:

- `[ASSUMPTION]` The local `cg` lib is representative enough of hosted scoring to be the primary dev
  loop (U-4). Fallback: dual-track local win% vs leaderboard rank.
- `[ASSUMPTION]` Matches are cheap enough to run a meaningful N locally (U-2). Fallback: shrink N.
- `[ASSUMPTION]` The simulator/environment version can be pinned and recorded even if not
  self-reported (NFR-4).
- `[RESOLVED 2026-06-17]` The report/prize track (a distinct, optional **Hackathon**) and the full
  competition timeline (U-5, U-6) are confirmed by the operator-supplied Overview — see §8.3, §10
  (CC-9), and §16 (OD-2/OD-3).

> The first project task is therefore the **Capability Probe** (PR-9): run one match, dump whatever
> the environment exposes, and record what is actually available before the harness is shaped around
> it (§10 "Simulator API uncertainty", §11 Day 1).

---

## 14. Risks & Dependencies

| Risk | Likelihood | Impact | Mitigation | Source |
|---|---|---|---|---|
| **Seed uncontrollable → no byte-replay** | High (no seed param seen) | Medium | Distribution-stable + audit-trail posture (NFR-3); larger N; log-based replay. | U-1, §5.6 |
| **Low local throughput blocks statistical power** | Unknown | Medium | Measure in probe; shrink N; defer RL/self-play. | U-2, §10 |
| **Local/hosted divergence** | Medium | Medium | Record provenance (NFR-4); track local vs leaderboard separately; treat divergence as a finding. | U-4, §10 |
| **Accidental commit of Competition Data** | Medium | **High (rules breach)** | Hard rule: sim lib + card data + starter deck stay local/gitignored; pre-commit hygiene; CC-1 in SDD. | CC-1 |
| **Leaderboard overfitting** | Medium | Medium | Frozen *local* opponent pool never tuned to the leaderboard; never refit on leaderboard feedback alone. | §10 |
| **Too-small opponent pool / small N** | High early | Medium | Label every win% with N; require minimum N before any verdict; grow pool deliberately. | §10 |
| **Overengineering / premature optimization** | Medium | Medium | Flat files; deferred-lanes list (§11.4); hard ordering data→optimize; review checklist (§12 of plan). | §10 |
| **Reproducibility without provenance** | Medium | Medium | Every run records git rev, sim version + source, content hashes (NFR-4). | §10 |
| **Simulator ≠ official Pokémon TCG rules** | Medium | Medium | cabt has documented deviations; analysis/heuristics follow cabt behavior, not the rulebook; keep the cabt rules-differences page as an analyst reference. | CC-10, §8.3 |
| **Deadline pressure erodes evidence-first ordering** | Medium | Medium | ~2-month runway (final 2026-08-16); the data→optimize ordering, claim ceilings, and the review checklist stay binding regardless of time pressure. | §8.3, §11.5 |
| **Hackathon rewards strength → premature optimization temptation** | Medium | Medium | Hackathon ranking weighs leaderboard performance, but TurnTrace's scope stays evidence; optimization happens *inside the machine* only after the first delta report (§11.3). | §8.3, §11.4 |

**External dependencies:** the Kaggle `cg` simulator lib + card data (Competition Data, local only);
the `kaggle` CLI for submission, replay, and log retrieval; a Python runtime matching the
simulator's. No new third-party dependencies are added in cycle-000 (operator hard rule).

---

## 15. Success Criteria — First Planning/Build Cycle (`cycle-000-bootstrap`)

Because cycle-000 is **planning only** (Operator decision, 2026-06-17), its success is the quality
and completeness of the planning artifacts — not running code.

**This cycle succeeds when ALL hold:**

1. **PRD approved** — this document, grounded (every requirement traces to a source), with explicit
   claim-ceiling posture (§9), competition constraints (§10), non-goals (§12), and the resolved-vs-
   unknown simulator surface (§8).
2. **SDD produced and approved** — translating the resolved simulator surface and the §6/§7
   requirements into a design, with the `sim/` glue isolated as the single blast radius for sim-API
   facts, and the runtime/offline separation enforced structurally.
3. **Sprint plan produced and approved** — Sprint 00 scoped to PR-1…PR-9 + stubs, with concrete,
   verifiable acceptance checks mirroring §7.4 of the plan, and rule-tuning explicitly forbidden
   until the first delta report.
4. **No implementation, no Kaggle files committed, no dependencies added** (operator hard rules
   upheld).
5. **Operator decisions (§17) recorded** — the open unknowns (U-5 Strategy track, U-6 timeline, and
   the repo-layout decision) are either answered or explicitly logged as pending before the build
   cycle opens.

> **Bounded definition of the *build's* success (for the next cycle, not this one):** Sprint 00
> succeeds when the random-legal agent runs the full evaluation set against one opponent under
> `regime-v001`, writes one immutable `run-0001/` (records + traces + summary + manifest + hashes),
> the trace-hash join is exercised, the immutability guard refuses to overwrite, and exactly one
> ceiling-bounded ledger row is appended — *regardless of win rate* (§7.4).

---

## 16. Operator Decisions Required Before Implementation

| ID | Decision | Why it matters | Status |
|---|---|---|---|
| **OD-1 — Repo layout / code home** | The plan proposes a root-level tree (`agents/ sim/ eval/ analysis/ frozen/ runs/ docs/`). TurnTrace is a Loa-mounted repo (App Zone = `src/lib/app/`; `grimoires/` is State Zone). Decide where the data-loop code lives and how `runs/` (generated) and `frozen/` (hand-authored) map onto the repo without colliding with Loa conventions. | Shapes the SDD's file tree and the gitignore boundary that keeps Competition Data out of version control (CC-1). | **Open — SDD input** |
| **OD-2 — Strategy Category confirmation (U-5)** | Confirm whether a formally distinct report track exists (vs. pure leaderboard). | Determines whether the Strategy report is a graded deliverable or an internal evidence artifact. | **Resolved 2026-06-17:** a distinct **Hackathon** track (report-based, prize-eligible) is separate from this Simulation competition; Hackathon ranking weighs leaderboard performance **and** report (§8.3). |
| **OD-3 — Competition timeline (U-6)** | Entry deadline, team-merger deadline, final-submission deadline. | Bounds how aggressively cycles must move; informs submission cadence (CC-5). | **Resolved 2026-06-17:** entry/merger **2026-08-09**; final submission **2026-08-16**; final eval ~2026-08-31 (§8.3, CC-9). |
| **OD-4 — Capability Probe is the first build task** | Confirm Sprint 00 opens with PR-9 (probe) before harness code is shaped. | Prevents shaping the harness around unverified assumptions (U-1…U-4). | **Recommended; confirm at sprint plan** |
| **OD-5 — Reproducibility posture** | Adopt distribution-stable + audit-trail as baseline; seed control treated as an unknown; byte-replay a future upgrade. | Sets claim-ceiling language and evaluation design. | **Decided 2026-06-17 (this PRD, NFR-3)** |
| **OD-6 — Cycle scope** | cycle-000 = planning artifacts only; Sprint 00 build is the next cycle. | Sets what "first-cycle success" means (§15). | **Decided 2026-06-17** |

---

## 17. Sources & Traceability

| Source | Used for |
|---|---|
| `grimoires/loa/context/Planning/Pokemon TCG AI Battle - Data Loop Plan.md` (§1–§12) | Product vision, disciplines, functional/non-functional requirements, claim-ceiling posture, maturity ladder, scope, risks. |
| `grimoires/loa/context/Planning/Competition Rules.md` | Competition-facing constraints (CC-1…CC-8): data use, redistribution, ingress/egress, licensing, submission/team limits, scoring. |
| `grimoires/loa/context/Planning/Competition Dataset Description.md` | Card data schema context; episode replay/export availability (CC-6). |
| `grimoires/loa/context/Planning/sample_submission/main.py` | Agent interface (`agent(obs_dict) -> list[int]`), deck submission, legal-option selection. |
| `grimoires/loa/context/Planning/sample_submission/cg/api.py` | State/observation/option/log schemas; ending-cause; optional search API. |
| `grimoires/loa/context/Planning/sample_submission/cg/game.py`, `cg/sim.py` | Local match execution surface; absence of a seed parameter. |
| `grimoires/loa/context/Planning/simulation_competitions.md` | Kaggle submission/replay/logs workflow (CC-6). |
| `grimoires/loa/context/Planning/pokemon-tcg-ai-battle-publicleaderboard-*.csv` | Confirms numeric leaderboard skill score (offline scouting input only; 1256 teams). |
| `grimoires/loa/context/Planning/competition-overview.md` (operator-supplied Overview, 2026-06-17) | Two-track structure (Simulation vs Hackathon), timeline/deadlines, cabt engine + kaggle-environments 1.14.10, legal-move guarantee, TrueSkill scoring (μ₀=600, margin-independent), validation episode, submission mechanics (§8.3, §10, §11.5). Resolves U-5/U-6. The live page itself is JS-rendered and was not machine-readable via fetch. |
| cabt API docs `https://matsuoinstitute.github.io/cabt/`; cabt rules-differences page; `kaggle-environments` 1.14.10 (`github.com/Kaggle/kaggle-environments`) | **Reference for the SDD/build phase** — not fetched in this planning cycle (out of scope; operator instruction limited fetching to official Kaggle pages). |
| Operator brief + decisions (2026-06-17) | Cycle scope, reproducibility posture, branding rule, hard rules, planning posture. |

---

*This PRD is product-level and intentionally stops short of implementation design. The next artifact
is the SDD (`/architect`), which translates §6/§7/§8 into a design with the `sim/` glue isolated and
the runtime/offline split enforced. No application code is written until the sprint plan exists and
the build cycle opens.*
