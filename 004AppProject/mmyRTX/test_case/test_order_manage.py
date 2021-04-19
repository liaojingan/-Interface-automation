# coding=utf-8
# @File     : test_order_manage.py
# @Time     : 2021/2/24 20:54
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import os
import time
import allure
import pytest
import threading
from configs.config import USER
from test_case.test_log import TestLog
from lib.apiLib.psw_login import PswLogin
from tools.get_yaml_data import GetYamlData
from lib.apiLib.order_manage import OrderManage


# 订单管理——测试类
@allure.epic('配送app')
@allure.feature('订单管理模块')
@pytest.mark.test_order_manage
class TestOrderManage(object):


    yaml_data = GetYamlData()
    log = TestLog().logger()

    # pytest框架测试类中不可使用__init__函数
    def setup_class(self):
        self.token = PswLogin().login(USER)

    # 传入的参数需要和线程调用传入的参数一致
    def dispatching_order(self, in_data, resp_data, order_id, order_state):
        res = OrderManage(self.token).confirm_delivery(in_data, order_id, order_state)
        if res == '接单成功~':
            try:
                assert res['code'] == resp_data['code']
                assert res['data']['msg'] == resp_data['msg']
            except Exception as err:
                self.log.error('---确认配送接口用例不通过，请检查问题~---')
                raise err
        elif res == '订单已接单，请勿重复操作~~':
            return '---列表中全部订单都已确认配送~---'

    @pytest.mark.run(order=1)
    @allure.severity('normal')
    @allure.title('确认配送接口用例')
    @allure.story('确认配送')
    @pytest.mark.test_confirm_delivery
    @pytest.mark.parametrize('in_data, resp_data', yaml_data.get_yaml_data('../data/order_manage.yaml'))
    def test_confirm_delivery(self, in_data, resp_data, order_list_init):
        """
        接口描述：测试配送员接单功能
        order_list_init[2]：                                        初始化环境传入待接单订单状态列表长度
        in_data：{'id': 'order_id'}                                 用例请求参数示例
        resp_data：{'code': '1000', 'msg': '接单成功~'}              用例断言接口示例
        order_id：['9YRG13V4QJGMLT9UBGZ', 'EMJPVPRXN3HQD8YEAMG']   初始化环境传入待接单订单id列表
        """
        # print(order_list_init)
        order_threads = (threading.Thread(target=self.dispatching_order, args=(in_data, resp_data, order_id, order_list_init[2])) for order_id in order_list_init[1])
        for order in order_threads:
            time.sleep(1)
            order.setDaemon(True)  # 设置为守护线程，不会因为主线程结束而中断
            order.start()
        for order in order_threads:
            order.join()  # 子线程全部加入，主线程等所有子线程运行完毕


    def on_way(self, in_data, resp_data, order_id, order_num):
        res = OrderManage(self.token).complete_delivery(in_data, order_id, order_num)
        try:
            assert res['code'] == resp_data['code']
            # assert res['data']['msg'] == resp_data['msg']
        except Exception as err:
            self.log.error('---完成配送接口用例不通过，请检查问题---')
            raise err

    @pytest.mark.run(order=2)
    @allure.severity('normal')
    @allure.title('完成配送接口用例')
    @allure.story('完成配送')
    @pytest.mark.test_delivery_succeeded
    @pytest.mark.parametrize('in_data, resp_data', yaml_data.get_yaml_data('../data/complete_delivery.yaml'))
    def test_delivery_succeeded(self, in_data, resp_data, order_confirm_init):
        """
        接口描述：测试配送员完成配送功能
        order_list_init[0]：                                       初始化环境传入在途中订单数量
        in_data：{'isDeliveryForm': 0, 'orderId': 'order_id'}      用例请求参数示例
        resp_data：{'code': '1000', 'msg': '提交成功，订单完成配送~'}  用例断言接口示例
        order_id：['9YRG13V4QJGMLT9UBGZ', 'EMJPVPRXN3HQD8YEAMG']  初始化环境传入待完成配送订单id列表
        """
        # print(order_confirm_init)
        order_threads = (threading.Thread(target=self.on_way, args=(in_data, resp_data, order_id, order_confirm_init[0]))for order_id in order_confirm_init[1])
        for order in order_threads:
            time.sleep(1)
            order.setDaemon(True)
            order.start()
        for order in order_threads:
            order.join()

    def pending_receipt(self, resp_data, order_info):
        res = OrderManage(self.token).receipt_order(*order_info)
        try:
            assert res['code'] == resp_data[0]['code']
            assert res['data']['msg'] == resp_data[1]['msg']
        except Exception as err:
            self.log.error('---回单处理接口用例不通过，请检查问题---')
            raise err

    @pytest.mark.run(order=3)
    @allure.severity('normal')
    @allure.title('回单处理接口用例')
    @allure.story('回单处理')
    @pytest.mark.test_receipt_order
    def test_receipt_order(self, receipt_order_init):
        """
        接口描述：测试订单回单处理功能
        resp_data：{'backBucketList': [{}}              用例断言接口示例
        in_data：{'code': '1000', 'msg': '回单成功'}     用例请求参数示例
        receipt_order_init：                           初始化环境传入订单商品空桶主id列表、订单空桶子id列表、订单商品品牌id、订单id列表
        """
        in_datas = []
        resp_datas = []
        data = self.yaml_data.get_yaml_data('../data/receipt_order.yaml')
        for in_data in data:
            in_datas.append(in_data[0])
            resp_datas.append(in_data[1])
        # print(resp_datas)

        # zip()函数用于将可迭代的对象作为参数,将对象中对应的元素打包成一个个元组,然后返回由这些元组组成的列表
        receipt_threads = (threading.Thread(target=self.pending_receipt, args=(resp_datas, order_info))for
                           order_info in zip(in_datas, receipt_order_init[0], receipt_order_init[1], receipt_order_init[2], receipt_order_init[3]))
        for receipt in receipt_threads:
            time.sleep(1)
            receipt.setDaemon(True)
            receipt.start()
        for receipt in receipt_threads:
            receipt.join()

    def app_pay(self, in_data, resp_data, pay_status, order_info):
        # 判断支付状态
        if "0" in pay_status:
            res = OrderManage(self.token).offline_pay(in_data, *order_info)
            try:
                assert res['code'] == resp_data['code']
                assert res['data']['msg'] == resp_data['msg']
            except Exception as err:
                self.log.error('---线下支付接口用例不通过，请检查问题---')
                raise err

    @pytest.mark.run(order=4)
    @allure.severity('critical')
    @allure.title('线下支付接口用例')
    @allure.story('线下支付')
    @pytest.mark.test_offline_pay
    @pytest.mark.parametrize('in_data, resp_data', yaml_data.get_yaml_data('../data/offline_pay.yaml'))
    def test_offline_pay(self, in_data, resp_data, offline_pay_init, offline_pay_init2):
        """
        接口描述：测试线下支付功能
        order_id：初始化环境传入的订单id列表
        offline_pay_init2：                                                    初始化环境传入的订单应收金额列表
        offline_pay_init1[1]：                                                 初始化环境传入的订单支付状态列表
        resp_data：{'code': '1000', 'msg': '支付成功'}                          用例断言接口示例
        in_data：{'offlinePaymentAmount': 10, 'orderId': 'id', 'payType': 2}  用例请求参数示例
        """
        pay_threads = (threading.Thread(target=self.app_pay, args=(in_data, resp_data, offline_pay_init[1], order_id))for order_id in zip(offline_pay_init[0], offline_pay_init2))
        for pay_thread in pay_threads:
            time.sleep(1)
            pay_thread.setDaemon(True)
            pay_thread.start()
        for pay_thread in pay_threads:
            pay_thread.join()


if __name__ == '__main__':
    for one in os.listdir('../report/temp'):
        if 'json' in one:
            os.remove(f'../report/temp/{one}')
    pytest.main(['test_order_manage.py', '-s', '--alluredir', '../report/temp'])
    os.system('allure serve ../report/temp')

