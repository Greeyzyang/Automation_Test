#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/8/25 17:39
# @Author : Greey
# @FileName: Module.py



import os
import sys
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

    def __init__(self):
        current_path = os.path.abspath(__file__)                                                # 获取当前文件路径
        father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")      # 获取当前文件的祖父目录
        config_path = father_path + "\\" + "Config\Config.ini"
        config_path = config_path.replace("\\", "/")
        self.config = ReadConfig(config_path)
        self.log = MyLog()
        env2 = "Wristband_Alpha"
        host = self.config.get_value(env2, "host")
        Returndata = Session().get_wristband_session(env2)
        self.method = "post"
        self.url = host + "/app/v2/wristband/bind_device"
        self.parm = {
            "did": "RY.HP1.418337",
            "mac": "2C:AA:8E:00:AB:95",
            "nonce": 141361162,
            "sn": 144,
            "sign": "AAAAAAAAAAAAAAAAAAAAAJemS1kss+AgcguKwa1M51aWLi9xnWNAKOeX7rCTosjR",
            "sign_version": 2,
            "device_token": Returndata[0],
            "model": "RY.HP1"
        }
        self.headers = Returndata[1]


    @allure.step("绑定手环成功")
    def bind_device(self):
        r = Request().post_wirst_request(method=self.method, url=self.url, data=self.parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)
        return self.parm['device_token'], self.headers




# if __name__ == '__main__':
#     A = Moudle().bind_device()
#     print(A)


