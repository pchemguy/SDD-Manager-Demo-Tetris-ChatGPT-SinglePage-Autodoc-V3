"""Full validation must complete before any visible or persistent commit."""
import json
import pytest
from playwright.sync_api import expect
from sql_assets import dependency
from sql_cases import database,INVALID
from session_data import saved_session
from test_file_failures import state,restore,payload


def test_invalid_sqlite_preserves_results_settings_cookies_url_and_board(app_page,mode,tmp_path):
    p=app_page
    if mode=='file':
        p.add_init_script("""window.persistenceTouches=0;Object.defineProperty(document,'cookie',{get(){persistenceTouches++;throw Error('forbidden');},set(){persistenceTouches++;throw Error('forbidden');}});history.replaceState=()=>{persistenceTouches++;throw Error('forbidden');};""")
        p.reload()
    restore(p,saved_session())
    p.locator('#start').click();p.keyboard.press('ArrowDown');p.locator('#pause').click()
    before=state(p);board=p.locator('#board').evaluate('c=>c.toDataURL()')
    cases=[database(tmp_path/(name+'.db'),mutation) for name,mutation in INVALID.items()]
    good=database(tmp_path/'valid.db')
    cases.extend([good+b'trailing',good[:100]+b'\xff'*100+good[200:],b'SQLite format 3\0'+b'\xff'*100])
    for data in cases:
        p.locator('#restore-file').set_input_files(payload(data,'pretend.json'))
        expect(p.locator('#save-session')).to_be_enabled(timeout=35000)
        expect(p.locator('#message')).to_contain_text('Cannot restore')
        assert state(p)==before
        assert p.locator('#board').evaluate('c=>c.toDataURL()')==board
        assert p.locator('#restore-file').input_value()==''
    if mode=='file':assert p.evaluate('persistenceTouches')==0


@pytest.mark.parametrize('fault',['network','integrity'])
def test_dependency_failure_keeps_json_game_and_live_state_usable(app_page,tmp_path,fault):
    p=app_page
    restore(p,saved_session());before=state(p)
    url=dependency()['url']
    if fault=='network':p.route(url,lambda route:route.abort('failed'))
    else:p.route(url,lambda route:route.fulfill(body='window.untrustedSQLiteExecuted=true;',content_type='application/javascript',headers={'Access-Control-Allow-Origin':'*'}))
    p.locator('#restore-file').set_input_files(payload(database(tmp_path/'valid.db')))
    expect(p.locator('#save-session')).to_be_enabled(timeout=35000)
    expect(p.locator('#message')).to_contain_text('Cannot restore')
    expect(p.locator('#message')).to_contain_text('JSON and the game remain available')
    assert state(p)==before
    assert p.evaluate('window.untrustedSQLiteExecuted===undefined')
    assert p.locator('script[src*="sql-asm-memory-growth"]').count()==0
    # JSON does not call the failed dependency; one valid download still works.
    p.locator('#save-session').click()
    with p.expect_download() as download:p.locator('#save-json').click()
    path=tmp_path/'still.json';download.value.save_as(path)
    assert json.loads(path.read_bytes())['settings']==saved_session()['settings']
    p.locator('#start').click();p.locator('#board').focus();p.keyboard.press('ArrowDown')
    assert p.locator('#score').inner_text()=='1'
