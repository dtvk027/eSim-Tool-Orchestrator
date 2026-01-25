import json
from pathlib import Path


class StateManager:
    def __init__(self, file="state.json"):
        self.file = Path(file)
        if not self.file.exists():
            self.file.write_text("{}")

    def load(self):
        return json.loads(self.file.read_text())

    def save(self, state):
        self.file.write_text(json.dumps(state, indent=2))
