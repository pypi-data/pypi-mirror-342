import ctypes
import platform
import os

from okrequest.sessions import Session

# 修复导入语句
from .api import get, post, put, delete, request
from .exceptions import RequestException, Timeout, ConnectionError

# # 动态加载Go编译的库
# def load_library():
#     system = platform.system().lower()
#     lib_path = os.path.join(os.path.dirname(__file__), 'libs')
    
#     if system == 'windows':
#         lib_name = 'httpclient.dll'
#     elif system == 'linux':
#         lib_name = 'httpclient.so'
#     else:
#         raise OSError("Unsupported platform")
    
#     return ctypes.CDLL(os.path.join(lib_path, lib_name))

# lib = load_library()

# 模拟requests的API
def request(method, url, **kwargs):
    with Session() as s:
        return s.request(method, url, **kwargs)

def get(url, **kwargs):
    return request('GET', url, **kwargs)

def post(url, data=None, json=None, **kwargs):
    return request('POST', url, data=data, json=json, **kwargs)

# 其他HTTP方法
def put(url, data=None, **kwargs):
    return request('PUT', url, data=data, **kwargs)

def delete(url, **kwargs):
    return request('DELETE', url, **kwargs)

__version__ = "0.1.0"