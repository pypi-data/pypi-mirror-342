import time

from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块

from resource.parameters_info.basic_parameter_info import target_name_ls


class TaskPet(TaskLogic):
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
        self.node_flag = False

    def task_刷怪(self):
        logger.info("刷怪")
        self.node_counter=0 #节点计数器初始化
        self.task_skill_attack() #刷怪

    def task_武将信息采集(self):
        self.node_current = "task_武将信息采集"
        if self.node_counter>=5: #节点计数器大于等于5时,任务失败
            self.node_current = "task_任务完成"
            self.node_counter=0 #节点计数器归零

        self.node_counter +=1 #节点计数器加1

        if "武将界面" in self.interface_info:
            if self.find_data_from_keys_list(["雇佣剑客"], self.word_handle_data):
                self.node_current="task_任务完成" #任务完成
                return True
            else:
                self.node_current="task_寻找西域商团青城山接引人"
                self.interface_closes()
                return True

        elif  "主界面" in self.interface_info:
            self.key_press("P", delay_time=1)

    def task_寻找西域商团青城山接引人(self):
        """
        点击收藏选项,提前把西域商团青城山接引人加入收藏,人工设置
        :return:
        """
        self.node_current = "task_寻找西域商团青城山接引人"

        if self.node_flag:
            if self.map_name and "青城山" in self.map_name:  # 说明在青城山
                if self.find_data_from_keys_list_click(["西域商团"], self.word_handle_data, delay_time=1):
                    self.node_current = "task_挂机点"
                    self.node_flag = False  # 节点标志位重置
                    return "task_finish"

                if self.map_position:
                    # 用逗号分割字符串
                    parts = self.map_position.split(',')
                    # 将分割后的字符串转换为整数
                    res_list = [int(part) for part in parts]
                    # (189,81)
                    if ((268 < res_list[0] < 275 and 45 < res_list[1] < 60) or
                            (self.target_info and "西域商团青城山" in str(self.target_info.get('name', '')))):
                        # 满足条件时执行的代码
                        self.node_current = "task_挂机点"
                        self.node_flag = False  # 节点标志位重置
                        return "task_finish"

        elif "地图界面" in self.interface_info:
            if not self.node_flag:
                logger.info("地图界面.选择西域商团青城山接引人")
                if self.find_data_from_keys_list(["自动寻路"], self.word_handle_data):
                    if self.find_data_from_keys_list_click(["收藏"], self.word_handle_data, delay_time=1):
                        self.find_data_from_keys_list_click(["西域商团青城山接引人"], self.word_handle_data, delay_time=1)
                        if self.find_data_from_keys_list_click(["寻路"], self.word_handle_data, delay_time=1):
                            self.node_flag=True 
                elif self.find_data_from_keys_list_click(["快捷搜索"], self.word_handle_data, delay_time=1):
                    pass
                elif self.find_data_from_keys_list_click(["resource/images_info/camp_task/地图_npc.bmp"], self.image_data, delay_time=1):
                    pass
            elif self.node_flag:
                self.interface_closes()

        elif "主界面" in self.interface_info :
            if not self.node_flag:
                self.key_press("M")


    def task_挂机点(self):
        coor_list=["resource/images_info/other/雇佣剑客地点_1.bmp","resource/images_info/other/雇佣剑客地点_2.bmp",
                   "resource/images_info/other/雇佣剑客地点_3.bmp","resource/images_info/other/雇佣剑客地点_4.bmp"]#地图上的坐标

        if self.role_running: #移动中
            self.interface_closes()
            time.sleep(3)

        elif self.node_counter>=10:#节点计数器大于等于8,重新开始
            self.node_current = "task_寻找西域商团青城山接引人"
            self.node_counter=0 #节点计数器重置
            self.node_flag = False  # 节点标志位重置
            return "task_finish"

        elif self.target_info['name'] in target_name_ls:
            self.node_current="task_挂机中"
            self.node_counter = 0  # 节点计数器重置
            self.node_flag = False  # 节点标志位重置
            return "task_finish"

        elif "地图界面" in self.interface_info:
            if self.find_data_from_keys_list_click(coor_list, self.image_data, action=3,delay_time=20,random_pro=True):
                self.node_current = "task_挂机中"
                self.node_counter = 0  # 节点计数器重置
                self.node_flag = False  # 节点标志位重置
                self.interface_closes() #关闭地图界面
                return "task_finish"

        elif "主界面" in self.interface_info:
            self.key_press("M",delay_time=1)

        self.node_counter += 1  # 节点计数器加1

    def task_挂机中(self):
        self.node_current = "task_挂机中"

        logger.info(f"计数器:{self.node_counter}")

        if self.node_counter>=10:#说明没有找到目标
            if self.map_name in ["青城山"]:
                self.node_current = "task_挂机点"
                self.node_counter = 0  # 节点计数器重置
                return "task_finish"
            else:
                self.node_current = "task_寻找西域商团青城山接引人"
                self.node_counter = 0  # 节点计数器重置
                return "task_finish"

        if not self.node_flag:
            if self.target_info['name'] in ["雇佣剑客", "佣剑"]:
                logger.error("目标锁定")
                self.node_flag = True
                return True
            elif self.task_刷怪():
                pass
            else:
                res_bool = self.task_target_hunting()
                if res_bool:
                    self.node_counter = 0
                elif not res_bool:
                    self.node_counter += 1  # 节点计数器加1

        elif self.node_flag:
            logger.error("判断是否白名怪")
            self.node_flag = False
            if self.find_data_from_keys_list_click(["resource/images_info/main_task/收服标志.bmp"], self.image_data,
                                                    x3=20, y3=20, delay_time=15):
                logger.warning("找到白名怪,收服中")
                self.node_current = "task_武将查询"
                return "task_finish"

            elif self.task_刷怪():
                pass



    def task_武将查询(self):
        self.node_current = "task_武将查询"
        if "武将界面" in self.interface_info:
            if self.find_data_from_keys_list(["雇佣剑客"],self.word_handle_data):#判断是否是雇佣剑客
                self.find_data_from_keys_list_click(["息"],self.word_handle_data,delay_time=35) #点击休息
                if self.find_data_from_keys_list_click(["雇佣剑客"],self.word_handle_data,delay_time=2) :#点击雇佣剑客
                    self.find_data_from_keys_list_click(["唤"],self.word_handle_data,delay_time=2) #点击召唤
                self.node_current="task_任务完成"
                return "task_finish"
            else:
                self.interface_closes()
                self.task_挂机中()

        elif "主界面" in self.interface_info:
            self.key_press("P",delay_time=1)
        else:
            self.interface_closes()

    def task_任务完成(self):
        if "主界面" in self.interface_info:
            self.ls_progress = "task_finish"
            self.node_current = "task_任务完成"
            return True
        else:
            self.interface_closes()

    def handle_task(self):
        task_methods = {
            "task_武将信息采集":self.task_武将信息采集,
            'task_寻找西域商团青城山接引人': self.task_寻找西域商团青城山接引人,
            'task_挂机点': self.task_挂机点,
            'task_挂机中': self.task_挂机中,
            'task_武将查询': self.task_武将查询,
            'task_任务完成': self.task_任务完成,
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

        if "大唐风流界面" in self.interface_info:
            self.interface_closes()

        if self.diff_time<-1: #根据实际情况调整
            logger.error("数据不可信")
            return False

        if not self.node_current:
            self.task_武将信息采集()
        elif self.handle_task():
            pass


scope=(278,152,1157,704)
pet_data={
    "word": {
        "雇佣剑客": {
            "scope": (960, 574, 1125, 699),
            "con": 0.8,
            "offset": (34, 5),
            "use": "pet",
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },  # 每日签到
        "西域商团": {
            "scope": (628, 175, 809, 211),
            "con": 0.8,
            "offset": (252, 4),
            "use": "成长奖励",
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },  # 每日签到
        "西域商团青城山接引人": {
            "scope": (582, 262, 783, 535),
            "con": 0.8,
            "offset": (0, 0),
            "use": "成长奖励",
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },  # 每日签到
        "自动寻路": {
            "scope": (734, 162, 858, 187),
            "con": 0.8,
            "offset": (0, 0),
            "use": "成长奖励",
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },  # 每日签到
        "快捷搜索": {
            "scope": (989, 558, 1090, 597),
            "con": 0.8,
            "offset": (0,0),
            "use": "成长奖励",
            "enable": True,
            "unique": True,
            'class': ["地图界面"],
        },  # 每日签到
        "收藏": {
            "scope": (552, 205, 619, 240),
            "con": 0.8,
            "offset": (0, 0),
            "use": "成长奖励",
            "enable": True,
            "unique": True,
        },  # 每日签到
        "寻路": {
            "scope": (568, 535, 669, 571),
            "con": 0.8,
            "offset": (0,0),
            "use": "成长奖励",
            "enable": True,
            "unique": True,
        },  # 每日签到
        "召": {
            "scope": (752,605,896,631),
            "con": 0.8,
            "offset": (0,0),
            "use": "成长奖励",
            "enable": True,
            "unique": True,
        },  # 每日签到
        "息": {
            "scope": (752,605,896,631),
            "con": 0.8,
            "offset": (0,0),
            "use": "成长奖励",
            "enable": True,
            "unique": True,
        },  # 每日签到
    },
    "image": {
        r"resource/images_info/main_task/收服标志.bmp": {
            "scope": (684, 475, 757, 540),
            "offset": (0, 0),
            "con": 0.8,
            "enable": True,
            "model":1,
            "unique": True,  # 模块特有的
        },
        r"resource/images_info/camp_task/地图_npc.bmp":{
            "scope":(1088,563,1153,618),
            "offset":(37,10),
            "con":0.8,
            "enable": True,
            "unique":True, #模块特有的
        },#奖励图标
        r"resource/images_info/other/雇佣剑客地点_1.bmp": {
            "scope": scope,
            "con": 0.8,
            "enable": True,
            "unique": True,  # 模块特有的
        },  # 奖励图标
        r"resource/images_info/other/雇佣剑客地点_2.bmp": {
            "scope": scope,
            "con": 0.8,
            "enable": True,
            "unique": True,  # 模块特有的
        },  # 奖励图标
        r"resource/images_info/other/雇佣剑客地点_3.bmp": {
            "scope": scope,
            "con": 0.8,
            "enable": True,
            "unique": True,  # 模块特有的
        },  # 奖励图标
        r"resource/images_info/other/雇佣剑客地点_4.bmp": {
            "scope": scope,
            "con": 0.8,
            "enable": True,
            "unique": True,  # 模块特有的
        },  # 奖励图标
    },
}

