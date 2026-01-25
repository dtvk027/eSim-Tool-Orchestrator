class BaseInstaller:
    def install(self, cmd, dry_run=False):
        raise NotImplementedError

    def run(self, cmd, dry_run=False):
        raise NotImplementedError
