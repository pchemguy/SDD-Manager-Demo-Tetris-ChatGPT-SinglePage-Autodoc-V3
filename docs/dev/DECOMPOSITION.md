# Component decomposition

## Scope and ownership

[ARCHITECTURE](ARCHITECTURE.md) defines dependency direction. This document owns canonical in-memory models and component API shapes. SPEC defines operation semantics, error codes, file representations and acceptance. Logical components are cohesive closures inside the embedded application script; they do not require separate application files or a public global API.

## Canonical models

| Type | Representation and owner |
| --- | --- |
| Cell / Board | Empty or one of I, J, L, O, S, T, Z; 20 rows of 10 cells. Engine owns settled cells; penetrator status belongs to the falling piece, not settled-cell identity. |
| FallingPiece | kind, orientation 0-3, integer x/y anchor, penetrator Boolean; Engine owns. Occupied-cell coordinates are derived from canonical SRS shape definitions. Matrix padding is not occupied space. |
| GameState | phase ready/running/paused/over, gameId, board, active piece or null, queue, held kind or null, holdUsed, score, lines, level, bonuses, groundedElapsedMs or null, gravityElapsedMs; Engine owns. |
| Settings | Exact string-key/string-value object defined below; SessionStore is canonical owner. Domain receives a read-only value for each action; presentation receives a copy. |
| Result | id string, score safe non-negative integer, timestamp canonical UTC string; SessionStore owns completed records. IDs use lowercase UUID v4; timestamps use YYYY-MM-DDTHH:mm:ss.sssZ. |
| Snapshot | Deep read-only copy of visible game state, current settings, leaderboard, derived landing cells and execution mode; Controller assembles; Renderer consumes. |
| SavedSession | formatVersion integer, results Result[], settings Settings; codecs create detached candidates. Validator creates the canonical validated value. |
| EngineEvent | gameCompleted with gameId and score, or stateChanged; Controller consumes. No DOM nodes, file handles or clock objects cross this boundary. |
| Outcome<T> | ok true with value T, or ok false with code and user-facing message; used for boundary/validation failures. Domain-invalid gameplay intents are safe no-ops with unchanged state. |

Settings keys, values and defaults have one design owner here:

| Key | Allowed values | Default |
| --- | --- | --- |
| ghost | hidden, dynamic, visible | dynamic |
| hardDrop | off, on | on |
| next | off, on | on |
| hardDropLock | general, immediate | general |
| lock | failed, interval | interval |
| hold | off, on | on |

Query parameter names and cookie suffixes use these exact keys. The domain uses immutable 4 by 4 SRS orientation definitions for I/J/L/O/S/T/Z and separate I versus JLSTZ kick tables. Empty matrix margins may extend outside the board; occupied cells may not. Spawn anchors align the topmost occupied row with row zero and center the occupied width. Final settlement requires every occupied cell in rows 0-19 and columns 0-9.

## Component APIs

### SettingsPolicy

Provides defaults(): Settings, parseValue(key, raw): Outcome<string>, resolve(urlValues, cookieValues): Settings and validateExact(candidate): Outcome<Settings>. Requires only the canonical setting definitions. Protocol adapters consume resolve; controls and Validator consume validateExact. Parsing does not perform browser I/O or silently invent extra settings.

### Engine

Provides createEngine(random: () => number), start(gameId: string), act(action: Action, settings: Settings), advance(elapsedMs: number, settings: Settings), setPaused(paused: Boolean), view(settings: Settings): GameView and drainEvents(): EngineEvent[]. Action is left/right/rotateCW/rotateCCW/softDrop/hardDrop/hold/penetrator. The controller owns invocation order. Engine owns all gameplay state, shape/kick definitions, bag generation, landing search and exactly-once completion production. Injected random values lie in [0,1). View returns detached data.

Internal collaboration operations cells(piece): CellPosition[], canSettle(piece, board): Boolean and landing(piece, board): Landing|null are private to the domain closure. Ghost, hard drop, gravity and penetrator movement use the same placement/landing rules; no renderer duplicates them. Engine consumes Settings rather than persisting a competing canonical configuration.

### SessionStore

Provides getSettings(): Settings, changeSettings(patch): Outcome<Settings>, record(result: Result), topResults(): Result[], exportSession(): SavedSession and replaceValidated(value: ValidatedSession). Owns sorting, top-ten truncation and duplicate-completion suppression. Requires SettingsPolicy and Validator; never writes cookies or URLs. Returned collections are detached. ValidatedSession is an internal capability/value produced only after full validation.

### Validator and codecs

Validator provides validateSession(raw: unknown): Outcome<ValidatedSession> and validateResult(raw): Outcome<Result>. It requires SettingsPolicy and the normative schema/semantic constraints in SPEC. JSONCodec exposes decode(text): Outcome<unknown>, encode(value: SavedSession): string. SQLiteCodec exposes ready(): Promise<Outcome<void>>, decode(bytes: Uint8Array): Promise<Outcome<unknown>> and encode(value): Promise<Outcome<Uint8Array>>. SQLiteCodec owns a temporary database per operation and closes statements/databases in finally paths. Neither codec receives SessionStore, DOM or persistence handles.

### ProtocolAdapter

createProtocolAdapter(protocol, browserCapabilities) returns mode, readInitialSettings(): Settings and persist(settings): Outcome<void>. File mode uses only defaults and an inert persistence operation; it has no cookie/query capabilities. HTTP(S) mode receives URL/history/cookie capabilities, preserves unrelated URL components and delegates value validation to SettingsPolicy. Controller receives failures and informs the user; this adapter cannot change leaderboard or board.

### FileController and DependencyLoader

FileController provides save(format: json|sqlite, value: SavedSession): Promise<Outcome<void>> and read(file: File): Promise<Outcome<ValidatedSession>>. It owns format selection, input size/signature checks, byte/text reads, temporary download URLs and disposal. It requires codecs and Validator. It cannot commit restored data. DependencyLoader exposes ensureSQLite(): Promise<Outcome<SQLiteRuntime>>, coalesces concurrent requests, uses a pinned browser script and returns a bounded clear failure; SQLiteCodec is its only consumer.

### Controller, Input and Renderer

Controller provides startOrRestart(), togglePause(), dispatch(action), updateSetting(key,value), save(format), restore(file), togglePanel(name) and snapshot(). It requires Engine, SessionStore, ProtocolAdapter, FileController and injected monotonic time, UTC time and UUID producers. It owns the serialized restore commit, game-time suspension, input busy flag and requestAnimationFrame scheduling. Completed events are converted to Result using gameId and UTC completion time, then recorded exactly once.

Input binds keyboard/native control events to controller operations and supplies no gameplay logic. It suppresses gameplay shortcuts in editable controls, repeated one-shot actions and file-interaction busy state. Renderer provides render(snapshot, panelVisibility) and showMessage(message, severity); it owns Canvas/DOM references, accessible labels and centered layout, and requires no codec/database access.

## Verification seams and invariants

Use injected randomness/time/IDs for domain and validation scenarios; compare snapshots before and after invalid intents. Exercise codecs through their public encode/decode methods and validate equivalent candidates, including malformed data and cleanup failures. Spy capabilities prove file mode never accesses cookies or configuration URLs. Browser interaction checks use the actual packaged HTML and keyboard/control bindings rather than a separate application build. No production test backdoor or mutable global is required; a test loader may extract the named pure sections from the same HTML for isolated checks.
