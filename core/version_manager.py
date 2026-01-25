import subprocess


class VersionManager:
    def check(self, version_cmd):
        try:
            out = subprocess.check_output(
                version_cmd, shell=True, stderr=subprocess.STDOUT
            )
            return out.decode().strip().split("\n")[0]
        except Exception:
            return None
