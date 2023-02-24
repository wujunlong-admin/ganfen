import datetime
import random
import time

import requests
from API.wesApi import TesApi, WesApi
from option_yaml.get_yaml_data import read_yaml_data
from log.get_log import get_log

url = read_yaml_data()[0]["ApiHost"]
logger = get_log('input_box.log')


class TestCase:
    def basic_data(self, SpecCode=None):
        if SpecCode == None:
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
                "length": 210,
                "width": 95,
                "height": 42,
                "fullPalletNum": 12,
                "measureUnit": "件",
                "packageUnit": "箱",
                "containerSpecType": "ORIGINAL",
                "maxWeight": 12,
                "maxHeight": 40,
                "weight": 0.4
            }]
            res = requests.post(url + "wes-engine/skus", json=data)
            if res.json()['returnCode'] == 10000007:
                return '容器规格中已存在相同规格容器'
        else:
            skuCode = datetime.datetime.now().strftime("%Y%m%d%H%M")
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
                "containerSpecCode": SpecCode,
                "containerSpecName": "元箱",
                "length": 210,
                "width": 95,
                "height": 42,
                "fullPalletNum": 12,
                "measureUnit": "件",
                "packageUnit": "箱",
                "containerSpecType": "ORIGINAL",
                "maxWeight": 12,
                "maxHeight": 40,
                "weight": 0.4
            }]
            res = requests.post(url + "wes-engine/skus", json=data)
            if res.json()['returnCode'] == 10000007:
                return '容器规格中已存在相同规格容器'
            return res.json()

    def for_inpot(self):
        basic = WesApi().basic_data()  # ('900345277', '202302211654')
        containerSpecCode = basic[0]
        skuCode = basic[1]
        all_for_num = 1
        while all_for_num <= 6:
            if all_for_num == 1:
                a = WesApi().inpot_task(containerSpecCode, 120, skuCode)
                logger.info('入库托盘A1为：' + a)
                while True:
                    box_postion = TesApi().select_box_Postion(a)
                    if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                        all_for_num += 1
                        break
            elif all_for_num == 2:
                b = WesApi().inpot_task('900345277', 48, '202302211654')
                logger.info('入库托盘A2为：' + b)
                while True:
                    box_postion = TesApi().select_box_Postion(b)
                    if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                        all_for_num += 1
                        break
            elif all_for_num == 3:
                c = WesApi().inpot_task('900345277', 72, '202302211654')
                logger.info('入库托盘A3为：' + c)
                while True:
                    box_postion = TesApi().select_box_Postion(c)
                    if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                        all_for_num += 1
                        break
            elif all_for_num == 4:
                d = WesApi().inpot_task('900345277', 48, '202302211654')
                logger.info('入库托盘A4为：' + d)
                while True:
                    box_postion = TesApi().select_box_Postion(d)
                    if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                        all_for_num += 1
                        break
            elif all_for_num == 5:
                e = WesApi().inpot_task('900345277', 48, '202302211654')
                logger.info('入库托盘A5为：' + e)
                while True:
                    box_postion = TesApi().select_box_Postion(e)
                    if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                        all_for_num += 1
                        break
            elif all_for_num == 6:
                f = WesApi().inpot_task('900345277', 24, '202302211654')
                print(f)


if __name__ == '__main__':
    # a = TestCase().basic_data(900345277)
    # print(a)
    # print(datetime.datetime.now().strftime("%Y%m%d%H%M"))
    # print(time.time())
    # import calendar
    # print(calendar.timegm(time.gmtime())*1000)
    a = TesApi().re_car()
    print(a)
