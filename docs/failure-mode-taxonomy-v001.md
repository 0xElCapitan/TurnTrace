# Failure-Mode Taxonomy v001 (PR-1 / S02-1)

> Versioned, sanitized, status-bearing schema over the failure modes catalogued in
> `docs/failure-modes.md`. This is the **machine-aligned** companion to that
> append-only narrative registry: one entry per `FM-01..FM-09`, each declaring its
> axis, computability, gating capability, detector status, and a field-name-only
> signature. A future revision is an additive file (`-v002`), never an in-place edit
> — mirroring the regime/spec versioning convention (`regime-v001`,
> `metrics-spec-v001`; `docs/claim-ceiling.md`).
>
> **Claim ceiling: Rung 1.** This taxonomy carries no ceiling of its own and makes
> no gameplay-strength assertion — the experiment ledger (`docs/ledger.md`) is the
> only ceiling-bearing artifact. No Competition Data appears here: signatures cite
> field **names** only; evidence is referenced by `run_id`+`match_id`+`decision_index`
> strings, never row contents (`requires-raw-data: cannot-surface`).

## Field model (per entry)

| Field | Type | Notes |
|---|---|---|
| `fm_id` | string `FM-NN` | reuses the existing ids in `docs/failure-modes.md` |
| `name` | string | short coarse outcome / loss name |
| `axis` | enum `outcome` \| `loss-attribution` | `outcome` = derivable from `result`/`ending_cause`; `loss-attribution` = per-decision quality (name-only) |
| `compute_status` | enum `computable-now` \| `deferred` | whether a sanitized detector may be computed today |
| `gating_capability` | enum `seed_controlled` \| `invalid_action_detectable` \| `timeout_detectable` \| `none` | the `sim/capabilities.json` flag that gates computability |
| `capability_value` | bool \| `n/a` | mirrors the probed flag value; `n/a` when `gating_capability: none` |
| `signature` | string | field-**name** reference only; never row contents |
| `evidence_ref` | string \| `null` | `run_id`+`match_id`+`decision_index` reference string only |
| `detector` | enum `present` \| `none-yet` \| `forbidden` | `forbidden` = a per-decision quality detector that this sprint does not open |
| `status` | enum `open` \| `mitigated` \| `watched` \| `wont-fix` | lifecycle status |

## Capability context (mirrors `sim/capabilities.json`)

The probe records `seed_controlled=false`, `invalid_action_detectable=true`,
`timeout_detectable=false`, `legal_actions_observed=true`,
`own_hidden_state_observable=true`. Every `capability_value` below mirrors one of
these flags; `gating_capability: none` means no capability flag blocks the
signature (it derives from always-recorded fields such as `ending_cause`).

## Detector boundary (binding — encodes NG3 / OD-4)

For `fm_id ∈ {FM-03, FM-04, FM-06, FM-08}` the detector is `forbidden`:

> **Building any per-decision quality detector/scorer for this category is NOT
> covered by the narrow-planning gate and is a separate operator decision.**

These four are `axis: loss-attribution` — they ask "was this specific decision
good?", which is a per-decision quality judgment. This sprint is EXPLAIN / AUDIT
only; it adds **no** scoring agent and **no** per-decision quality scorer. A
`detector: none-yet` value (FM-05, FM-09) records only that no detector exists
today and does **not** authorize building a per-decision *quality* scorer under
this gate — that remains the same separate operator decision.

---

## FM-01 — Invalid action (malformed selection)

```
fm_id: FM-01
name: invalid action (malformed selection)
axis: outcome
compute_status: computable-now
gating_capability: invalid_action_detectable
capability_value: true
signature: match-summary invalid_action_count > 0, OR result == "error" with a populated error field
evidence_ref: null
detector: present
status: watched
```

The legality gate. The simulator only offers legal moves and the agent picks
indices into that offered set, so the residual is a malformed selection
(out-of-range index, wrong count, duplicate indices). Hard-gated because
`invalid_action_detectable=true`: counted by `eval/aggregate.py` only over
detectable records, and the FM-01 masquerade guard in `eval/validate.py` keeps a
mishandled error from passing as a win/loss/draw. Detector present today.

## FM-02 — Timeout / over-budget decision

```
fm_id: FM-02
name: timeout / over-budget decision
axis: outcome
compute_status: deferred
gating_capability: timeout_detectable
capability_value: false
signature: match-summary timeout == true (field is null while undetectable)
evidence_ref: null
detector: none-yet
status: watched
```

Deferred because `timeout_detectable=false`: the local surface publishes no
per-move budget, so `timeout` is recorded as `null` and the timeout gate is a
soft warning, never a pass/fail. `decision_latency_ms` is still recorded as an
audit signal. Revisit only if a budget is later published.

## FM-03 — Bad prize trade

```
fm_id: FM-03
name: bad prize trade
axis: loss-attribution
compute_status: deferred
gating_capability: none
capability_value: n/a
signature: per-decision prize differential across adjacent trace public_state_summary fields
evidence_ref: null
detector: forbidden
status: open
```

Per-decision quality judgment. **Building any per-decision quality
detector/scorer for this category is NOT covered by the narrow-planning gate and
is a separate operator decision.**

## FM-04 — Wasted resource

```
fm_id: FM-04
name: wasted resource
axis: loss-attribution
compute_status: deferred
gating_capability: none
capability_value: n/a
signature: trace selected_action plays a resource with negligible recorded gain
evidence_ref: null
detector: forbidden
status: open
```

Per-decision quality judgment. **Building any per-decision quality
detector/scorer for this category is NOT covered by the narrow-planning gate and
is a separate operator decision.**

## FM-05 — Failed setup

```
fm_id: FM-05
name: failed setup
axis: loss-attribution
compute_status: deferred
gating_capability: none
capability_value: n/a
signature: early-turn trace private_state_summary shows no bench development / no energy attachment when legal
evidence_ref: null
detector: none-yet
status: open
```

No detector exists today. `detector: none-yet` records absence only; any
per-decision *quality* scorer for this category remains the separate operator
decision named in the detector boundary above.

## FM-06 — Missed lethal

```
fm_id: FM-06
name: missed lethal
axis: loss-attribution
compute_status: deferred
gating_capability: none
capability_value: n/a
signature: a winning option present in trace legal_actions_sample while selected_action chose otherwise
evidence_ref: null
detector: forbidden
status: open
```

Per-decision quality judgment (capability-limited: Sprint 00 stores OptionType
tokens, not full attack resolution). **Building any per-decision quality
detector/scorer for this category is NOT covered by the narrow-planning gate and
is a separate operator decision.**

## FM-07 — Over-draw / deck-out risk

```
fm_id: FM-07
name: over-draw / deck-out risk
axis: outcome
compute_status: computable-now
gating_capability: none
capability_value: n/a
signature: match-summary ending_cause distribution (the "deck-out" bucket) plus avg_turns
evidence_ref: null
detector: none-yet
status: watched
```

Computable now from always-recorded `ending_cause` + `avg_turns`; no capability
flag gates it. `detector: none-yet` today, transitioning to `present` once the
aggregate failure-mode report (`analysis/failure_report.py`, PR-2) lands the
`ending_cause`-bucket count. For random play a `deck-out`/`no-active` ending is
expected and is **not** a strategy fault.

## FM-08 — Bad search target

```
fm_id: FM-08
name: bad search target
axis: loss-attribution
compute_status: deferred
gating_capability: none
capability_value: n/a
signature: a search/tutor selected_action takes a lower-value card than a higher-value offered option
evidence_ref: null
detector: forbidden
status: open
```

Per-decision quality judgment. **Building any per-decision quality
detector/scorer for this category is NOT covered by the narrow-planning gate and
is a separate operator decision.**

## FM-09 — Poor energy sequencing

```
fm_id: FM-09
name: poor energy sequencing
axis: loss-attribution
compute_status: deferred
gating_capability: none
capability_value: n/a
signature: energy-attachment timing across trace decision_index rows
evidence_ref: null
detector: none-yet
status: open
```

No detector exists today. `detector: none-yet` records absence only; any
per-decision *quality* scorer for this category remains the separate operator
decision named in the detector boundary above.

---

## Enum reference (for validation)

- `axis ∈ {outcome, loss-attribution}`
- `compute_status ∈ {computable-now, deferred}`
- `gating_capability ∈ {seed_controlled, invalid_action_detectable, timeout_detectable, none}`
- `detector ∈ {present, none-yet, forbidden}` — `forbidden` ⇔ `fm_id ∈ {FM-03, FM-04, FM-06, FM-08}`
- `status ∈ {open, mitigated, watched, wont-fix}`

**Sanitization invariant.** No `result`/`ending_cause` distribution *values*, no
card ids/names, no deck lists, no trace rows appear in this file. Distributions
live only in local, git-ignored run dirs (`requires-raw-data: cannot-surface`);
the aggregate report (PR-2) emits sanitized counts to stdout, not into this
tracked artifact.
