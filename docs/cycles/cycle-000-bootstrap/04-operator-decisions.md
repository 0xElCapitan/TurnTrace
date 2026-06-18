# Operator Decisions — TurnTrace `cycle-000-bootstrap`

| Field | Value |
|---|---|
| **Cycle** | `cycle-000-bootstrap` |
| **Artifact** | `grimoires/loa/a2a/cycle-000-bootstrap/04-operator-decisions.md` |
| **Status** | Living record — updated through the planning cycle |
| **Last updated** | 2026-06-18 (loop-contract standing rule SP-7; earlier: evidence-storage patch; sprint-plan stage 2026-06-17) |
| **Related** | PRD §16 (`01-turntrace-prd.md`); SDD §10 (`02-turntrace-sdd.md`); Sprint Plan (`03-turntrace-sprint-plan.md`) |

> **Purpose.** Single source of truth for operator-level decisions that gate TurnTrace's build. The
> PRD opened these as OD-1…OD-6 (PRD §16); the SDD resolved OD-1 (SDD §4); this sprint-plan stage
> confirms OD-4 and records the remaining items the operator must close **before the build cycle
> opens**. cycle-000 is planning-only — no decision here authorizes code; the final row in
> §"Build-Gate Checklist" is the authorization step.

---

## 1. Decision Register (OD-1 … OD-6)

| ID | Decision | Resolution | Resolved at | Where recorded |
|----|----------|------------|-------------|----------------|
| **OD-1** | Repo layout / code home in a Loa-mounted repo | **RESOLVED — Option C:** keep the Data Loop Plan's root-level tree verbatim (`agents/ sim/ eval/ analysis/ frozen/ runs/ config/ docs/`) as this project's **App Zone**; `runs/` is the only generated tree (append-only, immutability-guarded); Loa System (`.claude/`) and State (`grimoires/`, `.beads/`, `.run/`) zones untouched. | 2026-06-17 (SDD) | SDD §4 (full options analysis + recommended tree) |
| **OD-2** | Strategy Category confirmation (was U-5) | **RESOLVED:** a distinct **Hackathon** track (report-based, prize-eligible) is separate from this **Simulation** competition; Hackathon ranking weighs leaderboard performance **AND** report. TurnTrace supplies the *evidence backbone* of the report; competitive standing is the agent's job. | 2026-06-17 (operator Overview) | PRD §8.3, §16; `competition-overview.md` |
| **OD-3** | Competition timeline (was U-6) | **RESOLVED:** Entry & Team-Merger **2026-08-09**; **Final Submission 2026-08-16**; final eval **2026-08-17 → ~2026-08-31**. ~2-month runway from the PRD. | 2026-06-17 (operator Overview) | PRD §8.3, §10 (CC-9), §16 |
| **OD-4** | Capability Probe (PR-9) is the **first** build task | **CONFIRMED (this sprint plan).** Sprint 00 opens with Task 00.1 (capability probe); it blocks Tasks 00.2–00.9 so the harness is shaped against the observed surface, never assumed. | 2026-06-17 (sprint plan) | Sprint Plan §"Sprint 00" Task 00.1, Dependencies; SDD §1.4, §8 Phase 1 |
| **OD-5** | Reproducibility posture | **DECIDED:** distribution-stable + audit-trail is the baseline; seed control is an unconfirmed capability (U-1), to be measured by the probe; byte-replay is a future upgrade if seed control is later proven. | 2026-06-17 (PRD, NFR-3) | PRD §7 (NFR-3), §16; SDD §3.5, §7.3 |
| **OD-6** | Cycle scope | **DECIDED:** cycle-000 = planning artifacts only (PRD → SDD → sprint plan). The Sprint 00 *build* is the next cycle. No code, no Kaggle files, no dependencies this cycle. | 2026-06-17 (PRD) | PRD §11.1, §16; SDD scope note |

**Status summary:** OD-1, OD-2, OD-3, OD-5, OD-6 fully resolved/decided. OD-4 confirmed at this stage.
There are **no open decisions inherited from PRD §16** — all six are closed.

---

## 2. Decisions Made By This Sprint Plan

Choices the sprint plan made that the operator should be aware of (each is a default the operator may
override before the build cycle opens):

| # | Decision | Rationale | Reversible? |
|---|----------|-----------|-------------|
| **SP-1** | **Two build sprints** (Sprint 00 = loop, Sprint 01 = first comparison), not one combined sprint | Mirrors the PRD's hard ordering data→optimize and the plan's Sprint 00 / Sprint 01 split (PRD §11.2–§11.3); keeps the first delta report as an explicit gate | Yes — sprints can be merged/split at build-cycle planning |
| **SP-2** | **No build beads created in cycle-000** | Creating build tasks now would imply implementation readiness ahead of the operator's build gate; cycle-000 is planning-only. Beads are created when `/implement`/`/run` opens the build cycle | Yes — beads created at build-cycle open |
| **SP-3** | **Calendar dates left TBD** for both sprints | The build cycle is not open; sequencing is fixed, calendar is not. Binding constraint is "complete with margin before 2026-08-16" (CC-9) | Yes — dates assigned at build-cycle planning |
| **SP-4** | **Sprint 00 sized LARGE (10 tasks); Sprint 01 sized MEDIUM (6 tasks)** | Within the skill's 7–10 (LARGE) / 4–6 (MEDIUM) bands; Sprint 00 carries all P0 foundation work | Yes |
| **SP-5** | **Config format default = JSON** (stdlib, no `pyyaml`) carried forward as the build default | SDD §2.3 soft default; keeps the stdlib-only constraint clean | Yes — sprint/build may revisit |
| **SP-6** | **Evidence-storage policy — raw generated run artifacts remain local/ignored by default; only sanitized / operator-approved evidence may be tracked in git.** Full `runs/<run_id>/` trees, raw traces, match logs, simulator outputs, deck files, card IDs, card names, `cg/`, starter files, PDFs, CSVs, and raw deck lists are not committed unless explicitly confirmed redistributable. Tracked = sanitized summaries, ledger rows, claim ceilings, failure-mode notes, planning docs, operator-approved artifacts. Reference runs by `run_id`/hashes/sanitized metrics/local path — never embed raw contents. | Extends CC-1/CC-2 to *generated* evidence; a sealed run is an evidence artifact, not automatically a tracked one. Mirrors Sprint Plan §"Evidence-Storage Policy" (ESP-1…ESP-5) | Only by **explicit operator approval** to track a specific, confirmed-redistributable artifact (CC-1/CC-2) |
| **SP-7** | **The Loa-native loop contract is the standing sprint execution rule.** Every sprint runs `/implement sprint-XX → /review-sprint sprint-XX → /audit-sprint sprint-XX`, with review/audit feedback re-entering only through `/implement` (the sole patch authority), and closes only after implementation + review + audit + operator acceptance. The authoritative contract lives at **`docs/operator/turntrace-loop-contract.md`**. | Makes sprint execution mechanics explicit and standing for all cycles from Cycle-001 onward. **This docs-only note does not open the build gate** (build still requires OA-2). | Standing rule — revisable by the operator |

---

## 3. Open Items Requiring Operator Action

> These are **not** PRD §16 decisions (those are closed). They are the gating actions the operator
> owns before/at the build cycle. None block the *planning* cycle's completion.

| ID | Item | Why it needs the operator | Needed by |
|----|------|---------------------------|-----------|
| **OA-1** | **Approve the planning artifacts** (PRD ✅ accepted, SDD ✅ accepted, this sprint plan ⏳ pending) | cycle-000 success criterion = all three approved (PRD §15) | To close cycle-000 |
| **OA-2** | **Open the build cycle** (authorize Sprint 00 execution) | cycle-000 is planning-only; code is written only after the build gate opens (OD-6) | Before any `/implement` / `/run` |
| **OA-3** | **Confirm local `cg/` Competition-Data lib is present and gitignored** on the build machine | Sprint 00 cannot run a match without it; it must never be committed (CC-1) | At build-cycle open |
| **OA-4** | **Confirm runway/cadence intent** — when the build cycle starts, given Entry/Merger 2026-08-09 and Final Submission 2026-08-16 | Bounds how aggressively the build cycle must move (PRD §11.5) | Before scheduling Sprint 00 |

**Capability unknowns U-1…U-4 are NOT operator decisions** — they are resolved by the capability
probe (Task 00.1), not by the operator. They are listed here only so the operator knows the probe's
findings (especially `seed_controlled` and measured `match_throughput`) will shape N-sizing and the
replay strategy in Sprint 01.

---

## 4. Build-Gate Checklist (the authorization step)

The build cycle (Sprint 00) opens only when **all** of the following hold:

- [ ] PRD approved (PRD §15.1) — **accepted**
- [ ] SDD approved (PRD §15.2) — **accepted**
- [ ] Sprint plan approved (PRD §15.3) — **pending operator review (OA-1)**
- [ ] No code / Kaggle files / dependencies committed in cycle-000 (PRD §15.4) — **upheld**
- [ ] Operator decisions recorded (PRD §15.5) — **this file**
- [ ] Operator explicitly opens the build cycle (OA-2)
- [ ] Local `cg/` lib confirmed present + gitignored (OA-3, CC-1)

---

## 5. Change Log

| Date | Stage | Change |
|------|-------|--------|
| 2026-06-17 | Sprint plan | Created. Consolidated OD-1…OD-6 (all closed); confirmed OD-4; recorded sprint-plan decisions SP-1…SP-5; surfaced open operator actions OA-1…OA-4 and the build-gate checklist. |
| 2026-06-18 | Sprint-plan patch | Added evidence-storage policy as **SP-6** (raw generated run artifacts stay local/ignored by default; only sanitized/operator-approved evidence is tracked). Mirrors new Sprint Plan §"Evidence-Storage Policy" (ESP-1…ESP-5). No PRD/SDD change required — extends CC-1/CC-2. |
| 2026-06-18 | Standing rule | Recorded the Loa-native loop contract as **SP-7**; authoritative at `docs/operator/turntrace-loop-contract.md`. Docs-only — build gate unchanged (still requires OA-2). |
