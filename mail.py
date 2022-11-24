from libs.ad import Adopter
from libs.settings import *
# from libs.wechat import getAccessToken, postMessage
from libs.mail import send_email


def main():
    try:
        adladp = Adopter(domain=domain, ip=server_address, user=manager_user, pwd=manager_pass)
        # 创建一个Adoper对象，并连接AD域服务器
        user_dict = adladp.search(search_base)  # 提供查询条件
        if user_dict:  # 如果user_dict不为空
            for user in user_dict.keys():  # 遍历字典中的key
                try:
                    print(user)
                    # send_email(user_email=user,username="ddd")  # 发送消息
                except Exception as err:
                    raise err
        else:
            print('No user')

    except Exception as err:
        raise err


if __name__ == '__main__':
    main()
