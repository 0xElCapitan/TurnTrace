# Experiment Ledger (PR-8)

> **The only ceiling-bearing artifact.** One append-only row per run; each row
> carries a non-empty `claim_ceiling` and its sample size `n`/`games`. Per-match
> records and `summary.csv` carry NO ceiling. A `verdict` of better/worse may be
> written ONLY for a same-regime, agent-only comparison with a ceiling + n —
> never across regimes (NFR-5). Rows are append-only; never edit a past row.

| date | run_id | regime_id | git_rev | sim_version | agent_version | opponent_pool_ref | seed_set_ref | games | win_rate | illegal_action_rate | timeout_rate | error_rate | avg_turns | mode | hypothesis | claim_ceiling | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-06-18 | run-0001 | regime-v001 | 2cf1f4fb68017c7ca440d4931449d5024b186688 | cabt (kaggle-environments 1.14.10) | random_legal-v001 | opponent-pool-v001 | seed-set-v001 | 12 | 0.5 | 0.0 | 0.0 | 0.0 | 13.42 | unseeded | Loop produces honest evidence regardless of win rate (Sprint 00 goal). | measures legality/throughput of random_legal-v001 on regime-v001 at n=12; NO strength claim — win rate here is not evidence of quality (ladder Rung 1). | mode=unseeded; timeout undetectable (soft gate); illegal-action gate hard (detectable=true). |
