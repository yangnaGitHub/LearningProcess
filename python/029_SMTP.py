#简单邮件传输协议,一组用于由源地址到目的地址传送邮件的规则,控制信件的中转方式
#smtplib提供了一种很方便的途径发送电子邮件,smtp协议进行了简单的封装
#import smtplib
#smtpObj = smtplib.SMTP( [host [, port [, local_hostname]]] )
#SMTP.sendmail(from_addr, to_addrs, msg[, mail_options, rcpt_options]
#注意msg的格式(smtp协议中定义的格式)
import smtplib
from email.mime.text import MIMEText
from email.header import Header
#############################
#sender = 'natasha1_yang@asus.com'
#receivers = ['ityangna0402@163.com']#接收邮件

#三个参数:第一个为文本内容,第二个plain设置文本格式,第三个utf-8设置编码
#message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
#message['From'] = Header("菜鸟教程", 'utf-8')
#message['To'] =  Header("测试", 'utf-8')
#message['Subject'] = Header("Python SMTP 邮件测试", 'utf-8')

#try:
#    smtpObj = smtplib.SMTP('localhost')
#    smtpObj.sendmail(sender, receivers, message.as_string())
#    print ("邮件发送成功")
#except smtplib.SMTPException:
#    print ("Error: 无法发送邮件")
#############################
#第三方SMTP服务
mail_host="smtp.163.com"#设置服务器
mail_user="ityangna0402@163.com"
mail_pass="happyyn8754"


sender = 'ityangna0402@163.com'
receivers = ['natasha1_yang@asus.com']

message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("菜鸟教程", 'utf-8')
message['To'] =  Header("测试", 'utf-8')

subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP() 
    smtpObj.connect(mail_host, 465)
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print ("邮件发送成功")
except smtplib.SMTPException:
    print ("Error: 无法发送邮件")
    
#Python发送HTML格式的邮件与发送纯文本消息的邮件不同之处就是将MIMEText中_subtype设置为html
#message = MIMEText(mail_msg, 'html', 'utf-8')

#发送带附件的邮件,首先要创建MIMEMultipart()实例,然后构造附件,如果有多个附件可依次构造
#message = MIMEMultipart()创建一个带附件的实例
#message.attach(MIMEText('这是菜鸟教程Python 邮件发送测试……', 'plain', 'utf-8'))邮件正文内容
#att1 = MIMEText(open('test.txt', 'rb').read(), 'base64', 'utf-8')构造附件1
#att1["Content-Type"] = 'application/octet-stream'
#att1["Content-Disposition"] = 'attachment; filename="test.txt"'
#message.attach(att1)
#att2 = MIMEText(open('runoob.txt', 'rb').read(), 'base64', 'utf-8')构造附件2
#att2["Content-Type"] = 'application/octet-stream'
#att2["Content-Disposition"] = 'attachment; filename="runoob.txt"'
#message.attach(att2)

#添加图片
