from game_ops.composed_tasks import *

"""
裂变链接-底层归乡2 战斗EX 自动打捞(MP41)
说明:
    - 把主力队放在第一梯队,狗粮队放在第二梯队。
    - 推荐队伍 三改 Zas M21,带光学瞄具, 五星必杀2空降妖精(实测四星的空降妖精也行)
    - 确保第一次进入战斗前,人形未满员(第一次不做自动回收处理”。
    - 关闭"回合结束二次确认"和"自动补给"
"""

# 所用的资源图片的文件夹名称
set_resource_subdir("shattered_connexion")


def menu_enter_mission():
    """
    从主菜单进入任务
    """

    # ==========================
    # 从主菜单进入"裂变链接"活动
    # ==========================

    # 点击“首页-战斗”
    BasicTasks.click_home_battle_button()

    wait(1)

    # 点击“常驻活动”
    ImageOps.find_image(IMG("mark_image"), y_offset=-200, action="click")
    # 点击“裂变链接”
    if not ImageOps.wait_image(IMG("shattered_connexion"), timeout=1):
        ImageOps.find_image(IMG("mark_image"), x_offset=200, y_offset=-660, action="move")
        MouseOps.scroll_mouse(3)
        wait(0.5)
        MouseOps.one_left_click()
    ImageOps.find_image(IMG("shattered_connexion"), random_point=True, action="click")

    # ==========================
    # 从"裂变链接"活动 进入 "底层归乡2 战斗EX"任务
    # ==========================

    ImageOps.wait_image(IMG("mark_image_logo"))
    if ImageOps.locate_image(IMG("difficulty_hard"), confidence=0.9) is None:
        ImageOps.find_image(IMG("difficulty_normal"), random_point=True, action="click")
        wait(0.5)

    location = ImageOps.locate_image(IMG("return_to_base_2_ex"), confidence=0.9)
    if location is not None:
        MouseOps.left_click_at(location.x, location.y)
        BasicTasks.click_start_the_task()  # 点击"确认出击"
    else:
        if ImageOps.locate_image(IMG("back_button")) is not None:
            ImageOps.find_image(IMG("back_button"), random_point=True, action="click")
            wait(2)
        else:
            ImageOps.find_image(IMG("mark_image_logo"), action="move")

        MouseOps.scroll_mouse(-1, 15)
        while True:
            location_chapter_5 = ImageOps.locate_image(IMG("chapter_5"))
            if location_chapter_5 is not None:
                MouseOps.left_click_at(location_chapter_5.x + 300, location_chapter_5.y + 200)
                break
            ImageOps.find_image(IMG("mark_image_logo"), x_offset=200, y_offset=-400, action="move")
            MouseOps.drag_rel(0, 500)

        ImageOps.find_image(IMG("mark_image_logo"), action="move")
        wait(2)
        MouseOps.scroll_mouse(-1, 20)

        while True:
            location = ImageOps.locate_image(IMG("return_to_base_2_ex"), confidence=0.9)
            if location is not None:
                MouseOps.left_click_at(location.x, location.y)
                BasicTasks.click_start_the_task()  # 点击"确认出击"
                break
            ImageOps.find_image(IMG("mark_image_logo"), x_offset=200, y_offset=200, action="move")
            MouseOps.drag_rel(1000, 0)


def repeat_mission():
    """
    重复进行入任务
    """
    wait(2)
    # 点击"终止作战-白色按钮"
    BasicTasks.click_cancel_battle_white()
    # 点击"重新作战"
    BasicTasks.click_restart_battle()


def start_mission_actions():
    """
    进入作战场景后的所有操作
    """
    # 等待"开始作战"按钮出现
    ImageOps.wait_image(COMMON_IMG("start_battle"))

    # 部署第一梯队并开始作战,第一梯队已经在场上(重复作战)就直接开始作战------------------------------------
    if ImageOps.locate_image(IMG("team_1")) is None:
        # 寻找指挥部,如果没找到,就缩放地图
        if ImageOps.locate_image(IMG("airport"), confidence=0.75) is None:
            MouseOps.scroll_mouse(-1, 50)
        ImageOps.find_image(IMG("airport"), confidence=0.75, random_point=True, action="click")
        BasicTasks.click_confirm()  # 点击确认部署
    BasicTasks.click_start_battle()  # 点击开始作战
    wait_in_range(2.2, 3)  # 等待动画加载
    # 部署第一梯队并开始作战,第一梯队已经在场上(重复作战)就直接开始作战------------------------------------

    # 选中第一梯队,并补给----------------------------------------------------------------------------
    ImageOps.find_image(IMG("team_1"), x_offset=-30, y_offset=30, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_1"), x_offset=-30, y_offset=30, action="click")  # 选中team1
    BasicTasks.click_supply_button()
    # 选中第一梯队,并补给----------------------------------------------------------------------------

    # 让第一梯队向上一格,并部署第二梯队-----------------------------------------------------------------
    ImageOps.find_image(IMG("team_1"), x_offset=-36, y_offset=-96, action="click")
    wait(1)
    ImageOps.find_image(IMG("airport"), confidence=0.75, random_point=True, action="click")
    wait(1)
    ImageOps.find_image(IMG("deploy_button"), random_point=True, action="click")
    BasicTasks.click_confirm()
    # 让第一梯队向上一格,并部署第二梯队-----------------------------------------------------------------

    # 结束回合,并等待战斗结束-------------------------------------------------------------------------
    BasicTasks.click_end_round_button()  # 点击结束回合
    ImageOps.find_image(IMG("battle_end_flag"), x_offset=200, y_offset=300, action="move")  # 移动到战斗结束标志
    ImageOps.hold_click_until_image(COMMON_IMG("mark_image_794"), interval=0.8)  # 持续点击直到794(战斗结束的标识)出现
    wait_in_range(8.5, 9.5)
    # 结束回合,并等待战斗结束-------------------------------------------------------------------------

    # 让第二梯队撤离---------------------------------------------------------------------------------
    ImageOps.find_image(IMG("team_2"), x_offset=-30, y_offset=30, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_2"), x_offset=-30, y_offset=30, action="click")
    BasicTasks.click_retreat_button()
    BasicTasks.click_confirm()
    wait(2)
    # 让第二梯队撤离---------------------------------------------------------------------------------

    # 开启计划模式,让第一梯队沿着路径点执行计划-----------------------------------------------------------
    BasicTasks.click_enable_plan_mode()
    ImageOps.find_image(IMG("team_1"), x_offset=-30, y_offset=30, action="click")  # 选中team1
    ImageOps.find_image(IMG("team_1"), x_offset=120, y_offset=30, action="click")  # 往右一格
    ImageOps.find_image(IMG("team_1"), x_offset=120, y_offset=-96, action="click")  # 向右上一格
    ImageOps.find_image(IMG("team_1"), x_offset=-196, y_offset=-96, action="click")  # 向左上一格
    BasicTasks.click_execute_plan()
    # 开启计划模式,让第一梯队沿着路径点执行计划-----------------------------------------------------------

    while True:

        # 检测分享按钮的出现,战斗结束后会出现分享按钮,如果有新的人形被打捞,自动战斗则会停止
        share_button = ImageOps.locate_image(COMMON_IMG("share_button"))
        if share_button is not None:
            MouseOps.move_to(share_button.x + 200, share_button.y + 300)
            ImageOps.hold_click_until_image(COMMON_IMG("mark_image_794"), interval=0.8)  # 持续点击直到794(战斗结束的标识)出现

        # 等待战斗结束
        if ImageOps.locate_image(IMG("mission_completed_mark"), confidence=0.95) is not None:
            break


def return_to_main_menu():
    """
    任务结束后,返回主菜单
    """
    wait(2)
    # 点击"终止作战-白色按钮"
    BasicTasks.click_cancel_battle_white()
    # 点击"终止作战-橙色按钮"
    BasicTasks.click_cancel_battle_orange()
    # 点击“返回按钮”
    BasicTasks.click_back_button()


# 检查执行次数是否超过限制
def check_action_limit(action_count, max_actions):
    if action_count >= max_actions:
        return True


def main(max_actions=6):
    """
    :param max_actions: 最大执行次数
    :return:
    """
    print_banner("[裂变链接-底层归乡2 战斗EX 自动打捞] 自动化执行开始")
    WindowOps.activate_window("少女前线")  # 激活游戏窗口
    action_count = 1  # 初始化执行计数
    action_limit = False

    while True:

        logging.info("[裂变链接-底层归乡2 战斗EX 自动打捞] 从主菜单进入任务")
        logging.info(f"[计数] 当前执行次数: {action_count}")
        menu_enter_mission()
        start_mission_actions()

        while True:
            # 检查执行次数是否超过限制
            if not action_limit:
                action_limit = check_action_limit(action_count, max_actions)

            # 任务完成并且没有达到最大执行次数,重复进行任务
            if not action_limit:
                logging.info("[裂变链接-底层归乡2 战斗EX 自动打捞] 重复进行任务")
                logging.info(f"[计数] 当前执行次数: {action_count}")
                repeat_mission()
                wait(2)

                # 处理意外窗口后,从主菜单重新开始
                if deal_unexpected_windows():
                    break

                start_mission_actions()
                action_count += 1

            # 任务完成并且达到最大执行次数,退出程序

            else:
                return_to_main_menu()
                print(f"[终止] 已达到最大执行次数 {max_actions},程序结束")

                print_banner("[裂变链接-底层归乡2 战斗EX 自动打捞] 自动化执行结束")
                exit()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"[异常] 程序发生错误: {e}")
