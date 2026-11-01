from domain import evaluate


def test_lowest_cavity_and_traversal_without_erasing_cells():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');const board=emptyBoard();for(const y of [5,14,19]){board[y][4]='J';board[y][5]='J';}e.fixture({board,active:{kind:'O',orientation:0,x:3,y:0,penetrator:true}});for(let i=0;i<5;i++)e.act('softDrop');const traversing=e.view();const ghost=e.view().ghostCells;e.act('hardDrop');const dropped=e.view();e.advance(1000);console.log(JSON.stringify([traversing.active.y,traversing.board.flat().filter(Boolean).length,ghost,dropped.activeCells,e.view().board.flat().filter(Boolean).length,e.view().active.penetrator]));""",fixture=True) == [5,6,[[4,17],[5,17],[4,18],[5,18]],[[4,17],[5,17],[4,18],[5,18]],10,False]


def test_move_without_a_future_nonoverlapping_landing_is_rejected():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');const board=emptyBoard();for(const y of [17,18,19])board[y][6]='L';e.fixture({board,active:{kind:'O',orientation:0,x:3,y:17,penetrator:true}});const moved=e.act('right');for(let i=0;i<20;i++)e.act('left');console.log(JSON.stringify([moved,e.view().active.x,e.view().activeCells.every(([x,y])=>x>=0&&x<10&&y>=0&&y<20)]));""",fixture=True) == [False,-1,True]


def test_down_stops_at_lowest_legal_cavity_before_colliding_floor():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');const board=emptyBoard();board[19][4]='J';e.fixture({board,active:{kind:'O',orientation:0,x:3,y:0,penetrator:true}});for(let i=0;i<25;i++)e.act('softDrop');console.log(JSON.stringify([e.view().active.y,e.view().groundedElapsedMs,e.view().board[19][4]]));""",fixture=True) == [17,0,'J']
