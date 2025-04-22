import time
from game_control.task_logic import TaskLogic, ImageComparer  # 接入基本的任务逻辑信息
from loguru import logger #接入日志模块
from resource.parameters_info.basic_parameter_info import gear_name_point_dict # 导入装备位置范围

class TaskEquipEnhanced(TaskLogic):
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

        self.err_num = 1 # 错误次数
        self.sorting_flag = False #  整理
        self.organize_backpack_flag = False  #定义一个标志位，用于判断是否进入整理
        self.material_info={}  # 定义一个空字典，用于存储材料信息
        self.eqiup_list = ["lower_武器","upper_武器","lower_防具","upper_防具"] # 定义一个空列表，用于存储可以强化的装备信息
        self.node_flag= False #定义一个标志位，用于判断是否进入节点
        self.eqiup_numpy = None #定义一个空列表，用于numpy数组信息
        self.scope_背包=None #定义一个空元组，用于存储背包范围的坐标
        self.equip_position = None #定义一个空元组，用于存储装备的位置信息
        self.last_equip_position = None # 定义一个空元组，用于之前存储装备的位置信息
        self.gear_type = None # 当前任务信息
        self.next_task= None # 用于存储下一个任务的信息
        self.num_enhance = 0  # 强化次数
        self.node_info_flag = False #装备详情标志位
        self.ready_flag = False  #装备强化已经准备完成
        self.intensify_op_flag = False # 强化操作标志位
        self.last_color_block_list= [] # 定义一个空列表，用于包裹空格
        self.current_color_block_list= [] # 定义一个空列表，用于包裹空格

    def find_close_elements(self,a_ls, b_ls):
        """
        找到列表 a 和 b 中的元素，满足它们的第一个和第二个值之间的差小于 6 的元素对。

        参数:
        a_ls (list): 包含元组的列表，每个元组包含多个值（如 (x, y, ... )）。
        b_ls (list): 包含元组的列表，每个元组也包含多个值（如 (x, y, ... )）。

        返回:
        list: 符合条件的元素对的列表，每个元素对仅包含 a 中的前两个值 (x, y)。
        """
        close_elements = []  # 用于存储符合条件的元素对

        # 遍历列表 a 中的每个元素
        for elem_a in a_ls:
            # 遍历列表 b 中的每个元素
            for elem_b in b_ls:
                # 检查 a 和 b 中元素的第一个和第二个值的差是否小于 6
                if abs(elem_a[0] - elem_b[0]) < 6 and abs(elem_a[1] - elem_b[1]) < 6:
                    # 如果满足条件，将 elem_a 的前两个值添加到结果列表
                    close_elements.append((elem_a[0], elem_a[1]))

        return close_elements  # 返回符合条件的元素对

    def task_背包范围识别(self):
        """
        识别背包范围
        """
        if self.node_counter>=5:#如果超过5次,则放弃任务
            self.node_current="task_强化完成"
            self.node_counter=0 #重置节点计数器
            return "task_finish"

        if "背包界面" in self.interface_info:
            if not self.sorting_flag:
                if self.find_data_from_keys_list_click(["resource/images_info/equipment_strengthening/整理.png"],
                                                    self.image_data, delay_time=2):
                    self.sorting_flag=True
                    self.mouse_move(1278,692,delay_time=0.5)
                    return True

            elif self.sorting_flag:
                res_dict=self.find_data_from_keys_list(["resource/images_info/equipment_strengthening/激战.png","resource/images_info/equipment_strengthening/整理.png","resource/images_info/other/背包空格.png"],self.image_data)
                """
                {'resource/images_info/equipment_strengthening/激战.png': {'scope': [(917, 377, 940, 409, 1.0)], 'enable': True, 'unique': True, 'model': 1}, 
                'resource/images_info/equipment_strengthening/整理.png': {'scope': [(1143, 672, 1161, 709, 1.0)], 'enable': True, 'unique': True, 'model': 1}}
                 """
                if res_dict and len(res_dict)==3: #如果识别到两个图标
                    # 获取原始的 scope 列表
                    self.last_scope_list = res_dict['resource/images_info/other/背包空格.png']['scope']
                    # 根据第二个元素进行排序(990, 492, 1021, 522, 0.999)
                    sorted_scope = sorted(self.last_scope_list, key=lambda x: x[1])[0]
                    top_left_ls=res_dict.get('resource/images_info/equipment_strengthening/激战.png')
                    x1, y1 = top_left_ls.get("scope")[0][0] - 286 + 9, top_left_ls.get("scope")[0][1] + 39
                    # x1,y1=sorted_scope[0]-30,sorted_scope[1]-30
                    bottom_right_ls=res_dict.get('resource/images_info/equipment_strengthening/整理.png')
                    x2,y2=bottom_right_ls.get("scope")[0][0]+28,bottom_right_ls.get("scope")[0][1]-108
                    self.scope_背包=(x1,y1,x2,y2)
                    self.node_current="task_武器强化部分查询"
                    self. queue_message({"interval": 1})  # 暂停识别线程
                    self.eqiup_numpy = self.vnc_sync.capture_full_screen_as_numpy() #同步截图
                    self.last_color_block_list=self.find_color_black(*self.scope_背包)
                    self.key_press("B",delay_time=1)
                    return True

        elif "主界面" in self.interface_info:
            self.key_press("B",delay_time=1)

        self.node_counter+=1 #节点计数器加1


    def task_装备强化部分查询(self, gear_type, next_task):
        """
        根据装备类型和下一个任务进行操作
        """
        self.gear_type=gear_type # 设置当前任务
        self.next_task = next_task # 设置下一个任务
        self.node_current = f"task_{gear_type}强化部分查询"

        logger.error(f"{gear_type}强化部分查询")

        if self.node_counter >= 8:  # 如果超过5次,则放弃任务
            self.node_current = next_task
            self.node_counter = 0  # 重置节点计数器
            return "task_finish"

        elif "背包界面" in self.interface_info:
            self.key_press("B",delay_time=1)
            return True

        elif "角色信息界面" in self.interface_info:
            logger.error(f"可以强化的装备信息:{self.eqiup_list}")
            # 只对武器和防具进行判断
            if gear_type == "武器":
                if "lower_武器" in self.eqiup_list or "upper_武器" in self.eqiup_list:  # 有武器强化的材料
                    self._process_装备强化(gear_type, next_task)
                    return True
                else:
                    self.node_current=self.next_task
                    return True

            elif gear_type in ["头盔","衣服","护手","腰带","鞋子"]:
                if "lower_防具" in self.eqiup_list or "upper_防具" in self.eqiup_list:  # 有防具强化的材料
                    self._process_装备强化(gear_type, next_task)
                    return True
                else:
                    self.node_current ="task_强化完成"
                    return True

        elif "主界面" in self.interface_info:
            self.key_press("c", delay_time=1)

        self.node_counter += 1

    def _process_装备强化(self, gear_type, next_task):
        if self.node_info_flag:
            x1,y1,x2,y2=equip_scope_details[gear_type]
            if  self.find_color_exists_in_array(x1,y1,x2,y2): # 如果是紫装
                self.mouse_right_click(*gear_name_point_dict[gear_type], delay_time=1)  # 装备取下
                self.interface_closes()
                self.node_current = "task_装备强化"
                self.node_info_flag = False # 装备点位
                return "task_finish"
            else:  # 如果没有强化等级,则放弃任务
                logger.error(f"未能找到当前{gear_type}强化等级,下一个")
                self.node_current = next_task
                self.node_info_flag = False # 装备点位
                self.node_counter=0 # 重置节点计数器

        elif not self.node_info_flag:
            logger.error(f"装备点位:{gear_name_point_dict[gear_type]}")
            self.node_info_flag = True
            return True

    def task_武器强化部分查询(self):
        self.task_装备强化部分查询("武器", "task_头盔强化部分查询")

    def task_头盔强化部分查询(self):
        self.task_装备强化部分查询("头盔", "task_衣服强化部分查询")

    def task_衣服强化部分查询(self):
        self.task_装备强化部分查询("衣服", "task_护手强化部分查询")

    def task_护手强化部分查询(self):
        self.task_装备强化部分查询("护手", "task_腰带强化部分查询")

    def task_腰带强化部分查询(self):
        self.task_装备强化部分查询("腰带", "task_鞋子强化部分查询")

    def task_鞋子强化部分查询(self):
        self.task_装备强化部分查询("鞋子", "task_强化完成")

    def task_装备强化(self):

        if self.node_counter >=8 or self.err_num >= 5:  # 如果超过5次,则放弃任务
            self.node_current = "task_强化完成"
            self.node_counter = 0  # 重置节点计数器
            self.err_num = 0 # 重置错误次数
            return "task_finish"

        if self.intensify_op_flag: # 开始强化
            if self.ready_flag:
                logger.error("装备穿回")
                if "背包界面" in self.interface_info:
                    if not self.organize_backpack_flag:
                        for i  in range(2):
                            self.mouse_right_click(*self.equip_position, delay_time=1)  # 穿上装备
                        if self.find_data_from_keys_list_click(["resource/images_info/equipment_strengthening/整理.png"],
                                                            self.image_data, delay_time=1):
                            self.organize_backpack_flag=True # 确认整理
                            return "task_finish"
                    elif self.organize_backpack_flag:
                        self.last_color_block_list = self.find_color_black(*self.scope_背包) # 获取当前屏幕截图
                        self.eqiup_numpy = self.vnc_sync.capture_full_screen_as_numpy() #同步截图
                        self.node_current = self.next_task  # 下一个任务节点
                        self.node_counter = 0  # 重置节点计数器
                        self.ready_flag = False  # 重置
                        self.intensify_op_flag= False # 重置
                        self.equip_position= None # 重置
                        self.current_color_block_list=[] # 重置
                        self.organize_backpack_flag=False # 重置
                        time.sleep(1)
                        # self.key_press("B", delay_time=1)
                        return "task_finish"

                elif "主界面" in self.interface_info:
                    self.key_press("B", delay_time=1)
                    return True

            elif not self.ready_flag:
                logger.error("测试点2")
                if self.num_enhance >= 4:
                    logger.warning("装备强化次数到预定值,停止")
                    self.num_enhance = 0  # 重置次数
                    self.node_counter = 0  # 重置节点计数器
                    self.ready_flag = True
                    return True
                elif "装备强化界面" in self.interface_info or self.find_data_from_keys_list(["欢迎光临"],self.word_handle_data):
                    x1, y1 = self.interface_info.get("装备强化界面", (790, 183))
                    self.mouse_left_click(x1 - 110, y1, delay_time=1)
                    logger.error(f"装备强化界面")
                    for i in range(4):
                        self.mouse_left_click_scope(695, 632, 732, 643)
                    self.mouse_left_click_scope(831, 631, 869, 643)
                    self.key_press("B")
                    self.num_enhance=5

        elif not self.intensify_op_flag: # 强化前准备工作
            logger.error("强化前准备工作")
            if self.equip_position: # 如果装备位存在
                if "背包界面" in self.interface_info:
                    if self.find_data_from_keys_list_click(["resource/images_info/equipment_strengthening/强化图标.png"],self.image_data,x3=10,y3=15,delay_time=1):
                        self.mouse_left_click(658,690)
                        logger.error("把装备放入强化界面")
                        self.mouse_right_click_scope(929, 573, 1177, 647,delay_time=1) #背包前置
                        for i in range(2):
                            self.mouse_right_click(*self.equip_position, delay_time=1) #丢入装备
                        self.mouse_right_click(770,198,delay_time=1) # 进阶前置
                        self.key_press("B")
                        self.node_counter = 0  # 重置节点计数器
                        self.intensify_op_flag = True
                        return True
                elif "主界面" in self.interface_info:
                    self.key_press("B", delay_time=1)
                    self.node_counter =0
                    return True
            elif not self.equip_position:  # 找出装备位置
                if "背包界面" in self.interface_info:
                    self.data_numpy = self.vnc_sync.capture_full_screen_as_numpy()  # 获取当前屏幕截图
                    # 创建图像差异查找器
                    finder = ImageComparer(self.eqiup_numpy, self.data_numpy)
                    # finder = ImageDifferenceFinder(self.eqiup_numpy, self.data_numpy)
                    # 找到不同的区域，最小面积为200
                    differences = finder.find_differences(*self.scope_背包)

                    self.current_color_block_list = self.find_color_black(*self.scope_背包)  # 计算当前背包空位
                    # 将列表转换为集合
                    set_a = set(self.last_color_block_list)  # 脱装备之前的空位
                    set_b = set(self.current_color_block_list)  # 当前背包空位
                    difference_ls = list(set_a - set_b)  # 装备的位置

                    logger.error(f"差异器计算结果:{differences}")
                    logger.error(f"前后色块对比结果:{difference_ls}")

                    self.node_counter = 0  # 重置节点计数器
                    # [(1026, 493, 28, 28, 637.0)]
                    if differences and difference_ls:  # 都存在的情况下
                        res_ls = self.find_close_elements(differences, difference_ls)
                        if res_ls:
                            self.equip_position = res_ls[0][0] + 15, res_ls[0][1] + 15
                            logger.error(f"装备位置可以信任,位置:{self.equip_position}")
                        else:
                            if len(difference_ls) == 1:
                                self.equip_position = difference_ls[0][0] + 15, difference_ls[0][
                                    1] + 15  # 已脱装备的位置计算为准
                                logger.error(f"装备位置计算失误信任,位置:{self.equip_position}")
                            elif len(differences) == 1:
                                self.equip_position = differences[0][0] + 15, differences[0][1] + 15  # 已脱装备的位置计算为准
                                logger.error(f"装备位置计算失误信任,位置:{self.equip_position}")
                            else:
                                self.err_num += 1
                    elif differences and not difference_ls:
                        self.equip_position = differences[0][0] + 15, differences[0][1] + 15

                    elif not differences and difference_ls:
                        self.equip_position = difference_ls[0][0] + 15, difference_ls[0][1] + 15

                    if not self.last_equip_position:
                        self.last_equip_position = self.equip_position
                    if self.last_equip_position:
                        if abs(self.equip_position[0] - self.last_equip_position[0]) > 30 or abs(
                                self.equip_position[1] - self.last_equip_position[1]) > 30:
                            self.equip_position = self.last_equip_position[0] - 15, self.equip_position[1]
                        self.last_equip_position = self.equip_position

                    else:
                        self.err_num += 1
                elif "主界面" in self.interface_info:
                    self.key_press("B", delay_time=1)
                    return True

        self.node_counter+=1 # 增加节点计数器


    def task_强化完成(self):
        if "主界面" in self.interface_info:
            self.ls_progress="task_finish"
            return "task_finish"
        else:
            self.interface_closes()

    def handle_task(self):
        task_methods = {
            "task_背包范围识别": self.task_背包范围识别,
            'task_武器强化部分查询': self.task_武器强化部分查询,
            'task_头盔强化部分查询': self.task_头盔强化部分查询,
            'task_衣服强化部分查询': self.task_衣服强化部分查询,
            'task_护手强化部分查询': self.task_护手强化部分查询,
            'task_腰带强化部分查询': self.task_腰带强化部分查询,
            'task_鞋子强化部分查询': self.task_鞋子强化部分查询,
            'task_装备强化': self.task_装备强化,
            'task_强化完成': self.task_强化完成,
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
        logger.error(f"背包范围:{self.scope_背包}")
        logger.error(f"装备信息状态:{self.node_info_flag}")
        logger.error(f"装备强化状态:{self.node_flag}")
        logger.error(f"准备状态:{self.ready_flag}")
        logger.error(f"脱装备前包裹空格:{self.last_color_block_list}")
        logger.error(f"脱装备后包裹空格:{self.current_color_block_list}")
        logger.error(f"装备点位:{self.equip_position}")


        if not self.node_current:
            self.task_背包范围识别()
        elif self.handle_task():
            pass

        self.queue_screenshot_sync(reset=False)  # 同步截图

#背包中识别的范围
equip_scope_背包=(419, 234, 1201, 772)
#装备位置,判断是否是紫色装备
equip_scope_details={
    "武器": (486, 281, 536, 315),
    "头盔": (467, 331, 512, 364),
    "衣服": (440, 379, 497, 413),
    "护手": (426, 426, 474, 460),
    "腰带": (425, 476, 471, 507),
    "鞋子": (438, 525, 500, 558),
}

equip_enhanced_data={
    "word": {
        "95%": {
            "scope": (565, 574, 842, 615),
            "con": 0.8,
            "model":1,
            "offset": (-55, 51),
            "use": "装备强化",
            "unique": True,
            "enable": True,
            'class': ["装备强化界面"],
        },
        "65%": {
            "scope": (565, 574, 842, 615),
            "con": 0.8,
            "model": 1,
            "offset": (-45, 61),
            "use": "装备强化",
            "unique": True,
            "enable": True,
            'class': ["装备强化界面"],
        },
        "欢迎光临":{
            "scope": (541, 194, 882, 253),
            "con": 0.8,
            "offset": (0, 0),
            "model": 1,
            "use": "装备强化",
            "enable":True,
            'class': ["装备强化界面"],
        },#每日签到

    },
    "image": {
        r"resource/images_info/equipment_strengthening/凤瞳.bmp":{
            "scope":equip_scope_背包,
            "con":0.8,
            "enable":True,
            "unique": True,
            "model":1,
            'class': ["背包界面"],
        },
        r"resource/images_info/equipment_strengthening/星级.bmp":{
            "scope":equip_scope_背包,
            "con":0.8,
            "enable":True,
            "unique": True,
            "model":1,
            'class': ["背包界面"],
        },
        r"resource/images_info/equipment_strengthening/破月.bmp":{
            "scope":equip_scope_背包,
            "con":0.8,
            "enable":True,
            "unique": True,
            "model":1,
            'class': ["背包界面"],
        },
        r"resource/images_info/equipment_strengthening/追星.bmp":{
            "scope":equip_scope_背包,
            "con":0.8,
            "enable":True,
            "unique": True,
            "model":1,
            'class': ["背包界面"],
        },
        r"resource/images_info/equipment_strengthening/龙睛.bmp":{
            "scope":equip_scope_背包,
            "con":0.8,
            "enable":True,
            "unique": True,
            "model":1,
            'class': ["背包界面"],
        },
        r"resource/images_info/equipment_strengthening/激战.png": {
            "scope": equip_scope_背包,
            "con": 0.8,
            "enable": True,
            "unique": True,
            "model": 1,
            'class': ["背包界面"],
        },
        r"resource/images_info/equipment_strengthening/整理.png": {
            "scope":(1103, 645, 1205, 736),
            "con": 0.8,
            "enable": True,
            "unique": True,
            "model": 1,
            'class': ["背包界面"],
        },
        r"resource/images_info/equipment_strengthening/强化图标.png": {
            "scope": equip_scope_背包,
            "con": 0.8,
            "enable": True,
            "unique": True,
            "model": 1,
            'class': ["背包界面"],
        },
        r"resource/images_info/other/背包空格.png": {
            "scope": equip_scope_背包,
            "con": 0.8,
            "enable": True,
            "unique": True,
            "model": 1,
            'class': ["背包界面"],
        },
    },
}