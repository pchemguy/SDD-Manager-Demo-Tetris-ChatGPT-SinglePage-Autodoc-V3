# Saved session formats

## JSON version 1

The canonical [JSON Schema](dev/contracts/session.schema.json) uses Draft 2020-12. A saved session is UTF-8 JSON with exactly formatVersion, results and settings. The format version is 1, independently of the application release version.

```json
{
  "formatVersion": 1,
  "results": [
    {
      "id": "00000000-0000-4000-8000-000000000001",
      "score": 1200,
      "timestamp": "2026-11-01T12:34:56.789Z"
    }
  ],
  "settings": {
    "ghost": "dynamic",
    "hardDrop": "on",
    "next": "on",
    "hardDropLock": "general",
    "lock": "interval",
    "hold": "on"
  }
}
```

Results contain at most ten objects; an empty array is valid. Each object has exactly these fields:

| Field | Constraint |
| --- | --- |
| id | Unique lowercase UUID v4, preserved across exports/imports |
| score | Non-negative integer from 0 through 9007199254740991 |
| timestamp | Calendar-valid UTC completion time, years 0001-9999, exactly YYYY-MM-DDTHH:mm:ss.sssZ |

Validation checks calendar correctness by parsing and formatting the timestamp, including leap days. It rejects offsets, missing milliseconds and normalized invalid dates. Decimal/exponent numeric spellings are accepted only when their exact mathematical value is a safe integer; fractional or oversized literals cannot pass through floating-point rounding or underflow.

All six settings are required with exactly the keys and values in the schema and [settings guide](../README.md#settings-and-persistence). Extra keys, missing keys, unknown versions, duplicate result IDs and coerced values are rejected. Results may arrive unsorted; successful validation ranks them by descending score, ascending UTC timestamp and then ID without changing any field.

The decoder rejects malformed UTF-8, a byte-order mark, duplicate JSON member names at any depth (including differently escaped spellings of the same name), trailing content and invalid JSON grammar. It bounds nesting and item counts; all schema-valid sessions fit those bounds. The browser embeds the validator and does not fetch the schema or require a validation library/CDN.

## Manual exchange contract

Manual files are limited to 1 MiB. Validation completes before replacing results or settings and before any cookie/URL update. An invalid file leaves those values unchanged and displays a clear error; pausing play for file interaction is allowed. A valid restore replaces the session leaderboard and all settings, preserving IDs, scores and UTC timestamps. It does not restore or reset the active board. HTTP(S) mirrors restored settings into cookies and URL parameters; direct-file mode changes memory only.

JSON downloads use tetris-session.json. Application source and release checksums are separate from session data. The SQLite format is added in its own delivery increment.

## SQLite version 1

SQLite exports are genuine databases with PRAGMA user_version=1, exactly these application declarations, and their automatically generated primary-key indexes:

```sql
CREATE TABLE high_scores (id TEXT PRIMARY KEY NOT NULL, score INTEGER NOT NULL CHECK(score >= 0), timestamp TEXT NOT NULL);
CREATE TABLE settings (key TEXT PRIMARY KEY NOT NULL, value TEXT NOT NULL);
```

The importer accepts whitespace/case variations in these declarations; other declarations are rejected even if they appear similar. It also checks actual column metadata, primary keys, required fields, database page length and integrity. It rejects extra tables, columns, indexes, views and triggers. No SQL supplied by a file is executed; all queries are fixed application statements. Every insert uses bound parameters. Six uniquely keyed settings rows are required. Runtime value types must be TEXT for IDs/timestamps/settings and INTEGER for safe non-negative scores. The same UUID, calendar, enum, duplicate and ten-result rules apply as JSON.

Each operation uses one temporary in-memory database. Prepared statements are freed and the database is closed on success or failure; cleanup failure rejects the operation. Nothing is committed to the active session by either codec.
