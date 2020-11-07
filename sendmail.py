import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender='860760123@163.com'
receiver=['newhackerman@qq.com']

mail_host="smtp.163.com"  #设置服务器
mail_user="newhackerman@163.com"    #用户名
mail_pass="xxxxxx"   #口令
mail_msg = """<p>Python 邮件发送测试...</p>
<p><a href="http://www.runoob.com">这是一个链接</a></p>"""
try:
    server=smtplib.SMTP_SSL("smtp.qq.com", 465)
    message=MIMEText(mail_msg,'html','utf-8')
    server.login(mail_user, mail_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
    server.sendmail(sender,[mail_user,],message.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    print ("邮件发送成功")
except smtplib.SMTPException:
    print ("Error: 无法发送邮件")