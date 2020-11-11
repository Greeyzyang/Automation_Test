#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/11/7 22:00
# @Author : Greey
# @FileName: Concurrent_Test.py


import pytest
import os
import time
import allure
from ApiTest.Common.Appcommon import App
from ApiTest.Common.Readyaml import Yamlc
from ApiTest.Common.Log import MyLog
from selenium.webdriver.common.by import By
import appium
import threading

current_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "../..")                                  #获取上上级目录
yaml_path = father_path + "\\" + "Testdata\\app.yaml"

@allure.feature('模拟设备端业务流程')
@allure.description('验证Wyzewatch设备操作场景')
class TestClass:
    def setup(self):
        print("Test Start")
        self.log = MyLog()
        desired_caps = Yamlc(yaml_path).get_yaml_data(1, "Model", "desired_caps")
        desired_caps2 = Yamlc(yaml_path).get_yaml_data(3, "Model", "desired_caps")
        self.wyzeband_mac1 = "9C:F6:DD:38:1A:F5"
        # self.wyzeband_mac = "9C:F6:DD:38:15:E7"
        self.wyzeband_mac2 = "9C:F6:DD:38:19:59"
        # self.wyzeband_mac = "9C:F6:DD:38:18:75"
        self.desired_caps = desired_caps
        self.app = App(desired_caps)
        self.app_setting = App(desired_caps2)
        self.log.debug(u'初始化测试数据')

    def teardown(self):
        # self.app.close_app()                                                                                           #关闭App
        print("Test End")

    @allure.story("模拟Saturn设备端操作验证")
    @allure.severity('blocker')
    @pytest.mark.smoke
    def test_smoke1(self):
        # App.start_appium(4723, 4724, "468207dd")
        self.driver = self.app.open_application('4723')
        time.sleep(1)
        self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='SATURN_设备']").click()
        time.sleep(1)
        while self.app.object_exist(self.wyzeband_mac1 + "  正在连接...") :
            time.sleep(1)
        if self.app.object_exist(self.wyzeband_mac1 + "  已连接") == False:
            self.app.find_elementby(By.XPATH, "//*[@text='解绑']").click()
            self.app.click_prompt_box()
            if (self.app.object_exist("realme Watch Saturn") or self.app.object_exist("WYZE") or self.app.object_exist("hey+")) == False:
                self.app.close_app()
                self.app_setting.restart_bluetooth()                                                                       #重启蓝牙
                self.driver = self.app.open_app()
                self.app.find_elementby(By.XPATH, "//*[@text='SATURN_设备']").click()
                self.app.find_elementby(By.XPATH, "//*[@text='解绑']").click()
            while self.app.object_exist(self.wyzeband_mac1) == False:
                time.sleep(1)
            self.app.find_elementby(By.XPATH, "//*[@text='" + self.wyzeband_mac1 + "']").click()
            while self.app.object_exist("请在设备上点击确认") == False:
                time.sleep(1)
            # self.driver.keyevent(4)
            # self.driver.keyevent(4)
            self.app.find_elementby(By.XPATH, "//*[@text='完成']").click()
            self.app.find_elementby(By.XPATH, "//*[@text='SATURN_设备']").click()
            self.app.saturn_inputclick("160", "240", "160", "240")
            self.driver.keyevent(4)
            self.app.find_elementby(By.XPATH, "//*[@text='SATURN_设备']").click()
            # self.app.find_elementby(By.XPATH, "//@text='" + self.wyzeband_mac1 + " 已连接']")
        # else:
        #     self.driver.keyevent(4)
        #     self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='SATURN_APP']").click()
        time.sleep(1)
        for i in range(1, 2):
            self.log.debug(str(i))
            self.app.device_upslide()
            self.app.device_home()
            self.app.device_longhome()
            self.app.device_home()
    def test_smoke2(self):
        # App.start_appium(4725, 4726, "HDP9K19128907088")
        self.driver1 = self.app_setting.open_application('4725')
        time.sleep(1)
        self.app_setting.find_elementby(By.XPATH, "//android.widget.Button[@text='SATURN_设备']").click()
        time.sleep(1)
        while self.app_setting.object_exist(self.wyzeband_mac2 + "  正在连接...") :
            time.sleep(1)
        if self.app_setting.object_exist(self.wyzeband_mac2 + "  已连接") == False:
            self.app_setting.find_elementby(By.XPATH, "//*[@text='解绑']").click()
            self.app_setting.click_prompt_box()
            if (self.app_setting.object_exist("realme Watch Saturn") or self.app_setting.object_exist("WYZE") or self.app_setting.object_exist("hey+")) == False:
                self.app_setting.close_app()
                # self.app_setting.restart_bluetooth()                                                                       #重启蓝牙
                self.driver = self.app_setting.open_app()
                self.app_setting.find_elementby(By.XPATH, "//*[@text='SATURN_设备']").click()
                self.app_setting.find_elementby(By.XPATH, "//*[@text='解绑']").click()
            while self.app_setting.object_exist(self.wyzeband_mac2) == False:
                time.sleep(1)
            self.app_setting.find_elementby(By.XPATH, "//*[@text='" + self.wyzeband_mac2 + "']").click()
            while self.app_setting.object_exist("请在设备上点击确认") == False:
                time.sleep(1)
            # self.driver.keyevent(4)
            # self.driver.keyevent(4)
            self.app_setting.find_elementby(By.XPATH, "//*[@text='完成']").click()
            self.app_setting.find_elementby(By.XPATH, "//*[@text='SATURN_设备']").click()
            self.app_setting.saturn_inputclick("160", "240", "160", "240")
            self.driver.keyevent(4)
            self.app_setting.find_elementby(By.XPATH, "//*[@text='SATURN_设备']").click()
            # self.app_setting.find_elementby(By.XPATH, "//@text='" + self.wyzeband_mac2 + " 已连接']")
        # else:
        #     self.driver.keyevent(4)
        #     self.app_setting.find_elementby(By.XPATH, "//android.widget.Button[@text='SATURN_APP']").click()
        time.sleep(1)
        for i in range(1, 2):
            self.log.debug(str(i))
            self.app_setting.device_upslide()
            self.app_setting.device_home()
            self.app_setting.device_longhome()
            self.app_setting.device_home()

# if __name__ == '__main__':
threads = []
t1 = threading.Thread(target=TestClass().test_smoke1)
threads.append(t1)
t2 = threading.Thread(target=TestClass().test_smoke2)
threads.append(t2)
for t in threads:
    t.start()
    # pytest.main()
