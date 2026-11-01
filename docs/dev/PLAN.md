# Delivery plan

## Strategy and scope

Deliver [PROJECT](PROJECT.md) through seven bounded useful increments against [SPEC](SPEC.md), using the APIs/models in [DECOMPOSITION](DECOMPOSITION.md). The first phase is a complete classic game with fixed interval locking, rather than infrastructure alone. Later phases preserve the playable baseline. Settings have a distinct session-only release before any configuration persistence. JSON and SQLite data formats share one validator and receive separate delivery increments.

Versions below identify capability releases; the saved-file format version remains 1. Dependencies are linear by phase, and each milestone follows its preceding delivery milestone. Do not activate later-phase tracking or work until the predecessor's exits, integration and publication are verified and that phase is within the selected implementation range.

## Phase and milestone map

| Phase / release | Useful outcome and included contracts | Deferred scope | Delivery milestones |
| --- | --- | --- | --- |
| Phase 1 — Classic baseline / 0.1.0 | S1 playable game; S2 fixed interval lock timing without modern actions; S4 core keys; S5 protocol detection only; S10 board/info/help and single HTML | Modern extensions, penetrator, settings, persistence, results/files | 1.1 Classic playable loop; 1.2 Verified single-file delivery |
| Phase 2 — Modern rules / 0.2.0 | S2 bag, SRS, hold, preview, conditional ghost and hard drop at fixed default settings; retain interval locking | Penetrator, configurable policy alternatives, persistence/results/files | 2.1 Modern piece state; 2.2 Shared landing and drop controls |
| Phase 3 — Penetrator / 0.3.0 | S3 bonuses, activation, traversal, lowest landing, white rendering and hold interaction | Settings, persistence/results/files | 3.1 Penetrator landing and controls; 3.2 Bonus and presentation integration |
| Phase 4 — Session settings / 0.4.0 | S4 all six controls; S2 both locking alternatives; settings panel/toggle; in-memory changes only | Cookies/URL resolution, leaderboard/files | 4.1 Six-setting session configuration |
| Phase 5 — HTTP configuration / 0.5.0 | S5 complete HTTP(S) read/write, invalid-value handling and strict file-mode isolation | Results and manual files | 5.1 Protocol-specific configuration persistence |
| Phase 6 — Results and JSON / 0.6.0 | S6 leaderboard; S7 JSON/schema; S9 JSON Save/Restore; all five panels and toggles | SQLite format option | 6.1 Session leaderboard; 6.2 JSON file exchange |
| Phase 7 — SQLite exchange / 1.0.0 | S8 SQLite; S9 both-format choice/detection; full S1-S10 acceptance | None within agreed target | 7.1 SQLite codec; 7.2 Both-format delivery |

Every phase also ends with its own Milestone <phase>.R — Phase review, containing exactly one phase code-review/testing/report task. IDs/names in this table are canonical for TASKS and hosted projection.

## Milestone outcomes and exits

### Phase 1 — Classic baseline

1.1 integrates board, shapes, movement, basic rotation without kicks, gravity, grounded interval timing, clearing, scoring, levels and game over with Start/Restart and Pause/Start. It demonstrates a playable game to completion; pure-domain checks cover collision/clears/timing and the browser exposes only available core controls. Standard random selection is sufficient until 7-bag arrives.

1.2 integrates keyboard/help, focus/page pause, centered board/info layout, help toggle and direct-file/HTTP startup. Produce the exact single HTML release artifact, installation instructions, version metadata and stable-name/checksum tooling. Exit evidence includes Chromium/Firefox in both modes and responsive widths. It demonstrates local double-click versus localhost play, allowing usability feedback on controls and layout before more panels appear. No blank feature panels or nonfunctional toggles are needed for deferred scope.

### Phase 2 — Modern rules

2.1 integrates 7-bag, explicit SRS geometry/kicks, one-hold-per-piece and next preview without changing lifecycle/scoring. Demonstrate bag boundaries, wall/floor rotations and blocked hold spawn. Shape/kick definitions must match their design/spec owners before consumers are integrated.

2.2 integrates the shared regular landing calculation into ghost and hard drop, including dynamic midline behavior and preserved grounded delay. Demonstrate ghost/hard-drop destination agreement and pause/timer boundaries in both execution modes. Fixed defaults remain visible in help; no settings persistence exists.

### Phase 3 — Penetrator

3.1 integrates feasible penetrating movement, activation and lowest landing through separated cavities, reusing the ghost/drop path and timing. Exit checks distinguish intermediate overlaps from legal final settlement and cover active-penetrator hold suppression and activation while grounded.

3.2 integrates four-line awards/cap, spend indicator and exclusive white piece/ghost rendering. Demonstrate an earn-spend-lock loop and resets, preserving settled cells and regular colors. Its narrow outcome justifies two delivery milestones rather than padding unrelated configuration work into this phase.

### Phase 4 — Session settings

4.1 integrates canonical setting enums/defaults, six native controls, both policy alternatives, immediate toggles and settings panel visibility. Verify changes through restart and reload: restart retains values; reload restores defaults in both modes. Assert zero cookie/configuration-URL/localStorage/IndexedDB persistence. Demonstrate changing lock policy without timer resets. A single delivery milestone fits this cohesive UI/domain connection.

### Phase 5 — HTTP configuration

5.1 integrates settings startup resolution, writeback and reload behavior through the protocol adapter. Verify every key independently under URL/cookie/default combinations, explicit defaults, malformed/duplicate values, unrelated URL fields, cookies blocked and history failure. Direct file mode has spies/equivalent observations proving no configuration URL or cookie access, including URLs containing settings. HTTPS attributes receive adapter checks; localhost HTTP evidence is identified accurately. This is a focused persistence milestone, separate from new result/file models.

### Phase 6 — Results and JSON

6.1 integrates exactly-once game-over records, UTC timestamps/UUIDs, top-ten ties/truncation, leaderboard panel and toggle. Demonstrate eleven completed games, zero scores and abandoned restarts, and prove reload clears results.

6.2 integrates strict duplicate-aware JSON decode, schema/semantic validation, downloads, restore replacement, size limits and file-operation pause/error UI. Introduce Save/Restore at the settings bottom with JSON available. Verify exact ID/score/time/setting round trips and unchanged-state rejection in both execution modes; HTTP restores mirror all settings while file restores leave URL/cookies untouched. Publish the JSON Schema and format guide. The milestone demonstrates portable session data; SQLite remains an explicit subsequent capability.

### Phase 7 — SQLite exchange

7.1 first verifies/pins an established-CDN single-script SQLite distribution against both protocols, then implements temporary-database export/import, version metadata, prepared statements, schema/type/integrity validation and cleanup. Failure of this distribution proof blocks dependent SQLite delivery; do not substitute a local worker/companion file or require a server. JSON remains the usable baseline.

7.2 integrates JSON/SQLite format choice and header-based restore detection. Verify both-format cross-round trips, malformed databases, duplicate/missing keys, fractional/oversized scores, wrong versions, bad timestamps and dependency failure. Exercise the complete browser-mode/width matrix, resource cleanup and full regression scope. The last phase review aggregates the final implementation report and unresolved eligible TODOs; contract violations cannot be deferred as TODOs.

## Verification and integration boundaries

Every delivery milestone exits through whole-capability code review, focused/regression checks, blocker repairs, a milestone report and HANDOFF update. TASKS assigns a standalone milestone review only when it contains at least four delivery tasks and its phase has at least two delivery milestones; otherwise the final delivery task owns these obligations. Each phase review waits for all delivery milestone completions and verified hosted closures, and checks cross-milestone interactions and the included contract subset. Reports use docs/dev/reports/phases/<phase>/<milestone>.md and PHASE-REPORT.md.

Core tests consume the actual HTML's pure named sections with deterministic time/randomness; browser checks exercise the packaged HTML. Provision isolated Chromium and Firefox under the repository browser policy and record versions, commands, failures and actual fallback coverage. Test-first evidence applies to nontrivial game/validation behavior. Unavailable checks are reported precisely and required mode/browser evidence remains a delivery gate; passing domain tests does not prove browser behavior. Native Windows execution is not a separate blocking requirement for this browser-only artifact.

Complete phases integrate from their phase branch into main using an explicit verified two-parent merge and published target readback. Partial milestones/ranges remain on the phase branch. Afterwards prepare the version's final release notes, pin its default-branch release commit/tag and publish the authorized GitHub release. The phase review prepares artifact evidence; it cannot claim a future merge or hosted release succeeded. Next-phase activation follows verified publication of the predecessor release.

## Release artifact contract

Each release contains tetris.html, README.md and SHA256SUMS; add session.schema.json from Phase 6 onward. All actual artifact basenames remain version-free. Enforce this with a project-local artifact-name check in both direct packaging and CI. The application version is embedded in HTML and agrees with release/tag/notes. Include direct-file and HTTP installation instructions, CDN requirements and observed verification limits. Verify actual artifact bytes before publication, then download/read back hosted assets and compare hashes before claiming delivery. Do not tag an unverified side-branch tip or move existing release tags.

## Risks and decision evidence

SQLite distribution compatibility, strict data validation and penetrator landing through disconnected cavities receive dedicated proof/tasks before their consumers. Browser provisioning failure triggers policy diagnostics and accurately scoped fallback, not invented passing results. At milestone demonstrations, concrete usability feedback may motivate a human instruction to continue, amend, simplify or stop; the plan itself grants no extra implementation range or automatic steering authority. Detailed check commands and actual evidence are established by implementation, not asserted by this plan.
