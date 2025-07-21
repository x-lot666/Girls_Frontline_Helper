from game_ops.composed_tasks import *
from core_ops.composed.composed_ops import *

"""
13-4 双vector拖尸
@author: moonight1199
说明：
    - 拖尸队放在第一梯队。
    - 第二只vector放在第二梯队，vector满弹药口粮。
    - 事先锁定不想回收的人型，该脚本会自动拆解3/4星人型。
    - 确保第一次进入战斗前,人形未满员(第一次不做自动回收处理”。
    - 关闭"回合结束二次确认"和"自动补给"
"""

# 所用的资源图片的文件夹名称
set_resource_subdir("13_4_vector")


def menu_enter_mission(final=False):
    """
    从主菜单进入任务
    """

    # 设置缩放标记，用于记录第一次战斗由于交换人形导致缩放重置的情况
    scroll_flag = False

    # 点击“首页-战斗”
    BasicTasks.click_home_battle_button()

    # 设置成普通难度
    ImageOps.find_image(IMG("mark_image"), x_offset=1120, y_offset=-600, action="click")

    # 如果能选中13-4则直接进入
    if not ImageOps.find_image(IMG("battle_13_4"), timeout=2, random_point=True, action="click"):
        # 切换至作战任务界面
        ImageOps.find_image(IMG("combat_mission"), action="click")

        # 切换至作战任务界面时未选择第十三战役则退出
        if not ImageOps.find_image(IMG("battle_13_4"), timeout=2, random_point=True, action="click"):
            # 将鼠标移动到战役选择区，并滚动至最下方
            battles = ["battle_3", "battle_6", "battle_9"]
            wait(1)
            for battle in battles:
                if ImageOps.find_image(IMG(battle)):
                    MouseOps.scroll_mouse(-1, 25)
                    break

            # 选择战役13
            ImageOps.find_image(IMG("battle_13"), confidence=0.98, random_point=True, action="click")

            # 选择战役13-4
            ImageOps.find_image(IMG("battle_13_4"), random_point=True, action="click")

    # 等待并点击“普通作战”
    ImageOps.find_image(COMMON_IMG("normal_battle"), random_point=True, action="click")

    # 等待出现“开始作战”
    ImageOps.wait_image(COMMON_IMG("start_battle"))

    # 寻找重型机场，如果没找到，就缩放地图
    if ImageOps.wait_image(IMG("airport"), timeout=1, confidence=0.75) is None:
        scroll_flag = True
        move_to_window_center("少女前线")
        wait(0.3)
        MouseOps.scroll_mouse(-1, 25)

    # 选择指挥部部署第一梯队
    ImageOps.find_image(IMG("headquarter"), random_point=True, action="click")
    BasicTasks.click_confirm()

    # 选择重型机场部署第二梯队
    ImageOps.find_image(IMG("airport"), confidence=0.75, random_point=True, action="click")
    ImageOps.find_image(IMG("choose_team"), timeout=1, random_point=True, action="click")
    BasicTasks.click_confirm()

    wait(1)
    # 交换第一梯队和第二梯队的vector
    exchange_vector()

    # 等待返回战斗页面
    wait(2)

    # 交换后重置缩放，此处
    if scroll_flag:
        move_to_window_center("少女前线")
        wait(0.3)
        MouseOps.scroll_mouse(-1, 25)

    # 进入作战后 到 结算页面前 的所有操作
    start_mission_actions()

    # 最后一次执行时直接退出
    if final:
        return

    # 等待并点击“再次作战”
    BasicTasks.click_repeat_battle()

    wait(2)

    # 由于结算时会弹出获取人形的界面,需要等结算完毕后点击一次
    # 持续点击,直到出现“再次作战”
    ImageOps.hold_click_until_image(COMMON_IMG("repeat_battle"), click_after=True)


# 交换第一梯队和第二梯队的vector
def exchange_vector():
    # 点击第一梯队
    ImageOps.find_image(IMG("team_1"), x_offset=-33, y_offset=30, action="click")

    # 点击“队伍编成”
    BasicTasks.click_team_composition()

    # 等待加载
    wait(1)

    # 点击vector
    ImageOps.find_image(IMG("vector"), random_point=True, action="click")

    # 筛选枪种为五星冲锋枪
    BasicTasks.click_filter()
    BasicTasks.click_filter_five_star()
    ImageOps.find_image(IMG("smg"), random_point=True, action="click")
    BasicTasks.click_confirm_filter()

    # 等待稳定
    wait(0.5)

    # 寻找仓库里的vector并换队
    while True:
        if ImageOps.locate_image(IMG("vector_team1"), confidence=0.9) is not None:
            ImageOps.find_image(IMG("vector_team1"), confidence=0.9, random_point=True, action="click")
            break
        MouseOps.scroll_mouse(-1, 5)

    wait(0.5)

    # 如果两只vector灾同一页则直接选择
    if ImageOps.locate_image(IMG("vector_team2"), confidence=0.9) is not None:
        ImageOps.find_image(IMG("vector_team2"), confidence=0.9, random_point=True, action="click")
    else:
    # 不在同一页时先回滚一页，再继续往下查找
        MouseOps.scroll_mouse(1, 5)
        while True:
            if ImageOps.locate_image(IMG("vector_team2"), confidence=0.9) is not None:
                ImageOps.find_image(IMG("vector_team2"), confidence=0.9, random_point=True, action="click")
                break
            MouseOps.scroll_mouse(-1, 5)

    # 点击“确定”
    BasicTasks.click_confirm_depot()

    # 点击“返回”
    BasicTasks.click_back_button()


# 进入作战后 到 结算页面前 的所有操作
def start_mission_actions():
    wait(0.5)

    # 等待并点击“开始作战”
    BasicTasks.click_start_battle()

    # 等待动画
    wait(3.6)

    # 选中第二梯队，并补给
    ImageOps.find_image(IMG("team_2"), x_offset=-33, y_offset=30, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_2"), x_offset=-33, y_offset=30, action="click")
    BasicTasks.click_supply_button()

    # 点击第一梯队
    ImageOps.find_image(IMG("team_1"), x_offset=-33, y_offset=30, action="click")

    # 等待并点击“计划模式”
    BasicTasks.click_enable_plan_mode()
    wait(0.5)

    # 点击两个敌人
    ImageOps.find_image(IMG("enemy_1"), x_offset=-50, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("enemy_2"), action="click")

    # 点击“下一回合”
    ImageOps.find_image(IMG("next_round"), random_point=True, action="click")

    # 等待并点击“执行计划”
    BasicTasks.click_execute_plan()


def final_mission():
    """
    最后一次执行任务
    """
    logging.info("[13-4 双vector拖尸] 进入最后一次执行")
    if deal_unexpected_windows_retire_3_4():
        menu_enter_mission(final=True)
    else:
        exchange_vector()
        start_mission_actions()
    # 等待任务结束
    ImageOps.find_image(COMMON_IMG("repeat_battle"), x_offset=300, action="move")
    # 返回主菜单
    ImageOps.hold_click_until_image(COMMON_IMG("back_button"), click_after=True)
    logging.info(f"[终止] 已达到最大执行次数")
    print_banner("[13-4 双vector拖尸] 自动化执行结束")

    exit()


def repeat_mission():
    """
    重复进入任务
    """

    # 交换第一梯队和第二梯队的vector
    exchange_vector()

    # 进入作战后 到 结算页面前 的所有操作
    start_mission_actions()

    # 等待并点击“再次作战”
    BasicTasks.click_repeat_battle()

    wait(2)

    # 由于结算时会弹出获取人形的界面,需要等结算完毕后点击一次
    # 持续点击,直到出现“再次作战”
    ImageOps.hold_click_until_image(COMMON_IMG("repeat_battle"), click_after=True)


def check_action_limit(action_count, max_actions):
    """
    检查执行次数是否超过最大限制
    :param action_count: 当前执行次数
    :param max_actions: 最大执行次数
    """
    if action_count >= max_actions:
        wait(1)
        final_mission()


def main(max_actions=999):
    """
    :param max_actions: 最大执行次数
    """
    print_banner("[13-4 双vector拖尸] 自动化执行开始，按f10强行退出")

    WindowOps.activate_window("少女前线")  # 激活游戏窗口
    action_count = 1  # 初始化执行计数

    while True:
        # 检查执行次数是否超过限制
        check_action_limit(action_count, max_actions)

        logging.info("[13-4 双vector拖尸] 场景 从主菜单进入任务")
        logging.info(f"[计数] 当前拖尸次数: {action_count} ")
        menu_enter_mission()
        action_count += 1

        while True:
            # 检查执行次数是否超过限制
            check_action_limit(action_count, max_actions)

            # 处理意外窗口后,从主菜单重新开始
            if deal_unexpected_windows_retire_3_4():
                break

            # 定位到“team 1”图像,表示可以继续进行任务
            if ImageOps.locate_image(IMG("team_1")):
                logging.info("[13-v 双vector拖尸] 场景 重复进行任务")
                logging.info(f"[计数] 当前打捞次数: {action_count} ")
                repeat_mission()
                action_count += 1


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"[异常] 程序发生错误: {e} ")
