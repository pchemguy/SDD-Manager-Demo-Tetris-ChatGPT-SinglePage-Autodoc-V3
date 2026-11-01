"""Evaluate pure embedded application sections with an isolated Node process."""
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]

def evaluate(body, html=None):
    """Run a scenario against the actual embedded pure sections, not a copy."""
    source = (pathlib.Path(html) if html else ROOT / 'tetris.html').read_text()
    code = source.split('// PURE-BEGIN', 1)[1].split('// PURE-END', 1)[0]
    result = subprocess.run(['node', '-e', code + '\n' + body], text=True,
                            capture_output=True, timeout=15, check=True)
    return json.loads(result.stdout)
