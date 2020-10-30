#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/9/15 17:04
# @Author : Greey
# @FileName: Test_IDT_Smoke.py



'''
测试步骤：
1：打开IDT
2：绑定手环
3：点击设备信息
4：点击设备电量
5：点击活动数据
6：点击数据同步
7：点击查找手环
8：点击重启手环
9：输入参数，点击发送通知（电话）
10：输入参数，点击发送通知（facebook消息）
11：输入参数，点击发送通知（短信）
12：输入参数，点击设置应用排序，点击获取应用排序
13：输入参数，点击设置勿扰模式（SMART），点击获取勿扰模式
14：输入参数，点击设置勿扰模式（DISABLE），点击获取勿扰模式
15：输入参数，点击设置勿扰模式（ALWAYS），点击获取勿扰模式
16：输入参数，点击设置勿扰模式（TIMING），点击获取勿扰模式
17：输入参数，点击设置抬腕亮屏（ON），点击获取抬腕亮屏
18：输入参数，点击设置抬腕亮屏（OFF），点击获取抬腕亮屏
19：输入参数，点击设置心率检测（ON），点击获取心率检测
20：输入参数，点击设置心率检测（OFF），点击获取心率检测
21：输入参数，点击设置屏幕亮度(LOW)，点击获取屏幕亮度
22：输入参数，点击设置屏幕亮度(MID)，点击获取屏幕亮度
23：输入参数，点击设置屏幕亮度(HIGH)，点击获取屏幕亮度
24：输入参数，点击设置震动开关（ON），点击获取震动开关
25：输入参数，点击设置震动开关（OFF），点击获取震动开关
26：输入参数，点击设置解锁方式（0），点击获取解锁方式
27：输入参数，点击设置解锁方式（1），点击获取解锁方式
28：点击解绑
29：退出APP

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
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "../..")                                  #获取上上级目录
yaml_path = father_path + "\\" + "Testdata\\app.yaml"

@allure.feature('设备端业务流程')
@allure.description('验证APP和Wyze交互场景')
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

    @allure.story("设备端通过性验证")
    @allure.severity('blocker')
    @pytest.mark.smoke
    def test_appwyze_smoke(self):
        self.driver = self.app.open_app()
        size = self.driver.get_window_size()
        self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='BRANDY_APP']").click()
        time.sleep(5)
        if self.app.object_exist(self.wyzeband_mac + "  已连接") == False:
            self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='解绑']").click()
            self.app.click_prompt_box()
            if self.app.object_exist_xpath("//android.view.ViewGroup[@index='0']") == False:
                self.app.close_app()
                self.app_setting.restart_bluetooth()                                                                       #重启蓝牙
                self.driver = self.app.open_app()
                self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='BRANDY_APP']").click()
                self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='扫描']").click()
            time.sleep(5)
            self.app.find_elementby(By.XPATH, "//*[@text='" + self.wyzeband_mac + "']").click()
            time.sleep(5)
            if self.app.object_exist("请在设备上点击确认"):
                self.driver.keyevent(4)
                self.driver.keyevent(4)
            self.app.brandy_inputclick("160", "300")
            self.driver.keyevent(4)
            self.app.find_elementby(By.XPATH, "//android.widget.Button[@text='BRANDY_APP']").click()
        self.app.tv_device_info()                                                                                      #设备信息
        self.app.tv_device_property()                                                                                  #设备电量
        self.app.tv_device_activity()                                                                                  #活动数据
        self.app.tv_device_data()                                                                                      #数据同步
        self.app.tv_find_device()                                                                                      #查找手环
        self.app.tv_reboot_device("BRANDY_APP")                                                                                    #重启手环
        self.app.tv_send_notification({"telephony": {"contact": "reeyx", "number": "1234567", "status": "RINGING_UNANSWERABLE"}, "type": "TELEPHONY"})       #发送通知
        self.app.tv_send_notification({"appMessage": {"appId": "app.facebook", "text": "ryeex text", "title": "ryeex title"}, "type": "APP_MESSAGE"})
        self.app.tv_send_notification({"sms": {"contact": "ryeex contact", "content": "ryeex content", "sender": "1234567"}, "type": "SMS"})

        self.app.tv_set_app_list("2,3,5,6,7,8,11,12,13,14,15")                                                                                     #设置应用排序
        self.app.tv_app_list("2, 3, 5")                                                                                         #获取应用排序

        self.app.swpe(size['width']*0.25, size['height']*0.85, size['width']*0.25, size['height']*0.5)
        self.app.tv_setDoNotDisturb({"homeVibrate": 0, "lunchModeEnable": 0, "mode": "ALWAYS", "raiseToWake": 0})                                                                                  #设置勿扰模式
        self.app.tv_getDoNotDisturb("ALWAYS")                                                                         #获取勿扰模式
        self.app.tv_setDoNotDisturb({"homeVibrate": 0, "lunchModeEnable": 0, "mode": "DISABLE", "raiseToWake": 0})
        self.app.tv_getDoNotDisturb("DISABLE")
        self.app.tv_setDoNotDisturb({"homeVibrate": 0, "lunchModeEnable": 0, "mode": "SMART", "raiseToWake": 0})
        self.app.tv_getDoNotDisturb("SMART")
        self.app.tv_setDoNotDisturb({"durations": [{"endTimeHour": 12, "endTimeMinute": 30, "startTimeHour": 10, "startTimeMinute": 30}], "homeVibrate": 0, "lunchModeEnable": 0, "mode": "TIMING", "raiseToWake": 0})
        self.app.tv_getDoNotDisturb("TIMING")

        self.app.tv_setDeviceRaiseToWake({"enable": True, "endTimeHour": 10, "endTimeMinute": 00, "startTimeHour": 8, "startTimeMinute": 00})                                                                             #设置抬腕亮屏
        self.app.tv_getDeviceRaiseToWake(True)                                                                             #获取抬腕亮屏
        self.app.tv_setDeviceRaiseToWake({"enable": False})
        self.app.tv_getDeviceRaiseToWake(False)

        self.app.swpe(size['width']*0.25, size['height']*0.95, size['width']*0.25, size['height']*0.5)
        self.app.tv_setHeartRateDetect({"enable": True, "interval": 5})                                                                               #设置心率检测
        self.app.tv_getHeartRateDetect(5)                                                                               #获取心率检测
        self.app.tv_setHeartRateDetect({"enable": False})
        self.app.tv_getHeartRateDetect(False)

        self.app.tv_setDeviceBrightness("MID")                                                                        #设置屏幕亮度
        self.app.tv_getDeviceBrightness("MID")                                                                              #获取屏幕亮度
        self.app.tv_setDeviceBrightness("LOW")
        self.app.tv_getDeviceBrightness("LOW")
        self.app.tv_setDeviceBrightness("HIGH")
        self.app.tv_setDeviceBrightness("HIGH")

        self.app.tv_setHomeVibrateSetting(True)                                                                            #设置震动开关
        self.app.tv_getHomeVibrateSetting(True)                                                                            #获取震动开关
        self.app.tv_setHomeVibrateSetting(False)
        self.app.tv_getHomeVibrateSetting(False)

        self.app.tv_setUnlock(1)                                                                                        #设置解锁方式
        self.app.tv_getUnlock(1)                                                                                        #获取解锁方式
        self.app.tv_setUnlock(0)
        self.app.tv_getUnlock(0)

        self.app.swpe(size['width']*0.25, size['height']*0.25, size['width']*0.25, size['height']*0.95)
        self.app.tv_unbind()                                                                                           #解绑
        self.app.close_app()                                                                                           #关闭App


if __name__ == '__main__':
     pytest.main()
