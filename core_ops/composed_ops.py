import math

import matplotlib.pyplot as plt
import numpy as np

from core_ops.basic_ops import *


# 使用win32api来实现精确的鼠标点击和移动,详情见move_mouse_smoothly()函数


# ==========================
# 复合操作
# ==========================

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
    print(f"[操作] 左键点击位置 ({x}, {y})")


def wait_image(image_path, confidence=0.8, interval=0.5, timeout=-1, random_point=False, padding=10):
    """
    等待图像出现
    :param image_path: 图片路径
    :param confidence: 相似度阈值,0-1之间
    :param interval: 等待间隔时间,单位秒
    :param timeout: 最长等待时间（秒），-1表示无限制
    :param random_point: 是否在返回图像内的随机位置
    :param padding: 图像边缘的安全间距,避免点击到边缘,单位像素
    :return: 找到图像的位置 (x, y) 或 None
    """
    print(f"[等待] 正在等待图像出现: {image_path}")
    start_time = time.time()
    while True:
        if random_point:
            location = locate_random_point_in_image(image_path, confidence, padding)
        else:
            location = locate_image(image_path, confidence)
        if location:
            print(f"[完成] 找到图像位置: {image_path}")
            return location
        if timeout != -1 and time.time() - start_time > timeout:
            print(f"[超时] {timeout} 秒内未找到图像: {image_path}")
            return None
        time.sleep(interval)


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


def wait_and_move(image_path, confidence=0.8, duration=0.1, x_offset=0, y_offset=0, interval=0.5, timeout=-1):
    """
    等待图像出现并移动鼠标
    :param image_path: 图片路径
    :param confidence: 相似度阈值,0-1之间
    :param duration: 移动鼠标的时间,单位秒
    :param x_offset: x轴偏移量
    :param y_offset: y轴偏移量
    :param interval: 等待间隔时间,单位秒
    :param timeout: 最长等待时间（秒），-1表示无限制
    :return: Boolean, True为找到并移动鼠标, False为未找到图像
    """
    location = wait_image(image_path, confidence, interval, timeout)
    if location is not None:
        time.sleep(0.8)  # 确保图像稳定后再移动
        current_x, current_y = pyautogui.position()  # 获取当前鼠标位置
        move_mouse_smoothly(current_x, current_y, location.x + x_offset, location.y + y_offset, duration=duration,
                            overshoot=True)
        # move_to(location.x + x_offset, location.y + y_offset, duration) #直接移动鼠标到目标位置
        print(f"[完成] 鼠标已移动到图像位置: {image_path}")
        return True
    return False


def wait_and_move_random(image_path, confidence=0.8, padding=10, duration=0.1, x_offset=0, y_offset=0, interval=0.5,
                         timeout=-1):
    """
    等待图像出现并移动鼠标到图像内的随机位置
    :param image_path: 图片路径
    :param confidence: 相似度阈值,0-1之间
    :param padding: 图像边缘的安全间距,避免点击到边缘,单位像素
    :param duration: 移动鼠标的时间,单位秒 
    :param x_offset: x轴偏移量
    :param y_offset: y轴偏移量
    :param interval: 等待间隔时间,单位秒
    :param timeout: 最长等待时间（秒），-1表示无限制
    :return: Boolean, True为找到并移动鼠标, False为未找到图像
    """
    location = wait_image(image_path, confidence, interval, timeout, random_point=True, padding=padding)
    if location is not None:
        time.sleep(0.8)  # 确保图像稳定后再移动
        current_x, current_y = pyautogui.position()  # 获取当前鼠标位置
        move_mouse_smoothly(current_x, current_y, location.x + x_offset, location.y + y_offset, duration=duration,
                            overshoot=True)
        # move_to(location.x + x_offset, location.y + y_offset, duration) #直接移动鼠标到目标位置
        print(f"[完成] 鼠标已移动到图像位置: {image_path}")
        return True
    return False


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


def wait_and_click(image_path, confidence=0.8, duration=0.1, x_offset=0, y_offset=0, interval=0.5, timeout=-1):
    """
    等待图像出现并点击
    :param image_path: 图片路径
    :param confidence: 相似度阈值,0-1之间
    :param duration: 移动鼠标的时间,单位秒
    :param x_offset: x轴偏移量
    :param y_offset: y轴偏移量
    :param interval: 等待间隔时间,单位秒
    :param timeout: 最长等待时间（秒），-1表示无限制
    :return: Boolean, True为找到并点击, False为未找到图像
    """

    location = wait_image(image_path, confidence, interval, timeout)
    if location is not None:
        time.sleep(0.8)  # 确保图像稳定后再点击
        left_click_at(location.x + x_offset, location.y + y_offset, duration)
        print(f"[完成] 点击图像: {image_path}")
        return True
    return False


def wait_and_click_random(image_path, confidence=0.8, padding=10, duration=0.1, x_offset=0, y_offset=0, interval=0.5,
                          timeout=-1):
    """
    等待图像出现并点击图像内的随机位置
    :param image_path: 图片路径
    :param confidence: 相似度阈值,0-1之间
    :param padding: 图像边缘的安全间距,避免点击到边缘,单位像素
    :param duration: 移动鼠标的时间,单位秒
    :param x_offset: x轴偏移量
    :param y_offset: y轴偏移量
    :param interval: 等待间隔时间,单位秒
    :param timeout: 最长等待时间（秒），-1表示无限制
    :return: Boolean, True为找到并点击, False为未找到图像
    """
    location = wait_image(image_path, confidence, interval, timeout, random_point=True, padding=padding)
    if location is not None:
        time.sleep(0.8)  # 确保图像稳定后再点击
        left_click_at(location.x + x_offset, location.y + y_offset, duration)
        print(f"[完成] 点击图像: {image_path}")
        return True
    return False


def hold_click_until_image(image_path, confidence=0.8, interval=0.5):
    """
    持续点击直到图像出现
    :param image_path: 图片路径
    :param confidence: 相似度阈值,0-1之间
    :param interval: 等待间隔时间,单位秒
    :return:
    """
    print(f"[等待] 持续点击中,并等待图像出现: {image_path}")
    while True:
        location = locate_image(image_path, confidence)
        if location:
            time.sleep(0.8)
            print(f"[完成] 确认到图像出现: {image_path}")
            return True
        one_left_click()
        time.sleep(interval)


def hold_click_until_image_click(image_path, confidence=0.8, duration=0.1, x_offset=0, y_offset=0, interval=0.5):
    """
    持续点击直到图像出现并点击
    :param image_path: 图片路径
    :param confidence: 相似度阈值,0-1之间
    :param duration: 鼠标移动的时间,单位秒
    :param x_offset: x轴偏移量
    :param y_offset: y轴偏移量
    :param interval: 等待间隔时间,单位秒
    :return:
    """
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


# ==========================
# 工具函数
# ==========================


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
