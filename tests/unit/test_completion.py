"""Clearing, scoring, level progression and exactly-once completion contracts."""
from domain import evaluate

def test_single_clear_compacts_and_scores():
    assert evaluate("const e=createEngine(()=>0);e.start('g');const board=emptyBoard();board[19].fill('J',0,6);e.fixture({board,active:{kind:'I',orientation:0,x:6,y:18,penetrator:false},groundedElapsedMs:null});e.advance(1000);const v=e.view();console.log(JSON.stringify([v.lines,v.score,v.level,v.board.flat().filter(Boolean).length]));", fixture=True) == [1,100,1,0]

def test_four_line_clear_preserves_cells_above_and_uses_preclear_level():
    assert evaluate("const e=createEngine(()=>0);e.start('g');const board=emptyBoard();for(let y=16;y<20;y++)board[y].fill('L',0,9);board[15][0]='T';e.fixture({board,active:{kind:'I',orientation:1,x:7,y:16,penetrator:false},groundedElapsedMs:null});e.advance(1000);const v=e.view();console.log(JSON.stringify([v.lines,v.score,v.board[19][0],v.bonuses]));", fixture=True) == [4,800,'T',1]

def test_level_changes_after_tenth_line():
    assert evaluate("const e=createEngine(()=>0);e.start('g');const board=emptyBoard();board[19].fill('J',0,6);e.fixture({board,lines:9,active:{kind:'I',orientation:0,x:6,y:18,penetrator:false},groundedElapsedMs:null});e.advance(1000);const v=e.view();console.log(JSON.stringify([v.lines,v.score,v.level,gravityInterval(v.level)]));", fixture=True) == [10,100,2,925]

def test_soft_drop_scores_only_successful_rows():
    assert evaluate("const e=createEngine(()=>0);e.start('g');for(let i=0;i<25;i++)e.act('softDrop');console.log(JSON.stringify(e.view().score));") == 19

def test_blocked_spawn_completes_once_and_restart_resets():
    assert evaluate("const e=createEngine(()=>0);e.start('g');const board=emptyBoard();board[0][3]='J';e.fixture({board,active:{kind:'I',orientation:0,x:3,y:18,penetrator:false},groundedElapsedMs:null});e.advance(1000);const a=e.drainEvents();e.advance(2000);const b=e.drainEvents();e.start('fresh');console.log(JSON.stringify([e.view().phase,e.view().score,a,b]));", fixture=True) == ['running',0,[{'type':'gameCompleted','gameId':'g','score':0}],[]]

import pytest

@pytest.mark.parametrize('count,score,remaining', [(2,300,2), (3,500,1)])
def test_two_and_three_line_scores(count, score, remaining):
    result = evaluate(f"const e=createEngine(()=>0);e.start('g');const board=emptyBoard();for(let y=20-{count};y<20;y++)board[y].fill('L',0,9);e.fixture({{board,active:{{kind:'I',orientation:1,x:7,y:16,penetrator:false}},groundedElapsedMs:null}});e.advance(1000);const v=e.view();console.log(JSON.stringify([v.lines,v.score,v.board.flat().filter(Boolean).length]));", fixture=True)
    assert result == [count,score,remaining]

def test_score_saturates_at_safe_integer_limit():
    assert evaluate("const e=createEngine(()=>0);e.start('g');e.fixture({score:Number.MAX_SAFE_INTEGER-1});e.act('softDrop');e.act('softDrop');console.log(JSON.stringify(e.view().score));", fixture=True) == 9007199254740991
