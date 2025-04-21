import random
import re
import time
import numpy as np
from PIL import Image
from otauto.a_star_v2 import PathFinder
from otauto.coordinate_converter import CoordinateConverter
from otauto.image_traits import ImageTraits
from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块
from resource.parameters_info.basic_parameter_info import dungeons_exit_dict, city_name, dungeons_node_dict, \
    reward_name, state_points_dict

"""
功能:副本模块
日期:2025-3-27 21:59:21
描述:
    模块化设计
"""

"""
explore
"""

class Explore(TaskLogic):
    """
    任务详情:这里接入任务的具体操作内容
    def task_details(self),所有操作接入这个函数中
    vnc: vnc对象
    vnc_port: vnc端口号
    queue_handle: 队列操作对象
    task_welfare
    """
    def __init__(self,vnc,vnc_port,queue_handle ,dungeons_name):
        super().__init__(vnc,vnc_port,queue_handle)
        self.queue_enable({"word":{4:"ban"}}) # 取消任务识别
        self.deaths_flag = False # 判断死亡标识符
        self.color_flag = False #判断地图上快速搜索上的功能是否已勾选
        self.node_flag = False #节点标识符
        self.moving_flag = False #移动模块标识符
        self.coordinate_node= None #节点坐标
        self.dungeons_name= dungeons_name # 副本名称
        self.ini_dungeons_dict = self.ini_handler.get_section_items(self.dungeons_name)  # 获取ini数据
        self.map_path = self.ini_dungeons_dict["map_path"]  # 地图路径
        self.color_path = self.ini_dungeons_dict["color_path"]  # 颜色路径
        self.goal_list=dungeons_node_dict[f"{self.dungeons_name}"] # 节点列表
        self.target_colors_hex =self.ini_dungeons_dict["target_colors_hex"].split(",")   # 允许通行的颜色
        self.route_color = self.ini_dungeons_dict["route_color"].split(",")  # 惩罚值最低的颜色
        self.penalty_color_hex = "00ff7f"  # 惩罚颜色
        image2 = Image.open(self.map_path) # 读取图像
        self.image2_array = np.array(image2) # 将PIL图像转换为NumPy数组
        self.path_finder = PathFinder() # 创建一个PathFinder对象
        self.imagetraits = ImageTraits()  # 只使用 SIFT
        self.converter = CoordinateConverter(self.map_path) # 创建一个CoordinateConverter对象
        self.node_flag=False # 节点标识
        self.exit_list=dungeons_exit_dict # 副本出口列表
        self.start = (-1, -1)  # 起点初始化
        self.goal = (-1, -1) # 当前目标点
        self.death_point = (-1, -1) # 死亡点
        self.goal_finish_list=[] # 已完成的节点列表
        self.target_point = None #目标点,和识别出来的起点最接近的节点
        self.goal_list_subscript=0 # 节点列表的下标
        self.astar_fail_num = 0 # A*算法失败次数
        self.boss_counter = 0 # boss计数器,避免未识别出来直接退出
        self.deaths_num = 0 # 死亡计数器
        self.point_list=[] # 坐标列表
        self.boss_flag=False # boss刷完
        self.equipment_disassembly_flag = False # 装备分解标识符
        self.equipment_disassembly_finish_flag = False # 装备分解完成标识符
        self.last_general_time= 0 # 武将存在的时间
        self.boss_name=set() # boss名称
        self.captain_leave_flag = False # 队长离开标识符
        self.boss_flag_confirm = False # 队员确认BOSS标识符
        self.team_mode = False # 队伍模式标识符
        self.last_红叶舞_time = 0 # 百花医红叶舞技能时间

    def task_刷怪模块(self):
        if "主界面" in self.interface_info:
            logger.error("刷怪中")
            self.node_counter=0 #节点计数器初始化
            self. task_skill_release() #刷怪
            self.key_press('TILDE',delay_time=0.2) # 拾取物品
            return True
        else:
            self.interface_closes()
            return True

    def task_收服模块(self):
        if self.find_data_from_keys_list_click(["resource/images_info/other/武将收服.png"], self.image_data,
                                               x3=20, y3=20, delay_time=15):
            self.mouse_move_scope(419, 453, 618, 582,delay_time=0.5)
            logger.warning("找到白名怪,收服中")
            self.point_list=[] # 重置坐标列表
            return "task_finish"

    def task_医生模块(self):
        """
        判断其他队员的血量进行加血操作
        """
        try:
            res_dict = self.find_word_from_acquire_num(42)
            if res_dict:
                logger.error(f"{res_dict}")
                """
                {'战神无情': (88, 206, 0.999, 42),
                '4088/4088': (94, 228, 0.998, 42),
                '你的宝贝': (87, 271, 0.999, 42),
                '2557/2557': (94, 293, 0.998, 42)}
                """
                for key, value in res_dict.items():
                    if "/" in key and any(char.isdigit() for char in key):
                        # 使用正则表达式提取数字
                        numbers = re.findall(r'\d+', key)

                        if len(numbers) == 2:  # 确保找到了两个数字
                            try:
                                # 将字符串列表转换为整数列表
                                int_list = [int(num) for num in numbers]
                                # 计算百分比
                                percentage = int((int_list[0] / int_list[1]) * 100)
                                logger.info(f"{int_list}, 血量百分比: {percentage}%")
                                if percentage <= 80:
                                    logger.error("血量过低")
                                    self.mouse_left_click(value[0], value[1], delay_time=0.8)
                                    for i in range(random.randint(1, 2)):
                                        self.key_press("8", delay_time=0.5)
                                    for i in range(random.randint(1, 2)):
                                        self.key_press("9", delay_time=1.5)
                                    return True
                            except ZeroDivisionError:
                                logger.warning(f"在计算百分比时出现除以零的情况，键: {key}")
                            except Exception as e:
                                logger.error(f"处理键 {key} 时发生错误: {e}")
        except Exception as e:
            logger.error(f"错误提示:{e}")

    def task_离开模块(self):
        if self.map_name in city_name:
            if self.team_mode:
                if self.role_sect in ["少林"]: #队长
                    points_str = ','.join(map(str, self.start)) # 将元组转换为字符串
                    #interactor – 交互器,默认值:-1 未战斗:0 战斗中:1 跟随中:2 移动中:3 boss战中:4 副本完成:5
                    self.redis_update_info("刷怪模块","1","-1","-1",points_str)

            if self.find_data_from_keys_list_click(["明日再来"], self.word_handle_data, delay_time=2):
                logger.info("该副本今天已经全部挑战完成")
                self.ls_progress = {"state": True}  # 模块运行结束
                return True

            elif self.find_data_from_keys_list_click(["确定"], self.word_handle_data, delay_time=2):
                logger.info("已退出副本,回到城池")
                self.ls_progress = {"state": False}  # 模块运行结束
                return True
            else:
                logger.error("到了城池,退出副本")
                self.ls_progress = {"state": False}  # 模块运行结束
                return True
        else:
            if self.find_data_from_keys_list_click(["resource/images_info/main_task/任务对话.png"], self.image_data,
                                                   delay_time=10):
                logger.info("退出副本")
                self.point_list=[] # 重置坐标列表
                return True

            elif self.find_data_from_keys_list_click(["离开"], self.word_handle_data, delay_time=10):
                logger.info("退出副本")
                self.point_list = []  # 重置坐标列表
                return True

            else:
                self.task_移动模块()  # 移动
                return True

    def task_拆解模块(self):
        self.node_current = "task_拆解模块"

        if not self.role_running or not self.map_differences:
            if self.node_counter>=5 or self.node_flag:
                if "主界面" in self.interface_info:
                    self.node_counter = 0
                    self.equipment_disassembly_flag= True
                    self.node_current="task_移动模块"
                    return "task_finish"
                else:
                    self.interface_closes()

            elif not self.node_flag:
                if "拆解界面" in self.interface_info :
                    self.mouse_left_click_scope(780, 539, 847, 553,delay_time=8) #点击拆解
                    self.mouse_left_click_scope(882, 185, 894, 200,delay_time=1) #关闭界面
                    self.node_flag=True
                    return True

                elif "地图界面" in self.interface_info :
                    self.find_map_npc(["装备"],"功能",delay_time=8)
                    self.node_counter=0 #重置

                elif "主界面" in self.interface_info:
                    self.key_press("M",delay_time=1)

                else: #其他界面,关闭
                    self.interface_closes()

        self.node_counter += 1 #节点计数器

    def task_辅助模块(self):
        self.key_press("TILDE")
        self.key_press("F") # 辅助功能
        # self.key_press("1") # 攻击

    def task_位置模块(self,node_list):
        """
        计算当前位置信息
        """
        self.start=(-1,-1) # 起点初始化
        self.goal=(-1,-1) # 目标点初始化

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
            self.start = traits_dict["role_position"]
            # goal = (94, 327)
            # self.target_point = self.find_closest_and_remaining(self.goal_list, traits_dict["role_position"]) # 会跑回头路
            self.target_point = self.find_remaining_nodes(self.goal_list, traits_dict["role_position"]) # 不会跑回头路
            try:
                self.goal = self.target_point[0] #最近的目标点

                # 检查 x 和 y 坐标的差是否都小于等于 3, 并且目标点不在已完成节点列表中
                if abs(self.start[0] - self.goal[0]) <= 3 and abs(self.start[1] - self.goal[1]) <= 3:
                    # 满足条件的代码块
                    logger.success(f"当前位置:{self.start}在终点附近,切换成下一个节点")
                    self.goal_finish_list.append(self.goal)  # 添加到已完成节点列表
                    # 判断是否到了最后一个节点
                    if len(self.target_point) == 1 and self.dungeons_name in ["屠狼洞","凤鸣山","长寿宫"]:
                        logger.error("到了最后一个节点,任务完成")
                        self.moving_flag = True
                        return "task_finish"

                    elif len(list(set(self.goal_finish_list))) == len(self.goal_list) and self.dungeons_name in reward_name:
                        self.moving_flag = True
                        return "task_finish"

                    elif len(list(set(self.goal_finish_list))) < len(self.goal_list) and self.dungeons_name in reward_name:  # 已完成的列表少于节点列表,说明还有节点没有完成
                        set_diff = set(self.goal_list).difference(set(self.goal_finish_list))
                        self.goal = list(set_diff)[0]
                        return "task_finish"

                    else:
                        self.goal = self.target_point[1] # 更新目标点
                        return "task_finish"
            except Exception as e:
                logger.error(f"{e}")
                self.goal = self.target_point[0]
                return "task_finish"

            logger.error(f"当前位置:{self.start},目标位置:{self.goal}")

            if len(self.goal_list) >= 2 and self.goal in self.goal_list[:2] and not self.equipment_disassembly_flag:  # 节点长度大于2,进行装备分解
                if self.dungeons_name in ["长寿宫"] and self.dungeons_name in reward_name:
                    self.equipment_disassembly_flag=True
                    return "task_finish"

                logger.error(f"当前位置:{self.goal}在起点附近,进行装备分解")
                self.node_current="task_拆解模块"
                return "task_finish"
        else:
            logger.error("当前位置获取失败")
            self.point_list.append(self.map_position) # 添加到坐标列表
            return "task_finish"

    def task_移动_保险(self):
        """
        A星寻路失败的处理
        """
        logger.error("移动_保险激活")
        if len(set(self.point_list))==1: #说明坐标为改变
            # logger.error(f"{self.mutil_colors_data}")
            if self.mutil_colors_data !={}:
                for key, value_data in self.mutil_colors_data.items():
                    if key in ["目标体_地图红点"]:
                        res_tuple = self.find_closest_point(value_data["scope"], self.role_map_position)
                        logger.error(f"{res_tuple}")
                        self.mouse_right_click(*res_tuple, delay_time=3)
                        self.point_list = []  # 重置坐标列表
                        return "task_finish"
            elif self.mutil_colors_data =={}:
                logger.warning("寻路失败,点击小地图")
                self.mouse_right_click(1367, 107,delay_time=2)  # 盲点击小地图
                self.point_list = []  # 重置坐标列表
                return  "task_finish"
        self.point_list = []  # 重置坐标列表

    def task_移动_astar(self):
        """
         A星移动模块
         :node_list :节点列表
        """
        if self.death_point != (-1,-1):
            self.goal=self.death_point # 前往死亡点
            self.death_point=(-1,-1) # 重置死亡点

        # 进行路径规划,A星算法
        res_list = self.path_finder.find_path(self.color_path, self.start, self.goal, self.target_colors_hex,
                                              self.route_color,self.penalty_color_hex)

        logger.error(f"A星移动模块激活:当前位置{self.start},目标位置{self.goal}")
        logger.error(f"目标颜色:{self.target_colors_hex},路线颜色:{self.route_color},边界颜色:{self.penalty_color_hex}")
        logger.error(f"A星算法规划结果:{res_list}")
        # 输出结果
        if res_list:
            # 每隔2个取1个
            self.astar_fail_num=0 # 失败次数初始化
            filtered_list = res_list[::3]
            converted_points = self.converter.process_points(filtered_list)
            logger.error(f"转换后的场景点击坐标列表：{converted_points}")
            # [(810, 405), (720, 315), (855, 450), (855, 450), (810, 405), (810, 405), (765, 360), (810, 405)]
            if converted_points:
                for point in converted_points:
                    self.mouse_right_click(point[0], point[1], delay_time=0.25)
                self.node_counter = 0  # 重置计数器
                self.goal_list_subscript = 0  # 重置节点索引值
                logger.error("已到达节点")
                self.key_press("TAB",delay_time=0.5)  # 切换到目标
                for i in range(random.randint(2, 3)):
                    self.key_press("1",delay_time=0.3)  # 攻击
                # self.queue_interval(1)
                return "task_finish"
        else:
            logger.error("A星算法规划失败")
            self.astar_fail_num+=1 # a星算法失败次数
            return "task_finish"

    def task_移动模块(self):
        if "主界面" in self.interface_info:
            self.point_list.append(self.map_position) # 添加到坐标列表

            if self.boss_flag or self.moving_flag:
                self.goal=dungeons_exit_dict[f"{self.dungeons_name}"][0] # 获取退出坐标
                self.node_current="task_离开模块"

            if self.task_加血值判断(): # 非战斗状态下回血
                self.key_press("0", delay_time=0.5)  # 角色加血

            if len(self.point_list) >=3 or self.astar_fail_num>=3:
                self.astar_fail_num=0 # 失败次数初始化
                if self.task_移动_保险()=="task_finish":
                    return "task_finish"

            if self.start !=(-1,-1) and self.goal !=(-1,-1):
                if self.task_移动_astar()=="task_finish":
                    return "task_finish"
        else:
            self.interface_closes()
            return "task_finish"

    def task_general(self):
        """
        通用操作
        """
        if self.deaths_flag: # 死亡处理
            logger.error("死亡处理")
            if self.map_name in ["长寿宫"]:
                time.sleep(60) #待测试
                if "地图界面" in self.interface_info :
                    if self.find_data_from_keys_list_click(["resource/images_info/other/队友标志.bmp"],self.image_data,action=3):
                        self.key_press("M")  # 关闭地图界面
                        self.deaths_flag = False  # 重置死亡标志
                        self.queue_interval(30)
                        time.sleep(30)
                    else:
                        self.mouse_right_click_scope(786, 335, 826, 358)
                        self.key_press("M")  # 关闭地图界面
                        self.deaths_flag = False  # 重置死亡标志
                        self.queue_interval(30)
                        time.sleep(30)

                elif "主界面" in self.interface_info:
                    self.key_press("M")
                else:
                    self.interface_closes()
            else:
                self.deaths_flag = False  # 重置死亡标志

            return "task_finish"

        self.captain_leave_flag = False  # 队长不在附近初始化

        res_team=self.find_data_from_keys_list(["resource/images_info/other/组队_离队标志.png"],self.image_data)
        if res_team: # 获取组队离队标志
            for key, value_dict in res_team.items():  # 查看列表中字典的键值对
                value_list = value_dict.get("scope")
                for scope in value_list: #[(26, 208, 40, 225, 0.988), (26, 273, 40, 290, 0.825)]
                    if scope[1]<250:
                        self.captain_leave_flag=True # 队长不在附近
                        break

        if self.find_data_from_keys_list(["连续按|空格|挣脱控制"],self.word_handle_data):
            for i in range(3, 6):
                self.key_press('SPACE', delay_time=0.3)

        if self.find_data_from_keys_list_click(["金币|物品|玉衡|奖励"], self.word_handle_data, delay_time=2):
            for i in range(random.randint(3, 5)):
                self.key_press('TILDE', delay_time=0.2)

        if self.find_data_from_keys_list_click(["物品", "奖励"], self.word_handle_data, delay_time=5):
            for i in range(random.randint(3, 5)):
                self.key_press('TILDE', delay_time=0.2)

        if self.find_data_from_keys_list_click(["复活点"], self.word_handle_data, delay_time=5):
            logger.error("角色死亡")
            self.key_press("0", delay_time=3) # 回血吃药
            self.goal_finish_list = [] # 重置目标列表
            self.deaths_num += 1 # 死亡次数加1
            self.deaths_flag=True # 死亡标志
            return "task_finish"

        if self.boss_flag:  # 避免漏捡
            logger.error("boss已经刷完,点击拾取物品")
            for i in range(random.randint(3, 5)):
                self.key_press('TILDE', delay_time=0.5)

        if self.find_data_from_keys_list_click(["确定"], self.word_handle_data, delay_time=2):
            self.key_press('TILDE', delay_time=0.5)

        if self.find_data_from_keys_list(["resource/images_info/other/武将_守护.png"], self.image_data):  # 武将存在
            self.last_general_time = int(time.time())

        if int(time.time()) - self.last_general_time > 300:  # 武将间隔召唤时间为5分钟
            logger.error("武将消失,重新刷")
            self.key_press("P", delay_time=1)
            self.mouse_left_click_scope(795, 617, 860, 621, delay_time=1)
            self.key_press("P", delay_time=1)
            self.last_general_time = int(time.time())  # 记录时间

    def task_hp(self):
        if self.task_加血值判断():
            if int(time.time()) - self.last_restore_1_time >= 120:  # 时间间间隔大于120秒
                for i in range(random.randint(2, 4)):  # 多次点击
                    self.key_press("-", delay_time=0.15)  # 血瓶1
                self.last_restore_1_time = int(time.time())
            elif int(time.time()) - self.last_restore_2_time >= 120:  # 时间间间隔大于120秒
                for i in range(random.randint(3, 5)):  # 多次点击
                    self.key_press("=", delay_time=0.15)  # 血瓶2
                self.last_restore_2_time = int(time.time())

    def task_boss(self):

        self.task_普通高频技能()  # 释放普通高频技能
        self.task_普通延迟技能()  # 释放普通延迟技能

    def task_on_hook(self,team_mode:bool=False):
        self.task_hp() # 恢复血量

        self.team_mode=team_mode # 团队模式
        if team_mode and self.role_sect in ["少林"]:
            if self.task_加血值判断(60):
                for i in range(random.randint(2, 4)):  # 多次点击
                    self.key_press("9", delay_time=0.15)  # 内功疗伤

            if self.target_info and self.target_info['name'] in ["纳魂尊者","灭魂灵兽", "摄魂玄女"]:
                if self.find_data_from_keys_list(["连续按|空格|挣脱控制"], self.word_handle_data):
                    if int(time.time()) - self.last_restore_1_time >= 120:  # 时间间间隔大于120秒
                        for i in range(random.randint(2, 4)):  # 多次点击
                            self.key_press("-", delay_time=0.15)  # 血瓶1
                        self.last_restore_1_time = int(time.time())
                    elif int(time.time()) - self.last_restore_2_time >= 120:  # 时间间间隔大于120秒
                        for i in range(random.randint(3, 5)):  # 多次点击
                            self.key_press("=", delay_time=0.15)  # 血瓶2
                        self.last_restore_2_time = int(time.time())
                    for i in range(3, 6):
                        self.key_press('SPACE', delay_time=0.3)
                if self.task_加血值判断():
                    # 时间间间隔大于90秒
                    if int(time.time()) - self.list_restore_time >= 90:
                        self.task_加血技能()  # 释放加血技能
                self.task_hp()  # 恢复血量
                logger.error(f"BOSS战斗中")
                self.task_boss()
                self.node_current = "task_boss"  # 刷怪节点
                points_str = ','.join(map(str, self.start))  # 将元组转换为字符串
                # interactor – 交互器,默认值:-1 未战斗:0 战斗中:1 跟随中:2 移动中:3 boss战中:4 副本完成:5
                self.redis_update_info("boss", "1", "-1", "4", points_str)
                return True

        if team_mode and self.role_sect not in ["少林"]:
            logger.remove()
            self.queue_enable({"yolo":{"红名怪":"ban"}})
            vnc_port=self.leader_info_dict["vnc_port"] # 获取队长端口
            captain_info = self.redis_find_team_info(f"team:{self.team_designation}:1:{vnc_port}") # 获取队长信息
            """
            {'task_name': 'TaskDungeons', 'task_message': '刷怪模块', 'health_degree': '5170/5170',
            'real_time_position': '白屏寨, 283,53', 'team_status': '1', 'schedule': '白屏寨',
            'interactor': '1', 'points': '-1,-1', 'updated_at': '1743214947'}
            """
            if self.captain_leave_flag:  # 队长不在附近
                if captain_info['points'] != '-1,-1':
                    self.task_移动模块()
                    self.node_current = "task_移动模块"  # 移动节点
                    return True
            else:
                if captain_info['interactor'] in ["5"]:
                    self.boss_flag_confirm = True # 队长离开副本
                    self.boss_flag=True # boss刷完
                    self.node_current = "task_离开模块"  # 移动节点
                    return True

                elif self.role_sect in ["凌云","凌云寨"]:
                    # logger.error("凌云操作")
                    self.key_press('TILDE', delay_time=0.2)
                    self.key_press("F2", delay_time=0.5)  # 选择队长
                    self.key_press("NUM0", delay_time=1)  # 选择跟随
                    for i in range(random.randint(2, 3)):
                        self.key_press("3", delay_time=0.5)
                    if captain_info['interactor'] in ["4", "1"]:
                        self.key_press("F2", delay_time=0.5)  # 选择队长
                        self.key_press("F", delay_time=1)  # 选择跟随
                        self.key_press("1", delay_time=2)
                        self.node_current = "task_刷怪模块"
                    elif captain_info['interactor'] in ["2"]:
                        self.key_press('TILDE', delay_time=0.2)
                        self.key_press("F2", delay_time=0.2)  # 选择队长
                        self.key_press("NUM0", delay_time=1)  # 选择跟随
                        self.node_current = "task_辅助模块"  # 移动节点
                    return True

                elif self.role_sect in ["灵宿","天煞"]:
                    if captain_info['interactor'] in ["2"]:
                        self.queue_interval(1)
                        self.key_press('TILDE', delay_time=0.2)
                        self.key_press("F2", delay_time=0.2)  # 选择队长
                        self.key_press("NUM0", delay_time=1)  # 选择跟随
                        self.node_current = "task_辅助模块"  # 移动节点
                    elif captain_info['interactor'] in ["4", "1"]:  # 队长在战斗中
                        self.task_hp()  # 恢复血量
                        self.queue_interval(1)
                        self.key_press('TILDE', delay_time=0.2)
                        self.key_press("F2", delay_time=0.5)  # 选择队长
                        self.key_press("NUM0", delay_time=1)  # 选择跟随
                        self.key_press("F", delay_time=1)  # 协助攻击
                        if self.task_怒气值判断():
                            self.task_怒气技能()  # 释放怒气技能
                        self.task_召唤技能()  # 释放召唤技能
                        self.node_current = "task_辅助模块"  # 移动节点
                    return True

                elif self.role_sect in ["百花医"]:  # 医生 ,加血,协助攻击
                    self.node_current = "task_辅助模块"  # 移动节点
                    if abs(int(time.time()) - self.skill_状态技能_last_time) >= 28 * 60:  # 状态技能间隔为28分钟
                        if self.team_duty in ["3"]:
                            self.mouse_left_click(*state_points_dict["alt+2"], delay_time=1)
                        elif self.team_duty in ["4"]:
                            self.mouse_left_click(*state_points_dict["alt+3"], delay_time=1)
                        elif self.team_duty in ["5"]:
                            self.mouse_left_click(*state_points_dict["alt+1"], delay_time=1)
                        self.mouse_left_click(*state_points_dict["alt+4"], delay_time=0.5)
                        self.mouse_move_scope(813, 737, 974, 797)
                        self.skill_状态技能_last_time = int(time.time())

                    if self.task_加血值判断():
                        self.key_press("9", delay_time=0.5)
                    self.key_press('TILDE', delay_time=0.2)

                    if self.team_duty in ["3","4"]:
                        self.key_press("F2", delay_time=0.5)  # 选择队长
                        self.key_press("NUM0", delay_time=1)  # 选择跟随
                        self.key_press("8", delay_time=0.5)
                    elif self.team_duty in ["5"]:
                        self.key_press("F4", delay_time=0.5)  # 选择攻击手
                        self.key_press("NUM0", delay_time=1)  # 选择跟随
                        self.key_press("8", delay_time=0.5)

                    if captain_info['interactor'] in ["4", "1"]: # 攻击
                        self.task_hp()  # 恢复血量
                        result = random.choice(["3", "4","5"])
                        if self.team_duty in ["3", "4"]:
                            self.key_press("F2", delay_time=0.5)  # 选择队长
                            self.key_press("F", delay_time=1)  # 选择跟随
                            self.task_召唤技能()  # 释放召唤技能
                            if self.task_怒气值判断():
                                self.task_怒气技能()  # 释放怒气技能
                            self.key_press("3", delay_time=0.5)  # 使用技能

                        elif self.team_duty in ["5"]:
                            self.key_press("F4", delay_time=0.5)  # 选择攻击手
                            self.key_press("F", delay_time=1)  # 选择跟随
                            if self.task_怒气值判断():
                                self.task_怒气技能()  # 释放怒气技能
                            self.key_press("3", delay_time=0.5)  # 使用技能

                        if self.team_duty == result and int(time.time()) - self.last_红叶舞_time >= 30:  # 随机选中
                            self.key_press("5", delay_time=3)  # 使用技能
                            self.last_红叶舞_time=int(time.time())

                    elif captain_info['interactor'] in ["2"]:
                        self.key_press('TILDE', delay_time=0.2)
                        if self.team_duty in ["3", "4"]:
                            self.key_press("F2", delay_time=0.2)  # 选择队长
                            self.key_press("NUM0", delay_time=1)  # 选择跟随
                        elif self.team_duty in ["5"]:
                            self.key_press("F4", delay_time=0.2)
                            self.key_press("NUM0", delay_time=1)
                    return True
                #未战斗:0 战斗中:1 跟随中:2 移动中:3 boss战中:4 副本完成:5

                elif captain_info['interactor'] in ["2"]:
                    self.queue_interval(1)
                    self.key_press('TILDE', delay_time=0.2)
                    self.key_press("F2", delay_time=0.2)  # 选择队长
                    self.key_press("NUM0", delay_time=1)  # 选择跟随
                    self.node_current = "task_辅助模块"  # 移动节点
                    return True

                elif captain_info['interactor'] in ["4","1"]:  # 队长在战斗中
                    self.task_hp()  # 恢复血量
                    self.queue_interval(1)
                    self.key_press('TILDE', delay_time=0.2)
                    self.key_press("F2", delay_time=0.5)  # 选择队长
                    self.key_press("NUM0", delay_time=1)  # 选择跟随
                    self.key_press("F", delay_time=1)  # 协助攻击
                    self.task_刷怪模块()
                    self.node_current = "task_刷怪模块"  # 移动节点
                    return True

        if self.target_info and self.target_info['name'] in ["屠狼牙","贱剑客","摄魂玄女"]:
            self.task_hp()  # 恢复血量
            logger.error(f"BOSS战斗中:{self.boss_name}")
            self.point_list=[] # 重置坐标列表
            self.boss_name.add(self.target_info['name'])
            self.task_刷怪模块()
            self.node_current = "task_刷怪模块"  # 刷怪节点
            if team_mode:
                if self.role_sect in ["少林"]: #队长
                    points_str = ','.join(map(str, self.start)) # 将元组转换为字符串
                    #interactor – 交互器,默认值:-1 未战斗:0 战斗中:1 跟随中:2 移动中:3 boss战中:4 副本完成:5
                    self.redis_update_info("刷怪模块","1","-1","4",points_str)
            return True

        if self.find_data_from_keys_list_click(["resource/images_info/main_task/任务对话.png"], self.image_data,
                                               delay_time=10):
            logger.info("退出副本")
            self.point_list = [] # 重置坐标列表
            self.boss_flag = True  # boss标识
            if team_mode:
                if self.role_sect in ["少林"]: #队长
                    points_str = ','.join(map(str, self.start))  # 将元组转换为字符串
                    # interactor – 交互器,默认值:-1 未战斗:0 战斗中:1 跟随中:2 移动中:3 boss战中:4 副本完成:5
                    self.redis_update_info("离开模块", "1", "-1", "5", points_str)
            return True

        elif self.find_data_from_keys_list_click(["离开"], self.word_handle_data, delay_time=10):
            logger.info("退出副本")
            self.point_list = []  # 重置坐标列表
            self.boss_flag = True  # boss标识
            if team_mode:
                if self.role_sect in ["少林"]: #队长
                    points_str = ','.join(map(str, self.start))  # 将元组转换为字符串
                    # interactor – 交互器,默认值:-1 未战斗:0 战斗中:1 跟随中:2 移动中:3 boss战中:4 副本完成:5
                    self.redis_update_info("离开模块", "1", "-1", "5", points_str)
            return True

        elif self.boss_counter>=3 or self.find_data_from_keys_list_click(["屠狼洞","凤鸣山"],self.word_handle_data,delay_time=1): # 在终点位置没有查找boos,退出副本
            self.node_current="task_离开模块"
            self.point_list = [] # 重置坐标列表
            self.boss_flag=True # boss标识
            if team_mode:
                if self.role_sect in ["少林"]: #队长
                    points_str = ','.join(map(str, self.start))  # 将元组转换为字符串
                    # interactor – 交互器,默认值:-1 未战斗:0 战斗中:1 跟随中:2 移动中:3 boss战中:4 副本完成:5
                    self.redis_update_info("离开模块", "1", "-1", "5", points_str)
            return True

        elif self.target_info and self.target_info['name'] in ["歪嘴军师"]:
            logger.error("武将收服目标")
            self.node_current = "task_收服模块"  # 收服模块
            return True

        elif self.boss_name and not self.target_info['lock'] : # boss已经刷完,但是没有锁定的情况下
            if "屠狼牙" in self.boss_name or "贱剑客" in self.boss_name or "摄魂玄女" in self.boss_name :
                self.node_current = "task_离开模块"
                self.point_list = []  # 重置坐标列表
                self.boss_flag = True  # boss标识
                if team_mode:
                    if self.role_sect in ["少林"]:  # 队长
                        points_str = ','.join(map(str, self.start))  # 将元组转换为字符串
                        # interactor – 交互器,默认值:-1 未战斗:0 战斗中:1 跟随中:2 移动中:3 boss战中:4 副本完成:5
                        self.redis_update_info("离开模块", "1", "-1", "5", points_str)
                return True

        elif self.target_info['lock']:  # 锁定目标
            self.node_current="task_刷怪模块" # 刷怪节点
            self.node_counter = 0  # 节点计数器初始化
            self.boss_counter=0 # boss次数初始化
            self.attack_range_num = 0  # 锁定次数初始化
            if team_mode:
                if self.role_sect in ["少林"]: #队长
                    points_str = ','.join(map(str, self.start))  # 将元组转换为字符串
                    # interactor – 交互器,默认值:-1 未战斗:0 战斗中:1 跟随中:2 移动中:3 boss战中:4 副本完成:5
                    self.redis_update_info("刷怪模块", "1", "-1", "1", points_str)
            return True

        elif not self.target_info['lock'] and not self.target_info["attack_range"]:  # 没有目标在攻击范围内,移动到目标节点
            self.node_current="task_移动模块" # 移动节点
            self.key_press("tab")  # 切换到目标
            self.attack_range_num = 0  # 锁定次数初始化
            if team_mode:
                if self.role_sect in ["少林"]: #队长
                    points_str = ','.join(map(str, self.start))  # 将元组转换为字符串
                    # interactor – 交互器,默认值:-1 未战斗:0 战斗中:1 跟随中:2 移动中:3 boss战中:4 副本完成:5
                    self.redis_update_info("移动模块", "1", "-1", "2", points_str)
            return True

        elif self.attack_range_num >2 and self.target_info["attack_range"]:  # 没有目标在攻击范围内,移动到目标节点,避免误判
            self.node_current="task_移动模块" # 移动节点
            self.attack_range_num = 0  # 锁定次数初始化
            if team_mode:
                if self.role_sect in ["少林"]: #队长
                    points_str = ','.join(map(str, self.start))  # 将元组转换为字符串
                    # interactor – 交互器,默认值:-1 未战斗:0 战斗中:1 跟随中:2 移动中:3 boss战中:4 副本完成:5
                    self.redis_update_info("移动模块", "1", "-1", "2", points_str)
            return True

        elif self.attack_range_num <=2 and self.target_info["attack_range"]:  # 目标在攻击范围内,锁定目标次数少于3
            self.key_press("TAB")  # 切换到目标
            self.node_counter = 0  # 节点计数器初始化
            self.attack_range_num += 1  # 锁定次数加1
            return True

        elif self.target_info["driftlessness"] and not self.moving_flag: # 未发现目标,移动到目标节点
            self.node_current="task_移动模块" # 移动节点
            if team_mode:
                if self.role_sect in ["少林"]: #队长
                    points_str = ','.join(map(str, self.start))  # 将元组转换为字符串
                    # interactor – 交互器,默认值:-1 未战斗:0 战斗中:1 跟随中:2 移动中:3 boss战中:4 副本完成:5
                    self.redis_update_info("移动模块", "1", "-1", "2", points_str)
            return True

        elif self.moving_flag and self.target_info["driftlessness"]: # 到了最后的节点,未发现目标
            logger.error("到了终点附近,退去副本")
            self.key_press("TAB", delay_time=1) # 尝试锁定目标
            self.boss_counter += 1  # 遇到boss次数
            return True

    def task_explore(self):
        """
        接入探索程序
        """
        pass

    def reward_add(self):
        pass


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
        logger.success(f"节点信息(self.node_current):{self.node_current}")
        endpoint_point = self.exit_list[f"{self.dungeons_name}"]
        logger.success(f"+==========================+")
        logger.error(f"队伍番号(self.team_designation):{self.team_designation}")
        logger.error(f"队伍职责(self.team_duty):{self.team_duty}")
        logger.error(f"队员节点(self.team_member):{self.team_member}")
        logger.error(f"队长节点(self.team_leader):{self.team_leader}")
        logger.error(f"队员信息(self.member_info_dict):{self.member_info_dict}")
        logger.error(f"队长信息(self.leader_info_dict):{self.leader_info_dict}")
        logger.error(f"队长离开标志(self.captain_leave_flag):{self.captain_leave_flag}")
        logger.success(f"+==========================+")
        logger.error(f"节点信息(self.goal_list):{self.goal_list}")
        logger.error(f"已完成节点信息(self.goal_list):{self.goal_finish_list}")
        logger.error(f"终点信息(endpoint_point):{endpoint_point}")
        logger.error(f"位置记录(self.point_list):{self.point_list}")
        logger.error(f"锁定次数(self.attack_range_num):{self.attack_range_num}")
        logger.error(f"死亡次数(self.deaths_num):{self.deaths_num}")
        logger.error(f"武将存在时间(self.last_general_time):{self.last_general_time}")
        logger.error(f"当前节点(self.node_current):{self.node_current}")
        logger.error(f"BOSS击杀标志(self.boss_flag):{self.boss_flag}")
        logger.error(f"BOSS名称(self.boss_name):{self.boss_name}")


        if self.task_general() == "task_finish":  # 通用操作
            return "task_finish"

        if self.boss_flag or self.boss_flag_confirm:
            if self.reward_add():
                return True
            self.task_位置模块(dungeons_exit_dict[f"{self.dungeons_name}"])  # 位置判断
            self.task_离开模块()

        elif not self.boss_flag:
            self.task_位置模块(dungeons_node_dict[f"{self.dungeons_name}"])  # 位置判断
            self.task_explore() # 探索模块



