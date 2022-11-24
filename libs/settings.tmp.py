# -*- coding: utf-8 -*-
# 基础配置
server_address = ""
manager_user = ""
manager_pass = ""
domain = ""
search_base = ""

# 邮箱配置
mail_charset = "utf8"
mail_from = ""
mail_from_name = ""
mail_signature = ""
# -----
smtp_auth_on = "true"
smtp_autotls = "true"
smtp_host = ""
smtp_pass = ""
smtp_port = 465
smtp_secure_type = "ssl"
smtp_user = ""

# 企业微信配置
wechat_agentid = "xxxxxxx"  # 应用id （此类型为int型）
wechat_corpid = ""  # 企业id
wechat_corpsecret = ""  # 创建的应用的secret

__all__ = [
    server_address,
    manager_user,
    manager_pass,
    domain,
    mail_charset,
    mail_from,
    mail_from_name,
    mail_signature,
    smtp_auth_on,
    smtp_autotls,
    smtp_host,
    smtp_pass,
    smtp_port,
    smtp_secure_type,
    smtp_user,
    wechat_agentid,
    wechat_corpid,
    wechat_corpsecret,
]
