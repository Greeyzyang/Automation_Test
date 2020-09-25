#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/8/24 10:32
# @Author : Greey
# @FileName: Test_Bind_Device.py


'''
测试步骤：
1：登录app（https://test-api.wyzecam.com/app/user/login）
2：生成手环token（https://test-wristband-service.wyzecam.com/app/v2/wristband/generate_token）
3：绑定手环（https://test-wristband-service.wyzecam.com/app/v3/user/bind）

预期结果：
1：登录app成功
2：成功生成token
3：绑定手环成功
'''

import pytest
import os
import json
import ast
import allure
from ApiTest.Common.Config import ReadConfig
from ApiTest.Common.Readyaml import Yamlc
from ApiTest.Common.Request import Request
from ApiTest.Common.Log import MyLog
from ApiTest.Common.Assert import Assertions
from ApiTest.Common.Session import Session


current_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "../..")
config_path = father_path + "\\" + "Config\Config.ini"
yaml_path = father_path + "\\" + "Testdata\\bind_device.yaml"


@allure.feature('绑定手环')
@allure.description('验证不同场景绑定手环')
class TestClass(object):
    def setup(self):
        print("Test Start***********************")
        self.config = ReadConfig(config_path)
        self.login_host = self.config.get_value("Wristband_Alpha", "host").encode('utf-8')                         #config文件获取host
        firmware_ver = self.config.get_value("Wristband_Alpha", "firmware_ver").encode('utf-8')
        self.yaml = Yamlc(yaml_path).get_yaml_data(1, "bind_device")
        self.method = Yamlc(yaml_path).get_yaml_data(1, "bind_device", "method")
        self.url = Yamlc(yaml_path).get_yaml_data(1, "bind_device", "url")
        self.parm = Yamlc(yaml_path).get_yaml_data(1, "bind_device", "parm")
        self.expect = Yamlc(yaml_path).get_yaml_data(1, "bind_device", "expect")                                    #yaml文件获取传入参数
        self.parm2 = Yamlc(yaml_path).get_yaml_data(2, "bind_device", "parm")
        self.expect2 = Yamlc(yaml_path).get_yaml_data(2, "bind_device", "expect")
        self.parm3 = Yamlc(yaml_path).get_yaml_data(3, "bind_device", "parm")
        self.expect3 = Yamlc(yaml_path).get_yaml_data(3, "bind_device", "expect")
        self.parm4 = Yamlc(yaml_path).get_yaml_data(4, "bind_device", "parm")
        self.expect4 = Yamlc(yaml_path).get_yaml_data(4, "bind_device", "expect")
        self.parm5 = Yamlc(yaml_path).get_yaml_data(5, "bind_device", "parm")
        self.expect5 = Yamlc(yaml_path).get_yaml_data(5, "bind_device", "expect")
        self.parm6 = Yamlc(yaml_path).get_yaml_data(6, "bind_device", "parm")
        self.expect6 = Yamlc(yaml_path).get_yaml_data(6, "bind_device", "expect")
        self.parm7 = Yamlc(yaml_path).get_yaml_data(7, "bind_device", "parm")
        self.expect7 = Yamlc(yaml_path).get_yaml_data(7, "bind_device", "expect")
        env2 = "Wristband_Alpha"
        Returndata = Session().get_wristband_session(env2)
        self.wirst_cookies = Returndata[0]                                        #获取wrist端的cookies
        self.headers = Returndata[1]                                              #获取wrist端的headers
        self.headers['firmware_ver'] = firmware_ver
        self.url = self.login_host + self.url
        self.parm['device_token'] = self.wirst_cookies
        self.log = MyLog()
        self.log.debug(u'初始化测试数据')

    def teardown(self):
        print("Test End***********************")

    case_name = Yamlc(yaml_path).get_yaml_data(1, "bind_device", "case_name").encode('utf-8')
    @allure.story(case_name)
    @allure.severity('blocker')
    def test_bind_device001(self):
        r = Request().post_wirst_request(self.method, self.url, self.parm, header=self.headers)
        print(r)
        Assertions().assert_code(r['code'], self.expect['code'])
        Assertions().assert_code(r['status_code'], self.expect['status_code'])
        Assertions().assert_time(r['time_total'], self.expect['respones_time'])
        Assertions().assert_code(r['message'], self.expect['message'])
        Assertions().assert_code(r['data']['rst'], self.expect['data']['rst'])

    case_name = Yamlc(yaml_path).get_yaml_data(2, "bind_device", "case_name").encode('utf-8')
    @allure.story(case_name)
    @allure.severity('blocker')
    def test_bind_device002(self):
        self.parm2['device_token'] = self.wirst_cookies
        headers = self.headers.copy()
        headers['firmware_ver'] = ''
        r = Request().post_wirst_request(self.method, self.url, self.parm2, header=headers)
        print(r)
        Assertions().assert_code(r['code'], self.expect2['code'])
        Assertions().assert_code(r['status_code'], self.expect2['status_code'])

    case_name = Yamlc(yaml_path).get_yaml_data(3, "bind_device", "case_name").encode('utf-8')
    @allure.story(case_name)
    @allure.severity('blocker')
    def test_bind_device003(self):
        self.parm3['device_token'] = self.wirst_cookies
        headers = self.headers.copy()
        headers['access_token'] = 'AAAAAAAAAAAAAAAA'
        r = Request().post_wirst_request(self.method, self.url, self.parm3, header=headers)
        print(r)
        Assertions().assert_code(r['code'], self.expect3['code'])
        Assertions().assert_code(r['status_code'], self.expect3['status_code'])

    case_name = Yamlc(yaml_path).get_yaml_data(4, "bind_device", "case_name").encode('utf-8')
    @allure.story(case_name)
    @allure.severity('blocker')
    def test_bind_device004(self):
        self.parm4['device_token'] = self.wirst_cookies
        r = Request().post_wirst_request(self.method, self.url, self.parm4, header=self.headers)
        print(r)
        Assertions().assert_code(r['code'], self.expect4['code'])
        Assertions().assert_code(r['status_code'], self.expect4['status_code'])

    case_name = Yamlc(yaml_path).get_yaml_data(5, "bind_device", "case_name").encode('utf-8')
    @allure.story(case_name)
    @allure.severity('blocker')
    def test_bind_device005(self):
        self.parm5['device_token'] = self.wirst_cookies
        r = Request().post_wirst_request(self.method, self.url, self.parm5, header=self.headers)
        print(r)
        Assertions().assert_code(r['code'], self.expect5['code'])
        Assertions().assert_code(r['status_code'], self.expect5['status_code'])

    case_name = Yamlc(yaml_path).get_yaml_data(6, "bind_device", "case_name").encode('utf-8')
    @allure.story(case_name)
    @allure.severity('blocker')
    def test_bind_device006(self):
        self.parm6['device_token'] = self.wirst_cookies + 'Greey'
        r = Request().post_wirst_request(self.method, self.url, self.parm6, header=self.headers)
        print(r)
        Assertions().assert_code(r['code'], self.expect6['code'])
        Assertions().assert_code(r['status_code'], self.expect6['status_code'])
if __name__ == '__main__':
    pytest.main("-v -s Test_Bind_Device.py::TestClass()::test_bind_device006")
    #pytest.main()
     #pytest.main(['Test_Bind_Device.py', '-s', "--alluredir=./Report/XML"])
     # os.system('pytest -s -q --alluredir C:/Users/EDZ/PycharmProjects/untitled/ApiTest/Report/XML')
     # os.system('allure generate C:/Users/EDZ/PycharmProjects/untitled/ApiTest/Report/XML -o C:/Users/EDZ/PycharmProjects/untitled/ApiTest/Report/HTML --clean')
