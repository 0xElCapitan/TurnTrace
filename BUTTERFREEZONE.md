# TurnTrace — Butterfree Zone

Operator/agent context for **TurnTrace**. Code-grounded, sanitized, and
deliberately small. This document describes TurnTrace itself — not the Loa
development framework that happens to be mounted under `.claude/`. It contains
no Competition Data; it only points at sanitized, tracked governance artifacts.

## Current standing

- **Cycle-007 is closed** — operator-accepted, committed, and pushed.
- **Standing claim ceiling: Rung 2 — "beats random-legal."**
- **Scope of that claim:** `scripted-v001` beats `random_legal-v001` under
  `regime-v003` — one ledgered, same-regime, descriptive result (a disjoint-bands
  rule over K=20 batches at n=500). Nothing broader is claimed.
- **Authorities:** `docs/ledger.md` (evidence-admission), `docs/claim-ceiling.md`
  (current standing-ceiling summary), `docs/cycles/cycle-007/07-closeout.md`
  (closeout of record).

## What TurnTrace is

TurnTrace is a **data-loop / evaluation harness for simulator-based trading card
game agents** (target: the `cabt` / Kaggle Pokémon TCG environment). Its posture:
produce data before optimizing agents; freeze baselines before claiming uplift;
keep run artifacts immutable; tie every claim to evidence. Application code is
**Python standard library only**; persistence is flat files (JSON/JSONL/CSV/MD),
no database.

## Architecture map

| Component | Role |
|-----------|------|
| `agents/runtime/` | Agents under test (`random_legal`, `scripted_baseline`); stdlib only |
| `sim/` | cabt adapter, environment resolver, live probe — the only `cabt` / Competition-Data boundary |
| `eval/` | Match + evaluation runners, schema validators, hygiene guard, canonical JSON |
| `analysis/` | Offline reporting over sealed run dirs — never touches `cabt` |
| `frozen/` | The **regime**: immutable decks/seeds/opponents/regimes/metrics — the test definition |
| `runs/` | Generated, sealed run dirs — local / gitignored by default |
| `docs/` | Durable cycle docs, operator contracts, `ledger.md`, `claim-ceiling.md` |
| `tests/` | stdlib `unittest` + plain-assert smokes / lint |

**Data flow (one evaluation):** `sim/probe.py` confirms the simulator is live →
`eval/run_eval.py` drives the runtime agents through `sim/` for the frozen seed set
→ a sealed run dir is written → `analysis/*` summarize it → only on explicit
deliverable intent is a single row admitted to `docs/ledger.md`.

## Hard boundaries

- **Only `sim/` touches `cabt` / Competition Data.** It is the single blast radius.
- **`analysis/` never touches `cabt`** — it reads sealed run dirs offline.
- **Runtime agents stay stdlib-only** (`agents/runtime/`).
- **Import direction is mechanically enforced** by `tests/test_import_direction.py`:
  runtime → stdlib; sim → cabt; eval → sim + runtime + analysis; analysis → analysis only.
- **`.claude/` is Loa development tooling (System Zone)** — it is *not* TurnTrace
  functionality and must never be edited as part of TurnTrace work.

## Claim ceiling

- **Standing ceiling: Rung 2 — "beats random-legal,"** bounded strictly to the one
  ledgered same-regime descriptive result (`scripted-v001` vs `random_legal-v001`
  under `regime-v003`).
- **Not claimed** (do not let any artifact imply otherwise):
  - no Rung 3 claim;
  - no calibration claim;
  - no tournament-strength claim;
  - no runtime-agent maturity claim;
  - no FunSearch / RL / self-play / deck-optimization / MCTS / value-model claim;
  - no broader Pokémon TCG strength claim.
- The append-only ledger is the **evidence-admission authority**;
  `docs/claim-ceiling.md` summarizes the current standing ceiling.

## Evidence / data containment

- **Raw generated runs stay local / gitignored by default.**
- **Never in tracked docs:** raw traces, simulator logs, deck lists, card IDs/names,
  Pokémon Elements, Competition Data, CSV/PDF dumps, `deck.csv`, or `cg/`.
- **May appear in tracked docs:** sanitized summaries, hashes, ledger rows, claim
  ceilings, and closeouts.
- **Mechanical guards:** `eval/hygiene_check.py` (path guard, CC-1/CC-2),
  `analysis/evidence_summary.py` (sanitized summaries + leak/empty-hash validator),
  plus adapter-level digests so raw card data never reaches a tracked artifact.

## Operator workflow

1. Probe the simulator (`sim/probe.py`).
2. Run an evaluation into a fresh sealed run dir (`eval/run_eval.py`).
3. Analyze the sealed run dir (`analysis/*`).
4. Only with explicit deliverable intent, admit **one** row to `docs/ledger.md`.
5. At cycle close, update `docs/claim-ceiling.md` and write the cycle closeout.

Cycles are durable. The ledger, claim-ceiling, and closeout are append-only
governance artifacts — treat them as immutable history, not scratch space.

## Key commands

```
# both env vars required; both point at LOCAL, gitignored inputs
TURNTRACE_CG_DIR=<dir with the cg package>   TURNTRACE_DECK_FILE=<local starter-deck csv>

python sim/probe.py                                   # confirm simulator is live
python eval/run_eval.py --run-id R --agent scripted_baseline [--deliverable]
python eval/run_match.py --match-index N --run-id R --match-id M --out-dir D
python eval/validate.py <run_dir>                     # schema-validate a run dir
python eval/mirror_validate.py                        # candidate-vs-self smoke
python eval/hygiene_check.py                          # Competition-Data staging guard
python analysis/aggregate.py <run_dir>               # run dir → summary.csv
python analysis/evidence_summary.py <run_dirs...>    # sanitized evidence summary
python tests/test_import_direction.py                # AST lint: import direction
python tests/test_evidence_summary.py                # standalone, no cabt
python tests/test_smokes.py                          # needs cabt + deck file
```

## Key files

- `README.md` — project front door
- `docs/ledger.md` — append-only evidence-admission ledger
- `docs/claim-ceiling.md` — current standing claim ceiling
- `docs/cycles/cycle-007/07-closeout.md` — Cycle-007 closeout of record
- `docs/cycles/cycle-007/06a-sp6-promoted-summary.md` — promoted SP-6 summary
- `analysis/evidence_summary.py` — sanitized summary + leak validator
- `eval/hygiene_check.py` — Competition-Data path guard
- `tests/test_import_direction.py` — import-direction invariant
- `tests/test_evidence_summary.py` — evidence-summary tests
- *(Loa lives under `.claude/` as development tooling only — System Zone, never edited.)*

## Do / Do Not

**Do**
- keep runtime agents stdlib-only and the import direction intact;
- keep Competition Data local; track only sanitized summaries, hashes, and ledger rows;
- tie every claim to a ledgered, same-regime result;
- treat ledger / claim-ceiling / closeout as append-only governance artifacts.

**Do Not**
- put raw traces, deck lists, card data, `cg/`, or `deck.csv` into tracked files;
- claim beyond Rung 2 (no calibration, tournament, RL / self-play / MCTS / value-model, or broader TCG strength);
- edit `.claude/` (System Zone) or any Cycle-007 evidence / ledger / claim-ceiling / closeout artifact;
- count a crash as a loss (FM-01), or overwrite a sealed run dir (the immutability guard refuses it).

## Carry-forward notes

- Moving the ceiling to Rung 3 requires fresh, pre-registered, same-regime evidence
  admitted through the ledger — not a documentation edit.
- This Butterfree Zone is a hand-maintained, sanitized context document. Update it on
  cycle close; do not regenerate it from a generic codebase ride (that is what put
  framework-centric noise here in the first place).
- Provenance: corrective rewrite following commit `e2b0e40`, which had committed a
  framework-centric BUTTERFREEZONE and generic ride/planning artifacts under
  `grimoires/loa/`.
