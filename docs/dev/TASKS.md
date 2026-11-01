# Implementation tasks

[PLAN](PLAN.md) owns phase/milestone outcomes and exits; [SPEC](SPEC.md) owns S1-S10 behavior. [layout](layout.md) maps edit scopes; [DECOMPOSITION](DECOMPOSITION.md) owns shared APIs/models. Every task is initially unchecked.

Each behavioral task includes meaningful test-first evidence, focused regressions and affected documentation. Dependencies below are intentionally sequential to preserve a usable path. Phase entry additionally requires accepted preparation integration, verified eligible tracking, authorized range and the prior phase release. Each delivery milestone has fewer than four delivery tasks, so its final task includes whole-milestone code review, testing, repairs, report and HANDOFF. Phase reviews prepare release evidence; later merge/tag/hosted publication is performed and read back by the coordinator before the next phase.

## Phase 1 — Classic baseline

- [x] Phase 1 — Classic baseline
    - [x] Milestone 1.1 — Classic playable loop
        - [x] T-001 — Provision isolated verification tools
            Verification: pytest readiness suite: 3 passed in 3.68s; isolated matching Chromium shell and Firefox file/HTTP input/Canvas/teardown verified; Firefox requires the documented process-local content-sandbox override on this host; extraction harness passed; no application acceptance claimed.
            Scope: requirements-dev.txt, tests/support, tests/unit and browser policy evidence; pin development tools and establish pytest/Node extraction harness.
            Depends on: accepted preparation, Phase 1 activation and selected implementation range.
            Evidence: Demonstrate isolated Chromium/Firefox provisioning and file/localhost launch evidence; report actual limits before dependent browser checks.
        - [x] T-002 — Implement classic motion and grounded timing
            Verification: RED: 5 movement/gravity/lock/pause assertions failed against the inert engine; GREEN: pytest tests/unit passed 11 tests, including occupied-cell bounds, all seven spawn geometries, rotation, partial-tick contact delay, lift-off and pause; fixture injection exists only in the Node test loader.
            Scope: tetris.html domain section and focused domain checks; S1 movement, shape bounds, gravity and S2 fixed interval locking.
            Depends on: T-001.
            Evidence: Deterministic collision/rotation/gravity and just-before/at-expiry tests; pause/lift-off boundaries; no grounded movement reset.
        - [x] T-003 — Integrate classic completion and game controls
            Verification: RED: 5 clear/score/level/completion cases failed before implementation; GREEN: 27 pytest cases passed (19 unit and 8 actual browser-mode cases); reviewed settled-cell writes, simultaneous compaction, pre-clear scoring, event deduplication, focus return and embedded-only UI; corrected an overly color-specific raster assertion to detect any regular piece color; full shortcut/help work remains T-004.
            Scope: tetris.html Engine/controller/renderer and checks; S1 clears, score, levels, spawn failure, game over, Start/Restart and Pause/Start.
            Depends on: T-002.
            Evidence: Play a game to completion, clear one through four rows, verify score/level and restart/pause; no duplicate completion.
            Milestone exit: review all 1.1 code and contracts, run focused/regression checks, repair blockers, include docs/dev/reports/phases/1/1.1.md and HANDOFF in this task completion commit; close all constituent issues, then verify milestone closure.

    - [x] Milestone 1.2 — Verified single-file delivery
        - [x] T-004 — Connect keyboard help and centered layout
            Verification: RED: missing Help control assertion failed before changes; GREEN: full pytest suite 45 passed in 40.96s; five-width anchor checks, X/Z/Space rotation, one-shot repeat suppression, IME/editable-input isolation and modeled blur pause/no-auto-resume passed in Chromium/Firefox file/HTTP; corrected the old all-buttons selector to target the required bottom gameplay row; native OS focus delivery remains unverified.
            Scope: tetris.html Input/Renderer; S4 core mappings, focus/page pause, help toggle and S10 center anchor.
            Depends on: T-003.
            Evidence: Keyboard works from the game, editable control focus is respected, page hiding pauses; toggle leaves board anchor stable.
        - [x] T-005 — Establish versioned release preparation tooling
            Recovery verification: CI run 41313446648 on 4974b429e6a6d7b64b191823577dd977f7bacd4c passed 49 tests in 47.84s, package creation and the independent name/hash gate on supported Ubuntu 24.04. The original host-selection failure is retained as historical evidence; reassessment is resolved.
            Verification: RED: 4 packaging/name/hash/version checks failed against inert commands; GREEN: 23 unit tests passed in 1.54s; actual 0.1.0 package and independent inventory/hash gate passed; exact HTML copied with stable version-free asset names; CI uses documented official actions and identical checks, but remote CI result is not yet claimed.
            Scope: VERSION, scripts/package.py, scripts/check_artifact_names.py, CI and packaging checks.
            Depends on: T-004.
            Evidence: Generate exact tetris.html/README.md/SHA256SUMS with version agreement, no companion application file and version-free basenames; exercise direct and CI name checks.
        - [x] T-006 — Verify classic packaged execution and document use
            Verification: Full suite against exact dist/tetris.html: 57 passed in 81.02s, including all browser-mode game-over/restart paths, five-width anchor checks, Canvas pixels, modeled visibility/focus pause and packaging failures; source/artifact bytes matched SHA-256 6564d1d578f36eb1b45cfd47ecfb9540935193e5c1caa784b3ec79851a1491a3; screenshot visually inspected with centered board and readable controls; reviewed keyboard/controller lifecycle and stable package/CI paths; actual hash is available in generated SHA256SUMS; native OS focus/Windows execution remain unverified.
            Scope: tests/browser, README.md, AGENTS.md, dependency/provisioning evidence and packaged HTML.
            Depends on: T-005.
            Evidence: Run Chromium/Firefox file/HTTP matrix at five widths; double-click and localhost instructions match observed behavior; fixed random/basic rotation scope is explicit.
            Milestone exit: review all 1.2 code and contracts, run focused/regression checks, repair blockers, include docs/dev/reports/phases/1/1.2.md and HANDOFF in this task completion commit; close all constituent issues, then verify milestone closure.

    - [x] Milestone 1.3 — Phase review
        - [x] T-007 — Review test and report phase 1
            Verification: Review RED: 5 live-region/valid-meta cases failed; GREEN: rebuilt packaged HTML passed 62 tests in 85.19s and independent artifact-name/hash gate; Prettier check and source/fixture boundaries passed; initial task-commit audit passed with scoped forward repairs; actual current HTML SHA-256 6ef0474070fda9c0a7b634250659d252adaa666886ec3bd9fe235d63531e36e5; final CI, integration and hosted release readbacks remain subsequent gates.
            Depends on: T-006 and completion/verified closure of delivery milestones 1.1, 1.2.
            Scope: cross-milestone code review, included S-contract exits, prior regressions, current release 0.1.0 artifact/name/hash/version evidence and unresolved findings.
            Evidence: repair blockers, commit docs/dev/reports/phases/1/PHASE-REPORT.md and HANDOFF with this task; close its issue and review milestone after publication. Coordinator then verifies explicit main integration and GitHub release 0.1.0 before any next-phase activation.

## Phase 2 — Modern rules

- [x] Phase 2 — Modern rules
    - [x] Milestone 2.1 — Modern piece state
        - [x] T-008 — Add seven-bag queue generation
            Verification: RED bag/preview case failed against independent draws; GREEN all 25 unit checks passed, including three full bags and preview transitions.
            Scope: tetris.html Engine queue and deterministic unit checks; S2.
            Depends on: T-007.
            Evidence: Every complete bag has all seven kinds, bags concatenate correctly and seeded tests cover boundaries without biasing gameplay queue.
        - [x] T-009 — Implement canonical SRS rotations and kicks
            Verification: RED two SRS cases failed; GREEN 28 unit checks passed, exact eight I and JLSTZ tables, wall and floor kicks, blocked rotation and grounded timer preservation.
            Scope: tetris.html shape/kick definitions and Engine rotation; DECOMPOSITION geometry and SPEC S2 tables.
            Depends on: T-008.
            Evidence: Check every transition table, I/JLSTZ distinction, O invariance, wall/floor success and fully blocked no-op.
        - [x] T-010 — Integrate hold and next preview
            Verification: RED both hold cases failed; GREEN 30 unit checks passed; reviewed bag consumption, SRS trials, hold reset and blocked spawn; hold/next canvases use canonical shapes and palette, native modifier shortcuts pass through.
            Scope: tetris.html Engine/Renderer/Input and modern-state checks.
            Depends on: T-009.
            Evidence: One hold per falling piece, reset on lock, orientation-zero replacement, blocked swap game over and accurate next kind.
            Milestone exit: review all 2.1 code and contracts, run focused/regression checks, repair blockers, include docs/dev/reports/phases/2/2.1.md and HANDOFF in this task completion commit; close all constituent issues, then verify milestone closure.

    - [x] Milestone 2.2 — Shared landing and drop controls
        - [x] T-011 — Add shared landing and conditional ghost
            Verification: RED three ghost cases failed; GREEN 33 unit checks passed; shared regular landing stops at first obstruction, ghost is read-only, whole straddling ghost hides and fully lower-half projection shows.
            Scope: tetris.html Engine.landing/view and Renderer; S2.
            Depends on: T-010.
            Evidence: Regular landing stops at first obstacle; hide straddling/upper-half ghost and show fully lower-half ghost without state changes.
        - [x] T-012 — Connect hard drop to existing lock timing
            Verification: RED two hard-drop cases failed; GREEN 36 unit checks passed; Enter uses shared ghost landing, two points per row, full contact interval after partial gravity tick and no repeat reset or score.
            Scope: tetris.html Engine/Input and timing checks; S2/S4.
            Depends on: T-011.
            Evidence: Enter reaches ghost destination, awards distance score, starts a full contact interval and preserves existing grounded elapsed time on repeat.
        - [x] T-013 — Verify modern rule interactions in both modes
            Verification: Packaged 0.2.0 HTML passed all 82 tests in 85.03s under Chromium and Firefox in file and HTTP modes; hold/preview/drop/contact, ghost raster, modifier isolation, pause and classic regressions passed; milestone code review found no blocker; artifact names and hashes passed.
            Scope: tests/browser, README.md and help content.
            Depends on: T-012.
            Evidence: Run hold/bag/kick/drop/ghost regressions in actual packaged file/HTTP HTML under both browsers; verify pause, focus and existing baseline.
            Milestone exit: review all 2.2 code and contracts, run focused/regression checks, repair blockers, include docs/dev/reports/phases/2/2.2.md and HANDOFF in this task completion commit; close all constituent issues, then verify milestone closure.

    - [x] Milestone 2.3 — Phase review
        - [x] T-014 — Review test and report phase 2
            Forward repair: P2-F1 missing Enter help text corrected after four RED browser cases; all 12 modern packaged-browser cases GREEN in 17.79s. Original closure retained; final hosted CI and reclosure pending.
            Verification: Phase-wide Engine/Input/Renderer review and six-task atomic commit audit passed; 82 packaged tests passed in 85.03s; version 0.2.0, source formatting and independent artifact-name/hash gates passed; delivery milestones 2.1 and 2.2 closed with readback; hosted CI, explicit integration and release remain subsequent gates.
            Depends on: T-013 and completion/verified closure of delivery milestones 2.1, 2.2.
            Scope: cross-milestone code review, included S-contract exits, prior regressions, current release 0.2.0 artifact/name/hash/version evidence and unresolved findings.
            Evidence: repair blockers, commit docs/dev/reports/phases/2/PHASE-REPORT.md and HANDOFF with this task; close its issue and review milestone after publication. Coordinator then verifies explicit main integration and GitHub release 0.2.0 before any next-phase activation.

## Phase 3 — Penetrator

- [ ] Phase 3 — Penetrator
    - [ ] Milestone 3.1 — Penetrator landing and controls
        - [ ] T-015 — Implement lowest feasible penetrating landing
            Scope: tetris.html domain feasibility/landing/rotation and cavity fixtures; S3.
            Depends on: T-014.
            Evidence: Traverse occupied rows without deletion; ghost/drop agree on the lowest legal cavity; reject out-of-bounds or no-landing motions.
        - [ ] T-016 — Integrate activation hold exclusion and timing
            Scope: tetris.html Engine/Input and interactions; S3.
            Depends on: T-015.
            Evidence: P spends once, repeated activation is a no-op, active hold is disabled, grounded activation preserves or releases timing correctly and final lock never overlaps.
            Milestone exit: review all 3.1 code and contracts, run focused/regression checks, repair blockers, include docs/dev/reports/phases/3/3.1.md and HANDOFF in this task completion commit; close all constituent issues, then verify milestone closure.

    - [ ] Milestone 3.2 — Bonus and presentation integration
        - [ ] T-017 — Award and cap penetrator bonuses
            Scope: tetris.html Engine scoring/bonus events and deterministic four-clear fixtures.
            Depends on: T-016.
            Evidence: Four-line clears award one, cap at three, activation spends one and restart resets; ordinary clears do not award.
        - [ ] T-018 — Render white penetrators and bonus indicator
            Scope: tetris.html Renderer/help, browser checks and README.md.
            Depends on: T-017.
            Evidence: Earn/spend/lock loop updates one symbol per bonus; regular pieces/ghost/hold/preview never use white; both modes/browsers preserve prior play.
            Milestone exit: review all 3.2 code and contracts, run focused/regression checks, repair blockers, include docs/dev/reports/phases/3/3.2.md and HANDOFF in this task completion commit; close all constituent issues, then verify milestone closure.

    - [ ] Milestone 3.3 — Phase review
        - [ ] T-019 — Review test and report phase 3
            Depends on: T-018 and completion/verified closure of delivery milestones 3.1, 3.2.
            Scope: cross-milestone code review, included S-contract exits, prior regressions, current release 0.3.0 artifact/name/hash/version evidence and unresolved findings.
            Evidence: repair blockers, commit docs/dev/reports/phases/3/PHASE-REPORT.md and HANDOFF with this task; close its issue and review milestone after publication. Coordinator then verifies explicit main integration and GitHub release 0.3.0 before any next-phase activation.

## Phase 4 — Session settings

- [ ] Phase 4 — Session settings
    - [ ] Milestone 4.1 — Six-setting session configuration
        - [ ] T-020 — Centralize exact setting validation and defaults
            Scope: tetris.html SettingsPolicy and SessionStore plus checks; S4 and DECOMPOSITION enums.
            Depends on: T-019.
            Evidence: All six keys validate exactly with canonical defaults and invalid values leave state unchanged; eliminate competing hard-coded defaults.
        - [ ] T-021 — Implement selectable locking and live policy changes
            Scope: tetris.html Engine/controller settings integration and deterministic timing tests; S2/S4.
            Depends on: T-020.
            Evidence: Failed-downward and immediate hard-drop policies work; switching policies preserves contact elapsed time and cannot reset a grounded interval.
        - [ ] T-022 — Add six controls and session-only settings panel
            Scope: tetris.html settings controls/toggle, Input/Renderer, README.md and browser checks.
            Depends on: T-021.
            Evidence: All six changes are immediate, restart retains and reload resets; zero cookie/query/localStorage/IndexedDB persistence; hiding settings hides its contents.
            Milestone exit: review all 4.1 code and contracts, run focused/regression checks, repair blockers, include docs/dev/reports/phases/4/4.1.md and HANDOFF in this task completion commit; close all constituent issues, then verify milestone closure.

    - [ ] Milestone 4.2 — Phase review
        - [ ] T-023 — Review test and report phase 4
            Depends on: T-022 and completion/verified closure of delivery milestones 4.1.
            Scope: cross-milestone code review, included S-contract exits, prior regressions, current release 0.4.0 artifact/name/hash/version evidence and unresolved findings.
            Evidence: repair blockers, commit docs/dev/reports/phases/4/PHASE-REPORT.md and HANDOFF with this task; close its issue and review milestone after publication. Coordinator then verifies explicit main integration and GitHub release 0.4.0 before any next-phase activation.

## Phase 5 — HTTP configuration

- [ ] Phase 5 — HTTP configuration
    - [ ] Milestone 5.1 — Protocol-specific configuration persistence
        - [ ] T-024 — Resolve HTTP settings from URL cookies and defaults
            Scope: tetris.html ProtocolAdapter/SettingsPolicy and precedence checks; S5.
            Depends on: T-023.
            Evidence: Resolve each key independently, save explicit defaults, retain cookies for omitted parameters and safely fall through malformed/duplicate values.
        - [ ] T-025 — Persist changes without navigation
            Scope: tetris.html HTTP adapter and browser persistence checks; S5.
            Depends on: T-024.
            Evidence: Update selected cookies/query via replaceState, preserve unrelated fields/fragment, set HTTP/HTTPS attributes correctly and warn on refusal.
        - [ ] T-026 — Verify file-mode isolation and reload behavior
            Scope: tests/unit/browser, README.md and protocol failure fixtures.
            Depends on: T-025.
            Evidence: Prove no file-mode cookie/config-URL access and default reloads; cover all six precedence/write paths, blocked cookies and history failure in both browsers.
            Milestone exit: review all 5.1 code and contracts, run focused/regression checks, repair blockers, include docs/dev/reports/phases/5/5.1.md and HANDOFF in this task completion commit; close all constituent issues, then verify milestone closure.

    - [ ] Milestone 5.2 — Phase review
        - [ ] T-027 — Review test and report phase 5
            Depends on: T-026 and completion/verified closure of delivery milestones 5.1.
            Scope: cross-milestone code review, included S-contract exits, prior regressions, current release 0.5.0 artifact/name/hash/version evidence and unresolved findings.
            Evidence: repair blockers, commit docs/dev/reports/phases/5/PHASE-REPORT.md and HANDOFF with this task; close its issue and review milestone after publication. Coordinator then verifies explicit main integration and GitHub release 0.5.0 before any next-phase activation.

## Phase 6 — Results and JSON

- [ ] Phase 6 — Results and JSON
    - [ ] Milestone 6.1 — Session leaderboard
        - [ ] T-028 — Record stable completed-game results once
            Scope: tetris.html SessionStore/controller and deterministic identity/time checks; S6.
            Depends on: T-027.
            Evidence: Game-over UUID/UTC records preserve safe scores including zero, duplicate events cannot insert twice and restart abandonment is excluded.
        - [ ] T-029 — Rank and display the session top ten
            Scope: tetris.html ranking/Renderer and leaderboard toggle.
            Depends on: T-028.
            Evidence: Eleven results truncate correctly; score/time/ID tie ordering is deterministic; panel order and board anchoring remain correct.
        - [ ] T-030 — Verify leaderboard lifecycle and game interactions
            Scope: tests/browser, README.md and result fixtures.
            Depends on: T-029.
            Evidence: Reload clears history, restart retains it, active play and pause do not insert scores, completed games update immediately in both modes.
            Milestone exit: review all 6.1 code and contracts, run focused/regression checks, repair blockers, include docs/dev/reports/phases/6/6.1.md and HANDOFF in this task completion commit; close all constituent issues, then verify milestone closure.

    - [ ] Milestone 6.2 — JSON file exchange
        - [ ] T-031 — Implement complete duplicate-aware JSON validation
            Scope: tetris.html Validator/JSONCodec, normative schema checks, fixtures and docs/FILE-FORMATS.md; S7.
            Depends on: T-030.
            Evidence: Validate schema equivalence and semantic dates/UUIDs/safe integers; reject duplicate object members/IDs, unknown versions, extra/missing settings and malformed UTF-8 before mutation.
        - [ ] T-032 — Connect manual JSON Save and Restore
            Scope: tetris.html FileController/controller/settings buttons and browser checks; S9.
            Depends on: T-031.
            Evidence: Download one JSON file; restore replaces results/settings and freezes file interaction, mirrors all HTTP settings or memory only in file mode; cancellation does not change data.
        - [ ] T-033 — Verify invalid-file isolation and portable JSON delivery
            Scope: tests/browser/fixtures, format guide, README.md and package schema inclusion.
            Depends on: T-032.
            Evidence: Round-trip exact IDs/scores/timestamps/settings in both modes; prove unchanged results/settings/cookies/URL for invalid/oversized/trailing/duplicate inputs; hide buttons with settings.
            Milestone exit: review all 6.2 code and contracts, run focused/regression checks, repair blockers, include docs/dev/reports/phases/6/6.2.md and HANDOFF in this task completion commit; close all constituent issues, then verify milestone closure.

    - [ ] Milestone 6.3 — Phase review
        - [ ] T-034 — Review test and report phase 6
            Depends on: T-033 and completion/verified closure of delivery milestones 6.1, 6.2.
            Scope: cross-milestone code review, included S-contract exits, prior regressions, current release 0.6.0 artifact/name/hash/version evidence and unresolved findings.
            Evidence: repair blockers, commit docs/dev/reports/phases/6/PHASE-REPORT.md and HANDOFF with this task; close its issue and review milestone after publication. Coordinator then verifies explicit main integration and GitHub release 0.6.0 before any next-phase activation.

## Phase 7 — SQLite exchange

- [ ] Phase 7 — SQLite exchange
    - [ ] Milestone 7.1 — SQLite codec
        - [ ] T-035 — Prove and pin a single-script CDN SQLite runtime
            Scope: tetris.html DependencyLoader, docs/DEPENDENCIES.md and browser loading evidence; S8.
            Depends on: T-034.
            Evidence: Verify actual pinned URL/version/license/integrity and initialization under file/HTTP in Chromium/Firefox without worker/companion local asset; clear bounded failure keeps JSON/game usable.
        - [ ] T-036 — Encode SQLite snapshots with version metadata
            Scope: tetris.html SQLiteCodec and round-trip fixtures; S8.
            Depends on: T-035.
            Evidence: Write genuine SQLite header, user_version=1 and exact two tables via bound values; preserve every field/type and close all resources.
        - [ ] T-037 — Validate SQLite imports before candidate creation
            Scope: tetris.html SQLiteCodec/Validator and invalid database fixtures.
            Depends on: T-036.
            Evidence: Check integrity/schema/metadata/types/keys/records against S7/S8, reject extra tables/views/triggers/columns, wrong versions and corrupt data; close statements/databases on all paths.
            Milestone exit: review all 7.1 code and contracts, run focused/regression checks, repair blockers, include docs/dev/reports/phases/7/7.1.md and HANDOFF in this task completion commit; close all constituent issues, then verify milestone closure.

    - [ ] Milestone 7.2 — Both-format delivery
        - [ ] T-038 — Integrate format choice and cross-format restore
            Scope: tetris.html FileController/UI and browser checks; S9.
            Depends on: T-037.
            Evidence: Save offers JSON/SQLite, restore detects content independent of extension, cross-round trips preserve fields and both modes honor their persistence rules.
        - [ ] T-039 — Verify codec failures cleanup and complete browser matrix
            Scope: tests/unit/browser/fixtures and resource/failure checks.
            Depends on: T-038.
            Evidence: Dependency failure, corrupt databases, invalid timestamps, duplicate/missing keys, fractional/unsafe scores and concurrent input leave live data unchanged; check cleanup and all five widths in four browser-mode combinations.
        - [ ] T-040 — Finalize complete single-file distribution and guides
            Scope: README.md, AGENTS.md, docs/FILE-FORMATS.md, docs/DEPENDENCIES.md, VERSION, package/release evidence.
            Depends on: T-039.
            Evidence: Full S1-S10 regression against actual generated HTML, names/checksums/version/schema agreement and installation instructions; no unverified platform/delivery claims.
            Milestone exit: review all 7.2 code and contracts, run focused/regression checks, repair blockers, include docs/dev/reports/phases/7/7.2.md and HANDOFF in this task completion commit; close all constituent issues, then verify milestone closure.

    - [ ] Milestone 7.3 — Phase review
        - [ ] T-041 — Review test and report phase 7
            Depends on: T-040 and completion/verified closure of delivery milestones 7.1, 7.2.
            Scope: cross-milestone code review, included S-contract exits, prior regressions, current release 1.0.0 artifact/name/hash/version evidence and unresolved findings.
            Evidence: repair blockers, commit docs/dev/reports/phases/7/PHASE-REPORT.md and HANDOFF with this task; close its issue and review milestone after publication. Coordinator then verifies explicit main integration and GitHub release 1.0.0 before any next-phase activation.
            Final scope: include docs/dev/reports/IMPLEMENTATION-REPORT.md aggregating all phases, verification limits and unresolved eligible TODOs; no contract violation may be deferred.
