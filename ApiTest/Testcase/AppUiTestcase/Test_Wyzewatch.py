#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/10/26 14:37
# @Author : Greey
# @FileName: Test_Wyzewatch.py

import pytest
import os
import time
import allure
from ApiTest.Common.Appcommon import App
from ApiTest.Common.Readyaml import Yamlc
from ApiTest.Common.Log import MyLog
from selenium.webdriver.common.by import By

current_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "../..")                                  #获取上上级目录
yaml_path = father_path + "\\" + "Testdata\\app.yaml"

@allure.feature('模拟设备端业务流程')
@allure.description('验证Wyze设备操作场景')
class TestClass:
    def setup(self):
        print("Test Start")
        self.log = MyLog()
        desired_caps = Yamlc(yaml_path).get_yaml_data(1, "Model", "desired_caps")
        desired_caps2 = Yamlc(yaml_path).get_yaml_data(2, "Model", "desired_caps")
        self.wyzeband_mac = "2C:AA:8E:8F:00:9E"
        self.desired_caps = desired_caps
        self.app = App(desired_caps)
        self.app_setting = App(desired_caps2)
        self.log.debug(u'初始化测试数据')

    def teardown(self):
        print("Test End")

    @allure.story("模拟设备端操作验证")
    @allure.severity('blocker')
    @pytest.mark.smoke
    def test_wyzewatch_smoke(self):
        self.driver = self.app.open_app()
        self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='调试JSON协议']").click()
        time.sleep(3)
        if self.app.object_exist(self.wyzeband_mac + "  已连接") == False:
            self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='解绑']").click()
            self.app.click_prompt_box()
        if self.app.object_exist_xpath("//android.view.ViewGroup[@index='0']") == False:
            self.app.close_app()
            self.app_setting.restart_bluetooth()                                                                       #重启蓝牙
            self.driver = self.app.open_app()
            self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='调试JSON协议']").click()
            self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='扫描']").click()
        time.sleep(5)
        self.app.find_elementby(By.XPATH, "//*[@text='" + self.wyzeband_mac + "']").click()
        time.sleep(5)
        if self.app.object_exist("请在设备上点击确认"):
            self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='完成']").click()
        self.app.input_data('{"id": ' + self.app.getid() + ', "method": "touch", "gesture": "click", "pos": {"x": "160", "y": "240"}}')
        self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='坐标点击']").click()
        self.app.clear_text()
        time.sleep(5)
        # self.app.find_elementby(By.XPATH, "//@text='" + self.wyzeband_mac + " 已连接']")
        self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='上滑']").click()
        self.app.device_click(80, 80)
        self.app.device_click(240, 80)
        self.app.device_click(240, 80)
        self.app.device_click(240, 80)
        self.app.device_click(80, 240)
        self.app.device_click(240, 240)
        self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='下滑']").click()
        self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='左滑']").click()
        self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='右滑']").click()
        # self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='解绑']").click()
        self.app.close_app()                                                                                           #关闭App


if __name__ == '__main__':
     pytest.main()
