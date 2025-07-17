from game_ops.basic_tasks import *


# --------------------------
# 游戏中的复合逻辑流程
# --------------------------

# 进入作战时仓库满员的人形回收
def retire_dolls():
    wait_and_click(COMMON_IMG("retire_dolls_0"), x_offset=-100, y_offset=0)
    wait(1.6)  # 等待人形回收界面加载,非常重要
    wait_and_click_random(COMMON_IMG("retire_dolls_1"), confidence=0.95, padding=15)
    wait_and_click_random(COMMON_IMG("retire_dolls_2"))
    wait_and_click_confirm()
    wait_and_click_random(COMMON_IMG("retire"))
    wait(1)  # 等待人形回收完成
    wait_and_click_back_button()
    print("[完成] 人形回收完成")


# 在主界面进行人形修理
def fix_dolls():
    print("[检测到] 人形修理按钮,开始修理人形")

    # 等待并点击“修理人形”
    wait_and_click_fix_doll()
    # 等待并点击“一键修复”
    wait_and_click_fix_all_dolls()
    # 等待并点击“确定”按钮
    wait_and_click_confirm()
    wait(1)
    # 等待并点击“返回”按钮
    wait_and_click_back_button()

    print("[完成] 人形修理完成")


# 处理意外窗口的复合函数
def deal_unexpected_windows():
    """
    处理意外窗口的整合函数
    当游戏出现各种意外窗口时,使画面回到主菜单,初始化画面
    :return: result
    """
    # 默认值False,如果处理过意外窗口则为True
    result = False

    # 检测进入作战时是否出现仓库满员-----------------------------------------------------------------------------------------
    if locate_image(COMMON_IMG("retire_dolls_0")):
        print("[检测到] 需要进行人形回收")
        retire_dolls()
        wait(5)
        result = True

    # 检测在主界面时是否出现后勤完成的界面------------------------------------------------------------------------------------
    if locate_image(COMMON_IMG("deploy_all")):
        print("[检测到] 后勤界面弹出")
        wait_and_click_random(COMMON_IMG("deploy_all"))
        count = 0
        # 有时候会跳出资源超出上限,无法再获取的提示框
        while True:
            print(f"这是第 {count + 1} 次循环")
            wait_and_click_confirm()
            count += 1
            if count >= 2:
                break
            wait(1)
        wait(5)
        result = True

    # 检测在主界面时是否出现解锁成就的界面------------------------------------------------------------------------------------
    if locate_image(COMMON_IMG("unlock_achievement")):
        print("[检测到] 解锁成就界面弹出")
        wait_and_move_random(COMMON_IMG("unlock_achievement"), y_offset=-200)
        while True:
            one_left_click()
            wait(1)
            if locate_image(COMMON_IMG("home_battle_button")):
                break
        wait(5)
        result = True

    # 检测在主界面时是否出现人形修复的界面------------------------------------------------------------------------------------
    if locate_image(COMMON_IMG("fix_doll")):
        fix_dolls()
        wait(5)
        result = True

    return result
