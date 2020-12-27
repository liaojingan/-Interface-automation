## 重构POST请求

```python
import requests
import json

url = 'https://m.runtianxia.net/api/rx/api/fans/dataList'
data = {
    'pageNo': 0,
    'pageSize': 10,
    'queryType': '',
    'requestMode': 1,
    'token': 'XEIPqDS1tWNL+eoJU+K2m+GIC8WIljT9J5QOxRa7pu5Dz37tOtmeP3QAwsqF6WQjN7ALAv9W3CPRHYB8WJrwNi0JjgyOVPKfijGOS2rJKfgy32/SJ1WXMGUqhAklY+AnRr0u+2bUxG54AOeHC7zQ3KVJnPl90Ltq/rlZt9RkL8s='
}
def send_post(url, data):
    res = requests.post(url=url, data=data).json()
    return json.dumps(res)
print(11)
print(send_post(url, data))
```

## 封装上面的函数

```python
import requests
import json

class RunMain(object):

    def __init__(self, url, method, data=None):
        self.res = self.run_main(url, method, data)

    def send_get(self, url, data):
        res = requests.get(url=url, data=data).json()
        return json.dumps(res, indent=2, sort_keys=True)

    def send_post(self, url, data):
        res = requests.post(url=url, data=data).json()
        return json.dumps(res, indent=2, sort_keys=True)

    def run_main(self, url, method, data=None):
        res = None
        if method == 'GET':
            self.res = self.send_get(url, data)
        else:
            res = self.send_post(url, data)
        return res


if __name__ == '__main__':
    url = 'https://www.imooc.com/apiw/logo?callback=jQuery21007436581783633556_1609061019018&_=1609061019019'
    run = RunMain(url, 'GET')
    print(run)
```

