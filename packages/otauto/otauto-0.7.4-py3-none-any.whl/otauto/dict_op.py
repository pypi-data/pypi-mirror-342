import re
"""
find_ppocr 使用
"""


def merge_similar_lines(input_dict, x3, y3):
    """
    合并字典中值的 y 坐标差值小于 5 的条目，并将 x3 和 y3 加入到每个合并值的坐标中。

    # 示例用法
    dic = {
        '【主线】贱客？剑客？': [[10, 13, 146, 26, 0.953]],
        '寻物：名录（0/1）': [[26, 28, 139, 44, 0.978]],
        '交付人：苏三': [[26, 45, 117, 59, 0.998]],
        '【阵营】【后勤】捕获毒蜂': [[11, 61, 183, 75, 0.987]],
        '寻物：': [[27, 78, 73, 91, 0.993]],
        '捕获的毒蜂（0/5）': [[69, 75, 183, 94, 0.947]],
        '【新手任务】玲珑的故事': [[10, 94, 167, 107, 0.994]],
        '完成：玲珑副本（未完成）': [[27, 110, 189, 123, 0.994]],
        '【新手任务】试炼场的试炼': [[10, 125, 182, 138, 0.996]],
        '完成：试炼场（未完成）': [[27, 142, 173, 155, 0.983]],
        '【新手任务】装备强化之旅': [[10, 158, 183, 170, 0.997]],
        '完成：装备强化（未完成）': [[27, 174, 189, 187, 0.987]],
        '【新手任务】金装的诱惑1': [[8, 187, 176, 204, 0.973]],
        '找人：名匠（未完成）': [[25, 203, 159, 221, 0.989]],
        '领取': [[110, 223, 139, 237, 0.999]],
        '247,': [[13, 9, 43, 24, 0.976]],
        '58': [[52, 9, 71, 24, 0.998]],
        '280': [[14, 9, 41, 24, 0.999]],
        '59': [[54, 10, 70, 23, 0.998]],
        '247,60': [[14, 9, 41, 24, 0.999]],}
    # 调用合并方法，假设 x3 = 5, y3 = 3
    merged_result = merge_similar_lines(dic, x3=100, y3=100)

    参数:
    input_dict (dict): 输入的字典，键为字符串，值为包含坐标和置信度的列表。
    x3 (int): 需要加到每个值的 x 坐标的值。
    y3 (int): 需要加到每个值的 y 坐标的值。

    返回:
    dict: 合并后的字典。
    """
    merged_dict = {}

    # 用于跟踪当前行的 y 坐标
    current_y = None
    current_keys = []
    current_values = []

    for key, value in input_dict.items():
        y_coord = value[0][1]  # 获取当前值的 y 坐标

        if current_y is None or abs(y_coord - current_y) >= 5:
            # 如果是新的行，保存之前的合并结果
            if current_keys:
                # 在合并时，将 x3 和 y3 加入到每个值的坐标中
                for v in current_values:
                    v[0] += x3  # x1
                    v[1] += y3  # y1
                    v[2] += x3  # x2
                    v[3] += y3  # y2
                merged_dict[''.join(current_keys)] = current_values  # 直接连接键
            # 重置当前行的键和值
            current_y = y_coord
            current_keys = [key]
            current_values = value
        else:
            # 如果在同一行，合并键和值
            current_keys.append(key)
            current_values.extend(value)

    # 保存最后一组合并的结果
    if current_keys:
        # 在合并时，将 x3 和 y3 加入到每个值的坐标中
        for v in current_values:
            v[0] += x3  # x1
            v[1] += y3  # y1
            v[2] += x3  # x2
            v[3] += y3  # y2
        merged_dict[''.join(current_keys)] = current_values  # 直接连接键

    return merged_dict

def extract_keys_to_tuple(input_dict):
    """
    # 示例用法
    dict1 = {'133,': [[45, 135, 77, 149, 0.961]], '，200': [[69, 135, 114, 149, 0.938]]}
    dict2 = {'136,': [[42, 135, 76, 149, 0.951]], '201': [[84, 134, 110, 149, 0.998]]}
    dict3 = {'121,208': [[44, 132, 112, 150, 0.947]]}

    # 调用方法并打印结果
    result1 = extract_keys_to_tuple(dict1)
    result2 = extract_keys_to_tuple(dict2)
    result3 = extract_keys_to_tuple(dict3)

    print(result1)  # 输出: (133, 200)
    print(result2)  # 输出: (136, 201)
    print(result3)  # 输出: (121, 208)

    从字典中提取键并返回一个元组，处理不同格式的键，仅保留数字。
    参数:
    input_dict (dict): 输入的字典，键为字符串，值为包含坐标和置信度的列表。

    返回:
    tuple: 提取的键组成的元组，仅包含数字。
    """
    # 提取键并去掉多余的字符（如逗号）
    keys = [key.strip() for key in input_dict.keys()]

    # 使用正则表达式提取数字部分
    cleaned_keys = []
    for key in keys:
        # 查找所有数字并连接成一个字符串
        numbers = re.findall(r'\d+', key)
        cleaned_keys.extend(numbers)

    # 将提取的数字转换为整数并返回元组
    return tuple(int(num) for num in cleaned_keys)

