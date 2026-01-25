# eSim Tool Orchestrator – Design Document

---

## 1. Purpose

The eSim Tool Orchestrator is designed to automate the lifecycle management of external tools required by the eSim EDA environment.

It addresses the following problems:

- Manual installation complexity
- Cross-platform incompatibilities
- Version mismatches
- Missing dependencies
- Lack of auditability
- Unsafe partial installs

---

## 2. Architectural Overview

The system follows a layered architecture:

```
CLI Layer  ->  Engine  ->  Core Services  ->  OS Installers
```

Each layer has a strict responsibility boundary.

---

## 3. Core Components

### 3.1 CLI (cli.py)

- User entry point
- Argument parsing
- Command routing
- Output rendering

Commands:

- install
- uninstall
- list
- version
- check-updates
- validate

---

### 3.2 Engine (core/engine.py)

Central orchestration layer.

Responsibilities:

- Load manifests
- Resolve OS
- Enforce idempotency
- Validate dependencies
- Dispatch installers
- Trigger rollback
- Persist state
- Apply configuration
- Emit logs

---

### 3.3 Manifest Loader (core/manifest_loader.py)

- Reads YAML tool definitions
- Validates schema
- Provides structured tool metadata

---

### 3.4 Resolver (core/resolver.py)

- Detects operating system
- Checks availability of dependencies
- Provides OS abstraction key

---

### 3.5 Installer Layer (installers/)

Two implementations:

- LinuxInstaller
- WindowsInstaller

Responsibilities:

- Execute shell commands
- Capture exit codes
- Support dry-run simulation

---

### 3.6 Version Manager (core/version_manager.py)

- Executes version commands
- Normalizes version output
- Decoupled from state

---

### 3.7 Update Checker (core/update_checker.py)

- Integrates with GitHub API
- Fetches latest releases
- Handles missing tags
- Handles API failures
- Returns structured update info

---

### 3.8 Config Manager (core/config_manager.py)

- Applies post-install configuration
- Writes persistent environment variables
- Injects runtime environment

---

### 3.9 State Manager (core/state_manager.py)

- Persists installation state
- Loads state safely
- Enforces deterministic behavior

---

### 3.10 Rollback Manager (core/rollback.py)

- Snapshots pre-install state
- Restores state on failure
- Guarantees system integrity

---

### 3.11 Logger (core/logger.py)

- Writes structured JSON logs
- Logs only real actions
- Supports auditing and debugging

---

### 3.12 Toolchain Validator (core/validator.py)

- Validates full eSim dependency graph
- Detects missing tools
- Returns readiness status

---

## 4. Data Flow (Install Example)

```
User -> CLI -> Engine
Engine -> ManifestLoader
Engine -> Resolver
Engine -> RollbackManager
Engine -> Installer
Engine -> VersionManager
Engine -> StateManager
Engine -> ConfigManager
Engine -> Logger
```

Failure Path:

```
Installer Failure -> Engine -> RollbackManager -> StateManager -> Logger
```

---

## 5. Safety Guarantees

| Guarantee               | Mechanism                     |
|------------------------|-------------------------------|
| No side-effects        | Dry-run mode                  |
| No partial installs    | Rollback snapshots            |
| Idempotent installs    | State gating                  |
| Deterministic behavior | Manifest-driven design        |
| Auditability           | Structured logging            |
| Failure isolation      | Exception handling + restore  |

---

## 6. Extensibility

The system is designed to be extensible without code changes.

New tools can be added by:

1. Creating a new YAML manifest
2. Defining install/uninstall commands
3. Defining version detection command
4. Defining dependencies

No Python code changes required.

---

## 7. Cross-Platform Strategy

OS abstraction is handled by:

- Resolver.get_os_key()
- Manifest OS blocks
- Installer subclasses

This allows consistent behavior across:

- Linux (apt)
- Windows (Chocolatey)

---

## 8. Error Handling Philosophy

The orchestrator follows a strict failure-safe policy:

- Fail fast
- Fail loud
- Never corrupt state
- Always restore previous state
- Always log failures

---

## 9. QA Certification Summary

The following scenarios were tested and passed:

- CLI boot
- Manifest parsing
- Dry-run install
- Real install
- Dependency failure
- Version detection
- Update checking (API integration)
- Configuration injection
- Rollback safety
- Structured logging
- Toolchain validation

---

## 10. Design Rationale

Key architectural decisions:

- Manifest-driven configuration over hardcoding
- Separation of concerns between layers
- Explicit rollback handling
- Dry-run as a first-class feature
- API-based update checking
- Structured logging instead of print debugging

---

## 11. Future Enhancements

- GUI frontend
- Automatic update execution
- Parallel installs
- Plugin system
- Remote manifests
- CI/CD integration

---

