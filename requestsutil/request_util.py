# 导入requests包
import requests
import json


class RequestsUtil:
    def request_res(self, url, data, method='GET', header=None):
        # 由于data参数可能不是json所以需要进行转换
        # change_data = json.loads(data)
        if method.upper() == 'GET':
            return requests.get(url, data)
        elif method.upper() == 'POST':
            return requests.post(url, json=data, headers=header)
        else:
            return '请求方式或参数错误！'
