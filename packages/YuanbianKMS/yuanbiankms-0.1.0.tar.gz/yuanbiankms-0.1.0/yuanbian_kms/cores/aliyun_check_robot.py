# -*- coding=utf-8 -*-
# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List
from flask import current_app
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_captcha20230305.client import Client as Captcha20230305Client
from alibabacloud_captcha20230305 import models as captcha_20230305_models


class AliyunCaptchaRequest:
    client = None
    def __init__(self):
        config = open_api_models.Config()
        # 设置请求地址 国内调用地址 captcha.cn-shanghai.aliyuncs.com
        # 新加坡调用地址 captcha.ap-southeast-1.aliyuncs.com
        config.endpoint = 'captcha.cn-shanghai.aliyuncs.com'
        # 设置连接超时为5000毫秒
        config.connect_timeout = 5000
        # 设置读超时为5000毫秒
        config.read_timeout = 5000
        #  ======================
        self.config = config


    def init_app(self, app):
        self.config.access_key_id = app.config.get('ACCESS_KEY_ID')
        self.config.access_key_secret = app.config.get('ACCESS_KEY_SECRET')
        self.client = Captcha20230305Client(self.config)
    def request(self, scene_id, captcha_verify_param):
        captcha_verify_code = "认证服务器故障"
        # 创建APi请求
        request = captcha_20230305_models.VerifyIntelligentCaptchaRequest()
        # 本次验证的场景ID，建议传入，防止前端被篡改场景
        request.scene_id = scene_id
        # 前端传来的验证参数 CaptchaVerifyParam
        request.captcha_verify_param = captcha_verify_param
        # ====================== 3. 发起请求） ======================\
        try:
            resp = self.client.verify_intelligent_captcha(request)
            # 建议使用您系统中的日志组件，打印返回
            # 获取验证码验证结果（请注意判空），将结果返回给前端。
            captcha_verify_result = resp.body.result.verify_result
            # 原因code
            captcha_verify_code = resp.body.result.verify_code
        except Exception as error:
            current_app.logger.error(error)
            # 建议使用您系统中的日志组件，打印异常
            # 出现异常建议认为验证通过，优先保证业务可用，然后尽快排查异常原因。
            captcha_verify_result = True
        return {"captcha_verify_result": captcha_verify_result,
                "captcha_verify_code": captcha_verify_code }



if __name__ == '__main__':
    pass