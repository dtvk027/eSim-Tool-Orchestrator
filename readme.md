# eSim Tool Orchestrator

Automated Tool Manager for eSim (Linux & Windows)

---

## Overview

The **eSim Tool Orchestrator** is a cross-platform automation engine that installs, configures, updates, validates, and manages all external tools required by the eSim ecosystem.

It replaces manual setup with a safe, auditable, and extensible orchestration system.

---

## Key Features

- Manifest-driven tool installation
- Cross-platform support (Linux + Windows)
- Version pinning and version detection
- Dependency resolution
- Dry-run simulation mode
- Rollback safety on failure
- Persistent state tracking
- Structured JSON logging
- GitHub-based update checking
- Post-install configuration handling
- Toolchain validation (domain-aligned with eSim)

---

## Supported Tools

| Tool          | Package Manager | Version Pinning | Update Check |
|---------------|-----------------|------------------|--------------|
| Ngspice       | apt / choco     | Yes (v40)        | Yes          |
| KiCad         | apt / choco     | Latest           | Yes          |
| GHDL          | apt / choco     | Latest           | Yes          |
| Verilator     | apt / choco     | Latest           | Yes          |
| OpenModelica  | apt / choco     | Latest           | Yes          |

---

## Installation

### Requirements

- Python 3.8+
- Windows: Chocolatey installed
- Linux: apt-based distro

### Setup

```bash
pip install requests
```

---

## Usage

### Install Tool

```bash
python cli.py install ngspice
```

### Dry-Run Install

```bash
python cli.py install ngspice --dry-run
```

### Uninstall Tool

```bash
python cli.py uninstall ngspice
```

### List Installed Tools

```bash
python cli.py list
```

### Check Tool Version

```bash
python cli.py version ngspice
```

### Check for Updates

```bash
python cli.py check-updates ngspice
```

### Validate Full Toolchain

```bash
python cli.py validate
```

---

## State Management

Installed tools are tracked in:

```
state.json
```

Example:

```json
{
  "ngspice": {
    "version": "Ngspice-40",
    "channel": "stable"
  }
}
```

---

## Logging

All real actions are logged in:

```
actions.jsonl
```

Each entry contains:

- Timestamp
- Tool
- Action
- Status
- Detail

Example:

```json
{"timestamp":"2026-01-25T19:46:36","tool":"ngspice","action":"install","status":"success","detail":"Ngspice-40"}
```

---

## Configuration Handling

Post-install configuration hooks are supported via manifest:

```yaml
post_install:
  env:
    ESIM_HOME: "/opt/esim"
```

Persistent env variables are written to:

```
.esim_env
```

---

## Update System

The orchestrator checks GitHub releases for updates.

Example:

```json
{
  "tool": "ngspice",
  "current": null,
  "latest": "unknown",
  "update_available": false,
  "note": "Project does not publish GitHub releases"
}
```

---

## Verified QA Checklist

The following tests were executed and passed:

- CLI boot sanity
- Manifest parsing
- Dry-run install
- Real install
- Dependency resolution
- Version detection
- Update checking (API integration)
- Configuration injection
- Rollback safety
- Structured logging
- Toolchain validation

---

## Project Structure

```
esim-tool-orchestrator/
├── cli.py
├── core/
│   ├── engine.py
│   ├── resolver.py
│   ├── manifest_loader.py
│   ├── version_manager.py
│   ├── update_checker.py
│   ├── config_manager.py
│   ├── rollback.py
│   ├── state_manager.py
│   ├── validator.py
│   └── logger.py
├── installers/
│   ├── windows.py
│   └── linux.py
├── manifests/
│   ├── ngspice.yaml
│   ├── kicad.yaml
│   ├── ghdl.yaml
│   ├── verilator.yaml
│   ├── openmodelica.yaml
│   └── esim.yaml
├── state.json
├── actions.jsonl
├── rollback.json
└── .esim_env
```

---

## Design Goals

- Safety-first automation
- Deterministic behavior
- Zero side-effects in dry-run
- Extensible manifest format
- Production-grade observability
- Interview-defensible architecture

---

## Author

**Name:** D. Tvk  
**Program:** B.Tech Computer Science  
**Submission For:** eSim Semester Long Internship – Spring 2026  
**GitHub:** https://github.com/D-Tvk  
**Location:** India  

---



