import time

import yaml
from PIL import Image
from loguru import logger

from otauto.clent_ppocr import OCRClient #高精度ocr模型
from otauto.docker_fdv1 import SyncGRPCTritonRunner
from otauto.image_matcher import ImageMatcher
from otauto.ini_file_operationv2 import INIFileHandler # ini文件操作
from otauto.imagefinder_v4 import ImageFinder # 图片识别
from otauto.multipoint_colors_v4 import multipoint_colors
import json
import numpy as np
import cv2

"""
时间:2025-2-13 16:27:55
描述:用于图片识别,docker里的文字,图片识别
np类型转换成python基本类型
"""

class ImageProcessor:
    def __init__(self):
        self.ini_handler = INIFileHandler() # 创建 INIFileHandler 实例
        self.image_finder = ImageFinder()  # 创建 ImageFinder 实例
        self.image_matcher = ImageMatcher() # 创建 ImageMatcher 实例
        self.ocrclient_handler=OCRClient() # 创建 OCRClient 实例
        docker_container_list=["ppocr-fastapi","fd_yolo","fd_ocr"]
        data_dict=self.ini_handler.get_multiple_sections_items(docker_container_list)
        logger.success(f"获取到的docker容器列表:{data_dict}")
        """
        {'ppocr-fastapi': {'ip': 'localhost', 'port': '5060'}, 
            'fd_yolo': {'ip': 'localhost', 'port': '8010'}, 
            'fd_ocr': {'ip': 'localhost', 'port': '8000'}
         }
        """
        self.ppocr_fastapi_ip= data_dict["ppocr-fastapi"]["ip"]
        self.ppocr_fastapi_port= data_dict["ppocr-fastapi"]["port"]
        self.fd_yolo_ip= data_dict["fd_yolo"]["ip"]
        self.fd_yolo_port= data_dict["fd_yolo"]["port"]
        self.fd_ocr_ip= data_dict["fd_ocr"]["ip"]
        self.fd_ocr_port= data_dict["fd_ocr"]["port"]
        self.category_name=self.yaml_label() # yolo文件标签

    def yaml_label(self,yaml_path: str = "config/label.yaml"):
        """
        查找指定目录及其子目录下所有的YAML文件（.yaml 或 .yml）
        :param yaml_path: 目录路径
        :return: None
        """
        # 加载yaml文件,读取标签
        if yaml_path:
            with open(yaml_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                logger.success(f"yaml文件加载成功:{data['names']}")
                return data['names']
        else:
            logger.error("未找到yaml文件,请检查config/yolo_yaml是否存在yaml文件")
            return False

    def ocr_dispose(self, dic_parameter, ls_texts):
        """
        处理OCR识别结果，返回格式化的结果字典。
        :param dic_parameter: 字典，包含目标区域的信息
        :param ls_texts: OCR识别结果列表
        :return: 格式化后的OCR识别结果字典
        """
        def find_closest_index(x_ocr, y_ocr, dic, diff:int=5):
            key_ls = []
            for key, value in dic.items():
                if value["scope"][0] - diff <= x_ocr <= value["scope"][2] + diff and value["scope"][1] - diff <= y_ocr <= value["scope"][3] + diff:
                    key_ls.append(key)
            return key_ls if key_ls else None

        dic_res = {}
        key_num = 0
        for text, x, y, confidence in ls_texts:
            index_ls = find_closest_index(x, y, dic_parameter)
            if index_ls is not None:
                for index in index_ls:
                    if text in dic_res.keys():
                        key_num += 1
                        dic_res.update({f"{text}_{key_num}": (x, y, confidence, index)})
                    else:
                        dic_res.update({text: (x, y, confidence, index)})

        return dic_res

    def convert_dict_to_tuples(self,data_dict,x3:int=0,y3:int=0):
        """
        将字典转换为元组列表。

        :param data_dict: 包含键和坐标信息的字典
        :return: 包含元组的列表
        """
        result = []

        # 遍历字典中的每个键值对
        for key, values in data_dict.items():
            for value in values:
                # 提取所需的元素并构建元组
                tuple_entry = (key, value[0]+x3, value[1]+y3, value[4])
                result.append(tuple_entry)

        return result

    def convert_dict_format(self,data):
        """
        将给定的字典格式转换为新的元组格式。
        :param data: 包含路径和字典的字典
        :return: 转换后的字典
        """
        result = {}

        for key, value in data.items():
            # 从原字典中提取 scope 和 con
            scope = value['scope']
            con = value['con']

            # 创建新的元组格式
            result[key] = (scope[0], scope[1], scope[2], scope[3], con)

        return result

    def image_processing_bytes(self,numpy_array, data_dict: dict):
        """
           api对应接口:图片处理
           截取整个画面,分割图片.
           目标图和分割后的图片进行对比,
           进行多次的比对,以字典的形式返回结果
           支持不同目标和相同目标
           [{'confidence': 1.0, 'rectangle': [881, 372], 'target_image': 'demo2.png'}, {'confidence': 1.0, 'rectangle': [1068, 461], 'target_image': 'demo3.png'}]
           """

        sub_images_dict={} # 小图字典
        sub_images_dict_ac={}

        for key, value in data_dict.items():
            enable=value.get("enable", True) # 获取启用状态
            if enable == "ban":  # 如果启用状态为ban, 跳过该参数
                enable = False

            # logger.debug(f"启用状态:{enable}")
            # 获取模型类型,默认为0
            model = value.get("model", 0)

            if model == 0 and enable: # 如果模型类型为0且启用状态为True
                sub_images_dict.update({key:(*value["scope"], value["con"])})
            if model == 1 and enable: # 如果模型类型为1且启用状态为True
                sub_images_dict_ac.update({key:(*value["scope"], value["con"])})

        # 查找小图在大图中的位置
        results = self.image_finder.find(numpy_array, sub_images_dict)
        # logger.success(f"图片识别结果:{results}")

        results_ac=self.image_matcher.match_sub_images(numpy_array, sub_images_dict_ac)

        # logger.success(f"图片识别结果:{results}")
        if results_ac:
            results.update(results_ac)
        return results


    def word_processing_bytes(self, numpy_array, data_dict: dict):
        """
        res=fd_ocr("fd/images/00001.jpg")
        print(res)
        :param numpy_array: numpy数组
        :param data_dict: 图片裁剪信息
        :return: 成功:["名称",x,y,con],失败[]
        """
        # logger.info(f"文字处理参数:{data_dict}")

        ls_ocr = {}
        model_1_dict={}
        res_texts = []

        try:
            # 使用cv2.imdecode解码图像
            screenshot_image = numpy_array
            height, width, _ = screenshot_image.shape

            # 为不同模型创建两个不同的 combined_image
            combined_image_model_0 = np.zeros((height, width, 3), dtype=np.uint8)

            for key, value in data_dict.items():
                enable = value.get("enable", True)  # 获取启用状态
                if enable=="ban": # 如果启用状态为ban, 跳过该参数
                    enable=False
                x1, y1, x2, y2 = value["scope"]
                con = value["con"]

                # 获取模型类型,默认为0
                model = value.get("model", 0)

                # 裁剪区域
                cropped_region = screenshot_image[y1:y2, x1:x2, :]  # 裁剪区域

                if model == 0 and enable:
                    combined_image_model_0[y1:y2, x1:x2, :] = cropped_region  # 复制到 combined_image_model_0 上

                elif model == 1 and enable:
                    # 直接调用 ppocr_detect 处理裁剪区域
                    res_dict = self.ocrclient_handler.run(cropped_region, url_ip=self.ppocr_fastapi_ip, url_port=self.ppocr_fastapi_port)  # 使用裁剪的区域进行高精度识别
                    # logger.success(f"高精度模型识别结果:{res_dict}")
                    if res_dict:
                        res_tuple = self.convert_dict_to_tuples(res_dict,x1,y1)
                        # logger.info(f"转换后的元组:{res_tuple}")
                        result = self.ocr_dispose(data_dict, res_tuple)
                        # logger.success(f"高精度模型识别结果:{result}")
                        model_1_dict.update(result)

            # 处理 model == 0 的图像
            if np.any(combined_image_model_0):  # 检查 combined_image_model_0 是否有内容
                model_name = "pp_ocr"
                model_version = "1"
                url = self.fd_ocr_ip + f":{self.fd_ocr_port}"
                runner = SyncGRPCTritonRunner(url, model_name, model_version)

                # 裁剪过的图片识别
                im = np.array([combined_image_model_0, ])
                result = runner.Run([im, ])
                batch_texts = result['rec_texts']
                batch_scores = result['rec_scores']
                batch_bboxes = result['det_bboxes']

                for i_batch in range(len(batch_texts)):
                    texts = batch_texts[i_batch]
                    scores = batch_scores[i_batch]
                    bboxes = batch_bboxes[i_batch]
                    for i_box in range(len(texts)):
                        # 将坐标点列表拆分为x和y坐标的列表
                        x_coords = bboxes[i_box][::2]  # 每隔一个元素取一个,即所有x坐标
                        y_coords = bboxes[i_box][1::2]  # 从第一个y坐标开始,每隔一个元素取一个
                        x_min = int(min(x_coords))
                        y_min = int(min(y_coords))
                        text = (texts[i_box].decode('utf-8'), x_min, y_min, float(round(scores[i_box], 3)))
                        res_texts.append(text)

                # logger.info(f"模型0识别结果:{res_texts}")
                # 调用函数处理识别结果
                ls_ocr = self.ocr_dispose(data_dict, res_texts)

        except Exception as e:
            if "index 0 is out of bounds for axis 0 with size 0" in str(e):
                logger.warning(f"没有检测到文字")
            else:
                logger.error(f"错误提示:{e}")

        # logger.error(f"model_1_dict最终识别结果:{model_1_dict}")
        # logger.success(f"最终识别结果:{ls_ocr}")
        ls_ocr.update(model_1_dict)
        return ls_ocr

    def yolo_processing_bytes(self,numpy_array,data_dict: dict, con: float):
        result_yolo = []
        if any(value.get('enable') == 'ban' for value in data_dict.values()):
            enable=False
        else:
            enable=True
        if not enable:
            logger.warning(f"不使用yolo检测")
            return result_yolo
        elif enable:
            logger.warning(f"使用yolo检测")
            model_name = "yolov5"
            model_version = "1"
            url = self.fd_yolo_ip + f":{self.fd_yolo_port}"
            runner = SyncGRPCTritonRunner(url, model_name, model_version)
            # logger.info(f"category_name:{self.category_name}")
            try:
                # 使用cv2.imdecode解码图像
                im = numpy_array
                im = np.array([im, ])
                for i in range(1):
                    result = runner.Run([im, ])
                    # print(f"yolo识别结果:{result}")
                    if result:
                        for name, values in result.items():
                            for j in range(len(values)):
                                value = values[j][0]
                                dic_res = json.loads(value)
                                for box, score, label_id in zip(dic_res['boxes'], dic_res['scores'], dic_res['label_ids']):
                                    x_min, y_min, _, _ = box  # 我们只取 x_min, y_min
                                    name_label = self.category_name[label_id]  # 根据label_id获取对应的类别名称
                                    # 假设我们取分数的整数部分，也可以根据需要保留小数
                                    conf = float(round(score, 3))  # 如果需要保留两位小数，则改为 int(score * 100)
                                    if conf >= con:
                                        result_yolo.append([name_label, int(x_min), int(y_min), conf])
            except Exception as e:
                if type(e).__name__ == "KeyError":
                    logger.error(f"category_name里没有这个label_id,请检查category_name")
                elif type(e).__name__ == "TypeError":
                    logger.error(f"请检查config/label.yaml是否存在yaml文件")
                else:
                    # 记录错误日志
                    logger.error(f"错误提示: {type(e).__name__} - {str(e)}")

        # logger.success(f"yolo识别结果:{result_yolo}")
        return result_yolo

    def color_processing_bytes(self,numpy_array, color_dict):
        """
        颜色获取
        """
        dic_color = {}
        # 使用cv2.imdecode解码图像
        img = numpy_array
        for key, value in color_dict.items():
            # 假设value是一个包含两个整数值的列表，代表坐标(x, y)
            x, y = int(value[0]), int(value[1])
            color = img[y, x]  # 注意：y, x的顺序,OpenCV使用BGR格式
            # 转换为RGB,(R, G, B, key,x,y)格式,便于后续处理
            rgb_color = (int(color[0]), int(color[1]), int(color[2]), key, x, y)
            if type(key) == str and len(key) == 6:  # 将16进制颜色字符串转换为RGB元组
                key_color = tuple(int(key[i:i + 2], 16) for i in (0, 2, 4))
                dic_color.update({key_color: rgb_color})
            if type(key) != str or len(key) != 6:  # 说明不是16进制颜色
                dic_color.update({key: rgb_color})

        # if dic_color:
        #     # 转换后的字典
        #     converted_res = {}
        #     for key, value in dic_color.items():
        #         # 将元组中的 uint8 转换为普通整数, 其他元素保持不变
        #         converted_res[key] = tuple(int(v) if isinstance(v, (np.uint8, int)) else v for v in value)
        #     dic_color=converted_res

        # logger.success(f"颜色获取结果:{dic_color}")
        return dic_color

    def mutil_colors_bytes(self,numpy_array, data_dict: dict):
        """多颜色范围获取"""
        mutil_colors_dict = {}
        # 使用cv2.imdecode解码图像
        screenshot_image = numpy_array
        # 使用aircv读取目标图片,图片在image文件夹里具体再改
        # 梨花义3:{'f0e8df': (1211, 391), '2df9f9': (1268, 390), 'cd110d': (1380, 394), 'scope': (1179, 249, 1394, 557), 'tolerance': 10}
        for color_name, color_parameters in data_dict.items():
            # 分割图片
            enable = color_parameters.get("enable", True)  # 获取启用状态
            x1, y1, x2, y2 = color_parameters["scope"]
            image_array = screenshot_image[y1:y2, x1:x2]
            colors = color_parameters["colors"]
            tolerance = color_parameters["tolerance"]
            if enable: # 如果启用状态为True
                res_colors_ls = multipoint_colors(image_array, colors, tolerance, x1, y1)
                if res_colors_ls:
                    mutil_colors_dict.update({color_name: res_colors_ls})

        if mutil_colors_dict:
            # 转换为普通整数
            for key in mutil_colors_dict:
                mutil_colors_dict[key] = [(int(x), int(y)) for x, y in mutil_colors_dict[key]]
        # logger.success(f"多颜色范围获取结果:{mutil_colors_dict}")
        return mutil_colors_dict

    def data_treating_bytes_area(self, treating_dict: dict, res_numpy, debug=False):
        """
        treating_dict = {"word":{1: (136, 19, 213, 39, 0.8), 2:(649,40,710,71,0.8),3:(1118,175,1198,203,0.8)},
                   "image": {'res/dtws/target/zxtx_1.bmp':( 577, 46, 726, 108, 0.8)},
                   "yolo":0.8,
                   "color":{"bf362a":(692,79)}}
        res=data_treating(win_hwnd,treating_dict)
        图片识别处理
        treating_dict:处理信息:
        :return:
        """
        res_treating = {}  # 结果数据存入
        for key in ["image", "word", "yolo", "color","mutil_colors"]:
            treating_dict.setdefault(key, None)

        if res_numpy.size>0:
            if debug:
                # 使用 Matplotlib 保存彩色图像
                # 创建图像并保存
                image = Image.fromarray(res_numpy)
                image.save('resource/images_info/demo/numpy.png')
                logger.success(f"保存成功")
                time.sleep(5)

            bgr_array = cv2.cvtColor(res_numpy, cv2.COLOR_RGB2BGR)

            if treating_dict["image"] is not None:  # 静态图片识别
                static_ls = self.image_processing_bytes(bgr_array, treating_dict["image"])
                res_treating.update({"image": static_ls})

            if treating_dict["word"] is not None:  # 文字识别
                ocr_ls = self.word_processing_bytes(bgr_array, treating_dict["word"])
                res_treating.update({"word": ocr_ls})

            if treating_dict["yolo"] is not None:  # yolo识别
                yolo_ls = self.yolo_processing_bytes(bgr_array,treating_dict["yolo"], 0.8)  # yolo识别
                res_treating.update({"yolo": yolo_ls})

            if treating_dict["color"] is not None:  # 颜色识别
                color_ls = self.color_processing_bytes(bgr_array, treating_dict["color"])
                res_treating.update({"color": color_ls})

            if treating_dict["mutil_colors"] is not None:  # 多颜色识别
                mutil_colors_ls =self. mutil_colors_bytes(bgr_array, treating_dict["mutil_colors"])
                res_treating.update({"mutil_colors": mutil_colors_ls})

        for key in ["image", "word", "yolo", "color", "mutil_colors"]:
            res_treating.setdefault(key, None)
        return {"numpy_data": res_numpy, "treating_data": res_treating}