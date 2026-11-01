import base64,json
import pytest
from test_sql_encode import sql_eval
from sql_cases import database,INVALID
from session_data import ranked_session,saved_session


def decode(data):
    return sql_eval('const c=createSQLiteCodec(async()=>({ok:true,value:SQL}));console.log(JSON.stringify(await c.decode(new Uint8Array(Buffer.from('+json.dumps(base64.b64encode(data).decode())+',"base64")))));')


def test_independent_database_and_cross_codec_roundtrip(tmp_path):
    assert decode(database(tmp_path/'good.db'))=={'ok':True,'value':ranked_session()}
    assert sql_eval('const c=createSQLiteCodec(async()=>({ok:true,value:SQL}));const bytes=await c.encode('+json.dumps(saved_session())+');const out=await c.decode(bytes.value);console.log(JSON.stringify(JSONCodec.decode(JSONCodec.encode(out.value))));')=={'ok':True,'value':ranked_session()}


@pytest.mark.parametrize('case',list(INVALID))
def test_invalid_sqlite_rejected(case,tmp_path):
    assert not decode(database(tmp_path/'bad.db',INVALID[case]))['ok']


@pytest.mark.parametrize('kind',['empty','corrupt','trailing'])
def test_corrupt_and_trailing_rejected(kind,tmp_path):
    data=database(tmp_path/'good.db')
    if kind=='empty':data=b''
    if kind=='corrupt':data=data[:100]+b'\xff'*100+data[200:]
    if kind=='trailing':data+=b'trailing'
    assert not decode(data)['ok']


def test_resources_freed_on_success_failure_and_free_error():
    assert sql_eval('const raw='+json.dumps(saved_session())+""";const base=createSQLiteCodec(async()=>({ok:true,value:SQL}));const bytes=(await base.encode(raw)).value;let opens=0,closes=0,creates=0,frees=0;let fault=false;function Database(data){opens++;const db=new SQL.Database(data),prepare=db.prepare.bind(db),close=db.close.bind(db);db.prepare=sql=>{creates++;const s=prepare(sql),free=s.free.bind(s);s.free=()=>{frees++;free();if(fault)throw Error('free');};return s;};db.close=()=>{closes++;close();};return db;}const c=createSQLiteCodec(async()=>({ok:true,value:{Database}}));const good=await c.decode(bytes);fault=true;const bad=await c.decode(bytes);console.log(JSON.stringify([good.ok,bad.ok,opens,closes,creates===frees]));""")==[True,False,2,2,True]
