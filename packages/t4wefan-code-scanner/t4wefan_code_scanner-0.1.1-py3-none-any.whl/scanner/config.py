# config.py
import toml
import os
from .project_typings.config_data import ConfigData

DEFAULT_CONFIG_FILE_NAME = ".scan_config.toml"

def get_default_config() -> ConfigData:
    """Returns the default configuration."""
    return ConfigData()

def load_config(dir: str) -> ConfigData:
    """Loads the configuration from the specified directory."""
    config_path = os.path.join(dir, DEFAULT_CONFIG_FILE_NAME)
    
    # 如果配置文件不存在，则创建并写入默认值
    if not os.path.exists(config_path):
        default_config = get_default_config()
        save_config(dir, default_config)
        return default_config

    try:
        with open(config_path, "r") as f:
            config_dict = toml.load(f)
            # 使用默认配置填充缺失的字段
            default_config = get_default_config()
            for key, value in default_config.to_dict().items():
                if key not in config_dict:
                    config_dict[key] = value
            config = ConfigData(**config_dict)
            return config
    except Exception as e:
        print(f"Error loading config file: {e}.  Using default config.")
        return get_default_config()

def save_config(dir: str, config: ConfigData):
    """Saves the configuration to the specified directory."""
    config_path = os.path.join(dir, DEFAULT_CONFIG_FILE_NAME)
    with open(config_path, "w") as f:
        # 使用 toml.dump 将 config 对象转换为字典并写入文件
        toml.dump(config.to_dict(), f)

def create_default_config(dir: str) -> bool:
    """Creates a default configuration file in the specified directory.
    Returns True if the file was created, False if it already exists.
    """
    config_path = os.path.join(dir, DEFAULT_CONFIG_FILE_NAME)
    if os.path.exists(config_path):
        return False

    default_config = get_default_config()
    save_config(dir, default_config)
    return True
