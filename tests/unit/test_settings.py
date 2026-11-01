from domain import evaluate


def test_exact_setting_keys_and_values_without_coercion():
    assert evaluate("""const valid=Object.entries(SETTING_VALUES).every(([k,vs])=>vs.every(v=>validateSettings({...DEFAULT_SETTINGS,[k]:v}).ok));const missing={...DEFAULT_SETTINGS};delete missing.hold;const bad=[null,[],missing,{...DEFAULT_SETTINGS,extra:'on'},{...DEFAULT_SETTINGS,hardDrop:true},{...DEFAULT_SETTINGS,ghost:'VISIBLE'}];console.log(JSON.stringify([valid,bad.every(v=>!validateSettings(v).ok)]));""") == [True,True]


def test_session_patch_is_atomic_and_returned_settings_are_detached():
    assert evaluate("""const s=createSessionStore();s.changeSettings({ghost:'visible'});const a=s.changeSettings({ghost:'hidden',hold:'bad'});const copy=s.getSettings();copy.hold='off';const b=s.changeSettings(null);console.log(JSON.stringify([a.ok,b.ok,s.getSettings()]));""") == [False,False,{'ghost':'visible','hardDrop':'on','next':'on','hardDropLock':'general','lock':'interval','hold':'on'}]
