# -*- coding: utf-8 -*-
# !/usr/bin/env python

from ldap3 import Server, Connection, ALL, NTLM

import os

"""
@Author: wjx
@Description: AD域
@Date: 2018-12-23 21:23:57
@LastEditTime: 2019-03-28 23:46:56
"""


class Adopter:
    """
    操作AD域的类
    """

    def __init__(self, domain, ip, user='administrator', pwd=None):
        """
        domain: 域名，格式为：xxx.xxx.xxx
        ip： ip地址，格式为：192.168.214.1
        user： 管理员账号
        pwd： 管理员密码
        """
        self.domain = domain
        self.DC = ','.join(['DC=' + dc for dc in domain.split('.')])  # csc.com -> DC=csc,DC=com
        self.pre = domain.split('.')[0].upper()  # 用户登陆的前缀
        self.ip = ip
        self.admin = user
        self.pwd = pwd
        self.server = Server(self.ip, get_info=ALL)
        self.conn = Connection(
            self.server,
            user=self.pre + '\\' + self.admin,
            password=self.pwd,
            auto_bind=True,
            authentication=NTLM
        )

    def search(self, org):
        """
        查询组织下的用户
        org: 组织，格式为：aaa.bbb 即bbb组织下的aaa组织，不包含域地址
        """
        att_list = ['displayName', 'userPrincipalName', 'userAccountControl', 'sAMAccountName', 'pwdLastSet']
        org_base = ','.join(['OU=' + ou for ou in org.split('.')]) + ',' + self.DC
        print(org_base)
        res = self.conn.search(
            search_base=org_base,
            search_filter='(objectclass=user)',  # 查询数据的类型
            attributes=att_list,  # 查询数据的哪些属性
            paged_size=1000
        )  # 一次查询多少数据
        if res:
            for user_name in self.conn.entries:
                yield user_name['displayName']
        else:
            print('查询失败:{} '.format(self.conn.result['description']))
            raise Exception("查询异常")

    def add_org(self, org):
        """
        增加组织
        org: 组织，格式为：aaa.bbb 即bbb组织下的aaa组织，不包含域地址
        """
        org_base = ','.join(['OU=' + ou for ou in org.split('.')]) + ',' + self.DC
        res = self.conn.add(org_base, object_class='OrganizationalUnit')  # 成功返回True，失败返回False
        if res:
            print('增加组织[ {} ]成功！'.format(org))
        else:
            print('增加组织[ {} ]发生错误" '.format(self.conn.result['description']))

    def add_user(
            self,
            org,
            displayName,
            sAMAccountName,
            cn,
            mail,
            title,
            department,
            sAMAccountType,
            sn,
            userAccountControl,
    ):
        """
        增加用户
        params: org增加到该组织下
        params: name：显示名称
        params: uid：账号
        params: departmentName
        params: sAMAccountType
        """
        org_base = ','.join(['OU=' + ou for ou in org.split('.')]) + ',' + self.DC
        user_att = {
            'mail': mail,
            'cn': cn,
            'displayName': displayName,
            'userPrincipalName': sAMAccountName + '@' + self.domain,  # uid@admin组成登录名
            'userAccountControl': userAccountControl,  # 启用账号
            'sAMAccountName': sAMAccountName,
            'department': department,
            'pwdLastSet': 1,  # 取消下次登录需要修改密码
            'sAMAccountType': sAMAccountType,
            'sn': sn,
            'title': title
        }
        print(user_att)
        res = self.conn.add(
            'CN={},{}'.format(sAMAccountName, org_base),
            object_class='user',
            attributes=user_att
        )
        if res:
            print('增加用户[ {} ]成功！'.format(displayName))
        else:
            print('增加用户[ {} ]发生错误：'.format(self.conn.result['description']))

    def add_users(self, config_files):
        """
        params: config_files
        """
        if not os.path.exists(config_files):
            raise FileNotFoundError(
                "文件不存在：{}".format(config_files)
            )
        with open(config_files, 'r', encoding='utf-8') as fff:
            data = fff.readlines()
        for xx in data:
            split_data = xx.split('|')
            self.add_user(
                cn=split_data[0],
                displayName=split_data[1],
                mail=split_data[2],
                title=split_data[3],
                department=split_data[4],
                org=split_data[5],
                sAMAccountName=split_data[6],
                sAMAccountType=split_data[7],
                sn=split_data[9],
                userAccountControl=split_data[10],
            )


__all__ = ['Adopter']
