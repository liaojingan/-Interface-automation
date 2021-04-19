# coding=utf-8
# @File     : test_log_basic.py
# @Time     : 2021/2/22 17:47
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
# coding=utf-8
# @File     : test_log.py
# @Time     : 2021/2/22 17:43
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm

import logging
import datetime


# 测试日志类
class TestLog(object):


    def logger(self):
        # 调用配置函数
        logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                            filename=f'../logs/{datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")}.txt',
                            level=logging.INFO,
                            filemode='a')
        return logging


if __name__ == '__main__':
    log_txt = TestLog()
    # 要设置比上面INFO等级高的日志才打印
    log_txt.logger().error('---hello---')



