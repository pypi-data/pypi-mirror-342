"""
ModelSafety SDK 异常模块
"""

from typing import Optional, Any


class ModelSafetyError(Exception):
    """ModelSafety SDK的基础异常类"""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        
    def __str__(self) -> str:
        return self.message


class APIError(ModelSafetyError):
    """API调用错误"""
    
    def __init__(self, message: str, http_status: Optional[int] = None, response: Optional[Any] = None):
        self.http_status = http_status
        self.response = response
        super().__init__(message)


class RateLimitError(APIError):
    """API请求速率限制错误"""
    pass


class ServerError(APIError):
    """服务器错误"""
    pass


class ConnectionError(ModelSafetyError):
    """网络连接错误"""
    pass 