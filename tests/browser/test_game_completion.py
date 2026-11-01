"""Reach real UI game over with deterministic pieces and controlled game time."""
def test_game_over_and_new_game_through_actual_controls(app_page):
    p = app_page
    p.clock.install(time='2026-01-01T00:00:00Z')
    p.reload()
    p.clock.pause_at('2026-01-01T00:00:02Z')
    p.locator('#start').click()
    for _ in range(21):
        if p.locator('#phase').inner_text() == 'Game over':
            break
        for _ in range(20):
            p.keyboard.press('ArrowDown')
        p.clock.run_for(1100)
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
