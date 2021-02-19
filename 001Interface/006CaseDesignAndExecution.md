### 自动化测试用例设计

    excel用例模板如下
    
|用例编号|模块|接口名称|优先级|标题|URL|前置条件|请求方式|请求头|请求参数|
|------|---|-------|-----|---|---|------|-------|----|-------|
|Login001|登录模块|登录认证|高|用户名正确，密码正确|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"sq0777","password":"xintian"}|
|Login002|登录模块|登录认证|中|正确的用户名，密码为空|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"sq0777","password":""}|
|Login003|登录模块|登录认证|中|用户名为空，密码正确|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"","password":"xintian"}|
|Login004|登录模块|登录认证|中|用户名和密码都为空|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"","password":""}|
|Login005|登录模块|登录认证|高|用户名正确，密码错误|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"sq0777","password":"789"}|
|Login006|登录模块|登录认证|高|用户名错误，密码正确|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"abcde","password":"xintian"}|

    接上面表格
    
|预期结果|响应预期结果|实际结果|
|------|----------|------|
|登录成功，返回正确信息|{"code": 20000, "data":"{"token": 123}", "flag": "**教育", "msg": "成功", "success": false}|通过代码自动填写|
|登录失败，返回错误信息|{"code": 9999, "data":"", "flag": "**教育", "msg": "输入的密码错误!", "success": false}|通过代码自动填写|
|登录失败，返回错误信息|{"code": 9999, "data": "", "flag": "**教育", "msg": "该用户不存在!", "success": false}|通过代码自动填写|
|登录失败，返回错误信息|{"code": 9999, "data": "", "flag": "**教育", "msg": "该用户不存在!", "success": false}|通过代码自动填写|
|登录失败，返回错误信息|{"code": 9999, "data": "", "flag": "**教育", "msg": "输入的密码错误!", "success": false}|通过代码自动填写|
|登录失败，返回错误信息|{"code": 9999, "data": "", "flag": "**教育", "msg": "该用户不存在!", "success": false}|通过代码自动填写|

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
       
       执行excel测试用例流程
        * 1、读取excel数据
        * 2、把excel读取的数据关联到请求的代码中
        * 3、写入测试结果到excel
        
       导入xlrd模块进行读取excel数据；
       导入xlwt模块进行写入excel数据；
       为了防止原始excel用例数据混乱，可将用例写入新的表中而不是原表中，可使用xlutils.copy模块拷贝
     
![case](img/case05.png)

    读取excel表格数据代码如下
    
    注意这里读取的方法选取：
        * 这里不可以使用xlrd模块的nrows方法，因为存在一张表包含多个接口的情况，而nrows只能获取行数无法判断内容，所以也无法判断用例是属于哪个接口的
        * 也不可以使用[start, end]手动计算一个接口的用例来定义范围，因为存在后期如果excel表中进行了删减操作，就会导致[start,end]范围失效
        * 最好定义行数的下标idx，循环判断用例标题名称是否在表格中
    
```python
# coding=utf-8
# @File     : get_excel_data.py
# @Time     : 2021/2/19 9:58
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm

# Tools包主要用来存放操作性代码，比如读表、转换数据等
import xlrd
import json

class GetExcelData(object):

    def get_data(self, sheet_name, case_name):
        res_list = []
        # 用例路径
        excel_dir = '../data/Delivery_System_excel-V1.5.xls'
        # 打开excel对象,formatting_info=True表示保持样式
        work_book = xlrd.open_workbook(excel_dir, formatting_info=True)
        # 根据表名称获取指定的表内容
        work_sheet = work_book.sheet_by_name(sheet_name)
        # 获取一列的数据，判断传入的值是否在这一列中，存在就返回
        idx = 0
        # col_values获取整列的值
        for one in work_sheet.col_values(0):
            if case_name in one:
                # 读取表格中数据cell，获取第row+1行，col+1列数据
                req_body_data = work_sheet.cell(idx, 9).value  # 请求参数body，为后面关联接口做准备（有时也需要获取前置条件）
                resp_data = work_sheet.cell(idx, 11).value  # 响应数据，为后面断言做准备
                # 读取excel数据为字符串，转成成字典格式存入列表中
                res_list.append((json.loads(req_body_data), json.loads(resp_data)))
            idx += 1
        return res_list
    
    
        # for one in range(start_row-1, end_row):
        #     # 读取表格中数据cell
        #     req_body_data = work_sheet.cell(one, 9).value  # 请求参数body
        #     resp_data = work_sheet.cell(one, 11).value  # 响应数据
        #     res_list.append((req_body_data, resp_data))
        # return res_list


if __name__ == '__main__':
    get_data1 = GetExcelData()
    for one in get_data1('登录模块', 'Login'):
        print(one)

"""
({'username': 'sq0777', 'password': 'xintian'}, {'code': 20000, 'data': {'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTg1MTE1MDMsInVzZXJJZCI6MSwidXNlcm5hbWUiOiJhZG1pbiJ9.NcuSGdggtGJLx7BdxsB1OA2tEJcs94e4grvs6JZ2p_Q'}, 'flag': '松勤教育', 'msg': '成功', 'success': False})
({'username': 'sq0777', 'password': ''}, {'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '输入的密码错误!', 'success': False})
({'username': '', 'password': 'xintian'}, {'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '该用户不存在!', 'success': False})
({'username': '', 'password': ''}, {'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '该用户不存在!', 'success': False})
({'username': 'sq0777', 'password': '789'}, {'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '输入的密码错误!', 'success': False})
({'username': 'abcde', 'password': 'xintian'}, {'code': 9999, 'data': '', 'flag': '松勤教育', 'msg': '该用户不存在!', 'success': False})
"""
```

    5. test_case包中新建testLogin.py登录接口测试用例文件
       测试登录接口的逻辑代码都放在这里
       
    流程：
        * 读取数据(导入get_excel_data模块即可)
        * 关联请求（关联需要测试的登录接口）
        * 写结果到excel中
        
    注意：excel表格中的数据需要用json格式（本质读取还是字符串）比较好，即用双引号
        
![case](img/case06.png)


```python
# coding=utf-8
# @File     : testLogin.py
# @Time     : 2021/2/19 11:30
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import json
# 导入tools包中get_excel_data模块读取数据
from tools.get_excel_data import GetExcelData
# 关联lib.apiLib包中的登录请求接口
from lib.apiLib.login import Login

class TestLogin(object):

    get_test_data = GetExcelData()
    sales_login = Login()

    def test_login(self):
        data_list = self.get_test_data.get_data('登录模块', 'Login')
        for one in range(0, len(data_list)):
            # print(data_list[one][1]['msg'])  # 注意传入的数据类型
            res = self.sales_login.login(json.dumps(data_list[one][0]), False)
            # 断言接口返回的msg值与excel表格中msg的值是否相等
            if res['msg'] == data_list[one][1]['msg']:
                print('---pass---')
            else:
                print('---fail---')


if __name__ == '__main__':
    test = TestLogin()
    test.test_login()
```

    6. 经过上面testLogin.py文件读取excel数据并且进行断言后，现在需要在tool包中get_excel_data.py文件中定义写入结果到excel的函数
       注意：因为存在多次调试或其他同事调试时会造成原表数据混乱，所以最好copy一个对象重新写入结果
       
       写入excel结果的函数如下
       
```python
# coding=utf-8
# @File     : get_excel_data.py
# @Time     : 2021/2/19 9:58
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm

# Tools包主要用来存放操作性代码，比如读表、转换数据等
import xlrd
import json
from xlutils.copy import copy

class GetExcelData(object):

    def get_data(self, sheet_name, case_name):
        res_list = []
        # 用例路径
        excel_dir = '../data/Delivery_System_excel-V1.5.xls'
        # 打开excel对象,formatting_info=True表示保持样式
        work_book = xlrd.open_workbook(excel_dir, formatting_info=True)
        # 根据表名称获取指定的表内容
        work_sheet = work_book.sheet_by_name(sheet_name)
        # 获取一列的数据，判断传入的值是否在这一列中，存在就返回
        idx = 0
        # col_values获取整列的值
        for one in work_sheet.col_values(0):
            if case_name in one:
                # 读取表格中数据cell，获取第row+1行，col+1列数据
                req_body_data = work_sheet.cell(idx, 9).value  # 请求参数body，为后面关联接口做准备（有时也需要获取前置条件）
                resp_data = work_sheet.cell(idx, 11).value  # 响应数据，为后面断言做准备
                # 读取excel数据为字符串，转成成字典格式存入列表中
                res_list.append((json.loads(req_body_data), json.loads(resp_data)))
            idx += 1
        return res_list
    
    def write_data(self):
        excel_dir = '../data/Delivery_System_excel-V1.5.xls'
        work_book = xlrd.open_workbook(excel_dir, formatting_info=True)
        # copy出来的对象不能使用sheet_by_name()通过表名称获取表格内容，只能使用get_sheet()下标获取新表
        work_book_new = copy(work_book)
        # 返回excel对象和表对象，方便后面断言后写入
        work_sheet_new = work_book_new.get_sheet(0)
        return work_book_new, work_sheet_new


if __name__ == '__main__':
    test = GetExcelData()
    test.write_data()
```
        
    7. 上面定义了写入方法后，在test_case包中的testLogin.py文件中调用写入方法，在断言后往excel写入内容
    
```python
# coding=utf-8
# @File     : testLogin.py
# @Time     : 2021/2/19 11:30
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import json
from tools.get_excel_data import GetExcelData
from lib.apiLib.login import Login


class TestLogin(object):

    get_test_data = GetExcelData()
    sales_login = Login()
    work_book_new, work_sheet_new = get_test_data.write_data()  # 将这个函数返回的元组对象进行赋值

    def test_login(self):
        data_list = self.get_test_data.get_data('登录模块', 'Login')
        for one in range(0, len(data_list)):
            # print(data_list[one][1]['msg'])  # 注意传入的数据类型
            res = self.sales_login.login(json.dumps(data_list[one][0]), False)
            # 断言接口返回的msg值与excel表格中msg的值是否相等
            if res['msg'] == data_list[one][1]['msg']:
                print('---pass---')
                # 断言后往新复制的excel表格中[实际结果]单元格中写入结果
                # 不能用index取下标，因为存在多个一样的数据，index只取第一个
                self.work_sheet_new.write(one+1, 12, 'pass')  # 行号、列号、写入字符串内容
            else:
                print('---fail---')
                self.work_sheet_new.write(one+1, 12, 'fail')
        # 写入结果后生成新excel表格到指定路径
        self.work_book_new.save('../data/res1.xls')


if __name__ == '__main__':
    TestLogin().test_login()
```
       
    
        
    
