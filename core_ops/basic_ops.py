import os
import random
import time
from collections import namedtuple

import pyautogui
import pygetwindow as gw
import win32api
import win32con
import win32gui
from pyautogui import ImageNotFoundException


# ==========================
# 鼠标基本操作
# ==========================

# 绝对移动鼠标到坐标 (x, y)
def move_to(x, y, duration=0.1):
    pyautogui.moveTo(x, y, duration=duration)
    print(f"[操作] 鼠标移动到 ({x}, {y})")


# 鼠标相对当前位置移动
def move_mouse(dx, dy):
    pyautogui.moveRel(dx, dy, duration=0.1)
    print(f"[操作] 鼠标向 {dx},{dy} 移动 ")


# 左键按下
def mouse_left_down():
    pyautogui.mouseDown(button='left')
    print("[操作] 左键按下")


# 左键松开
def mouse_left_up():
    pyautogui.mouseUp(button='left')
    print("[操作] 左键松开")


# 右键按下
def mouse_right_down():
    pyautogui.mouseDown(button='right')
    print("[操作] 右键按下")


# 右键松开
def mouse_right_up():
    pyautogui.mouseUp(button='right')
    print("[操作] 右键松开")


# 左键单击
def one_left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    print(f"[操作] 左键单击")


# 左键双击
def double_left_click():
    for _ in range(2):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(0.05)  # 双击间隔
    print(f"[操作] 左键双击")


# 鼠标滚轮滚动(正值向上,负值向下)
def scroll_mouse(circles=1, repeat=1):
    """
    模拟鼠标滚轮滚动操作
    :param circles: 每次滚动的圈数，正值向上，负值向下
    :param repeat: 重复执行的次数，默认1
    """
    units = int(circles * 120)  # 120 是滚轮一圈的单位
    for i in range(repeat):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, units, 0)
        time.sleep(0.02)
    print(f"[操作] 鼠标滚动 {circles} 圈, 重复 {repeat} 次")


# 拖动鼠标相对位置(按住左键拖动)
def drag_rel(dx, dy, duration=0.3):
    pyautogui.dragRel(dx, dy, duration=duration, button='left')
    print(f"[操作] 拖动鼠标 相对移动 dx={dx}, dy={dy}")


# 拖动鼠标到绝对位置(按住左键拖动)
def drag_to(x, y, duration=0.3):
    pyautogui.dragTo(x, y, duration=duration, button='left')
    print(f"[操作] 拖动鼠标 到位置 ({x}, {y})")


# 记录当前鼠标位置
def record_mouse_position():
    Point = namedtuple('Point', ['x', 'y'])
    x, y = pyautogui.position()
    location = Point(x, y)
    print(f"[记录] 当前鼠标坐标 ({location.x}, {location.y})")
    return location


# ==========================
# 图像识别操作
# ==========================

# 定位图像中心
def locate_image(image_path, confidence=0.8):
    if not os.path.exists(image_path):
        print(f"[错误] 图片不存在: {image_path}")
        return None

    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
    except ImageNotFoundException:
        # print(f"[识别失败] 未识别到图像 {image_path}")
        return None

    if location:
        print(f"[识别成功] 识别到图像 {image_path},位置：{location}")

    return location


# 在图像中随机定位一点
def locate_random_point_in_image(image_path, confidence=0.8, padding=10):
    if not os.path.exists(image_path):
        print(f"[错误] 图片不存在: {image_path}")
        return None

    try:
        # 返回图像矩形区域: (left, top, width, height)
        box = pyautogui.locateOnScreen(image_path, confidence=confidence)
    except Exception as e:
        # print(f"[识别失败] 未识别到图像 {image_path} {e}")
        return None

    if box:
        # 限制 padding 不超过一半宽高,避免区域无效
        max_pad_x = min(padding, box.width // 2 - 1)
        max_pad_y = min(padding, box.height // 2 - 1)

        x = random.randint(box.left + max_pad_x, box.left + box.width - 1 - max_pad_x)
        y = random.randint(box.top + max_pad_y, box.top + box.height - 1 - max_pad_y)

        print(f"[识别成功] 识别到图像 {image_path},随机坐标：({x}, {y})")
        return pyautogui.Point(x, y)

    print(f"[识别失败] 未找到图像 {image_path}")
    return None


# ==========================
# 工具函数
# ==========================

# 等待(秒)
def wait(seconds):
    print(f"[等待] {seconds} 秒")
    time.sleep(seconds)


def wait_in_range(min_seconds, max_seconds):
    """
    等待一个随机时间,在指定范围内
    :param min_seconds: 最小等待时间(秒)
    :param max_seconds: 最大等待时间(秒)
    """
    seconds = random.uniform(min_seconds, max_seconds)
    print(f"[等待] {seconds:.2f} 秒")
    time.sleep(seconds)


# 激活窗口并短暂置顶
def activate_the_window(title_keyword):
    """
    激活并短暂置顶窗口,使其出现在最前面一次
    """
    windows = gw.getWindowsWithTitle(title_keyword)
    if not windows:
        print(f"[错误] 未找到包含关键字“{title_keyword}”的窗口")
        return False

    window = windows[0]
    hwnd = window._hWnd

    if window.isMinimized:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    # 强制置顶 + 激活窗口（跳过 pygetwindow.activate()）
    win32gui.SetForegroundWindow(hwnd)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    print(f"[完成] 窗口“{window.title}”已被激活")
    return True
