import math

import numpy as np
from PIL import Image

# from otauto.a_star_v1 import PathFinder # 参考路线的版本
from otauto.a_star_v2 import PathFinder # 参考路线的版本
from otauto.coordinate_converter import CoordinateConverter
from otauto.image_traits import ImageTraits
from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块



class TaskAstar(TaskLogic):
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

        self.map_path= "resource/images_info/map_image/tld_color_2.png" # 地图路径
        self.target_colors_hex = ["6ec8fa", "70c8fa"]  # 允许通行的颜色
        self.route_color = ["e02a35",]  # 惩罚值最低的颜色
        self.penalty_color_hex = "00ff7f"  # 惩罚颜色
        image2 = Image.open(self.map_path) # 读取图像
        self.image2_array = np.array(image2) # 将PIL图像转换为NumPy数组
        self.path_finder = PathFinder() # 创建一个PathFinder对象
        self.converter = CoordinateConverter(self.map_path) # 创建一个CoordinateConverter对象
        self.node_flag=False # 节点标识
        self.moving_flag=False # 移动标识
        self.goal_list=node_list # todo:节点列表
        self.goal_finish_list=[] # 已完成的节点列表
        self.goal=(-1,-1)
        self.target_point = None #目标点,和识别出来的起点最接近的节点
        self.goal_list_subscript=0 # 节点列表的下标

    def find_closest_and_remaining(self,node_list, point):
        """
        找到与给定点最近的点，并返回该点及其后面的所有元素。

        :param node_list: 包含节点坐标的列表
        :param point: 参考点，格式为 (x, y)
        :return: 包含最近点及其后面元素的列表
        """

        def euclidean_distance(p1, p2):
            """计算两个点之间的欧几里得距离。"""
            return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        # 初始化最小距离和最近的点索引
        min_distance = float('inf')
        closest_index = -1

        # 遍历节点列表，计算每个点到给定点的距离
        for index, node in enumerate(node_list):
            distance = euclidean_distance(node, point)
            if distance < min_distance:
                min_distance = distance
                closest_index = index

        # 使用切片保留最近的点及其后面的所有元素
        return node_list[closest_index:]

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

        if self.node_counter >=15: # todo:人工处理
            logger.error("寻路失败,点击小地图")
            pass

        #todo: 角色死亡怎么处理

        if self.node_counter>=8: #todo:说明a星寻路失败,启用点击小地图的方式
            logger.warning("寻路失败,点击小地图")
            pass

        if self.node_counter>=5: #todo:说明a星寻路失败,启动节点寻路的方式
            logger.warning("A星寻路失败,启动节点寻路的方式")
            pass

        if not self.moving_flag and self.goal_list: # 移动标识为False且节点列表不为空
            #1应用特征比对方式获取坐标
            x1, y1, x2, y2 = 1258, 75, 1415, 225  # image1的裁剪区域,不能更改
            image1_cropped = self.data_numpy[y1:y2, x1:x2]  # 裁剪
            imagetraits = ImageTraits()  # 只使用 SIFT
            traits_dict=imagetraits.draw_matches(image1_cropped, self.image2_array)  # 绘制匹配结果
            logger.error(f"当前位置:{traits_dict}")
            #任务位置: {'num_inliers': 24, 'matches': 24, 'con': 1.0, 'role_position': (80, 334)}

            # 2根据起点和终点进行路径规划
            # 设置图像路径、起点、终点、目标颜色和路线颜色
            if traits_dict is not None and traits_dict["role_position"] != (-1,-1) :
                start = traits_dict["role_position"]
                # goal = (94, 327)
                self.target_point=self.find_closest_and_remaining(self.goal_list,traits_dict["role_position"])
                self.goal=self.target_point[self.goal_list_subscript]

                logger.error(f"当前位置:{start},目标位置:{self.goal}")

                # 3根据坐标值进行路径规划
                # 检查 x 和 y 坐标的差是否都小于等于 2
                if abs(start[0] - self.goal[0]) <= 2 and abs(start[1] - self.goal[1]) <= 2:
                    # 满足条件的代码块
                    logger.success(f"当前位置:{start}在终点附近,切换成下一个节点")
                    self.goal_finish_list.append(self.goal) #添加到已完成节点列表
                    # 判断是否到了最后一个节点
                    if len(self.target_point)==1:
                        logger.error("到了最后一个节点,任务完成")
                        self.moving_flag=True
                    else:
                        self.goal_list_subscript = 1
                else:
                    # 4 进行路径规划,A星算法
                    logger.error("开始A星算法")
                    logger.error(f"当前位置:{start},目标位置:{self.goal}")
                    logger.error(f"目标颜色:{self.target_colors_hex},路线颜色:{self.route_color},边界颜色:{self.penalty_color_hex}")

                    res_list = self.path_finder.find_path(self.map_path, start, self.goal, self.target_colors_hex, self.route_color,self.penalty_color_hex)
                    """
                    [(80, 335), (80, 334), (80, 333), (81, 333), (82, 333), (83, 333), (84, 333), (85, 333), (86, 333), (87, 333),
                    (88, 333), (88, 332), (89, 332), (89, 331), (90, 331), (90, 330), (91, 330), (91, 329), (91, 328), (92, 328),
                    (93, 328), (93, 327), (94, 327)]
                    """
                    logger.error(f"A星算法规划结果:{res_list}")
                    # 输出结果
                    if res_list:
                        # 每隔2个取1个
                        filtered_list = res_list[::3]
                        converted_points = self.converter.process_points(filtered_list)
                        logger.error(f"转换后的场景点击坐标列表：{converted_points}")
                        #[(810, 405), (720, 315), (855, 450), (855, 450), (810, 405), (810, 405), (765, 360), (810, 405)]
                        if converted_points:
                            for point in converted_points:
                                self.mouse_right_click(point[0], point[1],delay_time=0.4)
                            self.node_counter=0 # 重置计数器
                            self.goal_list_subscript=0 # 重置节点索引值
                            logger.error("已到达节点") #todo:接上刷挂操作
                            # self.moving_flag = True # 移动标识

        self.node_counter += 1

node_list = [
    (80, 334), (105, 323), (125, 307),
    (139, 295), (158, 277),(168, 271),
    (190, 261), (222, 240), (239, 246),
    (247, 250),(273, 262), (294, 255),
    (301, 248), (297, 219), (272, 203),
    (294, 194), (311, 181), (309, 163),
    (297, 141), (310, 132),(324, 129), (398, 87)
]


a_star_data={
    "word": {
        # 30: {
        #     "scope": (608, 225, 1006, 691),
        #     "con": 0.8,
        #     "offset": (0, 0),
        #     "use": "成长奖励",
        #     "unique": True,
        #     "enable": True,
        # },  # 每日签到
        # "高级特权":{
        #     "scope": (580,485,739,539),
        #     "con": 0.8,
        #     "offset": (0, 0),
        #     "use": "每日签到",
        #     "enable":True,
        # },#每日签到

    },
    "image": {
        # r"resource/images_info/other/奖励图标.bmp":{
        #     "scope":(1036, 41, 1254, 112),
        #     "con":0.8,
        #     "enable":True
        #     "unique": True,
        # },#奖励图标

    },
}