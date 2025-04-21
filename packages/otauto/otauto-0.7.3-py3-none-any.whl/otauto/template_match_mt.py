import cv2
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import time
import os
from loguru import logger

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
    logger.success(f"结果图保存到 {path}")


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
            # eq = cv2.equalizeHist(gray)  # 注释掉这行
            eq = gray  # 直接用灰度图
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
        # img_eq = cv2.equalizeHist(img_gray)  # 注释掉这行
        img_eq = img_gray  # 直接用灰度图

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
            logger.error(f"警告：模板图片不存在 {path}，跳过")
            continue
        pil_t = Image.open(path)
        template_img = pil_to_cv2(pil_t)
        template_imgs.append(template_img)
        roi = param.get('roi', None)  # 支持更复杂的模板ROI，key为'roi'
        template_rois.append(roi)
        con = param.get('con', 0.8)
        per_template_thresholds.append([con])
        paths.append(path)
    return template_imgs, template_rois, per_template_thresholds, paths

def template_match(np_img, template_params, debug=False):
    """
    判断画面
    np_img : numpy数组 rgb格式
    template_params : 图片参数
    debug : 是否保存图片
    """
    # 转成OpenCV BGR格式
    img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)

    # 加载模板
    template_imgs, template_rois, per_template_thresholds, template_paths = load_templates(template_params)
    if len(template_imgs) == 0:
        logger.success("无有效模板，程序退出")
        exit(1)

    matcher = MultiTemplateMatcher_MT(template_imgs, template_rois, nms_thresh=0.3, max_workers=8)

    rois = []
    for param in template_params.values():
        if param.get("enable", True) is False:
            continue
        rois.append(param['scope'])

    start_time = time.time()
    boxes, scores, template_ids = matcher.match(img, rois=rois, per_template_thresholds=per_template_thresholds)
    end_time = time.time()

    if debug:
        result_img = matcher.draw_boxes(img, boxes, template_ids=template_ids)
        save_image(result_img, "../result_template_mt.jpg")
        cv2.imshow("多线程模板匹配结果", result_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    logger.success(f"[多线程模板匹配] 耗时: {end_time - start_time:.3f} 秒")
    logger.success(f"检测到 {len(boxes)} 个匹配")

    # 构造结果字典
    res_dict = {}
    for i, (box, score, tid) in enumerate(zip(boxes, scores, template_ids)):
        x1, y1, x2, y2 = box
        path = template_paths[tid]
        param = template_params.get(path, {})
        if path not in res_dict:
            res_dict[path] = {
                "boxes": [],
                "scores": [],
                "enable": param.get("enable", True),
                "unique": param.get("unique", False),
                "class": param.get("class", []),
                "offset": param.get("offset", (0, 0)),
            }
        offset = param.get("offset", (0, 0))
        center_x = int((x1 + x2) / 2) + offset[0]
        center_y = int((y1 + y2) / 2) + offset[1]
        res_dict[path]["boxes"].append((center_x, center_y))
        res_dict[path]["scores"].append(score)
    return res_dict

# --------- 主程序 ---------
# if __name__ == "__main__":
#     # 模板参数示例，支持roi键定义模板内部裁剪区域
#     # 你的模板参数字典示例（可替换成你的完整字典）
#     template_params = {
#         r"resource/images_info/filter_images/背包界面.png": {
#             "scope": (1031, 655, 1112, 716),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["背包界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/角色信息界面.png": {
#             "scope": (951, 243, 1067, 285),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["角色信息界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/武将界面.png": {
#             "scope": (630, 573, 731, 611),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["地图界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/技能界面.png": {
#             "scope": (391, 535, 444, 631),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["技能界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/奖励界面.png": {
#             "scope": (853, 127, 931, 199),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["奖励界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/驿站界面.png": {
#             "scope": (660, 285, 783, 335),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["驿站界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/杂货界面.png": {
#             "scope": (627, 604, 688, 668),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["杂货界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/好友界面.png": {
#             "scope": (545, 628, 637, 677),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["好友界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/快捷搜索界面.png": {
#             "scope": (981, 547, 1096, 594),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["快捷搜索界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/地图界面.png": {
#             "scope": (1097, 670, 1157, 738),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["地图界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/商城界面.png": {
#             "scope": (1004, 633, 1145, 705),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["商城界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/装备进阶界面.png": {
#             "scope": (640, 165, 752, 204),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["装备进阶界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/枯树界面.png": {
#             "scope": (556, 218, 705, 271),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["枯树界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/系统菜单界面.png": {
#             "scope": (665, 349, 815, 386),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["系统菜单界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/装备强化界面.png": {
#             "scope": (577, 190, 683, 242),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["装备强化界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/爵位提升界面.png": {
#             "scope": (823, 558, 1016, 614),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["爵位提升界面"]
#         },  # 奖励图标
#         r"resource/images_info/filter_images/发布使界面.png": {
#             "scope": (563, 335, 685, 387),
#             "con": 0.8,
#             "model": 1,
#             "enable": True,
#             "unique": True,
#             'class': ["发布使界面"]
#         },  # 奖励图标
#
#     }
#
#     big_img_path = "../2025-04-16-003229.png"  # 替换成你的大图路径
#     if not os.path.exists(big_img_path):
#         print(f"大图不存在 {big_img_path}")
#         exit(1)
#
#     pil_img = Image.open(big_img_path)  # PIL Image
#     np_img = np.array(pil_img)  # numpy数组，RGB顺序
#
#
#     big_img_path = "../2025-04-16-003229.png"
#     if not os.path.exists(big_img_path):
#         print(f"大图不存在 {big_img_path}")
#         exit(1)
#
#     pil_img = Image.open(big_img_path)
#     np_img = np.array(pil_img)
#
#     res_dict = template_match(np_img, template_params, debug=True)
#     print("最终匹配结果字典：")
#     for k,v in res_dict.items():
#         print(f"模板: {k}")
#         print(f"  匹配框: {v['boxes']}")
#         print(f"  匹配分数: {v['scores']}")
#         print(f"  enable: {v['enable']}")
#         print(f"  unique: {v['unique']}")
#         print(f"  class: {v['class']}")


