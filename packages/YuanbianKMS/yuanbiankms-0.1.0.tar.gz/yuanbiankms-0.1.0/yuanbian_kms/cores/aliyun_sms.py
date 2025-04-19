# -*- coding=utf-8 -*-
import sys

from typing import List

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient


class YuanbianSMS:
    client = None

    def __init__(self, access_key_id, access_key_secret):
        self.create_client(access_key_id, access_key_secret)

    def create_client(self,
                      access_key_id: str,
                      access_key_secret: str,
                      ) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'dysmsapi.aliyuncs.com'
        self.client = Dysmsapi20170525Client(config)


    def create_client_with_sts(
            self,
            access_key_id: str,
            access_key_secret: str,
            security_token: str,
    ) -> Dysmsapi20170525Client:
        """
        使用STS鉴权方式初始化账号Client，推荐此方式。本示例默认使用AK&SK方式。
        @param access_key_id:
        @param access_key_secret:
        @param security_token:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret,
            # 必填，您的 Security Token,
            security_token=security_token,
            # 必填，表明使用 STS 方式,
            type='sts'
        )
        # 访问的域名
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    def main(self,
             *args: List[str],
             ) -> None:
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name=args[0],
            template_code=args[1],
            phone_numbers=args[2],
            template_param=args[3]
        )
        runtime = util_models.RuntimeOptions()
        resp = self.client.send_sms_with_options(send_sms_request, runtime)
        ConsoleClient.log(UtilClient.to_jsonstring(resp))


    async def main_async(
            self,
            *args: List[str],
    ) -> None:
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name=args[0],
            template_code=args[1],
            phone_numbers=args[2],
            template_param=args[3]
        )
        runtime = util_models.RuntimeOptions()
        resp = await self.client.send_sms_with_options_async(send_sms_request, runtime)
        ConsoleClient.log(UtilClient.to_jsonstring(resp))


if __name__ == '__main__':
    sign_name = "猿变实验室"
    template_code = "SMS_276382202"
    phone_numbers = "18912798378"
    template_param = '{"code": "111111"}'
    yuanbian_sms_service = YuanbianSMS("LTAI5tLcfPx9Jbfvy1pRHH9t", "QeKAWmFMxvadIHFRNykYNPZF4SPxZW")
    yuanbian_sms_service.main(sign_name, template_code, phone_numbers, template_param)
