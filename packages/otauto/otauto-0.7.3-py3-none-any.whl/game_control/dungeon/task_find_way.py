import numpy as np
from PIL import Image

from otauto.a_star_v2 import PathFinder
from otauto.coordinate_converter import CoordinateConverter
from otauto.image_traits import ImageTraits
from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块
from resource.parameters_info.basic_parameter_info import  dungeons_exit_dict, city_name,dungeons_node_dict



class TaskFindWay(TaskLogic):
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
        self.goal_list=dungeons_node_dict[f"{self.dungeons_name}"] # 节点列表
        self.target_colors_hex =self.ini_dungeons_dict["target_colors_hex"].split(",")   # 允许通行的颜色
        self.route_color = self.ini_dungeons_dict["route_color"].split(",")  # 惩罚值最低的颜色
        image2 = Image.open(self.map_path) # 读取图像
        self.image2_array = np.array(image2) # 将PIL图像转换为NumPy数组
        self.path_finder = PathFinder() # 创建一个PathFinder对象
        self.imagetraits = ImageTraits()  # 只使用 SIFT
        self.converter = CoordinateConverter(self.map_path) # 创建一个CoordinateConverter对象
        self.node_flag=False # 节点标识
        self.moving_flag=False # 移动标识
        self.exit_list=dungeons_exit_dict # 副本出口列表
        self.goal = (-1, -1) # 当前目标点
        self.goal_finish_list=[] # 已完成的节点列表
        self.target_point = None #目标点,和识别出来的起点最接近的节点
        self.goal_list_subscript=0 # 节点列表的下标
        self.boss_counter = 0 # boss计数器,避免未识别出来直接退出


    def moving(self):
        """
         移动模块
         :node_list :节点列表
        """
        logger.error("测试模块")
        endpoint_point=self.exit_list[f"{self.dungeons_name}"]
        logger.error(f"副本名称:{self.dungeons_name}")
        logger.error(f"节点信息:{self.goal_list}")
        logger.error(f"终点信息:{endpoint_point}")
        logger.error(f"已完成的节点:{self.goal_finish_list}")
        logger.error(f"锁定次数:{self.attack_range_num}")

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

            logger.error(f"当前位置:{start},目标位置:{self.goal}")

            # # 3根据坐标值进行路径规划
            # # 检查 x 和 y 坐标的差是否都小于等于 2, 并且目标点不在已完成节点列表中
            # if abs(start[0] - self.goal[0]) <= 2 and abs(start[1] - self.goal[1]) <= 2 :
            #     # 满足条件的代码块
            #     logger.success(f"当前位置:{start}在终点附近,切换成下一个节点")
            #     self.goal_finish_list.append(self.goal)  # 添加到已完成节点列表
            #     # 判断是否到了最后一个节点
            #     if len(self.target_point) == 1:
            #         logger.error("到了最后一个节点,任务完成")
            #         self.moving_flag = True
            #     else:
            #         self.goal_list_subscript = 1
            # else:
            #     # 4 进行路径规划,A星算法
            #     res_list = self.path_finder.find_path(self.map_path, start, self.goal, self.target_colors_hex,
            #                                           self.route_color)
            #     """
            #     [(80, 335), (80, 334), (80, 333), (81, 333), (82, 333), (83, 333), (84, 333), (85, 333), (86, 333), (87, 333),
            #     (88, 333), (88, 332), (89, 332), (89, 331), (90, 331), (90, 330), (91, 330), (91, 329), (91, 328), (92, 328),
            #     (93, 328), (93, 327), (94, 327)]
            #     """
            #     logger.error(f"A星算法规划结果:{res_list}")
            #     # 输出结果
            #     if res_list:
            #         # 每隔2个取1个
            #         filtered_list = res_list[::3]
            #         converted_points = self.converter.process_points(filtered_list)
            #         logger.error(f"转换后的场景点击坐标列表：{converted_points}")

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
        self.moving()

