import time

import numpy as np
from PIL import Image

from otauto.a_star_v1 import PathFinder
from otauto.coordinate_converter import CoordinateConverter
from otauto.image_traits import ImageTraits
from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块
from resource.parameters_info.basic_parameter_info import  dungeons_exit_dict, city_name,dungeons_node_dict


class TaskRewardDungeons(TaskLogic):
    """
    任务详情:这里接入任务的具体操作内容
    def task_details(self),所有操作接入这个函数中
    vnc: vnc对象
    vnc_port: vnc端口号
    queue_handle: 队列操作对象
    task_welfare
    """
    def __init__(self,vnc,vnc_port,queue_handle,dungeons_name):
        super().__init__(vnc,vnc_port,queue_handle)
        self.node_flag = False #节点标识符
        self.moving_flag = False #移动模块标识符
        self.coordinate_node= None #节点坐标
        self.dungeons_name= dungeons_name # 副本名称
        self.ini_dungeons_dict = self.ini_handler.get_section_items(self.dungeons_name)  # 获取ini数据
        self.map_path= self.ini_dungeons_dict["map_path"] # 地图路径
        self.color_path= self.ini_dungeons_dict["color_path"] # 颜色路径
        self.goal_list=dungeons_node_dict[f"{self.dungeons_name}"] # 节点列表
        self.target_colors_hex =self.ini_dungeons_dict["target_colors_hex"].split(",")   # 允许通行的颜色
        self.route_color = self.ini_dungeons_dict["route_color"].split(",")  # 惩罚值最低的颜色
        image2 = Image.open(self.map_path) # 读取图像
        self.image2_array = np.array(image2) # 将PIL图像转换为NumPy数组
        self.path_finder = PathFinder() # 创建一个PathFinder对象
        self.imagetraits = ImageTraits()  # 只使用 SIFT
        self.converter = CoordinateConverter(self.map_path) # 创建一个CoordinateConverter对象
        self.node_flag=False # 节点标识
        self.exit_list=dungeons_exit_dict # 副本出口列表
        self.goal = (-1, -1) # 当前目标点
        self.goal_finish_list=[] # 已完成的节点列表
        self.target_point = None #目标点,和识别出来的起点最接近的节点
        self.goal_list_subscript=0 # 节点列表的下标
        self.boss_counter = 0 # boss计数器,避免未识别出来直接退出
        self.point_list= [] # 节点坐标列表
        self.task_finish_flag= False # 任务完成标识符
        self.deaths_num = 0 # 死亡计数器
        self.last_general_time = 0 # 武将存在的时间

        self.npc_name_list = ['resource/images_info/reward_task/通缉犯.bmp', "resource/images_info/reward_task/霸山虎.bmp",
                         "resource/images_info/reward_task/异族细作.bmp", "resource/images_info/reward_task/血路独行.bmp",
                         "resource/images_info/reward_task/七窍玲珑.bmp", "resource/images_info/reward_task/不赦死囚.bmp"]


    def task_刷怪(self):
        logger.error("刷怪中")
        self.node_counter=0 #节点计数器初始化
        self.task_skill_attack() #刷怪
        self.key_press("~",delay_time=0.2)

    def leave_dungeon(self):

        if self.find_data_from_keys_list_click(["resource/images_info/main_task/任务对话.png"],self.image_data,delay_time=10):
            logger.info("退出副本")
            return True

        elif self.find_data_from_keys_list_click(["离开"], self.word_handle_data, delay_time=10):
            logger.info("退出副本")
            return True

        elif self.task_finish_flag : #说明任务已经完成,退出副本
            if "地图界面" in self.interface_info:
                res_dict = self.find_data_from_keys_list(["resource/images_info/reward_task/出口箭头_荒野.png"], self.image_data)
                if res_dict:
                    # {'resource/images_info/reward_task/通缉犯.bmp': {'scope': [(875, 455, 915, 466, 0.986)], 'offset': (24, 135), 'model': 1, 'enable': True, 'unique': True}}
                    logger.error(f"{res_dict}")
                    for key, value in res_dict.items():
                        x1, y1, x2, y2 = value["scope"][0][0], value["scope"][0][1], value["scope"][0][2],value["scope"][0][3]
                        x_median = (x1 + x2) // 2
                        y_median = (y1 + y2) // 2
                        point = x_median + value["offset"][0], y_median + value["offset"][1]
                        logger.error(f"任务目标点位:{point}")
                        self.mouse_move(point[0], point[1], delay_time=1)
                        self.mouse_right_click(point[0], point[1], delay_time=8)
                        logger.error("出口箭头_荒野,点击移动")
                        self.key_press("M", delay_time=2)
                        time.sleep(20)
                        return True

                elif self.find_data_from_keys_list_click(["出口"], self.word_handle_data, action=3, delay_time=2):
                    logger.error("找到出口,点击移动")
                    self.key_press("M", delay_time=2) #关闭地图界面
                    time.sleep(20)
                    return True
            elif "主界面" in self.interface_info:
                if not self.role_running: #说明角色没有移动,移动
                    logger.error("角色移动中,退出副本")
                    self.moving(dungeons_exit_dict[f"{self.dungeons_name}"])  # 移动
                    return True

        elif not self.task_finish_flag:
            if self.deaths_num>=5: #死亡次数大于5,退出副本
                self.task_finish_flag = True
                self.key_press("M",delay_time=2)
                return True

            elif self.find_data_from_keys_list_click(["确定","捕获成功"],self.word_handle_data,delay_time=3):
                logger.error("捕获成功,退出副本")
                self.task_finish_flag=True
                self.key_press("M",delay_time=2) #打开地图界面
                return True

            elif self.find_data_from_all_keys_list(["悬赏任务","点击交付"],self.word_acquire_data):
                self.task_finish_flag=True
                self.key_press("M",delay_time=2) #打开地图界面
                return True

            elif self.boss_counter>=3: # boss计数器大于5,退出副本 (373, 74)
                logger.error("已经完成,退出副本")
                self.task_finish_flag = True
                self.key_press("M", delay_time=2)  # 打开地图界面
                return True

    def finish_dungeon(self):
        if self.map_name in city_name:
            logger.error("到了城池,退出副本")
            self.ls_progress = "task_finish"  # 模块运行结束
            return True

    def moving(self,node_list:list):
        """
         移动模块
         :node_list :节点列表
        """
        if len(self.point_list)>=4:
            logger.error("人物未移动,点击小地图")
            if len(set(self.point_list))==1: #说明坐标为改变
                if self.mutil_colors_data !={}:
                    for key, value_data in self.mutil_colors_data.items():
                        if key in ["目标体_地图红点"]:
                            res_tuple = self.find_closest_point(value_data["scope"], self.role_map_position)
                            logger.error(f"{res_tuple}")
                            self.mouse_right_click(*res_tuple, delay_time=3)
                            self.point_list = []  # 重置坐标列表
                            return True
                elif self.mutil_colors_data == {}:
                    logger.warning("寻路失败,点击小地图")
                    self.mouse_right_click(1367, 107,delay_time=2)  # 盲点击小地图
                    self.point_list = []  # 重置坐标列表
                    return True
            self.point_list = []  # 重置坐标列表
            return True

        self.goal_list=node_list # 节点列表
        # 1应用特征比对方式获取坐标
        x1, y1, x2, y2 = 1258, 75, 1415, 225  # image1的裁剪区域,不能更改
        image1_cropped = self.data_numpy[y1:y2, x1:x2]  # 裁剪
        imagetraits = ImageTraits()  # 只使用 SIFT
        traits_dict = imagetraits.draw_matches(image1_cropped, self.image2_array)  # 绘制匹配结果
        logger.error(f"当前位置:{traits_dict}")
        # 任务位置: {'num_inliers': 24, 'matches': 24, 'con': 1.0, 'role_position': (80, 334)}

        # 2根据起点和终点进行路径规划
        # 设置图像路径、起点、终点、目标颜色和路线颜色
        if traits_dict is not None and traits_dict["role_position"] != (-1, -1):
            start = traits_dict["role_position"]
            # goal = (94, 327)
            self.target_point = self.find_closest_and_remaining(self.goal_list, traits_dict["role_position"])
            try:
                self.goal = self.target_point[self.goal_list_subscript]
            except Exception as e:
                logger.error(f"{e}")
                self.goal = self.target_point[0]
                if len(list(set(self.goal_finish_list))) < len(self.goal_list): # 已完成的列表少于节点列表,说明还有节点没有完成
                    set_diff=set(self.goal_list).difference(set(self.goal_finish_list))
                    self.goal=list(set_diff)[0]

            logger.error(f"当前位置:{start},目标位置:{self.goal}")

            # 3根据坐标值进行路径规划
            # 检查 x 和 y 坐标的差是否都小于等于 3, 并且目标点不在已完成节点列表中
            if abs(start[0] - self.goal[0]) <= 3 and abs(start[1] - self.goal[1]) <= 3 :
                # 满足条件的代码块
                logger.success(f"当前位置:{start}在终点附近,切换成下一个节点")
                self.goal_finish_list.append(self.goal)  # 添加到已完成节点列表
                # 判断是否到了最后一个节点
                if len(list(set(self.goal_finish_list))) ==len(self.goal_list):
                    logger.error("所有的节点已经探寻")
                    self.moving_flag = True
                else:
                    self.goal_list_subscript = 1
            else:
                if self.goal in self.goal_finish_list:
                    logger.error("目标点已经完成,切换下一个节点")
                    self.goal_list_subscript += 1
                    try:
                        self.goal=self.target_point[self.goal_list_subscript] # 切换下一个节点
                    except Exception as e:
                        logger.error(f"{e}")
                        if len(list(set(self.goal_finish_list))) < len(self.goal_list):  # 已完成的列表少于节点列表,说明还有节点没有完成
                            set_diff = set(self.goal_list).difference(set(self.goal_finish_list))
                            self.goal = list(set_diff)[0]

                if self.task_加血值判断():
                    self.key_press("0",delay_time=0.5) # 角色加血
                # 4 进行路径规划,A星算法
                res_list = self.path_finder.find_path(self.color_path, start, self.goal, self.target_colors_hex,
                                                      self.route_color)
                """
                [(80, 335), (80, 334), (80, 333), (81, 333), (82, 333), (83, 333), (84, 333), (85, 333), (86, 333), (87, 333),
                (88, 333), (88, 332), (89, 332), (89, 331), (90, 331), (90, 330), (91, 330), (91, 329), (91, 328), (92, 328),
                (93, 328), (93, 327), (94, 327)]
                """
                logger.error(f"A星算法规划结果:{res_list}")
                # 输出结果
                self.point_list.append(self.map_position)
                if res_list:
                    # 每隔2个取1个
                    filtered_list = res_list[::3]
                    converted_points = self.converter.process_points(filtered_list)
                    logger.error(f"转换后的场景点击坐标列表：{converted_points}")
                    # [(810, 405), (720, 315), (855, 450), (855, 450), (810, 405), (810, 405), (765, 360), (810, 405)]
                    if converted_points:
                        time_queue=len(converted_points)*0.4 #识别线程停顿时间
                        self. queue_message({"interval": round(time_queue+0.5, 2)}) # 发送识别线程停顿时间
                        for point in converted_points:
                            self.mouse_right_click(point[0], point[1], delay_time=0.4)
                        self.node_counter = 0  # 重置计数器
                        self.goal_list_subscript = 0  # 重置节点索引值
                        logger.error("已到达节点")  # todo:接上刷挂操作
                        self.key_press("tab",delay_time=0.2)  # 切换到目标
                        self.key_press("1",delay_time=0.2)  # 攻击
                        # self.moving_flag = True # 移动标识
                        return True

    def task_on_hook(self):
        """
        挂机模块
        """
        logger.error("挂机模块")
        endpoint_point=self.exit_list[f"{self.dungeons_name}"]
        logger.error(f"副本名称:{self.dungeons_name}")
        logger.error(f"节点信息:{self.goal_list}")
        logger.error(f"终点信息:{endpoint_point}")
        logger.error(f"已完成的节点:{self.goal_finish_list}")
        logger.error(f"位置记录:{self.point_list}")
        logger.error(f"锁定次数:{self.attack_range_num}")
        logger.error(f"死亡次数:{self.deaths_num}")
        logger.error(f"武将存在时间:{self.last_general_time}")

        if (-1,-1) in self.goal_list:
            logger.error("放弃该任务,直接退出副本")
            self.task_finish_flag=True

        if self.find_data_from_keys_list_click(["复活点"],self.word_handle_data,delay_time=5,action=2):
            logger.error("角色死亡")
            self.key_press("0",delay_time=3)
            self.goal_finish_list=[]
            self.deaths_num+=1
            return True

        if self.find_data_from_keys_list(["resource/images_info/other/武将_守护.png"], self.image_data) : # 武将存在
            self.last_general_time = int(time.time()) # 记录时间

        if int(time.time()) - self.last_general_time > 300:  # 武将间隔召唤时间为5分钟
            logger.error("武将消失,重新刷")
            self.key_press("P", delay_time=1)
            self.mouse_left_click(824, 631, delay_time=1)
            self.key_press("P", delay_time=1)
            self.last_general_time = int(time.time()) # 记录时间
            return True

        res_dict=self.find_data_from_keys_list(self.npc_name_list,self.image_data)
        if res_dict:
            #{'resource/images_info/reward_task/通缉犯.bmp': {'scope': [(875, 455, 915, 466, 0.986)], 'offset': (24, 135), 'model': 1, 'enable': True, 'unique': True}}
            logger.error(f"{res_dict}")
            for key,value in res_dict.items():
                x1,y1,x2,y2=value["scope"][0][0],value["scope"][0][1],value["scope"][0][2],value["scope"][0][3]
                x_median=(x1+x2)//2
                y_median=(y1+y2)//2
                point=x_median+value["offset"][0],y_median+value["offset"][1]
                logger.error(f"任务目标点位:{point}")
                self.mouse_move(point[0],point[1],delay_time=1)
                self.mouse_left_click(point[0],point[1],delay_time=8)
                return True

        if self.finish_dungeon(): # 完成副本
            return True

        if self.leave_dungeon(): # 退出副本
            return True

        if not self.task_finish_flag:
            if not self.node_flag:
                if self.target_info['lock']:
                    self.task_刷怪()
                    self.node_counter = 0  # 节点计数器初始化
                    self.attack_range_num = 0 # 锁定次数初始化
                    return True

                elif not self.target_info['lock'] and  not self.target_info["attack_range"]: # 没有目标在攻击范围内,移动到目标节点
                    self.moving(self.goal_list)
                    self.key_press("tab")  # 切换到目标
                    self.attack_range_num = 0 # 锁定次数初始化
                    return True

                elif self.attack_range_num>3 and not self.target_info["attack_range"]: #没有目标在攻击范围内,移动到目标节点
                    self.moving(self.goal_list)
                    self.attack_range_num = 0 # 锁定次数初始化
                    return True

                elif self.attack_range_num<=3 and self.target_info["attack_range"]:# 目标在攻击范围内,锁定目标次数少于3
                    self.key_press("tab")  # 切换到目标
                    self.node_counter = 0  # 节点计数器初始化
                    self.attack_range_num+=1 # 锁定次数加1
                    return True

                elif self.target_info["driftlessness"]:
                    self.moving(self.goal_list) # 移动
                    return True

            if self.node_counter>=10:
                logger.warning("寻路失败,点击小地图")
                self.mouse_right_click(1367, 112) #盲点击小地图
                return True

            elif self.node_counter>=5: #todo:说明a星寻路失败,启动节点寻路的方式
                if not self.target_info["driftlessness"] and not self.target_info["attack_range"]:  # 目标不在攻击范围内
                    if self.mutil_colors_data:
                        for key, value_data in self.mutil_colors_data.items():
                            if key in ["目标体_地图红点"]:
                                res_tuple = self.find_closest_point(value_data["scope"], self.role_map_position)
                                self.mouse_left_click(*res_tuple, delay_time=10)
                                return True
                elif self.target_info["driftlessness"]:
                    logger.error("无红点,特殊处理")

            if self.moving_flag and self.target_info["driftlessness"]: # todo:
                logger.error("到了终点附近,退去副本")
                self.boss_counter += 1  # 遇到boss次数

            # if not self.moving_flag and self.goal_list: # 移动标识为False且节点列表不为空
            #     logger.error("移动模块")
            #     self.moving(self.goal_list) # 移动

        self.node_counter += 1

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

        self.task_on_hook()

target_scope=(371, 136, 973, 696)
reward_dungeons_data={
    "word": {
        "出口": {
            "scope": (332, 193, 1117, 674),
            "con": 0.8,
            "offset": (0,0),
            "use": "悬赏任务",
            "model":1,
            "unique": True,
            "enable": True,
        },
        "捕获成功": {
            "scope": (507,367,597,404),
            "con": 0.8,
            "offset": (185,74),
            "use": "悬赏任务",
            "unique": True,
            "enable": True,
        },
        "确定":{
            "scope": (647, 428, 760, 485),
            "con": 0.8,
            "offset": (26, 10),
            "use": "悬赏任务",
            "unique": True,
            "enable": True,
        },
        "离开": {
            "scope": (558,587,633,618),
            "con": 0.8,
            "offset": (0, 0),
            "use": "悬赏任务",
            "enable": True,
        },
        "物品": {
            "scope": (698,439,782,462),
            "con": 0.8,
            "offset": (20, 10),
            "use": "悬赏任务",
            "unique": True,
            "enable": True,
        },
        "奖励": {
            "scope": (698,439,782,462),
            "con": 0.8,
            "offset": (0, 0),
            "use": "悬赏任务",
            "enable": True,
        },
    },
    "image": {
        "resource/images_info/reward_task/出口箭头_荒野.png": {
            "scope": (435, 444, 683, 614),
            "con": 0.8,
            "offset": (16, 123),
            "model": 1,
            "enable": True,
            "unique": True,
        },  # 奖励图标
        "resource/images_info/reward_task/通缉犯.bmp":{
            "scope":target_scope,
            "con":0.8,
            "offset":(16, 123),
            "model":1,
            "enable":True,
            "unique": True,
        },#奖励图标
        "resource/images_info/reward_task/霸山虎.bmp": {
            "scope": target_scope,
            "con": 0.8,
            "offset": (18, 157),
            "model": 1,
            "enable": True,
            "unique": True,
        },  # 奖励图标
        "resource/images_info/reward_task/异族细作.bmp": {
            "scope": target_scope,
            "con": 0.8,
            "offset": (41, 145),
            "model": 1,
            "enable": True,
            "unique": True,
        },  # 奖励图标
        "resource/images_info/reward_task/血路独行.bmp": {
            "scope": target_scope,
            "con": 0.8,
            "offset": (18, 138),
            "model": 1,
            "enable": True,
            "unique": True,
        },  # 奖励图标
        "resource/images_info/reward_task/七窍玲珑.png": {
            "scope": target_scope,
            "con": 0.8,
            "offset": (22, 176),
            "model": 1,
            "enable": True,
            "unique": True,
        },  # 奖励图标
        "resource/images_info/reward_task/不赦死囚.bmp": {
            "scope": target_scope,
            "con": 0.8,
            "offset": (22, 176),
            "model": 1,
            "enable": True,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/other/武将_守护.png": {
            "scope": (529, 766, 618, 823),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/main_task/任务对话.png": {
            "scope": (547, 579, 657, 635),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
        },
    },
}

