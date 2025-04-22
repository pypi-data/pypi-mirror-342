import random
import time
from otauto.coordinate_conversion import insert_intermediate_points_on_line
from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块
from resource.parameters_info.basic_parameter_info import target_name_ls, city_name


class TaskMain(TaskLogic):
    """
    任务详情:这里接入任务的具体操作内容
    def task_details(self),所有操作接入这个函数中
    vnc: vnc对象
    vnc_port: vnc端口号
    queue_handle: 队列操作对象
    task_welfare
    """
    def __init__(self,vnc,vnc_port,queue_handle,enhance_num:int=-1):
        super().__init__(vnc,vnc_port,queue_handle)
        self.move_num =1 # 移动次数
        self.guide_flag=False #引导任务标志
        self.capture_flg=False # 采集任务标志
        self.acceptance_flag = False # 收服任务标志
        self.general_flag=False # 武将任务标志
        self.boss_flag=False # boss任务标志
        self.tld_flag=False # 屠狼洞任务刷完标志
        self.fms_flag=False # 凤鸣山任务刷完标志
        self.hch_flag=False # 焕成壕支线任务标志
        self.dungeon_moving_flag=False # 副本移动标志
        self.res_dict={"map_name":"未知","task_id":-1,"奖励模块":False,"技能模块":False,"装备模块":False}
        self.十六级_flag=False # 十六级任务标志
        self.二十五级_flag=False # 二十五级任务标志
        self.tld_finish_flag=False # 屠狼洞任务刷完标志
        self.fms_finish_flag=False # 凤鸣山任务刷完标志
        self.enhance_num=enhance_num # 回传的参数
        self.lock_num = 0 # 锁定次数

    def handle_node(self, target_number):
        """
        处理节点任务
        self.handle_node("功能", 26, (738, 203, 796, 229), ["爵位领取人", "悬赏令发布使"],"白屏寨")
        self.handle_node("任务", 19, (799, 202, 856, 231), ["西域商团青城山接引人"],"青城山")
        self.handle_node("活动", 24, (922, 203, 980, 229), ["唐军任务领取人", "义军任务领取人"],"白屏寨")
        :param target_number:  目标数字
        :return:
        """
        pages_list = self.find_word_scope(743, 530, 862, 574)
        if pages_list:
            page_info = pages_list[0][0]
            actual_number = int(page_info.split('第')[1].split('/')[0])

            if actual_number < target_number:
                logger.info(f"实际数字 {actual_number} 小于目标数字 {target_number}，点击右边。")
                for _ in range(target_number - actual_number):
                    self.mouse_left_click(871, 553, delay_time=0.5)

            elif actual_number > target_number:
                logger.info(f"实际数字 {actual_number} 大于目标数字 {target_number}，点击左边。")
                for _ in range(actual_number - target_number):
                    self.mouse_left_click(738, 553, delay_time=0.5)

            elif actual_number == target_number:
                logger.info(f"实际数字 {actual_number} 等于目标数字 {target_number}，无需点击。")
                return True

    def type_十六级(self):
        """
        点击活动领取任务屠狼洞任务
        """
        if not self.role_running or not self.map_differences:
            if self.tld_finish_flag:
                for key, value in self.task_info.items():
                    if "16级" in key:  # 屠狼洞副本
                        self.find_data_from_keys_list_click(finish_keywords, self.task_info, x3=53, y3=7, delay_time=2)
                        self.mouse_move_scope(929, 263, 1163, 479)
                        return True

            elif not self.tld_finish_flag:
                if self.find_data_from_keys_list_click(["副本五次"], self.word_handle_data, delay_time=1):
                    self.tld_finish_flag = True
                    return True

                if self.十六级_flag:
                    if self.tld_flag:
                        if "地图界面" in self.interface_info:
                            self.key_press("M", delay_time=1)
                            return True

                        if self.map_name in ["屠狼洞"]:
                            self.res_dict = {"map_name": "屠狼洞", "task_id": 1, "奖励模块": False, "技能模块": False,
                                             "装备模块": False}
                            self.ls_progress = self.res_dict
                            self.tld_flag = False  # 屠狼洞任务刷完标志
                            return "task_wait"

                        elif self.find_data_from_keys_list_click(["确定"], self.word_handle_data, delay_time=1):
                            pass

                    elif not self.tld_flag:
                        if self.map_name in ["屠狼洞"]:
                            self.tld_flag=True
                            return True

                        elif self.find_data_from_keys_list_click(["屠狼洞内"], self.word_handle_data, delay_time=5):
                            logger.error("type_十六级,屠狼洞副本进入")
                            self.tld_flag = True  # 屠狼洞任务标志位
                            return True

                        elif "地图界面" in self.interface_info:
                            self.find_map_npc(["枯树"],"副本")

                        elif "主界面" in self.interface_info:
                            self.key_press("M")

                    return True

                elif not self.十六级_flag:
                    for key, value in self.task_info.items():
                        if "16级" in key:  # 屠狼洞副本
                            self.十六级_flag = True
                            return True

    def type_二十级(self):
        if self.enhance_num==5:
            self.hch_flag = True

        if not self.hch_flag:
            for key, value in self.task_info.items() :
                if any(keyword in key for keyword in ["20级", "熊", "皮", "黑风军", "督卫头目", "裴虎", "焕夫人"]):  # 焕成壕支线任务完
                    self.res_dict = {"map_name": "黑风寨", "task_id": 5, "奖励模块": False, "技能模块": False,
                                     "装备模块": False}
                    self.ls_progress = self.res_dict
                    self.hch_flag = False  # 凤鸣山任务刷完标志
                    return "task_wait"

    def type_二十五级(self):
        """
        点击活动,领取任务凤鸣山的任务
        """
        if not self.role_running or self.map_differences: #存在地图差值 或者在运动中
            if self.fms_finish_flag:
                for key, value in self.task_info.items():
                    if "25级" in key:  # 凤鸣山副本
                        self.find_data_from_keys_list_click(finish_keywords, self.task_info, x3=53, y3=7, delay_time=2)
                        self.mouse_move_scope(929, 263, 1163, 479)
                        return True

            elif not self.fms_finish_flag:
                if self.find_data_from_keys_list_click(["次数已满"], self.word_handle_data, delay_time=1):
                    self.fms_finish_flag = True
                    return True

                if self.二十五级_flag:
                    if self.fms_flag:
                        if "地图界面" in self.interface_info:
                            self.key_press("M", delay_time=1)
                            return True

                        if self.map_name in ["凤鸣山"]:
                            self.res_dict = {"map_name": "凤鸣山", "task_id": 1, "奖励模块": False, "技能模块": False,
                                             "装备模块": False}
                            self.ls_progress = self.res_dict
                            self.fms_flag = False  # 凤鸣山任务刷完标志
                            return "task_wait"

                        elif self.find_data_from_keys_list_click(["确定"], self.word_handle_data, delay_time=1):
                            pass

                    elif not self.fms_flag:
                        if self.map_name in ["凤鸣山"]:
                            self.fms_flag = True
                            return True

                        elif self.find_data_from_keys_list_click(["险峻的山路"], self.word_handle_data, delay_time=5):
                            logger.error("type_二十五级,凤鸣山副本进入")
                            self.fms_flag = True  # 凤鸣山任务标志位
                            return True

                        elif "地图界面" in self.interface_info:
                            logger.info("地图界面.选择任务领取人")
                            self.find_map_npc(["小黑子"],"副本")

                        elif "主界面" in self.interface_info:
                            self.key_press("M")

                    return True

                elif not self.二十五级_flag:
                    for key, value in self.task_info.items():
                        if "25级" in key:  # 凤鸣山副本
                            self.二十五级_flag = True
                            return True


    def type_长寿宫(self):
        if not self.role_running:
            for key,value in self.task_info.items():
                if "长寿宫" in key :
                    self.ls_progress={"task_id": 4}
                    return "task_wait"

    def type_悬赏(self):
        if not self.role_running:
            for key,value in self.task_info.items():
                if "悬赏" in key and "未" in key:
                    self.ls_progress={"task_id": 3}
                    return "task_wait"

                elif "悬赏" in key and "完成" in key:
                    self.find_data_from_keys_list_click(finish_keywords, self.task_info, x3=53, y3=7, delay_time=2)
                    self.mouse_move_scope(929, 263, 1163, 479)

    def type_凤鸣山(self):
        for key,value in self.task_info.items():
            if "贱客" in key and  self.map_name in city_name and self.enhance_num in [-1]:
                self.res_dict["奖励模块"]=False
                self.res_dict["技能模块"]=True
                self.res_dict["装备模块"]=True
                self.res_dict["map_name"] = "凤鸣山"
                self.res_dict["task_id"] = 0
                self.ls_progress = self.res_dict
                return "task_wait"

        if self.map_name in ["凤鸣山"]:
            logger.error("凤鸣山副本")
            self.res_dict["map_name"]="凤鸣山"
            self.res_dict["task_id"]=1
            self.ls_progress= self.res_dict
            return "task_wait"

        elif self.find_data_from_keys_list_click(["险峻的山路"],self.word_handle_data,delay_time=5):
            logger.error("副本进入")

    def type_爵位(self):
        if not self.role_running:
            for key,value in self.task_info.items():
                if "爵位" in key and "未" in key:
                    self.ls_progress={"task_id": 2}
                    return "task_wait"

                elif "爵位" in key and "完成" in key:
                    self.find_data_from_keys_list_click(finish_keywords, self.task_info, x3=53, y3=7, delay_time=2)
                    self.mouse_move_scope(929, 263, 1163, 479)

    def type_装备进阶(self):
        if self.find_data_from_keys_list_click(["确定"], self.word_handle_data, delay_time=1):
            pass

        if "装备进阶界面" in self.interface_info:
            for key,value in self.task_info.items():
                if "紫色" in key and "未" in key:
                    logger.error("进入装备进阶界面")
                    self.find_data_from_keys_list_click(["进阶"], self.unique_data["word"], delay_time=1)

                elif "紫色" in key and "完成" in key:
                    self.interface_closes()
                    self.find_data_from_keys_list_click(finish_keywords, self.task_info, x3=53, y3=7, delay_time=2)
                    self.mouse_move_scope(929, 263, 1163, 479)

    def type_阵营(self):
        if not self.role_running:
            for key,value in self.task_info.items():
                if "营" in key and "未" in key:
                    if self.find_data_from_keys_list_click(["均衡|弱"],self.word_handle_data,delay_time=2):
                        self.mouse_left_click(736,531)

                    elif self.find_data_from_keys_list_click(["resource/images_info/main_task/加入阵营.png"], self.image_data, delay_time=1):
                        pass

                    elif self.find_data_from_keys_list_click(["势力比：弱","势力比：均衡"],self.word_acquire_data,delay_time=2):
                        self.mouse_left_click(736,531)

                    elif self.find_data_from_keys_list_click(["阵营"], self.task_info, delay_time=1):
                        pass



                elif "营" in key and "完成" in key:
                    self.find_data_from_keys_list_click(finish_keywords, self.task_info, x3=53, y3=7, delay_time=5)
                    self.mouse_move_scope(929, 263, 1163, 479)

    def type_道具商城(self):

        if not self.role_running:
            for key,value in self.task_info.items():
                if "购买" in key and "未" in key:
                    if "商城界面" in self.interface_info:
                        if self.find_data_from_keys_list_click(["确定"], self.word_handle_data, delay_time=1):  # 确定
                            pass
                        elif self.find_data_from_keys_list_click(["购买"], self.word_handle_data,  delay_time=1):  # 购买
                            pass
                        elif self.find_data_from_keys_list_click(["青龙丹"], self.word_handle_data, delay_time=1):  # 青龙丹
                            pass
                        elif self.find_data_from_keys_list_click(["经验道具"],self.word_handle_data, delay_time=1):  # 经验道具
                            pass
                        elif self.find_data_from_keys_list_click(["游戏币"], self.word_handle_data, delay_time=1):  # 游戏币道具
                            pass

                    elif "主界面" in self.interface_info:
                        self.find_data_from_keys_list_click(["resource/images_info/main_task/商城.png"],self.image_data, delay_time=2)

                elif "购买" in key and "完成" in key:
                    self.interface_closes()
                    self.find_data_from_keys_list_click(finish_keywords, self.task_info, x3=53, y3=7, delay_time=5)
                    self.mouse_move_scope(929, 263, 1163, 479)

    def type_血衣镇(self):
        # 节点坐标
        coordinate_node_血衣镇 = [(118, 32), (121, 35), (125, 39), (125, 48), (126, 54), (127, 57), (124, 64),
                                  (125, 74), (127, 80), (126, 85),
                                  (120, 85), (113, 92), (112, 100), (112, 106), (112, 114), (114, 127), (109, 133),
                                  (99, 143),
                                  (91, 148), (89, 158), (90, 166), (90, 173), (90, 181), (91, 188), (94, 195),
                                  (94, 202), (93, 207),
                                  (89, 217), (86, 222), (81, 225), (76, 227), (71, 229), ]

        if self.map_name in ["血衣镇"]:

            logger.error("进入血衣镇")
            logger.error(f"武将收服:{self.general_flag}")
            logger.error(f"boss击杀:{self.boss_flag}")
            logger.error(f"移动次数:{self.move_num}")
            logger.error(f"锁敌次数:{self.lock_num}")

            if self.find_data_from_keys_list_click_scope(["确定"],self.word_handle_data,w=46,h=18,delay_time=2):
                pass

            if self.find_data_from_keys_list_click(["离开"], self.word_handle_data, delay_time=15):
                logger.info("退出副本")
                return True

            for key, value in self.task_info.items():
                if "铁枪" in key and "未" in key:
                    self.acceptance_flag = True
                elif "铁枪" in key and "完成" in key:
                    self.general_flag = True

            if self.boss_flag : #副本完成
                for i in range(random.randint(3,5)):
                    self.key_press("~",delay_time=0.5)
                self.find_data_from_keys_list_click(finish_keywords, self.task_info, x3=53, y3=7, delay_time=5)
                self.mouse_move_scope(1023, 242, 1141, 450)
                return  True

            elif not self.boss_flag: #判断是否击杀boss
                for key,value in self.task_info.items():
                    if "首领" in key and "已" in key:
                        self.boss_flag=True
                        return True

            if not self.general_flag:
                if self.acceptance_flag: # 收服武将
                    if self.find_data_from_keys_list_click(["恭喜你"],self.word_handle_data,delay_time=5):
                        logger.error("收服武将完成")
                    if self.acceptance_flag:
                        logger.error("收服武将")
                        if self.find_data_from_keys_list_click(["resource/images_info/main_task/收服标志.bmp"],
                                                               self.image_data, delay_time=15):
                            logger.info("点击收服标志")
                            return True
                        else:
                            self.key_press("tab")
                            return True

            if self.general_flag and self.target_info:
                self.key_press("~")
                if self.lock_num>=3:
                    if self.mutil_colors_data !={}:  # 目标不在攻击范围内
                        for key, value_data in self.mutil_colors_data.items():
                            if key in ["目标体_地图红点"]:
                                res_tuple = self.find_closest_point(value_data["scope"], self.role_map_position)
                                self.mouse_right_click(*res_tuple, delay_time=3)
                                self.key_press("tab",delay_time=0.2)
                                self.key_press("1",delay_time=0.5)
                        self.lock_num = 0 # 锁定目标次数初始化
                        return True

                if self.target_info["lock"]:  # 锁定目标
                    self.lock_num = 0  # 锁定目标次数初始化
                    num_iterations = random.randint(3, 8)  # 生成一个介于 3 和 6 之间的随机迭代次数
                    for i in range(num_iterations):  # 循环，运行生成的迭代次数
                        logger.info(f"第 {i + 1} 次攻击")
                        self.key_press("1", delay_time=0.5)

                elif self.target_info["attack_range"]:  # 目标在攻击范围内
                    self.key_press("tab")  # 切换到目标
                    self.lock_num+=1 # 锁定目标次数

                elif self.target_info["driftlessness"]:
                    self.move_num+=1
                    coordinate_node_dispose = insert_intermediate_points_on_line(coordinate_node_血衣镇)
                    res_num = self.way_finding_node_op(coordinate_node_dispose, debug=True, range_num=5, threshold=4)
                    if res_num == -1 or self.move_num>3:
                        logger.error("血衣镇节点移动失败")
                        self.mouse_right_click(1385, 89, delay_time=1)  # 点击移动
                        self.move_num=0 # 重置移动次数
                    elif res_num == 0:
                        logger.info("血衣镇节点移动中")

                elif self.mutil_colors_data:  # 目标不在攻击范围内
                    for key, value_data in self.mutil_colors_data.items():
                        if key in ["目标体_地图红点"]:
                            res_tuple = self.find_closest_point(value_data["scope"], self.role_map_position)
                            self.mouse_right_click(*res_tuple, delay_time=3)
                            self.key_press("tab", delay_time=0.2)
                            self.key_press("1", delay_time=0.5)

                        else:  # 小地图范围内无目标
                            self.move_num += 1
                            coordinate_node_dispose = insert_intermediate_points_on_line(coordinate_node_血衣镇)
                            res_num = self.way_finding_node_op(coordinate_node_dispose, debug=True, range_num=5, threshold=4)
                            if res_num == -1 or self.move_num > 3:
                                logger.error("血衣镇节点移动失败")
                                self.mouse_right_click(1385, 89, delay_time=1)  # 点击移动
                                self.key_press("tab",delay_time=0.2)
                                self.key_press("1",delay_time=0.5)
                                self.move_num = 0
                            elif res_num == 0:
                                logger.info("血衣镇节点移动中")

        elif self.find_data_from_keys_list_click(["血衣镇"],self.word_handle_data,delay_time=10):
            logger.info("进入血衣镇")

        elif not self.role_running or self.map_differences:
            for key, value in self.task_info.items():
                if "血衣首领" in key and "0" in key:
                    self.find_data_from_keys_list_click(["0"],self.task_info,delay_time=5)
                    self.mouse_move_scope(929, 263, 1163, 479)

                elif "血衣首领" in key and "完成" in key:
                    self.find_data_from_keys_list_click(finish_keywords,self.task_info,x3=53,y3=7,delay_time=10)
                    self.mouse_move_scope(929, 263, 1163, 479)

    def  type_屠狼洞(self):
        for key,value in self.task_info.items():
            if "屠狗帮" in key and self.map_name in city_name and self.enhance_num in [-1]:
                self.res_dict["奖励模块"]=True
                self.res_dict["技能模块"]=True
                self.res_dict["装备模块"]=True
                self.res_dict["task_id"] = 0
                self.res_dict["map_name"] = "屠狼洞"
                self.ls_progress = self.res_dict
                return "task_wait"

        if self.map_name in ["屠狼洞"]:
            logger.error("屠狼洞副本")
            self.res_dict["map_name"]="屠狼洞"
            self.res_dict["task_id"]=1
            self.ls_progress=self.res_dict
            return "task_wait"

        elif self.find_data_from_keys_list_click(["屠狼洞内"],self.word_handle_data,delay_time=5):
            logger.error("副本进入")

    def type_guide(self):
        if "系统菜单界面" in self.interface_info:
            self.key_press("ESC",delay_time=1)

        if self.find_data_from_keys_list_click(["resource/images_info/main_task/任务对话.png"],self.image_data,delay_time=3):
            for i in range(5):
                self.mouse_left_click(607,609,delay_time=1)
            return True

        elif "杂货界面" in self.interface_info:
            if self.find_data_from_keys_list_click(["确定"],self.word_handle_data,delay_time=1):
                self.key_press("B",delay_time=1)

                return True

        elif "背包界面" in self.interface_info:
            self.key_press("B",delay_time=1)


        elif "技能界面" in self.interface_info:
            if self.find_data_from_keys_list(["技能（完成）"],self.word_acquire_data):
                self.key_press("K",delay_time=1)

            elif self.find_data_from_keys_list(["未"], self.word_acquire_data):

               if self.find_data_from_keys_list_click(["resource/images_info/other/技能升级.png"],self.image_data,delay_time=1):
                    self.mouse_left_click_scope(646, 453, 680, 462,delay_time=0.5)
                    self.mouse_left_click(965,178,delay_time=0.5)
                    self.mouse_left_click(1273,299, delay_time=0.5)
                    self.mouse_move(1067,454,delay_time=0.5)
                    logger.info("点击技能图标")

        elif "驿站界面" in self.interface_info:

            self.find_data_from_keys_list_click(["确定"],self.word_handle_data)
            self.interface_closes()


    def perform_task_action(self, keywords, delay_time, mouse_x, mouse_y):
        """执行任务操作"""
        self.find_data_from_keys_list_click(keywords, self.task_info, delay_time=delay_time,x3=38,y3=6)
        self.mouse_move(mouse_x, mouse_y)

    def type_capture(self):

        if not self.role_running or self.map_differences:
            for key, value in self.task_info.items():
                if "集" in key and ("0/" in key or "1/" in key or "2/" in key):
                    for i in range(3):
                        if self.find_data_from_keys_list_click(["木料"], self.yolo_data, delay_time=5):
                            logger.info("采集中")
                    self.find_data_from_keys_list_click(["0"],self.task_info,delay_time=5)
                    self.mouse_move_scope(929, 263, 1163, 479)

                elif "集" in key and "完成" in key:
                    self.find_data_from_keys_list_click(finish_keywords,self.task_info,x3=53,y3=7,delay_time=5)
                    self.mouse_move_scope(929, 263, 1163, 479)

    def type_find(self,mouse_x=1156, mouse_y=328):
        """
        找寻任务
        :param mouse_x: 鼠标的 X 坐标
        :param mouse_y: 鼠标的 Y 坐标
        """

        def is_task_incomplete(task_name, keywords):
            """判断任务是否未完成"""
            return "未" in task_name and any(keyword in task_name for keyword in keywords)

        def is_task_complete(task_name, keywords):
            """判断任务是否已完成"""
            return "完成" in task_name and any(keyword in task_name for keyword in keywords)

        if not self.role_running or self.map_differences :
            keywords = ["寻找", "了解", "学习", "开通", "找人", "进阶", "抓获", "升到", "拜见","找",]
            try:
                for task_name, value in self.task_info.items():
                    if is_task_incomplete(task_name, keywords):
                        self.perform_task_action(["未"], delay_time=5, mouse_x=mouse_x, mouse_y=mouse_y)
                    elif is_task_complete(task_name, keywords):
                        self.perform_task_action(finish_keywords, delay_time=5, mouse_x=mouse_x, mouse_y=mouse_y)
            except Exception as e:
                print(f"Error while processing tasks: {e}")  # 或者使用 logging 模块

    def type_attack(self):
        """
        攻击
        {'【主线】熟悉武器': (1185, 258, 0.984, 4), '打倒：野猪（0/5）': (1202, 274, 0.959, 4), '交付人：明尘': (1203, 290, 0.998, 4)}

        :return:
        """
        target_name=self.target_info.get("name","未知")
        logger.info(f"目标:{target_name}")
        # 检查是否有键包含 "野猪",在主线任务目标中
        if target_name in target_name_ls:
            num_iterations = random.randint(3, 8) # 生成一个介于 3 和 6 之间的随机迭代次数
            for i in range(num_iterations):  # 循环，运行生成的迭代次数
                logger.info(f"第 {i + 1} 次攻击")
                self.key_press("1",delay_time=0.5)
        if not self.role_running or self.map_differences:
            for key,value in self.task_info.items():
                if any(keyword in key for keyword in ["名录","倒", "物", "到","打"]) and (any(digit in key for digit in ["0/","1/","2/","3/","4/","5/","6/","7/","8/","9/","/"]) or "/10" in key):
                    # 对于包含 "倒", "物", "到" 和 数字的情况
                    self.find_data_from_keys_list_click(["名录","0/","1/","2/","3/","4/","5/","6/","7/","8/","9/","/10","/",], self.task_info, x3=15, y3=5,delay_time=5)
                    self.mouse_move_scope(929, 263, 1163, 479)
                    num_iterations = random.randint(2, 5)  # 生成一个介于 3 和 6 之间的随机迭代次数
                    for i in range(num_iterations):  # 循环，运行生成的迭代次数
                        logger.info(f"第 {i + 1} 次攻击")
                        self.key_press("1", delay_time=0.5)
                elif any(keyword in key for keyword in ["名录","倒", "物","到","打"]) and "完成" in key:
                    # 对于包含 "倒" 或 "物" 和 "完成" 的情况
                    self.find_data_from_keys_list_click(finish_keywords, self.task_info, x3=53, y3=7, delay_time=5)
                    self.mouse_move_scope(929, 263, 1163, 479)

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
        logger.success(f"回传的参数:{self.enhance_num}")

        # 初始化
        self.res_dict = {"map_name": "未知", "task_id": -1, "奖励模块": False, "技能模块": False, "装备模块": False}
        if self.task_加血值判断():
            if int(time.time())-self.last_restore_1_time>=120: #时间间间隔大于120秒
                self.key_press("-",delay_time=0.3) #血瓶1
                self.last_restore_1_time=int(time.time())
            elif int(time.time())-self.last_restore_2_time>=120: # 时间间间隔大于120秒
                self.key_press("=", delay_time=0.3) #血瓶2
                self.last_restore_2_time = int(time.time())

        if self.find_data_from_keys_list_click(["领取","使用后"],self.word_handle_data,delay_time=1):
            logger.info("领取在线奖励")
            self.mouse_move_scope(968, 339, 1130, 447)


        if self.find_data_from_keys_list_click(["resource/images_info/main_task/确定.png"],self.image_data):
            pass

        elif self.find_data_from_keys_list_click(["复活点"],self.word_handle_data,delay_time=5):
            logger.error("角色死亡")
            self.key_press("0",delay_time=3)

        # 奖励中心
        elif self.find_data_from_keys_list_click(["福利中心"],self.word_handle_data,delay_time=2,action=3):
            self.mouse_left_click_scope(1032, 103, 1045, 118,delay_time=1)
            logger.info("福利中心关闭")

        # 交付中心
        elif self.find_data_from_keys_list_click(["点击交付"],self.word_acquire_data,delay_time=2):
            logger.info("交付任务")

        elif self.type_guide():
            logger.info("引导任务")

        elif self.find_data_from_keys_list_click(["resource/images_info/other/侠店关闭.png"],self.image_data,x3=801,y3=-40,delay_time=2):
            logger.error("侠店关闭")

        elif self.find_data_from_keys_list_click(["resource/images_info/other/大唐风流关闭.bmp","resource/images_info/other/侠影关闭.png"],self.image_data,delay_time=2):
            logger.error("大唐风流关闭,侠影关闭")

        elif self.find_data_from_keys_list_click_scope(["resource/images_info/main_task/对话点击.png"],self.image_data,w=245,h=24,delay_time=2):
            logger.info("对话中")

        elif self.find_data_from_keys_list_click(["resource/images_info/main_task/对话标识.png"],self.image_data,x3=-407,y3=35,delay_time=2):
            logger.error("对话中")

        elif self.find_data_from_keys_list_click(["继续主线"],self.task_info,delay_time=1):
            pass

        elif self.type_capture():
            pass

        elif self.type_血衣镇():
            pass

        elif self.type_道具商城():
            pass

        elif self.type_阵营():
            pass

        elif self.type_装备进阶():
            pass

        elif self.type_十六级():
            pass

        elif self.type_屠狼洞():
            pass

        elif self.type_二十级():
            pass

        elif self.type_爵位():
            pass

        elif self.type_二十五级():
            pass

        elif self.type_凤鸣山():
           pass

        elif self.type_悬赏():
            pass

        elif self.type_长寿宫():
            pass

        elif self.type_find():
            pass

        elif self.type_attack():
            pass

        self.queue_screenshot_sync(reset=False)

finish_keywords = ["交付人","付人","交付"]

main_data={
    "word": {
        4:{
            "scope":(1183, 250, 1412, 364),
            "model":1,
            "con":0.8,
           "use":"task_info",
            "enable":True,
            "unique": True,
        "class": ["地图界面","技能界面","商城界面","主界面"],
        },

        "使用后": {
            "scope": (461, 369, 679, 415),
            "con": 0.8,
            "offset": (199, 73),
            "use": "主线任务",
            "unique": True,
            "enable": True,
        },

        "福利中心":{
            "scope": (679, 93, 805, 124),
            "con": 0.8,
            "offset": (0,0),
            "use": "主线任务",
            "enable":True,
            "unique": True,
            'class': ["奖励界面"],
        },
        "确定": {
            "scope": (629,426,779,494),
            "con": 0.8,
            "offset": (21, 7),
            "use": "主线任务",
            "enable": True,
            "unique": True,
            'class': ["奖励界面","背包界面","杂货界面","驿站界面","商城界面"],
        },
        "血衣镇": {
            "scope": (558, 594, 721, 630),
            "con": 0.8,
            "offset": (0, 0),
            "use": "主线任务",
            "enable": True,
            "unique": True,
        },
        "屠狼洞内": {
            "scope": (557, 233, 850, 274),
            "con": 0.8,
            "offset": (39,282),
            "use": "主线任务",
            "enable": True,
            "unique": True,
            'class': ["枯树界面"],
        },
        "险峻的山路": {
            "scope": (559, 225, 850, 276),
            "con": 0.8,
            "offset": (39, 282),
            "use": "主线任务",
            "enable": True,
            "unique": True,
        },
        "恭喜你": {
            "scope": (477, 371, 675, 411),
            "con": 0.8,
            "offset": (218, 67),
            "use": "主线任务",
            "enable": True,
            "unique": True,
        },
        "离开": {
            "scope": (558, 587, 633, 618),
            "con": 0.8,
            "offset": (20, 8),
            "use": "主线任务",
            "enable": True,
            "unique": True,
        },
        "购买": {
            "scope": (445, 343, 530, 378),
            "con": 0.8,
            "offset": (0, 0),
            "use": "主线任务",
            "enable": True,
            "unique": True,
            'class': ["商城界面"],
        },
        "青龙丹": {
            "scope": (312, 274, 377, 305),
            "con": 0.8,
            "offset": (0, 0),
            "use": "主线任务",
            "enable": True,
            "unique": True,
            'class': ["商城界面"],
        },
        "经验道具": {
            "scope": (372,225,480,269),
            "con": 0.8,
            "offset": (0, 0),
            "use": "主线任务",
            "enable": True,
            "unique": True,
            'class': ["商城界面"],
        },
        "游戏币": {
            "scope": (829,200,919,241),
            "con": 0.8,
            "offset": (0, 0),
            "use": "主线任务",
            "enable": True,
            "unique": True,
            'class': ["商城界面"],
        },
        "商城": {
            "scope": (1188, 43, 1249, 110),
            "con": 0.8,
            "model":0,
            "offset": (0, 0),
            "use": "主线任务",
            "enable": True,
            "unique": True,
            'class': ["商城界面"],
        },
        "均衡|弱": {
            "scope": (569, 453, 889, 493),
            "con": 0.8,
            "offset": (0, 0),
            "use": "主线任务",
            "enable": True,
            "unique": True,
        },
        "进阶": {
            "scope": (805, 360, 909, 395),
            "con": 0.8,
            "offset": (22, 10),
            "use": "主线任务",
            "enable": True,
            "unique": True,
            'class': ["装备进阶界面"],
        },

        "全部": {
            "scope": (218, 185, 689, 253),
            "con": 0.8,
            "offset": (0, 0),
            "use": "主线任务",
            "enable": True,
            "unique": True,
        },
        "屠狼洞": {
            "scope": (270, 261, 406, 677),
            "con": 0.8,
            "offset": (648, 9),
            "use": "主线任务",
            "enable": True,
            "unique": True,
        },
        "凤鸣山": {
            "scope": (270, 261, 406, 677),
            "con": 0.8,
            "offset": (648, 9),
            "use": "主线任务",
            "enable": True,
            "unique": True,
        },
        "枯树": {
            "scope": (950, 307, 1060, 553),
            "con": 0.8,
            "offset": (0, 0),
            "use": "主线任务",
            "enable": True,
            "unique": True,
            'class': ["地图界面"],
        },
        "小黑子": {
            "scope": (950, 307, 1060, 553),
            "con": 0.8,
            "offset": (0, 0),
            "use": "主线任务",
            "enable": True,
            "unique": True,
        },
        "副本五次": {
            "scope": (507, 359, 759, 422),
            "con": 0.8,
            "offset": (185, 73),
            "use": "主线任务",
            "enable": True,
            "unique": True,
        },
        "次数已满": {
            "scope": (505, 367, 723, 422),
            "con": 0.8,
            "offset": (185, 73),
            "use": "主线任务",
            "enable": True,
            "unique": True,
        },
        "领取": {
            "scope": (1278, 462, 1327, 489),
            "con": 0.8,
            "offset": (10, -20),
            "use": "主线任务",
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },
    },
    "image": {
        r"resource/images_info/main_task/确定.png": {
            "scope": (475, 259, 1013, 591),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },  # 奖励图标
        r"resource/images_info/main_task/加入阵营.png": {
            "scope": (657, 494, 788, 547),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },  # 奖励图标
        r"resource/images_info/main_task/对话点击.png":{
            "scope":(439, 506, 762, 609),
            "con":0.8,
            "model":1,
            "enable":True,
            "unique": True,
            'class': ["对话界面"],
        },#奖励图标
        r"resource/images_info/main_task/对话标识.png": {
            "scope": (1021, 508, 1068, 568),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["对话界面"],
        },  # 奖励图标
        r"resource/images_info/other/技能升级.png": {
            "scope": (454, 218, 960, 636),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["技能界面"],
        },  # 奖励图标
        r"resource/images_info/main_task/收服标志.bmp": {
            "scope": (659,444,772,546),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
        },  # 奖励图标

        r"resource/images_info/main_task/任务对话.png": {
            "scope": (544, 582, 703, 631),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["对话界面"],
        },  # 奖励图标
        r"resource/images_info/main_task/活动.bmp": {
            "scope": (1140, 51, 1187, 109),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },  # 奖励图标
        r"resource/images_info/camp_task/地图_npc.bmp": {
            "scope": (1088, 563, 1153, 618),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["地图界面"],
        },  # 奖励图标
        r"resource/images_info/main_task/副本.png": {
            "scope": (671, 202, 743, 238),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/main_task/商城.png": {
            "scope": (1183, 43, 1257, 115),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },  # 奖励图标

    },
}