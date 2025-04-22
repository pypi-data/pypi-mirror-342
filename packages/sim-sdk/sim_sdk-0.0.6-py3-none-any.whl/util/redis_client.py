import redis
import logging
from threading import Lock
from util import nacos_client

config = nacos_client.get_config()  # 获取配置


class RedisClient:
    _instance = None  # 用于保存单例实例
    _lock = Lock()  # 锁，用于线程安全的单例模式

    def __new__(cls, *args, **kwargs):
        """ 单例模式实现 """
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls, *args, **kwargs)
                cls._instance._init_redis()
        return cls._instance

    def _init_redis(self):
        """ 初始化 Redis 连接池 """
        try:
            self.redis_pool = redis.ConnectionPool(
                host=config.get('redis_host'),
                port=config.get('redis_port'),
                db=config.get('redis_db'),
                password=config.get('redis_password')
            )
            self.redis_client = redis.Redis(connection_pool=self.redis_pool)
            logging.info("Redis 连接池已初始化")
        except Exception as e:
            logging.exception("Redis 连接池初始化失败")
            raise e

    def set(self, cache_key, cache_value, expire_time=60):
        """ 设置 Redis 键值对 """
        try:
            self.redis_client.set(cache_key, cache_value)
            self.redis_client.expire(cache_key, expire_time)
            return True
        except Exception as e:
            logging.exception(f"设置缓存失败，key: {cache_key}")
            return False

    def expire(self, cache_key, expire_time=60):
        """ 刷新 Redis 键的过期时间 """
        try:
            self.redis_client.expire(cache_key, expire_time)
            return True
        except Exception as e:
            logging.exception(f"刷新缓存过期时间失败，key: {cache_key}")
            return False

    def hset(self, cache_key, field, value, expire_time=60):
        """ 设置 Redis 哈希表中的字段值 """
        try:
            # 使用 hset 设置哈希表中的字段
            self.redis_client.hset(cache_key, field, value)

            # 设置缓存的过期时间（如果需要）
            self.redis_client.expire(cache_key, expire_time)

            return True
        except Exception as e:
            logging.exception(f"设置哈希表字段失败，key: {cache_key}, field: {field}")
            return False

    def get(self, cache_key):
        """ 获取 Redis 键值 """
        try:
            return self.redis_client.get(cache_key)
        except Exception as e:
            logging.exception(f"获取缓存失败，key: {cache_key}")
            return None

    def delete(self, cache_key):
        """ 删除 Redis 键值 """
        try:
            self.redis_client.delete(cache_key)
            return True
        except Exception as e:
            logging.exception(f"删除缓存失败，key: {cache_key}")
            return False

    def exists(self, cache_key):
        """ 判断 Redis 键是否存在 """
        try:
            return self.redis_client.exists(cache_key)
        except Exception as e:
            logging.exception(f"检查缓存存在性失败，key: {cache_key}")
            return False

    def increment(self, cache_key, amount=1):
        """ Redis 键值自增 """
        try:
            return self.redis_client.incr(cache_key, amount)
        except Exception as e:
            logging.exception(f"自增缓存失败，key: {cache_key}")
            return None

    def hincrement(self, cache_key, field, amount=1):
        """ Redis 哈希表字段自增 """
        try:
            return self.redis_client.hincrby(cache_key, field, amount)
        except Exception as e:
            logging.exception(f"自增哈希表字段失败，key: {cache_key}, field: {field}")
            return None

    def incr_float(self, cache_key, increment, expire_time=60):
        try:
            # 使用 INCRBYFLOAT 来进行浮点数累加
            new_value = self.redis_client.incrbyfloat(cache_key, increment)

            # 设置过期时间，只有在 expire_time 大于 0 的情况下
            if expire_time > 0:
                self.redis_client.expire(cache_key, expire_time)

            return new_value  # 返回累加后的新值
        except Exception as e:
            logging.exception("增加缓存发生异常")
            return None  # 操作失败时返回 None

    def set_multiple(self, mapping, expire_time=60):
        """ 批量设置 Redis 键值对 """
        try:
            with self.redis_client.pipeline() as pipe:
                for key, value in mapping.items():
                    pipe.set(key, value)
                    pipe.expire(key, expire_time)
                pipe.execute()
            return True
        except Exception as e:
            logging.exception("批量设置缓存失败")
            return False
