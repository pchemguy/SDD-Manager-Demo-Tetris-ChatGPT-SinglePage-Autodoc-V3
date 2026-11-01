"""Invalid content is atomic; busy/cancel/resource handling preserves manual semantics."""
import json
from playwright.sync_api import expect
from session_data import saved_session,ranked_session
from test_settings_ui import values


def payload(value,name='snapshot.any'):
    return {'name':name,'mimeType':'application/octet-stream','buffer':value if isinstance(value,bytes) else json.dumps(value).encode()}


def restore(p,value):
    p.locator('#restore-file').set_input_files(payload(value))
    expect(p.locator('#save-session')).to_be_enabled()
    expect(p.locator('#message')).to_contain_text('Restored')


def state(p):
    return {'settings':values(p),'rows':p.locator('#high-scores li').evaluate_all('(es)=>es.map(e=>[e.dataset.id,e.querySelector("strong").textContent,e.querySelector("time").dateTime])'),'url':p.url,'cookies':sorted(p.context.cookies(),key=lambda c:(c['name'],c['path']))}


def test_invalid_json_files_preserve_complete_live_and_persistent_state(app_page,mode):
    p=app_page
    if mode=='file':
        p.add_init_script("""window.persistenceTouches=0;Object.defineProperty(document,'cookie',{get(){persistenceTouches++;throw Error('forbidden');},set(){persistenceTouches++;throw Error('forbidden');}});history.replaceState=()=>{persistenceTouches++;throw Error('forbidden');};""")
    p.goto(p.url+'?ghost=hidden&other=keep#fragment')
    restore(p,saved_session())
    p.locator('#start').click();p.keyboard.press('ArrowDown');p.locator('#pause').click()
    before=state(p);board=p.locator('#board').evaluate('c=>c.toDataURL()')
    encoded=json.dumps(saved_session()).encode()
    bad_version=saved_session();bad_version['formatVersion']=2
    bad_date=saved_session();bad_date['results'][0]['timestamp']='2026-02-30T00:00:00.000Z'
    missing=saved_session();del missing['settings']['hold']
    duplicate=saved_session();duplicate['results'][1]['id']=duplicate['results'][0]['id']
    too_many=saved_session();too_many['results']=[{**too_many['results'][0],'id':'00000000-0000-4000-8000-'+format(i,'012x')} for i in range(11)]
    cases=[b'{"formatVersion":1,'+encoded[1:],encoded.replace(b'"hold": "off"',b'"hold": "off", "hold": "on"'),encoded+b' null',b'\xff',json.dumps(bad_version).encode(),json.dumps(bad_date).encode(),json.dumps(missing).encode(),json.dumps(duplicate).encode(),b' '*1048577,b'[]',encoded.replace(b'"score": 0',b'"score": 1.0000000000000001'),b'{"__proto__":{"polluted":true},'+encoded[1:],json.dumps(too_many).encode()]
    for n,data in enumerate(cases):
        p.locator('#restore-file').set_input_files(payload(data,'bad-'+str(n)+'.json'))
        expect(p.locator('#save-session')).to_be_enabled()
        expect(p.locator('#message')).to_contain_text('Cannot restore')
        assert state(p)==before
        assert p.locator('#board').evaluate('c=>c.toDataURL()')==board
        assert p.locator('#restore-file').input_value()==''
        assert p.evaluate('({}).polluted===undefined')
    if mode=='file': assert p.evaluate('persistenceTouches')==0


def test_busy_read_blocks_gameplay_and_second_file(app_page):
    p=app_page
    p.locator('#start').click();p.keyboard.press('ArrowDown')
    p.evaluate('() => {window.pendingReads=[];const bytes=new TextEncoder().encode("{\\"formatVersion\\": 1, \\"results\\": [{\\"id\\": \\"00000000-0000-4000-8000-000000000001\\", \\"score\\": 0, \\"timestamp\\": \\"2026-11-01T12:34:56.789Z\\"}, {\\"id\\": \\"00000000-0000-4000-8000-000000000002\\", \\"score\\": 9007199254740991, \\"timestamp\\": \\"2000-02-29T00:00:00.000Z\\"}], \\"settings\\": {\\"ghost\\": \\"visible\\", \\"hardDrop\\": \\"off\\", \\"next\\": \\"off\\", \\"hardDropLock\\": \\"immediate\\", \\"lock\\": \\"failed\\", \\"hold\\": \\"off\\"}}");File.prototype.arrayBuffer=function(){return new Promise((resolve,reject)=>{const timer=setTimeout(()=>reject(new Error(\'test gate timed out\')),5000);pendingReads.push(()=>{clearTimeout(timer);resolve(bytes.buffer.slice(0));});});};}')
    with p.expect_file_chooser() as chosen: p.locator('#restore-session').click()
    chosen.value.set_files(payload(saved_session()))
    expect(p.locator('#save-session')).to_be_disabled()
    assert p.locator('#start').is_disabled() and p.locator('#pause').is_disabled()
    assert p.locator('#settings select').evaluate_all('(es)=>es.every(e=>e.disabled)')
    p.locator('#board').focus();p.keyboard.press('r')
    assert p.locator('#score').inner_text()=='1'
    assert p.locator('#phase').inner_text()=='Paused'
    second=saved_session();second['results'][1]['score']=42
    p.locator('#restore-file').set_input_files(payload(second,'second.json'))
    assert p.evaluate('pendingReads.length')==1
    p.evaluate('pendingReads.shift()()')
    expect(p.locator('#save-session')).to_be_enabled()
    expect(p.locator('#message')).to_contain_text('Restored')
    assert p.locator('#high-scores strong').all_text_contents()==['9007199254740991','0']
    assert p.locator('#phase').inner_text()=='Paused'


def test_restore_cancel_handler_preserves_data(app_page):
    p=app_page
    restore(p,saved_session());before=state(p)
    with p.expect_file_chooser(): p.locator('#restore-session').click()
    p.locator('#restore-file').dispatch_event('cancel')
    expect(p.locator('#save-session')).to_be_enabled()
    assert state(p)==before
    assert p.locator('#restore-file').input_value()==''
    assert 'cancelled' in p.locator('#message').inner_text()


def test_settings_hides_file_buttons_and_download_urls_are_revoked(app_page):
    p=app_page
    p.add_init_script("""window.createdURLs=[];window.revokedURLs=[];const create=URL.createObjectURL.bind(URL),revoke=URL.revokeObjectURL.bind(URL);URL.createObjectURL=b=>{const u=create(b);createdURLs.push(u);return u;};URL.revokeObjectURL=u=>{revokedURLs.push(u);revoke(u);};""")
    p.reload();p.locator('#toggle-settings').click()
    assert p.locator('#save-session').is_hidden() and p.locator('#restore-session').is_hidden()
    p.locator('#toggle-settings').click()
    with p.expect_download(): p.locator('#save-session').click()
    p.wait_for_function('createdURLs.length===1&&revokedURLs.length===1')
    assert p.evaluate('createdURLs[0]===revokedURLs[0]')
    assert p.locator('a[download]').count()==0
