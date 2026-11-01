from domain import evaluate

HOST="""function host(){const scripts=[],timers=new Map();let next=0,removed=0,cleared=0,inits=0;const h={createScript:()=>({remove(){removed++;}}),appendScript:s=>scripts.push(s),getInitializer:()=>()=>{inits++;return Promise.resolve({Database:function(){}});},setTimeout:fn=>{timers.set(++next,fn);return next;},clearTimeout:id=>{cleared++;timers.delete(id);}};return {h,scripts,timers,counts:()=>[removed,cleared,inits]};}"""


def test_loader_coalesces_initialization_pins_script_and_cleans_up():
    assert evaluate(HOST+"""(async()=>{const h=host(),l=createDependencyLoader(h.h,50);const a=l.ensureSQLite(),b=l.ensureSQLite();const script=h.scripts[0];script.onload();const out=await Promise.all([a,b]);await l.ensureSQLite();console.log(JSON.stringify([out.every(x=>x.ok),h.scripts.length,h.counts(),script.src===SQLITE_DEPENDENCY.url,script.integrity===SQLITE_DEPENDENCY.integrity,script.crossOrigin,script.onload,script.onerror]));})();""") == [True,1,[1,1,1],True,True,'anonymous',None,None]


def test_timeout_is_bounded_late_callback_inert_and_retry_possible():
    assert evaluate(HOST+"""(async()=>{const h=host(),l=createDependencyLoader(h.h,50);const a=l.ensureSQLite(),late=h.scripts[0].onload;h.timers.values().next().value();const first=await a;late();const b=l.ensureSQLite();h.scripts[1].onload();const second=await b;console.log(JSON.stringify([first.code,second.ok,h.scripts.length,h.counts()]));})();""") == ['dependencyUnavailable',True,2,[2,2,1]]


def test_script_failure_does_not_affect_json_validation():
    assert evaluate(HOST+"""(async()=>{const h=host(),l=createDependencyLoader(h.h,50);const a=l.ensureSQLite();h.scripts[0].onerror();console.log(JSON.stringify([(await a).code,JSONCodec.decode('{"x":1}').ok,h.counts()]));})();""") == ['dependencyUnavailable',True,[1,1,0]]
