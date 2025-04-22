import cv2
import numpy as np
from loguru import logger
"""
更新日志:2024-9-29 12:49:43
更新内容:去除背景色功能,增加颜色容差,增加测试功能
"""

def hex_to_rgb(hex_color):
    """
    将16进制颜色转换为RGB格式
    :param hex_color: 16进制颜色字符串，例如 "#RRGGBB"
    :return: RGB格式的列表，例如 [R, G, B]
    """
    # 去掉可能存在的 '#' 符号
    hex_color = hex_color.lstrip('#')

    # 将每个两位的16进制数转换为十进制数
    rgb = [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]

    return rgb


def hex_to_bgr(hex_color):
    """
    将16进制颜色转换为BGR格式
    :param hex_color:
    :return:
    """
    rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    return list(reversed(rgb))

def remove_isolated_pixels(img, distance_threshold=10, is_open_operation=True):
    struct_elem = cv2.getStructuringElement(cv2.MORPH_RECT, (distance_threshold, distance_threshold))
    if is_open_operation:
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, struct_elem)
    else:
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, struct_elem)
    return img

def background_color_processing(image_data, color_list:list, tolerance:int=40,test_function:bool=False):
    """
    根据颜色字典过滤图片
    :param image_data: 图片数据
    :param color_dict: 颜色字典
    :param tolerance: 容差
    :param test_function: 是否测试
    :return:
    """
    # logger.info("开始背景色过滤")
    if color_list is None:
        logger.info("颜色筛选列表为空,返回原数据")
        return  image_data
    if color_list:
        # 判断输入的是否是字符串
        if isinstance(image_data, str):
            image_data = cv2.imdecode(np.fromfile(image_data,dtype=np.uint8),-1)
        else:
            image_data = image_data

        # 检查图像是否正确读取
        if image_data is not None:
            # 获取图像的通道数
            num_channels = image_data.shape[2] if len(image_data.shape) > 2 else 1

            # if num_channels == 1:
            #     print("图像模式：灰度图")
            # if num_channels == 3:
            #     print("图像模式：彩色图 (BGR)")
            if num_channels == 4:
                # print("图像模式：带 Alpha 通道的彩色图 (BGRA)")
                image_data = cv2.cvtColor(image_data, cv2.COLOR_BGRA2BGR)

        bgr_color_range = {color: (np.array(hex_to_bgr(color)) - tolerance, np.array(hex_to_bgr(color)) + tolerance) for color in color_list}

        res = np.zeros_like(image_data)

        # 循环过滤每种颜色
        for color, (lower, upper) in bgr_color_range.items():
            mask = cv2.inRange(image_data, lower, upper)
            color_res = cv2.bitwise_and(image_data, image_data, mask=mask)
            res = cv2.bitwise_or(res, color_res)

        # todo,使用形态学的闭操作去除距离大于10像素的离群点,效果不好
        res = remove_isolated_pixels(res, 1)

        if test_function:
            # 保存图片至文件
            cv2.imwrite('filtered_image.jpg', res)

        # logger.info("背景色过滤完成")
        return res




# 背景色过滤功能,保留的颜色
# background_list=['2df9f9','f0e8df','ed140f', '2df9f9',"fec86a"]
# image_path=r'D:\pc_work\dtwsv2\image_vnc\5901_area.png'

# image_path = r"D:\pc_work\dtwsv2_v4.0\res\dtws\demo\demo-010.png"  # 替换为你的图片路径
# background_list = ['c2aa66', '817b3c', '7f7336',"8f7839"]  # 替换为你的目标颜色
#
# res=background_color_processing(image_path,background_list,30,True)



