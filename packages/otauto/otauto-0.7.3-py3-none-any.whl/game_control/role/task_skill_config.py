import os
import random
import time

from game_control.role.gray_color import gray_ratio
from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块
from resource.parameters_info.basic_parameter_info import (skill_arrangement_少林, skill_arrangement_天煞,
                                                           skill_arrangement_凌云, skill_arrangement_蜀山,
                                                           skill_arrangement_灵宿, shortcut_bar_dict,
                                                           skill_arrangement_百花医, skill_arrangement_侠隐岛)


"""
功能:技能配置
日期:2025-2-27 13:20:41
描述:用于职业技能配置
"""

class TaskSkillConfig(TaskLogic):
    """
    任务详情:这里接入任务的具体操作内容
    def task_details(self),所有操作接入这个函数中
    vnc: vnc对象
    vnc_port: vnc端口号
    queue_handle: 队列操作对象
    task_welfare
    """
    def __init__(self,vnc,vnc_port,queue_handle):
        super().__init__(vnc,vnc_port,queue_handle)
        self.skill_allocation = None #需要配置的技能
        self.skill_config_scope={} #技能配置的坐标信息
        if self.role_sect in ["少林"]:
            self.skill_config_scope=skill_config_少林_scope #技能配置坐标信息
            self.skill_rage_num=skill_rage_num_少林 #怒气技能
            self.skill_arrangement = skill_arrangement_少林 #技能在快捷栏中的位置
        elif self.role_sect in ["凌云","凌云寨"]:
            self.skill_config_scope=skill_config_凌云_scope
            self.skill_rage_num = skill_rage_num_凌云
            self.skill_arrangement = skill_arrangement_凌云
        elif self.role_sect in ["蜀山"]:
            self.skill_config_scope=skill_config_蜀山_scope
            self.skill_rage_num = skill_rage_num_蜀山
            self.skill_arrangement = skill_arrangement_蜀山
        elif self.role_sect in ["天煞"]:
            self.skill_config_scope=skill_config_天煞_scope
            self.skill_rage_num = skill_rage_num_天煞
            self.skill_arrangement = skill_arrangement_天煞
        elif self.role_sect in ["灵宿"]:
            self.skill_config_scope=skill_config_灵宿_scope
            self.skill_rage_num = skill_rage_num_灵宿
            self.skill_arrangement = skill_arrangement_灵宿
        elif self.role_sect in ["百花医"]:
            self.skill_config_scope=skill_config_百花医_scope
            self.skill_rage_num = skill_rage_num_百花医
            self.skill_arrangement = skill_arrangement_百花医
        elif self.role_sect in ["侠隐岛"]:
            self.skill_config_scope=skill_config_侠隐岛_scope
            self.skill_rage_num = skill_rage_num_侠隐岛
            self.skill_arrangement = skill_arrangement_侠隐岛


    def get_filename_without_extension(self,path) -> str:
        """
        获取文件名（不带扩展名）
        :param path: 文件名
        :return:
        """
        filename_with_extension = os.path.basename(path)
        filename_without_extension = os.path.splitext(filename_with_extension)[0]
        return filename_without_extension

    def find_entry(self,data, specified_name):
        """
        从列表中找出有数字的条目，并返回其中数字最大的那个。
        如果没有数字，返回指定名称里最小置信度的条目。
        # 测试代码
            data = [
                ('如封似闭', 524, 300, 0.997),
                ('如封似闭', 680, 301, 0.998),
                ('如封似闭', 834, 298, 0.998),
                ('1级', 528, 322, 0.996),
                ('2级', 681, 321, 1.0),
                ('3级', 838, 322, 1.0)
            ]
            result = find_entry(data, '如封似闭')#(834, 298)

        Parameters:
        data (list): 每个元素是一个元组，包含条目信息。
        specified_name (str): 如果没有数字条目，找该名称中最小置信度的条目。

        Returns:
        tuple: 符合条件的条目
        """
        # 优先找出带数字的条目
        numerical_entries = [entry for entry in data if any(char.isdigit() for char in entry[0])]

        if numerical_entries:
            # 找出带数字条目中数字最小的一条
            max_numerical_entry = min(numerical_entries, key=lambda x: int(''.join(filter(str.isdigit, x[0]))))
            _, x, y, _ = max_numerical_entry
            return x - 26, y - 6
        else:
            # 找到指定名称里最小置信度的条目
            specified_name_entries = [entry for entry in data if entry[0] == specified_name]
            if specified_name_entries:
                min_confidence_entry = min(specified_name_entries, key=lambda x: x[1])
                _, x, y, _ = min_confidence_entry
                return x, y
            else:
                return None

    def create_shortcut_dict(self,shortcut_list, shortcut_bar_dict):
        """
        根据给定的快捷键列表和快捷栏字典，创建一个包含快捷键和对应坐标的字典。
        :param shortcut_list: 快捷键列表
        :param shortcut_bar_dict: 快捷栏字典
        :return: {'9': (518, 831), '2': (231, 830), '1': (192, 830)}或者{}
        """
        return {
            shortcut: (
                (coords[0] + coords[2]) // 2,
                (coords[1] + coords[3]) // 2
            )
            for shortcut in shortcut_list if shortcut in shortcut_bar_dict
            for coords in [shortcut_bar_dict[shortcut]]
        }

    def find_Shortcut_bar_function(self):
        """
        找到快捷栏字典中每个键对应的图片,用于快捷栏功能查找
        #示例代码:
            res=find_Shortcut_bar_function(shortcut_bar_dict, dic_image_hand)
            print(res)
        :return: '1': 'resource/images_info/role_skill/穿云剑.bmp', '2': 'resource/images_info/role_skill/如封似闭.bmp', }
        """
        # 创建一个空的新字典
        new_dict = {}
        if self.unique_data:
            # 对于快捷栏字典中的每个键和值
            for key, value in shortcut_bar_dict.items():
                #{"1":(172,810,212,850)}
                # 遍历图像字典来查找匹配的坐标
                for image_path, values in self.unique_data["image"].items():
                    """
                    {'word': {}, 
                    'image': {
                        'resource/images_info/role_skill/沾字决.png': {'scope': [(226, 826, 249, 842, 0.813)], 'enable': True, 'unique': True}, 
                        'resource/images_info/role_skill/舍身卫道.png': {'scope': [(295, 839, 328, 859, 0.842)], 'enable': True, 'unique': True},
                        'resource/images_info/role_skill/缠字决.png': {'scope': [(427, 827, 447, 857, 0.915)], 'enable': True, 'unique': True},
                        'resource/images_info/role_skill/狮子吼.png': {'scope': [(467, 827, 487, 857, 0.807)], 'enable': True, 'unique': True}, 
                        'resource/images_info/role_skill/般若功.png': {'scope': [(789, 826, 817, 855, 0.81)], 'enable': True, 'unique': True}, 
                        'resource/images_info/main_task/商城.bmp': {'scope': [(1206, 59, 1227, 82, 0.998)], 'unique': True}
                    }, 
                    'mutil_colors': {}
                    }
                    """
                    coords=values.get("scope")
                    # 遍历图像字典中的坐标列表
                    for coord in coords:
                        # 如果坐标的两点坐标(x, y)落在快捷栏的区域内
                        if value[0] <= coord[0] <= value[2] and value[1] <= coord[1] <= value[3]:
                            # 将快捷键与图像路径的映射加入新字典
                            new_dict[key] = image_path

        return new_dict

    def task_快捷栏功能(self):
        return self.find_Shortcut_bar_function()

    def task_技能位置(self,ocr_dict, set_dict):
        """
        技能在快捷栏的位置,和配置文件中的位置进行对比
        设置,更换,
        :param ocr_dict: 识别出来的字典
        :param set_dict: 设置好的字典
        :return: 2个字典不同的键值对
        """
        # 创建新的字典包含需要的信息
        new_dict = {"ocr_dict": {}, "set_dict": {}}

        # 寻找 ocr_dict 不在 set_dict 中的键值对
        for key, value in ocr_dict.items():
            if key not in set_dict:
                new_dict["ocr_dict"][key] = value

        # 寻找 ocr_dict 和 set_dict 中值不同的键值对
        for key in set(ocr_dict.keys()).intersection(set_dict.keys()):
            if ocr_dict[key] != set_dict[key]:
                new_dict["ocr_dict"][key] = ocr_dict[key]
                new_dict["set_dict"][key] = set_dict[key]

        # 寻找 set_dict 不在 ocr_dict 中的键值对
        for key, value in set_dict.items():
            if key not in ocr_dict:
                new_dict["set_dict"][key] = value

        return new_dict

    def task_位置纠正(self,shortcut_dict ):
        """
        识别快捷栏里的技能,和配置文件中的技能进行对比
        :param shortcut_dict: 快捷栏配置文件
        :return: 快捷栏编号['9', '1', '2']或者[]
        """
        # 创建存储匹配键的列表
        shortcut_bar_list = []
        ocr_dict = shortcut_dict['ocr_dict']
        set_dict = shortcut_dict['set_dict']
        # 遍历 ocr_dict
        for key, value in ocr_dict.items():
            # 检查 value 是否在 set_dict 的 values 中
            if value in set_dict.values():
                shortcut_bar_list.append(key)
            elif key in set_dict.keys():
                shortcut_bar_list.append(key)
        return shortcut_bar_list

    def task_技能配置判断(self):
        self.node_current = "task_技能配置判断"

        if self.node_counter >=8:  # 计数器大于等于5,退出
            logger.error("技能配置判断,出现错误,请人工配置")
            self.node_counter = 0  # 重置计数器
            self.node_current = "task_技能配置完成"
            return "task_finish"
        else:#多种情况处理
            ocr_dict = self.task_快捷栏功能()  # 查看快捷栏里的技能
            logger.debug(f"快捷栏技能:{ocr_dict}")

            res_dict=self.task_技能位置(ocr_dict,self.skill_arrangement)
            logger.debug(f"技能配置判断:{res_dict}")

            if res_dict["ocr_dict"] and res_dict["set_dict"]:#说明技能栏的技能和配置文件不匹配
                self.node_counter+=1 #节点计数器加一
                logger.info("技能栏的技能和配置文件不匹配")
                res_list=self.task_位置纠正(res_dict)#判断技能位置
                logger.error(f"技能位置:{res_list}")
                res_shortcut_dict=self.create_shortcut_dict(res_list,shortcut_bar_dict)#找出不符合位置的技能
                logger.debug(f"技能位置:{res_shortcut_dict}")
                if res_shortcut_dict: #如果存在技能错乱的情况
                    for coord in list(res_shortcut_dict.values()):
                        logger.info("快捷栏技能移除")
                        random_num=random.randint(1,8)
                        try:
                            self.mouse_drag(coord[0]+random_num,coord[1]+random_num,672+random_num,737+random_num,40)
                            time.sleep(1)
                        except Exception as e:
                            logger.error(f"快捷栏技能移除失败:{e}")
                    return True
                elif  res_dict["set_dict"]:#说明有技能不在快捷栏里
                    logger.info("有技能不在快捷栏里")
                    self.skill_allocation=res_dict["set_dict"] #获取技能配置
                    self.node_current="task_打开技能界面"
                    self.node_counter=0#重置计数器
                    return "task_finish"

            elif not res_dict["ocr_dict"]  and res_dict["set_dict"]:#说明有技能不在快捷栏里
                logger.info("有技能不在快捷栏里")
                self.skill_allocation=res_dict["set_dict"] #获取技能配置
                self.node_current="task_打开技能界面"
                self.node_counter=0#重置计数器
                return "task_finish"

            elif  not res_dict["set_dict"] :#说明技能栏的技能和配置文件完全匹配
                logger.info("技能栏的技能和配置文件完全匹配")
                self.node_current="task_技能配置完成"
                self.node_counter = 0  # 重置计数器
                return "task_finish"

    def task_打开技能界面(self):
        self.node_current = "task_打开技能界面"

        if self.node_counter >= 3:  # 计数器大于等于5,退出
            logger.error("打开技能界面出现未知错误,请人工配置")
            self.node_counter = 0  # 重置计数器
            self.node_current = "task_技能配置完成"
            return "task_finish"

        elif "技能界面" in self.interface_info:
            logger.info("技能界面")
            self.node_current = "task_技能解锁判断"
            self.node_counter = 0  # 重置计数器
            return "task_finish"

        elif "主界面" in self.interface_info:
            self.key_press("K", delay_time=2)
            self.node_counter += 1 # 计数器加一

    def task_技能解锁判断(self):
        self.node_current = "task_技能解锁判断"

        if self.node_counter >=3:  # 计数器大于等于5,退出
            logger.error("技能未解锁")
            self.node_counter = 0  # 重置计数器
            self.node_current = "task_技能配置完成"
            return "task_finish"

        try:
            if self.skill_allocation:
                for num in self.skill_allocation:
                    x1, y1, x2, y2 = self.skill_config_scope[num][1:] # 获取技能配置的技能范围
                    numpy_array = self.data_numpy[y1:y2, x1:x2] #裁剪技能位置
                    res_percentage = gray_ratio(numpy_array)
                    logger.debug(f"技能{num},灰度比:{res_percentage}")
                    if res_percentage > 0.4:  # 灰度比大于0.4,则认为技能未解锁
                        self.skill_allocation.pop(num)
        except Exception as e:
            if "RuntimeError: dictionary changed size during iteration" in str(e):
                self.node_current = "task_技能配置完成"
                self.node_counter = 0  # 重置计数器
                return "task_finish"

        if self.skill_allocation:  # 说明有技能已经解锁
            self.node_current = "task_技能配置"
            self.node_counter = 0  # 重置计数器
            return "task_finish"
        else:
            self.node_counter += 1  # 计数器加一

    def task_技能配置(self):
        self.node_current = "task_技能配置"

        if self.node_counter >= 5:  # 计数器大于等于5,退出
            logger.error("技能配置出现未知错误,请人工配置")
            self.node_counter = 0  # 重置计数器
            self.node_current = "task_技能配置完成"
            return "task_finish"

        elif "技能界面" in self.interface_info:
            logger.info(f"技能界面,开始技能配置{self.skill_allocation}")
            if self.skill_allocation:  # 说明有技能需要配置
                try:
                    for shortcut_number in self.skill_allocation:
                        # 获取快捷栏的坐标
                        shortcut_dict = self.create_shortcut_dict([shortcut_number], shortcut_bar_dict)
                        shortcut_coord = next(iter(shortcut_dict.values()))

                        if shortcut_number in self.skill_rage_num:
                            skill_name= self.get_filename_without_extension(self.skill_allocation[shortcut_number])
                            word_list=self.find_word_scope(*self.skill_config_scope[shortcut_number][1:])
                            res_coor_tuple=self.find_entry(word_list,skill_name)
                            logger.debug(f"怒气技能坐标,{res_coor_tuple}")
                            if res_coor_tuple:#怒气技能设置
                                logger.debug(f"怒气技能配置: {res_coor_tuple}, {shortcut_coord}")
                                self.mouse_drag(res_coor_tuple[0], res_coor_tuple[1], shortcut_coord[0], shortcut_coord[1]+10, 40)
                                time.sleep(2)
                                self.mouse_move(669 + random.randint(1, 8), 642 + random.randint(1, 8),delay_time=0.6)
                                self.mouse_right_click(669,642,delay_time=0.5)
                                self.skill_allocation.pop(shortcut_number)  # 移除已配置的技能
                                time.sleep(1)
                                break
                            self.node_counter+=1 # 计数器加一

                        else:
                            # 获取在技能界面里技能的坐标
                            res_dict = self.find_image_scope(*self.skill_config_scope[shortcut_number])
                            print(res_dict)
                            if res_dict:
                                for coords in res_dict.values():
                                    logger.debug(f"普通技能配置: {coords}, {shortcut_coord}")
                                    self.mouse_drag(coords[0][0], coords[0][1], shortcut_coord[0], shortcut_coord[1]+10, 65)
                                    time.sleep(2)
                                    self.mouse_move(669 + random.randint(1, 8), 642 + random.randint(1, 8),delay_time=0.6)
                                    self.mouse_right_click(669,642,delay_time=0.5)
                                    self.skill_allocation.pop(shortcut_number) #移除已配置的技能
                                    time.sleep(1)
                                break
                            self.node_counter += 1  # 计数器加一
                except Exception as e:
                    if "RuntimeError: dictionary changed size during iteration" in str(e):
                        self.node_current = "task_技能配置完成"
                        self.node_counter = 0  # 重置计数器
                        return "task_finish"

            else:
                logger.info("技能配置完成")
                self.node_current = "task_技能配置完成"
                self.node_counter = 0  # 重置计数器
                return "task_finish"

        elif self.interface_info in ["主界面"] and self.skill_allocation:#说明有技能未配置
            logger.info(f"{self.interface_info}")
            self.key_press("K")
            self.node_counter=0#重置计数器
            return "task_finish"

        elif self.interface_info in ["主界面"] and not self.skill_allocation: #说明技能配置完成
            logger.info(f"{self.interface_info}")
            self.node_current = "task_技能配置完成"
            self.node_counter = 0  # 重置计数器
            return "task_finish"

    def task_技能配置完成(self):
        self.ls_progress = "task_finish"
        self.node_current = "task_技能配置完成"

        if "主界面" in self.interface_info:
            return "task_finish"
        else:
            self.interface_closes()

    def handle_task(self):
        task_methods = {
            "task_技能配置判断": self.task_技能配置判断,
            "task_打开技能界面": self.task_打开技能界面,
            "task_技能解锁判断": self.task_技能解锁判断,
            "task_技能配置": self.task_技能配置,
            "task_技能配置完成": self.task_技能配置完成,
        }
        if self.node_current in task_methods:
            task_methods[self.node_current]()

    def task_details(self):
        """
        self.ls_progress=None # 进度信息:task_finish,task_fail,task_error,task_wait,
        self.node_current=None #当前节点
        self.node_list= []  # 节点列表
        self.node_counter = 0 # 节点计数器
        self.queue_message({"word": {11: {"enable": False}}}) # 参数关闭
        函数写入这里
        """
        logger.success(f"任务详情:{self.__class__.__name__}")
        logger.success(f"节点信息:{self.node_current}")

        if self.role_sect in ["少林"]:
            self.skill_config_scope=skill_config_少林_scope #技能配置坐标信息
            self.skill_rage_num=skill_rage_num_少林 #怒气技能
            self.skill_arrangement = skill_arrangement_少林 #技能在快捷栏中的位置
        elif self.role_sect in ["凌云","凌云寨"]:
            self.skill_config_scope=skill_config_凌云_scope
            self.skill_rage_num = skill_rage_num_凌云
            self.skill_arrangement = skill_arrangement_凌云
        elif self.role_sect in ["蜀山"]:
            self.skill_config_scope=skill_config_蜀山_scope
            self.skill_rage_num = skill_rage_num_蜀山
            self.skill_arrangement = skill_arrangement_蜀山
        elif self.role_sect in ["天煞"]:
            self.skill_config_scope=skill_config_天煞_scope
            self.skill_rage_num = skill_rage_num_天煞
            self.skill_arrangement = skill_arrangement_天煞
        elif self.role_sect in ["灵宿"]:
            self.skill_config_scope=skill_config_灵宿_scope
            self.skill_rage_num = skill_rage_num_灵宿
            self.skill_arrangement = skill_arrangement_灵宿
        elif self.role_sect in ["百花医"]:
            self.skill_config_scope=skill_config_百花医_scope
            self.skill_rage_num = skill_rage_num_百花医
            self.skill_arrangement = skill_arrangement_百花医
        elif self.role_sect in ["侠隐岛"]:
            self.skill_config_scope=skill_config_侠隐岛_scope
            self.skill_rage_num = skill_rage_num_侠隐岛
            self.skill_arrangement = skill_arrangement_侠隐岛


        if not self.node_current:
            self.task_技能配置判断()
        elif self.handle_task():
            pass

        self.queue_screenshot_sync(reset=False)

#快捷栏范围
skill_scope=(153, 815, 975, 866)

#怒气技能位置
skill_rage_num_少林=["-1"]
skill_rage_num_凌云=["-1",]
skill_rage_num_蜀山=["-1","-1"]
skill_rage_num_天煞=["-1","-1"]
skill_rage_num_灵宿=["-1"]
skill_rage_num_百花医=["-1"]
skill_rage_num_侠隐岛=["-1",] #假的

#技能界面中的技能位置
skill_config_少林_scope={
    "1": ["resource/images_info/role_skill/龙形棍.png",478, 435, 521, 478],
    "2": ["resource/images_info/role_skill/沾字决.png",479, 252, 520, 296],
    "3": ["resource/images_info/role_skill/明王震.png",790, 591, 837, 634],
    "4": ["resource/images_info/role_skill/舍身卫道.png",478, 357, 521, 399],
    "5": ["resource/images_info/role_skill/豹尾脚.png",790, 434, 833, 478],
    "6": ["resource/images_info/role_skill/虎形棍.png",635, 435, 676, 478],
    "7": ["resource/images_info/role_skill/缠字决.png",478, 304, 519, 346],
    "8": ["resource/images_info/role_skill/狮子吼.png",476, 537, 523, 585],
    "alt+1": ["resource/images_info/role_skill/般若功.png",477, 486, 521, 531],
    "alt+2": ["resource/images_info/role_skill/破衲功.png",632, 486, 679, 531],
    "9": ["resource/images_info/role_skill/内功疗伤.png",790, 487, 834, 531],
    "alt+4": ["resource/images_info/role_skill/清净佛音.png",633, 538, 677, 582],
}
skill_config_蜀山_scope={
    "8":["resource/images_info/role_skill/疾风追电.bmp",467,235,947,294], #怒气技能
    "2":["resource/images_info/role_skill/如封似闭.bmp",469,291,941,348],#怒气技能
    "1":["resource/images_info/role_skill/穿云剑.bmp",477,375,521,419],
    "5":["resource/images_info/role_skill/皓月斩.bmp",630,373,681,423],
    "4":["resource/images_info/role_skill/昊天掌.bmp",786,373,834,421],
    "alt+1":["resource/images_info/role_skill/琴心三叠.bmp",471,422,525,476],
    "alt+3":["resource/images_info/role_skill/雪花六出.bmp",631,427,679,474],
    "7":["resource/images_info/role_skill/风雷震_技能界面.bmp",786,428,834,473],
    "6":["resource/images_info/role_skill/御剑术-剑雨.bmp",474,476,522,526],
    "alt+2":["resource/images_info/role_skill/剑灵-回天.bmp",476,532,522,579],
    "3":["resource/images_info/role_skill/剑飞惊鸿.bmp",788,583,835,631],
}
skill_config_天煞_scope={
    "1":["resource/images_info/role_skill/破空斩.png",630, 432, 681, 481],
    "2":["resource/images_info/role_skill/毒龙刺.png",477, 435, 520, 477],
    "3":["resource/images_info/role_skill/怒火燎原.png",791, 434, 834, 480],
    "4":["resource/images_info/role_skill/撞击.png",477, 484, 523, 530],
    "5":["resource/images_info/role_skill/狂风沙.png",633, 486, 679, 529],
    "6":["resource/images_info/role_skill/气贯长虹.png",471, 240, 938, 300], #怒气技能
    "7":["resource/images_info/role_skill/山摇地震.png",473, 298, 940, 351], #怒气技能
}
skill_config_凌云_scope={
    "1":["resource/images_info/role_skill/百步穿杨.png",470, 234, 524, 296],
    "2":["resource/images_info/role_skill/箭无虚发.png",629, 239, 678, 293],
    "4":["resource/images_info/role_skill/战狼决.png",786, 239, 834, 290],
    "3":["resource/images_info/role_skill/灵兽阵.png",789, 296, 832, 342],
    "5":["resource/images_info/role_skill/飞羽诀.png",470, 456, 525, 506],
    "8":["resource/images_info/role_skill/捆兽索.png",630, 299, 678, 348], #怒气技能
}
skill_config_灵宿_scope={
    "1":["resource/images_info/role_skill/追灵诀.png",477, 248, 520, 296],
    "2":["resource/images_info/role_skill/阴阳诀.png",632, 251, 684, 297],
    "3":["resource/images_info/role_skill/劫火焚心.png",474, 457, 522, 504],
    "4":["resource/images_info/role_skill/无相涅槃.png",797, 258, 822, 285],#怒气技能
    "5":["resource/images_info/role_skill/残影镇魂.png",477, 299, 522, 347],
    "6":["resource/images_info/role_skill/诛神诀.png",631, 301, 676, 349],
    "7":["resource/images_info/role_skill/乱环诀.png",789, 302, 834, 347],
    "8": ["resource/images_info/role_skill/勾魂索魄.png",633, 355, 678, 397],
    "9": [ "resource/images_info/role_skill/涅槃.png", 478, 404, 521, 451],
}
skill_config_百花医_scope={
    "1": ["resource/images_info/role_skill/断肠引.png",478, 386, 519, 427],
    "2": ["resource/images_info/role_skill/蝶飞花舞.png",478, 250, 521, 294],
    "3": ["resource/images_info/role_skill/百花殇.png",637, 389, 669, 416],
    "4": ["resource/images_info/role_skill/出水芙蓉.png",477, 303, 522, 349],
    "5": ["resource/images_info/role_skill/红叶舞秋.png",476, 535, 523, 585],
    "6": ["resource/images_info/role_skill/八门化伤.png",787, 431, 836, 481],
    "8": ["resource/images_info/role_skill/妙手回春.png",482, 440, 514, 473],
    "9": ["resource/images_info/role_skill/逆转丹行.png",640, 441, 669, 472],
    "alt+1": ["resource/images_info/role_skill/攻击光环.png",632, 486, 680, 534],
    "alt+2": ["resource/images_info/role_skill/生命光环.png",788, 485, 836, 531],
    "alt+3": ["resource/images_info/role_skill/防御光环.png",474, 486, 523, 533],
    "alt+4": ["resource/images_info/role_skill/荆棘护甲.png",788, 378, 838, 431],
}

skill_config_侠隐岛_scope={
    "1": ["resource/images_info/role_skill/双排云.png",787, 248, 834, 295],
    "2": ["resource/images_info/role_skill/玄冰掌.png",633, 301, 675, 349],
    "3": ["resource/images_info/role_skill/火焰掌.png",474, 248, 522, 298],
    "4": ["resource/images_info/role_skill/烈焰击.png",476, 354, 522, 398],
    "5": ["resource/images_info/role_skill/混元击.png",477, 303, 522, 345],
    "6": ["resource/images_info/role_skill/平地惊雷.png",477, 407, 519, 451],
    "9": ["resource/images_info/role_skill/内力护体.png",630, 248, 679, 296],
    "alt+1": ["resource/images_info/role_skill/万象心法.png",631, 405, 678, 452],
}


#技能配置
skill_config_少林_data={
    "image": {
        r"resource/images_info/role_skill/龙形棍.png":{
            "scope":skill_scope,
            "con":0.8,
            "enable":True,
            "model":1,
            "unique": True,
        },#奖励图标
        r"resource/images_info/role_skill/沾字决.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/明王震.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标

        r"resource/images_info/role_skill/舍身卫道.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标

        r"resource/images_info/role_skill/豹尾脚.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标

        r"resource/images_info/role_skill/虎形棍.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/缠字决.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/狮子吼.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/般若功.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/破衲功.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/内功疗伤.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/清净佛音.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
    },
}
skill_config_蜀山_data = {
    "image": {
        r"resource/images_info/role_skill/疾风追电.bmp": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/如封似闭.bmp": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/穿云剑.bmp": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/皓月斩.bmp": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/昊天掌.bmp": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/琴心三叠.bmp": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/雪花六出.bmp": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/风雷震_技能界面.bmp": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/御剑术-剑雨.bmp": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/剑灵-回天.bmp": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/剑飞惊鸿.bmp": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
    }
}
skill_config_天煞_data = {
    "image": {
        r"resource/images_info/role_skill/破空斩.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/毒龙刺.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/怒火燎原.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/撞击.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/狂风沙.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/气贯长虹.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/山摇地震.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
    }
}
skill_config_凌云_data = {
    "image": {
        r"resource/images_info/role_skill/百步穿杨.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/箭无虚发.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/灵兽阵.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/战狼决.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/飞羽诀.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
        r"resource/images_info/role_skill/捆兽索.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable": True,
            "model": 1,
            "unique": True,
        },
    }
}
skill_config_灵宿_data={
    "image": {
        r"resource/images_info/role_skill/追灵诀.png":{
            "scope":skill_scope,
            "con":0.8,
            "enable":True,
            "model":1,
            "unique": True,
        },#奖励图标
        r"resource/images_info/role_skill/阴阳诀.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/劫火焚心.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标

        r"resource/images_info/role_skill/无相涅槃.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标

        r"resource/images_info/role_skill/残影镇魂.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标

        r"resource/images_info/role_skill/诛神诀.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/乱环诀.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/勾魂索魄.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/涅槃.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
    },
}
skill_config_百花医_data={
    "image": {
        r"resource/images_info/role_skill/断肠引.png":{
            "scope":skill_scope,
            "con":0.8,
            "enable":True,
            "model":1,
            "unique": True,
        },#奖励图标
        r"resource/images_info/role_skill/蝶飞花舞.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/百花殇.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标

        r"resource/images_info/role_skill/出水芙蓉.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标

        r"resource/images_info/role_skill/红叶舞秋.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标

        r"resource/images_info/role_skill/八门化伤.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/妙手回春.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/逆转丹行.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/攻击光环.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/生命光环.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/防御光环.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/荆棘护甲.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
    },
}
skill_config_侠隐岛_data={
    "image": {
        r"resource/images_info/role_skill/双排云.png":{
            "scope":skill_scope,
            "con":0.8,
            "enable":True,
            "model":1,
            "unique": True,
        },#奖励图标
        r"resource/images_info/role_skill/玄冰掌.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/火焰掌.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标

        r"resource/images_info/role_skill/烈焰击.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标

        r"resource/images_info/role_skill/混元击.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标

        r"resource/images_info/role_skill/平地惊雷.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/内力护体.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/role_skill/万象心法.png": {
            "scope": skill_scope,
            "con": 0.8,
            "enable":True,
            "model": 1,
            "unique": True,
        },  # 奖励图标
    },
}
