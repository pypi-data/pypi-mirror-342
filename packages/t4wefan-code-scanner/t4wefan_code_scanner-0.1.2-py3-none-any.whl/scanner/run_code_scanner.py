import sys
import os
from .cli import parse_args
from .config import load_config, create_default_config, save_config, get_default_config
from .scan import scan_directory
from .output import print_scan_results, write_markdown_to_file
from .project_typings.cli_args import CLIArgs

def main():
    cli_args: CLIArgs = parse_args(sys.argv[1:])

    # If no command was provided, cli_args will be empty, so we exit early
    if not any([cli_args.scan, cli_args.config, cli_args.config_add]):
        return

    if cli_args.scan:
        config = load_config(cli_args.scan.dir)
        scan_result = scan_directory(cli_args.scan.dir, config)
        print_scan_results(scan_result, cli_args.scan.no_color)
        write_markdown_to_file(cli_args.scan.dir, scan_result, config)

    elif cli_args.config:
        dir = cli_args.config.dir
        if create_default_config(dir):
            print(f"Created default config file in {dir}")
            default_config = get_default_config() # 获取默认配置
            save_config(dir, default_config) # 保存默认配置
            print("Default config saved.")  # 添加调试信息
        else:
            response = input("Config file already exists. Overwrite with default? (y/n): ")
            if response.lower() == "y":
                default_config = get_default_config()
                save_config(dir, default_config)
                print("Config file reset to default.")
            else:
                print("Config file not modified.")

    elif cli_args.config_add:
        dir = cli_args.config_add.dir
        config = load_config(dir)  # Load existing config, or create a new one with defaults

        if cli_args.config_add.no_file_tree is not None:
            config.no_file_tree = cli_args.config_add.no_file_tree
        if cli_args.config_add.max_size is not None:
            config.max_size = cli_args.config_add.max_size
        if cli_args.config_add.output is not None:
            config.output = cli_args.config_add.output
        if cli_args.config_add.ignore is not None:
            # 确保 config.ignore 是一个列表
            config.ignore = config.ignore or []
            config.ignore.extend(cli_args.config_add.ignore)
            config.ignore = list(set(config.ignore))  # Remove duplicates

        save_config(dir, config)
        print("Config file updated.")
        print("Config saved after update.") # 添加调试信息

