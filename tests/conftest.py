"""Shared test environment for the exact single-file application."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests' / 'support'))

import functools
import http.server
import threading
import pytest
from playwright.sync_api import sync_playwright
from browser_env import launch_browser

@pytest.fixture(scope='session')
def server_url():
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield 'http://127.0.0.1:' + str(server.server_port)
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)

@pytest.fixture(params=['chromium', 'firefox'])
def browser_name(request):
    return request.param

@pytest.fixture(params=['file', 'http'])
def mode(request):
    return request.param

@pytest.fixture
def app_page(browser_name, mode, server_url):
    with sync_playwright() as p:
        browser = launch_browser(p, browser_name)
        context = browser.new_context(viewport={'width':1280,'height':800})
        page = context.new_page()
        page.set_default_timeout(5000)
        page.goto((ROOT / 'tetris.html').as_uri() if mode == 'file' else server_url + '/tetris.html')
        try:
            yield page
        finally:
            context.close()
            browser.close()
