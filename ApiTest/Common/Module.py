#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/8/25 17:39
# @Author : Greey
# @FileName: Module.py



import os
import sys
import datetime
import allure
from ApiTest.Common.Config import ReadConfig
from ApiTest.Common.Readyaml import Yamlc
from ApiTest.Common.Request import Request
from ApiTest.Common.Log import MyLog
from ApiTest.Common.Assert import Assertions
from ApiTest.Common.Session import Session


"""
封装业务功能，类似UI自动化page object设计模式
*******************************************************
Allure中对严重级别的定义：
blocker级别：中断缺陷（客户端程序无响应，无法执行下一步操作）
critical级别：临界缺陷（ 功能点缺失）
normal级别：普通缺陷（数值计算错误）
minor级别：次要缺陷（界面错误与UI需求不符）
trivial级别：轻微缺陷（必输项无提示，或者提示不规范）
*******************************************************
"""

class Moudle(object):

    def __init__(self, env2):
        current_path = os.path.abspath(__file__)                                                # 获取当前文件路径
        father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")      # 获取当前文件的祖父目录
        config_path = father_path + "\\" + "Config\Config.ini"
        config_path = config_path.replace("\\", "/")
        self.file_path = father_path + "\\" + "Testdata\\space_flight.png"
        self.config = ReadConfig(config_path)
        self.log = MyLog()
        # env2 = "Wristband_Alpha"
        self.host = self.config.get_value(env2, "host")
        firmware_ver = self.config.get_value(env2, "firmware_ver")
        self.Returndata = Session().get_wristband_session(env2)
        # self.method = "post"
        self.headers = self.Returndata[1]
        self.headers['firmware_ver'] = firmware_ver                                                                   #生成token值之后'firmware_ver'字段获取设备的'version'值

    @allure.step("获取设备Token成功（不传参）")
    def get_token(self):
        self.get_token_url = self.host + "/app/v2/wristband/get_token"
        self.get_token_parm = {"tz": "Asia/Shanghai"}
        rdict = Request().post_wirst_request(method="post", url=self.get_token_url, data=self.get_token_parm, header=self.headers)
        Assertions().assert_code(rdict['status_code'], 200)

    @allure.step("获取设备Token成功（传参）")
    def get_token_data(self):
        self.get_token_url = self.host + "/app/v2/wristband/get_token"
        self.get_token_parm = {"tz": "Asia/Shanghai",  "did": "RY.HP1.418337"}
        rdict = Request().post_wirst_request(method="post", url=self.get_token_url, data=self.get_token_parm, header=self.headers)
        Assertions().assert_code(rdict['status_code'], 200)

    @allure.step("获取用户信息成功")
    def user_info(self):
        self.user_info_url = self.host + "/app/v2/wristband/user_info"
        self.user_info_parm = {"tz": "Asia/Shanghai"}
        rdict = Request().post_wirst_request(method="post", url=self.user_info_url, data=self.user_info_parm, header=self.headers)
        Assertions().assert_code(rdict['status_code'], 200)
        return rdict['data']['uid']

    @allure.step("生成手环token，绑定手环成功")
    def bind(self):
        self.bind_url = self.host + "/app/v3/user/bind"
        self.bind_parm = {
            "tz": "Asia/Shanghai",
            "did": "RY.HP1.418337",
            "mac": "2C:AA:8E:00:AB:95",
            "nonce": 141361162,
            "sn": 144,
            "sign": "AAAAAAAAAAAAAAAAAAAAAJemS1kss+AgcguKwa1M51aWLi9xnWNAKOeX7rCTosjR",
            "sign_version": 2,
            "device_token": self.Returndata[0],
            "model": "RY.HP1"
        }
        r = Request().post_wirst_request(method="post", url=self.bind_url, data=self.bind_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)
        self.device_token = self.bind_parm['device_token']
        return self.device_token, self.headers

    @allure.step("设置默认连接的key成功")
    def set_defaultconn(self):
        self.set_defaultconn_url = self.host + "/app/v2/wristband/set_defaultconn"
        self.set_defaultconn_parm = {"tz": "Asia/Shanghai", "mac": "2C:AA:8E:00:AB:95", "keyid": "ab6aa7f445393ffb"}
        r = Request().post_wirst_request(method="post", url=self.set_defaultconn_url, data=self.set_defaultconn_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("获取设备对应的默认自动连接设置成功")
    def get_defaultconn(self):
        self.get_defaultconn_url = self.host + "/app/v2/wristband/get_defaultconn"
        self.get_defaultconn_parm = {"tz": "Asia/Shanghai", "mac": "2C:AA:8E:00:AB:95"}
        r = Request().post_wirst_request(method="post", url=self.get_defaultconn_url, data=self.get_defaultconn_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("获取版本对应的功能列表（不包括基础功能）成功")
    def get_functions(self):
        self.get_functions_url = self.host + "/app/v2/wristband/get_functions"
        self.get_functions_parm = {"tz": "Asia/Shanghai", "version": "2.12.0"}
        r = Request().post_wirst_request(method="post", url=self.get_functions_url, data=self.get_functions_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("上传数据成功")
    def data_upload(self):
        self.data_upload_url = self.host + "/app/v2/wristband/data_upload"
        self.data_upload_parm = {
            "tz": "Asia/Shanghai",
            "data": ["Cg1SWS5IUDEuNDE4MzM3Eg0IARIJCHyIAYCc7cgBEi4IARIqCAIaIwoeCPbisvoFELXvsvoFIAAoADAAOABAAEgAUIDhAVgAoAEAiAEA"],
            "tz": "Asia\/Shanghai"
        }
        r = Request().post_wirst_request(method="post", url=self.data_upload_url, data=self.data_upload_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("获取睡眠数据成功")
    def get_sleep(self):
        self.get_sleep_url = self.host + "/app/v2/wristband/get_sleep"
        start_time = datetime.datetime.now().strftime("%Y-%m-%d")
        end_time = (datetime.datetime.now() + datetime.timedelta(days=6)).strftime("%Y-%m-%d")
        self.get_sleep_parm = {
            "tz": "Asia/Shanghai",
            "type": "multiday",
	        "start": start_time,
	        "end": end_time,
	        "tz": "Asia\/Shanghai"
        }
        r = Request().post_wirst_request(method="post", url=self.get_sleep_url, data=self.get_sleep_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("获取步数统计数据成功")
    def get_step(self):
        self.get_step_url = self.host + "/app/v2/wristband/get_step"
        start_time = datetime.datetime.now().strftime("%Y-%m-%d")
        end_time = (datetime.datetime.now() + datetime.timedelta(days=6)).strftime("%Y-%m-%d")
        self.get_step_parm = {
            "tz": "Asia/Shanghai",
            "type": "multiday",
	        "start": start_time,
	        "end": end_time,
	        "tz": "Asia\/Shanghai"
        }
        r = Request().post_wirst_request(method="post", url=self.get_step_url, data=self.get_step_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("获取心率统计数据成功")
    def get_heart_rate(self):
        self.get_heart_rate_url = self.host + "/app/v2/wristband/get_heart_rate"
        start_time = datetime.datetime.now().strftime("%Y-%m-%d")
        end_time = (datetime.datetime.now() + datetime.timedelta(days=6)).strftime("%Y-%m-%d")
        self.get_heart_rate_parm = {
            "tz": "Asia/Shanghai",
            "type": "multiday",
	        "start": start_time,
	        "end": end_time,
	        "tz": "Asia\/Shanghai"
        }
        r = Request().post_wirst_request(method="post", url=self.get_heart_rate_url, data=self.get_heart_rate_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("获取运动历史成功")
    def get_sport_history(self):
        self.get_sport_history_url = self.host + "/app/v2/wristband/get_sport_history"
        self.get_sport_history_parm = {
            "tz": "Asia/Shanghai",
	        "skip": 0,
	        "limit": 50,
	        "tz": "Asia\/Shanghai"
        }
        r = Request().post_wirst_request(method="post", url=self.get_sport_history_url, data=self.get_sport_history_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("获取某天的心率成功")
    def get_heart_rate_history(self):
        self.get_heart_rate_history_url = self.host + "/app/v2/wristband/get_heart_rate_history"
        start_time = datetime.datetime.now().strftime("%Y-%m-%d")
        self.get_heart_rate_history_parm = {
	        "date": start_time,
	        "tz": "Asia\/Shanghai"
        }
        r = Request().post_wirst_request(method="post", url=self.get_heart_rate_history_url, data=self.get_heart_rate_history_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("获取手环背景图成功")
    def get_band_bg_list(self):
        self.get_band_bg_list_url = self.host + "/app/v2/wristband/get_band_bg_list?tz=Asia%2FShanghai"
        self.get_band_bg_list_parm = {}
        r = Request().get_wirst_request(method="get", url=self.get_band_bg_list_url, data=self.get_band_bg_list_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("上传手环背景图成功")
    def upload_band_bg(self):
        new_headers = self.headers.copy()
        new_headers['Content-Type'] = 'multipart/form-data; boundary=abbe3833-66e4-4845-a44d-5c9bbeb27c6f'
        self.upload_band_bg_url = self.host + "/app/v2/wristband/upload_band_bg"
        # file_path = 'C://Users//EDZ//PycharmProjects//untitled//ApiTest//Testdata//space_flight.png'
        self.upload_band_bg_parm = {'pic_id': (None, 'o_7'),
                                    'file_path': ('space_flight.png', open(self.file_path, 'rb'), 'image/png')
                                    }
        r = Request().post_wirst_request(method="post", url=self.upload_band_bg_url, data=self.upload_band_bg_parm, header=new_headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("用户打点数据上报成功")
    def upload_taglog(self):
        self.upload_taglog_url = self.host + "/app/v3/upload/taglog"
        self.upload_taglog_parm = {
	        "tz": "Asia/Shanghai",
	        "datas": "CoMCCoACCiEKCE9QUE8gUjExEgE5GhBhYjZhYTdmNDQ1MzkzZmZiIAAySwpJCAgSLgoRMkM6QUE6OEU6MDA6QUI6OTUSDVJZLkhQMS40MTgzMzcaCDEuMC43Ljc5IgAaFQiijL36BRINQXNpYS9TaGFuZ2hhaTpBCj8KJgoRMkM6QUE6OEU6MDA6QUI6OTUSDVJZLkhQMS40MTgzMzcaACIAEhUImIy9+gUSDUFzaWEvU2hhbmdoYWlCSwpJCAYSLgoRMkM6QUE6OEU6MDA6QUI6OTUSDVJZLkhQMS40MTgzMzcaCDEuMC43Ljc5IgAaFQimjL36BRINQXNpYS9TaGFuZ2hhaQ=="
}
        r = Request().post_wirst_request(method="post", url=self.upload_taglog_url, data=self.upload_taglog_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)

    @allure.step("解除绑定手环成功")
    def unbind(self):
        self.unbind_url = self.host + "/app/v3/user/unbind"
        self.unbind_parm = {
	        "tz": "Asia/Shanghai",
            "did": "RY.HP1.418337",
            "device_token": self.device_token
}
        r = Request().post_wirst_request(method="post", url=self.unbind_url, data=self.unbind_parm, header=self.headers)
        Assertions().assert_code(r['status_code'], 200)



if __name__ == '__main__':
    A = Moudle("Wristband_Alpha")
    A.bind()
    A.upload_band_bg()



