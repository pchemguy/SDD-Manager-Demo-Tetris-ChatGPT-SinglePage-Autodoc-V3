"""Unchanged status must not continuously mutate an aria-live region."""
def test_ready_frames_do_not_reannounce_unchanged_status(app_page):
    p = app_page
    p.clock.install(time='2026-01-01T00:00:00Z')
    p.reload()
    p.clock.pause_at('2026-01-01T00:00:02Z')
    p.evaluate("""()=>{window.statusMutations=0;new MutationObserver(records=>{window.statusMutations+=records.length}).observe(document.querySelector('#phase'),{childList:true,subtree:true,characterData:true});}""")
    p.clock.run_for(200)
    assert p.evaluate('window.statusMutations') == 0
