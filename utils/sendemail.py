# 发送邮件（提醒是否购票成功）
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr  # 格式化邮件地址的显示形式
from datetime import datetime
import time
from config.settings import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER


sender = EMAIL_SENDER  
pwd = EMAIL_PASSWORD
receiver = EMAIL_RECEIVER

def mail(title, message):
    ret = True
    try:
        current_dt = time.strftime('%Y-%m-%d', time.localtime())
        msg = MIMEText(message, 'plain', 'utf-8')
        # 最终邮件头效果: From: ^_^ <user@qq.com>
        msg['From'] = formataddr(["^v^", sender])  # 发件人昵称
        msg['To'] = formataddr(["^v^", receiver])  # 收件人昵称
        msg['Subject'] = title

        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(sender, pwd)
        server.sendmail(sender, [receiver,], msg.as_string())
        server.quit()
    except Exception as e:
        ret = False
        print(e)
    return ret

if __name__ == '__main__':
    ret = mail('Test', 'Test')
    if ret:
        print("邮件发送成功!")
    else:
        print("邮件发送失败!")
