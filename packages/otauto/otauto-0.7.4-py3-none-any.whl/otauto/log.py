import os
import re
import sys
from datetime import datetime
from loguru import logger
import logging
import inspect
"""
#更新日志:2024-7-9 12:12:38
# loguru是一个Python的第三方日志库，它提供了简单易用的API来记录日志。
# logger.add("my_log_file.log")  # 将日志输出到文件
# logger.info("这是一条信息日志")
# logger.warning("这是一条警告日志")
# logger.error("这是一条错误日志")
# logger.critical("这是一条严重错误日志")
# logger.debug("这是一条调试日志")
# logger.success("操作成功")
"""

class Log_Info:
    def __init__(self, local_ip=None,local_port=None,local_window=None,debug=False):
        # 日志前置信息
        self.local_ip=local_ip
        self.local_port=local_port
        self.local_window=local_window
        self.debug=debug
        if not local_ip:
            self.local_ip="127.0.0.1" #本机ip
        if not local_port:
            self.local_port="5901" #本机端口
        if not local_window:
            self.local_window="001" #本机窗口

    def log_init(self):
        # 指定日志文件的路径, 默认放在桌面
        log_folder = r"C:/Users/Administrator/Desktop/log"

        # 获取当前日期并格式化为 YYYY-MM-DD
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(log_folder, f"{self.local_window}_{current_date}.log")

        # 确保日志文件夹存在
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        if not self.debug:
            # 移除所有默认的日志处理器
            logger.remove()

        # 添加一个日志处理器，指定编码为 UTF-8
        logger.add(log_file, level="DEBUG", format="{time} {level} {module}:{line} - {message}",
                   rotation="1 day", retention="10 days", enqueue=True, encoding="utf-8")

        # 在日志记录开始时写入指定内容
        self.safe_log("========== facility information ==========")
        self.safe_log(f"Local IP: {self.local_ip}")
        self.safe_log(f"Local Port: {self.local_port}")
        self.safe_log(f"Local Window: {self.local_window}")
        self.safe_log("========== Log session started ==========")

    def safe_log(self, message):
        """安全地记录日志，处理编码问题"""
        try:
            # 直接记录消息
            logger.debug(message)
        except UnicodeEncodeError:
            # 如果遇到编码错误，进行处理
            safe_message = message.encode('gbk', 'replace').decode('gbk')
            logger.debug(safe_message)


class ColoredFormatter(logging.Formatter):
    """自定义格式化器，添加颜色支持（示例）"""
    # 这里可以添加颜色代码
    COLORS = {
        'DEBUG': '\033[0;37m',  # 白色
        'INFO': '\033[0;32m',  # 绿色
        'WARNING': '\033[0;33m',  # 黄色
        'ERROR': '\033[0;31m',  # 红色
        'CRITICAL': '\033[1;31m'  # 亮红色
    }
    RESET = '\033[0m'  # 重置颜色

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        message = super().format(record)
        return f"{log_color}{message}{self.RESET}"

class ColoredLogger:
    """带有颜色输出的自定义日志记录器"""

    def __init__(self, name='ColoredLogger', level=logging.DEBUG):
        """初始化 ColoredLogger
        :param name: 日志记录器名称
        :param level: 日志级别
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # 创建自定义格式化器，包含行号
        formatter = ColoredFormatter('%(lineno)d - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # 将处理器添加到记录器
        self.logger.addHandler(console_handler)

    def validate_message(self, message):
        """验证消息是否有效"""
        # 检查 message 是否为 None、空字符串或仅包含空格
        if message is None or not isinstance(message, str) or not message.strip():
            return False
        # 只允许中文、字母、数字、常用符号和 () [] {}
        # 在此示例中，允许的常用符号包括：空格、句号、逗号、问号、感叹号、分号、冒号等
        if not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9(){}\[\] ,.!?;:]*$', message):
            return False
        return True

    def debug(self, message):
        """记录调试信息"""
        if self.validate_message(message):
            self.logger.debug(message, stacklevel=2)

    def info(self, message):
        """记录普通信息"""
        if self.validate_message(message):
            self.logger.info(message, stacklevel=2)

    def warning(self, message):
        """记录警告信息"""
        if self.validate_message(message):
            self.logger.warning(message, stacklevel=2)

    def success(self, message):
        """记录警告信息"""
        if self.validate_message(message):
            self.logger.warning(message, stacklevel=2)


    def error(self, message):
        """记录错误信息"""
        if self.validate_message(message):
            self.logger.error(message, stacklevel=2)

    def critical(self, message):
        """记录严重错误信息"""
        if self.validate_message(message):
            self.logger.critical(message, stacklevel=2)

    def remove(self):
        """关闭日志记录器"""
        # 设定日志记录器的级别为 CRITICAL，从而忽略所有其他级别的日志
        self.logger.setLevel(logging.CRITICAL)
        # 或者你可以移除所有处理器
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)



# # 示例用法
# if __name__ == "__main__":
#     colored_logger = ColoredLogger()
#     # 记录不同级别的日志消息
#     colored_logger.debug("这是一个调试信息")
#     colored_logger.info("这是一个信息")
#     colored_logger.warning("这是一个警告信息")
#     colored_logger.error("这是一个错误信息")
#     colored_logger.critical("这是一个严重错误信息")