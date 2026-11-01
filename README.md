# Single-page HTML Tetris

A single-file browser Tetris project under development. The [project brief](docs/dev/PROJECT.md) describes the proposed complete scope, execution modes and gameplay decisions. A playable classic source preview is available in tetris.html; the first verified release is still being prepared.

Development uses [SDD Manager](SDD-MANAGER.md). See the [AI-assisted development disclosure](AI_DISCLOSURE.md).

Preparation progress is recorded in [DOCS_TASKS](docs/dev/DOCS_TASKS.md), with decisions and checkpoint evidence in [DOCS_PREPARATION](docs/dev/DOCS_PREPARATION.md).

## Play the source preview

Open tetris.html directly in Chromium or Firefox, or serve the repository with an ordinary HTTP server and open tetris.html on localhost. No Node.js or application installation is needed to play.

Click Start/Restart (or Pause/Start from Ready). Left/Right move, Down soft-drops, Up/X/Space rotate clockwise and Z rotates counterclockwise. Escape pauses/resumes and R starts/restarts. The Help toggle shows the available controls. Pause/Start pauses/resumes; Start/Restart abandons the unfinished game and begins a fresh one. Locking waits one full gravity interval after contact; grounded movement does not restart the delay. Score, level and cleared lines appear beside the board.

Modern rules, settings, leaderboard and manual files are planned later increments, rather than available controls in this preview. Developer provisioning and observed browser limits are documented in [DEPENDENCIES](docs/DEPENDENCIES.md).

Losing focus or hiding the page pauses running play; return with Pause/Start or Escape. Narrow screens can scroll the scene; optional panels do not shift the board anchor. Native OS-window delivery remains outside the headless verification scope; handler behavior is tested separately.

## Package and verify

Development checks use pytest and the isolated browser environment described in docs/DEPENDENCIES.md. From the repository root, python scripts/package.py --out dist copies the exact HTML and supporting files, checks VERSION against embedded metadata and writes SHA256SUMS. Run python scripts/check_artifact_names.py dist --version 0.1.0 to independently check stable basenames and actual hashes. Use the current VERSION value for subsequent releases.

The release assets are tetris.html, README.md and SHA256SUMS. No assembly/build step is needed to play tetris.html. CI is configured to run pytest and the same packaging/name checks; local passing results do not imply an unobserved CI pass.
