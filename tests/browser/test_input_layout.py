"""Keyboard/focus/help and fixed board-anchor contracts."""
def test_help_toggle_and_board_anchor_at_five_widths(app_page):
    p = app_page
    assert p.locator('#toggle-help').count() == 1
    for width in [320,480,768,1280,1600]:
        p.set_viewport_size({'width':width,'height':800})
        p.wait_for_timeout(30)
        before = p.locator('#board').evaluate('(e)=>e.getBoundingClientRect().left+scrollX')
        p.locator('#toggle-help').click()
        assert p.locator('#help').is_visible()
        after = p.locator('#board').evaluate('(e)=>e.getBoundingClientRect().left+scrollX')
        assert abs(before-after) < 1
        assert p.locator('#info').is_visible()
        if width >= 1280:
            assert abs(p.locator('#board').evaluate('(e)=>{const r=e.getBoundingClientRect();return r.left+r.width/2}')-width/2) < 1
        p.locator('#toggle-help').click()
        assert p.locator('#help').is_hidden()

def test_restart_pause_and_editable_input_isolation(app_page):
    p = app_page
    p.locator('#start').click()
    p.keyboard.press('ArrowDown')
    p.keyboard.press('Escape')
    assert p.locator('#phase').inner_text() == 'Paused'
    p.keyboard.press('Escape')
    assert p.locator('#phase').inner_text() == 'Playing'
    p.keyboard.press('r')
    assert p.locator('#score').inner_text() == '0'
    p.evaluate('''()=>{const i=document.createElement('input');i.id='typing';document.body.append(i);i.focus();}''')
    p.keyboard.press('ArrowDown')
    p.keyboard.press('r')
    assert p.locator('#score').inner_text() == '0'
    assert p.locator('#typing').input_value() == 'r'

def test_focus_loss_handler_pauses_and_does_not_auto_resume(app_page):
    p = app_page
    p.locator('#start').click()
    p.evaluate("window.dispatchEvent(new Event('blur'))")
    assert p.locator('#phase').inner_text() == 'Paused'
    p.evaluate("window.dispatchEvent(new Event('focus'))")
    assert p.locator('#phase').inner_text() == 'Paused'


def test_rotation_aliases_repeat_and_ime_isolation(app_page):
    p = app_page
    p.locator('#start').click()
    p.keyboard.press('ArrowDown')
    before = p.locator('#board').evaluate('c=>c.toDataURL()')
    p.keyboard.press('x')
    rotated = p.locator('#board').evaluate('c=>c.toDataURL()')
    assert rotated != before
    p.locator('#board').dispatch_event('keydown', {'key':'x','repeat':True})
    assert p.locator('#board').evaluate('c=>c.toDataURL()') == rotated
    p.keyboard.press('z')
    assert p.locator('#board').evaluate('c=>c.toDataURL()') == before
    p.keyboard.press('Space')
    assert p.locator('#board').evaluate('c=>c.toDataURL()') == rotated
    score = p.locator('#score').inner_text()
    p.locator('#board').dispatch_event('keydown', {'key':'ArrowDown','isComposing':True})
    assert p.locator('#score').inner_text() == score
