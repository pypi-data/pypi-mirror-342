from openai import OpenAI
from typing import Dict, List
from .base import BaseAPIClient

class MoonShotClient(BaseAPIClient):
    """MoonShot API 客户端实现"""
    
    def _init_client(self) -> None:
        """初始化 MoonShot 客户端"""
        self.client = OpenAI(
            api_key=self.config['api_key'],
            base_url=self.config['base_url']
        )

    def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """
        调用 MoonShot 的聊天接口
        Args:
            messages: 消息列表
        Returns:
            str: AI 响应的文本
        """
        try:
            response = self.client.chat.completions.create(
                model=self.config['model'],
                messages=messages,
                stream=False,
                temperature=self.config.get('temperature', 0),
                max_tokens=self.config.get('max_tokens', 2000),
                response_format={'type': 'json_object'}
            )
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = f"MoonShot API 调用失败: {str(e)}"
            raise Exception(error_msg)

    def close(self) -> None:
        """清理资源"""
        super().close()