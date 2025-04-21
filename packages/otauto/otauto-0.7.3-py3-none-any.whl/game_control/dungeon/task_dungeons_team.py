from game_control.task_explore import Explore #接入探索者模块

"""
功能:副本模块
日期:2025-3-27 21:59:21
描述:
    模块化设计
"""

class TaskDungeonsTeam(Explore):
    """
    任务详情:这里接入任务的具体操作内容
    def task_details(self),所有操作接入这个函数中
    vnc: vnc对象
    vnc_port: vnc端口号
    queue_handle: 队列操作对象
    task_welfare
    """
    def __init__(self,vnc,vnc_port,queue_handle ,dungeons_name:str="长寿宫"):
        super().__init__(vnc,vnc_port,queue_handle,dungeons_name)

    def task_explore(self):
        self.task_on_hook(True)  # 挂机模块
        if self.node_current in ["task_刷怪模块", ]:  # 刷怪模块
            self.task_刷怪模块()
        elif self.node_current in ["task_移动模块", ] or not self.node_current:  # 移动模块
            self.task_移动模块()
        elif self.node_current in ["task_辅助模块", ]:  # 辅助模块
            self.task_辅助模块()


dungeons_team_data={
    "word": {
        42: {
            "scope": (62, 197, 166, 469),  # 左侧组队信息
            "con": 0.8,
            "offset": (0, 0),
            "use": "包裹清理",
            "model": 0,
            "unique": True,
            "enable": True,
        },
        "确定":{
            "scope": (647, 428, 760, 485),
            "con": 0.8,
            "offset": (0, 0),
            "use": "副本",
            "unique": True,
            "enable": True,
            'class': ["主界面"],
        },
        "离开": {
            "scope": (547, 579, 657, 635),
            "con": 0.8,
            "offset": (0, 0),
            "model" :1,
            "use": "副本",
            "enable": True,
            'class': ["主界面"],
        },
        "物品": {
            "scope": (698,439,782,462),
            "con": 0.8,
            "offset": (20, 10),
            "use": "副本",
            "unique": True,
            "enable": True,
            'class': ["主界面"],
        },
        "奖励": {
            "scope": (698,439,782,462),
            "con": 0.8,
            "offset": (0, 0),
            "use": "副本",
            "enable": True,
            'class': ["主界面"],
        },

        "装备": {
            "scope": (943, 302, 1094, 556),
            "con": 0.8,
            "offset": (15,5),
            "use": "副本",
            "unique": True,
            "enable": True,
            'class': ["主界面"],
        },
        "连续按|空格|挣脱控制": {
            "scope": (363, 204, 675, 261),
            "con": 0.8,
            "offset": (15, 5),
            "use": "副本",
            "unique": True,
            "enable": True,
            'class': ["主界面"],
        },
        "金币|物品|玉衡|奖励": {
            "scope": (576, 433, 913, 478),
            "con": 0.8,
            "offset": (15, 5),
            "use": "副本",
            "unique": True,
            "enable": True,
            'class': ["主界面"],
        },
    },
    "image": {
        r"resource/images_info/other/队友标志.bmp": {
            "scope": (296, 159, 1087, 669),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
        },  # 奖励图标
        r"resource/images_info/camp_task/地图_npc.bmp": {
            "scope": (1088, 563, 1153, 618),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["地图界面"],
        },  

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
        },
        r"resource/images_info/other/组队_离队标志.png": {
            "scope": (6, 187, 53, 370),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },
        r"resource/images_info/other/组队_目标少林.png": {
            "scope": (550, 81, 626, 175),
            "con": 0.8,
            "model": 1,
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },
        r"resource/images_info/other/空血槽.png": {
            "scope": (139, 216, 202, 486),
            "con": 0.8,
            "model":0,
            "enable": True,
            "unique": True,
            'class': ["主界面"],
        },
    },
}

