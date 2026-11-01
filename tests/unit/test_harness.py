"""The extraction harness must run supplied sections and isolate process state."""
from domain import evaluate

def test_extracts_only_the_named_pure_section(tmp_path):
    p = tmp_path / 'probe.html'
    p.write_text('<script>throw Error("outside");\n// PURE-BEGIN\nfunction square(x){return x*x;}\n// PURE-END\nthrow Error("outside");</script>')
    assert evaluate('console.log(JSON.stringify(square(7)))', p) == 49
