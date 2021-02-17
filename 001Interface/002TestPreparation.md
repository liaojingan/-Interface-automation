## 接口测试实战准备

### 1、实战项目简介-外卖系统（卖家端web）
    项目描述：本项目基于spring boot和vue的前后端分离
    技术架构。功能完善，包含：后端API、用户H5手机端、管理员WEB端、商户WEB端。
    主要功能包括：
    我的商铺：卖家商铺信息管理
    食品管理：商铺食品的常规操作
    订单管理：订单信息管理
    包含买家端、卖家端、管理员端
    
    地址：http://121.41.14.39:8082/shop/index.html#/login 
    账号：md0144 密码：lja199514
    
### 2、实战项目简介-外卖系统（卖家端web）-架构
    前端框架：Vue.js
    后端框架：Spring Boot
    数据库层：mysql+mongodb
    数据库连接池：Druid
    缓存：Ehcache
    
![架构图](img/interface01.png)

    提到性能一定要了解后台服务器如何部署
    
![后台部署](img/interface02.png)

### 3、常见项目软件体系
    
    单体项目
        tomcat里运行war
        springboot框架
        java -jar xx.jar
        springCloud 微服务
    项目类型
        1、前后端分离
        访问后端，会直接返回json数据格式--给前端使用，意味我们做接口需要处理json数据
        2、前后端不分离

### 4、HTTP协议解读

![http](img/http协议01.png)
   
    1. HTTP协议
    请求报文格式：四个部分
        第一部分：请求行，独占一行的；由：请求方法、请求路径、请求协议/版本组成。
        第二部分：请求头；从第二行到第N行，由键值对组成，可以有1对，也可以有N对。key:value
        第三部分：空行；独占一行的，由回车换行组成。
        第四部分：请求正文（请求消息体body）。

    常见请求头含义：
    1、User-Agent：告诉服务器客户端的相关信息（如果是浏览器会有版本，内核等信息）
    2、referer：告诉服务器，此请求是从哪个页面上发出来(防盗链)
    3、X-Requested-With：告诉服务器这个是一个ajax请求
    4、Cookie：带给服务器的cookie信息
    5、content-type：告诉服务器消息体的数据类型（决定提交参数的类型：json、表单、xml等）——重点
    
    注意：
        'Content-Type': 'application/x-www-form-urlencoded'则使用data表单格式
        'Content-Type': 'application/json'则使用json格式
        files  文件上传接口使用
        params  一般get请求使用的

    2、HTTP响应报文
    响应报文格式：四个部分组成
        第一部分：状态行，独占一行。由协议/协议的版本、状态码、状态描述符组成
        第二部分：响应头，从第二行到第N行，由键值对组成。
        第三部分：空行，独占一行的，由回车换行组成。
        第四部分：响应的正文
        
    常见响应头含义：
    1、location：告诉浏览器跳到哪里
    2、content-length：告诉浏览器回送数据的长度
    3、content-type：告诉浏览器回送数据的类型
    
![resp](img/resp01.png)
        
### 5、token

    一般前后端分离使用token（鉴权），token就是令牌的意思，比如进入景区购买了票服务员会提供门票给你
    这个门票就相当于令牌，进入后进行任意的消费，只需要最后出来结账即可，不用每次使用手机进行支付，解
    决了一直需要校验身份的问题，token优势在于只要校验过一次，在一定时限内都有效，不用再从数据库取值
    
    一般前后端分离项目中token会存在redis中，如果redis挂了就会报错token失效，前端页面正常但无法登陆

### 6、正向代理和反向代理
    fidder代理工作原理：
    浏览器 ————> fiddler ————> 服务器
    浏览器 <———— fiddler <———— 服务器
    正向代理对浏览器端是可见的
    
    ngix反向代理
    因为一个tomcat连接数是有限的，所有的请求都往同一个tomcat经过，性能就比较差
    所以就需要多个tomcat进行分担负载，也就是负载均衡。
    这些tomcat前面加了反向代理服务器ngix，PC发送请求通过反向代理服务器ngix和权
    重分配给tomcat进行解析请求，因为PC客户端不知道是发送给哪个tomcat，所以ngix
    反向代理是对客户端不透明的，对服务器是透明的
    
    tomcat应用服务器
    
### 7、fiddler
    
    post请求参数既可以放在body中，也可以放在url后面，主要看开发如何定义的，因为
    使用java语言定义body参数相对较麻烦，一些开发为了方便则直接放到url后
    
![post](img/post01.png)

### 8、json和字典区别

    json格式
        1、json有对象、数组两种结构，有字符串、数字、逻辑值、空值四种数据类型
        2、用大括号{}表示对象，对象是由属性组成的，属性是由键值对组成的，键和值用冒号隔开
           属性之间用逗号隔开，键必须用双引号引起来
        3、用中括号表示数组、数组由单独的值组成
        4、json灵活在于可以嵌套使用

    json：是一个数据格式，本身就是字符串类型
    dict:  数据类型，可以储存，pycharm控制台打印显示一定是单引号
    
    resp.text 返回是字符串格式响应体
    resp.json() 前提：响应数据一定要是json才可以使用，返回是字典

### 9、项目涉及url
    
    1、requests库帮助文档：http://cn.python-requests.org/zh_CN/latest/
    2、在线swagger接口文档：http://121.41.14.39:8082/doc.html#/home
    3、买家端--自行注册：http://vip.ytesting.com/waimai.html （账号：18824123101）
    4、卖家地址：http://121.41.14.39:8082/shop/index.html#/login 
    
    
```python
# coding=utf-8
# @File     : login.py
# @Time     : 2021/2/17 15:34
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import requests

HOST = 'http://121.41.14.39:8082'
def login(in_data):
    url = f'{HOST}/account/sLogin'
    payload = in_data
    # 这里in_data可以传给params，因为这个参数类似于get请求也是放在url后面的
    # 也可以传给data，因为抓包查看接口就是在WebForms
    req = requests.post(url=url, params=in_data)
    resp = req.text
    print(resp)

if __name__ == '__main__':
    # 接口文档提示password是使用了md5加密的，所以需要抓包查看加密字段传入而不是明文传入
    login({"username": "md0144", "password": "0e0e74cdac589d13e88043e96d29f8d3"})

# 响应结果
"""
{
	"code":20000,
	"data":{
		"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTM1NTE3OTMsInVzZXJJZCI6MTAxNDgsInVzZXJuYW1lIjoibWQwMTQ0In0.EdDWy742ULyQn8qhEGWxZJzhrRD8-yZqRd_5mkTYD6w"
	},
	"flag":"松勤教育",
	"msg":"成功",
	"success":false
}
"""
```

![login](img/login.png)

![login](img/login01.png)


### 10、定位问题方法

    打印对应的请求头、请求体body、请求url等去定位问题或者使用fiddler抓包定位
    print(resp.request.url) 请求url
    print(resp.request.headers) 打印请求头
    print(resp.request.body) 请求的body    响应对象.请求.请求体
    print(resp.headers) 响应头
    
    
    
   

    
    
        