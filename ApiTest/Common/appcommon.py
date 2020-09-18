#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/9/12 17:12
# @Author : Greey
# @FileName: Appcommon.py

from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
import Log
from selenium.webdriver.common.by import By
import time
import allure


class App(object):

    # 初始化设备参数
    def __init__(self, desired_caps):
        self.desired_caps = desired_caps
        self.log = Log.MyLog()

    @allure.step("打开app")
    def open_app(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        return self.driver

    #不同的driver
    @allure.step("打开Setting")
    def open_setting(self):
        self.driver2 = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        return self.driver2

    @allure.step("结束app进程")
    def close_app(self):
        self.driver.quit()


    @allure.step("结束setting进程")
    def close_setting(self):
        self.driver2.quit()

    # @allure.step("截图")
    # def get_screenshot(self, file_path):
    #     sleep(5)
    #     self.file_path = file_path
    #     if (os.path.exists(self.file_path) == False):                                       # 判断路径是否存在
    #         os.makedirs(self.file_path)
    #     now = time.strftime('%Y-%m-%d %H_%M_%S')
    #     filename = self.file_path + '\\' + now + '.png'
    #     self.driver.get_screenshot_as_file(filename)
    #     self.fp = open(filename, 'rb').read()
    #     return self.fp

    # 重写元素定位方法
    def find_elementby(self, *loc):
        try:
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element(*loc).is_displayed())             #隐式等待
            sleep(0.5)
            return self.driver.find_element(*loc)
        except:
            self.log.error(u"%s 未能找到 %s 元素" % loc)
            return False

    # 重写元素定位方法（不同的driver）
    def find_elementby2(self, *loc):
        try:
            WebDriverWait(self.driver2, 10).until(lambda driver: driver.find_element(*loc).is_displayed())            #隐式等待
            sleep(0.5)
            return self.driver2.find_element(*loc)
        except:
            self.log.error(u"%s 未能找到 %s 元素" % loc)
            return False

    def swpe(self, start_x, start_y, end_x, end_y):
        '''
        - start_x - 开始滑动的x坐标
        - start_y - 开始滑动的y坐标
        - end_x - 结束点x坐标
        - end_y - 结束点y坐标
        - duration - 持续时间，单位毫秒
        '''
        self.driver.swipe(start_x, start_y, end_x, end_y, 1000)
        time.sleep(5)
        # for i in range(2):    ###增加滑动次数，因为有时滑动不明显。这一步很有效果。2可以是更改的，如果滑动的少，可以增加滑动次数的。
        #     time.sleep(5)
        #     self.driver.swipe(start_x, start_y, end_x, end_y, 1000)

    def assert_in_text(self, expecttext='BleError', loc="//*[@class='android.widget.TextView' and @resource-id='com.ryeex.sdk.demo:id/tv_result']"):
        time.sleep(1)
        text = self.driver.find_element_by_xpath(loc).text
        try:
            assert str(expecttext) not in str(text)
        except:
            self.log.error(u'App页面Response验证失败%s' % text)
            raise

    def object_exist(self, text):
        loc = '//*[@text="' + text + '"]'''
        flag = True
        try:
            WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element(By.XPATH, loc).is_displayed())
            return flag
        except:
            flag = False
            return flag

    #重启蓝牙
    def restart_bluetooth(self):
        A = App(self.desired_caps)
        self.driver2 = A.open_setting()
        time.sleep(1)
        self.find_elementby2(By.XPATH, '//android.widget.TextView[@text="蓝牙"]').click()
        time.sleep(1)
        self.find_elementby2(By.XPATH, '//android.widget.TextView[@text="蓝牙"]').click()
        time.sleep(1)
        self.find_elementby2(By.XPATH, '//*[@class="android.widget.Switch" and @resource-id="com.android.settings:id/switch_widget"]').click()
        time.sleep(1)
        self.find_elementby2(By.XPATH, '//*[@class="android.widget.Switch" and @resource-id="com.android.settings:id/switch_widget"]').click()
        # self.driver2.keyevent(3)                                                                                       #模拟home键
        self.close_setting()

###-------------------------------------------------------------------业务脚本----------------------------------------------------------------------###

    @allure.step("忽略提示框")
    def click_prompt_box(self):
        if self.object_exist("总是允许") == True:
            self.find_elementby(By.XPATH, '//*[@text="不再询问"]').click()
            self.find_elementby(By.XPATH, '//*[@text="总是允许"]').click()

    @allure.step("设备信息")
    def tv_device_info(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设备信息"]').click()
        self.assert_in_text()

    @allure.step("设备电量")
    def tv_device_property(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设备电量"]').click()
        self.assert_in_text()

    @allure.step("活动数据")
    def tv_device_activity(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="活动数据"]').click()
        self.assert_in_text()

    @allure.step("数据同步")
    def tv_device_data(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="数据同步"]').click()
        self.assert_in_text()

    @allure.step("查找手环")
    def tv_find_device(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="查找手环"]').click()
        time.sleep(5)
        self.assert_in_text()

    @allure.step("重启手环")
    def tv_reboot_device(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="重启手环"]').click()
        time.sleep(15)
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="2C:AA:8E:00:AB:95  已连接"]')
        self.assert_in_text()

    @allure.step("发送通知")
    def tv_send_notification(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="发送通知"]').click()
        self.assert_in_text()

    @allure.step("获取应用排序")
    def tv_app_list(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="获取应用排序"]').click()
        self.assert_in_text()

    @allure.step("设置应用排序")
    def tv_set_app_list(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设置应用排序"]').click()
        self.assert_in_text()

    @allure.step("获取勿扰模式")
    def tv_getDoNotDisturb(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="获取勿扰模式"]').click()
        self.assert_in_text()

    @allure.step("设置勿扰模式")
    def tv_setDoNotDisturb(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设置勿扰模式"]').click()
        self.assert_in_text()

    @allure.step("获取抬腕亮屏")
    def tv_getDeviceRaiseToWake(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="获取抬腕亮屏"]').click()
        self.assert_in_text()

    @allure.step("设置抬腕亮屏")
    def tv_setDeviceRaiseToWake(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设置抬腕亮屏"]').click()
        self.assert_in_text()

    @allure.step("获取心率检测")
    def tv_getHeartRateDetect(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="获取心率检测"]').click()
        self.assert_in_text()

    @allure.step("设置心率检测")
    def tv_setHeartRateDetect(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设置心率检测"]').click()
        self.assert_in_text()

    @allure.step("获取屏幕亮度")
    def tv_getDeviceBrightness(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="获取屏幕亮度"]').click()
        self.assert_in_text()

    @allure.step("设置屏幕亮度")
    def tv_setDeviceBrightness(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设置屏幕亮度"]').click()
        self.assert_in_text()

    @allure.step("获取震动开关")
    def tv_getHomeVibrateSetting(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="获取震动开关"]').click()
        self.assert_in_text()

    @allure.step("设置震动开关")
    def tv_setHomeVibrateSetting(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设置震动开关"]').click()
        self.assert_in_text()

    @allure.step("设置解锁方式")
    def tv_setUnlock(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="设置解锁方式"]').click()
        self.assert_in_text()

    @allure.step("获取解锁方式")
    def tv_getUnlock(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="获取解锁方式"]').click()
        self.assert_in_text()

    @allure.step("解绑")
    def tv_unbind(self):
        self.find_elementby(By.XPATH, '//*[@class="android.widget.TextView" and @text="解绑"]').click()