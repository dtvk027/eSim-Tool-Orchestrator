import argparse
from core.engine import Engine

engine = Engine()

parser = argparse.ArgumentParser(description="eSim Tool Orchestrator")
sub = parser.add_subparsers(dest="command")

# Install command
install = sub.add_parser("install")
install.add_argument("tool")
install.add_argument("--dry-run", action="store_true")

# Uninstall command
uninstall = sub.add_parser("uninstall")
uninstall.add_argument("tool")
uninstall.add_argument("--dry-run", action="store_true")

# List installed tools
sub.add_parser("list")

# Version command
version = sub.add_parser("version")
version.add_argument("tool")

# Check updates command
update = sub.add_parser("check-updates")
update.add_argument("tool")

# Validate toolchain
sub.add_parser("validate")

args = parser.parse_args()

if args.command == "install":
    print(engine.install_tool(args.tool, dry_run=args.dry_run))

elif args.command == "uninstall":
    print(engine.uninstall_tool(args.tool, dry_run=args.dry_run))

elif args.command == "list":
    print(engine.list_tools())

elif args.command == "version":
    print(engine.check_version(args.tool))

elif args.command == "check-updates":
    print(engine.check_updates(args.tool))

elif args.command == "validate":
    print(engine.validate_toolchain())

else:
    parser.print_help()
