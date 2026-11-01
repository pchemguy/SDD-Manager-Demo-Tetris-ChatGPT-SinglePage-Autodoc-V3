"""Portable saved-session fixtures independent of runtime implementation."""
import copy

SETTINGS={'ghost':'visible','hardDrop':'off','next':'off','hardDropLock':'immediate','lock':'failed','hold':'off'}
RESULTS=[{'id':'00000000-0000-4000-8000-000000000001','score':0,'timestamp':'2026-11-01T12:34:56.789Z'}, {'id':'00000000-0000-4000-8000-000000000002','score':9007199254740991,'timestamp':'2000-02-29T00:00:00.000Z'}]

def saved_session():
    return copy.deepcopy({'formatVersion':1,'results':RESULTS,'settings':SETTINGS})

def ranked_session():
    value=saved_session();value['results'].reverse();return value
