import logging
import time
import uuid

import redis

from util import nacos_client

# 通过 get_config() 函数获取配置（懒加载）
current_config = nacos_client.get_config()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class RedisDistributedLock:
    def __init__(self, lock_name, expire=10):
        self.redis = redis.StrictRedis(host=current_config.get('redis_host'), port=current_config.get('redis_port'),
                                       db=current_config.get('redis_db'),
                                       password=current_config.get('redis_password'))
        self.lock_name = lock_name
        self.expire = expire  # 锁的超时时间（秒）
        self.lock_value = str(uuid.uuid4())  # 使用UUID作为锁的唯一标识符

    def acquire(self, blocking=True, timeout=None):
        """
        尝试获取锁。

        :param blocking: 是否阻塞等待锁。如果为True，则在当前线程等待直到锁可用；如果为False，则立即返回锁的状态。
        :param timeout: 阻塞等待锁时的超时时间（秒）。
        :return: 如果成功获取锁，则返回True；否则返回False。
        """
        end_time = None
        if timeout is not None:
            end_time = time.time() + timeout

        while True:
            # 尝试设置锁，如果键不存在则设置成功
            if self.redis.set(self.lock_name, self.lock_value, nx=True, ex=self.expire):
                return True

            if not blocking:
                # 非阻塞模式，立即返回False
                return False

            # 阻塞模式，等待直到锁可用或超时
            if timeout is not None:
                current_time = time.time()
                if current_time >= end_time:
                    return False
                sleep_time = end_time - current_time
                time.sleep(min(sleep_time, 0.01))  # 休眠一小段时间，避免忙等待
            else:
                time.sleep(0.01)  # 无限阻塞时，也稍微休眠一下

    def release(self):
        """
        释放锁。

        注意：释放锁之前应该确保当前线程确实持有该锁，以避免误释放其他线程的锁。
        这个实现通过比较锁的值来确保安全性。

        :return: 如果成功释放锁，则返回True；否则返回False。
        """
        pipe = self.redis.pipeline(True)
        try:
            while True:
                try:
                    # 使用Lua脚本原子性地检查锁的值并删除锁
                    script = """
                    if redis.call("get", KEYS[1]) == ARGV[1] then
                        return redis.call("del", KEYS[1])
                    else
                        return 0
                    end
                    """
                    result = pipe.eval(script, 1, self.lock_name, self.lock_value)
                    pipe.execute()
                    if result == 1:
                        return True
                    else:
                        return False
                except redis.exceptions.ConnectionError:
                    # 连接Redis时发生错误，尝试重新连接
                    self.redis.connection_pool.disconnect()
                    self.redis.connection_pool.get_connection()
        except Exception as e:
            # 其他异常，打印错误信息
            print(f"Error releasing lock: {e}")
            return False


# 测试
# lock_name = 'my_distributed_lock'
# lock = RedisDistributedLock(lock_name, expire=5)
#
#
# # 临界区函数
# def critical_section(thread_id):
#     print(f"Thread {thread_id} trying to acquire lock...")
#     if lock.acquire(blocking=True, timeout=10):
#         try:
#             print(f"Thread {thread_id} acquired lock!")
#             # 模拟临界区代码执行
#             time.sleep(2)  # 假设临界区代码需要2秒来执行
#             print(f"Thread {thread_id} finished executing critical section and will release lock.")
#         finally:
#             lock.release()
#             print(f"Thread {thread_id} released lock.")
#     else:
#         print(f"Thread {thread_id} failed to acquire lock within timeout.")
#
#     # 创建线程列表
#
#
# threads = []
# num_threads = 5
#
# # 创建并启动线程
# for i in range(num_threads):
#     thread = threading.Thread(target=critical_section, args=(i,))
#     threads.append(thread)
#     thread.start()
#
# # 等待所有线程完成
# for thread in threads:
#     thread.join()
#
# print("All threads have finished execution.")
