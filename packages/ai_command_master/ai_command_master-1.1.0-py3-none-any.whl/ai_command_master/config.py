from typing import Dict, Any, Optional
import os
import yaml
from pathlib import Path

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """初始化配置管理器
        
        初始化配置管理器的各项属性，包括：
        - config_dir: 配置文件根目录
        - default_config: 默认配置文件路径
        - user_config_dir: 用户配置文件目录
        - active_profile: 当前激活的配置文件名
        - config_data: 配置数据字典
        """
        # 配置文件根目录
        self.config_dir: str = os.path.join(os.path.dirname(__file__), 'config')
        # 默认配置文件路径
        self.default_config: str = os.path.join(self.config_dir, 'default.yaml')
        # 用户配置文件目录
        self.user_config_dir: str = os.path.join(self.config_dir, 'profiles')
        # 最后使用的配置记录文件
        self.last_profile_file: str = os.path.join(self.config_dir, '.last_profile')
        # 确保配置目录存在
        os.makedirs(self.user_config_dir, exist_ok=True)
        # 初始化配置数据
        self.config_data: Dict[str, Any] = {}
        # 获取上次使用的配置
        self.active_profile: str = self._get_last_profile()
        # 加载配置
        self.load_config()

    def _get_last_profile(self) -> str:
        """获取上次使用的配置名称"""
        try:
            if os.path.exists(self.last_profile_file):
                with open(self.last_profile_file, 'r', encoding='utf-8') as f:
                    last_profile = f.read().strip()
                # 验证配置文件是否存在
                if last_profile and os.path.exists(os.path.join(self.user_config_dir, f"{last_profile}.yaml")):
                    return last_profile
        except Exception:
            pass
        return 'default'

    def _save_last_profile(self) -> None:
        """保存当前使用的配置名称
        
        使用文件锁确保多进程安全写入
        """
        try:
            with open(self.last_profile_file, 'w', encoding='utf-8') as f:
                # Windows系统使用 msvcrt 进行文件锁定
                import msvcrt
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                try:
                    f.write(self.active_profile)
                    f.flush()  # 确保写入磁盘
                    os.fsync(f.fileno())  # 强制同步到磁盘
                finally:
                    # 释放锁
                    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except Exception as e:
            # print(f"保存配置文件时出错: {str(e)}")
            pass
    def get_available_profiles(self) -> list:
        """获取所有可用的配置文件列表"""
        profiles: list = []
        for file in os.listdir(self.user_config_dir):
            if file.endswith('.yaml'):
                profiles.append(file[:-5])  # 移除.yaml后缀
        return profiles

    def create_profile(self, profile_name: str, config_data: Dict[str, Any] = None) -> bool:
        """创建新的配置文件
        Args:
            profile_name: 配置文件名称
            config_data: 配置数据，如果为None则复制当前配置
        """
        if not profile_name:
            raise ValueError("配置文件名称不能为空")
            
        profile_path = os.path.join(self.user_config_dir, f"{profile_name}.yaml")
        
        # 如果文件已存在，返回False
        if os.path.exists(profile_path):
            return False
            
        # 如果没有提供配置数据，使用当前配置
        if config_data is None:
            config_data = self.config_data
            
        # 写入新配置文件
        with open(profile_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(config_data, f, allow_unicode=True)
            
        return True

    def switch_profile(self, profile_name: str) -> bool:
        """切换到指定的配置文件
        Args:.
            profile_name: 配置文件名称
        """
        profile_path = os.path.join(self.user_config_dir, f"{profile_name}.yaml")
        
        if not os.path.exists(profile_path):
            return False
            
        self.active_profile = profile_name
        # 保存当前配置状态
        self._save_last_profile()
        # 加载新配置
        self.load_config()
        return True

    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""

        # 如果用户配置文件目录为空，则创建用户配置文件目录
        if not os.path.exists(self.user_config_dir):
            os.makedirs(self.user_config_dir)

        try:
            # 首先加载默认配置
            with open(self.default_config, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f) or {}

            # 如果不是default配置，则加载对应的配置文件
            if self.active_profile != 'default':
                profile_path = os.path.join(self.user_config_dir, f"{self.active_profile}.yaml")
                if os.path.exists(profile_path):
                    with open(profile_path, 'r', encoding='utf-8') as f:
                        user_config = yaml.safe_load(f) or {}
                        # 深度合并配置
                        config_data = self._deep_merge(config_data, user_config)

            self.config_data = config_data
            return self.config_data
            
        except Exception as e:
            print(f"加载配置文件时出错: {str(e)}")
            return {}

    def _deep_merge(self, dict1: dict, dict2: dict) -> dict:
        """深度合并两个字典"""
        result = dict1.copy()
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def get_config(self, key: str = None) -> Any:
        """获取配置值"""
        if key is None:
            return self.config_data
        
        keys = key.split('.')
        value = self.config_data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        return value

    def get_active_profile(self) -> str:
        """获取当前激活的配置文件名称"""
        return self.active_profile