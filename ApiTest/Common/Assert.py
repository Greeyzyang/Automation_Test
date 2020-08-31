#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/8/19 11:37
# @Author : Greey
# @FileName: Assert.py
"""
封装Assert方法
"""
import Log
import json

class Assertions(object):
    def __init__(self):
        self.log = Log.MyLog()

    def assert_code(self, code, expected_code):
        """
        验证response状态码
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert str(code)== str(expected_code)
            return True
        except:
            self.log.error(u'response状态码验证失败，预期结果为%s,实际结果为%s' %(expected_code, code))
            raise

    def assert_body(self, body, body_msg, expected_msg):
        """
        验证response body中任意属性的值
        :param body:响应内容
        :param body_msg: 键
        :param expected_msg:
        :return:
        """
        try:
            msg = body[body_msg]
            assert msg == expected_msg
            return True
        except:
            self.log.error(u'Response验证失败，预期结果为%s，实际结果为%s' % (expected_msg, body_msg))
            raise

    def assert_in_text(self, body, expected_msg):
        """
        验证response body中是否包含预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            text = json.dumps(body, ensure_ascii=False)
            assert expected_msg in text
            return True
        except:
            self.log.error("Response没有包含%s" % expected_msg)
            raise

    def assert_text(self, body, expected_msg):
        """
        验证response body中是否等于预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            assert body == expected_msg
            return True
        except:
            self.log.error(u'Response验证失败，预期字符串为%s，实际字符串为%s' % (expected_msg, body))
            raise

    def assert_time(self, time, expected_time):
        """
        验证response body响应时间小于预期最大响应时间,单位：毫秒
        :param time:Response Time
        :param expected_time:
        :return:Null
        """
        try:
            assert str(time) < str(expected_time)
            return True
        except:
            self.log.debug(u'response时间大于预期响应时间，实际响应时间为%s，预期响应时间为%s,建议优化' % (expected_time, time))
            raise


# if __name__ =="__main__":
#     Assertions().assert_code(200, 401)



