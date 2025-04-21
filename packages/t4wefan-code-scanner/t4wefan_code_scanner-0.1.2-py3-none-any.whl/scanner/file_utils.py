# file_utils.py
import os
import fnmatch
from typing import List

def is_ignored(path: str, ignore_patterns: List[str]) -> bool:
    """Checks if the given path should be ignored based on the ignore patterns."""
    # 规范化路径，确保使用正斜杠
    path = path.replace("\\", "/")
    for pattern in ignore_patterns:
        # 规范化模式，确保使用正斜杠
        # print(pattern)
        pattern = pattern.replace("\\", "/")
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


def get_file_size_mb(path: str) -> float:
    """Gets the file size in MB."""
    size_in_bytes = os.path.getsize(path)
    size_in_mb = size_in_bytes / (1024 * 1024)
    return size_in_mb
