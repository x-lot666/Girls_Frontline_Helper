import traceback

from core_ops.utils import *
from game_ops.basic_tasks import *

"""
各种操作相关的复合逻辑
暂时放这里,功能多了后续再拆分成不同的模块
"""


def launch_gf():
    """
    激活游戏窗口,如果失败则自动打开少女前线
    """
    try:
        # 激活窗口失败就打开游戏
        if not WindowOps.activate_window("少女前线"):
            game_url = "steam://rungameid/3347970"
            WindowOps.open_application_by_url(game_url)
            # 等待窗口激活
            while True:
                if WindowOps.window_exists("少女前线"):
                    WindowOps.activate_window("少女前线")
                    break
            while True:
                # 出现登入按钮,则点击
                if ImageOps.locate_image(COMMON_IMG("login_button")):
                    ImageOps.find_image(COMMON_IMG("login_button"), action="click")

                # 确认进入主菜单后,退出循环
                if ImageOps.locate_image(COMMON_IMG("home_battle_button")):
                    break

                # 如果没有找到登入按钮,则点击窗口中心
                WindowOps.move_to_window_center("少女前线")
                MouseOps.one_left_click()
                wait(2)

        return True

    except Exception as e:
        error_message = f"[异常] 打开少女前线发生错误: {e}"
        logging.error(error_message)
        trace = traceback.format_exc()  # 获取堆栈跟踪的字符串表示
        logging.error(trace)
