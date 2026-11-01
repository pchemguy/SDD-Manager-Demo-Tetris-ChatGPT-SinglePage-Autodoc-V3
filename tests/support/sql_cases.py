"""Independent SQLite fixtures; uploaded data never provides executable SQL."""
import sqlite3
from session_data import saved_session

SCORES='CREATE TABLE high_scores (id TEXT PRIMARY KEY NOT NULL, score INTEGER NOT NULL CHECK(score >= 0), timestamp TEXT NOT NULL)'
SETTINGS='CREATE TABLE settings (key TEXT PRIMARY KEY NOT NULL, value TEXT NOT NULL)'


def database(path, mutation=None):
    with sqlite3.connect(path) as db:
        db.execute(SCORES);db.execute(SETTINGS);db.execute('PRAGMA user_version=1')
        raw=saved_session()
        db.executemany('INSERT INTO high_scores VALUES (?,?,?)',[(r['id'],r['score'],r['timestamp']) for r in raw['results']])
        db.executemany('INSERT INTO settings VALUES (?,?)',raw['settings'].items())
        if mutation:mutation(db)
    return path.read_bytes()


INVALID = {
 'version':lambda d:d.execute('PRAGMA user_version=2'),
 'extra-table':lambda d:d.execute('CREATE TABLE other(x)'),
 'view':lambda d:d.execute('CREATE VIEW other AS SELECT 1'),
 'trigger':lambda d:d.execute('CREATE TRIGGER extra AFTER INSERT ON settings BEGIN DELETE FROM high_scores; END'),
 'index':lambda d:d.execute('CREATE INDEX extra ON settings(value)'),
 'extra-column':lambda d:d.execute('ALTER TABLE high_scores ADD COLUMN extra TEXT'),
 'missing-table':lambda d:d.execute('DROP TABLE settings'),
 'missing-key':lambda d:d.execute("DELETE FROM settings WHERE key='hold'"),
 'unknown-key':lambda d:d.execute("UPDATE settings SET key='other' WHERE key='hold'"),
 'invalid-setting':lambda d:d.execute("UPDATE settings SET value='bad' WHERE key='hold'"),
 'unsafe':lambda d:d.execute('UPDATE high_scores SET score=9007199254740992'),
 'fraction':lambda d:d.execute('UPDATE high_scores SET score=0.5'),
 'text-score':lambda d:d.execute("UPDATE high_scores SET score='not a number'"),
 'blob-score':lambda d:d.execute("UPDATE high_scores SET score=x'31'"),
 'bad-date':lambda d:d.execute("UPDATE high_scores SET timestamp='2026-02-30T00:00:00.000Z'"),
 'bad-id':lambda d:d.execute("UPDATE high_scores SET id='bad' WHERE score=0"),
 'too-many':lambda d:d.executemany('INSERT INTO high_scores VALUES (?,?,?)',[(f'00000000-0000-4000-8000-{n:012d}',0,'2026-01-01T00:00:00.000Z') for n in range(100,111)]),
 'missing-pk':lambda d:(d.execute('ALTER TABLE settings RENAME TO old'),d.execute('CREATE TABLE settings(key TEXT NOT NULL,value TEXT NOT NULL)'),d.execute('INSERT INTO settings SELECT * FROM old'),d.execute('DROP TABLE old')),
 'missing-check':lambda d:(d.execute('ALTER TABLE high_scores RENAME TO old'),d.execute('CREATE TABLE high_scores(id TEXT PRIMARY KEY NOT NULL,score INTEGER NOT NULL,timestamp TEXT NOT NULL)'),d.execute('INSERT INTO high_scores SELECT * FROM old'),d.execute('DROP TABLE old')),
}
