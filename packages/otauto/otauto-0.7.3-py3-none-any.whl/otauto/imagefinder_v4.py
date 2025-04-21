import os
import numpy as np
import cv2
from PIL import Image

class ImageFinder:
    def __init__(self):
        """初始化 ImageFinder 类"""
        self.big_image_array = None
        self.small_image_arrays = {}  # 存储多个小图的数组

    @staticmethod
    def load_image(image_input, save_image=False, save_path=None):
        """加载图像，支持图像路径或 NumPy 数组
        :param image_input: 图像路径或 NumPy 数组
        :param save_image: 是否保存图像，如果输入为 NumPy 数组且为 True，则保存
        :param save_path: 保存路径
        """
        if isinstance(image_input, str):
            if not os.path.exists(image_input):
                raise FileNotFoundError(f"文件未找到: {image_input}")
            pil_image = Image.open(image_input)
            numpy_array = np.array(pil_image)
            if numpy_array.shape[2] == 4:  # RGBA
                numpy_array = numpy_array[:, :, :3]
            return cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR)

        elif isinstance(image_input, np.ndarray):
            if image_input.shape[2] == 4:  # RGBA
                numpy_array = image_input[:, :, :3]
                image_bgr = cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR)
            elif image_input.shape[2] == 3:  # RGB
                image_bgr = cv2.cvtColor(image_input, cv2.COLOR_RGB2BGR)
            else:
                raise ValueError("输入的 NumPy 数组必须是 RGB 或 RGBA 格式")

            # 如果需要保存图像
            if save_image and save_path:
                cv2.imwrite(save_path, image_bgr)

            return image_bgr

        else:
            raise ValueError("输入必须是图像路径或 NumPy 数组")

    def multi_scale_template_matching(self, small_image_array, scales, search_area):
        """多尺度模板匹配，返回小图在大图中的所有坐标和可信度"""
        results = []
        for scale in scales:
            resized_small = cv2.resize(small_image_array, None, fx=scale, fy=scale)
            threshold = 0.8  # 可以根据需要调整阈值

            x_start, y_start, x_end, y_end = search_area

            # 确保搜索区域在大图范围内
            if x_start < 0 or y_start < 0 or x_end > self.big_image_array.shape[1] or y_end > \
                    self.big_image_array.shape[0]:
                print(f"搜索区域超出大图范围: {search_area}")
                return None

            search_area_img = self.big_image_array[y_start:y_end, x_start:x_end]
            result = cv2.matchTemplate(search_area_img, resized_small, cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)

            if loc[0].size > 0:
                for pt in zip(*loc[::-1]):
                    x1, y1 = pt
                    h, w = resized_small.shape[:2]
                    x2, y2 = x1 + w, y1 + h

                    # 确保索引在范围内
                    if 0 <= y1 < result.shape[0] and 0 <= x1 < result.shape[1]:
                        confidence = result[y1, x1]  # 可信度来自匹配结果
                        confidence = round(float(confidence), 3)  # 限制小数点后 3 位
                        results.append(
                            (int(x1 + x_start), int(y1 + y_start), int(x2 + x_start), int(y2 + y_start), confidence))

        return results if results else None

    def find_subimage_with_feature_matching(self, small_image_array, search_area):
        """使用ORB特征匹配查找小图在大图中的所有位置和可信度"""
        big_gray = cv2.cvtColor(self.big_image_array, cv2.COLOR_BGR2GRAY)
        small_gray = cv2.cvtColor(small_image_array, cv2.COLOR_BGR2GRAY)

        orb = cv2.ORB_create()
        keypoints_big, descriptors_big = orb.detectAndCompute(big_gray, None)
        keypoints_small, descriptors_small = orb.detectAndCompute(small_gray, None)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors_small, descriptors_big)

        good_matches = sorted(matches, key=lambda x: x.distance)

        results = []
        if len(good_matches) > 10:
            # 提取匹配的关键点坐标
            src_pts = np.float32([keypoints_small[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints_big[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            # 使用 RANSAC 获取单应性矩阵
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            if M is not None:
                h, w = small_image_array.shape[:2]
                corners = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                transformed_corners = cv2.perspectiveTransform(corners, M)

                # 直接使用 transformed_corners 的坐标
                x1, y1 = np.min(transformed_corners[:, 0, 0]), np.min(transformed_corners[:, 0, 1])
                x2, y2 = np.max(transformed_corners[:, 0, 0]), np.max(transformed_corners[:, 0, 1])

                # 计算可信度
                confidence = len(good_matches) / len(matches)
                confidence = round(float(confidence), 3)  # 限制小数点后 3 位
                results.append((int(x1), int(y1), int(x2), int(y2), confidence))

                # 如果想要找到多个匹配点，可以遍历所有的匹配
                for m in good_matches:
                    # 只考虑匹配点的坐标
                    pt = keypoints_big[m.trainIdx].pt
                    results.append((int(pt[0]), int(pt[1]), int(pt[0] + w), int(pt[1] + h), confidence))

        return results if results else None

    def find(self, big_image=None, small_images=None):
        """查找多个小图在大图中的位置"""

        self.big_image_array = self.load_image(big_image)

        results = {}
        for small_image_path, params in small_images.items():
            self.small_image_arrays[small_image_path] = self.load_image(small_image_path)

            # 提取搜索区域
            search_area = params[:4]  # 提取前四个坐标
            confidence_threshold = params[4]  # 提取可信度阈值

            # 查找小图在大图中的位置
            coordinates = self.multi_scale_template_matching(self.small_image_arrays[small_image_path], [1.0], search_area)

            if coordinates is None:
                coordinates = self.find_subimage_with_feature_matching(self.small_image_arrays[small_image_path], search_area)
            if coordinates:
                results.setdefault(small_image_path, []).extend(coordinates)
        return results

# 创建 ImageFinder 实例
# image_finder = ImageFinder()
#
# # 指定大图的路径
# big_image_path = r'D:\pc_work\pc_script\resource\images_info\demo\image.png'  # 替换为实际的大图路径
#
# # 小图的参数字典
# sub_images_dict = {
#     r"D:\pc_work\pc_script\resource\images_info\main_task\活动.bmp": (1135, 42, 1197, 113, 0.8),
#     r'D:\pc_work\pc_script\resource\images_info\other\每日签到完成.bmp': (487, 277, 958, 489, 0.8),
#     r"D:\pc_work\pc_script\resource\images_info\main_task\商城.bmp": (1186, 44, 1250, 111, 0.8),
#     r"D:\pc_work\pc_script\resource\images_info\other\升级标志.bmp":(587, 498, 748, 549,0.8),
# }
#
# # 查找小图在大图中的位置
# results = image_finder.find(big_image=big_image_path, small_images=sub_images_dict)
# print(results)








