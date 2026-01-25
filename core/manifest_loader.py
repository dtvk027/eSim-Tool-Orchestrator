import yaml
from pathlib import Path


class ManifestLoader:
    def __init__(self, manifest_dir="manifests"):
        self.manifest_dir = Path(manifest_dir)

    def load(self, tool_name):
        path = self.manifest_dir / f"{tool_name}.yaml"
        if not path.exists():
            raise FileNotFoundError(f"Manifest not found: {tool_name}")
        with open(path, "r") as f:
            return yaml.safe_load(f)
