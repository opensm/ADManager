import smtplib
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

from lib.settings import MAIL_FROM, MAIL_FROM_NAME, MAIL_CHARSET, SMTP_HOST, SMTP_PORT, SMTP_USER, \
    SMTP_PASS


def send_email(user_email: str, username: str, display_name: str, out_date: str):
    """
    :param user_email:
    :param username:
    :param display_name:
    :param out_date:
    :return:
    """
    html_message = """
    <!DOCTYPE html>
<html >
  <body style="background-image: url('https://www.kaiyihome.com/assets/pc/image/home/60_02.jpg');">

    <div style="opacity: 1;background-color: aliceblue;margin-left: 10%;margin-right: 20%;">
        <div style="margin: 5%;">
            <div style="margin: 5%;">
                <h2>{},你好：</h2>

                <p>
                    &nbsp;&nbsp;&nbsp;&nbsp;您的AD域控账户：{},密码即将到期，请尽快重置密码，重置密码请按照文档：<a href="https://doc.weixin.qq.com/doc/w3_AWcAvgbgAP443TwhpQCRc0G6pSrkY?scode=AHIATgcBAA0tZUmhuRAWcAvgbgAP4&version=4.0.19.6020&platform=win"><span style="color: red;"><b>统一认证密码重置文档</b></span></a>.</p>
                    请在{}前完成重置。过期将无法登录相关系统。

                <p class="text-right">
                    <img src="img/uploads/signature.png" alt="">
                </p>
            </div>
            <div style="margin-bottom: 5%;">
                <h3>相关系统地址</h3>

                <ul >
                    <li><a style="text-decoration:none;color: #000;" href="https://passwd.kyoffice.cn"><span style="color: rgb(25, 0, 255);"><b>重置密码系统:</b></span>  https://passwd.kyoffice.cn</a></li>
                    <li><a style="text-decoration:none;color: #000;" href="https://relay.kyoffice.cn"><span style="color: rgb(25, 0, 255);"><b>外网堡垒机:</b></span>  https://relay.kyoffice.cn</a></li>
                    <li><a style="text-decoration:none;color: #000;" href="https://yb1-relay.kyoffice.cn"><span style="color: rgb(25, 0, 255);"><b>内网堡垒机:</b></span>  https://yb1-relay.kyoffice.cn</a></li>
                    <li><a style="text-decoration:none;color: #000;" href="https://jira.kyoffice.cn"><span style="color: rgb(25, 0, 255);"><b>jira系统:</b></span>  https://jira.kyoffice.cn</a></li>
                    <li><a style="text-decoration:none;color: #000;" href="https://confluence.kyoffice.cn"><span style="color: rgb(25, 0, 255);"><b>confluence系统:</b></span>  https://confluence.kyoffice.cn</a></li>
                    <li><a style="text-decoration:none;color: #000;" href="https://git.kyoffice.cn"><span style="color: rgb(25, 0, 255);"><b>代码仓库:</b></span>  https://git.kyoffice.cn</a></li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
    """.format(display_name, username, out_date)
    msg = MIMEText(html_message, 'html', MAIL_CHARSET)
    # 邮件主题
    msg['Subject'] = Header("【AD域控密码过期提示】关于账户【{}】AD域控密码即将过期的提示！".format(username), 'utf-8')
    # 发送方信息
    msg['From'] = MAIL_FROM_NAME
    # 接受方信息
    msg['To'] = user_email

    try:
        smtp = SMTP_SSL(host=SMTP_HOST, port=SMTP_PORT)
        smtp.set_debuglevel(1)
        smtp.ehlo(SMTP_HOST)
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.sendmail(MAIL_FROM, user_email, msg.as_string())
        smtp.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error', e)
