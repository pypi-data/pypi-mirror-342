def group_by_difference(res_list, threshold=20):
    """
    示例代码:
        res_list = [(992, 158), (976, 162), (770, 256), (755, 257),
                    (770, 259), (771, 259), (755, 260), (763, 260),
                    (755, 261), (755, 263), (534, 588), (532, 590),
                    (518, 592), (534, 592), (534, 593), (526, 594),
                    (525, 595), (534, 596)]
        grouped_result = group_by_difference(res_list)
        for idx, group in enumerate(grouped_result):
            print(f"Group {idx + 1}: {group}")
        结果:
        Group 1: [(518, 592), (532, 590), (534, 588), (534, 592), (534, 593), (534, 596), (525, 595), (526, 594)]
        Group 2: [(755, 257), (755, 260), (755, 261), (755, 263), (763, 260), (770, 256), (770, 259), (771, 259)]
        Group 3: [(976, 162), (992, 158)]

    坐标对按 ((x, y)[0]) 的差值小于指定值进行归类
    :param res_list: [(x, y), (x, y), ...]
    :param threshold: 差值阈值
    :return: [[(x, y), (x, y), ...], [(x, y), (x, y), ...], ...]
    """
    # Step 1: Sort the list based on the first element of each tuple
    sorted_list = sorted(res_list, key=lambda x: x[0])
    # Step 2: Group elements based on the difference in the first element
    groups = []
    current_group = []
    for item in sorted_list:
        if not current_group:
            current_group.append(item)
        else:
            if item[0] - current_group[-1][0] < threshold:
                current_group.append(item)
            else:
                groups.append(current_group)
                current_group = [item]

    # Append the last group if it exists
    if current_group:
        groups.append(current_group)
    return groups

def group_by_difference_first_elements(res_list, threshold=20):
    """
    分组,根据第一个元素进行分组,如果相邻两个元素的差值小于阈值,则认为它们属于同一组,结果只取第一个元素
    示例代码:
    res_list = [(992, 158), (976, 162), (770, 256), (755, 257),
            (770, 259), (771, 259), (755, 260), (763, 260),
            (755, 261), (755, 263), (534, 588), (532, 590),
            (518, 592), (534, 592), (534, 593), (526, 594),
            (525, 595), (534, 596)]
    grouped_first_elements = group_by_difference_first_elements(res_list)
    print("First element of each group:", grouped_first_elements)
    :param res_list: 列表
    :param threshold: 阀值
    :return: [(518, 592), (755, 257), (976, 162)]
    """
    # Step 1: Sort the list based on the first element of each tuple
    sorted_list = sorted(res_list, key=lambda x: x[0])
    # Step 2: Group elements based on the difference in the first element
    groups = []
    current_group = []
    for item in sorted_list:
        if not current_group:
            current_group.append(item)
        else:
            if item[0] - current_group[-1][0] < threshold:
                current_group.append(item)
            else:
                groups.append(current_group)
                current_group = [item]

    # Append the last group if it exists
    if current_group:
        groups.append(current_group)
    # Extract the first element of each group
    first_elements = [group[0] for group in groups]
    return first_elements

def check_proximity(position_list:list, position_tuple:tuple, threshold=20):
    """
    实例说明:
        target_position_map = [(1322, 136), (1331, 141), (1353, 157)]
        role_position_map = (1336, 149)
        result = check_proximity(target_position_map, role_position_map)
        print(result)  # Outputs: True or False
    遍历position_list，如果position_list中的坐标与position_tuple的坐标差值小于20，则返回True，否则返回False
    :param position_list: 坐标列表
    :param position_tuple: 比较的坐标元组
    :param threshold:  阈值
    :return: True or False
    """
    for target in position_list:
        if abs(target[0] - position_tuple[0]) < threshold and abs(target[1] - position_tuple[1]) < threshold:
            return True
    return False