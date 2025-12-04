from core_ops.utils.exceptions import MissionFinished
from game_ops.composed_tasks import *

"""
8-1 夜战 双Zas拖尸
@author: moonight1199
说明：
    - 第一梯队：拖尸队
    - 第二梯队：队长位zas
    - 第三梯队：狗粮
    
    - 确保第一次进入战斗前,装备仓库未满(第一次不做自动回收处理)
    - 关闭"回合结束二次确认"和"自动补给"

配置项使用说明：
    - temp_team：配置是否使用狗粮队
    - 开启狗粮队将会在重型机场部署第三梯队
    - 狗粮队相当于用2人口换10口粮
    
    - upgrade_equipment：配置是否在装备满仓是自动强化装备
    - 开启装备强化时，将按照等级排序依次强化装备
    - 可以将需要强化的装备提前强化至1级，使排序靠前
    - 关闭装备强化时，将在满仓时分解装备
"""

# 所用的资源图片的文件夹名称
resource_subdir = "8_1_midnight"

# 通用配置项------------------------------------------------------------------
temp_team = True  # 配置是否使用狗粮队
upgrade_equipment = True  # 配置是否在装备满仓时自动强化装备
# 通用配置项------------------------------------------------------------------

equipment_round = False  # 设置当前是否为处理完装备的回合，由此判断是否交换zas


def menu_enter_mission():
    """
    从主菜单进入任务
    """
    global equipment_round

    # 点击“首页-战斗”
    BasicTasks.click_home_battle_button()

    # 如果能选中8-1n则直接进入
    if not ImageOps.find_image(IMG("battle_8_1_n"), timeout=2, random_point=True, action="click"):
        # 切换至作战任务界面
        ImageOps.find_image(IMG("combat_mission"), action="click")

        # 如果没找到第八战役，滚动页面到底部
        if not ImageOps.find_image(IMG("battle_8"), confidence=0.95, timeout=1, action="click"):
            ImageOps.find_image(IMG("mark_image"), x_offset=250, y_offset=-200, action="move")
            wait(0.2)
            MouseOps.scroll_mouse(-3, 20)
            wait(0.5)
            # 向上滚动寻找第八战役
            MouseOps.scroll_mouse(1, 5)
            ImageOps.find_image(IMG("battle_8"), confidence=0.95, timeout=1, action="click")

            # 设置成夜战难度
            ImageOps.find_image(IMG("mark_image"), x_offset=1400, y_offset=-600, action="click")

            # 点击8-1n
            ImageOps.find_image(IMG("battle_8_1_n"), random_point=True, action="click")

    # 等待并点击“普通作战”
    ImageOps.find_image(COMMON_IMG("normal_battle"), random_point=True, action="click")

    # 等待开始按钮出现
    ImageOps.wait_image(COMMON_IMG("start_battle"))
    wait(1.5)

    # 只有从主界面进入才有可能出现地图异常，因此调整地图放在此处
    # 当地图上无法同时识别到“机场”和“重型机场”时，进行地图调整
    is_adjusted = False
    if not ImageOps.locate_image(IMG("airplane")) or not ImageOps.locate_image(IMG("heavy_dust_airplane")):
        is_adjusted = True
        adjust_page()

    # 部署梯队
    deploy_team()

    # 当不是处理装备回合时交换zas
    if equipment_round:
        equipment_round = False
    else:
        exchange_zas()

    # 若地图进行过调整，此处需要重新调整一次
    if is_adjusted:
        adjust_page()


def adjust_page():
    """
    调整地图页面位置
    """
    WindowOps.move_to_window_center("少女前线")
    wait(0.2)
    MouseOps.scroll_mouse(-3, 20)
    wait(1)
    # 强制将地图移动至最左上角
    for _ in range(2):
        WindowOps.move_to_window_center("少女前线")
        MouseOps.drag_rel(800, 450, duration=1)
    # 标准化地图位置
    WindowOps.move_to_window_center("少女前线")
    MouseOps.drag_rel(-430, -180, duration=1)


def deploy_team():
    """
    部署梯队
    """
    # 部署第一梯队-------------------------------------------------------------
    ImageOps.find_image(IMG("airplane"), action="click")
    BasicTasks.click_confirm()
    # 部署第一梯队-------------------------------------------------------------

    # 部署第二梯队-------------------------------------------------------------
    ImageOps.find_image(IMG("team_1"), x_offset=-100, y_offset=620, action="click")
    BasicTasks.click_confirm()
    # 部署第二梯队-------------------------------------------------------------

    # 部署第三梯队-------------------------------------------------------------
    if temp_team:
        ImageOps.find_image(IMG("heavy_dust_airplane"), random_point=True, action="click")
        ImageOps.find_image(IMG("choose_team"), random_point=True, action="click")
        BasicTasks.click_confirm()
    # 部署第三梯队-------------------------------------------------------------


def exchange_zas():
    """
    交换第一和第二梯队的zas
    """
    # 选择第一梯队
    ImageOps.find_image(IMG("team_1"), x_offset=-33, y_offset=30, action="click")
    # 点击“队伍编成”
    BasicTasks.click_team_composition()
    # 等待加载
    wait(1)
    # 点击Zas
    ImageOps.find_image(IMG("Zas_M21"), random_point=True, action="click")
    # 筛选枪种为五星突击步枪
    BasicTasks.click_filter()
    BasicTasks.click_filter_five_star()
    ImageOps.find_image(IMG("ar"), random_point=True, action="click")
    BasicTasks.click_confirm_filter()
    # 等待稳定
    wait(0.5)

    # 寻找仓库里的zas并换队
    while True:
        if ImageOps.locate_image(IMG("zas_team1"), confidence=0.9) is not None:
            ImageOps.find_image(IMG("zas_team1"), confidence=0.9, action="click")
            break
        MouseOps.scroll_mouse(-1, 5)

    # 如果两只zas在同一页则直接选择
    if ImageOps.locate_image(IMG("zas_team2"), confidence=0.9) is not None:
        ImageOps.find_image(IMG("zas_team2"), confidence=0.9, action="click")
    else:
        # 不在同一页时先回滚一页，再继续往下查找
        MouseOps.scroll_mouse(1, 5)
        while True:
            if ImageOps.locate_image(IMG("zas_team2"), confidence=0.9) is not None:
                ImageOps.find_image(IMG("zas_team2"), confidence=0.9, action="click")
                break
            MouseOps.scroll_mouse(-1, 5)

    # 点击“确定”
    BasicTasks.click_confirm_depot()
    # 点击“返回”
    BasicTasks.click_back_button()
    # 等待返回
    wait(2)


def start_mission_actions():
    """
    包括点击开始作战及之后的所有操作
    """
    global equipment_round

    # 点击开始作战
    BasicTasks.click_start_battle()

    # 等待动画加载
    wait_in_range(2.2, 3)

    # 重新作战的情况下，点击开始任务才会出现装备爆仓提醒
    if upgrade_equipment:
        # 配置升级装备时，走装备升级窗口处理流程
        if deal_unexpected_windows_upgrade_equipment():
            equipment_round = True
            return
    else:
        # 未配置升级装备时，走普通意外窗口处理流程
        if deal_unexpected_windows():
            equipment_round = True
            return

    # 第二梯队补充并撤离----------------------------------------------------------
    ImageOps.find_image(IMG("team_2"), x_offset=-33, y_offset=30, action="click")
    wait(0.5)
    MouseOps.one_left_click()
    BasicTasks.click_supply_button()
    ImageOps.find_image(IMG("team_2"), x_offset=-33, y_offset=30, action="click")
    BasicTasks.click_retreat_button()
    BasicTasks.click_confirm()
    # 第二梯队补充并撤离----------------------------------------------------------

    # 第一梯队开启计划模式---------------------------------------------------------
    ImageOps.find_image(IMG("team_1"), x_offset=-33, y_offset=30, action="click")
    BasicTasks.click_enable_plan_mode()
    ImageOps.find_image(IMG("team_1"), x_offset=-140, y_offset=230, action="click")
    ImageOps.find_image(IMG("team_1"), x_offset=-100, y_offset=620, action="click")
    # 第一梯队开启计划模式---------------------------------------------------------

    # 执行计划
    BasicTasks.click_execute_plan()

    # 等待开始执行
    wait(2)

    # 等待计划模式重新出现
    ImageOps.wait_image(COMMON_IMG("enable_plan_mode"))

    # 第一梯队撤离
    if temp_team:
        ImageOps.find_image(IMG("team_1"), x_offset=-33, y_offset=30, action="click")
        BasicTasks.click_retreat_button()
        BasicTasks.click_confirm()

    # 终止作战并重新开始
    BasicTasks.click_cancel_battle_white()
    BasicTasks.click_restart_battle()


def return_to_main_menu():
    """
    任务结束后，返回主菜单
    """
    # 等待动画加载
    wait_in_range(2.2, 3)
    BasicTasks.click_select_mission()
    BasicTasks.click_back_button()


def check_action_limit(action_count, max_actions):
    """
    检查执行次数是否超过限制
    """
    return action_count > max_actions


def main(max_actions=999):
    """
    :param max_actions:最大执行次数
    """
    set_resource_subdir(resource_subdir)
    print_banner("[8-1 midnight 双Zas拖尸] 自动化执行开始")
    logging.info(f"[配置] 使用狗粮队: {temp_team}")
    logging.info(f"[配置] 开启装备升级: {upgrade_equipment}")
    WindowOps.activate_window("少女前线")  # 激活游戏窗口
    action_count = 1  # 初始化执行计数
    action_limit = False  # 标记是否达到执行次数

    while True:
        logging.info("[8-1 midnight 双Zas拖尸] 从主菜单进入任务")
        logging.info(f"[计数] 当前执行次数: {action_count}")
        menu_enter_mission()  # 丛主菜单进入任务
        start_mission_actions()  # 进入任务后的所有操作
        action_count += 1

        while True:
            # 检查执行次数是否超过限制
            action_limit = check_action_limit(action_count, max_actions)

            # 任务完成并且没有达到最大执行次数,重复进行任务
            if not action_limit:
                logging.info("[8-1 midnight 双Zas拖尸] 重复进行任务")
                logging.info(f"[计数] 当前执行次数: {action_count}")
                exchange_zas()
                start_mission_actions()
                # 处理意外窗口后，从主菜单重新开始
                if equipment_round:
                    break
                action_count += 1
            else:
                return_to_main_menu()
                print(f"[终止] 已达到最大执行次数 {max_actions},程序结束")

                print_banner("[8-1 midnight 双Zas拖尸] 自动化执行结束")
                raise MissionFinished()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"[异常] 程序发生错误: {e} ")
