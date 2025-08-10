import threading

from core_ops.composed.composed_ops import *
"""
兵棋开房间挂机
@author: moonight1199
挖坑：
    - 实现冲锋枪流派全自动游玩
"""


set_resource_subdir("wargame")


# 从主菜单进入任务
def menu_enter_mission():
    # 打开菜单界面
    ImageOps.find_image(IMG("menu"), confidence=0.9, random_point=True, action="click")

    # 进入咖啡厅
    ImageOps.find_image(IMG("coffee_shop"), random_point=True, action="click")

    # 进入兵棋游戏界面
    ImageOps.find_image(IMG("wargame"), random_point=True, action="click")

    # 创建房间
    ImageOps.find_image(IMG("create_room"), random_point=True, action="click")

    # 选择四人游戏
    ImageOps.find_image(IMG("four_players"), timeout=1, random_point=True, action="click")

    # 进入房间
    ImageOps.find_image(IMG("confirm"), random_point=True, action="click")

    # 开始游戏并选择队伍
    start_and_choose_team()

    # 正式游玩
    playing_game()


# 开始游戏并选择队伍
def start_and_choose_team():
    # 开始游戏
    ImageOps.find_image(IMG("start_game"), random_point=True, action="click")

    # 选择队伍
    ImageOps.find_image(IMG("choose_team"), random_point=True, action="click")
    wait(0.5)
    MouseOps.one_left_click()

    # 点击确定
    ImageOps.find_image(IMG("confirm"), random_point=True, action="click")

    # 选择金币
    ImageOps.find_image(IMG("coin"), random_point=True, action="click")


# 游戏游玩主要函数
def playing_game():
    # 标记游戏是否正在进行，通过多线程停止
    playing = True

    # 进入购买界面
    while playing:
        while playing:
            # 判断是否进入商店
            if ImageOps.locate_image(IMG("finish_shopping")) is not None:
                # 结束商店购买
                ImageOps.find_image(IMG("finish_shopping"), random_point=True, action="click")
                break
            # 判断游戏是否结束
            elif ImageOps.locate_image(IMG("game_over")) is not None:
                playing = False
                break
            # 每一秒进行一次判断
            wait(1)

        # 进入游戏界面
        while playing:
            # 点击骰子
            ImageOps.find_image(IMG("dice"), random_point=True, action="click")

            # 判断是否投出一点和六点
            if ImageOps.wait_image(IMG("move_dice"), timeout=3) is not None:
                # 判断是否抛出六点
                if ImageOps.wait_image(IMG("another_chance_info"), timeout=1) is not None:
                    # 选择移动选项
                    ImageOps.find_image(IMG("move_dice"), wait=False, random_point=True, action="click")
                    # 点击移动
                    ImageOps.find_image(IMG("move"), random_point=True, action="click")
                    continue
                else:
                    # 选择移动选项
                    ImageOps.find_image(IMG("move_dice"), wait=False, random_point=True, action="click")

            # 点击移动
            ImageOps.find_image(IMG("move"), random_point=True, action="click")

            # 点击结束回合
            ImageOps.find_image(IMG("end_round"), random_point=True, action="click")

            break

    wait(0.5)

    # 点击任意位置
    MouseOps.one_left_click()

    # 等待加载结束
    wait(1)

    # 返回房间
    ImageOps.find_image(IMG("back_to_room"), random_point=True, action="click")


# 重复进入任务
def repeat_mission():
    start_and_choose_team()

    playing_game()


# 最后一次执行任务
def final_mission():
    logging.info("[兵棋开房间挂机] 进入最后一次执行")

    start_and_choose_team()

    playing_game()

    # 退出房间
    ImageOps.find_image(IMG("back_to_main"), random_point=True, action="click")

    # 点击确定
    BasicTasks.click_confirm()

    # 退回主菜单
    ImageOps.find_image(IMG("back_to_menu"), random_point=True, action="click")


# 检查执行次数是否超过最大限制
def check_action_limit(action_count, max_actions):
    """
    检查执行次数是否超过最大限制
    :param action_count: 当前执行次数
    :param max_actions: 最大执行次数
    """
    if action_count >= max_actions:
        wait(1)
        final_mission()


def main(max_actions=1):
    """
    :param max_actions: 最大执行次数
    """

    print_banner("[兵棋开房间挂机] 自动化执行开始")

    # 激活游戏窗口,如果失败则自动打开少女前线
    if not launch_gf():
        logging.error("[启动异常] 启动游戏失败")
        exit()

    action_count = 1  # 初始化执行计数

    if max_actions == 1:
        logging.info("[兵棋开房间挂机] 场景 从主菜单进入任务")
        logging.info("[兵棋开房间挂机] 进入最后一次执行")

        menu_enter_mission()

        # 退出房间
        ImageOps.find_image(IMG("back_to_main"), random_point=True, action="click")

        # 点击确定
        BasicTasks.click_confirm()

        # 退回主菜单
        ImageOps.find_image(IMG("back_to_menu"), random_point=True, action="click")

        exit()

    while True:
        # 检查执行次数是否超过限制
        check_action_limit(action_count, max_actions)

        logging.info("[兵棋开房间挂机] 场景 从主菜单进入任务")
        logging.info(f"[计数] 当前游戏次数: {action_count} ")
        menu_enter_mission()
        action_count += 1

        while True:
            # 检查执行次数是否超过限制
            check_action_limit(action_count, max_actions)

            # 定位到“开始游戏”图像,表示可以继续进行任务
            if ImageOps.locate_image(IMG("start_game")):
                logging.info("[兵棋开房间挂机] 场景 重复进行任务")
                logging.info(f"[计数] 当前游戏次数: {action_count} ")
                repeat_mission()
                action_count += 1


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"[异常] 程序发生错误: {e} ")
