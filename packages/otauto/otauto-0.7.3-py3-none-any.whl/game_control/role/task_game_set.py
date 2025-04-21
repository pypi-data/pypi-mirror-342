import random
import time

from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块

class TaskGameSet(TaskLogic):
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
        self.queue_enable({"word":{4:"ban"}})

        self.node_set=set() #集合
        self.node_menu_flag = False # 设置节点完成标志为false
        self.node_flag = False # 设置节点完成标志为false
        self.set_flag= False   # 设置标志为false
        self.药箱_flag = False # 设置标志为false
        self.追星_flag = False
        self.龙睛_flag= False
        self.究极生命药水_flag = False
        self.九转混元丹_flag = False

    def extract_smallest_right_shortcut(self,dic: dict):
        """
        从给定的字典中提取右侧快捷栏的坐标，并返回编号最小的快捷栏的坐标。
        参数:
        ----------
        a : dict
            包含快捷栏信息的字典，键为快捷栏名称，值为一个包含坐标和其他信息的元组。
        返回:
        -------
        dict
            一个字典，包含编号最小的快捷栏的坐标，格式为 {编号: (x, y)}。
            如果没有找到，则返回空字典 {}。
        """
        smallest_key = None
        smallest_value = None
        if not dic:
            return {}

        # 从原字典中提取右侧快捷栏的坐标
        for key, value in dic.items():
            if "右" in key:
                # 提取快捷栏编号，假设编号在键名中
                for i in range(2, 9):  # 1到10的快捷栏
                    if str(i) in key:
                        if smallest_key is None or i < smallest_key:
                            smallest_key = i
                            smallest_value = value[:2]  # 只保留坐标(x, y)
                        break  # 找到后可以跳出循环

        # 如果找到最小的快捷栏，将其放入字典中返回
        if smallest_key is not None and smallest_value is not None:
            return {smallest_key: smallest_value}
        else:
            return {}  # 如果没有找到，返回空字典

    def handle_node(self, node_name, target_number, npc_conditions):
        """
        处理节点任务
        self.handle_node("功能", 26, (738, 203, 796, 229), ["爵位领取人", "悬赏令发布使"],"白屏寨")
        self.handle_node("任务", 19, (799, 202, 856, 231), ["西域商团青城山接引人"],"青城山")
        self.handle_node("活动", 24, (922, 203, 980, 229), ["唐军任务领取人", "义军任务领取人"],"白屏寨")
        :param node_name:  节点名称
        :param target_number:  目标数字
        :param npc_conditions:  NPC条件
        :return:
        """

        if not self.node_flag:
            pages_list = self.find_word_scope(743, 530, 862, 574)
            if pages_list:
                page_info = pages_list[0][0]
                actual_number = int(page_info.split('第')[1].split('/')[0])

                if actual_number < target_number:
                    self.queue_interval(int(target_number - actual_number-5))
                    logger.info(f"实际数字 {actual_number} 小于目标数字 {target_number}，点击右边。")
                    for _ in range(target_number - actual_number):
                        self.mouse_left_click(871, 553, delay_time=0.5)
                    return True

                elif actual_number > target_number:
                    self.queue_interval(int(target_number - actual_number-5))
                    logger.info(f"实际数字 {actual_number} 大于目标数字 {target_number}，点击左边。")
                    for _ in range(actual_number - target_number):
                        self.mouse_left_click(738, 553, delay_time=0.5)
                    return True

                elif actual_number == target_number:
                    logger.info(f"实际数字 {actual_number} 等于目标数字 {target_number}，无需点击。")
                    self.node_flag = True
                    time.sleep(2)
                    return True

        elif self.node_flag:
            for npc in npc_conditions:
                if "res" in npc: # 说明是图片信息
                    self.find_data_from_keys_list_click([npc],self.image_data,delay_time=1)
                else:
                    self.find_data_from_keys_list_click([npc],self.word_handle_data,delay_time=1)
                self.find_data_from_keys_list_click(["resource/images_info/other/加入收藏.png"],self.image_data,delay_time=1)
                self.node_set.add(node_name)
                self.node_flag = False  # 设置节点完成标志为false

    def task_快捷键取消(self):
        """取消右侧快捷栏的快捷键"""
        self.node_current = "task_快捷键取消"

        if self.node_counter>=5:
            if "主界面" in self.interface_info:
                self.node_current = "task_游戏设置"
                self.node_flag= False # 设置节点完成标志为false
                self.node_counter=0 # 重置节点计数器
                return "task_finish"
            else:
                self.interface_closes()

        elif self.find_data_from_keys_list(["按键设定"],self.word_handle_data):
            logger.info("按键设定")
            # 筛选出最后一个元素为 99 的键值对
            result_dict = self.handle_dict_values(self.word_acquire_data,tag=99)
            logger.error(f"result_dict:{result_dict}")
            """
            result_dict:{'打开/关闭角色界面': (586, 604, 0.989, 99), '打开/关闭技能面板': (586, 630, 0.99, 99),
            '快捷栏按键10': (603, 264, 0.999, 99), '快捷栏按键11': (603, 290, 0.998, 99),
            '快捷栏按键12': (603, 316, 0.999, 99), '右侧快捷栏10': (603, 577, 0.996, 99), 
            '右侧快捷栏7_右侧快捷栏': (604, 495, 0.99, 99), '右侧快捷栏1': (607, 343, 0.994, 99),
            '右侧快捷栏2': (607, 369, 0.997, 99), '右侧快捷栏3': (607, 395, 0.997, 99), 
            '右侧快捷栏4': (607, 421, 0.997, 99), '右侧快捷栏5': (607, 446, 0.998, 99), 
            '右侧快捷栏6': (607, 473, 0.997, 99), '右侧快捷栏8': (607, 525, 0.996, 99),
            '右侧快捷栏9': (607, 552, 0.997, 99)}
            """
            res_dict=self.extract_smallest_right_shortcut(result_dict)
            if res_dict: #{2: (607, 369)}
                h=25 #格子之间的高度
                self.queue_screen(False)
                for key, value in res_dict.items():
                    x1,y1=value[0]+137,value[1]-h*(key-1)+7
                    print(x1,y1)
                    for i in range(0,10):
                        self.mouse_left_click(x1+random.randint(1,100), y1+i*h, delay_time=1.2)
                        self.mouse_left_click_scope(645, 673, 702, 687,delay_time=1.2) #取消设定
                self.mouse_left_click_scope(729, 674, 789, 687,delay_time=2) #确定
                self.key_press("esc",delay_time=2)
                self.node_counter = 10
                self.queue_screen(True)
                return True

            elif not res_dict:
                try:
                    self.mouse_drag(877, 284, 882, 370,step=10)  # 拖动
                    time.sleep(1)
                    self.node_flag = True
                except Exception as e:
                    logger.error(f"任务快捷键取消:{e}")

        elif self.find_data_from_keys_list_click(["按键设置"],self.word_handle_data,delay_time=1):
            logger.info("进入按键设置")

        elif "主界面" in self.interface_info :
            self.key_press("esc")

        self.node_counter+=1 # 节点计数器加1

    def task_游戏设置(self):
        """游戏设置"""
        self.node_current = "task_游戏设置"

        if self.node_counter>=5:
            if "主界面" in self.interface_info:
                self.node_current = "task_基础技能"
                self.node_flag= False # 设置节点完成标志为false
                self.node_counter=0 # 重置节点计数器
                return "task_finish"
            else:
                self.interface_closes()
                return True

        elif self.node_flag:
            if not self.set_flag:
                if self.find_data_from_keys_list_click(["恢复默认"], self.word_handle_data, delay_time=1):
                    self.set_flag=True
            elif self.set_flag:
                self.queue_screen(False)
                self.mouse_left_click_scope(578, 269, 683, 280, delay_time=1) # 关闭聊天泡泡
                self.mouse_left_click_scope(581, 360, 652, 368, delay_time=1) # 隐藏头盔
                self.mouse_left_click_scope(582, 392, 652, 401, delay_time=1) # 隐藏披风
                self.mouse_left_click_scope(580, 448, 652, 459, delay_time=1) # 隐藏红包
                self.mouse_left_click_scope(579, 484, 693, 493, delay_time=1) # 隐藏召唤物名称
                self.mouse_left_click_scope(723, 299, 823, 309, delay_time=1) # 关闭系统提示
                self.mouse_left_click_scope(723, 418, 824, 431, delay_time=1) # 隐藏神兵特效
                self.mouse_left_click_scope(726, 450, 822, 461, delay_time=1) # 隐藏他人宠物
                self.mouse_left_click_scope(683, 548, 753, 563, delay_time=1) # 确定
                self.key_press("esc",delay_time=2) # 关闭系统菜单
                self.set_flag=False
                self.node_counter=10 # 设置的次数改为10
                self.queue_screen(True)
                return True

        elif not self.node_flag:
            if "主界面" in self.interface_info :
                self.queue_screen(False)
                self.key_press("esc",delay_time=1)
                self.mouse_left_click_scope(674, 396, 800, 411,delay_time=1) #按键设置
                self.mouse_left_click_scope(527, 240, 544, 282,delay_time=1) # 视频设置
                self.mouse_left_click_scope(815, 264, 880, 279,delay_time=1) # 最低画质
                self.mouse_left_click_scope(528, 391, 545, 429,delay_time=1) #功能
                self.node_flag = True  # 设置节点完成标志为true
                self.queue_screen(True)
                return True

        self.node_counter+=1 # 节点计数器加1

    def task_基础技能(self):
        """基础技能"""
        self.node_current = "task_基础技能"

        if self.node_counter>=5:
            if "主界面" in self.interface_info:
                self.node_counter=0
                self.node_current="task_元宝购买"
                time.sleep(5)
                return "task_finish"
            else:
                self.interface_closes()

        elif "主界面" in self.interface_info:
            try:
                self.queue_screen(False)
                self.mouse_drag(804, 844, 847, 769, 30) #移除回城
                time.sleep(2)
                self.mouse_drag(635,842,586,771,25) #移除骑马
                time.sleep(2)
                self.mouse_drag(595,843,601,776,25) #移除药品
                time.sleep(2)
                self.mouse_left_click(1111,79,delay_time=2) #点击活动界面
                self.mouse_left_click(537,327,delay_time=2) #领取银元宝
                self.mouse_left_click(1040,111,delay_time=2) #关闭界面
                self.node_counter=10 #触发节点转移
                self.queue_screen(True)
                return True
            except Exception as e:
                logger.error(e)
        else:
            self.interface_closes()

        self.node_counter+=1

    def task_元宝购买(self):
        self.node_current="task_元宝购买"

        if self.node_counter>=5:
            if "主界面" in self.interface_info:
                self.node_counter=0
                self.node_current="task_药品整理"
                time.sleep(5)
                return "task_finish"
            else:
                self.interface_closes()

        elif "商城界面" in self.interface_info:
            if self.追星_flag and self.龙睛_flag and self.药箱_flag:
                logger.error("购买完成")
                self.mouse_left_click(1134,152,delay_time=2)
                self.node_counter=10 #触发节点转移
                return True

            elif not self.药箱_flag:
                self.queue_screen(False)
                self.mouse_left_click(972, 207, delay_time=2)  # 银宝斋
                self.mouse_left_click(519, 256, delay_time=2)  # 战斗补给
                self.mouse_left_click(1029, 328, delay_time=2)  # 药箱
                for i in range(9):  # 购买10个
                    self.mouse_left_click(994, 368, delay_time=0.5)
                self.mouse_left_click(1101, 367, delay_time=2)  # 购买
                self.mouse_left_click(663, 461, delay_time=1)  # 确定
                self.药箱_flag=True
                self.queue_screen(True)
                return True

            elif not self.追星_flag:
                self.queue_screen(False)
                self.mouse_left_click(337,257,delay_time=2) #强化宝石
                self.mouse_left_click(409,327,delay_time=2) # 追星
                for i in range(1): #购买2个
                    self.mouse_left_click(381,368,delay_time=0.5) # 购买2个
                self.mouse_left_click(484,367,delay_time=1) #购买
                self.mouse_left_click(648,458,delay_time=1) # 确定
                self.追星_flag=True
                self.queue_screen(True)
                return True
            elif not self.龙睛_flag :
                self.queue_screen(False)
                self.mouse_left_click(359,255,delay_time=2) #强化宝石
                self.mouse_left_click(628,322,delay_time=2) # 龙睛
                for i in range(14): #购买15个
                    self.mouse_left_click(583,367,delay_time=0.5) # 购买15个
                self.mouse_left_click(692,368,delay_time=1) #购买
                self.mouse_left_click(670,460,delay_time=1) # 确定
                self.龙睛_flag=True
                self.queue_screen(True)
                return True

        elif "主界面" in self.interface_info:
            self.mouse_left_click(1222,74,delay_time=2) #打开商城
            return True
        else:
            self.interface_closes()

        self.node_counter+=1


    def task_药品整理(self):
        self.node_current = "task_药品整理"

        if self.node_counter>=5:
            if "主界面" in self.interface_info:
                self.node_counter=0
                time.sleep(5)
                self.node_current="task_角色退出"
                return "task_finish"
            else:
                self.interface_closes()

        elif self.九转混元丹_flag and self.究极生命药水_flag:
            self.node_counter = 10  # 触发节点转移
            return True

        elif "背包界面" in self.interface_info:
            try:
                if not self.九转混元丹_flag:
                    res_dict=self.find_data_from_keys_list(["resource/images_info/other/九转混元丹.png"],self.image_data)
                    #{'resource/images_info/main_task/活动.bmp': {'scope': [(1152, 62, 1171, 81, 1.0)], 'model': 1, 'enable': True, 'unique': True}}
                    if res_dict:
                        scope_dict=res_dict.get("resource/images_info/other/九转混元丹.png")
                        scope_list=scope_dict.get("scope")
                        point=(scope_list[0][0]+14,scope_list[0][1]+12)
                        self.mouse_drag(*point, 637, 845, 30)  # 拖动,快捷键-
                        time.sleep(2)
                        self.mouse_right_click_scope(856, 568, 972, 652) # 移除
                        time.sleep(2)
                        self.九转混元丹_flag=True
                        self.node_counter =0
                        return True

                elif not self.究极生命药水_flag:
                    res_dict=self.find_data_from_keys_list(["resource/images_info/other/究极生命药水.png"],self.image_data)
                    #{'resource/images_info/main_task/活动.bmp': {'scope': [(1152, 62, 1171, 81, 1.0)], 'model': 1, 'enable': True, 'unique': True}}
                    if res_dict:
                        scope_dict=res_dict.get("resource/images_info/other/究极生命药水.png")
                        scope_list=scope_dict.get("scope")
                        point=(scope_list[0][0]+14,scope_list[0][1]+12)
                        self.mouse_drag(*point, 592, 843, 30)  # 拖动,快捷键=
                        time.sleep(2)
                        self.mouse_right_click_scope(856, 568, 972, 652) # 移除
                        time.sleep(2)
                        self.究极生命药水_flag=True
                        self.node_counter =0
                        return True

                point = None
                res_dict=self.find_data_from_keys_list(["resource/images_info/other/药箱.png"],self.image_data)
                #{'resource/images_info/main_task/活动.bmp': {'scope': [(1152, 62, 1171, 81, 1.0)], 'model': 1, 'enable': True, 'unique': True}}
                if res_dict:
                    scope_dict=res_dict.get("resource/images_info/other/药箱.png")
                    scope_list=scope_dict.get("scope")
                    point=(scope_list[0][0]+14,scope_list[0][1]+12)
                if point:
                    self.queue_screen(False)
                    for i in range(10): # 取出药品
                        self.mouse_right_click(*point,delay_time=7)
                    self.mouse_left_click(1158,688,delay_time=1) #整理背包
                    self.node_counter = 0
                    self.queue_screen(True)
                    return True
            except Exception as e:
                logger.error(e)

        elif "主界面" in self.interface_info:
            self.key_press("B",delay_time=2)
            return True

        self.node_counter+=1

    def task_角色退出(self):
        self.node_current = "task_角色退出"

        if self.node_counter>=5:
            self.node_counter=0
            time.sleep(5)
            self.ls_progress="task_finish"
            return "task_finish"

        elif self.find_data_from_keys_list(["返回"],self.word_handle_data):
            self.node_counter=10 #触发节点转移
            return True

        elif "主界面" in self.interface_info:
            self.queue_screen(False)
            self.key_press("esc",delay_time=2) # 菜单栏
            self.mouse_left_click(740,376,delay_time=2) # 角色退出
            self.mouse_left_click(665,458,delay_time=15) # 确定
            self.queue_screen(True)
            return True
        else:
            self.interface_closes()

        self.node_counter+=1

    def handle_task(self):
        task_methods = {
            "task_快捷键取消":self.task_快捷键取消,
            'task_游戏设置': self.task_游戏设置,
            "task_基础技能": self.task_基础技能,
            "task_元宝购买": self.task_元宝购买,
            "task_药品整理": self.task_药品整理,
            "task_角色退出": self.task_角色退出,
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

        if not self.node_current:
            self.task_快捷键取消()
        elif self.handle_task():
            pass

        self.queue_screenshot_sync(reset=False)

game_set_data={
    "word": {
        99: {
            "scope": (556, 260, 732, 659),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "model":1,
            "unique": True,
            "enable": True,
        },
        98: {
            "scope": (551, 231, 891, 502),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        97: {
            "scope": (671, 197, 985, 237),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "按键设置": {
            "scope": (671, 447, 804, 477),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
            'class': ["系统菜单界面"],
        },
        "游戏设置": {
            "scope": (672, 388, 807, 410),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "按键设定": {
            "scope": (668, 173, 779, 204),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "最低画质": {
            "scope": (800, 249, 889, 286),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "功": {
            "scope": (521, 384, 555, 433),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "取消设定": {
            "scope": (634, 658, 715, 691),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "确定": {
            "scope": (718, 656, 798, 693),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "恢复默认": {
            "scope": (544, 535, 639, 568),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "确": {
            "scope": (671, 536, 770, 571),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "定": {
            "scope": (674, 439, 739, 465),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "综": {
            "scope": (405, 539, 435, 620),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "返回": {
            "scope": (602, 721, 845, 819),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
            'class': ["系统菜单界面"],
        },
    },
    "image": {
        r"resource/images_info/camp_task/地图_npc.bmp":{
            "scope":(1088,563,1153,618),
            "con":0.8,
            "model":1,
            "enable":True,
            "unique": True,
            'class': ["地图界面"],
        },#奖励图标
        r"resource/images_info/other/快速搜索_关闭.png": {
            "scope": (1025, 110, 1168, 212),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["地图界面"]
        },  # 奖励图标
        r"resource/images_info/role_skill/回城.bmp": {
            "scope": (775, 803, 835, 855),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"]
        },  # 奖励图标
        r"resource/images_info/role_skill/普通攻击.png": {
            "scope": (462, 229, 782, 299),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"]
        },  # 奖励图标

        r"resource/images_info/other/药箱.png": {
            "scope": (634, 415, 1179, 569),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["背包界面"]
        },  # 奖励图标
        r"resource/images_info/other/九转混元丹.png": {
            "scope": (635, 415, 1173, 565),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["背包界面"]
        },  # 奖励图标
        r"resource/images_info/other/究极生命药水.png": {
            "scope": (635, 415, 1173, 565),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["背包界面"]
        },  # 奖励图标

    },
    "mutil_colors": {
        "按键设置_滚动条": {"colors": {
            "7c8192": (878, 351),
            "7a8091": (878, 358),
            "767d8e": (878, 371),
        },
        "scope": (865, 265, 887, 630),
        "tolerance": 25},
    }
}