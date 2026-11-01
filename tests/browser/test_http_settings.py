"""Persist all six settings only in HTTP mode and retain unrelated URL fields."""
from urllib.parse import urlsplit, parse_qs
from test_settings_ui import CHANGED, values


def test_all_setting_changes_and_reload_by_protocol(app_page, mode):
    p=app_page
    p.goto(p.url+'?other=alpha&other=beta#keep')
    for key,value in CHANGED.items(): p.locator('#setting-'+key).select_option(value)
    assert values(p)==CHANGED
    params=parse_qs(urlsplit(p.url).query)
    assert params['other']==['alpha','beta']
    assert urlsplit(p.url).fragment=='keep'
    cookies={c['name']:c for c in p.context.cookies()}
    if mode=='http':
        for key,value in CHANGED.items():
            assert params[key]==[value]
            assert cookies['tetris_'+key]['value']==value
            assert cookies['tetris_'+key]['path']=='/'
            assert cookies['tetris_'+key]['sameSite']=='Lax'
            assert cookies['tetris_'+key]['secure'] is False
        p.reload()
        assert values(p)==CHANGED
    else:
        assert set(params)=={'other'}
        assert cookies=={}


def test_startup_explicit_defaults_omitted_cookies_and_duplicates(app_page, mode, server_url):
    p=app_page
    p.context.add_cookies([{'name':'tetris_'+key,'value':value,'url':server_url} for key,value in CHANGED.items()])
    base=p.url
    p.goto(base+'?ghost=hidden&ghost=visible&hardDrop=on&hold=on&next=invalid')
    if mode=='http':
        expected={**CHANGED,'hardDrop':'on','hold':'on'}
        assert values(p)==expected
        saved={c['name']:c['value'] for c in p.context.cookies()}
        assert saved=={'tetris_'+key:value for key,value in expected.items()}
        p.goto(base)
        assert values(p)==expected
        assert {c['name']:c['value'] for c in p.context.cookies()}==saved
    else:
        from test_settings_ui import DEFAULTS
        assert values(p)==DEFAULTS
        assert {c['name']:c['value'] for c in p.context.cookies()}=={'tetris_'+key:value for key,value in CHANGED.items()}
