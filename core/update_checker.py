import requests

TOOL_RELEASES = {
    "ngspice": "ngspice/ngspice",
    "kicad": "KiCad/kicad-source-mirror",
    "verilator": "verilator/verilator",
    "ghdl": "ghdl/ghdl",
    "openmodelica": "OpenModelica/OpenModelica"
}

class UpdateChecker:
    def check(self, tool, current_version):
        repo = TOOL_RELEASES.get(tool)
        if not repo:
            return {
                "tool": tool,
                "status": "unknown_tool",
                "message": "No update source configured"
            }

        url = f"https://api.github.com/repos/{repo}/releases/latest"

        try:
            res = requests.get(url, timeout=5)

            if res.status_code == 404:
                return {
                    "tool": tool,
                    "current": current_version,
                    "latest": "unknown",
                    "update_available": False,
                    "note": "Project does not publish GitHub releases"
                }

            if res.status_code != 200:
                return {
                    "tool": tool,
                    "status": "api_error",
                    "code": res.status_code
                }

            data = res.json()
            latest = data.get("tag_name") or data.get("name")

            if not latest:
                return {
                    "tool": tool,
                    "current": current_version,
                    "latest": "unknown",
                    "update_available": False,
                    "note": "GitHub did not return a version tag"
                }

            return {
                "tool": tool,
                "current": current_version,
                "latest": latest,
                "update_available": current_version != latest
            }

        except Exception as e:
            return {
                "tool": tool,
                "status": "error",
                "detail": str(e)
            }
