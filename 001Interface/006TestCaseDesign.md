### 自动化测试用例设计

    excel用例模板如下
    
|用例编号|模块|接口名称|优先级|标题|URL|前置条件|请求方式|请求头|请求参数|预期结果|响应预期结果|实际结果|
|------|---|-------|-----|---|---|------|-------|----|-------|------|----------|-------|
|Login001|登录模块|登录认证|高|用户名正确，密码正确|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"sq0777","password":"xintian"}|登录成功，返回正确信息|{"code": 20000, "data":"{"token": 123}", "flag": "**教育", "msg": "成功", "success": false}||
|Login002|登录模块|登录认证|中|正确的用户名，密码为空|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"sq0777","password":""}|登录失败，返回错误信息|{"code": 9999, "data":"", "flag": "**教育", "msg": "输入的密码错误!", "success": false}||
|Login003|登录模块|登录认证|中|用户名为空，密码正确|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"","password":"xintian"}|登录失败，返回错误信息|{"code": 9999, "data": "", "flag": "**教育", "msg": "该用户不存在!", "success": false}||
|Login004|登录模块|登录认证|中|用户名和密码都为空|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"","password":""}|登录失败，返回错误信息|{"code": 9999, "data": "", "flag": "**教育", "msg": "该用户不存在!", "success": false}||
|Login005|登录模块|登录认证|高|用户名正确，密码错误|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"sq0777","password":"789"}|登录失败，返回错误信息|{"code": 9999, "data": "", "flag": "**教育", "msg": "输入的密码错误!", "success": false}||
|Login006|登录模块|登录认证|高|用户名错误，密码正确|/account/sLogin|数据库里存在登录用户名和密码|post|无|{"username":"abcde","password":"xintian"}|登录失败，返回错误信息|{"code": 9999, "data": "", "flag": "**教育", "msg": "该用户不存在!", "success": false}||
