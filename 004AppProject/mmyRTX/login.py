# coding=utf-8
# @File     : login.py
# @Time     : 2021/2/22 15:20
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import json
import pprint
import requests


HOST = 'http://app.runtianxia.cn'

def login(in_data, get_token=True):
    url = f'{HOST}/api/login/loginByPwd'
    payload = in_data
    req = requests.post(url=url, data=payload)
    # pprint.pprint(json.loads(req.text)['data']['obj']['token'])
    if get_token:
        return json.loads(req.text)['data']['obj']['token']
    else:
        print(json.loads(req.text))


if __name__ == '__main__':
    login({'username': '18829843843', 'password': '888888', 'deviceID': '0', 'm': '1', 'identityType': '1'}, get_token=False)



