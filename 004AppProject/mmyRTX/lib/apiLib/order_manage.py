# coding=utf-8
# @File     : order_manage.py
# @Time     : 2021/2/24 15:06
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import sys
sys.path.append('D:\Pycharm\mmyRTX\configs')
import requests
from configs.config import HOST
from lib.apiLib.psw_login import PswLogin
from lib.apiLib.order_home_page import OrderHomePage


# 订单管理——模块类
class OrderManage(object):


    def __init__(self, in_token):
        self.header = {'token': in_token}

    # 订单列表
    def order_list(self, in_data):
        url = f'{HOST}/api/order/orderList'
        payload = in_data
        res = requests.post(url=url, headers=self.header, data=payload)
        if len(res.json()["data"]["list"]) == 0:
            return '空空如也，还没有订单~'
        elif len(res.json()["data"]["list"]) > 0:
            return res.json()

    # 接单（确认配送）
    def confirm_delivery(self, in_data, confirm_order_id, order_state):
        url = f'{HOST}/api/order/dispatchingOrder'
        in_data['id'] = confirm_order_id
        payload = in_data
        if len(order_state) != 0:
            # print(order_state)
            res = requests.post(url=url, headers=self.header, data=payload)
            # if res.json()['data']['msg'] == '接单成功~':
            #     return res.json()
            # elif res.json()['data']['msg'] == '订单已接单，请勿重复操作~~':
            #     return res.json()['data']['msg']
            return res.json()

    # 完成配送
    def complete_delivery(self, in_data, complete_order_id, order_num):
        url = f'{HOST}/api/order/confirmOrder'
        # 将实时的变量定义为参数传入
        in_data["orderId"] = complete_order_id
        payload = in_data
        if order_num > 0:
            res = requests.post(url=url, headers=self.header, json=payload)
            if res.json()["data"]["msg"] == '提交成功，订单完成配送~':
                return res.json()
            elif res.json()["data"]["msg"] == '订单已完成配送':
                return res.json()
        elif order_num == 0:
            return '空空如也，还没有在途中订单~'

    # 订单详情
    def order_detail(self, in_data):
        url = f'{HOST}/api/order/orderDetail'
        payload = in_data
        res = requests.post(url=url, headers=self.header, data=payload)
        return res.json()

    # 回单订单
    def receipt_order(self, in_data, brand_id, bucket_id, bucket_main_id, order_list_id):
        url = f'{HOST}/api/order/receiptOrder'
        # 判断字典中的key是否存在
        if "backBucketList" in in_data.keys():
            in_data['backBucketList'][0]['brandId'] = brand_id
            in_data['backBucketList'][0]['bucketId'] = bucket_id
            in_data['backBucketList'][0]['bucketMainId'] = bucket_main_id

        elif "backBucketList" and "backMortgageBucketList" in in_data.keys() :
            in_data['backBucketList'][0]['brandId'] = brand_id
            in_data['backBucketList'][0]['bucketId'] = bucket_id
            in_data['backBucketList'][0]['bucketMainId'] = bucket_main_id
            in_data['backMortgageBucketList'][0]['brandId'] = brand_id
            in_data['backMortgageBucketList'][0]['bucketId'] = bucket_id
            in_data['backMortgageBucketList'][0]['bucketMainId'] = bucket_main_id

        elif "backBucketList" and "backMortgageBucketList" and "mortgageBucketList" in in_data.keys():
            in_data['backBucketList'][0]['brandId'] = brand_id
            in_data['backBucketList'][0]['bucketId'] = bucket_id
            in_data['backBucketList'][0]['bucketMainId'] = bucket_main_id
            in_data['backMortgageBucketList'][0]['brandId'] = brand_id
            in_data['backMortgageBucketList'][0]['bucketId'] = bucket_id
            in_data['backMortgageBucketList'][0]['bucketMainId'] = bucket_main_id
            in_data['mortgageBucketList'][0]['brandId'] = brand_id
            in_data['mortgageBucketList'][0]['bucketId'] = bucket_id
            in_data['mortgageBucketList'][0]['bucketMainId'] = bucket_main_id

        in_data['orderId'] = order_list_id
        payload = in_data
        res = requests.post(url=url, headers=self.header, json=payload)
        return res.json()

    # 订单回单金额
    def order_return_amount(self, in_data):
        url = f'{HOST}/api/order/orderReturnAmount'
        payload = in_data
        res = requests.post(url=url, headers=self.header, data=payload)
        return res.json()

    # 线下支付
    def offline_pay(self, in_data, pay_order_id, payment_amount):
        url = f'{HOST}/api/order/offlinePay'
        in_data['id'] = pay_order_id
        in_data['offlinePaymentAmount'] = payment_amount
        payload = in_data
        res = requests.post(url=url, headers=self.header, data=payload)
        return res.json()



if __name__ == '__main__':
    # 获取token
    token = PswLogin().login({'username': '18829843843', 'password': '888888', 'deviceID': '0', 'm': '1', 'identityType': '0'})
    manage = OrderManage(token)
    # 获取订单编号
    order_id = OrderHomePage(token).home_page({'indexState': '0', 'sort': '0', 'pageIndex': '1', 'pageSize': '10'})[0]
    # print(order_id)
    # manage.order_list({'orderState': '4', 'pageSize': '10', 'pageIndex': '1'})
    # manage.complete_delivery({"isDeliveryForm": "0", "orderId": order_id}, order_id)
