# project_typings/config_data.py
from typing import List
import os
from dataclasses import dataclass, field

@dataclass
class ConfigData:
    no_file_tree: bool = False
    output: str = f"{os.path.basename(os.path.abspath('.'))}.md"  # 直接计算默认值
    max_size: float = 0.5
    ignore: List[str] = field(default_factory=lambda: ["./.*","*.pyc","*__pycache__*","*.lock","*dist*","*.egg-info*"])

    def to_dict(self) -> dict:
        """将 ConfigData 对象转换为字典."""
        return {
            "no_file_tree": self.no_file_tree,
            "output": self.output,
            "max_size": self.max_size,
            "ignore": self.ignore,
        }
