import os
import cv2
import numpy as np
from PIL import Image


class ImageFinder:
    def __init__(self):
        """初始化 ImageFinder 类"""
        self.big_image_array = None
        self.small_image_array = None

    @staticmethod
    def load_image(image_input):
        """加载图像，支持图像路径或 NumPy 数组"""
        if isinstance(image_input, str):
            # 如果是字符串，认为是图像路径
            if not os.path.exists(image_input):
                raise FileNotFoundError(f"文件未找到: {image_input}")
            pil_image = Image.open(image_input)

            # 将 PIL 图像转换为 NumPy 数组
            numpy_array = np.array(pil_image)

            # 检查通道数
            if numpy_array.shape[2] == 4:  # RGBA
                # 只保留 RGB 通道
                numpy_array = numpy_array[:, :, :3]

            # 转换为 BGR 格式
            return cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR)

        elif isinstance(image_input, np.ndarray):
            # 检查通道数
            if image_input.shape[2] == 4:  # RGBA
                # 只保留 RGB 通道
                numpy_array = image_input[:, :, :3]
                # 转换为 BGR 格式
                return cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR)
            if image_input.shape[2] == 3:  # RGB
                # 转换为 BGR 格式
                return cv2.cvtColor(image_input, cv2.COLOR_RGB2BGR)

        else:
            raise ValueError("输入必须是图像路径或 NumPy 数组")

    def multi_scale_template_matching(self, scales, x3: int = 0, y3: int = 0):
        """多尺度模板匹配，返回小图在大图中的坐标和可信度"""
        for scale in scales:
            resized_small = cv2.resize(self.small_image_array, None, fx=scale, fy=scale)
            result = cv2.matchTemplate(self.big_image_array, resized_small, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8  # 可以根据需要调整阈值
            loc = np.where(result >= threshold)

            if loc[0].size > 0:
                max_val = result.max()  # 获取最大相似度
                confidence = max_val  # 可信度已经在 [0, 1] 范围内
                for pt in zip(*loc[::-1]):  # Switch columns and rows
                    x1, y1 = pt
                    h, w = resized_small.shape[:2]
                    x2, y2 = x1 + w, y1 + h
                    return (x1 + x3, y1 + y3, x2 + x3, y2 + y3, confidence)  # 返回坐标和可信度

        return None

    def find_subimage_with_feature_matching(self, x3: int = 0, y3: int = 0):
        """使用ORB特征匹配查找小图在大图中的位置和可信度"""
        big_gray = cv2.cvtColor(self.big_image_array, cv2.COLOR_BGR2GRAY)
        small_gray = cv2.cvtColor(self.small_image_array, cv2.COLOR_BGR2GRAY)

        orb = cv2.ORB_create()
        keypoints_big, descriptors_big = orb.detectAndCompute(big_gray, None)
        keypoints_small, descriptors_small = orb.detectAndCompute(small_gray, None)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors_small, descriptors_big)

        good_matches = sorted(matches, key=lambda x: x.distance)

        if len(good_matches) > 10:
            src_pts = np.float32([keypoints_small[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints_big[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            if M is not None:
                h, w = self.small_image_array.shape[:2]
                corners = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                transformed_corners = cv2.perspectiveTransform(corners, M)

                x1, y1 = np.min(transformed_corners[:, 0, 0]), np.min(transformed_corners[:, 0, 1])
                x2, y2 = np.max(transformed_corners[:, 0, 0]), np.max(transformed_corners[:, 0, 1])

                # 计算可信度
                confidence = len(good_matches) / len(matches)  # 归一化到 [0, 1]
                return (int(x1) + x3, int(y1) + y3, int(x2) + x3, int(y2) + y3, confidence)  # 返回坐标和可信度

        return None

    def draw_rectangle(self, coordinates):
        """在大图上绘制红色方框"""
        if coordinates:
            x1, y1, x2, y2 = coordinates
            cv2.rectangle(self.big_image_array, (x1, y1), (x2, y2), (0, 0, 255), 2)  # 红色方框

    def find(self, big_image=None, small_image=None,x3:int=0,y3:int=0):
        """查找小图在大图中的位置"""
        try:
            self.big_image_array = self.load_image(big_image)
            self.small_image_array = self.load_image(small_image)

            # 确保图像的深度和类型一致
            if self.big_image_array.dtype != np.uint8:
                self.big_image_array = self.big_image_array.astype(np.uint8)
            if self.small_image_array.dtype != np.uint8:
                self.small_image_array = self.small_image_array.astype(np.uint8)

            scales = [1.0]  # 可以根据需要调整缩放比例
            coordinates = self.multi_scale_template_matching(scales,x3,y3)

            if coordinates is None:
                coordinates = self.find_subimage_with_feature_matching(x3, y3)

            return coordinates

        except Exception as e:
            print(f"查找小图在大图中的位置时发生错误: {e}")
            return None


# # 使用示例
# big_image_path = r'D:\pc_work\dtwsv2_v5\res\dtws\demo\demo_002.png'
# small_image_path = r'D:\pc_work\dtwsv2_v5\res\dtws\role_skill\穿云剑.bmp'
# # 使用 PIL 加载图像
# img = Image.open(big_image_path)  # 注意此颜色顺序为rgb
# # 将 PIL 图像转换为 NumPy 数组
# big_numpy_array = np.array(img)
#
# try:
#     image_finder = ImageFinder()
#     coordinates = image_finder.find(big_numpy_array, small_image_path)
#
#     if coordinates:
#         x1, y1, x2, y2,con = coordinates
#         print(f"小图在大图中的坐标: ({x1}, {y1}), ({x2}, {y2},{con})")
#         image_finder.draw_rectangle(coordinates[:-1])  # 在大图上绘制方框
#
#         # 显示结果
#         cv2.imshow("Result", image_finder.big_image_array)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#     else:
#         print("小图未在大图中找到")
# except ValueError as e:
#     print(e)








