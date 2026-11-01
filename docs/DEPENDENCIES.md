# Development environment and dependency evidence

## Development-only tools

Tests use Python 3.12, Node 24, pytest 8.4.2, Playwright 1.56.0 and jsonschema 4.25.1. requirements-dev.txt pins the direct test tools. The application does not require Python, Node or these packages to play.

For a dedicated developer installation, install into an owned target directory with python -m pip install --target <directory> -r requirements-dev.txt, then include that directory in PYTHONPATH. Set PLAYWRIGHT_BROWSERS_PATH to an absolute dedicated browser directory for installation and tests. Provision with python -m playwright install --only-shell chromium firefox. Run python -m pytest from the repository root with those environment variables.

## Observed Linux readiness

The dedicated job installation uses Playwright-managed Chromium headless shell 141.0.7390.37 (revision 1194) and Firefox 142.0.1 (revision 1495), downloaded through official Playwright endpoints. Chromium completed installation before the first installer was interrupted by a cancelled network-approval response. That installer had stopped; its owned empty lock was removed. Firefox's first endpoint returned a malformed/truncated archive; Playwright's official Microsoft fallback supplied a valid 96.7 MiB archive and completed extraction. No alternate browser distribution was substituted.

The unmodified Firefox content sandbox failed writing /proc/self/uid_map with EPERM and crashed content processes. For this restricted host's trusted local probes only, TETRIS_FIREFOX_SANDBOX_OVERRIDE=1 makes the test launcher pass MOZ_DISABLE_CONTENT_SANDBOX=1 to Firefox. It does not alter the host sandbox or global settings. Omit this flag on a host where the normal content sandbox works; re-evaluate after host changes. Do not use the reduced-isolation launch for arbitrary untrusted pages.

With the process-local override, python -m pytest tests/unit/test_harness.py tests/browser/test_environment.py -q passed three tests in 3.68 seconds. Each browser completed two fresh context/input/Canvas/teardown cycles: direct-file navigation and a localhost HTTP page. Canvas pixel values, rather than DOM presence alone, established rasterization. These are environment checks, not application acceptance. Full Chromium, headed/native-window behavior and native Windows execution were not tested.

## Application dependencies

Core gameplay uses browser built-ins. A SQLite CDN distribution is selected, pinned and verified in its implementation task; no SQLite support is claimed yet.
