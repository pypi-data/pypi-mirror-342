import os
import cv2
import numpy as np
from PIL import Image

class ImageFinder:
    def __init__(self):
        """初始化 ImageFinder 类"""
        self.big_image_array = None
        self.small_image_arrays = {}  # 存储多个小图的数组

    @staticmethod
    def load_image(image_input):
        """加载图像，支持图像路径或 NumPy 数组"""
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
                return cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR)
            if image_input.shape[2] == 3:  # RGB
                return cv2.cvtColor(image_input, cv2.COLOR_RGB2BGR)

        else:
            raise ValueError("输入必须是图像路径或 NumPy 数组")

    def multi_scale_template_matching(self, small_image_array, scales, search_area=None,x3:int=0,y3:int=0):
        """多尺度模板匹配，返回小图在大图中的所有坐标和可信度"""
        results = []
        for scale in scales:
            resized_small = cv2.resize(small_image_array, None, fx=scale, fy=scale)
            if search_area is not None:
                x_start, y_start, x_end, y_end = search_area

                # 确保搜索区域在大图范围内
                if x_start < 0 or y_start < 0 or x_end > self.big_image_array.shape[1] or y_end > \
                        self.big_image_array.shape[0]:
                    print(f"搜索区域超出大图范围: {search_area}")
                    continue

                search_area_img = self.big_image_array[y_start:y_end, x_start:x_end]
            else:
                search_area_img = self.big_image_array

            result = cv2.matchTemplate(search_area_img, resized_small, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8  # 可以根据需要调整阈值
            loc = np.where(result >= threshold)

            if loc[0].size > 0:
                for pt in zip(*loc[::-1]):
                    x1, y1 = pt
                    h, w = resized_small.shape[:2]
                    x2, y2 = x1 + w, y1 + h

                    # 不再调整坐标到原图
                    # 直接使用 x1, y1, x2, y2

                    # 确保索引在范围内
                    if 0 <= y1 < result.shape[0] and 0 <= x1 < result.shape[1]:
                        confidence = result[y1, x1]  # 可信度来自匹配结果
                        confidence = round(confidence, 3)  # 限制小数点后 3 位
                        results.append((x1+x3, y1+y3, x2+x3, y2+y3, confidence))
                    else:
                        print(f"匹配结果索引超出范围: y1={y1}, x1={x1}, result.shape={result.shape}")

        return results if results else None

    def find_subimage_with_feature_matching(self, small_image_array, search_area=None,x3:int=0,y3:int=0):
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
            src_pts = np.float32([keypoints_small[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints_big[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            if M is not None:
                h, w = small_image_array.shape[:2]
                corners = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                transformed_corners = cv2.perspectiveTransform(corners, M)

                # 直接使用 transformed_corners 的坐标
                x1, y1 = np.min(transformed_corners[:, 0, 0]), np.min(transformed_corners[:, 0, 1])
                x2, y2 = np.max(transformed_corners[:, 0, 0]), np.max(transformed_corners[:, 0, 1])

                confidence = len(good_matches) / len(matches)
                results.append((int(x1)+x3, int(y1)+y3, int(x2)+x3, int(y2)+y3, round(confidence,3)))

        return results if results else None

    def find(self, big_image=None, small_images=None):
        """查找多个小图在大图中的位置"""

        self.big_image_array = self.load_image(big_image)

        results = {}
        for small_image_path, params in small_images.items():
            self.small_image_arrays[small_image_path] = self.load_image(small_image_path)

            # 提取坐标和置信度
            x1, y1, x2, y2, confidence = params[:5]
            search_area = (x1, y1, x2, y2)  # 使用元组中的坐标区域

            # 查找小图在大图中的位置
            coordinates = self.multi_scale_template_matching(self.small_image_arrays[small_image_path], [1.0], search_area,x3=x1,y3=y1)

            if coordinates is None:
                coordinates = self.find_subimage_with_feature_matching(self.small_image_arrays[small_image_path], search_area,x3=x1,y3=y1)
            if coordinates :
                results.setdefault(small_image_path, []).extend(coordinates)

        return results

# # 创建 ImageFinder 实例
# image_finder = ImageFinder()
#
# # 指定大图的路径
# big_image_path = r'D:\pc_work\pc_script\resource\dtws\demo\2025-01-29-180322.png'  # 替换为实际的大图路径
#
# # 小图的参数字典
# sub_images_dict =  {
#         'resource/dtws/main_task/背包.bmp': (1373, 705, 1438, 772, 0.8),
#         "resource/dtws/main_task/冒险.bmp":(1387,629,1429,682,0.8),
#         "resource/dtws/main_task/功能展开.bmp":(1385, 641, 1434, 708,0.8),
#         "resource/dtws/main_task/功能收起.bmp":(1386,690,1430,733,0.8),
#         "resource/dtws/main_task/帮会.bmp":(791, 242, 1433, 827,0.8),
#         "resource/dtws/main_task/战骑.bmp":(791, 242, 1433, 827,0.8),
#         "resource/dtws/main_task/技能.bmp":(791, 242, 1433, 827,0.8),
#         "resource/dtws/main_task/排行榜.bmp":(1387,446,1432,493,0.8),
#         "resource/dtws/main_task/武将.bmp":(926,695,968,743,0.8),
#         "resource/dtws/main_task/活动.bmp":(1143,29,1183,78,0.8),
#         "resource/dtws/main_task/角色.bmp":(824,695,868,746,0.8),
#         "resource/dtws/main_task/设置.bmp":(1389,383,1431,435,0.8),
#         "resource/dtws/main_task/充值窗口关闭.bmp":(1020,97,1056,130,0.8),
#         "resource/dtws/main_task/活动窗口关闭.bmp":(1117,208,1194,269,0.8),
#         "resource/dtws/main_task/福利窗口关闭.bmp":(1027,99,1056,131,0.8,),#待优化
#         "resource/dtws/main_task/对话界面_对话点击.bmp":(457,507,585,576,0.8),#457,539,585,580
#         "resource/dtws/main_task/背包关闭.bmp":(1161,386,1196,415,0.8),
#         "resource/dtws/other/大唐风流关闭.bmp":(1120,199,1192,255,0.8),
#         "resource/dtws/main_task/对话界面_未完成.bmp":(484,551,997,642,0.8,421,-235)
#         }
#
# # 查找小图在大图中的位置
# results = image_finder.find(big_image=big_image_path, small_images=sub_images_dict)
# print(results)









