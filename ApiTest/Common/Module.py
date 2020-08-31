#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/8/25 17:39
# @Author : Greey
# @FileName: Module.py



import os
import sys
import datetime
import allure
from ApiTest.Common.Config import ReadConfig
from ApiTest.Common.Readyaml import Yamlc
from ApiTest.Common.Request import Request
from ApiTest.Common.Log import MyLog
from ApiTest.Common.Assert import Assertions
from ApiTest.Common.Session import Session
"""
封装业务功能，类似UI自动化page object设计模式
*******************************************************
Allure中对严重级别的定义：
blocker级别：中断缺陷（客户端程序无响应，无法执行下一步操作）
critical级别：临界缺陷（ 功能点缺失）
normal级别：普通缺陷（数值计算错误）
minor级别：次要缺陷（界面错误与UI需求不符）
trivial级别：轻微缺陷（必输项无提示，或者提示不规范）
*******************************************************
"""

class Moudle(object):

    def __init__(self, env2):
        current_path = os.path.abspath(__file__)                                                # 获取当前文件路径
        father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")      # 获取当前文件的祖父目录
        config_path = father_path + "\\" + "Config\Config.ini"
        config_path = config_path.replace("\\", "/")
        self.config = ReadConfig(config_path)
        self.log = MyLog()
        # env2 = "Wristband_Alpha"
        self.host = self.config.get_value(env2, "host")
        self.Returndata = Session().get_wristband_session(env2)
        # self.method = "post"
        self.headers = self.Returndata[1]

    @allure.step("获取设备Token成功")
    def get_token(self):
        self.get_token_url = self.host + "/app/v2/wristband/get_token"
        self.get_token_parm = {}
        rdict = Request().post_wirst_request(method="post", url=self.get_token_url, data=self.get_token_parm, header=self.headers)
        Assertions().assert_code(rdict['status_code'], 200)

    @allure.step("获取用户信息成功")
    def user_info(self):
        self.user_info_url = self.host + "/app/v2/wristband/user_info"
        self.user_info_parm = {}
        rdict = Request().post_wirst_request(method="post", url=self.user_info_url, data=self.user_info_parm, header=self.headers)
        Assertions().assert_code(rdict['status_code'], 200)
        return rdict['data']['uid']

    @allure.step("绑定手环成功")
    def bind_device(self):
        self.bind_device_url = self.host + "/app/v2/wristband/bind_device"
        self.bind_device_parm = {
            "did": "RY.HP1.418337",
            "mac": "2C:AA:8E:00:AB:95",
            "nonce": 141361162,
            "sn": 144,
            "sign": "AAAAAAAAAAAAAAAAAAAAAJemS1kss+AgcguKwa1M51aWLi9xnWNAKOeX7rCTosjR",
            "sign_version": 2,
            "device_token": self.Returndata[0],
            "model": "RY.HP1"
        }
        r = Request().post_wirst_request(method="post", url=self.bind_device_url, data=self.bind_device_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)
        return self.bind_device_parm['device_token'], self.headers

    @allure.step("设置默认连接的key成功")
    def set_defaultconn(self):
        self.set_defaultconn_url = self.host + "/app/v2/wristband/set_defaultconn"
        self.set_defaultconn_parm = {"mac": "2C:AA:8E:00:AB:95", "keyid": "ab6aa7f445393ffb"}
        r = Request().post_wirst_request(method="post", url=self.set_defaultconn_url, data=self.set_defaultconn_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("获取设备对应的默认自动连接设置成功")
    def get_defaultconn(self):
        self.get_defaultconn_url = self.host + "/app/v2/wristband/get_defaultconn"
        self.get_defaultconn_parm = {"mac": "2C:AA:8E:00:AB:95"}
        r = Request().post_wirst_request(method="post", url=self.get_defaultconn_url, data=self.get_defaultconn_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("获取版本对应的功能列表（不包括基础功能）成功")
    def get_functions(self):
        self.get_functions_url = self.host + "/app/v2/wristband/get_functions"
        self.get_functions_parm = {{"version":"2.12.0"}}
        r = Request().post_wirst_request(method="post", url=self.get_functions_url, data=self.get_functions_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("上传数据成功")
    def data_upload(self):
        self.data_upload_url = self.host + "/app/v2/wristband/data_upload"
        self.data_upload_parm = {
            "data": ["Cg1SWS5IUDEuNDE4MzM3Eg0IARIJCHyIAYCc7cgBEi4IARIqCAIaIwoeCPbisvoFELXvsvoFIAAoADAAOABAAEgAUIDhAVgAoAEAiAEA"],
            "tz": "Asia\/Shanghai"
        }
        r = Request().post_wirst_request(method="post", url=self.data_upload_url, data=self.data_upload_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("获取睡眠数据成功")
    def get_sleep(self):
        self.get_sleep_url = self.host + "/app/v2/wristband/get_sleep"
        start_time = datetime.datetime.now().strftime("%Y-%m-%d")
        end_time = (datetime.datetime.now() + datetime.timedelta(days=6)).strftime("%Y-%m-%d")
        self.get_sleep_parm = {
	        "type": "multiday",
	        "start": start_time,
	        "end": end_time,
	        "tz": "Asia\/Shanghai"
        }
        r = Request().post_wirst_request(method="post", url=self.get_sleep_url, data=self.get_sleep_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)




# if __name__ == '__main__':
#     A = Moudle().bind_device()
#     print(A)


