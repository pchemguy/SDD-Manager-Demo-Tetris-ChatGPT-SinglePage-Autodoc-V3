"""Initialize the actual CDN distribution in both browser execution modes."""
import os
from sql_assets import source,dependency,asset


def test_pinned_single_script_sqlite_initializes_without_companion_or_worker(app_page):
    p=app_page
    if os.environ.get("TETRIS_SQLITE_VERIFIED_FETCH") == "1":
        # Managed-host browsers lack the proxy CA. Python verifies TLS, then the
        # browser independently checks the pinned SRI before executing bytes.
        data=asset().read_bytes()
        p.route(dependency()["url"],lambda route:route.fulfill(body=data,content_type="application/javascript",headers={"Access-Control-Allow-Origin":"*"}))
    requests=[];failures=[]
    p.on('request',lambda request:requests.append(request.url))
    p.on('requestfailed',lambda request:failures.append({'url':request.url,'failure':request.failure}))
    result=p.evaluate('(async()=>{'+source()+"""
        const loader=createDependencyLoader({createScript:()=>document.createElement('script'),appendScript:s=>document.head.append(s),getInitializer:()=>window.initSqlJs,setTimeout:(cb,ms)=>setTimeout(cb,ms),clearTimeout:id=>clearTimeout(id)},20000);
        const out=await loader.ensureSQLite();if(!out.ok)return out;
        const db=new out.value.Database();try {return {ok:true,sqlite:db.exec('SELECT sqlite_version()')[0].values[0][0],sum:db.exec('SELECT 2+3')[0].values[0][0]};}finally{db.close();}
    })()""")
    assert result.get('ok'), {'result':result,'failures':failures}
    assert result['sqlite']=='3.49.1' and result['sum']==5
    assert requests==[dependency()['url']], requests
    assert p.locator('script[src*="sql-asm-memory-growth"]').count()==0
