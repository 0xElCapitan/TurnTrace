# Cycle-006 Closeout — Sprint 01: Promotion-Check Hardening (`--promotion-check`)

> Closeout artifact. Status: **CLOSED — operator-accepted, committed, pushed.** Cycle-006 was a
> **preparation + one narrow hardening sprint**. It built the `--promotion-check` promotion *gate* and resolved the
> reversible-safe half of the Rung-2 admission seam in tracked planning artifacts. **It attempted no Rung 2,
> promoted no value, generated no fresh evidence, chose no `M`, issued no SP-6, wrote no Rung-2 ledger row, advanced
> no claim ceiling, and applied no PASS/FAIL/INCONCLUSIVE admission verdict.** Building the gate is **not** admitting
> Rung 2. **Rung 1 held; Rung 2 remains unearned.** The Rung-2 attempt is deferred to **Cycle-007 behind a separate
> explicit operator gate.**
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, Daily-Top-Episode data, or Competition Data were committed in
> Cycle-006. Test fixtures are stdlib-only synthetic. No numeric margin `M` and no dispersion metric values appear
> in any tracked artifact.

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-006 / Sprint 01 — Promotion-Check Hardening |
| **Type** | Closeout artifact |
| **Date** | 2026-06-19 |
| **Final verdict** | **PASS WITH NOTES — ACCEPTED** (operator-accepted) |
| **Status** | **CLOSED / accepted / committed / pushed** |
| **Posture** | Preparation + one narrow hardening sprint; **not** a Rung-2 admission attempt |
| **Claim ceiling** | **Rung 1** (held for the whole cycle; not raised) |
| **Ledger invariant** | `docs/ledger.md` byte-unchanged; hash `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` |

---

## 1. Outcome

Cycle-006 Sprint 01 is **closed and operator-accepted** with a final verdict of **PASS WITH NOTES — ACCEPTED**.
The sprint delivered exactly the scoped, audited `--promotion-check` promotion gate plus its regression tests,
landed through the full loop `/implement → /review-sprint → /audit-sprint → operator acceptance`, and held every
binding posture constraint.

The cycle's governance/design half (Track A — ratify 8a, record the `M` pre-registration procedure with no `M`,
design the Cycle-007 fresh-evidence batch, pre-register the PASS/FAIL/INCONCLUSIVE verdict rule + fail-state
language) was completed inside the accepted PRD/SDD (`01-prd.md` §16.3, §9; `02-sdd.md` §8–§10). The code half
(Track B) is this sprint.

## 2. What shipped — the `--promotion-check` promotion gate

The implemented result is a `--promotion-check <summary.json>` mode on `analysis/evidence_summary.py` (a new
`_run_promotion_check` driver + CLI arg + dispatch) and a regression block (block 14, 14a–14f) in
`tests/test_evidence_summary.py`. The gate:

- **re-reads the summary JSON from disk** (independent gate; never trusts an in-memory object);
- **runs `validate_summary` wholesale** (the full hardened validator — C1–C4 — unchanged);
- **preserves the mixed-regime single-regime guard → exit 2** (via `_collect_regime_ids`);
- on any validator violation, **exits 3** (fail-closed leak class);
- after the validator is clean, **hard-fails an empty/absent `hashes` integrity stamp → exit 3**
  (CF-1 / OD-C5-2 floor);
- **passes (exit 0) only when the summary is clean AND `hashes` is a non-empty map**;
- **writes nothing** and **promotes nothing** (no `docs/` write, never `docs/ledger.md`; reads no `hashes.txt`,
  no sidecar);
- **preserves generate-mode empty-`hashes` WARNING at exit 0** (unchanged);
- **preserves `--validate` empty/absent-`hashes` acceptance at exit 0** (the precheck is promotion-only;
  `validate_summary` is not modified);
- **preserves the `0/1/2/3` exit-code contract** (no new exit code — the empty/absent-`hashes` hard-fail rides
  exit 3).

By construction the gate is **parity-or-stricter** with `--validate` (NFR-1): it rejects exactly what `--validate`
rejects **plus** empty/absent `hashes`; no `--validate`-accepted-and-non-empty-hashes-clean input is rejected, and
no `--validate`-rejected input is accepted. Independently re-verified across every rejection class at review and
audit.

## 3. Audit result

The security/quality audit (`06-audit-report.md`, Paranoid Cypherpunk Auditor) returned **PASS WITH NOTES —
ACCEPTED** with **no security findings** (CRITICAL 0 · HIGH 0 · MEDIUM 0 · LOW 0) and **no required fixes**.
Paranoid probes confirmed: no data leak to stdout/stderr (a planted Competition-Data token in a value is not
surfaced), the gate is stdout-silent (decisions on stderr only), the empty/absent-`hashes` precheck is
un-bypassable (non-dict / list / empty-string-digest `hashes` are caught by the validator first), the gate is
idempotent, and it has zero write surface (ledger byte-unchanged after all runs).

## 4. Review/audit notes → Cycle-007 carry-forwards (non-blocking)

The review (`05-review-report.md`) and audit (`06-audit-report.md`) recorded four advisory notes, all confirmed
**non-blocking** and carried forward to Cycle-007 (none required to land this sprint):

1. **Add an absent-`hashes` regression test** when the gate is first wired into a real Cycle-007 promotion.
   (AC-2 specifies *empty* `hashes`, which **is** regression-tested at 14b; the *absent*-key branch was verified
   manually/independently at review and audit and is structurally covered by the precheck's `isinstance` guard,
   but not yet pinned by a dedicated test.)
2. **Optionally add exit-1 (unreadable input) and both-flags-precedence regression tests.** Both behaviours were
   verified manually; exit-1 is a verbatim copy of the tested `--validate` read-failure block, and the
   stricter-wins precedence is documented in-code.
3. **Cosmetic docstring realignment accepted** (the CLI-synopsis lines were re-indented for alignment;
   documentation-only, no behaviour/exit-code change).
4. **"Writes-nothing" test shallowness accepted** because the diff confirms the driver has **zero write surface**
   (the shallow top-level `iterdir` snapshot plus the diff inspection together are sufficient).

One pre-existing, out-of-scope observation was recorded for completeness only (uncaught `RecursionError` on a
maliciously deep JSON, identical to the existing `--validate` exposure, operator-offline threat model) — explicitly
**not** a finding and **not** a required fix.

## 5. Posture confirmations (binding non-goals — all held)

- **Rung 1 held** for the whole cycle.
- **Rung 2 remains unearned** — not pending, not claimed, not attempted.
- **The Rung-2 attempt remains deferred to Cycle-007 behind a separate explicit operator gate.**
- **No numeric margin `M`** was chosen (none in any Cycle-006 artifact).
- **No SP-6** was issued; **no value was promoted** to tracked status.
- **No Rung-2 ledger row** was written; **no claim-ceiling advance** occurred.
- **No fresh evidence** was generated (no eval run, no K-batch, no K=50 top-up, no run dir; synthetic fixtures
  only).
- **No PASS / FAIL / INCONCLUSIVE admission verdict** was applied (the verdict rule is pre-registered in
  `01-prd.md` §16.3 for Cycle-007, never executed in Cycle-006).
- **No runtime-agent, gameplay-heuristic, FunSearch, RL, self-play, deck-optimizer, value/win-probability-model,
  search/MCTS, tournament/leaderboard, or dashboard scope** entered Cycle-006.
- **No Daily-Top-Episodes ingest and no Kaggle episode ingest.**
- **No raw Competition Data or Pokémon Elements** were committed.
- **No cross-regime comparison; no inferential statistic computed; no OD-6 relaxation executed.**
- **No second validator module, no `*.schema.json`, no third-party dependency, no ledger-writing promotion mode.**
- **`.claude/` (System Zone) untouched; no State-Zone cleanup performed.**

## 6. Invariants verified at closeout

- **`docs/ledger.md` byte-unchanged** at hash `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` (verified before and
  after the implementation commit and at closeout; `git diff --exit-code` clean). The ledger remains the only
  ceiling-bearing artifact, at its two Rung-1 `regime-v001` rows.
- **`docs/claim-ceiling.md` unchanged** (`git diff --exit-code` clean).
- **`.claude/ frozen/ runs/ agents/ sim/` clean** throughout.
- **State-Zone files** (`.beads/issues.jsonl`, `grimoires/loa/NOTES.md`) remained **dirty and unstaged**; they
  carry pre-existing housekeeping unrelated to this sprint and were **not** part of any Cycle-006 commit and **not**
  part of this closeout.

## 7. Cycle-006 artifact inventory

| Artifact | Role |
|---|---|
| `docs/cycles/cycle-006/01-prd.md` | PRD (accepted; OD-C6-1 ratified) — committed in `082a953` |
| `docs/cycles/cycle-006/02-sdd.md` | SDD (OD-C6-2…6 settled; Track-A deliverables) — committed in `082a953` |
| `docs/cycles/cycle-006/03-sprint-plan.md` | Sprint plan (T1–T5) — committed in `082a953` |
| `docs/cycles/cycle-006/04-implementation-report.md` | Implementation report — committed in `a5cf339` |
| `docs/cycles/cycle-006/05-review-report.md` | Review report (PASS WITH NOTES) — committed in `a5cf339` |
| `docs/cycles/cycle-006/06-audit-report.md` | Audit report (PASS WITH NOTES — ACCEPTED; no findings) — committed in `a5cf339` |
| `docs/cycles/cycle-006/07-closeout.md` | This closeout — committed in the closeout commit |

**Tracked code (committed in `a5cf339`):** `analysis/evidence_summary.py` (+73/−4), `tests/test_evidence_summary.py`
(+77/−1).

## 8. Commit trail (Cycle-006)

- `082a953923e5fd8e4643171466cfcc23f413a8dd` — *docs: plan TurnTrace Cycle-006* (PRD + SDD + sprint plan)
- `a5cf339482122b51e2c11ec6a1d9e3020562ff2d` — *feat: add TurnTrace promotion-check gate* (the two code files +
  the implementation/review/audit reports)
- *(this commit)* — *docs: close TurnTrace Cycle-006 Sprint 01* (this closeout)

`docs/ledger.md` and `docs/claim-ceiling.md` appear in **none** of these commits.

## 9. Cycle-007 handoff (deferred behind a separate explicit operator gate)

A Cycle-007 Rung-2 *attempt* may proceed **only** behind a separate explicit operator gate and only when **all**
of the PRD §19 conditions hold: Cycle-006 accepted (✔ this closeout); 8a ratified (✔ OD-C6-1); `M` pre-registered
under the recorded procedure, fixed **before** any fresh band is generated/read and **never** against the
already-observed K=20+20 set; a fresh, never-observed same-regime K≥20 batch generated under a justified `n` that
clears the noise floor (new eval scope); `--promotion-check` live (✔ shipped this cycle); provenance/audit-trail
intact and the verdict a same-regime TurnTrace descriptive delta (never episode-derived); the five conjunctive
Rung-2 readiness criteria all hold; and an explicit operator gate opens. Only then is the pre-registered verdict
rule (`01-prd.md` §16.3) applied; only on PASS do SP-6 + the Rung-2 row + ceiling advance follow, each a separate
operator act. **Any unmet item → the Rung-2 attempt defers again.**

The non-blocking carry-forwards in §4 (especially carry-forward 1, the absent-`hashes` regression test) are best
addressed when the gate is first wired into a real Cycle-007 promotion.

---

> **Closeout statement (binding).** Cycle-006 Sprint 01 is **CLOSED and operator-accepted** at **PASS WITH NOTES —
> ACCEPTED**. The shipped result is the `--promotion-check` promotion gate: it re-reads the summary from disk, runs
> `validate_summary` wholesale, preserves mixed-regime exit 2, hard-fails empty/absent `hashes` at exit 3, passes
> at exit 0 only when clean and non-empty-`hashes`, writes nothing, promotes nothing, preserves generate-mode
> empty-`hashes` warning at exit 0, preserves `--validate` empty/absent-`hashes` acceptance at exit 0, and
> preserves the `0/1/2/3` exit-code contract. The audit found no security findings and no required fixes. **Rung 1
> held; Rung 2 remains unearned; no `M`, no SP-6, no value promotion, no Rung-2 ledger row, no claim-ceiling
> advance, no fresh evidence, and no admission verdict were produced.** `docs/ledger.md` remained byte-unchanged at
> `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` and `docs/claim-ceiling.md` is unchanged. **The gate is
> hardening/preparation, not admission. The Rung-2 attempt is deferred to Cycle-007 behind a separate explicit
> operator gate.**
