import cv2
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import time
import os

# --------- 工具函数 ---------
def pil_to_cv2(pil_img):
    """
    PIL图片转OpenCV BGR格式
    """
    cv_img = np.array(pil_img)
    if pil_img.mode == "RGB":
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
    elif pil_img.mode == "L":
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2BGR)
    return cv_img

def save_image(img, path):
    """
    保存图像到文件
    """
    cv2.imwrite(path, img)
    print(f"结果图保存到 {path}")

# --------- CUDA加速模板匹配 ---------
class CudaTemplateMatcher:
    def __init__(self, template_imgs, thresholds=None):
        """
        CUDA加速模板匹配
        参数:
            template_imgs: list，模板BGR np.ndarray列表
            thresholds: list，匹配阈值列表，默认[0.95, 0.9, 0.85]
        """
        if not cv2.cuda.getCudaEnabledDeviceCount():
            raise RuntimeError("未检测到CUDA设备或OpenCV未编译CUDA支持")
        self.templates = []
        self.template_sizes = []
        self.thresholds = thresholds if thresholds else [0.95, 0.9, 0.85]

        for img in template_imgs:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            eq = cv2.equalizeHist(gray)
            self.templates.append(eq)
            self.template_sizes.append((eq.shape[1], eq.shape[0]))

    def match(self, big_img_gray):
        """
        对大图进行多模板CUDA匹配，返回所有匹配框和分数
        参数:
            big_img_gray: np.ndarray，灰度图（直方图均衡化最好提前做）
        返回:
            boxes, scores, template_ids
        """
        gpu_img = cv2.cuda_GpuMat()
        gpu_img.upload(big_img_gray)
        boxes_all = []
        scores_all = []
        template_ids_all = []

        for tidx, template in enumerate(self.templates):
            w, h = self.template_sizes[tidx]
            gpu_tpl = cv2.cuda_GpuMat()
            gpu_tpl.upload(template)

            matcher = cv2.cuda.createTemplateMatching(cv2.CV_32FC1, cv2.TM_CCOEFF_NORMED)
            res_gpu = matcher.match(gpu_img, gpu_tpl)
            res = res_gpu.download()

            for thresh in self.thresholds:
                loc = np.where(res >= thresh)
                for pt in zip(*loc[::-1]):
                    boxes_all.append([pt[0], pt[1], pt[0]+w, pt[1]+h])
                    scores_all.append(res[pt[1], pt[0]])
                    template_ids_all.append(tidx)

        return boxes_all, scores_all, template_ids_all

# --------- 多线程多模板基于模板匹配 ---------
class MultiTemplateMatcher_MT:
    def __init__(self, template_imgs, template_rois=None, thresholds=None, nms_thresh=0.3, max_workers=4):
        """
        多线程CPU模板匹配
        参数:
            template_imgs: list，模板BGR np.ndarray列表
            template_rois: list，模板内部ROI(x1,y1,x2,y2)或None，默认None
            thresholds: list，匹配阈值列表，默认[0.95,0.9,0.85]
            nms_thresh: float，NMS阈值，默认0.3
            max_workers: int，线程数，默认4
        """
        self.templates = []
        self.template_sizes = []
        if template_rois is None:
            template_rois = [None]*len(template_imgs)

        for img, roi in zip(template_imgs, template_rois):
            if roi is not None:
                x1,y1,x2,y2 = roi
                sub_img = img[y1:y2, x1:x2]
            else:
                sub_img = img

            gray = cv2.cvtColor(sub_img, cv2.COLOR_BGR2GRAY)
            eq = cv2.equalizeHist(gray)
            self.templates.append(eq)
            self.template_sizes.append((eq.shape[1], eq.shape[0]))

        self.thresholds = thresholds if thresholds else [0.95, 0.9, 0.85]
        self.nms_thresh = nms_thresh
        self.max_workers = max_workers

    def nms_with_scores(self, boxes, scores):
        """
        非极大值抑制，去除重叠框
        返回保留框索引
        """
        if len(boxes) == 0:
            return []

        boxes = np.array(boxes)
        scores = np.array(scores)

        x1 = boxes[:,0]
        y1 = boxes[:,1]
        x2 = boxes[:,2]
        y2 = boxes[:,3]

        area = (x2 - x1 + 1) * (y2 - y1 + 1)
        idxs = np.argsort(scores)[::-1]

        pick = []
        while len(idxs) > 0:
            i = idxs[0]
            pick.append(i)
            idxs = idxs[1:]

            if len(idxs) == 0:
                break

            xx1 = np.maximum(x1[i], x1[idxs])
            yy1 = np.maximum(y1[i], y1[idxs])
            xx2 = np.minimum(x2[i], x2[idxs])
            yy2 = np.minimum(y2[i], y2[idxs])

            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)

            inter = w * h
            iou = inter / (area[i] + area[idxs] - inter)
            idxs = idxs[iou <= self.nms_thresh]

        return pick

    def _match_single(self, img_eq, roi, tidx, thresholds):
        """
        单模板单ROI匹配任务，供线程池调用
        """
        x1, y1, x2, y2 = roi
        img_roi = img_eq[y1:y2, x1:x2]
        template = self.templates[tidx]
        w, h = self.template_sizes[tidx]

        results = []
        if img_roi.shape[0] < h or img_roi.shape[1] < w:
            return results

        res = cv2.matchTemplate(img_roi, template, cv2.TM_CCOEFF_NORMED)

        for thresh in thresholds:
            loc = np.where(res >= thresh)
            for pt in zip(*loc[::-1]):
                bx1 = pt[0] + x1
                by1 = pt[1] + y1
                bx2 = bx1 + w
                by2 = by1 + h
                score = res[pt[1], pt[0]]
                results.append( ([bx1, by1, bx2, by2], score, tidx) )
        return results

    def match(self, img, rois=None, per_template_thresholds=None):
        """
        多线程多模板匹配入口
        """
        if rois is None:
            rois = [(0,0,img.shape[1], img.shape[0])]

        if per_template_thresholds is None:
            per_template_thresholds = [self.thresholds]*len(self.templates)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_eq = cv2.equalizeHist(img_gray)

        all_results = []

        tasks = []
        for roi in rois:
            for tidx in range(len(self.templates)):
                tasks.append( (roi, tidx, per_template_thresholds[tidx]) )

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self._match_single, img_eq, roi, tidx, thresholds) for roi,tidx,thresholds in tasks]
            for future in futures:
                res = future.result()
                if res:
                    all_results.extend(res)

        if not all_results:
            return [], [], []

        all_boxes = [r[0] for r in all_results]
        all_scores = [r[1] for r in all_results]
        all_template_ids = [r[2] for r in all_results]

        keep = self.nms_with_scores(all_boxes, all_scores)

        boxes = [all_boxes[i] for i in keep]
        scores = [all_scores[i] for i in keep]
        template_ids = [all_template_ids[i] for i in keep]

        return boxes, scores, template_ids

    def draw_boxes(self, img, boxes, template_ids=None, colors=None, thickness=2):
        """
        绘制匹配框
        """
        img_draw = img.copy()
        if template_ids is None:
            for box in boxes:
                x1,y1,x2,y2 = box
                cv2.rectangle(img_draw, (x1,y1), (x2,y2), (0,255,0), thickness)
        else:
            if colors is None:
                colors = {}
            for i, box in enumerate(boxes):
                tid = template_ids[i]
                if tid not in colors:
                    colors[tid] = tuple(np.random.randint(0,256,3).tolist())
                x1,y1,x2,y2 = box
                cv2.rectangle(img_draw, (x1,y1), (x2,y2), colors[tid], thickness)
        return img_draw

# --------- 基于特征点的匹配（含单应矩阵定位） ---------
class FeaturePointMatcher:
    def __init__(self, template_imgs, min_matches=10):
        """
        ORB特征点匹配器，支持单应矩阵定位
        参数:
            template_imgs: list，模板BGR np.ndarray
            min_matches: int，匹配点数阈值
        """
        self.orb = cv2.ORB_create(nfeatures=1500)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self.templates = []
        self.min_matches = min_matches

        for img in template_imgs:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            kp, des = self.orb.detectAndCompute(gray, None)
            self.templates.append({'kp': kp, 'des': des, 'img': img})

    def match(self, img):
        """
        匹配输入图像，返回匹配结果和估计的匹配区域（单应矩阵投影）
        返回格式:
            results: list，每项为dict，包含:
                template_id: 模板索引
                match_count: 匹配点数
                matches: 匹配对列表
                homography: 3x3单应矩阵 np.ndarray 或 None
                corners: 匹配区域四点坐标 np.ndarray (4,2) 或 None
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kp2, des2 = self.orb.detectAndCompute(gray, None)
        results = []

        if des2 is None:
            return results

        for idx, tpl in enumerate(self.templates):
            if tpl['des'] is None:
                continue
            matches = self.bf.match(tpl['des'], des2)
            matches = sorted(matches, key=lambda x: x.distance)
            good_matches = matches[:self.min_matches]

            if len(good_matches) >= self.min_matches:
                # 估计单应矩阵定位匹配区域
                src_pts = np.float32([tpl['kp'][m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)
                homography, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

                corners = None
                if homography is not None:
                    h, w = tpl['img'].shape[:2]
                    pts = np.float32([[0,0],[w,0],[w,h],[0,h]]).reshape(-1,1,2)
                    dst = cv2.perspectiveTransform(pts, homography)
                    corners = dst.reshape(-1,2)

                results.append({
                    'template_id': idx,
                    'match_count': len(good_matches),
                    'matches': good_matches,
                    'homography': homography,
                    'corners': corners
                })
        return results

    def draw_matches(self, img, template_id, template_img, matches, kp1, kp2, corners=None):
        """
        绘制匹配点和匹配区域
        """
        img_matches = cv2.drawMatches(template_img, kp1, img, kp2, matches, None, flags=2)

        if corners is not None:
            corners = np.int32(corners)
            offset = template_img.shape[1]
            # 画匹配区域多边形，注意大图关键点坐标偏移
            cv2.polylines(img_matches, [corners + np.array([offset,0])], True, (0,255,0), 3, cv2.LINE_AA)
        return img_matches

# --------- 加载模板 ---------
def load_templates(template_params):
    """
    根据模板参数字典加载模板图像及阈值和ROI
    返回:
        template_imgs: list，BGR np.ndarray列表
        template_rois: list，模板内部ROI(x1,y1,x2,y2)或None
        per_template_thresholds: list，匹配阈值列表
        paths: list，模板路径列表
    """
    template_imgs = []
    template_rois = []
    per_template_thresholds = []
    paths = []
    for path, param in template_params.items():
        if param.get("enable", True) is False:
            continue
        if not os.path.exists(path):
            print(f"警告：模板图片不存在 {path}，跳过")
            continue
        pil_t = Image.open(path)
        template_img = pil_to_cv2(pil_t)
        template_imgs.append(template_img)
        roi = param.get('roi', None)  # 支持更复杂的模板ROI，key为'roi'
        template_rois.append(roi)
        con = param.get('con', 0.9)
        per_template_thresholds.append([con])
        paths.append(path)
    return template_imgs, template_rois, per_template_thresholds, paths

# --------- 主程序 ---------
if __name__ == "__main__":
    # 模板参数示例，支持roi键定义模板内部裁剪区域
    # 你的模板参数字典示例（可替换成你的完整字典）
    equip_scope_背包=(611, 309, 1207, 736)
    template_params = {
        r"resource/images_info/demo/飞盘.png": {
            "scope": equip_scope_背包,
            "con": 0.8,
            "enable": True,
            "unique": True,
            "model": 1,
        },
        r"resource/images_info/demo/背包.png": {
            "scope":(1103, 645, 1205, 736),
            "con": 0.8,
            "enable": True,
            "unique": True,
            "model": 1,
        },
        r"resource/images_info/demo/强化.png": {
            "scope": equip_scope_背包,
            "con": 0.8,
            "enable": True,
            "unique": True,
            "model": 1,
        },
        r"resource/images_info/demo/卷轴1.png": {
            "scope": equip_scope_背包,
            "con": 0.8,
            "enable": True,
            "unique": True,
            "model": 1,
        },
        r"resource/images_info/demo/01.png": {
            "scope": (460, 529, 514, 576),
            "con": 0.8,
            "enable": True,
            "unique": True,
            "model": 1,
        },
    }

    big_img_path ="2025-04-16-003229.png" # 替换成你的大图路径
    if not os.path.exists(big_img_path):
        print(f"大图不存在 {big_img_path}")
        exit(1)

    pil_img = Image.open(big_img_path)
    img_cv = pil_to_cv2(pil_img)

    # 选择匹配模式: "template_mt" 多线程模板匹配(CPU)
    #               "template_cuda" CUDA加速模板匹配
    #               "feature" ORB特征点匹配(含单应矩阵定位)
    match_mode = "template_mt"  # 可改为 "template_mt" 或 "feature"

    # 加载模板
    template_imgs, template_rois, per_template_thresholds, template_paths = load_templates(template_params)
    if len(template_imgs) == 0:
        print("无有效模板，程序退出")
        exit(1)

    if match_mode == "template_mt":
        #multitemplatematcher
        matcher = MultiTemplateMatcher_MT(template_imgs, template_rois, nms_thresh=0.3, max_workers=8)
        rois = []
        for param in template_params.values():
            if param.get("enable", True) is False:
                continue
            rois.append(param['scope'])

        start_time = time.time()
        boxes, scores, template_ids = matcher.match(img_cv, rois=rois, per_template_thresholds=per_template_thresholds)
        end_time = time.time()

        print(f"[多线程模板匹配] 耗时: {end_time - start_time:.3f} 秒")
        print(f"检测到 {len(boxes)} 个匹配")
        for i, (box, score, tid) in enumerate(zip(boxes, scores, template_ids)):
            print(f"匹配{i+1}: 模板 {template_paths[tid]}, 位置 {box}, 匹配度 {score:.3f}")

        result_img = matcher.draw_boxes(img_cv, boxes, template_ids=template_ids)
        save_image(result_img, "result_template_mt.jpg")
        cv2.imshow("多线程模板匹配结果", result_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif match_mode == "template_cuda":
        try:
            matcher = CudaTemplateMatcher(template_imgs, thresholds=[0.9, 0.85])
        except RuntimeError as e:
            print("CUDA匹配初始化失败:", e)
            exit(1)

        gray_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        gray_eq = cv2.equalizeHist(gray_img)

        start_time = time.time()
        boxes, scores, template_ids = matcher.match(gray_eq)
        end_time = time.time()

        print(f"[CUDA模板匹配] 耗时: {end_time - start_time:.3f} 秒")
        print(f"检测到 {len(boxes)} 个匹配")
        for i, (box, score, tid) in enumerate(zip(boxes, scores, template_ids)):
            print(f"匹配{i+1}: 模板 {template_paths[tid]}, 位置 {box}, 匹配度 {score:.3f}")

        # CPU NMS
        def nms(boxes, scores, thresh=0.3):
            if len(boxes) == 0:
                return []
            boxes = np.array(boxes)
            scores = np.array(scores)
            x1 = boxes[:,0]
            y1 = boxes[:,1]
            x2 = boxes[:,2]
            y2 = boxes[:,3]
            area = (x2 - x1 + 1) * (y2 - y1 + 1)
            idxs = np.argsort(scores)[::-1]
            pick = []
            while len(idxs) > 0:
                i = idxs[0]
                pick.append(i)
                idxs = idxs[1:]
                if len(idxs) == 0:
                    break
                xx1 = np.maximum(x1[i], x1[idxs])
                yy1 = np.maximum(y1[i], y1[idxs])
                xx2 = np.minimum(x2[i], x2[idxs])
                yy2 = np.minimum(y2[i], y2[idxs])
                w = np.maximum(0, xx2 - xx1 + 1)
                h = np.maximum(0, yy2 - yy1 + 1)
                inter = w * h
                iou = inter / (area[i] + area[idxs] - inter)
                idxs = idxs[iou <= thresh]
            return pick

        keep = nms(boxes, scores, thresh=0.3)
        boxes = [boxes[i] for i in keep]
        scores = [scores[i] for i in keep]
        template_ids = [template_ids[i] for i in keep]

        # 画框
        colors = {}
        result_img = img_cv.copy()
        for box, tid in zip(boxes, template_ids):
            if tid not in colors:
                colors[tid] = tuple(np.random.randint(0,256,3).tolist())
            x1,y1,x2,y2 = box
            cv2.rectangle(result_img, (x1,y1), (x2,y2), colors[tid], 2)
            cv2.putText(result_img, f"{os.path.basename(template_paths[tid])}", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[tid], 1)

        save_image(result_img, "result_template_cuda.jpg")
        cv2.imshow("CUDA模板匹配结果", result_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif match_mode == "feature":
        matcher = FeaturePointMatcher(template_imgs, min_matches=15)

        start_time = time.time()
        results = matcher.match(img_cv)
        end_time = time.time()

        print(f"[特征点匹配] 耗时: {end_time - start_time:.3f} 秒")
        print(f"检测到 {len(results)} 个匹配")

        for res in results:
            tid = res['template_id']
            print(f"匹配模板 {template_paths[tid]}，匹配点数 {res['match_count']}")

        # 画出第一个匹配的结果（匹配点 + 匹配区域）
        if len(results) > 0:
            first = results[0]
            tid = first['template_id']
            tpl = template_imgs[tid]

            kp1, des1 = matcher.orb.detectAndCompute(tpl, None)
            kp2, des2 = matcher.orb.detectAndCompute(img_cv, None)
            matches = first['matches']
            corners = first['corners']

            img_matches = matcher.draw_matches(img_cv, tid, tpl, matches, kp1, kp2, corners)
            save_image(img_matches, "result_feature_match.jpg")
            cv2.imshow("特征点匹配结果", img_matches)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    else:
        print("未知匹配模式，请设置 match_mode 为 'template_mt', 'template_cuda' 或 'feature'")
