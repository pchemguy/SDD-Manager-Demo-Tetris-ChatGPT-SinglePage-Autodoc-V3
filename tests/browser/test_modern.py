"""Modern controls exercised through production UI, without engine globals."""
def freeze(p):
    p.clock.install(time='2026-01-01T00:00:00Z')
    p.reload()
    p.clock.pause_at('2026-01-01T00:00:02Z')
    p.locator('#start').click()


def test_hold_preview_drop_and_contact_interval(app_page):
    p=app_page
    freeze(p)
    assert p.locator('#next-kind').inner_text() == 'Z'
    p.keyboard.press('c')
    assert p.locator('#held-kind').inner_text() == 'I'
    assert p.locator('#next-kind').inner_text() == 'T'
    p.keyboard.press('Shift')
    assert p.locator('#held-kind').inner_text() == 'I'
    p.keyboard.press('Enter')
    assert p.locator('#score').inner_text() == '36'
    before=p.locator('#board').evaluate('c=>c.toDataURL()')
    p.keyboard.press('Enter')
    assert p.locator('#score').inner_text() == '36'
    p.clock.run_for(900)
    assert p.locator('#next-kind').inner_text() == 'T'
    p.clock.run_for(200)
    assert p.locator('#next-kind').inner_text() == 'S'
    assert p.locator('#board').evaluate('c=>c.toDataURL()') != before
    p.keyboard.press('c')
    assert p.locator('#held-kind').inner_text() == 'T'
    assert p.locator('#next-kind').inner_text() == 'S'


def test_ghost_outline_and_native_modifier_isolation(app_page):
    p=app_page
    freeze(p)
    # Empty-board I ghost lies at row 19; outline is cyan at its upper edge.
    assert p.locator('#board').evaluate("c=>{const a=c.getContext('2d').getImageData(94,574,1,1).data;return a[1]>150&&a[2]>150;}")
    before=p.locator('#board').evaluate('c=>c.toDataURL()')
    p.locator('#board').dispatch_event('keydown',{'key':'r','ctrlKey':True})
    assert p.locator('#board').evaluate('c=>c.toDataURL()') == before
    p.keyboard.press('Escape')
    p.keyboard.press('Enter')
    assert p.locator('#score').inner_text() == '0'


def test_help_lists_hard_drop_key(app_page):
    app_page.locator('#toggle-help').click()
    assert 'Enter' in app_page.locator('#help').inner_text()
    assert 'Hard drop' in app_page.locator('#help').inner_text()
