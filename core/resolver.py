import platform
import shutil


class Resolver:
    def __init__(self):
        self.os = platform.system().lower()

    def get_os_key(self):
        if "linux" in self.os:
            return "linux"
        elif "windows" in self.os:
            return "windows"
        else:
            raise RuntimeError("Unsupported OS")

    def check_dependencies(self, deps):
        missing = []
        for dep in deps:
            if shutil.which(dep) is None:
                missing.append(dep)
        return missing
