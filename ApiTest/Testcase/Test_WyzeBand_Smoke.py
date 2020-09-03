#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/8/31 16:18
# @Author : Greey
# @FileName: Test_WyzeBand_Smoke.py



'''
测试步骤：
1：登录app（https://test-api.wyzecam.com/app/user/login）
2：获取设备Token（https://test-api.wyzecam.com/app/v2/wristband/get_token）
3：获取用户信息（https://test-api.wyzecam.com/app/v2/wristband/user_info）
4：生成手环token（https://test-wristband-service.wyzecam.com/app/v2/wristband/generate_token）
5：绑定手环（https://test-wristband-service.wyzecam.com/app/v3/user/bind）
6：设置默认连接的key（https://test-wristband-service.wyzecam.com/app/v2/wristband/set_defaultconn）
7：获取设备对应的默认自动连接设置（https://test-wristband-service.wyzecam.com/app/v2/wristband/get_defaultconn）
8：获取版本对应的功能列表（不包括基础功能）（https://test-wristband-service.wyzecam.com/app/v2/wristband/get_functions）
9：上传数据（https://test-wristband-service.wyzecam.com/app/v2/wristband/data_upload）
10：获取睡眠数据（https://test-wristband-service.wyzecam.com/app/v2/wristband/get_sleep）
11：获取步数统计数据（https://test-wristband-service.wyzecam.com/app/v2/wristband/get_step）
12：获取心率统计数据（https://test-wristband-service.wyzecam.com/app/v2/wristband/get_heart_rate）
13：获取运动历史 （https://test-wristband-service.wyzecam.com/app/v2/wristband/get_sport_history）
14：获取某天的心率（https://test-wristband-service.wyzecam.com/app/v2/wristband/get_heart_rate_history）
15：获取手环背景图（https://test-wristband-service.wyzecam.com/app/v2/wristband/get_band_bg_list）
16：用户打点数据上报（https://test-wristband-service.wyzecam.com/app/v3/upload/taglog）
17：解绑手环（https://test-wristband-service.wyzecam.com/app/v3/user/unbind）

预期结果：
1：登录app成功
2：获取设备Token成功
3：获取用户信息成功
4：生成token成功
5：绑定手环成功
6：设置默认连接的key成功
7：获取设备对应的默认自动连接设置成功
8：获取版本对应的功能列表成功
9：上传数据成功
10：获取睡眠数据成功
11：获取步数统计数据成功
12：获取心率统计数据成功
13：获取运动历史成功
14：获取某天的心率成功
15：获取手环背景图成功
16：用户打点数据上报成功
17：解绑手环成功
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




@allure.feature('wyzeband接口业务流程')
@allure.description('验证不同场景解除绑定手环')
class TestClass:
    def setup(self):
        print("Test Start")
        self.log = MyLog()
        self.env2 = "Wristband_Alpha"
        self.moudle = Moudle(self.env2)
        self.log.debug(u'初始化测试数据')

    def teardown(self):
        print("Test End")

    @allure.story("wyzeband通过性验证")
    @allure.severity('blocker')
    def test_wyzeband_smoke(self):
        self.moudle.get_token()                                 #获取设备Token
        self.moudle.user_info()                                 #获取用户信息
        self.moudle.bind()                                      #绑定手环
        self.moudle.set_defaultconn()                           #设置默认连接的key
        self.moudle.get_defaultconn()                           #获取设备对应的默认自动连接设置
        self.moudle.get_functions()                             #获取版本对应的功能列表（不包括基础功能）
        self.moudle.data_upload()                               #上传数据
        self.moudle.get_sleep()                                 #获取睡眠数据
        self.moudle.get_step()                                  #获取步数统计数据
        self.moudle.get_heart_rate()                            #获取心率统计数据
        self.moudle.get_sport_history()                         #获取运动历史
        self.moudle.get_heart_rate_history()                    #获取某天的心率
        self.moudle.get_band_bg_list()                          #获取手环背景图
        self.moudle.upload_taglog()                             #用户打点数据上报
        self.moudle.unbind()                                    #解绑手环


if __name__ == '__main__':
     pytest.main()
