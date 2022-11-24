from libs.ad import *
from libs.settings import *
import sys
import getopt


def useage():
    print("%s -h \t#帮助文档" % sys.argv[0])
    print("%s -f [导入源文件] \t#导入用户数据" % sys.argv[0])


def main():
    if len(sys.argv) == 1:
        useage()
        sys.exit()
    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "f:h"
        )
    except getopt.GetoptError:
        print("%s -h" % sys.argv[0])
        sys.exit(1)
    command_dict = dict(options)
    # 帮助
    p = Adopter(domain=domain, ip=server_address, user=manager_user, pwd=manager_pass)
    if '-h' in command_dict.keys():
        useage()
        sys.exit()
    # 获取监控项数据
    elif '-f' in command_dict.keys():
        config_file = command_dict.get("-f")
        p.add_users(config_file)
    else:
        useage()
        sys.exit(1)


if __name__ == "__main__":
    main()
