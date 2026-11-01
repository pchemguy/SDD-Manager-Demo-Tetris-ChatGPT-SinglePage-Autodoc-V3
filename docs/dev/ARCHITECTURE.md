# Architecture

## Context and delivery boundary

[PROJECT](PROJECT.md) defines one desktop browser game distributed as a self-contained application HTML file. Canvas renders the board; semantic HTML owns information, settings, help and file controls. Embedded JavaScript uses named logical sections within one classic script, without module imports or a server runtime.

## Major blocks

| Block | Responsibility | Owns |
| --- | --- | --- |
| Game domain | Deterministic piece motion, landing, locking, scoring, bag, hold and penetrator rules | Board, active piece, queue, hold, bonuses and game state |
| Application controller | Convert input and monotonic elapsed time into domain operations; coordinate pause, restart, settings and restore | Clock scheduling, pressed keys, interaction busy state |
| Presentation | Render immutable snapshots; expose keyboard, settings, panel and file interactions | Canvas/DOM nodes and optional-panel visibility |
| Session data | Six-setting value validation, session leaderboard and validated replacement | Canonical configuration and completed-result collection |
| Boundary adapters | Protocol detection, URL/cookies, JSON/SQLite encoding, files and dependency loading | Browser I/O handles and temporary codec resources |

The controller depends on the domain and session data. Presentation submits intents to the controller and reads its snapshots. Boundary adapters return decoded candidates or errors; they cannot directly mutate domain or session data. Domain functions do not read DOM, wall clocks, cookies, URLs or files. Inject randomness, elapsed time and ID/timestamp production at the application boundary for reproducible verification.

## State and data flow

A single controller serializes input, gravity ticks and restore commits. Domain operations publish snapshots and a completed-game event; the controller records that event once in the session leaderboard. Rendering consumes state rather than owning game rules. The settings schema is the sole source of allowed keys, values and defaults, shared by controls and both persistence codecs.

Restore follows read/decode, complete validation, prepared replacement and commit. Validation uses a detached candidate and changes no live results, configuration, cookies or URL. The controller applies the canonical candidate once, then asks the HTTP(S) adapter to mirror settings. Browser persistence failures are surfaced; they never masquerade as successful persistence. Temporary SQLite databases and prepared statements are closed on success and failure. Restore excludes the active board and does not replay completed-game events.

## Execution modes and external dependencies

Inspect location.protocol once at startup. The file adapter initializes defaults and implements no configuration URL/cookie access. The HTTP(S) adapter resolves settings independently and writes their persistence representation. Both modes retain manual file download/upload. Unrecognized protocols show an unsupported-mode error rather than adopting HTTP persistence accidentally.

Core gameplay and JSON use browser built-ins. SQLite is an optional, lazily loaded, pinned CDN library behind the codec boundary; select a single-script browser distribution that does not require a local worker, companion file or local-file fetch. Dependency availability is verified in both modes before the SQLite phase is accepted. Loading failure leaves JSON and gameplay usable. Package version, URL, license and integrity metadata are pinned during the codec implementation task, based on an actual supported distribution; no unverified CDN URL is part of this architecture.

## Timing and visual stability

The controller uses a monotonic clock and explicit elapsed-time progression; pause and hidden-page suspension freeze game time. The domain owns grounded elapsed time and prevents grounded movement from resetting it. It computes one landing operation for ghost and hard drop, including penetrators. White belongs exclusively to penetrator piece rendering.

Use a centered board anchor with left and right panel groups. Optional-panel visibility cannot recenter the entire unequal-width group and shift the board. Narrow viewports permit scrolling and retain board/info access. Native settings controls retain focus and keyboard usability; game/panel actions return focus to the keyboard-focusable board as specified in SPEC; gameplay shortcuts are suppressed in editable controls and during file interaction.

## Design tradeoffs and verification seams

One deployable file does not require one undifferentiated global state. Cohesive closures and explicit function boundaries allow domain and validation checks without Canvas or real timers, while browser tests exercise the exact distributed HTML. Avoid frameworks, workers and build-time application assembly for this scope. No plugin mechanism, network backend or automatic result store is needed.

DECOMPOSITION defines component APIs and canonical models. SPEC owns behavioral guarantees and file contracts; PLAN owns staged delivery. Architecture readiness does not assert implementation or browser compatibility evidence.
