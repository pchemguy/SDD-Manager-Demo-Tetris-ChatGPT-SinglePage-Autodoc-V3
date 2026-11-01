from domain import evaluate

HARNESS="""
function harness(href,cookie,protocol='https:'){
 const writes=[];const caps={getURL:()=>href,getCookie:()=>cookie,setCookie(line){writes.push(line);const pair=line.split(';')[0],name=pair.split('=')[0];cookie=cookie.split(';').map(x=>x.trim()).filter(x=>x&&!x.startsWith(name+'=')).concat(pair).join('; ');},replaceURL(value){href=value;}};
 const adapter=createProtocolAdapter(protocol,caps);return {adapter,writes,url:()=>href,cookie:()=>cookie};
}
"""

def test_independent_url_cookie_default_resolution_and_explicit_default_save():
    assert evaluate(HARNESS+"""const h=harness('https://game.test/tetris.html?ghost=hidden&hardDrop=on&hold=off&tag=x#keep','tetris_ghost=visible; tetris_hardDrop=off; tetris_next=off; tetris_hardDropLock=immediate; tetris_lock=failed; tetris_hold=on');console.log(JSON.stringify([h.adapter.readInitialSettings(),h.writes.map(x=>x.split(';')[0])]));""") == [{'ghost':'hidden','hardDrop':'on','next':'off','hardDropLock':'immediate','lock':'failed','hold':'off'},['tetris_ghost=hidden','tetris_hardDrop=on','tetris_hold=off']]


def test_invalid_duplicate_url_values_fall_through_independently():
    assert evaluate(HARNESS+"""const h=harness('https://game.test/?ghost=hidden&ghost=visible&next=nope&hold=&hardDropLock=wrong','tetris_ghost=visible; tetris_next=off; tetris_hold=off; tetris_hardDropLock=bad; tetris_lock=bad');console.log(JSON.stringify([h.adapter.readInitialSettings(),h.writes.length]));""") == [{'ghost':'visible','hardDrop':'on','next':'off','hardDropLock':'general','lock':'interval','hold':'off'},0]


def test_malformed_duplicate_cookies_and_percent_values():
    assert evaluate(HARNESS+"""const h=harness('https://game.test/?ghost=%ZZ','tetris_ghost=%ZZ; tetris_hold=on; tetris_hold=off; tetris_next=%6fn; tetris_hardDropLock=immediate');console.log(JSON.stringify(h.adapter.readInitialSettings()));""") == {'ghost':'dynamic','hardDrop':'on','next':'on','hardDropLock':'immediate','lock':'interval','hold':'on'}


def test_file_adapter_never_touches_persistence_capabilities():
    assert evaluate("""let touches=0;const caps=new Proxy({},{get(){touches++;throw Error('forbidden capability');}});const a=createProtocolAdapter('file:',caps);console.log(JSON.stringify([a.mode,a.readInitialSettings(),a.persist(DEFAULT_SETTINGS).ok,touches]));""") == ['file',{'ghost':'dynamic','hardDrop':'on','next':'on','hardDropLock':'general','lock':'interval','hold':'on'},True,0]
