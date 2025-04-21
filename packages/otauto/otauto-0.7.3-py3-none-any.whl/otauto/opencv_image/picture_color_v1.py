import cv2
import numpy as np
from PIL import Image
from sklearn.neighbors import KDTree
"""
更新日志:2024-11-8 09:01:36
获取图片中的所有颜色，并去除相似颜色
"""

def rgb_to_hex(rgb):
    """
    将RGB颜色转换为十六进制颜色代码
    :param rgb:
    :return:
    """
    return '{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def color_distance(color1, color2):
    """
    计算两个颜色之间的欧氏距离
    :param color1:
    :param color2:
    :return:
    """
    return np.sqrt(np.sum((np.array(color1) - np.array(color2)) ** 2))

def get_image_from_path(image_path):
    """
    使用PIL读取图像并转换为OpenCV格式
    :param image_path: 图片路径
    :return: OpenCV格式的图像
    """
    pil_image = Image.open(image_path)
    # Convert PIL image to OpenCV format (numpy array)
    open_cv_image = np.array(pil_image)
    # Convert RGB to BGR
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
    return open_cv_image

def get_unique_colors(image_path, distance_threshold=10):
    """
    获取图片中的所有颜色，并去除相似颜色
    # 示例使用
    image_path = r'D:\pc_work\dtwsv2_v4.0\res\dtws\image_map_达摩洞一层\demo_1.png'  # 替换成你图片的路径
    colors = get_unique_colors(image_path, distance_threshold=10)  # 距离阈值可以根据需求调整
    #['4c4533', '524b39', '58513f', '5e5745','6f6450',]
    print(colors)
    :param image_path: 图片路径
    :param distance_threshold: 相似颜色的距离阈值
    :return:
    """
    # 读取图片
    img = get_image_from_path(image_path)
    # 将BGR格式转换为RGB格式
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 获取图片的所有像素颜色
    pixels = img.reshape((-1, 3))
    # 转换为元组并去重
    unique_colors = set(tuple(color) for color in pixels)
    # 将颜色排序
    sorted_unique_colors = sorted(unique_colors)
    # 去除相似颜色
    reduced_colors = []
    for color in sorted_unique_colors:
        if not reduced_colors:
            reduced_colors.append(color)
        else:
            if all(color_distance(color, existing_color) >= distance_threshold for existing_color in reduced_colors):
                reduced_colors.append(color)
    # 转换为十六进制表示
    hex_colors = [rgb_to_hex(color) for color in reduced_colors]
    return hex_colors

def get_unique_colors_tree(image_path, distance_threshold=10):
    """
    获取图片中的所有颜色，并去除相似颜色
    :param image_path: 图片路径
    :param distance_threshold: 相似颜色的距离阈值
    :return:
    """
    # 读取图片
    img = get_image_from_path(image_path)
    # 将BGR格式转换为RGB格式
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 获取图片的所有像素颜色
    pixels = img.reshape((-1, 3))
    # 转换为元组并去重
    unique_colors = list(set(map(tuple, pixels)))
    # 构造KD树
    tree = KDTree(unique_colors)
    # 标记已访问的颜色
    visited = set()
    reduced_colors = []
    for i, color in enumerate(unique_colors):
        if i in visited:
            continue
        reduced_colors.append(color)
        # 获取在distance_threshold范围内的所有颜色
        distances, indices = tree.query_radius([color], r=distance_threshold, return_distance=True)
        for idx in indices[0]:
            visited.add(idx)
    # 转换为十六进制表示
    hex_colors = [rgb_to_hex(color) for color in reduced_colors]
    return hex_colors

def filter_similar_colors(colors_hex, tolerance):
    """
    去掉小于容差范围的颜色
    # 示例用法
    colors_hex = ['4c4533', '524b39', '58513f', '5e5745','6f6450', '756a56', '7b705e', '817565', '877b6b','423a2f', '493f35', '514539', '574b3f']
    tolerance = 10
    filtered_colors = filter_similar_colors(colors_hex, tolerance)
    print(filtered_colors)
    :param colors_hex: 颜色列表
    :param tolerance: 颜色容差
    :return: 过滤过的颜色列表
    """
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def euclidean_distance(color1, color2):
        return sum((a - b) ** 2 for a, b in zip(color1, color2)) ** 0.5

    colors_rgb = [hex_to_rgb(color) for color in colors_hex]
    filtered_colors = []

    for i, color1 in enumerate(colors_rgb):
        is_similar = False
        for j, color2 in enumerate(colors_rgb):
            if i != j and euclidean_distance(color1, color2) <= tolerance:
                is_similar = True
                break
        if not is_similar:
            filtered_colors.append(colors_hex[i])
    return filtered_colors


# 示例使用
image_path = r'D:\pc_work\dtwsv2_v4.0\res\dtws\demo\红名.bmp'  # 替换成你图片的路径
colors = get_unique_colors(image_path, distance_threshold=10)  # 距离阈值可以根据需求调整
#['4c4533', '524b39', '58513f', '5e5745','6f6450',]
print(colors)

