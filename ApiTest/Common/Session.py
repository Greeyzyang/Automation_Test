#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/8/18 14:02
# @Author : Greey
# @FileName: Session.py


"""
封装获取cookie方法
"""

import requests
import Log
from Config import ReadConfig
import os
import json
import urllib3
import time
import hashlib
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

CIPHERS = (
        'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
        'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
        '!eNULL:!MD5'
    )

class DESAdapter(HTTPAdapter):
    """
    A TransportAdapter that re-enables 3DES support in Requests.
    """

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)

class Session(object):
    def __init__(self):
        current_path = os.path.abspath(__file__)            # 获取当前文件路径
        father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")      # 获取当前文件的祖父目录
        config_path = father_path + "\\" + "Config\Config.ini"
        config_path = config_path.replace("\\", "/")
        self.config = ReadConfig(config_path)
        self.log = Log.MyLog()
        urllib3.disable_warnings()                              #忽略提示证书验证异常信息
    def get_platfolm_session(self, env1):
        """
        获取session
        :param env1: Platfolm环境变量
        :return:
        """
        headers = {
            "User-Agent": "okhttp/4.7.2",
            "Content-Type": "application/json; charset=utf-8",
            "Accept-Encoding": "gzip"
        }

        if env1 == "Platfolm_Alpha":
            login_host = self.config.get_value("Platfolm_Alpha", "host")
            login_url = self.config.get_value("Platfolm_Alpha", "url")
            user_name = self.config.get_value("Platfolm_Alpha", "user_name")
            password = self.config.get_value("Platfolm_Alpha", "password")
            phone_system_type = self.config.get_value("Platfolm_Alpha", "phone_system_type")
            phone_id = self.config.get_value("General_variable", "phone_id")
            sc = self.config.get_value("Platfolm_Alpha", "sc")
            sv = self.config.get_value("Platfolm_Alpha", "sv")
            app_name = self.config.get_value("General_variable", "app_name")
            app_ver = self.config.get_value("General_variable", "app_ver")
            app_version = self.config.get_value("General_variable", "app_version")
            parm = {}
            parm['access_token'] = ""
            parm['app_name'] = app_name
            parm['app_ver'] = app_ver
            parm['app_version'] = app_version
            parm['password'] = password
            parm['phone_id'] = phone_id
            parm['phone_system_type'] = phone_system_type
            parm['sc'] = sc
            parm['sv'] = sv
            ttime = time.time()
            parm['ts'] = int(round(ttime * 1000))                             #模拟时间戳13位
            parm['user_name'] = user_name
            parm['user_name'] = user_name
            login_host = login_host.encode('utf-8')
            login_url = login_url.encode('utf-8')
            new_url = login_host + login_url
            parm = json.dumps(parm)
            session_platfolm_alpha = requests.session()
            respones = session_platfolm_alpha.post(new_url, parm, headers=headers, verify=False)                       #verify=False,解决SSL 根证书验错误
            print(respones.status_code)
            print(respones.content)
            r = json.loads(respones.content)
            self.log.debug('platfolm_cookies: %s' % r['data']['access_token'])
            return r['data']['access_token']
        elif env1 == "Platfolm_Beta":
            login_host = self.config.get_value("Platfolm_Beta", "host")
            login_url = self.config.get_value("Platfolm_Beta", "url")
            user_name = self.config.get_value("Platfolm_Beta", "user_name")
            password = self.config.get_value("Platfolm_Beta", "password")
            phone_system_type = self.config.get_value("Platfolm_Beta", "phone_system_type")
            phone_id = self.config.get_value("General_variable", "phone_id")
            sc = self.config.get_value("Platfolm_Beta", "sc")
            sv = self.config.get_value("Platfolm_Beta", "sv")
            #ts = self.config.get_value("Platfolm_Beta", "ts")
            app_name = self.config.get_value("General_variable", "app_name")
            app_ver = self.config.get_value("General_variable", "app_ver")
            app_version = self.config.get_value("General_variable", "app_version")
            parm = {}                                                           #新建一个数据字典
            parm['access_token'] = ""
            parm['app_name'] = app_name
            parm['app_ver'] = app_ver
            parm['app_version'] = app_version
            parm['password'] = password
            parm['phone_id'] = phone_id
            parm['phone_system_type'] = phone_system_type
            parm['sc'] = sc
            parm['sv'] = sv
            ttime = time.time()
            parm['ts'] = int(round(ttime * 1000))                               #模拟时间戳13位
            parm['user_name'] = user_name
            login_host = login_host.encode('utf-8')                             #将unicode类型转换为字符串类型
            login_url = login_url.encode('utf-8')
            new_url = login_host + login_url
            parm = json.dumps(parm)
            session_platfolm_beta = requests.session()
            respones = session_platfolm_beta.post(new_url, parm, headers=headers, verify=False)
            print(respones.status_code)
            print(respones.content)
            r = json.loads(respones.content)                                          #将字符串类型转换为字典类型
            self.log.debug('platfolm_cookies: %s' % r['data']['access_token'])
            return r['data']['access_token']

        else:
            self.log.error(u'不存在当前环境信息，请检查')
    def get_wristband_session(self, env2):
        """
        获取session
        :param env2: Wristband环境变量
        :return:
        """
        headers = {
            "User-Agent": "okhttp/4.7.2",
            "Content-Type": "application/json; charset=utf-8",
            "Accept-Encoding": "gzip"
        }

        if env2 == "Wristband_Alpha":
            login_host = self.config.get_value("Wristband_Alpha", "host")
            login_url = self.config.get_value("Wristband_Alpha", "url")
            phoneid = self.config.get_value("General_variable", "phone_id")
            appinfo = self.config.get_value("Wristband_Alpha", "appinfo")
            apikey = self.config.get_value("Wristband_Alpha", "apikey")
            #userinfo_url = self.config.get_value("Wristband_Alpha", "userinfo_url")
            parm = {}
            wristband_header = {}
            wristband_header['access_token'] = Session().get_platfolm_session("Platfolm_Alpha")
            wristband_header['phoneid'] = phoneid
            wristband_header['appinfo'] = appinfo
            wristband_header['requestid'] = hashlib.md5(str(time.clock()).encode('utf-8')).hexdigest()              #模拟唯一的request id
            wristband_header['apikey'] = apikey
            login_host = login_host.encode('utf-8')
            login_url = login_url.encode('utf-8')
            #userinfo_url = userinfo_url.encode('utf-8')
            new_url = login_host + login_url
            #new_userinfo_url = login_host + userinfo_url
            wristband_header = json.dumps(wristband_header)
            wristband_header = eval(wristband_header)
            new_header = dict(wristband_header, **headers)                                                             #合并2个字典组成一个新的header
            session_wristband_alpha = requests.session()
            session_wristband_alpha.mount(login_host, DESAdapter())                                                    #解决出现ssl.c661的问题
            respones = session_wristband_alpha.post(new_url, parm, headers=new_header, verify=False)                   #verify=False,解决SSL 根证书验错误
            print(respones.status_code)
            print(respones.content)
            r = eval(respones.content)
            self.log.debug('wristband_cookies: %s' % r['data']['rst'])
            return r['data']['rst'], new_header

        elif env2 == "Wristband_Beta":
            login_host = self.config.get_value("Wristband_Beta", "host")
            login_url = self.config.get_value("Wristband_Beta", "url")
            phoneid = self.config.get_value("General_variable", "phone_id")
            appinfo = self.config.get_value("Wristband_Beta", "appinfo")
            apikey = self.config.get_value("Wristband_Beta", "apikey")
            #appid = self.config.get_value("Wristband_Beta", "appid")
            #userinfo_url = self.config.get_value("Wristband_Beta", "userinfo_url")
            parm = {}
            wristband_header = {}
            wristband_header['access_token'] = Session().get_platfolm_session("Platfolm_Beta")
            wristband_header['access_token'] = wristband_header['access_token'].decode("utf-8")                    #将unicode类型转换为str类型
            wristband_header['phoneid'] = phoneid
            wristband_header['appinfo'] = appinfo
            wristband_header['requestid'] = hashlib.md5(str(time.clock()).encode('utf-8')).hexdigest()              #模拟唯一的request id
            wristband_header['apikey'] = apikey
            #wristband_header['appid'] = appid
            login_host = login_host.encode('utf-8')
            login_url = login_url.encode('utf-8')
            #userinfo_url = userinfo_url.encode('utf-8')
            new_url = login_host + login_url
            #new_userinfo_url = login_host + userinfo_url
            wristband_header = json.dumps(wristband_header)
            wristband_header = eval(wristband_header)                                                                  #将字符串转换为字典
            new_header = dict(wristband_header, **headers)                                                             #合并2个字典组成一个新的header
            session_wristband_beta = requests.session()
            session_wristband_beta.mount(login_host, DESAdapter())
            #session_wristband_beta.post(new_userinfo_url, parm, headers=new_header, verify=False)                      # /app/v2/wristband/user_info
            respones = session_wristband_beta.post(new_url, parm, headers=new_header, verify=False)                    #verify=False,解决SSL 根证书验错误
            print(respones.status_code)
            print(respones.content)
            r = eval(respones.content)
            self.log.debug('wristband_cookies: %s' % r['data']['rst'])
            return r['data']['rst'], new_header
        else:
            self.log.error(u'不存在当前环境信息，请检查')

if __name__ == '__main__':
    # A = Session().get_platfolm_session('Platfolm_Alpha')
    A = Session().get_wristband_session('Wristband_Alpha')
    print(A)
