"""A small clock stub verifies input ordering; ordinary play uses native time."""
def test_drop_contact_excludes_time_before_keyboard_action(app_page):
    p=app_page
    p.add_init_script("""window.testClock={now:0,frames:[]};Object.defineProperty(performance,'now',{value:()=>testClock.now});window.requestAnimationFrame=cb=>testClock.frames.push(cb);window.stepFrame=now=>{testClock.now=now;const batch=testClock.frames.splice(0);for(const cb of batch)cb(now);};""")
    p.reload()
    p.locator('#start').click(force=True)
    p.evaluate('testClock.now=900')
    p.keyboard.press('Enter')
    p.evaluate('stepFrame(1000)')
    assert p.locator('#next-kind').inner_text()=='Z'
    p.evaluate('stepFrame(1899)')
    assert p.locator('#next-kind').inner_text()=='Z'
    p.evaluate('stepFrame(1900)')
    assert p.locator('#next-kind').inner_text()=='T'
