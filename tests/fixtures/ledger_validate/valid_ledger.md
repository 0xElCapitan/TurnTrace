# Synthetic Ledger Fixture (S03 ledger_validate test)

> SYNTHETIC, minimal, safe. No real run data, Competition Data, card/deck content,
> Pokémon Elements, or raw traces. Mirrors the docs/ledger.md house format (the
> 18-column schema) so analysis/ledger_validate.py can be exercised off-line and
> independent of the gitignored runs/ tree. Hashes/ids are placeholder tokens.

| date | run_id | regime_id | git_rev | sim_version | agent_version | opponent_pool_ref | seed_set_ref | games | win_rate | illegal_action_rate | timeout_rate | error_rate | avg_turns | mode | hypothesis | claim_ceiling | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-01-01 | run-syn-1 | regime-syn-a | 1111111111111111111111111111111111111111 | sim-syn | agent-syn-001 | opponent-pool-syn | seed-set-syn | 10 | 0.5 | 0.0 | 0.0 | 0.0 | 8.0 | unseeded | synthetic row; no strength claim. | Rung 1 (legal completion): synthetic descriptive row; no strength claim. | synthetic notes; cited summary sha256 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa (local). |
| 2026-01-02 | run-syn-2 | regime-syn-a | 2222222222222222222222222222222222222222 | sim-syn | agent-syn-001 | opponent-pool-syn | seed-set-syn | 10 | see cited summary | see cited summary | see cited summary | see cited summary | see cited summary | unseeded | synthetic by-reference row. | Rung 2 (beats random-legal): synthetic by-reference descriptive row; no strength claim. | synthetic notes; see cited summary; sha256 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb (local, gitignored). |
