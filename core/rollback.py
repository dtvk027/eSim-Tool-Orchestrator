import json
from pathlib import Path


class RollbackManager:
    def __init__(self, file="rollback.json"):
        self.file = Path(file)
        if not self.file.exists():
            self.file.write_text("{}")

    def snapshot(self, tool, state):
        data = json.loads(self.file.read_text())
        data[tool] = state
        self.file.write_text(json.dumps(data, indent=2))

    def restore(self, tool):
        data = json.loads(self.file.read_text())
        return data.get(tool)
