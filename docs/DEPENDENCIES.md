# Development environment and dependency evidence

## Development-only tools

Tests use Python 3.12, Node 24, pytest 8.4.2, Playwright 1.56.0 and jsonschema 4.25.1. requirements-dev.txt pins the direct test tools. The application does not require Python, Node or these packages to play.

For a dedicated developer installation, install into an owned target directory with python -m pip install --target <directory> -r requirements-dev.txt, then include that directory in PYTHONPATH. Set PLAYWRIGHT_BROWSERS_PATH to an absolute dedicated browser directory for installation and tests. Provision with python -m playwright install --only-shell chromium firefox. Run python -m pytest from the repository root with those environment variables.

## Observed Linux readiness

The dedicated job installation uses Playwright-managed Chromium headless shell 141.0.7390.37 (revision 1194) and Firefox 142.0.1 (revision 1495), downloaded through official Playwright endpoints. Chromium completed installation before the first installer was interrupted by a cancelled network-approval response. That installer had stopped; its owned empty lock was removed. Firefox's first endpoint returned a malformed/truncated archive; Playwright's official Microsoft fallback supplied a valid 96.7 MiB archive and completed extraction. No alternate browser distribution was substituted.

The unmodified Firefox content sandbox failed writing /proc/self/uid_map with EPERM and crashed content processes. For this restricted host's trusted local probes only, TETRIS_FIREFOX_SANDBOX_OVERRIDE=1 makes the test launcher pass MOZ_DISABLE_CONTENT_SANDBOX=1 to Firefox. It does not alter the host sandbox or global settings. Omit this flag on a host where the normal content sandbox works; re-evaluate after host changes. Do not use the reduced-isolation launch for arbitrary untrusted pages.

With the process-local override, python -m pytest tests/unit/test_harness.py tests/browser/test_environment.py -q passed three tests in 3.68 seconds. Each browser completed two fresh context/input/Canvas/teardown cycles: direct-file navigation and a localhost HTTP page. Canvas pixel values, rather than DOM presence alone, established rasterization. These are environment checks, not application acceptance. Full Chromium, headed/native-window behavior and native Windows execution were not tested.

## Application dependencies

Core gameplay and JSON exchange use browser built-ins. SQLite exchange uses the optional sql.js pin and verified initialization described below; no worker or local companion file is required.

## CI actions

The workflow uses actions/checkout, actions/setup-python and actions/setup-node at v7, matching examples read from their official repository READMEs during implementation. CI selects Python 3.12, Node 24 and the pinned requirements; its browser path is job-specific. These are development dependencies, not application runtime imports.

## CI host recovery

Initial run 41313200837 selected Ubuntu 26.04 through ubuntu-latest; Playwright browser dependency provisioning rejected that unsupported host before tests or package gates ran. CI is pinned to ubuntu-24.04, matching the pinned runner's supported browser distribution. This is a host-selection correction; the runner version and browser coverage remain unchanged. Recovery run 41313446648 on 4974b429e6a6d7b64b191823577dd977f7bacd4c completed successfully: 49 tests in 47.84 seconds, package creation and independent artifact-name/hash validation all passed. No Firefox content-sandbox override was needed on that hosted runner. Reassessment is resolved.

## Packaged classic baseline checks

The generated dist/tetris.html was verified byte-identical to source and tested with TETRIS_TEST_ARTIFACT=dist/tetris.html. The complete local suite passed 57 cases in 81.02 seconds, including real UI game completion/restart in Chromium/Firefox under both file and HTTP, modeled visibility/focus pause, five viewport widths, package rejection cases and Canvas rendering. Chromium and Firefox screenshots were captured; the Chromium file-mode image was visually inspected for board centering, visible info/buttons, help readability and clipping. Native OS-window event delivery remains unverified. CI packages before browser tests and uses the same artifact selector.

## Phase 1 final review

Prettier 3.6.2 was installed in a dedicated external development-tool directory and used to format the sole HTML without adding a runtime dependency. Source formatting checks passed. Review fixed repeated unchanged aria-live status writes and accepted valid self-closing version metadata in packaging; all five focused reproductions failed before those fixes and passed afterward. The rebuilt artifact passed 62 pytest checks in 85.19 seconds and independent filename/hash validation. Direct PNG inspection confirmed cyan piece pixels at the expected coordinates in all four browser/mode screenshots; no rendering workaround was required.

## Timing checks

Engine tests supply deterministic elapsed time, including exact 999/1000ms contact boundaries. Browser scenarios use native animation time and wait for observable piece/game transitions. During Phase 3 verification, Playwright 1.56.0 virtual-clock runs intermittently moved from 2000ms back to an earlier clock value in Firefox and stopped driving game frames; pre-navigation installation and frame synchronization did not reliably repair it. That diagnostic layer was removed rather than changing game timing or dropping Firefox/file coverage. The browser suite still exercises the actual packaged HTML in both protocols/browsers.

Phase 4 adds a small deterministic controller-ordering test with a manual performance/animation-frame stub. It verifies that time before a keyboard drop is applied before the action and cannot shorten the new contact delay. This uses the actual packaged HTML without a mutable engine hook; ordinary end-to-end play continues to use native animation time.

## SQLite runtime pin

The optional, lazy runtime is sql.js 1.13.0, MIT licensed, using its documented single-script asm.js memory-growth compatibility distribution. SQLite itself is public domain. Official package metadata and README were checked at the upstream v1.13.0 tag (https://github.com/sql-js/sql.js/tree/v1.13.0). The pin is https://cdn.jsdelivr.net/npm/sql.js@1.13.0/dist/sql-asm-memory-growth.js, 1,364,441 bytes, SHA-256 443b49452c24718016c93d4b65727161fc4836a2a68554696b6cae9f2b8ec1be, with browser integrity sha384-00ZgJXAcDlCvHMXdlbRKwEZqgJIwmYhL5sXMl8gVTMAX4kFr42gyz11YXIsk5U45. The CDN response permits anonymous cross-origin loading. The initialized runtime reports SQLite 3.49.1. No worker, WASM download or companion local file is needed.

The loader coalesces requests, checks the initializer, bounds loading/initialization to 30 seconds, removes its script and timer on every outcome and permits retry after failure. Only SQLite invokes it; gameplay and JSON are independent. SQLite requires network access to this CDN on first use in a page session. No dependency bytes are bundled into the application or release.

Local Chromium and Firefox rejected the managed proxy's certificate (ERR_CERT_AUTHORITY_INVALID / SEC_ERROR_UNKNOWN_ISSUER); TLS verification was not disabled. The optional test flag TETRIS_SQLITE_VERIFIED_FETCH=1 routes only this exact URL using bytes fetched by Python with configured proxy/CA verification and independently checked SHA-384. Browsers still enforce SRI and initialize the actual distribution through script loading in file and HTTP modes; request inventory verifies no companion or worker requests. Omit the flag in ordinary environments and CI to verify direct CDN loading. The optional development cache is ignored by Git. An attempted system package installation could not change user/group identity in this host; no system trust modification was made.

## Direct CDN and complete exchange evidence

Hosted run 41336253654 on 4fc3457bb8a5333a0c20c4e4b3912b60172cb63c passed 235 tests in 320.71s, including direct CDN script initialization in Chromium/Firefox under file/HTTP. Neither the local verified-fetch route nor the Firefox sandbox override was set. Package inventory/hash gates also passed. This resolves the direct CDN-loading gate; the local proxy trust limitation remains accurately scoped to this development host.

The expanded packaged suite passed 252 tests locally in 339.46s, covering 22 invalid SQLite content classes, network/SRI failures with usable JSON/gameplay, cleanup and the accessible Save dialog at 320/480/768/1280/1600 widths in all four combinations. Chromium's actual 1280px dialog screenshot was visually inspected: readable text/buttons, centered modal and unclipped content. Local tests used the documented verified-fetch route. Full final-version and exact phase-tip checks remain the release gates.
