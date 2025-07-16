from core.macros import *

# 所用的资源图片的文件夹名称
set_resource_subdir("grey_zone_inquiry")


def menu_enter_mission():
    """
    从主菜单进入任务
    """

    # 等待并点击“‘灰域调查’活动入口”
    wait_and_click_random(IMG("grey_zone_inquiry"))

    wait(1)

    # 等待并点击“计划模式”
    wait_and_click_random(IMG("plan_mode"), padding=10)

    wait(1)

    # 选择 “探查许可证 + 资源”
    if locate_image(IMG("select_probe_and_resource")):
        wait_and_click_random(IMG("select_probe_and_resource"))

    # 等待并点击“全选按钮”
    wait_and_click_random(IMG("select_all_button"))

    # 等待并点击“运行计划模式”
    wait_and_click_random(IMG("execution_plan_mode"))


def repeat_mission(select_difficulty="hard_mode"):
    """
    重复进行入任务
    """

    # 等待并点击“刷新按钮”
    wait_and_click_random(IMG("refresh_button"), confidence=0.9)

    # 等待并点击“困难难度”
    wait_and_click_random(IMG(select_difficulty))

    # 等待并点击“确定”
    wait_and_click_confirm()

    wait(6)

    # 等待并点击“计划模式”
    wait_and_click_random(IMG("plan_mode"), padding=15)

    wait(1)

    # 选择 “探查许可证 + 资源”
    if locate_image(IMG("select_probe_and_resource")):
        wait_and_click_random(IMG("select_probe_and_resource"))

    # 等待并点击“全选按钮”
    wait_and_click_random(IMG("select_all_button"))

    # 等待并点击“运行计划模式”
    wait_and_click_random(IMG("execution_plan_mode"))


def deal_unexpected_windows_mission_completed():
    """
    处理意外窗口的函数
    任务完成
    :return: Boolean
    """
    # 默认值False,如果处理过意外窗口则为True
    result = False

    # 检测 任务完成
    if locate_image(IMG("plan_mode_completed")):
        wait_and_click_random(IMG("plan_mode_completed"))
        result = True

    return result


def deal_unexpected_windows_mission_failed():
    """
    处理意外窗口的函数
    任务失败:"当前战斗存在困难,将中断代理作战"
    :return: Boolean
    """
    # 默认值False,如果处理过意外窗口则为True
    result = False

    # 检测 任务失败:'当前战斗存在困难,将中断代理作战
    if locate_image(IMG("mission_failed")):
        print("[检测到] 任务失败:'当前战斗存在困难,将中断代理作战'")

        # 等待并点击“关闭按钮”
        wait_and_click_close_button()
        # 等待并点击“重新战斗”
        wait_and_click_retry_battle()
        wait(1.5)
        # 等待并点击“暂停战斗”
        wait_and_click_pause_battle()
        # 等待并点击“全体撤退”
        wait_and_click_evacuate_all()
        # 等待并点击战斗失败标识(enjoy表情)
        wait_and_click_fail_enjoy_face()

        # 等待10秒,如果战斗失败标识(enjoy表情)出现,则说明只有一只部队在场上,会自动退出当前战场
        # 否则,说明有多只部队在场上,需要手动终止作战
        wait(10)
        if locate_image(COMMON_IMG("fail_enjoy_face")):
            print("[检测到] 任务失败:战斗失败标识(enjoy表情)")
            # 等待并点击战斗失败标识(enjoy表情)右边600像素处
            wait_and_click(COMMON_IMG("fail_enjoy_face"), x_offset=600)

        else:
            print("[未检测到] 任务失败:战斗失败标识(enjoy表情)")
            # 等待并点击终止作战-白色按钮
            wait_and_click_cancel_battle_white()
            # 等待并点击终止作战-橙色按钮
            wait_and_click_cancel_battle_orange()

        wait_and_click_confirm()

        result = True

    return result


def deal_unexpected_windows_power_low():
    """
    处理意外窗口的函数
    任务未正常进行:"梯队无法满足关卡推荐效能要求"
    :return: Boolean
    """
    # 默认值False,如果处理过意外窗口则为True
    result = False

    # 检测 任务失败:'当前战斗存在困难,将中断代理作战
    if locate_image(IMG("power_low")):
        print("[检测到] 任务未正常进行:' 梯队无法满足关卡推荐效能要求'")

        # 等待并点击“关闭按钮”
        wait_and_click_close_button()

        # 等待并点击任务选择
        wait_and_click_select_mission()

        while True:
            # 识别“是否中断计划模式”
            if locate_image(IMG("interrupt_plan_mode")):
                wait_and_click_confirm()
                break

        # 等待并点击“任务完成”按钮
        wait_and_click_random(IMG("plan_mode_completed"))

        # 等待并点击“返回”按钮
        wait_and_click_random(IMG("back_button"))

        # 确认返回主菜单
        while True:
            if locate_image(COMMON_IMG("home_battle_button")):
                break

        if locate_image(COMMON_IMG("fix_doll")):
            # 检测到人形修复按钮,进入修复人形流程
            fix_dolls()

        result = True

    return result


# 检查执行次数是否超过限制
def check_action_limit(action_count, max_actions):
    if action_count >= max_actions:
        return True


def main(max_actions=3, select_difficulty="hard_mode"):
    """
    自动执行灰域调查场景
    :param max_actions: 最大执行次数
    :param select_difficulty: 选择的难度,默认为"hard_mode"
    "沙尘带": "easy_mode"
    "风暴带": "normal_mode"
    "硅状带": "hard_mode"
    "结晶带": "ex_mode"
    :return:
    """
    print("------------------------------------------------------------")
    print("[灰域调查 自动执行] 场景 自动化执行开始")
    print("------------------------------------------------------------")

    activate_the_window("少女前线")  # 激活游戏窗口
    action_count = 1  # 初始化执行计数
    action_limit = False

    while True:

        print("[灰域调查 自动执行] 场景 从主菜单进入任务")
        menu_enter_mission()
        print(f"[计数] 当前执行次数: {action_count} ----------------------------------------------")

        while True:
            # 检查执行次数是否超过限制
            if not action_limit:
                action_limit = check_action_limit(action_count, max_actions)

            # 处理意外窗口后,从主菜单重新开始
            if deal_unexpected_windows():
                break

            # 处理任务失败的情况
            deal_unexpected_windows_mission_failed()

            # 处理任务未正常进行的情况:梯队无法满足关卡推荐效能要求
            if deal_unexpected_windows_power_low():
                break

            # 检查任务是否完成
            if deal_unexpected_windows_mission_completed():
                # 任务完成并且没有达到最大执行次数,重复进行任务
                if not action_limit:
                    print("[灰域调查 自动执行] 场景 重复进行任务")
                    repeat_mission(select_difficulty)
                    action_count += 1
                    print(f"[计数] 当前执行次数: {action_count} ----------------------------------------------")

                # 任务完成并且达到最大执行次数,退出程序
                else:
                    print(f"[终止] 已达到最大执行次数 {max_actions},程序结束")
                    print("------------------------------------------------------------")
                    print("[灰域调查 自动执行] 场景 自动化执行结束")
                    print("------------------------------------------------------------")
                    exit()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[异常] 程序发生错误: {e}")
