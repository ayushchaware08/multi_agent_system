import json
import os
import time

# Prefer a repository-level logs folder so the backend (run from backend/app)
# writes into the central `logs/` directory at the repo root.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DEFAULT_LOG_PATH = os.path.join(BASE_DIR, "logs", "decision_logs.jsonl")
LOG_PATH = os.getenv("LOG_FILE", DEFAULT_LOG_PATH)

def append_raw_log(obj):
    dirpath = os.path.dirname(LOG_PATH)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": int(time.time()), **obj}, ensure_ascii=False) + "\n")

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
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()[-limit:]
    return [json.loads(l) for l in lines]
