from game_ops.composed_tasks import *

"""
1-1 刷友情点数
说明：
    - 第一梯队放狗粮队
"""

# 所用的资源图片的文件夹名称
set_resource_subdir("1_1")


def menu_enter_mission():
    """
    从主菜单进入任务
    """

    # 点击“首页-战斗”
    BasicTasks.click_home_battle_button()

    # 如果第一战役没被激活，则点击第一战役
    if not ImageOps.wait_image(IMG("battle_1_active"), confidence=0.9, timeout=1.5):
        # 切换至作战任务界面
        ImageOps.find_image(IMG("combat_mission"), action="click")

        # 如果没找到第一战役，滚动页面到顶部
        if not ImageOps.find_image(IMG("battle_1"), confidence=0.95, timeout=1, action="click"):
            ImageOps.find_image(IMG("mark_image"), x_offset=300, y_offset=-200, action="move")
            wait(0.2)
            MouseOps.scroll_mouse(3, 20)
            wait(0.5)
            ImageOps.find_image(IMG("battle_1"), confidence=0.95, action="click")

    # 设置成普通难度
    ImageOps.find_image(IMG("mark_image"), x_offset=1100, y_offset=-600, action="click")

    # 点击1_1
    ImageOps.find_image(IMG("battle_1_1"), action="click")

    # 等待并点击“普通作战”
    ImageOps.find_image(COMMON_IMG("normal_battle"), random_point=True, action="click")


def repeat_mission():
    """
    重复进行入任务
    """
    # 点击1_1
    ImageOps.find_image(IMG("battle_1_1"), action="click")

    # 等待并点击“普通作战”
    ImageOps.find_image(COMMON_IMG("normal_battle"), random_point=True, action="click")


def start_mission_actions():
    """
    进入作战场景后的所有操作
    """
    # 等待"开始作战"按钮出现
    ImageOps.wait_image(COMMON_IMG("start_battle"))
    wait(1.5)

    # 部署第一梯队并开始作战,梯队已经在场上(重复作战)就直接开始作战------------------------------------------
    if ImageOps.locate_image(IMG("team_1")) is None:
        # 寻找指挥部,如果没找到,就缩放地图
        if ImageOps.locate_image(IMG("hq_base"), confidence=0.70) is None:
            ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, action="move")
            MouseOps.scroll_mouse(-1, 50)

        # 点击指挥部,部署第一梯队
        ImageOps.find_image(IMG("hq_base"), confidence=0.70, random_point=True, action="click")
        BasicTasks.click_confirm()  # 点击确认部署
        wait(0.5)

    BasicTasks.click_start_battle()  # 点击开始作战
    wait_in_range(2.2, 3)  # 等待动画加载
    # 部署第一梯队并开始作战,梯队已经在场上(重复作战)就直接开始作战------------------------------------------

    # 选中第一梯队,向前方移动一格---------------------------------------------------------------------
    ImageOps.find_image(IMG("team_1"), x_offset=-30, y_offset=30, action="click")
    wait(0.5)
    ImageOps.find_image(IMG("team_1"), x_offset=200, y_offset=-110, action="click")
    # 选中第一梯队,向前方移动一格---------------------------------------------------------------------

    # 关闭弹窗,持续点击,直到 team_1 出现
    wait(1)
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=500, y_offset=-200)
    ImageOps.hold_click_until_image_appear(IMG("team_1"), interval=1, timeout=3)
    wait(1)


    # 部署好友支援----------------------------------------------------------------------------------
    # 清除选择
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                        action="click")
    ImageOps.find_image(IMG("team_1"), x_offset=-260, y_offset=150, action="click")
    ImageOps.find_image(IMG("assist_echelon"), random_point=True, action="click")  # 点击"支援梯队"
    ImageOps.find_image(IMG("select_friend_unit"), y_offset=300, action="click")  # 选择第二个支援队伍
    BasicTasks.click_confirm()  # 点击确认部署
    wait(0.5)
    # 部署好友支援----------------------------------------------------------------------------------

    # 把好友支援切换成"消灭敌人"模式-----------------------------------------------------------------
    # 清除选择
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                        action="click")
    ImageOps.find_image(IMG("team_1"), x_offset=-260, y_offset=150, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_1"), x_offset=-260, y_offset=150, action="click")
    BasicTasks.click_eliminate_enemy_mode()  # 点击消灭敌人模式
    wait(0.5)
    # 把好友支援切换成"消灭敌人"模式-----------------------------------------------------------------

    # 把狗粮队跟好友换位,结束回合-----------------------------------------------------------------
    # 清除选择
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                        action="click")
    ImageOps.find_image(IMG("team_1"), x_offset=-30, y_offset=30, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_1"), x_offset=-260, y_offset=150, action="click")
    ImageOps.find_image(COMMON_IMG("switch_button"), action="click")
    wait(0.5)
    BasicTasks.click_end_round_button()  # 结束回合
    # 把狗粮队跟好友换位,结束回合-----------------------------------------------------------------

    # # 持续点击,直到“关卡1_1”再次出现
    ImageOps.hold_click_until_image_appear(IMG("battle_1_1"), interval=1)


def return_to_main_menu():
    """
    任务结束后,返回主菜单
    """
    # 点击“返回按钮”
    ImageOps.hold_click_until_image_appear(COMMON_IMG("back_button"), interval=0.5, click_after=True)


# 检查执行次数是否超过限制
def check_action_limit(action_count, max_actions):
    if action_count > max_actions:
        return True


def main(max_actions=5):
    """
    一天最多刷5次,超过5次后不会获得友情点数
    :param max_actions: 最大执行次数
    :return:
    """
    print_banner("[1-1 刷友情点数] 自动化执行开始")
    WindowOps.activate_window("少女前线")  # 激活游戏窗口
    action_count = 1  # 初始化执行计数
    action_limit = False

    while True:

        logging.info("[1-1 刷友情点数] 从主菜单进入任务")
        logging.info(f"[计数] 当前执行次数: {action_count}")
        menu_enter_mission()  # 从主菜单进入任务
        start_mission_actions()  # 进入任务后的所有操作
        action_count += 1

        while True:
            # 检查执行次数是否超过限制
            if not action_limit:
                action_limit = check_action_limit(action_count, max_actions)

            # 任务完成并且没有达到最大执行次数,重复进行任务
            if not action_limit:
                logging.info("[1-1 刷友情点数] 重复进行任务")
                logging.info(f"[计数] 当前执行次数: {action_count}")
                repeat_mission()  # 重复进行任务
                # 处理意外窗口后,从主菜单重新开始
                if deal_unexpected_windows():
                    break
                start_mission_actions()  # 进入任务后的所有操作
                action_count += 1
            else:
                return_to_main_menu()
                print(f"[终止] 已达到最大执行次数 {max_actions},程序结束")

                print_banner("[1-1 刷友情点数] 自动化执行结束")
                exit()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"[异常] 程序发生错误: {e}")
