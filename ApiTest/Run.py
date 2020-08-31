# -*- coding: utf-8 -*-
# @Time : 2020/8/18 10:05
# @Author : Greey
# @FileName: Run.py

import os
import win32com.client
from ApiTest.Common.Log import MyLog
import pytest

# C = ReadConfig()
# on_off = C.get_configdata("EMAIL", "on_off")

def check_exsit(process_name):                                                                                        #判断某个进程是否存在
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
    if len(processCodeCov) > 0:
        os.system('TASKKILL /F /IM "%s"' % process_name)
        print '%s is exists' % process_name
    else:
        print '%s is not exists' % process_name

class AllTest(object):

    def __init__(self):
        global on_off
        self.log = MyLog()
        check_exsit("java.exe")
        # current_path = os.path.abspath(__file__)
        # father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
        # report_path = father_path + "\\" + "Config\Config.ini"
        # self.report_path = report_path.replace("\\", "/")
    def run(self):
        try:
            self.log.info("********TEST START** ******")
            pytest.main()
            # pytest.main(['--alluredir', 'C:/Users/EDZ/PycharmProjects/untitled/ApiTest/Report/xml'])
            # os.system('allure generate C:/Users/EDZ/PycharmProjects/untitled/ApiTest/Report/xml -o C:/Users/EDZ/PycharmProjects/untitled/ApiTest/Report/html --clean')                 #将报告转换成HTML
        except:
            self.log.error(u'测试用例执行失败，请检查')
        # finally:
        #     self.log.info("*********TEST END*********")
        #     # send test report by email
        #     if on_off == u'on':
        #         configEmail.MyEmail()
        #
        #
        #
        #     elif on_off == u'off':
        #         self.logger.info("Doesn't send report email to developer.")
        #     else:
        #         self.logger.info("Unknow state.")


if __name__ == '__main__':
    AllTest().run()






