import cv2
import os
from datetime import datetime
import numpy as np

class ImageStitcher:
    """
    图像拼接类
    功能: 读取指定路径的图像，进行预处理，拼接成一张完整的图像，并保存结果。
    更新日志: 2024-11-12 12:42:20
    """

    def __init__(self, paths):
        """
        初始化 ImageStitcher 类

        :param paths: 图像文件或文件夹的路径列表
        """
        self.paths = paths  # 存储图像路径
        self.images = []  # 存储加载的图像
        self.current_time = datetime.now()  # 当前时间
        self.formatted_time = self.current_time.strftime('%Y-%m-%d %H%M%S')  # 格式化时间

    def load_images_from_folder(self, folder):
        """从文件夹加载图像"""
        images = []
        for filename in sorted(os.listdir(folder)):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath):
                img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), cv2.IMREAD_COLOR)
                if img is not None:
                    images.append(img)
        return images

    def load_images(self):
        """加载图像"""
        for path in self.paths:
            if os.path.isdir(path):
                self.images.extend(self.load_images_from_folder(path))  # 从文件夹加载图像
            elif os.path.isfile(path):
                img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
                if img is not None:
                    self.images.append(img)  # 加载单个图像
            else:
                print(f"路径 '{path}' 既不是有效的文件也不是文件夹。")
        return self.images

    def adjust_contrast_brightness(self, image, contrast=1.3, brightness=30):
        """调整图像的对比度和亮度

        :param image: 输入图像
        :param contrast: 对比度因子，默认为 1.3
        :param brightness: 亮度偏移，默认为 30
        :return: 调整后的图像
        """
        adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
        return adjusted

    def preprocess_images(self):
        """对加载的图像进行预处理"""
        preprocessed_images = []
        for img in self.images:
            enhanced_img = self.adjust_contrast_brightness(img)  # 调整对比度和亮度
            preprocessed_images.append(enhanced_img)
        return preprocessed_images

    def stitch_images(self, images):
        """拼接图像

        :param images: 待拼接的图像列表
        :return: 拼接后的图像，如果拼接失败则返回 None
        """
        stitcher = cv2.Stitcher_create()  # 创建一个 Stitcher 对象
        status, stitched_image = stitcher.stitch(images)  # 拼接图像

        if status != cv2.Stitcher_OK:
            print("拼接图像时发生错误，状态码:", status)
            return None
        return stitched_image

    def save_result(self, result):
        """保存拼接结果

        :param result: 拼接后的图像
        """
        output_path = os.path.join(os.getcwd(), f"{self.formatted_time}.jpg")  # 生成输出文件名
        cv2.imencode('.jpg', result)[1].tofile(output_path)  # 保存图像
        print(f"拼接结果已保存到: {output_path}")

    def run(self):
        """运行拼接流程"""
        self.load_images()  # 加载图像
        if len(self.images) == 0:
            print("加载图像时发生错误。")
            return

        preprocessed_images = self.preprocess_images()  # 预处理图像
        result = self.stitch_images(preprocessed_images)  # 拼接图像

        if result is not None:
            # 显示结果
            cv2.imshow("Stitched Image", result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            self.save_result(result)  # 保存结果

# 使用示例
if __name__ == "__main__":
    paths = [r"D:\pc_work\pc_script-otauto\image-tools\002"]  # 指定图像路径
    image_stitcher = ImageStitcher(paths)  # 创建 ImageStitcher 实例
    image_stitcher.run()  # 运行拼接流程