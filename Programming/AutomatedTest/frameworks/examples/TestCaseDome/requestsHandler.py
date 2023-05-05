# 需要先执行 pip install requests 命令 
import requests
class RequestsHandler:
    def __init__(self):
        """session管理器"""
        self.session = requests.session()
    def visit(self, method, url, 
              params = None, 
              data= None, 
              json= None, 
              headers= None):
        result = self.session.request(method,url,
                                    params=params,
                                    data=data,
                                    json=json,
                                    headers=headers)
        try:
            # 返回 json 结果
            return result.json()
        except Exception:
            return 'not json'
    def close_session(self):
        self.session.close()
