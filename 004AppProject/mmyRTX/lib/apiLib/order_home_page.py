# coding=utf-8
# @File     : order_home_page.py
# @Time     : 2021/2/24 11:56
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import pprint
import requests
from configs.config import HOST
from lib.apiLib.psw_login import PswLogin



# 订单——模块类
class OrderHomePage(object):


    def __init__(self, in_token):
        self.header = {'token': in_token}

    # 首页
    def home_page(self, in_data):
        url = f'{HOST}/api/index/deliveryIndex'
        payload = in_data
        res = requests.post(url=url, headers=self.header, data=payload, verify=False)
        order_list = res.json()["data"]["list"]
        today_num = res.json()["data"]["obj"]["todayNum"]
        if today_num == 0:
            return '首页列表无订单，请添加~'
        elif today_num >= 1:
            for order_id in order_list:
                # 接单按钮状态：0显示，1不显示
                if order_id['orderList'][0]['acceptOrderButtonState'] == '0':
                    return [order_id['orderList'][0]['orderId'], res.json()['code']]
                # 完成配送按钮状态：0显示，1不显示
                elif order_id['orderList'][0]['acceptOrderButtonState'] == '1' and order_id['orderList'][0]['completeDistributionButtonState'] == '0':
                    return [order_id['orderList'][0]['orderId'], res.json()['code']]
                else:
                    return '订单不存在~'


if __name__ == '__main__':
    token = PswLogin().login({'username': '18829843843', 'password': '888888', 'deviceID': '0', 'm': '1', 'identityType': '0'})
    print(token)
    order = OrderHomePage(token)
    order.home_page({"indexState": '0', "sort": '0', "pageIndex": '1', "pageSize": '10'})
    # ['HCFBGUGBC9AQH36XOJF', '1000']







