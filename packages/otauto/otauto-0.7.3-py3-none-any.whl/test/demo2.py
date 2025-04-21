import cv2
import numpy as np

class SIFTMatcher:
    def __init__(self, contrastThreshold=0.03, edgeThreshold=5, nOctaveLayers=4, ratio_test=0.75, use_flann=True):
        """
        初始化 SIFT 特征匹配类

        参数:
        - contrastThreshold: SIFT 对比度阈值，影响特征点检测的灵敏度
        - edgeThreshold: SIFT 边缘响应阈值，控制边缘特征点的剔除
        - nOctaveLayers: SIFT 金字塔层数，影响尺度空间的特征检测
        - ratio_test: Lowe’s Ratio Test 阈值，默认为 0.75
        - use_flann: 是否使用 FLANN 进行特征匹配（默认 True）
        """
        self.sift = cv2.SIFT_create(contrastThreshold=contrastThreshold,
                                    edgeThreshold=edgeThreshold,
                                    nOctaveLayers=nOctaveLayers)
        self.ratio_test = ratio_test
        self.use_flann = use_flann

        if self.use_flann:
            # 配置 FLANN 参数
            FLANN_INDEX_KDTREE = 1
            self.index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            self.search_params = dict(checks=50)
            self.matcher = cv2.FlannBasedMatcher(self.index_params, self.search_params)
        else:
            # 使用暴力匹配器（BFMatcher）
            self.matcher = cv2.BFMatcher()

    def detect_and_compute(self, img):
        """
        检测 SIFT 关键点并计算描述子
        """
        keypoints, descriptors = self.sift.detectAndCompute(img, None)
        return keypoints, descriptors

    def match_features(self, img1, img2):
        """
        进行 SIFT 特征匹配，并应用 Lowe’s Ratio Test 和 RANSAC 过滤

        参数:
        - img1: 第一张输入图像（灰度图）
        - img2: 第二张输入图像（灰度图）

        返回:
        - good_matches: 过滤后的匹配点
        - keypoints1, keypoints2: 两张图像的关键点
        - M: 计算出的单应性矩阵（如果 RANSAC 失败，则返回 None）
        """
        # 计算 SIFT 关键点和描述子
        keypoints1, descriptors1 = self.detect_and_compute(img1)
        keypoints2, descriptors2 = self.detect_and_compute(img2)

        # 进行 KNN 近邻匹配
        matches = self.matcher.knnMatch(descriptors1, descriptors2, k=2)

        # Lowe’s Ratio Test 过滤错误匹配
        good_matches = [m for m, n in matches if m.distance < self.ratio_test * n.distance]

        # RANSAC 过滤错误匹配
        if len(good_matches) > 4:  # 至少需要 4 个点计算单应性矩阵
            src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()

            # 仅保留 RANSAC 内点匹配
            refined_matches = [good_matches[i] for i in range(len(matchesMask)) if matchesMask[i]]
        else:
            M = None
            refined_matches = good_matches  # 如果 RANSAC 失败，返回原始匹配

        return refined_matches, keypoints1, keypoints2, M

    def draw_matches(self, img1, img2, keypoints1, keypoints2, matches):
        """
        绘制匹配结果
        """
        img_matches = cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches, None,
                                      flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        return img_matches

# ========== 测试代码 ========== #
if __name__ == "__main__":
    # 读取两张图像（转换为灰度图）
    img1 = cv2.imread("image1.jpg", cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread("image2.jpg", cv2.IMREAD_GRAYSCALE)

    # 创建 SIFTMatcher 对象
    sift_matcher = SIFTMatcher()

    # 进行特征匹配
    matches, keypoints1, keypoints2, M = sift_matcher.match_features(img1, img2)

    # 绘制匹配结果
    img_matches = sift_matcher.draw_matches(img1, img2, keypoints1, keypoints2, matches)

    # 显示匹配结果
    cv2.imshow("SIFT Matches", img_matches)
    cv2.waitKey(0)
    cv2.destroyAllWindows()