from core.macros import *

# 溯源回归-行星环ex 自动打捞

# 所用的资源图片的文件夹名称
set_resource_subdir("back_to_origin")


def menu_enter_mission():
    """
    从主菜单进入任务
    """

    # 等待并点击“首页-战斗”
    wait_and_click_home_battle_button()

    # 等待并点击“‘溯源回归’活动入口”
    wait_and_click_random(IMG("back_to_origin"))

    # 等待页面加载完成
    wait_and_move(IMG("exchange_button"))

    # 等待并点击“行星环ex”
    if locate_image(IMG("planetary_rings_ex")):
        wait_and_click_random(IMG("planetary_rings_ex"))
    else:
        scroll_mouse(-3)  # 向下滚动鼠标,缩小地图
        while True:
            if locate_image(IMG("planetary_rings_ex")):
                wait_and_click_random(IMG("planetary_rings_ex"))
                break
            # 识别"day_1 耶稣之死",如果没有找到,则继续滚动鼠标回到开头
            while True:
                if locate_image(IMG("day_1")):
                    find_and_move(IMG("exchange_button"), x_offset=-700)
                    drag_rel(-500, 0, duration=0.3)
                    break
                find_and_move(IMG("exchange_button"), x_offset=-1200)
                drag_rel(1000, 0, duration=0.3)

    # 等待并点击“开始任务”
    wait_and_click_start_the_task()

    # 定位“机场”
    if locate_image(IMG("airport")):
        # 等待并点击“机场”
        wait_and_click(IMG("airport"), x_offset=-35, y_offset=0)
    else:
        while True:
            scroll_mouse(-3)
            if find_and_click(IMG("airport"), x_offset=-35, y_offset=0):
                break

    # 等待并点击“确定”
    wait_and_click_confirm()

    # 进入作战后 到 结算页面前 的所有操作
    start_mission_actions()

    # 等待并点击“再次作战”
    wait_and_click_repeat_battle()

    wait(2)

    # 由于结算时会弹出获取人形的界面,需要等结算完毕后点击一次
    # 持续点击,直到出现“再次作战”
    hold_click_until_image_click(COMMON_IMG("repeat_battle"))


def repeat_mission():
    """
    重复进行入任务
    """

    # 进入作战后 到 结算页面前 的所有操作
    start_mission_actions()

    # 等待并点击“再次作战”
    wait_and_click_repeat_battle()

    wait(2)

    # 由于结算时会弹出获取人形的界面,需要等结算完毕后点击一次
    # 持续点击,直到出现“再次作战”
    hold_click_until_image_click(COMMON_IMG("repeat_battle"))


# 进入作战后 到 结算页面前 的所有操作
def start_mission_actions():
    # 等待并点击“开始作战”
    wait_and_click_start_battle()

    # 等待动画
    wait(3.6)

    # 等待并点击“team 1”
    wait_and_click(IMG("team_1"), x_offset=-100, y_offset=30)

    # 等待并点击“计划模式”
    wait_and_click_enable_plan_mode()
    wait(0.5)

    # 点击人形最下面的敌人
    wait_and_move(IMG("team_1"), x_offset=-100, y_offset=360)
    # double_left_click()
    one_left_click()

    # 等待并点击“执行计划”
    wait_and_click_execute_plan()


# 检查执行次数是否超过限制
def check_action_limit(action_count, max_actions):
    if action_count >= max_actions:
        print("[溯源回归-行星环ex 自动打捞] 场景 进入最后一次执行")
        start_mission_actions()
        # 等待任务结束
        wait_and_move(COMMON_IMG("repeat_battle"), x_offset=300)
        # 返回主菜单
        hold_click_until_image_click(COMMON_IMG("back_button"))
        print(f"[终止] 已达到最大执行次数 {max_actions},程序结束")

        print("------------------------------------------------------------")
        print("[溯源回归-行星环ex 自动打捞] 场景 自动化执行结束")
        print("------------------------------------------------------------")

        exit()


def main(max_actions=4):
    """
    :param max_actions: 最大执行次数
    :return:
    """
    print("------------------------------------------------------------")
    print("[溯源回归-行星环ex 自动打捞] 场景 自动化执行开始")
    print("------------------------------------------------------------")

    activate_the_window("少女前线")  # 激活游戏窗口
    action_count = 1  # 初始化执行计数

    while True:
        # 检查执行次数是否超过限制
        check_action_limit(action_count, max_actions)

        print("[溯源回归-行星环ex 自动打捞] 场景 从主菜单进入任务")
        menu_enter_mission()
        action_count += 1
        print(f"[计数] 当前打捞次数: {action_count} ----------------------------------------------")

        while True:
            # 检查执行次数是否超过限制
            check_action_limit(action_count, max_actions)

            # 处理意外窗口后,从主菜单重新开始
            if deal_unexpected_windows():
                break

            # 定位到“team 1”图像,表示可以继续进行任务
            if locate_image(IMG("team_1")):
                print("[溯源回归-行星环ex 自动打捞] 场景 重复进行任务")
                repeat_mission()
                action_count += 1
                print(f"[计数] 当前打捞次数: {action_count} ----------------------------------------------")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[异常] 程序发生错误: {e}")
