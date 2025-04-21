import socket
import time

import cv2
import numpy as np
import win32con
import win32gui
from win32ui import  CreateBitmap, CreateDCFromHandle
from win32gui import GetWindowDC, GetClientRect,  BitBlt,  ReleaseDC, DeleteObject
from loguru import logger
from ctypes import windll



class Command:
    def __init__(self, socket_ip:str):
        """
        初始化 Command 类
        :param server_address: 服务器地址和端口，默认为 ('localhost', 12345)
        """
        self.socket_ip = socket_ip
        self.server_address = (self.socket_ip, 49152)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def find_windows(self):
        """
        查找符合指定标题或类名的窗口
        :return:[],[986344, 133040]
        """
        found_windows = []
        title_pattern = self.socket_ip
        class_pattern = "TscShellContainerClass"

        def enum_windows_callback(hwnd, extra):
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            if (title_pattern and title_pattern in title) and (class_pattern and class_pattern in class_name):
                found_windows.append(hwnd)

        win32gui.EnumWindows(enum_windows_callback, None)
        return found_windows

    def image_numpy_locality(self, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0, debug: bool = False,image_w: int = 1440, image_h: int = 900,screen_num:int=2):
        """接收图像数据
        :param x1: 截图区域的左上角x坐标
        :param y1: 截图区域的左上角y坐标
        :param x2: 截图区域的右下角x坐标
        :param y2: 截图区域的右下角y坐标
        :param image_w: 图像的宽度，默认为 1440
        :param image_h: 图像的高度，默认为 900
        :param screen_num: 屏幕编号，默认为 2
        :param debug: 是否启用调试模式，默认为 False
        :return: 返回接收到的图像数据的三维 NumPy 数组
        """
        # 发送截图命令
        self.send_command(f"screenshot,{screen_num}")
        # print("已发送截图命令。")

        # 接收图像大小
        img_size_bytes = self.sock.recv(4)
        img_size = int.from_bytes(img_size_bytes, 'big')
        # print(f"接收到图像大小: {img_size} 字节")

        # 接收图像数据
        img_data = bytearray()
        while len(img_data) < img_size:
            packet = self.sock.recv(img_size - len(img_data))  # 根据剩余大小接收
            if not packet:
                break
            img_data.extend(packet)

        # 将图像数据转换为 NumPy 数组
        img_np = np.frombuffer(img_data, dtype=np.uint8)


        # 检查数据大小是否与预期匹配
        expected_size = image_h * image_w * 3  # 计算预期的字节数（RGB图像）
        if img_np.size != expected_size:
            logger.error(f"接收到的图像数据大小不匹配: {img_np.size} (实际) vs {expected_size} (预期)")
            return None  # 返回 None 表示发生了错误

        # 处理图像数据
        img = img_np.reshape((image_h, image_w, 3))  # 重新调整为图像尺寸

        if any((x1, y1, x2, y2)):
            img = img[y1:y2, x1:x2]  # 根据坐标切片图像

        if debug:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # 转换颜色格式
            cv2.imwrite("screenshot.jpg", img)  # 保存图像
            logger.success(f"图像已保存")

        return img  # 返回三维 NumPy 数组

    # def image_numpy_locality(self,x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0, debug: bool = False):
    #     """
    #     适用于游戏本地游戏的情况
    #     截取指定窗口的图像并返回OpenCV格式的图像数组
    #     :param x1: 截图区域的左上角x坐标
    #     :param y1: 截图区域的左上角y坐标
    #     :param x2: 截图区域的右下角x坐标
    #     :param y2: 截图区域的右下角y坐标
    #     :param debug: 是否保存截图
    #     :return: OpenCV格式的图像数组或None如果失败
    #     """
    #
    #     try:
    #         win_hand=self.find_windows()
    #         hwnd=win_hand[0]
    #         logger.info(f"获取窗口的句柄{hwnd}")
    #         # 获取窗口的尺寸
    #         if x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0:
    #             # 获取客户区的尺寸
    #             left, top, right, bot = GetClientRect(hwnd)
    #             w = right - left
    #             h = bot - top
    #         else:
    #             w = x2 - x1
    #             h = y2 - y1
    #         # 创建设备上下文
    #         hwndDC = GetWindowDC(hwnd)
    #         mfcDC = CreateDCFromHandle(hwndDC)
    #         saveDC = mfcDC.CreateCompatibleDC()
    #         # 创建位图对象准备保存图片
    #         saveBitMap = CreateBitmap()
    #         saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    #         # 将截图保存到saveBitMap中
    #         saveDC.SelectObject(saveBitMap)
    #         if x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0:
    #             result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)  # 1为客户区截图
    #         else:
    #             # 这里我们只是简单地复制窗口的内容到位图中
    #             result = BitBlt(saveDC.GetSafeHdc(), 0, 0, w, h, hwndDC, x1, y1, win32con.SRCCOPY)
    #
    #         # 将位图数据转换为字节数组
    #         bmp_info = saveBitMap.GetInfo()
    #         bmp_str = saveBitMap.GetBitmapBits(True)
    #
    #         # 使用numpy将字节数组转换为图像数组
    #         img_array = np.frombuffer(bmp_str, dtype=np.uint8)
    #         img_array.shape = (h, w, 4)  # 注意BMP默认是BGRA格式
    #         # 使用 OpenCV 转换为 RGB 格式
    #         rgb_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2RGB)
    #
    #         # 保存图片到硬盘,测试用
    #         if debug:
    #             logger.info("保存截图")
    #             if img_array.dtype != np.uint8:  # 检查 img_array 的数据类型是否为 uint8
    #                 img_array = (img_array * 255).astype(np.uint8)  # 如果不是，将其转换为 uint8 类型
    #             cv2.imwrite('shan_client.jpg', img_array)  # 保存为 .jpg 文件
    #
    #         # 清理资源
    #         mfcDC.DeleteDC()
    #         saveDC.DeleteDC()
    #         ReleaseDC(hwnd, hwndDC)
    #         DeleteObject(saveBitMap.GetHandle())
    #
    #         return rgb_array
    #     except Exception as e:
    #         # print(f"保存截图失败: {e}")
    #         return None

    def connect(self):
        """连接到服务器"""
        try:
            # print("正在连接到服务器...")
            self.sock.connect(self.server_address)
            # print("连接成功！")
        except Exception as e:
            pass
            # print(f"连接失败: {e}")

    def send_command(self, command):
        """
        发送命令到服务器

        :param command: 要发送的命令字符串
        """
        try:
            # print(f"发送命令: {command}")
            self.sock.sendall(command.encode('utf-8'))
        except Exception as e:
            pass
            # print(f"发送命令时发生错误: {e}")

    def right_click(self, x, y, delay_time:float=0.3):
        """
        发送右键点击命令

        :param x: 点击的 x 坐标
        :param y: 点击的 y 坐标
        :param delay_time:float=0.3: 执行点击的持续时间
        """
        command = f"right_click,{x},{y},{delay_time}"
        self.send_command(command)

    def left_click(self, x, y, delay_time:float=0.3):
        """
        发送左键点击命令

        :param x: 点击的 x 坐标
        :param y: 点击的 y 坐标
        :param delay_time:float=0.3: 执行点击的持续时间
        """
        command = f"left_click,{x},{y},{delay_time}"
        self.send_command(command)

    def left_double_click(self, x, y, delay_time:float=0.3):
        """
        发送左双击命令

        :param x: 点击的 x 坐标
        :param y: 点击的 y 坐标
        :param delay_time:float=0.3: 执行双击的持续时间
        """
        command = f"left_double_click,{x},{y},{delay_time}"
        self.send_command(command)

    def move (self, x, y, delay_time:float=0.3):
        """
        发送移动命令
        :param x: 点击的 x 坐标
        :param y: 点击的 y 坐标
        :param delay_time:float=0.3: 执行双击的持续时间
        """
        command = f"move,{x},{y},{delay_time}"
        self.send_command(command)

    def drag(self, start_x, start_y, end_x, end_y, delay_time:float=0.3, steps:int=60):
        """
        发送拖动命令

        :param start_x: 拖动起始点的 x 坐标
        :param start_y: 拖动起始点的 y 坐标
        :param end_x: 拖动结束点的 x 坐标
        :param end_y: 拖动结束点的 y 坐标
        :param delay_time:float=0.3: 执行拖动的持续时间
        :param steps: 拖动过程中的步骤数
        """
        command = f"drag,{start_x},{start_y},{end_x},{end_y},{delay_time},{steps}"
        self.send_command(command)

    def key_press(self, key, delay_time:float=0.3):
        """
        发送按键命令

        :param key: 要按下的按键
        :param delay_time:float=0.3: 按键按下的持续时间
        """
        command = f"key_press,{key},{delay_time}"
        self.send_command(command)

    def key_down(self, key, delay_time:float=0.3):
        """
        发送按键按下命令
        """
        command= f"key_down,{key},{delay_time}"
        self.send_command(command)

    def key_up(self, key, delay_time:float=0.3):
        """
        发送按键抬起命令
        """
        command= f"key_up,{key},{delay_time}"
        self.send_command(command)

    def close(self):
        """关闭连接"""
        self.sock.close()
        # print("连接已关闭。")

# def main():
#     command = Command('192.168.110.122')
#     command.connect()
#     #
#     # for i in range(10):
#     #     time.sleep(1)
#     #     command.image_numpy_locality()
#     # res=command.image_numpy_locality(100,100,200,200)
#     # print(res)
#     # command.move(100,100,delay_time=1)
#
#     # # 发送各种命令
#     # command.right_click(500, 500, 0.3)  # 右键点击
#     # command.left_click(500, 500, 0.3)   # 左键点击
#     # command.left_double_click(44,441, 0.3)  # 左双击
#     # command.drag(2334, 44, 1882, 324, 0.3, 30)  # 拖动
#     # command.key_press('NUM9')  # 按下 'M' 键
#
#     command.close()  # 关闭连接
#
# if __name__ == "__main__":
#     main()