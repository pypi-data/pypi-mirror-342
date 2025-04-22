
from typing import Dict, Any
from .base import BaseAPIClient
from .deepseek import DeepSeekClient
from .moonshot import MoonShotClient

class APIClientFactory:
    """API客户端工厂类"""
    
    # 支持的服务商映射
    _providers = {
        'deepseek': DeepSeekClient,
        'moonshot': MoonShotClient,
        # 其他服务商的实现类...
    }
    
    @classmethod
    def get_api_client(cls, provider: str, config: Dict[str, Any]) -> BaseAPIClient:
        """
        获取API客户端实例
        
        Args:
            provider: 服务商名称
            config: 配置参数
            
        Returns:
            BaseAPIClient: API客户端实例
        """
        provider = provider.lower()    # 转小写找对应模型提供商
        if provider not in cls._providers:
            raise ValueError(f"不支持的服务商: {provider}")
            
        client_class = cls._providers[provider]
        return client_class(config)
