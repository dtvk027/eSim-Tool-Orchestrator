import json
from datetime import datetime


class Logger:
    def __init__(self, file="actions.jsonl"):
        self.file = file

    def log(self, tool, action, status, detail=""):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "tool": tool,
            "action": action,
            "status": status,
            "detail": detail
        }
        with open(self.file, "a") as f:
            f.write(json.dumps(entry) + "\n")
