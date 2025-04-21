import os
from datetime import datetime
import time
from PIL import Image
from loguru import logger
from otauto.vncdotool_main.vncdotool import api

"""
功能:vnc截图
日期:2025-3-11 18:00:31
描述:
    1. vnc截图,全图,区域
    2.区域地图截图范围:1258, 75, 1414, 207
"""

class VncTools:
    """
    VNCtools类,用于连接VNC服务器并截取屏幕,键鼠操作
    :param vnc_server: VNC服务器的地址
    :param vnc_port: VNC服务器的端口
    :param vnc_password: VNC服务器的密码
    """
    def __init__(self, vnc_server: str = "127.0.0.1", vnc_port: int = 5900, vnc_password: str = None):
        # VNC 服务器的地址、端口和密码
        self.vnc_server = vnc_server  # VNC 服务器的地址
        self.vnc_port = vnc_port  # VNC 服务器的端口
        self.vnc_password = vnc_password  # VNC 服务器的密码

        # 连接到 VNC 服务器
        try:
            self.vnc = api.connect(f"{self.vnc_server}::{self.vnc_port}", password=self.vnc_password)
            logger.success(f"Connected to VNC server at {self.vnc_server}:{self.vnc_port}")
        except Exception as e:
            logger.error(f"Failed to connect to VNC server: {e}")
            raise

    def create_directory(self, path: str):
        """创建目录（如果不存在的话）"""
        if not os.path.exists(path):
            os.makedirs(path)
            logger.info(f"Created directory: {path}")

    def screenshot_full(self, img_path: str = "full", debug: bool = False):
        """全屏截图"""
        self.create_directory(img_path)  # 确保目录存在
        current_time = datetime.now().strftime("%M%S")
        full_img_path = os.path.join(img_path, f"{current_time}.jpg")
        self.vnc.captureScreen(full_img_path)
        print(f"Screenshot saved to: {full_img_path}")
        if debug:
            img = Image.open(full_img_path)
            img.show()

    def screenshot_area(self, x1: int, y1: int, x2: int, y2: int, img_path: str = "area", debug: bool = False):
        """区域截图"""
        self.create_directory(img_path)  # 确保目录存在
        current_time = datetime.now().strftime("%M%S")
        area_img_path = os.path.join(img_path, f"{current_time}.jpg")
        h = y2 - y1  # 修改为 y2 - y1
        w = x2 - x1  # 修改为 x2 - x1
        self.vnc.captureRegion(area_img_path, x1, y1, w, h)  # 修改传递的参数顺序
        print(f"Screenshot saved to: {area_img_path}")
        if debug:
            img = Image.open(area_img_path)
            img.show()

# 使用示例
vnctools = VncTools("192.168.110.245", 5904)
while True:
    vnctools.screenshot_area(1258, 75, 1414, 207)
    time.sleep(3)









