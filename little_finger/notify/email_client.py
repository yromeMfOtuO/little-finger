"""
通过邮件发送通知
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header


class EmailClient:
    """
    发送邮件
    """

    def __init__(self, config):
        """
        初始化配置， 示例配置如下：
        {
            "sender": "**@**.**",
            "sender_name": "**",
            "receivers": [
              "**@**.**"
            ],
            "recievers_name": "**",
            "smtpHost": "smtp.qq.com",
            "smtpPort": 465,
            "authCode": "**" // 邮箱开启
          }
        :param config: 配置 dict
        """
        if config is None:
            raise Exception('获取邮箱配置失败')
        self.__sender = config['sender']
        self.__sender_name = config['sender_name']
        self.__receivers = config['receivers']
        self.__recievers_name = config['recievers_name']
        self.__host = config['smtpHost']
        self.__port = config['smtpPort']
        self.__auth_code = config['authCode']
        self.__s = None
        self.__initial()

    def __initial(self):
        try:
            # 通过SSL方式发送，服务器地址和端口
            self.__s = smtplib.SMTP_SSL(self.__host, self.__port)
            # 登录邮箱
            self.__s.login(self.__sender, self.__auth_code)
            print('client initial success')
        except smtplib.SMTPException as e:
            print("client initial error")
            raise Exception("client initial error") from e

    def send(self, subject, content, receivers=None, recievers_name=None):
        """
        发送邮件通知
        :param subject: 主题
        :param content: 内容
        :param receivers: 收件人优先
        :param recievers_name: 收件人名
        :return: none
        """
        receiver_name = recievers_name if recievers_name else self.__recievers_name
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = Header(self.__sender_name, 'utf-8')  # 发送者
        message['To'] = Header(receiver_name, 'utf-8')  # 接收者
        message['Subject'] = Header(subject, 'utf-8')

        receiver = receivers if receivers else self.__receivers
        try:
            self.__s.sendmail(self.__sender, receiver, message.as_string())
            print('send email success')
        except smtplib.SMTPException as e:
            print("send email error")
            raise Exception("send email error") from e
