# -*- coding: utf-8 -*-

import base64, json
# pip install  pycryptodome
from Crypto.Cipher import AES

# 128位分组
BLOCK_SIZE = AES.block_size

# 补位
pad = lambda s, length: s + (BLOCK_SIZE - length % BLOCK_SIZE) * chr(BLOCK_SIZE - length % BLOCK_SIZE)

# 还原
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def encrypt_content(content, encrypt_type, encrypt_key, charset):
    if "AES" == encrypt_type.upper():
        return aes_encrypt_content(content, encrypt_key, charset)
    raise Exception("当前不支持该算法类型encrypt_type=" + encrypt_type)

def aes_encrypt_content(content, encrypt_key, charset):
    '''
    使用AES算法进行对称加密
    :param content:
    :param encrypt_key:
    :param charset:
    :return:
    '''
    length = len(bytes(content, encoding=charset))
    padded_content = pad(content, length)
    iv = b'\0' * BLOCK_SIZE
    # 创建加密方式
    cryptor = AES.new(encrypt_key.encode(), AES.MODE_CBC, iv)
    # 加密
    encrypted_content = cryptor.encrypt(padded_content.encode())
    # 将加密结果转换为b64encode编码字节
    encrypted_content = base64.b64encode(encrypted_content)
    # 将字节转换成字符串
    encrypted_content = str(encrypted_content, encoding=charset)
    return encrypted_content

def decrypt_content(encrypted_content, encrypt_type, encrypt_key, charset):
    if "AES" == encrypt_type.upper():
        return aes_decrypt_content(encrypted_content, encrypt_key, charset)
    raise Exception("当前不支持该算法类型encrypt_type=" + encrypt_type)

def aes_decrypt_content(encrypted_content, encrypt_key, charset):
    encrypted_content = base64.b64decode(encrypted_content)
    iv = b'\0' * BLOCK_SIZE
    cryptor = AES.new(encrypt_key.encode(), AES.MODE_CBC, iv)
    content = unpad(cryptor.decrypt(encrypted_content))
    content = content.decode(charset)
    return content

def decode_data(data, sso_secret_key):
    data = base64.urlsafe_b64decode(data)
    data = decrypt_content(data, "AES", sso_secret_key, "utf-8")
    data = json.loads(data)
    return data

def encode_data(data, sso_secret_key):
    data = json.dumps(data)
    data = encrypt_content(data, "AES", sso_secret_key, "utf-8")
    data = base64.urlsafe_b64encode(data.encode()).decode()
    return data

if __name__ == "__main__":
    encrypt_type = "aes"
    encrypt_key = "1234567891234567"
    content = "hello world"
    charset = "utf-8"
    encrypted_content = encrypt_content(content, encrypt_type,  encrypt_key, charset)
    print(encrypted_content)
    res = decrypt_content(encrypted_content, encrypt_type, encrypt_key, charset)
    res = print(res)


