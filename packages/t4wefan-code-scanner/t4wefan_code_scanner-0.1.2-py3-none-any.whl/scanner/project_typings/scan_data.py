# project_typings/scan_data.py
from typing import List, Tuple, Dict

class ScanResult:
    file_paths: List[str] = []
    dir_paths: List[str] = []
    too_large_files: List[Tuple[str, float]] = [] # 文件路径和大小(MB)
    file_contents: Dict[str, str] = {} # 文件路径和文件内容
