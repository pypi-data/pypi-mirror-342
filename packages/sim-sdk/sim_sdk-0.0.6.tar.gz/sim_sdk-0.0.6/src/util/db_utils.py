import logging
from contextlib import contextmanager

import pymysql
from pymysql import OperationalError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CustomDBUtils:
    def __init__(self, db_config):
        """初始化数据库配置，创建数据库连接池"""
        self.db_config = db_config

    def _get_connection(self):
        """每次获取新的数据库连接"""
        return pymysql.connect(
            host=self.db_config["host"],
            port=self.db_config["port"],
            user=self.db_config["user"],
            password=self.db_config["password"],
            database=self.db_config["database"],
            charset=self.db_config["charset"],
            cursorclass=pymysql.cursors.DictCursor
        )

    @contextmanager
    def get_cursor(self):
        """上下文管理器，确保游标在使用后关闭"""
        connection = self._get_connection()  # 从连接池获取连接
        cursor = connection.cursor()
        try:
            yield cursor
            connection.commit()  # 提交事务
        except Exception as e:
            logging.exception("执行 SQL 出现异常")
            connection.rollback()  # 回滚事务
            raise e
        finally:
            cursor.close()
            connection.close()  # 归还连接到连接池

    def execute_batch_sql(self, sql, values_list):
        try:
            with self.get_cursor() as cursor:
                cursor.executemany(sql, values_list)
        except OperationalError as e:
            logging.exception("MySQL 执行 SQL 发生异常: %s", e)
        except Exception as e:
            logging.exception("批量执行sql异常，sql: %s,values_list:%s", sql, values_list)
            raise e

    def insert_batch(self, sql_statements, values_list):
        """批量执行 SQL（插入、更新、删除等操作），返回插入的 ID 集合"""
        inserted_ids = []  # 用于存储插入的 ID 集合
        try:
            with self.get_cursor() as cursor:
                for sql, values in zip(sql_statements, values_list):
                    cursor.execute(sql, values)
                    # 获取插入的 ID，假设有自增长字段
                    last_inserted_id = cursor.lastrowid
                    inserted_ids.append(last_inserted_id)  # 添加到返回的 ID 集合
        except OperationalError as e:
            logging.exception("MySQL 执行 SQL 发生异常: %s", e)
        except Exception as e:
            logging.exception("执行 SQL 发生异常")
            raise e

        return inserted_ids  # 返回插入的 ID 集合

    def insert_and_get_id(self, sql, data):
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, data)
                # 获取插入的 ID，假设有自增长字段
                last_inserted_id = cursor.lastrowid
                return last_inserted_id
        except OperationalError as e:
            logging.exception("MySQL 执行 SQL 发生异常: %s", e)
        except Exception as e:
            logging.exception("执行 SQL 发生异常")
            raise e

    def execute_sql(self, sql_statements, values_list):
        """批量执行 SQL（插入、更新、删除等操作）"""
        try:
            with self.get_cursor() as cursor:
                for sql, values in zip(sql_statements, values_list):
                    cursor.execute(sql, values)
        except OperationalError as e:
            logging.exception("MySQL 执行 SQL 发生异常: %s", e)
        except Exception as e:
            logging.exception("执行 SQL 发生异常")
            raise e

    def execute_single_sql(self, sql_statement):
        """执行单个完整 SQL（插入、更新、删除等操作）"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql_statement)
        except OperationalError as e:
            logging.exception("MySQL 执行 SQL 发生异常: %s", e)
        except Exception as e:
            logging.exception("执行 SQL 发生异常")
            raise e

    def fetch_one(self, sql, params=None):
        """执行查询并返回一条记录"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, params or [])
                return cursor.fetchone()  # 返回字典形式的查询结果
        except OperationalError as e:
            logging.exception("MySQL 执行 SQL 发生异常: %s", e)
        except Exception as e:
            logging.exception("查询执行失败")
            raise e

    def fetch_all(self, sql, params=None):
        """执行查询并返回所有记录"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, params or [])
                return cursor.fetchall()  # 返回字典形式的查询结果
        except OperationalError as e:
            logging.exception("MySQL 执行 SQL 发生异常: %s", e)
        except Exception as e:
            logging.exception("查询执行失败")
            raise e
