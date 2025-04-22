from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块

from resource.parameters_info.basic_parameter_info import reward_name, city_name


class TaskReward(TaskLogic):
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
        self.queue_enable({"word":{4:True}}) #开启任务识别
        self.task_fail_num = 0 # 任务失败次数
        self.task_counter=0 #任务计数器

    def task_寻找悬赏令发布使(self):
        self.node_current="task_寻找悬赏令发布使"

        if not self.role_running or not self.map_differences:
            if self.map_name not in ["白屏寨"]:
                self.find_data_from_keys_list_click(["悬赏任务"], self.task_info, delay_time=30)
            else:
                if "发布使界面" in self.interface_info:
                    logger.info("悬赏令发布使界面表示该节点已完成")
                    self.node_current = "task_购买悬赏令"
                    self.node_flag=False
                    return "task_finish"

                elif "地图界面" in self.interface_info:
                    logger.info("地图界面.选择任务领取人")
                    self.find_map_npc(["悬赏令发布使"],"功能")


                elif "主界面" in self.interface_info:
                    self.key_press("M")

    def task_购买悬赏令(self):
        """
        1点击购买悬赏令
        2选择悬赏令数目1,右键
        3关闭购买界面
        4背包界面有悬赏令,购买完成
        :return:
        """
        self.node_current = "task_购买悬赏令"

        if "背包界面" in self.interface_info and self.node_flag:
            logger.info("4背包界面有悬赏令,购买完成")
            if self.mutil_colors_data and "悬赏令(绿)" in self.mutil_colors_data or self.find_data_from_keys_list(["resource/images_info/reward_task/背包_悬赏令.bmp"],self.image_data):
                self.node_current="task_领取悬赏任务"
                return "task_finish"

        elif "发布使界面" in self.interface_info and not self.node_flag:
            if self.find_data_from_keys_list_click(["购买"], self.word_handle_data):
                logger.info("点击购买")

        elif "杂货界面" in  self.interface_info:
            if self.find_data_from_keys_list_click(["resource/images_info/reward_task/悬赏令_数目1.bmp"],self.image_data,delay_time=2,action=3):
                self.mouse_left_click_scope(874, 182, 890, 195)
                self.node_flag=True
            elif self.find_data_from_keys_list_click(["悬赏"],self.word_handle_data,delay_time=2,action=3):
                self.mouse_left_click_scope(874, 182, 890, 195)
                self.node_flag=True

        elif "主界面" in self.interface_info:
            self.node_current="task_寻找悬赏令发布使"

    def task_领取悬赏任务(self):
        """
        1 点击悬赏令,右键
        2 点击悬赏任务,右键
        3 确定领取
        4任务界面出现"疑犯","悬赏"等关键字,领取完成
        :return:
        """
        self.node_current = "task_领取悬赏任务"

        if self.find_data_from_keys_list_click(["你确认使用"], self.word_handle_data, delay_time=2):
            if self.find_data_from_keys_list(["只能接受"], self.word_handle_data):  # 说明任务次数已经使用完毕
                logger.info("任务次数已经使用完毕")
                self.node_current = "task_交付任务"
                return True

        elif "背包界面" in self.interface_info or self.find_data_from_keys_list(["币"],self.word_handle_data):
            if self.find_data_from_keys_list(["疑犯(0/1)"], self.word_acquire_data) or self.find_data_from_keys_list(['打倒:疑犯(0/1)'], self.mutil_colors_data):
                logger.debug("任务领取完成")
                self.interface_closes()
                self.node_current = "task_寻找疑犯"
                return "task_finish"

            elif self.find_data_from_keys_list_click(["resource/images_info/reward_task/悬赏任务_绿色.bmp"], self.image_data, delay_time=2,action=3):
                self.mouse_move(832, 450, 1)  # 鼠标移开位置

            elif self.find_data_from_keys_list_click(["悬赏令(绿)"], self.mutil_colors_data,  delay_time=2,action=3):
                pass

        elif "主界面" in self.interface_info:
            self.key_press("B",delay_time=1)

    def task_寻找疑犯(self):
        """
        1,点击疑犯
        2,自动寻路中
        3,在疑犯附近查找疑犯
        4,进入副本
        :return:
        """
        self.node_current = "task_寻找疑犯"

        if self.find_data_from_keys_list_click(["贼人"], self.word_handle_data, delay_time=10):
            logger.info("找到疑犯,准备进入副本")
            self.node_current= "task_副本操作"
            return "task_finish"

        elif "背包界面" in self.interface_info:
            self.interface_closes()

        elif "主界面" in self.interface_info and not self.role_running:
            if self.find_data_from_keys_list_click(["【删除任务】"],self.word_acquire_data):
                logger.info("删除任务,任务失败")
                self.node_current = "task_寻找悬赏令发布使"
                self.task_counter+=1 #任务失败计数

            elif self.find_data_from_keys_list_click(["疑犯"],self.word_handle_data,x3=17,y3=122,delay_time=2):#坐标未变化
                logger.info("找到疑犯")

            elif  self.find_data_from_keys_list_click(["疑犯(0/1)"], self.word_acquire_data,x3=50,y3=5,delay_time=2):#坐标未变化
                self.mouse_move_scope(950, 262, 1112, 485)
                logger.info("找疑犯中")

            elif self.find_data_from_keys_list_click(["打倒:疑犯(0/1)"], self.mutil_colors_data,x3=50,y3=5,delay_time=2):#坐标未变化
                self.mouse_move_scope(950, 262, 1112, 485)
                logger.info("找疑犯中")

    def task_副本操作(self):
        """
        1进入副本
        2触发技能攻击
        3抓取犯人
        4离开副本
        :return:
        """
        self.node_current = "task_副本操作"

        if self.map_name in reward_name:
            logger.error("副本操作中")
            self.ls_progress={"map_name":f"{self.map_name}"}
            return "task_wait"

    def task_交付任务(self):
        """
        1,点击交付
        :return:
        """
        self.node_current = "task_交付任务"
        self.ls_progress="task_finish"

        if "主界面" in self.interface_info:
            if self.find_data_from_all_keys_list(["点击交付","疑犯(已完成)"], self.word_acquire_data):
                return "task_finish"
        else:
            self.interface_closes()


    def handle_task(self):
        task_methods = {
            'task_寻找悬赏令发布使': self.task_寻找悬赏令发布使,
            'task_购买悬赏令': self.task_购买悬赏令,
            'task_领取悬赏任务': self.task_领取悬赏任务,
            'task_寻找疑犯': self.task_寻找疑犯,
            'task_副本操作': self.task_副本操作,
            'task_交付任务': self.task_交付任务
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
        if self.find_data_from_keys_list_click(["悬赏副本销毁","销毁"],self.word_handle_data) and self.map_name in city_name:
            logger.error("悬赏副本销毁")

        elif self.find_data_from_keys_list_click(["点击交付"],self.task_info,delay_time=2):
            pass

        elif self.find_data_from_keys_list(["疑犯（已完成）","悬赏任务（完成）"],self.task_info) and self.map_name in city_name:
           self.task_交付任务()

        elif self.find_data_from_keys_list_click(["删除任务","删除","失败"],self.word_acquire_data,delay_time=2)   and self.map_name in city_name:
            logger.error("删除任务")
            self.task_寻找悬赏令发布使()
            self.task_counter += 1

        elif self.map_name in reward_name:
            self.task_副本操作()

        elif self.find_data_from_keys_list(["打倒:疑犯(0/1)"],self.mutil_colors_data) and not self.node_current:
            self.task_寻找疑犯()

        elif not self.node_current:
            self.task_寻找悬赏令发布使()
        elif self.handle_task():
            pass

        self.queue_screenshot_sync(reset=False)  # 同步截图


#任务资源
scope_背包悬赏令=(638,412,1173,560)
reward_data={
    "word": {
        "悬赏副本销毁": {
            "scope": (458, 370, 573, 418),
            "con": 0.8,
            "offset": (230, 65),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "悬赏令发布使": {
            "scope": (948, 310, 1100, 549),
            "con": 0.8,
            "offset": (0, 0),
            "use": "悬赏任务",
            "unique": True,
            "enable": True,
            "class": "快捷搜索界面"
        },  # 悬赏任务
        "开启了阵营":{
            "scope": (462,344,625,368),
            "con": 0.8,
            "offset": (242,131),
            "use": "悬赏任务",
            "enable":True,
        },#悬赏任务
        "可以提升": {
            "scope": (466,375,647,405),
            "con": 0.8,
            "offset": (232,73),
            "use": "悬赏任务",
            "unique": True,
            "enable": True,
        },  # 悬赏任务
        "你确认使用":{
            "scope": (510,366,800,401),
            "con": 0.8,
            "offset": (143,73),
            "use": "悬赏任务",
            "enable":True,
            'class': ["背包界面"],

        },#悬赏任务
        "贼人": {
            "scope": (564,587,852,615),
            "con": 0.8,
            "offset": (52, 10),
            "use": "悬赏任务",
            "unique": True,
            "enable": True,
        },  # 悬赏任务
        "币":{
            "scope": (964,567,1048,643),
            "con": 0.8,
            "offset": (0, 0),
            "use": "悬赏任务",
            "enable":True,
        },#悬赏任务
        "悬赏": {
            "scope": (587,254,652,279),
            "con": 0.8,
            "offset": (-29,18),
            "use": "悬赏任务",
            "unique": True,
            "enable": True,
            'class': ["杂货界面"],
        },  # 悬赏任务
        "购买":{
            "scope": (556, 504, 689, 527),
            "con": 0.8,
            "offset": (0, 0),
            "use": "悬赏任务",
            "enable":True,
            'class': ["发布使界面"],
        },#悬赏任务
        "疑犯": {
            "scope": (270,120,1056,592),
            "con": 0.8,
            "offset": (0, 0),
            "use": "悬赏任务",
            "unique": True,
            "enable": True,
        },  # 悬赏任务
        "只能接受":{
            "scope": (598, 168, 845, 205),
            "con": 0.8,
            "offset": (0, 0),
            "use": "悬赏任务",
            "enable":True,
        },#悬赏任务
    },
    "image": {
        r"resource/images_info/other/快速搜索_关闭.png": {
            "scope": (1025, 110, 1168, 212),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["地图界面"],
        },  # 奖励图标
        r"resource/images_info/camp_task/地图_npc.bmp":{
            "scope":(1088,563,1153,618),
            "con":0.8,
            "enable":True,
            "unique": True,
            'class': ["地图界面"],
        },#奖励图标
        r"resource/images_info/reward_task/悬赏令_数目1.bmp":{
            "scope":(546,252,610,302),
            "con":0.8,
            "enable":True,
            "unique": True,
            'class': ["杂货界面"],
        },#奖励图标
        r"resource/images_info/reward_task/悬赏任务_绿色.bmp":{
            "scope":scope_背包悬赏令,
            "con":0.8,
            "enable":True,
            "unique": True,
            'class': ["背包界面"],
        },#奖励图标
        r"resource/images_info/reward_task/悬赏任务_蓝色.bmp":{
            "scope":scope_背包悬赏令,
            "con":0.8,
            "enable":True,
            "unique": True,
            'class': ["背包界面"],
        },#奖励图标
        r"resource/images_info/reward_task/背包_悬赏令.bmp":{
            "scope":scope_背包悬赏令,
            "con":0.8,
            "enable":True,
            "unique": True,
            'class': ["背包界面"],


        },#奖励图标

    },
    "mutil_colors": {
        "【悬赏】": {
            "colors": {
                "dcad5c": (1188, 484),
                "987840": (1202, 485),
                "876b39": (1221, 492),
                "edbb63": (1233, 486),
                "fec86a": (1231, 496),
            },
            "scope": (1177, 251, 1395, 552),
            "tolerance": 25
        },
        "打倒:疑犯(0/1)": {
            "colors": {
                "1b9595": (1250, 517),
                "2ae8e8": (1259, 523),
                "2df9f9": (1267, 520),
                "1ea6a6": (1277, 525),
                "ae0f0b": (1293, 521),
                "cd110d": (1305, 526),
            },
            "scope": (1177, 251, 1395, 552),
            "tolerance": 30
        },
        "悬赏令(绿)": {
            "colors": {
                "cf3a38": (1071, 467),
                "cdceda": (1061, 477),
                "2b0c22": (1086, 455),
            },
            "scope": scope_背包悬赏令,
            "tolerance": 25
        },
        "悬赏任务(未完成)": {
            "colors": {
                "2ae8e8": (1255, 282),
                "27d8d8": (1270, 286),
                "2df9f9": (1303, 284),
                "ed140f": (1324, 282),
            },
                "scope": (1200, 276, 1372, 304),
                "tolerance": 20
        },
        "交付人:王捕快": {
            "colors": {
                "ff8800": (1267, 298),
                "ee7f00": (1287, 301),
                "cc6d00": (1306, 298),
            },
            "scope": (1259, 289, 1311, 308),
            "tolerance": 20
        },
    }
}



