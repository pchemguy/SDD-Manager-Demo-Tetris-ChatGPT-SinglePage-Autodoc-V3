"""Six native settings, session lifetime, keyboard isolation and panel anchoring."""
from playwright.sync_api import expect

DEFAULTS={'ghost':'dynamic','hardDrop':'on','next':'on','hardDropLock':'general','lock':'interval','hold':'on'}
CHANGED={'ghost':'visible','hardDrop':'off','next':'off','hardDropLock':'immediate','lock':'failed','hold':'off'}

def values(p):
    return p.locator('#settings select').evaluate_all('(es)=>Object.fromEntries(es.map(e=>[e.dataset.setting,e.value]))')


def test_settings_restart_and_reload_by_protocol(app_page, mode):
    p=app_page
    assert p.locator('#settings select').count()==6
    assert values(p)==DEFAULTS
    before=p.url
    for key,value in CHANGED.items(): p.locator('#setting-'+key).select_option(value)
    p.locator('#setting-hold').focus()
    p.keyboard.press('r')
    assert p.locator('#phase').inner_text()=='Ready'
    p.locator('#start').click()
    p.keyboard.press('c')
    p.keyboard.press('Enter')
    assert p.locator('#held-kind').inner_text()=='—'
    assert p.locator('#score').inner_text()=='0'
    assert p.locator('#next').is_hidden()
    p.locator('#start').click()
    assert values(p)==CHANGED
    if mode=='file': assert p.url==before
    p.reload()
    assert values(p)==(DEFAULTS if mode=='file' else CHANGED)


def test_settings_ghost_lock_controls_and_panel_anchor(app_page):
    p=app_page
    assert p.locator('#toggle-settings').count()==1
    for width in [320,480,768,1280,1600]:
        p.set_viewport_size({'width':width,'height':800})
        before=p.locator('#board').evaluate('e=>e.getBoundingClientRect().left+scrollX')
        p.locator('#toggle-settings').click()
        assert p.locator('#settings').is_hidden()
        assert abs(p.locator('#board').evaluate('e=>e.getBoundingClientRect().left+scrollX')-before)<1
        p.locator('#toggle-settings').click()
    p.set_viewport_size({'width':1280,'height':800})
    p.locator('#start').click()
    p.locator('#setting-ghost').select_option('hidden')
    assert p.locator('#board').evaluate("c=>{const a=c.getContext('2d').getImageData(94,574,1,1).data;return a[1]<100;}")
    p.locator('#setting-ghost').select_option('visible')
    assert p.locator('#board').evaluate("c=>{const a=c.getContext('2d').getImageData(94,574,1,1).data;return a[1]>150;}")
    p.locator('#setting-hardDropLock').select_option('immediate')
    p.locator('#board').focus()
    p.keyboard.press('Enter')
    assert p.locator('#next-kind').inner_text()=='T'
    p.locator('#setting-hardDropLock').select_option('general')
    p.locator('#setting-lock').select_option('failed')
    p.locator('#start').click()
    p.keyboard.press('Enter')
    assert p.locator('#next-kind').inner_text()=='Z'
    p.keyboard.press('ArrowDown')
    assert p.locator('#next-kind').inner_text()=='T'


def test_protocol_isolation_and_blocked_persistence(app_page, mode):
    p=app_page
    p.add_init_script("""window.persistenceTouches=0;Object.defineProperty(document,'cookie',{get(){window.persistenceTouches++;throw Error('cookie access');},set(){window.persistenceTouches++;throw Error('cookie access');}});history.replaceState=()=>{window.persistenceTouches++;throw Error('history access');};""")
    p.goto(p.url+'?ghost=hidden#keep')
    assert p.locator('#setting-ghost').count()==1
    assert p.locator('#setting-ghost').input_value()==('dynamic' if mode=='file' else 'hidden')
    p.locator('#setting-ghost').select_option('visible')
    if mode=='file':
        assert p.evaluate('persistenceTouches')==0
    else:
        assert p.evaluate('persistenceTouches')>0
        assert 'persistent configuration is unavailable' in p.locator('#message').inner_text()
    assert p.url.endswith('?ghost=hidden#keep')
