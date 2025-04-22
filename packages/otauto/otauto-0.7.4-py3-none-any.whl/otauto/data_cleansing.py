import re
import numpy as np
from scipy.ndimage import label
from otauto.log import ColoredLogger
from otauto.text_correctionv1 import correct_term
from resource.parameters_info.basic_parameter_info import target_name_ls
logger = ColoredLogger()
# 移除日志
logger.remove()
"""
日期:2025-2-1 08:37:29
信息:数据清洗
"""


class DataCleansing:
    def __init__(self, parameter_data: dict=None,debug:bool = False):
        """
        :param parameter_data: 参数数据
        :param debug: 是否开启调试信息
        """
        self.parameter_data = parameter_data  # 参数数据
        self.queue_handle=None
        self.original_data = {}  # 原始数据
        self.numpy_data = np.empty((0, 0, 0))  # 原始数据_数组
        self.debug = debug  # 是否开启调试信息

        self.parameter_data_word = {} # 参数数据_文字
        self.parameter_data_image = {} # 参数数据_图片
        self.parameter_data_color = {} # 参数数据_颜色
        self.parameter_data_yolo = {} # 参数数据_目标检测
        self.parameter_data_mutil_colors = {} # 参数数据_多颜色
        self.parameter_data_unique = {} # 参数数据_特有的

        self.update_parameter = {} # 更新参数数据,线程队列中获取

        self.original_data_word = {} # 原始数据_文字
        self.original_data_image = {} # 原始数据_图片
        self.original_data_color = {} # 原始数据_颜色
        self.original_data_yolo = {} # 原始数据_目标检测
        self.original_data_mutil_colors = {} # 原始数据_多颜色

        self.processed_data_word_acquire = {} # 处理后的数据_文字,获取该局域的文字
        self.processed_data_word_handle = {} # 处理后的数据_文字,文字对比
        self.processed_data_image = {} # 处理后的数据_图片
        self.processed_data_color_acquire = {} # 处理后的数据_颜色,获取该点的颜色
        self.processed_data_color_handle = {} # 处理后的数据_颜色,颜色对比
        self.processed_data_yolo = {} # 处理后的数据_目标检测
        self.processed_data_mutil_colors = {} # 处理后的数据_多颜色
        self.processed_data_unique = { "word":{},
                                       "image":{},
                                       "mutil_colors":{},

        } # 处理后的数据_特有的

        self.error_info_dict={} #错误信息

        self.role_position_map=(1336,149) #角色位置,小地图
        self.role_position_scene=(720,450) #角色位置,游戏场景

        self.role_info_dict={"name":"none", #角色名称
                             "HP":"-1", #角色的HP
                             "MP":"-1", #角色的MP
                             "RP":"-1", #角色的RP
                             "level":"-1", #角色的等级
                             "scoring":"-1", #角色的评分
                             "role_factions":"none", # 角色阵营
                             "running":False, #是否自动寻路中
                             "swap_gear":False, #是否更换装备中
                             "combating":False, #是否战斗中
                             "loading":False, #是否加载中
                             "healing_resurgence":False, #是否复活中
                             }
        self.target_info_dict={"name":"none", #目标名称"
                               "lock":False, #是否锁定
                               "attack_range":False ,#是否攻击范围内
                               "driftlessness":False, #是否无目标
                             }
        self.coordinate_info_dict = {"map_name":"none",#地图名称
                                     "map_position":"-1,-1" #地图坐标
                                     }  # 坐标信息
        self.task_info_dict = {}  # 任务信息
        self.gear_info_dict = {} # 装备信息
        self.pet_info_dict = {}  # 宠物信息
        self.summons_info_dict = {} # 召唤兽信息
        self.interface_info_dict = {"主界面": (-1, -1)}  # 界面信息

    def get_color_pixel_coordinates(self,image, hex_color, tolerance):
        """
        判断小地图上的白色点
        : numpy数组
        :颜色值 "ffffff"
        :颜色容差 20

        """
        # 将十六进制颜色转换为 RGB
        hex_color = hex_color.lstrip('#')  # 去掉 #
        target_color = np.array([int(hex_color[i:i + 2], 16) for i in (0, 2, 4)])  # 转换为 RGB

        # 计算颜色范围
        lower_bound = np.clip(target_color - tolerance, 0, 255)
        upper_bound = np.clip(target_color + tolerance, 0, 255)

        # 创建颜色范围掩码
        mask = ((image >= lower_bound) & (image <= upper_bound)).all(axis=-1).astype(np.uint8) * 255

        # 使用 SciPy 的 label 函数来找到连通区域
        structure = np.ones((3, 3), dtype=int)  # 定义邻接结构
        labeled_array, num_features = label(mask, structure)

        # 准备存储符合条件的色块坐标
        blocks = {}

        for label_id in range(1, num_features + 1):  # 从1开始，0是背景
            # 获取当前色块的坐标
            coordinates = np.column_stack(np.where(labeled_array == label_id))
            if len(coordinates)>=3:  # 只保留点数大于3的色块
                blocks[label_id] = coordinates

        # logger.success(f"{blocks}")
        # 判断条件
        if blocks and len(blocks) == 4 and all(len(value) == 4 for value in blocks.values()):
            return True

        return False

    def process_decimal_strings(self,input_strings):
        """
        # 示例
        input_strings = ['189.81', 'a189.81', 'c123,45', 'abc123.456xyz', '123.45', '456,78']
        output_strings = process_decimal_strings(input_strings)
        """
        def replace_decimal_separator(input_string):
            # 使用正则表达式匹配只有数字和小数点或逗号的字符串
            pattern = r'^\d+([.,]\d+)?$'

            # 检查输入字符串是否符合条件
            if re.match(pattern, input_string):
                # 替换小数点为逗号
                return input_string.replace('.', ',').replace(',', ',')
            return None  # 返回 None 表示剔除该字符串

        # 处理每个输入字符串并过滤掉 None 值
        output_strings = [replace_decimal_separator(s) for s in input_strings]
        output_strings = [s for s in output_strings if s is not None]

        return output_strings

    def get_first_points_of_continuous_segments(self,points):
        """
        获取连续段中每个连续段的第一个点
        :param points: 点的列表，每个点是一个元组 (x, y)
        :return: 连续段中每个连续段的第一个点的列表
        """
        # 首先对点进行排序
        points.sort()
        continuous_segments = []
        current_segment = []
        for i in range(len(points)):
            if not current_segment:
                current_segment.append(points[i])
            else:
                # 检查当前点是否与当前序列的最后一个点连续
                last_point = current_segment[-1]
                if (points[i][0] == last_point[0] and points[i][1] == last_point[1] + 1) or \
                        (points[i][1] == last_point[1] and points[i][0] == last_point[0] + 1):
                    current_segment.append(points[i])
                else:
                    # 如果不连续,记录当前序列的第一个点
                    if len(current_segment) > 1:  # 只有当有连续点时才记录第一个点
                        continuous_segments.append(current_segment[0])
                    else:  # 如果是独立点,直接添加
                        continuous_segments.append(current_segment[0])
                    current_segment = [points[i]]
        # 处理最后一个连续段
        if current_segment:
            if len(current_segment) > 1:
                continuous_segments.append(current_segment[0])
            else:
                continuous_segments.append(current_segment[0])
        return continuous_segments

    def transform_dic(self,dic):
        """
        将字典中的值从字符串转换为列表，并返回一个新的字典
        dic = {
        '背包': (865, 284, 1.0, '背|包'),
        '': (925, 365, 0.0, '背包'),
        '_4': (904, 396, 0.0, '背包'),
        '清': (694, 473, 0.045, '复活点'),
        }
        # 调用转换方法
        new_dic = transform_dic(dic)
        # 打印结果:{'背|包': (865, 284, 1.0)}
        print(new_dic)
        """
        new_dic = {}
        for key, value in dic.items():
            # 检查键和值的最后一个元素是否都是字符串
            if isinstance(key, str) and isinstance(value[-1], str):
                # 分割值[-1]的字符串
                split_values = value[-1].split('|')
                # 检查分割出来的每个部分是否在键中
                if any(part in key for part in split_values):
                    # 如果条件满足, 将其添加到新的字典中
                    new_dic[value[-1]] = (value[0], value[1], value[2])
        return new_dic

    def group_by_difference(self,res_list, threshold=20):
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

    def merge_and_sort_dic(self,dic):
        """
        合并值[1],值[-1]相同的键值对
        dic = {
            '【主线】两件信物': (1187, 260, 0.976, 4),'找人:秦富(未完成)': (1203, 274, 0.966, 4),
            '找人:程咬银': (1204, 291, 0.998, 4),'(未完成)': (1297, 290, 0.96, 4),
            '交付人:小七': (1204, 308, 0.999, 4),'【新手任务】试炼场的试炼': (1187, 323, 0.996, 4),
            '完成:试炼场(未完成)': (1204, 339, 0.991, 4),'风华剧情】绝代风华·云梦泽': (1192, 356, 0.985, 4),
            '前往:云梦泽(完成该系列任': (1201, 369, 0.998, 4),'务,可开启风华驿站)(未完成)': (1181, 388, 0.994, 4),
            '活动': (1276, 501, 1.0, 4),'系统': (1345, 501, 1.0, 4),'剑试关下': (1192, 524, 0.825, 4),
            '提醒': (1278, 518, 0.999, 4),'消息': (1344, 518, 1.0, 4),'一': (1415, 263, 0.732, 4)
        }
        merged_dic = merge_and_sort_dic(dic)
        print(merged_dic)
        """
        similar_pairs = []
        items = list(dic.items())
        # 遍历所有的键值对,寻找相似的键值对
        for i in range(len(items)):
            current_key, current_value = items[i]
            for j in range(i + 1, len(items)):
                next_key, next_value = items[j]
                # 检查条件: 第二个值的误差小于5, 且最后一个值相同
                if abs(next_value[1] - current_value[1]) < 5 and next_value[-1] == current_value[-1]:
                    similar_pairs.append((current_key, next_key))
        merged_dic = {}
        merged_keys = set()  # 用于跟踪已经合并的键
        # 合并相似的键
        for key1, key2 in similar_pairs:
            if key1 in merged_keys or key2 in merged_keys:
                continue  # 如果其中一个键已经被合并,则跳过
            # 获取两个键的值
            value1 = dic[key1]
            value2 = dic[key2]
            # 取两个值的最小值
            merged_value = tuple(min(v1, v2) for v1, v2 in zip(value1, value2))
            # 生成合并后的键
            merged_key = f"{key1}{key2}"
            # 添加到新的字典中
            merged_dic[merged_key] = merged_value
            # 标记这两个键为已合并
            merged_keys.update([key1, key2])
        # 将未合并的键添加到新的字典中
        unmerged_items = {key: value for key, value in dic.items() if key not in merged_keys}
        merged_dic.update(unmerged_items)
        # 按照第一个元素从小到大排序
        merged_dic = dict(sorted(merged_dic.items(), key=lambda item: item[1][0]))
        return merged_dic

    def group_by_difference_first_elements(self,res_list, threshold=5):
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

    def check_proximity(self,position_list: list, position_tuple: tuple, threshold=20):
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
            if abs(target[0] - position_tuple[0]) <=threshold and abs(target[1] - position_tuple[1]) <= threshold:
                return True
        return False

    def is_correct_and_compare(self,s):
        """
        判断字符串是否为两个数字通过斜杠 / 分隔的形式，并比较两个数字的值。
        两边必须是数字。
        # 测试
            test_string1 = '1317/1317'
            result1 = is_correct_and_compare(test_string1)
            print(f"'{test_string1}' 格式正确且符合比较条件: {result1}")

            test_string2 = '1317/2634'
            result2 = is_correct_and_compare(test_string2)
            print(f"'{test_string2}' 格式正确且符合比较条件: {result2}")

            test_string3 = 'abc/123'
            result3 = is_correct_and_compare(test_string3)
            print(f"'{test_string3}' 格式正确且符合比较条件: {result3}")

            test_string4 = '123/'
            result4 = is_correct_and_compare(test_string4)
            print(f"'{test_string4}' 格式正确且符合比较条件: {result4}")
        :param s: 需要判断的字符串
        :return: 如果格式正确且符合条件返回 True，格式不正确或条件不满足返回 False
        """
        # 定义正则模式：确保斜杠两边都是数字
        pattern = r'^\d+/\d+$'

        # 检查格式是否正确
        if not re.match(pattern, s):
            return False

        # 分割字符串
        parts = s.split('/')

        # 转换为整数
        num1 = int(parts[0])
        num2 = int(parts[1])

        # 比较数值
        return num1 < num2 / 2

    def is_point_in_rectangle(self,point, rect):
        """
        判断点是否在矩形内
        :param point:   (x, y) 坐标
        :param rect:     (x_min, y_min, x_max, y_max) 矩形坐标
        :return:   True or False
        """
        x, y = point
        x_min, y_min, x_max, y_max = rect
        return x_min <= x <= x_max and y_min <= y <= y_max

    def is_in_eliminate_scope(self, midpoint: tuple, eliminate_scope: list) -> bool:
        """
        判断给定点是否在消除的矩形范围内
        :param midpoint: 中心点坐标 (x, y)
        :param eliminate_scope: 需要消除的矩形范围列表
        :return: 如果在消除范围内，返回True，否则返回False
        """
        return any(self.is_point_in_rectangle(midpoint, rect) for rect in eliminate_scope)


    def contains_all_elements(self,list1, list2,list_num):
        """判断list1是否是list2的子集"""
        if len(list1)>=list_num:
            set1 = set(list1)
            set2 = set(list2)
            return set2.issubset(set1)

    def get_merge_dicts(self,dict_a, dict_b):
        """合并两个字典，如果有相同的键，则以 dict_a 的值为准"""
        merged_dict = {}
        # 先处理 dict_a
        for key in dict_a:
            if key not in merged_dict:
                merged_dict[key] = {}
            merged_dict[key].update(dict_a[key])
        # 再处理 dict_b
        for key in dict_b:
            if key not in merged_dict:
                merged_dict[key] = {}
            # 更新 dict_b 的键，如果存在相同的键，则以 dict_a 的值为准
            for subkey, value in dict_b[key].items():
                if subkey not in merged_dict[key]:  # 只有当子键不存在时才添加
                    merged_dict[key][subkey] = value
        return merged_dict

    def role_info(self): #todo:有些没有写入
        """
        注意,字典的1为角色信息
        self.role_info_dict={"name":"角色名称", #角色名称
                     "HP":"0", #角色的HP
                     "MP":"0", #角色的MP
                     "RP":"0", #角色的RP
                     "running":False, #是否自动寻路中
                     "swap_gear":False, #是否更换装备中
                     "combating":False, #是否战斗中
                     "loading":False, #是否加载中
                     "healing_resurgence":False, #是否复活中
                     }
        """

        self.role_info_dict["running"]=False #是否自动寻路中
        self.role_info_dict["swap_gear"]=False   #是否更换装备中
        self.role_info_dict["combating"]=False  #是否战斗中
        self.role_info_dict["loading"]=False    #是否加载中
        self.role_info_dict["healing_resurgence"]=False #是否复活中

        logger.info(f"{self.processed_data_word_acquire}")
        #{'多情温暖': (118, 39, 0.998, 1), '多情温暖_1': (118, 39, 0.998, 8), '6711/6711': (121, 68, 0.999, 1), '6711/6711_2': (121, 68, 0.999, 8), '1453/1453': (133, 76, 0.997, 1), '1453/1453_3': (133, 76, 0.997, 8), '0/100': (133, 94, 0.98, 1), '219,43': (1300, 204, 0.92, 3), '游魂堡': (1300, 42, 0.993, 7)}
        # 使用字典推导式提取最后一个元素为1的键值对,角色名称,hp,mp,rp
        role_attribute_data = {key: value for key, value in self.processed_data_word_acquire.items() if value[-1] == 1}
        # 使用字典推导式提取最后一个元素为5的键值对,是否自动寻路中
        running_data= {key: value for key, value in self.processed_data_word_acquire.items() if value[-1] == 5}
        # 使用字典推导式提取最后一个元素为6的键值对,是否更换装备
        replace_data = {key: value for key, value in self.processed_data_word_acquire.items() if value[-1] == 6}
        # 使用字典推导式提取最后一个元素为8的键值对,是否加载中
        loading_data = {key: value for key, value in self.processed_data_word_acquire.items() if value[-1] == 8}
        # 使用字典推导式提取最后一个元素为9的键值对,角色等级
        role_level = {key: value for key, value in self.processed_data_word_acquire.items() if value[-1] == 9}
        # 使用字典推导式提取最后一个元素为10的键值对,角色评分
        role_scoring = {key: value for key, value in self.processed_data_word_acquire.items() if value[-1] == 10}

        pattern = r'^\d+/\d+$' # 正则表达式用于验证格式,用于验证hp,mp,rp的格式

        for key, value in role_attribute_data.items(): # 角色属性处理
            if 30 < value[1] < 45:
                self.role_info_dict["name"]=key
            if 55 < value[1] < 75 and re.match(pattern, key) :
                self.role_info_dict["HP"] = key
            if 75 < value[1] < 88 and re.match(pattern, key) :
                self.role_info_dict["MP"] = key
            if 88 < value[1] < 105 and re.match(pattern, key) :
                self.role_info_dict["RP"] = key

        for key, value in running_data.items(): # 自动寻路状态
            if "自动" in key or "寻路" in key:
                self.role_info_dict["running"]=True
                break

        for key, value in replace_data.items(): # 是否更换装备
            if  "马上" in key or "使用" in key or "装备" in key:
                self.role_info_dict["swap_gear"]=True
                break

        for key, value in loading_data.items(): # 是否加载中
            if "易" in key or "NETEASE" in key or "www.163" in key:
                self.role_info_dict["loading"]=True
                break

        for key, value in role_level.items(): # 角色等级
            # 使用正则表达式判断是否是数字
            pattern = r'^\d+$'  # 正则表达式: 只匹配正整数
            is_number = bool(re.match(pattern, key))
            if is_number:
                self.role_info_dict["level"] = key

        for key, value in role_scoring.items(): # 角色评分
            # 使用正则表达式判断是否是数字
            pattern = r'^\d+$'  # 正则表达式: 只匹配正整数
            is_number = bool(re.match(pattern, key))
            if is_number:
                self.role_info_dict["scoring"] = key

        if not self.role_info_dict["running"] and  self.numpy_data.size: # 判断是否自动寻路中,根据小地图
            x1, y1, x2, y2 = 1312, 119, 1365, 175
            cropped_image = self.numpy_data[y1:y2, x1:x2]
            hex_color = "ffffff"  # 目标颜色 (白色)
            tolerance = 5  # 容差
            if self.get_color_pixel_coordinates(cropped_image, hex_color, tolerance):
                logger.info(f"自动寻路中,出现小地图白点")
                self.role_info_dict["running"] = True

        # logger.success(f"role_info_dict:{self.role_info_dict}")

    def target_info(self):
        """
        注意,字典的2为目标信息
        self.target_info_dict={"name":"目标名称", #目标名称"
                       "lock":False, #是否锁定
                       "attack_range":False ,#是否攻击范围内
                       "driftlessness":False, #是否无目标
                     }
        """

        self.target_info_dict={"name":"none", #目标名称
                               "lock":False, #是否锁定
                               "attack_range":False ,#是否攻击范围内
                               "driftlessness":False, #是否无目标
                             }

        # 使用字典推导式提取最后一个元素为2的键值对,是否识别出有目标名称
        target_data= {key: value for key, value in self.processed_data_word_acquire.items() if value[-1] == 2}
        yolo_label=self.original_data_yolo
        mutil_colors_data=self.original_data_mutil_colors

        if yolo_label :
            #[['红色名称', 658, 68, 0.916], ['雇佣剑客', 556, 380, 0.889], ['红名怪', 817, 216, 0.844]]
            for label in yolo_label:
                if label[0] in target_name_ls:
                    self.target_info_dict["lock"]=True # 目标已锁定
                if "红名怪" in label[0]:
                    self.target_info_dict["attack_range"]=True

        if target_data :
            for key, value in target_data.items():
                target_name=correct_term(key, target_name_ls) #纠错
                self.target_info_dict["name"]=target_name
                if target_name in target_name_ls:
                    self.target_info_dict["lock"]=True # 目标已锁定

        if mutil_colors_data:
            for key ,value in mutil_colors_data.items():
                if "目标体_地图红点" in key:
                    target_position_map = self.group_by_difference_first_elements(value, threshold=5)
                    #(1336,149)
                    if self.check_proximity(target_position_map, self.role_position_map, threshold=15):
                        logger.info("目标体在小地图出现,且在角色附近")
                        self.target_info_dict["attack_range"]=True

        if not yolo_label and not mutil_colors_data:
            self.target_info_dict["driftlessness"]=True

        # logger.info(f"target_data:{target_data}")
        # logger.info(f"yolo_label:{yolo_label}")
        # logger.info(f"mutil_colors_data:{mutil_colors_data}")
        # logger.success(f"target_info_dict:{self.target_info_dict}")

    def map_info(self):
        """
        注意,字典的3为坐标点,7为地图名称
        self.coordinate_info_dict = {"map_name":"地图名称",#地图名称
                             "map_position":"地图坐标" #地图坐标
                             }  # 坐标信息
        """
        self.coordinate_info_dict = {"map_name":"none",#地图名称
                                     "map_position":"-1,-1" #地图坐标
                                     }  # 坐标信息

        # 使用字典推导式提取最后一个元素为3的键值对,地图坐标
        map_position_data= {key: value for key, value in self.processed_data_word_acquire.items() if value[-1] == 3}
        # 使用字典推导式提取最后一个元素为6的键值对,地图名称
        map_name_data = {key: value for key, value in self.processed_data_word_acquire.items() if value[-1] == 7}

        if map_position_data:
            if len(map_position_data)==2:
                # 使用正则表达式提取符合条件的键
                pattern = re.compile(r'^\d+\.?$|^\d+,$')  # 匹配纯数字、带小数点或带逗号的数字
                keys = [key for key in map_position_data.keys() if pattern.match(key)]  # 筛选符合条件的键
                # 组合键字符串，只提取数字部分
                keys_string = ','.join(re.sub(r'\D', '', key) for key in keys)  # 提取数字部分并组合
                # 提取最小值
                if keys:  # 确保至少有一个符合条件的键
                    # 提取对应的值元组
                    value_tuples = [map_position_data[key] for key in keys]
                    # 计算每个位置的最小值
                    min_values = tuple(min(values) for values in zip(*value_tuples))
                    # 创建新的字典
                    new_dict = {keys_string: min_values}
                    for key, value in new_dict.items():
                        self.coordinate_info_dict["map_position"]=key

            if  len(map_position_data)==1:
                for key, value in map_position_data.items():
                    output_strings = self.process_decimal_strings([key])
                    if output_strings:
                        key=output_strings[0]
                        self.coordinate_info_dict["map_position"]=key

        if map_name_data:
            for key, value in map_name_data.items():
                self.coordinate_info_dict["map_name"]=key

        # logger.info(f"map_position_data:{map_position_data}")
        #{'277.': (1307, 208, 0.878, 3), '57': (1344, 207, 0.999, 3)}
        # logger.info(f"map_name_data:{map_name_data}")
        # logger.error(f"coordinate_info_dict:{self.coordinate_info_dict}")

    def task_info(self):
        """
        注意,字典的4为任务信息
        {'【主线】两件信物': (1186, 258, 0.975, 4),
        '找人：秦富（未完成）': (1204, 275, 0.983, 4),
        '找人：程咬银（未完成）': (1203, 289, 0.964, 4),
        '交付人：小七': (1203, 307, 0.998, 4),
        '【新手任务】试炼场的试炼': (1186, 323, 0.996, 4),
        '完成：试炼场（未完成）': (1203, 339, 0.988, 4),
        '【风华剧情】绝代风华·云梦泽': (1188, 355, 0.991, 4),
        '前往：云梦泽（完成该系列任': (1203, 372, 0.998, 4),
        '务，可开启风华驿站）（未完成）': (1182, 387, 0.995, 4),
        '活动系统': (1277, 501, 1.0, 4),
        '提醒消息': (1278, 517, 0.999, 4),
        '剑试天下': (1192, 524, 0.85, 4)}
        self.task_info_dict = {}
        """
        self.task_info_dict = {}  # 初始化
        # 使用字典推导式提取最后一个元素为4的键值对,任务
        task_data = {key: value for key, value in self.processed_data_word_acquire.items() if value[-1] == 4}
        merge_task_data=self.merge_and_sort_dic(task_data) #合并同一行的数据
        sorted_items = sorted(merge_task_data.items(), key=lambda item: item[1][1])# 使用 sorted 函数按值的第二个元素排序
        sorted_dic = dict(sorted_items) # 将排序后的结果转换回字典
        self.task_info_dict=sorted_dic
        # logger.info(f"sorted_dic:{sorted_dic}")
        # logger.success(f"task_info_dict:{self.task_info_dict}")

    def interface_info(self):
        """
        待加,坐标为关闭,('界面', 884, 196)
        {'背包': (865, 284, 1.0, '背包'), '': (925, 365, 0.0, '背包'),
        '_4': (904, 396, 0.0, '背包'), '清': (694, 473, 0.045, '复活点'),
        '银元宝': (636, 574, 0.916, '拆解所得'), '绑定元宝': (636, 600, 0.998, '休想'),
        '绑定元宝_5': (636, 600, 0.998, '拆解所得')}
        """
        pass
        # self.interface_info_dict = {"主界面": (-1, -1)}  # 初始化
        # result_dict = {} # 初始化新的字典
        # interface_data=self.processed_data_word_handle # 获取处理后的数据
        # interface_data_image=self.processed_data_image # 获取处理后的图片
        #
        # # 遍历 interface_data 的键
        # for key in interface_data:
        #     if key in self.parameter_data_word:  # 如果 interface_data 的键在 game_interface 中
        #         # 获取对应的界面信息
        #         interface_info = self.parameter_data_word[key]
        #         # 更新结果字典
        #         if "界面" in interface_info['use']:
        #             result_dict[f"{interface_info['use']}"] = (interface_data[key][0],  interface_data[key][1])
        #
        # if result_dict:
        #     # logger.info(f"result_dict:{result_dict}")
        #     self.interface_info_dict = result_dict
        #
        # else:
        #     for key, value in interface_data_image.items():
        #         if key in self.parameter_data_image:
        #             interface_info = self.parameter_data_image[key]
        #             #{'scope': (1066, 121, 1169, 195), 'con': 0.8, 'ues': '大唐风流界面'}
        #             value_str=interface_info.get("ues","未知")
        #             if "界面" in value_str:
        #                 result_dict[f"{value_str}"] = (interface_info['scope'][0],  interface_info['scope'][1])
        #     if result_dict:
        #         logger.error(f"result_dict:{result_dict}")
        #         self.interface_info_dict = result_dict

        # logger.info(f"interface_data:{interface_data}")
        # logger.success(f"interface_info_dict:{self.interface_info_dict}")

    def gear_info(self):
        """
        装备信息
        """
        self.gear_info_dict = {}  # 初始化

        keyword_list=["武器","头盔","衣服","护手","腰带","鞋子","项链","戒指","玉佩","护身符",
                      "1阶","2阶","3阶","4阶","5阶","6阶","7阶","8阶",
                      "+1","+2","+3","+4","+5","+6","+7","+8",]
        # 使用字典推导式提取最后一个元素为11的键值对,装备
        gear_data = {key: value for key, value in self.processed_data_word_acquire.items() if value[-1] == 11}
        """
        '角色信息': (703, 167, 0.999, 11), '装备': (415, 201, 0.995, 11), '荣誉': (469, 201, 0.998, 11), '贡献': (535, 201, 0.939, 11),
        '角色评分': (894, 230, 0.998, 11), '487_13': (988, 232, 0.999, 11), '60]': (610, 233, 0.772, 11), 
        '无双战士[4487': (484, 233, 0.965, 11), '30级': (486, 251, 0.998, 11), '培养指引_15': (967, 260, 0.998, 11), 
        '公': (832, 272, 0.09, 11), 'X战斗属性': (894, 284, 0.872, 11), '攻击力': (888, 313, 0.997, 11), '261': (1015, 313, 0.999, 11),
        '六道浑元棍（+2)': (642, 328, 0.898, 11), '法术攻击': (886, 331, 0.997, 11), '49': (1021, 334, 0.998, 11), 
        '7阶武器': (678, 356, 0.988, 11), '伤害强度': (888, 356, 0.994, 11), '1.261': (999, 356, 0.997, 11), 
        '1': (652, 377, 0.29, 11), '星级★★★': (681, 380, 0.974, 11), '防御值': (888, 378, 0.999, 11), 
        '167': (1017, 380, 0.998, 11), '不可拆解': (682, 399, 0.998, 11), 
        '全抗性': (889, 401, 0.997, 11), '240': (1014, 399, 0.999, 11), 
        '少林派': (681, 418, 0.998, 11), '长兵': (849, 421, 0.999, 11), 'O': (898, 432, 0.338, 11), 
        '基础属性': (919, 435, 0.944, 11), '需求等级：30': (681, 438, 0.999, 11), '': (904, 442, 0.0, 11), 
        '体质': (888, 458, 0.999, 11), '耐久100/100': (681, 460, 0.998, 11), 'R': (433, 426, 0.089, 11), 
        '222': (1017, 460, 1.0, 11), '侨': (435, 475, 0.885, 11), '力量': (888, 481, 0.998, 11), '172': (1015, 481, 0.998, 11),
        '敏捷': (888, 503, 0.997, 11), '已绑定': (550, 488, 0.993, 11), '攻击力221': (549, 506, 0.994, 11),
        '172_24': (1017, 504, 0.998, 11), '智力': (888, 525, 0.999, 11), '31': (1023, 525, 0.999, 11), 
        '敏捷+20': (550, 547, 0.996, 11), '力量+20': (550, 528, 0.994, 11), '精神': (888, 547, 1.0, 11), 
        '31_26': (1023, 549, 0.999, 11), '体质+28': (550, 568, 0.995, 11), '战术属性': (886, 568, 0.993, 11), 
        '强化进度(0/1)：': (550, 589, 0.962, 11), '暴击率': (888, 605, 0.998, 11), '6.2%': (1005, 605, 0.998, 11), 
        '刻刻警醒少林弟子勿忘慈悲六道之': (624, 626, 0.983, 11), '装备评分：22': (549, 606, 0.99, 11), '命中率': (888, 627, 0.999, 11), 
        '95%': (1015, 629, 0.998, 11), '风云录': (828, 649, 0.986, 11), '佛家法器': (549, 632, 0.999, 11), 
        '格挡率': (888, 649, 0.991, 11), '28%': (1014, 649, 0.999, 11), '_31': (583, 652, 0.0, 11),
        '心。': (535, 652, 0.994, 11), '售店价格：': (550, 672, 0.998, 11), '：0': (618, 672, 0.843, 11), 
        '闪避率': (888, 672, 0.998, 11), '0%': (1021, 672, 0.999, 11), '技能闪避率': (888, 694, 0.998, 11),
        '0%_32': (1023, 694, 0.999, 11), '品': (682, 703, 0.316, 11), '1G': (636, 700, 0.236, 11)}
        """
        # 创建一个正则表达式模式，用于匹配 "+1" 到 "+8" 前面可以有其他字符串，后面不能有其他数字
        pattern = re.compile(r'.*\+\d$')  # 匹配以+开头，后面跟着一个数字，且是字符串的结尾
        # 创建一个正则表达式模式，用于排除包含数字后缀的情况
        exclude_pattern = re.compile(r'.*\+\d+\d')
        # 找出键中包含 keyword_list 里的元素的键值对
        self.gear_info_dict = {
            k: v for k, v in gear_data.items()
            if (any(keyword in k for keyword in keyword_list) or pattern.match(k)) and not exclude_pattern.match(k)
        }
        # logger.success(f"self.gear_info_dict:{self.gear_info_dict}")

    def pet_info(self):
        """
        宠物信息
        """
        keyword_list=["铁枪","歪嘴军师","雇佣剑客"]
        # 使用字典推导式提取最后一个元素为4的键值对,任务
        pet_data = {key: value for key, value in self.processed_data_word_acquire.items() if value[-1] == 12}
        """
        {'武将列表': (1020, 553, 0.999, 12), '铁枪_34': (1026, 593, 0.998, 12), '_35': (1126, 595, 0.0, 12), '歪嘴军师': (1009, 617, 0.998, 12), '普': (1129, 620, 0.938, 12)}
        """
        if pet_data:
            for key,value in pet_data.items():
                pet_name=correct_term(key,keyword_list)
                if pet_name:
                    self.pet_info_dict[pet_name]=value

        # logger.success(f"pet_data:{pet_data}")
        # logger.success(f"self.pet_info_dict:{self.pet_info_dict}")

    def summons_info(self):
        """
        召唤物信息
        """
        self.summons_info_dict = {}
        keyword_list=["灵鹊","雪狼"]
        # 使用字典推导式提取最后一个元素为4的键值对,任务
        summons_data = {key: value for key, value in self.processed_data_word_acquire.items() if value[-1] == 13}
        if summons_data:
            for key,value in summons_data.items():
                summons_name=correct_term(key,keyword_list)
                if summons_name:
                    self.summons_info_dict[summons_name]=value

        # logger.success(f"summons_data:{summons_data}")
        # logger.success(f"self.pet_info_dict:{self.summons_info_dict}")

    def unique_info(self):
        """
        模块数据,特定该流程需要用到的所有数据信息
        """
        # 找到包含 'unique': True 的键值对

        self.processed_data_unique = { "word":{},
                                       "image":{},
                                       "mutil_colors":{},
        } #初始化

        for main_key, sub_dict in self.parameter_data.items():
            for sub_key, attributes in sub_dict.items():
                if isinstance(attributes, dict) and attributes.get('unique') is True:
                    if main_key not in self.parameter_data_unique:
                        self.parameter_data_unique[main_key] = {}
                    self.parameter_data_unique[main_key][sub_key] = attributes

        # logger.success(f"self.parameter_data_unique:{self.parameter_data_unique}")
        """
        {'word': {'系统菜单': {'scope': (663, 255, 820, 316), 'con': 0.8, 'offset': (30, 248), 'use': '系统菜单界面', 'unique': True}}, 
        'image': {'resource/images_info/main_task/商城.bmp': {'scope': (1190, 46, 1245, 111), 'con': 0.8, 'unique': True}}}
        
        self.processed_data_word_acquire, # 获取到的文字信息
        self.processed_data_word_handle, # 获取到的文字信息
        self.processed_data_image, # 获取到的图片信息
        self.processed_data_mutil_colors, # 获取到的多颜色信息
        """
        # logger.success(f"{self.processed_data_word_handle}")
        if self.parameter_data_unique:
            for main_key, sub_dict in self.parameter_data_unique.items():
                if main_key == "word":
                    for sub_key, attributes in sub_dict.items():
                        if isinstance(sub_key,str): # 如果键值对中的值是字符串
                            # logger.success(f"{sub_key}")
                            if sub_key in self.processed_data_word_handle:
                                self.processed_data_unique[main_key].update({sub_key: self.processed_data_word_handle[sub_key]})
                        if isinstance(sub_key, int): # 如果键值对中的值是数字
                            if sub_key in self.processed_data_word_acquire:
                                self.processed_data_unique[main_key].update({sub_key: self.processed_data_word_acquire[sub_key]})
                if main_key == "image":
                    for sub_key, attributes in sub_dict.items():
                        if sub_key in self.processed_data_image:
                            self.processed_data_unique[main_key].update({sub_key: self.processed_data_image[sub_key]})
                if main_key == "mutil_colors":
                    for sub_key, attributes in sub_dict.items():
                        if sub_key in self.processed_data_mutil_colors:
                            self.processed_data_unique[main_key].update({sub_key: self.processed_data_mutil_colors[sub_key]})

        # logger.success(f"self.processed_data_unique:{self.processed_data_unique}")


    def error_info(self, difference: int = 5):
        """
        错误信息的判断
        """
        self.error_info_dict = {} # 初始化
        pass

    def information_processing(self):
        """
        信息处理,处理参数数据中其他键值对和元素数据之间的关系
        """
        logger.info(f"信息处理中...")
        # # logger.error(f"参数数据:{self.parameter_data}")
        # logger.error(f"原始数据:{self.original_data}")

        self.processed_data_word_acquire = {} # 初始化,处理后的数据_文字,获取该局域的文字
        self.processed_data_word_handle = {} # 初始化,处理后的数据_文字,文字对比
        self.processed_data_image = {} # 初始化,处理后的数据_图片
        self.processed_data_color_acquire = {} # 初始化,处理后的数据_颜色,获取该点的颜色
        self.processed_data_color_handle = {} # 初始化,处理后的数据_颜色,颜色对比
        self.processed_data_yolo = {} # 初始化,处理后的数据_目标检测
        self.processed_data_mutil_colors = {} # 初始化,处理后的数据_多颜色

        # 这里我们定义一些默认值
        default_word = {}
        default_image = {}
        default_color = {}
        default_yolo = {}
        default_mutil_colors = {}
        processed_data_word_handle={}
        result_word_handle = {}
        numpy_data=None # 默认值,为None

        #线程队列信息处理,避免没必要的信息识别
        if self.queue_handle is not None: #队列为空,返回 True,否则返回 False
            self.update_parameter=self.queue_handle
            logger.success(f"数据清洗收到线程队列信息:{self.update_parameter}")
        if self.update_parameter:
            for key, value in self.update_parameter.items():
                if key in ["image"]:
                    for key_data, value_data in value.items():
                        self.parameter_data_image[key_data].update(value_data)
                if key in ["word"]:
                    for key_data, value_data in value.items():
                        self.parameter_data_word[key_data].update(value_data)
                if key in ["mutil_colors"]:
                    for key_data, value_data in value.items():
                        self.parameter_data_mutil_colors[key_data].update(value_data)
            self.update_parameter={} # 清空更新的参数

        # 确保 self.parameter_data 和 self.original_data 不是 None
        self.parameter_data = self.parameter_data if self.parameter_data is not None else {}
        self.original_data = self.original_data if self.original_data is not None else {}

        # 参数数据导入
        self.parameter_data_word = self.parameter_data.get('word', default_word)
        self.parameter_data_image = self.parameter_data.get('image', default_image)
        self.parameter_data_color = self.parameter_data.get('color', default_color)
        self.parameter_data_yolo = self.parameter_data.get('yolo', default_yolo)
        self.parameter_data_mutil_colors = self.parameter_data.get('mutil_colors', default_mutil_colors)

        # 原始数据导入
        self.original_data_word = self.original_data.get('word', default_word)
        self.original_data_image = self.original_data.get('image', default_image)
        self.original_data_color = self.original_data.get('color', default_color)
        self.original_data_yolo = self.original_data.get('yolo', default_yolo)
        self.original_data_mutil_colors = self.original_data.get('mutil_colors', default_mutil_colors)

        # 文字类数据处理
        for key, value in self.original_data_word.items():
            # 获取最后一个元素
            last_element = value[-1]
            # 根据最后一个元素的类型将数据存储到不同的字典中
            if isinstance(last_element, int):
                self.processed_data_word_acquire[key] = value
            elif isinstance(last_element, str):
                processed_data_word_handle[key] = value

        processed_dict=self.transform_dic(processed_data_word_handle) #是否是目标文字
        # 遍历 interface_data 的键
        for key in processed_dict:
            if key in self.parameter_data_word :  # 如果 interface_data 的键在 game_interface 中
                # 获取对应的界面信息
                interface_info = self.parameter_data_word [key]
                # 获取原始坐标
                original_x, original_y, value = processed_dict[key]
                # 检查是否存在 "offset"
                if "offset" in interface_info:
                    offset = interface_info.get("offset", (0, 0))  # 如果没有 offset，使用默认值 (0, 0)
                    # 计算新的坐标
                    new_x = original_x + offset[0]
                    new_y = original_y + offset[1]
                else:
                    # 如果没有 "offset", 使用原始坐标
                    new_x = original_x
                    new_y = original_y
                # 更新结果字典
                result_word_handle[key] = (new_x, new_y, value)

        self.processed_data_word_handle.update(result_word_handle)  # 更新过滤完成的字典
        # logger.success(f"processed_data_word_handle:{self.processed_data_word_handle}")

        # 颜色类数据处理
        # logger.info(f"颜色原始数据原始数据:{self.original_data_color}")
        # logger.info(f"颜色参数数据:{self.parameter_data_color}")
        """
        {1: (73, 108, 132, 1, 440, 180),
        2: (29, 120, 98, 2, 923, 305),
        3: (6, 11, 12, 3, 565, 462), 
        (163, 53, 46): (46, 53, 163, 'a3352e', 616, 99),
        (222, 65, 48): (48, 65, 222, 'de4130', 697, 100),
        (207, 54, 39): (39, 54, 207, 'cf3627', 763, 101), 
        (255, 136, 0): (66, 80, 87, 'ff8800', 1251, 242)}
        
        {1: (440, 180),
        2: (923, 305),
        3: (565, 462),
        'a3352e': (616, 99), 
        'de4130': (697, 100),
        'cf3627': (763, 101),
        'ff8800': (1251, 242)}
        """
        # 新的结果字典
        new_res = {}
        # 用于存储元组键的 RGB 值
        tuple_rgb_values = {}
        # 遍历原字典
        for key, value in self.original_data_color.items():
            if isinstance(key, int):
                # 处理整数键
                new_res[key] = {
                    "scope": value[-2:],
                    "rgb": value[:3]
                }
            else:
                # 处理元组键
                color_code = value[3]  # 颜色代码
                rgb_value = value[:3]
                # 检查容差
                should_add = True
                for existing_rgb in tuple_rgb_values.values():
                    if all(abs(existing_rgb[i] - rgb_value[i]) < 10 for i in range(3)):
                        continue
                    else:
                        should_add = False
                        break
                if should_add:
                    new_res[color_code] = {
                        "scope": value[-2:],
                        "rgb": rgb_value
                    }
                    tuple_rgb_values[color_code] = rgb_value

        for key, value in new_res.items():
            # 根据最后一个元素的类型将数据存储到不同的字典中
            if isinstance(key, int):
                self.processed_data_color_acquire[key] = value
            elif isinstance(key, str):
                self.processed_data_color_handle[key] = value

        # 图片类数据处理
        # logger.info(f"图片原始数据原始数据:{self.original_data_image}")
        # logger.info(f"图片参数数据:{self.parameter_data_image}")
        """
        {'resource/images_info/main_task/商城.bmp': None, 
        'resource/images_info/main_task/冒险.bmp': None, 
        'resource/images_info/main_task/帮会.bmp': None,
        'resource/images_info/main_task/角色.bmp': None,
        'resource/images_info/main_task/技能.bmp': None, 
        'resource/images_info/camp_task/义军图腾.bmp': None, 
        'resource/images_info/camp_task/唐军图腾.bmp': [(658, 834, 675, 853, 0.826)]
        }
        
        {'resource/images_info/main_task/商城.bmp': {'scope': (1190, 46, 1245, 111), 'con': 0.8}, 
        'resource/images_info/main_task/冒险.bmp': {'scope': (1377, 596, 1437, 660), 'con': 0.8},
        'resource/images_info/main_task/帮会.bmp': {'scope': (1285, 660, 1333, 723), 'con': 0.8},
        'resource/images_info/main_task/角色.bmp': {'scope': (804, 655, 882, 731), 'con': 0.8}, 
        'resource/images_info/main_task/技能.bmp': {'scope': (871, 654, 924, 724), 'con': 0.8},
        'resource/images_info/camp_task/义军图腾.bmp': {'scope': (649, 817, 691, 872, 0.8), 'con': 0.8,"ues":"义军图腾"}, 
        'resource/images_info/camp_task/唐军图腾.bmp': {'scope': (649, 817, 691, 872, 0.8), 'con': 0.8,"ues":"唐军图腾"}
        }
        """
        # 使用字典推导式过滤值不为 None 的键值对
        filtered_data = {k: v for k, v in self.original_data_image.items() if v is not None}
        # 构建最终结果
        final_result = {}
        for key in filtered_data.keys():
            # 如果键在 dict_a 中,提取额外信息
            if key in self.parameter_data_image:
                additional_data = {k: v for k, v in self.parameter_data_image[key].items() if k not in ["con"]}
                # 将 "scope" 转换为列表
                additional_data["scope"] = filtered_data[key]  # 直接使用 filtered_data 中的值
                final_result[key] = additional_data
        self.processed_data_image= final_result  # 更新过滤完成的字典

        #yolo类数据处理
        # logger.info(f"图片原始数据原始数据:{self.original_data_yolo}")
        # logger.info(f"图片参数数据:{self.parameter_data_yolo}")
        """
        [['红色名称', 658, 68, 0.936], 
        ['雇佣剑客', 1371, 524, 0.932], 
        ['红名怪', 460, 39, 0.895],
        ['雇佣剑客', 931, 136, 0.892],
        ['雇佣剑客', 483, 548, 0.888]]
        
        {'木料': {'con': 0.8, 'offset': (0, 0), 'model': 0, 'delay_time': 1.2, 'weight': 10},
        '疑犯': {'con': 0.8, 'offset': (0, 0), 'model': 0, 'delay_time': 1.2, 'weight': 10}, 
        '雇佣剑客': {'con': 0.8, 'offset': (0, 0), 'model': 0, 'delay_time': 1.2, 'weight': 10},
        '红名怪': {'con': 0.8, 'offset': (0, 0), 'model': 0, 'delay_time': 1.2, 'weight': 10},
        '红色名称': {'con': 0.8, 'offset': (0, 0), 'model': 0, 'delay_time': 1.2, 'weight': 10}, 
        '宝箱': {'con': 0.8, 'offset': (0, 0), 'model': 0, 'delay_time': 1.2, 'weight': 10}}
        """
        # 初始化结果字典
        yolo_dict = {}
        # 遍历 res_yolo_list
        for item in self.original_data_yolo:
            name = item[0]
            coordinates = (item[1], item[2], item[3])  # (x, y, confidence)

            # 检查名称是否在 yolo_pro 中
            if name in self.parameter_data_yolo:
                # 如果名称在 res 中则添加坐标到 scope, 否则初始化
                if name not in yolo_dict:
                    yolo_dict[name] = {
                        "scope": [coordinates]
                    }

                    # 添加除 "con" 和 "model" 以外的字段
                    for key in self.parameter_data_yolo[name]:
                        if key not in ["con", "model"]:
                            yolo_dict[name][key] = self.parameter_data_yolo[name][key]
                else:
                    yolo_dict[name]["scope"].append(coordinates)

        # 更新 self.processed_data_yolo
        self.processed_data_yolo=yolo_dict


        # mutil_colors类数据处理
        # logger.info(f"mutil_colors原始数据原始数据:{self.original_data_mutil_colors}")
        # logger.info(f"mutil_colors参数数据:{self.parameter_data_mutil_colors}")
        """
        {'目标体_地图红点': [(1342, 139), (1342, 140), (1342, 141), (1360, 155), (1360, 156), (1360, 157), (1326, 160), (1326, 161), (1326, 162)], 
        '目标体血条': [(664, 93), (665, 93), (666, 93), (667, 93), (668, 93), (669, 93), (670, 93), (671, 93), (672, 93), (673, 93), (674, 93), (675, 93), (676, 93), (677, 93), (678, 93), (679, 93), (680, 93), (681, 93), (682, 93), (683, 93), (684, 93), (685, 93), (686, 93), (687, 93), (688, 93), (689, 93), (690, 93), (691, 93), (692, 93), (693, 93), (694, 93), (695, 93), (696, 93), (697, 93), (698, 93), (699, 93), (700, 93), (701, 93), (702, 93), (703, 93), (704, 93), (705, 93), (706, 93), (707, 93), (708, 93), (709, 93), (710, 93), (711, 93), (725, 93), (726, 93), (727, 93), (728, 93), (729, 93), (730, 93), (731, 93)],
        '目标体等级': [(585, 154), (586, 154), (585, 155), (586, 155)]}
        {'目标体_地图红点': {'colors': {'f3120a': (1601, 17), 'e31109': (1598, 17), 'fe966f': (1604, 16)}, 'scope': (1257, 73, 1414, 207), 'tolerance': 30}, 
        '目标体血条': {'colors': {'9e885c': (690, 93), 'aea89f': (680, 94), 'a9322a': (665, 100), '9b938c': (681, 110)}, 'scope': (584, 87, 808, 120), 'tolerance': 25}, 
        '目标体等级': {'colors': {'9f3029': (585, 155), '9f2c25': (573, 164), 'a13028': (584, 174), '9f2e27': (595, 164)}, 'scope': (567, 148, 601, 179), 'tolerance': 25}}
        """
        # 使用列表推导式构建结果字典
        mutil_colors={}
        # 处理每个键
        for key, points in self.original_data_mutil_colors.items():
            first_points = self.get_first_points_of_continuous_segments(points)
            mutil_colors[key] = {"scope": first_points}

        # 合并数据
        if mutil_colors:
            for key in mutil_colors.keys():
                if key in self.parameter_data_mutil_colors:
                    # 获取 pro_dict 中的所有键值对,排除 'colors', 'scope', 'tolerance'
                    for k, v in self.parameter_data_mutil_colors[key].items():
                        if k not in ['colors', 'scope', 'tolerance']:
                            mutil_colors[key][k] = v

        self.processed_data_mutil_colors=mutil_colors  # 更新过滤完成的字典


    def message_to_log(self, word_dict: dict, items_per_line: int = 3):
        """
        # 记录日志
        logger.success(f"dic_word_ocr:\n{formatted_dict}")
        将字典或列表转换为字符串,并按每行指定数量进行换行
        :param word_dict: 字典或列表
        :param items_per_line: 换行的键值对数目
        :return: 格式化后的字符串
        """
        if word_dict is None:
            return ""

        formatted_items = []

        if isinstance(word_dict, dict):
            # 获取字典的键值对列表
            items = list(word_dict.items())
            # 分割成每行指定数量的键值对
            for i in range(0, len(items), items_per_line):
                formatted_items.append(', '.join([f"{k}: {v}" for k, v in items[i:i + items_per_line]]))

        elif isinstance(word_dict, list):
            # 分割列表并格式化
            for i in range(0, len(word_dict), items_per_line):
                formatted_items.append(', '.join([str(item) for item in word_dict[i:i + items_per_line]]))

        # 将分割后的内容连接成多行字符串
        formatted_dict = '\n'.join(formatted_items)
        return formatted_dict


    def debug_info(self):
        logger.success("+=====================参数数据=====================================+")
        logger.success(f"self.parameter_data_word:{self.message_to_log(self.parameter_data_word)}")
        logger.success(f"self.parameter_data_image:{self.message_to_log(self.parameter_data_image)}")
        logger.success(f"self.parameter_data_color:{self.message_to_log(self.parameter_data_color)}")
        logger.success(f"self.parameter_data_yolo:{self.message_to_log(self.parameter_data_yolo)}")
        logger.success(f"self.parameter_data_mutil_colors:{self.message_to_log(self.parameter_data_mutil_colors)}")

        logger.success("+=====================原始数据=====================================+")
        logger.success(f"self.original_data_word:{self.message_to_log(self.original_data_word)}")
        logger.success(f"self.original_data_image:{self.message_to_log(self.original_data_image)}")
        logger.success(f"self.original_data_color:{self.message_to_log(self.original_data_color)}")
        logger.success(f"self.original_data_yolo:{self.message_to_log(self.original_data_yolo)}")
        logger.success(f"self.original_data_mutil_colors:{self.message_to_log(self.original_data_mutil_colors)}")

        logger.success("+======================游戏信息===================================+")
        logger.success(f"self.role_info_dict:{self.message_to_log(self.role_info_dict)}")
        logger.success(f"self.target_info_dict:{self.message_to_log(self.target_info_dict)}")
        logger.success(f"self.coordinate_info_dict:{self.message_to_log(self.coordinate_info_dict)}")
        logger.success(f"self.task_info_dict:{self.message_to_log(self.task_info_dict)}")
        logger.success(f"self.gear_info_dict:{self.message_to_log(self.gear_info_dict)}")
        logger.success(f"self.pet_info_dict:{self.message_to_log(self.pet_info_dict)}")
        logger.success(f"self.summons_info_dict:{self.message_to_log(self.summons_info_dict)}")
        logger.success(f"self.interface_info_dict:{self.message_to_log(self.interface_info_dict)}")


    def run(self,original_data,numpy_data,queue_handle):
        self.queue_handle=None

        self.queue_handle=queue_handle # 线程队列信息
        self.original_data=original_data #原始数据
        self.numpy_data=numpy_data #numpy数据
        self.information_processing() #原始数据初级处理
        self.role_info() #角色信息
        self.target_info() #目标信息
        self.map_info() #地图信息
        self.task_info() #任务信息
        self.gear_info() #角色装备信息
        self.pet_info() #宠物信息
        self.summons_info() #召唤物信息
        self.interface_info() #界面信息
        self.unique_info()  # 参数信息_特有的
        if self.debug:
            self.debug_info()

        logger.success(f"数据清洗中")

        return {"role_info_dict":self.role_info_dict, # 角色信息
                "target_info_dict":self.target_info_dict,  # 目标信息
                "coordinate_info_dict":self.coordinate_info_dict, # 坐标信息
                "task_info_dict":self.task_info_dict, # 任务信息
                "gear_info_dict":self.gear_info_dict, # 角色装备信息
                "pet_info_dict":self.pet_info_dict, # 宠物信息
                "summons_info_dict":self.summons_info_dict, # 召唤物信息
                "interface_info_dict":self.interface_info_dict, # 界面信息
                "processed_data_word_acquire":self.processed_data_word_acquire, # 获取到的文字信息
                "processed_data_word_handle":self.processed_data_word_handle, # 处理后的文字信息
                "processed_data_color_acquire":self.processed_data_color_acquire, # 获取到的颜色信息
                "processed_data_color_handle":self.processed_data_color_handle, # 处理后的颜色信息
                "processed_data_image":self.processed_data_image, # 获取到的图片信息
                "processed_data_yolo":self.processed_data_yolo, # 获取到的yolo信息
                "processed_data_mutil_colors":self.processed_data_mutil_colors, # 获取到的多颜色信息
                "processed_data_unique": self.processed_data_unique,  # 参数信息_特有的
                }



