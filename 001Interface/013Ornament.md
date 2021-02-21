### 编码

    * 位：计算机的最小单位 二进制中的一位，用二进制的 0/1表示
    * 字节：八位组成一个字节。
    * 字符：我们肉眼可见的文字与符号。
    * 字符集：字符的集合。
    * 编码：将字符转换成计算机可识别的0/1代码。
    * 解码：将计算机表示的0/1编码转换成肉眼可见的字符
    
    GBK、GB2312等与UTF8之间都必须通过Unicode编码才能相互转换：
    
        * GBK、GB2312－－Unicode－－UTF8
        * UTF8－－Unicode－－GBK、GB2312
        
        GBK,GB2312以及Unicode既是字符集，也是编码方式，而UTF-8只是编码方式，并不是字符集
        GBK编码中英文字符只占一个字节

### 项目中的编码处理问题
        
    * 字符串通过编码转换为字节码 str--->(encode)--- >bytes 
    
    * 字节码通过解码转换为字符串 bytes--->(decode)- -->str
 
```python
# coding=utf-8
# @File     : code_test.py
# @Time     : 2021/2/20 21:38
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm

import sys

# 获取工具设置的编码格式，不是python本身的编码格式
print(sys.getdefaultencoding())

# 字符串--unicode
str1 = '你好'
res = str1.encode('utf-8')  # 编码：字符串转换成字节码
print(res)

res1 = res.decode('utf-8')  # 解码：字节码转换成字符串
print(res1)

"""
utf-8
b'\xe4\xbd\xa0\xe5\xa5\xbd'
你好
"""
```   

    获取响应的编码格式使用prit(req.encoding)
    
```python
# coding=utf-8
# @File     : login.py
# @Time     : 2021/2/17 15:34
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import hashlib
import requests
import pprint

HOST = 'http://121.41.14.39:8082'

# 登录密码加密
def get_md5(psw):
    md5 = hashlib.md5()
    md5.update(psw.encode('UTF-8'))
    return md5.hexdigest()

def login(in_data, get_token=True):
    url = f'{HOST}/account/sLogin'
    in_data['password'] = get_md5(in_data['password'])
    payload = in_data
    req = requests.post(url=url, params=payload)
    print(req.encoding)
    # 判断是返回token还是返回全部响应数据
    if get_token:
        return req.json()['data']['token']
    else:
        return req.json()


if __name__ == '__main__':
    text = login({'username': 'md0144', 'password': 'lja199514'}, get_token=False)
    pprint.pprint(text)

"""
UTF-8
{'code': 20000,
 'data': {'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTM4MzI1MjYsInVzZXJJZCI6MTAxNDgsInVzZXJuYW1lIjoibWQwMTQ0In0.XsR7jDZ-aVu02NjXW_7M2fd37JbHaw59i4buSPt43e0'},
 'flag': '松勤教育',
 'msg': '成功',
 'success': False}
"""
```

### 装饰器（语法糖）

    本身功能不改变，增加其他逻辑装扮
    
    函数也是一个对象
        
        * 在Python的世界里，函数和之前的对象（列表、字符串等）都是一个对象
        * 函数名可以作为参数传递
        * 也可以赋值给其他变量
        * 函数名也可以作为返回值返回
        
    闭包
        * 在一个内部函数里面，对在外部作用域（但不是全局作用域）的变量进行引用，那么这个内部函数就是闭包
        
```python
# coding=utf-8
# @File     : code_test.py
# @Time     : 2021/2/20 21:38
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm

def outer():
    x = 10
    # inner函数就是闭包函数
    def inner():
        print(x)
        # 闭包函数名作为返回值
    return inner
outer()()

"""
10
"""
```


### 装饰器概念

    装饰器本质：一个函数，该函数用来处理其他函数，它可以让其他函数在不修改代码前提下增加额外的功能，
    装饰器的返回值可以是一个函数对象。
        
    使用场景：插入日志，事务处理，缓存，权限校验等
    有了装饰器：可以抽离出大量与函数功能本身无关的雷同代码，并且可以继续复用
    
    总结：为已存在的对象，增加额外的概念
    
### 装饰器需求场景

    需求：领导想知道，该测试用例执行，服务器的响应时间是多少，我们怎么实现该代码？
    
    未加装饰器代码的用例如下、
    
```python
# coding=utf-8
# @File     : code_test.py
# @Time     : 2021/2/20 21:38
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import time

# 自动化测试场景
def foo():
    print('需要执行的用例')
    time.sleep(1)  # 用例执行间隔等待时间
```

    方案一：用例执行前开始计时，中间运行foo()函数，最后结束计时，使用开始和结束时间相减得出结果
    这种方案未修改代码，但修改了原有的执行方式，代码如下
    
```python
# coding=utf-8
# @File     : code_test.py
# @Time     : 2021/2/20 21:38
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import time

# 自动化测试场景
def foo():
    print('需要执行的用例')
    time.sleep(1)  # 用例执行间隔等待时间


"""
开始计时
foo()
结束计时
"""
def show_time(func):
    start_time = time.time()
    func()  # 传入需要执行用例的代码
    end_time = time.time()
    print('该服务器响应时间:', end_time-start_time)

show_time(foo)  # 函数名可以作为参数传入，函数名本身就是一个对象

"""
需要执行的用例
该服务器响应时间: 1.0002210140228271
"""
```
    方案二需要优化上面的代码：
    
        比如原本一个foo()函数被几个模块调用了，但是后面添加需求时其中一个模块修改了原有foo()函数执行方式，就会导致其他也调用这个foo()函数模块出问题
        
        下面代码：不改变foo()执行方式，使show_time()函数得到一个返回值，再进行调用
    
```python
# coding=utf-8
# @File     : code_test.py
# @Time     : 2021/2/20 21:38
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import time

# 自动化测试场景
def foo():
    print('需要执行的用例')
    time.sleep(1)  # 用例执行间隔等待时间

def show_time(func):
    def inner():
        start_time = time.time()
        func()  # 传入需要执行用例的代码
        end_time = time.time()
        print('该服务器响应时间:', end_time-start_time)
    return inner  # 返回一个函数对象

foo1 = show_time(foo)  # 传入foo函数得到返回的inner对象，然后赋值给foo1
foo1()  # foo1再进行函数调用

"""
需要执行的用例
该服务器响应时间: 1.000330924987793
"""
```

    方案三：
        方案二缺点：如果有十个函数就需要调用十次重新赋值，foo1 = show_time(foo)、foo2 = show_time(foo)......
        
        优化：引入语法糖（装饰器）
        为了不改变foo()原有函数执行方式，只需要在调用了这个函数的功能模块上将返回对象定义成装饰器即可，其他模块就不会受影响
        
        下面代码中如果想要将foo()函数传入到show_time()函数中只需要将将@show_time语法糖加上即可
        
```python
# coding=utf-8
# @File     : code_test.py
# @Time     : 2021/2/20 21:38
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import time


def show_time(func):
    def inner():
        start_time = time.time()
        func()  # 传入需要执行用例的代码
        end_time = time.time()
        print('该服务器响应时间:', end_time-start_time)
    return inner  # 返回一个函数对象


# 自动化测试场景
@show_time  # 将上面返回的函数对象作为装饰器
def foo():
    print('需要执行的用例')
    time.sleep(1)  # 用例执行间隔等待时间

@show_time
def foo2():
    print('需要执行的用例')
    time.sleep(1)


foo()
foo2()

"""
需要执行的用例
该服务器响应时间: 1.0009191036224365
需要执行的用例
该服务器响应时间: 1.0001766681671143
"""
```

![装饰器](img/zsq01.png)


### 带参数的装饰器

    需求场景：需要了解执行用例的测试人员
    
    * 就是在show_time()函数外面再加一层函数嵌套some_body_run(name)，并且传入参数name，最后再返回show_time对象
    * 注意代码执行顺序
    
```python
# coding=utf-8
# @File     : code_test.py
# @Time     : 2021/2/20 21:38
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import time

def some_body_run(name):
    def show_time(func):
        def inner():
            start_time = time.time()
            func()  # 传入需要执行用例的代码
            end_time = time.time()
            print('该服务器响应时间:', end_time-start_time)
            print('该测试用例的执行者是:', name)
        return inner  # 返回一个函数对象
    return show_time


# 自动化测试场景
@some_body_run('tom')  # 将上面返回的函数对象作为装饰器，并传入执行者名称
def foo():
    print('需要执行的用例')
    time.sleep(1)  # 用例执行间隔等待时间


foo()

"""
需要执行的用例
该服务器响应时间: 1.0007059574127197
该测试用例的执行者是: tom
"""
```
        
        