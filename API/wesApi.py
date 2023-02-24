import calendar
import random
import datetime
import time

import requests
from sql_data.sqlutil import SqlUtil
from requestsutil.request_util import RequestsUtil
from option_yaml.get_yaml_data import read_yaml_data
from log.get_log import get_log

url = read_yaml_data()[0]["ApiHost"]
logger = get_log(str(datetime.datetime.now().date()) + 'log.log')


class WesApi:
    # 物料下发接口
    def basic_data(self, containerCode=None, length=None, width=None, height=None):
        if containerCode == None:
            skuCode = datetime.datetime.now().strftime("%Y%m%d%H%M")
            containerSpecCode = "900345" + str(random.randint(1, 1000))
            logger.info(f"容器规格：{containerSpecCode}，sku为：{skuCode}")
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
            res = requests.post(url + "wes-engine/skus", json=data)
            if res.json()['returnCode'] == 10000007:
                return '容器规格中已存在相同规格容器' + res.json()
            # return containerSpecCode, skuCode
            return containerSpecCode, skuCode
        else:
            skuCode = datetime.datetime.now().strftime("%Y%m%d%H%M")
            logger.info(f"sku为：{skuCode}")
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
                "containerSpecCode": containerCode,
                "containerSpecName": "元箱",
                "length": length / 10,
                "width": width / 10,
                "height": height / 10,
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
                return '容器规格中已存在相同规格容器', res.json()
            # return containerSpecCode, skuCode
            return skuCode

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
                            "qty": "12",
                            "skuCode": "202302171643",
                            "skuName": "海澜之家",
                            "owner": "test02",
                            "qualityState": "QUALIFIED",
                            "lot": "0301",
                            "status": "ON_SHELF",
                            "packageAmount": "12",
                            "oddCarton": 0
                        }]
                    }]
                }
            }]
        }
        res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
        if res.json()['returnMsg'] == 'success' and res.json()['returnUserMsg'] == '成功':
            return containerCode, boxCode
        return res.json()

    # 无箱码接口
    def inpot_task(self, containerSpecCode, piece_num, skuCode):
        skuCode1 = datetime.datetime.now().strftime("%Y%m%d%H%M")
        containerCode = '90000' + str(random.randint(1, 1000))
        data = {
            "taskList": [{
                "regionCode": "ps",
                "containerCode": containerCode,
                "originStation": "ST-Pallet-303",
                "orderTaskId": skuCode1,
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
                        "containerSpecCode": containerSpecCode,
                        "qty": piece_num,
                        "skuCode": skuCode,
                        "skuName": "海澜之家	",
                        "owner": "test",
                        "qualityState": "QUALIFIED",
                        "lot": "0301",
                        "status": "ON_SHELF",
                        "packageAmount": "12",
                        "oddCarton": 0
                    }]
                }
            }]
        }
        res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
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
                            "packageAmount": "20",
                            "oddCarton": 0
                        }]
                    }]
                }
            }]
        }
        res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
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
                        "packageAmount": "20",
                        "oddCarton": 0
                    }]
                }
            }]
        }
        res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
        if res.json()['returnMsg'] == 'success' and res.json()['returnUserMsg'] == '成功':
            return containerCode
        return res.json()


class TesApi:
    # 查询电量为0小车
    def select_car(self):
        sql = """select * from tes.robot where region_code = 'ps' 
        and  ext like '%"ucPower":20%'"""
        res_sql = SqlUtil().connect_data_tes(sql)
        return res_sql

    # 查询托盘位置
    def select_box_Postion(self, box):
        sql = f"select position_type, node from tes.frame where frame_id={box}"
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


class TestCase:
    def for_inpot(self, containercode=None, skucode=None, length=None, width=None, height=None):
        logger.info('调用者传入容器规格参数:' + str(containercode) + ",sku参数为：" + str(skucode))
        if containercode != None:
            logger.info('调用者传入容器规格参数:' + str(containercode))
            new_basic_sku = WesApi().basic_data(containercode, length, width,
                                                height)  # ('900345277', '202302211654')
            containerSpecCode = containercode
            skuCode = new_basic_sku
            all_for_num = 1
            while all_for_num <= 7:
                time.sleep(1)
                # 48  批次早入库托盘
                if all_for_num == 1:
                    # a = WesApi().inpot_task(containerSpecCode, 48, skuCode)
                    orderTaskId = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    boxCode = '90000' + str(random.randint(1, 1000))
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": boxCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": orderTaskId,
                            "orderType": "001",
                            "inPosition": True,
                            "ext": {
                                "register": True,
                                "unlock": "START_INBOUND"
                            },
                            "container": {
                                "containerCode": boxCode,
                                "containerType": "PALLET",
                                "containerSpecCode": "c1600691636949",
                                "stocks": [{
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 48,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": datetime.datetime.now().strftime("%Y%m%d%H%M"),
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0,
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        logger.info("批次早入库托盘A1,入库失败！！")
                        return res.json()
                    logger.info('批次早入库托盘A1为：' + boxCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(boxCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 48  生产早入库托盘
                elif all_for_num == 2:
                    # b = WesApi().inpot_task(containerSpecCode, 48, skuCode)
                    skuCode1 = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    containerCode = '90000' + str(random.randint(1, 1000))
                    time.sleep(2)
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": containerCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": skuCode1,
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
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 48,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": "0301",
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0,
                                    "receivingDate": 1642672402000,
                                    "manufacturingDate": 1676865035,
                                    "expirationDate": 1740031232000
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        return logger.info("生产日期早入库托盘A2,入库失败！！")
                    logger.info('生产日期早入库托盘A2为：' + containerCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(containerCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 72 普通入库
                elif all_for_num == 3:
                    c = WesApi().inpot_task(containerSpecCode, 72, skuCode)
                    logger.info('入库托盘A3为：' + c)
                    while True:
                        box_postion = TesApi().select_box_Postion(c)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 120 生产日期晚入库
                elif all_for_num == 4:
                    skuCode1 = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    containerCode = '90000' + str(random.randint(1, 1000))
                    time.sleep(2)
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": containerCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": skuCode1,
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
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 120,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": "0301",
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0,
                                    "receivingDate": 1647788002000,
                                    "manufacturingDate": calendar.timegm(time.gmtime()) * 1000,
                                    "expirationDate": 1740031232000
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        return logger.info("生产日期晚入库托盘A4,入库失败！！")
                    logger.info('生成日期晚入库托盘A4为：' + containerCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(containerCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 48 批次晚入库
                elif all_for_num == 5:
                    # e = WesApi().inpot_task(containerSpecCode, 48, skuCode)
                    skuCode1 = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    containerCode = '90000' + str(random.randint(1, 1000))
                    time.sleep(2)
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": containerCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": skuCode1,
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
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 48,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": datetime.datetime.now().strftime("%Y%m%d%H%M"),
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        return logger.info("批次晚入库托盘A5,入库失败！！")
                    logger.info('批次晚入库托盘A5为：' + containerCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(containerCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 48 生产日期晚入库
                elif all_for_num == 6:
                    # f = WesApi().inpot_task(containerSpecCode, 48, skuCode)
                    skuCode1 = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    containerCode = '90000' + str(random.randint(1, 1000))
                    time.sleep(2)
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": containerCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": skuCode1,
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
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 48,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": "0301",
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0,
                                    "receivingDate": 1647788002000,
                                    "manufacturingDate": calendar.timegm(time.gmtime()) * 1000,
                                    "expirationDate": 1740031232000
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        return logger.info("生产日期晚入库托盘A6,入库失败！！")
                    logger.info('生成日期晚入库托盘A6为：' + containerCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(containerCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 24 普通入库
                elif all_for_num == 7:
                    c = WesApi().inpot_task(containerSpecCode, 24, skuCode)
                    logger.info('入库托盘A7为：' + str(c))
                    while True:
                        box_postion = TesApi().select_box_Postion(c)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
            return '执行完毕'
        elif containercode != None and skucode != None:
            containerSpecCode = containercode
            skuCode = skucode
            all_for_num = 1
            while all_for_num <= 7:
                time.sleep(1)
                # 48  批次早入库托盘
                if all_for_num == 1:
                    # a = WesApi().inpot_task(containerSpecCode, 48, skuCode)
                    orderTaskId = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    boxCode = '90000' + str(random.randint(1, 1000))
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": boxCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": orderTaskId,
                            "orderType": "001",
                            "inPosition": True,
                            "ext": {
                                "register": True,
                                "unlock": "START_INBOUND"
                            },
                            "container": {
                                "containerCode": boxCode,
                                "containerType": "PALLET",
                                "containerSpecCode": "c1600691636949",
                                "stocks": [{
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 48,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": datetime.datetime.now().strftime("%Y%m%d%H%M"),
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0,
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        logger.info("批次早入库托盘A1,入库失败！！")
                        return res.json()
                    logger.info('批次早入库托盘A1为：' + boxCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(boxCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 48  生产早入库托盘
                elif all_for_num == 2:
                    # b = WesApi().inpot_task(containerSpecCode, 48, skuCode)
                    skuCode1 = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    containerCode = '90000' + str(random.randint(1, 1000))
                    time.sleep(2)
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": containerCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": skuCode1,
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
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 48,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": "0301",
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0,
                                    "receivingDate": 1642672402000,
                                    "manufacturingDate": 1676865035,
                                    "expirationDate": 1740031232000
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        return logger.info("生产日期早入库托盘A2,入库失败！！")
                    logger.info('生产日期早入库托盘A2为：' + containerCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(containerCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 72 普通入库
                elif all_for_num == 3:
                    c = WesApi().inpot_task(containerSpecCode, 72, skuCode)
                    logger.info('入库托盘A3为：' + c)
                    while True:
                        box_postion = TesApi().select_box_Postion(c)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 120 生产日期晚入库
                elif all_for_num == 4:
                    skuCode1 = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    containerCode = '90000' + str(random.randint(1, 1000))
                    time.sleep(2)
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": containerCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": skuCode1,
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
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 120,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": "0301",
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0,
                                    "receivingDate": 1647788002000,
                                    "manufacturingDate": calendar.timegm(time.gmtime()) * 1000,
                                    "expirationDate": 1740031232000
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        return logger.info("生产日期晚入库托盘A4,入库失败！！")
                    logger.info('生成日期晚入库托盘A4为：' + containerCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(containerCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 48 批次晚入库
                elif all_for_num == 5:
                    # e = WesApi().inpot_task(containerSpecCode, 48, skuCode)
                    skuCode1 = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    containerCode = '90000' + str(random.randint(1, 1000))
                    time.sleep(2)
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": containerCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": skuCode1,
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
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 48,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": datetime.datetime.now().strftime("%Y%m%d%H%M"),
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        return logger.info("批次晚入库托盘A5,入库失败！！")
                    logger.info('批次晚入库托盘A5为：' + containerCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(containerCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 48 生产日期晚入库
                elif all_for_num == 6:
                    # f = WesApi().inpot_task(containerSpecCode, 48, skuCode)
                    skuCode1 = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    containerCode = '90000' + str(random.randint(1, 1000))
                    time.sleep(2)
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": containerCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": skuCode1,
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
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 48,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": "0301",
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0,
                                    "receivingDate": 1647788002000,
                                    "manufacturingDate": calendar.timegm(time.gmtime()) * 1000,
                                    "expirationDate": 1740031232000
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        return logger.info("生产日期晚入库托盘A6,入库失败！！")
                    logger.info('生成日期晚入库托盘A6为：' + containerCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(containerCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 24 普通入库
                elif all_for_num == 7:
                    c = WesApi().inpot_task(containerSpecCode, 24, skuCode)
                    logger.info('入库托盘A7为：' + c)
                    while True:
                        box_postion = TesApi().select_box_Postion(c)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
            return '执行完毕'
        else:
            new_basic = WesApi().basic_data()  # ('900345277', '202302211654')
            logger.info('调用者传入容器规格参数:' + str(new_basic[0]) + ",sku参数为：" + str(new_basic[1]))
            containerSpecCode = new_basic[0]
            skuCode = new_basic[1]
            all_for_num = 1
            while all_for_num <= 7:
                time.sleep(1)
                # 48  批次早入库托盘
                if all_for_num == 1:
                    # a = WesApi().inpot_task(containerSpecCode, 48, skuCode)
                    orderTaskId = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    boxCode = '90000' + str(random.randint(1, 1000))
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": boxCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": orderTaskId,
                            "orderType": "001",
                            "inPosition": True,
                            "ext": {
                                "register": True,
                                "unlock": "START_INBOUND"
                            },
                            "container": {
                                "containerCode": boxCode,
                                "containerType": "PALLET",
                                "containerSpecCode": "c1600691636949",
                                "stocks": [{
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 48,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": datetime.datetime.now().strftime("%Y%m%d%H%M"),
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0,
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        logger.info("批次早入库托盘A1,入库失败！！")
                        return res.json()
                    logger.info('批次早入库托盘A1为：' + boxCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(boxCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 48  生产早入库托盘
                elif all_for_num == 2:
                    # b = WesApi().inpot_task(containerSpecCode, 48, skuCode)
                    skuCode1 = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    containerCode = '90000' + str(random.randint(1, 1000))
                    time.sleep(2)
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": containerCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": skuCode1,
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
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 48,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": "0301",
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0,
                                    "receivingDate": 1642672402000,
                                    "manufacturingDate": 1676865035,
                                    "expirationDate": 1740031232000
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        return logger.info("生产日期早入库托盘A2,入库失败！！")
                    logger.info('生产日期早入库托盘A2为：' + containerCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(containerCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 72 普通入库
                elif all_for_num == 3:
                    c = WesApi().inpot_task(containerSpecCode, 72, skuCode)
                    logger.info('入库托盘A3为：' + c)
                    while True:
                        box_postion = TesApi().select_box_Postion(c)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 120 生产日期晚入库
                elif all_for_num == 4:
                    skuCode1 = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    containerCode = '90000' + str(random.randint(1, 1000))
                    time.sleep(2)
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": containerCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": skuCode1,
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
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 120,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": "0301",
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0,
                                    "receivingDate": 1647788002000,
                                    "manufacturingDate": calendar.timegm(time.gmtime()) * 1000,
                                    "expirationDate": 1740031232000
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        return logger.info("生产日期晚入库托盘A4,入库失败！！")
                    logger.info('生成日期晚入库托盘A4为：' + containerCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(containerCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 48 批次晚入库
                elif all_for_num == 5:
                    # e = WesApi().inpot_task(containerSpecCode, 48, skuCode)
                    skuCode1 = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    containerCode = '90000' + str(random.randint(1, 1000))
                    time.sleep(2)
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": containerCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": skuCode1,
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
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 48,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": datetime.datetime.now().strftime("%Y%m%d%H%M"),
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        return logger.info("批次晚入库托盘A5,入库失败！！")
                    logger.info('批次晚入库托盘A5为：' + containerCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(containerCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 48 生产日期晚入库
                elif all_for_num == 6:
                    # f = WesApi().inpot_task(containerSpecCode, 48, skuCode)
                    skuCode1 = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    containerCode = '90000' + str(random.randint(1, 1000))
                    time.sleep(2)
                    data = {
                        "taskList": [{
                            "regionCode": "ps",
                            "containerCode": containerCode,
                            "originStation": "ST-Pallet-303",
                            "orderTaskId": skuCode1,
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
                                    "containerSpecCode": containerSpecCode,
                                    "qty": 48,
                                    "skuCode": skuCode,
                                    "skuName": "海澜之家	",
                                    "owner": "test",
                                    "qualityState": "QUALIFIED",
                                    "lot": "0301",
                                    "status": "ON_SHELF",
                                    "packageAmount": "12",
                                    "oddCarton": 0,
                                    "receivingDate": 1647788002000,
                                    "manufacturingDate": calendar.timegm(time.gmtime()) * 1000,
                                    "expirationDate": 1740031232000
                                }]
                            }
                        }]
                    }
                    res = requests.post(url + "/wes-engine/api/task:moveIn", json=data)
                    if res.json()['returnMsg'] != 'success' and res.json()['returnUserMsg'] != '成功':
                        return logger.info("生产日期晚入库托盘A6,入库失败！！")
                    logger.info('生成日期晚入库托盘A6为：' + containerCode)
                    while True:
                        box_postion = TesApi().select_box_Postion(containerCode)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
                # 24 普通入库
                elif all_for_num == 7:
                    c = WesApi().inpot_task(containerSpecCode, 24, skuCode)
                    logger.info('入库托盘A7为：' + c)
                    while True:
                        box_postion = TesApi().select_box_Postion(c)
                        if box_postion[0]['position_type'] != 0 and box_postion[0]['node'] != '100.1790':
                            all_for_num += 1
                            break
            return '执行完毕'

    def auto_create(self):
        # 查询数据库中是否有可用数据规格
        sql = "select container_spec_code ,length, width, height from wes_engine.container_spec " \
              "where container_spec_type = 'ORIGINAL'"
        res_sql = SqlUtil().connect_data_wes(sql)
        # 进入判断
        if res_sql == ():
            res = TestCase().for_inpot()
            return res
        else:
            res = TestCase().for_inpot(containercode=res_sql[0]['container_spec_code'],
                                       length=res_sql[0]['length'],
                                       width=res_sql[0]['width'],
                                       height=res_sql[0]['height'])
            return res


if __name__ == '__main__':
    # 主数据下发（物料管理）
    # a = WesApi().basic_data('900345983')
    # print(a)

    # 有箱码下发入库任务
    # a = WesApi().inpot_task_code()
    # print(a)

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
    # print(type(a))
    # 基础数据容器规格为空的时候调用以下函数
    # a = TestCase().for_inpot()
    # print(a)
    # 基础数据容器规格不为空的时候调用以下函数(可根据日志查询已生成的容器规格编号)
    # a = TestCase().for_inpot(900345729)
    # print(a)
    a = TestCase().auto_create()
    print(a)
