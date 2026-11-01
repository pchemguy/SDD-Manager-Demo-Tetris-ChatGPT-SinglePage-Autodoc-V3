import json
from domain import evaluate
from session_data import saved_session, ranked_session


def test_store_replacement_is_atomic_and_exports_detached_complete_data():
    raw=json.dumps(saved_session())
    assert evaluate('const raw='+raw+";const s=createSessionStore();s.record({...raw.results[0],score:1});const before=JSON.stringify(s.exportSession());const bad=s.replaceValidated({...raw,settings:{...raw.settings,hold:'bad'}});const unchanged=JSON.stringify(s.exportSession())===before;const good=s.replaceValidated(raw);raw.results[0].score=999;const copy=s.exportSession();copy.settings.hold='on';console.log(JSON.stringify([bad.ok,unchanged,good.ok,s.exportSession()]));") == [False,True,True,ranked_session()]


def test_file_read_validates_encoding_size_read_failures_and_version():
    assert evaluate('const raw='+json.dumps(saved_session())+""";(async()=>{const c=createFileController(async()=>{}),bytes=new TextEncoder().encode(JSON.stringify(raw));let readLarge=false;const good=await c.read({size:bytes.length,arrayBuffer:async()=>bytes.buffer});const large=await c.read({size:1048577,arrayBuffer:async()=>{readLarge=true;throw Error('must not read');}});const encoding=await c.read({size:2,arrayBuffer:async()=>new Uint8Array([0xc0,0xaf]).buffer});const versionBytes=new TextEncoder().encode(JSON.stringify({...raw,formatVersion:2}));const version=await c.read({size:versionBytes.length,arrayBuffer:async()=>versionBytes.buffer});const broken=await c.read({size:1,arrayBuffer:async()=>{throw Error('denied');}});console.log(JSON.stringify([good.value,large.code,readLarge,encoding.code,version.code,broken.code]));})();""") == [ranked_session(),'fileTooLarge',False,'invalidEncoding','unsupportedVersion','invalidValue']


def test_json_save_downloads_one_valid_file_and_invalid_candidate_downloads_none():
    assert evaluate('const raw='+json.dumps(saved_session())+""";(async()=>{const downloads=[];const c=createFileController(async(bytes,name,type)=>downloads.push({name,type,value:JSON.parse(new TextDecoder().decode(bytes))}));const good=await c.save('json',raw);const bad=await c.save('json',{...raw,settings:{}});console.log(JSON.stringify([good.ok,bad.ok,downloads]));})();""") == [True,False,[{'name':'tetris-session.json','type':'application/json','value':ranked_session()}]]
