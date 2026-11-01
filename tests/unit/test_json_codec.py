"""Compare embedded validation with the published schema and independent calendar checks."""
import datetime
import json
import pathlib
import pytest
from jsonschema import Draft202012Validator, FormatChecker
from domain import evaluate

SETTINGS={'ghost':'dynamic','hardDrop':'on','next':'on','hardDropLock':'general','lock':'interval','hold':'on'}
RESULT={'id':'00000000-0000-4000-8000-000000000001','score':0,'timestamp':'2026-11-01T12:34:56.789Z'}

def snapshot():
    return {'formatVersion':1,'results':[RESULT.copy()],'settings':SETTINGS.copy()}


def test_schema_and_embedded_validation_agree_on_complete_candidates():
    schema=json.loads((pathlib.Path(__file__).resolve().parents[2]/'docs/dev/contracts/session.schema.json').read_text())
    Draft202012Validator.check_schema(schema)
    checker=FormatChecker()
    @checker.checks('date-time')
    def calendar(value):
        if not isinstance(value,str): return True
        try: datetime.datetime.fromisoformat(value);return True
        except ValueError: return False
    validator=Draft202012Validator(schema,format_checker=checker)
    cases=[snapshot(),{'formatVersion':1,'results':[],'settings':SETTINGS.copy()},None,[],{}, {**snapshot(),'extra':1}]
    for field,value in [('id','BAD'),('score',-1),('score',0.5),('score','0'),('score',9007199254740992),('timestamp','2026-02-30T12:34:56.789Z'),('timestamp','0000-01-01T00:00:00.000Z'),('timestamp','2026-11-01T12:34:56Z'),('extra',True)]:
        raw=snapshot();raw['results'][0][field]=value;cases.append(raw)
    raw=snapshot();del raw['settings']['hold'];cases.append(raw)
    raw=snapshot();raw['settings']['next']=True;cases.append(raw)
    raw=snapshot();raw['results'][0]['score']=9007199254740991;cases.append(raw)
    expected=[validator.is_valid(c) for c in cases]
    assert evaluate('console.log(JSON.stringify('+json.dumps(cases)+'.map(x=>validateSession(x).ok)));')==expected


def test_duplicate_ids_unsupported_versions_and_round_trip_preserve_fields():
    raw=snapshot();raw['results'].append({**RESULT,'id':'00000000-0000-4000-8000-000000000002','score':9007199254740991,'timestamp':'2000-02-29T00:00:00.000Z'})
    expected={**raw,'results':list(reversed(raw['results']))}
    assert evaluate('const raw='+json.dumps(raw)+";const encoded=JSONCodec.encode(raw);const decoded=JSONCodec.decode(encoded);const good=validateSession(decoded.value);const dup=validateSession({...raw,results:[raw.results[0],raw.results[0]]});const version=validateSession({...raw,formatVersion:2});console.log(JSON.stringify([good.value,dup.code,version.code]));") == [expected,'invalidValue','unsupportedVersion']


@pytest.mark.parametrize('text', ['{"a":1,"a":2}','{"a":1,"\\u0061":2}','{"x":{"hold":"on","hold":"off"}}','{} null','[1,]','{"x":"bad\x01"}',''])
def test_duplicate_aware_parser_rejects_invalid_complete_text(text):
    assert evaluate('console.log(JSON.stringify(JSONCodec.decode('+json.dumps(text)+').code));')=='invalidJSON'


def test_exact_numeric_validation_does_not_round_fractional_or_unsafe_input():
    assert evaluate("""const valid=['1','1.0','1e0','1000e-3','0e9999999'].map(t=>JSONCodec.decode('{"score":'+t+'}'));const bad=['1.0000000000000001','9007199254740991.1','1e-1000','9007199254740992'].map(t=>JSONCodec.decode('{"score":'+t+'}').code);console.log(JSON.stringify([valid.map(x=>x.value.score),bad]));""") == [[1,1,1,1,0],['invalidValue']*4]


def test_encoding_and_bounded_parser_failures_are_clear():
    assert evaluate("""const encoding=JSONCodec.decodeBytes(new Uint8Array([0xc0,0xaf]));const deep=JSONCodec.decode('['.repeat(65)+'0'+']'.repeat(65));const string=JSONCodec.decode(JSON.stringify({x:'brace } and "quote"'}));console.log(JSON.stringify([encoding.code,deep.code,string.ok]));""") == ['invalidEncoding','invalidJSON',True]
