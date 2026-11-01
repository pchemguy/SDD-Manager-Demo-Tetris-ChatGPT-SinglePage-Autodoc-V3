from domain import evaluate


def test_failed_policy_soft_attempt_and_partial_gravity_phase():
    assert evaluate("""const f={...DEFAULT_SETTINGS,lock:'failed'};const e=createEngine(()=>0);e.start('g');e.advance(900,f);e.act('hardDrop',f);const a=e.view().board.flat().filter(Boolean).length;e.advance(99,f);const b=e.view().board.flat().filter(Boolean).length;e.advance(1,f);const c=e.view().board.flat().filter(Boolean).length;e.start('new');e.act('hardDrop',f);e.act('softDrop',f);console.log(JSON.stringify([a,b,c,e.view().board.flat().filter(Boolean).length]));""") == [0,0,4,4]


def test_immediate_policy_including_zero_distance_drop():
    assert evaluate("""const e=createEngine(()=>0);e.start('g');e.act('hardDrop');e.advance(100);e.act('hardDrop',{...DEFAULT_SETTINGS,hardDropLock:'immediate'});console.log(JSON.stringify([e.view().board.flat().filter(Boolean).length,e.view().score]));""") == [4,38]


def test_switching_policies_cannot_reset_tracked_contact():
    assert evaluate("""const e=createEngine(()=>0),f={...DEFAULT_SETTINGS,lock:'failed'};e.start('g');e.act('hardDrop',f);e.advance(400,f);e.advance(200);e.advance(200,f);const tracked=e.view().groundedElapsedMs;e.advance(0);e.advance(199);const before=e.view().board.flat().filter(Boolean).length;e.advance(1);console.log(JSON.stringify([tracked,before,e.view().board.flat().filter(Boolean).length]));""") == [800,0,4]


def test_switch_to_interval_honors_already_elapsed_contact_on_zero_update():
    assert evaluate("const e=createEngine(()=>0);e.start('g');e.act('hardDrop');e.fixture({groundedElapsedMs:1000});e.advance(0);console.log(JSON.stringify(e.view().board.flat().filter(Boolean).length));",fixture=True) == 4
