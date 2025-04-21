# output.py
from typing import List, Tuple
import os
from .project_typings.config_data import ConfigData
from .project_typings.scan_data import ScanResult
from .file_utils import is_ignored

# ANSI color codes
COLOR_RESET = "\033[0m"
COLOR_GOLD = "\033[33m"
COLOR_CYAN = "\033[36m"

def print_scan_results(scan_result: ScanResult, no_color: bool = False):
    """Prints the scan results to the console."""
    for dir_path in scan_result.dir_paths:
        if no_color:
            print(f"Scanning directory: {dir_path}/")
        else:
            print(f"{COLOR_GOLD}Scanning directory: {dir_path}/{COLOR_RESET}")

        # 打印目录下的文件
        for file_path in scan_result.file_paths:
            if os.path.dirname(file_path) == dir_path:
                if no_color:
                    print(file_path)
                else:
                    print(f"{COLOR_CYAN}{file_path}{COLOR_RESET}")

    for file_path, file_size in scan_result.too_large_files:
        print(f"Too large file: {file_path} ({file_size:.2f} MB)")

def get_language_tag(file_path: str) -> str:
    """根据文件扩展名获取相应的语言标签."""
    extension = os.path.splitext(file_path)[1].lower()
    language_map = {
        ".py": "python",
        ".js": "javascript",
        ".html": "html",
        ".css": "css",
        ".md": "markdown",
        ".toml": "toml",
        ".sh": "bash",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".xml": "xml",
        ".txt": "text",
    }
    return language_map.get(extension, "text")  # 默认使用 "text"

def generate_markdown(dir: str, scan_result: ScanResult, config: ConfigData) -> str:
    """Generates the markdown output."""
    markdown = f"# Code Scan of {dir}\n\n"

    if not config.no_file_tree:
        markdown += "## File Tree\n\n"
        markdown += generate_file_tree(dir, scan_result, config)
        markdown += "\n\n"

    # 添加源代码
    markdown += "## Source Code\n\n"
    for file_path in sorted(scan_result.file_paths):
        markdown += f"### {file_path}\n\n"
        if file_path in scan_result.file_contents:
            language_tag = get_language_tag(file_path)
            markdown += f"```{language_tag}\n"
            markdown += scan_result.file_contents[file_path]
            markdown += "\n```\n\n"
        else:
            markdown += "Error: Could not read file content or file too large.\n\n"

    if scan_result.too_large_files:
        markdown += "\n\n## Too Large Files\n\n"
        for file_path, file_size in scan_result.too_large_files:
            markdown += f"- {file_path} ({file_size:.2f} MB)\n"
    return markdown

def generate_file_tree(dir: str, scan_result: ScanResult, config: ConfigData) -> str:
    """Generates a simple file tree representation."""
    tree = f"- {dir}\n"  # 总是包含根目录

    # 获取根目录下的文件和文件夹
    root_files = [f for f in scan_result.file_paths if os.path.dirname(f) == dir]
    root_dirs = [d for d in scan_result.dir_paths if os.path.dirname(d) == dir and d != dir]

    # 添加根目录下的文件夹
    for dir_path in sorted(root_dirs):
        if is_empty_directory(dir_path, scan_result, config):
            continue
        dir_name = os.path.basename(dir_path)
        tree += f"  - {dir_name}/\n"

        # 添加子目录下的文件
        for file_path in sorted(scan_result.file_paths):
            if os.path.dirname(file_path) == dir_path:
                file_name = os.path.basename(file_path)
                tree += f"    - {file_name}\n"

    # 添加根目录下的文件
    for file_path in sorted(root_files):
        file_name = os.path.basename(file_path)
        tree += f"  - {file_name}\n"

    return tree

def is_empty_directory(dir_path: str, scan_result: ScanResult, config: ConfigData) -> bool:
    """Checks if a directory is empty, considering ignored files."""
    # 如果目录中还有未忽略的文件，则认为它不是空的
    for file_path in scan_result.file_paths:
        if os.path.dirname(file_path) == dir_path:
            return False

    # 如果目录中还有未忽略的子目录，则认为它不是空的
    for sub_dir_path in scan_result.dir_paths:
        if os.path.dirname(sub_dir_path) == dir_path and sub_dir_path != dir_path:
            return False

    return True

def write_markdown_to_file(dir: str, scan_result: ScanResult, config: ConfigData):
    """Writes the markdown output to a file."""
    output_file = config.output.replace("{当前文件夹名}", os.path.basename(os.path.abspath(dir)))
    markdown = generate_markdown(dir, scan_result, config)
    with open(output_file, "w") as f:
        f.write(markdown)
