# --*--coding:utf-8--*--
import os
import sys
if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.curdir))

import json
import time
import redis
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import settings


class REDIS_QUEUE(object):
    def __init__(self):
        pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        self.conn = redis.Redis(connection_pool=pool)

    def send_email_via_queue(self, sender, to_email, subject, content):
        data = {
            'sender': sender,
            'to_email': to_email,
            'subject': subject,
            'content': content
        }
        self.conn.rpush(settings.REDIS_QUEUE_NAME, json.dumps(data))

    def process_email_queue(self):
        while 1:
            packed = self.conn.brpop(settings.REDIS_QUEUE_NAME, 0)
            if not packed:
                continue
            to_send = json.loads(packed[1])
            self.send_email(to_send)

    def send_email(self, to_send):
        sender = to_send.get('sender')
        receivers = [to_send.get('to_email')]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        mail_msg = to_send.get('content')
        message = MIMEText(mail_msg, 'html', 'utf-8')
        message['Subject'] = Header(to_send.get('subject'), 'utf-8')
        message['From'] = Header(sender, 'utf-8')
        message['To'] = Header(to_send.get('to_email'), 'utf-8')

        try:
            smtpObj = smtplib.SMTP_SSL()
            smtpObj.connect(settings.SMTP_ADD, settings.SMTP_PORT)  # 25 为 SMTP 端口号
            smtpObj.login(settings.SMTP_USER, settings.SMTP_PASS)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print "邮件发送成功"
        except smtplib.SMTPException:
            print "Error: 无法发送邮件"

if __name__ == '__main__':
    obj = REDIS_QUEUE()
    # obj.send_email_via_queue('push@kindle15.com', '1572402228@qq.com', 'test', 'content')
    obj.process_email_queue()
