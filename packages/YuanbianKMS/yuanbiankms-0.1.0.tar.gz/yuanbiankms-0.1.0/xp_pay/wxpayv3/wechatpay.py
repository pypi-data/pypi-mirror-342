# -*- coding=utf-8 -*-
import os
import requests
import json
from datetime import datetime, timezone
from .utils import build_authorization, aes_decrypt, \
    load_certificate, rsa_verify
class WechatPay:
    __api_gateway__ = "https://api.mch.weixin.qq.com"

    def __init__(self, config):
        """
        app_id:  appid
        mch_id:  商户号
        key:  签名key
        serial_no: 证书编号
        cert_file:  证书路径
        cert_key:  商户私钥证书key路径
        """
        self._app_id = config['APP_ID']
        self._mch_id = config['MCH_ID']
        self._apiv3_key = config['KEY']
        self.cert_file = config['WXPAY_CERT_FILE']
        self._private_key = config['WXPAY_CERT_KEY']
        self._cert_dir = config['WXPAY_CERT_DIR']
        self._serial_no = config['SERIAL_NO']
        self.notify_url = config['WXPAY_NOTIFY_URL']
        self.debug = config['DEBUG']
        self._certificates = []
        self._proxy = None
        self._init_certificates()


# native下单
    def place_order(self, data):
        native_api = "/v3/pay/transactions/native"
        api_url = self.__api_gateway__ + native_api
        headers = {
            "Authorization": build_authorization(native_api,
                                                 "POST",
                                                 self._mch_id,
                                                 self._serial_no,
                                                 self._private_key,
                                                 data),
            "Content-Type": "application/json",
            "Accept": "application/json",

        }
        data.update({"notify_url": self.notify_url})
        response = requests.post(api_url, json=data, headers=headers)
        return response.json()

# 初始化证书
    def _init_certificates(self):

        for file_name in os.listdir(self._cert_dir):
            if not file_name.lower().endswith('.pem'):
                continue
            with open(os.path.join(self._cert_dir, file_name)) as f:
                certificate = load_certificate(f.read())
            now = datetime.now(timezone.utc)
            if certificate and certificate.not_valid_after_utc >= now >= certificate.not_valid_before_utc:
                self._certificates.append(certificate)
        if not self._certificates:
            self._update_certificates()
        if not self._certificates:
            raise Exception('No wechatpay platform certificate, please double check your init params.')
    def _update_certificates(self):
        """下载平台证书公钥"""
        api_path = '/v3/certificates'
        code, res = self.request(api_path, skip_verify=True)
        if code != 200:
            return
        data = res.get('data')
        # 提取返回数据 data包含多个证书
        for value in data:
            # 证书编号
            serial_no = value.get('serial_no')
            # 有效期
            effective_time = value.get('effective_time')
            # 过期时间
            expire_time = value.get('expire_time')
            # 加密信息字段
            encrypt_certificate = value.get('encrypt_certificate')
            algorithm = nonce = associated_data = ciphertext = None
            if encrypt_certificate:
                # 算法
                algorithm = encrypt_certificate.get('algorithm')
                # 随机字符串
                nonce = encrypt_certificate.get('nonce')
                # 附加数据
                associated_data = encrypt_certificate.get('associated_data')
                # 密文
                ciphertext = encrypt_certificate.get('ciphertext')
            if not (
                    serial_no
                    and effective_time
                    and expire_time
                    and algorithm
                    and nonce
                    and associated_data
                    and ciphertext):
                continue
            # 对证书解密 aes解密
            cert_str = aes_decrypt(
                nonce=nonce,
                ciphertext=ciphertext,
                associated_data=associated_data,
                apiv3_key=self._apiv3_key)
            # 509加密协议
            certificate = load_certificate(cert_str)
            if not certificate:
                continue
            # 验证证书有效期
            now = datetime.utcnow()
            if certificate.not_valid_after < now < certificate.not_valid_before:
                continue
            self._certificates.append(certificate)
            # 保存证书到指定目录

            with open(os.path.join(self._cert_dir , serial_no + '.pem'), 'w') as f:
                f.write(cert_str)

    def request(self, path, method="GET", data="", skip_verify=False, sign_data="", files=None,
                cipher_data=False, headers={}):
        if files:
            headers.update({'Content-Type': 'multipart/form-data'})
        else:
            headers.update({'Content-Type': 'application/json'})
        headers.update({'Accept': 'application/json'})
        headers.update({'User-Agent': 'WechatPay V3 API - Yuanbian Lab'})
        if cipher_data:
            headers.update({'Wechatpay-Serial': hex(self._last_certificate().serial_number)[2:].upper()})
        authorization = build_authorization(
            path,
            method,
            self._mch_id,
            self._serial_no,
            self._private_key,
            data=data if data else sign_data)
        headers.update({'Authorization': authorization})
        # if self._logger:
        #     self._logger.debug('Request url: %s' % self._gate_way + path)
        #     self._logger.debug('Request type: %s' % method.value)
        #     self._logger.debug('Request headers: %s' % headers)
        #     self._logger.debug('Request params: %s' % data)
        if method == "GET":
            response = requests.get(url=self.__api_gateway__ + path, headers=headers, proxies=self._proxy)
        elif method == "POST":
            response = requests.post(url=self.__api_gateway__ + path, json=None if files else data,
                                     data=data if files else None, headers=headers, files=files, proxies=self._proxy)
        elif method == "PATCH":
            response = requests.patch(url=self.__api_gateway__ + path, json=data, headers=headers, proxies=self._proxy)
        elif method == "PUT":
            response = requests.put(url=self.__api_gateway__ + path, json=data, headers=headers, proxies=self._proxy)
        elif method == "DELETE":
            response = requests.delete(url=self.__api_gateway__ + path, headers=headers, proxies=self._proxy)
        else:
            raise Exception('wechatpayv3 does no support this request type.')
        # if self._logger:
        #     self._logger.debug('Response status code: %s' % response.status_code)
        #     self._logger.debug('Response headers: %s' % response.headers)
        #     self._logger.debug('Response content: %s' % response.text)
        if response.status_code in range(200, 300) and not skip_verify:
            if not self._verify_signature(response.headers, response.text):
                raise Exception('failed to verify the signature')
        return response.status_code, response.json() if 'application/json' in response.headers.get(
            'Content-Type') else response.text

    def pay_notify(self, signature, timestamp, nonce, serial_no, data):
        res = self._verify_signature(signature, timestamp, nonce, serial_no, data.decode())
        # 解密
        if res:
            order_data = self.decrypt_callback(data)
        else:
            order_data = None
        return res, json.loads(order_data)

    def _verify_signature(self, signature, timestamp, nonce, serial_no, data):
        """验证回调签名
        :return:
        """

        cert_found = False
        for cert in self._certificates:
            if int(serial_no, 16) == cert.serial_number:
                cert_found = True
                certificate = cert
                break
        if not cert_found:
            self._update_certificates()
            for cert in self._certificates:
                # 找到与请求头证书编号一致的证书
                if int('0x' + serial_no, 16) == cert.serial_number:
                    cert_found = True
                    certificate = cert
                    break
            if not cert_found:
                return False
        # rsa验签
        if not rsa_verify(timestamp, nonce, data, signature, certificate):
            return False
        return True

    def decrypt_callback(self, data):
        # if isinstance(body, bytes):
        #     body = body.decode('UTF-8')
        # if self._logger:
        #     self._logger.debug('Callback headers: %s' % headers)
        #     self._logger.debug('Callback body: %s' % body)

        data = json.loads(data)
        resource_type = data.get('resource_type')
        if resource_type != 'encrypt-resource':
            return None
        resource = data.get('resource')
        if not resource:
            return None
        algorithm = resource.get('algorithm')
        if algorithm != 'AEAD_AES_256_GCM':
            raise Exception('wechatpayv3 does not support this algorithm')
        nonce = resource.get('nonce')
        ciphertext = resource.get('ciphertext')
        associated_data = resource.get('associated_data')
        if not (nonce and ciphertext):
            return None
        if not associated_data:
            associated_data = ''
        result = aes_decrypt(
            nonce=nonce,
            ciphertext=ciphertext,
            associated_data=associated_data,
            apiv3_key=self._apiv3_key)
        # if self._logger:
        #     self._logger.debug('Callback result: %s' % result)
        return result





