import cv2
import numpy as np
"""
更新日志:2024-9-29 12:51:05
更新内容:
    cpu版本,使用numpy的布尔索引提前过滤主颜色
    注意opencv读取的图片是bgr格式.
"""

# 定义 get_rgb_from_hex 函数
def get_rgb_from_hex(hex_color):
    """将十六进制颜色转换为 RGB 颜色"""
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


# 计算相对坐标
def calculate_relative_positions(colors):
    """计算相对坐标"""
    main_color = next(iter(colors))
    main_position = colors[main_color]

    relative_positions = {color: (pos[0] - main_position[0], pos[1] - main_position[1])
                          for color, pos in colors.items() if color != main_color}

    return main_color, relative_positions


# 判断颜色是否在允许的偏差范围内
def is_color_within_tolerance(color1, color2, tolerance):
    """判断两个颜色是否在允许的偏差范围内"""
    return np.all(np.abs(np.array(color1) - np.array(color2)) <= tolerance)


# 优化：使用 NumPy 的布尔索引提前过滤主颜色
def filter_main_color(image_array, main_rgb, tolerance):
    """使用布尔索引提前过滤出与主颜色接近的像素"""
    # 计算每个像素与主颜色的差异
    diff = np.abs(image_array - main_rgb)

    # 在三个通道上都满足容差条件的像素
    mask = np.all(diff <= tolerance, axis=-1)

    # 返回满足条件的像素的坐标
    return np.argwhere(mask)


# 查找符合条件的三点并记录主颜色坐标，允许颜色偏差
def find_points_with_tolerance(image_array, colors, relative_positions, tolerance=10, offset_x=0, offset_y=0):
    """在图像中查找符合条件的点，允许颜色偏差"""
    if not image_array.size or not colors:
        return []

    main_color, _ = next(iter(colors.items()))
    main_rgb = np.array(get_rgb_from_hex(main_color))

    height, width, _ = image_array.shape
    matching_positions = []

    # 优化：提前过滤出与主颜色匹配的像素
    main_color_candidates = filter_main_color(image_array, main_rgb, tolerance)

    # 遍历所有与主颜色匹配的候选像素
    for y, x in main_color_candidates:
        if is_surrounding_colors_match(image_array, x, y, relative_positions, tolerance):
            matching_positions.append((int(x + offset_x), int(y + offset_y)))

    return matching_positions


def is_surrounding_colors_match(image_array, x, y, relative_positions, tolerance):
    """判断相对位置的颜色是否匹配"""
    height, width, _ = image_array.shape

    for color, (dx, dy) in relative_positions.items():
        target_x = x + dx
        target_y = y + dy

        # 检查目标坐标是否在图像范围内
        if not (0 <= target_x < width and 0 <= target_y < height):
            return False

        target_color = image_array[target_y, target_x]
        expected_rgb = get_rgb_from_hex(color)

        # 如果颜色不匹配，则返回 False
        if not is_color_within_tolerance(target_color, expected_rgb, tolerance):
            return False

    return True

def multipoint_colors_rgb(image_array, colors, tolerance:int=10, x:int=0, y:int=0):
    """主函数：在图像中查找符合条件的颜色点"""

    main_color, relative_positions = calculate_relative_positions(colors)
    # print("v4,cpu版本")
    return find_points_with_tolerance(image_array, colors, relative_positions, tolerance, x, y)

def multipoint_colors(image_array, colors, tolerance:int=10, x:int=0, y:int=0):
    """主函数：在图像中查找符合条件的颜色点"""

    if isinstance(image_array, np.ndarray) :#注意通过Image.open读取的图片为RGB格式，注销掉该行
        # logger.debug("输入为cv2格式")
        image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

    main_color, relative_positions = calculate_relative_positions(colors)
    # print("v4,cpu版本")
    return find_points_with_tolerance(image_array, colors, relative_positions, tolerance, x, y)


# 测试代码
# if __name__ == "__main__":
#     # 定义颜色和坐标
#     colors= {"cc6d00": (1267, 342),
#                "884900": (1276, 347),
#                "995200": (1284, 342),
#                "ff8800": (1284, 351), }
#
#     # 读取图像并转换为 NumPy 数组
#     image_path = r'D:\pc_work\dtwsv2\image_vnc\5901.png'
#     image = Image.open(image_path)
#     image_array = np.array(image)
# #
#     # 调用函数查找匹配的坐标
#     res = multipoint_colors(image_array, colors, tolerance=10, x=0, y=0)
#     print(res)
