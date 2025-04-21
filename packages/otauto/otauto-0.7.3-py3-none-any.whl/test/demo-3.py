import torch
import kornia as K
import cv2
import numpy as np
from loftr import LoFTR
from loftr.utils.cvpr_ds_config import default_cfg


class ImageMatcher:
    def __init__(self, method='SuperPoint', device=None):
        self.method = method
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") if device is None else device

        if self.method == 'SuperPoint':
            self.model = K.feature.SuperPoint().to(self.device)
        elif self.method == 'LoFTR':
            self.model = LoFTR(config=default_cfg).to(self.device)
            self.model.load_state_dict(torch.load("loftr_outdoor.ckpt")["state_dict"])  # 加载预训练模型
            self.model.eval()
        else:
            raise ValueError("Unsupported method. Use 'SuperPoint' or 'LoFTR'.")

    def load_image(self, image_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (640, 480))  # 统一大小
        img_tensor = K.image_to_tensor(img).float() / 255.0 if self.method == 'SuperPoint' else torch.from_numpy(
            img).float() / 255.0
        img_tensor = img_tensor.unsqueeze(0) if self.method == 'SuperPoint' else img_tensor.unsqueeze(0).unsqueeze(
            0)  # 添加 batch 和 channel 维度
        return img, img_tensor

    def match_images(self, img1_path, img2_path):
        img1, img1_tensor = self.load_image(img1_path)
        img2, img2_tensor = self.load_image(img2_path)

        with torch.no_grad():
            if self.method == 'SuperPoint':
                keypoints1, descriptors1 = self.model(img1_tensor.to(self.device))
                keypoints2, descriptors2 = self.model(img2_tensor.to(self.device))

                # 转换为 numpy 格式
                keypoints1 = keypoints1[0].cpu().numpy()
                keypoints2 = keypoints2[0].cpu().numpy()
                descriptors1 = descriptors1[0].cpu().numpy()
                descriptors2 = descriptors2[0].cpu().numpy()

                # 进行最近邻匹配
                bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
                matches = bf.match(descriptors1.T, descriptors2.T)

                return img1, keypoints1, img2, keypoints2, matches

            elif self.method == 'LoFTR':
                batch = {"image0": img1_tensor.to(self.device), "image1": img2_tensor.to(self.device)}
                self.model(batch)

                mkpts0 = batch["mkpts0_f"].cpu().numpy()
                mkpts1 = batch["mkpts1_f"].cpu().numpy()

                return img1, mkpts0, img2, mkpts1

    def draw_matches(self, img1, keypoints1, img2, keypoints2, matches):
        if self.method == 'SuperPoint':
            img_matches = cv2.drawMatches(
                img1, [cv2.KeyPoint(x[0], x[1], 1) for x in keypoints1.T],
                img2, [cv2.KeyPoint(x[0], x[1], 1) for x in keypoints2.T],
                matches, None
            )
        elif self.method == 'LoFTR':
            img_matches = cv2.drawMatches(
                img1, [cv2.KeyPoint(x[0], x[1], 1) for x in keypoints1],
                img2, [cv2.KeyPoint(x[0], x[1], 1) for x in keypoints2],
                [cv2.DMatch(i, i, 0) for i in range(len(keypoints1))], None
            )
        return img_matches


# 使用示例
if __name__ == "__main__":
    matcher = ImageMatcher(method='SuperPoint')  # 或者使用 'LoFTR'
    img1, keypoints1, img2, keypoints2, matches = matcher.match_images("image1.jpg", "image2.jpg")

    img_matches = matcher.draw_matches(img1, keypoints1, img2, keypoints2, matches)
    cv2.imshow("Matches", img_matches)
    cv2.waitKey(0)
    cv2.destroyAllWindows()