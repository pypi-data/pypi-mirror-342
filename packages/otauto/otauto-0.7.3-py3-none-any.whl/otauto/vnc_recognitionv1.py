import asyncio
import os
import random
import time
import numpy as np
from PIL import Image
from loguru import logger

from otauto.vncdotool_main.vncdotool import api

"""
时间:2025-1-28 16:03:53
描述:用于vnc操作
"""

def downsample_image(image, scale_factor=0.1):
    """将图像缩小到指定比例"""
    width, height = image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def compare_region(image1, image2, x1, y1, x2, y2):
    """比较图像的指定区域"""
    region1 = image1[y1:y2, x1:x2]
    region2 = image2[y1:y2, x1:x2]
    return np.array_equal(region1, region2)

def multi_scale_compare(image1, image2, scale_factor=0.5):
    """对整个图像进行缩小尺寸比对"""
    image1_small = downsample_image(Image.fromarray(image1), scale_factor)
    image2_small = downsample_image(Image.fromarray(image2), scale_factor)

    # 将缩小后的图像转换为 NumPy 数组并比较
    return np.array_equal(np.array(image1_small), np.array(image2_small))
class VNC_recognition:
    """
    VNCtools类,用于连接VNC服务器并截取屏幕
    :param vnc_server: VNC服务器的地址
    :param vnc_port: VNC服务器的端口
    :param vnc_password: VNC服务器的密码
    """
    def __init__(self, vnc_server: str = "127.0.0.1", vnc_port: int = 5900, vnc_password: str = None):
        # VNC 服务器的地址、端口和密码
        self.vnc_server = vnc_server  # VNC 服务器的地址
        self.vnc_port = vnc_port  # VNC 服务器的端口
        self.vnc_password = vnc_password  # VNC 服务器的密码
        current_file_path = os.path.abspath(__file__)  # 获取项目的绝对路径
        self.project_path = os.path.dirname(os.path.dirname(current_file_path))  # 获取项目的根目录

        try:
            self.vnc = api.connect(f"{self.vnc_server}::{self.vnc_port}", password=self.vnc_password)
            logger.success(f"Connected to VNC server at {self.vnc_server}:{self.vnc_port}")
        except Exception as e:
            logger.error(f"Failed to connect to VNC server: {e}")  # 使用 logger.error 记录错误
            raise ConnectionError(f"Failed to connect to VNC server: {e}")  # 抛出更具体的异常

    def capture_full_screen_as_numpy(self, debug: bool = False, retries: int = 3, delay: float = 0.5) -> np.ndarray:
        """调用 VNCDoToolClient 的 captureScreenAsArray 方法捕获全屏并返回 NumPy 数组"""
        logger.debug("Capturing full screen as NumPy array using VNCDoToolClient.")

        for attempt in range(retries):
            try:
                numpy_image = self.vnc.captureScreenAsArray()

                # 检查返回的类型
                if not isinstance(numpy_image, np.ndarray):
                    raise ValueError("Captured image is not a valid NumPy array.")

                if debug:
                    # 将 NumPy 数组转换为图像
                    image = Image.fromarray(numpy_image)

                    # 拼接保存路径
                    save_dir = os.path.join(self.project_path, "res", "test")
                    os.makedirs(save_dir, exist_ok=True)  # 创建目录(如果不存在)
                    full_path = os.path.join(save_dir, f"{self.vnc_port}_capture_full_screen_as_numpy.png")

                    # 保存图像
                    image.save(full_path)
                    logger.info(f"Captured image saved to {full_path}")

                return numpy_image

            except Exception as e:
                logger.error(f"Error capturing screen on attempt {attempt + 1}/{retries}: {e}")
                time.sleep(delay)  # 等待一段时间再重试

        logger.error("All attempts to capture the screen have failed.")
        return None  # 或者返回一个空的 NumPy 数组,例如 np.array([]) 以表示失败

    def capture_region_as_numpy(self, x1: int, y1: int, x2: int, y2: int, debug: bool = False):
        """调用 VNCDoToolClient 的 captureRegionAsArray 方法捕获指定区域并返回 NumPy 数组"""
        logger.debug(f"Capturing region as NumPy array: ({x1}, {y1}, {x2}, {y2}) using VNCDoToolClient.")
        try:
            numpy_image = self.vnc.captureRegionAsArray(x1, y1, x2, y2)
            if debug:
                # 将 NumPy 数组转换为图像
                image = Image.fromarray(numpy_image)
                # 拼接保存路径
                save_dir = os.path.join(self.project_path, "res", "test")  # 使用 os.path.join 确保路径正确
                os.makedirs(save_dir, exist_ok=True)  # 创建目录（如果不存在）
                full_path = os.path.join(save_dir, f"{self.vnc_port}_capture_region_as_numpy.png")
                # 保存图像
                image.save(full_path)
                logger.info(f"Captured image saved to {full_path}")
            return numpy_image
        except Exception as e:
            logger.error(f"Error capturing region: {e}")
            return None  # 或者根据需求返回其他值

    async def async_capture_full_screen_as_numpy(self, interval: float = 0.3, debug: bool = False):
        """
        异步捕获全屏截图，并在每次捕获后返回最新截图。
        :param interval: 截图间隔时间（秒）
        :param debug: 是否保存截图用于调试
        :return: 返回最新的截图 NumPy 数组
        """
        logger.debug("Starting asynchronous full screen capture.")

        previous_image = None  # 用于存储上一次的截图

        while True:
            try:
                # 捕获当前屏幕截图
                current_image = self.capture_full_screen_as_numpy(debug=debug)

                if current_image is None:
                    logger.error("Failed to capture screen.")
                    await asyncio.sleep(interval)
                    continue

                logger.debug("Returning the captured image.")
                yield current_image  # 使用 yield 返回当前图像

                # 等待一段时间后继续
                await asyncio.sleep(interval)

            except Exception as e:
                logger.error(f"Error during asynchronous capture: {e}")
                await asyncio.sleep(interval)

    # async def async_capture_full_screen_as_numpy(self, interval: float = 0.3, debug: bool = False):
    #     """
    #     异步捕获全屏截图，并在内容发生变化时更新。
    #     :param interval: 截图间隔时间（秒）
    #     :param debug: 是否保存截图用于调试
    #     :return: 返回最新的截图 NumPy 数组
    #     """
    #     logger.debug("Starting asynchronous full screen capture.")
    #
    #     previous_image = None  # 用于存储上一次的截图
    #
    #     while True:
    #         try:
    #             # 捕获当前屏幕截图
    #             current_image = self.capture_full_screen_as_numpy(debug=debug)
    #
    #             if current_image is None:
    #                 logger.error("Failed to capture screen.")
    #                 await asyncio.sleep(interval)
    #                 continue
    #
    #             # 如果这是第一次截图，直接返回
    #             if previous_image is None:
    #                 previous_image = current_image
    #                 logger.debug("First capture, returning the initial image.")
    #                 yield current_image  # 使用 yield 返回初始图像
    #                 continue  # 继续循环
    #
    #             # 使用多尺度比较判断图像是否发生变化
    #             if not multi_scale_compare(previous_image, current_image, scale_factor=0.2):
    #                 logger.success("Screen content has changed, updating the image.")
    #                 previous_image = current_image
    #                 yield current_image  # 使用 yield 返回更新的图像
    #
    #             # 如果截图内容没有变化，等待一段时间后继续
    #             logger.debug("Screen content has not changed, waiting for the next capture.")
    #             await asyncio.sleep(interval)
    #
    #         except Exception as e:
    #             logger.error(f"Error during asynchronous capture: {e}")
    #             await asyncio.sleep(interval)

    def mouse_move(self,x,y):# 鼠标移动
        """
        鼠标移动
        :param x: int:x坐标
        :param y: int:y坐标
        :return: 无
        """
        # 使用randint生成随机整数
        random_number = random.randint(1, 5)
        self.vnc.mouseMove(x+random_number,y+random_number)
        # 随机停顿
        time.sleep(random.uniform(0.05, 0.2))

    def mouse_left_click(self,x,y,x3:int=0,y3:int=0,delay_time=0.1):# 鼠标左键点击
        """
        鼠标左键单击
        :param x: int:x坐标
        :param y: int:y坐标
        :param x3: int:x坐标偏移量
        :param y3: int:y坐标偏移量
        :param delay_time:点击以后延迟时间
        :return: 无
        """
        # 使用randint生成随机整数
        random_number = random.randint(1, 5)
        self.vnc.mouseMove(x+random_number+x3,y+random_number+y3)
        # 随机停顿
        time.sleep(random.uniform(0.05, 0.2))
        self.vnc.mousePress(1)
        time.sleep(delay_time)

    def mouse_double_left_click(self,x,y,x3:int=0,y3:int=0,delay_time=0.1):
        """
        鼠标左键双击
        :param x: int:x坐标
        :param y: int:y坐标
        :param x3: int:x坐标偏移量
        :param y3: int:y坐标偏移量
        :param delay_time:点击以后延迟时间
        :return: 无
        """
        # 使用randint生成随机整数
        random_number = random.randint(1, 5)
        self.vnc.mouseMove(x + random_number+x3, y + random_number+y3)
        # 随机停顿
        time.sleep(random.uniform(0.05, 0.2))
        self.vnc.mousePress(1)
        # 随机停顿
        time.sleep(random.uniform(0.05, 0.2))
        self.vnc.mousePress(1)
        time.sleep(delay_time)

    def mouse_right_click(self,x,y,x3:int=0,y3:int=0,delay_time=0.1):# 鼠标右键点击
        """
        鼠标右键单击
        :param x: int:x坐标
        :param y: int:y坐标
        :param x3: int:x坐标偏移量
        :param y3: int:y坐标偏移量
        :param delay_time:点击以后延迟时间
        :return: 无
        """
        # 使用randint生成随机整数
        random_number = random.randint(1, 5)
        self.vnc.mouseMove(x + random_number+x3, y + random_number+y3)
        # 随机停顿
        time.sleep(random.uniform(0.05, 0.2))
        self.vnc.mousePress(3)
        time.sleep(delay_time)

    def mouse_drag(self,x1,y1,x2,y2,step:int=20):
        """
        鼠标拖拽,注意不完成
        :param x1: 开始拖拽坐标x
        :param y1: 开始拖拽坐标y
        :param x2: 结束拖拽坐标x
        :param y2: 结束拖拽坐标y
        :param step: 步长
        :return:
        """
        # 使用randint生成随机整数
        random_number = random.randint(1, 5)
        self.vnc.mouseMove(x1 + random_number, y1 + random_number)
        # 随机停顿
        time.sleep(random.uniform(0.05, 0.2))
        self.vnc.mouseDown(1)
        self.vnc.mouseDrag(x2,y2,step)
        if self.vnc.mouseUp(1):
            return True
        else:
            return False

    def mouse_up(self,button):
        """
        鼠标释放
        : button: int:1左键,3右键
        :return:
        """
        self.vnc.mouseUp(button)
        time.sleep(0.1)

    def mouse_down(self,button):
        """
        鼠标按下
        : button: int:1左键,3右键
        :return:
        """
        self.vnc.mouseDown(button)
        time.sleep(0.1)

    def key_press(self,key,delay_time=0.1):# 按键
        """
        按键
        :param key:str:字母,大写的识别率更好一些
        :param delay_time: 按键以后延迟时间
        :return: 无
        """
        self.vnc.keyPress(key)
        time.sleep(delay_time)

    def key_down(self,key,delay_time=0.1):# 按键
        """
        键按下
        :param key: str:字母,大写的识别率更好一些
        :param delay_time: 按下去保持时间
        :return: 无
        """
        self.vnc.keyDown(key)
        time.sleep(delay_time)

    def key_up(self,key,delay_time=0.1):# 按键
        """
        键释放
        :param key: str:字母,大写的识别率更好一些
        :param delay_time: 释放后延迟时间
        :return: 无
        """
        self.vnc.keyUp(key)
        time.sleep(delay_time)





