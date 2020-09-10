#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/8/18 14:00
# @Author : Greey
# @FileName: Request.py

"""
封装request
"""

import requests
import Log
import urllib3
import json

class Request(object):

    def __init__(self):
        self.log = Log.MyLog()
        urllib3.disable_warnings()                              #忽略提示证书验证异常信息

    def get_wirst_request(self, method, url, data, header):
        """
        Get请求
        :param method: 请求方法
        :param url: host+url
        :param data: 请求体
        :param header: 请求头
        :return:
        """
        if not url.startswith('https://'):                   #判断地址是否以"https://"开头
            url = '%s%s' % ('https://', url)
        if method == 'get':
            try:
                if data is None:
                    self.respones = requests.get(url=url, headers=header, verify=False)
                else:
                    self.respones = requests.get(url=url, params=data, headers=header, verify=False)
            except:
                self.log.error(u'get请求失败，请检查')
                raise
        else:
            self.log.error(u'请求方式失败，请检查')
        try:
            self.rdict = eval(self.respones.content)
        except:
            self.log.debug(u'respones没有字段')
            self.rdict = {}
        self.rdict['time_total'] = self.respones.elapsed.total_seconds()                              #响应时间
        self.rdict['status_code'] = self.respones.status_code                                         #状态码
        return self.rdict

    def post_wirst_request(self, method, url, data, header):
        """
        Post请求
        :param method: 请求方法
        :param url: host+url
        :param data: 请求体
        :param header: 请求头
        :return:
        """
        if method == 'post':
            if not url.startswith('https://'):
                url = '%s%s' % ('https://', url)
            try:
                if data is None:
                    self.respones = requests.post(url=url, headers=header, verify=False)
                else:
                    self.respones = requests.post(url=url, params=data, headers=header, verify=False)
            except:
                self.log.error(u'post请求失败，请检查')
                raise
        else:
            self.log.error(u'请求方式失败，请检查')
        try:
            self.rdict = json.loads(self.respones.content)
        except:
            self.log.debug(u'respones没有字段')
            self.rdict = {}
        self.rdict['time_total'] = self.respones.elapsed.total_seconds()
        self.rdict['status_code'] = self.respones.status_code
        return self.rdict



# if __name__ == '__main__':
#     Request("Wristband_Alpha")