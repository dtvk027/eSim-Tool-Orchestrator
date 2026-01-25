import os
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.env_file = Path(".esim_env")

    def apply_env(self, env_vars):
        if not env_vars:
            return

        with open(self.env_file, "a") as f:
            for k, v in env_vars.items():
                os.environ[k] = v
                f.write(f"{k}={v}\n")

    def load_env(self):
        if not self.env_file.exists():
            return
        with open(self.env_file) as f:
            for line in f:
                k, v = line.strip().split("=", 1)
                os.environ[k] = v
