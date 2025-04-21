import numpy as np
import requests
import json
import base64
import cv2  # 确保安装了opencv-python
from loguru import logger


class OCRClient:
    def __init__(self, det=True, rec=True):
        self.url = "localhost"
        self.det = det
        self.rec = rec

    def cv2_to_base64(self, image):
        """将图像数据转换为base64编码"""
        return base64.b64encode(image).decode("utf8")

    def process_image_array(self, image_array):
        """处理NumPy数组格式的图像数据并发送请求"""
        result_dict = {}
        if not isinstance(image_array, np.ndarray):
            raise ValueError("Input must be a NumPy array.")

        # 将RGB图像转换为BGR格式
        image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        # 将NumPy数组转换为字节数据
        _, buffer = cv2.imencode('.png', image_array)  # 使用cv2.imencode将NumPy数组编码为PNG格式
        image_data = buffer.tobytes()  # 转换为字节

        image = self.cv2_to_base64(image_data)

        data = {"key": ["image"], "value": [image]}
        r = requests.post(url=self.url, data=json.dumps(data))
        result = r.json()

        # logger.success(f"高精度识别结果:{result}")

        if result["err_no"] == 0:
            ocr_result = result["value"][0]
            if not self.det:
                logger.success(ocr_result)
            else:
                try:
                    for item in eval(ocr_result):
                        # 提取时间和置信度
                        key_str = item[0][0]
                        confidence = round(item[0][1], 3)  # 四舍五入到三位小数
                        x1, y1 = int(item[1][0][0]), int(item[1][0][1])
                        x2, y2 = int(item[1][2][0]), int(item[1][2][1])
                        # 检查key_str是否已经在result_dict中
                        if key_str in result_dict:
                            # 如果存在，添加新的[x1, y1, x2, y2, confidence]到现有的值列表中
                            result_dict[key_str].append([x1, y1, x2, y2, confidence])
                        else:
                            # 如果不存在，创建新的条目
                            result_dict[key_str] = [[x1, y1, x2, y2, confidence]]
                    return result_dict
                except Exception as e:
                    logger.error(f"坐标合并错误: {e}")
                    return result_dict
        else:
            logger.error("For details about error message, see PipelineServingLogs/pipeline.log")
            return result_dict

    def run(self, image_array, url_ip, url_port):
        """
        运行OCR处理
        :param image_array: 单个NumPy数组
        :param url_ip: OCR服务的IP
        :param url_port: OCR服务的端口
        """
        self.url = f"http://{url_ip}:{url_port}/ocr/prediction"

        if not isinstance(image_array, np.ndarray):
            raise ValueError("Input must be a NumPy array.")

        return self.process_image_array(image_array)


# if __name__ == "__main__":
#     # 直接定义参数
#     url_1 = "192.168.110.146"
#
#     # 创建 OCRClient 实例
#     ocr_client = OCRClient()
#
#     # 示例: 读取单个图像并转换为NumPy数组
#     img_file = r"D:\pc_work\pc_script\server\docker\fastapi\2024-12-19-090022.png"  # 替换为实际图像路径
#     image_array = cv2.imread(img_file)
#
#     # 确保读取成功
#     if image_array is None:
#         print("无法读取图像，请检查路径是否正确。")
#     else:
#         # 运行OCR处理
#         res = ocr_client.run(image_array, url_1, "9998")
#         print(res)