# project_typings/cli_args.py
from typing import Optional, List
from dataclasses import dataclass, field

@dataclass
class ScanArgs:
    dir: str = "."
    no_color: bool = False

@dataclass
class ConfigAddArgs:
    dir: str = "."
    no_file_tree: Optional[bool] = None
    max_size: Optional[float] = None
    output: Optional[str] = None
    ignore: Optional[List[str]] = None

@dataclass
class ConfigArgs:
    dir: str = "."

@dataclass
class CLIArgs:
    scan: Optional[ScanArgs] = None
    config: Optional[ConfigArgs] = None
    config_add: Optional[ConfigAddArgs] = None
