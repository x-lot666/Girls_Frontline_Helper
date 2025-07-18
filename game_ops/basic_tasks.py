from core_ops.composed_ops import *
from utils.resource import *


# ==========================
# 游戏中的基础操作
# ==========================

# 等待并点击“首页-战斗”
def wait_and_click_home_battle_button():
    wait_and_click_random(COMMON_IMG("home_battle_button"))


# 等待并点击“确认出击”
def wait_and_click_start_the_task():
    wait_and_click_random(COMMON_IMG("start_the_task"))


# 等待并点击“确定”
def wait_and_click_confirm():
    wait_and_click_random(COMMON_IMG("confirm"), confidence=0.75)


# 等待并点击“开始作战”
def wait_and_click_start_battle():
    wait_and_click_random(COMMON_IMG("start_battle"))


# 等待并点击“计划模式”
def wait_and_click_enable_plan_mode():
    wait_and_click_random(COMMON_IMG("enable_plan_mode"))


# 等待并点击“执行计划”
def wait_and_click_execute_plan():
    wait_and_click_random(COMMON_IMG("execute_plan"))


# 等待并点击“再次作战”
def wait_and_click_repeat_battle():
    wait_and_click_random(COMMON_IMG("repeat_battle"))


# 等待并点击“返回按钮”
def wait_and_click_back_button():
    wait_and_click_random(COMMON_IMG("back_button"))


# 等待并点击“关闭按钮”
def wait_and_click_close_button():
    wait_and_click_random(COMMON_IMG("close_button"))


# 等待并点击“重新战斗”
def wait_and_click_retry_battle():
    wait_and_click_random(COMMON_IMG("retry_battle"))


# 等待并点击“暂停战斗”
def wait_and_click_pause_battle():
    wait_and_click_random(COMMON_IMG("pause_battle"))


# 等待并点击“全体撤退”
def wait_and_click_evacuate_all():
    wait_and_click_random(COMMON_IMG("evacuate_all"))


# 等待并点击“添加标靶”
def wait_and_click_add_target():
    wait_and_click_random(COMMON_IMG("add_target"))


# 等待并点击"战斗失败标识(enjoy表情)"
def wait_and_click_fail_enjoy_face():
    wait_and_click_random(COMMON_IMG("fail_enjoy_face"))


# 等待并点击"终止作战-白色按钮"
def wait_and_click_cancel_battle_white():
    wait_and_click_random(COMMON_IMG("cancel_battle_white"))


# 等待并点击"终止作战-橙色按钮"
def wait_and_click_cancel_battle_orange():
    wait_and_click_random(COMMON_IMG("cancel_battle_orange"))


# 等待并点击"任务选择"
def wait_and_click_select_mission():
    wait_and_click_random(COMMON_IMG("select_mission"))


# 等待并点击"人形修复"
def wait_and_click_fix_doll():
    wait_and_click_random(COMMON_IMG("fix_doll"))


# 等待并点击"一键修复"
def wait_and_click_fix_all_dolls():
    wait_and_click_random(COMMON_IMG("fix_all_dolls"))


# 等待并点击"重新作战"
def wait_and_click_restart_battle():
    wait_and_click_random(COMMON_IMG("restart_battle"))


# 等待并点击"补给按钮"
def wait_and_click_supply_button():
    wait_and_click_random(COMMON_IMG("supply_button"))


# 等待并点击"撤离按钮"
def wait_and_click_retreat_button():
    wait_and_click_random(COMMON_IMG("retreat_button"))


# 等待并点击"结束回合"
def wait_and_click_end_round_button():
    wait_and_click_random(COMMON_IMG("end_round_button"))


# 等待并点击"设置按钮"
def wait_and_click_config_button():
    wait_and_click_random(COMMON_IMG("config_button"))


# 等待并点击"切换按钮"
def wait_and_click_toggle_button():
    wait_and_click(COMMON_IMG("toggle_button"))


# 等待并点击"作战配置"
def wait_and_click_battle_config():
    wait_and_click_random(COMMON_IMG("battle_config"))


# 等待并点击
def wait_and_click_():
    wait_and_click_random(COMMON_IMG(""))
