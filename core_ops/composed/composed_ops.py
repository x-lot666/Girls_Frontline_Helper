from core_ops.utils import *
from game_ops.basic_tasks import *

"""
各种操作相关的复合逻辑
暂时放这里,功能多了后续再拆分成不同的模块
"""


def launch_gf():
    """
    打开少女前线
    """
    game_url = "steam://rungameid/3347970"
    WindowOps.open_application_by_url(game_url)
