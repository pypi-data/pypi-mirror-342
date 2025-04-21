import os
import numpy as np
from PIL import Image
from otauto.image_traits import ImageTraits

class ImageMatcher:
    def __init__(self, reference_image_path: str):
        """
        初始化 ImageMatcher 类

        :param reference_image_path: 参考图像的路径
        """
        self.reference_image_path = reference_image_path  # 参考图像路径
        self.matcher = ImageTraits()  # 特征匹配实例
        self.points_ls = []  # 存储所有匹配结果的列表

    def load_image(self, image_path: str):
        """
        加载图像并转换为数组

        :param image_path: 图像文件的路径
        :return: 图像的数组表示（numpy 数组），如果加载失败则返回 None
        """
        try:
            image = Image.open(image_path)  # 加载图像
            return np.array(image)  # 转换为 numpy 数组
        except FileNotFoundError:
            print(f"文件未找到: {image_path}")
            return None
        except Exception as e:
            print(f"加载图像时发生错误: {e}")
            return None

    def crop_image(self, image_array: np.ndarray, x1: int, y1: int, x2: int, y2: int):
        """
        裁剪图像

        :param image_array: 待裁剪的图像数组
        :param x1: 裁剪区域左上角的 x 坐标
        :param y1: 裁剪区域左上角的 y 坐标
        :param x2: 裁剪区域右下角的 x 坐标
        :param y2: 裁剪区域右下角的 y 坐标
        :return: 裁剪后的图像数组，如果裁剪区域超出边界则返回 None
        """
        if y1 < 0 or y2 > image_array.shape[0] or x1 < 0 or x2 > image_array.shape[1]:
            print("裁剪区域超出图像边界，请检查坐标。")
            return None
        return image_array[y1:y2, x1:x2]  # 返回裁剪后的图像

    def match_images(self, image_folder: str):
        """
        对文件夹中的所有图像进行特征匹配

        遍历指定文件夹中的所有 PNG 图像，与参考图像进行匹配，并存储匹配结果。

        :param image_folder: 待匹配图像文件夹路径
        """
        # 获取文件夹中的所有 PNG 文件
        image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]
        num = len(image_files)  # 获取文件数量

        for i in range(num):
            image1_path = os.path.join(image_folder, f'0{i + 1}.png')  # 构建图像路径
            image1_array = self.load_image(image1_path)  # 加载待匹配图像
            image2_array = self.load_image(self.reference_image_path)  # 加载参考图像

            if image1_array is not None and image2_array is not None:
                # 裁剪区域
                x1, y1, x2, y2 = 1258, 75, 1415, 225  # image1 的裁剪区域
                image1_cropped = self.crop_image(image1_array, x1, y1, x2, y2)  # 裁剪图像

                if image1_cropped is not None:
                    res = self.matcher.draw_matches(image1_cropped, image2_array, True)  # 进行特征匹配
                    if res is not None:
                        self.points_ls.append(res["role_position"])  # 存储匹配结果
                        print(f"匹配结果: {res}")
                    else:
                        print(f"未能获取匹配结果。图像: {image1_path}")

        print(f"点位数量: {len(self.points_ls)}, 列表: {self.points_ls}")  # 输出匹配结果数量

    def match_single_image(self, image_path: str):
        """
        对单张图像进行特征匹配

        :param image_path: 待匹配的单张图像路径
        :return: 匹配结果的角色位置，如果匹配失败返回 None
        """
        image1_array = self.load_image(image_path)  # 加载待匹配图像
        image2_array = self.load_image(self.reference_image_path)  # 加载参考图像

        if image1_array is not None and image2_array is not None:
            # 裁剪区域
            # x1, y1, x2, y2 = 1258, 75, 1415, 225  # image1 的裁剪区域
            x1, y1, x2, y2 = 640, 417, 1171, 564  # image1 的裁剪区域
            image1_cropped = self.crop_image(image1_array, x1, y1, x2, y2)  # 裁剪图像

            if image1_cropped is not None:
                res = self.matcher.draw_matches(image1_cropped, image2_array, True)  # 进行特征匹配
                if res is not None:
                    print(f"单张匹配结果: {res}")
                    return res["role_position"]  # 返回匹配结果的角色位置
                else:
                    print("未能获取匹配结果。")
        return None  # 返回 None 表示匹配失败

# 使用示例
if __name__ == "__main__":
    reference_image_path = r'D:\pc_work\pc_script-otauto\image-tools\2025-03-30-110640.png'  # 参考图像路径
    image_matcher = ImageMatcher(reference_image_path)  # 创建 ImageMatcher 实例

    # # 匹配文件夹中的所有图像,文件名称必须是01~999这样命名
    # image_folder = r'D:\pc_work\pc_script-otauto\image-tools\full'  # 待匹配图像文件夹路径
    # image_matcher.match_images(image_folder)  # 匹配文件夹中的所有图像

    # 进行单张图像匹配
    single_image_path = r'D:\pc_work\pc_script-otauto\image-tools\2025-03-30-110716.png'  # 单张图像路径
    single_match_result = image_matcher.match_single_image(single_image_path)  # 进行单张图像匹配