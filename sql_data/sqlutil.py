import pymysql
from option_yaml.get_yaml_data import read_yaml_data


class SqlUtil:
    def connect_data_wes(self, sql_data):
        # 创建数据库链接
        db = pymysql.connect(
            host=read_yaml_data()[2]['dataHost'],  # 主机ip
            user=read_yaml_data()[2]['user'],  # 数据库用户
            password=read_yaml_data()[2]['password'],  # 用户对应的密码
            database=read_yaml_data()[2]['databases'],  # 对应的数据库
            port=read_yaml_data()[2]['port'],  # 数据库端口，默认3306,
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建游标:游标用于传递python给mysql的命令和mysql返回的内容
        cursor = db.cursor()
        sql = sql_data
        # 执行部分
        cursor.execute(sql)  # 执行命令，返回查询的条数
        return cursor.fetchall()

    def connect_data_tes(self, sql_data):
        # 创建数据库链接
        db = pymysql.connect(
            host=read_yaml_data()[1]['dataHost'],  # 主机ip
            user=read_yaml_data()[1]['user'],  # 数据库用户
            password=read_yaml_data()[1]['password'],  # 用户对应的密码
            database=read_yaml_data()[1]['databases'],  # 对应的数据库
            port=read_yaml_data()[1]['port'],  # 数据库端口，默认3306,
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建游标:游标用于传递python给mysql的命令和mysql返回的内容
        cursor = db.cursor()
        sql = sql_data
        # 执行部分
        cursor.execute(sql)  # 执行命令，返回查询的条数
        return cursor.fetchall()

# if __name__ == '__main__':
#     sql = "select * from tes.frame where frame_id='90000077'"
#     a = SqlUtil().connect_data_wes(sql)
#     print(a)
