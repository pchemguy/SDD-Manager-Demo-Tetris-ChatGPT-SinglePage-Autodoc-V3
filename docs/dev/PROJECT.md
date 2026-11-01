# Single-page HTML Tetris

## Purpose and users

Provide a keyboard-operated Tetris game for desktop browser users, distributed as one readable HTML file. Players can open it directly from disk or serve the same file over HTTP(S), including localhost. The project demonstrates practical specification-driven development through useful, independently verified releases.

## Intended outcome

Deliver a playable classic baseline first, then bounded capability increments covering the complete scope below. Each completed, verified and integrated implementation phase receives a version tag, release notes and a GitHub release. The proposed first playable version is 0.1.0; subsequent capability increments increase the minor version, with 1.0.0 marking completion of the agreed target. Detailed phase ownership and exits belong in PLAN.

## Complete target scope

- Classic Tetris: a 10 by 20 visible board, seven tetrominoes, movement, rotation, gravity, soft drop, line clearing, score, levels, starting/restarting, pause/resume and game over.
- Modern rules: hold, next-piece preview, ghost, 7-bag generation, wall kicks, hard drop and a default full gravity interval of grounded lock delay. Hard drop follows the general locking policy unless its immediate-lock setting is selected.
- Conditional ghost visibility based on whether the projected piece lies above the board midline.
- Penetrator activation by hotkey, consuming one available bonus until locking. Penetrators pass through occupied cells without destroying them and lock only at a non-overlapping in-bounds position. Their hard-drop and ghost destinations agree on the lowest valid landing. A four-line clear awards one bonus, capped at three. Penetrators are entirely white; regular pieces never use white. The info panel shows one symbol per bonus.
- Six configurable settings: ghost visibility, hard-drop availability, next-preview visibility, hard-drop locking policy, general locking policy and hold availability. Deliver an in-memory, session-only configuration increment before persistence.
- HTTP(S) configuration persistence using per-setting URL parameter, cookie, then default precedence. Explicit valid URL values are saved to cookies even when equal to defaults. Missing parameters retain cookies. Setting changes update cookies and query parameters.
- In file mode, initialize settings from defaults and keep them in memory. Do not read/write cookies or read/modify configuration parameters, including during manual restore.
- A session leaderboard containing the top ten completed-game results by score.
- Manual Save/Restore at the bottom of the settings panel, hidden with that panel. One downloaded JSON or SQLite file contains the leaderboard and all six settings. Restore replaces the leaderboard and applies settings, updating cookies/query parameters only over HTTP(S).
- Stable result IDs, non-negative integer scores and UTC completion timestamps survive both formats. JSON has a format version, results and settings plus a published JSON Schema. SQLite uses high_scores(id, score, timestamp), settings(key, value), unique setting keys and metadata format versioning. Validate the complete input before changing any application or persistence state; errors leave it unchanged.

## Interface and operation

Panels appear left to right: leaderboard, game info and controls, centered board, settings, controls/help. The board and game info remain visible. Separate leaderboard, settings and help toggles appear above the two gameplay buttons in the info panel. Its bottom contains only Start/Restart on the left and Pause/Start on the right. Other gameplay actions use the keyboard. The right button starts a ready game, pauses a running game and resumes a paused game.

Keep the board centered as optional panels open or close. On narrow screens, retain access to all panels through scrolling without collapsing or hiding the board and game info. Final sizing and keyboard mappings belong in the specification.

## Delivery constraints and proposed approach

Detect execution mode automatically with location.protocol. All application HTML, CSS and JavaScript reside in one well-organized HTML file; no application server, build step or package installation is required to play. Established-CDN JavaScript libraries are the only permitted external dependencies. Tests, documentation, the JSON Schema and release metadata are supporting repository artifacts, rather than additional required application files.

Use plain JavaScript, a Canvas board and HTML panels. A DOM-cell board is also viable and would ease cell-level inspection, but adds presentation elements without simplifying the gameplay model. A framework introduces unnecessary dependencies for this fixed application. The proposed approach keeps game rules independent of rendering within the embedded script.

Any CDN-dependent SQLite capability must work from both execution modes and report loading failure clearly without changing state. Network-free SQLite operation is not promised by this proposal. Verify actual packaged HTML in Chromium and Firefox, through direct file navigation and HTTP(S)-mode serving, before claiming the corresponding phase delivered.

## Proposed gameplay decisions for acceptance

These recommendations resolve the material gameplay boundaries; detailed contracts belong in the specification.

| Concern | Proposed behavior and rationale |
| --- | --- |
| Ghost straddling the midline | In dynamic mode, hide if any projected occupied cell is in visible rows 0-9; show only when every cell lies in rows 10-19. This avoids displaying a partly upper-half ghost. |
| Lock delay | Start one full current gravity interval when a piece first becomes grounded. Grounded movement/rotation and repeated hard drops do not restart it. Actual lift-off clears it; grounding again starts a new interval. Pause freezes elapsed time. |
| Penetrator movement and locking | Passing through occupied cells is allowed, but a move/rotation must retain an entirely in-bounds, non-overlapping landing at or below the resulting position. Descent stops at that lowest valid landing, including when an intermediate overlapping row lies closer to the floor. Never lock an overlapping piece or delete existing cells. |
| Penetrator activation and hold | Start each game with zero bonuses. Activation spends one immediately, is irreversible for that piece and cannot be repeated on an already active penetrator. Disable hold while penetrator is active; otherwise allow one hold per falling piece. Activation that opens a lower landing releases grounding; otherwise preserve its existing delay. |
| Completed games and restart | Add a result once on game over, including a zero score. Restarting abandons the current unfinished game and earns no result. Starting a game resets bonuses while retaining session settings and leaderboard. |
| Leaderboard ties | Sort descending score, then earlier UTC completion time, then stable ID, retaining at most ten. Restore rejects duplicate IDs and invalid records rather than silently repairing them. |
| Defaults | Dynamic ghost visibility; hard drop, next preview and hold enabled; full-interval general locking; hard drop follows that policy. |
| Invalid URL/cookie settings | Ignore an invalid value and continue to the next source for that setting. Reject duplicate configuration parameters as invalid for that setting. Do not save invalid values. File mode never consults these sources. |
| Invalid manual restore | Reject the entire file on unsupported versions, malformed schema, invalid timestamps/scores/settings, duplicate IDs/keys or missing/extra settings. Stage and validate all content before applying any result, setting, cookie or query change. |
| Live settings and restore | Visual and availability changes take effect immediately. A locking-policy change preserves existing grounded elapsed time; it never grants a delay reset. Restore changes settings and leaderboard, not the board or active game; pause a running game for file interaction and require explicit resume. |

## Scope limits

The target is one desktop browser game. Multiplayer, accounts, automatic leaderboard persistence and native/extension packages are outside the supplied scope. Manual saves contain results and settings, not an in-progress board. Precise scoring, timing, keys, file limits and data contracts remain downstream specification details within the accepted scope.
