from PIL import Image, ImageDraw
import heapq
import math
from  loguru import logger

"""
功能:A星算法
日期:2025-3-8 12:48:18
功能:
    1 拼接地图
    2 用颜色标识可通行区域
    3 用颜色标识最佳路线
ai模型对话内容:
    image_path = r"D:\pc_work\pc_script\resource\images_info\map_image\tld_color_1.png"
    output_path = r"D:\pc_work\pc_script\route_image.png"
    start = (83, 333)
    goal = (387, 80)
    walkable_colors = ["6ec8fa", "70c8fa", "ff0000","D53948","B26A84"]
    route_color = ["ff0000","D53948","B26A84"] 添加惩罚机制，该颜色具有更低的通行成本
    tolerance = 30  # 颜色容差值
    写一个a星算法,python类
    image_path为图片路径
    output_path为保存结果图片路径
    start 起点
    goal 终点
    walkable_colors 可通行的颜色
    route_color = ["ff0000","D53948","B26A84"] 路线最佳选择的颜色值
    tolerance  颜色容差值
    返回值为路线的坐标点
    代码加上中文说明和参数注释
    参数需要有注释,说明
"""

class PathFinder:
    """
    # 示例用法
    if __name__ == "__main__":
        # 创建 PathFinder 实例
        path_finder = PathFinder()

        # 设置图像路径、起点、终点、目标颜色和路线颜色
        image_path = r"D:\pc_work\pc_script\resource\images_info\map_image\tld_color_2.png"
        start = (83, 333)
        goal = (387, 80)
        target_colors_hex = ["6ec8fa", "70c8fa", "e02a35", "d23d4d", "9b8aad"]  # 允许通行的颜色
        route_color = ["e02a35", "d23d4d", "9b8aad"]  # 惩罚值最低的颜色
        output_image_path = r"D:\pc_work\pc_script\route_image.png"

        # 查找路径并绘制结果
        path = path_finder.find_path(image_path, start, goal, target_colors_hex, route_color, tolerance=30, output_image_path=output_image_path, debug=True)

        # 输出结果
        if path:
            print("找到路径:", path)
        else:
            print("没有找到路径")
    """
    def __init__(self):
        """初始化 PathFinder 类的实例，不需要参数"""
        pass

    @staticmethod
    def hex_to_rgb(hex_color):
        """将十六进制颜色转换为RGB格式"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def load_image(self, image_path):
        """加载图像并转换为RGB格式"""
        try:
            img = Image.open(image_path)
            return img.convert('RGB')  # 确保图像是RGB格式
        except Exception as e:
            print(f"无法打开图像: {e}")
            return None

    def is_color_within_tolerance(self, pixel_color, target_color, tolerance):
        """判断像素颜色是否在目标颜色的容差范围内"""
        return all(abs(pc - tc) <= tolerance for pc, tc in zip(pixel_color, target_color))

    def get_color_cost(self, pixel_color, route_colors_rgb, high_cost=10, low_cost=1, tolerance=30):
        """根据颜色返回代价
        :param pixel_color: 当前像素的RGB颜色
        :param route_colors_rgb: 允许通行的颜色列表（RGB格式）
        :param high_cost: 不允许通行的颜色的代价（默认10）
        :param low_cost: 允许通行的颜色的代价（默认1）
        :param tolerance: 颜色容差
        :return: 返回该像素的代价
        """
        if any(self.is_color_within_tolerance(pixel_color, color, tolerance) for color in route_colors_rgb):
            return low_cost  # 低代价
        return high_cost  # 高代价

    def heuristic(self, a, b):
        """计算启发式代价（欧几里得距离）
        :param a: 点A的坐标
        :param b: 点B的坐标
        :return: 返回A点到B点的距离
        """
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def a_star_search(self, img, start, goal, target_colors_rgb, route_colors_rgb, tolerance):
        """执行A*搜索算法
        :param img: 要处理的图像
        :param start: 起点坐标 (x, y)
        :param goal: 终点坐标 (x, y)
        :param target_colors_rgb: 允许通行的颜色列表（RGB格式）
        :param route_colors_rgb: 允许通行的颜色（惩罚值最低的颜色）
        :param tolerance: 颜色容差
        :return: 返回从起点到终点的路径列表，如果找不到路径则返回空列表
        """
        width, height = img.size
        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                path = []
                while current != start:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)

                if 0 <= neighbor[0] < width and 0 <= neighbor[1] < height:
                    pixel_color = img.getpixel(neighbor)

                    if any(self.is_color_within_tolerance(pixel_color, target_color, tolerance) for target_color in target_colors_rgb):
                        # 获取颜色代价
                        color_cost = self.get_color_cost(pixel_color, route_colors_rgb, tolerance=tolerance)
                        new_cost = cost_so_far[current] + color_cost

                        if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                            cost_so_far[neighbor] = new_cost
                            priority = new_cost + self.heuristic(goal, neighbor)
                            heapq.heappush(open_list, (priority, neighbor))
                            came_from[neighbor] = current

        return []  # 如果没有找到路径，返回空列表

    def find_path(self, image_path, start, goal, target_colors_hex, route_color_hex, tolerance=30, output_image_path=None, debug=False):
        """查找路径并绘制在图像上
        :param image_path: 图像文件路径
        :param start: 起点坐标 (x, y)
        :param goal: 终点坐标 (x, y)
        :param target_colors_hex: 允许通行的目标颜色列表（十六进制格式）
        :param route_color_hex: 允许通行的颜色（惩罚值最低的颜色，十六进制格式）
        :param tolerance: 颜色容差（默认30）
        :param output_image_path: 输出图像的路径，如果提供则保存结果图像
        :param debug: 是否在图像上绘制路径（默认False）
        :return: 返回从起点到终点的路径列表，如果找不到路径则返回空列表
        """
        # 加载图像
        img = self.load_image(image_path)
        if img is None:
            return []

        # 将目标颜色和路线颜色转换为 RGB 格式
        target_colors_rgb = [self.hex_to_rgb(color) for color in target_colors_hex]
        route_colors_rgb = [self.hex_to_rgb(color) for color in route_color_hex]

        # 执行 A* 搜索
        path = self.a_star_search(img, start, goal, target_colors_rgb, route_colors_rgb, tolerance)

        if debug and path:
            draw = ImageDraw.Draw(img)
            for point in path:
                draw.point(point, fill=(255, 0, 0))  # 绘制红色路径

            # 保存或显示结果图像
            if output_image_path:
                img.save(output_image_path)
                logger.success(f"路径已绘制并保存到 {output_image_path}")
            else:
                img.show()

        return path

