import random
from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块
from resource.parameters_info.basic_parameter_info import target_name_ls


class TaskSpur(TaskLogic):
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

    def task_任务接取(self):
        self.node_current="task_任务接取"

        if self.node_counter>=5 or self.node_flag:
            self.node_counter=0
            self.node_flag=False
            self.node_current="task_任务完成"

        elif "对话界面" in self.interface_info:
            self.node_current="task_任务中"

        elif "地图界面" in self.interface_info:
            logger.info("地图界面.选择任务领取人")
            self.find_map_npc(["焕成壕"], "任务")

        elif "主界面" in self.interface_info:
            self.key_press("M", delay_time=1)
            self.node_counter=0 # 重置计数器

        self.node_counter+=1

    def task_任务中(self):
        self.node_current="task_任务中"

        if self.node_counter>=5 or self.node_flag:
            self.node_counter=0
            self.node_flag=False
            self.node_current="task_任务完成"

        if "对话界面" in self.interface_info and self.find_data_from_keys_list_click(["焕夫人"],self.word_handle_data,delay_time=1):
            for i in range(5):
                self.mouse_left_click_scope(513, 546, 720, 568)
            self.key_press("ESC", delay_time=0.5)
            self.node_current="task_任务完成"

        res_dict = self.handle_dict_values(self.word_acquire_data, tag=30)
        if res_dict:
            logger.error(f"支线任务:{res_dict}")
            """
            {
            '新手任务】玲珑的故事_2_【新手任务】玲珑的故事_2': (1186, 323, 0.995, 30),
            '【新手任务】试炼场的试炼_4': (1186, 355, 0.998, 30),
            '【支线】绝望的商人': (1186, 387, 0.996, 30),
            '寻物：熊皮（0/2）': (1202, 402, 0.942, 30),
            '交付人：徐颖天_1': (1203, 306, 0.957, 30),
            '完成：玲珑副本（未完成）_3': (1203, 338, 0.984, 30),
            '完成：试炼场（未完成）': (1203, 370, 0.993, 30),
            '交付人：焕成壕': (1203, 419, 0.986, 30)
            }
            """
            target_name = self.target_info.get("name", "未知")
            logger.info(f"目标:{target_name}")
            # 检查是否有键包含 "野猪",在主线任务目标中
            if target_name in target_name_ls:
                num_iterations = random.randint(3, 8)  # 生成一个介于 3 和 6 之间的随机迭代次数
                for i in range(num_iterations):  # 循环，运行生成的迭代次数
                    logger.info(f"第 {i + 1} 次攻击")
                    self.key_press("1", delay_time=0.5)
            elif not self.role_running or self.map_differences:
                for key, value in res_dict.items():
                    if any(keyword in key for keyword in ["熊", "皮", "黑风军", "督卫头目", "裴虎"]) and any(
                            digit in key for digit in ["未", "0", "/1", "/2", "/10"]):
                        logger.error(f"支线任务目标{key}")
                        self.find_data_from_keys_list_click(["熊", "皮", "黑风军", "督卫头目", "裴虎"], res_dict,
                                                            delay_time=5, x3=15, y3=5, )
                        self.mouse_move_scope(1009, 334, 1164, 464)
                        self.key_press("1", delay_time=0.5)
                        self.interface_closes()
                        self.node_counter=0
                        return True
                    elif any(keyword in key for keyword in
                             ["熊", "皮", "黑风军", "督卫头目", "裴虎", "焕夫人", "夫人"]) and "完成" in key:
                        if self.find_data_from_keys_list_click(["焕成壕", "壕", "皮衣店", ], res_dict, x3=53, y3=7,
                                                               delay_time=5):
                            self.mouse_move_scope(1009, 334, 1164, 464)
                            self.interface_closes()
                            self.node_counter=0
                            return True
                        elif self.find_data_from_keys_list_click(["焕夫人", "夫人", ], res_dict, x3=53, y3=7,
                                                                 delay_time=5):
                            self.mouse_move_scope(1009, 334, 1164, 464)
                            self.interface_closes()
                            self.node_counter=0
                            return True


    def task_任务完成(self):
        self.node_current="task_任务完成"

        if self.node_counter>=5 or self.node_flag:
            self.node_counter=0
            self.node_flag=False
            self.ls_progress="task_finish"
        elif "主界面" in self.interface_info:
            self.node_flag=True
        else:
            self.interface_closes()

    def handle_task(self):
        task_methods = {
            'task_任务接取': self.task_任务接取,
            'task_任务中': self.task_任务中,
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

        for key, value in self.task_info.items():
            if any(keyword in key for keyword in ["20级", "熊", "皮", "黑风军", "督卫头目", "裴虎", "焕夫人"]):  # 焕成壕支线任务完
                self.task_任务中()

        if not self.node_current:
            self.task_任务接取()
        elif self.handle_task():
            pass

        self.queue_screenshot_sync(reset=False)


spur_data={
    "word": {
        30: {
            "scope": (1184, 244, 1408, 492), #支线任务识别范围
            "model": 1,
            "con": 0.8,
            "use": "task_info",
            "enable": True,
            "unique": True,
            "class":["主界面","对话界面","地图界面",]
        },
        "焕成壕": {
            "scope": (951, 308, 1111, 431),
            "con": 0.8,
            "offset": (23, 10),
            "use": "主线任务",
            "enable": True,
            "unique": True,
            'class': ["地图界面"],
        },
        "焕夫人": {
            "scope": (453, 345, 553, 382),
            "con": 0.8,
            "offset": (105, 211),
            "use": "主线任务",
            "enable": True,
            "unique": True,
            'class': ["对话界面"],
        },
    },
}