# System specification

## Scope and contract ownership

The application fulfills [PROJECT](PROJECT.md) using [ARCHITECTURE](ARCHITECTURE.md) and the models/APIs in [DECOMPOSITION](DECOMPOSITION.md). This document owns observable behavior and operation semantics. The [JSON Schema](contracts/session.schema.json) owns structural JSON constraints; semantic constraints below apply to both JSON and SQLite. Requirement groups S1-S10 are the acceptance references for delivery planning.

## S1 — Classic game and lifecycle

Use a visible 10-column, 20-row board with all seven tetrominoes. Occupied cells must remain in bounds. Spawn a centered orientation-zero piece with its topmost occupied row at row zero. If it overlaps settled cells, complete the game. Invalid movement/rotation is a no-op. Settled cells are immutable until full rows clear; compact remaining rows downward and insert empty rows above. A lock adds the active piece, clears all full rows simultaneously, updates score/lines/level, then spawns a piece. Emit exactly one completion event per game ID.

Initial phase is ready, score/lines zero and level one. Start/Restart begins a fresh game and UUID, resets board, hold, queue, bonuses and timing, and retains session settings/results. Restart abandons unfinished play without a leaderboard entry. Pause/Start starts ready play, pauses running play or resumes paused play; from game over it starts a fresh game. Ignore movement in ready/paused/over phases. Pause freezes all game clocks, clears pressed input, and never advances a piece on resume. Losing window focus or hiding the page pauses a running game; focus return requires explicit resume.

Award 100/300/500/800 times the pre-clear level for one/two/three/four rows; add one point per successful soft-drop row and two per hard-drop row. No score for blocked or repeated zero-distance drops. Level is 1 + floor(totalLines/10). Gravity interval is max(100, 1000 - 75*(level-1)) milliseconds. Score must remain a safe non-negative integer; saturate at Number.MAX_SAFE_INTEGER. Gameplay may not produce more than four cleared rows from one tetromino lock.

## S2 — Modern pieces, landing and lock timing

Use Fisher-Yates shuffled 7-bags; each complete bag contains every kind exactly once. Maintain sufficient queued kinds for one-piece preview. Hold stores only kind and spawns the replacement in orientation zero without penetrator status. Permit one hold per falling piece; reset eligibility after locking. Swapping into an obstructed spawn completes the game. An invalid/disabled hold is a no-op.

Use clockwise/counterclockwise SRS rotations and ordered I and JLSTZ wall-kick tables; O has no shape-changing rotation or translation kick. Try the unshifted rotated position then the translation trials below; accept the first valid candidate. Occupied cells, not empty matrix margins, determine board bounds. Spawn centering and shape coordinates must be consistent between game, preview and hold.

For a regular piece, landing is the last legal position along an uninterrupted downward path before the next occupied-cell collision or floor. The ghost displays that landing without changing state. In dynamic mode hide the entire ghost if any projected occupied cell is in rows 0-9; show it only if all are in rows 10-19. Hidden and visible modes respectively always hide/show an available ghost. No ghost exists when there is no active piece.

Grounded means at its landing position. Under interval locking, begin a full gravity interval when the piece becomes grounded, including after a gravity/input movement. Capture that interval at grounding. Elapsed grounded time advances independently of gravity phase; a partial pending gravity tick does not shorten it. Lateral moves, rotations and repeated hard drops that stay grounded preserve elapsed time. Actual lift-off clears it; grounding again starts a fresh interval. Pause/busy suspension freezes it. At expiry lock once if still grounded. A timer cannot lock an invalid/overlapping position.

Under failed locking, lock on a failed downward gravity or soft-drop attempt. Hard drop moves directly to landing but, when following the general policy, does not itself make a failed downward attempt; a later gravity/soft-drop attempt locks it. Immediate hard-drop policy locks after the hard-drop action, including a zero-distance action. Under interval policy, hard drop begins a full grounded interval if newly grounded and otherwise preserves elapsed time. Disabling hard drop makes its key a no-op.

When changing from interval to failed policy discard the timer and await a failed attempt. When changing from failed to interval while grounded, preserve tracked grounded elapsed time and use the grounding interval captured on contact; lock on the next controller update if it has already elapsed. Track contact time regardless of policy so toggling settings cannot create artificial resets.

## S3 — Penetrator

A four-line clear awards one bonus after settlement, capped at three. Begin each game with zero. P activates a running regular piece only when a bonus exists, spends exactly one immediately and marks it penetrator until locking. Repeated activation, no bonus or non-running state is a no-op. Active penetrators cannot be held. Existing settled cells are never erased by penetration.

For a penetrator, enumerate legal non-overlapping placements at or below the current anchor with the same orientation/x, and choose the greatest y. Descent may cross occupied cells to reach it, including separated legal cavities. Hard drop and ghost use exactly this destination. During traversal the active piece may visually overlap settled cells; it must never settle there. Reject a translation/rotation if occupied cells leave the board or there is no legal landing at or below its resulting anchor. Downward movement stops at the lowest legal landing even when the board floor would place the shape in collision. Apply kick candidates using these penetrator feasibility rules.

Activation of a grounded piece releases grounding if the selected landing is lower; otherwise preserve the existing contact timer. A newly spawned piece cannot rescue an already failed spawn through activation. Locking writes the ordinary kind into settled cells and removes penetrator status. Render every active penetrator cell and its visible ghost in white; use non-white colors for regular active/held/preview/settled pieces and ghosts. Distinguish the white ghost by outline/opacity. Show exactly one bonus symbol per stored bonus and update on each spend/award.

## S4 — Settings and input

The six keys, enums and defaults in DECOMPOSITION are canonical. Native controls offer only those values. Disabled hold does not discard an already stored kind; disabled next preview hides it without changing queue. Setting changes are immediate and preserve active board/results. Locking changes obey S2. Resetting a game does not reset settings. Optional-panel visibility is session UI state outside these six settings and outside exported data.

Keyboard mappings: Left/Right move, Down soft-drops, Up or X or Space rotates clockwise, Z rotates counterclockwise, C or Shift holds, Enter hard-drops, P activates penetrator, Escape pauses/resumes, R starts/restarts. Suppress browser scrolling for handled gameplay keys. Use native repeat only for horizontal movement and soft drop; suppress repeated one-shot rotation/hold/drop/penetrator/pause/restart. Do not intercept gameplay keys while an input/select/textarea/button has focus, during IME composition or while file interaction is busy. Buttons and settings remain keyboard accessible; typing into a control must not move a piece.

During the session-only settings increment, changes survive restart and panel hiding but not page reload. No cookies, localStorage, IndexedDB or configuration query persistence is used by that increment. Leaderboard history is session-only in every version except explicit manual export/import.

## S5 — Execution mode and configuration persistence

Detect location.protocol automatically. For file:, initialize all six settings from defaults; do not access document.cookie or inspect/modify configuration URL parameters. Reload restores defaults; manual restore affects only memory. For http:/https:, resolve each key independently: first a valid single explicit query value, then a valid saved cookie, then default. Invalid/duplicate query values fall through; malformed/duplicate cookies for that key fall through to default. Unknown query parameters are preserved and ignored. Empty values are invalid. Decode safely; malformed percent encoding must not crash startup.

Cookies are named tetris_<key>, with path=/, SameSite=Lax and Max-Age=31536000; add Secure on HTTPS. Save each valid explicit query value into its cookie, including default-valued settings. Missing query keys do not overwrite existing cookies. Startup need not add missing keys to the URL. On an individual setting change, update that setting's cookie and replace its query parameter using history.replaceState without navigation; preserve unrelated parameters and fragment. On restore, mirror all six settings. Treat a restore's valid settings as the effective values even if its URL previously supplied conflicting settings.

Persistence inability, including cookie refusal or history failure, displays a clear warning while retaining the valid in-memory setting. Read back attempted cookies where supported; do not claim they were saved if blocked. Unsupported protocols display an error and do not initialize persistence. Both supported execution paths run the same game and manual Save/Restore UI.

## S6 — Session leaderboard

At game over record {id: gameId, score, timestamp} once, with UTC completion time generated at completion. Include zero scores. Rank descending score, ascending timestamp, then lexicographic ID; retain at most ten. Refresh display immediately. Restart does not duplicate or insert an abandoned result. Reload clears history; neither URL nor cookies contain results. Manual restore replaces, rather than merges, the collection. Display score and readable completion time; retain original UTC string and stable ID internally.

## S7 — JSON format and semantic validation

Save UTF-8 JSON with exactly formatVersion:1, results and settings. The normative schema requires every setting, rejects extra keys and limits results to ten. Each result has exactly id, score and timestamp. ID is a lowercase UUID v4; score is a JSON integer from zero through 9007199254740991. Timestamp is a canonical UTC string with four-digit year and millisecond precision. Validate calendar correctness by a parse/format round trip, not regex alone. Reject duplicate IDs, invalid calendar dates and non-finite/coerced numeric values. Results need not arrive sorted; validate all then sort using S6 while preserving exact fields.

Reject unsupported versions, invalid UTF-8, duplicate JSON object member names at any depth, trailing garbage, non-object roots and schema violations. Native JSON.parse alone cannot detect duplicate members; use a duplicate-aware lexical pass/parser before schema/semantic validation. Embed validation logic matching the normative schema; browser operation must not fetch the schema or require a validation CDN. Publish the schema alongside file-format documentation.

## S8 — SQLite format

Save a genuine SQLite database with header SQLite format 3 followed by a NUL byte and PRAGMA user_version=1. Use these exact application tables and fields:

```sql
CREATE TABLE high_scores (
    id TEXT PRIMARY KEY NOT NULL,
    score INTEGER NOT NULL CHECK(score >= 0),
    timestamp TEXT NOT NULL
);
CREATE TABLE settings (
    key TEXT PRIMARY KEY NOT NULL,
    value TEXT NOT NULL
);
```

Insert zero to ten results and exactly one row for each of the six setting keys. Bind values using prepared statements; no SQL is assembled from file content. Integers must be actual SQLite INTEGER values within the shared safe range, not REAL or numeric text. Timestamp, ID, enums, duplicate and result-count rules are identical to S7. Schema declaration, primary keys, required fields, runtime value types and database integrity must be checked before reading into a candidate. Reject unsupported metadata versions, extra/missing application tables or columns, user-defined views/triggers and unexpected setting rows. SQLite-generated indexes for the declared primary keys are permitted. Do not execute SQL stored in uploaded content, attach databases, register custom functions or load extensions.

Use an in-memory SQLite runtime with no persistent database, worker or companion local asset requirement. Pin a supported established-CDN JavaScript distribution and verify its initialization from both protocols. Each operation closes all statements and databases on every outcome. SQLite round trips preserve every ID, integer, timestamp and setting exactly.

## S9 — Manual file operations and errors

Save opens an accessible JSON/SQLite format choice and downloads one data file per successful action. Restore accepts either by content: identify SQLite by its header; otherwise parse as UTF-8 JSON. Filename/extension alone is not trusted. Limit uploaded files to 1 MiB and reject oversized files before decoding. Download names are tetris-session.json and tetris-session.sqlite. Cancel is a no-op on data. Disable concurrent file operations and pause running gameplay while choosing/processing files; require explicit resume afterward.

Restore order is read, decode, complete structural/semantic validation, canonical candidate preparation, then atomic in-memory replacement of results/settings. Until validation succeeds, results, settings, cookies and URL are unchanged. On rejected/cancelled input, show a clear message and preserve those values; suspending gameplay for file interaction is allowed. A valid restore does not replace the board, reset score, emit completion events or silently resume play. HTTP persistence mirroring happens only after successful validation; persistence failures follow S5, distinct from content-validation failure.

Use stable error categories unsupportedMode, fileTooLarge, invalidEncoding, invalidJSON, invalidSchema, invalidValue, unsupportedVersion, invalidSQLite, dependencyUnavailable and persistenceUnavailable. Present understandable messages without raw stack traces. Dependency failure/timeout affects SQLite only; JSON and the game remain usable. Revoke download object URLs after use and release temporary input/database resources.

## S10 — Layout, packaging and objective acceptance

Order panels leaderboard, info/controls, board, settings, help. Keep board/info present, with separate optional-panel toggles above Start/Restart and Pause/Start at the info panel bottom. No other clickable gameplay actions exist. Save/Restore belong at the settings bottom and disappear when settings are hidden. Keep the board anchor unchanged when toggles change; on wide screens its center aligns with the viewport center within one CSS pixel. On narrow screens allow scrolling of the scene; toggling does not move the board's scene coordinate, and board/info remain accessible without hiding them.

Distribute one tetris.html with embedded application markup/style/script and no application imports, server or build requirement. Supporting schema, README and release checksums are separate documentation/artifacts. Test the actual release HTML in isolated Chromium and Firefox through file navigation and localhost HTTP; a local-file check must not be replaced by a server check. Verify representative widths 320, 480, 768, 1280 and 1600 CSS pixels, keyboard focus, toggle stability, pause/restart and failure messages. HTTPS cookie attributes are separately inspected/tested against the HTTPS protocol adapter; do not claim a live HTTPS-hosting test from a localhost HTTP check.

End-to-end acceptance covers S1 game completion/clears/scoring; S2 bag, hold, SRS, straddling ghost and exact lock boundaries; S3 separated cavities, invalid penetrator moves, bonus cap and hold suppression; S4 all six controls and session reset; S5 independent precedence/default-valued URLs/invalid values, reloads and file-mode absence of persistence access; S6 eleven completed games/ties/restart deduplication; S7-S9 both-format cross-round trips, strict invalid inputs and unchanged-state failures; and S10 packaged execution/layout in the browser-mode matrix. Phase exits apply only to their included contract groups, preserving the previously delivered subset.

## S2 rotation translation trials

Orientations are 0, R, 2, L (indices 0,1,2,3). Each row begins with (0,0), followed by the listed four offsets. Coordinates use positive y downward; apply offsets to the rotated anchor.

| Transition | JLSTZ offsets after (0,0) | I offsets after (0,0) |
| --- | --- | --- |
| 0 to R | (-1,0),(-1,-1),(0,2),(-1,2) | (-2,0),(1,0),(-2,1),(1,-2) |
| R to 0 | (1,0),(1,1),(0,-2),(1,-2) | (2,0),(-1,0),(2,-1),(-1,2) |
| R to 2 | (1,0),(1,1),(0,-2),(1,-2) | (-1,0),(2,0),(-1,-2),(2,1) |
| 2 to R | (-1,0),(-1,-1),(0,2),(-1,2) | (1,0),(-2,0),(1,2),(-2,-1) |
| 2 to L | (1,0),(1,-1),(0,2),(1,2) | (2,0),(-1,0),(2,-1),(-1,2) |
| L to 2 | (-1,0),(-1,1),(0,-2),(-1,-2) | (-2,0),(1,0),(-2,1),(1,-2) |
| L to 0 | (-1,0),(-1,1),(0,-2),(-1,-2) | (1,0),(-2,0),(1,2),(-2,-1) |
| 0 to L | (1,0),(1,-1),(0,2),(1,2) | (-1,0),(2,0),(-1,-2),(2,1) |
