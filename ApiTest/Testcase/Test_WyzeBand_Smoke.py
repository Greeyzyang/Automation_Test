#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/8/31 16:18
# @Author : Greey
# @FileName: Test_WyzeBand_Smoke.py



'''
测试步骤：
1：登录app（https://test-api.wyzecam.com/app/user/login）
2：生成手环token（https://test-wristband-service.wyzecam.com/app/v2/wristband/generate_token）
3：绑定手环（https://test-wristband-service.wyzecam.com//app/v2/wristband/bind_device）

预期结果：
1：登录app成功
2：成功生成token
3：绑定手环成功
'''