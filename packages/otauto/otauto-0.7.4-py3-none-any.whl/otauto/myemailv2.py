from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
from PIL import Image
from  loguru import logger
import numpy as np
from io import BytesIO

from otauto.ini_file_operationv2 import INIFileHandler # 导入ini文件操作类

"""
功能:邮箱信息发送
日期:2025-2-14 10:56:14
描述:
    qq邮箱和139邮箱发送
"""

class EmailHandler:
    def __init__(self):
        # 从ini文件中读取邮箱信息
        try:
            self.ini_handler = INIFileHandler()  # ini操作对象
            self.ini_data_dict = self.ini_handler.get_section_items("email")  # 获取ini数据
            self.email_qq_sender = self.ini_data_dict.get("email_qq_sender", "")
            self.email_qq_password = self.ini_data_dict.get("email_qq_password", "")
            self.email_qq_receiver = [email.strip() for email in
                                      self.ini_data_dict.get("email_qq_receiver", "").split(",") if email.strip()]
            self.email_139_sender = self.ini_data_dict.get("email_139_sender", "")
            self.email_139_password = self.ini_data_dict.get("email_139_password", "")
            self.email_139_receiver = [email.strip() for email in
                                       self.ini_data_dict.get("email_139_receiver", "").split(",") if email.strip()]
        except Exception as e:
            logger.error(f"读取邮箱信息时发生错误: {e}")
            # 可以选择设置一些默认值或采取其他措施
            self.email_qq_sender = ""
            self.email_qq_password = ""
            self.email_qq_receiver = []
            self.email_139_sender = ""
            self.email_139_password = ""
            self.email_139_receiver = []

    def compress_image(self, input_path: str, output_path: str, quality: int = 80):
        """
        压缩图片并保存

        :param input_path: 输入图片路径
        :param output_path: 输出图片路径
        :param quality: 压缩质量，范围从 1 到 100，默认值为 80
        """
        with Image.open(input_path) as img:
            img.save(output_path, "JPEG", quality=quality)
            logger.info(f"压缩后的图片保存到: {output_path}")

    def send_email(self, sender_email: str, password: str, receiver: list, subject: str, body: str,
                   image_data: np.ndarray,
                   smtp_server: str):
        """
        发送电子邮件

        :param sender_email: 发件人邮箱
        :param password: 发件人授权码
        :param receiver: 收件人邮箱列表
        :param subject: 邮件标题
        :param body: 邮件正文内容
        :param image_data: 图像数据（NumPy数组）
        :param smtp_server: SMTP服务器地址
        """
        # 初始化一个邮件主体
        msg = MIMEMultipart()
        # 检查图像数据是否有效
        if image_data is not None and isinstance(image_data, np.ndarray):
            # 将 NumPy 数组转换为 PIL 图像
            pil_image = Image.fromarray(image_data)
            # 创建一个字节流对象
            image_bytes = BytesIO()
            # 将图像保存到字节流中
            pil_image.save(image_bytes, format='JPEG')
            image_bytes.seek(0)  # 将指针移动到字节流的开头
            # 添加图片附件
            pngpart = MIMEApplication(image_bytes.getvalue())
            pngpart.add_header('Content-Disposition', 'attachment', filename='image.jpg')
            msg.attach(pngpart)
        else:
            logger.warning("图像数据无效或为空")

        msg["Subject"] = Header(subject, 'utf-8')
        msg["From"] = sender_email
        msg['To'] = ";".join(receiver)

        # 邮件正文内容
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        try:
            # 发送邮件
            with SMTP_SSL(smtp_server) as smtp:
                smtp.login(sender_email, password)
                smtp.sendmail(sender_email, receiver, msg.as_string())
            logger.info("邮件发送成功")
        except Exception as e:
            logger.error(f"邮件发送失败: {e}")

    def send_email_qq(self, tests: str, image_data=None):
        """
        发送QQ邮箱邮件

        :param tests: 邮件正文内容
        :param image_data: numpy数组格式的图片数据
        """
        smtp_server = 'smtp.qq.com'
        subject = '游戏信息提示'
        receiver = self.email_qq_receiver
        self.send_email(self.email_qq_sender, self.email_qq_password, receiver, subject, tests, image_data, smtp_server)

    def send_email_139(self, tests: str, image_data=None):
        """
        发送139邮箱邮件

        :param tests: 邮件正文内容
        :param image_data: numpy数组格式的图片数据
        """
        smtp_server = 'smtp.139.com'
        subject = '游戏信息提示'
        receiver = self.email_139_receiver
        self.send_email(self.email_139_sender, self.email_139_password, receiver, subject, tests, image_data,
                        smtp_server)


# 使用示例
# if __name__ == "__main__":
#     email_sender = Email()
#     email_sender.send_email_qq("这是测试邮件", "path/to/your/image.jpg")  # 替换为实际路径
#     email_sender.send_email_139("这是测试邮件", "path/to/your/image.jpg")  # 替换为实际路径
