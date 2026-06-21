# Cycle-008 PRD — Diagnostics & Rung-3 Readiness: Build Trace-Safe Descriptive Eyes, Not Instincts

> Planning artifact (PRD). Status: **DRAFT — awaiting operator acceptance.** This PRD specifies a **narrow
> diagnostics + governance-hardening** cycle (research Option A spine + a bounded D-lite governance rider). The PRD
> itself **opens no implementation gate and authorizes no irreversible act**: code lands only through
> `/architect → /sprint-plan → /implement → /review-sprint → /audit-sprint → operator acceptance`
> (`docs/operator/turntrace-loop-contract.md` §1, §6; OA-2-class build gate). **This drafting pass builds no code,
> generates no fresh evidence, runs no eval, chooses no candidate, pre-registers no Rung-3 attempt, chooses no numeric
> margin `M`, issues no SP-6, promotes no value, writes no ledger row, and advances no claim ceiling.** It defines
> *what Cycle-008 must hold* at product/governance level; it does not design the SDD or sprint plan.
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, hand contents, simulator logs, run-dir dumps,
> Pokémon Elements, Daily-Top-Episode data, Kaggle episode data, Discord/peer screenshots, `deck.csv` rows, `cg/`
> SDK, PDFs/CSVs, or Competition Data appear here (CC-1/CC-2, ESP; SP-6/SP-9). **No dispersion metric values appear
> here. No numeric margin `M` is chosen or stated.** Runs are referenced by `run_id`/pattern, regimes by
> `regime_id`, metrics by sanitized *name* only. The forbidden agent words (*strong / competitive / optimal /
> calibrated / complete*) and the inferential terms (*std-dev / variance / CI / p-value / significance /
> hypothesis-test / error-bar*) appear only as the negated/forbidden language they are.

## 0. State verified (2026-06-20, before drafting)

| Assumption to verify | Result |
|---|---|
| Current HEAD / branch | `main` @ `95d4811` — *docs: clean TurnTrace README and Butterfree Zone* (== `origin/main`; not behind) |
| Local branch not behind `origin/main` | both at `95d4811e068066c7df898de1f03d6530cd2a781e` — not behind |
| Cycle-007 status | **CLOSED — accepted, committed, pushed** (`docs/cycles/cycle-007/07-closeout.md`); Rung 2 earned and held |
| `docs/ledger.md` byte-unchanged | **byte-unchanged**; `git hash-object = 7da7e9a8dbed6561669d1569445eb9fe67a953fb` |
| `docs/claim-ceiling.md` unchanged | **unchanged**; ceiling = **Rung 2** (`git hash-object = 3d99759b919f7d75bc41ea81cd82e5f1fb974be7`) |
| `.claude/` untouched | **no drift**; `integrity_enforcement: strict` → no HALT |
| No staged files | **none staged** |
| `.beads/issues.jsonl`, `grimoires/loa/NOTES.md`, `grimoires/loa/README.draft.md` dirty | all modified/untracked, **unstaged** (pre-existing State-Zone housekeeping); **must not be staged or cleaned** by this cycle |
| Binding research input present | `grimoires/loa/a2a/cycle-008/00-pre-prd-research.md` (gitignored State-Zone; recommends Option A + D-lite; accepted by operator) |

**All assumptions hold. No finding forces a stop.** PRD acceptance and the build gate are **separate operator acts**
this PRD does not self-authorize.

| Field | Value |
|---|---|
| **Cycle** | Cycle-008 |
| **Working title** | Diagnostics & Rung-3 Readiness: Build Trace-Safe Descriptive Eyes, Not Instincts |
| **Type** | Product Requirements Document (planning artifact for a diagnostics + governance-hardening cycle) |
| **Status** | DRAFT — awaiting operator acceptance; next Golden-Path step is SDD / architecture |
| **Date** | 2026-06-20 |
| **Current main** | `95d4811` — *docs: clean TurnTrace README and Butterfree Zone* |
| **Binding research input** | `grimoires/loa/a2a/cycle-008/00-pre-prd-research.md` (gitignored State-Zone research input; recommends **Option A + D-lite**, accepted by operator for this pass) |
| **Posture** | **Diagnostics + Rung-3 readiness + D-lite governance.** Rung 2 holds at open and is **preserved**; no ceiling movement this cycle. Build **instruments, not instincts.** |
| **Claim ceiling (at open)** | **Rung 2 — "beats random-legal"** (narrowly bounded to `scripted-v001` over `random_legal-v001` under `regime-v003`) |

## Required posture (binding)

- **Cycle-008 is a diagnostics + governance-hardening cycle** (research Option A spine + bounded D-lite rider). It is
  **not** a Rung-3 attempt, **not** a target-selection cycle, and **not** agent-building.
- **Rung 2 holds at cycle open and is preserved.** No ledger row is written; no claim-ceiling advance occurs; the
  standing claim stays narrowly bounded to `scripted-v001` beating `random_legal-v001` under `regime-v003`.
- **Descriptive-only — instruments, not instincts.** The diagnostic may report *what happened*. It MUST NOT judge play
  quality, score a decision, assert a "should-have," recommend a move, or act as a coach / evaluator / policy
  recommender.
- **Scouting is hypothesis, never proof.** The scouting document and any peer/leaderboard/episode notes are search
  targets only; an improvement claim from scouting alone is **FM-11** and is forbidden (`docs/failure-modes.md:142-160`).
- **Same-regime / same-deck / same-opponent-pool discipline is preserved.** A regime pins `{seed_set, opponent_pool,
  deck_pool, metrics_spec}`; a deck change is regime-changing by construction; cross-regime comparison is barred (NFR-5).
- **Prefer existing sealed runs.** Diagnostics read existing sealed run artifacts. Any fresh diagnostic run is
  explicitly **non-ceiling-bearing** and must justify why existing sealed runs are insufficient.
- **No numeric margin `M` anywhere.** `M` lives only in a future Rung-3 pre-registration record (a numeric `M` in any
  other tracked artifact is a posture violation → HALT).
- **No new simulator instrumentation.** No energy / attach instrumentation, no per-Pokémon instrumentation, no card
  semantics, no attack-cost decoding, no OptionType semantic decoding.
- **No per-decision quality detectors/scorers for FM-03 / FM-04 / FM-06 / FM-08.** Those remain a separate operator
  decision (`docs/failure-mode-taxonomy-v001.md` detector boundary).
- **The runtime-agent lane stays closed.** No new agent, pilot, heuristic, candidate, value/win-probability model,
  search loop, FunSearch loop, RL/self-play system, MCTS, tournament harness, deck optimizer, or dashboard.
- **Rung-3 ladder semantics is a bounded docs-only deliverable** (OD-C8-3, resolved): it defines the comparison
  **form only** and freezes nothing.
- **`.claude/` (System Zone) is never edited; no State-Zone cleanup is performed.** Pre-existing dirty State-Zone files
  stay unstaged and untouched.

**The bright line for the whole cycle:** *Cycle-007 earned Rung 2 by re-running a frozen agent and pre-registering one
clean comparison. Cycle-008 does not attempt the next rung — it builds the trace-safe, descriptive diagnostic eyes and
the governance hardening that make a future Rung-3 target selection credible, then stops. It builds instruments, not
instincts. Until a future, separately-gated, pre-registered attempt, Rung 2 holds, `docs/ledger.md` stays
byte-unchanged, and no value is promoted.*

## 1. Product / cycle overview

TurnTrace is a local, sanitized data-loop / evaluation harness for a simulator-based trading-card-game agent
(`README.md:3-5`). Across seven cycles it built and exercised a strict evidence-and-claim-ceiling discipline,
culminating in **Cycle-007**, the first gated Rung-2 admission attempt, which PASSed and advanced the ceiling
**Rung 1 → Rung 2 ("beats random-legal")**, bounded strictly to one ledgered same-regime descriptive result
(`docs/cycles/cycle-007/07-closeout.md`).

The Cycle-008 pre-PRD research (`grimoires/loa/a2a/cycle-008/00-pre-prd-research.md`) used external competition
scouting signals as **hypotheses** and evaluated six cycle shapes (A–F) against current repo reality. It found that
the behaviors the scouting signals point at (board survivability, prize tempo, retreat, attach) sit behind a **triple
constraint**: (C) capability — the simulator surface exposes only counts/booleans/outcomes, not energy, per-Pokémon
state, or decoded action semantics; (T) tooling — **no `analysis/` tool reads per-decision trace *content* today**
(only `replay_check` reads sidecars opaquely for hashing); (G) governance — descriptive aggregates are within the
already-open narrow-planning lane, but per-decision *quality scorers* for FM-03/04/06/08 are explicitly forbidden
without a separate operator decision. The research recommended **Option A (diagnostics / feature-readiness) as the
spine, with a bounded D-lite governance rider, staged ahead of target-selection (B) and any candidate build (C)**.
**The operator has accepted Option A + D-lite for this planning pass, with guardrails.**

**Mission (binding).** Give TurnTrace better **same-regime, trace-safe, descriptive** diagnostic eyes — and harden the
ledger gate the next rung will lean on — so that a future Rung-3 target can be chosen from *measured observables*, not
from peer intuition. Build instruments, not instincts. Advance no claim.

**Who consumes this PRD.** The **operator** (accepts this PRD; opens the build gate; is the only party who could later
open a Rung-3 attempt — out of scope here); the **architect / sprint-planner** (`/architect`, `/sprint-plan`, who
resolve the SDD-level and sprint-level design this PRD defers); the **implementer** (`/implement`, who lands the
sanctioned `analysis/` diagnostic, the sanitizer, the ledger-row validator, and the docs); and the
**reviewer/auditor** (`/review-sprint`, `/audit-sprint`).

## 2. Problem statement

Rung 2 is earned, but the loop is **blind** to the behaviors a future Rung-3 target would care about, and the ledger
gate is not yet mechanically validated. Concretely:

1. **No `analysis/` tool reads per-decision trace content.** The sealed `decision-trace.jsonl` sidecars record rich
   board-shape fields (`active_present`, `bench_count`, `prize_count` per side; `final_prize_counts`; `ending_cause`),
   but every existing analysis tool reads only `match_results/*.json` summaries — only `replay_check.py` opens the
   sidecars, and only opaquely for hash recompute. The descriptive signals exist in sealed artifacts but are
   **unconsumed**.
2. **There is no tracked ledger-row validator.** The Rung-2 row was appended via a guarded binary-append script; no
   tracked schema validator content-checks `docs/ledger.md` (Cycle-007 carry-forward 3,
   `docs/cycles/cycle-007/07-closeout.md:219-222`). The next rung's row would lean on an unvalidated gate.
3. **Rung 3 is named but undefined.** `docs/claim-ceiling.md:32` states only "No Rung 3, and no claim beyond 'beats
   random-legal'." Without a governance definition of the comparison *form*, Cycle-009 risks conflating "what does
   Rung 3 mean?" with "what candidate should we try?"
4. **Conventions are informal.** The SP-6 / promoted-summary `NNa-` numbering convention and the ledger
   metric-column ("see cited summary") convention are carry-forwards (1 and 2) not yet written down.

None of these is solved by building an agent or attempting a rung. Each is an **instrument** or a **governance
clarity** gap. Cycle-008 closes the measurable, descriptive, same-regime subset of them and explicitly documents what
remains blocked.

## 3. Posture statement (binding)

- **Cycle-008 is a diagnostics + governance-hardening cycle** (research Option A + D-lite). **Rung 2 holds at open and
  is preserved.**
- **No Rung-3 attempt, no target selection, no candidate, no fresh promotion evidence, no SP-6, no ledger row, no
  ceiling advance** occurs in Cycle-008.
- **The diagnostic is descriptive-only.** It applies no quality judgment and produces no per-decision score,
  "should-have," or recommendation. It is not a coach.
- **This PRD authorizes nothing irreversible.** It opens no gate, chooses no `M`, builds no code, generates no
  evidence, and mutates neither `docs/ledger.md` nor `docs/claim-ceiling.md`.
- **The PRD makes no claim of agent strength, calibration, tournament readiness, leaderboard standing, or broader
  Pokémon TCG skill** — those words appear only as forbidden/negated language.

## 4. Goals — what Cycle-008 must produce

Stated at product/governance level. **How** these are sprinted/architected is deferred to the SDD and sprint plan
(§16); this PRD states **what** must hold.

- **G1 — Trace-safe descriptive diagnostic.** A new bounded `analysis/` module that reads existing sealed run artifacts
  (`match_results/*.json` and `traces/<match_id>.jsonl` sidecars) and emits **sanitized, descriptive aggregate**
  outputs over the authorized surfaces (§9). Offline, stdlib-only, single-regime, descriptive-only.
- **G2 — Output sanitizer (fail-closed).** The diagnostic's tracked-eligible output passes a sanitization discipline
  parity-or-stricter with `eval/hygiene_check.py` + `analysis/evidence_summary.py`, and **rejects poisoned fixtures**.
- **G3 — Ledger-row validator (D-lite governance rider).** A tracked validator that content-checks `docs/ledger.md`
  rows against the 18-column schema and append-only discipline, **rejecting malformed rows** and **writing/promoting
  nothing** (Cycle-007 carry-forward 3).
- **G4 — Governance & convention docs (D-lite).** The SP-6 / promoted-summary `NNa-` numbering convention
  (carry-forward 1); the ledger metric-column "see cited summary" convention (carry-forward 2); and a **blocked-family
  map** classifying each scouting-inspired surface as measurable-now / needs-future-sim-instrumentation /
  requires-separate-operator-authorization.
- **G5 — Rung-3 ladder semantics (bounded docs-only).** A docs-only definition of the Rung-3 comparison **form only** —
  *a future candidate must beat the current non-trivial incumbent under a same-regime, fresh-evidence, pre-registered
  comparison* — that **freezes no candidate, threshold, numeric `M`, `K`/`n` values, regime id, or target feature
  family**, and opens no attempt (OD-C8-3, resolved).
- **G6 — Preserve all invariants (hard).** `docs/ledger.md` stays byte-unchanged (`7da7e9a8…`),
  `docs/claim-ceiling.md` stays unchanged (`3d99759b…`; still Rung 2), no value reaches tracked promotion status, and
  the ledger remains the only ceiling-bearing artifact.

## 5. Scope

**In scope (Cycle-008), behind the loop + the build gate.**
- Tracked planning/governance artifacts under `docs/cycles/cycle-008/` (this PRD; the SDD; the sprint plan).
- A **new bounded `analysis/` diagnostic module** reading existing sealed run artifacts and emitting sanitized
  descriptive aggregates over the §9 surfaces — landing through `/implement → /review-sprint → /audit-sprint`.
- A **fail-closed output sanitizer** for the diagnostic (parity-or-stricter with the existing hygiene/validator
  discipline), plus tests including poisoned fixtures.
- A **tracked ledger-row validator** (gate-only; writes nothing).
- **Docs**: SP-6/promoted-summary numbering convention; ledger metric-column convention; blocked-family map; the
  bounded docs-only **Rung-3 ladder semantics** definition (form only).
- Tests for all of the above (stdlib `unittest` / plain-assert, parity with the existing suite).

**Out of scope (Cycle-008).**
- Any Rung-3 attempt; any Rung-3 target/candidate selection; any pre-registration of a Rung-3 attempt; any numeric `M`.
- Any fresh **promotion** evidence; any SP-6; any ledger row; any claim-ceiling advance; any PASS/FAIL/INCONCLUSIVE
  verdict.
- Any new runtime agent, pilot, heuristic, candidate, value/win-probability model, search loop, FunSearch, RL,
  self-play, MCTS, tournament harness, deck optimizer, or dashboard.
- Any **per-decision quality detector/scorer** for FM-03 / FM-04 / FM-06 / FM-08, or any move-quality judgment,
  "should-have," coaching, or policy recommendation.
- Any new **simulator instrumentation**: energy / attach, per-Pokémon state, card semantics, attack-cost decoding, or
  OptionType semantic decoding.
- Any new regime; any deck change; any cross-regime comparison; any inferential statistic.
- Any Daily-Top-Episodes / Kaggle episode ingest; any episode-derived claim.
- Any raw Competition Data / Pokémon Elements / deck lists / card IDs/names / raw traces / simulator logs / run-dir
  dumps / `deck.csv` / `cg/` / PDFs/CSVs / Discord/peer data in tracked docs.
- Any `.claude/` edit; any State-Zone cleanup.

## 6. Non-goals (explicit)

Cycle-008 does **not**:

- **Attempt Rung 3, choose a Rung-3 target, or freeze a candidate / `M` / `K` / `n` / regime id / target feature
  family.** Defining the Rung-3 comparison *form* (G5) is governance clarity, not target selection.
- **Judge play quality.** No per-decision score, "should-have," missed-lethal/bad-trade/wasted-resource detector
  (FM-03/04/06/08), coaching, or gameplay-policy recommendation.
- **Imply agent strength.** No claim that any agent is *strong / competitive / optimal / calibrated / complete*, and
  no implication of calibration, tournament readiness, leaderboard standing, or broader Pokémon TCG skill (forbidden
  words appear only as negated language).
- **Add simulator instrumentation** (energy / per-Pokémon / card semantics / attack-cost / OptionType decode) or widen
  the runtime decision contract.
- **Promote anything, write a ledger row, or move the ceiling.** Rung 2 is preserved exactly as Cycle-007 left it.
- **Compare across regimes, change the deck, or mint a new regime.**
- **Ingest episodes** or treat scouting / Daily Top Episodes as proof (SP-9; FM-11).
- **Embed raw Competition Data / Pokémon Elements / traces / logs / deck lists** in tracked docs; **edit `.claude/`;**
  or **clean State-Zone dirt.**

## 7. Functional requirements

The FRs state **what** Cycle-008 must hold; **how** (module shape, internal design, task breakdown) is deferred to the
SDD and sprint plan (§16).

### C8-FR-1 — Trace-safe descriptive diagnostic
1. A **new bounded module under `analysis/`** MUST read existing sealed run artifacts — `runs/<run_id>/match_results/*.json`
   and the per-decision `runs/<run_id>/traces/<match_id>.jsonl` sidecars — and emit **descriptive aggregate** outputs over
   the authorized surfaces (§9).
2. The module MUST be **descriptive-only**: it MUST use the allowed descriptive vocabulary (`count`, `min`, `max`,
   `range`, `mean`, `median`, `spread`) and MUST NOT compute or emit any move-quality judgment, per-decision score,
   "should-have," optimal-action label, or recommendation. It is not a coach, evaluator of move quality, or policy
   recommender (NFR-3, NFR-10).
3. The module MUST remain **offline**: it imports run-dir artifacts and intra-`analysis/` helpers only, and MUST NOT
   import `sim` or `cabt` (NFR-2; `tests/test_import_direction.py`). It MUST be **stdlib-only** (NFR-1).
4. The module MUST enforce **single-regime** inputs: a mixed-regime invocation hard-refuses (exit 2), parity with
   `analysis/delta_report.py` / `dispersion_report.py` / `evidence_summary.py` (NFR-5).
5. The module MUST **prefer existing sealed runs**; it MUST be exercisable and acceptance-tested against **synthetic
   fixtures** so it does not depend on any specific local (gitignored) run dir being present (C8-FR-7).

### C8-FR-2 — Authorized diagnostic surfaces (descriptive)
The diagnostic MAY emit, and is bounded to, the following **descriptive** surfaces, each computed from existing recorded
trace/summary fields with **no new simulator instrumentation** (NFR-9):
1. **Outcome aggregates** — counts/rates of `ending_cause` ∈ {`no-active`, `deck-out`, `prize-out`, `card-effect`,
   `error`} and `result` ∈ {`win`, `loss`, `draw`, `error`} (consistent with `analysis/failure_report.py`).
2. **Board-shape distributions** — descriptive distributions of `active_present` (bool) and `bench_count` per side
   across decision rows (`public_state_summary`).
3. **Prize trajectory** — descriptive statistics of the `prize_count` trajectory and the terminal `final_prize_counts`.
4. **Decision-latency distribution** — descriptive statistics of `decision_latency_ms` (and match `wall_clock_ms`).
5. **Error / illegal / malformed-selection regression surfaces** — `result == error` presence, `invalid_action_count`
   (where `invalid_action_detectable` is true), with `timeout` reported as the soft, undetectable signal it is
   (`timeout = null`).
6. Each surface MUST be **descriptive of what occurred**; none may be framed as a mistake, fault, or quality score, and
   none may require energy, per-Pokémon state, card identity, retreat cost, or decoded OptionType semantics (NFR-9,
   NFR-10).

### C8-FR-3 — Output sanitizer (fail-closed)
1. The diagnostic's tracked-eligible output MUST pass a sanitization discipline **parity-or-stricter** with
   `eval/hygiene_check.py` and `analysis/evidence_summary.py`'s validator.
2. The sanitizer MUST **reject (fail-closed)** any output containing: Competition-Data paths; card IDs/names or Pokémon
   Elements; raw per-decision-row field names/values (e.g. `public_state_summary`, `selected_action`,
   `legal_actions_sample`, `decision_latency_ms` as raw rows, `private_state_summary`, `post_decision_observation`);
   inferential vocabulary; affirmative forbidden agent words; cross-regime field/value markers; a numeric `M`-shaped
   governance threshold; or a `hashes`-keyed value that is not SHA-256-shaped.
3. A **poisoned fixture** for each rejection class MUST be rejected; a clean fixture MUST be accepted. The sanitizer
   MUST be exit-code-disciplined consistent with the existing validator contract.

### C8-FR-4 — Ledger-row validator (D-lite governance rider)
1. A **tracked validator** MUST content-check `docs/ledger.md` rows: the **18-column schema verbatim**
   (`date | run_id | regime_id | git_rev | sim_version | agent_version | opponent_pool_ref | seed_set_ref | games |
   win_rate | illegal_action_rate | timeout_rate | error_rate | avg_turns | mode | hypothesis | claim_ceiling |
   notes`), **non-empty `claim_ceiling`**, append-only discipline (no edited past row), single `regime_id` per row, and
   SHA-256-shaped hash references where the row cites a summary by hash.
2. The validator MUST **reject a malformed row** (wrong column count, empty `claim_ceiling`, an edited prior row, a
   non-SHA-256 hash where a digest is required) and MUST **accept the current valid `docs/ledger.md`**.
3. The validator MUST be **gate-only**: it writes nothing, promotes nothing, and never mutates `docs/ledger.md` or any
   tracked `docs/` path (NFR-6).

### C8-FR-5 — Governance & convention docs (D-lite)
1. **SP-6 / promoted-summary numbering convention** — document the `NNa-` insertion convention (e.g.
   `06a-sp6-promoted-summary.md`) so future cycles avoid `07-`/closeout path ambiguity (carry-forward 1).
2. **Ledger metric-column convention** — document the "see cited summary" by-reference + content-hash pattern for the
   numeric columns (carry-forward 2), preserving the no-embed safety pattern.
3. **Blocked-family map** — a tracked, sanitized map classifying each scouting-inspired surface as one of:
   **measurable now** (descriptive, this cycle); **needs future sim instrumentation** (e.g. energy/attach, backup
   attacker, retreat/attack semantics — capability-blocked today); **requires separate operator authorization** (the
   per-decision quality surfaces FM-03/04/06/08). The map names no card data and embeds no raw content.

### C8-FR-6 — Rung-3 ladder semantics (bounded docs-only; OD-C8-3 resolved)
1. Cycle-008 MUST author a **bounded docs-only** definition of Rung-3 ladder **semantics** — the comparison **form
   only**: *a future candidate must beat the current non-trivial incumbent under a same-regime, fresh-evidence,
   pre-registered comparison.*
2. The definition MUST **freeze nothing**: no candidate identity, no numeric `M`, no `K`/`n` values, no regime id, no
   target feature family, and no threshold. It MUST **open no Rung-3 attempt**.
3. Its sole purpose is governance clarity — to make future Rung-3 target selection credible and to prevent Cycle-009
   from conflating "what does Rung 3 mean?" with "what candidate should we try?" It is descriptive of the *form*, never
   prescriptive of a *target*.

### C8-FR-7 — Fresh-run posture (prefer existing sealed runs)
1. The diagnostic MUST **prefer existing sealed run artifacts** as its input.
2. Any proposed **fresh diagnostic run** MUST be explicitly **non-ceiling-bearing**, MUST justify why existing sealed
   runs are insufficient, and MUST NOT be a promotion-evidence run, feed a ledger row, or touch the claim ceiling. A
   fresh run, if any, is descriptive instrumentation only.

### C8-FR-8 — Invariants held (hard)
1. Until and unless a future separately-gated cycle says otherwise, `docs/ledger.md` MUST stay byte-unchanged
   (`7da7e9a8…`), `docs/claim-ceiling.md` MUST stay unchanged (`3d99759b…`; still Rung 2), **no** value is promoted,
   **no** SP-6 is issued, **no** ledger row is written, and **no** ceiling advance occurs.
2. The ledger remains the **only ceiling-bearing artifact**; the diagnostic, sanitizer, validator, and docs carry **no
   ceiling of their own**.

## 8. Non-functional / validation requirements

- **NFR-1 — stdlib-only.** No third-party runtime dependency is added; the diagnostic, sanitizer, and validator are
  Python standard library only.
- **NFR-2 — Import-direction preserved.** `analysis/` imports run-dir artifacts + intra-`analysis/` helpers only;
  **no `sim` / `cabt` import**; `tests/test_import_direction.py` stays green.
- **NFR-3 — Descriptive-only / no quality judgment.** No per-decision scorer, move-quality label, "should-have,"
  coaching, or policy recommendation; the diagnostic reports observed counts/distributions/trajectories only.
- **NFR-4 — Sanitization / data boundary.** No tracked-doc leakage; the output sanitizer rejects poisoned fixtures; no
  raw Competition Data / Pokémon Elements / traces / logs / deck lists / `deck.csv` / `cg/` reach tracked artifacts;
  reference-not-embed (`run_id` / hashes / sanitized metric names / local path only).
- **NFR-5 — Same-regime only.** Mixed-regime input hard-refuses (exit 2); no cross-regime comparison; no deck change;
  no new regime.
- **NFR-6 — Ledger / ceiling invariance.** No ledger row written; no claim-ceiling movement; the ledger-row validator
  writes nothing.
- **NFR-7 — No numeric `M`.** No numeric promotion margin `M` appears in any Cycle-008 artifact; `M` belongs only to a
  future pre-registration record.
- **NFR-8 — Claim safety.** Forbidden agent words and inferential terms appear only as negated/forbidden language; no
  PRD or diagnostic language implies Rung 3, agent strength, calibration, tournament readiness, leaderboard strength,
  or broader Pokémon TCG skill.
- **NFR-9 — No new instrumentation.** No energy / per-Pokémon / card-semantics / attack-cost / OptionType-semantic
  decoding; the diagnostic uses only fields the simulator already exposes and the trace already records.
- **NFR-10 — Detector boundary.** No per-decision quality detector/scorer for FM-03 / FM-04 / FM-06 / FM-08; those
  remain a separate operator decision (`docs/failure-mode-taxonomy-v001.md`).
- **NFR-11 — Zone discipline.** Tracked code is App Zone (`analysis/`, `tests/`); planning artifacts are Docs/State
  Zone; `.claude/` is never touched; pre-existing dirty State-Zone files stay unstaged and uncleaned.
- **NFR-12 — Implement-time citation revalidation.** Any line anchor a later sprint relies on MUST be re-validated
  against the build-time HEAD before coding.

## 9. Diagnostic surface scope (binding)

The diagnostic is bounded to the **descriptive** surfaces in C8-FR-2, each computed from already-recorded fields. The
research's triple-constraint classification governs what is in vs out:

- **Measurable now (descriptive, in scope):** outcome / ending-cause aggregates (incl. `no-active`, `deck-out`,
  `prize-out`); `active_present` / `bench_count` distributions; `prize_count` trajectory descriptive stats;
  decision-latency distribution; error / illegal / malformed-selection regression surfaces.
- **Needs future sim instrumentation (out of scope; documented in the blocked-family map, G4):** backup-attacker
  readiness, attach / energy tempo, attack-vs-setup timing, contextual-retreat semantics — all require fields the
  simulator surface does not expose today (no energy field, no per-Pokémon state, raw OptionType tokens only).
- **Requires separate operator authorization (out of scope; documented):** per-decision quality judgment of prize
  trades (FM-03), wasted resources (FM-04), missed lethals (FM-06), bad search targets (FM-08) — `detector: forbidden`.

The diagnostic MUST describe **what happened** within the "measurable now" set, and the blocked-family map MUST record
the other two classes as future candidates, **not** built now (OD-C8-5).

## 10. Sanitization & data-boundary requirements (product level)

At product/requirements level (architecture → SDD), Cycle-008 MUST:
1. **Keep all raw data local.** Generated runs and their sidecars stay local/gitignored; tracked artifacts hold
   sanitized references only (`run_id` / hashes / sanitized metric names / local path).
2. **Sanitize diagnostic output before any tracked use.** The C8-FR-3 sanitizer is the mechanical gate; it is
   parity-or-stricter with `eval/hygiene_check.py` and `analysis/evidence_summary.py`, and is fail-closed.
3. **Never embed raw per-decision content.** Decision-row field names/values, card identity, Pokémon Elements, and
   inferential terms never appear in tracked diagnostic output (parity with the `evidence_summary` forbidden-field
   discipline).

## 11. Rung-3 readiness & ladder-semantics scope (binding)

- **Rung-3 ladder semantics (G5 / C8-FR-6) is a docs-only definition of the comparison form**, authorized by OD-C8-3:
  *a future candidate must beat the current non-trivial incumbent under a same-regime, fresh-evidence, pre-registered
  comparison.* It freezes no candidate, threshold, numeric `M`, `K`/`n`, regime id, or target feature family, and opens
  no attempt.
- **Readiness, not attempt.** Cycle-008 makes future target selection *credible* by producing measured, same-regime,
  descriptive observables and by hardening the ledger gate; it does not select a target or generate promotion evidence.
- **The incumbent referenced by the form is descriptive context only.** Naming the *form* ("beats the current
  non-trivial incumbent") is governance clarity; it neither freezes `scripted-v001` as a baseline for a specific
  attempt nor authorizes one.

## 12. Claim-ceiling posture

The loop sits at **ladder Rung 2**, and **Cycle-008 holds Rung 2 at open and preserves it**:

```
Rung 0  env not trusted
Rung 1  legal completion
Rung 2  beats random-legal                         ← current, held and PRESERVED this cycle
Rung 3  beats the non-trivial incumbent            ← NOT attempted; comparison FORM defined docs-only (G5); no target frozen
        (same-regime, fresh-evidence, pre-registered)
Rung 4  stable, report-ready
```

**Allowed claim form** — relative, local, descriptive, carrying its `n`, `K`, and `regime_id`. **Forbidden claim forms**
(negated-only): gameplay strength; statistical significance; cross-regime uplift; leaderboard quality; calibration;
optimality; competitiveness. Only the ledger, advanced by a future separately-gated operator decision on a
pre-registered PASS, can carry Rung 3. **Cycle-008 advances no ceiling.**

## 13. Evidence-storage & data-boundary discipline

Carried verbatim-in-intent from the standing rules (`docs/operator/turntrace-loop-contract.md` §7-§8;
`docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` SP-6/SP-8/SP-9; `docs/failure-modes.md` FM-10/FM-11):

- **Raw Competition Data never enters git** (CC-1/CC-2): `cg/` SDK, card data, raw deck lists, `deck.csv`, PDFs/CSVs,
  run-dir dumps — local-only under gitignored `grimoires/loa/context/`.
- **Pokémon Elements never appear in tracked artifacts.**
- **Generated runs, dispersion values, and diagnostic raw output stay local/gitignored;** tracked artifacts hold
  sanitized references only. **No numeric `M`** appears in any tracked artifact.
- **Daily Top Episodes / raw episode datasets stay local/ignored (SP-9);** never tracked, never a runtime dependency,
  never Rung-readiness proof without a same-regime TurnTrace comparison (FM-11).
- **Simulator behaviour is authoritative (SP-8 / CC-10);** official-rule assumptions must not override it (FM-10).
- **Only sanitized artifacts are tracked.** `eval/hygiene_check.py` remains the mechanical staging gate; the new
  diagnostic sanitizer is parity-or-stricter.

## 14. Risks and mitigations

| ID | Risk | Mitigation |
|---|---|---|
| **R1** | **Scouting treated as proof (FM-11)** | Required posture + NFR-8: scouting is hypothesis only; no episode/peer claim enters tracked docs; the diagnostic measures same-regime observables. |
| **R2** | **Diagnostic drifts into a coach / quality scorer** | C8-FR-1.2 / NFR-3 / NFR-10: descriptive-only; no per-decision score/"should-have"; FM-03/04/06/08 detectors forbidden; OD-C8-2 withholds quality-scoring authorization. |
| **R3** | **Sim-instrumentation creep** (energy / per-Pokémon / OptionType decode) | NFR-9 / §9: only already-recorded fields used; blocked families documented (G4), not built (OD-C8-5). |
| **R4** | **Tracked-doc leakage of raw data** | C8-FR-3 / NFR-4 / §10: fail-closed sanitizer parity-or-stricter; poisoned-fixture tests; `eval/hygiene_check.py` staging gate. |
| **R5** | **Cross-regime comparison / deck change** | NFR-5: single-regime hard-refusal (exit 2); no deck change; no new regime; deck is regime-pinned by content hash. |
| **R6** | **Numeric `M` leakage** | NFR-7: no `M` in any Cycle-008 artifact; `M` belongs only to a future pre-registration record. |
| **R7** | **Rung-3 scope creep** (defining a target while defining the form) | C8-FR-6 / §11: form-only docs; freezes no candidate/threshold/`M`/`K`/`n`/regime/feature-family; opens no attempt. |
| **R8** | **Ledger / claim-ceiling drift** | C8-FR-8 / NFR-6: hashes pinned (`7da7e9a8…` / `3d99759b…`); validator writes nothing; no row; no ceiling move. |
| **R9** | **Overclaim beyond Rung 2** | NFR-8 / §12: forbidden words negated-only; diagnostics carry no ceiling; no strength/calibration/tournament/leaderboard implication. |
| **R10** | **Runtime-agent / FunSearch / RL / MCTS / deck-optimizer / dashboard creep** | §5/§6: lane closed; Cycle-008 builds instruments, not agents. |
| **R11** | **Diagnostic depends on absent local run dirs** | C8-FR-1.5 / C8-FR-7: acceptance via synthetic fixtures; prefer existing sealed runs; any fresh run is non-ceiling-bearing and justified. |
| **R12** | **`.claude/` / State-Zone pollution** | NFR-11: System Zone untouched; pre-existing dirt unstaged and uncleaned. |
| **R13** | **Local-vs-hosted divergence misread as a result** | NFR-3 / blocked-family map: parity is an entry-point/legality property (`mirror_validate`); metric-level parity is documented as needing future work, not claimed. |

## 15. Operator decisions

This PRD encodes the decisions; OD-C8-3 is resolved this pass (per operator authorization), the rest are enumerated for
the operator to take at the stated time.

| ID | Decision | Status / When |
|---|---|---|
| **OD-C8-1 — Open Cycle-008 as a diagnostics + governance-hardening cycle only** | Open the cycle for the narrow diagnostics + D-lite governance work; broad optimization stays closed. | Operator act, before SDD |
| **OD-C8-2 — Authorize descriptive trace-safe aggregate diagnostics only** | Authorize the §9 "measurable now" descriptive surfaces; **withhold** authorization for any quality scoring or per-decision gameplay judgment (FM-03/04/06/08). | Operator act, before SDD |
| **OD-C8-3 — Rung-3 ladder semantics scope** | **RESOLVED (this pass): authorize a bounded docs-only Rung-3 ladder-semantics deliverable — comparison form only ("a future candidate must beat the current non-trivial incumbent under a same-regime, fresh-evidence, pre-registered comparison"); freeze no candidate / threshold / numeric `M` / `K`/`n` / regime id / target feature family; open no attempt.** | **Resolved** |
| **OD-C8-4 — No new regime / no deck change / no Rung-3 evidence** | Confirm Cycle-008 mints no regime, changes no deck, and generates no Rung-3 / promotion evidence. | Operator confirm, before SDD |
| **OD-C8-5 — Blocked families documented, not built** | Confirm the needs-instrumentation and requires-authorization families are documented as future candidates (G4 blocked-family map), not implemented now. | Operator confirm, before SDD |
| **OD-C8-6 — Build gate (OA-2-class)** | Open the build gate for the sanctioned code work (diagnostic + sanitizer + ledger-row validator + tests), scoped to `analysis/` / `tests/`. | After SDD / sprint-plan |

## 16. Success criteria

### 16.1 Planning-cycle success (this PRD)
- Accepted by the operator (Option A + D-lite) and proceeds to `/architect` (SDD), not directly to implementation.
- Grounded in the pre-PRD research and tracked authorities; clearly a **diagnostics + governance** cycle, not a Rung-3
  attempt and not agent-building; records the descriptive-only bound, the sanitization discipline, the blocked-family
  classification, and the bounded Rung-3 semantics scope.
- **Rung 2 held;** `docs/ledger.md` byte-unchanged (`7da7e9a8…`); `docs/claim-ceiling.md` unchanged; no raw data
  embedded; `.claude/` untouched; State-Zone files unstaged and uncleaned.

### 16.2 Deliverable success (concrete, testable — when the cycle runs in later sprints)
- **Diagnostic (C8-FR-1/2):** given a synthetic sealed-run fixture, emits the §9 descriptive surfaces; emits **no**
  quality/score/recommendation field (asserted absent); **refuses a mixed-regime fixture (exit 2)**; **imports no
  `sim`/`cabt`** (AST lint green); stdlib-only.
- **Sanitizer (C8-FR-3):** **rejects** each poisoned-fixture class (card name, raw decision row, inferential term,
  forbidden agent word, cross-regime field, non-SHA-256 hash, numeric-`M`-shaped token) with a fail-closed exit;
  **accepts** a clean fixture.
- **Ledger-row validator (C8-FR-4):** **rejects** a malformed row (wrong column count; empty `claim_ceiling`; edited
  past row; bad hash) and **accepts** the current valid `docs/ledger.md`; **writes nothing**.
- **Docs (C8-FR-5/6):** the Rung-3 semantics doc states the comparison **form only** and freezes nothing (asserted: no
  candidate / `M` / `K`/`n` / regime id / feature family); the blocked-family map is present and classified; the
  numbering and ledger-column conventions are written down.
- **Invariants (C8-FR-8):** ledger and claim-ceiling hashes unchanged; no ledger row; no ceiling movement; `.claude/`
  clean; State-Zone dirt unstaged.

### 16.3 Hard invariants (whole cycle)
`docs/ledger.md` byte-unchanged at `7da7e9a8…`; `docs/claim-ceiling.md` unchanged (Rung 2); the ledger remains the only
ceiling-bearing artifact; the diagnostic/sanitizer/validator/docs carry no ceiling of their own; no value promoted;
stdlib-only / analysis-offline imports; no new sim instrumentation; no per-decision quality scorer; no numeric `M`;
`.claude/` untouched; State-Zone dirt unstaged.

## 17. Sources and traceability

> **Local decision input (gitignored State Zone, not a tracked dependency):**
> `grimoires/loa/a2a/cycle-008/00-pre-prd-research.md` (the Cycle-008 pre-PRD research; recommends **Option A + D-lite**,
> accepted by the operator for this pass; current-state audit; triple-constraint feature matrix; existing-tooling
> assessment; candidate-target assessment; risk register; forbidden scope).
> **Tracked governance authorities:** `docs/claim-ceiling.md` (standing ceiling Rung 2; forbidden words; never compare
> across regimes); `docs/ledger.md` (the only ceiling-bearing artifact; 18-column schema; three rows incl. the Rung-2
> `regime-v003` row); `docs/cycles/cycle-007/07-closeout.md` (Rung-2 closeout of record; carry-forwards 1–4; final
> hashes); `docs/operator/turntrace-loop-contract.md` (§1 loop; §6 OA-2 build gate; §7-§8 hygiene / claim language);
> `docs/failure-modes.md` + `docs/failure-mode-taxonomy-v001.md` (FM-03/04/06/08 `detector: forbidden`; FM-07
> computable-now; FM-10/FM-11); `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` (SP-6 / SP-8 / SP-9; OA-2);
> `docs/operator/deferred-lane-gate-after-sprint-01.md` (narrow-planning lane open; trace-safe aggregate diagnostics
> allowed; broad optimization closed).
> **Tracked frozen authorities:** `frozen/README.md` (regime = `{seed_set, opponent_pool, deck_pool, metrics_spec}`;
> a new version is a new file; deck pinned by hash); `frozen/regimes/regime-v003.json` (the Rung-2 regime);
> `frozen/metrics/metrics-spec-v001.json` (five correctness metrics; none of the scouting-family metrics present).
> **Tracked project framing:** `README.md` (architecture, zones, import direction, Rung-2 claim);
> `BUTTERFREEZONE.md` (standing, hard boundaries, evidence containment).
> **Tracked code (reality grounding, at `95d4811`):** `analysis/*` (aggregate / dispersion / delta_report /
> replay_check / failure_report / evidence_summary / e2e_validate — outcome/aggregate readers; only `replay_check`
> reads sidecars, opaquely); `eval/run_match.py` (records the trace; agent invoked with counts only),
> `eval/run_eval.py`, `eval/validate.py`, `eval/hygiene_check.py`, `eval/mirror_validate.py`, `eval/schemas.md`
> (trace schema authority); `sim/adapter.py` (observation views: counts/booleans/OptionType tokens, no energy/no
> per-Pokémon); `agents/runtime/scripted_baseline.py` (the current incumbent); `tests/test_import_direction.py`,
> `tests/test_evidence_summary.py`, `tests/test_smokes.py`.
> Current main at authoring: `95d4811`. Claim ceiling: **Rung 2 (unchanged).** This PRD opens no implementation gate,
> builds no code, generates no evidence, runs no eval, chooses no `M`, selects no candidate, opens no Rung-3 attempt,
> issues no SP-6, promotes no value, writes no ledger row, advances no ceiling, mutates no ledger, and edits no
> `.claude/`.

---

> **PRD statement (binding).** Cycle-008 is a **diagnostics + governance-hardening cycle** (research Option A spine +
> bounded D-lite rider). **Rung 2 holds at cycle open and is preserved** — narrowly bounded to `scripted-v001` beating
> `random_legal-v001` under `regime-v003`. Cycle-008 builds **trace-safe, descriptive, same-regime diagnostic eyes** (a
> new bounded `analysis/` module over existing sealed runs, with a fail-closed output sanitizer), a **ledger-row
> validator**, and **governance/convention docs** including a **bounded docs-only Rung-3 ladder-semantics** definition
> that states the comparison *form only* and freezes nothing. The diagnostic is **descriptive-only** — it says what
> happened and never judges play quality, scores a decision, or recommends a move. **Cycle-008 attempts no Rung 3,
> selects no target, freezes no candidate / numeric `M` / `K` / `n` / regime id / feature family, adds no simulator
> instrumentation, builds no per-decision quality scorer for FM-03/04/06/08, builds no runtime agent or
> optimization/search/learning surface, generates no promotion evidence, issues no SP-6, writes no ledger row, and
> advances no ceiling.** Scouting signals are hypotheses only (FM-11), never proof; same-regime / same-deck /
> same-opponent-pool discipline is preserved; existing sealed runs are preferred and any fresh run is explicitly
> non-ceiling-bearing. **This drafting pass built no code, generated no evidence, chose no `M`, selected no candidate,
> and took no terminal act.** `docs/ledger.md` remains byte-unchanged at `7da7e9a8dbed6561669d1569445eb9fe67a953fb`;
> `docs/claim-ceiling.md` is unchanged at `3d99759b919f7d75bc41ea81cd82e5f1fb974be7`.
