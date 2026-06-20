# Cycle-007 Closeout — Gated Rung-2 Admission Attempt: PASS, Rung 2 Earned

> Closeout artifact. Status: **CLOSED — operator-accepted, committed, pushed.** Cycle-007 ran the
> **gated Rung-2 admission attempt**: pre-register one frozen comparison tuple, pin the absent-`hashes`
> promotion gate, generate fresh same-regime evidence, apply the pre-registered verdict, and — **on PASS
> only** — take the three separate OD-C7-10 terminal acts. The verdict was **PASS**; the standing claim
> ceiling advanced **Rung 1 → Rung 2 ("beats random-legal")**, bounded strictly to the one ledgered
> same-regime descriptive result. This S05 closeout makes that result durable and understandable; **it
> generates no evidence, edits no ledger row, edits no claim ceiling, and makes no new rung claim.**
>
> **Sanitized note.** No raw traces, simulator logs, deck lists, card IDs/names, Pokémon Elements,
> Competition Data, Daily-Top-Episodes, run-dir dumps, PDFs/CSVs, `deck.csv`, `cg/`, raw evidence rows,
> the local summary JSON, per-batch tables, inferential statistics (no p-value, confidence interval,
> hypothesis test, std-dev, variance, or model estimate), the numeric governance threshold `M`, or any
> forbidden agent word (*strong / competitive / optimal / calibrated / complete*) appears in this
> closeout. Evidence lives only in local/gitignored run dirs and the local/gitignored summary; this
> closeout cites it by **reference + content hash + sanitized names only**.

| Field | Value |
|---|---|
| **Cycle / Sprint** | Cycle-007 / Sprint **S05 — Closeout** |
| **Type** | Closeout artifact (docs) |
| **Date** | 2026-06-20 |
| **Cycle outcome** | **PASS** — Rung-2 admission attempt succeeded under the pre-registered descriptive disjoint-bands rule |
| **Final verdict (cycle)** | **PASS → Rung 2 earned and claimed** |
| **Status** | **CLOSED / operator-accepted / committed / pushed** (terminal chain durable on `origin/main`) |
| **Claim ceiling** | **Rung 2 — "beats random-legal"** (advanced from Rung 1 this cycle; bounded to the one ledgered scope) |
| **Final HEAD / origin/main** | `45e31ca35740950b20749d7a2cca67e11560173d` |
| **`docs/ledger.md` hash (final)** | `7da7e9a8dbed6561669d1569445eb9fe67a953fb` (`git hash-object`, LF-normalized) |
| **`docs/claim-ceiling.md` hash (final)** | `3d99759b919f7d75bc41ea81cd82e5f1fb974be7` (`git hash-object`, LF-normalized) |

---

## 1. Final outcome

Cycle-007 is **closed as Rung 2 earned and claimed.** The standing claim ceiling is now **Rung 2 —
"beats random-legal."** It is earned **only** to this narrow, ledgered extent:

- **Scope (same-regime, descriptive).** The candidate `scripted-v001` beats the `random_legal-v001`
  baseline under the frozen `regime-v003`, with the candidate's per-batch win-rate band strictly above
  the baseline's by at least the pre-registered descriptive margin `M` across the pre-registered
  `K = 20` same-regime batches at `n = 500` (the ratified §16.3 descriptive **disjoint-bands** rule).
  This is a **same-regime delta only** — no inferential statistic, no episode-derived claim, and no
  forbidden agent word applies even on this PASS.
- **Authority.** The committed **Rung-2 ledger row** in `docs/ledger.md` (row commit `399bbf01…`).
  `docs/ledger.md` remains the **only ceiling-bearing artifact**; `docs/claim-ceiling.md` only states
  the standing posture and points at the ledgered basis.

**What Rung 2 does NOT grant** (the advance is bounded to the ledgered "beats random-legal" scope —
nothing more):

- **No Rung 3**, and no claim beyond "beats random-legal" under `regime-v003`.
- **No calibration** improvement, no win-probability reliability, no value model.
- **No tournament or meta strength**, no leaderboard standing, no absolute strength.
- **No runtime-agent maturity** — `scripted-v001` is an existing frozen agent re-run to *generate
  evidence*; no agent, heuristic, search, or learning system was built or tuned.
- **No FunSearch / RL / self-play / deck-optimization / MCTS / value-model outcome** of any kind.
- **No general Pokémon TCG strength** beyond this ledgered Rung-2 scope.

The Rung-2 standing holds **only** because the pre-registered same-regime comparison PASSed **and** the
three separate ledgered terminal acts (SP-6 → Rung-2 row → ceiling advance) were each taken in order
under OD-C7-10. A FAIL or INCONCLUSIVE would have advanced nothing.

## 2. Durable commit chain

Every commit below is verified an ancestor of the final HEAD `45e31ca…` with the subject shown. The
chain is the durable, tamper-evident record of the cycle.

| Step | Commit | Subject |
|---|---|---|
| **Planning baseline** | `1bfd773b647a1e0a2ddb69cadf6aa7e942b49bb0` | `docs: plan TurnTrace Cycle-007` (PRD + SDD + sprint plan; parent `48a69fc`) |
| **S01 gate-pin** | `ceb6f673c9b6fe5a0c1c2e372de0ea6be8ce91c1` | `test: pin promotion-check absent hashes` |
| **S02 pre-registration** | `a27aef38db5cded5120c4eb923f6a7e8cd27a6e2` | `docs: pre-register Cycle-007 Rung-2 attempt` |
| **S03 admissibility / provenance** | `3f6dcd9bfdebe7dfb1c323266c99e14134006018` | `docs: record Cycle-007 S03 admissibility evidence` |
| **S04 PASS verdict** | `a1466ba133e133bf02e0845c4639f1c0aedd5b8a` | `docs: record Cycle-007 S04 PASS verdict` |
| **OD-C7-10 act 1 — SP-6** | `d445141b5f60c458a78f6e6891082ce70bf252f2` | `docs: promote Cycle-007 SP-6 summary` (touched only `06a-sp6-promoted-summary.md`) |
| **OD-C7-10 act 2 — Rung-2 ledger row** | `399bbf01308dfa2fbd982b6f3b4f71730af53472` | `docs: record Cycle-007 Rung-2 ledger row` (touched only `docs/ledger.md`, +1 row) |
| **OD-C7-10 act 3 — claim-ceiling advance** | `45e31ca35740950b20749d7a2cca67e11560173d` | `docs: advance Cycle-007 claim ceiling to Rung 2` (touched only `docs/claim-ceiling.md`) |

The three terminal commits are each **single-file** commits in the SP-6 → row → ceiling order — the
OD-C7-10 separation made durable in history. This S05 closeout, if committed by the operator, would be
a separate later commit; **no S05 commit/push is taken in this pass** (§10).

## 3. S00 continuity (parity with Cycle-006)

For durable parity with the Cycle-006 closeout's verdict-chain record, the **S00 — Preflight & invariant
verification** outcome is recorded here (the S00 implementation/review/audit reports are local/gitignored
State-Zone artifacts, §8; this closeout is their durable tracked surface):

- **Implementation:** complete — all preflight invariant checks passed; zero execution acts; no code /
  test / evidence / eval / ledger / ceiling change; OD-C7-3 surfaced as the operator's to open.
- **Review:** **PASS WITH NOTES** (0 blocking findings; non-blocking notes carried to S05).
- **Audit:** **PASS WITH NOTES — approved** (0 security findings; 0 blocking; non-blocking notes carried
  to S05).
- **Acceptance:** **accepted by operator** (decision recorded 2026-06-19).

**Planning baseline SHA:** the authorizing baseline after the Cycle-007 planning docs landed is
`1bfd773b647a1e0a2ddb69cadf6aa7e942b49bb0` (`docs: plan TurnTrace Cycle-007`, parent `48a69fc`, three
docs, pushed to `origin/main`). Recording it here fulfills the S00 review carry-forward to "name the SHA
in the S05 closeout" and to provide the durable, tracked audit trail of the S00 baseline that the local
(gitignored) S00 report deferred to closeout by design.

## 4. Sprint-by-sprint summary

| Sprint / act | What it did | Verdict |
|---|---|---|
| **S00 — Preflight & invariant verification** | Verified baseline invariants; surfaced OD-C7-3 (Rung-2 attempt gate) as the operator's to open; no execution act. | impl complete → review PASS WITH NOTES → audit PASS WITH NOTES → operator-accepted |
| **S01 — Gate-pin (absent-`hashes`)** | Pinned the `--promotion-check` absent-`hashes` regression so the promotion gate's integrity-stamp floor is test-enforced before any real promotion relied on it. | landed at `ceb6f67…`; review/audit PASS WITH NOTES |
| **S02 — Pre-registration record** | Froze the **one** comparison tuple `(candidate scripted-v001, baseline random_legal, regime-v003, M, K=20, n=500, stopping rule)` and the §11 tightenings — "**`M` before bands**" — committed before any fresh band existed. | committed `a27aef3…`; review/audit PASS WITH NOTES |
| **S03 — Fresh same-regime evidence + gate** | Under OD-C7-9, generated the fresh `regime-v003` batch (40 local/gitignored run dirs; one local/gitignored summary) and ran both admissibility gates — **admissibility only**, no verdict. | committed `3f6dcd9…`; review/audit PASS (WITH NOTES) |
| **S04 — Verdict application** | Applied the pre-registered §16.3 disjoint-bands rule to exactly the one tuple; re-checked both gates; recorded the verdict. | **PASS**; committed `a1466ba…`; review/audit PASS WITH NOTES |
| **OD-C7-10 act 1 — SP-6** | Promoted the sanitized evidence summary to tracked status by reference + content hash + sanitized names (never raw content). | committed `d445141…` |
| **OD-C7-10 act 2 — Rung-2 ledger row** | Appended exactly one Rung-2 `regime-v003` row to `docs/ledger.md` (18-column schema verbatim, append-only, cites the promoted summary by reference + hash). | committed `399bbf0…` |
| **OD-C7-10 act 3 — claim-ceiling advance** | Advanced `docs/claim-ceiling.md` to **Rung 2**, bounded to the ledgered "beats random-legal" scope. | committed `45e31ca…` |
| **S05 — Closeout** | This artifact: state the outcome, verify the ordering held, confirm invariants, record carry-forwards — no evidence, no ledger/ceiling edit, no new claim. | this report |

## 5. Evidence / admissibility summary (sanitized — by reference)

The fresh evidence and its admissibility are recorded durably in the tracked S03 and S04 reports; this
closeout summarizes them by **reference** and does **not** restate band/dispersion/win-rate values or
embed any local summary content.

- **Fresh same-regime batch (S03).** Exactly `K = 20` batches per side at `n = 500` matches per batch
  per agent, all under the one new frozen `regime-v003`; baseline `random_legal-v001`
  (`run-v003-b-1 … -20`) and candidate `scripted-v001` (`run-v003-c-1 … -20`) — 40 sealed run dirs,
  all local/gitignored. The stopping rule was honored (exactly K=20 read, then stop; no top-up, no
  optional stopping, no candidate swap, no `M` change). Detail:
  `docs/cycles/cycle-007/05-evidence-generation-report.md` @ `3f6dcd9…`.
- **Admissibility (S03/S04).** Both gates exit `0` on the local summary —
  `python analysis/evidence_summary.py --validate <local-summary>` and `--promotion-check
  <local-summary>` — establishing schema-conforming, sanitized, single-regime admissibility with a
  non-empty integrity stamp. The gates write nothing and promote nothing.
- **Integrity stamp (S03 carry-forward wording).** The summary's integrity stamp consists of **40 run
  entries bound to 2 per-side config/source digests** (every value a 64-hex SHA-256), i.e.
  provenance-per-*side* over the 40 distinct `run_id`s — the wording validated by the S03/S04 reports.
- **Verdict surface (S04).** The PASS rests on the descriptive disjoint-bands condition: the candidate's
  per-batch win-rate band lies strictly above the baseline's by at least the pre-registered descriptive
  margin `M`, using allowed descriptive vocabulary only (no inferential statistic). The minimal
  descriptive surface (per-batch `min`/`max` and their difference) is already disclosed in
  `docs/cycles/cycle-007/06-verdict-application.md` §6–§7 (@ `a1466ba…`) and carried in
  `docs/cycles/cycle-007/06a-sp6-promoted-summary.md` §6 (@ `d445141…`); it is **referenced, not
  repeated, here**.
- **Source summary content digest:** sha256
  `60d3c8afeba121e8884a5493989b8633fa6ae4116bf2a60b8537f15c2acb0ddf` (the local/gitignored
  `.run/s03-gen/evidence-summary-regime-v003.json`; promoted by reference + this hash in SP-6, cited by
  reference + this hash in the Rung-2 ledger row). The numeric governance threshold `M` lives **only**
  in `docs/cycles/cycle-007/04-pre-registration.md` §2 and is not restated here.

## 6. Governance summary (gate-ordering audit — all cases)

The binding ordering constraints all held; no terminal act preceded its gate:

- **O1 satisfied — "`M` before bands."** The S02 pre-registration commit `a27aef38…` is **strictly
  ancestral** to the S03 generation commit `3f6dcd9…` (`git merge-base --is-ancestor a27aef3 3f6dcd9` →
  exit `0`), and the S02 commit touched only `04-pre-registration.md` (no run-dir / evidence / regime
  path). The full tuple — including `M` — was frozen **before** any `regime-v003` band existed;
  tamper-evident in history.
- **O2 satisfied — gate-pin before reliance.** The S01 absent-`hashes` gate-pin landed at `ceb6f67…`
  **before** `--promotion-check` was relied on to admit the fresh summary in S03/S04 and before the SP-6
  promotion.
- **OD-C7-9 satisfied — fresh-evidence authorization scoped to S03 only.** The eval-scope lane (NG12/
  NFR-8 runtime-agent lane stays closed) was opened only for S03 generation; it authorized no verdict
  and no terminal act.
- **OD-C7-10 satisfied — three separate ordered acts.** SP-6 (`d445141…`) → Rung-2 ledger row
  (`399bbf0…`) → claim-ceiling advance (`45e31ca…`) were each a separate, single-file, individually
  operator-authorized commit, in order.
- **No terminal act occurred before PASS.** SP-6, the ledger row, and the ceiling advance all post-date
  the S04 PASS verdict commit `a1466ba…`. Ledger and claim-ceiling boundaries were preserved: the ledger
  gained exactly one appended Rung-2 row (no past-row edit), and the ceiling advanced exactly one rung,
  bounded to the ledgered scope.

## 7. Final hashes & invariant verification (S05 command results)

Verified against actual command output at S05 (this pass):

| Invariant | Command | Result |
|---|---|---|
| **Final HEAD** | `git rev-parse HEAD` | `45e31ca35740950b20749d7a2cca67e11560173d` (== `origin/main`; not behind) |
| **Ledger hash (final)** | `git hash-object docs/ledger.md` | `7da7e9a8dbed6561669d1569445eb9fe67a953fb` |
| **Claim-ceiling hash (final)** | `git hash-object docs/claim-ceiling.md` | `3d99759b919f7d75bc41ea81cd82e5f1fb974be7` |
| **Claim ceiling reads Rung 2** | read `docs/claim-ceiling.md` | "Current standing ceiling: Rung 2 — beats random-legal" ✓ |
| **Exactly one Rung-2 `regime-v003` row** | inspect `docs/ledger.md` | one appended `regime-v003` Rung-2 row; prior `regime-v001` rows unedited ✓ |
| **System Zone clean** | `git diff --exit-code -- .claude/` | clean ✓ |
| **State-Zone dirt unstaged** | `git status --porcelain` | only ` M .beads/issues.jsonl` and ` M grimoires/loa/NOTES.md` (pre-existing, unstaged) ✓ |
| **Nothing staged** | `git status --porcelain` | no staged entries ✓ |

For audit completeness, the **prior Rung-1 baseline** hashes (before the terminal acts) were
`docs/ledger.md` = `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` and `docs/claim-ceiling.md` =
`b914ca1b89fdd539da4d19d008231ac9f00c45ee` (recorded in the S03/S04/SP-6 reports). The advance to the
final hashes above is accounted for by exactly the two single-file terminal commits `399bbf0…`
(ledger row) and `45e31ca…` (ceiling), and nothing else.

**Commit/push at S05:** none. This closeout authors `docs/cycles/cycle-007/07-closeout.md` only and is
**not staged, committed, or pushed** in this pass; the operator may commit it separately. The durable
Rung-2 chain (§2) was already committed and pushed under its own per-act authorizations.

## 8. State-Zone report inventory

Per-sprint implementation, review, and audit reports exist locally under
`grimoires/loa/a2a/cycle-007/…` — for `sprint-00`, `sprint-01`, `sprint-02`, `sprint-03`, `sprint-04`,
`sprint-04-sp6`, `sprint-04-ledger-row`, `sprint-04-claim-ceiling`, and this closeout's
`sprint-05/01-implementation-report.md`. These are **gitignored State-Zone artifacts** (`.gitignore`
`grimoires/loa/a2a/`) and are **not part of the durable tracked surface.** The tracked, durable record
of the cycle is the `docs/cycles/cycle-007/` series (`01-prd` … `06-verdict-application`,
`06a-sp6-promoted-summary`, this `07-closeout`), plus `docs/ledger.md` and `docs/claim-ceiling.md`.

## 9. Carry-forwards (non-blocking, for Cycle-008)

Concise and non-blocking; none gates this closeout:

1. **Formalize the SP-6 / closeout numbering convention.** SP-6 was authored as `06a-sp6-promoted-summary.md`
   (immediately after `06-verdict-application.md`) specifically to avoid colliding with the reserved
   `07-closeout.md`. Document this `NNa-` insertion convention so future cycles avoid `07-` path
   ambiguity.
2. **Ledger metric-column convention.** The Rung-2 row discloses metric *names* with `see cited summary`
   in the numeric columns (no per-batch band values, no `M` leak). If a future convention ever needs
   embedded numeric values, update the convention deliberately while preserving the **"see cited
   summary" by-reference + content-hash safety pattern**.
3. **Mechanize ledger-row validation.** The Rung-2 row was appended via a guarded binary-append script
   (pre-append blob-hash match; idempotent regime-absence check; tail/column checks), but there is no
   *tracked* ledger-schema validator (`eval/hygiene_check.py` is path-based and does not content-check
   the ledger; existing tests use throwaway ledgers). Consider a tracked ledger-row validator.
4. **Preserve the no-raw-data / no-Pokémon-elements tracked-docs discipline.** The strict separation
   (evidence local/gitignored; governance cites by reference + content hash + sanitized names) held
   across the whole cycle and must continue to.

## 10. Explicit non-acts (this S05 pass)

This S05 closeout pass:

- generated **no** evidence (no eval, no run, no band read);
- made **no** additional `docs/ledger.md` edit (byte-unchanged at `7da7e9a8…`);
- made **no** additional `docs/claim-ceiling.md` edit (byte-unchanged at `3d99759b…`; still Rung 2);
- made **no** new rung claim and widened **no** scope;
- did **no** runtime-agent work, and **no** FunSearch / RL / self-play / deck-optimization / MCTS /
  value-model work;
- made **no** `.claude/` (System Zone) edit;
- staged, cleaned, or committed **no** State-Zone dirt (`.beads/issues.jsonl` and
  `grimoires/loa/NOTES.md` remain modified-unstaged);
- staged, committed, or pushed **nothing** (the only change introduced is this tracked closeout file).

---

> **Closeout statement (binding).** Cycle-007 is **CLOSED and operator-accepted** with cycle outcome
> **PASS**. The pre-registered same-regime descriptive disjoint-bands comparison PASSed: under
> `regime-v003` at `n = 500` over `K = 20` batches, the candidate `scripted-v001` beats the
> `random_legal-v001` baseline by at least the pre-registered descriptive margin `M` — a same-regime
> descriptive delta only, with no inferential statistic and no forbidden agent word. On that PASS the
> three OD-C7-10 terminal acts were taken in order — **SP-6 (`d445141…`) → Rung-2 ledger row
> (`399bbf0…`) → claim-ceiling advance (`45e31ca…`)** — each a separate single-file operator-authorized
> commit. The standing claim ceiling is now **Rung 2 — "beats random-legal,"** bounded strictly to this
> one ledgered scope: **no Rung 3, no calibration, no tournament/absolute strength, no runtime-agent
> maturity, no FunSearch/RL/self-play/deck-optimization, and no general Pokémon TCG strength.** O1
> ("`M` before bands"), O2 (gate-pin before reliance), OD-C7-9 (fresh evidence in S03 only), and
> OD-C7-10 (three separate ordered acts, none before PASS) all held; ledger and claim-ceiling boundaries
> were preserved. `docs/ledger.md` = `7da7e9a8dbed6561669d1569445eb9fe67a953fb` and `docs/claim-ceiling.md`
> = `3d99759b919f7d75bc41ea81cd82e5f1fb974be7` at final HEAD `45e31ca35740950b20749d7a2cca67e11560173d`.
> **This S05 closeout generated no evidence, edited no ledger row, edited no claim ceiling, did no
> runtime-agent work, and touched no `.claude/`.**
