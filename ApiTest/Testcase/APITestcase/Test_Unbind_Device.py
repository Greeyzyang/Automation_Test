#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/8/25 16:51
# @Author : Greey
# @FileName: Test_Unbind_Device.py


'''
测试步骤：
1：登录app（https://test-api.wyzecam.com/app/user/login）
2：生成手环token（https://test-wristband-service.wyzecam.com/app/v2/wristband/generate_token）
3：绑定手环（https://test-wristband-service.wyzecam.com/app/v3/user/bind）
4：解除绑定手环（https://test-wristband-service.wyzecam.com/app/v3/user/unbind）
预期结果：
1：登录app成功
2：成功生成token
3：绑定手环成功
4：解除绑定手环成功
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
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "../..")
config_path = father_path + "\\" + "Config\\Config.ini"
yaml_path = father_path + "\\" + "Testdata\\unbind_device.yaml"



@allure.feature('解除绑定手环')
@allure.description('验证不同场景解除绑定手环')
class TestClass:
    def setup(self):
        print("Test Start")
        self.config = ReadConfig(config_path)
        self.login_host = self.config.get_value("Wristband_Alpha", "host")
        self.login_host = self.login_host.encode('utf-8')                                                             #config文件获取host

        self.yaml = Yamlc(yaml_path).get_yaml_data(1, "unbind_device")
        self.method = Yamlc(yaml_path).get_yaml_data(1, "unbind_device", "method")
        self.url = Yamlc(yaml_path).get_yaml_data(1, "unbind_device", "url")
        self.parm = Yamlc(yaml_path).get_yaml_data(1, "unbind_device", "parm")
        self.expect = Yamlc(yaml_path).get_yaml_data(1, "unbind_device", "expect")                                  #yaml文件获取传入参数
        self.parm2 = Yamlc(yaml_path).get_yaml_data(2, "unbind_device", "parm")
        self.expect2 = Yamlc(yaml_path).get_yaml_data(2, "unbind_device", "expect")
        self.parm3 = Yamlc(yaml_path).get_yaml_data(3, "unbind_device", "parm")
        self.expect3 = Yamlc(yaml_path).get_yaml_data(3, "unbind_device", "expect")
        self.url = self.login_host + self.url
        self.log = MyLog()
        self.log.debug(u'初始化测试数据')

    def teardown(self):
        print("Test End")

    case_name = Yamlc(yaml_path).get_yaml_data(1, "unbind_device", "case_name")
    @allure.story(case_name)
    @allure.severity('blocker')
    def test_unbind_device001(self):
        Returndata = Moudle("Wristband_Alpha").bind()
        self.parm['device_token'] = Returndata[0]
        self.headers = Returndata[1]
        r = Request().post_wirst_request(method=self.method, url=self.url, data=self.parm, header=self.headers)
        print(r)
        Assertions().assert_code(r['code'], self.expect['code'])
        Assertions().assert_code(r['status_code'], self.expect['status_code'])
        Assertions().assert_time(r['time_total'], self.expect['respones_time'])
        Assertions().assert_code(r['message'], self.expect['message'])
        Assertions().assert_code(r['data']['rst'], self.expect['data']['rst'])


    case_name = Yamlc(yaml_path).get_yaml_data(2, "unbind_device", "case_name")
    @allure.story(case_name)
    @allure.severity('blocker')
    def test_unbind_device002(self):
        Returndata = Moudle("Wristband_Alpha").bind()
        self.parm2['device_token'] = Returndata[0]
        self.headers = Returndata[1]
        r = Request().post_wirst_request(method=self.method, url=self.url, data=self.parm2, header=self.headers)
        print(r)
        Assertions().assert_code(r['code'], self.expect2['code'])
        Assertions().assert_code(r['status_code'], self.expect2['status_code'])

    case_name = Yamlc(yaml_path).get_yaml_data(3, "unbind_device", "case_name")
    @allure.story(case_name)
    @allure.severity('blocker')
    def test_unbind_device002(self):
        Returndata = Moudle("Wristband_Alpha").bind()
        #
        self.parm3['device_token'] = Returndata[0] + 'Greey'
        self.headers = Returndata[1]
        r = Request().post_wirst_request(method=self.method, url=self.url, data=self.parm3, header=self.headers)
        print(r)
        Assertions().assert_code(r['code'], self.expect3['code'])
        Assertions().assert_code(r['status_code'], self.expect3['status_code'])
if __name__ == '__main__':
     pytest.main()
