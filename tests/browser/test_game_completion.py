"""Reach real game over and verify the completed-result lifecycle."""
import datetime
import re
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
    score=p.locator('#score').inner_text()
    assert p.locator('#high-scores li').count()==1
    assert p.locator('#high-scores strong').inner_text()==score
    result_id=p.locator('#high-scores li').get_attribute('data-id')
    assert re.fullmatch(r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}',result_id)
    timestamp=p.locator('#high-scores time').get_attribute('datetime')
    assert re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z',timestamp)
    assert datetime.datetime.fromisoformat(timestamp).utcoffset().total_seconds()==0
    p.wait_for_timeout(100)
    assert p.locator('#high-scores li').count()==1
    p.locator('#pause').click()
    assert p.locator('#phase').inner_text() == 'Playing'
    assert p.locator('#score').inner_text() == '0'
    assert p.locator('#high-scores li').get_attribute('data-id')==result_id
    assert result_id not in p.url
    assert p.context.cookies()==[]
    p.reload()
    assert p.locator('#high-scores li').count()==0

def test_visibility_handler_freezes_until_explicit_resume(app_page):
    p = app_page
    p.locator('#start').click()
    p.evaluate("Object.defineProperty(document,'hidden',{get:()=>true,configurable:true});document.dispatchEvent(new Event('visibilitychange'))")
    assert p.locator('#phase').inner_text() == 'Paused'
    p.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")
    assert p.locator('#phase').inner_text() == 'Paused'
