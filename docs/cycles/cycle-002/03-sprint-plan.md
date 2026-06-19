# Cycle-002 Sprint Plan — Evaluation Scale + Comparison Confidence

> Planning artifact (Sprint Plan). Status: **DRAFT — research/planning only.** This document opens **NO build gate.**
> Implementation of build-gated sprints requires a separate, explicit operator build-gate action (OA-2 equivalent)
> per `docs/operator/turntrace-loop-contract.md` §6. This Sprint Plan creates no `/implement` prompt and authorizes no code.
> Binding inputs: `docs/cycles/cycle-002/01-prd.md` (accepted PRD) and `docs/cycles/cycle-002/02-sdd.md` (accepted,
> HITL-reviewed SDD). Supporting: `docs/cycles/cycle-002/00-research-and-planning.md`.
> Sanitized note. No raw traces, card IDs/names, deck lists, simulator logs, PDFs/CSVs, or Competition Data appear
> here (CC-1/CC-2, ESP). Runs are referenced by `run_id`, hashes, sanitized metrics, claim ceilings, and local
> path/status only. The forbidden agent claim words (*strong / competitive / optimal / calibrated / complete*)
> appear only as negated/forbidden language.

| Field | Value |
|---|---|
| **Cycle** | Cycle-002 |
| **Working title** | Evaluation Scale + Comparison Confidence |
| **Type** | Sprint Plan (planning artifact, not a build artifact) |
| **Status** | DRAFT — awaiting operator acceptance; next Golden-Path step for build sprints is the build gate (OA-2), not implementation now |
| **Date** | 2026-06-18 |
| **Current main** | `bd28f84` — *docs: add TurnTrace Cycle-002 SDD* (local) |
| **Posture** | Improve the EVALUATION HARNESS, not the agent |
| **Claim ceiling** | Rung 1 (unchanged; not raised) |
| **Shape** | 3 sprints (operator-ratified, review 2026-06-18) |

## 1. Sprint-cycle objective

Translate the accepted PRD and SDD into an implementation-ready, **three-sprint** plan that — **when a build gate is
later opened** — stands up a stable, sanitized, larger same-regime evaluation harness under an additive
`regime-v002`, runs repeated same-regime batches cheaply, and reports observed dispersion descriptively — with the
runtime agents **frozen**, every claim bounded to **Rung 1**, `docs/ledger.md` preserved as the only ceiling-bearing
artifact, and no cross-regime comparison (`01-prd.md:56-59`; `02-sdd.md:30-33`).

The spine is **D → A → C/B**, with **G** binding throughout and **E/F** as docs/criteria only:

| Lane | Sprint | C2-FR | Net-new build surface |
|---|---|---|---|
| **E/F/G** — criteria/repro/discipline docs | **Sprint 00** | C2-FR-5, C2-FR-6, C2-FR-7 | None (docs only) |
| **D** — cost/runtime budget first | **Sprint 01** | C2-FR-1 | None new — a measurement *use* of `eval/run_eval.py` |
| **A** — scale via additive `regime-v002` | **Sprint 01** | C2-FR-2 | Two additive **frozen** files |
| **C** — repeated same-regime batches | **Sprint 02** | C2-FR-3 | At most a thin runner (Stretch); else reuse `run_eval` |
| **B + reporting** — descriptive dispersion | **Sprint 02** | C2-FR-4 | One offline `analysis/dispersion_report.py` module |

**The entire net-new code surface of Cycle-002 is two additive things** (`02-sdd.md:55-57`): (1) additive frozen
`regime-v002` files, and (2) one offline cross-run descriptive-dispersion module. Everything else is reuse of existing
harness mechanics or docs.

## 2. Posture and gates (binding)

```
This Sprint Plan opens no build gate.
Implementation of Sprint 01 / Sprint 02 requires a later explicit operator OA-2 / build-gate action.
Cycle-002 improves evaluation scale and comparison confidence, not runtime-agent strength.
Broad optimization remains closed.
The runtime-agent improvement lane remains closed.
The claim ceiling remains Rung 1 until an explicit later operator decision earns otherwise.
```

- **Improve the evaluation harness, not the agent.** No rule/heuristic/scoring change to `agents/runtime/`; the
  agents (`random_legal`, `scripted_baseline`) are **frozen inputs**, never targets (`02-sdd.md:124,152`; PRD NG1).
- **Broad optimization stays closed.** Every "Still closed" item (`docs/operator/deferred-lane-gate-after-sprint-01.md:71-87`)
  remains closed and requires a separate, explicit operator decision. This Sprint Plan opens none.
- **Claim ceiling held at Rung 1.** No task raises it; `docs/ledger.md` remains the only ceiling-bearing artifact
  (`docs/claim-ceiling.md:5-6`).
- **Build gate (OA-2) is the single hard procedural gate** for build sprints. Planning artifacts — including this
  Sprint Plan — never open the gate (loop contract §6).

### 2.1 Docs sprint vs build sprints (the procedural firebreak)

The 3-sprint shape draws a clean line between the **docs-only** lane and the **build-gated** lanes:

- **Sprint 00 is docs-only and opens no OA-2 build gate** — but it still runs the **normal Loa sprint cadence**:
  `/implement → /review-sprint → /audit-sprint → explicit operator acceptance/closeout`. Its deliverables
  (C2-FR-5/6/7) are sanitized **tracked docs only** (no app code, no `frozen/` files, no runs, no build-gated paths),
  so no OA-2 is required; the cadence is run for **quality**, not because BUILD work is authorized. Review/audit MUST
  check: no forbidden affirmative claim words; no card names / card IDs / deck contents / simulator logs / raw trace
  material; `eval/hygiene_check.py` passes; no build-gated paths touched; nothing under `.claude/`, `.beads/`,
  `grimoires/loa/a2a/`, `runs/`, or `docs/ledger.md` staged. (Operator workflow decision, review 2026-06-18: even
  docs-only sprints get review/audit, because prior review caught sensitive/token issues before task completion.)
- **Sprint 01 and Sprint 02 are build-gated.** They write App-Zone artifacts (`frozen/`, `analysis/`, `tests/`) and
  run evaluations, so each lands **only** through `/implement → /review-sprint → /audit-sprint` after a separate
  explicit OA-2, integrated fast-forward only (loop contract §1-§3).

## 3. Sprint shape (operator-ratified)

**3 sprints (ratified, review 2026-06-18):**

| Sprint | Title | Gate | Lane(s) | Class summary |
|---|---|---|---|---|
| **Sprint 00** | Criteria / Posture / Sprint Readiness | **No OA-2 gate** (docs-only; normal review/audit cadence) | E, F, G | All Core docs |
| **Sprint 01** | Scale Foundation | **Build-gated (OA-2)** | D, A | Core build + proofs |
| **Sprint 02** | Repeated Batch + Dispersion Report | **Build-gated (OA-2)** | C, B | Core build + 2 Stretch |

**Why 3 over 2 (ratified):** it puts a procedural firebreak between the docs-only lane (Sprint 00 opens no OA-2 gate and closes via the normal
implement→review→audit→acceptance cadence) and the build-gated lanes, and sequences the spine exactly **D→A→C/B** — Sprint 01 does **D** (budget) +
**A** (regime) and its dry-run output (`N`) feeds Sprint 02's **C/B**, preserving the "know the cost *before* committing
to K" ordering that risk R6 depends on. A one-sprint plan is rejected: it would fold regime authoring, 2K batch runs, a
new analysis module, and all docs into a single LARGE unit, erasing the D→A→C/B ordering.

## 4. Core vs Stretch (operator-ratified)

- **Core:** docs-only criteria/repro/ledger-discipline notes (S00) · additive `seed-set-v002.json` + `regime-v002.json`
  (S01) · dry-run budget procedure/note (S01) · 2K run-dir model (S02) · `analysis/dispersion_report.py` (S02) ·
  single-regime refusal exit 2 (S02) · descriptive-only output `min/max/range/mean/median/spread/count` (S02) ·
  sanitization + import-boundary tests (S02).
- **Stretch:** paired-delta dispersion (candidate−baseline within each pair, then the spread of that delta across K
  pairs) · thin `eval/run_batch.py` wrapper (**only if** the chosen K makes manual 2K invocation a real risk; loop-only,
  no eval semantics) · tracked sanitized cycle-close summary (**only on** explicit operator SP-6 relaxation).

## 5. SDD-ratified defaults carried (Checkpoint 3)

All ratified in SDD §14 / §7.4 / §6.1 (operator review 2026-06-18) and carried verbatim into this plan:

| Default | Value |
|---|---|
| Allowed statistics | `min, max, range, mean, median, spread, count` only |
| Std dev / variance | **Excluded** in Cycle-002 (descriptive but deliberately omitted for the bright line) |
| Inferential statistics | **Forbidden** — no CIs, p-values, "significant," hypothesis tests, inferential error bars |
| Batch model | K paired comparisons = **2K** sealed run dirs |
| Run IDs | `run-v002-b-<i>` (baseline) / `run-v002-c-<i>` (candidate) |
| ID authority | `manifest.json` is authority for `regime_id`/`agent_id`/metadata; run-id is human-readable convenience only |
| Batch runner | **C-i** (manual `run_eval` ×2K) default; **C-ii** thin wrapper only if K justifies, loop-only |
| Component reuse | `regime-v002` reuses opponent/deck/metrics-v001 by reference + hash; **only the seed-set changes** |
| `regime-v001` | Byte-unchanged; `regime-v002` is additive future build work, not already existing |
| Ledger | Scale/batch runs non-deliverable by default → no ledger row; `docs/ledger.md` only ceiling-bearer |
| Storage | Full run dirs + dispersion reports local/git-ignored by default |
| Sample size `N` | **Not fixed by this plan** — an output of the Sprint-01 dry-run (OD-4); schema fixed, number is data |

## 6. Sprint 00 — Criteria / Posture / Sprint Readiness (docs-only, NO build gate)

**Posture:** docs-only; opens **no OA-2 build gate**; touches **tracked docs only** (no app code, no `frozen/` files, no
run dirs, no ledger changes, no build-gated paths). Still runs the **normal Loa sprint cadence** — `/implement →
/review-sprint → /audit-sprint → explicit operator acceptance/closeout` — for quality, not because BUILD work is
authorized. Independent of Sprint 01/02 (may run first or in parallel).

| Task | C2-FR / Lane | Title | Output (tracked) |
|---|---|---|---|
| **S00-T1** | C2-FR-5 / E | Rung 2 readiness criteria | `docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` |
| **S00-T2** | C2-FR-6 / F | Reproducibility-reality note | `docs/cycles/cycle-002/05-reproducibility-reality.md` |
| **S00-T3** | C2-FR-7 / G | Ledger / report-discipline note | `docs/cycles/cycle-002/06-ledger-report-discipline.md` |
| **S00-T4** | (readiness) | Operator-decision register + OA-2 readiness checklist | `docs/cycles/cycle-002/07-operator-decision-register.md` |

### S00-T1 — Rung 2 readiness criteria (Core, docs) → [G6]
State what a future Rung 2 *consideration* would minimally require (SDD §9.1; `01-prd.md` C2-FR-5): (1) a same-regime
baseline-vs-candidate comparison at a justified larger `n` under one regime; (2) an explicitly **designed and
operator-approved** inferential procedure; (3) the candidate exceeding the random-legal baseline by a **pre-registered
margin** under that design; (4) provenance + audit-trail intact; (5) a deliberate operator-authorized advance of the
ledger row's `claim_ceiling`. The doc **explicitly does not claim Rung 2** (Rung 2 = "beats random-legal,"
`docs/cycles/cycle-000-bootstrap/01-turntrace-prd.md:274-276`) and records that the inferential design + ceiling advance
is a separate operator decision. No forbidden claim words except negated.

### S00-T2 — Reproducibility-reality note (Core, docs) → [G7]
Per SDD §9.2: (a) confirm/record `seed_controlled=false` (`docs/claim-ceiling.md:42-52`); (b) define "stable" at the
larger `n` as **distribution-stable + audit-trail** (not byte-identical); (c) document that, because runs are unseeded,
observed dispersion **conflates agent behavior with uncontrolled simulator RNG and cannot be separated** into an isolated
"agent variance" without seed control (research RQ-8). No manufactured seed control; byte-identical replay stays a future
upgrade only if seed control is later proven.

### S00-T3 — Ledger / report-discipline note (Core, docs) → [G8]
Per SDD §8/§9.3: codify that non-deliverable scale/variance runs write **no** ledger row (the shipped default); the
ledger does **not** grow a row per batch; only an explicitly designated deliverable run may write a row; larger-run
reports stay local/ignored unless operator-approved (SP-6). Docs/policy only — codifies existing behavior, requires no
code change.

### S00-T4 — Operator-decision register + OA-2 readiness checklist (Core, docs) → [G all]
A tracked register of the Cycle-002 build assumptions and their ratified dispositions (SDD §14 OD-1..OD-9 + the three
review forks OD-6/OD-B1/OD-B3), plus a checklist of what must hold before the operator opens OA-2 for Sprint 01/02
(scope confirmed, agents frozen, sanitization gate active, `N`/K to be set from the dry-run, etc.). No decision is
silently opened by this register; it records, it does not authorize.

**Sprint 00 acceptance:** all four docs exist, tracked, sanitized; `eval/hygiene_check.py` passes on each; no forbidden
claim word except negated; no app code / `frozen/` / run dir / ledger change; Rung-1 language throughout; the Rung-2
doc claims no Rung 2.

**Sprint 00 review/audit gate (docs-focused, no OA-2).** `/review-sprint` + `/audit-sprint` run on the four docs and MUST
verify: (1) no forbidden affirmative claim word (only negated/forbidden language); (2) no card names / card IDs / deck
contents / simulator logs / raw trace material; (3) `eval/hygiene_check.py` passes on each tracked doc; (4) no
build-gated path touched (no `frozen/`, `analysis/`, `eval/`, `runs/`); (5) nothing under `.claude/`, `.beads/`,
`grimoires/loa/a2a/`, `runs/`, or `docs/ledger.md` is staged. Review/audit artifacts persist only to gitignored
`grimoires/loa/a2a/...`; the COMPLETED marker is created only after explicit operator closeout authorization. Sprint 00
opens **no** OA-2 build gate.

## 7. Sprint 01 — Scale Foundation (build-gated; requires OA-2)

**Posture:** build-gated; lands only through `/implement → /review-sprint → /audit-sprint` after OA-2. Produces the two
additive frozen files + the dry-run budget note + the byte-unchanged / no-ledger / guard proofs. No `agents/runtime/`
change.

| Task | C2-FR / Lane | Title | Class | Zone |
|---|---|---|---|---|
| **S01-T1** | C2-FR-1 / D | Dry-run budget procedure + sanitized local note; choose `N` + storage ceiling | Core | use of `eval/` + local note |
| **S01-T2** | C2-FR-2 / A | Additive `frozen/seeds/seed-set-v002.json` at chosen `N` | Core | App (`frozen/`) |
| **S01-T3** | C2-FR-2 / A | Additive `frozen/regimes/regime-v002.json` (tuple by ref+hash) | Core | App (`frozen/`) |
| **S01-T4** | C2-FR-2 | `regime-v001` byte-unchanged proof (test) | Core | tests |
| **S01-T5** | C2-FR-7 / G | No-ledger-by-default proof (test) | Core | tests |
| **S01-T6** | C2-FR-2 | Deck-drift + immutability guards still hold at scale (test) | Core | tests |

### S01-T1 — Dry-run budget + choose `N` (Core, Lane D) → [G2]
Measure **per-match wall-clock** and **per-run disk footprint** from a bounded local probe (re-run the existing harness;
the probe recorded ~80-190 matches/s, `frozen/seeds/seed-set-v001.json` `n_note`), extrapolate to candidate `N`, and
choose a **safe `N`** and a **storage ceiling** for the 2K batch. Emit a **sanitized local budget note** (time/size
numbers only — no run contents). Non-deliverable: bare `run_eval` writes `summary.csv` only, **no** ledger row
(`eval/run_eval.py:281-288,333-336`).

> **[Sprint Plan note — resolves the D↔A ordering]** `N` must be chosen *before* the frozen `seed-set-v002` is authored,
> but the dry-run needs a larger-`n` cost signal. Resolution: the dry-run measures per-match cost + per-run disk from a
> **local, throwaway** probe (the existing `regime-v001` n=12 run and/or a local non-frozen interim seed-set) and
> **extrapolates** to candidate `N`. The frozen `seed-set-v002` is authored **only after** `N` is fixed (S01-T2), so no
> frozen file is ever rewritten. Order within Sprint 01: **S01-T1 (budget → `N`) → S01-T2/T3 (author frozen files) →
> S01-T4/T5/T6 (proofs)**.
>
> **Interim-file safety (binding).** Any interim seed-set or probe file used for the dry-run MUST remain
> **local/git-ignored**: it is **not staged**, **not committed**, **not treated as frozen evidence**, and **not
> referenced as a durable regime component**. Only the final additive `frozen/seeds/seed-set-v002.json` and
> `frozen/regimes/regime-v002.json` become tracked (after Sprint 01 build approval). If an interim file cannot be kept
> safely local/ignored, the implementer MUST switch to another bounded local measurement method and **HALT before
> staging**.

### S01-T2 — `seed-set-v002.json` (Core, `frozen/`) → [G1]
Author an **additive** `frozen/seeds/seed-set-v002.json` per SDD §5.2: `seed_set_id: "seed-set-v002"`,
`mode: "unseeded"`, `seeds: null`, `match_indices` = a contiguous neutral list `1..N`, `n: N`. `N` from S01-T1. The
match-index list is **neutral** (no index chosen to flatter an agent) and the file is **hash-pinned before any agent
runs** (risk R2). Mirrors `seed-set-v001.json` schema exactly, changing only the scale.

### S01-T3 — `regime-v002.json` (Core, `frozen/`) → [G1]
Author an **additive** `frozen/regimes/regime-v002.json` per SDD §5.3: `regime_id: "regime-v002"`,
`seed_set: "seed-set-v002"`, and **reuse** `opponent_pool: "opponent-pool-v001"`, `deck_pool: "deck-pool-v001"`,
`metrics_spec: "metrics-spec-v001"` by reference (decision OD-3); `mode: "unseeded"`. Only the seed-set differs. The
`notes` field records: never compare to v001 rows (NFR-5); a component change is a new regime, never an edit.

### S01-T4 — `regime-v001` byte-unchanged proof (Core, tests) → [G7]
A test asserting `frozen/regimes/regime-v001.json` and its four component files (`seed-set-v001`, `opponent-pool-v001`,
`deck-pool-v001`, `metrics-spec-v001`) are **byte-identical** before/after Sprint 01 (SDD §12; NG7). `regime-v002`
references the three reused components by id, and a `regime-v002` run's `hashes.txt` records their content hashes
(`eval/run_eval.py:239-243`) — provable reuse without re-minting.

### S01-T5 — No-ledger-by-default proof (Core, tests) → [G8]
A test asserting a bare/non-deliverable `run_eval` invocation against `regime-v002` appends **no** row to a **redirected
test ledger** (never the tracked `docs/ledger.md`) while still writing `summary.csv` (`eval/run_eval.py:281-288`). This is
the shipped default; the test pins it for the larger regime.

### S01-T6 — Guards hold at scale (Core, tests) → [G7]
A test asserting the deck-drift guard (`eval/run_eval.py:128-134`) and the immutability guard (exit 3;
`eval/run_eval.py:138-154`) operate unchanged at the larger `N` under `regime-v002`. Because `regime-v002` reuses
`deck-pool-v001`, a changed live deck still (correctly) refuses the run. No guard is modified.

**Sprint 01 acceptance:** see §11 AC table (AC-S01-*).

## 8. Sprint 02 — Repeated Batch + Dispersion Report (build-gated; requires OA-2)

**Posture:** build-gated; lands only through `/implement → /review-sprint → /audit-sprint` after OA-2. Depends on
Sprint 01 (needs `regime-v002` + the chosen `N`). Produces the 2K run dirs (local) + the offline dispersion module.

| Task | C2-FR / Lane | Title | Class | Zone |
|---|---|---|---|---|
| **S02-T1** | C2-FR-3 / C | Repeated same-regime batches → 2K sealed run dirs (C-i) | Core | use of `eval/` → `runs/` (local) |
| **S02-T2** | C2-FR-4 / B | `analysis/dispersion_report.py` (descriptive dispersion; single-regime guard; Rung-1 footer) | Core | App (`analysis/`) |
| **S02-T3** | C2-FR-4 | Dispersion-report tests (single-regime exit 2; descriptive-only; import boundary; sanitization) | Core | tests |
| **S02-T4** | C2-FR-4 | Paired-delta dispersion | **Stretch** | App (`analysis/`) |
| **S02-T5** | C2-FR-3 | Thin `eval/run_batch.py` wrapper (only if K justifies; loop-only) | **Stretch** | App (`eval/`) |
| **S02-T6** | all ACs | End-to-end goal validation (AC sweep, no new code) | Core | docs |

### S02-T1 — Repeated batches → 2K run dirs (Core, Lane C) → [G3]
Run K **paired** comparisons under one `regime-v002`: for `i ∈ {1..K}`, one baseline run (`random_legal`, id
`run-v002-b-<i>`) and one candidate run (`scripted_baseline`, id `run-v002-c-<i>`), all sharing `regime_id =
regime-v002` (SDD §6.1). Total = **2K** sealed immutable run dirs, **local/git-ignored** (ESP-1). **Non-deliverable** —
no `--deliverable`/`--ledger`, so no ledger row (SDD §8.1). Default mechanism is **C-i** (manual `run_eval` ×2K); the
per-`run_id` immutability guard + idempotency carry the discipline (`eval/run_eval.py:138-154`). `K` from OD-4 (informed
by the S01 dry-run). `manifest.json` is the authority for `regime_id`/`agent_id`; the descriptive run-id is convenience
only (SDD §6.1).

### S02-T2 — `analysis/dispersion_report.py` (Core, `analysis/`) → [G4]
New offline module per SDD §7. **Reads only** each run dir's `manifest.json` + `match_results/*.json` (never
`traces/*.jsonl`, never error-string bodies). Per-run stats via `aggregate.aggregate_run()` (intra-`analysis/` reuse).
**Output:** per metric, across the K runs of an agent, the **`min`, `max`, `range`, `mean`, `median`, `spread`** — each
carrying `n`, `K`, `regime_id` + a Rung-1 footer and **no ceiling of its own**. **Descriptive only** — the module
**computes no** std dev/variance, CIs, p-values, "significant," hypothesis tests, or inferential error bars; their
absence is **structural, not prose** (SDD §7.4). CLI: `dispersion_report.py <run_dir>... [--json] [--out <local-path>]`;
exit `0` ok · `1` input failure · `2` mixed-regime refusal. Output **local/git-ignored by default** (`--out` is local;
SDD §7.5). **Imports:** stdlib + intra-`analysis/` `import aggregate` only; **never** `eval/`, `sim/`, `cabt`,
`agents/runtime/` (SDD §6.3).

### S02-T3 — Dispersion-report tests (Core, tests) → [G4, G7]
Tests pinning: (a) **single-regime guard** — mixed `regime_id` inputs → **exit 2**; uniform `regime-v002` inputs →
exit 0 (SDD §7.3, structurally mirroring `delta_report`'s `CrossRegimeRefusal`); (b) **descriptive-only** — the rendered
report contains range/mean/median/spread and **none** of {std dev, variance, confidence interval, p-value, significant,
hypothesis, error bar}; (c) **import boundary** — static check that the module imports none of `eval`/`sim`/`cabt`/
`agents/runtime` (intra-`analysis/` `import aggregate` allowed), added to the lint's scanned set; (d) **sanitization** —
no raw rows / card IDs / deck lists in output; `eval/hygiene_check.py --paths <report>` → exit 0; (e) **missing input** —
empty/missing `match_results` → exit 1. Synthetic fixtures only (no Competition Data); any randomized fixture sets a
fixed seed (test-harness determinism only — not simulator seed control).

### S02-T4 — Paired-delta dispersion (Stretch, `analysis/`) → [G4]
Within each pair `i`, compute candidate−baseline for a metric, then report the **dispersion of that delta across the K
pairs** (range/mean/median/spread). **Descriptive only** — a paired-delta spread is still observed spread, never an
inferential or strength claim, framed by the unseeded-process caveat (SDD §6.2). Include only if S02-T1..T3 land with
capacity remaining.

### S02-T5 — Thin `eval/run_batch.py` wrapper (Stretch, `eval/`) → [G3]
**Scope guard (binding):** `eval/run_batch.py` is **Stretch only** and **must not become Core** in Sprint 02 unless the
operator explicitly amends the sprint scope **after `K` is chosen**. **C-i** (manual `run_eval` ×2K) remains the **Core
default**. Authorize C-ii **only if** the chosen K makes 2K manual invocations a meaningful operator risk (OD-B1). It is
a **loop only** around `run_eval.run_eval()` over a generated `run_id` list for one `regime-v002`: **no** new evaluation
semantics,
**no** agent logic, **no** ledger-by-default (`write_ledger` stays False), **no** runtime/`sim` change, **no**
claim-ceiling movement; it refuses any non-`regime-v002` input.

### S02-T6 — End-to-end goal validation (Core, docs) → [all goals]
After S02-T1..T3 land, sweep the cycle's goals/ACs and record evidence in the tracked **sprint-scoped** report
`docs/cycles/cycle-002/sprint-02-implementation-report.md` (no generic `implementation-report.md`, no overwrite-prone
generic path); no new code. No goal marked achieved without evidence; claim ceiling re-verified Rung 1; hygiene clean;
no cross-regime comparison anywhere.

**Sprint 02 acceptance:** see §11 AC table (AC-S02-*).

## 9. Task ordering / dependency graph

```
Sprint 00 (docs-only, no gate) ── independent ── can land on operator acceptance
   S00-T1 (Rung-2 criteria) · S00-T2 (repro) · S00-T3 (ledger discipline) · S00-T4 (decision register/checklist)

Sprint 01 (build-gated, needs OA-2)
   S01-T1 (dry-run budget → choose N)
        │  N feeds the frozen seed-set
        ▼
   S01-T2 (seed-set-v002) ──▶ S01-T3 (regime-v002)
        │                          │
        ▼                          ▼
   S01-T4 (v001 byte-unchanged) · S01-T5 (no-ledger proof) · S01-T6 (guards hold)
        │  regime-v002 + N
        ▼
Sprint 02 (build-gated, needs OA-2)
   S02-T1 (2K paired batches → 2K local run dirs)
        │  2K sealed run dirs
        ▼
   S02-T2 (dispersion_report.py) ──▶ S02-T3 (dispersion tests)
        ├─▶ S02-T4 (paired-delta dispersion — Stretch)
        └─▶ S02-T5 (thin run_batch wrapper — Stretch, only if K justifies)
        ▼
   S02-T6 (E2E goal validation — last)
```

- **Sprint 00** is independent (docs-only) — may be authored first or in parallel with Sprint 01 planning; it opens no
  gate and lands on acceptance.
- **Sprint 01** must precede **Sprint 02** (Sprint 02 needs `regime-v002` + the chosen `N`).
- Within Sprint 01, **S01-T1 (budget→N) precedes S01-T2/T3 (frozen files)** so no frozen file is rewritten.
- No `agents/runtime/` change appears anywhere in the graph.

## 10. File authorization matrix

**Authorized for a future `/implement` ONLY (per sprint; no other path may be touched):**

| Path | Sprint / Task | Action | Zone |
|---|---|---|---|
| `docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` | S00-T1 | create | docs (tracked) |
| `docs/cycles/cycle-002/05-reproducibility-reality.md` | S00-T2 | create | docs (tracked) |
| `docs/cycles/cycle-002/06-ledger-report-discipline.md` | S00-T3 | create | docs (tracked) |
| `docs/cycles/cycle-002/07-operator-decision-register.md` | S00-T4 | create | docs (tracked) |
| `frozen/seeds/seed-set-v002.json` | S01-T2 | **create (additive)** | App (`frozen/`) |
| `frozen/regimes/regime-v002.json` | S01-T3 | **create (additive)** | App (`frozen/`) |
| `tests/test_smokes.py` (or `tests/test_import_direction.py`) | S01-T4/T5/T6, S02-T3 | create/edit test classes | tests |
| `analysis/dispersion_report.py` | S02-T2 (+T4 Stretch) | create | App (`analysis/`) |
| `eval/run_batch.py` | S02-T5 (Stretch only) | create (loop-only) | App (`eval/`) |
| a Sprint-01 budget note (local) | S01-T1 | create | **local / git-ignored** |
| `docs/cycles/cycle-002/sprint-00-implementation-report.md` | S00 closeout | create | docs (tracked) |
| `docs/cycles/cycle-002/sprint-01-implementation-report.md` | S01 closeout | create | docs (tracked) |
| `docs/cycles/cycle-002/sprint-02-implementation-report.md` | S02-T6 / closeout | create | docs (tracked) |

**Explicitly FORBIDDEN to touch (any sprint, any task):**

| Path | Why |
|---|---|
| `agents/runtime/` | No runtime-agent behavior change (NG1). Frozen inputs. |
| `frozen/regimes/regime-v001.json` + its four components (`seed-set-v001`, `opponent-pool-v001`, `deck-pool-v001`, `metrics-spec-v001`) | **Byte-unchanged** — a component change is a new regime, never an edit (NG7; `docs/claim-ceiling.md:29-35`). `regime-v002` is **additive**. |
| `eval/run_eval.py`, `analysis/aggregate.py`, `analysis/delta_report.py`, `analysis/failure_report.py`, `analysis/replay_check.py`, `eval/hygiene_check.py` | Reused **unchanged** as design inputs; no edit designed in Cycle-002. |
| `runs/` (tracked) | Only `runs/.gitkeep` tracked; the 2K run dirs stay **local/git-ignored** (ESP-1). |
| `docs/ledger.md` | **No row per batch.** Scale/batch runs are non-deliverable; only an explicitly designated deliverable run may write a row (none in scope). The only ceiling-bearing artifact. |
| `cg/`, `deck.csv`, `grimoires/loa/context/` | Competition Data — never committed/read into tracked artifacts (CC-1/CC-2). |
| `grimoires/loa/a2a/` | Review/audit/COMPLETED markers persist here (gitignored), orchestrator-written after the pure-review skills return — never by `/implement`. |
| `.claude/` | System Zone — never edited. |
| `.beads/` | Not Cycle-002 build scope (OD-9); `.beads/issues.jsonl` stays unstaged. |

**Implementation-report path rule (binding).** Each sprint's implementation report uses an explicit **sprint-scoped,
cycle-scoped** tracked path — `docs/cycles/cycle-002/sprint-00-implementation-report.md`,
`docs/cycles/cycle-002/sprint-01-implementation-report.md`, `docs/cycles/cycle-002/sprint-02-implementation-report.md`.
**No generic `implementation-report.md`** and no overwrite-prone generic artifact path is permitted; reports are
sprint-scoped and cycle-scoped. Review/audit artifacts (engineer-feedback, auditor-sprint-feedback) and the COMPLETED
marker live **only** in gitignored `grimoires/loa/a2a/...` and are never tracked; the COMPLETED marker is created only
after explicit operator closeout authorization.

## 11. Acceptance criteria

All bounded to Rung 1; all forbid agent strengthening; all forbid cross-regime comparison and inferential statistics.

### Sprint 00 (docs-only)

| AC | Theme | Task | Validation | Stop condition |
|---|---|---|---|---|
| **AC-S00-1** | Criteria honesty | S00-T1 | Rung-2 doc states criteria, claims **no** Rung 2; names the inferential-design + ceiling-advance as a separate decision | The doc claims or implies Rung 2, or omits the separate-decision boundary → HALT |
| **AC-S00-2** | Repro honesty | S00-T2 | Confirms `seed_controlled=false`; defines "stable" = distribution-stable + audit-trail; records the unseeded agent-vs-RNG caveat; no manufactured seed control | A byte-identical/determinism claim or manufactured seed control appears → HALT |
| **AC-S00-3** | Ledger discipline | S00-T3 | Records: no row per batch; deliverable-only rows; reports local/ignored unless SP-6 | The note authorizes a row per batch or a tracked report by default → HALT |
| **AC-S00-4** | Readiness | S00-T4 | Register lists ratified ODs; OA-2 checklist present; no decision silently opened | The register opens a "Still closed" lane or a build gate → HALT |
| **AC-S00-5** | Docs hygiene | all S00 | `eval/hygiene_check.py` passes on each doc; forbidden words only negated; no app code/`frozen/`/run dir/ledger change | Any Competition-Data token, forbidden affirmative claim word, or non-docs change → HALT |

### Sprint 01 (build-gated)

| AC | Theme | Task | Validation | Stop condition |
|---|---|---|---|---|
| **AC-S01-1** | Budget chosen safely | S01-T1 | Sanitized **local** budget note records wall-clock + disk + a safe `N` + storage ceiling; dry-run wrote **no** ledger row; outputs local/ignored | The budget note is tracked with run contents, or a ledger row was written → HALT |
| **AC-S01-2** | Additive regime | S01-T2/T3 | `seed-set-v002` + `regime-v002` exist as **additive** files (`mode=unseeded`, `seeds=null`, `match_indices` len == `N`); only the seed-set differs; reuse opponent/deck/metrics by ref | A frozen v001 component is edited, or `regime-v002` re-mints a reused component without authorization → HALT |
| **AC-S01-3** | v001 byte-unchanged | S01-T4 | Test asserts `regime-v001.json` + its 4 components byte-identical before/after | Any v001 component differs by one byte → HALT |
| **AC-S01-4** | No ledger by default | S01-T5 | Bare/non-deliverable `run_eval` on `regime-v002` appends no row to a **redirected test** ledger; `summary.csv` still written | A non-deliverable run appends to `docs/ledger.md` (or any ledger by default) → HALT |
| **AC-S01-5** | Guards hold | S01-T6 | Deck-drift guard + immutability guard (exit 3) operate unchanged at the larger `N` | A guard is modified or fails to refuse a populated dir / drifted deck → HALT |
| **AC-S01-6** | Frozen, no agent change | all S01 | No `agents/runtime/` edit; `eval/run_eval.py` logic unchanged; hygiene clean on tracked frozen files | Any `agents/runtime/` or harness-logic change → HALT |

### Sprint 02 (build-gated)

| AC | Theme | Task | Validation | Stop condition |
|---|---|---|---|---|
| **AC-S02-1** | 2K local runs | S02-T1 | 2K sealed run dirs under one `regime-v002`, ids `run-v002-b/c-<i>`, **local/git-ignored**, **non-deliverable** (no ledger row); `manifest.json` authoritative | A run dir is tracked, a ledger row is written, or runs mix regimes → HALT |
| **AC-S02-2** | Descriptive dispersion | S02-T2 | Report emits `min/max/range/mean/median/spread/count` per metric with `n`/`K`/`regime_id` + Rung-1 footer; **no** std dev/variance; **no** inferential statistic | The module computes std dev/variance or any inferential statistic → HALT |
| **AC-S02-3** | Single-regime refusal | S02-T2/T3 | Mixed-`regime_id` inputs → **exit 2**; uniform `regime-v002` → exit 0; missing input → **exit 1** | The report aggregates across regimes, or fails to refuse mixed input → HALT |
| **AC-S02-4** | Import boundary | S02-T2/T3 | Static check: `dispersion_report.py` imports none of `eval`/`sim`/`cabt`/`agents/runtime`; intra-`analysis/` `import aggregate` allowed; module in the lint's scanned set | The module imports a forbidden zone, or escapes the import-direction lint → HALT |
| **AC-S02-5** | Sanitization | S02-T2/T3 | Reads only `manifest.json` + `match_results/*.json`; never `traces/*.jsonl`; output has no raw rows / card IDs / deck lists; `eval/hygiene_check.py` passes | Any raw trace row / card / deck token in output, or a `traces/` read → HALT |
| **AC-S02-6** | Populated-dir refusal | S02-T1 | Re-running into a populated run dir → **exit 3** through the unchanged `run_eval` immutability guard | The immutability guard is bypassed or modified → HALT |
| **AC-S02-7** | Stretch discipline | S02-T4/T5 | Paired-delta is descriptive-only; any `run_batch.py` is loop-only (no eval semantics/agent logic/ledger-by-default/runtime-sim change/ceiling movement) | A Stretch task adds eval semantics, an inferential stat, or a strength narrative → HALT |
| **AC-S02-8** | Goals met | S02-T6 | Tracked implementation report records evidence for every goal; Rung-1 re-verified; hygiene clean | A goal is marked achieved without evidence, or a claim exceeds Rung 1 → HALT |

### Cross-cutting (all sprints)

| AC | Theme | Validation | Stop condition |
|---|---|---|---|
| **AC-X1** | Claim ceiling held | No tracked artifact claims beyond Rung 1; `docs/ledger.md` stays the only ceiling-bearing artifact | Any artifact makes a claim beyond Rung 1, or a non-ledger artifact asserts a ceiling → HALT |
| **AC-X2** | No cross-regime | No tracked artifact places a `regime-v002` number beside a v001 ledger row as a comparison | Any cross-regime comparison appears → HALT |
| **AC-X3** | Loop discipline (all sprints) | S00/S01/S02 each land through `/implement → /review-sprint → /audit-sprint`; one review + one audit artifact each; no out-of-loop edits. Sprint 00 runs the cadence with **no OA-2** (docs-only); S01/S02 require OA-2 | Code lands outside `/implement`, or a COMPLETED marker appears without operator authorization → HALT |
| **AC-X4** | Forbidden words | The words *strong/competitive/optimal/calibrated/complete* appear only as negated/forbidden language across all changed tracked files | Any affirmative use → HALT |
| **AC-X5** | Review/audit storage | Review/audit/COMPLETED artifacts persist only to git-ignored `grimoires/loa/a2a/...` | Any review/audit artifact tracked or patching implementation → HALT |

## 12. Validation commands

**Always-run gates (every build task, before staging):**

```bash
python tests/test_import_direction.py        # offline/runtime separation (dispersion_report auto-included)
python tests/test_smokes.py                  # stdlib unittest suite; new/edited classes live here
python eval/hygiene_check.py --paths <changed tracked files>
```

**Planned targeted checks (build sprints):**

- `regime-v001` + 4 components byte-identical before/after (S01-T4)
- `seed-set-v002` schema: `mode==unseeded`, `seeds==null`, `len(match_indices)==N` (S01-T2)
- bare `run_eval` on `regime-v002` writes **no** ledger row (redirected test ledger), still writes `summary.csv` (S01-T5)
- deck-drift + immutability (exit 3) guards unchanged at scale (S01-T6)
- dispersion report: mixed-regime → exit 2; uniform `regime-v002` → exit 0; missing input → exit 1 (S02-T3)
- dispersion report descriptive-only: contains range/mean/median/spread; contains **none** of {std dev, variance, CI, p-value, significant, hypothesis, error bar} (S02-T3)
- dispersion report import-boundary static check + lint-scanned-set assertion (S02-T3)
- dispersion report sanitization: no raw rows/card/deck tokens; `hygiene_check` exit 0; no `traces/` read (S02-T3)

> **No validation step may mutate `regime-v001` (or any v001 component), the tracked `docs/ledger.md`, or any sealed run
> dir.** Ledger-write tests use a temporary ledger path; tamper/flip fixtures copy into a tempdir first; randomized
> fixtures set a fixed seed (test-harness determinism only — never simulator seed control).

## 13. Review / audit expectations (all sprints)

Per the loop contract (§1-§3, §10), **every** Cycle-002 sprint — including the docs-only Sprint 00 — closes through
exactly **one `/review-sprint` artifact and one `/audit-sprint` artifact**; corrective changes re-enter only through
`/implement`. **Sprint 00 runs this cadence with no OA-2 build gate** (docs-only; the gate is required only for the
build sprints 01/02). Future review/audit MUST verify:

- implementation touched **only** the authorized paths (§10); no forbidden path edited
- **no runtime-agent behavior change** (no `agents/runtime/` edit; import-direction lint intact)
- **`regime-v001` byte-unchanged**; `regime-v002` additive only
- **no Competition Data or raw run data** in any tracked file (hygiene clean; no card/deck/trace tokens)
- **no `docs/ledger.md` mutation** — no non-deliverable run writes a row; no row per batch
- **dispersion report is descriptive-only** — no std dev/variance, no inferential statistic; single-regime guard (exit 2) intact
- **all run dirs local/ignored**; the dispersion report local by default
- **claim ceiling remains Rung 1**; the ledger remains the only ceiling-bearing artifact
- **no COMPLETED marker** until explicit operator closeout authorization

> Review/audit are pure-review skills: `Write`/`Edit` disabled inside them is **expected, not a failure**. The
> review/audit artifact is persisted by the orchestrator into `grimoires/loa/a2a/...` after the skill returns.

## 14. Evidence-storage and sanitization rules

Per loop contract §7 / ESP-1..ESP-5 / SP-6 and SDD §4.1:

- **Full run dirs stay local/git-ignored.** The 2K `runs/run-v002-*/` trees stay local; `hygiene_check.py` blocks
  `runs/<id>/...` paths. Only `runs/.gitkeep` is tracked.
- **Budget note + dispersion report are local/git-ignored by default.** Promotion of any sanitized summary to tracked
  status requires an explicit operator **SP-6 relaxation** at cycle close (Stretch); even then it carries
  counts/aggregates/dispersion only — never raw rows.
- **Tracked docs reference only** `run_id`, content hashes, sanitized metrics, aggregate categories, claim ceilings, and
  local path/status — never embedded raw values.
- **Forbidden in any tracked artifact:** raw traces, card IDs/names, deck lists, hand contents, simulator logs,
  PDFs/CSVs, `deck.csv` rows, Competition Data.
- **`requires-raw-data: cannot-surface`** — actual per-run distributions and run-dir file contents are not surfaced in
  any tracked artifact, including this Sprint Plan.

## 15. Claim-ceiling rules

- **Rung 1 remains the ceiling** for all Cycle-002 artifacts. No task raises it.
- **`docs/ledger.md` remains the only ceiling-bearing artifact** (`docs/claim-ceiling.md:5-6`). The dispersion report,
  budget note, criteria/repro/discipline docs, and this plan carry **no** ceiling — only a Rung-1 footer.
- **Allowed claim form** (descriptive, local, with `n`/`K`/`regime_id`): *"under `regime-v002` at n=N across K batches,
  the observed `<metric>` ranged from X to Y (mean Z)."*
- **No gameplay-strength, statistical-significance, cross-regime, or leaderboard claim** in any tracked output.
  Cross-regime is additionally hard-refused by the dispersion report's single-regime guard (exit 2).
- **Forbidden words** (`strong, competitive, optimal, calibrated, complete`) checked by grep across every changed tracked
  file (AC-X4); they may appear only as negated/forbidden language.

## 16. Risks / stop conditions

| # | Risk | Mitigation (plan-level) | Stop condition |
|---|------|---|---|
| R1 | Cross-regime contamination — v002 narrated against v001 n=12. | Dispersion report single-regime guard (exit 2); every report carries `regime-v002`+`n`+`K`; no v002 number beside a v001 row (AC-X2, AC-S02-3). | Any cross-regime comparison appears → HALT. |
| R2 | Accidental agent optimization — scale drifts into tuning / seed-shopping. | `agents/runtime/` frozen + unauthorized (§10); `regime-v002` seed-set contiguous, neutral, hash-pinned before any agent runs (S01-T2); review rejects any decision-logic touch. | A per-decision scorer or any `agents/runtime/` edit → HALT. |
| R3 | Confidence-language overreach — descriptive presented as inferential. | The dispersion module has **no inferential code path** (SDD §7.4); ratified vocabulary excludes std dev/variance; audit greps for forbidden/inferential terms; Rung-1 footer everywhere (AC-S02-2, AC-X4). | A std dev/variance/CI/p-value/"significant" appears in a tracked report → HALT. |
| R4 | Claim-ceiling inflation — larger-`n` win_rate movement read as "better." | Rung-1 hold as explicit AC (AC-X1); ledger stays sole ceiling-bearer; Rung 2 is criteria-only (S00-T1), never claimed; paired deltas reported as observed spread only. | Any artifact makes a claim beyond Rung 1 → HALT. |
| R5 | Competition-Data / raw-trace leakage at scale. | Roll-up restricted to coarse sanitized aggregate metrics; `traces/*.jsonl` never opened; `hygiene_check` active; reports local/ignored by default (AC-S02-5). | Any card/deck/trace token in a tracked output, or a `traces/` read → HALT. |
| R6 | Storage/cost surprise — many large batches exhaust disk / slow I/O. | S01-T1 dry-run measures wall-clock + disk and sets a safe `N` + storage ceiling **before** Sprint 02 commits to K (AC-S01-1). | The 2K batch is started without a budget note / chosen `N` → HALT. |
| R7 | Building before the gate — this plan misread as authorization. | This plan opens no build gate and creates no `/implement` prompt; S01/S02 require OA-2; the next step for build is the gate. | Any code patch before OA-2 → HALT (out-of-loop edit). |
| R8 | Unseeded variance misattribution — dispersion read as isolated agent variance. | S00-T2 repro note + an inline caveat in every dispersion report frame dispersion as the whole unseeded process (AC-S00-2). | A report presents dispersion as an isolated agent-variance estimate → HALT. |
| R9 | `regime-v001` mutation — larger seed-set written by editing v001. | S01-T2 authors **additive** files; S01-T4 byte-equality test; review verifies no `frozen/regime-v001` diff (AC-S01-3). | Any v001 component differs by one byte → HALT. |
| R10 | Manual 2K-invocation footgun — wrong `--run-id` / accidental `--deliverable`. | C-i default with the per-`run_id` immutability guard; **C-ii** thin wrapper authorized (S02-T5) if the chosen K makes manual runs a real risk (OD-B1). | A batch run writes a ledger row or collides a run-id → HALT. |
| R11 | A new `analysis/` module silently escapes the import-direction lint. | S02-T3 adds an assertion that `dispersion_report.py` is in the lint's scanned set with zero violations (AC-S02-4). | The lint does not cover the new module → HALT until the assertion is added. |

**Reproducibility / seeding (binding for tests).** Any test fixture generating randomized records MUST set and surface a
fixed random seed — a determinism requirement for the *test harness only*. It does **not** manufacture simulator seed
control (`sim/capabilities.json: seed_controlled=false` is unchanged). Real-run reproducibility stays `mode=unseeded` /
distribution-stable + audit-trail (`docs/claim-ceiling.md:42-52`).

## 17. Explicit out-of-scope (forbidden — mention only)

Opening any of these requires a separate, explicit operator decision that supersedes the standing notes:

**Broad optimization (still closed):** runtime-agent tuning · runtime-agent heuristic changes · any `agents/runtime/`
behavior change · RL · self-play · deck optimizer · value model · win-probability model · search/lookahead/MCTS · ELO ·
tournament system · multi-agent tournament comparisons · leaderboard optimization · Kaggle upload automation ·
submission packaging · dashboard · SaaS/product surface · two-direction ablation ledger.

**Claim / statistics boundaries:** per-decision agent-quality scoring/detectors · claim-ceiling upgrade ·
statistical-significance claims · cross-regime uplift · byte-identical determinism work while `seed_controlled=false` ·
**sample standard deviation or variance in Cycle-002 reports** · any inferential statistic (CIs, p-values, "significant,"
hypothesis tests, inferential error bars).

**Data / sanitization boundaries:** raw trace/card/deck/simulator-log exposure or emission into tracked artifacts;
committing card IDs/names, deck lists, hand contents, PDFs/CSVs, `deck.csv` rows, or run-dir dumps.

**Process / regime boundaries:** editing `.claude/`; editing `regime-v001` or any of its components (a larger seed-set is
a *new* `regime-v002` file, never an edit); comparing `regime-v002` numbers to v001 ledger rows; out-of-loop edits;
premature COMPLETED marker; any build before the operator opens OA-2.

## 18. Open decisions carried to the build gate

| ID | Decision | Disposition |
|---|---|---|
| **OD-1** | Open OA-2 for Sprint 01/02 | Required before any `/implement`/`/run`; this plan authorizes none |
| **OD-3** | `regime-v002` component reuse vs re-mint | **Ratified:** reuse opponent/deck/metrics-v001 by ref+hash; only seed-set changes (SDD §5.4) |
| **OD-4** | Target `N` and batch count `K` | **Output of the S01-T1 dry-run** — schema fixed, numbers data; not fixed by this plan |
| **OD-5** | Ledger-row policy for scale runs | **Ratified:** no row per batch; at most one designated deliverable run per regime (SDD §8.1) |
| **OD-6** | Allowed descriptive-statistics vocabulary | **Ratified:** `min/max/range/mean/median/spread/count`; std dev/variance + inferential excluded (SDD §7.4) |
| **OD-7** | Where the dispersion report lives | **Ratified:** local/git-ignored by default; tracked summary only on explicit SP-6 relaxation (SDD §4.1) |
| **OD-8** | Rung 2 stays criteria-only | **Ratified:** yes — S00-T1 defines criteria; Cycle-002 claims no Rung 2 (SDD §9.1) |
| **OD-B1** | Batch runner C-i vs C-ii | **Ratified:** C-i (manual) is the Core default; C-ii `run_batch.py` stays **Stretch only** — not Core unless the operator amends scope after K is chosen — and only if K makes 2K manual runs a meaningful risk; wrapper loop-only (SDD §3.3) |
| **OD-B3** | Run-id naming | **Ratified:** descriptive `run-v002-b/c-<i>`; `manifest.json` stays authority (SDD §6.1) |
| **OD-9** | `.beads/.br_history/` gitignore housekeeping (CF-04) | Handled separately, not Cycle-002 build scope; `.beads/issues.jsonl` stays unstaged |

## 19. Build-gate statement

```
This Sprint Plan opens no build gate.
Sprint 00 is docs-only (tracked docs only) and runs the normal /implement -> /review-sprint -> /audit-sprint -> acceptance cadence, opening no OA-2 build gate.
Sprint 01 and Sprint 02 require a later explicit operator OA-2 / build-gate action.
Broad optimization remains closed.
Runtime-agent changes remain forbidden.
The claim ceiling remains Rung 1.
```

The single hard procedural gate for build is OA-2 (`docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` §3; loop
contract §6). `/implement` may run for Sprint 01/02 only after the operator explicitly opens the build gate. Until then,
only planning (and the Sprint-00 docs lane, on acceptance) proceeds. This plan creates no `/implement` prompt and writes
no app code.

## 20. Recommendation

**Sprint Plan is ready for operator acceptance** — 3 sprints, Core/Stretch and SDD-ratified defaults as confirmed:
**Sprint 00** (docs-only, all Core, no gate) · **Sprint 01** (Scale Foundation, Core build, needs OA-2) · **Sprint 02**
(Repeated Batch + Dispersion, Core build + 2 Stretch, needs OA-2). Every build task is confined to additive `frozen/`,
offline `analysis/`, `tests/`, and local run dirs; the agents stay frozen; `regime-v001` stays byte-unchanged; the
ledger gets no row per batch; statistics are descriptive-only.

**Do NOT begin implementation.** This plan opens no build gate and creates no `/implement` prompt. After operator
acceptance, the next steps are one of:

1. **commit the Sprint Plan** (planning artifact lands on `main`), and/or run **Sprint 00** (docs-only; normal
   `/implement → /review-sprint → /audit-sprint → acceptance` cadence; **no OA-2 gate**); then
2. the operator later opens an explicit build gate (**OA-2**) for Sprint 01 → Sprint 02.

Neither build step is performed by this Sprint Plan. It creates the artifact and reports status only.

> **Sources:** `docs/cycles/cycle-002/02-sdd.md` (binding input; §1.2, §3.3, §4.1, §5, §6.1, §7, §8, §9, §14);
> `docs/cycles/cycle-002/01-prd.md` (C2-FR-1..7, AC-1..9, NG1..10); `docs/cycles/cycle-002/00-research-and-planning.md`
> (RQ-3/4/5/6/7/8/10); `docs/operator/turntrace-loop-contract.md` (§1-§3, §6-§10);
> `docs/operator/deferred-lane-gate-after-sprint-01.md` (still-closed list, L71-87); `docs/claim-ceiling.md`
> (L5-6, L22-23, L29-35, L42-64); `docs/ledger.md` (L3-12); `frozen/regimes/regime-v001.json` (L4-9);
> `frozen/seeds/seed-set-v001.json` (n=12; unseeded; raise-N-in-v002 rationale);
> `docs/cycles/cycle-000-bootstrap/01-turntrace-prd.md` (ladder L274-276); `eval/run_eval.py` (L121, L128-154,
> L239-243, L281-288, L333-336); `analysis/aggregate.py` (L56-89, L125-140); `analysis/delta_report.py`
> (cross-regime refusal); `analysis/failure_report.py` (sanitization contract); `eval/hygiene_check.py` (L35-45).
> Every task maps to a PRD/SDD requirement and a repo-grounded source. This plan opens no build gate, designs no
> runtime-agent change, and creates no `/implement` prompt.
