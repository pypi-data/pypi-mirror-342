import threading
import traceback
from concurrent.futures import ThreadPoolExecutor
import time # 用于暂停程序
import queue # 用于多线程间通信
from loguru import logger # 用于日志记录
from otauto.data_cleansing import DataCleansing
from otauto.image_processing import ImageProcessor
from otauto.vnc_recognition import VNC_recognition
stop_event = threading.Event()  # 创建一个事件用于停止线程
data_ready_event = threading.Event()  # 用于通知数据准备好
thread_local = threading.local() # 用于存储线程私有数据
from otauto.template_match_mt import template_match # 画面过滤

# 创建多个 logger 实例
data_logger = logger.bind(name="data")  # 正常日志记录

class LimitedQueue:
    """
    一个有最大容量的队列
    :param max_size: 队列的最大容量
    """
    def __init__(self, max_size):
        self.queue = queue.Queue(maxsize=max_size)
    def put(self, item):
        if self.queue.full():
            self.queue.get()  # 移除最旧的项
        self.queue.put(item)
    def get(self):
        return self.queue.get()
    def size(self):
        return self.queue.qsize()
    def empty(self):
        return self.queue.empty()
    def __iter__(self):
        return iter(self.queue.queue)


result_queue = LimitedQueue(max_size=1)  # 设定队列最大容量为3


def main_v1(vnc: VNC_recognition, parameter_dict, queue_handle, interval: float = 0.8, image_w: int = 1440,image_h: int = 900):
    """
    主函数
    :param vnc: VNC_recognition对象
    :param parameter_dict: 参数字典
    :param queue_handle: 线程队列
    :param interval: 截图间隔时间,默认为0.6秒
    :param image_w: 图像的宽度，默认为 1440
    :param image_h: 图像的高度，默认为 900
    """
    imageprocessor = ImageProcessor()
    data_cleansing = DataCleansing(parameter_dict)
    screen_flag = True  # 用于控制是否进行截图
    screen_num=0 # 用于统计截图次数
    uuid = None  # 用于存储uuid
    time.sleep(3)

    try:
        while True:
            updated_image = None  # 用于存储更新后的numpy数组
            delay_flag=True # 用于控制暂停司机
            queue_msg = None  # 用于接收线程队列信息
            data_treating_debug = False  # 用于调试

            if not queue_handle.empty():
                queue_msg = queue_handle.get()
                logger.info("收到线程队列信息")

                if "screen_flag" in queue_msg:
                    if queue_msg["screen_flag"]=="False":
                        screen_flag = False
                    elif queue_msg["screen_flag"]=="True":
                        screen_flag = True

                elif "interval" in queue_msg:
                    new_interval = queue_msg["interval"]
                    logger.error(f"信息处理暂停时间为: {new_interval}")
                    time.sleep(new_interval)

                elif "numpy_data" in queue_msg:
                    screen_flag=False
                    uuid=queue_msg["numpy_data"]
                    logger.error(f"uuid:{uuid},同步截图...")
                    updated_image = vnc.capture_full_screen_as_numpy(image_w=image_w, image_h=image_h)
                    screen_num=0
                    if stop_event.is_set():
                        stop_event.clear()  # 清除事件, 以便将来可以重新使用
                        logger.success("数据线程收到停止信号,停止捕获。")
                        return

            if updated_image is None: # 说明没有使用线程队列,同步截图
                screen_num+=1

            if screen_flag : # 如果需要截图
                uuid=None
                logger.error("异步截图...")
                updated_image = vnc.capture_full_screen_as_numpy(image_w=image_w, image_h=image_h)  # 使用同步捕获方法
                if stop_event.is_set():
                    stop_event.clear()  # 清除事件, 以便将来可以重新使用
                    logger.success("数据线程收到停止信号,停止捕获。")
                    return

            if updated_image is not None:
                screen_num=0 # 重置截图次数
                logger.success("数据线程启动成功, Updated image captured successfully!")
                res = imageprocessor.data_treating_bytes_area(parameter_dict, updated_image, data_treating_debug)
                res_dict = res["treating_data"]
                numpy_data = res["numpy_data"]
                res_data = data_cleansing.run(res_dict, numpy_data, queue_msg)
                logger.debug(f"data_cleansing result from main:uuid:{uuid}, data:{res_data}")

                finish_data = {
                    "data_cleansing": res_data,
                    "uptime": time.time(),
                    "numpy_data": res["numpy_data"],
                    "uuid": uuid
                }
                result_queue.put(finish_data)
                data_ready_event.set()  # 通知 run_info 数据已准备好
            else:
                pass

            if delay_flag:
                time.sleep(interval)  # 控制截图间隔
            logger.debug(f"截图策略:{screen_flag},等待次数:{screen_num}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        traceback.print_exc()  # 打印堆栈跟踪

def main(vnc: VNC_recognition, parameter_dict, queue_handle, interval: float = 0.8, image_w: int = 1440,image_h: int = 900):
    """
    主函数
    :param vnc: VNC_recognition对象
    :param parameter_dict: 参数字典
    :param queue_handle: 线程队列
    :param interval: 截图间隔时间,默认为0.6秒
    :param image_w: 图像的宽度，默认为 1440
    :param image_h: 图像的高度，默认为 900
    """
    imageprocessor = ImageProcessor()
    filter_par=parameter_dict["filter"]
    data_cleansing = DataCleansing(parameter_dict)
    screen_flag = True  # 用于控制是否进行截图
    screen_num=0 # 用于统计截图次数
    uuid = None  # 用于存储uuid
    time.sleep(3)

    try:
        while True:
            filter_interface_info_dict = {"主界面": (-1,-1)}
            updated_image = None  # 用于存储更新后的numpy数组
            delay_flag=True # 用于控制暂停司机
            queue_msg = None  # 用于接收线程队列信息
            data_treating_debug = False  # 用于调试

            if not queue_handle.empty():
                queue_msg = queue_handle.get()
                logger.info("收到线程队列信息")

                if "screen_flag" in queue_msg:
                    if queue_msg["screen_flag"]=="False":
                        screen_flag = False
                    elif queue_msg["screen_flag"]=="True":
                        screen_flag = True

                elif "enable" in queue_msg:
                    dic_res= queue_msg["enable"]
                    """
                    "word":{"背包":"ban"}
                    "image":{}
                    "yolo":{}
                    """
                    for key,value in dic_res.items():
                        if key=="word":
                            for key_word, value_word in value.items():
                                parameter_dict["word"][key_word]["enable"]=value_word
                        if key=="image":
                            for key_image, value_image in value.items():
                                parameter_dict["image"][key_image]["enable"]=value_image
                        if key=="yolo":
                            for key_yolo, value_yolo in value.items():
                                parameter_dict["yolo"][key_yolo]["enable"]=value_yolo

                elif "interval" in queue_msg:
                    new_interval = queue_msg["interval"]
                    logger.error(f"信息处理暂停时间为: {new_interval}")
                    time.sleep(new_interval)

                elif "numpy_data" in queue_msg:
                    screen_flag=False
                    uuid=queue_msg["numpy_data"]
                    logger.error(f"uuid:{uuid},同步截图...")
                    updated_image = vnc.capture_full_screen_as_numpy(image_w=image_w, image_h=image_h)
                    screen_num=0
                    if stop_event.is_set():
                        stop_event.clear()  # 清除事件, 以便将来可以重新使用
                        logger.success("数据线程收到停止信号,停止捕获。")
                        return

            if updated_image is None: # 说明没有使用线程队列,同步截图
                screen_num+=1

            if screen_flag : # 如果需要截图
                uuid=None
                logger.error("异步截图...")
                updated_image = vnc.capture_full_screen_as_numpy(image_w=image_w, image_h=image_h)  # 使用同步捕获方法
                if stop_event.is_set():
                    stop_event.clear()  # 清除事件, 以便将来可以重新使用
                    logger.success("数据线程收到停止信号,停止捕获。")
                    return

            if updated_image is not None:
                # 界面过滤
                filter_res = template_match(updated_image, filter_par)
                if filter_res != {}:
                    filter_interface_info_dict = {}  # 清空过滤界面信息
                    logger.error("界面过滤成功")
                    for key, value in filter_res.items():
                        filter_interface_info_dict.update({value["class"][0]: value["boxes"][0]})

                logger.debug(f"界面信息:{filter_interface_info_dict}")
                # {'地图界面': [645, 582, 717, 601]}，只会识别该类别的文字,图片
                key_list = list(filter_interface_info_dict.keys())
                detected_keys = set(key_list)

                def class_matches(detected_keys, interface_class):
                    # interface_class 可能是列表或字符串
                    if isinstance(interface_class, str):
                        return any(key == interface_class or key in interface_class for key in detected_keys)
                    elif isinstance(interface_class, (list, tuple, set)):
                        return any(key in interface_class for key in detected_keys)
                    return False

                for value_word in parameter_dict.get("word", {}).values():
                    interface_class = value_word.get("class", ["主界面"])
                    if value_word["enable"] !="ban":
                        value_word["enable"] = class_matches(detected_keys, interface_class)

                for value_image in parameter_dict.get("image", {}).values():
                    interface_class = value_image.get("class", ["主界面"])
                    if value_image["enable"]!="ban":
                        value_image["enable"] = class_matches(detected_keys, interface_class)

                for value_yolo in parameter_dict.get("yolo", {}).values():
                    interface_class = value_yolo.get("class", ["主界面"])
                    if value_yolo["enable"]!="ban":
                        value_yolo["enable"] = class_matches(detected_keys, interface_class)

                # print(parameter_dict["word"])

                screen_num=0 # 重置截图次数
                logger.success("数据线程启动成功, Updated image captured successfully!")
                res = imageprocessor.data_treating_bytes_area(parameter_dict, updated_image, data_treating_debug)
                res_dict = res["treating_data"]
                numpy_data = res["numpy_data"]
                res_data = data_cleansing.run(res_dict, numpy_data, queue_msg)
                logger.debug(f"data_cleansing result from main:uuid:{uuid}, data:{res_data}")

                finish_data = {
                    "data_cleansing": res_data,
                    "uptime": time.time(),
                    "numpy_data": res["numpy_data"],
                    "uuid": uuid,
                    "filter_interface_info_dict": filter_interface_info_dict
                }
                result_queue.put(finish_data)
                data_ready_event.set()  # 通知 run_info 数据已准备好
            else:
                pass

            if delay_flag:
                time.sleep(interval)  # 控制截图间隔
            logger.debug(f"截图策略:{screen_flag},等待次数:{screen_num}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        traceback.print_exc()  # 打印堆栈跟踪


def run_sync(vnc: VNC_recognition, parameter_dict, queue_handle, interval: float = 0.6, image_w: int = 1440,image_h: int = 900):
    """
    运行同步函数
    :param vnc: VNC_recognition对象
    :param parameter_dict: 参数字典
    :param queue_handle: 线程队列
    :param interval: 截图间隔时间,默认为0.6秒
    :param image_w: 图像的宽度，默认为 1440
    :param image_h: 图像的高度，默认为 900
    """
    main(vnc, parameter_dict, queue_handle, interval, image_w, image_h)

def run_info(task_instance, loop_num: int = 20, delay_time: float = 0.6):
    """
    :param task_instance: 任务类的实例
    :param delay_time: 暂停时间 0.5-1秒,空载的时候最小0.5秒
    :param loop_num: 循环次数
    """
    i = 0
    time.sleep(5)
    wait_num=0 # 用于统计等待的时间

    if task_instance is None:
        logger.error("任务实例未提供.")
        return

    while True:
        time.sleep(delay_time)
        i += 1
        logger.info(f"程序运行中... 当前循环:{i}")
        logger.info(f"等待次数: {wait_num}")

        if i >= loop_num or wait_num>=5:
            logger.success("程序运行到设置的最大数,发送停止信号.")
            stop_event.set()  # 设置停止事件
            return "task_error"

        # 等待数据准备好
        data_ready_event.wait(timeout=5)  # 等待直到数据准备好
        data_ready_event.clear()  # 清除事件, 以便下次使用

        logger.error(f"队列大小: {result_queue.size()}")

        # 检查队列的大小
        if result_queue.size() > 1:
            # 清空队列
            while not result_queue.empty():
                result_queue.get()  # 逐个移除队列中的元素

        if not result_queue.empty():
            wait_num=0 # 等待计数器置0
            latest_result = result_queue.get()
            # 执行任务的 run 方法
            task_result = task_instance.run(latest_result) #todo:这里加其他结果
            if isinstance(task_result, str):
                if task_result in ["task_finish", "task_error", "task_fail", "task_wait"]:
                    logger.success(f"任务完成,发送停止信号.任务结果: {task_result}")
                    stop_event.set()  # 设置停止事件
                    return task_result  # 返回任务结果
            elif isinstance(task_result, dict):
                logger.success(f"任务完成,发送停止信号.任务结果: {task_result}")
                stop_event.set()  # 设置停止事件
                return task_result  # 返回任务结果
        else:
            logger.info("队列为空,没有结果可处理")
            wait_num+=1 # 统计等待+1

def run_in_process(vnc,parameter_dict, task_instance,queue_handle,loop_num:int=20,delay_time=0.5,interval: float = 0.6,image_w: int = 1440, image_h: int = 900):
    """
    在进程中运行任务
    :param vnc: VNC_recognition对象
    :param parameter_dict: 参数字典
    :param task_instance: 任务类的实例
    :param queue_handle: 线程队列
    :param loop_num: 循环次数
    :param delay_time: 暂停时间,空载的时候最小0.5秒,不然数据不可信
    :param interval: 截图间隔时间,默认为0.6秒
    :param image_w: 图像的宽度，默认为 1440
    :param image_h: 图像的高度，默认为 900
    """
    with ThreadPoolExecutor(max_workers=2) as executor:
        # 提交任务
        executor.submit(run_sync, vnc, parameter_dict, queue_handle,interval,image_w, image_h)  # 提交第一个任务,用于捕获图像,识别图像,处理数据
        future2 = executor.submit(run_info,task_instance,loop_num,delay_time)  # 提交第二个任务,用于处理数据,执行任务逻辑

        # 只获取 future2 的结果
        try:
            result = future2.result()  # 获取结果
            logger.success(f"任务完成: {result}")
        except Exception as e:
            logger.error(f"任务发生异常: {e}")
            traceback.print_exc()  # 打印堆栈跟踪

    return result


# if __name__ == "__main__":
#     # 使用进程池执行器运行任务
#     with ProcessPoolExecutor() as executor:
#         executor.submit(run_in_process, "192.168.110.245", 5901)  # 启动一个进程并运行 run_in_process
#         executor.submit(run_in_process, "192.168.110.245", 5902)
#         executor.submit(run_in_process, "192.168.110.245", 5903)
#         executor.submit(run_in_process, "192.168.110.245", 5904)