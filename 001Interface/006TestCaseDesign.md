### 自动化测试用例设计

    excel用例模板如下
    
|用例编号|模块|接口名称|优先级|标题|URL|前置条件|请求方式|请求头|请求参数|预期结果|响应预期结果|实际结果|
|------|---|-------|-----|---|---|------|-------|----|-------|------|----------|------|
|Login001|登录模块|登录认证|高|用户名正确，密码正确|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"sq0777","password":"xintian"}|登录成功，返回正确信息|{"code": 20000, "data":"{"token": 123}", "flag": "**教育", "msg": "成功", "success": false}|通过代码自动填写|
|Login002|登录模块|登录认证|中|正确的用户名，密码为空|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"sq0777","password":""}|登录失败，返回错误信息|{"code": 9999, "data":"", "flag": "**教育", "msg": "输入的密码错误!", "success": false}|通过代码自动填写|
|Login003|登录模块|登录认证|中|用户名为空，密码正确|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"","password":"xintian"}|登录失败，返回错误信息|{"code": 9999, "data": "", "flag": "**教育", "msg": "该用户不存在!", "success": false}|通过代码自动填写|
|Login004|登录模块|登录认证|中|用户名和密码都为空|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"","password":""}|登录失败，返回错误信息|{"code": 9999, "data": "", "flag": "**教育", "msg": "该用户不存在!", "success": false}|通过代码自动填写|
|Login005|登录模块|登录认证|高|用户名正确，密码错误|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"sq0777","password":"789"}|登录失败，返回错误信息|{"code": 9999, "data": "", "flag": "**教育", "msg": "输入的密码错误!", "success": false}|通过代码自动填写|
|Login006|登录模块|登录认证|高|用户名错误，密码正确|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"abcde","password":"xintian"}|登录失败，返回错误信息|{"code": 9999, "data": "", "flag": "**教育", "msg": "该用户不存在!", "success": false}|通过代码自动填写|

### Python操作excel

    lib目录下再添加apiLib目录的目的：之后项目如果添加ui自动化，则直接新建uiLib目录即可
    在apiLib目录下可新建模块名称的py文件，例如：登录模块login；我的商铺my_shop
    
![case](img/case01.png)

    登录模块api编写
        1. 首先configs包中新建config.py文件，将HOST作为配置参数
        
![case](img/case02.png)

```python
# coding=utf-8
# @File     : config.py
# @Time     : 2021/2/17 15:34
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm

HOST = 'http://121.41.14.39:8082'
```
    
    2. 然后在apiLib包下新建login.py登录模块文件，导入上面config.py文件中配置的HOST参数
       基本库代码的意思就是：只是编写一个接口（登录接口）请求、响应获取返回值的内容
       因为Login类没有初始化的内容，所以不需要创建__init__初始化函数
       
       注意：从excel读取数据都是字符串的类型
    
![case](img/case03.png)

```python
# coding=utf-8
# @File     : login.py
# @Time     : 2021/2/17 15:34
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm

import json
import hashlib
import requests
from configs.config import HOST


# lib包主要写基本库的代码，不需要写太多逻辑代码，逻辑代码写在test_case包中
# md5加密
def get_md5(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode('UTF-8'))  # 加密操作
    return md5.hexdigest()  # 获取加密结果


class Login(object):

    # 可以直接接收json字符串
    def login(self, in_data, get_token=True):
        # 为了便于维护，尽量少写硬编码需要将url的ip和域名提取放入到config配置文件中
        url = f'{HOST}/account/sLogin'
        # 将字符串转换成字典，是为了保证从excel读取数据是字符串类型，下面无法通过value（password）取对应的值，所以转换成字典
        in_data = json.loads(in_data)
        in_data['password'] = get_md5(in_data['password'])  # 对密码进行加密操作
        payload = in_data
        resp = requests.post(url=url, data=payload)
        # 根据场景判断是否需要返回token值
        if get_token:
            return resp.json()['data']['token']
        else:
            return resp.json()


if __name__ == '__main__':
    # print(Login().login({'username': 'md0144', 'password': 'lja199514'}))
    # 模拟从excel读取json字符——注意传入的值要带双引号
    print(Login().login('''{"username": "md0144", "password": "lja199514"}'''))

"""
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTM2OTg0NDcsInVzZXJJZCI6MTAxNDgsInVzZXJuYW1lIjoibWQwMTQ0In0.iMNYLYasA7L_BWAZ8BQlUxdC_NHFIZp_sU5hlCiw2BI
"""
```
    
    3. data文件夹中放入excel用例文件
    
![case](img/case04.png)


    4. 接着在tools包下新建getExcelData.py文件实现读取excel用例表
       Tools包主要用来存放操作性代码，比如读表、转换数据等
        
    
