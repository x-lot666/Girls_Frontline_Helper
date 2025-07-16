import math
from collections import namedtuple

import pyautogui
from pyautogui import ImageNotFoundException
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import pygetwindow as gw
import win32api
import win32gui
import win32con
import random


# pyautogui跟win32api混用模拟鼠标操作,属实是无奈之举
# 使用pyautogui会导致各种问题,尤其是在点击操作上
# 于是使用win32api来实现精确的鼠标点击和移动,详情见move_mouse_smoothly()函数


# --------------------------
# 鼠标基本操作
# --------------------------

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


# 鼠标左键点击指定坐标
def left_click_at(x, y, duration=0.1):
    current_x, current_y = pyautogui.position()  # 获取当前鼠标位置
    move_mouse_smoothly(current_x, current_y, x, y, duration=duration, overshoot=True)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    print(f"[操作] 左键点击位置 ({x}, {y})")


# 鼠标滚轮滚动(正值向上,负值向下)
def scroll_mouse(circles=1):
    units = int(circles * 120)  # 120是鼠标滚轮的一个刻度
    # 调用鼠标滚轮事件，最后一个参数是滚动的单位数，正数向上滚，负数向下滚
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, units, 0)
    print(f"[操作] 鼠标滚动 {circles} 圈({units} 单位)")


# 拖动鼠标相对位置(按住左键拖动)
def drag_rel(dx, dy, duration=0.1):
    pyautogui.dragRel(dx, dy, duration=duration, button='left')
    print(f"[操作] 拖动鼠标 相对移动 dx={dx}, dy={dy}")


# 拖动鼠标到绝对位置(按住左键拖动)
def drag_to(x, y, duration=0.1):
    pyautogui.dragTo(x, y, duration=duration, button='left')
    print(f"[操作] 拖动鼠标 到位置 ({x}, {y})")


# 记录当前鼠标位置
def record_mouse_position():
    Point = namedtuple('Point', ['x', 'y'])
    x, y = pyautogui.position()
    location = Point(x, y)
    print(f"[记录] 当前鼠标坐标 ({location.x}, {location.y})")
    return location


# --------------------------
# 图像识别操作
# --------------------------

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


# --------------------------
# 图像识别后的复合操作
# --------------------------


# 搜索图像并移动
def find_and_move(image_path, confidence=0.8, duration=0.1, x_offset=0, y_offset=0):
    """
    搜索图像并移动鼠标
    :param image_path: 图片路径
    :param confidence: 相似度阈值,0-1之间
    :param duration: 轴移动的时间,单位秒
    :param x_offset: x轴偏移量
    :param y_offset: y轴偏移量
    :return: Boolean, True为找到并移动鼠标, False为未找到图像
    """
    location = locate_image(image_path, confidence)
    if location:
        current_x, current_y = pyautogui.position()  # 获取当前鼠标位置
        move_mouse_smoothly(current_x, current_y, location.x + x_offset, location.y + y_offset, duration=duration,
                            overshoot=True)
        # move_to(location.x + x_offset, location.y + y_offset, duration) #直接移动鼠标到目标位置
        print(f"[完成] 鼠标已移动到图像位置: {image_path}")
        return True
    print(f"[未找到] 图像位置: {image_path}")
    return False


# 等待图像出现并移动鼠标
def wait_and_move(image_path, confidence=0.8, duration=0.1, x_offset=0, y_offset=0, interval=0.5):
    """
    等待图像出现并移动鼠标
    :param image_path: 图片路径
    :param confidence: 相似度阈值,0-1之间
    :param duration: 移动鼠标的时间,单位秒
    :param x_offset: x轴偏移量
    :param y_offset: y轴偏移量
    :param interval: 等待间隔时间,单位秒
    :return: 
    """
    print(f"[等待] 正在等待图像出现: {image_path}")
    while True:
        location = locate_image(image_path, confidence)
        if location:
            time.sleep(0.8)  # 确保图像稳定后再点击
            current_x, current_y = pyautogui.position()  # 获取当前鼠标位置
            move_mouse_smoothly(current_x, current_y, location.x + x_offset, location.y + y_offset, duration=duration,
                                overshoot=True)
            # move_to(location.x + x_offset, location.y + y_offset, duration) #直接移动鼠标到目标位置
            print(f"[完成] 鼠标已移动到图像位置: {image_path}")
            return True
        time.sleep(interval)


# 等待并移动到图像内的随机位置
def wait_and_move_random(image_path, confidence=0.8, padding=10, duration=0.1, x_offset=0, y_offset=0, interval=0.5):
    """
    等待图像出现并移动鼠标到图像内的随机位置
    :param image_path: 图片路径
    :param confidence: 相似度阈值,0-1之间
    :param padding: 图像边缘的安全间距,避免点击到边缘,单位像素
    :param duration: 移动鼠标的时间,单位秒 
    :param x_offset: x轴偏移量
    :param y_offset: y轴偏移量
    :param interval: 等待间隔时间,单位秒
    :return: 
    """
    print(f"[等待] 正在等待图像出现: {image_path}")
    while True:
        location = locate_random_point_in_image(image_path, confidence, padding)
        if location:
            time.sleep(0.8)  # 确保图像稳定后再点击
            current_x, current_y = pyautogui.position()  # 获取当前鼠标位置
            move_mouse_smoothly(current_x, current_y, location.x + x_offset, location.y + y_offset, duration=duration,
                                overshoot=True)
            # move_to(location.x + x_offset, location.y + y_offset, duration) #直接移动鼠标到目标位置
            print(f"[完成] 鼠标已移动到图像位置: {image_path}")
            return True
        time.sleep(interval)


# 搜索图像并点击
def find_and_click(image_path, confidence=0.8, duration=0.1, x_offset=0, y_offset=0):
    """
    搜索图像并点击,如果找到则点击图像中心偏移位置
    :param image_path: 图片路径
    :param confidence: 相似度阈值,0-1之间
    :param duration: 移动鼠标的时间,单位秒
    :param x_offset: x轴偏移量
    :param y_offset: y轴偏移量
    :return: Boolean, True为找到并点击, False为未找到图像
    """
    location = locate_image(image_path, confidence)
    if location:
        left_click_at(location.x + x_offset, location.y + y_offset, duration)
        print(f"[完成] 点击图像: {image_path}")
        return True
    print(f"[未找到] 图像位置: {image_path}")
    return False


# 等待图像出现并点击
def wait_and_click(image_path, confidence=0.8, duration=0.1, x_offset=0, y_offset=0, interval=0.5):
    """
    等待图像出现并点击
    :param image_path: 图片路径
    :param confidence: 相似度阈值,0-1之间
    :param duration: 移动鼠标的时间,单位秒
    :param x_offset: x轴偏移量
    :param y_offset: y轴偏移量
    :param interval: 等待间隔时间,单位秒
    :return: 
    """
    print(f"[等待] 正在等待图像出现: {image_path}")
    while True:
        location = locate_image(image_path, confidence)
        if location:
            time.sleep(0.8)  # 确保图像稳定后再点击
            left_click_at(location.x + x_offset, location.y + y_offset, duration)
            print(f"[完成] 点击图像: {image_path}")
            return True
        time.sleep(interval)


# 等待并点击图像内的随机位置
def wait_and_click_random(image_path, confidence=0.8, padding=10, duration=0.1, x_offset=0, y_offset=0, interval=0.5):
    """
    等待图像出现并点击图像内的随机位置
    :param image_path: 图片路径
    :param confidence: 相似度阈值,0-1之间
    :param padding: 图像边缘的安全间距,避免点击到边缘,单位像素
    :param duration: 移动鼠标的时间,单位秒 
    :param x_offset: x轴偏移量
    :param y_offset: y轴偏移量
    :param interval: 等待间隔时间,单位秒
    :return: 
    """
    print(f"[等待] 正在等待图像出现: {image_path}")
    while True:
        location = locate_random_point_in_image(image_path, confidence, padding)
        if location:
            time.sleep(0.8)  # 确保图像稳定后再点击
            left_click_at(location.x + x_offset, location.y + y_offset, duration)
            print(f"[完成] 点击图像: {image_path}")
            return True
        time.sleep(interval)


# 保持点击,并等待图像出现
def hold_click_until_image(image_path, confidence=0.8, interval=0.5):
    print(f"[等待] 持续点击中,并等待图像出现: {image_path}")
    while True:
        location = locate_image(image_path, confidence)
        if location:
            time.sleep(0.8)
            print(f"[完成] 确认到图像出现: {image_path}")
            return True
        one_left_click()
        time.sleep(interval)


# 保持点击,并等待图像出现并点击
def hold_click_until_image_click(image_path, confidence=0.8, duration=0.1, x_offset=0, y_offset=0, interval=0.5):
    print(f"[等待] 持续点击中,并等待图像出现: {image_path}")
    while True:
        location = locate_image(image_path, confidence)
        if location:
            time.sleep(0.8)  # 确保图像稳定后再点击
            left_click_at(location.x + x_offset, location.y + y_offset, duration)
            print(f"[完成] 点击图像: {image_path}")
            return True
        one_left_click()
        time.sleep(interval)


# --------------------------
# 工具函数
# --------------------------

# 等待(秒)
def wait(seconds):
    print(f"[等待] {seconds} 秒")
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


def bezier_curve(points, n=50):
    """
    生成贝塞尔曲线路径(任意阶)
    :param points: 控制点列表,每个点为 (x, y) 元组
    :param n: 生成的路径点数,默认50
    :return: shape=(n, 2) 的坐标数组
    """

    def bernstein_poly(i, n, t):
        return math.comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

    t = np.linspace(0.0, 1.0, n)
    curve = np.zeros((n, 2))
    order = len(points) - 1
    for i in range(len(points)):
        curve += np.outer(bernstein_poly(i, order, t), points[i])
    return curve


def jitter_path(path, jitter_range=1.5):
    """
    对路径中的每个点加入 ±jitter_range 范围内的抖动(模拟人手的微抖动)
    :param path: 输入路径,shape=(n, 2) 的坐标数组
    :param jitter_range: 抖动范围 x 轴和 y 轴方向 都随机加上一个范围在 ±jitter_range 之间的偏移量。
    """
    jitter = np.random.uniform(-jitter_range, jitter_range, size=path.shape)
    return path + jitter


def move_mouse_smoothly(x1, y1, x2, y2, duration=0.1, steps=30, overshoot=True, plot=True):
    """
    从 (x1, y1) 平滑移动鼠标到 (x2, y2),支持曲线轨迹、抖动、加速减速、轨迹可视化
    没有用pyautogui.moveTo(精度问题),使用win32api.SetCursorPos实现精确移动
    :param duration: 总移动时间(秒)
    :param steps: 路径点数
    :param overshoot: 是否加入“偏移后回正”效果
    :param plot: 是否开启可视化路径
    """
    # 生成贝塞尔曲线路径
    if overshoot:
        ox = random.choice([-1, 1]) * random.randint(10, 30)
        oy = random.choice([-1, 1]) * random.randint(10, 30)
        x2_overshoot = x2 + ox
        y2_overshoot = y2 + oy
        control_points = [
            (x1, y1),
            ((x1 + x2) / 2 + random.randint(-80, 80), (y1 + y2) / 2 + random.randint(-80, 80)),
            ((x1 + x2_overshoot) / 2, (y1 + y2_overshoot) / 2),
            (x2_overshoot, y2_overshoot)
        ]
        path = bezier_curve(control_points, n=steps)
        path = np.vstack([path, [x2, y2]])  # 回正
    else:
        control_points = [
            (x1, y1),
            ((x1 + x2) / 2 + random.randint(-80, 80), (y1 + y2) / 2 + random.randint(-80, 80)),
            (x2, y2)
        ]
        path = bezier_curve(control_points, n=steps)

    # 抖动
    path = jitter_path(path, jitter_range=1.0)

    # 可视化
    if plot:
        plt.figure(figsize=(6, 4))
        plt.plot(path[:, 0], path[:, 1], marker='o', linestyle='-', color='blue')
        plt.scatter([x1, x2], [y1, y2], color='red', label='start/end')
        plt.title("Mouse Movement Path")
        plt.gca().invert_yaxis()
        plt.axis("equal")
        plt.legend()
        plt.grid(True)
        plt.show()

    # 精确控制总耗时
    start_time = time.perf_counter()
    total_points = len(path)

    for i, (x, y) in enumerate(path):
        win32api.SetCursorPos((int(x), int(y)))
        next_t = (i + 1) / total_points * duration
        while time.perf_counter() - start_time < next_t:
            time.sleep(0)
