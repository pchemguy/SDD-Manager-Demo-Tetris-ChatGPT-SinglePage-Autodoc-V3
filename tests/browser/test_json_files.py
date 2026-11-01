"""Actual JSON downloads and file chooser restore in both supported modes."""
import json
from urllib.parse import parse_qs,urlsplit
from playwright.sync_api import expect
from session_data import saved_session, ranked_session
from test_settings_ui import values


def test_manual_json_download_restore_and_second_export(app_page, mode, tmp_path):
    p=app_page
    assert p.locator('#save-session').count()==1
    assert p.locator('#restore-session').count()==1
    p.locator('#start').click()
    p.keyboard.press('ArrowDown')
    before_url=p.url
    with p.expect_download() as first:
        p.locator('#save-session').click();p.locator('#save-json').click()
    download=first.value
    assert download.suggested_filename=='tetris-session.json'
    path=tmp_path/'first.json';download.save_as(path)
    first_data=json.loads(path.read_bytes())
    assert first_data['formatVersion']==1 and first_data['results']==[]
    assert p.locator('#phase').inner_text()=='Paused'
    before_board=p.locator('#board').evaluate('c=>c.toDataURL()')
    with p.expect_file_chooser() as choice:
        p.locator('#restore-session').click()
    choice.value.set_files({'name':'snapshot.data','mimeType':'application/octet-stream','buffer':json.dumps(saved_session()).encode()})
    expect(p.locator('#message')).to_contain_text('Restored')
    assert values(p)==saved_session()['settings']
    assert p.locator('#high-scores strong').all_text_contents()==['9007199254740991','0']
    assert p.locator('#high-scores li').evaluate_all('(es)=>es.map(e=>e.dataset.id)')==[r['id'] for r in ranked_session()['results']]
    assert p.locator('#high-scores time').evaluate_all('(es)=>es.map(e=>e.dateTime)')==[r['timestamp'] for r in ranked_session()['results']]
    assert p.locator('#phase').inner_text()=='Paused'
    assert p.locator('#score').inner_text()=='1'
    assert p.locator('#board').evaluate('c=>c.toDataURL()')==before_board
    if mode=='http':
        params=parse_qs(urlsplit(p.url).query)
        cookies={c['name']:c['value'] for c in p.context.cookies()}
        for key,value in saved_session()['settings'].items():
            assert params[key]==[value]
            assert cookies['tetris_'+key]==value
    else:
        assert p.url==before_url
        assert p.context.cookies()==[]
    with p.expect_download() as second:
        p.locator('#save-session').click();p.locator('#save-json').click()
    path=tmp_path/'second.json';second.value.save_as(path)
    assert json.loads(path.read_bytes())==ranked_session()
