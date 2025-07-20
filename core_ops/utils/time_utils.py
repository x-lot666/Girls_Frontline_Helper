import random
import time

from config.logger_config import *

"""
封装时间相关的操作
"""


# 等待(秒)
def wait(seconds):
    logging.debug(f"[等待] {seconds} 秒")
    time.sleep(seconds)


def wait_in_range(min_seconds, max_seconds):
    """
    等待一个随机时间,在指定范围内
    :param min_seconds: 最小等待时间(秒)
    :param max_seconds: 最大等待时间(秒)
    """
    seconds = random.uniform(min_seconds, max_seconds)
    logging.debug(f"[等待] {seconds:.2f} 秒")
    time.sleep(seconds)
