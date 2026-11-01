"""Reach real UI game over with deterministic pieces and native animation time."""
def test_game_over_and_new_game_through_actual_controls(app_page):
    p = app_page
    p.locator('#start').click()
    for _ in range(21):
        if p.locator('#phase').inner_text() == 'Game over':
            break
        next_kind=p.locator('#next-kind').inner_text()
        for _ in range(20):
            p.keyboard.press('ArrowDown')
        p.wait_for_function("next=>document.getElementById('phase').textContent==='Game over'||document.getElementById('next-kind').textContent!==next",arg=next_kind,timeout=5000)
    assert p.locator('#phase').inner_text() == 'Game over'
    assert int(p.locator('#score').inner_text()) > 0
    p.locator('#pause').click()
    assert p.locator('#phase').inner_text() == 'Playing'
    assert p.locator('#score').inner_text() == '0'

def test_visibility_handler_freezes_until_explicit_resume(app_page):
    p = app_page
    p.locator('#start').click()
    p.evaluate("Object.defineProperty(document,'hidden',{get:()=>true,configurable:true});document.dispatchEvent(new Event('visibilitychange'))")
    assert p.locator('#phase').inner_text() == 'Paused'
    p.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")
    assert p.locator('#phase').inner_text() == 'Paused'
