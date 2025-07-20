import time
from collections import namedtuple

import matplotlib.pyplot as plt
import pyautogui
import win32api
import win32con

from config.logger_config import *
from core_ops.utils.mouse_utils import *



class MouseOps:
    """
    封装鼠标操作的工具类
    """

    @staticmethod
    def move_to(x, y, duration=0.1):
        pyautogui.moveTo(x, y, duration=duration)
        logging.debug(f"[鼠标操作] 鼠标移动到 ({x}, {y})")

    @staticmethod
    def move_mouse(dx, dy):
        pyautogui.moveRel(dx, dy, duration=0.1)
        logging.debug(f"[鼠标操作] 鼠标向 {dx},{dy} 移动 ")

    @staticmethod
    def mouse_left_down():
        pyautogui.mouseDown(button='left')
        logging.debug("[鼠标操作] 左键按下")

    @staticmethod
    def mouse_left_up():
        pyautogui.mouseUp(button='left')
        logging.debug("[鼠标操作] 左键松开")

    @staticmethod
    def mouse_right_down():
        pyautogui.mouseDown(button='right')
        logging.debug("[鼠标操作] 右键按下")

    @staticmethod
    def mouse_right_up():
        pyautogui.mouseUp(button='right')
        logging.debug("[鼠标操作] 右键松开")

    @staticmethod
    def one_left_click():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        logging.debug(f"[鼠标操作] 左键单击")

    @staticmethod
    def double_left_click():
        for _ in range(2):
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.05)
        logging.debug(f"[鼠标操作] 左键双击")

    @staticmethod
    def scroll_mouse(circles=1, repeat=1):
        units = int(circles * 120)
        for _ in range(repeat):
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, units, 0)
            time.sleep(0.02)
        logging.debug(f"[鼠标操作] 鼠标滚动 {circles} 圈, 重复 {repeat} 次")

    @staticmethod
    def drag_rel(dx, dy, duration=0.3):
        pyautogui.dragRel(dx, dy, duration=duration, button='left')
        logging.debug(f"[鼠标操作] 拖动鼠标 相对移动 dx={dx}, dy={dy}")

    @staticmethod
    def drag_to(x, y, duration=0.3):
        pyautogui.dragTo(x, y, duration=duration, button='left')
        logging.debug(f"[鼠标操作] 拖动鼠标 到位置 ({x}, {y})")

    @staticmethod
    def record_mouse_position():
        Point = namedtuple('Point', ['x', 'y'])
        x, y = pyautogui.position()
        location = Point(x, y)
        logging.debug(f"[鼠标操作] 记录当前鼠标坐标 ({location.x}, {location.y})")
        return location

    @staticmethod
    def left_click_at(x, y, duration=0.1, overshoot=True, plot=False):
        """
        在指定坐标 (x, y) 处左键点击,并平滑移动鼠标到该位置
        :param x:
        :param y:
        :param duration: 鼠标移动到目标位置的时间,单位秒
        :param overshoot: 是否加入“偏移后回正”效果
        :param plot: 是否开启可视化路径
        :return:
        """
        current_x, current_y = pyautogui.position()  # 获取当前鼠标位置
        MouseOps.move_mouse_smoothly(current_x, current_y, x, y, duration=duration, overshoot=overshoot, plot=plot)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        logging.debug(f"[鼠标操作] 左键点击位置 ({x}, {y})")

    @staticmethod
    def move_mouse_smoothly(x1, y1, x2, y2, duration=0.1, steps=30, overshoot=True, plot=False):
        """
        从 (x1, y1) 平滑移动鼠标到 (x2, y2),支持曲线轨迹、抖动、加速减速、轨迹可视化
        没有用pyautogui.moveTo(精度问题),使用win32api.SetCursorPos实现精确移动
        (x1, y1) 通常为鼠标当前的位置
        :param x1: 起始点 x 坐标
        :param y1: 起始点 y 坐标
        :param x2: 目标点 x 坐标
        :param y2: 目标点 y 坐标
        :param duration: 总移动时间(秒)
        :param steps: 路径点数
        :param overshoot: 是否加入“偏移后回正”效果
        :param plot: 是否开启可视化路径
        """

        distance = math.hypot(x2 - x1, y2 - y1)
        overshoot = overshoot and distance > 300
        offset_scale = min(distance / 200, 1.0)
        ctrl_offset = int(80 * offset_scale)
        jitter_strength = 1.0 * offset_scale

        control_points = generate_control_points(x1, y1, x2, y2, overshoot, ctrl_offset)
        path = bezier_curve(control_points, n=steps)

        if overshoot:
            path = np.vstack([path, [x2, y2]])  # 回正

        if jitter_strength > 0:
            path = jitter_path(path, jitter_strength)

        if plot:
            MouseOps.plot_path(path, x1, y1, x2, y2)

        MouseOps.move_along_path(path, duration)

    @staticmethod
    def move_along_path(path, duration):
        """沿着路径移动鼠标，精确控制时间"""
        start_time = time.perf_counter()
        total_points = len(path)

        for i, (x, y) in enumerate(path):
            win32api.SetCursorPos((int(x), int(y)))
            next_t = (i + 1) / total_points * duration
            while time.perf_counter() - start_time < next_t:
                time.sleep(0)

    @staticmethod
    def plot_path(path, x1, y1, x2, y2):
        """可视化鼠标移动路径"""
        plt.figure(figsize=(6, 4))
        plt.plot(path[:, 0], path[:, 1], marker='o', linestyle='-', color='blue')
        plt.scatter([x1, x2], [y1, y2], color='red', label='start/end')
        plt.title("Mouse Movement Path")
        plt.gca().invert_yaxis()
        plt.axis("equal")
        plt.legend()
        plt.grid(True)
        plt.show()
