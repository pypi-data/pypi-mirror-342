import os
import numpy as np
from PIL import Image
from loguru import logger
import aircv as ac
"""
功能:图片模版匹配
日期:2025-2-18 13:30:01
描述:
    区域多位置模版匹配
"""

class ImageMatcher:
    def __init__(self):
        """
        初始化 ImageMatcher 类
        """
        self.target_image = None

    def load_image(self, image_path: str) -> np.ndarray:
        """
        加载图像并转换为 NumPy 数组
        :param image_path: 图像路径
        :return: NumPy 数组格式的图像
        """
        if os.path.exists(image_path):
            img = Image.open(image_path)
            return np.array(img)
        else:
            logger.error(f"Image path does not exist: {image_path}")
            return None

    def picture_matching(self, numpy_array: np.ndarray, con: float = 0.8, x1: int = 0, y1: int = 0, x2: int = None,
                         y2: int = None):
        """
        检查小图在大图片中的匹配情况
        :param numpy_array: 小图的 NumPy 数组
        :param con: 置信度
        :param x1: 小图的左上角 x 坐标
        :param y1: 小图的左上角 y 坐标
        :param x2: 小图的右下角 x 坐标
        :param y2: 小图的右下角 y 坐标
        :return: 匹配结果
        """
        if self.target_image is not None:
            # 裁剪大图到识别范围
            if x2 is not None and y2 is not None:
                cropped_image = self.target_image[y1:y2, x1:x2]
            else:
                cropped_image = self.target_image

            results = ac.find_all_template(cropped_image, numpy_array, threshold=con)
            # logger.info(f"results: {results}")

            # 格式化结果
            formatted_results = []
            for match in results:
                rectangle = match['rectangle']
                confidence = match['confidence']
                x_1, y_1 = rectangle[0]  # 左上角
                x_2, y_2 = rectangle[3]  # 右下角
                formatted_results.append((int(x_1 + x1), int(y_1 + y1), int(x_2 + x1), int(y_2 + y1),float(round(confidence, 3))))

            return formatted_results
        else:
            logger.error("Target image is not loaded.")
            return []

    def match_sub_images(self, big_image, sub_images_dict: dict):
        """
        对字典中的每个小图进行匹配
        :param big_image: 大图路径或 NumPy 数组
        :param sub_images_dict: 小图路径及其参数字典
        :return: 匹配结果字典
        """
        match_results = {}

        # logger.success(f"信息:{big_image}")

        # 判断 big_image 的类型
        if isinstance(big_image, str):
            self.target_image = self.load_image(big_image)  # 加载大图
            if self.target_image is None:
                logger.error("Failed to load the big image.")
                return match_results  # 如果加载失败，返回空结果
        elif isinstance(big_image, np.ndarray):
            self.target_image = big_image  # 直接使用 NumPy 数组
        else:
            logger.error("big_image must be a file path (str) or a NumPy array.")
            return match_results  # 如果类型不正确，返回空结果

        for image_path, params in sub_images_dict.items():
            sub_image = Image.open(image_path)
            sub_image_array = np.array(sub_image)
            x1, y1, x2, y2, con = params  # 获取坐标和置信度
            result = self.picture_matching(sub_image_array, con, x1, y1, x2, y2)
            if result:
                match_results[image_path] = result
        return match_results


# 使用示例
# if __name__ == "__main__":
#     big_image_path = r'D:\pc_work\pc_script\resource\images_info\demo\image.png'
#     # 或者直接使用 NumPy 数组
#     # big_image = np.array(Image.open(big_image_path))
#     image_matcher = ImageMatcher()
#
#     # 小图的参数字典，包含识别范围和置信度
#     sub_images_dict = {
#         r"D:\pc_work\pc_script\resource\images_info\main_task\活动.bmp": (1135, 42, 1197, 113, 0.8),
#         r'D:\pc_work\pc_script\resource\images_info\other\每日签到完成.bmp': (487, 277, 958, 489, 0.8),
#         r"D:\pc_work\pc_script\resource\images_info\main_task\商城.bmp": (1186, 44, 1250, 111, 0.8),
#         r"D:\pc_work\pc_script\resource\images_info\other\升级标志.bmp": (587, 498, 748, 549, 0.8),
#     }
#
#     # results = image_matcher.match_sub_images(big_image_path, sub_images_dict)
#     # print(results)
#
#     # 如果想用 NumPy 数组作为大图
#     big_image = np.array(Image.open(big_image_path))
#     results = image_matcher.match_sub_images(big_image, sub_images_dict)
#     print(results)