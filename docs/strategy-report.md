# Strategy Report — Evidence Pack (PR-12 / S02-6)

> **Sprint 02 fill state.** §1, §4, §6, §7 and the PERMITS/FORBIDS boundary are now
> filled at **Rung 1**. §2 (deck concept), §3 (agent logic), §8 (proof bundle) remain
> TODO skeletons; §5 (ablation table) remains **DEFERRED**. **Rule:** every non-skeleton
> claim sentence points to a specific logged artifact (match-summary, decision-trace,
> ledger row, regime hash, or `analysis/` output) — a sentence with no artifact is
> deleted. No Competition Data (card IDs/names) appears here; decks are referenced by
> `deck_id` + hash, runs by `run_id` + hashes, and no raw metric values are pasted beyond
> what the sanitized ledger already carries.

## PERMITS / FORBIDS (claim boundary)

This report's claims live inside a fixed boundary mirroring the deferred-lane gate
(`docs/operator/deferred-lane-gate-after-sprint-01.md:37-69`).

- **PERMITS** — stating that the candidate (`run-0002`) differs from the baseline
  (`run-0001`) on a metric by the recorded delta under `regime-v001` at n=12, explained as
  the mechanical consequence of the single agent-under-test change; bounded by the Rung-1
  ledger ceiling (`docs/ledger.md:11-12`; per-metric deltas via `analysis/delta_report.py`).
- **FORBIDS** — any gameplay-strength, statistical-significance, cross-regime, or
  leaderboard claim (`docs/operator/deferred-lane-gate-after-sprint-01.md:39-42`); the
  forbidden words *strong / competitive / optimal / calibrated / complete* except as
  negated/forbidden language (`docs/claim-ceiling.md:54-59`); and every still-closed
  broad-optimization lane — RL, self-play, deck optimizer, value model, win-probability
  model, dashboard, ELO or tournament system, search/lookahead/MCTS, Kaggle upload
  automation, leaderboard optimization, agent tuning loops, submission packaging,
  two-direction ablation ledger, SaaS/product surface
  (`docs/operator/deferred-lane-gate-after-sprint-01.md:71-87`). Cross-regime comparison is
  additionally hard-refused (exit 2) by `analysis/delta_report.py`.

## 1. Claim ceiling (what we assert, and its limits)
- *Content:* what is and is not claimed (see `docs/claim-ceiling.md`).
- *Source:* the frozen regime (scope) + the experiment ledger (headline numbers, `n`,
  each row's `claim_ceiling`). Written last; binding on the rest.
- *Status:* FILLED (Sprint 02, Rung 1). The claim ceiling is **Rung 1 — legal completion
  only**; no gameplay-strength claim is made (`docs/claim-ceiling.md:22-23`). The
  experiment ledger (`docs/ledger.md`) is the **only ceiling-bearing artifact**
  (`docs/claim-ceiling.md:5-6`); each run row carries a non-empty `claim_ceiling` bounding
  its `n` (`docs/ledger.md:11-12`). No other artifact in this report asserts a ceiling of
  its own — the delta report and aggregate report carry only a Rung-1 footer
  (`analysis/delta_report.py`, `analysis/failure_report.py`).

## 2. Deck concept
- *Content:* the deck used, its intent, why chosen.
- *Source:* `deck-pool-v001` reference + `deck_hash` (card list is local Competition Data).
- *Status:* TODO.

## 3. Agent logic
- *Content:* how the agent selects moves — rules, thresholds, tie-breaks.
- *Source:* decision-trace (rules firing) + tuning-knob provenance.
- *Status:* TODO — Sprint 00 agent is `random_legal` (uniform over offered legal options;
  no rules, no scoring).

## 4. Evaluation method
- *Content:* opponent pool, evaluation set, number of games, reproducibility procedure,
  win/loss/error definitions.
- *Source:* `regime-v001` (`regime_id`) + experiment ledger (`run_id`, `git_rev`,
  timestamps).
- *Status:* FILLED (Sprint 02). Evaluation is a **same-regime, agent-only** comparison of
  baseline `run-0001` (`random_legal-v001`) against candidate `run-0002` (`scripted-v001`)
  under `regime-v001`, `games`=12, `mode=unseeded` (`docs/ledger.md:11-12`). The frozen
  regime fixes seed-set + opponent-pool + deck-pool + metrics-spec; a change to any
  component is a new regime, never an edit (`docs/claim-ceiling.md:29-34`). Win/loss/draw/
  error derive from the single `result` enum, agent-under-test (player 0) perspective
  (`docs/claim-ceiling.md:15-16`). Per-metric deltas are produced read-only by
  `analysis/delta_report.py`, which hard-refuses any cross-regime comparison
  (`CrossRegimeRefusal` → exit 2). Reproducibility is distribution-stable + audit-trail
  (`docs/claim-ceiling.md:42-52`).

## 5. Ablation table
- *Content:* agent variants vs baseline — rule changed, win-rate delta, per-category
  breakdown, sample size, and the `revert_check_result` column.
- *Source:* the ablation-ledger (later cycle). An ablation row whose revert check did not
  pass is **not** report-eligible.
- *Status:* DEFERRED — no ablations in Sprint 00 (the first delta report is Sprint 01).

## 6. Failure-mode section
- *Content:* where the agent is weak or breaks.
- *Source:* `docs/failure-modes.md` + error/loss-flagged match-summaries. **Mandatory** —
  omitting known failures violates the Rung 4 honesty gate.
- *Status:* FILLED (Sprint 02). Known failure modes are catalogued in the append-only
  registry `docs/failure-modes.md` and the versioned, status-bearing
  `docs/failure-mode-taxonomy-v001.md`. **Computable-now:** FM-01 (legality / malformed
  selection, `detector: present`, gated by `invalid_action_detectable=true`) and FM-07
  (deck-out / over-draw, via the `ending_cause` distribution + `avg_turns`); sanitized
  aggregate counts for these are emitted to stdout by `analysis/failure_report.py`
  (counts only — never raw rows). **Deferred:** FM-02 (timeout, gated by
  `timeout_detectable=false`), and FM-05 / FM-09 (`detector: none-yet`). **The per-decision
  loss-attribution categories FM-03 / FM-04 / FM-06 / FM-08 carry `detector: forbidden`** —
  this sprint opens no per-decision quality detector or scorer
  (`docs/failure-mode-taxonomy-v001.md`).

## 7. Limitations
- *Content:* honest framing — small samples, pool-specific results, simulator unknowns
  (seed control, time budget) that weakened a proof.
- *Source:* regime scope + the Rung 0 unknown/fallback list (`sim/README.md`) + sample
  sizes.
- *Status:* FILLED (Sprint 02). (1) `mode=unseeded` — no controllable RNG seed
  (`sim/capabilities.json: seed_controlled=false`), so there is no byte-identical replay;
  reproducibility is distribution-stable + audit-trail (`docs/claim-ceiling.md:42-52`).
  (2) Timeout is undetectable (`sim/capabilities.json: timeout_detectable=false`); the
  timeout gate is a soft warning and `timeout=null` per record
  (`docs/failure-modes.md:49-58`). (3) `games`=12 is a small sample
  (`docs/ledger.md:11-12`). (4) The only opponent is the mirror `random_legal` under
  `opponent-pool-v001` — results are pool-specific and do not generalize
  (`docs/claim-ceiling.md:24-26`, `docs/claim-ceiling.md:31`).

## 8. Appendix / proof bundle
- *Content:* the raw evidence enabling an outside reader to verify or replay — ledger rows,
  per-match records, hashes, replay instructions.
- *Source:* the full experiment ledger, `match-summary` files, sampled decision-traces,
  regime hashes. (Raw run trees are local/git-ignored; reference by `run_id` + hashes.)
- *Status:* TODO.

---

### Traceability discipline
Before any future version is final, do one pass mapping **every claim sentence → one
artifact reference**. Any sentence that fails the map is backed by adding the artifact or
deleted. The report's credibility comes entirely from this property.
