from core_ops.composed.composed_ops import *
from core_ops.utils.exceptions import MissionFinished
from game_ops.composed_tasks import *

"""
裂变链接-底层归乡2 战斗EX 自动打捞(MP41)
说明:
    - 把主力队放在第一梯队,狗粮队放在第二梯队。
    - 推荐队伍 三改 Zas M21,带光学瞄具, 五星必杀2空降妖精(实测四星的空降妖精也行)
    - 确保第一次进入战斗前,仓库人形未满员(第一次不做自动回收处理”。
    - 关闭"回合结束二次确认"和"自动补给"
"""

# 所用的资源图片的文件夹名称
resource_subdir = "shattered_connexion"


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
    BasicTasks.click_campaign()

    # 等待动画加载
    wait(1)

    # 点击“‘裂变链接’”
    if not ImageOps.find_image(IMG("shattered_connexion"), random_point=True, action="click", timeout=1):

        # 点击“‘裂变链接’活动入口”
        if (not ImageOps.locate_image(IMG("shattered_connexion_entry_active")) and
                not ImageOps.find_image(IMG("shattered_connexion_entry"), action="click", wait=False)):
            ImageOps.find_image(IMG("mark_image"), x_offset=200, y_offset=-660, action="move")
            while True:
                MouseOps.scroll_mouse(-3)
                wait(0.5)
                if ImageOps.locate_image(IMG("shattered_connexion_entry")):
                    ImageOps.find_image(IMG("shattered_connexion_entry"), action="click")
                    break
                if ImageOps.locate_image(IMG("shattered_connexion_entry_active")):
                    break

        wait(1)  # 非常重要,等待动画加载

        # 点击“‘裂变链接’”
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

    # 寻找"底层归乡2 战斗EX"按钮,如果找到了就点击
    location = ImageOps.locate_image(IMG("return_to_base_2_ex"), confidence=0.9)
    if location is not None:
        MouseOps.left_click_at(location.x, location.y)
        BasicTasks.click_start_the_task()  # 点击"确认出击"
    else:
        # 没找到就回到章节目录
        if ImageOps.locate_image(IMG("back_button")) is not None:
            ImageOps.find_image(IMG("back_button"), random_point=True, action="click")
            wait(2)
        else:
            ImageOps.find_image(IMG("mark_image_logo"), action="move")

        # 缩放章节目录
        MouseOps.scroll_mouse(-1, 15)
        while True:
            # 寻找"第五章节",找不到就拖动画面到顶部,通过偏移量来点击"第四章节"
            location_chapter_5 = ImageOps.locate_image(IMG("chapter_5"))
            if location_chapter_5 is not None:
                MouseOps.left_click_at(location_chapter_5.x + 300, location_chapter_5.y + 200)
                break
            ImageOps.find_image(IMG("mark_image_logo"), x_offset=200, y_offset=-400, action="move")
            MouseOps.drag_rel(0, 500)

        ImageOps.find_image(IMG("mark_image_logo"), action="move")
        wait(2)
        # 缩放任务列表
        MouseOps.scroll_mouse(-1, 20)

        while True:
            # 寻找"底层归乡2 战斗EX"按钮,如果找到了就点击,没找到就拖动画面到最左边
            location = ImageOps.locate_image(IMG("return_to_base_2_ex"), confidence=0.9)
            if location is not None:
                MouseOps.left_click_at(location.x, location.y)
                BasicTasks.click_start_the_task()  # 点击"确认出击"
                # 出现确定按钮,则点击(每天第一次进入关卡时会出现)
                ImageOps.find_image(COMMON_IMG("confirm"), confidence=0.7, action="click", timeout=1)
                break
            ImageOps.find_image(IMG("mark_image_logo"), x_offset=200, y_offset=200, action="move")
            MouseOps.drag_rel(1000, 0)


def repeat_mission():
    """
    重复进行入任务
    :return: True
    """
    wait(2)
    # 点击"终止作战-白色按钮"
    BasicTasks.click_cancel_battle_white()
    # 点击"重新作战"
    BasicTasks.click_restart_battle()
    # 为什么要把 点击开始作战 移到这里?因为仓库满了后,是点了"开始作战"后才弹出的
    # 等待"开始作战"按钮出现
    ImageOps.wait_image(COMMON_IMG("start_battle"))
    wait(2)
    # 点击开始作战
    BasicTasks.click_start_battle()
    return True


def start_mission_actions(repeat=False):
    """
    进入作战场景后的所有操作
    :param repeat: 是否是重复作战,如果是重复作战,则不需要等待"开始作战"按钮出现
    """
    # 如果不是重复作战(首次进入任务)
    if not repeat:
        # 等待"开始作战"按钮出现
        ImageOps.wait_image(COMMON_IMG("start_battle"))
        wait(2)

        # 部署第一梯队并开始作战已经在场上就直接开始作战---------------------------------------------------
        # 寻找指挥部,如果没找到,就缩放地图
        if ImageOps.locate_image(IMG("hq_base"), confidence=0.75) is None:
            WindowOps.move_to_window_center("少女前线")
            MouseOps.scroll_mouse(-1, 60)
        ImageOps.find_image(IMG("hq_base"), confidence=0.75, random_point=True, action="click")
        BasicTasks.click_confirm()  # 点击确认部署
        BasicTasks.click_start_battle()  # 点击开始作战
        # 部署第一梯队并开始作战已经在场上就直接开始作战---------------------------------------------------

    wait_in_range(2.2, 3)  # 等待动画加载

    # 选中第一梯队,并补给----------------------------------------------------------------------------
    ImageOps.find_image(IMG("team_1"), x_offset=-30, y_offset=30, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_1"), x_offset=-30, y_offset=30, action="click")  # 选中team1
    BasicTasks.click_supply_button()
    # 选中第一梯队,并补给----------------------------------------------------------------------------

    # 让第一梯队向上一格,并部署第二梯队-----------------------------------------------------------------
    ImageOps.find_image(IMG("team_1"), x_offset=-36, y_offset=-96, action="click")
    wait(1)
    ImageOps.find_image(IMG("hq_base"), confidence=0.75, random_point=True, action="click")
    wait(1)
    BasicTasks.click_deploy_button()  # 点击部署按钮
    BasicTasks.click_confirm()
    # 让第一梯队向上一格,并部署第二梯队-----------------------------------------------------------------

    # 结束回合,并等待战斗结束-------------------------------------------------------------------------
    BasicTasks.click_end_round_button()  # 点击结束回合
    ImageOps.find_image(IMG("battle_end_flag"), x_offset=200, y_offset=300, action="move")  # 移动到战斗结束标志
    ImageOps.hold_click_until_image_appear(COMMON_IMG("mark_image_794"), interval=0.8)  # 持续点击直到794(战斗结束的标识)出现
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
    wait(0.1)
    ImageOps.find_image(IMG("team_1"), x_offset=120, y_offset=30, action="click")  # 往右一格
    wait(0.1)
    ImageOps.find_image(IMG("team_1"), x_offset=120, y_offset=-96, action="click")  # 向右上一格
    wait(0.1)
    ImageOps.find_image(IMG("team_1"), x_offset=-196, y_offset=-96, action="click")  # 向左上一格
    BasicTasks.click_execute_plan()
    # 开启计划模式,让第一梯队沿着路径点执行计划-----------------------------------------------------------

    while True:

        # 检测分享按钮的出现,战斗结束后会出现分享按钮,如果有新的人形被打捞,自动战斗则会停止
        share_button = ImageOps.locate_image(COMMON_IMG("share_button"))
        if share_button is not None:
            MouseOps.move_to(share_button.x + 200, share_button.y + 300)
            ImageOps.hold_click_until_image_appear(COMMON_IMG("mark_image_794"), interval=0.8)  # 持续点击直到794(战斗结束的标识)出现

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


def main(max_actions=30):
    """
    :param max_actions: 最大执行次数
    :return:
    """
    set_resource_subdir(resource_subdir)
    print_banner("[裂变链接-底层归乡2 战斗EX 自动打捞] 自动化执行开始")
    # 激活游戏窗口,如果失败则自动打开少女前线
    if not launch_gf():
        logging.error("[启动异常] 启动游戏失败")
        raise MissionFinished()
    action_count = 1  # 初始化执行计数
    action_limit = False

    while True:
        logging.info("先进行一次人形回收,防止程序卡死")
        menu_enter_retire_dolls()

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
                repeat = repeat_mission()
                wait(2)

                # 处理意外窗口后,从主菜单重新开始
                if deal_unexpected_windows():
                    break

                start_mission_actions(repeat)
                action_count += 1

            # 任务完成并且达到最大执行次数,退出程序

            else:
                return_to_main_menu()
                print(f"[终止] 已达到最大执行次数 {max_actions},程序结束")

                print_banner("[裂变链接-底层归乡2 战斗EX 自动打捞] 自动化执行结束")
                raise MissionFinished()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"[异常] 程序发生错误: {e}")
