from core_ops.basic import *
from core_ops.utils.resource_utils import *


# ==========================
# 游戏中的基础操作
# ==========================

class BasicTasks:
    # 点击“首页-战斗”
    @staticmethod
    def click_home_battle_button():
        ImageOps.find_image(COMMON_IMG("home_battle_button"), random_point=True, action="click")

    # 点击“确认出击”
    @staticmethod
    def click_start_the_task():
        ImageOps.find_image(COMMON_IMG("start_the_task"), random_point=True, action="click")

    # 点击“确定”
    @staticmethod
    def click_confirm():
        ImageOps.find_image(COMMON_IMG("confirm"), confidence=0.75, random_point=True, action="click")

    # 点击“开始作战”
    @staticmethod
    def click_start_battle():
        ImageOps.find_image(COMMON_IMG("start_battle"), random_point=True, action="click")

    # 点击“计划模式”
    @staticmethod
    def click_enable_plan_mode():
        ImageOps.find_image(COMMON_IMG("enable_plan_mode"), random_point=True, action="click")

    # 点击“执行计划”
    @staticmethod
    def click_execute_plan():
        ImageOps.find_image(COMMON_IMG("execute_plan"), random_point=True, action="click")

    # 点击“再次作战”
    @staticmethod
    def click_repeat_battle():
        ImageOps.find_image(COMMON_IMG("repeat_battle"), random_point=True, action="click")

    # 点击“返回按钮”
    @staticmethod
    def click_back_button():
        ImageOps.find_image(COMMON_IMG("back_button"), random_point=True, action="click")

    # 点击“关闭按钮”
    @staticmethod
    def click_close_button():
        ImageOps.find_image(COMMON_IMG("close_button"), random_point=True, action="click")

    # 点击“重新战斗”
    @staticmethod
    def click_retry_battle():
        ImageOps.find_image(COMMON_IMG("retry_battle"), random_point=True, action="click")

    # 点击“暂停战斗”
    @staticmethod
    def click_pause_battle():
        ImageOps.find_image(COMMON_IMG("pause_battle"), random_point=True, action="click")

    # 点击“全体撤退”
    @staticmethod
    def click_evacuate_all():
        ImageOps.find_image(COMMON_IMG("evacuate_all"), random_point=True, action="click")

    # 点击“添加标靶”
    @staticmethod
    def click_add_target():
        ImageOps.find_image(COMMON_IMG("add_target"), random_point=True, action="click")

    # 点击"战斗失败标识(enjoy表情)"
    @staticmethod
    def click_fail_enjoy_face():
        ImageOps.find_image(COMMON_IMG("fail_enjoy_face"), random_point=True, action="click")

    # 点击"终止作战-白色按钮"
    @staticmethod
    def click_cancel_battle_white():
        ImageOps.find_image(COMMON_IMG("cancel_battle_white"), random_point=True, action="click")

    # 点击"终止作战-橙色按钮"
    @staticmethod
    def click_cancel_battle_orange():
        ImageOps.find_image(COMMON_IMG("cancel_battle_orange"), random_point=True, action="click")

    # 点击"任务选择"
    @staticmethod
    def click_select_mission():
        ImageOps.find_image(COMMON_IMG("select_mission"), random_point=True, action="click")

    # 点击"人形修复"
    @staticmethod
    def click_fix_doll():
        ImageOps.find_image(COMMON_IMG("fix_doll"), random_point=True, action="click")

    # 点击"一键修复"
    @staticmethod
    def click_fix_all_dolls():
        ImageOps.find_image(COMMON_IMG("fix_all_dolls"), random_point=True, action="click")

    # 点击"重新作战"
    @staticmethod
    def click_restart_battle():
        ImageOps.find_image(COMMON_IMG("restart_battle"), random_point=True, action="click")

    # 点击"补给按钮"
    @staticmethod
    def click_supply_button():
        ImageOps.find_image(COMMON_IMG("supply_button"), random_point=True, action="click")

    # 点击"撤离按钮"
    @staticmethod
    def click_retreat_button():
        ImageOps.find_image(COMMON_IMG("retreat_button"), random_point=True, action="click")

    # 点击"结束回合"
    @staticmethod
    def click_end_round_button():
        ImageOps.find_image(COMMON_IMG("end_round_button"), random_point=True, action="click")

    # 点击"设置按钮"
    @staticmethod
    def click_config_button():
        ImageOps.find_image(COMMON_IMG("config_button"), random_point=True, action="click")

    # 点击"切换按钮"
    @staticmethod
    def click_toggle_button():
        ImageOps.find_image(COMMON_IMG("toggle_button"), action="click")

    # 点击"作战配置"
    @staticmethod
    def click_battle_config():
        ImageOps.find_image(COMMON_IMG("battle_config"), random_point=True, action="click")
