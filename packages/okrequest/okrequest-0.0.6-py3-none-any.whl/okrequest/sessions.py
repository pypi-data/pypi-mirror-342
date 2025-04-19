import base64
import json
import ctypes
from urllib.parse import urlencode
import asyncio
import threading
from pathlib import Path
import platform
import os

from .exceptions import RequestException
from .models import Response

# 根据平台加载不同的库文件
system = platform.system()
lib_path = os.path.join(os.path.dirname(__file__), 'libs')

if system == "Windows":
    lib_path = lib_path + "/httpclient.dll"
    lib = ctypes.CDLL(lib_path)
elif system == "Linux":
    lib_path = lib_path + "/httpclient.so"
    lib = ctypes.CDLL(lib_path)
else:
    raise RuntimeError(f"不支持的操作系统: {system}")

# 设置函数参数和返回类型
lib.Get.argtypes = [ctypes.c_char_p, ctypes.c_int]
lib.Get.restype = ctypes.c_char_p

lib.Post.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
lib.Post.restype = ctypes.c_char_p

lib.PostJSON.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
lib.PostJSON.restype = ctypes.c_char_p

lib.RequestWithOptions.argtypes = [ctypes.c_char_p]
lib.RequestWithOptions.restype = ctypes.c_char_p

class Session:
    """会话对象，类似于 requests.Session"""
    
    def __init__(self):
        self.headers = {}
        self.cookies = {}
        self.timeout = 30
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass
    
    def request(self, method, url, **kwargs):
        """发送请求
        
        :param method: HTTP 方法
        :param url: URL
        :param kwargs: 其他参数，与 requests 库兼容
        :return: Response 对象
        
        """
        # 合并 headers
        headers = {}
        headers.update(self.headers)
        headers.update(kwargs.get('headers', {}))
        
        # 处理超时
        timeout = kwargs.get('timeout', self.timeout)
        
        # 处理 params
        params = kwargs.get('params')
        if params:
            if '?' in url:
                url = f"{url}&{urlencode(params)}"
            else:
                url = f"{url}?{urlencode(params)}"
        
        # 处理不同类型的请求体
        body = b''
        if kwargs.get('json') is not None:
            headers['Content-Type'] = 'application/json'
            body = json.dumps(kwargs['json']).encode('utf-8')
        elif kwargs.get('data') is not None:
            data = kwargs['data']
            if isinstance(data, dict):
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                body = urlencode(data).encode('utf-8')
            else:
                body = data if isinstance(data, bytes) else str(data).encode('utf-8')
        
        
        proxy_url = ""
        proxies = kwargs.get('proxies')
        if proxies:
            proxy_url = proxies.get('http') or proxies.get('https')
            
        #cookiea
        cookies = kwargs.get('cookies')
        if cookies:
            cookies_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
            headers['cookie'] = cookies_str

        #body要转为base64
        body = base64.b64encode(body).decode('utf-8')
        
        impersonate = kwargs.get('impersonate')
        
        options = {
            'method': method.upper(),
            'url': url,
            'headers': headers,
            'body': body,# body.decode('utf-8') if isinstance(body, bytes) else body,
            'timeout': timeout,
            'proxy_url': proxy_url,
            "impersonate":impersonate
            
        }

        options_json = json.dumps(options)
        headers_json = json.dumps(headers)
        
        # print(options_json)
        # print(headers_json)
        
        result = lib.RequestWithOptions(options_json.encode('utf-8'))
        result_str = ctypes.string_at(result).decode('utf-8')
        
        # 解析响应
        result_json = json.loads(result_str)
        if 'error' in result_json:
            raise RequestException(result_json['error'])
        
        return Response(result_json)
    
    async def request_async(self, method, url, **kwargs):
        """异步发送请求
        
        :param method: HTTP 方法
        :param url: URL
        :param kwargs: 其他参数，与 requests 库兼容
        :return: Response 对象
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, lambda: self.request(method, url, **kwargs)
        )
    
    def get(self, url, **kwargs):
        """发送 GET 请求"""
        kwargs.setdefault('allow_redirects', True)
        return self.request('get', url, **kwargs)
    
    async def get_async(self, url, **kwargs):
        """异步发送 GET 请求"""
        kwargs.setdefault('allow_redirects', True)
        return await self.request_async('get', url, **kwargs)
    
    def post(self, url, data=None, json=None, **kwargs):
        """发送 POST 请求"""
        return self.request('post', url, data=data, json=json, **kwargs)
    
    async def post_async(self, url, data=None, json=None, **kwargs):
        """异步发送 POST 请求"""
        return await self.request_async('post', url, data=data, json=json, **kwargs)
    
    def put(self, url, data=None, **kwargs):
        """发送 PUT 请求"""
        return self.request('put', url, data=data, **kwargs)
    
    async def put_async(self, url, data=None, **kwargs):
        """异步发送 PUT 请求"""
        return await self.request_async('put', url, data=data, **kwargs)
    
    def delete(self, url, **kwargs):
        """发送 DELETE 请求"""
        return self.request('delete', url, **kwargs)
    
    async def delete_async(self, url, **kwargs):
        """异步发送 DELETE 请求"""
        return await self.request_async('delete', url, **kwargs) 