import os
import random
import time

import pyautogui
from pyautogui import ImageNotFoundException

from config.logger_config import *
from core_ops.basic.mouse_ops import MouseOps


class ImageOps:
    """
    图像定位和操作工具类，提供图像识别、定位后的鼠标操作功能
    """

    # 随机定位图像时的边缘间距
    _padding = 20

    @staticmethod
    def locate_image(image_path, confidence=0.8):
        """
        定位图像中心点
        :param image_path: 图片路径
        :param confidence: 相似度阈值,0-1之间
        :return: 图像中心点坐标 (x, y) 或 None
        """
        if not os.path.exists(image_path):
            logging.error(f"[图像识别] 图片不存在: {image_path}")
            return None

        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        except ImageNotFoundException:
            logging.debug(f"[图像识别] 未识别到图像 {image_path}")
            return None

        if location:
            logging.debug(f"[图像识别] 识别到图像 {image_path},位置：{location}")

        return location

    @staticmethod
    def locate_random_point_in_image(image_path, confidence=0.8, padding=_padding):
        """
        定位图像中的随机点
        :param image_path: 图片路径
        :param confidence: 相似度阈值,0-1之间
        :param padding: 图像边缘的安全间距,避免点击到边缘,单位像素
        :return: 图像内的随机点坐标 (x, y) 或 None
        """
        if not os.path.exists(image_path):
            logging.error(f"[图像识别] 图片不存在: {image_path}")
            return None

        try:
            # 返回图像矩形区域: (left, top, width, height)
            box = pyautogui.locateOnScreen(image_path, confidence=confidence)
        except Exception as e:
            logging.debug(f"[图像识别] 未识别到图像 {image_path} {e}")
            return None

        if box:
            # 限制 padding 不超过一半宽高,避免区域无效
            max_pad_x = min(padding, box.width // 2 - 1)
            max_pad_y = min(padding, box.height // 2 - 1)

            x = random.randint(box.left + max_pad_x, box.left + box.width - 1 - max_pad_x)
            y = random.randint(box.top + max_pad_y, box.top + box.height - 1 - max_pad_y)

            logging.debug(f"[图像识别] 识别到图像 {image_path},随机坐标：({x}, {y})")
            return pyautogui.Point(x, y)

        return None

    @staticmethod
    def wait_image(image_path, confidence=0.8, interval=0.5, timeout=-1, random_point=False, padding=_padding):
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
        logging.debug(f"[图像识别] 正在等待图像出现: {image_path}")
        start_time = time.time()
        while True:
            if random_point:
                location = ImageOps.locate_random_point_in_image(image_path, confidence, padding)
            else:
                location = ImageOps.locate_image(image_path, confidence)
            if location:
                logging.debug(f"[图像识别] 找到图像位置: {image_path}")
                return location
            if timeout != -1 and time.time() - start_time > timeout:
                logging.warning(f"[图像识别] {timeout} 秒内未找到图像: {image_path}")
                return None
            time.sleep(interval)

    @staticmethod
    def find_image(image_path, confidence=0.8, duration=0.1, x_offset=0, y_offset=0,
                   wait=True, interval=0.5, timeout=-1, random_point=False, padding=_padding,
                   action="move"):
        """
        搜索或等待图像出现，然后执行指定操作（移动或点击）
        :param image_path: 图片路径
        :param confidence: 相似度阈值,0-1之间
        :param duration: 移动鼠标的时间,单位秒
        :param x_offset: x轴偏移量
        :param y_offset: y轴偏移量
        :param wait: 是否等待图像出现
        :param interval: 等待间隔时间,单位秒
        :param timeout: 最长等待时间（秒），-1表示无限制
        :param random_point: 是否移动/点击图像内的随机位置
        :param padding: 图像边缘的安全间距,避免点击到边缘,单位像素
        :param action: 操作类型，"move" 表示移动鼠标，"click" 表示点击
        :return: Boolean, True为找到并执行操作, False为未找到图像
        """
        logging.debug(f"[图像识别] 正在等待图像出现: {image_path}")
        location = None

        if wait:
            location = ImageOps.wait_image(image_path, confidence, interval, timeout, random_point, padding)
            if location is None:
                return False  # 等待超时或未找到图像

            time.sleep(0.8)  # 确保图像稳定后再操作
        else:
            if random_point:
                location = ImageOps.locate_random_point_in_image(image_path, confidence, padding)
            else:
                location = ImageOps.locate_image(image_path, confidence)

            if location is None:
                logging.warning(f"[图像识别] 未找到图像,图像位置: {image_path}")
                return False  # 未找到图像

        # 执行操作
        target_x = location.x + x_offset
        target_y = location.y + y_offset

        if action == "move":
            current_x, current_y = pyautogui.position()
            MouseOps.move_mouse_smoothly(current_x, current_y, target_x, target_y, duration=duration, overshoot=True)
            logging.debug(f"[鼠标操作] 鼠标已移动到图像位置: {image_path}")
        elif action == "click":
            MouseOps.left_click_at(target_x, target_y, duration=duration)
            logging.debug(f"[鼠标操作] 点击图像: {image_path}")
        else:
            logging.error(f"[鼠标操作] 未知的操作类型: {action}")
            return False

        return True

    @staticmethod
    def hold_click_until_image_appear(image_path, confidence=0.8, duration=0.1, x_offset=0, y_offset=0, interval=0.5,
                                      timeout=-1, click_after=False):
        """
        持续点击直到图像出现，可以选择在图像出现后点击
        :param image_path: 图片路径
        :param confidence: 相似度阈值,0-1之间
        :param duration: 鼠标移动的时间,单位秒 (仅在 click_after=True 时使用)
        :param x_offset: x轴偏移量 (仅在 click_after=True 时使用)
        :param y_offset: y轴偏移量 (仅在 click_after=True 时使用)
        :param interval: 等待间隔时间,单位秒
        :param timeout: 等待超时时间，单位秒，-1 表示无限等待
        :param click_after: 是否在图像出现后点击
        :return: True (如果找到图像)，False（超时未找到）
        """
        logging.debug(f"[图像识别] 持续点击中,并等待图像出现: {image_path}")
        start_time = time.time()

        while True:
            if timeout != -1 and (time.time() - start_time) >= timeout:
                logging.warning(f"[图像识别] 等待图像出现超时: {image_path}")
                return False

            location = ImageOps.locate_image(image_path, confidence)
            if location:
                time.sleep(0.8)  # 确保图像稳定

                if click_after:
                    MouseOps.left_click_at(location.x + x_offset, location.y + y_offset, duration)
                    logging.debug(f"[鼠标操作] 点击图像: {image_path}")
                else:
                    logging.debug(f"[图像识别] 确认到图像出现: {image_path}")

                return True

            MouseOps.one_left_click()
            time.sleep(interval)

    @staticmethod
    def hold_click_until_image_disappears(image_path, confidence=0.8, interval=0.5, timeout=-1, x=None, y=None):
        """
        持续点击直到图像消失，可选在点击前将鼠标移动到指定位置。
        :param image_path: 图片路径
        :param confidence: 图像识别相似度阈值 (0-1)
        :param interval: 点击与检测的间隔秒数
        :param timeout: 最长等待时间（秒），-1表示无限制
        :param x: 可选，点击前鼠标移动到的X坐标
        :param y: 可选，点击前鼠标移动到的Y坐标
        :return: True（图像已消失）或 False（超时仍未消失）
        """
        logging.debug(f"[图像识别] 持续点击并等待图像消失: {image_path}")
        start_time = time.time()

        while True:
            location = ImageOps.locate_image(image_path, confidence)
            if not location:
                logging.debug(f"[图像识别] 图像已消失: {image_path}")
                return True

            if x is not None and y is not None:
                MouseOps.move_to(x, y)  # 鼠标移动到指定位置

            MouseOps.one_left_click()
            time.sleep(interval)

            if timeout != -1 and timeout is not None and (time.time() - start_time) >= timeout:
                logging.warning(f"[图像识别] 等待图像消失超时: {image_path}")
                return False

    @staticmethod
    def is_image_stable_for_seconds(image_path, confidence=0.8, check_time=10, interval=0.5):
        """
        持续检测图像 x 秒，如果一直存在则返回 True，否则返回 False。
        :param image_path: 图片路径
        :param confidence: 图像识别相似度阈值 (0-1)
        :param check_time: 检测时间，单位秒
        :param interval: 检测间隔时间，单位秒
        """
        start_time = time.time()
        while time.time() - start_time < check_time:
            time.sleep(interval)
            if not ImageOps.locate_image(image_path, confidence):
                return False  # 只要有一次没找到，就立即返回 False
        return True
