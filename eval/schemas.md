# `eval/schemas.md` — Sprint 00 flat-file field lists (Task 00.6)

> Plain field lists — the design authority for the Sprint 00 artifacts (SDD §3,
> plan §4 / §7.2). The machine-checkable form lives in `eval/validate.py`; this
> doc and that validator must agree. No code logic here.
>
> **Capability-tolerance rule (NFR-6):** a capability-uncertain field may be
> `null` **iff** its capability flag says the capability is absent. The probe
> (`sim/capabilities.json`) sets those flags. Sprint 00 observed: `seed_controlled=false`,
> `invalid_action_detectable=true`, `timeout` undetectable (`null`),
> `legal_actions_observed=true`, `own_hidden_state_observable=true`.
>
> **Competition-Data rule (CC-1/CC-2, ESP):** no schema field carries raw card
> IDs/names or deck lists. Card-identity signals are stored as SHA-256 digests
> or counts only — so even local (git-ignored) traces never hold Pokémon Elements.

## `match-summary.json` — one object per match (`runs/<run_id>/match_results/<match_id>.json`)

Carries **no claim ceiling** (the ledger is the only ceiling-bearing artifact).

| Field | Type | Null? | Notes |
|---|---|---|---|
| `run_id`, `match_id`, `regime_id` | string | no | foreign keys |
| `experiment_id` | string | yes | null in Sprint 00 |
| `agent_id`, `agent_version` | string | no | agent under test (player 0) |
| `opponent_id` | string | no | player 1 |
| `deck_id` | string | no | FK into deck-pool |
| `opponent_deck_id` | string | yes | known (mirror) → set |
| `seed` | int | yes | **null** (`seed_controlled=false`) |
| `seed_controlled` | bool | no | false (no seed param exposed) |
| `match_index` | int | no | always present — unseeded-mode identity |
| `result` | enum | no | `win`/`loss`/`draw`/`error` — single source of truth |
| `ending_cause` | string | yes | `prize-out`/`deck-out`/`no-active`/`card-effect`/`error` |
| `turns` | int | no | turns before end |
| `timeout` | bool | yes | **null** (no published budget; `budget_source=assumed`) |
| `invalid_action_count` | int | yes | int (detectable=true); null only if undetectable |
| `invalid_action_detectable` | bool | no | true |
| `total_decisions` | int | yes | agent decision rows; null iff `trace_present=false` |
| `trace_present` | bool | no | true in Sprint 00 |
| `trace_hash` | string | yes | SHA-256 of canonical sidecar; null iff no trace |
| `started_at`, `completed_at` | string | no | ISO-8601 |
| `wall_clock_ms` | int | no | match wall time |
| `simulator_version` | string | no | `cabt (kaggle-environments 1.14.10)` |
| `sim_version_source` | enum | no | `reported`/`installed-pin` |
| `deck_hash` | string | no | content hash of the deck (drift detection) |
| `error` | string | yes | non-null **iff** `result==error` (FM-01 guard) |
| `notes` | string | no | capability gaps, mode |

**Invariants:** `result==error` ⇔ `error` populated. `seed_controlled=true`
requires integer `seed`. `invalid_action_detectable=true` requires integer
`invalid_action_count`. `trace_present=true` requires string `trace_hash` and
integer `total_decisions`. `total_decisions` == count of agent decision rows.

## `decision-trace.jsonl` — one object per record (`runs/<run_id>/traces/<match_id>.jsonl`)

Optional artifact (loop runs on summaries alone if absent). Two `record_type`s.
The `trace_hash` in the summary is SHA-256 over the canonical serialization of
**all** rows (sorted keys, compact, ASCII; integers only — no floats).

**Decision row** (`record_type="decision"`):

| Field | Type | Null? | Notes |
|---|---|---|---|
| `run_id`, `match_id`, `regime_id` | string | no | FKs |
| `decision_index` | int | no | global monotonic, 0-based |
| `turn` | int | no | turn at decision |
| `player` | enum | no | `agent` (player 0) / `opponent` (player 1) |
| `phase` | int | yes | select context token (raw) |
| `public_state_summary` | object | yes | counts both sides (no card IDs) |
| `private_state_summary` | object | yes | **agent rows only**; own hand count + card-id digest, discard/prize/deck counts. Opponent rows: **null** (no leakage) |
| `legal_actions_count` | int | yes | number of offered options |
| `legal_actions_digest` | string | yes | SHA-256 of canonical OptionType list |
| `legal_actions_sample` | array | yes | first-k OptionType tokens |
| `selected_action` | object | no | `{indices, option_types}` (no card IDs) |
| `selected_action_type` | int | yes | primary selected OptionType (raw token) |
| `decision_latency_ms` | int | no | wall time around the agent call |
| `random_seed` | null | — | audit-trail posture (seed uncontrolled) |
| `error` | string | yes | rejection/crash on this decision; else null |
| `post_decision_observation` | null | — | reconstruct from next row / terminal |

**Terminal row** (`record_type="terminal"`, exactly one, last):

| Field | Type | Notes |
|---|---|---|
| `run_id`, `match_id`, `regime_id` | string | FKs |
| `decision_index` | int | terminal index |
| `result` | enum | `win`/`loss`/`draw`/`error` |
| `ending_cause` | string\|null | mapped from cabt reason |
| `turns` | int | final turn count |
| `final_prize_counts` | array\|null | prizes remaining `[p0, p1]` |
| `last_decision_index` | int | last decision row index |

## `summary.csv` — aggregate per run (`runs/<run_id>/summary.csv`)

Columns: `regime_id, run_id, agent_version, opponent_id, n_matches, win_rate,
illegal_action_rate, timeout_rate, error_rate, avg_turns, avg_wall_clock_ms`.
Aggregated from the single `result` enum. `n_matches` == per-match file count.

## `manifest.json` — run ID authority (`runs/<run_id>/manifest.json`)

`run_id`, `regime_id`, `expected_match_ids` (non-empty list), `agent_id`,
`opponent_id`, `deck_a_id`, `deck_b_id`, `match_indices`, `opponent_pool_id`,
`agent_version`, `created_at`, `mode`. Written **first**; the immutability guard
checks every written `match_id` against `expected_match_ids`.

## `hashes.txt` — provenance stamp (`runs/<run_id>/hashes.txt`)

`KEY=VALUE` lines. **Required non-empty (AC-6):** `git_rev`, `sim_version`,
`seed_list_hash`, `timestamp`. Also: `git_dirty`, `created_at`,
`sim_version_source`, `agent_version`, `deck_pool_hash`, `opponent_pool_hash`,
`metrics_spec_hash`, `regime_hash`, `deck_hash`. Flat SHA-256 strings — no
signing, no hash chains (plan §7.3).

## `ledger.md` row — the only ceiling-bearing artifact (`docs/ledger.md`)

One append-only row per run: `date, run_id, regime_id, git_rev, sim_version,
agent_version, opponent_pool_ref, seed_set_ref, games, win_rate,
illegal_action_rate, timeout_rate, error_rate, avg_turns, mode, hypothesis,
claim_ceiling, notes`. `claim_ceiling` **required and non-empty**.
