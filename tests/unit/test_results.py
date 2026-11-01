from domain import evaluate

RESULT="{id:'00000000-0000-4000-8000-000000000001',score:0,timestamp:'2026-11-01T12:34:56.789Z'}"


def test_result_stable_fields_zero_score_and_completion_deduplication():
    assert evaluate("const s=createSessionStore(),r="+RESULT+";s.record(r);s.record({...r,score:100});r.score=200;const copy=s.topResults();copy[0].score=300;console.log(JSON.stringify(s.topResults()));") == [{'id':'00000000-0000-4000-8000-000000000001','score':0,'timestamp':'2026-11-01T12:34:56.789Z'}]


def test_result_validation_rejects_unsafe_scores_ids_and_calendar_dates():
    assert evaluate("const r="+RESULT+";const cases=[{...r,score:-1},{...r,score:1.5},{...r,score:'1'},{...r,score:Number.MAX_SAFE_INTEGER+1},{...r,id:r.id.toUpperCase().replace('4000','1000')},{...r,timestamp:'2026-02-30T12:34:56.789Z'},{...r,timestamp:'2026-11-01T12:34:56Z'},{...r,extra:true}];const s=createSessionStore();console.log(JSON.stringify([cases.every(x=>!validateResult(x).ok),cases.every(x=>!s.record(x).ok),s.topResults()]));") == [True,True,[]]


def test_engine_completion_can_be_recorded_once_with_injected_utc_time():
    assert evaluate("const e=createEngine(()=>0),s=createSessionStore();e.start('00000000-0000-4000-8000-000000000001');const board=emptyBoard();board[0][3]='J';e.fixture({board,active:{kind:'I',orientation:0,x:3,y:18},groundedElapsedMs:null});e.advance(1000);for(const v of e.drainEvents())s.record({id:v.gameId,score:v.score,timestamp:'2026-11-01T00:00:00.000Z'});e.advance(2000);e.start('00000000-0000-4000-8000-000000000002');console.log(JSON.stringify([s.topResults(),e.drainEvents()]));",fixture=True) == [[{'id':'00000000-0000-4000-8000-000000000001','score':0,'timestamp':'2026-11-01T00:00:00.000Z'}],[]]


def test_top_ten_after_eleven_games_and_dropped_id_cannot_reinsert():
    assert evaluate("""const s=createSessionStore();const id=i=>'00000000-0000-4000-8000-'+i.toString(16).padStart(12,'0');for(let i=0;i<11;i++)s.record({id:id(i),score:i,timestamp:'2026-11-01T00:00:00.000Z'});const again=s.record({id:id(0),score:999,timestamp:'2026-11-01T00:00:00.000Z'});console.log(JSON.stringify([s.topResults().map(r=>r.score),again.value]));""") == [[10,9,8,7,6,5,4,3,2,1],False]


def test_equal_scores_sort_utc_time_then_lexicographic_id():
    assert evaluate("""const s=createSessionStore();for(const [n,day]of [[3,'01'],[1,'02'],[2,'01']])s.record({id:'00000000-0000-4000-8000-'+String(n).padStart(12,'0'),score:100,timestamp:'2026-11-'+day+'T00:00:00.000Z'});console.log(JSON.stringify(s.topResults().map(r=>r.id.slice(-1))));""") == ['2','3','1']
