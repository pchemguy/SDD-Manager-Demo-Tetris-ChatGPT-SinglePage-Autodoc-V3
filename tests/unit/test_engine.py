"""Classic placement and timing contracts, with literal independently derived results."""
from domain import evaluate

def test_left_motion_changes_anchor():
    assert evaluate("const e=createEngine(()=>0);e.start('g');e.act('left',DEFAULT_SETTINGS);console.log(JSON.stringify(e.view().active.x));") == 2

def test_occupied_cells_respect_left_boundary():
    assert evaluate("const e=createEngine(()=>0);e.start('g');for(let i=0;i<30;i++)e.act('left',DEFAULT_SETTINGS);console.log(JSON.stringify(e.view().active.x));") == 0

def test_gravity_waits_one_complete_interval():
    assert evaluate("const e=createEngine(()=>0);e.start('g');e.advance(999,DEFAULT_SETTINGS);const a=e.view().active.y;e.advance(1,DEFAULT_SETTINGS);console.log(JSON.stringify([a,e.view().active.y]));") == [-1, 0]

def test_contact_gets_full_delay_and_grounded_move_does_not_reset():
    assert evaluate("const e=createEngine(()=>0);e.start('g');for(let i=0;i<19;i++)e.act('softDrop',DEFAULT_SETTINGS);e.advance(999,DEFAULT_SETTINGS);const a=e.view().board.flat().filter(Boolean).length;e.act('left',DEFAULT_SETTINGS);e.advance(1,DEFAULT_SETTINGS);console.log(JSON.stringify([a,e.view().board.flat().filter(Boolean).length]));") == [0, 4]

def test_pause_freezes_game_time():
    assert evaluate("const e=createEngine(()=>0);e.start('g');e.setPaused(true);e.advance(8000,DEFAULT_SETTINGS);const a=e.view().active.y;e.setPaused(false);e.advance(1000,DEFAULT_SETTINGS);console.log(JSON.stringify([a,e.view().active.y]));") == [-1, 0]


def test_rotation_uses_occupied_cells_and_rejects_outside_board():
    assert evaluate("const e=createEngine(()=>0);e.start('g');e.act('rotateCW');const a=e.view().active.orientation;e.act('softDrop');e.act('rotateCW');console.log(JSON.stringify([a,e.view().active.orientation,e.view().activeCells]));") == [0, 1, [[5,0],[5,1],[5,2],[5,3]]]

def test_lift_off_discards_grounded_elapsed_time():
    assert evaluate("const e=createEngine(()=>0);e.start('g');const board=emptyBoard();board[10][6]='O';e.fixture({board,active:{kind:'I',orientation:0,x:3,y:8,penetrator:false},groundedElapsedMs:null});e.advance(500);e.act('left');console.log(JSON.stringify([e.view().groundedElapsedMs,e.view().board.flat().filter(Boolean).length]));", fixture=True) == [None, 1]

def test_partial_gravity_tick_does_not_shorten_contact_delay():
    assert evaluate("const e=createEngine(()=>0);e.start('g');e.advance(900);for(let i=0;i<19;i++)e.act('softDrop');e.advance(999);const a=e.view().board.flat().filter(Boolean).length;e.advance(1);console.log(JSON.stringify([a,e.view().board.flat().filter(Boolean).length]));") == [0,4]

def test_all_seven_spawn_geometries_are_four_visible_cells():
    assert evaluate("console.log(JSON.stringify(KINDS.map((_,i)=>{const e=createEngine(()=>i/7);e.start('g');const p=e.view().activeCells;return p.length===4&&p.every(([x,y])=>x>=0&&x<10&&y>=0&&y<20);}))); ") == [True]*7

def test_pause_ignores_movement_as_well_as_elapsed_time():
    assert evaluate("const e=createEngine(()=>0);e.start('g');e.setPaused(true);e.act('left');e.advance(-100);console.log(JSON.stringify([e.view().phase,e.view().active.x,e.view().active.y]));") == ['paused',3,-1]
