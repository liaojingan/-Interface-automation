## requests库强化技能上

### 1、数据加密解密
    
    1、加密算法分类
        加密算法主要分为：哈希算法、对称加密算法、非对称加密算法。
        哈希算法：如：MD5/SHA256
        对称加密算法：如：DES/AES/CBC
        非对称加密算法：如：RSA
        此外，还有一种编码算法，叫Base64（注意它不是加密算法）,也是用的比较多的
    
    1.1 哈希算法
        哈希是一种加密算法，也称为散列函数或杂凑函数。哈希函数是一个公开函数，可以将任意长度的消息
        M映射成为一个长度较短且长度固定的值H（M），称H（M）为哈希值、散列值（Hash Value）、杂
        凑值或者消息摘要。它是一种单向密码体制，即一个从明文到密文的不可逆映射，只有加密过程，没有解密过程。
    特点：
        易压缩：对于任意大小的输入x，Hash值的长度很小，在实际应用中，函数H产生的Hash值其长度是固定的。
        易计算：对于任意给定的消息，计算其Hash值比较容易。
        单向性：对于给定的Hash值，要找到使得在计算上是不可行的，即求Hash的逆很困难。在给定某个哈
        希函数H和哈希值H（M）的情况下，得出M在计算上是不可行的。即从哈希输出无法倒推输入的原始数值。
        这是哈希函数安全性的基础。代表：MD5、SHA256等
        
    1.2 对称加密算法
        双方使用的同一个密钥，既可以加密又可以解密，这种加密方法称为对称加密，也称为单密钥加密。
        优点：速度快，对称性加密通常在消息发送方需要加密大量数据时使用，算法公开、计算量小、加密速度快、加密效率高。
        缺点：在数据传送前，发送方和接收方必须商定好秘钥，然后 使双方都能保存好秘钥。其次如果一方的秘钥被泄露，那么
        加密信息也就不安全了。另外，每对用户每次使用对称加密算法时，都需要使用其他人不知道的唯一秘 钥，这会使得收、
        发双方所拥有的钥匙数量巨大，密钥管理成为双方的负担。代表：DES、AES、CBC等
        
    1.3 非对称加密算法
        一对密钥由公钥和私钥组成（可以使用很多对密钥）。私钥解密公钥加密数据，公钥解密私钥加密数据（私钥公钥可以互相加密解密）
        缺点：速度较慢
        优点：安全
        代表：RSA、Elgamal、背包算法、Rabin、Diffie-Hellman、ECC（椭圆曲线加密算法）。 使用最广泛的是RSA算法，Elgamal其次。
        
    1.4 Base64编码
        Base64是编码技术而不是加密技术。可以将任意的字节数组数据，通过算法，生成只有（大小写英文、数字、+、/）（一共64个字符）
        内容表示的字符串数据。即将任意的内容转换为可见的字符串形式。提供解码功能。

### 2、加密算法使用场景
    由于加密算法的特点不同，所以使用的场合也不同。
    用户登录，一般采用md5算法、RSA算法
    数据完整性校验，一般采用md5算法
    Token ，一般采用base64编码
    
### 3、Python中实现数据加密示例
   
```python
# Base64编码
import base64
#1-1 待编码字符串 
str1 = "111111" 
#1-2 编码 
pwd = base64.b64encode(str1.encode("UTF-8")) 
print('编码后的结果为：',pwd) 
#1-3 解码 
b_str = base64.b64decode(pwd) 
print('解码后的字节码为：',b_str) 
print('解码后：',b_str.decode('UTF-8'))
```

```python
# SHA256加密算法
import hashlib 
#1-1 待加密的字符串 
str='111111' 
#1-2 实例化一个sha256对象 
sha256=hashlib.sha256() 
#1-3 调用update方法进行加密 
sha256.update(str.encode('utf-8')) 
#1-4 调用hexdigest方法,获取加密结果 
print(sha256.hexdigest()) 
#结果为：bcb15f821479b4d5772bd0ca866c00ad5f926e3580720659cc80d39c9d09802a
```

```python
# MD5加密算法
import hashlib 
#1-1 待加密的字符串 
str='111111' 
#1-2 实例化一个md5对象 
md5=hashlib.md5() 
#1-3 调用update方法进行加密 
md5.update(str.encode('utf-8')) 
#1-4 调用hexdigest方法,获取加密结果 
print(md5.hexdigest()) 
#输出结果为：96e79218965eb72c92a549dd5a330112
```

```python
# RSA加密
import rsa 
#1-1 待加密的字符串 
str='111111' 
#1-2 实例化加密对象
(pubkey,privkey)=rsa.newkeys(1024) 
#1-3 公钥加密1 
pwd1=rsa.encrypt(str.encode('utf-8'),pubkey) 
print('加密后结果1为：',pwd1.hex()) 
#1-4 私钥解密1 
depwd1=rsa.decrypt(pwd1,privkey) 
print('解密后的结果1为：',depwd1.decode())
```

### 4、接口关键性名称透析
    1、token令牌（有时效性）
        * Token由服务器产生的，存在服务的内存或硬盘中
        * 有一套产生规则，会涉及到加密算法
        [用token来实现登录]
        * 开发提供一个Token接口，根据用户名+密码，获取一个Token值返回一个Token（字符串）
        * Token值服务器通过什么传给客户端？
            主要是通过响应消息体传给客户端
            也存在通过通过响应头或者Cookie传递给客户端，不过很少
            
    加密工具网站：https://tool.chinaz.com/Tools/md5.aspx （一般使用md5小写加密）
  
    定义get_md5加密函数，返回加密结果，在登录函数使用加密函数获取password的加密字符串
    再请求登录接口返回响应的json数据
    
      
```python
# coding=utf-8
# @File     : login.py
# @Time     : 2021/2/17 15:34
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import hashlib
import requests

HOST = 'http://121.41.14.39:8082'

# 登录密码加密
def get_md5(psw):
    md5 = hashlib.md5()  # 实例化对象
    md5.update(psw.encode('UTF-8'))  # 加密
    return md5.hexdigest()  # 返回加密结果

def login(in_data):
    url = f'{HOST}/account/sLogin'
    in_data['password'] = get_md5(in_data['password'])  # 根据传入的password值获取md5加密值
    payload = in_data
    req = requests.post(url=url, params=payload)
    resp = req.text
    print(resp)

if __name__ == '__main__':
    # 接口文档提示password是使用了md5加密的，所以需要抓包查看加密字段传入而不是明文传入
    login({'username': 'md0144', 'password': 'lja199514'})

"""
{
	"code":20000,
	"data":{
		"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTM2MDg3NTksInVzZXJJZCI6MTAxNDgsInVzZXJuYW1lIjoibWQwMTQ0In0.5PNse7mmZVnrfwxEFcGTqfslq-Oq1KTEPcxtykEPLcw"
	},
	"flag":"松勤教育",
	"msg":"成功",
	"success":false
}
"""
```

    获取响应数据中的token值，注意响应数据是什么格式的内容
    
```python
# coding=utf-8
# @File     : login.py
# @Time     : 2021/2/17 15:34
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import hashlib
import requests

HOST = 'http://121.41.14.39:8082'

# 登录密码加密
def get_md5(psw):
    md5 = hashlib.md5()
    md5.update(psw.encode('UTF-8'))
    return md5.hexdigest()

def login(in_data):
    url = f'{HOST}/account/sLogin'
    in_data['password'] = get_md5(in_data['password'])
    payload = in_data
    req = requests.post(url=url, params=payload)
    # 查看'Content-Type': 'application/json响应头是json格式字符串
    # print(req.headers)
    # 为了将上面响应返回的json数据转换成字典获取，方便获取token值，使用req.json()
    print(req.json())
    # 获取响应值中的token
    return req.json()['data']['token']

if __name__ == '__main__':
    login({'username': 'md0144', 'password': 'lja199514'})
```

    自动化测试登录接口则不需要返回token值，所以需要添加一个参数get_token进行判断
    是需要获取响应内容还是获取token 
    
```python
# coding=utf-8
# @File     : login.py
# @Time     : 2021/2/17 15:34
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import hashlib
import requests

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
    # 判断是返回token还是返回全部响应数据
    if get_token:
        return req.json()['data']['token']
    else:
        return req.json()


if __name__ == '__main__':
    text = login({'username': 'md0144', 'password': 'lja199514'}, get_token=False)
    print(text)
```
    
    2、Cookie（一般前后端不分离项目使用）
        * Cookie是分站点的，站点和站点之间的Cookie是相互独立的
        * 浏览器的Cookie是保存在浏览器的本地某个位置的
        * 服务端可以通过响应头中的set-Cookie参数，对客户端的Cookie进行管理
        * 浏览器的每次请求都会把该站点的Cookie发送给服务器
        * 实现登录：Cookie + Session 配合使用的
        
        原理：PC端请求访问后，server服务端接收到一个请求返回响应，Cookie就会跟随
        响应头部headers中的set-Cookie返回；再次请求时就会带上之前的Cookie值就可以正常的校验身份了
        
        分站点名词解析：例如nginx连接了多个tomcat进行负载均衡，而多个tomcat中是需要SessionId进行
        共享的，否则一个请求访问不同的tomcat时会出现SessionId不存在的情况
        
    3、SessionId（会话）
        * session是一个对象，是服务器产生的，保存在服务器的内存中（所以需要考虑性能问题）
        * session有自己的管理机制，包括session产生、销毁、超时等
        * sessionID是session对象的一个属性，是全局唯一的，永远不会重复的
        
        
    4、Cookie & sessionId合作
        一、快速理解
            用户登录成功服务器创建session，返回给客户端，客户端浏览器把session保存在它的cookie中
            
        二、过程描述
            * 登录成功服务器立马创建Session，并通过[响应头]中的set-Cookie属性把session返回给客户端
            * 浏览器把响应头中的set-cookie内容保存起来，存在浏览器自己的cookie中
            * 以后浏览器每次发送请求时，都会把该站点的全部cookie通过请求头中，传递给服务器
            
### 5、请求关联实战

    Cookie关联实战
        前端访问路径：http://120.55.190.222:7080/mgr/login/login.html
        账号：auto 密码：sdfsdfsdf
    
    1、登录接口url    
    一、http协议接口
        http://120.55.190.222:7080/mgr/login/login.html
    二、https协议接口
        https://120.55.190.222/mgr/login/login.html
        
    2、请求体
    
|参数|auto|是否必填|
|---|----|-------|
|username|auto|必填|
|password|sdfsdfsdf|必填|

    3、响应头
        Content-Type 必填 该字段值为 application/json，表示返回 JSON 格式的文本信息。
        Set-Cookie 必填 该字段保存本次登录的sessionid，比如：sessionid=89emkau5vhyg8vcwfwvq2pvr7ul2t5sc

    4、响应体
        如果请求成功，返回json格式的消息体，如下所示，retcode值为0 表示登录认证成功
        
```python
{"retcode": 0}
```

    如果输入的用户名或者密码错误，则返回结果为
    
```python
{"retcode": 1, "reason": "用户或者密码错误"}
```

    注意：
        * 如果参数是data类型的，例如：name=lisi&age=20 那么content-type就是表单，不需要传
        * 如果参数是json类型的，直接可传入字典，那么content-type就是json格式的
        * 如果参数是params类型的，参数直接放到url后面
        
        


      
      