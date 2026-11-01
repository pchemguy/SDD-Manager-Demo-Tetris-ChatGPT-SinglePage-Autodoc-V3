"""Earn a bonus by actual keyboard play, then spend and lock it."""
from test_modern import start_game


def test_four_line_bonus_white_activation_hold_exclusion_and_lock(app_page):
    p=app_page
    start_game(p)
    assert p.locator('#bonuses').count() == 1
    plan=[(0,0),(0,3),(0,6),(0,5),(0,0),(3,7),(1,-1),(0,2),(2,4)]
    def place(orientation,x):
        next_kind=p.locator('#next-kind').inner_text()
        p.keyboard.press('ArrowDown')
        for _ in range(orientation): p.keyboard.press('x')
        for _ in range(abs(x-3)): p.keyboard.press('ArrowRight' if x>3 else 'ArrowLeft')
        p.keyboard.press('Enter')
        p.wait_for_function("old=>document.getElementById('next-kind').textContent!==old",arg=next_kind)
    for i,(o,x) in enumerate(plan):
        if i==7: p.keyboard.press('c')
        place(o,x)
    p.keyboard.press('c')
    place(1,7)
    assert p.locator('#lines').inner_text() == '4'
    assert p.locator('#bonuses').inner_text() == '⚡'
    held=p.locator('#held-kind').inner_text()
    p.keyboard.press('p')
    assert p.locator('#bonuses').inner_text() == ''
    assert p.locator('#board').evaluate('''c=>{const ctx=c.getContext('2d');return [4,5].every(x=>[0,1].every(y=>[5,25].every(oy=>{const a=ctx.getImageData(x*30+5,y*30+oy,1,1).data;return a[0]===255&&a[1]===255&&a[2]===255;})));}''')
    assert p.locator('#board').evaluate("c=>{const a=c.getContext('2d').getImageData(124,544,1,1).data;return a[0]===255&&a[1]===255&&a[2]===255;}")
    p.keyboard.press('c')
    assert p.locator('#held-kind').inner_text() == held
    next_kind=p.locator('#next-kind').inner_text()
    p.keyboard.press('Enter')
    p.wait_for_function("old=>document.getElementById('next-kind').textContent!==old",arg=next_kind)
    assert p.locator('#board').evaluate("c=>{const a=c.getContext('2d').getImageData(125,575,1,1).data;return !(a[0]===255&&a[1]===255&&a[2]===255);}")
    p.keyboard.press('r')
    assert p.locator('#bonuses').inner_text() == ''
