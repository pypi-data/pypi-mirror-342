"""
ModelSafety SDK 客户端
"""

import os
import json
import requests
from urllib.parse import urljoin
from typing import Dict, List, Union, Optional, Any
import random

from .exceptions import (
    ModelSafetyError, 
    APIError, 
    RateLimitError, 
    ServerError, 
    ConnectionError
)

class ModelSafetyClient:
    """
    ModelSafety API 客户端，提供对大模型观测评估平台的所有功能访问
    """
    
    def __init__(
        self, 
        base_url: str = "http://starvii.tpddns.cn:9004",
        api_key: Optional[str] = None  # 保留参数但不使用，向后兼容
    ):
        """
        初始化ModelSafety客户端
        
        Args:
            base_url: API服务器地址，默认为http://starvii.tpddns.cn:9004
            api_key: 为了向后兼容保留的参数，但不再使用
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"modelsafety-python-sdk/0.1.0"
        })
    
    def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None, 
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        stream: bool = False
    ) -> Any:
        """发送请求到API并处理响应"""
        url = urljoin(self.base_url, endpoint)
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, stream=stream)
            elif method.upper() == "POST":
                if files:
                    # 文件上传请求不设置Content-Type，由requests自动设置
                    headers = self.session.headers.copy()
                    if "Content-Type" in headers:
                        del headers["Content-Type"]
                    response = self.session.post(url, params=params, json=data, files=files, headers=headers)
                else:
                    response = self.session.post(url, params=params, json=data)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            # 处理不同状态码
            if response.status_code == 429:
                raise RateLimitError("API请求次数超限", http_status=response.status_code)
            elif 400 <= response.status_code < 500:
                try:
                    error_data = response.json()
                    message = error_data.get("message", "请求出错")
                except ValueError:
                    message = "请求出错"
                raise APIError(message, http_status=response.status_code, response=response)
            elif response.status_code >= 500:
                raise ServerError("服务器错误", http_status=response.status_code)
            
            # 文件下载
            if stream:
                return response
            
            # 解析JSON响应
            try:
                result = response.json()
                # API返回错误信息
                if not result.get("success", True):
                    raise APIError(result.get("message", "API调用失败"), response=result)
                return result
            except ValueError:
                return response.content
                
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"网络连接错误: {str(e)}")
    
    # ==================== 题库管理 API ====================
    

    def generate_questions_directly(self, data) -> Dict:
        """
        
        Args:
            data: 请求数据
            
        Returns:
            API响应结果，包含生成的题目列表
        """
        
        result = self._request("POST", "/api/questions/generate", data=data)
        print("题库生成结果：",result)
        return result
    


    def transform_questions_directly(self, data) -> Dict:
        """
        直接变换题目
        
        Args:
            data: 请求数据
            
        Returns:
            API响应结果，包含变形后的题目
        """
       
        
        result = self._request("POST", "/api/questions/transform", data=data)
        print("题目变形结果：",result)
        return result        

    # ==================== 模型测试与审核 API ====================

    def audit_model_directly(self, data: Dict) -> Dict:
        """
        直接审核模型响应
        
        Returns:
            API响应结果
        """

        result = self._request("POST", "/api/audit/test-models", data=data)
        print("模型审核结果：",result)
        return result


    
