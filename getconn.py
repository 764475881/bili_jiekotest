import pymysql
from dbutils.pooled_db import PooledDB

class DBConnectionPool:
    _pool = None

    def __init__(self):
        if self._pool is None:
            self._create_pool()

    @classmethod
    def _create_pool(cls):
        config = {
            'user': 'root',
            'password': 'xxx',
            'host': '10.11.12.141',
            'database': 'xxx',
            'port': 3306,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor  # 推荐添加返回字典格式游标
        }

        # 连接池配置
        cls._pool = PooledDB(
            creator=pymysql,    # 使用pymysql作为连接创建者
            mincached=2,       # 初始化时创建的空闲连接数
            maxcached=5,       # 池中空闲连接的最大数量
            maxconnections=20,  # 池中最大连接数
            blocking=True,      # 当连接数达到最大时阻塞等待
            **config
        )

    def get_connection(self):
        """从连接池获取连接"""
        return self._pool.connection()

    @classmethod
    def close_all(cls):
        """关闭所有连接（通常在程序退出时调用）"""
        if cls._pool:
            cls._pool.close()
            cls._pool = None

