import os
import yaml
from typing import Dict, Any

class ConfigManager:

    """配置管理类，用于处理应用程序的配置文件。

    该类负责管理默认配置和用户配置文件，支持配置的加载和保存操作。
    配置文件使用YAML格式，存储在'./ai_command_master/config/'目录下：
    - default.yaml: 默认配置文件，包含基础配置项
    - config.yaml: 用户配置文件，用于覆盖默认配置
    """

    _instance: 'Config | None' = None    # 私有化_instance用来储存唯一实例

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """初始化配置管理器，设置配置文件路径"""
        # hasattr(self, 'config_dir') 检查 self 对象是否已经具有 config_dir 属性
        if not hasattr(self, 'config_dir'):
            self.config_dir: str = os.path.join(os.path.dirname(__file__), 'config')     # 配置文件目录
            self.default_config: str = os.path.join(self.config_dir, 'default.yaml')     # 默认配置文件路径
            self.user_config: str = os.path.join(self.config_dir, 'config.yaml')         # 用户配置文件路径
            self.config_data: dict = {}                                                  # 存储合并后的配置数据

    def load_config(self) -> Dict[str, Any]:

        """加载并合并配置文件。

        首先加载默认配置文件，然后如果存在用户配置文件，
        则使用用户配置覆盖默认配置中的相应项。

        Returns:
            self.config_data
            Dict[str, Any]: 合并后的配置数据字典
        """

        try:
            # 检查用户配置文件是否存在,存在就加载用户配置,不存在就加载默认配置
            if os.path.exists(self.user_config):
                # 加载用户配置
                with open(self.user_config, 'r', encoding='utf-8') as f:
                    self.config_data = yaml.safe_load(f)
            else:
                # 加载默认配置
                with open(self.default_config, 'r', encoding='utf-8') as f:
                    self.config_data = yaml.safe_load(f)
            return self.config_data
        except FileNotFoundError as e:
            # 配置文件都未找到
            print(f"错误: 配置文件 {self.user_config} 或 {self.default_config} 不存在，请检查路径。")
            return {}    # 返回空字典


    # 列出配置文件
    def list_config(self):
        config_path: str = self.config_dir
        config_files: list = os.listdir(config_path)
        i: int = 1
        print("=== 配置文件 ===")
        for file in config_files:
            if file.endswith('.yaml'):
                print(f"{i}. {file}")
                i += 1


    # 修改配置文件
    def set_config(self) -> None:
        """交互式修改配置
        允许用户逐行查看配置项，并可以选择性地修改值
        按回车跳过当前配置项，输入新值则更新配置
        """
        # 加载当前配置
        current_config = self.load_config()
        
        # 定义要显示的配置项
        display_keys = ['model_provider', 'model', 'base_url', 'api_key', 'max_token', 'temperature']
        
        print("=== 当前配置项 ===")
        print("(直接回车跳过，输入新值进行修改)")
        
        # 逐行显示并允许修改
        for key in display_keys:
            if key in current_config:
                current_value = current_config[key]
                print(f"\n当前 {key}: {current_value}")
                new_value = input(f"新的 {key} (回车跳过): ").strip()
                
                # 如果用户输入了新值，则更新配置
                if new_value:
                    current_config[key] = new_value
        
        # 保存修改后的配置到用户配置文件
        try:
            with open(self.user_config, 'w', encoding='utf-8') as f:
                yaml.safe_dump(current_config, f, allow_unicode=True)
            print("\n配置已更新并保存")
        except Exception as e:
            print(f"\n保存配置时出错: {e}")