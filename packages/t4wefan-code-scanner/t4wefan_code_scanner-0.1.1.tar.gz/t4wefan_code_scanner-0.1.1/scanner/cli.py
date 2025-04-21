# cli.py
import argparse
from typing import List
from .project_typings.cli_args import CLIArgs, ScanArgs, ConfigArgs, ConfigAddArgs

def parse_args(args: List[str]) -> CLIArgs:
    parser = argparse.ArgumentParser(description="Code Scanner")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan a directory")
    scan_parser.add_argument("dir", nargs="?", default=".", help="Directory to scan (default: .)")
    scan_parser.add_argument("--no-color", action="store_true", help="Disable colored output")

    # Config command
    config_parser = subparsers.add_parser("config", help="Configure the scanner")
    config_subparsers = config_parser.add_subparsers(dest="subcommand", help="Config subcommands")

    # Config add subcommand
    config_add_parser = config_subparsers.add_parser("add", help="Add configuration options")
    config_add_parser.add_argument("dir", nargs="?", default=".", help="Directory containing the config file (default: .)")
    config_add_parser.add_argument("--no-file-tree", action="store_true", help="Disable file tree output")
    config_add_parser.add_argument("--max-size", "-m", type=float, help="Maximum file size (MB)")
    config_add_parser.add_argument("--output", "-o", type=str, help="Output file name")
    config_add_parser.add_argument("--ignore", "-i", type=str, action="append", help="Ignore pattern (can be used multiple times)")

    # Config init subcommand
    config_init_parser = config_subparsers.add_parser("init", help="Initialize config file")
    config_init_parser.add_argument("dir", nargs="?", default=".", help="Directory containing the config file (default: .)")

    parsed_args = parser.parse_args(args)

    cli_args = CLIArgs()

    if parsed_args.command == "scan":
        cli_args.scan = ScanArgs()
        cli_args.scan.dir = parsed_args.dir
        cli_args.scan.no_color = parsed_args.no_color
    elif parsed_args.command == "config":
        if parsed_args.subcommand == "add":
            cli_args.config_add = ConfigAddArgs()
            cli_args.config_add.dir = parsed_args.dir
            cli_args.config_add.no_file_tree = parsed_args.no_file_tree if hasattr(parsed_args, "no_file_tree") else None
            cli_args.config_add.max_size = parsed_args.max_size if hasattr(parsed_args, "max_size") else None
            cli_args.config_add.output = parsed_args.output if hasattr(parsed_args, "output") else None
            cli_args.config_add.ignore = parsed_args.ignore if hasattr(parsed_args, "ignore") else None
        elif parsed_args.subcommand == "init":
            cli_args.config = ConfigArgs()
            cli_args.config.dir = parsed_args.dir
        else:
            # If no subcommand is provided, print help message for config
            config_parser.print_help()
            return cli_args # Return empty CLIArgs to prevent further execution
    elif not parsed_args.command:
        # If no command is provided, print help message
        parser.print_help()
        return cli_args # Return empty CLIArgs to prevent further execution
    else:
        # Default to scan with current directory if no command is given
        cli_args.scan = ScanArgs()
        cli_args.scan.dir = "." # Default directory
        cli_args.scan.no_color = False

    return cli_args
