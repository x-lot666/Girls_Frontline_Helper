from game_ops.composed_tasks import *

"""
溯源回归-行星环ex 自动打捞
说明:
    - 把主力队放在第一梯队。
    - 确保第一次进入战斗前,人形未满员(第一次不做自动回收处理”。
    - 关闭"回合结束二次确认"和"自动补给"
"""

# 所用的资源图片的文件夹名称
set_resource_subdir("back_to_origin")


def menu_enter_mission(final=False):
    """
    从主菜单进入任务
    :param final: 是否为最后一次执行任务
    """

    # 点击“首页-战斗”
    BasicTasks.click_home_battle_button()

    # 点击“‘溯源回归’活动入口”
    ImageOps.find_image(IMG("back_to_origin"), random_point=True, padding=20, action="click")

    # 等待页面加载完成
    ImageOps.wait_image(IMG("exchange_button"))

    # 点击“行星环ex”
    if ImageOps.locate_image(IMG("planetary_rings_ex")):
        ImageOps.find_image(IMG("planetary_rings_ex"), random_point=True, action="click")
    else:
        MouseOps.scroll_mouse(-3, 15)  # 向下滚动鼠标,缩小地图
        while True:
            if ImageOps.locate_image(IMG("planetary_rings_ex")):
                ImageOps.find_image(IMG("planetary_rings_ex"), random_point=True, action="click")
                break
            # 识别"day_1 耶稣之死",如果没有找到,则继续滚动鼠标回到开头
            while True:
                if ImageOps.locate_image(IMG("day_1")):
                    ImageOps.find_image(IMG("exchange_button"), x_offset=-700, wait=False, action="move")
                    MouseOps.drag_rel(-500, 0)
                    break
                ImageOps.find_image(IMG("exchange_button"), x_offset=-1200, wait=False, action="move")
                MouseOps.drag_rel(1000, 0)

    # 点击“确认出击”
    BasicTasks.click_start_the_task()

    # 等待“开始作战”按钮出现
    ImageOps.wait_image(COMMON_IMG("start_battle"))

    # 定位“机场”
    if ImageOps.locate_image(IMG("airport")) is None:
        MouseOps.scroll_mouse(-3, 50)
    ImageOps.find_image(IMG("airport"), action="click")

    # 点击“确定”
    BasicTasks.click_confirm()

    # 进入作战后 到 结算页面前 的所有操作
    start_mission_actions()

    if final:
        return

    # 点击“再次作战”
    BasicTasks.click_repeat_battle()

    wait(1)

    # 由于结算时会弹出获取人形的界面,需要等结算完毕后点击一次
    # 持续点击,直到出现“再次作战”
    ImageOps.hold_click_until_image(COMMON_IMG("repeat_battle"), click_after=True)


def repeat_mission():
    """
    重复进行入任务
    """

    # 进入作战后 到 结算页面前 的所有操作
    start_mission_actions()

    # 点击“再次作战”
    BasicTasks.click_repeat_battle()

    wait(1)

    # 由于结算时会弹出获取人形的界面,需要等结算完毕后点击一次
    # 持续点击,直到出现“再次作战”
    ImageOps.hold_click_until_image(COMMON_IMG("repeat_battle"), click_after=True)


# 进入作战后 到 结算页面前 的所有操作
def start_mission_actions():
    wait(0.5)

    # 点击“开始作战”
    BasicTasks.click_start_battle()

    # 等待动画
    wait(3.6)

    # 选中“team 1”
    ImageOps.find_image(IMG("team_1"), x_offset=-33, y_offset=30, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_1"), x_offset=-33, y_offset=30, action="click")

    # 点击“补给按钮”
    BasicTasks.click_supply_button()

    # 点击“计划模式”
    BasicTasks.click_enable_plan_mode()
    wait(0.5)

    # 点击人形最下面的敌人
    ImageOps.find_image(IMG("team_1"), x_offset=-33, y_offset=360, action="click")

    # 点击“执行计划”
    BasicTasks.click_execute_plan()


def final_mission():
    """
    最后一次执行任务
    """
    logging.info("[溯源回归-行星环ex 自动打捞] 进入最后一次执行")
    if deal_unexpected_windows():
        menu_enter_mission(final=True)
    else:
        start_mission_actions()
    # 等待任务结束
    ImageOps.find_image(COMMON_IMG("repeat_battle"), x_offset=300, action="move")
    # 返回主菜单
    ImageOps.hold_click_until_image(COMMON_IMG("back_button"), click_after=True)
    logging.info(f"[终止] 已达到最大执行次数")
    print_banner("[溯源回归-行星环ex 自动打捞] 自动化执行结束")

    exit()


# 检查执行次数是否超过限制
def check_action_limit(action_count, max_actions):
    if action_count >= max_actions:
        wait(1)
        final_mission()


def main(max_actions=2):
    """
    :param max_actions: 最大执行次数
    """
    print_banner("[溯源回归-行星环ex 自动打捞] 自动化执行开始")
    WindowOps.activate_window("少女前线")  # 激活游戏窗口
    action_count = 1  # 初始化执行计数

    while True:
        # 检查执行次数是否超过限制
        check_action_limit(action_count, max_actions)

        logging.info("[溯源回归-行星环ex 自动打捞] 从主菜单进入任务")
        logging.info(f"[计数] 当前打捞次数: {action_count} ")
        menu_enter_mission()
        action_count += 1

        while True:
            # 检查执行次数是否超过限制
            check_action_limit(action_count, max_actions)

            # 处理意外窗口后,从主菜单重新开始
            if deal_unexpected_windows():
                break

            # 定位到“team 1”图像,表示可以继续进行任务
            if ImageOps.locate_image(IMG("team_1")):
                logging.info("[溯源回归-行星环ex 自动打捞] 重复进行任务")
                logging.info(f"[计数] 当前打捞次数: {action_count} ")
                repeat_mission()
                action_count += 1


if __name__ == '__main__':
    # try:
    main()
    # except Exception as e:
    #     logging.error(f"[异常] 程序发生错误: {e}")
