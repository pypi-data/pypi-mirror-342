import math
import heapq
from PIL import Image, ImageDraw
from otauto.log import ColoredLogger
logger = ColoredLogger()
# 移除日志
logger.remove()

"""
功能: A星寻路 ,带参考路径
日期: 2025-3-24 21:23:16
描述:
    1 拼接地图
    2 用颜色标识最佳路线
    3 允许通行的颜色
    4 惩罚值最低的颜色
    5 惩罚颜色
"""

class PathFinder:
    """
    路径寻找器类，使用 A* 算法在图像中寻找从起点到终点的路径。
    示例用法：
    if __name__ == "__main__":
        path_finder = PathFinder()

        # 设置图像路径、起点、终点、目标颜色和路线颜色
        image_path = r"D:\pc_work\pc_script-pypi\resource\images_info\map_image\way_demo.png"
        start = (200, 425)  # 起点坐标
        goal = (166, 401)   # 终点坐标
        target_colors_hex = ["6ec8fa"]  # 允许通行的颜色
        route_color_hex = ["ff00fe"]  # 惩罚值最低的颜色
        penalty_color_hex = "00ff7f"  # 惩罚颜色
        output_image_path = r"D:\pc_work\pc_script-pypi\route_image.png"

        path = path_finder.find_path(
            image_path,
            start,
            goal,
            target_colors_hex,
            route_color_hex,
            penalty_color_hex,
            tolerance=30,
            output_image_path=output_image_path,
            debug=True
        )

        if path:
            logger.info("找到路径:", path)
        else:
            logger.info("没有找到路径")
    """

    def __init__(self):
        """初始化 PathFinder 类的实例，不需要参数"""
        pass

    @staticmethod
    def hex_to_rgb(hex_color):
        """将十六进制颜色转换为 RGB 格式
        :param hex_color: 十六进制颜色字符串（例如：'#ff0000'）
        :return: RGB 颜色元组 (r, g, b)
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def load_image(self, image_path):
        """加载图像并转换为 RGB 格式
        :param image_path: 图像文件路径
        :return: 转换后的 RGB 图像对象
        """
        try:
            img = Image.open(image_path)
            return img.convert('RGB')  # 确保图像是 RGB 格式
        except Exception as e:
            logger.info(f"无法打开图像: {e}")
            return None

    def is_color_within_tolerance(self, pixel_color, target_color, tolerance):
        """判断像素颜色是否在目标颜色的容差范围内
        :param pixel_color: 当前像素颜色 (r, g, b)
        :param target_color: 目标颜色 (r, g, b)
        :param tolerance: 颜色容差
        :return: 如果在容差范围内返回 True，否则返回 False
        """
        return all(abs(pc - tc) <= tolerance for pc, tc in zip(pixel_color, target_color))

    def get_color_cost(self, pixel_color, route_colors_rgb, penalty_color_rgb=None, high_cost=10, low_cost=1,
                       penalty_scale=10, tolerance=30):
        """根据颜色返回代价
        :param pixel_color: 当前像素颜色 (r, g, b)
        :param route_colors_rgb: 允许通行的颜色列表（RGB 格式）
        :param penalty_color_rgb: 惩罚颜色（RGB 格式）
        :param high_cost: 高代价值
        :param low_cost: 低代价值
        :param penalty_scale: 惩罚比例
        :param tolerance: 颜色容差
        :return: 计算得出的代价
        """
        if any(self.is_color_within_tolerance(pixel_color, color, tolerance) for color in route_colors_rgb):
            return low_cost  # 低代价

        # 计算与惩罚颜色的欧几里得距离
        if penalty_color_rgb:
            distance_to_penalty_color = sum(
                abs(pc - pc_penalty) for pc, pc_penalty in zip(pixel_color, penalty_color_rgb))
            penalty = penalty_scale / (distance_to_penalty_color + 1)  # 避免除以零
            return high_cost + penalty

        return high_cost

    def heuristic(self, a, b):
        """计算启发式代价（欧几里得距离）
        :param a: 点 A 的坐标 (x, y)
        :param b: 点 B 的坐标 (x, y)
        :return: 返回 A 点到 B 点的距离
        """
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def a_star_search(self, img, start, goal, target_colors_rgb, route_colors_rgb, penalty_color_rgb, tolerance):
        """执行 A* 搜索算法
        :param img: 要处理的图像
        :param start: 起点坐标 (x, y)
        :param goal: 终点坐标 (x, y)
        :param target_colors_rgb: 允许通行的颜色列表（RGB 格式）
        :param route_colors_rgb: 允许通行的颜色（惩罚值最低的颜色）
        :param penalty_color_rgb: 惩罚颜色（RGB 格式）
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
                        color_cost = self.get_color_cost(pixel_color, route_colors_rgb, penalty_color_rgb, tolerance=tolerance)
                        new_cost = cost_so_far[current] + color_cost

                        if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                            cost_so_far[neighbor] = new_cost
                            priority = new_cost + self.heuristic(goal, neighbor)
                            heapq.heappush(open_list, (priority, neighbor))
                            came_from[neighbor] = current

        return []  # 如果没有找到路径，返回空列表

    def find_nearest_route_color(self, img, start, route_colors_rgb, tolerance=30):
        """找到距离 start 最近的 route_color_hex 颜色点
        :param img: 要处理的图像
        :param start: 起点坐标 (x, y)
        :param route_colors_rgb: 允许通行的颜色列表（RGB 格式）
        :param tolerance: 颜色容差
        :return: 最近的 route_color_hex 颜色点坐标，如果找不到则返回 None
        """
        width, height = img.size
        queue = [(0, start)]  # BFS 队列
        visited = set()

        while queue:
            cost, current = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)

            pixel_color = img.getpixel(current)
            if any(self.is_color_within_tolerance(pixel_color, color, tolerance) for color in route_colors_rgb):
                logger.info(f"找到最近的 route_color_hex 颜色点: {current}")  # Debug 输出
                return current  # 找到最近的 route_color_hex 颜色点

            # 遍历邻居
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),  # 上下左右
                           (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # 对角线
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < width and 0 <= neighbor[1] < height and neighbor not in visited:
                    heapq.heappush(queue, (cost + 1, neighbor))

        logger.info(f"未找到 {start} 附近的 route_color_hex 颜色点")  # Debug 输出
        return None  # 找不到 route_color_hex 颜色区域

    def draw_path_on_image(self, img, path, output_image_path):
        """在图像上绘制路径
        :param img: 要处理的图像
        :param path: 路径坐标列表
        :param output_image_path: 输出图像文件路径
        """
        draw = ImageDraw.Draw(img)
        for point in path:
            draw.point(point, fill=(0, 0, 255))  # 蓝色路径

        if output_image_path:
            img.save(output_image_path)
            logger.info(f"路径已绘制并保存到 {output_image_path}")
        else:
            img.show()

    def remove_collapsed_points(self,points):
        """删除路径中可能的折叠点
        :param points: 原始路径列表
        :return: 去除折叠点后的新路径列表
        """
        i = 0
        while i < len(points) - 1:
            found = False  # 用于标记是否找到符合条件的点
            for h in range(i + 2, len(points)):  # 检查所有后续点
                if (abs(points[i][0] - points[h][0]) == 0 and abs(points[i][1] - points[h][1]) <= 1) or \
                        (abs(points[i][0] - points[h][0]) == 1 and abs(points[i][1] - points[h][1]) <= 0):
                    del points[i + 1:h]  # 删除不符合条件的点
                    found = True  # 标记已找到符合条件的点
                    break  # 退出内层循环，重新开始外层循环
            if not found:
                i += 1  # 如果没有找到符合条件的点，则移动到下一个点
        return points  # 返回处理后的点列表


    def find_path(self, image_path, start, goal, target_colors_hex, route_color_hex, penalty_color_hex, tolerance=50,
                  output_image_path=None, debug=False):
        """查找路径并绘制在图像上
        :param image_path: 图像文件路径
        :param start: 起点坐标 (x, y)
        :param goal: 终点坐标 (x, y)
        :param target_colors_hex: 允许通行的颜色列表（十六进制格式）
        :param route_color_hex: 路线颜色（十六进制格式）
        :param penalty_color_hex: 惩罚颜色（十六进制格式）
        :param tolerance: 颜色容差
        :param output_image_path: 输出图像文件路径
        :param debug: 是否启用调试模式（绘制路径）
        :return: 从起点到终点的路径列表，如果找不到路径则返回空列表
        """
        # 1. 加载图像
        img = self.load_image(image_path)
        if img is None:
            return []

        # 2. 颜色转换
        target_colors_rgb = [self.hex_to_rgb(color) for color in target_colors_hex]
        route_colors_rgb = [self.hex_to_rgb(color) for color in route_color_hex]
        penalty_color_rgb = self.hex_to_rgb(penalty_color_hex)

        # 3. 找到最近的 route_color_hex 颜色点
        start_nearest = self.find_nearest_route_color(img, start, route_colors_rgb, tolerance)
        goal_nearest = self.find_nearest_route_color(img, goal, route_colors_rgb, tolerance)

        logger.info(f"start_nearest:{start_nearest}")
        logger.info(f"goal_nearest:{goal_nearest}")

        if not start_nearest or not goal_nearest:
            logger.info("无法找到最近的 route_color_hex 颜色区域")
            return []

        target_colors_rgb_general = target_colors_rgb + route_colors_rgb
        # 4. 计算三段路径
        path1 = self.a_star_search(img, start, start_nearest, target_colors_rgb_general, target_colors_rgb_general,
                                   penalty_color_rgb,
                                   tolerance)
        path2 = self.a_star_search(img, start_nearest, goal_nearest, route_colors_rgb, route_colors_rgb,
                                   penalty_color_rgb, tolerance)
        path3 = self.a_star_search(img, goal_nearest, goal, target_colors_rgb_general, target_colors_rgb_general,
                                   penalty_color_rgb,
                                   tolerance)

        logger.info(f"path1:{path1}")
        logger.info(f"path2:{path2}")
        logger.info(f"path3:{path3}")

        # 5. 拼接路径
        full_path = path1 + path2[1:] + path3[1:]  # 避免重复点

        # 6. 检查路径是否折叠并删除重复点
        visited = set()
        deduplicated_path = []

        for point in full_path:
            if point not in visited:
                visited.add(point)
                deduplicated_path.append(point)

        if len(deduplicated_path) < len(full_path):
            logger.info("路径存在折叠，已删除重复的点。")

        deduplicated_path=self.remove_collapsed_points(deduplicated_path)

        # 7. 绘制路径（如果启用 debug）
        if debug and deduplicated_path:
            self.draw_path_on_image(img, deduplicated_path, output_image_path)

        return deduplicated_path





