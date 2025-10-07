import json, os, time
LOG_PATH = os.getenv("LOG_FILE", "logs/decision_logs.jsonl")

def append_raw_log(obj):
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps({"ts": int(time.time()), **obj}) + "\n")

def record_decision(decision, rationale, user_input, trace):
    entry = {
        "timestamp": int(time.time()),
        "decision": decision,
        "rationale": rationale,
        "input": user_input,
        "trace": trace
    }
    append_raw_log(entry)
    return entry["timestamp"]

def tail_logs(limit=100):
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r") as f:
        lines = f.readlines()[-limit:]
    return [json.loads(l) for l in lines]
