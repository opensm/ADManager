from libs.ad import *
from libs.settings import *

if __name__ == '__main__':
    ad93 = Adoper(domain=domain, ip=server_address, pwd=manager_pass, user=manager_user)
    for user in ad93.search('信息科技部.总行.cibuser'):
        print(user)
    # ad93.add_org('python02.cibuser')
    # ad93.add_user('python02.cibuser', 'python03类用户', 'python03')
