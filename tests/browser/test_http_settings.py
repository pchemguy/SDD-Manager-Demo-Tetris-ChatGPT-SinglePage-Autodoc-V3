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
