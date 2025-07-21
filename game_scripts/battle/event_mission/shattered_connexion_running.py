from game_ops.composed_tasks import *

"""
裂变链接-认知裂变1 战斗EX 跑步机
说明:
    - 把要练级的队伍放在一,二,三梯队。
        - 不知道跑步机是什么或者不清楚队伍配置的话,可以参考以下链接:https://www.bilibili.com/video/BV1aJMUeHEVR
    - 确保好友支援里有白包子
    - 关闭"回合结束二次确认"和"自动补给"
    - 进入计划模式,设置好路径后,可以隐藏游戏窗口,等全部执行后再切换回来,只有计划模式完全执行后,才会重新操作
"""

# 所用的资源图片的文件夹名称
set_resource_subdir("shattered_connexion_running")


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
    wait(1)  # 非常重要,等待动画加载
    ImageOps.find_image(IMG("shattered_connexion"), random_point=True, action="click")

    # ==========================
    # 从"裂变链接"活动 进入 "底层归乡2 战斗EX"任务
    # ==========================

    # 等待"裂变链接-底层归乡2 战斗EX"的logo出现(难度选择上面的那朵花)
    ImageOps.wait_image(IMG("mark_image_logo"))
    # 如果没有找到困难难度,说明当前是普通难度,点击切换成困难难度
    if ImageOps.locate_image(IMG("difficulty_hard"), confidence=0.9) is None:
        ImageOps.find_image(IMG("difficulty_normal"), random_point=True, action="click")
        wait(0.5)

    # 寻找"认知裂变 1 战斗EX"按钮,如果找到了就点击
    location = ImageOps.locate_image(IMG("cognitive_fission_ex"), confidence=0.9)
    if location is not None:
        MouseOps.left_click_at(location.x, location.y)
        BasicTasks.click_start_the_task()  # 点击"确认出击"
    else:
        # 没找到就回到章节目录
        if ImageOps.locate_image(IMG("back_button")) is not None:
            ImageOps.find_image(IMG("back_button"), random_point=True, action="click")
            wait(1.5)
        else:
            ImageOps.find_image(IMG("mark_image_logo"), action="move")

        # 缩放章节目录
        MouseOps.scroll_mouse(-1, 15)
        while True:
            # 寻找"第一章节",找不到就拖动画面到底部,通过偏移量来点击"第三章节"
            location_chapter_1 = ImageOps.locate_image(IMG("chapter_1"))
            if location_chapter_1 is not None:
                MouseOps.left_click_at(location_chapter_1.x + -240, location_chapter_1.y + -380)
                break
            ImageOps.find_image(IMG("mark_image_logo"), x_offset=200, y_offset=100, action="move")
            MouseOps.drag_rel(0, -500)

        ImageOps.find_image(IMG("mark_image_logo"), action="move")
        wait(1)
        # 缩放任务列表
        MouseOps.scroll_mouse(-1, 20)

        while True:
            # 寻找"认知裂变 1 战斗EX"按钮,如果找到了就点击,没找到就拖动画面到最左边
            location = ImageOps.locate_image(IMG("cognitive_fission_ex"), confidence=0.9)
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
    wait(1)
    # 点击"再次作战"
    BasicTasks.click_repeat_battle()
    wait(1)


def start_mission_actions():
    """
    进入作战场景后的所有操作
    """
    # 等待"开始作战"按钮出现
    ImageOps.wait_image(COMMON_IMG("start_battle"))
    wait(1.5)

    # 部署一,二梯队并开始作战,梯队已经在场上(重复作战)就直接开始作战-----------------------------------------
    if ImageOps.locate_image(IMG("team_1")) is None:
        # 寻找指挥部,如果没找到,就缩放地图
        if ImageOps.locate_image(IMG("hq_base"), confidence=0.70) is None:
            MouseOps.scroll_mouse(-1, 50)

        # 点击重型机场,部署第一梯队
        ImageOps.find_image(IMG("large_airport"), confidence=0.70, random_point=True, action="click")
        ImageOps.find_image(IMG("select_echelon"), action="click")  # 点击"选择梯队"
        BasicTasks.click_confirm()  # 点击确认部署
        wait(0.5)

        # 点击指挥部,部署第二梯队
        ImageOps.find_image(IMG("hq_base"), confidence=0.70, random_point=True, action="click")
        BasicTasks.click_confirm()  # 点击确认部署
        wait(0.5)

    BasicTasks.click_start_battle()  # 点击开始作战
    wait_in_range(2.2, 3)  # 等待动画加载
    # 部署一,二梯队并开始作战,梯队已经在场上(重复作战)就直接开始作战-----------------------------------------

    # 选中第一梯队,向右下方移动一格--------------------------------------------------------------------
    ImageOps.find_image(IMG("team_1"), x_offset=-30, y_offset=30, action="click")
    wait(0.5)
    ImageOps.find_image(IMG("team_1"), x_offset=110, y_offset=60, action="click")
    wait(2)
    # 选中第一梯队,向右下方移动一格--------------------------------------------------------------------

    # 选中第二梯队,向右下方移动一格--------------------------------------------------------------------
    ImageOps.find_image(IMG("team_2"), x_offset=-30, y_offset=30, action="click")
    wait(0.5)
    ImageOps.find_image(IMG("team_2"), x_offset=15, y_offset=130, action="click")
    wait(2)
    # 选中第二梯队,向右下方移动一格--------------------------------------------------------------------

    # 点击重型机场,部署支援梯队(白包子)----------------------------------------------------------------
    # 清除选择
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                        action="click")
    ImageOps.find_image(IMG("large_airport"), confidence=0.70, random_point=True, action="click")  # 点击重型机场
    wait(0.2)
    ImageOps.find_image(IMG("select_echelon"), action="click")  # 点击"选择梯队"
    wait(0.2)
    ImageOps.find_image(IMG("assist_echelon"), random_point=True, action="click")  # 点击"支援梯队"
    # 移动鼠标到"友军选择"下方
    ImageOps.find_image(IMG("select_friend_unit"), y_offset=200, random_point=True, action="move")
    while True:
        # 寻找白包子...
        if ImageOps.locate_image(IMG("baozi")):
            ImageOps.find_image(IMG("baozi"), random_point=True, action="click")
            break
        MouseOps.scroll_mouse_py(-3)
    BasicTasks.click_confirm()  # 点击确认部署
    wait(0.5)
    # 点击重型机场,部署支援梯队(白包子)----------------------------------------------------------------

    # 把白包子设置成"消灭敌人"模式--------------------------------------------------------------------
    ImageOps.find_image(IMG("team_1"), x_offset=-200, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_1"), x_offset=-200, action="click")
    wait(0.2)
    BasicTasks.click_eliminate_enemy_mode()  # 点击消灭敌人模式
    wait(0.5)
    # 把白包子设置成"消灭敌人"模式--------------------------------------------------------------------

    # 点击指挥部,部署第三梯队------------------------------------------------------------------------
    # 清除选择
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                        action="click")
    ImageOps.find_image(IMG("hq_base"), confidence=0.70, random_point=True, action="click")
    BasicTasks.click_confirm()  # 点击确认部署
    # 点击指挥部,部署第三梯队------------------------------------------------------------------------

    # 计划模式,设置路径并执行------------------------------------------------------------------------
    # 清除选择
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                        action="click")

    BasicTasks.click_enable_plan_mode()  # 点击计划模式
    wait(0.2)
    # 第一梯队
    ImageOps.find_image(IMG("team_1"), x_offset=-30, y_offset=30, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_1"), x_offset=240, y_offset=50, action="click")

    # 清除选择
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                        action="click")

    # 第二梯队
    ImageOps.find_image(IMG("team_2"), x_offset=-30, y_offset=30, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_2"), x_offset=300, y_offset=0, action="click")

    # 清除选择
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                        action="click")

    # 第三梯队
    ImageOps.find_image(IMG("team_3"), x_offset=-30, y_offset=30, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_3"), x_offset=180, y_offset=100, action="click")
    wait(0.2)
    BasicTasks.click_next_turn()  # 点击下一回合
    wait(0.2)
    ImageOps.find_image(IMG("team_2"), x_offset=-30, y_offset=30, action="click")
    BasicTasks.click_move_button()  # 点击移动按钮

    BasicTasks.click_execute_plan()  # 点击执行计划
    # 计划模式,设置路径并执行------------------------------------------------------------------------

    # 等待第三回合开始
    if ImageOps.wait_image(IMG("turn_3"), confidence=0.85):
        wait(10)

    # 把白包子设置成"待机"模式-----------------------------------------------------------------------
    # 清除选择
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                        action="click")
    wait(0.5)
    ImageOps.find_image(IMG("team_1"), x_offset=-180, y_offset=-10, action="click")
    wait(0.5)
    ImageOps.find_image(IMG("team_1"), x_offset=-180, y_offset=-10, action="click")
    BasicTasks.click_standby_mode()  # 点击待机模式
    # 把白包子设置成"待机"模式-----------------------------------------------------------------------

    # 计划模式,跑步机,启动!-------------------------------------------------------------------------
    # 清除选择
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                        action="click")
    wait(0.5)
    BasicTasks.click_enable_plan_mode()  # 点击计划模式
    wait(0.2)
    ImageOps.find_image(IMG("team_3"), x_offset=-30, y_offset=30, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_3"), x_offset=120, y_offset=-10, action="click")
    ImageOps.find_image(COMMON_IMG("next_turn"), action="move")  # 移动鼠标到"下一回合"按钮的位置
    for i in range(80):
        MouseOps.one_left_click()
    BasicTasks.click_execute_plan()  # 点击执行计划
    # 计划模式,跑步机,启动!-------------------------------------------------------------------------


def check_image_for_10_seconds(image_path):
    """
    持续检测图像 10 秒，如果一直存在则返回 True，否则返回 False。
    """
    start_time = time.time()
    while time.time() - start_time < 10:
        time.sleep(1)
        if not ImageOps.locate_image(image_path):
            return False  # 只要有一次没找到，就立即返回 False
    return True


def loop_mission():
    """
    持续执行跑步机任务,直到战斗结束
    :return:
    """
    # 检测计划模式是否结束
    while True:
        # 检测到"再次作战"按钮,表示一个流程全部结束
        if ImageOps.locate_image(COMMON_IMG("repeat_battle")):
            return True
        # 连续10秒检测到"战斗结束标志",表示一次跑步完成
        if check_image_for_10_seconds(IMG("battle_end_flag")):
            break
    ImageOps.find_image(IMG("battle_end_flag"), x_offset=300, y_offset=50, random_point=True, action="click")
    wait(8)  # 等待战斗结束动画

    # 计划模式结束后重新设置路径

    # 清除选择
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                        action="click")
    wait(0.5)
    BasicTasks.click_enable_plan_mode()  # 点击计划模式
    wait(0.2)
    ImageOps.find_image(IMG("team_3"), x_offset=-30, y_offset=30, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_3"), x_offset=50, y_offset=-80, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_3"), x_offset=-30, y_offset=30, action="click")
    ImageOps.find_image(COMMON_IMG("next_turn"), action="move")  # 移动鼠标到"下一回合"按钮的位置
    for i in range(80):
        MouseOps.one_left_click()
    BasicTasks.click_execute_plan()  # 点击执行计划


def return_to_main_menu():
    """
    任务结束后,返回主菜单
    """
    if ImageOps.locate_image(COMMON_IMG("repeat_battle")):
        wait(1)
    # 点击一次空白处
    ImageOps.find_image(COMMON_IMG("repeat_battle"), x_offset=300, action="click")
    # 点击“返回按钮”
    BasicTasks.click_back_button()


# 检查执行次数是否超过限制
def check_action_limit(action_count, max_actions):
    if action_count > max_actions:
        return True


def main(max_actions=2):
    """
    :param max_actions: 最大执行次数
    :return:
    """
    print_banner("[裂变链接-认知裂变1 战斗EX 跑步机自动执行] 自动化执行开始")
    WindowOps.activate_window("少女前线")  # 激活游戏窗口
    action_count = 1  # 初始化执行计数
    action_limit = False

    while True:

        logging.info("[裂变链接-认知裂变1 战斗EX 跑步机自动执行] 从主菜单进入任务")
        logging.info(f"[计数] 当前执行次数: {action_count}")
        menu_enter_mission()  # 从主菜单进入任务
        start_mission_actions()  # 开始第一轮跑步的所有操作
        loop_mission()  # 持续执行跑步机任务,直到战斗结束
        action_count += 1

        while True:
            # 检查执行次数是否超过限制
            if not action_limit:
                action_limit = check_action_limit(action_count, max_actions)

            # 任务完成并且没有达到最大执行次数,重复进行任务
            if not action_limit:
                logging.info("[裂变链接-认知裂变1 战斗EX 跑步机自动执行] 重复进行任务")
                logging.info(f"[计数] 当前执行次数: {action_count}")
                repeat_mission()  # 重复进行任务
                # 处理意外窗口后,从主菜单重新开始
                if deal_unexpected_windows():
                    break
                start_mission_actions()  # 开始第一轮跑步的所有操作
                loop_mission()  # 持续执行跑步机任务,直到战斗结束
                action_count += 1
            else:
                return_to_main_menu()
                print(f"[终止] 已达到最大执行次数 {max_actions},程序结束")

                print_banner("[裂变链接-认知裂变1 战斗EX 跑步机自动执行] 自动化执行结束")
                exit()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"[异常] 程序发生错误: {e}")
