"""
功能:掉小于容差范围的颜色
更新日志:2024-11-13 13:16:40
"""
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

# # 示例用法
# colors_hex = ['4c4533', '524b39', '58513f', '5e5745','6f6450', '756a56', '7b705e', '817565', '877b6b','423a2f', '493f35', '514539', '574b3f']
# tolerance = 10
# filtered_colors = filter_similar_colors(colors_hex, tolerance)
# print(filtered_colors)