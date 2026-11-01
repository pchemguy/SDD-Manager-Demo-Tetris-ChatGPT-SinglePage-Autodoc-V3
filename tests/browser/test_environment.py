"""Representative isolated browser lifecycle, input and Canvas readiness."""
import functools
import http.server
import threading
import pytest
from playwright.sync_api import sync_playwright
from browser_env import launch_browser

@pytest.mark.parametrize('browser_name', ['chromium', 'firefox'])
def test_two_fresh_context_input_render_teardown_cycles(browser_name, tmp_path):
    probe = tmp_path / "probe.html"
    probe.write_text('<input aria-label="Probe"><canvas width="12" height="12"></canvas>')
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(tmp_path)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    with sync_playwright() as p:
        browser = launch_browser(p, browser_name)
        try:
            for url in [probe.as_uri(), "http://127.0.0.1:" + str(server.server_port) + "/probe.html"]:
                context = browser.new_context()
                try:
                    page = context.new_page()
                    page.goto(url)
                    page.get_by_label('Probe').fill('working')
                    assert page.get_by_label('Probe').input_value() == 'working'
                    assert page.evaluate('''() => {const c=document.querySelector('canvas').getContext('2d'); c.fillStyle='rgb(200,0,0)'; c.fillRect(0,0,12,12); return c.getImageData(1,1,1,1).data[0];}''') == 200
                finally:
                    context.close()
        finally:
            browser.close()
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
