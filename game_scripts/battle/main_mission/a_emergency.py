import threading

from core_ops.composed.composed_ops import *
from game_ops.composed_tasks import *

"""
循演战役 A-紧急 自动打捞
说明:
    - 把主力队放在第一梯队。
    - 确保第一次进入战斗前,仓库人形未满员(第一次不做自动回收处理”。
    - 关闭"回合结束二次确认"和"自动补给"
"""

# ====================================================
# =                      全局变量
# ====================================================
# 请不要修改此处的任何变量,各项可调参数在主函数"main()"处设置

# 所用的资源图片的文件夹名称
set_resource_subdir("a_emergency")

# 场景名称
scene_name = "[循演战役 A-紧急 自动打捞]"

# 线程设置
window_event = threading.Event()
window_thread = None  # 方便后面重启监控线程

# 设置打捞的线路
rescued_line = 1
# 设置打捞的关卡
rescued_mission = 1


def menu_enter_mission(final=False):
    """
    从主菜单进入任务
    :param final: 是否为最后一次执行任务
    """

    # 点击“首页-战斗”
    BasicTasks.click_home_battle_button()

    # 如果循演战役没被激活，则点击循演战役
    if not ImageOps.wait_image(IMG("battle_a_active"), confidence=0.9, timeout=1.5):
        # 切换至作战任务界面
        ImageOps.find_image(COMMON_IMG("combat_mission"), action="click")

        # 如果没找到循演战役，滚动页面到底部
        if not ImageOps.find_image(IMG("battle_a"), confidence=0.95, timeout=1, action="click"):
            while True:
                ImageOps.find_image(IMG("mark_image"), x_offset=260, y_offset=-200, action="move")
                wait(0.2)
                MouseOps.scroll_mouse(-3, 20)
                if ImageOps.find_image(IMG("battle_a"), confidence=0.95, timeout=0.5,
                                       action="click") or ImageOps.find_image(IMG("battle_a_active"), confidence=0.90,
                                                                              timeout=0.5, action="move"):
                    break

    # 设置成紧急难度
    ImageOps.find_image(IMG("mark_image"), x_offset=1250, y_offset=-600, action="click")

    # 如果没找到对应关卡，滚动页面到底部
    # 点击a_n
    if not ImageOps.find_image(IMG("battle_a_" + str(rescued_mission)), confidence=0.90, timeout=0.5, action="click"):
        while True:
            ImageOps.find_image(IMG("mark_image_2"), action="move")
            wait(0.2)
            MouseOps.scroll_mouse(-3, 5)
            # 点击a_n
            if ImageOps.find_image(IMG("battle_a_" + str(rescued_mission)), confidence=0.90, timeout=0.5, action="click"):
                break

    # 等待并点击“普通作战”
    ImageOps.find_image(COMMON_IMG("normal_battle"), random_point=True, action="click")

    # 等待“开始作战”按钮出现
    ImageOps.wait_image(COMMON_IMG("start_battle"))

    # 定位“机场”
    if ImageOps.locate_image(IMG("airport"), confidence=0.90) is None:
        ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, padding=30,
                            action="move")
        MouseOps.scroll_mouse(-3, 60)  # 向下滚动鼠标,缩小地图
        MouseOps.drag_rel(0, 600)  # 把地图移到最上方

        while True:
            if ImageOps.locate_image(IMG("airport"), confidence=0.90):
                break

            # 把地图移到最右边
            ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=1000, y_offset=-300, random_point=True,
                                padding=30,
                                action="move")
            MouseOps.drag_rel(-1000, 0, 0.5)

            if ImageOps.locate_image(IMG("airport"), confidence=0.90):
                break

    # 这里通过定位地图中心加上准确的偏移量来定位每个机场的位置
    # 从上到下顺序排序
    # 机场一: x_offset= 270, y_offset= -100
    # 机场二: x_offset= 270, y_offset= 280

    # rescued_line in (1, 2, 3)  # 把1设置默认值,防止程序报错
    y_offset = -100
    if rescued_line in (4, 5, 6):
        y_offset = 280

    ImageOps.find_image(IMG("airport"), confidence=0.80, x_offset=270, y_offset=y_offset, action="click")


    # 点击“确定”
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

    # 这里通过定位地图中心加上准确的偏移量来定位每条线路的位置

    # rescued_line = 1  # 把1设置默认值,防止程序报错
    y_offset = -220
    if rescued_line == 2:
        y_offset = -100
    elif rescued_line == 3:
        y_offset = 30
    elif rescued_line == 4:
        y_offset = 160
    elif rescued_line == 5:
        y_offset = 280
    elif rescued_line == 6:
        y_offset = 385

    ImageOps.find_image(IMG("airport"), confidence=0.80, x_offset=150, y_offset=y_offset, action="click")
    ImageOps.find_image(IMG("airport"), confidence=0.80, x_offset=-100, y_offset=y_offset, action="click")
    ImageOps.find_image(IMG("airport"), confidence=0.80, x_offset=-350, y_offset=y_offset, action="click")
    ImageOps.find_image(IMG("airport"), confidence=0.80, x_offset=-100, y_offset=y_offset, action="click")

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


def main(max_actions=30, rescued_line_type=6, rescued_mission_type=1):
    """
    :param max_actions: 最大执行次数

    :param rescued_line_type: 打捞的线路,从上往下顺序排序,如图

        * * * * * 线路一, "*"表示小怪,每一行都是一条打捞线路
        * * * * * 线路二
        * * * * * 线路三
        * * * * * 线路四
        * * * * * 线路五
        * * * * * 线路六

        rescued_line = 1 表示打捞 线路一
        rescued_line = 2 表示打捞 线路二
        rescued_line = 3 表示打捞 线路三
        rescued_line = 4 表示打捞 线路四
        rescued_line = 5 表示打捞 线路五
        rescued_line = 6 表示打捞 线路六

    :param rescued_mission_type:打捞的关卡,填 1~6, "6" 对应的关卡是 A6-无限循环
    """
    global rescued_line
    rescued_line = rescued_line_type
    global rescued_mission
    rescued_mission = rescued_mission_type

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

            # 定位到“team 1”或机场的图像,表示可以继续进行任务
            if ImageOps.locate_image(IMG("team_1")) or ImageOps.locate_image(IMG("airport"), confidence=0.7):
                logging.info(scene_name + " 重复进行任务")
                logging.info(f"[计数] 当前打捞次数: {action_count} ")
                repeat_mission()
                action_count += 1


if __name__ == '__main__':
    # try:
    main()
    # except Exception as e:
    #     logging.error(f"[异常] 程序发生错误: {e}")
