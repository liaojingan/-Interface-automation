## 环境初始化和数据清除

    场景1：
        * 自动化和性能测试要保证环境一定程度上的干净
     
    场景2：     
    修改商铺信息接口需要一些前置条件（这些前置条件就是环境初始化的内容）
        * 修改商铺信息接口包含了上传图片的接口
        * 修改商铺接口需要列出商铺接口提供商铺ID参数值
        * 外部还需要鉴权校验值token
        
    场景3：
        * 运行自动化测试后生成了许多脏数据，需要先清除数据再测试
        
![init](img/init01.png)
    
### 修改商铺信息接口测试

    接口文档如下
    
![init](img/init02.png)   

    1. 从上图接口文档可以看出要想测试修改商铺信息接口，首先要从图片上传接口中获取到realFileName参数的值
    作为修改商铺信息接口image_path参数的值，且需要从列出商铺接口中获取到对应的商铺id值作为修改商铺信息接口id参数值
    
        * 组装文件对象中的文件类型可以抓包查看Content-Type的值：image/jpeg
        * 图片上传接口文档如下图所示
        
![init](img/init03.png) 

        * lib————>apiLib————>myShop.py文件中定义图片上传接口函数
        * 抓包查看文件名称是file和文件类型：image/jpeg，文件对象打开方式使用rb（非文本文档都用rb表示以二进制打开）对应下面代码中组装文件对象的内容
        * data目录下先保存一张图片（03.png）方便测试
        
![init](img/init04.png)     

    图片上传接口模块类代码如下

```python
# coding=utf-8
# @File     : myShop.py
# @Time     : 2021/2/19 16:42
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import pprint
import requests
from configs.config import HOST
from lib.apiLib.login import Login


class MyShop(object):

    def __init__(self, in_token):
        self.header = {'Authorization': in_token}

    # 列出商铺
    def shop_list(self, in_data):
        url = f'{HOST}/shopping/myShop'
        payload = in_data
        res = requests.get(url=url, params=payload, headers=self.header)
        # print(res.text)
        return res.json()

    # 图片上传接口
    def file_upload(self, filename, file_dir):
        """
        :param filename: 文件名称
        :param file_dir: 文件路径
        :return:
        """
        url = f'{HOST}/file'
        # 组装文件对象（文件名，文件对象（路径、打开方式），文件类型）
        user_file = {'file': (filename, open(file_dir, 'rb'), 'image/jpeg')}
        res = requests.post(url=url, headers=self.header, files=user_file)
        return res.json()['data']['realFileName']


if __name__ == '__main__':
    # 登录获取token
    token = Login().login('''{"username": "md0144", "password": "lja199514"}''')
    shop = MyShop(token)
    shop.file_upload('03.png', '../../data/03.png')

"""
2cdb6cfa-8eb5-499b-923f-e54ac1c3c05e.png
"""
```

    2. 跟上面一样的文件中定义修改商铺信息接口代码如下
    
```python
# coding=utf-8
# @File     : myShop.py
# @Time     : 2021/2/19 16:42
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import pprint
import requests
from configs.config import HOST
from lib.apiLib.login import Login


class MyShop(object):

    def __init__(self, in_token):
        self.header = {'Authorization': in_token}

    # 列出商铺
    def shop_list(self, in_data):
        url = f'{HOST}/shopping/myShop'
        payload = in_data
        res = requests.get(url=url, params=payload, headers=self.header)
        # pprint.pprint(res.json()['data']['records'][0]['id'])  # 获取到商铺id值
        return res.json()

    # 图片上传接口
    def file_upload(self, filename, file_dir):
        """
        :param filename: 文件名称
        :param file_dir: 文件路径
        :return:
        """
        url = f'{HOST}/file'
        # 组装文件对象（文件名，文件对象（路径、打开方式），文件类型）
        user_file = {'file': (filename, open(file_dir, 'rb'), 'image/jpeg')}
        res = requests.post(url=url, headers=self.header, files=user_file)
        return res.json()['data']['realFileName']

    # 修改商铺接口信息
    """
        {
            "name": "星巴克新建店",
            "address": "上海市静安区秣陵路303号",
            "id": "3269",
            "Phone": "13176876632",
            "rating": "6.0",
            "recent_order_num":100,
            "category": "快餐便当/简餐",
            "description": "满30减5，满60减8",
            "image_path": "b8be9abc-a85f-4b5b-ab13-52f48538f96c.png",
            "image": "http://121.41.14.39:8082/file/getImgStream?fileName=b8be9abc-a85f-4b5b-ab13-52f48538f96c.png"
        }
    """

    # 修改商铺接口
    # 请求时，实时变更的数据需要参数化（商铺Id，图形信息）
    def shop_update(self, in_data, shop_id, image_info):
        url = f'{HOST}/shopping/updatemyshop'
        in_data['id'] = shop_id  # 关联列出商铺接口获取的
        in_data['image_path'] = image_info  # 关联图片上传接口获取的
        in_data['image'] = f'{HOST}/file/getImgStream?fileName={image_info}'
        payload = in_data
        res = requests.post(url=url, headers=self.header, data=payload)
        print('--修改成功--')
        return res.json()


if __name__ == '__main__':
    # 登录获取token
    token = Login().login('''{"username": "md0144", "password": "lja199514"}''')
    shop = MyShop(token)
    real_file_name = shop.file_upload('03.png', '../../data/03.png')
    shopId = shop.shop_list({'page': 1, 'limit': 20})
    # print(shopId['data']['records'][0]['id'])  # 获取商铺id
    inData = {'name': '测试店', 'address': '上海市静安区秣陵路303号', 'description': 'description', 'id': shopId, 'rating': 6, 'recent_order_num': 100, 'category': '快餐便当/简餐', 'image_path': real_file_name, 'image': f'{HOST}/file/getImgStream?fileName={real_file_name}'}
    shop.shop_update(inData, shopId, real_file_name)
```
    
    3. test_case包中的test_myShop.py文件中定义修改商铺接口的测试类
       目前下面的test_shop_update函数暂未完全实现，需要先了解如何清除环境初始化内容后再对该函数进行补充操作
    
```python
# coding=utf-8
# @File     : test_myShop.py
# @Time     : 2021/2/19 19:28
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import os
import pytest
from lib.apiLib.myShop import MyShop
from lib.apiLib.login import Login
from tools.get_excel_data import GetExcelData


class TestMyShop(object):

    get_excel_data = GetExcelData()

    # 每个类下面所有的方法调用只运行一次，有七个我的商铺接口，但也只初始化一次登录
    def setup_class(self):
        self.token = Login().login('''{"username": "md0144", "password": "lja199514"}''')

    @pytest.mark.parametrize('in_data, resp_data', get_excel_data.get_data('我的商铺', 'listshopping'))
    def test_shop_list(self, in_data, resp_data):
        res = MyShop(self.token).shop_list(in_data)
        # 返回数据中code不是为空的，即存在则根据code值断言，不存在code值则根据error断言
        if res.get('code') is not None:
            assert res['code'] == resp_data['code']
        else:
            assert res['error'] == resp_data['error']

    @pytest.mark.parametrize('in_data, resp_data', get_excel_data.get_data('我的商铺', 'updateshopping'))
    def test_shop_update(self, in_data, resp_data):
        res = MyShop(self.token).shop_update(in_data)
        assert res['code'] == resp_data['code']


if __name__ == '__main__':
    # 删除历史重复数据
    for one in os.listdir('../report/temp'):
        if 'json' in one:
            os.remove(f'../report/temp/{one}')
    # --alluredir==../report/temp  生成allure报告需要的源数据
    pytest.main(['test_myShop.py', '-s', '--alluredir', '../report/temp'])
    # allure serve + 路径 表示起服务后自动打开浏览器
    os.system('allure serve ../report/temp')
```


### 修改商铺信息接口初始化操作

    总结测试修改商铺信息接口前，需要先初始化一些数据（即前置条件）
        * 一、保证是已登录状态
        * 二、从图片上传接口获取到图片信息
        * 三、从列出商铺接口获取到商铺id
        但登陆已经在setup_class()方法中初始化过了，所以在下面shop_update_init()方法中不需要了
        为什么不在这个shop_update_init()方法中定义登陆方法呢，因为其他接口同样需要登陆所以就抽取出去了
        
    conftest.py文件代码更新如下
    
```python
# coding=utf-8
# @File     : conftest.py
# @Time     : 2021/2/4 16:36
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm

import pytest
from lib.apiLib.login import Login
from lib.apiLib.myShop import MyShop


@pytest.fixture(scope='session', autouse=True)
def start_demo(request):
    print('---自动化测试开始执行---')

    # 数据清除操作，比如删除测试生成的数据
    def fin():
        print('---自动化测试结束---')
        # 需要先在上面的start_demo方法中传入参数request
    request.addfinalizer(fin)

@pytest.fixture(scope='function')   # 只能使用function级别，因为只有商铺修改才需要初始化这些数据
def shop_update_init():
    print('---修改商铺初始化操作---')
    token = Login().login('''{"username": "md0144", "password": "lja199514"}''')  # 登陆
    shop_id = MyShop(token).shop_list({'page': 1, 'limit': 20})['data']['records'][0]['id']  # 获取商铺id
    real_file_name = MyShop(token).file_upload('03.png', '../data/03.png')  # 获取图片信息
    return shop_id, real_file_name  # 以元组形式返回商品id和图片信息
```

    测试类方法test_shop_update调用上面的shop_update_init()修改商铺接口初始化返回的数据
        
    调用初始化数据方法：
    
        * 方法一：使用装饰器@pytest.mark.usefixtures()括号传入需要运行的用例名称，注意该方式是不能有返回值的（这个接口是有返回值的所以不能用）
        * 方法二：测试类里面的方法直接传fixture里定义的初始化函数名称作为参数
        * 方法三：叠加usefixtures：如果一个方法或者一个class用例想要同时调用多个初始化fixture操作
                可以使用@pytest.mark.usefixture()进行叠加，叠加顺序为先执行的放底层，后执行的放上层（适用于需要操作多个初始化的用例）
                
        综上可知：使用方法二即可，test_myShop.py代码修改如下
        
```python
# coding=utf-8
# @File     : test_myShop.py
# @Time     : 2021/2/19 19:28
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import os
import pytest
from lib.apiLib.myShop import MyShop
from lib.apiLib.login import Login
from tools.get_excel_data import GetExcelData


class TestMyShop(object):

    get_excel_data = GetExcelData()

    # 每个类下面所有的方法调用只运行一次，有七个我的商铺接口，但也只初始化一次登录
    def setup_class(self):
        self.token = Login().login('''{"username": "md0144", "password": "lja199514"}''')

    @pytest.mark.parametrize('in_data, resp_data', get_excel_data.get_data('我的商铺', 'listshopping'))
    def test_shop_list(self, in_data, resp_data):
        res = MyShop(self.token).shop_list(in_data)
        # 返回数据中code不是为空的，即存在则根据code值断言，不存在code值则根据error断言
        if res.get('code') is not None:
            assert res['code'] == resp_data['code']
        else:
            assert res['error'] == resp_data['error']

    @pytest.mark.parametrize('in_data, resp_data', get_excel_data.get_data('我的商铺', 'updateshopping'))
    def test_shop_update(self, in_data, resp_data, shop_update_init):  # 传入初始化fixture定义的函数名称作为参数
        # 从conftest.py文件的shop_update_init()函数返回的元组数据中以下标形式取值
        # shop_update_init[0]、shop_update_init[1]表示从返回元组中取出商铺id和图片信息
        res = MyShop(self.token).shop_update(in_data, shop_update_init[0], shop_update_init[1])
        assert res['code'] == resp_data['code']


if __name__ == '__main__':
    # 删除历史重复数据
    for one in os.listdir('../report/temp'):
        if 'json' in one:
            os.remove(f'../report/temp/{one}')
    # --alluredir==../report/temp  生成allure报告需要的源数据
    pytest.main(['test_myShop.py', '-s', '--alluredir', '../report/temp'])
    # allure serve + 路径 表示起服务后自动打开浏览器
    os.system('allure serve ../report/temp')

"""
test_myShop.py ---自动化测试开始执行---
.......---修改商铺初始化操作---
.---修改商铺初始化操作---
.---修改商铺初始化操作---
.---修改商铺初始化操作---
.---修改商铺初始化操作---
.---修改商铺初始化操作---
.---修改商铺初始化操作---
.---自动化测试结束---

============================= 14 passed in 6.75s ==============================
"""
```
   
### Pytest的环境初始化操作

    1. 先在test_case包中创建一个conftest.py文件（注意：该文件的名称是固定的）
       这个文件是有作用域的，放在test_case包中就只对这个包中的用例生效，放在项目外面就对整个项目生效
       
![init](img/init05.png)  

    2. fixtrue作用范围
    
        fixture里面有个scope参数可以控制fixture的作用范围（默认是function）：session>module>class>function
        
            * -function：每一个函数或方法都会调用
            * -class：每一个类调用一次，一个类中可以有多个方法
            * -module：每一个.py文件调用一次，该文件内又有多个function和class
            * -session：是多个文件调用一次，可以跨.py文件调用，每个.py文件就是module
            
    3. fixture（scope='function'，params=None，autouse=False，ids=None，name=None）源码解析
    
        * scope：控制fixture的初始化作用范围
        * autouse：判断是否执行用例时先自动执行初始化操作，默认False不自动执行初始化操作，True自动执行初始化操作
                  一般只有包中全局才需要设置为True自动执行
        
```python
# coding=utf-8
# @File     : conftest.py
# @Time     : 2021/2/4 16:36
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm

# 环境初始化操作
import pytest

# fixture()可以选择作用范围：session>module>class>function
@pytest.fixture(scope='session', autouse=True)  # 包中所有用例执行前先初始化操作，只执行一次，且自动执行
# 表示运行后在该包下任何一个test文件在执行前，都会先执行这个（初始化）操作
def start_demo():
    print('---自动化测试开始执行---')

# 运行test_login.py文件返回结果
"""
test_login.py ---自动化测试开始执行---
.

============================== 6 passed in 0.41s ==============================
"""
```

    scope=function则会在每条用例执行测试，先进行一次初始化操作，下面测试登录接口有6条用例所以执行了6次初始化
    
```python
# coding=utf-8
# @File     : conftest.py
# @Time     : 2021/2/4 16:36
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm

# 环境初始化操作
import pytest

# fixture()可以选择function则每条用例前都会先执行一次初始化操作
@pytest.fixture(scope='function', autouse=True)
def start_demo():
    print('---自动化测试开始执行---')

"""
test_login.py ---自动化测试开始执行---
{'code': 20000, 'data': {'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTM3OTEwMzksInVzZXJJZCI6MzIzOCwidXNlcm5hbWUiOiJzcTA3NzcifQ.z8c0rm3Dnxj44hs0mHUQTg0J5cBOI0L_jNSX4cTCEks'}, 'flag': '松勤教育', 'msg': '成功', 'success': False}
.---自动化测试开始执行---
{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '输入的密码错误!', 'success': False}
.---自动化测试开始执行---
{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '该用户不存在!', 'success': False}
.---自动化测试开始执行---
{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '该用户不存在!', 'success': False}
.---自动化测试开始执行---
{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '输入的密码错误!', 'success': False}
.---自动化测试开始执行---
{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '该用户不存在!', 'success': False}
.

============================== 6 passed in 0.40s ==============================
"""
```

    4. fin()方法执行测试后数据清除操作
        * 注意测试执行前传入的参数
        * fin()方法需要放在strat_demo()函数中，即函数嵌套函数
        
```python
# coding=utf-8
# @File     : conftest.py
# @Time     : 2021/2/4 16:36
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm

# 环境初始化操作
import pytest

@pytest.fixture(scope='session', autouse=True)
def start_demo(request):
    print('---自动化测试开始执行---')

    # 数据清除操作，比如删除测试生成的数据
    def fin():
        print('---自动化测试结束---')
        # 需要先在上面的start_demo方法中传入参数request
    request.addfinalizer(fin)   # 起到绑定作用，就是开始和结束操作绑定

"""
test_login.py ---自动化测试开始执行---
{'code': 20000, 'data': {'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTM3OTIzNTYsInVzZXJJZCI6MzIzOCwidXNlcm5hbWUiOiJzcTA3NzcifQ.qHY1YB9vafnd2faUprhQcSCI0yiuZMtTIMHcWYiSfqs'}, 'flag': '松勤教育', 'msg': '成功', 'success': False}
.{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '输入的密码错误!', 'success': False}
.{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '该用户不存在!', 'success': False}
.{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '该用户不存在!', 'success': False}
.{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '输入的密码错误!', 'success': False}
.{'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '该用户不存在!', 'success': False}
.---自动化测试结束---
"""
```
        
       
        