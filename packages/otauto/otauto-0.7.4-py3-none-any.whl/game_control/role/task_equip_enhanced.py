import re
import time

from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块
import cv2
import numpy as np
from PIL import Image
from resource.parameters_info.basic_parameter_info import gear_name_point_dict, gear_name_cope_dict  # 导入装备位置范围


class ImageDifferenceFinder:
    def __init__(self, image1_array, image2_array):
        # 将NumPy数组转换为OpenCV格式（BGR）
        self.image1 = cv2.cvtColor(image1_array, cv2.COLOR_RGB2BGR)
        self.image2 = cv2.cvtColor(image2_array, cv2.COLOR_RGB2BGR)

        if self.image1 is None or self.image2 is None:
            raise ValueError("无法加载图像，请检查输入数组。")

    def find_differences(self, x1, y1, x2, y2, min_area=100):
        # 确保两张图像的大小一致
        if self.image1.shape != self.image2.shape:
            raise ValueError("两张图像的大小不一致。")

        # 裁剪指定区域
        cropped_image1 = self.image1[y1:y2, x1:x2]
        cropped_image2 = self.image2[y1:y2, x1:x2]

        # 计算图像差异
        diff = cv2.absdiff(cropped_image1, cropped_image2)
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # 应用阈值以二值化差异图
        _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)

        # 找到轮廓
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 存储符合条件的不同区域
        different_areas = []

        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= min_area:
                x, y, w, h = cv2.boundingRect(contour)
                # 调整坐标到原图的位置
                different_areas.append((x + x1, y + y1, w, h, area))

        return different_areas

    def draw_differences(self, different_areas):
        # 在第一张图像上绘制不同区域
        output_image = self.image1.copy()
        for (x, y, w, h, area) in different_areas:
            cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 绿色矩形框
        return output_image


# # 示例用法
# if __name__ == "__main__":
#     # 从文件读取图像并转换为PIL图像
#     image1 = Image.open('resource/images_info/demo/2025-03-06-165217.png')  # 图像1
#     image2 = Image.open('resource/images_info/demo/2025-03-06-170346.png')  # 图像2
#
#     # 将PIL图像转换为NumPy数组
#     image1_array = np.array(image1)
#     image2_array = np.array(image2)
#
#     # 创建图像差异查找器
#     finder = ImageDifferenceFinder(image1_array, image2_array)
#
#     # 指定要比较的区域 (x1, y1, x2, y2)
#     x1, y1, x2, y2 = 419, 234, 1201, 655  # 请根据需要修改这个区域
#     # 找到不同的区域，最小面积为100
#     differences = finder.find_differences(x1, y1, x2, y2, min_area=100)
#
#     if differences:
#         print(f"找到 {len(differences)} 个不同区域：")
#         for diff in differences:
#             print(f"位置: {diff[:4]}, 面积: {diff[4]}")
#
#         # 绘制不同区域
#         output_image = finder.draw_differences(differences)
#
#         # 显示结果
#         cv2.imshow('Differences', output_image)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#     else:
#         print("未找到不同区域。")

class TaskEquipEnhanced(TaskLogic):
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
        self.node_materials_flag = False #定义一个标志位，用于判断材料是否进入节点
        self.organize_backpack_flag = False  #定义一个标志位，用于判断是否进入整理
        self.material_info={}  # 定义一个空字典，用于存储材料信息
        self.eqiup_list = [] # 定义一个空列表，用于存储可以强化的装备信息
        self.node_flag= False #定义一个标志位，用于判断是否进入节点
        self.eqiup_numpy = None #定义一个空列表，用于numpy数组信息
        self.scope_背包=None #定义一个空元组，用于存储背包范围的坐标
        self.equip_position = None #定义一个空元组，用于存储装备的位置信息
        self.gear_type = None # 当前任务信息
        self.next_task= None # 用于存储下一个任务的信息
        self.num_enhance = 0  # 强化次数
        self.node_info_flag = False #装备详情标志位
        self.ready_flag = False  #装备强化已经准备完成
        self.intensify_op_flag = False # 强化操作标志位

    def hex_to_rgb(self,hex_color):
        """将十六进制颜色转换为 RGB 格式"""
        hex_color = hex_color.lstrip('#')  # 移除前导的 '#' 符号
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))  # 转换为 RGB

    def color_exists_in_array(self, color_array,color_hex:str="#a335ee", tolerance=20):
        """检查指定颜色是否存在于 NumPy 数组中，允许一定的容差"""
        # 将十六进制颜色转换为 RGB
        target_color = np.array(self.hex_to_rgb(color_hex), dtype=np.uint8)
        # 计算颜色差异
        color_diff = np.abs(color_array.astype(np.int16) - target_color.astype(np.int16))  # 使用 int16 防止溢出
        # 检查颜色差异是否在容差范围内
        return np.any(np.all(color_diff <= tolerance, axis=-1))

    def task_背包范围识别(self):
        """
        识别背包范围
        """
        if self.node_counter>=5:#如果超过5次,则放弃任务
            self.node_current="task_强化完成"
            self.node_counter=0 #重置节点计数器
            return "task_finish"

        if "背包界面" in self.interface_info:
            res_dict=self.find_data_from_keys_list(["resource/images_info/equipment_strengthening/激战.png","resource/images_info/equipment_strengthening/整理.png"],self.image_data)
            """
            {'resource/images_info/equipment_strengthening/激战.png': {'scope': [(917, 377, 940, 409, 1.0)], 'enable': True, 'unique': True, 'model': 1}, 
            'resource/images_info/equipment_strengthening/整理.png': {'scope': [(1143, 672, 1161, 709, 1.0)], 'enable': True, 'unique': True, 'model': 1}}
            """
            if res_dict and len(res_dict)==2: #如果识别到两个图标
                top_left_ls=res_dict.get('resource/images_info/equipment_strengthening/激战.png')
                x1,y1=top_left_ls.get("scope")[0][0]-286,top_left_ls.get("scope")[0][1]+39
                bottom_right_ls=res_dict.get('resource/images_info/equipment_strengthening/整理.png')
                x2,y2=bottom_right_ls.get("scope")[0][0]+28,bottom_right_ls.get("scope")[0][1]-108
                self.scope_背包=(x1,y1,x2,y2)
                self.node_current="task_武器强化部分查询"
                return True

        elif "主界面" in self.interface_info:
            self.key_press("B",delay_time=1)

        self.node_counter+=1 #节点计数器加1

    def task_强化材料查询(self):
        """
        查看背包里是否有强化材料
        根据强化材料和装备情况分类进行操作
        """
        self.node_current = "task_强化材料查询"

        if self.node_counter>=8:#如果超过5次,则放弃任务
            self.node_current="task_强化完成"
            self.node_counter=0 #重置节点计数器
            return "task_finish"

        if "背包界面" in self.interface_info:
            if not self.organize_backpack_flag:
                logger.error("整理背包")
                self.find_data_from_keys_list_click(["resource/images_info/equipment_strengthening/整理.png"],self.image_data,delay_time=2)
                self.organize_backpack_flag = True
                self.node_counter=0 #重置节点计数器
                return True
            elif self.organize_backpack_flag:
                self.eqiup_numpy = self.data_numpy  # 保存numpy数组信息
                self.material_info=self.find_data_from_keys_list(["破月", "追星", "龙睛","凤瞳"], self.image_data)
                logger.info(f"材料查询结果:{self.material_info}")
                """
                {'resource/images_info/equipment_strengthening/凤瞳.bmp': {'scope': [(1096, 426, 1108, 450, 0.98)], 'enable': True, 'unique': True, 'model': 1}, 
                'resource/images_info/equipment_strengthening/破月.bmp': {'scope': [(1134, 430, 1153, 451, 0.945)], 'enable': True, 'unique': True, 'model': 1}, 
                'resource/images_info/equipment_strengthening/追星.bmp': {'scope': [(1030, 429, 1049, 449, 0.979)], 'enable': True, 'unique': True, 'model': 1},
                "resource/images_info/equipment_strengthening/龙睛.bmp": {'scope': [(1063, 431, 1089, 444, 0.994)], 'enable': True, 'unique': True, 'model': 1},
                """
                if self.material_info:
                    """不同的材料强化部分不一样"""
                    for key, value in self.material_info.items():
                        if "追星" in key : #武器0~3强化
                            self.eqiup_list.append("lower_武器")
                        if "破月" in key: # 武器4~7强化
                            self.eqiup_list.append("upper_武器")
                        if "龙睛" in key: #防具0~3强化
                            self.eqiup_list.append("lower_防具")
                        if "凤瞳" in key: #防具4~7强化
                            self.eqiup_list.append("upper_防具")
                if self.eqiup_list: #存在装备可以强化的列表
                    self.node_current=f"task_{self.gear_type}强化部分查询"
                    self.interface_closes()
                    self.organize_backpack_flag = False # 重置整理标志位
                    self.node_materials_flag= True # 材料标志位
                    return True

        elif "角色信息界面" in self.interface_info:
            self.key_press("C",delay_time=1)

        elif "主界面" in self.interface_info:
            self.key_press("B", delay_time=1)

        self.node_counter += 1  # 增加节点计数器

    def task_装备强化部分查询(self, gear_type, next_task):
        """
        根据装备类型和下一个任务进行操作
        """
        self.gear_type=gear_type # 设置当前任务
        self.next_task = next_task # 设置下一个任务
        self.node_current = f"task_{gear_type}强化部分查询"

        logger.error(f"{gear_type}强化部分查询")

        if self.node_counter >= 8:  # 如果超过5次,则放弃任务
            self.node_current = next_task
            self.node_counter = 0  # 重置节点计数器
            return "task_finish"
        elif not self.node_materials_flag:
            self.task_强化材料查询()

        elif self.node_materials_flag:
            if "角色信息界面" in self.interface_info:
                logger.error(f"可以强化的装备信息:{self.eqiup_list}")
                # 只对武器和防具进行判断
                if gear_type == "武器":
                    if "lower_武器" in self.eqiup_list or "upper_武器" in self.eqiup_list:  # 有武器强化的材料
                        self._process_装备强化(gear_type, next_task)
                    else:
                        self.node_current=self.next_task
                        return True

                elif gear_type in ["头盔","衣服","护手","腰带","鞋子"]:
                    if "lower_防具" in self.eqiup_list or "upper_防具" in self.eqiup_list:  # 有防具强化的材料
                        self._process_装备强化(gear_type, next_task)
                    else:
                        self.node_current ="task_强化完成"
                        return True

            elif "主界面" in self.interface_info:
                self.key_press("c", delay_time=1)

        self.node_counter += 1

    def _process_装备强化(self, gear_type, next_task):
        if self.node_info_flag:
            res_list = self.find_word_scope(*equip_scope_details[gear_type], model=1)
            x1,y1,x2,y2=equip_scope_details[gear_type]
            color_numpy=self.data_numpy[y1:y2, x1:x2] #识别颜色的区域
            logger.info(f"{gear_type}强化等级:{res_list}")
            pattern = r'^[\u4e00-\u9fa5]+$'  # +1,+3,或者全是中文
            if res_list and self.color_exists_in_array(color_numpy): # 如果是紫装
                for res in res_list:
                    gear_name = res[0]
                    if re.match(pattern, gear_name) or re.search(r'\+\d', gear_name):
                        self.mouse_right_click(*gear_name_point_dict[gear_type], delay_time=1)  # 装备取下
                        self.interface_closes()
                        self.node_current = "task_装备强化"
                        self.node_info_flag = False # 装备点位
                        self.node_materials_flag = False  # 重置标志位, 材料
                        return "task_finish"
            else:  # 如果没有强化等级,则放弃任务
                logger.error(f"未能找到当前{gear_type}强化等级,下一个")
                self.node_current = next_task
                self.node_info_flag = False # 装备点位
                self.node_materials_flag= False # 重置标志位, 材料
                self.node_counter=0 # 重置节点计数器

        elif not self.node_info_flag:
            logger.error(f"装备点位:{gear_name_point_dict[gear_type]}")
            self.mouse_move(*gear_name_point_dict[gear_type], delay_time=2)
            self.node_info_flag = True
            return True

    def task_武器强化部分查询(self):
        self.task_装备强化部分查询("武器", "task_头盔强化部分查询")

    def task_头盔强化部分查询(self):
        self.task_装备强化部分查询("头盔", "task_衣服强化部分查询")

    def task_衣服强化部分查询(self):
        self.task_装备强化部分查询("衣服", "task_护手强化部分查询")

    def task_护手强化部分查询(self):
        self.task_装备强化部分查询("护手", "task_腰带强化部分查询")

    def task_腰带强化部分查询(self):
        self.task_装备强化部分查询("腰带", "task_鞋子强化部分查询")

    def task_鞋子强化部分查询(self):
        self.task_装备强化部分查询("鞋子", "task_强化完成")

    def task_装备强化(self):

        if self.node_counter >=8:  # 如果超过5次,则放弃任务
            self.node_current = "task_强化完成"
            self.node_counter = 0  # 重置节点计数器
            return "task_finish"

        if self.intensify_op_flag: # 开始强化
            if self.ready_flag:
                logger.error("测试点3")
                if "背包界面" in self.interface_info:
                    self.mouse_right_click(*self.equip_position, delay_time=3)  # 穿上装备
                    self.find_data_from_keys_list_click(["resource/images_info/equipment_strengthening/整理.png"],
                                                        self.image_data, delay_time=2)
                    self.node_current = self.next_task  # 下一个任务节点
                    self.node_counter = 0  # 重置节点计数器
                    self.ready_flag = False  # 重置
                    self.intensify_op_flag= False # 重置
                    self.eqiup_list = []  # 重置装备列表
                    return "task_finish"
                elif "主界面" in self.interface_info:
                    self.key_press("B", delay_time=1)

            elif not self.ready_flag:
                logger.error("测试点2")
                if "装备强化界面" in self.interface_info or self.find_data_from_keys_list(["欢迎光临"],
                                                                                          self.word_handle_data):
                    x1, y1 = self.interface_info.get("装备强化界面")
                    self.mouse_left_click(x1 - 110, y1, delay_time=1)
                    logger.error(f"装备强化界面")
                    if self.num_enhance >= 4:
                        logger.warning("装备强化次数到预定值,停止")
                        self.interface_closes()  # 关闭界面
                        self.num_enhance = 0  # 重置次数
                        self.node_counter = 0  # 重置节点计数器
                        self.ready_flag = True
                    elif self.find_data_from_keys_list_click(["95%", "65%"], self.word_handle_data, delay_time=3):
                        self.node_counter = 0  # 重置节点计数器
                        self.num_enhance += 1  # 增加强化次数
                        logger.info("装备强化界面,强化中")
                    elif self.find_data_from_keys_list_click(
                            ["resource/images_info/equipment_strengthening/无材料.png"], self.image_data, x3=208, y3=82,
                            delay_time=1):
                        logger.warning("装备强化界面,无材料")
                        self.node_counter = 0  # 重置节点计数器
                        self.num_enhance = 0  # 重置次数
                        self.ready_flag = True  # 重置标志位
                        return True
        elif not self.intensify_op_flag: # 强化前准备工作
            logger.error("强化前准备工作")
            if self.equip_position: # 如果装备位存在
                if "装备强化界面" in self.interface_info:
                    self.intensify_op_flag = True
                    return True
                elif "背包界面" in self.interface_info:
                    if self.find_data_from_keys_list_click(["resource/images_info/equipment_strengthening/强化图标.png"],self.image_data,x3=10,y3=15,delay_time=1):
                        logger.error("把装备放入强化界面")
                        self.mouse_left_click(977,359,delay_time=1) #背包前置
                        self.mouse_right_click(*self.equip_position, delay_time=1) #丢入装备
                        self.mouse_left_click(770,198,delay_time=1) # 进阶前置
                        self.key_press("B")
                        self.node_counter = 0  # 重置节点计数器
                        return True
                elif "主界面" in self.interface_info:
                    self.key_press("B", delay_time=1)
                    self.node_counter =0
                    return True
            elif not  self.equip_position: # 找出装备位置
                if "背包界面" in self.interface_info:
                    # 创建图像差异查找器
                    finder = ImageDifferenceFinder(self.eqiup_numpy, self.data_numpy)
                    # 找到不同的区域，最小面积为100
                    differences = finder.find_differences(*self.scope_背包, min_area=100)
                    logger.info(f"装备位置:{differences}")
                    self.node_counter = 0  # 重置节点计数器
                    #[(1026, 493, 28, 28, 637.0)]
                    if differences:
                        self.equip_position=differences[0][0]+15,differences[0][1]+15
                elif "主界面" in self.interface_info:
                    self.key_press("B", delay_time=1)
                    return True

        self.node_counter+=1 # 增加节点计数器


    def task_强化完成(self):
        if "主界面" in self.interface_info:
            self.ls_progress="task_finish"
            return "task_finish"
        else:
            self.interface_closes()

    def handle_task(self):
        task_methods = {
            "task_背包范围识别": self.task_背包范围识别,
            'task_强化材料查询':self.task_强化材料查询,
            'task_武器强化部分查询': self.task_武器强化部分查询,
            'task_头盔强化部分查询': self.task_头盔强化部分查询,
            'task_衣服强化部分查询': self.task_衣服强化部分查询,
            'task_护手强化部分查询': self.task_护手强化部分查询,
            'task_腰带强化部分查询': self.task_腰带强化部分查询,
            'task_鞋子强化部分查询': self.task_鞋子强化部分查询,
            'task_装备强化': self.task_装备强化,
            'task_强化完成': self.task_强化完成,
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
        logger.error(f"装备信息状态:{self.node_info_flag}")
        logger.error(f"装备强化状态:{self.node_flag}")
        logger.error(f"准备状态:{self.ready_flag}")

        if not self.node_current:
            self.task_背包范围识别()
        elif self.handle_task():
            pass

#背包中识别的范围
equip_scope_背包=(419, 234, 1201, 727)
#装备的详细说明
equip_scope_details={
    "武器": (623, 325, 812, 381),
    "头盔": (621, 376, 761, 428),
    "衣服": (615, 421, 732, 479),
    "护手": (585, 99, 731, 151),
    "腰带": (583, 146, 701, 202),
    "鞋子": (617, 192, 735, 249),
}

equip_enhanced_data={
    "word": {
        "95%": {
            "scope": (565, 574, 842, 615),
            "con": 0.8,
            "model":1,
            "offset": (-55, 51),
            "use": "装备强化",
            "unique": True,
            "enable": True,
        },
        "65%": {
            "scope": (565, 574, 842, 615),
            "con": 0.8,
            "model": 1,
            "offset": (-45, 61),
            "use": "装备强化",
            "unique": True,
            "enable": True,
        },
        "欢迎光临":{
            "scope": (541, 194, 882, 253),
            "con": 0.8,
            "offset": (0, 0),
            "model": 1,
            "use": "装备强化",
            "enable":True,
        },#每日签到

    },
    "image": {
        r"resource/images_info/equipment_strengthening/凤瞳.bmp":{
            "scope":equip_scope_背包,
            "con":0.8,
            "enable":True,
            "unique": True,
            "model":1,
        },
        r"resource/images_info/equipment_strengthening/星级.bmp":{
            "scope":equip_scope_背包,
            "con":0.8,
            "enable":True,
            "unique": True,
            "model":1,
        },
        r"resource/images_info/equipment_strengthening/破月.bmp":{
            "scope":equip_scope_背包,
            "con":0.8,
            "enable":True,
            "unique": True,
            "model":1,
        },
        r"resource/images_info/equipment_strengthening/追星.bmp":{
            "scope":equip_scope_背包,
            "con":0.8,
            "enable":True,
            "unique": True,
            "model":1,
        },
        r"resource/images_info/equipment_strengthening/龙睛.bmp":{
            "scope":equip_scope_背包,
            "con":0.8,
            "enable":True,
            "unique": True,
            "model":1,
        },
        r"resource/images_info/equipment_strengthening/激战.png": {
            "scope": equip_scope_背包,
            "con": 0.8,
            "enable": True,
            "unique": True,
            "model": 1,
        },
        r"resource/images_info/equipment_strengthening/整理.png": {
            "scope": equip_scope_背包,
            "con": 0.8,
            "enable": True,
            "unique": True,
            "model": 1,
        },
        r"resource/images_info/equipment_strengthening/强化图标.png": {
            "scope": equip_scope_背包,
            "con": 0.8,
            "enable": True,
            "unique": True,
            "model": 1,
        },
        r"resource/images_info/equipment_strengthening/无材料.png": {
            "scope": (555, 524, 707, 612),
            "con": 0.8,
            "enable": True,
            "unique": True,
            "model":1,
        },
    },
}