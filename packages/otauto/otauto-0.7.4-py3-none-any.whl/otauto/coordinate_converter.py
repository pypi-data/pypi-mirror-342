import math
from PIL import Image
from loguru import logger
"""
功能:坐标换算
日期:2025-3-8 19:48:32
描述:
    注意,要固定视角,最好2.5d视角
    人物在屏幕中间
    大唐无双是特殊的x,y坐标系,要是其他游戏请在
    coordinate_point_conversion方法里改成
    angle_degrees =angle-45 改成angle_degrees =angle
ai模型对话内容:
    坐标系的原点（0, 0）位于图像的左上角。
    x坐标表示水平方向，y坐标表示垂直方向。
    x值从左到右增加，y值从上到下增加。
    求图片中2点之间的在正常的笛卡尔坐标的度数
    写一个python方法
"""

class CoordinateConverter:
    """
    # 示例用法
    image_path = 'resource/images_info/map_image/tld_color_2.png'
    point_list = [(82, 336), (84, 335), (88, 330), (91, 327)]
    converter = CoordinateConverter(image_path)
    converted_points = converter.process_points(point_list)
    logger.success(f"转换后的地图坐标列表：{converted_points}")
    """
    def __init__(self, image_path, scale=45, x_role=720, y_role=450, x_scene=720, y_scene=450):
        self.image = Image.open(image_path)
        self.image_height = self.image.height
        self.scale = scale
        self.x_role = x_role
        self.y_role = y_role
        self.x_scene = x_scene
        self.y_scene = y_scene

    def calculate_angle_and_length(self, pointA, pointB):
        """
        计算两个点在正常笛卡尔坐标系下的角度和长度。

        :param pointA: 第一个点的坐标 (x1, y1)
        :param pointB: 第二个点的坐标 (x2, y2)
        :return: 角度（度），长度（单位：像素）
        """
        x1, y1 = pointA
        x2, y2 = pointB

        # 转换y坐标
        y1_transformed = self.image_height - y1
        y2_transformed = self.image_height - y2

        # 计算长度
        length = math.sqrt((x2 - x1) ** 2 + (y2_transformed - y1_transformed) ** 2)

        # 计算斜率
        delta_y = y2_transformed - y1_transformed
        delta_x = x2 - x1

        # 计算角度
        if delta_x == 0:  # 避免除以零
            angle = 90.0 if delta_y > 0 else 270.0
        else:
            angle = math.degrees(math.atan2(delta_y, delta_x))

        # 确保角度在0到360度之间
        if angle < 0:
            angle += 360

        return angle, length

    def coordinate_point_conversion(self, pointA, pointB, debug=False):
        """
        换算游戏坐标和屏幕坐标之间的关系

        :param pointA: 第一个点的坐标 (x1, y1)
        :param pointB: 第二个点的坐标 (x2, y2)
        :param debug: 是否开启调试
        :return: (x,y)角色在场景中的移动位置
        """
        angle, distance = self.calculate_angle_and_length(pointA, pointB)
        length = distance * self.scale
        angle_degrees = angle
        angle_radians = math.radians(angle_degrees)

        x = length * math.cos(angle_radians)  # x方向的长度
        y = length * math.sin(angle_radians)  # y方向的长度

        # 计算新的坐标
        if self.x_scene > abs(x) and self.y_scene > abs(y):  # 如果x,y移动距离超过场景限制，则不执行
            x_destination = self.x_role + x  # 计算后的坐标
            y_destination = self.y_role - y  # 计算后的坐标
        elif self.x_scene < abs(x) or self.y_scene < abs(y):  # 说明实时坐标识别错误，则不执行
            return -1, -1

        if debug:
            logger.success(f"线长度: {distance:.2f}")
            logger.success(f"与x轴的角度: {angle:.2f}")
            logger.success(f"x,y移动距离: ({x:.2f}, {y:.2f})")
            logger.success(f"屏幕坐标: ({x_destination:.2f}, {y_destination:.2f})")

        return int(x_destination + 0.5), int(y_destination + 0.5)

    def process_points(self, point_list):
        """
        处理点列表，计算相邻点之间的角度和长度，并转换坐标

        :param point_list: 点列表
        :return: 转换后的地图坐标列表
        """
        results = []
        for i in range(len(point_list) - 1):
            pointA = point_list[i]
            pointB = point_list[i + 1]
            res = self.coordinate_point_conversion(pointA, pointB, debug=True)
            results.append(res)
        return results

