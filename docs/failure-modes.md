# Failure-Mode Registry (PR-10)

> Human-maintained, append-only catalogue of every way the loop produces wrong or
> untrustworthy output (plan §4.5). For Sprint 00 this is a prose cross-reference,
> not a machine join. New modes are appended; status updated in place. An entry is
> only worth keeping if its **Signature** can be computed from fields the simulator
> actually gives us (per the capability probe, `sim/README.md`).
>
> No Competition Data here — reference trace rows by `run_id`+`match_id`+`decision_index`.

> See the machine-aligned, status-bearing taxonomy: `docs/failure-mode-taxonomy-v001.md`.

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

## Competition-findings additions (FM-10 … FM-11)

> Appended 2026-06-19 by the pre-Cycle-005 competition-findings docs patch (operator decisions
> SP-8 / SP-9, `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md`). These are **seeded from
> competition findings, not observed in a run** — so `First seen` is `none (seeded)` and there are
> no `run_id`/`match_id`/`decision_index` examples yet. No Competition Data: simulator-behavior
> content only; no card IDs/names, deck lists, or trace rows.

### FM-10: Official-rule assumption mismatch
- Status: watched
- First seen: none (seeded from competition findings 2026-06-19; SP-8)
- Signature: an expected action is absent from the offered legal options (`obs.select.option`); or a
  trace note shows an official-rule action category that analysis expected but the simulator never
  offered; or an analyzer-derived outcome disagrees with the simulator terminal result
  (`match-summary` `result` / `ending_cause`).
- Description: an agent or offline analyzer assumes official Pokémon TCG behavior where the `cabt`
  simulator uses different competition behavior — e.g. an officially declarable attack the simulator
  omits when its effect cannot resolve; automatic (left-to-right) vs. player-chosen multi-target
  ordering; or simultaneous-Knock-Out prize ordering. Per SP-8 the simulator is authoritative.
- Why it costs games: usually outcome-equivalent, but a mis-modeled legality/ordering can make the
  agent expect an action it can never take, or make offline analysis mis-attribute an outcome the
  simulator already decided.
- Examples: none (seeded; no run evidence). Record any later-observed divergence as a
  simulator-behavior note by `run_id`+`match_id`+`decision_index`.
- Regression check: none yet — the binding discipline is "trust `obs.select.option`, simulator logs,
  and the simulator terminal result; never build runtime logic around official-rule actions the
  simulator does not expose." Record a mismatch as a simulator-behavior note, **not** an agent failure.
- Notes: a guardrail, not an observed defect; pairs with SP-8 / CC-10. Detectable wherever the
  expected action category is enumerable from `obs.select.option`.

### FM-11: Top-episode overfitting / contaminated evidence
- Status: open
- First seen: none (seeded from competition findings 2026-06-19; SP-9)
- Signature: a change rationale cites daily top episodes but **no** same-regime TurnTrace run-vs-run
  comparison exists; or report language implies improvement from scouting alone; or raw top-episode
  data appears in git / tracked docs (this last leg is mechanically caught by the
  `eval/hygiene_check.py` raw-data path rules).
- Description: agent changes are justified by public top-episode observations without proving
  improvement under a frozen TurnTrace regime. Top episodes are hypothesis-generation input only
  (SP-9); they are not a same-regime benchmark and not proof of improvement.
- Why it costs games: belief without same-regime evidence drifts the agent on opponent-pool drift or
  run-to-run luck instead of a real, attributable delta — the exact failure TurnTrace exists to prevent.
- Examples: none (seeded; no run evidence).
- Regression check: require a same-regime TurnTrace comparison (descriptive deltas under the existing
  ceiling) before any improvement claim; keep raw daily datasets local/ignored (track only sanitized
  notes and hashes). The raw-data-in-git leg is gated by `eval/hygiene_check.py`.
- Notes: a process / evidence-discipline guardrail; the "raw data in git" leg is a true mechanical
  signature, the "no same-regime comparison" leg is a provenance/process check. Pairs with
  SP-9 / SP-6 / CC-6.
