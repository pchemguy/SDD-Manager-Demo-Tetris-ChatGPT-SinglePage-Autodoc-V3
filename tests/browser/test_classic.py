"""Playable classic path through the actual single-file page in both browsers/modes."""
def test_start_input_pause_and_restart(app_page):
    page = app_page
    assert page.locator('#phase').inner_text() == 'Ready'
    page.locator('#start').click()
    assert page.locator('#phase').inner_text() == 'Playing'
    assert page.locator('#board').evaluate('(c)=>c===document.activeElement')
    page.keyboard.press('ArrowDown')
    assert page.locator('#score').inner_text() == '1'
    # Rasterization must contain colored active cells, not merely an empty canvas.
    assert page.locator('#board').evaluate('''c=>{const a=c.getContext('2d').getImageData(0,0,300,600).data;for(let i=0;i<a.length;i+=4)if(Math.max(a[i],a[i+1],a[i+2])>120&&Math.max(a[i],a[i+1],a[i+2])-Math.min(a[i],a[i+1],a[i+2])>50)return true;return false;}''')
    page.locator('#pause').click()
    assert page.locator('#phase').inner_text() == 'Paused'
    page.keyboard.press('ArrowDown')
    assert page.locator('#score').inner_text() == '1'
    page.locator('#pause').click()
    assert page.locator('#phase').inner_text() == 'Playing'
    page.locator('#start').click()
    assert page.locator('#score').inner_text() == '0'
    assert page.locator('#phase').inner_text() == 'Playing'

def test_right_button_starts_ready_play(app_page):
    app_page.locator('#pause').click()
    assert app_page.locator('#phase').inner_text() == 'Playing'
    assert app_page.locator('#info .bottom-controls button').all_text_contents() == ['Start/Restart','Pause/Start']
