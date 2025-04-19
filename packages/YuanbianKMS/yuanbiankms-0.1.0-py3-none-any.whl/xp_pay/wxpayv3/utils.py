# coding: utf-8
import os,random
import hashlib
import time
import json
from base64 import b64decode, b64encode

from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP, PKCS1v15
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA1, SHA256, SM3, Hash
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.x509 import load_pem_x509_certificate


try:
    import qrcode
except:
    os.system("pip install qrcode")
    import qrcode

import base64
from io import StringIO

def sorted_str(params, key, null=False):
    """ key按照ASCII排序
    没什么用了
    """
    if null:
        s = '&'.join((str(k) + '=' + str(params[k])) for k in sorted(params))
    else:
        s = '&'.join((str(k) + '=' + str(params[k])) for k in sorted(params) if params[k])
    return s + '&key={}'.format(key)
def sign_md5(s, upper=True):
    """ md5签名 没有用了 """
    if upper:
        return hashlib.md5(s.encode("utf-8")).hexdigest().upper()
    else:
        return hashlib.md5(s.encode("utf-8")).hexdigest()

def random_str(length, upper=True):
    """ 随机字符串 """
    sample = 'abcdefghijklmnopqrstuvwxyz'
    sample += sample.upper()
    sample += '1234567890'
    result = ''.join(random.sample(sample, length))
    return result.upper() if upper else result

# 二维生成
def make_code(text):
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=4
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image()
    img_buffer = StringIO.StringIO()
    img.save(img_buffer, 'png')
    res = img_buffer.getvalue()
    img_buffer.close()
    return base64.b64encode(res)
def build_authorization(path,
                        method,
                        mchid,
                        serial_no,
                        private_key_path,
                        data=None,
                        ):
    """生成authorization密文"""
    timestamp = round(time.time())
    nonce_str = random_str(32)
    body = data if isinstance(data, str) else json.dumps(data)
    sign_str = '%s\n%s\n%s\n%s\n%s\n' % (method, path, timestamp, nonce_str, body)
    signature = rsa_sign(private_key_path=private_key_path, sign_str=sign_str)
    authorization = f'WECHATPAY2-SHA256-RSA2048 mchid="{mchid}",serial_no="{serial_no}",nonce_str="{nonce_str}",timestamp="{timestamp}",signature="{signature}"'
    return authorization

def format_private_key(private_key_str):
    pem_start = '-----BEGIN PRIVATE KEY-----\n'
    pem_end = '\n-----END PRIVATE KEY-----'
    if not private_key_str.startswith(pem_start):
        private_key_str = pem_start + private_key_str
    if not private_key_str.endswith(pem_end):
        private_key_str = private_key_str + pem_end
    return private_key_str

def rsa_sign(private_key_path, sign_str):
    """生成签名
    使用支付工具生成的商户私钥加密
    """
    private_key = load_pem_private_key(open(private_key_path, "rb").read(), password=None)
    message = sign_str.encode("utf-8")
    signature = private_key.sign(data=message, padding=PKCS1v15(), algorithm=SHA256())
    _sign = b64encode(signature).decode('utf-8')
    return _sign


def aes_decrypt(nonce, ciphertext, associated_data, apiv3_key):
    """使用AES对称解密"""
    key_bytes = apiv3_key.encode()
    nonce_bytes = nonce.encode()
    associated_data_bytes = associated_data.encode()
    data = b64decode(ciphertext)
    # 创建AESGCM
    aesgcm = AESGCM(key=key_bytes)
    try:
        result = aesgcm.decrypt(nonce=nonce_bytes, data=data, associated_data=associated_data_bytes).decode('UTF-8')
    except InvalidTag:
        result = None
    return result

# 加载证书
def load_certificate(certificate_str):
    try:
        return load_pem_x509_certificate(data=certificate_str.encode(), backend=default_backend())
    except:
        return None

# 微信回调rsa 验签
def rsa_verify(timestamp, nonce, body, signature, certificate):
    """ 微信回调验签，从请求头中获得参数与证书"""
    sign_str = '%s\n%s\n%s\n' % (timestamp, nonce, body)
    public_key = certificate.public_key()
    message = sign_str.encode()
    try:
        signature = b64decode(signature)
    except:
        return False
    try:
        public_key.verify(signature, message, PKCS1v15(), SHA256())
    except InvalidSignature:
        return False
    return True

