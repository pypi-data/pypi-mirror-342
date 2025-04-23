"""数据格式化处理模块
该模块负责解析和格式化AI模型的响应数据，主要功能包括：
- 解析AI响应的JSON格式数据
- 提取对话类型、风险等级、警告信息等
- 将JSON数据转换为统一的字典格式
"""

import json
from typing import Dict

class DataFormatter:
    """数据格式化处理类
    
    用于处理AI模型返回的JSON格式数据，将其转换为标准的字典数据。
    
    输入格式示例:
        {
            "输出头": {
                "内容类型": "Command",
                "危险提示": {
                    "危险等级": "Low",
                    "具体危险信息": "正常交流,无风险"
                },
                "提示信息": ""
            },
            "输出体": "请提供具体指令需求"
        }
    
    输出格式:
        {
            'conversation_type': 'Command',
            'risk_level': 'Low',
            'warning': '正常交流,无风险',
            'tip': '',
            'content': '请提供具体指令需求'
        }
    """
    
    def __init__(self, input_string: str):
        """初始化数据格式化处理器
        
        Args:
            input_string (str): 需要解析的JSON字符串
        """
        self.input_string = input_string

    def parse(self) -> Dict[str, str]:
        """解析JSON字符串为统一的结构化数据
        
        Returns:
            dict: 包含以下字段的字典：
                - conversation_type: 对话类型 (Command/Text)
                - risk_level: 风险等级 (High/Medium/Low)
                - warning: 风险说明
                - tip: 提示信息
                - content: 主要内容
                
        Raises:
            json.JSONDecodeError: 当输入的字符串不是有效的JSON格式时
            KeyError: 当JSON中缺少必要的字段时
        """
        try:
            # 解析JSON字符串
            data = json.loads(self.input_string)
            
            # 初始化结果字典
            result = {
                'conversation_type': '',
                'risk_level': '',
                'warning': '',
                'tip': '',
                'content': ''
            }
            
            # 提取数据
            header = data['输出头']
            result['conversation_type'] = header['内容类型']
            result['risk_level'] = header['危险提示']['危险等级']
            result['warning'] = header['危险提示']['具体危险信息']
            result['tip'] = header['提示信息']
            result['content'] = data['输出体']
            
            return result
            
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"输入不是有效的JSON格式: {str(e)}", e.doc, e.pos)
        except KeyError as e:
            raise KeyError(f"JSON数据缺少必要字段: {str(e)}")