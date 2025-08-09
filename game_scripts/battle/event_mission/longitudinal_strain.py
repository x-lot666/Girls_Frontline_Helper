import threading

from core_ops.composed.composed_ops import launch_gf
from game_ops.composed_tasks import *

"""
纵向应变-五重奏回旋曲ux 自动打捞(M240L)
说明:
    - 把主力队放在第一梯队。
    - 确保第一次进入战斗前,仓库人形未满员(第一次不做自动回收处理”。
    - 关闭"回合结束二次确认"和"自动补给"
特别说明:
    - 本来想写铁血队抽薪,但只挂了8把就捞到M240L,感觉爆率还挺高,就懒得写了。
"""

# ====================================================
# =                      全局变量
# ====================================================

# 所用的资源图片的文件夹名称
set_resource_subdir("longitudinal_strain")

# 场景名称
scene_name = "[纵向应变-五重奏回旋曲ux 自动打捞]"

# 线程设置
window_event = threading.Event()
window_thread = None  # 方便后面重启监控线程


def menu_enter_mission(final=False):
    """
    从主菜单进入任务
    :param final: 是否为最后一次执行任务
    """

    # 点击“首页-战斗”
    BasicTasks.click_home_battle_button()

    # 点击“常驻活动”
    BasicTasks.click_campaign()

    # 点击“‘纵向应变’活动入口”
    if (not ImageOps.locate_image(IMG("longitudinal_strain_active")) and
            not ImageOps.find_image(IMG("longitudinal_strain"), action="click", timeout=2)):
        ImageOps.find_image(IMG("mark_image"), x_offset=200, y_offset=-660, action="move")
        while True:
            MouseOps.scroll_mouse(3)
            wait(0.5)
            if ImageOps.locate_image(IMG("longitudinal_strain")):
                ImageOps.find_image(IMG("longitudinal_strain"))
                break

    wait(1)  # 非常重要,等待动画加载

    ImageOps.find_image(IMG("longitudinal_strain_button"), random_point=True, action="click")

    # 等待页面加载完成
    ImageOps.wait_image(IMG("mark_image_logo"))

    # 点击“F09车厢”
    ImageOps.find_image(IMG("carriage_f09"), action="click")

    # 切换成ux难度
    while True:
        if ImageOps.locate_image(IMG("ux_mode")):
            break
        ImageOps.find_image(IMG("exchange_button"), x_offset=-200, y_offset=0, action="click")
        wait(0.5)

    # 点击“五重奏回旋曲ux”
    ImageOps.find_image(IMG("quintet_rondo_ux"), y_offset=-66, action="click")

    # 点击“确认出击”
    BasicTasks.click_start_the_task()

    # 等待“开始作战”按钮出现
    ImageOps.wait_image(COMMON_IMG("start_battle"))

    # 定位“机场”
    if ImageOps.locate_image(IMG("airport"), confidence=0.70) is None:
        ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                            action="move")
        MouseOps.scroll_mouse(-3, 60)
    ImageOps.find_image(IMG("airport"), confidence=0.70, action="click")

    # 点击“确定”,部署第一梯队
    BasicTasks.click_confirm()

    # 开始作战后 到 结算页面前 的所有操作
    start_mission_actions()

    if final:
        return

    # 点击“再次作战”
    BasicTasks.click_repeat_battle()

    wait(1)

    # 由于结算时会弹出获取人形的界面,需要等结算完毕后点击一次
    # 持续点击,直到出现“再次作战”
    ImageOps.hold_click_until_image_appear(COMMON_IMG("repeat_battle"), click_after=True)


def repeat_mission():
    """
    重复进行入任务
    """

    # 开始作战后 到 结算页面前 的所有操作
    start_mission_actions()

    # 点击“再次作战”
    BasicTasks.click_repeat_battle()

    wait(1)

    # 由于结算时会弹出获取人形的界面,需要等结算完毕后点击一次
    # 持续点击,直到出现“再次作战”
    ImageOps.hold_click_until_image_appear(COMMON_IMG("repeat_battle"), click_after=True)


# 开始作战后 到 结算页面前 的所有操作
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

    # 点击路径点1
    ImageOps.find_image(IMG("team_1"), x_offset=-315, y_offset=-130, action="click")

    # 点击路径点2
    ImageOps.find_image(IMG("team_1"), x_offset=-320, y_offset=-30, action="click")

    # 点击“执行计划”
    BasicTasks.click_execute_plan()


def final_mission():
    """
    最后一次执行任务
    """
    logging.info(scene_name + " 进入最后一次执行")
    if deal_unexpected_windows():
        menu_enter_mission(final=True)
    else:
        start_mission_actions()
    # 等待任务结束
    ImageOps.find_image(COMMON_IMG("repeat_battle"), x_offset=300, action="move")
    # 返回主菜单
    ImageOps.hold_click_until_image_appear(COMMON_IMG("back_button"), click_after=True)
    logging.info(f"[终止] 已达到最大执行次数")
    print_banner(scene_name + " 自动化执行结束")

    exit()


# 检查执行次数是否超过限制
def check_action_limit(action_count, max_actions):
    if action_count >= max_actions:
        wait(1)
        final_mission()


def window_monitor(action_limit_event):
    """
    设置监控线程：检测是否出现:处理后会“返回主菜单”的意外窗口
    所有处理后返回主菜单的意外窗口,都在这里设置:常规意外窗口(常规战役)+特定意外窗口(灰域or活动)
    如果返回主菜单，则设置全局事件，自己退出本轮线程
    """
    while not window_event.is_set():
        try:
            # 常规意外窗口
            if deal_unexpected_windows():
                window_event.set()  # 通知主线程
                logging.info("[监控线程] 已处理异常窗口，并返回到主菜单")
                return
        except Exception as e:
            logging.error("[监控线程] 发生异常: %s", e)
        time.sleep(1)


def main(max_actions=30):
    """
    :param max_actions: 最大执行次数
    """
    print_banner(scene_name + " 自动化执行开始")
    # 激活游戏窗口,如果失败则自动打开少女前线
    if not launch_gf():
        logging.error("[启动异常] 启动游戏失败")
        exit()
    action_count = 1  # 初始化执行计数

    while True:
        # 检查执行次数是否超过限制
        check_action_limit(action_count, max_actions)

        logging.info(scene_name + " 从主菜单进入任务")
        logging.info(f"[计数] 当前打捞次数: {action_count} ")
        menu_enter_mission()
        action_count += 1

        # 进入循环前，把窗口事件清零，并启动监控线程
        window_event.clear()
        window_thread = threading.Thread(target=window_monitor, args=(window_event,), daemon=True)
        window_thread.start()

        while True:
            # 检查执行次数是否超过限制
            check_action_limit(action_count, max_actions)

            # 如果监控线程已发现异常 → 跳出循环、回到主流程
            if window_event.is_set():
                break

            # 定位到“team 1”图像,表示可以继续进行任务
            if ImageOps.locate_image(IMG("team_1")):
                logging.info(scene_name + " 重复进行任务")
                logging.info(f"[计数] 当前打捞次数: {action_count} ")
                repeat_mission()
                action_count += 1


if __name__ == '__main__':
    # try:
    main()
    # except Exception as e:
    #     logging.error(f"[异常] 程序发生错误: {e}")
