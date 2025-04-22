import cv2
import numpy as np
import os
from pathlib import Path
from scipy.spatial import distance
"""
功能:范围内单颜色查找,也支持多个单颜色识别
"""


def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (4, 2, 0))

def imread_with_chinese_path(image_path):
    if isinstance(image_path, Path):
        image_path = str(image_path)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"No such file: '{image_path}'")
    img = np.fromfile(image_path, dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


def find_color_in_image(img, target_hex, tolerance=10, distance_threshold=5, x3=0, y3=0):
    """
    在范围内指定单颜色或多颜色是否存在
    :param img: numpy数组
    :param target_hex: 以'|'分隔的hex颜色字符串
    :param tolerance: 颜色容差
    :param distance_threshold: 像素之间距离阈值
    :param x3: x轴偏移量
    :param y3: y轴偏移量
    :return: {"fdfbad":{}, "ffffff":{}}，每种颜色返回其找到的坐标群
    """

    # Step 1: Split the target_hex string into a list of hex colors
    hex_colors = target_hex.split('|')

    result = {}

    for hex_color in hex_colors:
        # Convert target hex color to RGB
        target_rgb = hex_to_bgr(hex_color)

        # Define lower and upper bounds based on the tolerance
        lower_bound = np.array([max(0, c - tolerance) for c in target_rgb])
        upper_bound = np.array([min(255, c + tolerance) for c in target_rgb])

        # Create masks to locate the colors within the tolerance in the image
        image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) #颜色转换,实际生产环境中，需要将图片转换为RGB格式,测试阶段，注销改行
        mask = cv2.inRange(image, lower_bound, upper_bound)

        # Find coordinates of the pixels that match the target color
        coordinates = np.column_stack(np.where(mask > 0))

        # Helper function to find clusters based on distance threshold
        def cluster_coordinates(coords, threshold):
            clusters = []
            for coord in coords:
                found_cluster = False
                for cluster in clusters:
                    if any(distance.euclidean(coord, point) <= threshold for point in cluster):
                        cluster.append(coord)
                        found_cluster = True
                        break
                if not found_cluster:
                    clusters.append([coord])
            return clusters

        # Cluster the coordinates based on distance threshold
        clustered_coords = cluster_coordinates(coordinates, distance_threshold)

        # Create a dictionary to store the coordinates with x+x3 and y+y3
        color_result = {}

        for idx, cluster in enumerate(clustered_coords, 1):
            color_result[idx] = [(x + x3, y + y3) for x, y in cluster]

        result[hex_color] = color_result

    return result

#
# # Example usage
# image_path = r'D:\pc_work\dtwsv2_v4.0\res\dtws\demo\单色测试.bmp'  # Replace with the path to your image, which can include Chinese characters
# target_hex = 'fff5cf|f4e52b'  # White color
# img=imread_with_chinese_path(image_path)
#
# # Find the coordinates
# coordinates_dict = find_color_in_image(img, target_hex)
#
# # Print the coordinates
# for key in coordinates_dict:
#     print(f"{key}: {coordinates_dict[key]}")