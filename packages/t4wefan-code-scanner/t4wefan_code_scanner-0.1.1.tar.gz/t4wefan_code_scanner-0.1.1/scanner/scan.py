# scan.py
import os
from typing import List, Tuple
from .config import load_config
from .file_utils import is_ignored, get_file_size_mb
from .project_typings.config_data import ConfigData
from .project_typings.scan_data import ScanResult

def scan_directory(dir: str, config: ConfigData) -> ScanResult:
    """Scans the given directory and returns the file and directory paths."""
    scan_result = ScanResult()

    for root, _, files in os.walk(dir):
        # 避免处理被忽略的文件夹
        if is_ignored(root, config.ignore):
            # print(f"Ignoring directory: {root}")  # 移除调试信息
            continue

        scan_result.dir_paths.append(root)

        for file in files:
            file_path = os.path.join(root, file)

            if is_ignored(file_path, config.ignore):
                # print(f"Ignoring file: {file_path}")  # 移除调试信息
                continue

            file_size_mb = get_file_size_mb(file_path)
            if file_size_mb > config.max_size:
                scan_result.too_large_files.append((file_path, file_size_mb))
                continue

            scan_result.file_paths.append(file_path)

            # 读取文件内容
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    scan_result.file_contents[file_path] = f.read()
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                scan_result.file_contents[file_path] = f"Error reading file: {e}"

    return scan_result
