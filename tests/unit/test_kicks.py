from domain import evaluate


def test_i_wall_and_t_floor_kicks():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');e.fixture({active:{kind:'I',orientation:1,x:-2,y:10}});e.act('rotateCW');const a=e.view().active;e.fixture({active:{kind:'T',orientation:0,x:3,y:18},groundedElapsedMs:null});e.advance(350);e.act('rotateCW');console.log(JSON.stringify([[a.x,a.y,a.orientation],[e.view().active.x,e.view().active.y,e.view().active.orientation],e.view().groundedElapsedMs]));""", fixture=True) == [[0,10,2],[2,17,1],350]


def test_all_transition_offsets_match_normative_tables():
    import pathlib, re
    text=(pathlib.Path(__file__).resolve().parents[2]/'docs/dev/SPEC.md').read_text()
    rows=re.findall(r'^\| ([0R2L]) to ([0R2L]) \| (.*?) \| (.*?) \|$',text,re.M)
    expected={'normal':{}, 'I':{}}
    for a,b,j,i in rows:
        key=str('0R2L'.index(a))+str('0R2L'.index(b))
        for group,values in [('normal',j),('I',i)]:
            expected[group][key]=[[0,0]]+[[int(x),int(y)] for x,y in re.findall(r'\((-?\d+),(-?\d+)\)',values)]
    assert evaluate('console.log(JSON.stringify(KICKS));') == expected


def test_o_invariant_and_fully_blocked_rotation():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');e.fixture({active:{kind:'O',orientation:0,x:3,y:5}});const before=e.view().activeCells;e.act('rotateCW');const same=JSON.stringify(before)===JSON.stringify(e.view().activeCells);const board=Array.from({length:20},()=>Array(10).fill('J'));const active={kind:'T',orientation:0,x:3,y:5};for(const[x,y]of pieceCells(active))board[y][x]=null;e.fixture({board,active});console.log(JSON.stringify([same,e.act('rotateCW'),e.view().active.orientation]));""",fixture=True) == [True,False,0]
