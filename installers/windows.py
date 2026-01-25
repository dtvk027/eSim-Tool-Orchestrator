import subprocess
from .base import BaseInstaller


class WindowsInstaller(BaseInstaller):
    def install(self, cmd, dry_run=False):
        return self.run(cmd, dry_run)

    def run(self, cmd, dry_run=False):
        if dry_run:
            return f"[DRY-RUN] {cmd}"
        subprocess.run(cmd, shell=True, check=True)
        return "success"
