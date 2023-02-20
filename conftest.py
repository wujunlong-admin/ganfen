import pytest
import datetime
import random
import requests
from option_yaml.get_yaml_data import read_yaml_data

url = read_yaml_data()[0]["ApiHost"]


@pytest.fixture(scope="class")
def basic_data():
    skuCode = datetime.datetime.now().strftime("%Y%m%d%H%M")
    containerSpecCode = "900345" + str(random.randint(1, 1000))
    data = [{
        "updateFlag": "ADD",
        "skuCode": skuCode,
        "skuName": "海澜之家",
        "skuDesc": "小个子/甜美",
        "skuType": "衣服",
        "primaryCategory": "男装",
        "secondaryCategory": "黑色",
        "minorCategory": "XXL",
        "validityPeriod": 366,
        "status": "OPEN",
        "packageWeight": 0.3,
        "packageAmount": 12,
        "containerSpecCode": containerSpecCode,
        "containerSpecName": "元箱",
        "length": 200,
        "width": 90,
        "height": 40,
        "fullPalletNum": 12,
        "measureUnit": "件",
        "packageUnit": "箱",
        "containerSpecType": "ORIGINAL",
        "maxWeight": 12,
        "maxHeight": 40,
        "weight": 0.4
    }]
    requests.post(url + "wes-engine/skus", json=data)
    return containerSpecCode, skuCode



# 该方法主要用于处理控制台参数编码问题
def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
