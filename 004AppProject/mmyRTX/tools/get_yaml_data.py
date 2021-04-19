# coding=utf-8
# @File     : get_yaml_data.py
# @Time     : 2021/2/22 17:39
# @Author   : jingan
# @Email    : 3028480064@qq.com
# @Software : PyCharm
import json
import yaml
import pprint


# 获取data文件中的yaml用例数据
class GetYamlData(object):


    # def get_yaml_data(self, file_dir, case_name):
    #
    #     fo = open(file_dir, 'r', encoding='utf-8')
    #     res = yaml.load(fo, Loader=yaml.FullLoader)
    #     res_list = []
    #     for one in res:
    #         if case_name in one['case_name']:
    #             res_list.append((one['data'], one['resp']))
    #     return res_list
        # 注意在外层缩进
        # pprint.pprint(res_list)

    def get_yaml_data(self, file_dir):

        fo = open(file_dir, 'r', encoding='utf-8')
        res = yaml.load(fo, Loader=yaml.FullLoader)
        res_list = []
        for one in res:
            res_list.append((one['data'], one['resp']))
        # pprint.pprint(res_list)
        return res_list




if __name__ == '__main__':
    yaml_data = GetYamlData()
    yaml_data.get_yaml_data('../data/order_home_page.yaml')





