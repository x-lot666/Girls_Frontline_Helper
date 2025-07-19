import time
from collections import namedtuple

import pyautogui
import win32api
import win32con


class MouseOps:
    """
    封装鼠标操作的工具类
    """

    @staticmethod
    def move_to(x, y, duration=0.1):
        pyautogui.moveTo(x, y, duration=duration)
        print(f"[鼠标操作] 鼠标移动到 ({x}, {y})")

    @staticmethod
    def move_mouse(dx, dy):
        pyautogui.moveRel(dx, dy, duration=0.1)
        print(f"[鼠标操作] 鼠标向 {dx},{dy} 移动 ")

    @staticmethod
    def mouse_left_down():
        pyautogui.mouseDown(button='left')
        print("[鼠标操作] 左键按下")

    @staticmethod
    def mouse_left_up():
        pyautogui.mouseUp(button='left')
        print("[鼠标操作] 左键松开")

    @staticmethod
    def mouse_right_down():
        pyautogui.mouseDown(button='right')
        print("[鼠标操作] 右键按下")

    @staticmethod
    def mouse_right_up():
        pyautogui.mouseUp(button='right')
        print("[鼠标操作] 右键松开")

    @staticmethod
    def one_left_click():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        print(f"[鼠标操作] 左键单击")

    @staticmethod
    def double_left_click():
        for _ in range(2):
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.05)
        print(f"[鼠标操作] 左键双击")

    @staticmethod
    def scroll_mouse(circles=1, repeat=1):
        units = int(circles * 120)
        for _ in range(repeat):
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, units, 0)
            time.sleep(0.02)
        print(f"[鼠标操作] 鼠标滚动 {circles} 圈, 重复 {repeat} 次")

    @staticmethod
    def drag_rel(dx, dy, duration=0.3):
        pyautogui.dragRel(dx, dy, duration=duration, button='left')
        print(f"[鼠标操作] 拖动鼠标 相对移动 dx={dx}, dy={dy}")

    @staticmethod
    def drag_to(x, y, duration=0.3):
        pyautogui.dragTo(x, y, duration=duration, button='left')
        print(f"[鼠标操作] 拖动鼠标 到位置 ({x}, {y})")

    @staticmethod
    def record_mouse_position():
        Point = namedtuple('Point', ['x', 'y'])
        x, y = pyautogui.position()
        location = Point(x, y)
        print(f"[鼠标操作] 记录当前鼠标坐标 ({location.x}, {location.y})")
        return location

    @staticmethod
    def left_click_at(x, y, duration=0.1):
        """
        在指定坐标 (x, y) 处左键点击,并平滑移动鼠标到该位置
        :param x:
        :param y:
        :param duration: 鼠标移动到目标位置的时间,单位秒
        :return:
        """
        current_x, current_y = pyautogui.position()  # 获取当前鼠标位置
        move_mouse_smoothly(current_x, current_y, x, y, duration=duration, overshoot=True)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        print(f"[鼠标操作] 左键点击位置 ({x}, {y})")
