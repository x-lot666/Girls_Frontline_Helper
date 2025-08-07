import threading

from core_ops.composed.composed_ops import *
from game_ops.composed_tasks import *

"""
虚子粒对-真空湮灭 自动打捞
说明:
    - 把主力队放在第一梯队。
    - 确保第一次进入战斗前,仓库人形未满员(第一次不做自动回收处理”。
    - 关闭"回合结束二次确认"和"自动补给"
更新:
    - 2024-08-08:应朋友要求,增加了普通难度打捞,在主函数处设置,默认ex难度。
"""

# ====================================================
# =                      全局变量
# ====================================================

# 所用的资源图片的文件夹名称
set_resource_subdir("virtual_pair")

# 线程设置
window_event = threading.Event()
window_thread = None  # 方便后面重启监控线程

# 设置打捞的人形类型
rescued_doll = 5
# 难度选择
select_difficulty = "ex_mode"
# 设置任务名称和机场名称,用于后续难度选择
mission_name = "vacuum_annihilation_ex"
airport_name = "airport_ex"


def menu_enter_mission(final=False):
    """
    从主菜单进入任务
    :param final: 是否为最后一次执行任务
    """

    global mission_name
    global airport_name

    # 点击“‘虚子粒对’活动入口”
    ImageOps.find_image(IMG("virtual_pair"), action="click")

    # 等待页面加载完成
    ImageOps.wait_image(IMG("mark_image_logo"))

    # 难度选择
    if select_difficulty == "normal_mode":
        mission_name = "vacuum_annihilation"
        airport_name = "airport"
        while True:
            # 如果不是“普通”难度,就一直点,直到切换到“普通”难度
            if ImageOps.locate_image(IMG("normal_mode")):
                break
            ImageOps.find_image(IMG("mark_image_logo"), y_offset=200, action="click")
            wait(0.5)

    else:
        # 如果难度是“普通”,就点一下,切换到其他难度
        # 真空湮灭只有ex难度,ux难度实际上也是ex难度
        ImageOps.find_image(IMG("normal_mode"), action="click", timeout=0.5)

    # 点击“真空湮灭”
    if ImageOps.locate_image(IMG(mission_name)):
        ImageOps.find_image(IMG(mission_name), random_point=True, action="click")
    else:
        MouseOps.scroll_mouse(-3, 15)  # 向下滚动鼠标,缩小地图
        while True:
            if ImageOps.locate_image(IMG(mission_name)):
                ImageOps.find_image(IMG(mission_name), random_point=True, action="click")
                break
            # 识别"真空湮灭",如果没有找到,则继续滚动鼠标回到开头
            while True:
                if ImageOps.locate_image(IMG(mission_name)):
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
    if ImageOps.locate_image(IMG(airport_name), confidence=0.70) is None:
        ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                            action="move")
        MouseOps.scroll_mouse(-3, 60)

    # 这里通过定位地图中心加上准确的偏移量来定位每个机场的位置
    # 机场一(左下): x_offset=-170, y_offset= 275
    # 机场二(右下): x_offset= 155, y_offset= 275
    # 机场三(右上): x_offset= 385, y_offset=-100

    # rescued_doll = 5, 把5设置默认值,防止程序报错
    x_offset = 385
    y_offset = -100
    if rescued_doll in (1, 2):
        x_offset = -170
        y_offset = 275
    elif rescued_doll in (3, 4):
        x_offset = 155
        y_offset = 275

    ImageOps.find_image(IMG(airport_name), confidence=0.70, x_offset=x_offset, y_offset=y_offset, action="click")

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
    ImageOps.hold_click_until_image_appear(COMMON_IMG("repeat_battle"), click_after=True)


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
    ImageOps.hold_click_until_image_appear(COMMON_IMG("repeat_battle"), click_after=True)


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

    # 这里通过定位地图中心加上准确的偏移量来定位每条线路终点的位置
    # 终点一(打捞M1895 CB): x_offset=-170, y_offset= 275
    # 终点二(打捞Cx4 风暴/SRS): x_offset= 155, y_offset= 275
    # 终点三(打捞AK-74U): x_offset= 385, y_offset=-100
    # 终点四(打捞TKB-408): x_offset= 385, y_offset=-100

    # rescued_doll = 5, 把5设置默认值,防止程序报错
    x_offset = 385
    y_offset = 275
    if rescued_doll is 1:
        x_offset = -325
        y_offset = -200
    elif rescued_doll in (2, 3):
        x_offset = -5
        y_offset = -200
    elif rescued_doll is 4:
        x_offset = 305
        y_offset = -200

    ImageOps.find_image(IMG(airport_name), confidence=0.70, x_offset=x_offset, y_offset=y_offset, action="click")

    # 点击“执行计划”
    BasicTasks.click_execute_plan()


def final_mission():
    """
    最后一次执行任务
    """
    logging.info("[虚子粒对-真空湮灭 自动打捞] 进入最后一次执行")
    if deal_unexpected_windows():
        menu_enter_mission(final=True)
    else:
        start_mission_actions()
    # 等待任务结束
    ImageOps.find_image(COMMON_IMG("repeat_battle"), x_offset=300, action="move")
    # 返回主菜单
    ImageOps.hold_click_until_image_appear(COMMON_IMG("back_button"), click_after=True)
    logging.info(f"[终止] 已达到最大执行次数")
    print_banner("[虚子粒对-真空湮灭 自动打捞] 自动化执行结束")

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


def main(max_actions=30, rescued_doll_type=5, difficulty="ex_mode"):
    """
    :param max_actions: 最大执行次数
    :param rescued_doll_type: 打捞的人形类型
        rescued_doll = 1 表示打捞 M1895 CB
        rescued_doll = 2 表示打捞 Cx4 风暴
        rescued_doll = 3 表示打捞 SRS
        rescued_doll = 4 表示打捞 AK-74U
        rescued_doll = 5 表示打捞 TKB-408

    :param difficulty: 选择的难度,默认为"ex_mode"
        "普通": "normal_mode"
        "困难": "ex_mode"
    """
    global rescued_doll
    global select_difficulty
    rescued_doll = rescued_doll_type
    select_difficulty = difficulty

    print_banner("[虚子粒对-真空湮灭 自动打捞] 自动化执行开始")
    # 激活游戏窗口,如果失败则自动打开少女前线
    if not launch_gf():
        logging.error("[启动异常] 启动游戏失败")
        exit()

    action_count = 1  # 初始化执行计数

    while True:
        # 检查执行次数是否超过限制
        check_action_limit(action_count, max_actions)

        logging.info("[虚子粒对-真空湮灭 自动打捞] 从主菜单进入任务")
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
                logging.info("[虚子粒对-真空湮灭 自动打捞] 重复进行任务")
                logging.info(f"[计数] 当前打捞次数: {action_count} ")
                repeat_mission()
                action_count += 1


if __name__ == '__main__':
    # try:
    main()
    # except Exception as e:
    #     logging.error(f"[异常] 程序发生错误: {e}")
