import base64, json, sqlite3
from domain import evaluate
from sql_assets import asset
from session_data import saved_session,ranked_session


def sql_eval(body):
    return evaluate('const initialize=require('+json.dumps(str(asset()))+');(async()=>{const SQL=await initialize();'+body+'})();')


def test_export_is_real_sqlite_with_exact_schema_metadata_types_and_fields(tmp_path):
    raw=saved_session()
    encoded=sql_eval('const c=createSQLiteCodec(async()=>({ok:true,value:SQL}));const out=await c.encode('+json.dumps(raw)+');console.log(JSON.stringify({ok:out.ok,bytes:out.ok?Buffer.from(out.value).toString("base64"):out}));')
    assert encoded['ok']
    data=base64.b64decode(encoded['bytes']);assert data.startswith(b'SQLite format 3\0')
    path=tmp_path/'session.sqlite';path.write_bytes(data)
    with sqlite3.connect(path) as db:
        assert db.execute('PRAGMA user_version').fetchone()==(1,)
        assert db.execute('PRAGMA integrity_check').fetchone()==('ok',)
        assert db.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name").fetchall()==[('high_scores',),('settings',)]
        rows=db.execute('SELECT id,score,timestamp,typeof(score) FROM high_scores ORDER BY score DESC').fetchall()
        assert rows==[(r['id'],r['score'],r['timestamp'],'integer') for r in ranked_session()['results']]
        assert dict(db.execute('SELECT key,value FROM settings'))==raw['settings']


def test_invalid_export_never_opens_database_and_resources_close_on_insert_failure():
    assert sql_eval("""let opens=0,closes=0,frees=0;function Database(){opens++;const db=new SQL.Database();const prepare=db.prepare.bind(db);db.prepare=sql=>{const s=prepare(sql);const free=s.free.bind(s);s.free=()=>{frees++;return free();};s.run=()=>{throw Error('injected');};return s;};const close=db.close.bind(db);db.close=()=>{closes++;close();};return db;}const c=createSQLiteCodec(async()=>({ok:true,value:{Database}}));const invalid=await c.encode({});const bad=await c.encode("""+json.dumps(saved_session())+""");console.log(JSON.stringify([invalid.ok,bad.code,opens,closes,frees]));""")==[False,'invalidSQLite',1,1,1]
