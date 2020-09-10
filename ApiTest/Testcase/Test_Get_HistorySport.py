#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/9/10 14:34
# @Author : Greey
# @FileName: Test_Get_HistorySport.py


'''
测试步骤：
1：登录app（https://test-api.wyzecam.com/app/user/login）
2：生成手环token（https://test-wristband-service.wyzecam.com/app/v2/wristband/generate_token）
3：绑定手环（https://test-wristband-service.wyzecam.com/app/v3/user/bind）
4：获取历史运动记录（https://test-wristband-service.wyzecam.com/app/v3/user/unbind）
预期结果：
1：登录app成功
2：成功生成token
3：绑定手环成功
4：获取历史运动记录成功
'''


import pytest
import os
import sys
import allure
from ApiTest.Common.Config import ReadConfig
from ApiTest.Common.Readyaml import Yamlc
from ApiTest.Common.Request import Request
from ApiTest.Common.Log import MyLog
from ApiTest.Common.Assert import Assertions
from ApiTest.Common.Session import Session
from ApiTest.Common.Module import Moudle

current_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
config_path = father_path + "\\" + "Config\\Config.ini"
yaml_path = father_path + "\\" + "Testdata\\get_historysport.yaml"


@allure.feature('获取历史运动记录')
@allure.description('验证不同场景获取运动历史记录')
class TestClass:
    def setup(self):
        print("Test Start")
        self.config = ReadConfig(config_path)
        self.login_host = self.config.get_value("Wristband_Alpha", "host")
        self.login_host = self.login_host.encode('utf-8')                                                             #config文件获取host

        self.yaml = Yamlc(yaml_path).get_yaml_data(1, "get_historysport")
        self.method = Yamlc(yaml_path).get_yaml_data(1, "get_historysport", "method")
        self.url = Yamlc(yaml_path).get_yaml_data(1, "get_historysport", "url")
        self.parm = Yamlc(yaml_path).get_yaml_data(1, "get_historysport", "parm")
        self.expect = Yamlc(yaml_path).get_yaml_data(1, "get_historysport", "expect")                                  #yaml文件获取传入参数
        self.parm2 = Yamlc(yaml_path).get_yaml_data(2, "get_historysport", "parm")
        self.expect2 = Yamlc(yaml_path).get_yaml_data(2, "get_historysport", "expect")
        self.url = self.login_host + self.url
        self.log = MyLog()
        self.log.debug(u'初始化测试数据')

    def teardown(self):
        print("Test End")

    case_name = Yamlc(yaml_path).get_yaml_data(1, "get_historysport", "case_name")
    @allure.story(case_name)
    @allure.severity('blocker')
    def test_get_historysport001(self):
        Returndata = Moudle("Wristband_Alpha").bind()
        self.headers = Returndata[1]
        r = Request().post_wirst_request(method=self.method, url=self.url, data=self.parm, header=self.headers)
        print(r)
        Assertions().assert_code(r['code'], self.expect['code'])
        Assertions().assert_code(r['status_code'], self.expect['status_code'])

    case_name = Yamlc(yaml_path).get_yaml_data(2, "get_historysport", "case_name")
    @allure.story(case_name)
    @allure.severity('blocker')
    def test_get_historysport002(self):
        Returndata = Moudle("Wristband_Alpha").bind()
        self.headers = Returndata[1]
        r = Request().post_wirst_request(method=self.method, url=self.url, data=self.parm2, header=self.headers)
        print(r)
        Assertions().assert_code(r['code'], self.expect2['code'])
        Assertions().assert_code(r['status_code'], self.expect2['status_code'])
if __name__ == '__main__':
     pytest.main()