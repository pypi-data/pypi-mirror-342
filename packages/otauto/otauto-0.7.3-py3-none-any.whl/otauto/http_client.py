import base64
import sys

import requests
import json
import cv2
import numpy as np

def get_image_info(image_path):

    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return height, width, rgb_img



image_path = "12.jpg"
height, width, rgb_img = get_image_info(image_path)
rgb_img = rgb_img.tolist()
image_shape = [1]
image_shape.append(height)
image_shape.append(width)
image_shape.append(3)
# image_shape = np.array(image_shape)

data ={
  "inputs": [
    {
      "name": "INPUT",
      "shape": image_shape,
      "datatype": "UINT8",
      "data": rgb_img
    }
  ],
  "outputs": [
    {
      "name": "rec_texts"
    },
    {
      "name": "rec_scores"
    },
    {
      "name": "det_bboxes"
    }
  ]
}


url = "http://124.71.102.56:8000/v2/models/pp_ocr/versions/1/infer"
headers = {"Content-type": "application/json"}
r = requests.post(url=url, headers=headers, data=json.dumps(data))
result = r.json()['outputs']
batch_texts = result[2]['data']
batch_scores = result[1]['data']
batch_bboxes = result[0]['data']
print(len(batch_texts))
print(len(batch_scores))
print(len(batch_bboxes))
for i in range(len(batch_texts)):
    print('text=',batch_texts[i], ' score=',batch_scores[i], ' bbox=', batch_bboxes[i*8:(i+1)*8])