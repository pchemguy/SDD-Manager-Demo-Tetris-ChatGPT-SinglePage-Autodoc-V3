# Single-page HTML Tetris

Classic Tetris in one HTML file: seven tetrominoes, movement and rotation, soft drop, gravity, line clearing, score, levels, pause, restart and game over. Version 0.2.0 adds modern rules. Remaining capabilities follow the bounded [delivery plan](docs/dev/PLAN.md).

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
| Escape | Pause / resume |
| R | Start / restart |
| Help toggle | Show/hide keyboard help |

Locking waits one full gravity interval after becoming grounded. Grounded movement/rotation does not restart it; actual lift-off starts a fresh delay at the next contact. Pause freezes game time. Losing focus or hiding the page pauses play and requires explicit resume. The board stays anchored as panels toggle; narrow screens can scroll the scene.

Clear rows for points and advance one level every ten lines. The queue uses shuffled seven-piece bags. SRS wall/floor kicks, one-piece hold and next preview are enabled. A ghost previews landing and hides if any projected cell is above the midline. Enter hard-drops to the same landing, with two points per row and the same full contact delay.

## Release files

Each classic release includes tetris.html, README.md and SHA256SUMS. Check the downloaded HTML against SHA256SUMS if verifying its bytes. Release artifact names remain stable across versions. GitHub's automatic source archive is separate from the deployable HTML.

## Development and verification

requirements-dev.txt pins pytest, Playwright and JSON Schema tooling. [Dependency/setup evidence](docs/DEPENDENCIES.md) explains dedicated installation/browser paths and this restricted Linux host's process-local Firefox recovery. Playing does not require developer tools.

From the repository root, run python -m pytest with that isolated environment. Run python scripts/package.py --out dist, then python scripts/check_artifact_names.py dist --version 0.2.0. Use the current VERSION for subsequent releases. Set TETRIS_TEST_ARTIFACT=dist/tetris.html to make browser checks exercise the generated artifact; CI does this after packaging.

Headless Chromium and Playwright Firefox are checked through direct-file and localhost HTTP execution, including the five widths in SPEC. Native OS-window event delivery and native Windows execution are not established by these headless checks. See [TASKS](docs/dev/TASKS.md) and implementation reports for exact current evidence.

Development uses [SDD Manager](SDD-MANAGER.md). See the [AI-assisted development disclosure](AI_DISCLOSURE.md). The [project brief](docs/dev/PROJECT.md), [specification](docs/dev/SPEC.md) and [handoff](docs/dev/HANDOFF.md) describe the complete intended scope and current checkpoint.

Hold a piece with C or Shift, once per falling piece. The hold and next displays show orientation-zero pieces; the queue draws from shuffled seven-piece bags. Rotations use SRS wall/floor kicks.
