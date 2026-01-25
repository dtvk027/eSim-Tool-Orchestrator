from core.manifest_loader import ManifestLoader
from core.resolver import Resolver
from core.version_manager import VersionManager
from core.state_manager import StateManager
from core.config_manager import ConfigManager
from core.logger import Logger
from core.rollback import RollbackManager
from core.update_checker import UpdateChecker
from core.validator import ToolchainValidator
from installers.linux import LinuxInstaller
from installers.windows import WindowsInstaller


class Engine:
    def __init__(self):
        self.loader = ManifestLoader()
        self.resolver = Resolver()
        self.version_mgr = VersionManager()
        self.state_mgr = StateManager()
        self.config_mgr = ConfigManager()
        self.logger = Logger()
        self.rollback_mgr = RollbackManager()
        self.update_checker = UpdateChecker()
        self.validator = ToolchainValidator()

        self.installer = (
            LinuxInstaller()
            if self.resolver.get_os_key() == "linux"
            else WindowsInstaller()
        )

    def install_tool(self, tool, channel="stable", dry_run=False):
        manifest = self.loader.load(tool)
        os_key = self.resolver.get_os_key()
        state = self.state_mgr.load()

        # Idempotency: already installed
        if tool in state and not dry_run:
            return f"{tool} already installed (version {state[tool]['version']})"

        # Dependency check
        deps = manifest.get("dependencies", [])
        missing = self.resolver.check_dependencies(deps)
        if missing:
            if not dry_run:
                self.logger.log(tool, "dependency_check", "failed", str(missing))
            return f"Missing dependencies: {missing}"

        tool_cfg = manifest["channels"][channel][os_key]
        cmd = tool_cfg["install"]

        # Snapshot for rollback (real installs only)
        if not dry_run:
            self.rollback_mgr.snapshot(tool, state.get(tool, {}))

        try:
            result = self.installer.install(cmd, dry_run)

            # Version detection
            version = self.version_mgr.check(tool_cfg["version_cmd"])

            # Persist state (real installs only)
            if not dry_run:
                state[tool] = {
                    "version": version or "unknown",
                    "channel": channel
                }
                self.state_mgr.save(state)

                # Apply env config (if any)
                env = manifest.get("post_install", {}).get("env", {})
                self.config_mgr.apply_env(env)

                # Log success
                self.logger.log(tool, "install", "success", version)

            return result

        except Exception as e:
            # Failure handling (real installs only)
            if not dry_run:
                self.logger.log(tool, "install", "failed", str(e))
                restored = self.rollback_mgr.restore(tool)
                if restored:
                    state[tool] = restored
                    self.state_mgr.save(state)
            return f"Installation failed. Rolled back. Error: {e}"

    def uninstall_tool(self, tool, dry_run=False):
        manifest = self.loader.load(tool)
        os_key = self.resolver.get_os_key()
        state = self.state_mgr.load()

        if tool not in state:
            return f"{tool} is not installed"

        uninstall_cmd = manifest["channels"]["stable"][os_key].get("uninstall")
        if not uninstall_cmd:
            return f"No uninstall command defined for {tool}"

        try:
            result = self.installer.install(uninstall_cmd, dry_run)
            if not dry_run:
                del state[tool]
                self.state_mgr.save(state)
                self.logger.log(tool, "uninstall", "success", "")
            return result
        except Exception as e:
            if not dry_run:
                self.logger.log(tool, "uninstall", "failed", str(e))
            return f"Uninstall failed: {e}"

    def list_tools(self):
        return self.state_mgr.load()

    def check_version(self, tool):
        manifest = self.loader.load(tool)
        os_key = self.resolver.get_os_key()
        cfg = manifest["channels"]["stable"][os_key]
        return self.version_mgr.check(cfg["version_cmd"])

    def check_updates(self, tool):
        state = self.state_mgr.load()
        current = state.get(tool, {}).get("version")
        return self.update_checker.check(tool, current)

    def validate_toolchain(self):
        state = self.state_mgr.load()
        missing = self.validator.validate(state)
        if missing:
            return {"status": "incomplete", "missing": missing}
        return {"status": "ready", "message": "All eSim dependencies installed"}
