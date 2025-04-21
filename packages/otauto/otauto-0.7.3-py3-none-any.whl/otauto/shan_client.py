import time
import cv2
import numpy as np
import zmq
from PIL import Image
from otauto.log import ColoredLogger

logger = ColoredLogger()
# 移除日志
logger.remove()

class Command:
    def __init__(self,window_ip:str="127.0.0.1"):
        """
        初始化 Command 类
        """
        self.context = zmq.Context()
        self.window_ip=window_ip

        # 创建 REQ 套接字,截图
        self.screenshot_socket = self.context.socket(zmq.REQ)
        self.screenshot_socket.connect(f'tcp://{self.window_ip}:49151')

        # 创建套接字,鼠标
        self.mouse_socket = self.context.socket(zmq.REQ)
        self.mouse_socket.connect(f"tcp://{self.window_ip}:49152")

        # 创建套接字,键盘
        self.keyboard_socket = self.context.socket(zmq.REQ)
        self.keyboard_socket.connect(f"tcp://{self.window_ip}:49153")

    def connect(self):
        """连接到服务器"""
        try:
            print("正在连接到服务器...")
            self.screenshot_socket.connect(f'tcp://{self.window_ip}:49151')
            self.mouse_socket.connect(f"tcp://{self.window_ip}:49152")
            self.keyboard_socket.connect(f"tcp://{self.window_ip}:49153")
            print("连接成功！")
        except Exception as e:
            print(f"连接失败: {e}")


    def right_click(self, x, y, delay_time:float=0.3):
        """
        发送右键点击命令

        :param x: 点击的 x 坐标
        :param y: 点击的 y 坐标
        :param delay_time:float=0.3: 执行点击的持续时间
        """
        command = f"right_click,{x},{y},{delay_time}"
        self.mouse_socket.send(command.encode('utf-8'))
        time.sleep(delay_time)
        res=self.mouse_socket.recv_string()
        return res

    def left_click(self, x, y, delay_time:float=0.3):
        """
        发送左键点击命令

        :param x: 点击的 x 坐标
        :param y: 点击的 y 坐标
        :param delay_time:float=0.3: 执行点击的持续时间
        """
        command = f"left_click,{x},{y},{delay_time}"
        self.mouse_socket.send(command.encode('utf-8'))
        time.sleep(delay_time)
        res=self.mouse_socket.recv_string()
        return res

    def left_double_click(self, x, y, delay_time:float=0.3):
        """
        发送左双击命令

        :param x: 点击的 x 坐标
        :param y: 点击的 y 坐标
        :param delay_time:float=0.3: 执行双击的持续时间
        """
        command = f"left_double_click,{x},{y},{delay_time}"
        self.mouse_socket.send(command.encode('utf-8'))
        time.sleep(delay_time)
        res=self.mouse_socket.recv_string()
        return res

    def move(self, x, y, delay_time:float=0.3):
        """
        发送鼠标移动命令
        """
        command=f"move,{x},{y},{delay_time}"
        self.mouse_socket.send(command.encode('utf-8'))
        time.sleep(delay_time)
        res=self.mouse_socket.recv_string()
        return res

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
        self.mouse_socket.send(command.encode('utf-8'))
        time.sleep(delay_time)
        res=self.mouse_socket.recv_string()
        return res

    def key_press(self, key, delay_time:float=0.3):
        """
        发送按键命令

        :param key: 要按下的按键
        :param delay_time:float=0.3: 按键按下的持续时间
        """
        command = f"key_press,{key},{delay_time}"
        self.keyboard_socket.send(command.encode('utf-8'))
        time.sleep(delay_time)
        res=self.keyboard_socket.recv_string()
        logger.success(res)
        return res

    def key_up (self, key, delay_time:float=0.1):
        """
        发送按键抬起命令
        """
        command = f"key_up,{key},{delay_time}"
        self.keyboard_socket.send(command.encode('utf-8'))
        time.sleep(delay_time)
        res=self.keyboard_socket.recv_string()
        return res

    def key_down(self, key, delay_time:float=0.3):
        """
        发送按键按下命令
        """
        command = f"key_down,{key},{delay_time}"
        self.keyboard_socket.send(command.encode('utf-8'))
        time.sleep(delay_time)
        res=self.keyboard_socket.recv_string()
        return res


    def image_numpy_locality(self, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0, debug: bool = False,image_w: int = 1440, image_h: int = 900,screen_num:int=1):
        """
        接收图像数据
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
        command=f"{screen_num}"
        self.screenshot_socket.send(command.encode('utf-8'))
        # print("已发送截图命令。")

        # 接收响应
        bmp_data = self.screenshot_socket.recv()  # 接收字节流
        if bmp_data == b"Invalid screen index":
            # print("错误: 无效的屏幕索引")
            return

        # 将字节数据转换为 NumPy 数组
        image_data = np.frombuffer(bmp_data, dtype=np.uint8)  # 将字节流转换为 NumPy 数组

        # 确保数组的长度与预期的图像大小相符
        if image_data.size != image_w * image_h * 4:
            # print(f"错误: 接收到的图像数据大小不匹配，实际大小: {image_data.size}")
            return

        # 重新排列为 (height, width, 4)
        image_data = image_data.reshape((image_h, image_w, 4))

        # 转换为 RGB 格式
        rgb_image_data = image_data[:, :, [2, 1, 0]]  # 重新排列通道

        if any((x1, y1, x2, y2)):
            rgb_image_data = rgb_image_data[y1:y2, x1:x2]  # 根据坐标切片图像

        if debug:
            # 打印数组的形状
            # print("图像的形状:", image_data.shape)  # 输出形状，例如 (高度, 宽度, 通道数)
            # 将其转换为 Pillow 图像
            image = Image.fromarray(rgb_image_data, 'RGB')
            # 保存图像到文件
            image.save(f'screenshot_{screen_num}.png')  # 或者使用 .bmp 扩展名

        return rgb_image_data


    def close(self):
        """关闭连接"""
        self.screenshot_socket.close()
        self.mouse_socket.close()
        self.keyboard_socket.close()
        print("连接已关闭。")

def main():
    command = Command("192.168.110.122")
    command.connect()

    # 发送各种命令
    # command.right_click(500, 500, 0.3)  # 右键点击
    res=command.image_numpy_locality(debug=True)
    # print("数组是:",res)
    # command.left_click(500, 500, 0.3)   # 左键点击
    # time.sleep(0.1)
    # command.left_double_click(44,441, 0.3)  # 左双击wwwwwb
    # command.drag(2334, 44, 1882, 324, 0.3, 30)  # 拖动w
    #
    # command.key_down('W',delay_time=1)
    # time.sleep(1)
    # command.key_up('W',delay_time=1)  # 按下 'M'
    # command.key_press('B')
    # command.close()  # 关闭连接

if __name__ == "__main__":
    main()