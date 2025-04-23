"""系统信息模块
该模块负责收集和提供系统环境信息，包括：
- 操作系统类型和版本
- 用户信息（用户名）
- 系统路径（用户目录、当前工作目录）
"""
import os
import platform
import getpass


class SystemInfo:
    """系统信息收集类
    
    用于收集和存储当前系统环境的相关信息，为应用程序提供运行环境上下文。
    
    Attributes:
        system_info (dict): 存储系统信息的字典，包含以下键：
            - 系统: 操作系统类型
            - 系统版本: 操作系统版本号
            - 用户名: 当前用户名
            - 用户家目录: 用户主目录的绝对路径
            - 当前工作目录: 程序运行时的工作目录
    """
    def __init__(self):
        """初始化系统信息收集器
        
        在实例化时自动收集所有系统相关信息
        """
        self.system_info: dict = {
            '系统': platform.system(),
            '系统版本': platform.version(),
            '用户名': getpass.getuser(),
            '用户家目录': os.path.expanduser('~'),
            '当前工作目录': os.getcwd()
        }
    
    def get_system_info(self) -> dict:
        """获取系统信息
        
        Returns:
            dict: 包含所有系统信息的字典
        """
        return self.system_info
