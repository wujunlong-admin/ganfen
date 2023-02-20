import random
import datetime
import requests
from sql_data.sqlutil import SqlUtil
from requestsutil.request_util import RequestsUtil
from option_yaml.get_yaml_data import read_yaml_data

url = read_yaml_data()[0]["ApiHost"]


class WesApi:
    # 物料下发接口
    def basic_data(self):
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

    # 入库/反库接口
    # 包含箱码接口
    def inpot_task_code(self):
        orderTaskId = datetime.datetime.now().strftime("%Y%m%d%H%M")
        containerCode = '90000' + str(random.randint(1, 1000))
        boxCode = '800000' + str(random.randint(1, 1000))
        data = {
            "taskList": [{
                "regionCode": "ps",
                "containerCode": containerCode,
                "originStation": "ST-Pallet-303",
                "orderTaskId": orderTaskId,
                "orderType": "001",
                "inPosition": True,
                "ext": {
                    "register": True,
                    "unlock": "START_INBOUND"
                },
                "container": {
                    "containerCode": containerCode,
                    "containerType": "PALLET",
                    "containerSpecCode": "c1600691636949",
                    "containers": [{
                        "containerCode": boxCode,
                        "containerType": "ORIGINAL",
                        "containerSpecCode": "90034537",
                        "stocks": [{
                            "containerSpecCode": "90034537",
                            "qty": "20",
                            "skuCode": "202302171643",
                            "skuName": "海澜之家",
                            "owner": "test",
                            "qualityState": "QUALIFIED",
                            "lot": "0301",
                            "status": "ON_SHELF",
                            "packageAmount": "20"
                        }]
                    }]
                }
            }]
        }
        res = requests.post(url + "wes-engine/task:moveIn", json=data)
        print(res.json())
        if res.json()['returnMsg'] == 'success' and res.json()['returnUserMsg'] == '成功':
            return containerCode, boxCode
        return res.json()

    # 无箱码接口
    def inpot_task(self):
        skuCode = datetime.datetime.now().strftime("%Y%m%d%H%M")
        containerCode = '90000' + str(random.randint(1, 1000))
        data = {
            "taskList": [{
                "regionCode": "ps",
                "containerCode": containerCode,
                "originStation": "ST-Pallet-303",
                "orderTaskId": skuCode,
                "orderType": "001",
                "inPosition": True,
                "ext": {
                    "register": True,
                    "unlock": "START_INBOUND"
                },
                "container": {
                    "containerCode": containerCode,
                    "containerType": "PALLET",
                    "containerSpecCode": "c1600691636949",
                    "stocks": [{
                        "containerSpecCode": "90034537",
                        "qty": "20",
                        "skuCode": "202302171643",
                        "skuName": "海澜之家	",
                        "owner": "test",
                        "qualityState": "QUALIFIED",
                        "lot": "0301",
                        "status": "ON_SHELF",
                        "packageAmount": "20"
                    }]
                }
            }]
        }
        res = requests.post(url + "wes-engine/task:moveIn", json=data)
        if res.json()['returnMsg'] == 'success' and res.json()['returnUserMsg'] == '成功':
            return containerCode
        return res.json()

    # 包含箱码接口-混sku
    def inpot_task_code_sku(self):
        skuCode = datetime.datetime.now().strftime("%Y%m%d%H%M")
        containerCode = '90000' + str(random.randint(1, 1000))
        boxCode = '800000' + str(random.randint(1, 1000))
        data = {
            "taskList": [{
                "regionCode": "ps",
                "containerCode": containerCode,
                "originStation": "ST-Pallet-303",
                "orderTaskId": skuCode,
                "orderType": "001",
                "inPosition": True,
                "ext": {
                    "register": True,
                    "unlock": "START_INBOUND"
                },
                "container": {
                    "containerCode": containerCode,
                    "containerType": "PALLET",
                    "containerSpecCode": "c1600691636949",
                    "containers": [{
                        "containerCode": boxCode,
                        "containerType": "ORIGINAL",
                        "containerSpecCode": "90034537",
                        "stocks": [{
                            "containerSpecCode": "90034537",
                            "qty": "20",
                            "skuCode": "202302171643",
                            "skuName": "海澜之家",
                            "owner": "test",
                            "qualityState": "QUALIFIED",
                            "lot": "0301",
                            "status": "ON_SHELF",
                            "packageAmount": "20"
                        }, {
                            "containerSpecCode": "90034593",
                            "qty": "20",
                            "skuCode": "202302171642",
                            "skuName": "海澜之家",
                            "owner": "test",
                            "qualityState": "QUALIFIED",
                            "lot": "0301",
                            "status": "ON_SHELF",
                            "packageAmount": "20"
                        }]
                    }]
                }
            }]
        }
        res = requests.post(url + "wes-engine/task:moveIn", json=data)
        if res.json()['returnMsg'] == 'success' and res.json()['returnUserMsg'] == '成功':
            return containerCode, boxCode
        return res.json()

    # 无箱码接口-混sku
    def inpot_task_sku(self):
        skuCode = datetime.datetime.now().strftime("%Y%m%d%H%M")
        containerCode = '90000' + str(random.randint(1, 1000))
        data = {
            "taskList": [{
                "regionCode": "ps",
                "containerCode": containerCode,
                "originStation": "ST-Pallet-303",
                "orderTaskId": skuCode,
                "orderType": "001",
                "inPosition": True,
                "ext": {
                    "register": True,
                    "unlock": "START_INBOUND"
                },
                "container": {
                    "containerCode": containerCode,
                    "containerType": "PALLET",
                    "containerSpecCode": "c1600691636949",
                    "stocks": [{
                        "containerSpecCode": "90034537",
                        "qty": "20",
                        "skuCode": "202302171643",
                        "skuName": "海澜之家	",
                        "owner": "test",
                        "qualityState": "QUALIFIED",
                        "lot": "0301",
                        "status": "ON_SHELF",
                        "packageAmount": "20"
                    }, {
                        "containerSpecCode": "90034593",
                        "qty": "20",
                        "skuCode": "202302171642",
                        "skuName": "海澜之家",
                        "owner": "test",
                        "qualityState": "QUALIFIED",
                        "lot": "0301",
                        "status": "ON_SHELF",
                        "packageAmount": "20"
                    }]
                }
            }]
        }
        res = requests.post(url + "wes-engine/task:moveIn", json=data)
        if res.json()['returnMsg'] == 'success' and res.json()['returnUserMsg'] == '成功':
            return containerCode
        return res.json()


class TesApi:
    # 查询电量为0小车
    def select_car(self):
        sql = """select robot_id, current_point from tes.robot where region_code = 'ps' 
        and  ext like '%"ucPower":0%'"""
        res_sql = SqlUtil().connect_data_tes(sql)
        return res_sql

    # 小车离线
    def car_off(self, car_num):
        method = 'post'
        url = read_yaml_data()[0]["ApiHost"]
        data = {
            "robotIDs": car_num
        }
        res = RequestsUtil().request_res(url + "tes/apiv2/solo/offlineRobot", data, method)
        return res.json()

    # 小车注册
    def car_on(self, car_num, node):
        url = read_yaml_data()[0]["ApiHost"]
        data = {
            "robotInfos": f"""[{{"robotID": "{car_num}", "deviceType": "268", "node": "{node}", "power": 90}}]"""
        }

        requests.post(url + "tes/apiv2/solo/registerRobot", data=data)
        return car_num

    def re_car(self):
        all_car = TesApi().select_car()
        car_all_num = []
        if all_car != []:
            for i in range(len(all_car)):
                TesApi().car_off(all_car[i]['robot_id'])
                car_num = TesApi().car_on(all_car[i]['robot_id'], all_car[i]['current_point'])
                car_all_num.append(car_num)
            return car_all_num
        return '当前无电量为0的小车'


if __name__ == '__main__':
    # 主数据下发（物料管理）
    # a = WesApi().basic_data()
    # print(a)

    # 有箱码下发入库任务
    a = WesApi().inpot_task_code()
    print(a)

    # 有箱码下发混sku入库任务
    # a = WesApi().inpot_task_code_sku()
    # print(a)

    # 无箱码下发入库任务
    # a = WesApi().inpot_task()
    # print(a)

    # 无箱码下发混sku入库任务
    # a = WesApi().inpot_task_sku()
    # print(a)

    # 小车重新注册
    # a = TesApi().re_car()
    # print(a)
