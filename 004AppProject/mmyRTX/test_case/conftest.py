# coding=utf-8
# @File     : conftest.py
# @Time     : 2021/2/25 9:22
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
# 初始化不能使用类
import pytest
from configs.config import USER
from lib.apiLib.psw_login import PswLogin
from lib.apiLib.order_manage import OrderManage
from lib.apiLib.order_home_page import OrderHomePage


@pytest.fixture(scope='session', autouse=True)
def start_test(request):
    print('---自动化测试开始执行---')

    def fin():
        print('---自动化测试结束---')
    request.addfinalizer(fin)

# 确认配送接口初始化
@pytest.fixture(scope='function')
def order_id_init():
    token = PswLogin().login(USER)
    # 获取订单编号
    order_id = OrderHomePage(token).home_page({'indexState': '0', 'sort': '0', 'pageIndex': '1', 'pageSize': '10'})[0]
    return order_id

# 确认配送接口初始化
@pytest.fixture(scope='function')
def order_list_init():
    token = PswLogin().login(USER)
    order_list = OrderManage(token).order_list({'orderState': '6', 'pageSize': '50', 'pageIndex': '1'})
    delivery_num = order_list["data"]["obj"]["deliveryNum"]                # 待接单订单数量
    order_ids = order_list["data"]["list"]
    # 获取订单id列表
    order_list = []
    for order_id in order_ids:
        if order_id["orderState"] == "0":  # 0:待配送; 1:待指派; 2:在途中; 3:待回单; 4:代收款; 5:待审核; 6:已完成
            order_list.append(order_id["orderId"])

    # 获取待指派订单状态列表
    order_state = []
    for state in order_ids:
        if state["orderState"] == "0":
            order_state.append(state["orderState"])
    return [delivery_num, order_list, order_state]

# 完成配送接口初始化
@pytest.fixture(scope='function')
def order_confirm_init():
    token = PswLogin().login(USER)
    order_list = OrderManage(token).order_list({'orderState': '6', 'pageSize': '50', 'pageIndex': '1'})
    on_way_num = order_list["data"]["obj"]["onWayNum"]                     # 在途中订单数量
    order_ids = order_list["data"]["list"]
    # 获取订单id列表
    order_list = []
    for order_id in order_ids:
        if order_id["orderState"] == "2":  # 0:待配送; 1:待指派; 2:在途中; 3:待回单; 4:代收款; 5:待审核; 6:已完成
            order_list.append(order_id["orderId"])
    return [on_way_num, order_list]

# 回单处理接口初始化
@pytest.fixture(scope='function')
def receipt_order_init():
    token = PswLogin().login(USER)
    # 获取订单列表
    order_list = OrderManage(token).order_list({"orderState": "6", "pageSize": "50", "pageIndex": "1"})
    pending_receipt_num = order_list["data"]["obj"]["pendingReceiptNum"]              # 待回单数量
    order_ids = order_list["data"]["list"]
    # 获取订单id列表
    order_list = []
    for order_id in order_ids:
        if order_id["orderState"] == "3":  # 0:待配送; 1:待指派; 2:在途中; 3:待回单; 4:代收款; 5:待审核; 6:已完成
            order_list.append(order_id["orderId"])
    # 获取订单商品品牌id
    bucket_brand_id_list = []
    for bucket_brand_id in order_ids:
        if bucket_brand_id["orderState"] == "3":
            bucket_brand_id2 = bucket_brand_id["productList"]
            for product in bucket_brand_id2:
                bucket_brand_id_list.append(product["bucketBrandId"])
    # 获取订单空桶子id列表
    bucket_sub_id_list = []
    for bucket_sub_id in order_ids:
        if bucket_sub_id["orderState"] == "3":
            bucket_sub_id2 = bucket_sub_id["productList"]
            for product in bucket_sub_id2:
                bucket_sub_id_list.append(product["bucketSubId"])
    # 获取订单商品空桶主id
    brand_main_id_list = []
    for brand_main_id in order_ids:
        if brand_main_id["orderState"] == "3":
            brand_main_id2 = brand_main_id["productList"]
            for product in brand_main_id2:
                brand_main_id_list.append(product["bucketMainId"])

    return [bucket_brand_id_list, bucket_sub_id_list, brand_main_id_list, order_list]

# 线下支付接口初始化1
@pytest.fixture(scope='function')
def offline_pay_init():
    token = PswLogin().login(USER)
    # 获取订单列表
    order_list = OrderManage(token).order_list({"orderState": "6", "pageSize": "50", "pageIndex": "1"})
    order_ids = order_list["data"]["list"]
    # 获取订单id列表
    order_list = []
    for order_id in order_ids:
        if order_id["orderState"] == "4":  # 0:待配送; 1:待指派; 2:在途中; 3:待回单; 4:待收款; 5:待审核; 6:已完成
            order_list.append(order_id["orderId"])
    # 获取订单支付状态列表
    pay_state = []
    for state in order_ids:
        if state["orderState"] == "4":
            pay_state.append(state["payState"])  # 0未支付；1已支付
    return [order_list, pay_state]

# 线下支付接口初始化2
@pytest.fixture(scope='function')
def offline_pay_init2(offline_pay_init):
    # 获取每个订单对应的应收金额列表返回
    amount_list = []
    token = PswLogin().login(USER)
    for order in offline_pay_init[0]:
        return_amount = OrderManage(token).order_return_amount({"id": order, "token": token})
        amount_receive = return_amount["data"]["obj"]["amountReceivable"]
        amount_list.append(amount_receive)
    return amount_list



