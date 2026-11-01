# Single-page HTML Tetris

Classic Tetris in one HTML file: seven tetrominoes, movement and rotation, soft drop, gravity, line clearing, score, levels, pause, restart and game over. Version 0.5.0 adds per-setting HTTP(S) URL and cookie persistence. Remaining capabilities follow the bounded [delivery plan](docs/dev/PLAN.md).

## Play

Download [tetris.html](https://github.com/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-SinglePage-Autodoc-V3/releases/latest/download/tetris.html) from the latest published release and open it directly in Chromium or Firefox. No Node.js, package installation or application server is required.

The same file works over HTTP(S). For a localhost example with Python already available, run python -m http.server 8000 in the file's directory, then open http://localhost:8000/tetris.html. The page detects its execution mode automatically.

## Controls and rules

| Control | Action |
| --- | --- |
| Start/Restart | Start or abandon the unfinished game and restart |
| Pause/Start | Start ready play, pause, or resume |
| Left / Right | Move |
| Down | Soft drop |
| Up / X / Space | Rotate clockwise |
| Z | Rotate counterclockwise |
| C / Shift | Hold, once per falling piece |
| Enter | Hard drop |
| P | Activate an available penetrator bonus |
| Escape | Pause / resume |
| R | Start / restart |
| Leaderboard toggle | Show/hide session results |
| Settings toggle | Show/hide configuration |
| Help toggle | Show/hide keyboard help |

By default, locking waits one full gravity interval after becoming grounded. Grounded movement/rotation does not restart it; actual lift-off starts a fresh delay at the next contact. Pause freezes game time. Losing focus or hiding the page pauses play and requires explicit resume. The board stays anchored as panels toggle; narrow screens can scroll the scene.

Clear rows for points and advance one level every ten lines. The queue uses shuffled seven-piece bags. SRS wall/floor kicks, one-piece hold and next preview are enabled. A ghost previews landing and hides if any projected cell is above the midline. Enter hard-drops to the same landing, with two points per row and the same full contact delay.

## Release files

Each classic release includes tetris.html, README.md and SHA256SUMS. Check the downloaded HTML against SHA256SUMS if verifying its bytes. Release artifact names remain stable across versions. GitHub's automatic source archive is separate from the deployable HTML.

## Development and verification

requirements-dev.txt pins pytest, Playwright and JSON Schema tooling. [Dependency/setup evidence](docs/DEPENDENCIES.md) explains dedicated installation/browser paths and this restricted Linux host's process-local Firefox recovery. Playing does not require developer tools.

From the repository root, run python -m pytest with that isolated environment. Run python scripts/package.py --out dist, then python scripts/check_artifact_names.py dist --version 0.5.0. Use the current VERSION for subsequent releases. Set TETRIS_TEST_ARTIFACT=dist/tetris.html to make browser checks exercise the generated artifact; CI does this after packaging.

Headless Chromium and Playwright Firefox are checked through direct-file and localhost HTTP execution, including the five widths in SPEC. Native OS-window event delivery and native Windows execution are not established by these headless checks. See [TASKS](docs/dev/TASKS.md) and implementation reports for exact current evidence.

Development uses [SDD Manager](SDD-MANAGER.md). See the [AI-assisted development disclosure](AI_DISCLOSURE.md). The [project brief](docs/dev/PROJECT.md), [specification](docs/dev/SPEC.md) and [handoff](docs/dev/HANDOFF.md) describe the complete intended scope and current checkpoint.

Hold a piece with C or Shift, once per falling piece. The hold and next displays show orientation-zero pieces; the queue draws from shuffled seven-piece bags. Rotations use SRS wall/floor kicks.

Clear four lines at once for one penetrator bonus, up to three. P spends one to make the current piece white until it locks. It can pass through occupied cells, but its final landing must not overlap them. Ghost and hard drop select the lowest legal landing. Hold is disabled for an active penetrator; settled pieces return to their ordinary colors.

## Settings and persistence

The Settings panel controls ghost visibility, hard drop, next preview, hard-drop locking, general locking and hold. Defaults use a dynamic ghost, enabled hard drop/preview/hold, a full gravity interval of contact delay and hard drop following the general policy. The alternative general policy locks on a failed downward attempt. Immediate hard-drop locking also locks a zero-distance drop. Changing policies preserves contact time. Input time is accounted before movement or a policy change, so time preceding contact cannot shorten its delay.

Settings apply immediately and survive game restart and panel hiding. The Settings toggle preserves the board anchor and native controls keep keyboard focus.

In HTTP(S) mode each setting resolves independently: a valid single explicit URL parameter, then its saved cookie, then its default. Parameter names are ghost, hardDrop, next, hardDropLock, lock and hold; cookie names add the tetris_ prefix. Invalid or duplicate values fall through. Explicit URL values are saved into cookies even when equal to defaults; omitted URL keys retain saved values. Changing a setting updates its cookie and URL parameter without navigation, preserving unrelated parameters and the fragment. Cookies use a one-year lifetime, path=/ and SameSite=Lax, plus Secure on HTTPS. A persistence failure warns while keeping the setting active in memory.

| URL key | Allowed values | Default |
| --- | --- | --- |
| ghost | hidden, dynamic, visible | dynamic |
| hardDrop | off, on | on |
| next | off, on | on |
| hardDropLock | general, immediate | general |
| lock | failed, interval | interval |
| hold | off, on | on |

For example, append ?ghost=visible&hardDrop=off to an HTTP(S) game URL. Omitted settings continue to use their saved cookies or defaults.

In direct-file mode settings always start from defaults, remain in memory and reset on reload. The application does not read/write cookies or read/modify configuration query parameters in that mode. Leaderboard and manual file exchange follow in later increments.

## Leaderboard

Completed games enter the session top ten automatically, including zero scores. Results rank by descending score, then ascending UTC completion time and stable ID. The panel shows scores and readable completion times; each record retains its original UTC timestamp and UUID v4. Restart and pause keep history without adding an abandoned game. Reload clears the history; results are never stored in cookies or URL parameters.
