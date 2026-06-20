# Cycle-007 S03 — Fresh Same-Regime Evidence-Generation Report

**Date:** 2026-06-19
**Cycle / sprint:** Cycle-007, Sprint **S03** — Fresh same-regime evidence generation + gate.
**Type:** eval scope (NG12 lifted only here, under operator gate **OD-C7-9**).
**Status:** **admissibility established only.** This report records *that* the fresh batch
was generated under the committed S02 pre-registration and *that* both gates pass — by
reference, hash, and sanitized name only. **No verdict (PASS / FAIL / INCONCLUSIVE) is
applied here; no terminal act occurs.**

> Sanitization posture: this tracked artifact carries **references + content hashes +
> sanitized metric/agent names + local path-status only**. It embeds **no** raw traces,
> simulator logs, deck lists, card IDs/names, Pokémon Elements, Competition Data, run-dir
> dumps, raw evidence rows, dispersion/band/win-rate values, inferential statistics, the
> numeric `M`, any verdict, or any ceiling-bearing language. The bands themselves live only
> in the local/gitignored run dirs and the local/gitignored summary.

---

## 1. Authorization (OD-C7-9)

**OD-C7-9 fresh-evidence authorization is on record for this turn (S03 only).** It authorizes
generating fresh same-regime evidence under the committed S02 pre-registration record,
creating local/gitignored run dirs and one local/gitignored evidence summary, running
`--validate` and `--promotion-check` on that local summary, freezing the new `regime-v003`
definition, and writing this one sanitized tracked report.

OD-C7-9 does **not** authorize S04, verdict application, SP-6, value promotion, a Rung-2
ledger row, a claim-ceiling advance, or any terminal act — none of which occur here (§8).

---

## 2. Commit-order / O1 ancestry ("M before bands")

- **S02 O1 precedence anchor (pre-registration commit):**
  `a27aef38db5cded5120c4eb923f6a7e8cd27a6e2`
  (subject: `docs: pre-register Cycle-007 Rung-2 attempt`).
- **S02 commit touched only** `docs/cycles/cycle-007/04-pre-registration.md`
  (1 file, +253) — **no** run-dir / evidence / regime path; the S03 generation surface was
  untouched at the pre-registration commit.
- **Ancestry proof:**
  `git merge-base --is-ancestor a27aef38db5cded5120c4eb923f6a7e8cd27a6e2 HEAD` → exit `0`.
- Every generated run stamps `git_rev = a27aef38db5cded5120c4eb923f6a7e8cd27a6e2` in its
  `hashes.txt`, so the batch is provably generated **at/after** the pre-registration commit —
  the "`M` fixed before any band exists" property is tamper-evident in history.

---

## 3. Regime (sanitized): `regime-v003`

One new, never-observed frozen regime; baseline and candidate both run under it (same-regime).
Only the seed-set differs from the prior regimes; the opponent/deck/metrics components are
reused **by reference + content hash** (the `regime-v002` convention). `regime-v001` and
`regime-v002` and their components are **byte-unchanged** (no edit of a prior regime).

**Tracked frozen files created (content hash = sha256 of file bytes):**

| File | sha256 |
|------|--------|
| `frozen/regimes/regime-v003.json` | `5cab765cc5a854f100f34d435d110d76bcb64dcf238c450dd230b140857ed59f` |
| `frozen/seeds/seed-set-v003.json` | `fcdf901a70226839f3a9daffc4cae9a39d867672530e13426422b3d5de07cd2c` |

**Reused-by-reference components (byte-unchanged; stamped into every run's `hashes.txt`):**

| File | sha256 |
|------|--------|
| `frozen/opponents/opponent-pool-v001.json` | `b9cafd79ca1b7bcda56d4c784a2486e839cc4058d507c65c2dac646003579a32` |
| `frozen/decks/deck-pool-v001.json` | `c149f3a38657320105a3ab3fa281f54addc1e2da37942a5084c49446841a4b2e` |
| `frozen/metrics/metrics-spec-v001.json` | `63f16b1f3b23ea33ca045cd286474e97759ee78c09f8ccebfc3a2836d33ea0ae` |

`seed-set-v003` is a genuinely new component (not a renamed copy of a prior seed-set): under
`seed_controlled=false` a match index is a neutral identity label, and `seed-set-v003` uses a
contiguous index block disjoint from both prior seed-sets, hash-pinned before any agent ran.
Its `seed_list_hash` is `18b8c58ada1e5ec6fd70f3a7b47f35288f6c8223955329b805922fd95015d961`
(distinct from the prior seed-sets). The justified-`n` argument is unchanged from the S02
record (the threshold and any band values are **not** restated here).

---

## 4. Agents (sanitized version names)

| Role | Agent version | Run-id family |
|------|---------------|---------------|
| baseline | `random_legal-v001` | `run-v003-b-1` … `run-v003-b-20` |
| candidate | `scripted-v001` | `run-v003-c-1` … `run-v003-c-20` |

Both are **existing frozen agents** re-run to generate evidence (eval scope; no new agent,
heuristic, search, or learning system was built or tuned). The candidate runs against the
frozen `random_legal` opponent; the baseline runs against the same frozen opponent (mirror).

---

## 5. Fresh batch (run IDs + local status only)

- **Exactly K = 20 batches per agent at n = 500** matches per batch per agent, all under the
  one `regime-v003`. Run IDs: `run-v003-b-1 … run-v003-b-20` (baseline) and
  `run-v003-c-1 … run-v003-c-20` (candidate) — 40 sealed run dirs total.
- **Stopping rule honored:** exactly the pre-declared K=20 at n=500 were read, then stop. No
  K=50, no top-up, no observed-batch expansion, no optional stopping, no batch-padding, no
  interim verdict/peeking, no candidate/baseline swap, no best-of-N, no `M` change.
- **Local-by-default (ESP-1):** the run dirs live only under local/gitignored
  `runs/run-v003-{b,c}-{1..20}/…` and are **not** staged or tracked. No raw run content
  enters git.
- **Provenance / audit-trail present in every run** (verified across all 40):
  - regime-tuple stamp in `hashes.txt` (regime / seed-set / opponent-pool / deck-pool /
    metrics-spec content hashes);
  - source-hash provenance (`agent_source_hash`, `opponent_source_hash`, config hash);
  - per-decision canonical traces (`traces/<match_id>.jsonl`, 500 per run) with a per-match
    `trace_hash`;
  - `git_rev = a27aef38…` (the S02 anchor) stamped in each run.

---

## 6. Evidence summary (local/gitignored) + content digest

- **Exactly one** evidence summary was written to a **local/gitignored** path:
  `.run/s03-gen/evidence-summary-regime-v003.json` (under `.run/`, gitignored). It is **not**
  written under tracked `docs/`, and is **not** staged or committed.
- Summary shape (sanitized identity fields only; **no** band/dispersion values restated here):
  single `regime_id = regime-v003`, `n = 500`, `K = 20`, two agents each with K=20 runs, and
  a **non-empty integrity stamp** (`hashes` map with 40 entries, every value a 64-hex sha256
  digest).
- **Summary content digest:** sha256
  `60d3c8afeba121e8884a5493989b8633fa6ae4116bf2a60b8537f15c2acb0ddf`.
- **Generator local-by-default guard confirmed:** the generator **refuses a tracked `--out`**
  — a `--out docs/…` target exits `1` and writes nothing.

---

## 7. Gate results (command names + exit codes)

Both admissibility gates were run on the local summary; both exit `0`.

| Gate command | Exit code |
|--------------|-----------|
| `python analysis/evidence_summary.py --validate <local-summary>` | `0` |
| `python analysis/evidence_summary.py --promotion-check <local-summary>` | `0` |

- `--validate` exit 0 → schema-conforming, sanitized, single-regime.
- `--promotion-check` exit 0 → the full hardened validator is clean **and** the summary
  carries a non-empty `hashes` integrity stamp (parity-or-stricter with `--validate`). It
  **writes nothing and promotes nothing**.

Both gates passing establishes **admissibility** of the fresh batch for the S04 verdict step.
It is **not** itself a verdict and asserts nothing about how the candidate compares to the
baseline.

---

## 8. Non-occurrence statement (this S03 pass)

This S03 pass:

- applied **no** verdict (no PASS / FAIL / INCONCLUSIVE);
- issued **no** SP-6;
- promoted **no** value to tracked status (the summary stays local/gitignored);
- wrote **no** Rung-2 ledger row;
- advanced **no** claim ceiling;
- did **not** modify `docs/ledger.md` (byte-unchanged at
  `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`) or `docs/claim-ceiling.md` (byte-unchanged at
  `b914ca1b89fdd539da4d19d008231ac9f00c45ee`; still Rung 1);
- started **no** S04 work.

The loop's standing posture is unchanged: the experiment ledger (`docs/ledger.md`) remains
the only ceiling-bearing artifact, and this fresh evidence carries no ceiling of its own.

---

## 9. Tracked vs local artifacts

**Tracked (this sprint):**
- `docs/cycles/cycle-007/05-evidence-generation-report.md` (this report);
- `frozen/regimes/regime-v003.json`, `frozen/seeds/seed-set-v003.json` (the new frozen
  regime + seed-set components needed to define `regime-v003`).

**Local / gitignored (never committed):**
- the 40 fresh run dirs under `runs/run-v003-{b,c}-{1..20}/…`;
- the one evidence summary `.run/s03-gen/evidence-summary-regime-v003.json`.

---

## 10. Sources / traceability

- **Pre-registration tuple, `M`/`K`/`n`/stopping rule, verdict rule (by reference):**
  `docs/cycles/cycle-007/04-pre-registration.md` (§1–§11).
- **S03 contract / acceptance criteria:** `docs/cycles/cycle-007/03-sprint-plan.md`
  (Sprint S03; O1, O3, O5).
- **Fresh-evidence storage, promotion gate, commit-order, terminal acts:**
  `docs/cycles/cycle-007/02-sdd.md` (§2.3, §3, §4, §6).
- **Functional requirements:** `docs/cycles/cycle-007/01-prd.md` (C7-FR-1 … C7-FR-7).
- **Generator + both gate modes:** `analysis/evidence_summary.py`;
  pinned by `tests/test_evidence_summary.py` (absent-`hashes` regression, landed at
  `ceb6f67`).
- **Provenance stamp / immutability:** `eval/run_eval.py`; staging guard
  `eval/hygiene_check.py`.
