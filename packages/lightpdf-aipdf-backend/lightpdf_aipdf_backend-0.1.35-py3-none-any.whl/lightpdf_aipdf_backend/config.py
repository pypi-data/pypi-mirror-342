import os
from typing import Dict, Any

class Config:
    """应用配置类"""
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # 模型价格配置
    MODEL_PRICES: Dict[str, Dict[str, Any]] = {
        'gpt-4o-mini': {
            'input': 0.150,    # 输入价格
            'output': 0.600,   # 输出价格
            'cached': 0.075,   # 缓存价格
            'currency': '$',    # 美元
            'divisor': 1000000  # 每百万token
        },
        'gpt-4.1-nano': {
            'input': 0.10,     # 输入价格 ($0.10 per 1M tokens)
            'output': 0.40,    # 输出价格 ($0.40 per 1M tokens)
            'cached': 0.025,   # 缓存价格 ($0.025 per 1M tokens)
            'currency': '$',    # 美元
            'divisor': 1000000  # 每百万token
        },
        'qwen-max': {
            'input': 0.0024,   # 输入价格
            'output': 0.0096,  # 输出价格
            'currency': '¥',    # 人民币
            'divisor': 1000     # 每千token
        },
        'qwen-plus': {
            'input': 0.0008,   # 输入价格
            'output': 0.002,   # 输出价格
            'currency': '¥',    # 人民币
            'divisor': 1000     # 每千token
        },
        'qwen-turbo': {
            'input': 0.0003,   # 输入价格
            'output': 0.0006,  # 输出价格
            'currency': '¥',    # 人民币
            'divisor': 1000     # 每千token
        },
        'qwen-long': {
            'input': 0.0005,   # 输入价格
            'output': 0.002,   # 输出价格
            'currency': '¥',    # 人民币
            'divisor': 1000     # 每千token
        }
    }
    
    @classmethod
    def validate(cls):
        """验证关键配置项"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("Missing OpenAI API Key")
            
    @classmethod
    def get_model_price(cls, model_name: str) -> Dict[str, Any]:
        """获取指定模型的价格配置
        
        Args:
            model_name: 模型名称
            
        Returns:
            Dict[str, Any]: 价格配置信息
        """
        return cls.MODEL_PRICES.get(model_name, cls.MODEL_PRICES['gpt-4o-mini']) 