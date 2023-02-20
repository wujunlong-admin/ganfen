import os
import logging
import datetime
from logging.handlers import RotatingFileHandler

# print(datetime.now().date())

# 测试

log_path = os.path.dirname(os.path.abspath(__file__))
projenct_path = os.path.dirname(log_path)
loging_path = os.path.join(projenct_path, 'log')
logings_path = os.path.join(loging_path, 'logs')


def get_log(log_name):
    # 创建日志器
    logger = logging.getLogger(log_name)
    # 收集日志级别
    logger.setLevel('INFO')
    # 设定日志输出格式
    fmt = "%(asctime)s -%(levelname)s -%(filename)s -Line:%(lineno)d -Message:%(message)s"
    log_forment = logging.Formatter(fmt)
    # 日志写入路径
    file_name = os.path.join(logings_path, log_name)
    file_handler = RotatingFileHandler(file_name, maxBytes=20 * 1024 * 1024, backupCount=10, encoding='utf-8')
    # 控制台输出日志
    stream_handler = logging.StreamHandler()
    # 输出日志级别
    stream_handler.setLevel('INFO')
    # 指定日志格式
    stream_handler.setFormatter(log_forment)
    # 指定输出级别
    file_handler.setLevel('INFO')
    file_handler.setFormatter(log_forment)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


if __name__ == '__main__':
    log = get_log(str(datetime.datetime.now().date()) + 'case.log')
    log.info('这是一个INFO日志')


