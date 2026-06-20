# TurnTrace — System Design (Reality-Grounded)

> **Source of truth:** reverse-engineered from CODE by `/ride` 2026-06-20. Per-cycle
> forward SDDs exist under `docs/cycles/cycle-NNN/02-sdd.md` and remain authoritative for
> intent; this file reflects the shipped system. Grounding markers throughout.
>
> **Document metadata:** generator riding-codebase · Loa 1.180.0.

## Tech stack (verified)

| Layer | Choice | Evidence |
|-------|--------|----------|
| Language | Python (probed: 3.14.0) | `sim/capabilities.json:python` |
| Dependencies | [GROUNDED] **none** — stdlib only (NFR-7) | no third-party import in app code |
| Simulator | cabt via `cg` package (kaggle-environments 1.14.10), local/git-ignored | `sim/adapter.py:73`, `sim/capabilities.json` |
| Tests | stdlib `unittest` + plain-assert checks | `tests/test_smokes.py`, `tests/test_evidence_summary.py` |
| Persistence | flat files (JSON/JSONL/CSV/MD); no DB | run-dir layout, `eval/run_match.py:222` |
| VCS integration | `git` shell-out for provenance | `eval/run_eval.py:71` |

## Module structure (four zones)

[GROUNDED] Import direction is mechanically enforced (`tests/test_import_direction.py`):

| Zone | Modules | May import | cabt? |
|------|---------|-----------|-------|
| `agents/runtime/` | random_legal, scripted_baseline | stdlib | no |
| `sim/` (single blast radius) | adapter, _env, probe | stdlib + cabt | **yes (only here)** |
| `eval/` | run_match, run_eval, validate, mirror_validate, hygiene_check, canonical_json | stdlib + sim + agents/runtime + analysis | via sim |
| `analysis/` | aggregate, delta_report, dispersion_report, evidence_summary, failure_report, replay_check, e2e_validate | stdlib + analysis | no |

See `reality/architecture-overview.md` for the component diagram and data flow.

## Key design decisions (as built)

- [GROUNDED] **Single blast radius.** Only `sim/adapter.py` + `sim/probe.py` touch cabt;
  everything else depends on the `SimAdapter` port. If the live API changes, only `sim/`
  changes. (`sim/adapter.py:8-13`)
- [GROUNDED] **Capability-driven, not assumption-driven.** Every capability is a flag from
  the probe, defaulting conservative until proven. `seed_controlled=false` because cabt
  exposes no RNG seed. (`sim/probe.py:65,393`, `sim/adapter.py:41`)
- [GROUNDED] **Immutability + provenance.** Run dirs are write-once; `manifest.json` is the
  ID authority; `hashes.txt` pins git_rev + component hashes + agent source hashes.
  (`eval/run_eval.py:138,177,230`)
- [GROUNDED] **FM-01 masquerade guard.** A crash is `result="error"`, never a loss; the
  validator enforces `result==error ⟺ error field populated`. (`eval/run_match.py:162`,
  `eval/validate.py`)
- [GROUNDED] **Deliverable-intent ledger gate.** A ledger row is written only on explicit
  `--deliverable`/`--ledger`; bare runs write `summary.csv` only. (`eval/run_eval.py:335`)
- [GROUNDED] **Descriptive-only statistics.** Comparisons use disjoint-bands / dispersion
  over batches; no inferential statistic and no forbidden agent word may appear.
  (`analysis/dispersion_report.py`, `analysis/evidence_summary.py`, `docs/claim-ceiling.md`)
- [GROUNDED] **Competition-Data containment.** Adapter views emit counts / OptionType enums
  / SHA-256 digests, never raw card IDs; hygiene + evidence validators backstop it.
  (`sim/adapter.py:15-19,51`)

## Data model

[GROUNDED] The "data model" is the flat-file run-dir contract — see `reality/types.md` for
full field lists of `match-summary.json`, `decision-trace.jsonl`, `manifest.json`,
`hashes.txt`, `summary.csv`, the `ledger.md` row, and the frozen-input shapes. Authority:
`eval/schemas.md`, enforced by `eval/validate.py`.

## API surface

[GROUNDED] See `reality/api-surface.md` (every public function + signature + `file:line`)
and `reality/entry-points.md` (every CLI + exit codes). No HTTP/RPC surface exists; the
external contracts are the cabt port, the `agent(obs_dict)` submission contract, the local
filesystem, and `git`.

## Grounding summary

- Claims: 21 · [GROUNDED] 21 (100%) · [INFERRED] 0 · [ASSUMPTION] 0.
- Quality target (>80% grounded, <10% assumption): **met.**
- Assumptions requiring validation: none.
