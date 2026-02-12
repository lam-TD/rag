import os
import schemathesis

FAKE_MODEL = os.getenv("LLM_FAKE_MODEL", "fake")
INT_FIELDS = set(filter(None, os.getenv("SCHEMA_INT_FIELDS", "max_tokens,top_k,seed").split(",")))

def _fix(obj):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in INT_FIELDS and isinstance(v, float) and v.is_integer():
                out[k] = int(v)  # 2.0 -> 2
            else:
                out[k] = _fix(v)
        return out
    if isinstance(obj, list):
        return [_fix(x) for x in obj]
    return obj

@schemathesis.hook("map_body")
def map_body(ctx, body):
    if isinstance(body, dict) and "llm_model" in body:
        body = dict(body)
        body["llm_model"] = FAKE_MODEL
    return _fix(body)

@schemathesis.hook("before_call")
def before_call(ctx, case, kwargs):
    token = os.getenv("API_TOKEN")
    if token:
        case.headers = dict(case.headers or {})
        case.headers["Authorization"] = f"Bearer {token}"