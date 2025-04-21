import configparser
import importlib
import os
import socket
import sys
import threading
import multiprocessing
import time
import tkinter as tk
from queue import Empty,Queue  # 从标准库的 queue 模块导入 Empty
from tkinter import ttk, messagebox, filedialog

from loguru import logger
from otauto.redis_main import RedisHashManager
import random
import uuid

#文件监控
from watchdog.observers import Observer # 监控文件变化
from watchdog.events import FileSystemEventHandler # 监控文件变化

from otauto.ini_file_operationv2 import INIFileHandler
from otauto.log import Log_Info

from pattern.task_enhanceh import task_enhanced # 强化模式
from pattern.task_setting import task_setting # 设置模式导入
from pattern.task_start import task_start # 起号模式导入
from pattern.task_team_mode import task_team_mode
from pattern.task_test import task_test # 测试模式导入
from pattern.task_friends import task_friends # 好友模式
from pattern.task_wayfinding import task_wayfinding # 寻路模式

"""
更新日志:2024-12-23 17:24:07
1. 增加mongodb数据库操作
2. 增加任务队列
3. 增加任务监控
4. 增加任务执行
5. 增加任务日志
6. 增加任务配置
7. 增加任务状态
8. 增加任务进度
9.运行模式选择
"""

# 获取当前文件的绝对路径
current_file_directory = os.path.abspath(os.path.dirname(__file__))
# 获取项目根目录
TARGET_DIRECTORY = os.path.abspath(os.path.join(current_file_directory, os.pardir))
logger.success(f"项目的绝对路径:{TARGET_DIRECTORY}")
DEFAULT_CONFIG_PATH = "config/config.ini" # 配置文件路径,相对路径

# 存储进程句柄
processes = {}

queue_ui=Queue() # 创建队列,ui信息队列

def generate_uuid_numeric_id(min_length=6, max_length=12):
    # 生成一个 UUID 的整数表示
    unique_id = str(uuid.uuid4().int)
    # 随机选择一个长度在 min_length 和 max_length 之间
    length = random.randint(min_length, max_length)
    # 截取所需长度的数字 ID
    return int(unique_id[:length])

def task_op(row, queue, win_title, running_mode:str="测试模式",log_debug: bool = True):
    """
    任务接入
    :param row: 表格行号
    :param queue: 信息队列
    :param win_title:  窗口标题
    :param log_debug:  是否开启调试日志
    :param running_mode: 运行模式
    :return:
    """
    data_dict = INIFileHandler().get_section_items(win_title)  # 读取配置文件
    logger.info(f"读取配置文件成功: {data_dict}")

    vnc_server = data_dict["vnc_ip"]
    vnc_port_num = int(data_dict["vnc_port"])

    logger.success(
        f"本窗口的基本信息:win_title: {win_title}, vnc_ip: {vnc_server}, vnc_port: {vnc_port_num}")

    if not log_debug: #如果不开启调试日志,则会在电脑上桌面生成日志文件
        logger.remove() # 移除默认的日志记录器
        # Log_Info(local_ip=vnc_server, local_port=vnc_port_num, local_window=win_title).log_init()


    if running_mode=="测试模式": #todo,测试模式代码入口
        logger.info("进入测试模式")

        task_res=task_test(win_title)
        """
        参数说明
        win_title: 窗口标题
        queue: 信息队列
        """
        # 将任务完成的结果放入队列
        queue.put((row, task_res))  # 将结果放入队列
        logger.info(f"任务执行的结果是: {task_res}")

    elif running_mode=="生产模式":
        # task_res=task_起号(int(win_hwnd),queue)
        """
        参数说明
        py: pyautogui对象
        win_hwnd: 窗口句柄
        queue: 信息队列
        """
        # 将任务完成的结果放入队列
        # queue.put((row, task_res))  # 将结果放入队列
        # logger.info(f"任务执行的结果是: {task_res}")


    elif running_mode=="设置模式":
        logger.info("进入设置模式")
        task_res=task_setting(win_title)
        """
        参数说明
        py: pyautogui对象
        win_hwnd: 窗口句柄
        queue: 信息队列
        """
        # 将任务完成的结果放入队列
        queue.put((row, task_res))  # 将结果放入队列
        logger.info(f"任务执行的结果是: {task_res}")

    elif running_mode=="起号模式": #  start
        logger.info("进入起号模式")
        task_res=task_start(win_title)
        """
        参数说明
        py: pyautogui对象
        win_hwnd: 窗口句柄
        queue: 信息队列
        """
        # 将任务完成的结果放入队列
        queue.put((row, task_res))  # 将结果放入队列
        logger.info(f"任务执行的结果是: {task_res}")

    elif running_mode=="好友模式": # friends
        logger.info("进入好友模式")
        task_res=task_friends(win_title)
        """
        参数说明
        py: pyautogui对象
        win_hwnd: 窗口句柄
        queue: 信息队列
        """
        # 将任务完成的结果放入队列
        queue.put((row, task_res))  # 将结果放入队列
        logger.info(f"任务执行的结果是: {task_res}")

    elif running_mode=="强化模式": # enhanced
        logger.info("进入强化模式")
        task_res=task_enhanced(win_title)
        """
        参数说明
        py: pyautogui对象
        win_hwnd: 窗口句柄
        queue: 信息队列
        """
        # 将任务完成的结果放入队列
        queue.put((row, task_res))  # 将结果放入队列
        logger.info(f"任务执行的结果是: {task_res}")

    elif running_mode=="寻路模式": # wayfinding
        logger.info("进入寻路模式")
        task_res=task_wayfinding(win_title)
        """
        参数说明
        py: pyautogui对象
        win_hwnd: 窗口句柄
        queue: 信息队列
        """
        # 将任务完成的结果放入队列
        queue.put((row, task_res))  # 将结果放入队列
        logger.info(f"任务执行的结果是: {task_res}")

    elif running_mode=="团队副本模式": # team_mode
        logger.info("进入团队副本模式")
        task_res=task_team_mode(win_title)
        """
        参数说明
        py: pyautogui对象
        win_hwnd: 窗口句柄
        queue: 信息队列
        """
        # 将任务完成的结果放入队列
        queue.put((row, task_res))  # 将结果放入队列
        logger.info(f"任务执行的结果是: {task_res}")


class ConfigChangeHandler(FileSystemEventHandler):
    """文件夹变化处理类"""
    def __init__(self, app):
        self.app = app

    def on_modified(self, event):
        """文件被修改时调用"""
        if event.src_path.endswith('.py'):
            self.app.reload_script(event.src_path)

    def on_created(self, event):
        """文件被创建时调用"""
        if event.src_path.endswith('.py'):
            self.app.reload_script(event.src_path)

    def on_deleted(self, event):
        """文件被删除时调用"""
        if event.src_path.endswith('.py'):
            self.app.reload_script(event.src_path)

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("游戏UI")
        self.root.geometry("900x600")
        self.config_path = None  # 初始化配置文件路径
        self.redis_manager = RedisHashManager()
        # # 创建信息栏框架
        # self.create_info_bar()

        #运行模式选择
        self.running_mode="测试模式"

        # 当前窗口编号
        self.current_window_num = 1

        # 创建菜单栏
        self.create_menu()

        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_widgets()
        self.fetch_and_update_mongodb_info()
        self.start_file_monitoring()  # 启动文件监控

    def create_menu(self):
        """创建菜单栏"""
        menu_bar = tk.Menu(self.root)

        # 添加配置菜单
        config_menu = tk.Menu(menu_bar, tearoff=0)
        config_menu.add_command(label="加载ini配置", command=self.load_config)
        config_menu.add_command(label="加载yolo_label配置", command=self.yolo_label_config)
        config_menu.add_command(label="设置服务器信息", command=self.show_server_info_dialog)  # 新增的菜单项
        config_menu.add_command(label="设置窗口信息", command=self.show_window_info_dialog)  # 新增的菜单项
        config_menu.add_separator()
        config_menu.add_command(label="退出", command=self.on_close)  # 退出选项
        menu_bar.add_cascade(label="配置", menu=config_menu)

        # 添加其他菜单项
        menu_bar.add_command(label="menu_2", command=self.menu_2_action)
        menu_bar.add_command(label="menu_3", command=self.menu_3_action)
        menu_bar.add_command(label="menu_4", command=self.menu_4_action)

        # 显示菜单栏
        self.root.config(menu=menu_bar)

    def menu_2_action(self):
        """menu_2 的操作"""
        messagebox.showinfo("信息", "你选择了 menu_2")

    def menu_3_action(self):
        """menu_3 的操作"""
        messagebox.showinfo("信息", "你选择了 menu_3")

    def menu_4_action(self):
        """menu_4 的操作"""
        messagebox.showinfo("信息", "你选择了 menu_4")

    # def create_info_bar(self):
    #     """创建信息栏和滚动条"""
    #     info_frame = ttk.Frame(self.root)
    #     info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
    #
    #     # 创建文本框
    #     self.info_text = tk.Text(info_frame, width=50, height=20, wrap=tk.WORD)
    #     self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    #
    #     # 创建滚动条
    #     scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
    #     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    #
    #     # 将滚动条与文本框关联
    #     self.info_text.config(yscrollcommand=scrollbar.set)
    #
    # def update_info_bar(self, message):
    #     """更新信息栏内容"""
    #     self.info_text.insert(tk.END, message + '\n')  # 在文本框末尾插入信息
    #     self.info_text.see(tk.END)  # 确保文本框滚动到最后一行


    def load_config(self):
        """显示文件对话框，允许用户选择配置文件"""
        file_path = filedialog.askopenfilename(title="选择配置文件", filetypes=[("INI files", "*.ini"), ("All files", "*.*")])
        if file_path:  # 如果用户选择了文件
            self.handle_push_button_ini(file_path)  # 处理文件路径
        else:
            messagebox.showwarning("警告", "未选择任何文件！")  # 如果用户未选择文件，显示警告

    def yolo_label_config(self):
        """显示文件对话框，允许用户选择配置文件"""
        file_path = filedialog.askopenfilename(title="选择yolo_label配置文件", filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")])
        if file_path:  # 如果用户选择了文件
            self.handle_push_button_yolo_label(file_path)  # 处理文件路径
        else:
            messagebox.showwarning("警告", "未选择任何文件！")  # 如果用户未选择文件，显示警告

    def show_server_info_dialog(self):
        """显示服务器信息输入对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("输入服务器信息")
        dialog.geometry("300x150")

        ttk.Label(dialog, text="服务器 IP:").pack(pady=5)
        server_ip_entry = ttk.Entry(dialog, width=30)
        server_ip_entry.pack(pady=5)

        def on_confirm():
            server_ip = server_ip_entry.get().strip()
            if self.validate_ip(server_ip):
                logger.info(f"已设置服务器 IP: {server_ip}")
                self.status_bar.config(text=f"已设置服务器 IP: {server_ip}")

                # 写入到默认的 INI 文件中
                self.update_ini_file(server_ip)

                dialog.destroy()  # 关闭对话框
            else:
                messagebox.showerror("错误", "请输入有效的 IP 地址！")

        confirm_button = ttk.Button(dialog, text="确定", command=on_confirm)
        confirm_button.pack(pady=10)

    def update_ini_file(self, server_ip):
        """将服务器 IP 写入到默认的 INI 文件中"""
        config = configparser.ConfigParser()

        # 读取当前的 INI 文件，指定编码为 utf-8
        with open(DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as configfile:
            config.read_file(configfile)

        # 确保 'server' 节存在
        if 'server' not in config:
            config.add_section('server')

        # 更新服务器 IP
        config.set('server', 'server_ip', server_ip)

        # 将更新后的内容写回到 INI 文件
        with open(DEFAULT_CONFIG_PATH, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

        logger.info(f"服务器 IP '{server_ip}' 已写入到 {DEFAULT_CONFIG_PATH} 的 'server' 节中。")

    def show_window_info_dialog(self):
        """显示窗口信息输入对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"输入窗口信息 - 窗口{self.current_window_num}")
        dialog.geometry("500x400")

        # 创建样式
        style = ttk.Style()
        style.configure("Normal.TEntry", foreground="black")  # 正常样式

        # 设置自定义窗口编号输入框
        ttk.Label(dialog, text="窗口编号 (1-199):").pack(pady=5)
        window_num_entry = ttk.Entry(dialog, style="Normal.TEntry", width=30)
        window_num_entry.pack(pady=5, padx=(30, 30), fill=tk.X)  # 设置左右间距并填满宽度

        # 设置 VNC IP 输入框
        ttk.Label(dialog, text="VNC IP:例如 192.168.1.1").pack(pady=5)
        vnc_ip_entry = ttk.Entry(dialog, style="Normal.TEntry", width=30)
        vnc_ip_entry.pack(pady=5, padx=(30, 30), fill=tk.X)  # 设置左右间距并填满宽度

        # 设置 VNC 端口输入框
        ttk.Label(dialog, text="VNC 端口:例如:5900").pack(pady=5)
        vnc_port_entry = ttk.Entry(dialog, style="Normal.TEntry", width=30)
        vnc_port_entry.pack(pady=5, padx=(30, 30), fill=tk.X)  # 设置左右间距并填满宽度

        # 设置角色 ID 输入框
        ttk.Label(dialog, text="角色 ID (多个用,隔开):例如 001,002,003").pack(pady=5)
        role_id_entry = ttk.Entry(dialog, style="Normal.TEntry", width=30)
        role_id_entry.pack(pady=5, padx=(30, 30), fill=tk.X)  # 设置左右间距并填满宽度

        def on_confirm():
            # 获取用户输入的窗口编号，如果没有输入则使用当前窗口编号
            window_num = window_num_entry.get().strip()
            if window_num.isdigit() and 1 <= int(window_num) <= 199:
                window_num = int(window_num)  # 用户输入的有效窗口编号
            else:
                window_num = self.current_window_num  # 使用当前窗口编号作为默认值

            vnc_ip = vnc_ip_entry.get().strip()
            vnc_port = vnc_port_entry.get().strip()
            role_id = role_id_entry.get().strip()

            # 这里可以添加对其他输入的验证
            if self.validate_ip(vnc_ip) and vnc_port.isdigit() and role_id:
                logger.info(
                    f"窗口{window_num} 信息: VNC IP: {vnc_ip}, VNC 端口: {vnc_port}, 角色 ID: {role_id}")
                self.status_bar.config(text=f"已设置窗口{window_num}的信息")

                # 更新或创建 INI 文件中的节
                self.update_window_info_to_ini(window_num, vnc_ip, vnc_port, role_id)

                # 清空输入框
                window_num_entry.delete(0, tk.END)
                vnc_ip_entry.delete(0, tk.END)
                vnc_port_entry.delete(0, tk.END)
                role_id_entry.delete(0, tk.END)

                # 更新窗口编号，确保下一个窗口编号加 1
                self.current_window_num = min(self.current_window_num + 1, 199)  # 限制最大为 199
                dialog.title(f"输入窗口信息 - 窗口{self.current_window_num}")
                window_num_entry.insert(0, str(self.current_window_num))  # 更新窗口编号输入框
            else:
                messagebox.showerror("错误", "输入无效，请检查输入内容！")

        confirm_button = ttk.Button(dialog, text="确定", command=on_confirm)
        confirm_button.pack(pady=10)

    def update_window_info_to_ini(self, window_num, vnc_ip, vnc_port, role_id):
        """将窗口信息写入到默认的 INI 文件中"""
        config = configparser.ConfigParser()

        # 读取当前的 INI 文件，指定编码为 utf-8
        try:
            with open(DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as configfile:
                config.read_file(configfile)
        except FileNotFoundError:
            logger.warning(f"{DEFAULT_CONFIG_PATH} 文件未找到，创建新文件。")

        section_name = f"{window_num:03}"  # 窗口编号格式化为三位数

        # 确保节存在
        if section_name not in config:
            config.add_section(section_name)

        # 更新 VNC IP、VNC 端口和角色 ID
        config.set(section_name, 'vnc_ip', vnc_ip)
        config.set(section_name, 'vnc_port', vnc_port)
        config.set(section_name, 'role_id', role_id)

        # 将更新后的内容写回到 INI 文件
        with open(DEFAULT_CONFIG_PATH, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

        logger.info(f"窗口信息已写入到 {DEFAULT_CONFIG_PATH} 的节 {section_name} 中。")

    def validate_ip(self, ip):
        """简单的 IP 地址验证"""
        import re
        pattern = re.compile(r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        return re.match(pattern, ip) is not None

    def create_widgets(self):
        """创建UI组件"""
        # 创建版本信息标签
        self.version_label = ttk.Label(self.root, text="版本: 1.0.0", anchor='e')  # 右对齐
        self.version_label.pack(side=tk.BOTTOM, anchor='e', padx=10, pady=5)  # 右下角位置

        # 创建样式
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        style.map("Treeview", background=[('selected', 'lightblue'), ('', 'white')])
        style.configure("Treeview", bordercolor="black", borderwidth=1)

        # 创建模式选择框架
        mode_frame = ttk.Frame(self.root)
        mode_frame.pack(pady=10)

        # 模式选择变量
        self.mode_var = tk.StringVar(value="测试模式")  # 默认选择“测试模式”

        # 创建单选按钮
        modes = ["测试模式","寻路模式","生产模式" ,"起号模式","团队副本模式","采集模式","拉镖模式","阵营模式","强化模式","好友模式","设置模式"]
        for mode in modes:
            ttk.Radiobutton(mode_frame, text=mode, variable=self.mode_var, value=mode,
                            command=self.print_selected_mode).pack(side=tk.LEFT, padx=5)

        # 创建 Treeview 表格
        self.columns = ("win_num", "running_status", "win_hand", "vnc_ip", "vnc_port", "taks_name", "task_info", "position_info",'health_degree',"team_info","combat_info",)
        self.tree = ttk.Treeview(self.root, columns=self.columns, show='headings', height=15)
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        # 设置每列的标题和宽度
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)

        # 创建输入框和按钮
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10)

        # 创建状态栏框架
        status_frame = ttk.Frame(self.root, borderwidth=2, relief=tk.SUNKEN,height=300)  # 创建带边框的框架
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)  # 将框架放在底部并填充宽度

        # 创建状态栏
        self.status_bar = ttk.Label(status_frame, text="欢迎使用应用程序", anchor=tk.W)  # 将状态栏放在框架内
        self.status_bar.pack(side=tk.LEFT, padx=10, pady=5)  # 在框架中放置状态栏，增加内边距

        # 设置状态栏的最大高度
        status_frame.config(height=300)  # 设置框架的最大高度为300

        # 创建按钮框架
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side=tk.LEFT, padx=20, pady=10)

        self.insert_button = ttk.Button(button_frame, text="查找窗口", command=self.insert_data_to_tree)
        self.insert_button.pack(side=tk.LEFT, padx=10)

        self.start_button = ttk.Button(button_frame, text="单窗口启动", command=self.start_process)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = ttk.Button(button_frame, text="单窗口停止", command=self.stop_process)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.start_all_button = ttk.Button(button_frame, text="一键启动所有窗口", command=self.start_all_processes)
        self.start_all_button.pack(side=tk.LEFT, padx=10)

        self.stop_all_button = ttk.Button(button_frame, text="一键停止所有窗口", command=self.stop_all_processes)
        self.stop_all_button.pack(side=tk.LEFT, padx=10)

        # 绑定选择事件
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def print_selected_mode(self):
        """打印用户选择的模式到控制台"""
        selected_mode = self.mode_var.get()
        self.running_mode = selected_mode
        logger.info(f"用户选择的模式: {self.running_mode}")
        self.status_bar.config(text=f"程序运行模式: {self.running_mode}")

    def start_file_monitoring(self):
        """启动文件监控"""
        event_handler = ConfigChangeHandler(self) # 创建事件处理器
        observer = Observer() # 创建一个观察者对象
        observer.schedule(event_handler, path=TARGET_DIRECTORY, recursive=False) # 观察指定目录下的文件
        observer.start() # 启动观察者
        self.observer = observer # 将观察者对象保存到实例变量中，以便在需要时停止观察者

    def reload_script(self, file_path):
        """重新加载指定的.py文件"""
        logger.info(f"{file_path} 文件已修改，正在重新加载...")
        try:
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
                self.status_bar.config(text=f"重新加载脚本: {file_path}")  # 更新状态栏
            else:
                logger.warning(f"模块 {module_name} 未加载，无法重新加载。")
                self.status_bar.config(text=f"模块 {module_name} 未加载，无法重新加载。")  # 更新状态栏
        except Exception as e:
            logger.error(f"重新加载模块时发生错误: {e}")
            self.status_bar.config(text=f"重新加载错误: {e}")  # 更新状态栏

    def handle_push_button_ini(self, input_text=None):
        """处理加载配置文件按钮的点击事件"""
        try:
            if input_text is None:  #  如果未提供输入文本，则使用默认值
                input_text = DEFAULT_CONFIG_PATH

            if os.path.isfile(input_text) and input_text.endswith('.ini'):
                logger.success(f"INI 文件路径: {input_text}")
                self.config_path = input_text
                self.status_bar.config(text=f"成功找到 INI 文件: {input_text}")
                # 读取配置文件内容并覆盖 config/config.ini
                self.overwrite_config_file(input_text)
            else:
                self.show_error_message("输入的路径无效，请检查是否为有效的 INI 文件！")
        except Exception as e:
            self.show_error_message(f"处理错误: {e}")

    def handle_push_button_yolo_label(self, input_text=None):
        """处理加载配置文件按钮的点击事件"""
        try:
            if input_text is None:  #  如果未提供输入文本，则使用默认值
                input_text = "config/label.yaml"

            if os.path.isfile(input_text) and input_text.endswith('.yaml'):
                logger.success(f"YAML 文件路径: {input_text}")
                self.status_bar.config(text=f"成功找到 YAML 文件: {input_text}")
                # 读取配置文件内容并覆盖 config/config.ini
                self.overwrite_config_file_yolo(input_text)
            else:
                self.show_error_message("输入的路径无效，请检查是否为有效的 YAML 文件！")
        except Exception as e:
            self.show_error_message(f"处理错误: {e}")

    def overwrite_config_file(self, source_path):
        """覆盖 config/config.ini 文件的内容"""
        target_path = os.path.join("config", "config.ini")  # 目标文件路径

        try:
            # 读取源文件内容,指定 UTF-8 编码
            with open(source_path, 'r', encoding='utf-8') as source_file:
                content = source_file.read()  # 读取源文件内容

            # 写入到目标文件,指定 UTF-8 编码
            with open(target_path, 'w', encoding='utf-8') as target_file:
                target_file.write(content)  # 写入到目标文件

            logger.success(f"成功覆盖文件: {target_path}")
        except Exception as e:
            self.show_error_message(f"覆盖文件时出错: {e}")

    def overwrite_config_file_yolo(self, source_path):
        """覆盖 config/config.ini 文件的内容"""
        target_path = os.path.join("config", "label.yaml")  # 目标文件路径

        try:
            # 读取源文件内容,指定 UTF-8 编码
            with open(source_path, 'r', encoding='utf-8') as source_file:
                content = source_file.read()  # 读取源文件内容

            # 写入到目标文件,指定 UTF-8 编码
            with open(target_path, 'w', encoding='utf-8') as target_file:
                target_file.write(content)  # 写入到目标文件

            logger.success(f"成功覆盖文件: {target_path}")
        except Exception as e:
            self.show_error_message(f"覆盖文件时出错: {e}")

    def show_error_message(self, message):
        """显示错误信息"""
        messagebox.showerror("错误", message)

    def insert_data_to_tree(self):
        """将数据插入到树形视图中"""
        # 查找窗口数据
        new_data = self.find_windows()
        logger.info(f"找到的窗口数据: {new_data}")

        # 获取当前树形视图中的所有项
        current_items = {}
        for index, item in enumerate(self.tree.get_children()):
            values = self.tree.item(item)['values']
            # 格式化第一列的值为三位数的字符串
            formatted_values = [f"{int(values[0]):03}"] + values[1:]  # 保留其他列不变
            current_items[index] = formatted_values  # 使用行号（索引）作为键
            # print(f"行号: {index}, 数据: {formatted_values}")  # 打印每一项的所有数据

        # print("得到的所有数据是", current_items)

        updated_data = []

        # 更新现有项和收集新项
        for item in sorted(new_data, key=lambda x: int(x[1])):
            item_id = item[2]  # 假设 item[2] 是唯一标识符
            # 使用行号作为键，查找现有项
            existing_key = next((k for k, v in current_items.items() if v[2] == item_id), None)

            if existing_key is not None:
                # 如果当前项存在，获取现有值
                existing_values = list(current_items[existing_key])
                # print("现有值:", existing_values)

                # 检查该行是否有数据（假设只要第一列有数据就不更新）
                if existing_values[0] == "":  # 如果第一列为空，则更新
                    # 格式化第一列的值
                    existing_values[0] = f"{int(item[1]):03}"  # 将值格式化为三位数，例如'001'
                    existing_values[2] = item[2]  # 更新第三列的值

                # 将更新后的项加入到 updated_data
                updated_data.append(tuple(existing_values))
            else:
                # 如果当前项不存在，将新项加入到 updated_data
                updated_data.append((f"{int(item[1]):03}", "", item[2], "", "", "", "", ""))  # 格式化新项的第一列

        # 清空树形视图
        self.tree.delete(*self.tree.get_children())

        # 插入更新后的数据
        for values in updated_data:
            self.tree.insert("", tk.END, values=values)


    def fetch_and_update_mongodb_info(self): #todo:从mongodb获取信息并更新到treeview中
        """从MongoDB中获取信息并更新到Treeview中"""
        pass
        # res_ls = []  # 值列表
        # time.sleep(1)
        # key_ls = self.redis_manager.scan_keys("uimsg:*")
        # if len(key_ls) > 0:
        #     for key in key_ls:
        #         res = self.redis_manager.get_hash(key)
        #         res_ls.append(res)
        #
        # logger.info(f"redis_manager:{res_ls}")
        # """
        #  [{'task_name': 'TaskMain', 'task_message': '主线任务', 'team_info': '-1', 'position_info': '白屏寨, 279,54', 'health_degree': '4856/4856', 'combat_info': 'False'}]
        #  """

    def on_tree_select(self, event):
        """处理树形视图行选择事件"""
        selected_item = self.tree.selection()
        if selected_item:
            try:
                item_values = self.tree.item(selected_item, 'values')
                if isinstance(item_values, tuple) and len(item_values) > 0:
                    logger.info(f"选中的行数据: {item_values}")
                else:
                    logger.warning("选中的行数据格式不正确")
            except Exception as e:
                logger.error(f"处理选中行数据时发生错误: {e}")

    def start_process(self):
        """根据选中的行启动一个进程"""
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')
            win_hand = item_values[2]
            win_num = item_values[0]
            logger.info(f"选中的句柄: {win_hand}, 窗口编号: {win_num}")

            self.start_single_process(selected_item, win_num, win_hand)
        else:
            messagebox.showwarning("警告", "请先选择窗口！")

    def start_all_processes(self):
        """启动所有查找到的窗口"""
        all_items = self.tree.get_children()
        if not all_items:
            messagebox.showwarning("警告", "没有找到任何窗口！")
            return

        for item in all_items:
            item_values = self.tree.item(item, 'values')
            win_hand = item_values[2]
            win_num = item_values[0]

            if item_values[1] == "运行中":
                logger.warning(f"窗口 {win_num} 已经在运行中，跳过启动。")
                continue

            self.start_single_process(item, win_num, win_hand)
            time.sleep(5)

        messagebox.showinfo("信息", "所有窗口已启动！")

    def start_single_process(self, item, win_num, win_hand):
        """启动单个窗口的进程"""

        try:
            if self.config_path is None:
                self.config_path = DEFAULT_CONFIG_PATH
                messagebox.showwarning("警告", "使用默认配置文件！请确认是否正确！")
                return  # 如果没有配置文件路径，返回，不启动进程

            # 检查窗口状态
            current_status = self.tree.item(item, 'values')[1]  # 假设状态在第二列
            if current_status == "运行中":
                messagebox.showwarning("警告", f"窗口 {win_num} 已在运行中！请勿重复启动！")
                return  # 如果已经在运行中，返回，不启动进程

            # 读取配置文件
            config = configparser.ConfigParser()
            config.read(self.config_path, encoding='utf-8')

            # 格式化节名
            section_name = f"{int(win_num):03}"  # 确保节名为三位数格式

            # 检查节名是否存在
            if section_name not in config:
                messagebox.showerror("错误", f"未找到窗口编号 {win_num} 对应的配置节！")
                return

            # 获取 vnc_ip 和 vnc_port
            vnc_ip = config.get(section_name, 'vnc_ip', fallback=None)
            vnc_port = config.get(section_name, 'vnc_port', fallback=None)

            if vnc_ip is None or vnc_port is None:
                messagebox.showerror("错误", f"窗口 {win_num} 的 VNC 配置不完整！")
                return

            logger.info(f"窗口 {win_num} 的 VNC 配置: IP = {vnc_ip}, 端口 = {vnc_port}")

            logger.info(f"启动窗口: {win_hand}, 窗口编号: {win_num}")

            queue = multiprocessing.Queue()  # 任务信息队列

            process = multiprocessing.Process(target=task_op,
                                              args=(win_num, queue, win_num, self.running_mode, True))
            process.start()
            processes[win_hand] = (process, queue)  # 确保将进程存储在字典中

            logger.info(f"进程 {process.pid} 已启动，窗口句柄: {win_hand}")

            # 启动一个线程来监听队列
            threading.Thread(target=self.process_queue, args=(queue, win_hand, item), daemon=True).start()

            # 更新窗口状态为“运行中”
            self.tree.item(item, values=(win_num, "运行中", win_hand, vnc_ip, vnc_port, "", "", "", ""))
        except Exception as e:
            logger.error(f"启动进程时发生错误: {e}")
            messagebox.showerror("错误", f"启动进程时发生错误: {e}")

    def process_queue(self, queue, win_hand, item):
        """处理队列中的任务完成信号"""
        while True:
            time.sleep(1)
            try:
                message = queue.get(timeout=3)  # 设置超时以防止阻塞
                logger.success(f"收到进程队列信息: {message}")
                if isinstance(message, tuple) and len(message) == 2:
                    # 假设消息是一个包含两个元素的元组
                    row, result = message
                    logger.warning(f"进程队列信息,任务 {row} 完成，结果: {result}")
                    # ('004', {'errmsg': '角色门派获取失败,请正确配置文件'})

                    # 处理进程完成后的逻辑
                    if win_hand in processes:
                        process, _ = processes[win_hand]
                        process.terminate()  # 停止进程
                        process.join()  # 等待进程终止
                        del processes[win_hand]  # 从字典中删除进程

                        if result is not None and "errmsg" in result:
                            info = result["errmsg"]
                            messagebox.showerror("错误", f"{info}")
                        else:
                            messagebox.showinfo("信息", f"窗口 {win_hand} 的任务已完成！")

                        # 更新树形控件的状态
                        current_values = self.tree.item(item, 'values')
                        self.tree.item(item, values=current_values[:1] + ("停止",) + current_values[2:])
                    break  # 退出循环

            except Empty:
                continue  # 如果队列为空，则继续循环
            except Exception as e:
                logger.error(f"处理队列时发生错误: {e}")
                break  # 退出循环，避免无限循环

    def stop_process(self):
        """停止选中的行的进程"""
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')
            win_hand = item_values[2]
            if win_hand in processes:
                process, queue = processes[win_hand]  # 获取进程和队列
                try:
                    process.terminate()  # 使用 terminate() 方法终止进程
                    process.join()  # 等待进程终止

                    # 清空队列信息
                    while not queue.empty():
                        queue.get()  # 获取并丢弃队列中的所有项
                    logger.info(f"队列已清空: {win_hand}")

                    del queue # 删除队列对象

                    del processes[win_hand]  # 从字典中删除进程
                    messagebox.showinfo("信息", "窗口已停止！")
                    self.tree.item(selected_item, values=item_values[:1] + ("停止",) + item_values[2:])
                except Exception as e:
                    messagebox.showerror("错误", f"停止窗口失败: {e}")
            else:
                messagebox.showwarning("警告", "未找到与该句柄对应的窗口！")
        else:
            messagebox.showwarning("警告", "请先选择窗口！")

    def stop_all_processes(self):
        """停止所有查找到的窗口"""
        if not processes:
            messagebox.showwarning("警告", "没有正在运行的窗口！")
            return

        for win_hand, (process, queue) in processes.items():
            try:
                process.terminate()  # 终止进程
                process.join()  # 等待进程终止
                logger.info(f"已停止进程: {win_hand}")
            except Exception as e:
                logger.error(f"停止进程 {win_hand} 失败: {e}")

        processes.clear()
        for item in self.tree.get_children():
            item_values = self.tree.item(item, 'values')
            self.tree.item(item, values=item_values[:1] + ("停止",) + item_values[2:])

        messagebox.showinfo("信息", "所有窗口已停止！")

    def on_close(self):
        """处理窗口关闭事件"""
        # 停止文件监控
        if hasattr(self, 'observer'):
            self.observer.stop()
            self.observer.join()
            logger.info("文件监控已停止。")

        # 停止所有正在运行的进程
        for win_hand, (process, queue) in processes.items():
            try:
                process.terminate()  # 使用 terminate() 方法终止进程
                process.join()  # 等待进程终止
                logger.info(f"已停止进程: {win_hand}")
            except Exception as e:
                logger.error(f"停止进程 {win_hand} 失败: {e}")

        self.root.destroy()  # 销毁主窗口

    def find_windows(self):
        """查找窗口"""
        targets = [] # 创建一个空列表
        successful_connections = []  # 存储成功连接的结果
        for i in range(1, 201):
            section_name = f"{i:03}"
            try:
                data = INIFileHandler().get_section_items(section_name)
                ip = data["vnc_ip"]
                port = int(data["vnc_port"])
                win_num = data["vnc_window"]
                targets.append((ip, port, win_num, int(win_num)))
            except Exception as e:
                pass

        for ip, port, vnc_num,win_num in targets:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)  # 可选：设置连接超时时间为 2 秒
            result = sock.connect_ex((ip, 49152))
            if result == 0:
                successful_connections.append((f"{ip}:{port}", vnc_num, win_num))
            else:
                pass
                # print(f"连接失败: {ip}:{port}")
            sock.close()
        successful_connections.sort(key=lambda x: int(x[1]))
        return successful_connections

def run():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

# if __name__ == "__main__":
#     run()