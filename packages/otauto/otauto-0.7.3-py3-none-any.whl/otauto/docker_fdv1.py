import numpy as np
from typing import Optional
import cv2
import json
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput

"""
下载依赖包:pip3 install tritonclient[all]
更新日志:2024-7-9 10:35:59
pc端Docker-Desktop fd-ocr fd-yolo接口
fd_url = "localhost" #实际docker服务器的ip地址,默认为本机
category_name={} #类别名称，用于识别结果输出,yolo训练的配置文件中获取
"""

fd_url = "localhost"
category_name={}


class SyncGRPCTritonRunner:
    DEFAULT_MAX_RESP_WAIT_S = 120

    def __init__(
            self,
            server_url: str,
            model_name: str,
            model_version: str,
            *,
            verbose=False,
            resp_wait_s: Optional[float] = None, ):
        self._server_url = server_url
        self._model_name = model_name
        self._model_version = model_version
        self._verbose = verbose
        self._response_wait_t = self.DEFAULT_MAX_RESP_WAIT_S if resp_wait_s is None else resp_wait_s

        self._client = InferenceServerClient(
            self._server_url, verbose=self._verbose)
        error = self._verify_triton_state(self._client)
        if error:
            raise RuntimeError(
                f"Could not communicate to Triton Server: {error}")

        model_config = self._client.get_model_config(self._model_name,
                                                     self._model_version)
        model_metadata = self._client.get_model_metadata(self._model_name,
                                                         self._model_version)

        self._inputs = {tm.name: tm for tm in model_metadata.inputs}
        self._input_names = list(self._inputs)
        self._outputs = {tm.name: tm for tm in model_metadata.outputs}
        self._output_names = list(self._outputs)
        self._outputs_req = [
            InferRequestedOutput(name) for name in self._outputs
        ]

    def Run(self, inputs):
        """
        Args:
            inputs: list, Each value corresponds to an input name of self._input_names
        Returns:
            results: dict, {name : numpy.array}
        """
        infer_inputs = []
        for idx, data in enumerate(inputs):
            infer_input = InferInput(self._input_names[idx], data.shape,
                                     "UINT8")
            infer_input.set_data_from_numpy(data)
            infer_inputs.append(infer_input)

        results = self._client.infer(
            model_name=self._model_name,
            model_version=self._model_version,
            inputs=infer_inputs,
            outputs=self._outputs_req,
            client_timeout=self._response_wait_t, )
        results = {name: results.as_numpy(name) for name in self._output_names}
        return results

    def _verify_triton_state(self, triton_client):
        if not triton_client.is_server_live():
            return f"Triton server {self._server_url} is not live"
        elif not triton_client.is_server_ready():
            return f"Triton server {self._server_url} is not ready"
        elif not triton_client.is_model_ready(self._model_name,
                                              self._model_version):
            return f"Model {self._model_name}:{self._model_version} is not ready"
        return None


def fd_yolo(picture_path: str):
    """
    res=fd_yolo("fd/images/00001.jpg")
    print(res)
    :summary: 使用yolo模型进行图片检测
    :param picture_path: 图片路径
    :return: 成功:["名称",x,y,con],失败[]
    """
    result_yolo = []
    model_name = "yolov5"
    model_version = "1"
    url = fd_url + ":8011"
    runner = SyncGRPCTritonRunner(url, model_name, model_version)
    try:
        im = cv2.imread(picture_path)
        im = np.array([im, ])
        for i in range(1):
            result = runner.Run([im, ])
            if result:
                for name, values in result.items():
                    for j in range(len(values)):
                        value = values[j][0]
                        dic_res = json.loads(value)
                        for box, score, label_id in zip(dic_res['boxes'], dic_res['scores'], dic_res['label_ids']):
                            x_min, y_min, _, _ = box  # 我们只取 x_min, y_min
                            name_label = category_name[label_id]
                            # 假设我们取分数的整数部分，也可以根据需要保留小数
                            conf = round(score, 3)  # 如果需要保留两位小数，则改为 int(score * 100)
                            result_yolo.append([name_label, int(x_min), int(y_min), conf])
    except Exception as e:
        logger.error(f"错误提示:{e}")
    return result_yolo


def word_vnc(numpy_array,x1,y1):
    """
    :numpy_array: numpy数组
    :return: 成功:["名称",x,y,con],失败[]
    """
    ls_ocr = []
    res_texts = []
    model_name = "pp_ocr"
    model_version = "1"
    url = fd_url + ":8001"
    runner = SyncGRPCTritonRunner(url, model_name, model_version)
    try:
        im = np.array([numpy_array, ])
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
                x_coords = bboxes[i_box][::2]  # 每隔一个元素取一个，即所有x坐标
                y_coords = bboxes[i_box][1::2]  # 从第一个y坐标开始，每隔一个元素取一个
                x_min = min(x_coords)
                y_min = min(y_coords)
                text = (texts[i_box].decode('utf-8'), x_min+x1, y_min+y1, round(scores[i_box], 3))
                res_texts.append(text)
        # 调用函数处理识别结果
        ls_ocr=res_texts
    except Exception as e:
        if "index 0 is out of bounds for axis 0 with size 0" in str(e):
            logger.warning(f"没有检测到文字")
        else:
            logger.error(f"错误提示:{e}")
    return ls_ocr


def fd_ocr(image_array: np.ndarray):
    """
    使用OCR模型进行图片检测
    :param image_array: 输入的图像数据（NumPy数组）
    :return: 成功: ["名称", x, y, con], 失败: []
    """
    res_texts = []
    model_name = "pp_ocr"
    model_version = "1"
    url = fd_url + ":8001"
    runner = SyncGRPCTritonRunner(url, model_name, model_version)

    try:
        # 检查输入是否为 NumPy 数组
        if not isinstance(image_array, np.ndarray):
            raise ValueError("输入必须是一个 NumPy 数组")

        # 转换 BGR 到 RGB（如果需要）
        if image_array.shape[-1] == 3:  # 确保是三通道图像
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

        # 将图像转换为批处理格式
        im = np.array([image_array, ])

        # 运行推理
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
                x_coords = bboxes[i_box][::2]  # 每隔一个元素取一个，即所有x坐标
                y_coords = bboxes[i_box][1::2]  # 从第一个y坐标开始，每隔一个元素取一个
                x_min = min(x_coords)
                y_min = min(y_coords)
                text = (texts[i_box].decode('utf-8'), x_min, y_min, round(scores[i_box], 3))
                res_texts.append(text)
    except Exception as e:
        if "index 0 is out of bounds for axis 0 with size 0" in str(e):
            logger.warning("没有检测到文字")
        else:
            logger.error(f"错误提示: {e}")

    return res_texts
# numpy_array=cv2.imread(r"D:\pc_work\pc_script\communication\fd\2024-12-19-090022.png")
# res=word_vnc(numpy_array,0,0)
# print(res)