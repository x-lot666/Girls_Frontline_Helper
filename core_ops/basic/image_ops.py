import os
import random

import pyautogui
from pyautogui import ImageNotFoundException


class ImageOps:
    """
    图像定位工具类，提供图像识别和定位功能
    """

    @staticmethod
    def locate_image(image_path, confidence=0.8):
        """
        定位图像中心点
        """
        if not os.path.exists(image_path):
            print(f"[图像识别] 图片不存在: {image_path}")
            return None

        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        except ImageNotFoundException:
            # print(f"[图像识别] 未识别到图像 {image_path}")
            return None

        if location:
            print(f"[图像识别] 识别到图像 {image_path},位置：{location}")

        return location

    @staticmethod
    def locate_random_point_in_image(image_path, confidence=0.8, padding=10):
        """
        定位图像中的随机点
        """
        if not os.path.exists(image_path):
            print(f"[图像识别] 图片不存在: {image_path}")
            return None

        try:
            # 返回图像矩形区域: (left, top, width, height)
            box = pyautogui.locateOnScreen(image_path, confidence=confidence)
        except Exception as e:
            # print(f"[图像识别] 未识别到图像 {image_path} {e}")
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
