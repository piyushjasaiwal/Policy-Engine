from models.final_result import FinalResult
import os
import json

def log_audit_trail(verdict: FinalResult):
    LOG_DIR = "evaluation_audit_logs"
    os.makedirs(LOG_DIR, exist_ok=True)
    
    file_path = f"{LOG_DIR}/{verdict.request_id}_audit_logs.jsonl"
    with open(file_path, "a") as f:
        json_safe_dict = json.loads(verdict.model_dump_json())
        json.dump(json_safe_dict, f, indent=4, sort_keys=False)