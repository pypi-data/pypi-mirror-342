import cv2
import numpy as np
"""
功能:找出2个图片中相似的区域
更新日志:2024-11-12 14:42:13
得到的结果是彩色图
"""

def match_features(image_path1, image_path2, match_threshold=0.75, debug=False):
    # 解码为 Unicode
    image_path1 = image_path1.encode('utf-8').decode('utf-8')
    image_path2 = image_path2.encode('utf-8').decode('utf-8')

    # 加载图片
    img1 = cv2.imdecode(np.fromfile(image_path1, dtype=np.uint8), cv2.IMREAD_COLOR)  # 使用彩色读取
    img2 = cv2.imdecode(np.fromfile(image_path2, dtype=np.uint8), cv2.IMREAD_COLOR)  # 使用彩色读取

    if img1 is None or img2 is None:
        raise ValueError("One of the images could not be loaded. Check the paths.")

    # 转换为灰度图像以便检测特征点（SIFT 在灰度图像上效果更好）
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 初始化 SIFT 描述子
    sift = cv2.SIFT_create()

    # 检测关键点并计算描述符
    keypoints_1, descriptors_1 = sift.detectAndCompute(gray1, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(gray2, None)

    # 使用 BFMatcher 暴力匹配特征点
    bf = cv2.BFMatcher(cv2.NORM_L2)
    matches = bf.knnMatch(descriptors_1, descriptors_2, k=2)

    # 应用 Lowe 的比例测试来筛选匹配
    good_matches = []
    for m, n in matches:
        if m.distance < match_threshold * n.distance:
            good_matches.append(m)

    print(f"Number of good matches: {len(good_matches)}")

    matches_mask = None  # 默认没有匹配掩码
    matched_keypoints_1_coords = []  # 存储匹配的关键点的坐标

    # 使用 RANSAC 进行几何校验
    if len(good_matches) > 4:  # 至少需要4个点进行单应性计算
        src_pts = np.float32([keypoints_1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints_2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        if M is not None:
            matches_mask = mask.ravel().tolist()
            # 计算内点的百分比
            inliers = np.sum(matches_mask)
            total = len(matches_mask)
            inlier_ratio = inliers / total
            print(f"Inlier ratio: {inlier_ratio:.2f}")

            # 提取 RANSAC 内点对应的关键点坐标
            matched_keypoints_1_coords = [keypoints_1[m.queryIdx].pt for i, m in enumerate(good_matches) if matches_mask[i]]

    if debug:
        # 可视化匹配结果
        img_matches = cv2.drawMatches(img1, keypoints_1, img2, keypoints_2, good_matches, None,
                                      matchesMask=matches_mask, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        # 显示匹配结果
        cv2.imshow("Matches", img_matches)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # 保存结果图片到文件
        cv2.imencode('.jpg', img_matches)[1].tofile('../matches_with_中文.jpg')
    else:
        if matches_mask is None:
            print("Not enough matches found for RANSAC.")

    # 如果未执行 RANSAC 或未找到单应性矩阵，将返回所有通过 Lowe 筛选的匹配点
    if not matched_keypoints_1_coords:
        matched_keypoints_1_coords = [keypoints_1[m.queryIdx].pt for m in good_matches]

    # 返回匹配的关键点坐标
    return matched_keypoints_1_coords

# 指定包含中文字符的图片路径
image_path1 = 'res/dtws/other/装备进阶1.png'
image_path2 = 'res/dtws/demo/demo_1.bmp'

# 使用示例
matched_keypoints_coords = match_features(image_path1, image_path2, match_threshold=0.6, debug=True)
print(f"Number of key points in {image_path1}: {len(matched_keypoints_coords)}")
print(f"Key points coordinates in {image_path1}: {matched_keypoints_coords}")
