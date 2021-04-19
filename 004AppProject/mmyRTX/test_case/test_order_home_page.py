# coding=utf-8
# @File     : test_order_home_page.py
# @Time     : 2021/2/24 16:14
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import os
import json
import pytest
import allure
from tools.test_log_basic import TestLog
from lib.apiLib.psw_login import PswLogin
from tools.get_yaml_data import GetYamlData
from lib.apiLib.order_home_page import OrderHomePage
from configs.config import USER


# 首页——测试类
@allure.epic("配送app")
@allure.feature("首页模块")
@pytest.mark.home
class TestOrderHome(object):


    yaml_data = GetYamlData()
    log = TestLog().logger()

    # 初始化
    def setup_class(self):
        self.token = PswLogin().login(USER)

    @allure.severity("normal")
    @allure.title("首页列表接口用例")
    @allure.story("首页列表")
    @pytest.mark.test_home_page
    @pytest.mark.parametrize("in_data, resp_data", yaml_data.get_yaml_data("../data/order_home_page.yaml"))
    def test_home_page(self, in_data, resp_data):
        """
        接口描述：测试配送app首页列表订单数据
        """
        with allure.step(json.dumps(in_data)):
            res = OrderHomePage(self.token).home_page(in_data)
            if res == '首页列表无订单，请添加~':
                return '列表无订单'
            else:
                try:
                    with allure.step(res[1]):
                        assert res[1] == resp_data["code"]
                except Exception as err:
                    self.log.error("----首页接口用例不通过，请检查问题---")
                    raise err


if __name__ == "__main__":
    for one in os.listdir("../report/temp"):
        if "json" in one:
            os.remove(f"../report/temp/{one}")
    pytest.main(["test_order_home_page.py", "-s", "--alluredir", "../report/temp"])
    os.system("allure serve ../report/temp")









