### 元素定位方法

    选择界面元素
        * 根据元素的特征：ID,Name,Class,TagName,等
        * 根据元素特征和关系：css,xpath
    
    操作界面元素 
        * 输入操作：点击、输入文字、拖拽等
        * 输出操作：获取元素的各种属性
        * 根据界面上获取的数据进行分析和处理
        
### 实例操作如下

    自定义test.html文件
    
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<p id="abc">海客谈瀛洲，烟涛微茫信难求</p>
<a name="abd">天南地北双飞客，老翅儿几回寒暑</a>
<br>
<a href="https://www.baidu.com">点击进入百度</a>
<br>
<span>人道海水深，不抵相思半</span>
<br>
<span class="xyz">无意苦争春，一任群芳妒</span>
<div>
    <ul>
        <li>驿外断桥边</li>
        <li>寂寞开无主</li>
        <li>已是黄昏独自愁</li>
    </ul>
</div>
<span class="hello nice world">结庐在人境，而无车马喧</span>
</body>
</html>
```

    新建"b元素定位方法.py文件"
    
```python
# coding=utf-8
# @File     : b元素方法定位.py
# @Time     : 2021/5/4 9:34
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
from selenium import webdriver

# 创建浏览器驱动对象，打开浏览器
driver = webdriver.Chrome()
# 访问浏览器
# 获取自定义test.html路径，先复制绝对路径，通过浏览器访问，然后复制浏览器中完整链接即可
driver.get("file:///E:/WebAutoUI/WebSeleniumUI/test.html")

"""
# 根据id属性进行定位，只返回找到的第一个元素
ele = driver.find_element_by_id("abc")
# 获取元素文本值并打印
print(ele.text)
"""

"""
# 根据name属性定位，只返回找到的第一个元素
ele = driver.find_element_by_name("abd")
print(ele.text)
"""

"""
# 根据链接文本进行定位，只返回找到的第一个元素
ele = driver.find_element_by_link_text("点击进入百度")
ele.click()
"""

"""
# 根据链接文本模糊定位，只返回找到的第一个元素
ele = driver.find_element_by_partial_link_text("点击进入")
ele.click()
"""

"""
# 根据tag_name进行定位，只返回找到的第一个元素
ele = driver.find_element_by_tag_name("span")
print(ele.text)
"""

""" 
# 根据class属性进行定位，只返回找到的第一个元素
ele = driver.find_element_by_class_name("hello")
print(ele.text)
"""

"""
# 根据xpath进行定位，只返回找到的第一个元素
ele = driver.find_element_by_xpath("html/body/div/ul/li[2]")
print(ele.text)
"""

"""
# 根据css选择器匹配元素
ele = driver.find_element_by_css_selector("html > body > div > ul > li:nth-child(2)")
print(ele.text)
"""

# 匹配元素列表，返回所有能匹配到的元素，存在一个列表里边
eleSli = driver.find_elements_by_class_name("xyz")
for ele in eleSli:
    print(ele.text)

driver.quit()
```