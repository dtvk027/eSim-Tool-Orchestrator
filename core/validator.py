class ToolchainValidator:
    REQUIRED = ["kicad", "ngspice", "ghdl", "verilator", "openmodelica"]

    def validate(self, state):
        missing = []
        for tool in self.REQUIRED:
            if tool not in state:
                missing.append(tool)
        return missing
