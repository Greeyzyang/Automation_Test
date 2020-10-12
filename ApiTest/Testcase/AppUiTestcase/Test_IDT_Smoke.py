#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/9/15 17:04
# @Author : Greey
# @FileName: Test_IDT_Smoke.py



'''
测试步骤：
1：登录app
2:点击SDK所有按钮

预期结果：
1：登录app成功
2:点击SDK所有按钮成功

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
        self.app.click_prompt_box()
        size = self.driver.get_window_size()                                                                           #获取屏幕尺寸
        time.sleep(3)
        if self.app.object_exist_xpath("//android.view.ViewGroup[@index='0']") == False:
            self.app.close_app()
            self.app_setting.restart_bluetooth()                                                                       #重启蓝牙
            self.driver = self.app.open_app()
            self.app.click_prompt_box()
            if self.app.object_exist("2C:AA:8E:00:AB:95") == False:
                self.driver.keyevent(4)                                                                                #模拟返回键
                self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="解绑"]').click()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="2C:AA:8E:00:AB:95"]').click()
        time.sleep(5)
        if self.app.object_exist("绑定失败"):
            self.driver.keyevent(4)
            self.driver.keyevent(4)
            time.sleep(10)
            self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="2C:AA:8E:00:AB:95  已连接"]')
        # self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="请在设备上点击确认"]')
        # self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="绑定成功"]')
        # self.app.find_elementby(By.XPATH, '//*[@class="android.widget.Button" and @text="完成"]').click()
        self.app.click_prompt_box()
        self.app.click_prompt_box()
        self.app.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="2C:AA:8E:00:AB:95  已连接"]')
        self.app.tv_device_info()                                                                                      #设备信息
        self.app.tv_device_property()                                                                                  #设备电量
        self.app.tv_device_activity()                                                                                  #活动数据
        self.app.tv_device_data()                                                                                      #数据同步
        self.app.tv_find_device()                                                                                      #查找手环
        self.app.tv_reboot_device()                                                                                    #重启手环
        self.app.tv_send_notification("{\"telephony\":{\"contact\":\"reeyx\",\"number\":\"1234567\",\"status\":\"RINGING_UNANSWERABLE\"},\"type\":\"TELEPHONY\"}")       #发送通知
        self.app.tv_send_notification("{\"appMessage\":{\"appId\":\"app.facebook\",\"text\":\"ryeex text\",\"title\":\"ryeex title\"},\"type\":\"APP_MESSAGE\"}")
        self.app.tv_send_notification("{\"sms\":{\"contact\":\"ryeex contact\",\"content\":\"ryeex content\",\"sender\":\"1234567\"},\"type\":\"SMS\"}")

        self.app.tv_set_app_list("2,3,5,6,7,8,11,12,13,14,15")                                                                                     #设置应用排序
        self.app.tv_app_list("2, 3, 5")                                                                                         #获取应用排序

        self.app.swpe(size['width']*0.25, size['height']*0.85, size['width']*0.25, size['height']*0.5)
        self.app.tv_setDoNotDisturb("{\"homeVibrate\":0,\"lunchModeEnable\":0,\"mode\":\"ALWAYS\",\"raiseToWake\":0}")                                                                                  #设置勿扰模式
        self.app.tv_getDoNotDisturb("ALWAYS")                                                                         #获取勿扰模式
        self.app.tv_setDoNotDisturb("{\"homeVibrate\":0,\"lunchModeEnable\":0,\"mode\":\"DISABLE\",\"raiseToWake\":0}")
        self.app.tv_getDoNotDisturb("DISABLE")
        self.app.tv_setDoNotDisturb("{\"homeVibrate\":0,\"lunchModeEnable\":0,\"mode\":\"SMART\",\"raiseToWake\":0}")
        self.app.tv_getDoNotDisturb("SMART")
        self.app.tv_setDoNotDisturb("{\"durations\":[{\"endTimeHour\":12,\"endTimeMinute\":30,\"startTimeHour\":10,\"startTimeMinute\":30}],\"homeVibrate\":0,\"lunchModeEnable\":0,\"mode\":\"TIMING\",\"raiseToWake\":0}")
        self.app.tv_getDoNotDisturb("TIMING")

        self.app.tv_setDeviceRaiseToWake("{\"enable\":true,\"endTimeHour\":10,\"endTimeMinute\":00,\"startTimeHour\":8,\"startTimeMinute\":00}")                                                                             #设置抬腕亮屏
        self.app.tv_getDeviceRaiseToWake("true")                                                                             #获取抬腕亮屏
        self.app.tv_setDeviceRaiseToWake("{\"enable\":false}")
        self.app.tv_getDeviceRaiseToWake("false")

        self.app.swpe(size['width']*0.25, size['height']*0.95, size['width']*0.25, size['height']*0.5)
        self.app.tv_setHeartRateDetect("{\"enable\":true,\"interval\":5}")                                                                               #设置心率检测
        self.app.tv_getHeartRateDetect("5")                                                                               #获取心率检测
        self.app.tv_setHeartRateDetect("{\"enable\":false}")
        self.app.tv_getHeartRateDetect("false")

        self.app.tv_setDeviceBrightness("MID")                                                                        #设置屏幕亮度
        self.app.tv_getDeviceBrightness("MID")                                                                              #获取屏幕亮度
        self.app.tv_setDeviceBrightness("LOW")
        self.app.tv_getDeviceBrightness("LOW")
        self.app.tv_setDeviceBrightness("HIGH")
        self.app.tv_setDeviceBrightness("HIGH")

        self.app.tv_setHomeVibrateSetting("true")                                                                            #设置震动开关
        self.app.tv_getHomeVibrateSetting("true")                                                                            #获取震动开关
        self.app.tv_setHomeVibrateSetting("false")
        self.app.tv_getHomeVibrateSetting("false")

        self.app.tv_setUnlock("1")                                                                                        #设置解锁方式
        self.app.tv_getUnlock("1")                                                                                        #获取解锁方式
        self.app.tv_setUnlock("0")
        self.app.tv_getUnlock("0")

        self.app.swpe(size['width']*0.25, size['height']*0.25, size['width']*0.25, size['height']*0.95)
        self.app.tv_unbind()                                                                                           #解绑
        self.app.close_app()                                                                                           #关闭App


if __name__ == '__main__':
     pytest.main()
