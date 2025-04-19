import base64
import json

class Response:
    """HTTP 响应对象，类似于 requests.Response"""
    
    def __init__(self, data):
        self.status_code = data.get('status_code', 0)
        self.headers = data.get('headers', {})
        self._content = data.get('content', b'')
        if isinstance(self._content, str): #这里的值是base64编码的，解码
            self._content = base64.b64decode(self._content)
            # self._content = self._content.decode('utf-8')
            
        # if isinstance(self._content, bytes):
        #     self._content = base64.b64decode(self._content)
            
        self.url = data.get('url', '')
        self.elapsed = data.get('elapsed', 0)
        self._text = None
        self._json = None
        self.cookies = data.get('cookies', [])
    
    @property
    def content(self):
        """返回响应内容的字节表示"""
        return self._content
    
    @property
    def text(self):
        """返回响应内容的文本表示"""
        if self._text is None:
            self._text = self._content.decode('utf-8')
        return self._text
    
    def json(self):
        """解析 JSON 响应内容"""
        if self._json is None:
            self._json = json.loads(self.text)
        return self._json
    
    def raise_for_status(self):
        """如果响应状态码表示 HTTP 错误，则引发异常"""
        if 400 <= self.status_code < 600:
            from .exceptions import HTTPError
            raise HTTPError(f"HTTP 错误 {self.status_code}", response=self)
    
    def __repr__(self):
        return f"<Response [{self.status_code}]>" 