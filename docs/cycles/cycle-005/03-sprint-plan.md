# Cycle-005 Sprint Plan — Promotion-Gate Hardening (C1–C4)

> Planning artifact (Sprint Plan). Status: **DRAFT — awaiting operator acceptance + build gate.** This sprint
> plan translates the accepted Cycle-005 PRD + SDD into one focused implementation sprint. It **opens no
> implementation gate**: code lands only through
> `/architect → /sprint-plan → /implement → /review-sprint → /audit-sprint → operator acceptance`
> (`docs/operator/turntrace-loop-contract.md` §6, the OA-2-class build gate). **Cycle-005 attempts no Rung 2,
> promotes no value, and mutates neither the ledger nor the claim ceiling.**
>
> **Sanitized note.** No raw traces, card IDs/names, deck lists, hand contents, simulator logs, PDFs/CSVs,
> `deck.csv` rows, run-dir dumps, Pokémon Elements, Daily-Top-Episode data, or Competition Data appear here
> (CC-1/CC-2, ESP, SP-6/SP-9). **No dispersion metric values appear here** — evidence stays local/gitignored and
> is referenced qualitatively only. Runs are referenced by `run_id` pattern, count, hashes, sanitized metric
> *names*, claim ceilings, and local path/status only. The forbidden agent words (*strong / competitive /
> optimal / calibrated / complete*) and the inferential terms (*std-dev / variance / CI / p-value / significance
> / hypothesis-test / error-bar*) appear only as the negated/forbidden language they are.

| Field | Value |
|---|---|
| **Cycle** | Cycle-005 |
| **Working title** | Promotion-Gate Hardening (C1–C4) |
| **Type** | Sprint Plan (implementation roadmap for one hardening sprint) |
| **Status** | DRAFT — awaiting operator acceptance; next Golden-Path step is `/implement` (under a later build gate) |
| **Date** | 2026-06-19 |
| **Current main** | `337fc4f` — *docs: record TurnTrace competition findings* (== `origin/main`) |
| **Primary authorities** | `docs/cycles/cycle-005/01-prd.md` (accepted PRD); `docs/cycles/cycle-005/02-sdd.md` (accepted SDD) |
| **Posture** | **Hardening-only.** Modify exactly `analysis/evidence_summary.py` + `tests/test_evidence_summary.py` for C1–C4; hold every other bright line. |
| **Claim ceiling** | **Rung 1** (held for the whole cycle; not raised). |
| **Ledger** | `docs/ledger.md` byte-unchanged; hash `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`. |

---

## Preflight verification (recorded at authoring, HEAD `337fc4f`)

| Check | Command | Result | Verdict |
|---|---|---|---|
| HEAD / branch | `git rev-parse HEAD` | `337fc4ff6b2cb628779b1898e51674036c51427d` | ✓ `337fc4f` |
| Working tree | `git status --porcelain` | ` M .beads/issues.jsonl` · ` M grimoires/loa/NOTES.md` · `?? docs/cycles/cycle-005/` | ✓ only pre-existing State-Zone + untracked Cycle-005 planning docs |
| Not behind origin | `git ls-remote origin main` | `337fc4f…` | ✓ equal (not behind) |
| Ledger byte-unchanged | `git hash-object docs/ledger.md` | `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` | ✓ |
| Ledger diff clean | `git diff --exit-code -- docs/ledger.md` | exit 0 | ✓ |
| Protected-path drift | `git status --porcelain .claude/ frozen/ runs/ agents/ sim/ analysis/ tests/` | empty | ✓ no tracked drift |
| Build target present | source read | `analysis/evidence_summary.py` (511 lines) + `tests/test_evidence_summary.py` (289 lines, 12 checks) tracked + accepted | ✓ |

**All preflight expectations hold. No finding forces a stop.** Implementation remains un-authorized until the
operator accepts the PRD/SDD and opens the build gate.

---

## Executive summary

Cycle-004 built the offline evidence-summary generator (`build_summary`) plus an independent fail-closed
validator (`validate_summary` + the `--validate` re-read mode) and closed **accepted, pushed, at Rung 1**,
promoting nothing (`docs/cycles/cycle-004/07-closeout.md`). The Cycle-004 audit recorded **four pre-promotion
hardening carry-forwards (C1–C4)** as non-blocking for the build-only cycle but **mandatory before the validator
becomes load-bearing at any value-promotion gate** (`docs/cycles/cycle-004/06-audit-report.md` §9). Cycle-005 is
the cycle that lands exactly those four hardenings.

**Mission (binding).** Harden `analysis/evidence_summary.py` and `tests/test_evidence_summary.py` exactly as the
SDD designed, so the validator becomes **strictly more conservative, never looser**, before any future
value-promotion gate — while holding Rung 1, leaving `docs/ledger.md` byte-unchanged, promoting no value,
attempting no Rung 2, and deferring the Rung-2 admission seam (8a–8d) to a separate later gate (Cycle-006+).

**Sprint count: 1** (single focused sprint). The hardening touches one module + its test file; there is no
architectural seam that justifies a split (same single-sprint rationale as Cycle-004,
`docs/cycles/cycle-004/03-sprint-plan.md`). If repo reality at build time proves a split is necessary, the
implementer MUST stop and report rather than expand scope silently.

| Sprint | Title | Scope | Tasks |
|---|---|---|---|
| **Sprint 01** | Promotion-Gate Hardening C1–C4 | **MEDIUM** | T1–T7 (7 tasks) |

---

## Binding posture (carried verbatim-in-intent from PRD §"Required posture" + SDD §15)

Cycle-005 is **hardening-only.** Across the whole cycle the sprint preserves **all** of:

- **No Rung-2 attempt.** No "beats random-legal" verdict of any kind.
- **No Rung-2 admission.** No same-regime admission verdict is written or implied.
- **No Rung-2 ledger row.** `docs/ledger.md` stays byte-unchanged at its two Rung-1 `regime-v001` rows.
- **No claim-ceiling advance.** `docs/claim-ceiling.md` unchanged; the ledger remains the only ceiling-bearing
  artifact.
- **No numeric margin `M`** chosen anywhere.
- **No SP-6** live-value promotion; no dispersion value reaches tracked status.
- **No OD-6 decision / relaxation;** no inferential statistic computed (the validator *rejects* inferential
  terms; it does not produce them).
- **No same-regime evidence verdict.**
- **No new eval runs; no K=50 top-up; no K expansion; no paired-delta tooling** (NG12 carried).
- **No runtime-agent work;** agents stay frozen.
- **No gameplay-heuristic work;** no broad optimization (RL, self-play, deck optimizer, value/win-probability
  model, search/MCTS, ELO/tournament, dashboard, leaderboard).
- **No Daily Top Episodes ingest;** no Kaggle automation. Daily Top Episodes remain local-only hypothesis input,
  never proof of improvement (SP-9).
- **No FunSearch work** (no dependency, interface, scaffold, integration, or candidate-search surface).
- **No broad refactor** of TurnTrace; the only tracked code touched is the two evidence-summary artifacts.
- **No `.schema.json`** file.
- **No second validator module** (`analysis/evidence_summary_validate.py`).
- **No third-party dependency** — the in-module constant and stdlib-only posture are preserved.
- **No `.claude/` (System Zone) edits.**
- **No State-Zone cleanup;** pre-existing dirty State-Zone files stay unstaged and untouched.
- **No raw Competition Data / Pokémon Elements / traces / card names / deck lists / simulator logs.**
- **No ledger mutation. No claim-ceiling mutation.**

**Rung 1 remains held for the whole cycle.**

The validator becomes **strictly more conservative, not looser** (PRD NFR-1, SDD §2.1). Every change either
rejects more inputs or rejects the same set; no change accepts an input the current validator rejects. The
12 existing checks remain green; generator behaviour stays compatible (only the empty-`hashes` stderr warning is
additive).

---

## Sprint 01 — Promotion-Gate Hardening C1–C4

### Sprint Goal

Harden `analysis/evidence_summary.py` and `tests/test_evidence_summary.py` exactly as designed by the SDD —
landing C1–C4 so the evidence-summary validator becomes strictly more conservative — while holding Rung 1,
leaving the ledger byte-unchanged, and promoting no value.

### Scope: **MEDIUM** (7 tasks)

### The four hardenings (SDD §4, grounded at HEAD `337fc4f`)

- **C1 (priority hard blocker)** — nested-`hashes` digest-shape enforcement. Today `SAFE_FIELDS` is a flat
  field-name allow-list (`analysis/evidence_summary.py:83-88`) and the digest-shape check runs top-level only
  (`:369-379` / shape test `:372`), while `_walk` descends into a `hashes`-keyed dict without enforcing value
  shape at that nested position (`:333-350`). A nested `hashes` map carrying a clean non-digest token passes.
  **Decision (OD-C5-1): traversal-based enforcement, in-module, no schema rewrite.**
- **C2** — forbidden-word negation hardening. Today a broad 36-char window (`_NEG_WINDOW = 36`, `:263`; window
  scan `:303`; `_affirmative_forbidden_words` `:298-306`) lets an unrelated negation suppress an affirmative
  forbidden word. **Decision: immediate-precedence negation (or equivalently tighter rule).**
- **C3** — repo-root-resolved `--out` guard. Today `_refuse_tracked_out` (`:410-421`) tests a
  normalized-but-not-repo-resolved path (`_norm_path` `:282-283`); an absolute path into repo `docs/` for a
  non-`ledger.md` file slips the prefix check. **Decision: repo-root-resolve `--out` before the prefix check,
  using `REPO_ROOT` (`:57`).**
- **C4** — empty-`hashes` warning. Today `_manifest_run_hash` returns `None` when no 64-hex `*_hash` is present
  (`:117-132`); `hashes[run_id]` is never set (`:180-182`); `hashes` degrades to `{}` silently and
  `validate_summary` accepts it as clean (`:369-370`). **Decision (OD-C5-2/OD-C5-5): generator emits a stderr
  warning on empty `hashes`; `--validate` still accepts empty `hashes` at exit 0; no new exit code; no
  `--promotion-check` mode this cycle.**

> **Anchor caveat (NFR-9 / SDD §5.1).** Every line anchor above is line-anchored to `analysis/evidence_summary.py`
> at HEAD `337fc4f`. `/implement` MUST re-validate each anchor it relies on against the **build-time HEAD** before
> coding; anchors accurate now may desync if the file moves.

### Deliverables

- [ ] C1 — `_enforce_hashes_digest` (or equivalent helper) added and wired into `_walk` for **every**
  `hashes`-keyed dict at any depth; top-level digest block + flat `SAFE_FIELDS` preserved; no schema rewrite, no
  `.schema.json`, no new dependency. → **[G-1]**
- [ ] C2 — `_affirmative_forbidden_words` negation test replaced with immediate-precedence (or equivalently
  tighter) negation; `_NEG_WINDOW` removed/repurposed; `_NEGATION_RE` token set preserved; legitimate
  negated/forbidden-language examples preserved. → **[G-2]**
- [ ] C3 — `_refuse_tracked_out` resolves `--out` against repo root before the tracked-`docs/` prefix check;
  absolute repo `docs/` paths refused; relative `docs/` refusal and the `ledger.md` basename guard both
  preserved; local/gitignored output still allowed. → **[G-3]**
- [ ] C4 — generator emits a stderr `WARNING` when assembled `hashes` is empty; manifest-only sourcing preserved
  (no `hashes.txt` read); `--validate` still accepts empty `hashes` at exit 0; no new exit code; no
  `--promotion-check` mode. → **[G-4]**
- [ ] Regression tests — new block `# --- 13. C1–C4 hardening ---` with checks 13a–13l (SDD §5.2) added to
  `tests/test_evidence_summary.py`; all 12 existing checks preserved unmodified; stdlib-only synthetic fixtures;
  no local K-batch dependency; no raw data. → **[G-5]**
- [ ] `docs/cycles/cycle-005/04-implementation-report.md` written with the full evidence set (see "Implementation
  report requirements"). → **[G-6]**

### Acceptance Criteria (SDD §12 / PRD §14.2, AC-1 … AC-8)

- [ ] **AC-1 — C1 (priority):** a **nested** `hashes` map carrying a clean non-digest token is **rejected**
  (fail-closed, exit 3); digest-shape is enforced at every position; a nested **valid** digest is not falsely
  flagged as a digest violation; the top-level digest path still rejects non-digests.
- [ ] **AC-2 — C2:** an unrelated negation no longer suppresses an affirmative forbidden word (`strong` now
  flagged, exit 3); an immediate negation (and legitimate negated/forbidden-language examples) still validate; no
  affirmative quality claim is admitted.
- [ ] **AC-3 — C3:** an absolute path into repo `docs/` (non-ledger) is **refused**; relative `docs/` and the
  `ledger.md` basename are still refused; a safe local path is still allowed; `docs/ledger.md` byte-unchanged.
- [ ] **AC-4 — C4:** an empty `hashes` is **not silently accepted** — generate emits a stderr `WARNING` and exits
  0; non-empty `hashes` emits no warning; manifest-only sourcing preserved; **no `hashes.txt` read**.
- [ ] **AC-5 — Tests:** each of C1–C4 has at least one runnable regression check (block 13); **all existing 12
  checks remain green**; `tests/test_import_direction.py` green; `python eval/hygiene_check.py --paths …` exit 0
  on tracked artifacts.
- [ ] **AC-6 — Conservative-only / compatible:** the validator is strictly stricter-or-equal; generator behaviour
  stays compatible (only the empty-`hashes` warning is additive).
- [ ] **AC-7 — Posture held (hard):** Rung 1 held; `docs/ledger.md` byte-unchanged (`2a2f1c2…`);
  `docs/claim-ceiling.md` unchanged; no value promoted; stdlib-only / analysis-only imports; no `M`/SP-6/Rung-2
  row; no `.claude/` drift; State-Zone files unstaged; no second module / `.schema.json` / dependency; no new
  exit code.
- [ ] **AC-8 — Cadence:** lands through `/implement → /review-sprint → /audit-sprint → operator acceptance`, so
  the hardened gate is **reviewed and audited before any Rung-2 attempt**.

### Technical Tasks (ordered)

> Each task lists its goal contribution `→ [G-N]`. T1 is preflight + anchor revalidation; T2–T5 are the four
> hardenings in SDD-ordered sequence (C1 priority first); T6 is tests; T7 is final gates + report. The
> implementer follows the SDD §5.1 surgical order.

#### T1 — Preflight + anchor revalidation → **[G-1…G-6]**

- [ ] Verify build-time HEAD is `337fc4f` or a descendant containing it; local branch not behind `origin/main`.
- [ ] Verify `git hash-object docs/ledger.md == 2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b` and
  `git diff --exit-code -- docs/ledger.md` clean.
- [ ] Verify protected paths show no tracked drift:
  `git status --porcelain .claude/ frozen/ runs/ agents/ sim/`.
- [ ] Verify no staged files: `git diff --cached --name-only` empty.
- [ ] **Revalidate every SDD source anchor** against build-time HEAD (NFR-9): `SAFE_FIELDS` (`:83-88`),
  `_SHA256_RE` (`:107`), `_manifest_run_hash` (`:117-132`), `build_summary` hashes set (`:180-182`),
  `_NEG_WINDOW` (`:263`), the 36-char window scan (`:303`), `_norm_path` (`:282-283`),
  `_affirmative_forbidden_words` (`:298-306`), `_walk` (`:333-350`), `validate_summary` top-level digest block
  (`:369-379`), `_refuse_tracked_out` (`:410-421`), `REPO_ROOT` (`:57`), `main` (`:456`). In the test file:
  `_HEX64` (`:33`), `make_run_dir` (`:49`) with `manifest_hash` default (`:51`), `validate_file_exit` (`:75`),
  `run_checks` (`:87`), the 12 numbered blocks, the "all 12 required checks" summary line (`:284`).
- [ ] Confirm no repo reality contradiction. If any anchor has desynced or repo reality contradicts the SDD,
  **STOP and report** the concrete discrepancy before coding — do not silently adapt.

#### T2 — C1 nested-`hashes` digest-shape enforcement → **[G-1]** (PRIORITY)

- [ ] Add `_enforce_hashes_digest(field_path, hashes_dict, out)` (or an equivalent helper) beside `_scan_string`,
  mirroring its `out.append((field, reason))` contract; reject any value that is not a SHA-256 digest string with
  the **same reason message** the existing top-level block uses (so test assertions keyed on
  `"Pokemon-Element"` / `"SHA-256 digest"` match at any position).
- [ ] Call it from `_walk` whenever a key `k == "hashes"` and its value is a dict, **in addition to** the existing
  recursive descent; retain the existing `keys_are_fields=(k != "hashes")` recursion so child keys (run_ids) are
  still scanned as data.
- [ ] **Preserve** the top-level digest block in `validate_summary` (`:369-379`) for back-compat parity (it
  becomes redundant-but-harmless once traversal enforcement runs, and keeps the top-level test path green).
- [ ] **Preserve** the flat `SAFE_FIELDS` allow-list unchanged.
- [ ] **No schema rewrite. No `.schema.json`. No new dependency.**
- [ ] Conservative-only proof: C1 adds rejections (nested non-digest values now fail) and removes none; a nested
  **valid** digest still passes; the generator emits `hashes` only at top-level, so no generator output regresses.

#### T3 — C2 forbidden-word negation hardening → **[G-2]**

- [ ] Replace the broad 36-char negation window scan in `_affirmative_forbidden_words` (`:298-306`) with an
  **immediate-precedence** rule (or an equivalently tighter rule): a forbidden word is suppressed only when a
  negation token is the immediately preceding token (intervening whitespace/punctuation allowed, no intervening
  content word). E.g. match `(?:\b(no|not|never|non|without|neither|nor)\b|n't)\s*$` against the text immediately
  preceding the word, rather than scanning a 36-char span.
- [ ] Remove or repurpose `_NEG_WINDOW` (`:263`); **preserve** the `_NEGATION_RE` token set.
- [ ] **Preserve legitimate negated/forbidden-language examples** in reports (e.g. `"NO strength claim"`,
  `"never strong"`, `"not optimal"`, validator-rejection examples) — these remain suppressed (valid).
- [ ] Ensure an unrelated negation no longer suppresses an affirmative forbidden word
  (`"claim not made; agent strong"` → `strong` flagged, exit 3).
- [ ] **Never admit** an affirmative agent-quality claim using any of the five forbidden words
  (*strong / competitive / optimal / calibrated / complete*).
- [ ] Conservative-only proof: the tighter rule suppresses a **subset** of what the 36-char window suppressed, so
  it flags a **superset** of affirmative forbidden words — strictly stricter.

#### T4 — C3 repo-root-resolved `--out` guard → **[G-3]**

- [ ] In `_refuse_tracked_out` (`:410-421`), before the prefix check, resolve the candidate `out_path` against the
  repo root (`REPO_ROOT` `:57`) via `Path.resolve()` and refuse if it lands inside the tracked `docs/` tree
  (`resolved == docs_root or docs_root in resolved.parents`).
- [ ] **Refuse** absolute repo `docs/` paths (the new rejection).
- [ ] **Preserve** the relative-`docs/` refusal (existing `docs/x.json` case must still raise).
- [ ] **Preserve** the `ledger.md` basename guard verbatim (existing `a/b/ledger.md` case must still raise) — it
  stays independent and on any path.
- [ ] **Preserve** the local/gitignored output allowance (a safe local temp path must not raise).
- [ ] `docs/ledger.md` protection is unchanged and independent; the primary control
  (`git diff --exit-code -- docs/ledger.md` byte-unchanged) holds regardless of this guard.
- [ ] Conservative-only proof: strictly more paths refused; no previously-refused path becomes allowed.

#### T5 — C4 empty-`hashes` warning → **[G-4]**

- [ ] **Preserve** manifest-only hash sourcing — do **not** change `_manifest_run_hash` (`:117-132`) to read any
  new source. **Do not read `hashes.txt`** (none exists; none is introduced).
- [ ] In `main`'s generate branch, after assembling the summary, check `if not summary.get("hashes"):` and emit a
  stderr `WARNING` line (e.g. `evidence_summary: WARNING — empty hashes (no manifest integrity stamp found); a
  future promotion gate must reject this`). Keep `build_summary` JSON-first on stdout; the warning goes to
  **stderr** so the stdout JSON contract is untouched.
- [ ] **Preserve exit 0** for the warning-only case; `validate_summary` continues to accept an empty `hashes` at
  exit 0 (it is structurally valid, just un-stamped).
- [ ] **Do not introduce a new exit code** — the `0/1/2/3` contract is preserved verbatim (SDD §7).
- [ ] **Do not introduce a `--promotion-check` mode** (OD-C5-3 deferred to Cycle-006+).
- [ ] Conservative-only proof: behaviour for non-empty `hashes` is byte-identical; the empty case gains only a
  stderr warning, same exit 0, same emitted JSON shape.

#### T6 — Test updates → **[G-5]**

- [ ] **Preserve all 12 existing checks** unmodified.
- [ ] Add a new block `# --- 13. C1–C4 hardening ---` inside `run_checks(tmp)` after block 12; update `main()`'s
  summary line from "all 12 required checks" to the new total.
- [ ] Add regression checks **13a–13l** as designed in SDD §5.2:

  | Check | Asserts | Maps to |
  |---|---|---|
  | **13a** C1 — nested non-digest rejected | inject `good["agents"][0]["hashes"] = {"r": "clean-non-digest"}`; violation at a nested `hashes.*` path; `validate_file_exit == 3` | AC-1 |
  | **13b** C1 — nested valid digest passes | inject `good["agents"][0]["hashes"] = {"r": _HEX64}`; validates clean OR (if `hashes` nested under `agents` is allow-list-rejected) the rejection reason is the allow-list reason, **not** a digest false-negative | AC-1, NFR-1 |
  | **13c** C1 — top-level digest still enforced | existing top-level non-digest case still `exit 3` | AC-1 |
  | **13d** C2 — unrelated negation no longer suppresses | `claim_ceiling = "claim not made; agent strong"` → flagged `strong`; `exit 3` | AC-2 |
  | **13e** C2 — immediate negation still suppresses | `"never strong"` / `"NO strength claim"`-style → validates clean | AC-2, R4 |
  | **13f** C2 — affirmative still rejected | `"agent is strong"` → flagged | AC-2 |
  | **13g** C3 — absolute repo-docs path refused | `_refuse_tracked_out((REPO_ROOT / "docs" / "x.json"))` raises `ValueError` | AC-3 |
  | **13h** C3 — relative docs + ledger basename still refused | existing `docs/x.json` and `a/b/ledger.md` still raise | AC-3 |
  | **13i** C3 — safe local path still allowed | a gitignored local temp path does **not** raise | AC-3, NFR-1 |
  | **13j** C4 — empty hashes warns, exits 0 | generate with a manifest carrying **no** 64-hex `*_hash`; capture stderr; assert `WARNING`/`empty hashes` line AND exit 0 AND `docs/ledger.md` byte-unchanged | AC-4 |
  | **13k** C4 — non-empty hashes does NOT warn | existing valid-`manifest_hash` fixture: no warning; exit 0 | AC-4, NFR-1 |
  | **13l** C4 — no `hashes.txt` read | source-grep: `"hashes.txt"` absent from `analysis/evidence_summary.py` | AC-4, NFR-4 |

- [ ] Reuse existing fixtures/helpers (`good` summary fixture, `make_run_dir`, `validate_file_exit`, `_HEX64`).
  For 13j, add a `make_run_dir` variant whose manifest carries no 64-hex `*_hash` (e.g. a keyword-only option or a
  small inline manifest) — **stdlib-only, synthetic, no raw data**.
- [ ] **Keep stdlib-only synthetic fixtures.** **No local K-batch dependency. No raw data.**

#### T7 — Final gates + implementation report → **[G-6]**

- [ ] Run the required tests and hygiene checks (see "Required test commands").
- [ ] Verify `docs/ledger.md` byte-unchanged (hash `2a2f1c2…`; `git diff --exit-code` clean).
- [ ] Verify protected paths untouched (`.claude/ frozen/ runs/ agents/ sim/`).
- [ ] Verify nothing staged (`git diff --cached --name-only` empty).
- [ ] Write `docs/cycles/cycle-005/04-implementation-report.md` with the full evidence set below.

### Dependencies

- **Upstream:** accepted Cycle-005 PRD (`docs/cycles/cycle-005/01-prd.md`) + accepted SDD
  (`docs/cycles/cycle-005/02-sdd.md`); an explicit operator build gate (OA-2-class,
  `docs/operator/turntrace-loop-contract.md` §6).
- **Task ordering:** T1 → T2 (C1, priority) → T3 (C2) → T4 (C3) → T5 (C4) → T6 (tests) → T7 (gates + report).
  T6 depends on T2–T5; T7 depends on all prior tasks.
- **Read-only (import-only, never edited):** `analysis/aggregate.py`, `analysis/dispersion_report.py`,
  `eval/hygiene_check.py`.
- **External:** none. Stdlib-only; Python 3.14.0 local. No third-party dependency.

### Risks & Mitigation (SDD §14 / PRD §15)

| ID | Risk | Mitigation |
|---|---|---|
| **R1** | C1 fix loosens the gate (a restructure accidentally accepts something previously rejected). | Traversal enforcement, **not** a schema rewrite; top-level digest block + flat allow-list preserved; 12 existing checks green (AC-5); nested-rejection check 13a (AC-1). |
| **R2** | Scope-creep into admission — hardening drifts into a verdict / `M` / promotion / promotion-mode. | OD-C5-3 defers promotion-mode; §"Binding posture" non-goals; no `M`/SP-6/Rung-2 row; seam 8a–8d untouched; OD-C5-6 reporting language. |
| **R3** | Citation rot — the C1–C4 line anchors desync from source before build. | NFR-9 / T1: `/implement` re-validates anchors at build-time HEAD. |
| **R4** | C2 over-tightening — a legitimate negated/forbidden-language example wrongly flagged. | Immediate-precedence (subset suppression); checks 13e/13f pin both the affirmative-catch and the legitimate-negation-pass. |
| **R5** | Ledger / docs mutation via the generator's `--out`. | C3 repo-root guard; ledger basename guard; `git diff --exit-code -- docs/ledger.md` byte-unchanged (AC-3/AC-7); independent of the guard. |
| **R6** | Dependency / second-module / `.schema.json` creep during the C1 work. | OD-C5-1 traversal-in-module; §"Forbidden files" list; import-direction test (check 12); in-module constant preserved. |
| **R7** | C4 false warning / break of round-trip checks (a valid-hash fixture trips the warning). | Warning only on `hashes == {}`; checks 6/10 use valid `manifest_hash` fixtures (non-empty); check 13k pins no-warning-on-non-empty. |
| **R8** | C3 `Path.resolve()` cwd-sensitivity — a relative path resolved from outside the repo. | Cycle runs from repo root by construction; basename ledger guard preserved on any path; existing relative-`docs/` test preserved (13h). |
| **R9** | FM-10 (official-rule assumption mismatch). | NFR-8 simulator-authoritative; no verdict logic built; record any divergence as a simulator-behavior note, not an agent failure. |
| **R10** | FM-11 (top-episode overfitting / contaminated evidence). | No episode ingest; synthetic fixtures only; raw-data-in-git mechanically caught by `eval/hygiene_check.py` + validator hygiene parity. |

### Success Metrics (quantifiable)

- `python tests/test_evidence_summary.py` exit 0 — all 12 existing checks **plus** 13a–13l green.
- `python tests/test_import_direction.py` exit 0.
- `python eval/hygiene_check.py --paths analysis/evidence_summary.py tests/test_evidence_summary.py docs/cycles/cycle-005/04-implementation-report.md` exit 0.
- `git hash-object docs/ledger.md` == `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`.
- `git diff --exit-code -- docs/ledger.md` exit 0 (byte-unchanged).
- `git status --porcelain .claude/ frozen/ runs/ agents/ sim/` empty (no protected-path drift).
- `git diff --cached --name-only` empty (nothing staged by the implementer).
- Exactly **two** App-Zone code files changed (`analysis/evidence_summary.py`, `tests/test_evidence_summary.py`)
  plus **one** Docs/State report (`docs/cycles/cycle-005/04-implementation-report.md`).

---

## Authorized implementation files

Only these paths are authorized for change in Sprint 01:

| Path | Zone | Authority |
|---|---|---|
| `analysis/evidence_summary.py` | App (tracked) | PRD §5, D-1; SDD §3 |
| `tests/test_evidence_summary.py` | App (tracked) | PRD AC-5; SDD §3, §5.2 |
| `docs/cycles/cycle-005/04-implementation-report.md` | Docs/State | loop contract (written under `/implement`) |

The standard later review/audit reports **may** be created by their own skills (not by the implementer's code
patch):

- `docs/cycles/cycle-005/05-review-report.md` (under `/review-sprint`)
- `docs/cycles/cycle-005/06-audit-report.md` (under `/audit-sprint`)

**No other tracked path is authorized.** If implementation appears to require another file, the implementer MUST
**stop and report** a concrete repo-reality reason before touching it; this sprint plan authorizes none.

## Forbidden files / paths (no change authorized)

The implementer MUST NOT change any of:

- `docs/ledger.md`
- `docs/claim-ceiling.md`
- `.claude/**`
- `runs/**`
- `agents/**`
- `sim/**`
- `frozen/**`
- `grimoires/loa/context/**`
- `deck.csv`
- raw episode datasets / raw data paths
- `analysis/aggregate.py`
- `analysis/dispersion_report.py`
- `analysis/delta_report.py`
- `eval/**`
- dependency / manifest files (`requirements*.txt`, `pyproject.toml`, `setup.cfg`, etc.)
- any `*.schema.json`
- `analysis/evidence_summary_validate.py` (no second validator module)

No `.schema.json`. No second validator module. No third-party dependency. No State-Zone cleanup (pre-existing
dirty `.beads/issues.jsonl` + `grimoires/loa/NOTES.md` stay unstaged, untouched). `analysis/aggregate.py`,
`analysis/dispersion_report.py`, and `eval/hygiene_check.py` remain **import-only** (read, never edited).

---

## Required test commands

The implementer MUST run, and the implementation report MUST record (with exit statuses):

```bash
python tests/test_evidence_summary.py
python tests/test_import_direction.py
python eval/hygiene_check.py --paths analysis/evidence_summary.py tests/test_evidence_summary.py docs/cycles/cycle-005/04-implementation-report.md
git hash-object docs/ledger.md
git diff --exit-code -- docs/ledger.md
git status --porcelain .claude/ frozen/ runs/ agents/ sim/
git diff --cached --name-only
```

**The ledger hash MUST equal `2a2f1c2dc540b6d7e7a68aad5ab3c6b109dcee4b`.** Any ledger-hash drift → HALT and
report.

---

## Implementation report requirements

`docs/cycles/cycle-005/04-implementation-report.md` MUST include:

- **Preflight verification** (HEAD, ledger hash, protected paths, no staged files).
- **Anchor revalidation notes** (each SDD anchor confirmed at build-time HEAD, or the concrete discrepancy that
  forced a stop).
- **Files changed** (exactly the authorized set).
- **C1–C4 implementation summary** (what changed in each, conservative-only proof per hardening).
- **C1–C4 test summary** (13a–13l outcomes; the 12 existing checks remain green).
- **Exact commands run and exit statuses** (the full Required-test-commands block).
- **Proof ledger hash unchanged** (`git hash-object docs/ledger.md` == `2a2f1c2…`; `git diff --exit-code` clean).
- **Proof claim ceiling unchanged** (`docs/claim-ceiling.md` untouched).
- **Proof protected paths untouched** (`.claude/ frozen/ runs/ agents/ sim/` no drift).
- **Proof no raw data added** (no Competition Data / Pokémon Elements / traces / card names / deck lists /
  simulator logs / Daily-Top-Episode data; synthetic fixtures only; hygiene-check exit 0).
- **Proof no value promoted** (no dispersion value reaches tracked status; no SP-6).
- **Proof Rung 2 remains deferred** (no `M`, no Rung-2 row, no ceiling advance, no `--promotion-check`, no new
  exit code; C1–C4 closed as **hardening, not admission** — OD-C5-6 reporting language).
- **Final `git status --porcelain`.**
- **Any deviations or blockers.**

> **Reporting language (OD-C5-6, binding).** The report MUST state, verbatim in intent: *C1 fixed and tested
> (nested-`hashes` digest-shape enforced; nested non-digest rejected, exit 3); C2 fixed and tested
> (immediate-precedence negation; unrelated negation no longer suppresses; legitimate negated examples
> preserved); C3 fixed and tested (repo-root-resolved `--out` guard; absolute repo-docs path refused; ledger
> byte-unchanged); C4 warning behaviour defined and tested (empty `hashes` warns, exit 0; no silent acceptance;
> no `hashes.txt` read); Rung 2 still deferred; no value promoted; C1–C4 closed only as hardening, not as
> admission.*

---

## Review / audit guidance

Reviewer (`/review-sprint`) and auditor (`/audit-sprint`) focus (SDD §13):

- [ ] **Independently test C1** — a nested non-digest token under any `hashes`-keyed dict → exit 3, reason cites
  SHA-256 digest / Pokémon-Element; a nested **valid** digest is not falsely flagged; the top-level digest path
  is unchanged.
- [ ] **Independently test C2** — `"claim not made; agent strong"` → flagged; `"never strong"` /
  `"NO strength claim"` → clean; `"agent is strong"` → flagged. No legitimate negated example broken (R4).
- [ ] **Independently test C3** — an absolute repo-docs path refused; relative `docs/` + `ledger.md` basename
  still refused; a local path allowed; `git diff --exit-code -- docs/ledger.md` clean.
- [ ] **Independently test C4** — empty `hashes` warns on stderr, exit 0; non-empty silent; `"hashes.txt"` absent
  from source.
- [ ] **Confirm no input previously rejected is now accepted**, unless explicitly justified by the SDD; the 12
  existing checks remain green (conservative-only).
- [ ] **Confirm Rung 1 held and the ledger unchanged** (hash `2a2f1c2…`; claim-ceiling unchanged).
- [ ] **Confirm no raw data, no Daily Top Episodes, no runtime-agent scope, no eval runs.**
- [ ] **Confirm no schema file, second module, or dependency**; in-module constant / one-module / stdlib-only
  preserved; no new exit code.
- [ ] **Confirm C1–C4 closed as hardening, not admission** (OD-C5-6 reporting language); Rung 2 deferred; no
  value promoted.

---

## Goal traceability (Appendix C)

PRD goals (`docs/cycles/cycle-005/01-prd.md` §3) mapped to Sprint 01 tasks:

| Goal | Description | Contributing tasks |
|---|---|---|
| **G-1** | C1 positional hardening (priority hard blocker) | T1, T2 |
| **G-2** | C2 negation hardening | T1, T3 |
| **G-3** | C3 `--out` repo-root guard | T1, T4 |
| **G-4** | C4 empty-hashes handling | T1, T5 |
| **G-5** | Regression tests (each of C1–C4 leaves a runnable check; 12 existing stay green) | T6 |
| **G-6** | Conservative-only, compatible (validator strictly stricter-or-equal; 12 checks green) | T2, T3, T4, T5, T6, T7 |
| **G-7** | Rung 1 held; ledger byte-unchanged; no value promoted | T1, T7 (verified end to end) |

**Goal-coverage check:** every PRD goal G-1…G-7 has at least one contributing task. No goal is orphaned.

**E2E posture-validation:** T7 is the cycle exit gate (single sprint). It runs the full Required-test-commands
block and proves the posture invariants (ledger byte-unchanged, claim ceiling unchanged, protected paths
untouched, nothing staged, Rung 2 deferred). This is the P0 must-complete task. There is no separate same-regime
E2E *evidence* task by design — Cycle-005 promotes no value and runs no new evals; the E2E gate is the
posture-and-hardening verification, not a verdict.

---

## Explicit deferred items (to Cycle-006 or a later explicit gate)

Recorded as deferred — **none attempted in Cycle-005**:

- **Rung-2 attempt.**
- **Rung-2 admission.**
- **Rung-2 ledger row.**
- **Claim-ceiling advance.**
- **Numeric `M`.**
- **SP-6** live-value promotion.
- **OD-6 relaxation** / any inferential statistic.
- **`--promotion-check` mode** (would hard-fail on empty `hashes` and re-run the full hardened validator before
  any promotion).
- **A defensible pre-registration of `M`** that avoids post-hoc thresholding on the already-generated K=20+20
  bands (PRD §8.3).
- **The four Rung-2 seam decisions 8a–8d** (8a disjoint-bands-vs-OD-6; 8b numeric `M`; 8c SP-6; 8d Rung-2 row /
  ceiling-advance) — governance decisions the operator owns
  (`docs/cycles/cycle-003/07-od6-criterion-2-proposal.md` §5).
- **The five conjunctive Rung-2 readiness criteria**
  (`docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` §2), all required before a Rung-2 *consideration*.
- **Any use of Daily Top Episodes beyond local hypothesis generation.**

A Rung-2 attempt may proceed **only after** Cycle-005 passes review/audit **and** an explicit operator gate opens.

---

## CLI / exit-code contract (unchanged — SDD §7)

```
generate:  python analysis/evidence_summary.py <run_dir> [<run_dir> ...] [--json] [--out <local-path>]
validate:  python analysis/evidence_summary.py --validate <summary.json>

Exit codes (PRESERVED VERBATIM — no new code added):
  0  clean / valid          (now: may also carry a stderr WARNING for empty hashes — still exit 0)
  1  input failure
  2  mixed-regime refusal
  3  forbidden-field/value/word leak (fail-closed; never 0 on a leak)
```

C1 strengthens exit-3 (nested non-digest → 3). C2 strengthens exit-3 (affirmative forbidden word now caught
despite an unrelated negation). C3 strengthens the generate-mode `--out` refusal (absolute repo-docs path → the
existing exit-1 input-failure path). C4 adds a stderr warning on exit 0. **No exit code changes meaning; none is
added.**

---

## Self-review checklist (sprint-plan QA)

- [x] All MVP/hardening features from the PRD (C1–C4) are accounted for.
- [x] The single sprint is feasible as one iteration (one module + its test file).
- [x] All deliverables and acceptance criteria have checkboxes and are testable.
- [x] Technical tasks are specific and ordered (C1 priority first).
- [x] Technical approach aligns with the SDD (OD-C5-1…OD-C5-6 honored verbatim).
- [x] Risks identified with mitigation (R1–R10).
- [x] Dependencies explicit (PRD/SDD + operator build gate; task ordering; import-only files).
- [x] All PRD goals mapped to tasks (Appendix C); none orphaned.
- [x] Tasks annotated with goal contributions.
- [x] Posture-validation gate (T7) included in the (single) final sprint.
- [x] Authorized files = 3; forbidden files enumerated; stop-and-report rule stated.
- [x] Required test commands + ledger hash stated; deferred items recorded.

---

## Sources and traceability

> **Primary authorities:** `docs/cycles/cycle-005/01-prd.md` (accepted PRD); `docs/cycles/cycle-005/02-sdd.md`
> (accepted SDD — OD-C5-1…OD-C5-6, AC-1…AC-8, §5.2 test plan).
> **Supporting inputs:** `grimoires/loa/a2a/cycle-005/00-pre-prd-research.md` (recommendation A, hardening-only);
> `docs/operator/cycle-005-planning-inputs.md` (carry-forward index);
> `docs/cycles/cycle-004/07-closeout.md` §8 (C1–C4 carry-forwards), `06-audit-report.md` §7/§9 (C1–C4 reproduced),
> `05-review-report.md` §9, `04-implementation-report.md` §4 (local exercise on the K=20+20 dirs).
> **Tracked code (hardening target, anchors at `337fc4f`):** `analysis/evidence_summary.py`
> (`REPO_ROOT` `:57`; `SAFE_FIELDS` `:83-88`; `_SHA256_RE` `:107`; `_manifest_run_hash` `:117-132`;
> `build_summary` `:135`, hashes set `:180-182`; `_NEG_WINDOW` `:263`; window scan `:303`; `_norm_path`
> `:282-283`; `_affirmative_forbidden_words` `:298-306`; `_walk` `:333-350`; `validate_summary` `:353`, digest
> block `:369-379`; `_refuse_tracked_out` `:410-421`; `main` `:456`); `tests/test_evidence_summary.py` (`_HEX64`
> `:33`; `make_run_dir` `:49` / `manifest_hash` default `:51`; `validate_file_exit` `:75`; `run_checks` `:87`;
> 12 numbered checks; summary line `:284`).
> **Cycle-003 design authorities:** `04-evidence-summary-schema-spec.md`; `05-generator-validator-shape.md`;
> `06-rung-2-ledger-convention.md` (§3 row cites summary by reference + hash — the C4 motivation);
> `07-od6-criterion-2-proposal.md` (§3 pre-registration, §5 seam 8a–8d); `08-funsearch-forward-compat.md`.
> **Posture docs:** `docs/cycles/cycle-002/04-rung-2-readiness-criteria.md` §2;
> `docs/cycles/cycle-000-bootstrap/04-operator-decisions.md` (SP-6/SP-8/SP-9); `docs/failure-modes.md`
> (FM-10/FM-11); `docs/claim-ceiling.md` (Rung 1; forbidden words); `docs/ledger.md` (hash `2a2f1c2…`);
> `docs/operator/turntrace-loop-contract.md` (§6 build gate; §7-§8 hygiene/claim language).
> Current main at authoring: `337fc4f`. Claim ceiling: **Rung 1 (unchanged).** This sprint plan opens no
> implementation gate, builds no code, mutates no ledger, advances no ceiling, promotes no value, and edits no
> `.claude/`.
