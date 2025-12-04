from core_ops.composed.composed_ops import *
from game_ops.composed_tasks import *

"""
灰域调查-计划模式 自动化执行
说明:
    - 本脚本使用的仍然是游戏内置的计划模式,只是针对灰域调查的各种意外窗口进行了处理
    - 确保第一次进入战斗前,仓库人形未满员(第一次不做自动回收处理”。
"""

# 所用的资源图片的文件夹名称
resource_subdir = "grey_zone_inquiry"


def menu_enter_mission():
    """
    从主菜单进入任务
    """

    # 点击“‘灰域调查’活动入口”
    ImageOps.find_image(IMG("grey_zone_inquiry"), random_point=True, action="click")

    wait(1)

    while True:
        # 如果没找到“全选按钮”,就重复点击计划模式
        if ImageOps.locate_image(IMG("select_all_button")):

            # 选择 “探查许可证 + 资源”
            ImageOps.find_image(IMG("cost_type"), y_offset=90, action="click")

            # 点击“全选按钮”
            ImageOps.find_image(IMG("select_all_button"), random_point=True, action="click")
            break
        # 点击“计划模式”
        ImageOps.find_image(IMG("plan_mode"), action="click")
        wait(1)

    # 点击“运行计划模式”
    ImageOps.find_image(IMG("execution_plan_mode"), random_point=True, action="click")


def repeat_mission(select_difficulty="hard_mode"):
    """
    重复进行入任务
    :param select_difficulty: 难度选择,默认为"hard_mode"
    """

    # 点击“刷新按钮”
    ImageOps.find_image(IMG("refresh_button"), confidence=0.9, random_point=True, action="click")

    # 点击“困难难度”
    ImageOps.find_image(IMG(select_difficulty), random_point=True, action="click")

    # 点击“确定”
    BasicTasks.click_confirm()

    wait(6)

    while True:
        # 如果没找到“全选按钮”,就重复点击计划模式
        if ImageOps.locate_image(IMG("select_all_button")):

            # 选择 “探查许可证 + 资源”
            ImageOps.find_image(IMG("cost_type"), y_offset=90, action="click")

            # 点击“全选按钮”
            ImageOps.find_image(IMG("select_all_button"), random_point=True, action="click")
            break
        # 点击“计划模式”
        ImageOps.find_image(IMG("plan_mode"), action="click")
        wait(1)

    # 点击“运行计划模式”
    ImageOps.find_image(IMG("execution_plan_mode"), random_point=True, action="click")


def deal_unexpected_windows_mission_completed():
    """
    处理意外窗口的函数
    任务完成
    :return: Boolean
    """
    # 默认值False,如果处理过意外窗口则为True
    result = False

    # 持续检测 任务完成的标识出现,如果有其他窗口覆盖掉,则返回主循环中处理其他窗口
    if ImageOps.is_image_stable_for_seconds(IMG("plan_mode_completed"), confidence=0.92, check_time=3):
        ImageOps.find_image(IMG("plan_mode_completed"), confidence=0.92, random_point=True, action="click")
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
    if ImageOps.locate_image(IMG("mission_failed")):
        logging.info("[窗口检测] 任务失败:'当前战斗存在困难,将中断代理作战'")

        # 点击“关闭按钮”
        BasicTasks.click_close_button()

        # 有两种情况:被打到剩最后一只人形,或者是直接任务失败(小怪走到终点了,通常触发于代理模式下的弹药耗尽,后者人形会被重创)
        # 本来是在这里做个判断的,后来想想还是视为一种情况处理,都重新回到主菜单,看看需不需要修复人形
        if ImageOps.wait_image(COMMON_IMG("retry_battle"), timeout=2):
            # 点击“重新战斗”
            BasicTasks.click_retry_battle()
            wait(1.5)
            # 点击“暂停战斗”
            BasicTasks.click_pause_battle()
            # 点击“全体撤退”
            BasicTasks.click_evacuate_all()
            # 点击战斗失败标识(enjoy表情)
            BasicTasks.click_fail_enjoy_face()

        # 等待10秒,如果战斗失败标识(enjoy表情)出现,则说明只有一只部队在场上,会自动退出当前战场
        # 否则,说明有多只部队在场上,需要手动终止作战
        if ImageOps.wait_image(COMMON_IMG("fail_enjoy_face"), timeout=8):
            logging.info("[窗口检测] 任务失败:战斗失败标识(enjoy表情)")
            # 点击战斗失败标识(enjoy表情)右边600像素处
            ImageOps.find_image(COMMON_IMG("fail_enjoy_face"), x_offset=600, action="click")

        else:
            logging.info("[窗口检测] 任务失败:未检测到战斗失败标识(enjoy表情), 手动终止作战")
            # 点击终止作战-白色按钮
            BasicTasks.click_cancel_battle_white()
            # 点击终止作战-橙色按钮
            BasicTasks.click_cancel_battle_orange()

        BasicTasks.click_confirm()

        #进入修复人形流程
        # 点击“任务完成”按钮
        ImageOps.find_image(IMG("plan_mode_completed"), random_point=True, action="click")

        # 点击“返回”按钮
        ImageOps.find_image(IMG("back_button"), random_point=True, action="click")

        wait(5)

        # 返回主菜单后处理意外窗口
        deal_unexpected_windows()

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
    if ImageOps.locate_image(IMG("power_low")):
        logging.info("[窗口检测] 任务未正常进行:' 梯队无法满足关卡推荐效能要求'")

        # 点击“关闭按钮”
        BasicTasks.click_close_button()

        # 点击任务选择
        BasicTasks.click_select_mission()

        while True:
            # 识别“是否中断计划模式”
            if ImageOps.locate_image(IMG("interrupt_plan_mode")):
                BasicTasks.click_confirm()
                break

        # 点击“任务完成”按钮
        ImageOps.find_image(IMG("plan_mode_completed"), random_point=True, action="click")

        # 点击“返回”按钮
        ImageOps.find_image(IMG("back_button"), random_point=True, action="click")

        # 确认返回主菜单

        wait(5)

        # 返回主菜单后处理意外窗口
        deal_unexpected_windows()

        result = True

    return result


# 检查执行次数是否超过限制
def check_action_limit(action_count, max_actions):
    if action_count >= max_actions:
        return True


def main(max_actions=3, select_difficulty="hard_mode"):
    """
    :param max_actions: 最大执行次数
    :param select_difficulty: 选择的难度,默认为"hard_mode"
    "沙尘带": "easy_mode"
    "风暴带": "normal_mode"
    "硅状带": "hard_mode"
    "结晶带": "ex_mode"
    :return:
    """
    set_resource_subdir(resource_subdir)
    print_banner("[灰域调查 自动执行] 自动化执行开始")
    # 激活游戏窗口,如果失败则自动打开少女前线
    if not launch_gf():
        logging.error("[启动异常] 启动游戏失败")
        exit()
    action_count = 1  # 初始化执行计数
    action_limit = False

    while True:
        logging.info("先进行一次人形回收,防止程序卡死")
        menu_enter_retire_dolls()

        logging.info("[灰域调查 自动执行] 从主菜单进入任务")
        menu_enter_mission()
        logging.info(f"[计数] 当前执行次数: {action_count}")

        while True:
            # 检查执行次数是否超过限制
            if not action_limit:
                action_limit = check_action_limit(action_count, max_actions)

            # 处理意外窗口后,从主菜单重新开始
            if deal_unexpected_windows():
                break

            # 处理任务失败的情况,回到主菜单看看需不需要修复人形
            if deal_unexpected_windows_mission_failed():
                break

            # 处理任务未正常进行的情况:梯队无法满足关卡推荐效能要求
            if deal_unexpected_windows_power_low():
                break

            # 检查任务是否完成
            if deal_unexpected_windows_mission_completed():
                # 任务完成并且没有达到最大执行次数,重复进行任务
                if not action_limit:
                    logging.info("[灰域调查 自动执行] 重复进行任务")
                    repeat_mission(select_difficulty)
                    action_count += 1
                    logging.info(f"[计数] 当前执行次数: {action_count}")

                # 任务完成并且达到最大执行次数,退出程序
                else:
                    logging.info(f"[终止] 已达到最大执行次数,程序结束")
                    print_banner("[灰域调查 自动执行] 自动化执行结束")
                    exit()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        error_message = f"[异常] 程序发生错误: {e}"
        logging.error(error_message)
        trace = traceback.format_exc()  # 获取堆栈跟踪的字符串表示
        logging.error(trace)
