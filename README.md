# TurnTrace

TurnTrace is a data-loop and evaluation harness for a simulator-based trading
card game agent — built to measure an agent against a frozen baseline before
making any claim about it.

Initial target: the Kaggle Pokémon TCG AI Battle Challenge (`cabt`).

**Status:** through development Cycle-007 · stdlib-only Python (~21 files,
~5,689 LOC) · standing claim ceiling **Rung 2 — "beats random-legal."**

## What it is

TurnTrace is an evidence-grounded evaluation harness for a single trading-card-game
agent playing against a simulator. The simulator integration is real and has been
run — `sim/probe.py` confirms `cabt` is live and records its capability flags — and
the evaluation pipeline produces sealed, immutable run artifacts that the offline
analysis tools read to decide what, if anything, can be claimed.

It is deliberately small and dependency-free: the application code is **Python
standard library only**, with no third-party runtime dependencies.

## Core posture

- produce data before optimizing agents
- freeze baselines before claiming uplift
- preserve immutable run artifacts
- log decision traces where the simulator allows
- keep runtime agents separate from offline analysis
- keep claims tied to evidence

## Architecture

The codebase is four zones with a **mechanically enforced** import direction —
`tests/test_import_direction.py` fails the build if any layer imports across the
boundary the wrong way:

```
cabt (cg) ──► sim/        the ONLY layer that touches the simulator / Competition Data
              adapter.py · _env.py · probe.py
                  │  (only eval/ may import sim/)
                  ▼
              eval/        run_match · run_eval · validate · hygiene_check
              ▲   │
agents/runtime/   │ writes a sealed, git-ignored run dir
(stdlib only)     ▼
random_legal      runs/<run_id>/   manifest · match_results · traces · hashes.txt
scripted_baseline      │ read-only
                       ▼
              analysis/   aggregate → delta / dispersion / evidence / failure /
              (offline,   replay / e2e → one append-only docs/ledger.md row
               stdlib,
               no cabt)
```

`sim/` is the only "blast radius": it is the lone layer that loads the simulator and
the only place Competition Data can enter. Raw card data never enters a tracked
artifact — enforced by adapter digests, `hygiene_check`, and an evidence-summary
validator.

| Directory | Role |
|-----------|------|
| `agents/runtime/` | Agents under test — `random_legal`, `scripted_baseline` (stdlib only) |
| `sim/` | cabt adapter, environment resolver, live probe (the only simulator-touching layer) |
| `eval/` | Match + evaluation runners, schema validators, hygiene/mirror checks |
| `analysis/` | Offline reporting over sealed run dirs — never touches cabt |
| `frozen/` | The *regime*: immutable decks, seeds, opponents, regimes, metrics |
| `runs/` | Generated, sealed, git-ignored run outputs |
| `docs/cycles/`, `docs/operator/` | Durable planning, the loop contract, and the claim ceiling |

## Running an evaluation

All entry points are stdlib `argparse` CLIs; run them with `python <path>`. Two
environment variables point at the **local, git-ignored** simulator and starter deck,
and both are required:

- `TURNTRACE_CG_DIR` — directory containing the `cg` package (cabt)
- `TURNTRACE_DECK_FILE` — local starter-deck CSV

A typical first run:

```bash
# 1. Probe that the simulator is alive (exit 0 = a match completed)
python sim/probe.py

# 2. Evaluate N matches into one sealed run directory
python eval/run_eval.py --run-id R --agent scripted_baseline

# 3. Analyze the sealed run dir
python analysis/aggregate.py runs/R
```

A ledger row in `docs/ledger.md` is written **only** with explicit deliverable intent
(`--deliverable` or `--ledger PATH`); a bare run produces `summary.csv` but no ledger
row.

Tests are stdlib `unittest` + plain-assert smokes (no pytest):

```bash
python tests/test_import_direction.py    # standalone AST lint, no cabt
python tests/test_evidence_summary.py    # standalone, no cabt
python tests/test_smokes.py              # needs cabt + TURNTRACE_DECK_FILE
```

## Claim ceiling

The standing claim ceiling is **Rung 2 — "beats random-legal,"** earned in Cycle-007
and recorded in `docs/claim-ceiling.md` and `docs/ledger.md`. The ledger row is a PASS
for `scripted-v001` over `random_legal-v001` under `regime-v003`, decided by a
descriptive disjoint-bands rule across K=20 batches at n=500.

That is the entire strength claim, and it is bounded by design: *beats a random-legal
baseline, under this frozen regime.* TurnTrace does not claim that any agent is strong,
competitive, calibrated, optimal, or complete. The append-only ledger is the
evidence-admission authority; `docs/claim-ceiling.md` summarizes the current standing
ceiling. The forbidden strength words remain gated out of other artifacts.

## For contributors

A few load-bearing invariants are baked into code — please don't fight them:

- **Stay in your zone.** `agents/runtime/` is stdlib-only; only `sim/` may touch cabt;
  only `eval/` may import `sim/`; `analysis/` imports nothing but itself.
- **A crash is an error, not a loss** (`result="error"` is never counted as a loss).
- **Sealed run dirs are immutable** — the guard refuses a populated dir and exits 3.
- **The ledger owns the claim ceiling** — raising what an agent may claim goes through
  the cycle / claim-ceiling process, not a code comment.

## Built with

TurnTrace is developed using the [Loa](.claude/) agent-development framework (the
tooling under `.claude/`); Loa's skills and commands are development tooling, not
features of TurnTrace itself.
