import math
import random

import numpy as np


def bernstein_poly(i, n, t):
    """伯恩斯坦多项式"""
    return math.comb(n, i) * (t ** i) * ((1 - t) ** (n - i))


def bezier_curve(points, n=50):
    """
    生成贝塞尔曲线路径(任意阶)
    :param points: 控制点列表,每个点为 (x, y) 元组
    :param n: 生成的路径点数,默认50
    :return: shape=(n, 2) 的坐标数组
    """
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


def generate_control_points(x1, y1, x2, y2, overshoot, ctrl_offset):
    """生成贝塞尔曲线的控制点"""
    if overshoot:
        ox = random.choice([-1, 1]) * random.randint(10, 30)
        oy = random.choice([-1, 1]) * random.randint(10, 30)
        x2_overshoot = x2 + ox
        y2_overshoot = y2 + oy
        return [
            (x1, y1),
            ((x1 + x2) / 2 + random.randint(-ctrl_offset, ctrl_offset),
             (y1 + y2) / 2 + random.randint(-ctrl_offset, ctrl_offset)),
            ((x1 + x2_overshoot) / 2, (y1 + y2_overshoot) / 2),
            (x2_overshoot, y2_overshoot)
        ]
    else:
        return [
            (x1, y1),
            ((x1 + x2) / 2 + random.randint(-ctrl_offset, ctrl_offset),
             (y1 + y2) / 2 + random.randint(-ctrl_offset, ctrl_offset)),
            (x2, y2)
        ]
