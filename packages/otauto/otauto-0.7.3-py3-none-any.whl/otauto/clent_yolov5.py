import requests
from PIL import Image
import numpy as np
import io


def calculate_midpoint(bbox):
    x1, y1, x2, y2 = bbox
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    return int(x), int(y)


def yolov5_detect(image_input, model_name,url_ip:str='127.0.0.1',url_port:str='5050'):
    """
    yolov5模型预测
    #示例代码
    # 使用文件路径
    image_path = r"D:\pc_work\yolov5-master\datasets\main\images\screenshot_20241110_121344.jpg"
    detections = yolov5_detect(image_path, 'yolov5n')
    print(detections)

    # 使用 PIL 图像对象
    img = Image.open(image_path)
    detections = yolov5_detect(img, 'yolov5n')
    print(detections)

    # 使用 NumPy 数组
    numpy_array = np.array(img)
    detections = yolov5_detect(numpy_array, 'yolov5n')
    print(detections)
    # 预测图片
    detections = yolov5_detect(image_path, model_name)
    print(detections)
    :param image_input: 可以是图像路径（字符串），也可以是PIL图像对象或者NumPy数组
    :param model_name: 要使用的yolov5模型名称，例如'yolov5n'
    :return: 检测结果
    """
    if isinstance(image_input, str):
        # 处理图像路径字符串
        with open(image_input, 'rb') as image_file:
            files = {'file': image_file}
            response = requests.post(f"http://{url_ip}:{url_port}/predict/{model_name}", files=files)
    elif isinstance(image_input, Image.Image):
        # 处理PIL图像对象
        image_bytes = io.BytesIO()
        image_input.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        files = {'file': ('image.png', image_bytes, 'image/png')}
        response = requests.post(f"http://{url_ip}:{url_port}/predict/{model_name}", files=files)
    elif isinstance(image_input, np.ndarray):
        # 处理NumPy数组
        img = Image.fromarray(image_input)
        image_bytes = io.BytesIO()
        img.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        files = {'file': ('image.png', image_bytes, 'image/png')}
        response = requests.post(f"http://{url_ip}:{url_port}/predict/{model_name}", files=files)
    else:
        return "Invalid image input type"

    if response.status_code == 200:
        results = response.json()
        if results:
            for item in results:
                # Convert bbox to integers
                item['bbox'] = [int(coord) for coord in item['bbox']]
                # Calculate midpoint
                item['midpoint'] = calculate_midpoint(item['bbox'])
                # Round confidence to three decimal places
                item['confidence'] = round(item['confidence'], 3)
        return results
    else:
        return f"Error: {response.status_code} - {response.text}"


# # 使用文件路径
# image_path = r"D:\pc_work\yolov5-master\datasets\main\images\screenshot_20241110_121344.jpg"
# detections = yolov5_detect(image_path, 'yolov5n')
# print(detections)

# # 使用 PIL 图像对象
# img = Image.open(image_path)
# detections = yolov5_detect(img, 'yolov5n')
# print(detections)
#
# # 使用 NumPy 数组
# numpy_array = np.array(img)
# detections = yolov5_detect(numpy_array, 'yolov5n')
# print(detections)