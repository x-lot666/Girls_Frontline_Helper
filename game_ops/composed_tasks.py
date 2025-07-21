from core_ops.utils import *
from game_ops.basic_tasks import *


# --------------------------
# 游戏中的复合逻辑流程
# --------------------------

# 进入作战时仓库满员的人形回收
def retire_dolls():
    logging.info("[人形回收] 开始人形回收流程")
    ImageOps.find_image(COMMON_IMG("retire_dolls_0"), x_offset=-100, y_offset=0, action="click")
    wait(1.6)  # 等待人形回收界面加载,非常重要
    ImageOps.find_image(COMMON_IMG("retire_dolls_1"), confidence=0.95, random_point=True, padding=15, action="click")
    ImageOps.find_image(COMMON_IMG("retire_dolls_2"), random_point=True, action="click")
    BasicTasks.click_confirm()
    ImageOps.find_image(COMMON_IMG("retire"), random_point=True, action="click")
    wait(1)  # 等待人形回收完成
    BasicTasks.click_back_button()
    logging.info("[人形回收] 人形回收完成")


# 在主界面进行人形修理
def fix_dolls():
    logging.info("[人形修理] 开始人形修理流程")
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


# --------------------------
# 意外窗口处理函数
# --------------------------

def _handle_full_retire_dolls():
    """处理仓库满员的人形回收窗口"""
    if ImageOps.locate_image(COMMON_IMG("retire_dolls_0")):
        logging.info("[窗口检测] 需要进行人形回收")
        retire_dolls()
        wait(5)
        return True
    return False


def _handle_logistics_complete():
    """处理后勤完成窗口"""
    if ImageOps.locate_image(COMMON_IMG("deploy_all")):
        logging.info("[窗口检测] 后勤界面弹出")
        ImageOps.find_image(COMMON_IMG("deploy_all"), random_point=True, action="click")
        # 有时候会跳出资源超出上限,无法再获取的提示框
        ImageOps.find_image(COMMON_IMG("confirm"), confidence=0.75, random_point=True, action="click", timeout=3)
        wait(5)
        return True
    return False


def _handle_achievement_unlock():
    """处理解锁成就窗口"""
    if ImageOps.locate_image(COMMON_IMG("unlock_achievement")):
        logging.info("[窗口检测] 解锁成就界面弹出")
        ImageOps.find_image(COMMON_IMG("unlock_achievement"), y_offset=-200, random_point=True, action="click")
        while True:
            MouseOps.one_left_click()
            wait(1)
            if ImageOps.locate_image(COMMON_IMG("home_battle_button")):
                break
        wait(5)
        return True
    return False


def _handle_doll_repair():
    """处理人形修复窗口"""
    if ImageOps.locate_image(COMMON_IMG("fix_doll")):
        fix_dolls()
        wait(5)
        return True
    return False


# 处理意外窗口的复合函数
def deal_unexpected_windows():
    """
    处理意外窗口的整合函数
    当游戏出现各种意外窗口时,使画面回到主菜单,初始化画面
    :return: result
    """
    result = False

    # 依次处理各种意外窗口
    if _handle_full_retire_dolls():
        result = True
    if _handle_logistics_complete():
        result = True
    if _handle_achievement_unlock():
        result = True
    if _handle_doll_repair():
        result = True

    return result
