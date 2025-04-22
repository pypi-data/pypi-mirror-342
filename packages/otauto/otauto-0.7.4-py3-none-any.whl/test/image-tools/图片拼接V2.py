import os

import cv2


def stitch_images(image_paths):
    # 读取所有图片
    images = [cv2.imread(img_path) for img_path in image_paths]

    # 创建 Stitcher 对象
    stitcher = cv2.Stitcher_create()

    # 拼接图片
    status, stitched_image = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        print("拼接成功!")
        # 显示结果
        cv2.imshow('Stitched Image', stitched_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # 保存结果
        cv2.imwrite('004/stitched_image.jpg', stitched_image)
    else:
        print("拼接失败，错误代码: ", status)


def get_image_paths_from_folder(folder_path):
    # 获取文件夹中的所有图片路径
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']  # 可以根据需要添加其他图片格式
    image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                   if os.path.isfile(os.path.join(folder_path, f)) and
                   os.path.splitext(f)[1].lower() in image_extensions]
    return image_paths

# 指定图片所在的文件夹路径
folder_path = r'D:\pc_work\pc_script-otauto\image-tools\004'  # 替换为你的文件夹路径

# 获取图片路径列表
image_paths = get_image_paths_from_folder(folder_path)

# 调用拼接函数
stitch_images(image_paths)