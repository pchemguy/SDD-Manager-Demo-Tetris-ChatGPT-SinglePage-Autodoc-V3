from domain import evaluate


def test_hold_once_then_orientation_zero_swap_after_lock():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');const next=e.view().queue[0];const first=e.act('hold');const repeat=e.act('hold');const a=e.view();for(let i=0;i<23;i++)e.act('softDrop');e.advance(1000);e.act('softDrop');e.act('rotateCW');e.act('hold');const b=e.view();console.log(JSON.stringify([first,repeat,a.held,a.active.kind===next,b.active.kind,b.active.orientation,b.holdUsed]));""") == [True,False,'I',True,'I',0,True]


def test_disabled_hold_and_obstructed_swap():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');const off=e.act('hold',{...DEFAULT_SETTINGS,hold:'off'});const board=emptyBoard();board[0].fill('O');e.fixture({board,held:'O'});const swap=e.act('hold');console.log(JSON.stringify([off,swap,e.view().phase,e.drainEvents().length]));""",fixture=True) == [False,True,'over',1]
