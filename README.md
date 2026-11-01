# Single-page HTML Tetris

Version 1.0.0 delivers classic Tetris, modern piece rules, penetrator bonuses, configurable locking, a session leaderboard and validated JSON/SQLite Save and Restore. All application HTML, CSS and JavaScript live in one tetris.html file.

## Play

Download [tetris.html](https://github.com/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-SinglePage-Autodoc-V3/releases/latest/download/tetris.html) and open it directly in Chromium or Firefox. No installation or application server is required. Gameplay and JSON exchange work offline. SQLite exchange loads the optional pinned sql.js library from jsDelivr on first use in each page session and requires network access; failure leaves JSON and gameplay available.

The same file works over HTTP(S). For localhost with Python already installed, run `python -m http.server 8000` in its directory and open http://localhost:8000/tetris.html. The page automatically detects direct-file versus HTTP(S) execution.

## Controls and rules

| Control | Action |
| --- | --- |
| Start/Restart | Start, or abandon the unfinished game and restart |
| Pause/Start | Start ready play, pause or resume |
| Left / Right | Move |
| Down | Soft drop |
| Up / X / Space | Rotate clockwise |
| Z | Rotate counterclockwise |
| C / Shift | Hold, once per falling piece |
| Enter | Hard drop |
| P | Spend an available penetrator bonus |
| Escape | Pause / resume |
| R | Start / restart |

Gameplay actions other than the two bottom buttons use the keyboard. The three toggles immediately above them show/hide Leaderboard, Settings and Controls/help. The board stays centered when panels toggle. Narrow screens can scroll the scene to reach adjacent panels; the board and game information remain visible.

The queue uses shuffled seven-piece bags and SRS wall/floor kicks. Hold and the next-piece preview show orientation-zero pieces. Clear rows for 100/300/500/800 points for one/two/three/four lines, multiplied by the current level. Soft drop awards one point per row and hard drop two. Every ten lines advances a level and increases gravity.

By default, a piece locks after one full gravity interval from becoming grounded. Grounded movement, rotation and repeated hard drops do not restart the timer. Actual lift-off clears contact time and the next contact starts a fresh interval. Pause freezes game time. Losing focus or hiding the page pauses play and requires explicit resume. Hard drop follows the general policy unless immediate locking is selected; immediate locking also applies to a zero-distance hard drop.

The ghost previews the same landing as hard drop. In dynamic mode it hides whenever any projected cell is above row 10 of the 20-row board, including a piece straddling the midline; it reappears when every projected cell is in the lower half.

Clear four lines at once to earn one penetrator bonus, up to three. P spends one and turns the current falling piece entirely white until it locks. It can pass through occupied cells without destroying them. Ghost and hard drop find its lowest legal landing, which must fit entirely inside the board without overlap. Hold is blocked while penetration is active. Bonuses appear as lightning symbols and reset on restart; settled penetrators return to their ordinary piece color.

## Settings and persistence

Settings apply immediately, survive game restart and panel hiding, and use these keys in URLs, cookies and manual files:

| URL/file key | Allowed values | Default |
| --- | --- | --- |
| ghost | hidden, dynamic, visible | dynamic |
| hardDrop | off, on | on |
| next | off, on | on |
| hardDropLock | general, immediate | general |
| lock | failed, interval | interval |
| hold | off, on | on |

The alternative general locking policy locks on a failed downward movement attempt. Changing policies preserves contact time; time before an input cannot shorten a new contact delay.

In HTTP(S) mode each setting resolves independently: a valid single explicit URL parameter, its saved cookie, then its default. Invalid or duplicate values fall through to the next source. Cookie names add the tetris_ prefix. Explicit URL values are saved even when equal to defaults; omitted parameters retain saved values. A setting change updates its cookie and query parameter without navigation, preserving unrelated parameters and the fragment. Cookies use a one-year lifetime, path=/ and SameSite=Lax, plus Secure on HTTPS. Persistence failure displays a warning while retaining the active setting in memory.

For example, append `?ghost=visible&hardDrop=off` to an HTTP(S) game URL. Other settings retain saved cookies or defaults.

In direct-file mode settings start from defaults on every reload and remain in memory. The application does not read/write cookies or read/modify configuration URL parameters in that mode. Manual Restore remains available and changes settings only in memory.

## Leaderboard and manual files

The leaderboard keeps the ten best completed games for the current page session, including zero scores. Ranking uses descending score, then ascending UTC completion time and stable ID. Each result retains its lowercase UUID v4, non-negative safe integer score and canonical UTC timestamp. Restart does not record abandoned play or clear history. Reload clears results; they are never stored in cookies or URLs.

Save and Restore sit at the bottom of Settings and hide with that panel. Save opens a keyboard-accessible JSON/SQLite choice, with JSON selected first and Cancel available. It downloads one tetris-session.json or tetris-session.sqlite containing the current top ten results and all six settings. Restore detects SQLite by its file header and otherwise parses UTF-8 JSON; extensions and MIME types are not trusted. Files may be at most 1 MiB.

The entire file is validated before changing results, settings, cookies or URLs. Valid Restore replaces the session leaderboard and settings, preserves exact fields and keeps the active board intact. HTTP(S) also mirrors all six settings into cookies and query parameters. Invalid files show a clear error and leave these values unchanged. File interaction pauses running play and blocks concurrent actions; use Pause/Start to resume explicitly afterward. Cancel changes no saved data.

Both formats use format version 1, independent of the application release version. JSON rejects duplicate members, malformed UTF-8, trailing content and invalid schema/values. SQLite checks metadata, exact declarations, columns, primary keys, integrity and runtime types; it rejects unexpected tables, views, triggers and indexes. See [file formats](docs/FILE-FORMATS.md) and [JSON Schema](docs/dev/contracts/session.schema.json). SQLite load/initialization is bounded to 30 seconds and can be retried; JSON has no CDN dependency.

## Release files

Each release provides tetris.html, README.md, session.schema.json and SHA256SUMS. Compare downloaded bytes with SHA256SUMS to verify them. Artifact names stay stable across versions. GitHub's automatic source archives are separate from the deployable HTML.

## Development and verification

[Dependency/setup evidence](docs/DEPENDENCIES.md) documents pinned development tools, the SQLite URL/license/integrity, isolated browser installation and this managed host's local verification limits. Playing requires none of the Python/Node development tools.

From the repository root, with requirements-dev.txt installed in a dedicated Python environment and Playwright browsers provisioned, run:

```sh
python scripts/package.py --out dist
TETRIS_TEST_ARTIFACT=dist/tetris.html python -m pytest -q
python scripts/check_artifact_names.py dist --version 1.0.0
```

CI tests the actual packaged HTML in headless Chromium and Playwright Firefox through direct-file and localhost HTTP execution, including 320/480/768/1280/1600 widths. HTTPS cookie attributes are separately tested at the adapter boundary; this does not claim live HTTPS hosting. Native Windows and headed OS-window event delivery are outside the verified scope. Consult [implementation reports](docs/dev/reports/) for exact results and limits.

Development uses [SDD Manager](SDD-MANAGER.md); see the [AI-assisted development disclosure](AI_DISCLOSURE.md), [project brief](docs/dev/PROJECT.md), [specification](docs/dev/SPEC.md), [delivery plan](docs/dev/PLAN.md), [tasks](docs/dev/TASKS.md) and [handoff](docs/dev/HANDOFF.md).
