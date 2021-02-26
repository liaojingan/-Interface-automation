### 什么是ui自动化测试

    1、通过自动化测试工具或其他手段
    2、按照测试人员的计划--测试用例--执行测试
    3、目的是减轻手工测试的工作量
    简单来说，就是用代码模仿手工操作


### ui自动化测试有哪些需要注意的？
    
    1、ui的文本
    2、交互逻辑的正确性
    3、ui上用户行为的正确性

### ui自动化难点

    对比手工测试
    1、难以发现非预期的bug
    2、ui的复杂多变带来巨大的成本
    3、ui的测试用例，多关于用户交互方面的（不关注数据）

### 什么是selenium？

    web测试工具，运行在浏览器当中，像真正的用户在手工操作一样
    支持主流的浏览器，其功能包括：
        1、浏览器的兼容性
        2、创建回归测试
        

### 什么是webdriver？

    对浏览器提供的原生API进行封装，用这套API可以操作浏览器

    selenium是python的一个库，我们写selenium代码，也是在写python代码
    python代码不能直接操作浏览器，但可以操作webdriver
    webdriver可以操作浏览器，所以，我们间接的可以用python操作浏览器

### ui自动化操作流程

    选择界面元素
        根据元素的特征进行选择：ID、Name、Class、TagName 等
        根据元素的特征及关系：css、xpath
    操作界面元素
        输入操作：点击、输入文字、拖拽元素
        输出操作：获取元素的各种属性

### 元素定位注意事项（一定注意，并牢记）

    1、当你想要操作某个确定的元素的时候，一定保持自己的表达式唯一定位
    2、当你需要操作一组元素的时候，你必须保证自己的表达式
        a.能匹配到所有想要操作的元素
        b.不会匹配到任何其他不想操作的元素

    selenium没有给我们提供判断元素是否存在的方法，所以我们可以用匹配元素列表的方式判断。
    现根据表达式匹配元素列表，然后判断列表是否为空，若列表为空，则元素不存在，若列表不为空，则元素存在

### 练习项目
    
    1. 先启动项目中mysql的.bat文件，root密码123456、端口3306，启动后不关闭
       最后一步，单独安装Navicat或workbench客户端，通过客户端连接即可
    2. 再启动opms.exe
    3. 浏览器访问：127.0.0.1:8088，账号：libai 密码opms123
    
### selenium库和Chromdriver.exe驱动安装

    测试是否可以打开浏览器
    
```python
# coding=utf-8
# @File     : test.py
# @Time     : 2021/2/26 8:32
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import time
from selenium import webdriver

# 创建浏览器驱动对象，这里是打开浏览器
driver = webdriver.Chrome()
# 访问网址
driver.get("http://www.baidu.com")
driver.maximize_window()
# 找到元素，找到文本输入框
ele = driver.find_element_by_id("kw")
# 操作元素，输入内容
ele.send_keys("习近平")
time.sleep(1)
# 找到元素，找到 百度一下 按钮
ele = driver.find_element_by_id("su")
# 操作元素，点击按钮
ele.click()

driver.quit()
```

    