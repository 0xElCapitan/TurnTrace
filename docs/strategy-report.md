# Strategy Report — Evidence Pack (PR-12, SKELETON)

> **Sprint 00 stub: headings + placeholders only.** Creating the structure now fixes
> where later runs and (later-cycle) ablations slot in (plan §9). Most sections stay
> empty until the artifacts exist. **Rule:** every claim sentence must point to a
> specific logged artifact (match-summary, decision-trace, ledger row, regime hash) —
> a sentence with no artifact is deleted. No Competition Data (card IDs/names) appears
> in this report; reference decks by `deck_id` + hash.

## 1. Claim ceiling (what we assert, and its limits)
- *Content:* what is and is not claimed (see `docs/claim-ceiling.md`).
- *Source:* the frozen regime (scope) + the experiment ledger (headline numbers, `n`,
  each row's `claim_ceiling`). Written last; binding on the rest.
- *Status:* TODO — Sprint 00 ceiling is Rung 1 (legality/throughput only; no strength claim).

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
- *Status:* TODO — Sprint 00: `random_legal` vs mirror over `seed-set-v001`, `mode=unseeded`,
  distribution-stable + audit-trail.

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
- *Status:* TODO — seed catalogue FM-01…FM-09 exists; evidence fills in as runs accrue.

## 7. Limitations
- *Content:* honest framing — small samples, pool-specific results, simulator unknowns
  (seed control, time budget) that weakened a proof.
- *Source:* regime scope + the Rung 0 unknown/fallback list (`sim/README.md`) + sample
  sizes.
- *Status:* TODO — Sprint 00: unseeded (no byte-replay), timeout undetectable, n small,
  opponent = mirror only.

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
