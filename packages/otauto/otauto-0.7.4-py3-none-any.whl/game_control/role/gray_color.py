import cv2
import numpy as np
from PIL import Image
"""
功能:计算图片中灰阶颜色的比例
更新日志:2024-11-13 13:15:33
"""


def is_gray(color):
    # 一个颜色是灰色的条件是：R=G=B
    return color[0] == color[1] == color[2]

def gray_ratio(input_data):
    """
    计算图片中灰色调的比例
    # 示例用法
        image_path = "res/dtws/demo/灰阶图02.bmp"
        gray_proportion = gray_ratio(image_path)
        print(f"Gray proportion: {gray_proportion:.2%}")
    :param input_data: 图片路径字符串或 numpy 数组
    :return:
    """
    if isinstance(input_data, str):
        # 使用 imread 读取图片，确保可以读取中文路径
        image = cv2.imdecode(np.fromfile(input_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Cannot load image from the provided path.")
    elif isinstance(input_data, np.ndarray):
        image = input_data
    else:
        raise ValueError("Input must be a file path or numpy array.")

    # 获取图片的像素点总数
    total_pixels = image.size / 3  # 因为每个像素点有三个分量（B、G、R）

    # 获取灰色调像素点的数量
    gray_pixels = 0
    for row in image:
        for pixel in row:
            if is_gray(pixel):
                gray_pixels += 1

    # 计算灰色调像素的比例
    gray_ratio = gray_pixels / total_pixels

    return gray_ratio


# 示例用法
# 从文件读取
# image_path = r"D:\pc_work\dtwsv2_v4.0\res\dtws\demo\灰阶图.bmp"
# gray_proportion_from_file = gray_ratio(image_path)
# print(f"Gray proportion from file: {gray_proportion_from_file:.2%}")

# # 从numpy数组读取
# img = Image.open(image_path)
# numpy_array = np.array(img)
# gray_proportion_from_array = gray_ratio(numpy_array)
# print(f"Gray proportion from numpy array: {gray_proportion_from_array:.2%}")





