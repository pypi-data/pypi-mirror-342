from email.mime.application import MIMEApplication
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


# smtplib模块主要负责发送邮件：是一个发送邮件的动作，连接邮箱服务器，登录邮箱，发送邮件（有发件人，收信人，邮件内容）。
# email模块主要负责构造邮件：指的是邮箱页面显示的一些构造，如发件人，收件人，主题，正文，附件等。

class Email:
    def __init__(self, tests,image_url):
        self.tests = tests
        self.image_url = image_url
    def emailqq(tests,image_url):
        """
        报错信息
        :param image_url:图片路径
        :param tests: "文字"
        :return:
        """
        host_server = 'smtp.qq.com'  #qq邮箱smtp服务器
        sender_qq = '283044916@qq.com' #发件人邮箱
        pwd = 'etwntcveffkxbghc'#你的授权码
        receiver = ['283044916@qq.com' ]#收件人邮箱['283044916@qq.com','824864@qq.com' ]
        #receiver = '913@qq.com'
        mail_title = '游戏提示' #邮件标题
        mail_content = tests #邮件正文内容

        # 初始化一个邮件主体
        msg = MIMEMultipart()

        # png类型的附件
        pngpart = MIMEApplication(open(image_url, 'rb').read())
        pngpart.add_header('Content-Disposition', 'attachment', filename=image_url)
        msg.attach(pngpart)

        msg["Subject"] = Header(mail_title,'utf-8')
        msg["From"] = sender_qq
        # msg["To"] = Header("测试邮箱",'utf-8')
        msg['To'] = ";".join(receiver)
        # 邮件正文内容
        msg.attach(MIMEText(mail_content,'plain','utf-8'))
        smtp = SMTP_SSL(host_server) # ssl登录
        smtp.login(sender_qq,pwd)
        smtp.sendmail(sender_qq,receiver,msg.as_string())
        # quit():用于结束SMTP会话。
        smtp.quit()


    def email_139(tests,image_url):
        """
        接受优质信息

        :param tests: "文字"
        :param image_url:图片路径
        :return:
        """
        host_server = 'smtp.139.com'  #139邮箱smtp服务器
        sender_qq = 'ordtie@139.com' #发件人邮箱
        pwd = 'ed6317972d6d8d603100'#你的授权码
        receiver = ['ordtie@139.com' ]#收件人邮箱['283044916@qq.com','824864@qq.com' ]
        mail_title = '倩女幽魂提示信息' #邮件标题
        mail_content = tests #邮件正文内容
        # 初始化一个邮件主体
        msg = MIMEMultipart()

        # png类型的附件
        pngpart = MIMEApplication(open(image_url, 'rb').read())
        pngpart.add_header('Content-Disposition', 'attachment', filename=image_url)
        msg.attach(pngpart)

        msg["Subject"] = Header(mail_title,'utf-8')
        msg["From"] = sender_qq
        # msg["To"] = Header("测试邮箱",'utf-8')
        msg['To'] = ";".join(receiver)
        # 邮件正文内容
        msg.attach(MIMEText(mail_content,'plain','utf-8'))
        smtp = SMTP_SSL(host_server) # ssl登录
        smtp.login(sender_qq,pwd)
        smtp.sendmail(sender_qq,receiver,msg.as_string())
        # quit():用于结束SMTP会话。
        smtp.quit()

