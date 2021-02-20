### Yaml测试用例格式

    1. data目录下新建data.yaml文件（建议不同模块接口放在不同的yaml文件）
    2. 使用列表套字典的格式定义用例
        * 原因：列表中包含元素，每个元素就是一个用例，字典用例里面可以定义接口详情数据
        
![yaml](img/yaml02.png)

    用例内容如下
    
```yaml
- #login_test_01
  url: /account/sLogin #路径
  method: POST #方法
  detail: 用户名正确，密码正确 #标题详情
  headers: #请求头
  data: #请求体 封装为字典
    username: sq0777
    password: xintian
  resp:
    code: 20000
    msg: 成功

- #login_test_02
  url: /account/sLogin #路径
  method: POST #方法
  detail: 正确的用户名，密码为空 #详情
  headers: #请求头
  data: #请求体
    username: sq0777
    password: ""  # 密码为空需要写上双引号
  resp:
    code: 9999
    msg: 输入的密码错误!

- #login_test_03
  url: /account/sLogin #路径
  method: POST #方法
  detail: 用户名为空，密码正确 #详情
  headers: #请求头
  data: #请求体
    username: ""
    password: xintian
  resp:
    code: 9999
    msg: 该用户不存在!

- #login_test_04
  url: /account/sLogin #路径
  method: POST #方法
  detail: 用户名和密码都为空 #详情
  headers: #请求头
  data: #请求体
    username: ""
    password: ""
  resp:
    code: 9999
    msg: 该用户不存在!

- #login_test_05
  url: /account/sLogin #路径
  method: POST #方法
  detail: 用户名正确，密码错误 #详情
  headers: #请求头
  data: #请求体
    username: sq0777
    password: 78u
  resp:
    code: 9999
    msg: 输入的密码错误!

- #login_test_06
  url: /account/sLogin #路径
  method: POST #方法
  detail: 用户名错误，密码正确 #详情
  headers: #请求头
  data: #请求体
    username: abcde
    password: xintian
  resp:
    code: 9999
    msg: 该用户不存在!
```

    3. tools ————> get_yaml_data.py文件定义函数获取上面yaml用例文件的数据
        
![yaml](img/yaml03.png)

    代码如下
   
```python
# coding=utf-8
# @File     : get_yaml_data.py
# @Time     : 2021/2/5 16:16
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import yaml

class GetYamlData(object):

    def get_yaml_data(self, file_dir):
        """
        原则：尽量少修改代码
        1: 获取什么数据
            data {'username': 'sq0777', 'password': 'xintian'}
            resp {'code': 20000, 'msg': '成功'}}
        2: 数据该如何组装返回
            分析：框架pytest需要什么格式数据
                1- 列表格式 [(),()]
                2- 要求是字典格式
        :param file_dir: 表示需要读取的yaml文件路径
        :return:
        """
        res_list = []
        fo = open(file_dir, 'r', encoding='utf-8')  # 内存中打开yaml文件
        res = yaml.load(fo, Loader=yaml.FullLoader)  # 使用第三方库获取
        print(res)
        for one in res:
            # 从yaml文件获取数据后，提取出data、resp值返回，为后面登录和断言准备
            res_list.append((one['data'], one['resp']))
        return res_list


if __name__ == '__main__':
    yaml_data = GetYamlData()
    yaml_data.get_yaml_data('../data/data.yaml')
```

    4. 接着在test_case包中的test_login.py文件导入get_yaml_data模块数据
       然后函数中使用pytest框架的装饰器调用：@pytest.mark.parametrize('in_data, resp_data', yaml_data.get_yaml_data('../data/data.yaml'))
       
![yaml](img/yaml04.png)

    代码如下
    
```python
# coding=utf-8
# @File     : test_login.py
# @Time     : 2021/2/3 15:01
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import os
import json
import allure
import pytest
from lib.apiLib.login import Login
from tools.get_excel_data import GetExcelData
from tools.get_yaml_data import GetYamlData

@allure.feature('登录模块')
@allure.epic('外卖系统')
@pytest.mark.testLogin
class TestLogin(object):

    login = Login()
    get_excel_data = GetExcelData()
    yaml_data = GetYamlData()

    @allure.issue('http://www.baidu.com')
    @allure.severity('critical')
    @allure.title('登录接口用例')
    @allure.story('登录')
    @pytest.mark.login
    @pytest.mark.parametrize('in_data, resp_data', yaml_data.get_yaml_data('../data/data.yaml'))
    # @pytest.mark.parametrize('in_data, resp_data', get_excel_data.get_data('登录模块', 'Login'))
    # 对应传入上面的两个参数到test_login()中，in_data参数用于登录，resp_data参数用于后面取值断言
    def test_login(self, in_data, resp_data):
        res = self.login.login(json.dumps(in_data), get_token=False)
        print(res)
        assert res['msg'] == resp_data['msg']


if __name__ == '__main__':
    # 删除历史重复数据
    for one in os.listdir('../report/temp'):
        if 'json' in one:
            os.remove(f'../report/temp/{one}')
    # --alluredir==../report/temp  生成allure报告需要的源数据
    pytest.main(['test_login.py', '-s', '--alluredir', '../report/temp'])
    # allure serve + 路径 表示起服务后自动打开浏览器
    os.system('allure serve ../report/temp')

"""
test_login.py ---自动化测试开始执行---
{'code': 20000, 'data': {'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTM4Mjc1OTksInVzZXJJZCI6MzIzOCwidXNlcm5hbWUiOiJzcTA3NzcifQ.0kKLLN4P-Xh6YqMCFvY4SNP9Ir0eGSn0K2BZerbX4cU'}, 'flag': '松勤教育', 'msg': '成功', 'success': False}
.{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '输入的密码错误!', 'success': False}
.{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '该用户不存在!', 'success': False}
.{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '该用户不存在!', 'success': False}
.{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '输入的密码错误!', 'success': False}
.{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '该用户不存在!', 'success': False}
.---自动化测试结束---

============================== 6 passed in 0.56s ==============================
"""
```

### 运行模式

    1- 使用 终端(win/linux)运行： python -ｍ run.py
    2- 使用执行文件运行： run.bat(Win) ; run.sh(Linux) 运行指令 ./run.sh
    3- jenkins运行 会使用自带的sh 功能运行