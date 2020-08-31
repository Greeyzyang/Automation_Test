#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/8/18 14:04
# @Author : Greey
# @FileName: Config.py

import os
import codecs
import configparser
import Log

class ReadConfig(object):
    def __init__(self, filepath):
        self.log = Log.MyLog
        self.Cc = configparser.ConfigParser()
        self.file_path = filepath
        self.Cc.read(self.file_path, encoding="utf-8")

    def get_config_file(self):
        """
        :return: Null
        """
        if (os.path.exists(self.file_path) == False):          # 判断路径是否存在
            self.log.error(u'Config文件不存在')
        else:
            try:
                self.Cc.read(self.file_path, encoding="utf-8")
            except:
                self.log.error(u'获取Config配置文件失败，请检查文件路径')
                raise

    def get_value(self, section, name):
        """
        :param section:
        :param name:
        :return:获取某个section某个key所对应的value
        """
        try:
            value = self.Cc.get(section, name)
            return value
        except:
            self.log.error(u'获取键值失败，请检查config文件')
            raise

    def get_options(self, section):
        """
        :param section:
        :return:获取某个section所对应的键
        """
        try:
            options = self.Cc.options(section)
            return options
        except:
            self.log.error(u'获取键名失败，请检查config文件')
            raise

    def get_items(self, sections):
        """
         :param section:
         :return:获取某个section所对应的键值对
        """
        try:
            items = self.Cc.items(sections)
            return items
        except:
            self.log.error(u'获取键值对失败，请检查config文件')
            raise


    def get_sections(self):
        """
        :return: 获取文件所有的sections
        """
        try:
            sections = self.Cc.sections()
            return sections
        except:
            self.log.error(u'获取所有sections失败，请检查config文件')
            raise

# if __name__ == "__main__":
#     C = "C:\Users\EDZ\PycharmProjects\untitled\ApiTest\Config\Config.ini"
#     ReadConfig("C:\Users\EDZ\PycharmProjects\untitled\ApiTest\Config\Config.ini").get_config_file()
#     A = ReadConfig(C).get_value("Beta", "host")
#     print(A)