#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/8/18 14:57
# @Author : Greey
# @FileName: Readyaml.py

import os
import io
import yaml
import Log

'''
封装Yaml
'''

class Yamlc(object):
    def __init__(self, filepath):
        self.log = Log.MyLog()
        self.file_path = filepath
        f = open(self.file_path, 'r')
        self.yaml = yaml.load(f, Loader=yaml.FullLoader)
    # 获取配置文件路径
    def get_yaml_file(self):
        """
        :param filepath: yaml文件路径
        :return: No
        """
        if (os.path.exists(self.file_path) == False):          # 判断路径是否存在
            self.log.error(u'Yaml文件不存在')
        else:
            try:
                f = io.open(self.file_path, 'r', encoding='utf-8')
                self.yaml = yaml.load(f.read())
            except:
                self.log.error(u'获取Yaml配置文件失败，请检查文件路径')
                raise
    # 获取配置文件数据
    def get_yaml_data(self, n, *var):
        """
        :param self:目前只支持最多2个参数
        :param n: var 获取第n个列表
        :param *var: var 长度为1时，返回一个数组/var 长度为2时，返回一个结果
        :return: yamldata
        """
        try:
            self.var = var
            if len(self.var) == 1:
                self.yamldata = self.yaml[self.var[0]][n-1]
            elif len(self.var) == 2:
                # self.yamldata = self.yaml[self.var[0]][self.var[1]]
                self.yamldata = self.yaml[self.var[0]][n-1][self.var[1]]
            return self.yamldata
        except:
            self.log.error(u'读取配置文件参数不正确,请检查传参')

# if __name__ == "__main__":
#     C = "C:\\Users\\EDZ\\PycharmProjects\\untitled\\ApiTest\\Testdata\\bind_device.yaml"
#     A = Yamlc(C)
#     B = A.get_yaml_data(1, "bind_device", "method")
#     print(B)
