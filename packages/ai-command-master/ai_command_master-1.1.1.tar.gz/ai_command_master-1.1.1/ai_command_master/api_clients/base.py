from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseAPIClient(ABC):
    """API客户端基础接口类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化客户端
        Args:
            config: 配置参数字典
        """
        self.config = config
        self.client = None
        self._init_client()
    
    @abstractmethod
    def _init_client(self) -> None:
        """初始化具体的API客户端实例"""
        pass

    @abstractmethod
    def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """
        聊天完成接口
        Args:
            messages: 消息列表，每个消息包含 role 和 content
        Returns:
            str: AI响应的文本
        """
        pass

    def close(self) -> None:
        """关闭并清理客户端资源"""
        if self.client:
            self.client = None