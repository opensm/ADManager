import json
import requests
import datetime
from lib.settings import WECHAT_CORPID, WECHAT_CORPSECRET, WECHAT_AGENTID

headers = {"Content-Type": "text/plain"}  # 输出格式


# 获取企业微信中相应应用的Access_Token
def getAccessToken():
    """
    :return:
    """
    try:
        request = requests.get(
            url="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" +
                WECHAT_CORPID + "&corpsecret=" + WECHAT_CORPSECRET,
            headers=headers
        )  # 向企业微信api发送请求获取Access_Token凭证
        request = json.loads(request.text)  # 将获取的结果转为字典数据类型
        access_token = False
        if request['errcode'] == 0:  # 获取返回信息的报错数据,并判断返回数据是否为0
            access_token = request['access_token']  # 若报错信息为0，即请求未发生错误，获取返回信息中的Access_Token
    except Exception as err:
        raise err
    else:
        return access_token  # 返回Access_Token


# 通过邮箱获取该用户在企业微信中的ID
def getuserID(access_token, email):
    """
    :param access_token:
    :param email:
    :return:
    """
    try:
        data = {
            "email": email,  # 指定的用户邮箱
            "email_type": 2  # 查询的邮箱类型：1为企业邮箱，2为个人邮箱
        }
        request = requests.post(
            url="https://qyapi.weixin.qq.com/cgi-bin/user/get_userid_by_email?access_token=" + access_token,
            headers=headers, json=data)  # 向企业微信发送请求，通过邮箱获取用户的企业ID
        request = json.loads(request.text)
        userid = False
        if request['errcode'] == 0:
            userid = request['userid']
    except Exception as err:
        raise err
    else:
        return userid


# 使用Access_Token，通过企业中的应用向特定用户发送信息
def postMessage(access_token, agentid, email, PasswordLastSet):
    """
    :param access_token:
    :param agentid:
    :param email:
    :param PasswordLastSet:
    :return:
    """
    try:
        userid = getuserID(access_token, email)  # 通过用户邮箱获取用户在企业微信中的ID
        time = 90 - (datetime.datetime.now() - PasswordLastSet).days  # 计算还有几天过期
        if time >= 0:  # 若用户还没有过期
            data = {
                "touser": userid,  # 所要发送的用户
                "msgtype": "text",  # 发送内容的格式
                "agentid": agentid,  # 使用哪一个应用发送
                "text": {  # 发送内容
                    "content": "您的域账户密码（邮件、Jira、Git、windows开机密码）即将在" + str(time) + "天后过期， " + (
                            PasswordLastSet + datetime.timedelta(days=+90)).strftime(
                        '%Y/%m/%d %H:%M:%S') + "之后您将无法使用该账户登陆相关系统，请您尽快更改密码。\n"
                },
                "safe": 0,  # 表示发送内容是否保密（0为可对外分享，1为不可分享，切内容显示水印）
                "enable_id_trans": 0,  # 是否开启id转译
                "enable_duplicate_check": 1,  # 是否开启重复消息检查
                "duplicate_check_interval": 1  # 重复消息检查的时间间隔，默认1800s，最大不超过4h（单位为s）
            }
        else:  # 若用户已过期
            data = {
                "touser": userid,
                "msgtype": "text",
                "agentid": agentid,
                "text": {
                    "content": "您的域账户密码（邮件、Jira、Git、windows开机密码）已过期"
                               "之后您将无法使用该账户登陆相关系统，请您尽快更改密码。\n"

                },
                "safe": 0,
                "enable_id_trans": 0,
                "enable_duplicate_check": 1,
                "duplicate_check_interval": 1
            }
        request = requests.post(url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + access_token,
                                headers=headers, json=data)  # 向企业微信发送请求，将信息发送给相应的用户
    except Exception as err:
        raise err
    else:
        return request.text
