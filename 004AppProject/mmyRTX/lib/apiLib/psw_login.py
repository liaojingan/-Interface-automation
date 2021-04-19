# coding=utf-8
# @File     : psw_login.py
# @Time     : 2021/2/22 17:13
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import json
import requests
from configs.config import HOST
requests.packages.urllib3.disable_warnings()


# 密码登录——模块类
class PswLogin(object):


    def login(self, in_data, get_token=True):
        url = f'{HOST}/api/login/loginByPwd'
        payload = in_data
        res = requests.post(url=url, data=payload, verify=False)
        if get_token:
            return json.loads(res.text)['data']['obj']['token']  # str
            # print(json.loads(res.text)['data']['obj']['token'])
        else:
            return json.loads(res.text)  # dict
            # print(json.loads(res.text))



if __name__ == '__main__':
    psw_login = PswLogin()
    psw_login.login({'username': '18829843843', 'password': '888888', 'deviceID': '0', 'm': '1', 'identityType': '0'}, get_token=False)

