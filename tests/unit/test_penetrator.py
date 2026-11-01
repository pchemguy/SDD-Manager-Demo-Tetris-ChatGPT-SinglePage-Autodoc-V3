from domain import evaluate


def test_lowest_cavity_and_traversal_without_erasing_cells():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');const board=emptyBoard();for(const y of [5,14,19]){board[y][4]='J';board[y][5]='J';}e.fixture({board,active:{kind:'O',orientation:0,x:3,y:0,penetrator:true}});for(let i=0;i<5;i++)e.act('softDrop');const traversing=e.view();const ghost=e.view().ghostCells;e.act('hardDrop');const dropped=e.view();e.advance(1000);console.log(JSON.stringify([traversing.active.y,traversing.board.flat().filter(Boolean).length,ghost,dropped.activeCells,e.view().board.flat().filter(Boolean).length,e.view().active.penetrator]));""",fixture=True) == [5,6,[[4,17],[5,17],[4,18],[5,18]],[[4,17],[5,17],[4,18],[5,18]],10,False]


def test_move_without_a_future_nonoverlapping_landing_is_rejected():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');const board=emptyBoard();for(const y of [17,18,19])board[y][6]='L';e.fixture({board,active:{kind:'O',orientation:0,x:3,y:17,penetrator:true}});const moved=e.act('right');for(let i=0;i<20;i++)e.act('left');console.log(JSON.stringify([moved,e.view().active.x,e.view().activeCells.every(([x,y])=>x>=0&&x<10&&y>=0&&y<20)]));""",fixture=True) == [False,-1,True]


def test_down_stops_at_lowest_legal_cavity_before_colliding_floor():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');const board=emptyBoard();board[19][4]='J';e.fixture({board,active:{kind:'O',orientation:0,x:3,y:0,penetrator:true}});for(let i=0;i<25;i++)e.act('softDrop');console.log(JSON.stringify([e.view().active.y,e.view().groundedElapsedMs,e.view().board[19][4]]));""",fixture=True) == [17,0,'J']


def test_activation_spends_once_suppresses_hold_and_releases_support():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');const board=emptyBoard();board[8][4]='J';e.fixture({board,bonuses:1,active:{kind:'O',orientation:0,x:3,y:6},groundedElapsedMs:null});e.advance(700);const activate=e.act('penetrator');const v=e.view();const repeat=e.act('penetrator'),hold=e.act('hold');e.act('hardDrop');e.advance(1000);console.log(JSON.stringify([activate,v.bonuses,v.active.penetrator,v.groundedElapsedMs,repeat,hold,e.view().active.penetrator,e.view().board[8][4]]));""",fixture=True) == [True,0,True,None,False,False,False,'J']


def test_activation_without_lift_preserves_delay_and_pause_rejects():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');e.act('hardDrop');e.fixture({bonuses:2});e.advance(700);e.act('penetrator');const timer=e.view().groundedElapsedMs;e.advance(300);e.setPaused(true);const paused=e.act('penetrator');e.setPaused(false);e.fixture({bonuses:0});console.log(JSON.stringify([timer,e.view().board.flat().filter(Boolean).length,paused,e.act('penetrator')]));""",fixture=True) == [700,4,False,False]


def test_penetrator_rotation_can_overlap_without_invalid_settlement():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');const board=emptyBoard();board[7][5]='L';e.fixture({board,active:{kind:'I',orientation:0,x:3,y:5,penetrator:true}});const rotated=e.act('rotateCW');const v=e.view();e.act('hardDrop');e.advance(1000);console.log(JSON.stringify([rotated,v.active.x,v.active.y,v.active.orientation,e.view().board[7][5],e.view().board.flat().filter(Boolean).length]));""",fixture=True) == [True,3,5,1,'L',5]


def test_four_line_award_caps_spends_and_restart_resets():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');const balances=[];for(let i=0;i<4;i++){const board=emptyBoard();for(let y=16;y<20;y++)board[y].fill('L',0,9);e.fixture({board,active:{kind:'I',orientation:1,x:7,y:16},groundedElapsedMs:null});e.advance(1000);balances.push(e.view().bonuses);}e.act('penetrator');balances.push(e.view().bonuses);e.start('new');balances.push(e.view().bonuses);console.log(JSON.stringify(balances));""",fixture=True) == [1,2,3,3,2,0]
