from core_ops.utils import *
from game_ops.basic_tasks import *

"""
各种操作相关的复合逻辑
暂时放这里,功能多了后续再拆分成不同的模块
"""


# 将鼠标移动到窗口中心
def move_to_window_center(title_keyword):
    center_x, center_y = WindowOps.get_center_of_window(title_keyword)

    if center_x is None:
        logging.error(f"[鼠标操作] 窗口“{title_keyword}”获取失败")
        return False

    MouseOps.move_to(center_x, center_y)

    logging.debug("[鼠标操作] 将鼠标移动到游戏窗口中心完成")

    return True
