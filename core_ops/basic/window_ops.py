import pygetwindow as gw
import win32con
import win32gui

from config.logger_config import *


class WindowOps:
    """
    窗口操作工具类，提供窗口管理和基本操作功能
    """

    @staticmethod
    def activate_window(title_keyword):
        """
        激活并短暂置顶包含指定关键字的窗口，使其出现在最前面一次
        """
        windows = gw.getWindowsWithTitle(title_keyword)
        if not windows:
            logging.error(f"[窗口操作] 未找到包含关键字“{title_keyword}”的窗口")
            return False

        window = windows[0]
        hwnd = window._hWnd

        if window.isMinimized:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

        # 强制置顶 + 激活窗口
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        logging.debug(f"[窗口操作] 窗口“{window.title}”已被激活")
        return True
