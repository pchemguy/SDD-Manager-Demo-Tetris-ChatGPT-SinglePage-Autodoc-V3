"""Read the application-owned pin and verify the optional development cache."""
import base64
import hashlib
import os
import pathlib
import urllib.request
from domain import ROOT, evaluate


def dependency():
    return evaluate('console.log(JSON.stringify(SQLITE_DEPENDENCY));')


def asset():
    pin=dependency()
    path=ROOT/'.test-cache'/('sql-asm-memory-growth-'+pin['version']+'.js')
    if not path.exists():
        request=urllib.request.Request(pin['url'],headers={'Accept-Encoding':'identity'})
        with urllib.request.urlopen(request,timeout=30) as response:
            data=response.read(10000000)
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(data)
    data=path.read_bytes()
    actual='sha384-'+base64.b64encode(hashlib.sha384(data).digest()).decode()
    if actual!=pin['integrity']:
        raise AssertionError('Pinned SQLite script cache integrity mismatch')
    return path


def source():
    path=ROOT/os.environ.get('TETRIS_TEST_ARTIFACT','tetris.html')
    return path.read_text().split('// PURE-BEGIN',1)[1].split('// PURE-END',1)[0]
