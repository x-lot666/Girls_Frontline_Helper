from core_ops.utils import *
from game_ops.basic_tasks import *


# --------------------------
# 游戏中的复合逻辑流程
# --------------------------

# 从主菜单进行人形回收
def menu_enter_retire_dolls():
    logging.info("[人形回收] 开始人形回收流程")
    ImageOps.find_image(COMMON_IMG("factory"), confidence=0.9, padding=15, action="click")
    ImageOps.find_image(COMMON_IMG("resource_retire"), confidence=0.9, padding=15, action="click")
    wait(0.8)  # 等待人形回收界面加载,非常重要
    ImageOps.find_image(COMMON_IMG("retire_dolls_1"), confidence=0.95, random_point=True, padding=15, action="click")

    if ImageOps.wait_image(COMMON_IMG("retire_dolls_2"), timeout=1):
        ImageOps.find_image(COMMON_IMG("retire_dolls_2"), random_point=True, action="click")

        if ImageOps.wait_image(COMMON_IMG("confirm"), confidence=0.75, timeout=1):
            BasicTasks.click_confirm()
            ImageOps.find_image(COMMON_IMG("retire"), random_point=True, action="click")
            wait(1)  # 等待人形回收完成

        else:
            logging.info("[人形回收] 无可回收人形")
            BasicTasks.click_back_button()
            wait(0.5)
            BasicTasks.click_back_button()
    else:
        logging.info("[人形回收] 无可回收人形")
    BasicTasks.click_back_button()
    logging.info("[人形回收] 人形回收完成")


# 进入作战时仓库满员的人形回收
def retire_dolls():
    logging.info("[人形回收] 开始人形回收流程")
    # 此处这样处理是因为有时候人形回收入口会被其他界面遮挡,导致无法定位到
    # 详细见_handle_reward_window()函数
    if not ImageOps.find_image(COMMON_IMG("retire_dolls_0"), x_offset=-100, y_offset=0, action="click", timeout=5):
        logging.info("[人形回收] 未定位到人形回收入口,可能被其他界面遮挡")
        return
    if not ImageOps.wait_image(COMMON_IMG("retire_dolls_1"), confidence=0.95, timeout=5):
        logging.info("[人形回收] 未定位到人形回收入口,可能被其他界面遮挡")
        return
    wait(0.8)  # 等待人形回收界面加载,非常重要
    ImageOps.find_image(COMMON_IMG("retire_dolls_1"), confidence=0.95, random_point=True, padding=15, action="click")
    ImageOps.find_image(COMMON_IMG("retire_dolls_2"), random_point=True, action="click")
    BasicTasks.click_confirm()
    ImageOps.find_image(COMMON_IMG("retire"), random_point=True, action="click")
    wait(1)  # 等待人形回收完成
    BasicTasks.click_back_button()
    logging.info("[人形回收] 人形回收完成")


# 进入作战时仓库满员的人形回收，会回收3/4星人型
def retire_dolls_3_4():
    logging.info("[人形回收] 开始人形回收(包含3/4星人型)流程")
    # 此处这样处理是因为有时候人形回收入口会被其他界面遮挡,导致无法定位到
    # 详细见_handle_reward_window()函数
    if not ImageOps.find_image(COMMON_IMG("retire_dolls_0"), x_offset=-100, y_offset=0, action="click", timeout=5):
        logging.info("[人形回收] 未定位到人形回收入口,可能被其他界面遮挡")
        return
    if not ImageOps.wait_image(COMMON_IMG("retire_dolls_1"), confidence=0.95, timeout=5):
        logging.info("[人形回收] 未定位到人形回收入口,可能被其他界面遮挡")
        return
    wait(0.8)  # 等待人形回收界面加载,非常重要
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


def recycle_equipment():
    logging.info("[装备回收] 开始装备回收流程")
    if not ImageOps.find_image(COMMON_IMG("recycle_equipment_0"), x_offset=-100, y_offset=0, action="click", timeout=5):
        logging.info("[装备回收] 未定位到装备回收入口,可能被其他界面遮挡")
        return
    ImageOps.wait_image(COMMON_IMG("recycle_UI"), confidence=0.95)
    wait(0.8)  # 等待回收界面加载,非常重要
    ImageOps.find_image(COMMON_IMG("recycle_UI"), x_offset=-100, action="click")
    ImageOps.find_image(COMMON_IMG("recycle_equipment_1"), random_point=True, action="click")
    ImageOps.find_image(COMMON_IMG("confirm_recycle_equipment"), random_point=True, action="click")
    ImageOps.find_image(COMMON_IMG("retire"), random_point=True, action="click")
    wait(1)  # 等待装备回收完成
    BasicTasks.click_back_button()
    logging.info("[装备回收] 装备回收完成")


# 根据等级排序强化装备
def upgrade_equipment_by_level():
    logging.info("[装备强化] 开始装备强化流程")
    if not ImageOps.find_image(COMMON_IMG("recycle_equipment_0"), x_offset=100, y_offset=0, action="click", timeout=5):
        logging.info("[装备强化] 未定位到装备强化入口,可能被其他界面遮挡")
        return
    ImageOps.wait_image(COMMON_IMG("upgrade_equip_0"))
    wait(0.8)  # 等待回收界面加载，非常重要
    # 选择被强化装备--------------------------------------------------------------------------------------
    ImageOps.find_image(COMMON_IMG("upgrade_equip_0"), random_point=True, action="click")
    ImageOps.find_image(COMMON_IMG("sort"), random_point=True, action="click")
    ImageOps.find_image(COMMON_IMG("sort"), x_offset=-230, y_offset=100, action="click")
    ImageOps.find_image(COMMON_IMG("sort"), x_offset=-1350, y_offset=90, action="click")
    # 选择被强化装备--------------------------------------------------------------------------------------

    # 选择强化狗粮---------------------------------------------------------------------------------------
    ImageOps.find_image(COMMON_IMG("upgrade_equip_1"), random_point=True, action="click")
    ImageOps.find_image(COMMON_IMG("upgrade_equip_2"), random_point=True, action="click")
    wait(0.5)
    MouseOps.one_left_click()
    wait(0.5)
    MouseOps.one_left_click()
    ImageOps.find_image(COMMON_IMG("confirm_upgrade_equip"), random_point=True, action="click")
    # 选择强化狗粮---------------------------------------------------------------------------------------

    # 强化装备
    BasicTasks.click_confirm()
    wait(0.2)
    # 高星提醒
    BasicTasks.click_confirm()
    # 等待装备强化完成
    wait(2)
    BasicTasks.click_back_button()
    logging.info("[装备强化] 装备强化完成")


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
    if ImageOps.locate_image(COMMON_IMG("retire_dolls_0"), confidence=0.98):
        logging.info("[窗口检测] 需要进行人形回收")
        retire_dolls()
        wait(5)
        return True
    return False


def _handle_full_recycle_equipment():
    """处理仓库满员的装备回收窗口"""
    if ImageOps.locate_image(COMMON_IMG("recycle_equipment_0"), confidence=0.98):
        logging.info("[窗口检测] 需要进行装备回收")
        recycle_equipment()
        wait(5)
        return True
    return False


def _handle_logistics_complete():
    """处理后勤完成窗口"""
    if ImageOps.locate_image(COMMON_IMG("deploy_all")):
        logging.info("[窗口检测] 后勤界面弹出")
        ImageOps.find_image(COMMON_IMG("deploy_all"), random_point=True, action="click")
        # 有时候会跳出资源超出上限,无法再获取的提示框
        ImageOps.find_image(COMMON_IMG("confirm"), confidence=0.75, random_point=True, action="click", timeout=1)
        wait(1)
        ImageOps.find_image(COMMON_IMG("confirm"), confidence=0.75, random_point=True, action="click", timeout=1)
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


def _handle_reward_window():
    """
    处理奖励窗口
    目前发现该窗口只会在特定情况下弹出:
    在灰域调查中,代理作战的时候刚好人形满员导致退出代理模式,并且点数刚好触发奖励,才会弹出此窗口
    由于是人形满员的窗口先弹出,所以这个窗口会被忽略掉
    目前来看只能在回收人形里来解决(添加超时机制,避免卡在回收人形的过程中)
    并且,处理此窗口,不返回True,因为点此窗口后,会停留在当前界面,而不是回到主菜单
    """
    if ImageOps.locate_image(COMMON_IMG("reward_window")):
        logging.info("[窗口检测] 领取奖励界面弹出")
        ImageOps.find_image(COMMON_IMG("reward_window"), x_offset=600, y_offset=-180, action="click", timeout=2)
        wait(1)


def _handle_doll_repair():
    """处理人形修复窗口"""
    if ImageOps.locate_image(COMMON_IMG("fix_doll")):
        fix_dolls()
        wait(5)
        return True
    return False


def _handle_new_dolls():
    """处理打捞人形时出现新人形的窗口"""
    if ImageOps.is_image_stable_for_seconds(COMMON_IMG("share_button"), confidence=0.80, check_time=3):
        logging.info("[窗口检测] 打捞到新人形")
        ImageOps.find_image(COMMON_IMG("share_button"), confidence=0.80, y_offset=160, action="click")
        wait(1)


# 处理意外窗口的复合函数
def deal_unexpected_windows():
    """
    处理意外窗口的整合函数。
    当游戏出现各种意外窗口时，依次处理它们，同时添加超时机制，只要处理过一个就重新开始检查，直到一个也没有为止。
    这样可以确保所有意外窗口都被处理(不然很可能因为顺序问题,导致多个窗口同时触发出现少处理的情况)。
    :return: 是否处理过任何意外窗口（True 表示处理过至少一个）
    """
    result = False

    while True:
        handled = False  # 当前轮次是否处理了窗口

        # 依次处理各种意外窗口
        if _handle_full_retire_dolls():
            handled = True
        elif _handle_full_recycle_equipment():
            handled = True
        elif _handle_reward_window():
            handled = True
        elif _handle_logistics_complete():
            handled = True
        elif _handle_achievement_unlock():
            handled = True
        elif _handle_doll_repair():
            handled = True
        elif _handle_new_dolls():
            handled = True

        if handled:
            result = True
            continue  # 回到开头，重新检查所有窗口
        else:
            break  # 当前轮次没有处理任何窗口，说明已经没有意外窗口了

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
    if ImageOps.locate_image(COMMON_IMG("retire_dolls_0"), confidence=0.98):
        logging.info("[窗口检测] 需要进行人形回收")
        retire_dolls_3_4()
        wait(5)
        result1 = True

    # 调用原始意外窗口的复合函数，处理其他异常
    result2 = deal_unexpected_windows()

    return result1 or result2


# 处理意外窗口的复合函数，会根据强化等级排序强化装备
def deal_unexpected_windows_upgrade_equipment():
    """
    处理意外窗口的整合函数，会根据强化等级排序强化装备
    当游戏出现各种意外窗口时,使画面回到主菜单,初始化画面
    :return: result
    """
    # 默认值False,如果处理过意外窗口则为True
    result1 = False

    # 确保图像稳定
    wait(0.1)

    # 检测进入作战时是否出现装备爆仓-----------------------------------------------------------------------------------------
    if ImageOps.locate_image(COMMON_IMG("recycle_equipment_0"), confidence=0.98):
        logging.info("[窗口检测] 需要进行装备强化")
        upgrade_equipment_by_level()
        wait(5)
        result1 = True

    # 调用原始意外窗口的复合函数，处理其他异常
    result2 = deal_unexpected_windows()

    return result1 or result2
