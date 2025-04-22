import cv2
import numpy as np
from PIL import Image
from loguru import logger

"""
特征匹配算法
注意：图片太小无法算出特征
"""

class ImageTraits:
    def __init__(self):
        """初始化 ImageMatcher 类的实例，设置相关属性"""

        self.offset = 0  # 偏移量
        self.error_x =0 # x错误值
        self.error_y =0 # y错误值
        self.role_position = None  # 角色位置
        self.image1_center = None  # 小图的中心点
        self.x_center = None  # 大图的中心点 x 坐标
        self.y_center = None  # 大图的中心点 y 坐标
        self.scope_1 = None  # 小图的内点区域
        self.scope_2 = None  # 大图的内点区域
        self.scope_center_2 = None  # 大图的中心点
        self.image1 = None  # 查询图像
        self.image2 = None  # 训练图像

    def preprocess_image(self, image_array):
        """图像预处理：转换为灰度图，应用高斯模糊和直方图均衡化
        :param image_array: 输入的图像数组（RGB格式）
        :return: 处理后的图像（灰度图并经过高斯模糊和直方图均衡化）
        """
        gray_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)  # 转换为灰度图
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)  # 应用高斯模糊
        equalized_image = cv2.equalizeHist(blurred_image)  # 应用直方图均衡化
        return equalized_image

    def find_and_match_keypoints(self):
        """使用 SIFT 方法检测特征点并进行匹配
        :return: 返回第一幅图像的关键点、第二幅图像的关键点和匹配结果
        """
        sift = cv2.SIFT_create()  # 创建 SIFT 特征检测器
        keypoints1, descriptors1 = sift.detectAndCompute(self.image1, None)  # 检测小图的特征点和描述符
        keypoints2, descriptors2 = sift.detectAndCompute(self.image2, None)  # 检测大图的特征点和描述符

        # 使用 FLANN 匹配器进行特征匹配
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)  # 创建 FLANN 匹配器
        matches = flann.knnMatch(descriptors1, descriptors2, k=2)  # 进行 KNN 匹配

        # 应用比率测试：选择好的匹配
        good_matches = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:  # 选择较好的匹配
                good_matches.append(m)

        return keypoints1, keypoints2, good_matches

    def draw_matches(self, image1_array, image2_array, debug=False):
        """绘制匹配点并计算内点和外点的比例
        :param image1_array: 查询图像（小图）的数组
        :param image2_array: 训练图像（大图）的数组
        :param debug: 是否显示调试信息（默认为 False）
        """
        self.image1 = self.preprocess_image(image1_array)  # 处理查询图像
        self.image2 = self.preprocess_image(image2_array)  # 处理训练图像

        keypoints1, keypoints2, matches = self.find_and_match_keypoints()  # 查找并匹配特征点

        if len(matches) < 4:
            print("匹配点数量不足，无法计算单应性矩阵。")
            return  # 如果匹配点数量不足，返回

        points1 = np.array([keypoints1[m.queryIdx].pt for m in matches])  # 获取第一幅图像的匹配点坐标
        points2 = np.array([keypoints2[m.trainIdx].pt for m in matches])  # 获取第二幅图像的匹配点坐标

        # 计算第一幅图像的中心点
        height1, width1 = self.image1.shape  # 获取第一幅图像的高度和宽度
        self.image1_center = (width1 // 2, height1 // 2)  # 计算中心点 (x, y)

        # 使用 RANSAC 计算单应性矩阵
        homography, mask = cv2.findHomography(points1, points2, cv2.RANSAC)  # 计算单应性矩阵

        # 计算内点和外点
        inliers = mask.ravel().tolist()  # 将掩码展平为列表
        num_inliers = inliers.count(1)  # 计算内点数量

        # 可信度计算：内点数量与总匹配数量的比例
        confidence = num_inliers / len(matches)

        # 计算内点的比例
        scale_x_values = []  # 存储内点的x方向比例
        scale_y_values = []  # 存储内点的y方向比例

        for i in range(len(matches)):
            if inliers[i] == 1:  # 只计算内点
                scale_x = points2[i, 0] / points1[i, 0] if points1[i, 0] != 0 else 0
                scale_y = points2[i, 1] / points1[i, 1] if points1[i, 1] != 0 else 0

                scale_x_values.append(scale_x)  # 添加内点x方向的比例
                scale_y_values.append(scale_y)  # 添加内点y方向的比例

        # 创建一个彩色图像以绘制匹配结果
        matched_image = cv2.drawMatches(self.image1, keypoints1, self.image2, keypoints2, matches, None,
                                        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        # 计算内点的坐标
        inlier_points1 = points1[np.array(inliers) == 1]  # 选择内点在第一幅图像中的坐标
        inlier_points2 = points2[np.array(inliers) == 1]  # 选择内点在第二幅图像中的坐标

        if len(inlier_points1) > 0:
            # 计算第一幅图像内点的最小和最大坐标
            min_x1, min_y1 = inlier_points1.min(axis=0).astype(int)
            max_x1, max_y1 = inlier_points1.max(axis=0).astype(int)

            self.scope_center_1 = (int((max_x1 + min_x1) / 2), int((max_y1 + min_y1) / 2))  # 计算小图内点的中心

            if debug:
                # 在第一幅图像上绘制内点方框
                cv2.rectangle(matched_image, (min_x1, min_y1), (max_x1, max_y1), (0, 255, 0), 2)  # 绘制绿色方框

        if len(inlier_points2) > 0:
            # 计算第二幅图像内点的最小和最大坐标
            min_x2, min_y2 = inlier_points2.min(axis=0).astype(int)
            max_x2, max_y2 = inlier_points2.max(axis=0).astype(int)

            self.scope_center_2 = (int((max_x2 + min_x2) / 2), int((max_y2 + min_y2) / 2))  # 计算大图内点的中心

            self.error_x = self.image1_center[0] - self.scope_center_1[0]
            self.error_y = self.image1_center[1] - self.scope_center_1[1]

            # 计算宽度和高度
            width = max_x2 - min_x2
            height = max_y2 - min_y2
            # 根据较小的维度来调整方框的大小，使其接近正方形
            square_side = int(max(width, height))  # 取较大的边作为正方形的边长
            # 计算新的坐标，使方框居中
            new_min_x2 = max(min_x2 + (width - square_side) // 2, 0)
            new_min_y2 = max(min_y2 + (height - square_side) // 2, 0)
            # 确保新的最大坐标不超过图像边界
            new_max_x2 = min(new_min_x2 + square_side, self.image2.shape[1])
            new_max_y2 = min(new_min_y2 + square_side, self.image2.shape[0])
            self.x_center = (new_max_x2 + new_min_x2) // 2 + self.offset  # 计算大图中心
            self.y_center = (new_max_y2 + new_min_y2) // 2  # 计算大图中心
            self.role_position=(self.x_center + self.error_x-self.offset, self.y_center + self.error_y)
            if debug:
                # 在第二幅图像上绘制接近正方形的内点方框
                self.offset = self.image1.shape[1]  # 第一幅图像的宽度
                cv2.rectangle(matched_image, (new_min_x2 + self.offset, new_min_y2), (new_max_x2 + self.offset, new_max_y2),
                              (0, 255, 0), 2)  # 绘制绿色方框
                # 绘制红点标记中心
                cv2.circle(matched_image, (self.x_center + self.error_x+self.offset, self.y_center + self.error_y), 5, (0, 0, 255), -1)  # 绘制红色点

        # 显示匹配结果
        if debug:
            logger.success(f"内点数量,num_inliers: {num_inliers}")
            logger.success(f"总匹配数量,matches: {len(matches)}")
            logger.success(f"可信度,con: {confidence:.2f}")
            logger.success(f"x误差: {self.error_x}")
            logger.success(f"y误差: {self.error_y}")
            logger.success(f"小图原图中心点: {self.image1_center}")
            logger.success(f"小图内点中心点: {self.scope_center_1}")
            logger.success(f"大图内点中心点: {self.scope_center_2}")
            logger.success(f"角色位置,role_position: {self.role_position}")

            # 保存匹配结果到指定文件夹
            output_image_path = r"resource/images_info/demo/image_traits.png"  # 替换为您的输出路径
            # 使用 cv2.imwrite 保存图像
            cv2.imwrite(output_image_path, matched_image)  # 保存匹配结果图像
            logger.success(f"匹配结果已保存到: {output_image_path}")  # 日志记录保存成功信息

        # 返回匹配结果的详细信息
        return {
            "num_inliers": num_inliers if num_inliers is not None else 0,  # 默认值为 0
            "matches": len(matches) if matches is not None else 0,  # 默认值为 0
            "con": confidence if confidence is not None else 0.0,  # 默认值为 0.0
            "role_position": self.role_position if self.role_position is not None else (-1, -1),  # 默认值为 (-1, -1)
        }

# # 使用示例
# if __name__ == "__main__":
#     # for num in range(1,7):
#         num=20
#         image1 = Image.open(f'resource/image_b/0{num}.png')
#         image2 = Image.open('../resource/images_info/map_image/map_达摩洞一层_data.jpg')
#         image1_array = np.array(image1)
#         image2_array = np.array(image2)
#
#         # 裁剪 image1_array 和 image2_array，例如裁剪区域 (x, y, width, height)
#         x1, y1, x2, y2 = 1258, 75, 1415, 225  # image1的裁剪区域
#
#         # 计算原始裁剪区域的中心点
#         center_x = (x1 + x2) / 2
#         center_y = (y1 + y2) / 2
#
#         # 缩小比例
#         scale_factor = 1
#
#         # 新的宽度和高度
#         new_width = (x2 - x1) * scale_factor
#         new_height = (y2 - y1) * scale_factor
#
#         # 计算新的裁剪区域坐标，使其居中
#         new_x1 = int(center_x - new_width / 2)
#         new_y1 = int(center_y - new_height / 2)
#         new_x2 = int(center_x + new_width / 2)
#         new_y2 = int(center_y + new_height / 2)
#         image1_cropped = image1_array[new_y1:new_y2, new_x1:new_x2] # 裁剪
#
#         x2, y2, w2, h2 = 15, 17, 122, 101  # image2的裁剪区域
#         image2_cropped = image2_array[y2:y2 + h2, x2:x2 + w2]  # 裁剪
#
#         matcher = ImageMatcher()  # 只使用 SIFT
#         res=matcher.draw_matches(image1_cropped, image2_array,True)  # 绘制匹配结果
#         print(f"{res}")