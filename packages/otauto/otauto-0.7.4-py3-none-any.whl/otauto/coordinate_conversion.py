import math
import re
from loguru import logger
"""
注意,要固定视角,最好2.5d视角
人物在屏幕中间
大唐无双是特殊的x,y坐标系,要是其他游戏请在
coordinate_point_conversion方法里改成
angle_degrees =angle-45 改成angle_degrees =angle
"""
def insert_intermediate_points_on_line(coordinate_node,threshold:int=3):
    """
    插值坐标点
    示例代码:
        coordinate_node = [(118, 100), (116, 104), (113, 111), (111, 120), (112, 125), (113, 129), (113, 135), (112, 141), (109, 150), (106, 156)]
        new_coordinate_node = insert_intermediate_points_on_line(coordinate_node)
        print(new_coordinate_node)
    :coordinate_node:坐标列表
    :threshold:插值阈值
    """
    def interpolate_points(p1, p2):
        points = [p1]
        x1, y1 = p1
        x2, y2 = p2

        while abs(x2 - x1) > threshold or abs(y2 - y1) > threshold:
            if abs(x2 - x1) > threshold:
                step_x = threshold if x2 > x1 else -threshold
            else:
                step_x = x2 - x1

            if abs(x2 - x1) != 0:
                step_y = (step_x * (y2 - y1)) / (x2 - x1)
                if abs(step_y) > threshold:
                    step_y = threshold if y2 > y1 else -threshold
                    step_x = (step_y * (x2 - x1)) / (y2 - y1)
            else:
                step_y = threshold if y2 > y1 else -threshold

            new_point = (x1 + step_x, y1 + step_y)
            points.append((int(new_point[0]), int(new_point[1])))
            x1, y1 = int(new_point[0]), int(new_point[1])

        points.append(p2)
        return points

    new_coordinate_node = []
    for i in range(len(coordinate_node) - 1):
        new_coordinate_node.extend(interpolate_points(coordinate_node[i], coordinate_node[i + 1])[:-1])

    new_coordinate_node.append(coordinate_node[-1])
    return new_coordinate_node


def distance_and_angle_scaled(x1, y1, x2, y2, scale=45):
    """
    计算两点之间的距离和角度，并按比例缩放坐标
    注意是计算正常笛卡尔坐标系下,不是屏幕坐标
    示例代码
    x1, y1 = 120, 100 #起点坐标
    x2, y2 = 117,102 #目标坐标
    distance, angle = distance_and_angle_scaled(x1, y1, x2, y2)
    print(f"Distance: {distance}") #长度
    print(f"Angle (degrees): {angle}") #角度

    :param x1: 起点坐标x
    :param y1: 起点坐标y
    :param x2: 目的坐标x
    :param y2: 目的坐标y
    :param scale: 坐标和像素点之间的比例:45,50,55
    :return:
    """
    dx = (x2 - x1) * scale
    dy = (y2 - y1) * scale
    distance = math.sqrt(dx ** 2 + dy ** 2)
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    if angle_deg < 0:# 转换为正角度
        angle_deg += 360
    return distance, angle_deg


def coordinate_point_conversion(x1, y1,x2,y2,scale:int=45,x_role:int=720,y_role:int=450,x_scene:int=720,y_scene:int=450,debug:bool=False):
    """
    示例代码:
    x1, y1 = 117, 103 #起点坐标
    x2, y2 = 120,100 #目标坐标
    x_role, y_role = (720, 450)  # 角色位置,原点坐标,人物是在屏幕中间
    x_point, y_point = coordinate_point_conversion(x1, y1, x2, y2,debug=True)
    print(x_point,y_point)

    换算游戏坐标和屏幕坐标之间的关系
    :param x1: 游戏坐标x
    :param y1: 游戏坐标y
    :param x2: 屏幕坐标x
    :param y2: 屏幕坐标y
    :param scale: 坐标和像素点之间的比例:45,50,55
    :param x_role: 角色在场景中的坐标x
    :param y_role: 角色在场景中的坐标y
    :param x_scene: 游戏里x轴的长度
    :param y_scene: 游戏里y轴的长度
    :param debug: 是否开启调试
    :return: (x,y)角色在场景中的移动位置
    """
    x_destination,y_destination=0,0
    distance, angle = distance_and_angle_scaled(x1, y1, x2, y2,scale)
    length = distance
    angle_degrees =angle-45 #大唐无双的坐标是随时针旋转了45度,所有要减去45度,一般的游戏不需要减去
    angle_radians = math.radians(angle_degrees)
    x = length * math.cos(angle_radians) #x方向的长度
    y = length * math.sin(angle_radians) #y方向的长度
    if x_scene>abs(x) and y_scene>abs(y): #如果x,y移动距离超过50,则不执行
        x_destination=x_role+x #计算后的坐标,x轴的正方向和笛卡尔坐标系相同
        y_destination=y_role-y #计算后的坐标,y轴的正方向和笛卡尔坐标系相反
    elif x_scene<abs(x) or y_scene<abs(y):#说明实时坐标识别错误,则不执行
        return -1,-1

    if debug:
        logger.debug(f"线长度: {distance}")
        logger.debug(f"与x轴的角度: {angle}")
        logger.debug(f"x,y移动距离: ({x:.2f}, {y:.2f})")
        logger.debug(f"屏幕坐标: ({x_destination:.2f}, {y_destination:.2f})")
    return int(x_destination+0.5),int(y_destination+0.5)


def coordinate_merging(list_data):
    """
    将data列表中的每个子列表的第一个元素合并为一个字符串，并去除多余的句点或逗号。
    # 示例代码:
        data = [[('71,', 1307, 206, 0.96), ('206', 1337, 207, 0.975)], [('78.', 1304, 207, 0.865), ('200', 1328, 204, 0.997)],
                [('1,', 1304, 207, 0.965), ('20', 1328, 204, 0.993)]]
        print(coordinate_merging(data))
        # 期望输出: [(71, 206), (78, 200), (1, 20)]
    :param list_data: 包含多个子列表的列表。每个子列表包含多个元组，元组的第一个元素是字符串。
    :return: 一个包含元组的列表，每个元组由两个整数组成。
    """

    def merge_strings(sublist):
        """ 将子列表中的第一个元素合并为字符串 """
        merged_string = ""
        for item in sublist:
            if "." in item[0] or "," in item[0]:  # 包含句点或逗号
                merged_string += item[0]
            else:
                merged_string += item[0] + "."
        # 移除最后一个多余的符号(句点或逗号)
        merged_string = merged_string.rstrip(".,")
        return merged_string

    result = [merge_strings(sublist) for sublist in list_data]

    result_coor = []
    try:
        for item in result:
            item = item.strip()
            separators = [".", ","]
            for sep in separators:
                if sep in item:
                    parts = item.split(sep)
                    break
            result_coor.append((int(parts[0]), int(parts[1])))
    except Exception as e:
        logger.error(f"坐标合并错误: {e}")

    return result_coor


def coordinate_processing(data_list: list):
    """
    处理坐标数据，将每个元素中的第一个元组中的第一个元素拆分为两个整数，并返回新的列表
    示例代码:
        data = [[('75.203', 1306, 203, 0.996)], [('80.198', 1304, 204, 0.961)], [('83.195', 1305, 206, 0.994)],
        [('86.194', 1306, 208, 0.986)], [('89.193', 1305, 206, 0.978)], [('92.190', 1305, 204, 0.922)],
        [('94.188', 1305, 207, 0.995)], [('97.185', 1304, 205, 0.968)], [('98.182', 1305, 207, 0.976)],
        [('99.179', 1305, 207, 0.95)], [('100.175', 1302, 207, 0.994)], [('101.170', 1302, 206, 0.999)],
        [('102.167', 1302, 207, 0.999)], [('103.163', 1302, 207, 0.999)], [('104.160', 1302, 207, 0.946)],
        [('104.156', 1302, 207, 0.952)], [('105.153', 1302, 207, 0.989)], [('106.149', 1302, 207, 0.996)]]
        print(coordinate_processing(data))

    :param data_list:
    :return:
    """
    # 构建新的列表
    new_list = []
    try:
        for item in data_list:
            if "." in item[0]:  # 如果字符串中包含"."，则不加"."
                # 获取元素中的[0]，即 ('75.203', 1306, 203, 0.996)
                first_element = item[0]
                # 提取第一个元素 '75.203'
                value = first_element
                # 拆分并转换为两个整数
                part1, part2 = map(int, value.split('.'))
                # 构成新的元组并追加到新列表中
                new_list.append((part1, part2))
    except Exception as e:
        logger.error(f"坐标处理错误: {e}")
    return new_list

def extract_numbers(data):
    """
    提取数据中的数字部分
    :param data: 一个包含数字和字符串的元组列表
    :return: (110,110)
    """
    # 初始化一个空列表来存储结果
    result = []

    # 迭代数据
    for item in data:
        text = item[0]
        # 使用正则表达式只提取由数字组成的部分
        match = re.match(r'(\d+)', text)
        if match:
            # 将字符串转换为数字并添加到结果列表中
            result.append(int(match.group(1)))

    # 转换为元组
    result_tuple = tuple(result)
    return result_tuple


def real_time_coordinate(coor_data:list,debug:bool=False):
    """
    ocr实时识别出来的坐标处理
    :param coor_data: [[('71', 1307, 206, 0.96), ('206', 1337, 207, 0.975)], [('78.', 1304, 207, 0.865), ('200', 1328, 204, 0.997)]]
    :return: (0,0)识别失败,(110,110)识别成功
    """
    coor_list_a_set = []  # 长度为1的元组组合
    coor_list_two_sets = []  # 长度为2的元组组合
    coor_list_other_sets = []  # 长度大于2的元组组合
    coor_list_a_set_dispose = []  # 长度为1的元组组合处理后的结果
    coor_list_two_sets_dispose = []  # 长度为2的元组组合处理后的结果
    coor_list_other_sets_dispose = []  # 长度大于2的元组组合处理后的结果


    if len(coor_data) == 1:
        coor_list_a_set=coor_data
    elif len(coor_data) == 2:
        coor_list_two_sets.append(coor_data)
    elif len(coor_data) > 2:
        coor_list_other_sets=coor_data
    if coor_list_a_set:
        coor_list_a_set_dispose = coordinate_processing(coor_list_a_set)
    elif coor_list_two_sets:
        coor_list_two_sets_dispose = coordinate_merging(coor_list_two_sets)
    elif coor_list_other_sets:
        coor_list_other_sets_dispose=extract_numbers(coor_list_other_sets)

    if debug:
        logger.debug(f"coor_data: {coor_data}")
        logger.debug(f"coor_list_a_set: {coor_list_a_set}")
        logger.debug(f"coor_list_two_sets: {coor_list_two_sets}")
        logger.debug(f"coor_list_other_sets: {coor_list_other_sets}")
        logger.debug(f"coor_list_a_set_dispose: {coor_list_a_set_dispose}")
        logger.debug(f"coor_list_two_sets_dispose: {coor_list_two_sets_dispose}")
        logger.debug(f"coor_list_other_sets_dispose: {coor_list_other_sets_dispose}")

    if coor_list_a_set_dispose:
        return coor_list_a_set_dispose[0]
    elif coor_list_two_sets_dispose:
        return coor_list_two_sets_dispose[0]
    elif coor_list_other_sets_dispose:
        return coor_list_other_sets_dispose
    else:
        return 0, 0


def way_finding_node_standby(real_time_coor: tuple, coordinate_node: list):
    """
    实时坐标与坐标节点匹配,超出误差值的时候使用
    :param real_time_coor: 实时坐标
    :param coordinate_node: 坐标节点
    :return: 结果列表，包含当前节点和下一个节点（如果有）
    """
    res_list = []
    x_real_time, y_real_time = real_time_coor

    if x_real_time is None or y_real_time is None:
        return res_list

    closest_node_index = -1
    min_total_diff = float('inf')

    for i, (x_node, y_node) in enumerate(coordinate_node):
        # 检查是否完全匹配
        if (x_real_time, y_real_time) == (x_node, y_node):
            res_list.append(real_time_coor)

            if i + 1 < len(coordinate_node):
                next_node = coordinate_node[i + 1]
                res_list.append(next_node)
            return res_list

        # 计算差值
        x_diff = abs(x_real_time - x_node)
        y_diff = abs(y_real_time - y_node)
        total_diff = x_diff + y_diff

        # 更新最小差值节点
        if total_diff < min_total_diff:
            min_total_diff = total_diff
            closest_node_index = i

    # 始终添加找到的最接近节点
    if closest_node_index != -1:
        closest_node = coordinate_node[closest_node_index]
        res_list.append(closest_node)

        if closest_node_index + 1 < len(coordinate_node):
            next_node = coordinate_node[closest_node_index + 1]
            res_list.append(next_node)

    return res_list


def way_finding_node(real_time_coor: tuple, coordinate_node: list, difference: int = 6,threshold:int=3):
    """
    实时坐标与坐标节点匹配
    示例代码:
        coor = (107,80)
        coordinate_node_屠狼洞 = [(101, 52), (106, 55), (108, 65), (109, 76), (108, 81), (107, 86), (108, 95),
                                  (108, 100), (108, 106), (107, 112), (111, 118), (107, 128), (109, 134),
                                  (108, 141), (108, 149), (110, 155), (117, 157), (124, 156), (132, 155),
                                  (139, 157), (143, 164), (144, 171), (143, 178), (142, 185),
                                  (134, 188), (124, 190), (118, 190), (112, 192), (108, 201), (108, 209),
                                  (109, 215), (108, 224), (100, 229), (94, 228), (87, 228),
                                  (83, 235), (84, 241), (83, 247), (85, 254), (86, 261), (86, 270), (85, 278),
                                  (85, 286), (86, 287), (84, 296), (85, 301), (78, 301), (69, 302)]

        res = way_finding_node(coor, coordinate_node_屠狼洞)
        print(res)

    :param real_time_coor: 实时坐标
    :param coordinate_node: 坐标节点
    :param difference: 差距,默认为6,太小会有问题
    :param threshold: 距离阈值,默认为3,地形狭小改小改值
    :return: 结果列表，包含当前节点和下一个节点（如果有）
    """
    res_list = []
    x_real_time, y_real_time = real_time_coor
    logger.debug(f"实时坐标 {(x_real_time, y_real_time)}")

    if x_real_time is None or y_real_time is None:
        return res_list

    closest_node_index = -1
    min_total_diff = float('inf')

    for i, (x_node, y_node) in enumerate(coordinate_node):
        # 检查是否完全匹配
        if (x_real_time, y_real_time) == (x_node, y_node):
            logger.debug(f"实时坐标正好对应坐标节点 {(x_node, y_node)}")
            res_list.append(real_time_coor)

            if i + 1 < len(coordinate_node):
                next_node = coordinate_node[i + 1]
                logger.debug(f"下一个节点坐标是 {next_node}")
                res_list.append(next_node)
            else:
                logger.debug("已经到达最后一个节点，并且完成目标")
            return res_list

        # 计算差值
        x_diff = abs(x_real_time - x_node)
        y_diff = abs(y_real_time - y_node)
        total_diff = x_diff + y_diff

        # 更新最小差值节点
        if total_diff < min_total_diff:
            min_total_diff = total_diff
            closest_node_index = i

    # 检查找到的最接近节点是否在允许的差值范围内
    if closest_node_index != -1 and min_total_diff <= 2 * difference:
        closest_node = coordinate_node[closest_node_index]
        logger.debug(f"距离最近的节点是 {closest_node}")
        res_list.append((x_real_time, y_real_time))

        if closest_node_index + 1 < len(coordinate_node):
            next_node = coordinate_node[closest_node_index + 1]
            logger.debug(f"下一个节点坐标是 {next_node}")
            res_list.append(next_node)

    # 如果遍历完所有节点都没有匹配成功，并且没有找到足够接近的节点
    if not res_list and coordinate_node:
        last_node = coordinate_node[-1]
        x_diff = abs(x_real_time - last_node[0])
        y_diff = abs(y_real_time - last_node[1])

        logger.debug("已经到达最后一个节点，检查是否完成目标")
        if x_diff <= difference and y_diff <= difference:
            logger.debug("已经到达最后一个节点，并且完成目标")
        else:
            logger.debug("已经到达最后一个节点，但还没有完成目标，目标差距仍然大于允许范围")

        res_list.append(real_time_coor)

    if len(res_list) == 1 and res_list[0] == real_time_coor and real_time_coor != coordinate_node[-1]:
        logger.debug("没有找到合适的节点")
        result_list = way_finding_node_standby(real_time_coor, coordinate_node)  # 最近的2个节点
        res_list.append(result_list[0])

    if len(res_list) == 2:
        res_list_dispose = insert_intermediate_points_on_line(res_list,threshold)  # 避免离节点的距离过大，添加中点
        res_list = res_list_dispose[:2]  # 只取前两个节点

    logger.debug(f"结果列表 {res_list}")
    return res_list
