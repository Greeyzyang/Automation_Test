#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/9/15 17:04
# @Author : Greey
# @FileName: Test_AppSDK_Smoke.py



'''
测试步骤：
1：登录app
2:点击所有按钮

预期结果：
1：登录app成功
2:点击所有按钮成功

'''


import pytest
import os
import time
import allure
from ApiTest.Common.Appcommon import App
from ApiTest.Common.Readyaml import Yamlc
from ApiTest.Common.Log import MyLog
from selenium.webdriver.common.by import By

current_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
yaml_path = father_path + "\\" + "Testdata\\app.yaml"


@allure.feature('设备端业务流程')
@allure.description('验证APP和Wyze交互场景')
class TestClass:
    def setup(self):
        print("Test Start")
        self.log = MyLog()
        desired_caps = Yamlc(yaml_path).get_yaml_data(1, "Model", "desired_caps")
        desired_caps2 = Yamlc(yaml_path).get_yaml_data(2, "Model", "desired_caps")
        self.app = App(desired_caps)
        self.app_setting = App(desired_caps2)
        self.log.debug(u'初始化测试数据')

    def teardown(self):
        print("Test End")

    @allure.story("设备端通过性验证")
    @allure.severity('blocker')
    def test_appwyze_smoke(self):
        self.driver = self.app.open_app()
        if self.app.object_exist("总是允许") == True:
            self.app.find_elementby(By.XPATH, '//*[@text="总是允许"]').click()
        size = self.driver.get_window_size()
        if self.app.object_exist("2C:AA:8E:00:AB:95") == False:
            self.app.close_app()
            self.app_setting.restart_bluetooth()
            self.app.open_app()
            if self.app.object_exist("2C:AA:8E:00:AB:95") == False:
                self.driver.keyevent(4)                     #模拟返回键
                self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="解绑"]').click()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="2C:AA:8E:00:AB:95"]').click()
        # self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="请在设备上点击确认"]')
        # self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="绑定成功"]')


        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.Button" and @text="完成"]').click()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="2C:AA:8E:00:AB:95  已连接"]')
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设备信息"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设备电量"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="活动数据"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="数据同步"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="查找手环"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="重启手环"]').click()
        time.sleep(15)
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="发送通知"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="获取应用排序"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设置应用排序"]').click()
        self.app.assert_in_text()
        self.app.swpe(size['width']*0.25, size['height']*0.85, size['width']*0.25, size['height']*0.5)
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="获取勿扰模式"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设置勿扰模式"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="获取抬腕亮屏"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设置抬腕亮屏"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="获取心率检测"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设置心率检测"]').click()
        self.app.assert_in_text()
        self.app.swpe(size['width']*0.25, size['height']*0.95, size['width']*0.25, size['height']*0.5)
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="获取屏幕亮度"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设置屏幕亮度"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="获取震动开关"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设置震动开关"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设置解锁方式"]').click()
        self.app.assert_in_text()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="获取解锁方式"]').click()
        self.app.assert_in_text()
        self.app.swpe(size['width']*0.25, size['height']*0.25, size['width']*0.25, size['height']*0.95)
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="解绑"]').click()
        self.app.close_app()


if __name__ == '__main__':
     pytest.main()
