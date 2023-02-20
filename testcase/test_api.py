import datetime
from log.get_log import get_log
from API.wesApi import WesApi, TesApi

log = get_log(str(datetime.datetime.now().date()) + 'case.log')
class TestApi:
    # 有箱码入库
    def test_01_inpot_task_code(self):
        log.info('这是一个INFO信息')
        return "这是一个测试方法"
        # log.info('容器规格为:' + basic_data[0], 'sku号为:' + basic_data[1])
        # return WesApi().inpot_task_code(basic_data[0], basic_data[1])
