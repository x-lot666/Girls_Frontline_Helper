import logging

from core_ops.utils import *
from game_ops.basic_tasks import *


# --------------------------
# 游戏中的复合逻辑流程
# --------------------------

# 进入作战时仓库满员的人形回收
def retire_dolls():
    ImageOps.find_image(COMMON_IMG("retire_dolls_0"), x_offset=-100, y_offset=0, action="click")
    wait(1.6)  # 等待人形回收界面加载,非常重要
    ImageOps.find_image(COMMON_IMG("retire_dolls_1"), confidence=0.95, random_point=True, padding=15, action="click")
    ImageOps.find_image(COMMON_IMG("retire_dolls_2"), random_point=True, action="click")
    BasicTasks.click_confirm()
    ImageOps.find_image(COMMON_IMG("retire"), random_point=True, action="click")
    wait(1)  # 等待人形回收完成
    BasicTasks.click_back_button()
    logging.info("[人形回收] 人形回收完成")


# 进入作战时仓库满员的人形回收，会回收3/4星人型
def retire_dolls_3_4():
    ImageOps.find_image(COMMON_IMG("retire_dolls_0"), x_offset=-100, y_offset=0, action="click")
    wait(1.6)  # 等待人形回收界面加载,非常重要
    ImageOps.find_image(COMMON_IMG("retire_dolls_1"), confidence=0.95, random_point=True, padding=15, action="click")
    ImageOps.find_image(COMMON_IMG("retire_dolls_2"), random_point=True, action="click")
    BasicTasks.click_filter()
    BasicTasks.click_filter_four_star()  # 筛选出四星人型
    BasicTasks.click_filter_three_star()  # 筛选出三星人型
    BasicTasks.click_confirm_filter()

    # 定位到第一个三星人型，没有三星人型时，定位到第一个四星人型,选择一面的所有人型
    if BasicTasks.click_doll_three_star() or BasicTasks.click_doll_four_star():
        current_x, current_y = MouseOps.record_mouse_position()
        for _ in range(5):
            current_x += 220
            MouseOps.left_click_at(current_x, current_y)
        wait(0.1)
        current_x -= 1320
        current_y += 400
        for _ in range(6):
            current_x += 220
            MouseOps.left_click_at(current_x, current_y)

    BasicTasks.click_confirm()
    ImageOps.find_image(COMMON_IMG("retire"), random_point=True, action="click")
    # 弹出高星级回收提醒
    BasicTasks.click_confirm()
    wait(1)  # 等待人形回收完成
    BasicTasks.click_back_button()
    logging.info("[人形回收] 人形回收完成")


# 在主界面进行人形修理
def fix_dolls():
    logging.info("[人形修理] 检测到人形修理按钮,开始修理人形")

    # 点击“修理人形”
    BasicTasks.click_fix_doll()
    # 点击“一键修复”
    BasicTasks.click_fix_all_dolls()
    # 点击“确定”按钮
    BasicTasks.click_confirm()
    wait(1)
    # 点击“返回”按钮
    BasicTasks.click_back_button()

    logging.info("[人形修理] 人形修理完成")


# 处理意外窗口的复合函数
def deal_unexpected_windows():
    """
    处理意外窗口的整合函数
    当游戏出现各种意外窗口时,使画面回到主菜单,初始化画面
    :return: result
    """
    # 默认值False,如果处理过意外窗口则为True
    result = False

    # 检测进入作战时是否出现仓库满员-----------------------------------------------------------------------------------------
    if ImageOps.locate_image(COMMON_IMG("retire_dolls_0")):
        logging.info("[窗口检测] 需要进行人形回收")
        retire_dolls()
        wait(5)
        result = True

    # 检测在主界面时是否出现后勤完成的界面------------------------------------------------------------------------------------
    if ImageOps.locate_image(COMMON_IMG("deploy_all")):
        logging.info("[窗口检测] 后勤界面弹出")
        ImageOps.find_image(COMMON_IMG("deploy_all"), random_point=True, action="click")
        count = 0
        # 有时候会跳出资源超出上限,无法再获取的提示框
        while True:
            BasicTasks.click_confirm()
            count += 1
            if count >= 2:
                break
            wait(1)
        wait(5)
        result = True

    # 检测在主界面时是否出现解锁成就的界面------------------------------------------------------------------------------------
    if ImageOps.locate_image(COMMON_IMG("unlock_achievement")):
        logging.info("[窗口检测] 解锁成就界面弹出")
        ImageOps.find_image(COMMON_IMG("unlock_achievement"), y_offset=-200, random_point=True, action="click")
        while True:
            MouseOps.one_left_click()
            wait(1)
            if ImageOps.locate_image(COMMON_IMG("home_battle_button")):
                break
        wait(5)
        result = True

    # 检测在主界面时是否出现人形修复的界面------------------------------------------------------------------------------------
    if ImageOps.locate_image(COMMON_IMG("fix_doll")):
        fix_dolls()
        wait(5)
        result = True

    return result


# 处理意外窗口的复合函数，会拆解3/4星人型
def deal_unexpected_windows_retire_3_4():
    """
    处理意外窗口的整合函数，会拆解3/4星人型
    当游戏出现各种意外窗口时,使画面回到主菜单,初始化画面
    :return: result
    """
    # 默认值False,如果处理过意外窗口则为True
    result1 = False

    # 确保图像稳定
    wait(0.1)

    # 检测进入作战时是否出现仓库满员-----------------------------------------------------------------------------------------
    if ImageOps.locate_image(COMMON_IMG("retire_dolls_0")):
        logging.info("[窗口检测] 需要进行人形回收")
        retire_dolls_3_4()
        wait(5)
        result1 = True

    # 调用原始意外窗口的复合函数，处理其他异常
    result2 = deal_unexpected_windows()

    return result1 or result2


# 将鼠标移动到窗口中心
def move_to_window_center(title_keyword):
    center_x, center_y = WindowOps.get_center_of_window(title_keyword)

    if center_x is None:
        logging.error(f"[鼠标操作] 窗口“{title_keyword}”获取失败")
        return False

    MouseOps.move_to(center_x, center_y)

    logging.debug("[鼠标操作] 将鼠标移动到游戏窗口中心完成")

    return True
