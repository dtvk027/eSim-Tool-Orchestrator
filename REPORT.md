# Automated Tool Manager for eSim

## Screening Task 5 -- Documented Report

------------------------------------------------------------------------

## 1. Introduction

eSim is an open-source EDA tool that integrates multiple external tools
such as Ngspice, KiCad, GHDL, Verilator, and OpenModelica.
Manually installing, configuring, and maintaining these tools is
time-consuming and error-prone.

This project implements an **Automated Tool Manager** that provides:

-   Cross-platform installation (Linux & Windows)
-   Dependency resolution
-   Version management
-   Update checking
-   Rollback safety
-   Persistent configuration
-   Toolchain validation
-   Structured logging
-   CLI-based user interface

------------------------------------------------------------------------

## 2. Objectives

The goals of this project were:

-   Automate installation and configuration of eSim dependencies
-   Ensure compatibility with Linux and Windows
-   Implement version control and update checking
-   Provide dependency checking and user feedback
-   Enable rollback safety for failed installs
-   Provide a simple CLI interface
-   Maintain audit logs
-   Support extensibility via manifests

------------------------------------------------------------------------

## 3. System Architecture

The system follows a layered architecture:

CLI → Engine → Core Services → OS Installers

### Key Components

  Component            Purpose
  -------------------- -----------------------------------
  cli.py               CLI interface and command routing
  Engine               Central orchestration logic
  ManifestLoader       Loads YAML tool definitions
  Resolver             OS detection + dependency checks
  VersionManager       Tool version detection
  UpdateChecker        GitHub API integration
  ConfigManager        Persistent environment config
  StateManager         Installed tool tracking
  RollbackManager      Failure-safe rollback
  Logger               Structured audit logging
  ToolchainValidator   Full eSim dependency validation
  LinuxInstaller       apt execution
  WindowsInstaller     Chocolatey execution

------------------------------------------------------------------------

## 4. Functional Features

### 4.1 Tool Installation

-   Manifest-driven installation
-   Version pinning (e.g., Ngspice v40)
-   Dry-run mode
-   Cross-platform support
-   Uninstall support

------------------------------------------------------------------------

### 4.2 Dependency Checker

-   Reads tool dependencies from manifest
-   Detects missing tools
-   Blocks installation if dependencies are missing
-   Provides user feedback

------------------------------------------------------------------------

### 4.3 Version Management

-   Executes tool-specific version commands
-   Normalizes version output
-   Stores detected version in state.json

------------------------------------------------------------------------

### 4.4 Update & Upgrade System

-   Integrates with GitHub API
-   Fetches latest releases
-   Handles edge cases (missing releases)
-   Provides structured update diagnostics

------------------------------------------------------------------------

### 4.5 Configuration Handling

-   Supports post-install hooks via manifest
-   Writes persistent environment variables
-   Injects runtime environment variables
-   Isolated from dry-run mode

------------------------------------------------------------------------

### 4.6 Rollback Safety

-   Snapshots system state before install
-   Restores state on failure
-   Prevents partial installs
-   Logs failure events

------------------------------------------------------------------------

### 4.7 Logging System

-   Structured JSON logs (actions.jsonl)
-   Logs success + failure
-   Timestamped audit trail
-   Debuggable execution history

------------------------------------------------------------------------

### 4.8 Toolchain Validation

-   Domain-aligned validation using esim.yaml
-   Detects missing dependencies
-   Returns readiness status

------------------------------------------------------------------------

## 5. Cross-Platform Strategy

The orchestrator supports:

  OS        Package Manager
  --------- -----------------
  Linux     apt
  Windows   Chocolatey

OS abstraction is handled via:

-   Resolver.get_os_key()
-   Manifest OS blocks
-   Installer subclasses

------------------------------------------------------------------------

## 6. Safety Guarantees

  Guarantee                Mechanism
  ------------------------ --------------------
  No side-effects          Dry-run mode
  No partial installs      Rollback safety
  Idempotent behavior      State gating
  Deterministic behavior   Manifest-driven
  Auditability             Structured logging
  Failure isolation        Exception handling

------------------------------------------------------------------------

## 7. QA Verification Summary

All major functional paths were tested and verified:

-   CLI boot sanity
-   Manifest parsing
-   Dry-run install
-   Real install
-   Dependency failure detection
-   Version detection
-   Update checking (API integration)
-   Configuration injection
-   Rollback safety
-   Structured logging
-   Toolchain validation

------------------------------------------------------------------------

## 8. Extensibility

New tools can be added by:

1.  Creating a YAML manifest
2.  Defining install/uninstall commands
3.  Defining version detection command
4.  Defining dependencies

No Python code changes required.

------------------------------------------------------------------------

## 9. Conclusion

This project delivers a production-grade Automated Tool Manager for eSim
that:

-   Fully satisfies all screening task requirements
-   Implements additional safety and audit features
-   Supports cross-platform execution
-   Is extensible, maintainable, and failure-safe

It transforms manual tool setup into a deterministic, automated, and
validated workflow.

------------------------------------------------------------------------

## 10. Author

Name: D. Tvk
Program: B.Tech Computer Science
Submission For: eSim Semester Long Internship -- Spring 2026
GitHub: https://github.com/D-Tvk
Location: India

------------------------------------------------------------------------
