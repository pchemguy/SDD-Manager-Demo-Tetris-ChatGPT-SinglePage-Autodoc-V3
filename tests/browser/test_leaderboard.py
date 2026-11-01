"""Optional leaderboard sits left of info without moving the board anchor."""
def test_leaderboard_panel_order_and_toggle(app_page):
    p=app_page
    assert p.locator('#leaderboard').count()==1
    assert p.locator('#leaderboard-empty').is_visible()
    assert p.locator('#high-scores li').count()==0
    assert p.evaluate("['leaderboard','info','board','settings','help'].map(id=>document.getElementById(id)).every((e,i,a)=>i===0||Boolean(a[i-1].compareDocumentPosition(e)&Node.DOCUMENT_POSITION_FOLLOWING))")
    for width in [320,480,768,1280,1600]:
        p.set_viewport_size({'width':width,'height':800})
        before=p.locator('#board').evaluate('e=>e.getBoundingClientRect().left+scrollX')
        p.locator('#toggle-leaderboard').click()
        assert p.locator('#leaderboard').is_hidden()
        assert p.locator('#info').is_visible()
        assert abs(p.locator('#board').evaluate('e=>e.getBoundingClientRect().left+scrollX')-before)<1
        p.locator('#toggle-leaderboard').click()
        assert p.locator('#leaderboard').is_visible()
