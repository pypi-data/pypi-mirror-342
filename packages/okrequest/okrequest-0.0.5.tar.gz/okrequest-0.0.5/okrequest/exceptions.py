class RequestException(Exception):
    """所有异常的基类"""
    pass

class HTTPError(RequestException):
    """HTTP 错误"""
    def __init__(self, message, response=None):
        super().__init__(message)
        self.response = response

class ConnectionError(RequestException):
    """连接错误"""
    pass

class Timeout(RequestException):
    """请求超时"""
    pass 