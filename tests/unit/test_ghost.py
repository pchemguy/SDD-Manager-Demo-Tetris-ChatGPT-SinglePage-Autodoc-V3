from domain import evaluate


def test_ghost_stops_before_first_obstacle_and_is_pure():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');const b=emptyBoard();b[12][4]='O';e.fixture({board:b});const a=e.view({ghost:'visible'});const v=e.view();console.log(JSON.stringify([a.ghostCells,a.active.y,v.active.y,v.score]));""", fixture=True) == [[[3,11],[4,11],[5,11],[6,11]],-1,-1,0]


def test_midline_straddle_hides_whole_ghost():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');const b=emptyBoard();b[11][4]='I';e.fixture({board:b,active:{kind:'O',orientation:0,x:3,y:0}});const upper=e.view().ghostCells;const shown=e.view({...DEFAULT_SETTINGS,ghost:'visible'}).ghostCells;b[11][4]=null;b[12][4]='I';e.fixture({board:b});console.log(JSON.stringify([upper,shown,e.view().ghostCells,e.view({...DEFAULT_SETTINGS,ghost:'hidden'}).ghostCells]));""",fixture=True) == [[],[[4,9],[5,9],[4,10],[5,10]],[[4,10],[5,10],[4,11],[5,11]],[]]


def test_no_active_piece_has_no_ghost():
    assert evaluate("console.log(JSON.stringify(createEngine().view().ghostCells));") == []
