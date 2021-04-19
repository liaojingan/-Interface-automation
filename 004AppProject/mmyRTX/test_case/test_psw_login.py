# coding=utf-8
# @File     : test_psw_login.py
# @Time     : 2021/2/22 17:20
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import os
import json
import allure
import pytest
from lib.apiLib.psw_login import PswLogin
from tools.get_yaml_data import GetYamlData
from tools.test_log_basic import TestLog


# 密码登录——测试类
@allure.epic('配送app')
@allure.feature('密码登录模块')
@pytest.mark.testLogin
class TestLogin(object):


    login = PswLogin()
    yaml_data = GetYamlData()
    log = TestLog().logger()

    # @allure.issue('http://www.baidu.com')
    @allure.severity('critical')
    @allure.title('登录接口用例')
    @allure.story('登录')
    @pytest.mark.test_login
    @pytest.mark.parametrize('in_data, resp_data', yaml_data.get_yaml_data('../data/login_data.yaml'))
    # 对应传入上面的两个参数到test_login()中，in_data参数用于登录，resp_data参数用于后面取值断言
    def test_login(self, in_data, resp_data):
        """
        接口描述：测试用户登录配送app功能
        """
        with allure.step(json.dumps(in_data)):  # in_data是不可哈希元素，不能直接传入
            res = self.login.login(in_data, get_token=False)
        try:
            # 注意：断言取值的层级关系
            with allure.step(res['code']):
                assert res['code'] == resp_data['code']
        except Exception as err:
            self.log.error('---登录接口用例不通过，请检查问题---')
            # 抛出异常
            raise err


if __name__ == '__main__':
    # 删除历史重复数据
    for one in os.listdir('../report/temp'):
        if 'json' in one:
            os.remove(f'../report/temp/{one}')
    # --alluredir==../report/temp  生成allure报告需要的源数据
    pytest.main(['test_psw_login.py', '-s', '--alluredir', '../report/temp'])
    # allure serve + 路径 表示起服务后自动打开浏览器
    os.system('allure serve ../report/temp')
