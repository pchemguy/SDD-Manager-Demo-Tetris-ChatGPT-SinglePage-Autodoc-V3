import json
from urllib.parse import parse_qs,urlsplit
from playwright.sync_api import expect
from sql_cases import database
from session_data import ranked_session,saved_session
from test_file_failures import state,restore


def test_sqlite_restore_save_json_and_sqlite_preserve_exact_fields(app_page,mode,tmp_path):
    p=app_page
    restore(p,database(tmp_path/'source.db'))
    before=state(p)
    if mode=='http':
        params=parse_qs(urlsplit(p.url).query)
        cookies={c['name']:c['value'] for c in p.context.cookies()}
        for key,value in saved_session()['settings'].items():
            assert params[key]==[value] and cookies['tetris_'+key]==value
    else:assert p.context.cookies()==[] and urlsplit(p.url).query==''
    # Successful restore renews cookie lifetimes; compare content/attributes.
    def stable(value):
        return {**value,'cookies':[{k:v for k,v in c.items() if k!='expires'} for c in value['cookies']]}
    for format in ['json','sqlite']:
        p.locator('#save-session').click()
        expect(p.locator('#save-format')).to_be_visible()
        with p.expect_download() as download:p.locator('#save-'+format).click()
        path=tmp_path/('saved.'+format);download.value.save_as(path)
        assert download.value.suggested_filename=='tetris-session.'+format
        if format=='json':assert json.loads(path.read_bytes())==ranked_session()
        restore(p,path.read_bytes())
        assert stable(state(p))==stable(before)


def test_save_choice_cancel_preserves_session_and_requires_resume(app_page):
    p=app_page
    p.locator('#start').click()
    before=state(p)
    p.locator('#save-session').click()
    expect(p.locator('#save-format')).to_be_visible()
    assert p.locator('#save-json').evaluate('e=>e===document.activeElement')
    assert p.locator('#phase').inner_text()=='Paused'
    p.keyboard.press('Escape')
    expect(p.locator('#save-format')).to_be_hidden()
    expect(p.locator('#save-session')).to_be_enabled()
    assert state(p)==before
    assert p.locator('#phase').inner_text()=='Paused'


def test_save_dialog_fits_five_widths_with_keyboard_focus(app_page,browser_name,mode):
    p=app_page
    for width in [320,480,768,1280,1600]:
        p.set_viewport_size({'width':width,'height':800})
        p.locator('#save-session').click()
        box=p.locator('#save-format').bounding_box()
        assert box['x']>=0 and box['x']+box['width']<=width
        for selector in ['#save-json','#save-sqlite','#cancel-save']:
            b=p.locator(selector).bounding_box()
            assert b['x']>=box['x'] and b['x']+b['width']<=box['x']+box['width']
        assert p.locator('#save-json').evaluate('e=>e===document.activeElement')
        if width==1280:
            from domain import ROOT
            output=ROOT/'test-results';output.mkdir(exist_ok=True)
            p.screenshot(path=str(output/('save-dialog-'+browser_name+'-'+mode+'.png')))
        p.locator('#cancel-save').click()
        expect(p.locator('#save-format')).to_be_hidden()
