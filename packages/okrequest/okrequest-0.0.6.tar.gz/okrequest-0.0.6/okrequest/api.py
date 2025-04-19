from .sessions import Session

def request(method, url, **kwargs):
    """发送 HTTP 请求
    
    :param method: HTTP 方法
    :param url: URL
    :param kwargs: 其他参数，与 requests 库兼容
    :return: Response 对象
    """
    with Session() as session:
        return session.request(method=method, url=url, **kwargs)

def get(url, params=None, **kwargs):
    """发送 GET 请求
    
    :param url: URL
    :param params: URL 参数
    :param kwargs: 其他参数，与 requests 库兼容
    :return: Response 对象
    """
    kwargs.setdefault('allow_redirects', True)
    return request('get', url, params=params, **kwargs)

def post(url, data=None, json=None, **kwargs):
    """发送 POST 请求
    
    :param url: URL
    :param data: 表单数据
    :param json: JSON 数据
    :param kwargs: 其他参数，与 requests 库兼容
    :return: Response 对象
    """
    return request('post', url, data=data, json=json, **kwargs)

def put(url, data=None, **kwargs):
    """发送 PUT 请求
    
    :param url: URL
    :param data: 请求数据
    :param kwargs: 其他参数，与 requests 库兼容
    :return: Response 对象
    """
    return request('put', url, data=data, **kwargs)

def delete(url, **kwargs):
    """发送 DELETE 请求
    
    :param url: URL
    :param kwargs: 其他参数，与 requests 库兼容
    :return: Response 对象
    """
    return request('delete', url, **kwargs) 


