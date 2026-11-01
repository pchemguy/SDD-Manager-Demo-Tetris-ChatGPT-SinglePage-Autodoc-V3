from domain import evaluate


def test_hard_drop_matches_ghost_with_full_contact_delay():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');e.advance(900);const ghost=e.view().ghostCells;e.act('hardDrop');const same=JSON.stringify(ghost)===JSON.stringify(e.view().activeCells);const score=e.view().score;e.advance(999);const before=e.view().board.flat().filter(Boolean).length;e.advance(1);console.log(JSON.stringify([same,score,before,e.view().board.flat().filter(Boolean).length]));""") == [True,38,0,4]


def test_repeated_drop_preserves_elapsed_and_scores_nothing():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');e.act('hardDrop');e.advance(700);e.act('hardDrop');console.log(JSON.stringify([e.view().score,e.view().groundedElapsedMs]));""") == [38,700]


def test_disabled_hard_drop_is_noop():
    assert evaluate("const e=createEngine(()=>0);e.start('g');console.log(JSON.stringify([e.act('hardDrop',{...DEFAULT_SETTINGS,hardDrop:'off'}),e.view().active.y,e.view().score]));") == [False,-1,0]


def test_held_z_piece_full_interval_is_independent_of_browser_frames():
    assert evaluate("const e=createEngine(()=>0);e.start('g');e.act('hold');e.act('hold');e.act('hardDrop');e.act('hardDrop');e.advance(999);const a=e.view();e.advance(1);const b=e.view();console.log(JSON.stringify([a.active.kind,a.queue[0],a.score,b.active.kind,b.queue[0]]));") == ['Z','T',36,'T','S']
