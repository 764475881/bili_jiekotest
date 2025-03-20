import pymysql

class Getconn:
    def getconn(self):
        # 数据库连接配置
        global conn
        config = {
            'user': 'root',      # 数据库用户名
            'password': 'xxx',  # 数据库密码
            'host': 'xxxx',          # 数据库地址
            'database': 'miku',  # 数据库名称
            'port': 3306,                 # 数据库端口（默认3306）
            'charset': 'utf8mb4'          # 字符集
        }
    
        # 连接数据库
        try:
            conn = pymysql.connect(**config)
            return conn
        except pymysql.Error as err:
            print("数据库连接失败:", err)
            if conn is not None:
                conn.close()