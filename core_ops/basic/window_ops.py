import os
import subprocess

import pygetwindow as gw
import win32con
import win32gui
import win32process

from config.logger_config import *
from core_ops.basic import MouseOps


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

    @staticmethod
    def get_center_of_window(title_keyword):
        """
        获取窗口中心坐标并返回
        """
        windows = gw.getWindowsWithTitle(title_keyword)
        if not windows:
            logging.error(f"[窗口操作] 未找到包含关键字“{title_keyword}”的窗口")
            return None

        window = windows[0]

        # 获取窗口位置和尺寸
        left, top, width, height = window.left, window.top, window.width, window.height

        # 计算中心坐标
        center_x = left + width // 2
        center_y = top + height // 2

        return center_x, center_y

    @staticmethod
    def move_to_window_center(title_keyword):
        """
        将鼠标移动到包含指定关键字的窗口中心。
        """
        center_x, center_y = WindowOps.get_center_of_window(title_keyword)

        if center_x is None:
            logging.error(f"[鼠标操作] 窗口“{title_keyword}”获取失败")
            return False

        MouseOps.move_to(center_x, center_y)

        logging.debug("[鼠标操作] 将鼠标移动到游戏窗口中心完成")

        return True

    @staticmethod
    def open_application_by_url(url):
        """
        使用 url 打开Steam的应用程序。
        Steam里少女前线的 URL 格式为"steam://rungameid/3347970"
        :param url: Steam应用程序的 url(右键游戏图标 -> 属性 -> URL)
        """
        try:
            # 使用 os.startfile (Windows) 或 subprocess.Popen (跨平台)
            if os.name == 'nt':  # Windows
                os.startfile(url)
            else:  # 其他操作系统 (Linux, macOS)
                subprocess.Popen(['xdg-open', url])  # 使用 xdg-open (Linux) 或 open (macOS)
            logging.info(f"[系统操作]成功打开应用程序: {url}")
            return True
        except Exception as e:
            logging.error(f"[系统操作]打开应用程序失败: {e}")
            return False

    @staticmethod
    def close_window(title_keyword):
        """
        关闭包含指定关键字的窗口的应用程序。
        """
        windows = gw.getWindowsWithTitle(title_keyword)
        if not windows:
            logging.error(f"[窗口操作] 未找到包含关键字“{title_keyword}”的窗口")
            return False

        window = windows[0]
        hwnd = window._hWnd

        try:
            # 使用 win32gui.PostMessage 发送 WM_CLOSE 消息
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            logging.info(f"[窗口操作] 已发送关闭窗口“{window.title}”的请求")
            return True
        except Exception as e:
            logging.error(f"[窗口操作] 关闭窗口“{window.title}”失败: {e}")
            return False

    @staticmethod
    def force_close_window(title_keyword):
        """
        强制关闭包含指定关键字的窗口的应用程序。  使用 taskkill 命令。
        """
        windows = gw.getWindowsWithTitle(title_keyword)
        if not windows:
            logging.error(f"[窗口操作] 未找到包含关键字“{title_keyword}”的窗口")
            return False

        window = windows[0]
        hwnd = window._hWnd

        try:
            # 获取进程 ID (PID)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            # 使用 taskkill 命令强制关闭进程
            os.system(f"taskkill /F /PID {pid}")
            logging.info(f"[窗口操作] 强制关闭窗口“{window.title}” (PID: {pid})")
            return True
        except Exception as e:
            logging.error(f"[窗口操作] 强制关闭窗口“{window.title}”失败: {e}")
            return False
