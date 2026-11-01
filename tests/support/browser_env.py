"""Dedicated Playwright launch policy; restricted-host Firefox override is opt-in."""
import os

def launch_browser(playwright, name):
    """Launch only required managed browsers, with a bounded startup."""
    options = {'headless': True, 'timeout': 15000}
    if name == 'firefox' and os.environ.get('TETRIS_FIREFOX_SANDBOX_OVERRIDE') == '1':
        options['env'] = dict(os.environ, MOZ_DISABLE_CONTENT_SANDBOX='1')
    return getattr(playwright, name).launch(**options)
