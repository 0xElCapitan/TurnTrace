# `frozen/` — the immutable regime (PR-6)

`frozen/` holds the **regime**: the immutable test definition that every run is
measured under. A regime is the four-component tuple stamp (SDD §3.6, plan §5.2):

```
regime-v001 = { seed-set-v001, opponent-pool-v001, deck-pool-v001, metrics-spec-v001 }
```

## Freeze rules (binding)

1. **A new version is a new file, never an edit.** Changing the seed set, the
   opponent pool, the deck pool, the metrics spec — or moving to a new
   simulator/env version — requires `regime-v002` (and new component files),
   never an in-place edit of `v001` (plan §5.3). A new sim version silently
   changes outcomes, so it is itself a regime trigger.
2. **Never compare across regimes** (NFR-5). A result is only meaningful
   relative to its own `regime_id`. "57% on v002" and "52% on v001" are not
   comparable, and their difference is not uplift.
3. **References + hashes only — never Competition Data** (CC-1/CC-2, ESP-3).
   `decks/deck-pool-v001.json` stores `{deck_id, deck_hash, source_ref}` — no
   card lists, IDs, or names. Cards resolve at runtime from the local,
   git-ignored deck file.
4. **Hashed into every run.** `run_eval` hashes each component file and the
   regime into `runs/<run_id>/hashes.txt`, so a run's inputs are provable later.

## Sprint 00 posture

`seed-set-v001` is **unseeded** (the probe found no controllable RNG seed;
`sim/capabilities.json: seed_controlled=false`): it is a fixed, ordered list of
match indices, and reproducibility is distribution-stable + audit-trail (NFR-3).
`metrics-spec-v001` gates correctness (legality/completion), not strength —
Sprint 00 makes no strength claim (ladder Rung 1).
