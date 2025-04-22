from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块

class TaskDetails(TaskLogic):
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

    def task_01(self):
        self.node_current = "task_01"

        if not self.role_running or not self.map_differences:
            if self.node_counter >= 5 or self.node_flag:
                if "主界面" in self.interface_info:
                    self.node_counter = 0
                    self.node_flag = False # 重置
                    self.color_flag = False  # 重置
                    self.node_current= "task_02"
                    self.ls_progress="task_finish"
                    return "task_finish"
                else:
                    self.interface_closes()

            elif not self.node_flag:
                if self.find_data_from_keys_list(["resource/images_info/other/队伍.png"],self.image_data): # todo
                    self.node_flag=True
                    return True

                elif "地图界面" in self.interface_info:
                    if self.find_map_npc(["长寿宫"], "副本"):
                        self.node_counter = 0  # 重置

                elif "主界面" in self.interface_info:
                    self.key_press("m", delay_time=1)

                else:  # 其他界面,关闭
                    self.interface_closes()

        self.node_counter += 1  # 节点计数器
    def task_02(self):
        pass
    def task_03(self):
        pass
    def handle_task(self):
        task_methods = {
            'task_01': self.task_01,
            'task_02': self.task_02,
            'task_03': self.task_03,
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
            pass
        elif self.handle_task():
            pass


name_change_data={
    "word": {
        "需要金钱": {
            "scope": (374, 503, 470, 545),
            "con": 0.8,
            "offset": (0, 0),
            "use": "包裹清理",
            "model": 1,
            "unique": True,
            "enable": True,
        },
    },
    "image": {
        r"resource/images_info/other/中原.png": {
            "scope": (665, 232, 778, 292),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
        },
    },
}