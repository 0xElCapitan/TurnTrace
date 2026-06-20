# TurnTrace — Product Requirements (Reality-Grounded)

> **Source of truth:** this PRD was reverse-engineered from CODE by `/ride` 2026-06-20,
> not from a forward design doc. Forward PRDs already exist per cycle under
> `docs/cycles/cycle-NNN/01-prd.md` — those remain authoritative for intent; this file
> reflects what the shipped code actually does. Every claim carries a grounding marker.
>
> **Document metadata:** generator riding-codebase · Loa 1.180.0 · drift policy `code`.

## Product summary

[GROUNDED] TurnTrace is a data-loop and evaluation harness that runs a trading-card-game
agent against a local simulator (cabt / Kaggle Pokémon TCG), seals immutable per-run
artifacts with provenance, aggregates results into an append-only ledger, and enforces a
bounded **claim ceiling** so no unearned strength claim escapes. (`README.md:3`,
`eval/run_eval.py`, `docs/claim-ceiling.md`)

## User types

| User | Needs | Evidence |
|------|-------|----------|
| [GROUNDED] Researcher / operator | Run evaluations, compare agents, advance the claim ceiling under a fixed loop | `docs/operator/turntrace-loop-contract.md`, `eval/run_eval.py`, `analysis/delta_report.py` |
| [GROUNDED] Auditor / reviewer | Verify reproducibility + provenance of any run without rerunning it | `hashes.txt` provenance, `analysis/replay_check.py`, `eval/validate.py` |
| [INFERRED] Competition submitter | Validate a candidate agent before hosted submission | `eval/mirror_validate.py` (candidate-vs-self smoke), `agent(obs_dict)` contract |

## Functional requirements (as built)

| ID | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-1 | Probe the simulator and record observed capabilities with conservative fallbacks | [GROUNDED] Built | `sim/probe.py`, `sim/capabilities.json` |
| FR-2 | Play one match → match-summary + decision-trace joined by a content hash | [GROUNDED] Built | `eval/run_match.py:75,188` |
| FR-3 | Drive N matches into one sealed, immutable run dir with provenance | [GROUNDED] Built | `eval/run_eval.py:95,138,230` |
| FR-4 | Refuse to overwrite a populated run dir (immutability) | [GROUNDED] Built | `eval/run_eval.py:138` |
| FR-5 | Two baseline agents: random-legal floor + deterministic scripted | [GROUNDED] Built | `agents/runtime/*.py` |
| FR-6 | Aggregate a run → summary.csv + (on deliverable intent) one ledger row | [GROUNDED] Built | `analysis/aggregate.py`, `eval/run_eval.py:335` |
| FR-7 | Same-regime A/B delta + cross-run dispersion (descriptive only) | [GROUNDED] Built | `analysis/delta_report.py`, `analysis/dispersion_report.py` |
| FR-8 | Sanitized evidence summary + independent fail-closed validator | [GROUNDED] Built | `analysis/evidence_summary.py` |
| FR-9 | Reproducibility check (audit-trail hash; byte-identical gated on seed control) | [GROUNDED] Built | `analysis/replay_check.py` |
| FR-10 | Validate run-dir artifacts against schemas | [GROUNDED] Built | `eval/validate.py` |
| FR-11 | Map PRD goals G-1..G-7 to on-disk evidence | [GROUNDED] Built | `analysis/e2e_validate.py` |
| FR-12 | Block Competition Data from being committed | [GROUNDED] Built | `eval/hygiene_check.py` |

## Non-functional requirements (verified in code)

- [GROUNDED] NFR-1 Runtime/offline separation enforced by import-direction lint (`tests/test_import_direction.py`).
- [GROUNDED] NFR-7 stdlib-only application code (no third-party deps in agents/sim/eval/analysis).
- [GROUNDED] NFR-2 Immutable run artifacts (`eval/run_eval.py:138`).
- [GROUNDED] NFR-3 Reproducibility = distribution-stable + audit-trail (seed uncontrolled) (`sim/probe.py:65`, `analysis/replay_check.py`).
- [GROUNDED] CC-1/CC-2 Competition Data is local-only, never in tracked artifacts (`sim/adapter.py:15-19`).

## Claim ceiling (product posture)

[GROUNDED] Standing ceiling: **Rung 2 — "beats random-legal"** (earned Cycle-007;
`docs/claim-ceiling.md:1-104`, ledger row `run-v003-c-1..20`). Explicitly NOT granted:
Rung 3, calibration, tournament/absolute strength, runtime-agent maturity, or any
FunSearch/RL/self-play/deck-optimization claim. Forbidden agent words
(strong/competitive/optimal/calibrated/complete) are gated.

## Grounding summary

- Claims: 24 · [GROUNDED] 22 (92%) · [INFERRED] 1 (4%) · [ASSUMPTION] 0.
- Quality target (>80% grounded, <10% assumption): **met.**
- Assumptions requiring validation: none material (the one INFERRED item, "competition
  submitter" user type, is a reasonable read of `mirror_validate.py` + the `agent()` contract).
