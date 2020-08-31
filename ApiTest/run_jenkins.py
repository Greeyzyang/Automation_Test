#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/8/27 16:33
# @Author : Greey
# @FileName: run_jenkins.py


import os
import pytest


if __name__ == '__main__':
    #pytest.main()
    pytest.main(['--alluredir', 'C:/Users/EDZ/PycharmProjects/untitled/Jenkins/workspace/Api_Autotest/allure-results'])
    # os.system('allure generate C:/Users/EDZ/PycharmProjects/untitled/ApiTest/Report/xml -o C:/Users/EDZ/PycharmProjects/untitled/ApiTest/Report/html --clean')