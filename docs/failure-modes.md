# Failure-Mode Registry (PR-10)

> Human-maintained, append-only catalogue of every way the loop produces wrong or
> untrustworthy output (plan §4.5). For Sprint 00 this is a prose cross-reference,
> not a machine join. New modes are appended; status updated in place. An entry is
> only worth keeping if its **Signature** can be computed from fields the simulator
> actually gives us (per the capability probe, `sim/README.md`).
>
> No Competition Data here — reference trace rows by `run_id`+`match_id`+`decision_index`.

## Entry template

```
### FM-<id>: <short name>
- Status: open | mitigated | watched | wont-fix
- First seen: <date> (run_id / match_id)
- Signature: how to detect it in decision-trace.jsonl / match-summary.json
- Description: what goes wrong, in plain terms
- Why it costs games: the outcome link
- Examples: run_id + match_id + decision_index
- Regression check: the automated test/metric, or "none yet"
- Notes: caveats, capability gaps
```

## Capability context (Sprint 00 probe findings)

`sim/capabilities.json`: `seed_controlled=false`, `invalid_action_detectable=true`,
timeout undetectable (`timeout=null`), `legal_actions_observed=true`,
`own_hidden_state_observable=true`. These determine which signatures below are
computable now versus deferred.

## Seed catalogue (FM-01 … FM-09)

### FM-01: Invalid action proposed (reframed: malformed selection)
- Status: watched
- Signature: decision-trace row with `error != null`, or match-summary `invalid_action_count > 0`.
- Description: The agent submits a selection the engine rejects. **Reframe:** because
  `cabt` only ever offers legal moves and the agent picks indices into that set, a
  genuinely "illegal *move*" is not possible — the residual failure is a **malformed
  selection** (out-of-range index, wrong count, or duplicate indices; cg/api.py error
  codes 4/5/6). `random_legal` samples within `[minCount, maxCount]` over offered
  options, so this should stay at 0.
- Why it costs games: a malformed selection raises and the runner records `result=error`
  (never a masqueraded loss — the FM-01 masquerade guard in `eval/validate.py`).
- Regression check: `illegal_action_rate == 0` on the baseline set, **only where**
  `invalid_action_detectable=true` (it is). An undetectable rate is never a pass.
- Notes: detectable=true (probe), so this is a hard gate (metrics-spec-v001).

### FM-02: Timeout / over-budget decision
- Status: watched (capability-limited)
- Signature: match-summary `timeout=true`, or `decision_latency_ms` near budget.
- Description: a decision exceeds a per-move/per-game time budget.
- Why it costs games: turn/game lost to clock.
- Regression check: `max(decision_latency_ms) < budget` — **deferred**: no budget is
  published by the local surface (`timeout_detectable=false`), so `timeout=null` per
  record and the §5.4 timeout gate is a **soft warning**. `decision_latency_ms` is still
  recorded as an audit signal.
- Notes: `budget_source=assumed`; revisit if a budget is later published.

### FM-03: Bad prize trade
- Status: open
- Signature: `post_decision_observation` / next-row `public_state_summary` shows we
  gave up a higher-value KO than we took; prize differential swings against us.
- Regression check: none yet (needs a prize-differential metric in offline analysis).

### FM-04: Wasted resource
- Status: open
- Signature: `selected_action` plays a supporter/energy/item with negligible gain.
- Regression check: none yet.

### FM-05: Failed setup
- Status: open
- Signature: early-turn trace shows no bench development / no energy attachment when legal.
- Regression check: none yet.

### FM-06: Missed lethal
- Status: open (capability-limited)
- Signature: a winning legal action existed in `legal_actions_sample` but
  `selected_action` was something else.
- Regression check: offline scan for "winning legal action existed but not chosen" —
  needs richer action decoding than Sprint 00 captures (we store OptionType tokens, not
  full attack resolution). Fallback: detect post-hoc when next-turn state shows the
  opponent survived a lethal board.

### FM-07: Over-draw / deck-out risk
- Status: watched
- Signature: draw-heavy actions while deck count low; turns approaching deck size.
  Observed end reason `deck-out` (cabt reason=2) is a direct signal.
- Why it costs games: starting a turn with 0 deck cards is a loss (cabt reason=2).
- Regression check: track `ending_cause` distribution and `avg_turns`. (For random play,
  `deck-out`/`no-active` ends are expected and are NOT a strategy fault.)

### FM-08: Bad search target
- Status: open
- Signature: a search/tutor action selects a suboptimal card vs a higher-value option.
- Regression check: none yet.

### FM-09: Poor energy sequencing
- Status: open
- Signature: energy attachments mistimed/misdirected across turns.
- Regression check: none yet.

## Known unknowns (resolved by the probe)

- **Seed control:** ABSENT (no RNG seed parameter). → unseeded, audit-trail posture.
- **Legal-action enumeration:** CONFIRMED.
- **Hidden-state visibility:** own hand observable; opponent hand + own deck order hidden
  (and never logged).
