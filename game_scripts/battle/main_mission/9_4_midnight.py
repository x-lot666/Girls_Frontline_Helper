from game_ops.composed_tasks import *

"""
9-4 夜战 斯捷奇金专属(APS专用枪托) 打捞
(很不幸,脚本我都没写完,枪托就刷出来了,只捞了20把不到)
说明：
    - 需要 无伤清三红雷 跟 打法官无重创 的队伍,建议第一次运行自己看着,打不过就加进靶场里试试
    
    - 第一梯队: 无伤清三红雷
        - 我使用的队伍是: 马暴队(马提尼亨利+SCAR-H+暴风+斯捷奇金+PPK)
        
    - 第二梯队: 打法官无重创
        - 我使用的队伍是: 标准日月索(P10C+MP41)
        
    - 确保第一次进入战斗前,装备仓库未满(第一次不做自动回收处理”。
    - 关闭"回合结束二次确认"和"自动补给"
"""

# 所用的资源图片的文件夹名称
set_resource_subdir("9_4_midnight")


def menu_enter_mission():
    """
    从主菜单进入任务
    """

    # 点击“首页-战斗”
    BasicTasks.click_home_battle_button()

    # 如果第九战役没被激活，则点击第九战役
    if not ImageOps.wait_image(IMG("battle_9_active"), confidence=0.96, timeout=1.5):
        # 切换至作战任务界面
        ImageOps.find_image(IMG("combat_mission"), action="click")

        # 如果没找到第九战役，滚动页面到底部
        if not ImageOps.find_image(IMG("battle_9"), confidence=0.96, timeout=1, action="click"):
            ImageOps.find_image(IMG("mark_image"), x_offset=260, y_offset=-200, action="move")
            wait(0.2)
            MouseOps.scroll_mouse(-3, 20)
            wait(0.5)
            MouseOps.scroll_mouse(3, 2)
            wait(2)
            ImageOps.find_image(IMG("battle_9"), confidence=0.96, action="click")

    # 设置成夜战难度
    ImageOps.find_image(IMG("mark_image"), x_offset=1400, y_offset=-600, action="click")

    # 点击9_4
    ImageOps.find_image(IMG("mark_image"), x_offset=800, y_offset=-55, action="click")

    # 等待并点击“普通作战”
    ImageOps.find_image(COMMON_IMG("normal_battle"), random_point=True, action="click")


def repeat_mission():
    """
    重复进行入任务
    """
    # 点击"再次作战"按钮
    ImageOps.find_image(COMMON_IMG("repeat_battle"), action="click")


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

    # 选中第一梯队,补给后向右方移动一格-----------------------------------------------------------------
    ImageOps.find_image(IMG("team_1"), x_offset=-30, y_offset=30, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_1"), x_offset=-30, y_offset=30, action="click")
    BasicTasks.click_supply_button()
    ImageOps.find_image(IMG("team_1"), x_offset=165, y_offset=-10, action="click")
    # 选中第一梯队,补给后向右方移动一格-----------------------------------------------------------------

    # 关闭结算画面
    if ImageOps.find_image(IMG("battle_end_flag"), x_offset=500, action="click"):
        ImageOps.hold_click_until_image_appear(COMMON_IMG("end_round_button"))

    # 部署第二梯队,并补给----------------------------------------------------------------------------
    # 清除选择
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                        action="click")

    ImageOps.find_image(IMG("team_1"), x_offset=-250, y_offset=70, action="click")
    BasicTasks.click_confirm()  # 点击确认部署
    wait(0.5)
    ImageOps.find_image(IMG("team_2"), x_offset=-30, y_offset=30, action="click")
    wait(0.2)
    ImageOps.find_image(IMG("team_2"), x_offset=-30, y_offset=30, action="click")
    BasicTasks.click_supply_button()
    # 部署第二梯队,并补给----------------------------------------------------------------------------

    # 计划模式,设置路径并执行------------------------------------------------------------------------
    # 清除选择
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                        action="click")

    BasicTasks.click_enable_plan_mode()  # 点击计划模式
    # 选中第一梯队,并设置路径点
    ImageOps.find_image(IMG("team_1"), x_offset=-30, y_offset=30, action="click")
    wait(0.5)
    ImageOps.find_image(IMG("team_1"), x_offset=170, y_offset=-100, action="click")
    BasicTasks.click_next_turn()  # 点击下一回合

    # 清除选择
    ImageOps.find_image(COMMON_IMG("enable_plan_mode"), x_offset=0, y_offset=-300, random_point=True, padding=30,
                        action="click")

    # 选中第二梯队,并设置路径点
    ImageOps.find_image(IMG("team_2"), x_offset=-30, y_offset=30, action="click")
    wait(0.5)
    ImageOps.find_image(IMG("team_2"), x_offset=560, y_offset=-190, action="click")

    BasicTasks.click_execute_plan()  # 点击执行计划
    # 计划模式,设置路径并执行------------------------------------------------------------------------

    # 等待"敌人过于强大"的提示出现
    ImageOps.find_image(IMG("confirm_button_red"), random_point=True, action="click")

    # 等待"再次作战"按钮出现(说明回合结束)
    ImageOps.wait_image(COMMON_IMG("repeat_battle"))
    wait(1)
    ImageOps.find_image(COMMON_IMG("repeat_battle"), action="click")
    wait(0.5)
    # 把鼠标往右移动,避免下面点击到“再次作战”按钮
    MouseOps.move_mouse(300, 0)
    wait(0.5)

    # 持续点击,直到“再次作战”再次出现
    ImageOps.hold_click_until_image_appear(COMMON_IMG("repeat_battle"), interval=1)


def return_to_main_menu():
    """
    任务结束后,返回主菜单
    """
    if ImageOps.locate_image(COMMON_IMG("repeat_battle")):
        wait(1)
    # 点击一次空白处
    ImageOps.find_image(COMMON_IMG("repeat_battle"), x_offset=300, action="click")

    # 点击“返回按钮”
    ImageOps.hold_click_until_image_appear(COMMON_IMG("back_button"), interval=0.5, click_after=True)


# 检查执行次数是否超过限制
def check_action_limit(action_count, max_actions):
    if action_count > max_actions:
        return True


def main(max_actions=3):
    """
    :param max_actions: 最大执行次数
    :return:
    """
    print_banner("[9-4 midnight 斯捷奇金专属 'APS专用枪托' 打捞] 自动化执行开始")
    WindowOps.activate_window("少女前线")  # 激活游戏窗口
    action_count = 1  # 初始化执行计数
    action_limit = False

    while True:

        logging.info("[9-4 midnight 斯捷奇金专属 'APS专用枪托' 打捞] 从主菜单进入任务")
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
                logging.info("[9-4 midnight 斯捷奇金专属 'APS专用枪托' 打捞] 重复进行任务")
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

                print_banner("[9-4 midnight 斯捷奇金专属 'APS专用枪托' 打捞] 自动化执行结束")
                exit()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"[异常] 程序发生错误: {e}")
