"""Real packaging commands must preserve app bytes and reject unsafe inventories."""
import hashlib
import pathlib
import subprocess
import sys
from domain import ROOT

def source(tmp_path):
    src = tmp_path / 'source'
    src.mkdir()
    (src/'VERSION').write_text('0.1.0\n')
    (src/'tetris.html').write_text('<meta name="app-version" content="0.1.0"><p>one application file</p>')
    (src/'README.md').write_text('Open tetris.html.\n')
    return src

def command(script, *args):
    return subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],capture_output=True,text=True,timeout=15)

def test_packaging_preserves_html_and_checksums(tmp_path):
    src = source(tmp_path)
    out = tmp_path/'dist'
    result = command('package.py','--source',src,'--out',out)
    assert result.returncode == 0, result.stderr
    assert {p.name for p in out.iterdir()} == {'tetris.html','README.md','SHA256SUMS'}
    assert (out/'tetris.html').read_bytes() == (src/'tetris.html').read_bytes()
    checks = dict(line.split('  ')[::-1] for line in (out/'SHA256SUMS').read_text().splitlines())
    assert checks['tetris.html'] == hashlib.sha256((out/'tetris.html').read_bytes()).hexdigest()
    assert command('check_artifact_names.py',out,'--version','0.1.0').returncode == 0

def test_name_gate_rejects_versioned_actual_filename(tmp_path):
    out = tmp_path/'dist';out.mkdir()
    (out/'tetris-v0.1.0.html').write_text('bad naming')
    assert command('check_artifact_names.py',out,'--version','0.1.0').returncode != 0

def test_gate_rejects_tampered_bytes(tmp_path):
    src = source(tmp_path);out = tmp_path/'dist'
    assert command('package.py','--source',src,'--out',out).returncode == 0
    assert out.exists()
    (out/'tetris.html').write_text('tampered')
    assert command('check_artifact_names.py',out,'--version','0.1.0').returncode != 0

def test_version_mismatch_is_rejected_before_output(tmp_path):
    src = source(tmp_path);out = tmp_path/'dist'
    (src/'VERSION').write_text('0.2.0\n')
    assert command('package.py','--source',src,'--out',out).returncode != 0
    assert not out.exists()
