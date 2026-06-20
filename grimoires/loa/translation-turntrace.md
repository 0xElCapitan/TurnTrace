# TurnTrace — A Narrative for Users & Contributors

> DevRel translation produced by `/translate` (Step 3 of the README re-grounding
> sprint) from `BUTTERFREEZONE.md` + `grimoires/loa/reality/*`, at HEAD `e933e8a`.
> **CODE IS TRUTH.** Every claim below is grounded in a code or reality citation.
> This is an *inspiration source* for the README, not the README itself.
>
> ⚠️ **Grounding note:** the `BUTTERFREEZONE.md` generator conflated the *Loa
> development framework* mounted in `.claude/` with the TurnTrace application —
> it reported "40 skills," "TypeScript/JavaScript," and a "Bridgebuilder" agent.
> **None of those describe TurnTrace.** This narrative describes the actual
> application: a stdlib-only Python evaluation harness. Loa is the tooling the
> project is *built with*, not a feature of it.

---

## The one-liner

**TurnTrace is an evidence-grounded evaluation harness for a single trading-card-game
agent playing against a simulator** (`cabt` / the Kaggle Pokémon TCG environment)
(`reality/architecture-overview.md:7-8`).

It is deliberately small and deliberately honest: **~21 Python files, ~5,689 lines,
zero third-party dependencies in the application code** (`reality/index.md:29`;
stdlib-only is mechanically the rule, NFR-7, `reality/architecture-overview.md:60`).

## The idea behind it

Most "my agent is good at game X" projects start by tuning the agent. TurnTrace
inverts that. Its design philosophy, in its own words:

> *produce data before optimizing; freeze baselines before claiming uplift; seal
> immutable run artifacts; tie every claim to a bounded **claim ceiling**.*
> (`reality/architecture-overview.md:9-10`)

In plain terms — four habits the codebase enforces in code, not just in docs:

1. **Data before agents.** You build the measurement loop first, so any later claim
   about an agent has evidence behind it.
2. **Freeze the test.** Baselines, seeds, decks, and metrics are frozen into a
   *regime* under `frozen/` — the immutable definition every run is measured against.
3. **Seal the outputs.** Each run writes a run directory that is never overwritten;
   the immutability guard refuses a populated dir and exits 3 (`run_eval.py:138`).
4. **Never out-claim the evidence.** A single append-only ledger (`docs/ledger.md`)
   is the *only* artifact allowed to carry a strength claim, and a set of
   "forbidden agent words" (strong / competitive / optimal / calibrated / complete)
   is gated so no unearned claim slips into an artifact
   (`reality/architecture-overview.md:72-74`).

## Where the project actually stands

TurnTrace is **not** a bootstrap shell (the repo-root README still says it is — that
README is stale by three development cycles; see `grimoires/loa/drift-report.md`).

- It is **through Cycle-007** of development — 7 cycles archived under `docs/cycles/`
  (`reality/architecture-overview.md:80`).
- The simulator integration is **real and has been run**: `sim/probe.py` confirmed
  cabt is runnable and recorded its capability flags (`reality/architecture-overview.md:45`).
- The standing **claim ceiling is Rung 2 — "beats random-legal,"** earned in
  Cycle-007 and recorded in `docs/claim-ceiling.md` and `docs/ledger.md`
  (`reality/architecture-overview.md:72`). The ledger holds 3 data rows; the
  Rung-2 row is a PASS for the `scripted_baseline` agent over the `random_legal`
  baseline, decided by a descriptive disjoint-bands rule across K=20 batches at
  n=500 under regime-v003 (`reality/architecture-overview.md:81-83`).

That is the whole strength claim, and it is intentionally bounded: *beats a
random-legal baseline, under this frozen regime.* Nothing more is claimed, by design.

## How it's put together (for the curious)

The codebase is four zones with a strict, **mechanically enforced** import direction
(`reality/architecture-overview.md:40-41`):

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

The single most important property here: **`sim/` is the only "blast radius."** It is
the lone layer that loads the simulator and the only place Competition Data can enter.
Raw card data is never allowed into a tracked artifact — enforced by adapter digests,
`hygiene_check`, and an evidence-summary validator (`reality/architecture-overview.md:75-76`).
A separate AST lint, `tests/test_import_direction.py`, fails the build if any layer
imports across that boundary the wrong way (`reality/entry-points.md:48`).

**Module map** (application code only; counts from `reality/structure.md` /
extracted module map):

| Directory | Role |
|-----------|------|
| `agents/runtime/` | The agents under test — `random_legal`, `scripted_baseline` (stdlib only) |
| `sim/` | cabt adapter, environment resolver, live probe (the only simulator-touching layer) |
| `eval/` | Match + evaluation runners, schema validators, hygiene/mirror checks |
| `analysis/` | Offline reporting over sealed run dirs — never touches cabt |
| `frozen/` | The *regime*: immutable decks, seeds, opponents, regimes, metrics |
| `runs/` | Generated, sealed, git-ignored run outputs |
| `docs/cycles/`, `docs/operator/` | Durable planning + the loop contract / claim ceiling (this is where planning lives — **not** `grimoires/loa/a2a/`) |

## For users — running an evaluation

Everything is a stdlib `argparse` CLI you invoke with `python <path>`
(`reality/entry-points.md:3`). Two environment variables point at the *local,
git-ignored* simulator and starter deck, and both are required
(`reality/entry-points.md:9-13`):

- `TURNTRACE_CG_DIR` → the directory containing the `cg` package (cabt)
- `TURNTRACE_DECK_FILE` → the local starter-deck CSV

A typical first run:

1. **Probe** that the simulator is alive — `python sim/probe.py`
   (exit 0 = a match completed) (`reality/entry-points.md:24`).
2. **Evaluate** — `python eval/run_eval.py --run-id R --agent scripted_baseline`
   drives N matches into one sealed run dir (`reality/entry-points.md:26`).
   A ledger row is written **only** with explicit deliverable intent
   (`--deliverable` or `--ledger PATH`); a bare run produces `summary.csv` but no
   ledger row (`reality/entry-points.md:38-42`).
3. **Analyze** — point the offline tools at the sealed run dir:
   `aggregate.py`, `delta_report.py`, `dispersion_report.py`,
   `evidence_summary.py`, `replay_check.py`, `e2e_validate.py`
   (`reality/entry-points.md:30-36`).

## For contributors — what to respect

If you want to add an agent or a report, the codebase has a few load-bearing
invariants baked into code that you should not fight:

- **Stay inside your zone.** `agents/runtime/` is stdlib-only; only `sim/` may touch
  cabt; only `eval/` may import `sim/`; `analysis/` imports nothing but itself.
  `tests/test_import_direction.py` enforces this (`reality/architecture-overview.md:40-41`).
- **A crash is an error, not a loss.** `result="error"` is never counted as a loss
  (FM-01, `run_match.py:162`) — keep that contract.
- **Sealed dirs are immutable.** Don't write back into a populated run dir; the
  guard exits 3 on purpose (`run_eval.py:138`).
- **The ledger owns the claim ceiling.** If your change would let an agent claim more
  than "beats random-legal," that has to go through the cycle/claim-ceiling process —
  not a code comment. Forbidden agent words are gated (`reality/architecture-overview.md:72-74`).
- **Tests are stdlib.** Three smoke/lint files today — `test_smokes.py` (needs cabt),
  `test_evidence_summary.py` and `test_import_direction.py` (standalone) — using
  `unittest` + plain asserts, **no pytest** in app code
  (`reality/entry-points.md:44-48`).

## Honest boundaries (what TurnTrace does *not* claim)

This is the part worth keeping front-and-center, because the whole project is built
around it:

- It does **not** claim general gameplay strength. The only standing claim is the
  bounded, relative, local **Rung-2** result above.
- It is **not** a framework, a library, or a multi-agent toolkit. It is one harness
  for one agent against one simulator.
- The "40 skills / slash-commands / Bridgebuilder agent / TypeScript" you may see in
  auto-generated context belong to **Loa**, the agent-development framework this
  repository is *built with* — they are tooling, not TurnTrace features.

---

## Grounding self-audit

| Claim | Source | Grounded? |
|-------|--------|-----------|
| Purpose: eval harness for one TCG agent vs cabt | `reality/architecture-overview.md:7-8` | ✅ |
| ~21 py files / ~5,689 LOC / stdlib-only | `reality/index.md:29`, `:60` | ✅ |
| Through Cycle-007 | `reality/architecture-overview.md:80` | ✅ |
| Claim ceiling = Rung 2 "beats random-legal" | `reality/architecture-overview.md:72`, `docs/claim-ceiling.md` | ✅ |
| Immutability guard exit 3 | `run_eval.py:138` | ✅ |
| Import direction enforced | `tests/test_import_direction.py`, `reality/architecture-overview.md:40-41` | ✅ |
| 3 stdlib test files (not 6, not pytest) | `reality/entry-points.md:44-48` | ✅ |
| Env vars required | `reality/entry-points.md:9-13` | ✅ |
| "40 skills / TS / Bridgebuilder" are Loa, not TurnTrace | BUTTERFREEZONE conflation, corrected per drift-report.md | ✅ (flagged) |

**No ungrounded strength claims introduced.** Forbidden agent words avoided.
Audience: prospective users + contributors. Status: ready as README inspiration source.
