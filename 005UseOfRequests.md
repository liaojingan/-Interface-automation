# Requests库参考文档
    https://2.python-requests.org/zh_CN/latest/user/quickstart.html
    
## Requests库安装

    方法一：终端或cmd命令窗口执行：pip install requests -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com命令即可
    其中：http://pypi.douban.com/simple/ --trusted-host pypi.douban.com为豆瓣源
    
    
    url可选：
        阿里云 http://mirrors.aliyun.com/pypi/simple/
        中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/
        豆瓣(douban) http://pypi.douban.com/simple/
        清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/
        中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple/
        
    方法二：可在pypi.org/下载压缩包
        解压到python目录下，然后cmd命令窗口进入到解压后的requests目录执行python setup.py install安装
        
    
## Requests库的使用

    1、请求方法的使用
        *导入requests模块；
        *获取某个网页
        
```python
# 请求方法的使用：用data参数说明放在消息体中
import requests

r1 = requests.get('https://api.github.com/events')
r2 = requests.put('http://httpbin.org/put',data = {'key':'value'})
r3 = requests.delete('http://httpbin.org/delete')
r4 = requests.post('http://httpbin.org/post', data = {'key':'value'})
```

    2、URL参数的使用
        *方法一：可以数据键值对形式置于URL中，跟在一个问号后面
        *方法二：使用params关键字参数，以一个字符串字典来提供这些参数
        
```python
# 参数的使用:使用params参数说明放在urlencode中
import requests,pprint

# 方法一
r1 = requests.get("http://localhost/api/mgr/sq_mgr/?action=list_course&pagenum=1&pagesize=20")
# 以json格式打印数据
pprint.pprint(r1.json())

# 方法二
params = {'action':'list_course', 'pagenum':'1', 'pagesize':'20'}
r = requests.get("http://localhost/api/mgr/sq_mgr/", params=params)
pprint.pprint(r.json())
```

    3、定制请求头的使用
        *传递一个dict给headers参数即可
        *注意: 所有的 header 值必须是 string、bytestring 或者 unicode。尽管传递 unicode header 也是允许的，但不建议这样做。
        
```python
# 定制请求头
import requests

headers = {'user':'jingan',
           'password':'123456'}
response = requests.get("http://localhost/api/mgr/sq_mgr/", headers=headers)

rj =response.text
print(rj)
```    

    4、复杂的POST请求及响应内容
        *你想要发送一些编码为表单形式的数据——非常像一个 HTML 表单。要实现这个，只需简单地传递一个字典给 data 参数。
         你的数据字典在发出请求时会自动编码为表单形式：  
         
        *x-www-form-urlencoded格式
        
```python
# 复杂post请求（x-www-form-urlencoded）转换为json格式对象，方便数据处理
import requests

pl = {
    'action': 'add_course',
    'data' : '''
            {
                "name":"php",
                "desc":"php课程",
                "display_idx":"3"
            }'''
}

response = requests.post("http://localhost/api/mgr/sq_mgr/",data=pl)
ret=response.json()

if ret['retcode'] == 0:
    print("pass")
else:
    print("error")
```


```python
# 复杂post请求
import requests

payload = {
  "action" : "add_course_json",
  "data"	 : {
    "name":"初中数学",
    "desc":"初中数学课程",
    "display_idx":"4"
  }
}
response = requests.post("http://localhost/apijson/mgr/sq_mgr/", json=payload)

rj =response.text
print(rj)
```





 