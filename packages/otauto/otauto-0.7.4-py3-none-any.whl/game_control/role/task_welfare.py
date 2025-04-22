from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块

"""
功能:福利领取
日期:2025-2-17 23:23:56
描述:
    
"""


class TaskWelfare(TaskLogic):
    """
    任务详情:这里接入任务的具体操作内容
    def task_details(self),所有操作接入这个函数中
    vnc: vnc对象
    vnc_port: vnc端口号
    queue_handle: 队列操作对象
    """
    def __init__(self,vnc,vnc_port,queue_handle):
        super().__init__(vnc,vnc_port,queue_handle)

    def task_打开福利中心(self):
        """
        1,对话界面点击对话
        2,完成条件,该节点完成
        :return:
        """
        self.node_current="task_打开福利中心"

        if self.node_counter >= 5:
            self.interface_closes()
            self.node_counter = 0
            self.node_current = "task_领取完成"
            return "task_finish"

        elif "奖励界面" in self.interface_info:
            self.node_current = "task_每日签到"
            return "task_finish"

        elif "主界面" in self.interface_info:
            self.mouse_left_click_scope(1102, 67, 1115, 85)

        self.node_counter+=1

    def task_每日签到(self):
        self.node_current = "task_每日签到"

        if "每日签到" in self.node_list or self.node_counter>=5:#说明已领取
            self.node_current = "task_成长奖励"
            self.node_counter=0 #操作次数清零
            if not self.find_data_from_keys_list_click(["resource/images_info/other/奖励中心.png"], self.image_data):
                self.mouse_left_click(588,168,delay_time=1)
            return "task_finish"

        elif "奖励界面" in self.interface_info :
            condition_2= self.find_data_from_keys_list(['resource/images_info/other/每日签到完成.bmp'],self.image_data)
            logger.info(f"每日签到界面:{condition_2}")
            """
            {'resource/images_info/other/每日签到完成.bmp': {'scope': [(602, 307, 619, 320, 0.998), 
                                                                    (542, 307, 559, 320, 0.987), 
                                                                    (662, 307, 679, 320, 0.977)], 
                                                            'model': 1, 
                                                            'enable': True,
                                                            }
            }
            """
            if condition_2:
                value_dict=condition_2.get('resource/images_info/other/每日签到完成.bmp',{})
                scope_list=value_dict.get('scope',[])
                if scope_list:
                    # 使用 max 函数和 lambda 表达式找到 [0] 最大的元素
                    max_element = max(scope_list, key=lambda x: x[0]) #找出x坐标值最大的元素
                    logger.debug(f"max_element:{max_element}")
                    if max_element[0]<900: #说明不是最后一列,点击后一格的位置
                        self.mouse_double_left_click(max_element[0]+54,max_element[1]+19,delay_time=1)
                        self.node_list.append("每日签到")

        elif "主界面" in self.interface_info:
            self.node_current = "task_打开福利中心"
            self.node_counter = 0 #操作次数清零
            return "task_finish"
        else:
            self.interface_closes()

        self.node_counter += 1  # 操作次数+1,防止死循环

    def task_成长奖励(self):
        self.node_current = "task_成长奖励"

        if "成长奖励" in self.node_list or self.node_counter >= 10:
            self.node_current = "task_领取完成"
            self.node_counter = 0
            return "task_finish"

        elif "奖励界面" in self.interface_info:
            res_dict = self.find_word_from_acquire_num(30)  # 获取文字信息
            # logger.debug(f"成长奖励:{res_dict}")
            """
            {'25级': (643, 262, 1.0, 30), '已领取': (912, 262, 0.999, 30), '30级': (643, 315, 1.0, 30), 
            '立即领取': (898, 313, 0.999, 30), '业': (768, 324, 0.07, 30), '35级': (642, 367, 1.0, 30),
            '?': (811, 368, 0.038, 30), '待领取': (912, 370, 0.996, 30), '不': (768, 377, 0.049, 30),}
            """
            if self.find_data_from_keys_list_click(["使用后"],self.word_handle_data,delay_time=1):
                logger.info("取消丹药使用")

            if "成长奖励" not in self.node_list:
                if not self.find_data_from_keys_list_click(["成长奖励"], self.word_handle_data):
                    self.mouse_left_click(509,255,delay_time=1)
                self.mouse_left_click(945,384,delay_time=1)
                self.mouse_left_click(936,330,delay_time=1)
                self.mouse_left_click(948,272,delay_time=1)

            if res_dict:
                for key, value in res_dict.items():
                    if "立即" in key:
                        self.mouse_left_click(value[0], value[1], delay_time=1)
                    if "已领取" in key:
                        self.node_list.append("成长奖励")

        elif "主界面" in self.interface_info:
            self.node_current = "task_打开福利中心"
            self.node_counter = 0 #操作次数清零
            return "task_finish"
        else:
            self.interface_closes()

        self.node_counter += 1  # 节点计数器+1

    def task_领取完成(self):
        self.node_current = "task_领取完成"

        if "主界面" in self.interface_info:
            self.node_counter = 0 #操作次数清零
            self.ls_progress="task_finish"
            return "task_finish"
        else:
            self.interface_closes()

        self.node_counter += 1  # 操作次数+1,防止死循环


    def handle_task(self):
        task_methods = {
            "task_打开福利中心": self.task_打开福利中心,
            "task_每日签到": self.task_每日签到,
            "task_成长奖励": self.task_成长奖励,
            "task_领取完成": self.task_领取完成,
        }
        if self.node_current in task_methods:
            task_methods[self.node_current]()

    def task_details(self):
        """
        self.ls_progress=None # 进度信息:task_finish,task_fail,task_error,task_wait,task_get,task_running
        self.node_current=None #当前节点
        self.node_list= []  # 节点列表
        self.node_counter = 0 # 节点计数器
        self.queue_message({"word": {11: {"enable": False}}}) # 参数关闭
        函数写入这里
        """
        logger.success(f"任务详情:{self.__class__.__name__}")
        logger.success(f"节点信息:{self.node_current}")

        if self.target_info["name"] not in ["none","福利中心"]:
            logger.success("取消选择NPC")
            self.key_press("ESC",delay_time=1)

        if self.find_data_from_keys_list_click(["使用后"],self.word_handle_data,delay_time=1):
            logger.info("使用后")

        if not self.node_current:
            self.task_打开福利中心()
        elif self.handle_task():
            pass

        self.queue_screenshot_sync(reset=False)


task_welfare_data={
    "word": {
        30: {
            "scope": (608, 225, 1006, 691),
            "con": 0.8,
            "offset": (0, 0),
            "use": "成长奖励",
            "enable": True,
            'class': ["奖励界面"],
        },  # 每日签到
        "高级特权":{
            "scope": (580,485,739,539),
            "con": 0.8,
            "offset": (0, 0),
            "use": "每日签到",
            "enable":True,
            'class': ["奖励界面"],
        },#每日签到

        "成长奖励": {
            "scope": (436, 224, 590, 399),
            "con": 0.8,
            "offset": (43, 7),
            "use": "成长奖励",
            "enable": True,
            'class': ["奖励界面"],
        },  # 成长奖励

        "少侠": {
            "scope": (506,368,566,407),
            "con": 0.8,
            "offset": (181,73),
            "use": "每日签到",
            "enable": True,
            'class': ["奖励界面"],
        },  # 少侠
        "使用后": {
            "scope": (456, 365, 677, 416),
            "con": 0.8,
            "offset": (199, 73),
            "use": "每日签到",
            "enable": True,
            'class': ["奖励界面"],
        },  # 少侠
    },
    "image": {
        #"resource/images_info/camp_task/义军图腾.bmp": {'scope':(649, 817, 691, 872), 'con': 0.8,"ues":"义军图腾","enable":True}
        r"resource/images_info/other/奖励图标.bmp":{
            "scope":(1036, 41, 1254, 112),
            "con":0.8,
            "enable":True,
            'class': ["奖励界面"],
        },#奖励图标
        r"resource/images_info/other/每日签到完成.bmp":{
            "scope":(487, 277, 958, 489),
            "model":1,
            "con":0.8,
            "enable":True,
            'class': ["奖励界面"],
        },#每日签到完成
        r"resource/images_info/other/奖励中心.png": {
            "scope": (575, 146, 605, 178),
            "model": 0,
            "con": 0.8,
            "enable": True,
            'class': ["奖励界面"],
        },  # 每日签到完成
    },
}