import manufacturingagents.default_config as default_config
from typing import Dict, Optional
from manufacturingagents.config.config_manager import config_manager

# Use default config but allow it to be overridden
_config: Optional[Dict] = None
DATA_DIR: Optional[str] = None


def initialize_config():
    """Initialize the configuration with default values."""
    global _config, DATA_DIR
    if _config is None:
        # 优先使用配置管理器的设置
        settings = config_manager.load_settings()
        _config = default_config.DEFAULT_CONFIG.copy()
        
        # 如果配置管理器中有数据目录设置，使用它
        if settings.get("data_dir"):
            _config["data_dir"] = settings["data_dir"]
        
        DATA_DIR = _config["data_dir"]
        
        # 确保目录存在
        config_manager.ensure_directories_exist()


def set_config(config: Dict):
    """Update the configuration with custom values."""
    global _config, DATA_DIR
    if _config is None:
        _config = default_config.DEFAULT_CONFIG.copy()
    
    _config.update(config)
    DATA_DIR = _config["data_dir"]
    
    # 如果设置了数据目录，同时更新配置管理器
    if "data_dir" in config:
        config_manager.set_data_dir(config["data_dir"])


def get_config() -> Dict:
    """Get the current configuration."""
    if _config is None:
        initialize_config()

    # 动态获取最新的数据目录配置
    current_data_dir = config_manager.get_data_dir()
    if _config["data_dir"] != current_data_dir:
        _config["data_dir"] = current_data_dir
        global DATA_DIR
        DATA_DIR = current_data_dir

    # 注意：数据库配置现在由 tradingagents.config.database_manager 管理
    # 这里不再包含数据库配置，避免配置冲突
    config_copy = _config.copy()

    return config_copy


def get_data_dir() -> str:
    """获取数据目录路径"""
    return config_manager.get_data_dir()


def set_data_dir(data_dir: str):
    """设置数据目录路径"""
    config_manager.set_data_dir(data_dir)
    # 更新全局变量
    global _config, DATA_DIR
    if _config is None:
        initialize_config()
    _config["data_dir"] = data_dir
    DATA_DIR = data_dir


# Initialize with default config
initialize_config()
