import asyncio
import os
import random
import time
import numpy as np
from PIL import Image

from otauto.ini_file_operationv2 import INIFileHandler
# from loguru import logger

from otauto.log import ColoredLogger
from otauto.shan_client import Command
from resource.parameters_info.basic_parameter_info import vnc_port_win_tille_dict

logger = ColoredLogger()

# 移除日志
logger.remove()

key_dict = {
    "a": "A",
    "b": "B",
    "c": "C",
    "d": "D",
    "e": "E",
    "f": "F",
    "g": "G",
    "h": "H",
    "i": "I",
    "j": "J",
    "k": "K",
    "l": "L",
    "m": "M",
    "n": "N",
    "o": "O",
    "p": "P",
    "q": "Q",
    "r": "R",
    "s": "S",
    "t": "T",
    "u": "U",
    "v": "V",
    "w": "W",
    "x": "X",
    "y": "Y",
    "z": "Z",
    "kp0": "NUM0",
    "kp1": "NUM1",
    "kp2": "NUM2",
    "kp3": "NUM3",
    "kp4": "NUM4",
    "kp5": "NUM5",
    "kp6": "NUM6",
    "kp7": "NUM7",
    "kp8": "NUM8",
    "kp9": "NUM9",
    "space": "SPACE",
    "enter": "ENTER",
    "esc": "ESC",
    "tab": "TAB",
    "backspace": "BACKSPACE",
    "minus": "MINUS",
    "f1": "F1",
    "f2": "F2",
    "f3": "F3",
    "f4": "F4",
    "f5": "F5",
    "f6": "F6",
    "f7": "F7",
    "f8": "F8",
    "f9": "F9",
    "f10": "F10",
    "f11": "F11",
    "f12": "F12",
    "ctrl": "CTRL",
    "shift": "SHIFT",
    "alt": "ALT",
    "win": "WIN",
    "up": "UP",
    "down": "DOWN",
    "left": "LEFT",
    "right": "RIGHT",
    "insert": "INSERT",
    "delete": "DELETE",
    "home": "HOME",
    "end": "END",
    "pageup": "PAGEUP",
    "pagedown": "PAGEDOWN",
    "numlock": "NUMLOCK",
    "scrolllock": "SCROLLLOCK",
    "printscreen": "PRINTSCREEN",
    "pause": "PAUSE",
    "application": "APPLICATION",
    "numpad_enter": "NUMPAD_ENTER",
    "numpad_plus": "NUMPAD_PLUS",
    "numpad_minus": "NUMPAD_MINUS",
    "numpad_multiply": "NUMPAD_MULTIPLY",
    "numpad_divide": "NUMPAD_DIVIDE",
    "~": "TILDE",  # 波浪号（`~）
    "-": "DASH",    # 减号（-）
    "=": "EQUAL",  # 等号（=）
    "[": "LEFTBRACKET",  # 左方括号（[）
    "]": "RIGHTBRACKET",  # 右方括号（]）
    "backslash": "BACKSLASH",  # 反斜杠（\）
    "forward_slash": "FORWARD_SLASH",  # 正斜杠（/）
}

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
    """
    def __init__(self, vnc_server: str = "127.0.0.1", vnc_port: int = 49152):
        # VNC 服务器的地址、端口和密码
        self.vnc_server = vnc_server  # VNC 服务器的地址
        self.vnc_port = vnc_port  # VNC 服务器的端口
        current_file_path = os.path.abspath(__file__)  # 获取项目的绝对路径
        self.project_path = os.path.dirname(os.path.dirname(current_file_path))  # 获取项目的根目录

        self.ini_data_dict = INIFileHandler().get_section_items(vnc_port_win_tille_dict[self.vnc_port])  # 获取ini数据
        self.screen_num = self.ini_data_dict.get("screen_num")  # 获取屏幕编号

        try:
            self.vnc = Command(self.vnc_server) # 实例化 Command 类
            self.vnc.connect() # 连接到 socket 服务器
            logger.success(f"Connected to socket server at {self.vnc_server}:{self.vnc_port}")
        except Exception as e:
            logger.error(f"Failed to connect to socket server: {e}")  # 使用 logger.error 记录错误
            raise ConnectionError(f"Failed to connect to socket server: {e}")  # 抛出更具体的异常

    def capture_full_screen_test(self,full_path, debug: bool = False, retries: int = 1, delay: float = 0.5,image_w: int = 1440, image_h: int = 900) :
        """调用 VNCDoToolClient 的 captureScreenAsArray 方法捕获全屏并返回 NumPy 数组"""
        logger.debug("Capturing full screen as NumPy array using VNCDoToolClient.")

        for attempt in range(retries):
            try:
                numpy_image = self.vnc.image_numpy_locality(debug=debug,image_w=image_w, image_h=image_h,screen_num=self.screen_num) # 调用 vnc.image_numpy_locality 方法
                time.sleep(0.1)

                # 检查返回的类型
                if not isinstance(numpy_image, np.ndarray):
                    raise ValueError("Captured image is not a valid NumPy array.")

                # 将 NumPy 数组转换为图像
                image = Image.fromarray(numpy_image)
                # 保存图像
                image.save(full_path)
                logger.info(f"Captured image saved to {full_path}")

            except Exception as e:
                logger.error(f"Error capturing screen on attempt {attempt + 1}/{retries}: {e}")
                time.sleep(delay)  # 等待一段时间再重试

    def capture_full_screen_as_numpy(self, debug: bool = False, retries: int =1, delay: float = 0.5,image_w: int = 1440, image_h: int = 900) -> np.ndarray:
        """调用 VNCDoToolClient 的 captureScreenAsArray 方法捕获全屏并返回 NumPy 数组"""
        logger.debug("Capturing full screen as NumPy array using VNCDoToolClient.")

        for attempt in range(retries):
            try:
                numpy_image = self.vnc.image_numpy_locality(debug=debug,image_w=image_w, image_h=image_h,screen_num=self.screen_num) # 调用 vnc.image_numpy_locality 方法
                time.sleep(0.1)

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

    def capture_region_as_numpy(self, x1: int, y1: int, x2: int, y2: int, debug: bool = False,image_w: int = 1440, image_h: int = 900):
        """调用 VNCDoToolClient 的 captureRegionAsArray 方法捕获指定区域并返回 NumPy 数组"""
        logger.debug(f"Capturing region as NumPy array: ({x1}, {y1}, {x2}, {y2}) using VNCDoToolClient.")
        try:
            numpy_image = self.vnc.image_numpy_locality(x1, y1, x2, y2,debug=debug,image_w=image_w, image_h=image_h,screen_num=self.screen_num)
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


    def mouse_move(self,x,y,delay_time:float=0.3):# 鼠标移动
        """
        鼠标移动
        :param x: int:x坐标
        :param y: int:y坐标
        :param delay_time:点击以后延迟时间
        :return: 无
        """
        # 使用randint生成随机整数
        random_number = random.randint(1, 5)
        self.vnc.move(x+random_number,y+random_number,delay_time)
        # 随机停顿
        time.sleep(delay_time)

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
        self.vnc.left_click(x+random_number+x3,y+random_number+y3,delay_time)
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
        self.vnc.left_double_click(x + random_number+x3, y + random_number+y3,delay_time)
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
        self.vnc.right_click(x + random_number+x3, y + random_number+y3,delay_time)
        time.sleep(delay_time)

    def mouse_drag(self,x1,y1,x2,y2,step:int=50,delay_time=0.2):
        """
        鼠标拖拽,注意不完成
        :param x1: 开始拖拽坐标x
        :param y1: 开始拖拽坐标y
        :param x2: 结束拖拽坐标x
        :param y2: 结束拖拽坐标y
        :param step: 步长
        :param delay_time:点击以后延迟时间
        :return: 无
        """
        # 使用randint生成随机整数
        random_number = random.randint(1, 5)
        self.vnc.drag(x1 + random_number, y1 + random_number, x2 + random_number, y2 + random_number,delay_time=0.3, steps=step)
        time.sleep(delay_time)


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

    def key_press(self,key_str,delay_time=0.1):# 按键
        """
        按键
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
        'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'NUM0', 'NUM1', 'NUM2', 'NUM3', 'NUM4', 'NUM5',
        'NUM6', 'NUM7', 'NUM8', 'NUM9', 'SPACE', 'ENTER', 'ESC', 'TAB', 'BACKSPACE', 'MINUS', 'LEFTBRACE', 'RIGHTBRACE',
        'SEMI', 'QUOTE', 'COMMA', 'DOT', 'SLASH', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11',
        'F12', 'CTRL', 'SHIFT', 'ALT', 'WIN', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'INSERT', 'DELETE', 'HOME', 'END', 'PAGEUP',
        'PAGEDOWN', 'NUMLOCK', 'SCROLLLOCK', 'PRINTSCREEN', 'PAUSE', 'APPLICATION', 'NUMPAD_ENTER', 'NUMPAD_PLUS',
        'NUMPAD_MINUS', 'NUMPAD_MULTIPLY', 'NUMPAD_DIVIDE', 'TILDE', 'DASH', 'EQUAL', 'LEFTBRACKET', 'RIGHTBRACKET',
        'BACKSLASH', 'FORWARD_SLASH']

        'APPLICATION'  # 应用程序键
        'NUMPAD_ENTER'# 小键盘的回车键
        'NUMPAD_PLUS'# 小键盘的加号
        'NUMPAD_MINUS' # 小键盘的减号
        'NUMPAD_MULTIPLY'# 小键盘的乘号
        'NUMPAD_DIVIDE'# 小键盘的除号
        'TILDE' # 波浪号（`~）
        'DASH' # 减号（-）
        'EQUAL'  # 等号（=）
        'LEFTBRACKET' # 左方括号（[）
        'RIGHTBRACKET' # 右方括号（]）
        'BACKSLASH' # 反斜杠（\）
        'FORWARD_SLASH'# 正斜杠（/）

        :param key_str:str:字母,大写的识别率更好一些
        :param delay_time: 按键以后延迟时间
        :return: 无
        """
        key_list=list(key_dict.keys())
        if key_str in key_list:
            button=key_dict[key_str]
        else:
            button=key_str
        self.vnc.key_press(button)
        time.sleep(delay_time)

    def key_down(self,key_str,delay_time=0.1):# 按键
        """
        键按下
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
        'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'NUM0', 'NUM1', 'NUM2', 'NUM3', 'NUM4', 'NUM5',
        'NUM6', 'NUM7', 'NUM8', 'NUM9', 'SPACE', 'ENTER', 'ESC', 'TAB', 'BACKSPACE', 'MINUS', 'LEFTBRACE', 'RIGHTBRACE',
        'SEMI', 'QUOTE', 'COMMA', 'DOT', 'SLASH', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11',
        'F12', 'CTRL', 'SHIFT', 'ALT', 'WIN', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'INSERT', 'DELETE', 'HOME', 'END', 'PAGEUP',
        'PAGEDOWN', 'NUMLOCK', 'SCROLLLOCK', 'PRINTSCREEN', 'PAUSE', 'APPLICATION', 'NUMPAD_ENTER', 'NUMPAD_PLUS',
        'NUMPAD_MINUS', 'NUMPAD_MULTIPLY', 'NUMPAD_DIVIDE', 'TILDE', 'DASH', 'EQUAL', 'LEFTBRACKET', 'RIGHTBRACKET',
        'BACKSLASH', 'FORWARD_SLASH']

        'APPLICATION'  # 应用程序键
        'NUMPAD_ENTER'# 小键盘的回车键
        'NUMPAD_PLUS'# 小键盘的加号
        'NUMPAD_MINUS' # 小键盘的减号
        'NUMPAD_MULTIPLY'# 小键盘的乘号
        'NUMPAD_DIVIDE'# 小键盘的除号
        'TILDE' # 波浪号（`~）
        'DASH' # 减号（-）
        'EQUAL'  # 等号（=）
        'LEFTBRACKET' # 左方括号（[）
        'RIGHTBRACKET' # 右方括号（]）
        'BACKSLASH' # 反斜杠（\）
        'FORWARD_SLASH'# 正斜杠（/）

        :param key_str: str:字母,大写的识别率更好一些
        :param delay_time: 按下去保持时间
        :return: 无
        """
        key_list=list(key_dict.keys())
        if key_str in key_list:
            button=key_dict[key_str]
        else:
            button=key_str
        self.vnc.key_down(button,delay_time)
        time.sleep(delay_time)

    def key_up(self,key_str,delay_time=0.1):# 按键
        """
        键释放
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
        'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'NUM0', 'NUM1', 'NUM2', 'NUM3', 'NUM4', 'NUM5',
        'NUM6', 'NUM7', 'NUM8', 'NUM9', 'SPACE', 'ENTER', 'ESC', 'TAB', 'BACKSPACE', 'MINUS', 'LEFTBRACE', 'RIGHTBRACE',
        'SEMI', 'QUOTE', 'COMMA', 'DOT', 'SLASH', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11',
        'F12', 'CTRL', 'SHIFT', 'ALT', 'WIN', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'INSERT', 'DELETE', 'HOME', 'END', 'PAGEUP',
        'PAGEDOWN', 'NUMLOCK', 'SCROLLLOCK', 'PRINTSCREEN', 'PAUSE', 'APPLICATION', 'NUMPAD_ENTER', 'NUMPAD_PLUS',
        'NUMPAD_MINUS', 'NUMPAD_MULTIPLY', 'NUMPAD_DIVIDE', 'TILDE', 'DASH', 'EQUAL', 'LEFTBRACKET', 'RIGHTBRACKET',
        'BACKSLASH', 'FORWARD_SLASH']

        'APPLICATION'  # 应用程序键
        'NUMPAD_ENTER'# 小键盘的回车键
        'NUMPAD_PLUS'# 小键盘的加号
        'NUMPAD_MINUS' # 小键盘的减号
        'NUMPAD_MULTIPLY'# 小键盘的乘号
        'NUMPAD_DIVIDE'# 小键盘的除号
        'TILDE' # 波浪号（`~）
        'DASH' # 减号（-）
        'EQUAL'  # 等号（=）
        'LEFTBRACKET' # 左方括号（[）
        'RIGHTBRACKET' # 右方括号（]）
        'BACKSLASH' # 反斜杠（\）
        'FORWARD_SLASH'# 正斜杠（/）

        :param key_str: str:字母,大写的识别率更好一些
        :param delay_time: 释放后延迟时间
        :return: 无
        """
        key_list=list(key_dict.keys())
        if key_str in key_list:
            button=key_dict[key_str]
        else:
            button=key_str
        self.vnc.key_up(button,delay_time)
        time.sleep(delay_time)


# vnc=VNC_recognition("192.168.110.122")
# # vnc.mouse_right_click(500,500)
# vnc.capture_full_screen_as_numpy(debug=True,)

