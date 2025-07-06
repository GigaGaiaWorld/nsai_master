# utils/runtime_fake.py
from problog.extern  import problog_export
from problog.program import PrologString
import threading

SNIPPET_DB = {
    "HASH":
        "addition(X,Y,Z) :- digit(X,X2), digit(Y,Y2), Z is X2+Y2."
}

_LOCK, _LOADED = threading.RLock(), set()

@problog_export('+str')
def langda_pred(hashval, database=None):
    with _LOCK:
        if hashval not in _LOADED:
            code = SNIPPET_DB.get(hashval)
            if code is None:
                return 0.5
            for stmt in PrologString(code):
                database += stmt          # ★ 真正写入 ClauseDB
            _LOADED.add(hashval)
    return True                           # 指令成功
