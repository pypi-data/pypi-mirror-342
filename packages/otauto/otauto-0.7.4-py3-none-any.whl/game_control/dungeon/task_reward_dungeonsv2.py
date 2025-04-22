import time

from loguru import logger

from game_control.task_explore import Explore #接入探索者模块

"""
功能:副本模块
日期:2025-3-27 21:59:21
描述:
    模块化设计
"""

class TaskRewardDungeons(Explore):
    """
    任务详情:这里接入任务的具体操作内容
    def task_details(self),所有操作接入这个函数中
    vnc: vnc对象
    vnc_port: vnc端口号
    queue_handle: 队列操作对象
    task_welfare
    """
    def __init__(self,vnc,vnc_port,queue_handle ,dungeons_name):
        super().__init__(vnc,vnc_port,queue_handle,dungeons_name)
        self.map_piont_flag=False #地图标记
        self.npc_name_list = [
            'resource/images_info/reward_task/通缉犯.bmp', "resource/images_info/reward_task/霸山虎.bmp",
            "resource/images_info/reward_task/异族细作.bmp", "resource/images_info/reward_task/血路独行.bmp",
            "resource/images_info/reward_task/七窍玲珑.bmp", "resource/images_info/reward_task/不赦死囚.bmp"
        ]

    def reward_add(self):
        if not self.map_piont_flag :
            logger.success("点击地图界面,移动到出口")
            if "地图界面" in self.interface_info:
                res_dict = self.find_data_from_keys_list(["resource/images_info/reward_task/出口箭头_荒野.png"],
                                                         self.image_data)
                if res_dict:
                    # {'resource/images_info/reward_task/通缉犯.bmp': {'scope': [(875, 455, 915, 466, 0.986)], 'offset': (24, 135), 'model': 1, 'enable': True, 'unique': True}}
                    logger.error(f"{res_dict}")
                    for key, value in res_dict.items():
                        x1, y1, x2, y2 = value["scope"][0][0], value["scope"][0][1], value["scope"][0][2], \
                        value["scope"][0][3]
                        x_median = (x1 + x2) // 2
                        y_median = (y1 + y2) // 2
                        point = x_median + value["offset"][0], y_median + value["offset"][1]
                        logger.error(f"任务目标点位:{point}")
                        self.mouse_move(point[0], point[1], delay_time=1)
                        self.mouse_right_click(point[0], point[1], delay_time=2)
                        logger.error("出口箭头_荒野,点击移动")
                        self.key_press("M", delay_time=2)
                        time.sleep(10)
                        self.queue_screenshot_sync()
                        self.map_piont_flag = True
                        return True

                elif self.find_data_from_keys_list_click(["出口"], self.word_handle_data, action=3, delay_time=2):
                    logger.error("找到出口,点击移动")
                    self.key_press("M", delay_time=2)  # 关闭地图界面
                    time.sleep(10)
                    self.queue_screenshot_sync()
                    self.map_piont_flag = True
                    return True
            elif "主界面" in self.interface_info:
                self.key_press("M", delay_time=2)
                self.queue_screenshot_sync()
                return True


    def task_explore(self):
        if self.map_name in ["破庙","南荒毒沼"] or self.deaths_num >= 5:  # 死亡次数大于5,退出副本
            self.boss_flag = True
            return True

        if self.find_data_from_keys_list_click(["确定", "捕获成功"], self.word_handle_data, delay_time=3):
            logger.error("捕获成功,退出副本")
            self.boss_flag = True
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

        self.task_on_hook()  # 挂机模块

        if self.node_current in ["task_刷怪模块", ]:  # 刷怪模块
            self.task_刷怪模块()
        elif self.node_current in ["task_移动模块", ] or not self.node_current:  # 移动模块
            self.task_移动模块()




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
            'class': ["地图界面"],
        },
        "捕获成功": {
            "scope": (507,367,597,404),
            "con": 0.8,
            "offset": (185,74),
            "use": "悬赏任务",
            "unique": True,
            "enable": True,
            'class': ["主界面"],
        },
        "确定":{
            "scope": (647, 428, 760, 485),
            "con": 0.8,
            "offset": (26, 10),
            "use": "悬赏任务",
            "unique": True,
            "enable": True,
            'class': ["主界面"],
        },
        "离开": {
            "scope": (558,587,633,618),
            "con": 0.8,
            "offset": (0, 0),
            "use": "悬赏任务",
            "enable": True,
            'class': ["主界面"],
        },
        "物品": {
            "scope": (698,439,782,462),
            "con": 0.8,
            "offset": (20, 10),
            "use": "悬赏任务",
            "unique": True,
            "enable": True,
            'class': ["主界面"],
        },
        "奖励": {
            "scope": (698,439,782,462),
            "con": 0.8,
            "offset": (0, 0),
            "use": "悬赏任务",
            "enable": True,
            'class': ["主界面"],
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
            'class': ["地图界面"],
        },  # 奖励图标
        r"resource/images_info/camp_task/地图_npc.bmp": {
            "scope": (1088, 563, 1153, 618),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["地图界面"],
        },  
        r"resource/images_info/other/武将收服.png":{
            "scope":(619, 409, 828, 606),
            "con":0.8,
            "model":1,
            "enable":True,
            "unique": True,
            'class': ["主界面"],
        },#奖励图标
        r"resource/images_info/other/武将_守护.png": {
            "scope": (529, 766, 618, 823),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },
        r"resource/images_info/main_task/任务对话.png": {
            "scope": (547, 579, 657, 635),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },
        "resource/images_info/reward_task/通缉犯.bmp":{
            "scope":target_scope,
            "con":0.8,
            "offset":(16, 123),
            "model":1,
            "enable":True,
            "unique": True,
            'class': ["主界面"],
        },#奖励图标
        "resource/images_info/reward_task/霸山虎.bmp": {
            "scope": target_scope,
            "con": 0.8,
            "offset": (18, 157),
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },  # 奖励图标
        "resource/images_info/reward_task/异族细作.bmp": {
            "scope": target_scope,
            "con": 0.8,
            "offset": (41, 145),
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },  # 奖励图标
        "resource/images_info/reward_task/血路独行.bmp": {
            "scope": target_scope,
            "con": 0.8,
            "offset": (18, 138),
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },  # 奖励图标
        "resource/images_info/reward_task/七窍玲珑.png": {
            "scope": target_scope,
            "con": 0.8,
            "offset": (22, 176),
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },  # 奖励图标
        "resource/images_info/reward_task/不赦死囚.bmp": {
            "scope": target_scope,
            "con": 0.8,
            "offset": (22, 176),
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },  # 奖励图标
    },
}

