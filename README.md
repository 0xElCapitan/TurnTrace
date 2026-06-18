# TurnTrace

TurnTrace is a data-loop and evaluation harness for simulator-based trading card game agents.

Initial target: the Kaggle Pokémon TCG AI Battle Challenge.

## Current status

Bootstrap only.

No simulator integration exists yet.  
No agent implementation exists yet.  
No gameplay-strength claims are made.

## Core posture

- produce data before optimizing agents
- freeze baselines before claiming uplift
- preserve immutable run artifacts
- log decision traces where the simulator allows
- keep runtime agents separate from offline analysis
- keep claims tied to evidence

## Early architecture

Runtime agent code belongs under:

`agents/runtime/`

Simulator adapter code belongs under:

`sim/`

Evaluation runners belong under:

`eval/`

Offline analysis belongs under:

`analysis/`

Frozen evaluation inputs belong under:

`frozen/`

Generated run outputs belong under:

`runs/`

Planning and operator artifacts belong under:

`grimoires/loa/a2a/`

Durable cycle docs belong under:

`docs/cycles/`

## Claim ceiling

At this stage, TurnTrace only claims to be a repository shell for a future data-loop harness.

It does not claim that any agent is strong, competitive, calibrated, optimal, or complete.
