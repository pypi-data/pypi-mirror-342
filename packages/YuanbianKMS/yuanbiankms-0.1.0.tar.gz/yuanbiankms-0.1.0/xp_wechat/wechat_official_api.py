# -*- coding=utf-8 -*-
import hashlib
import requests
from urllib.parse import quote, urljoin, urlencode
from flask import current_app
from .utils import to_dict, get_access_token

__all__ = ["WechatOfficialApi"]


class WechatOfficialApi:
    """微信公众号相关接口
        wechat_verier_get - GET  微信接口安全认证
        wechat_verier_post - POST 微信消息接口
        verier - 微信接口数据安全鉴别
        getQrcode - 获得场景二维码
        get_wechat_unionid - 根据openid获得微信用户unionid
        get_wechat_user_info - 根据openid获得微信用户信息
    """
    def __init__(self):
        pass

    @classmethod
    def verier(cls, data):
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        token = current_app.config.get('WX_API_TOKEN')

        lists = [token, timestamp, nonce]
        lists.sort()
        sha1 = hashlib.sha1()
        sha1.update("".join(lists).encode())
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            return True
        else:
            return False

    @classmethod
    def wechat_verier_post(cls, data):
        data = to_dict(data)
        if data['MsgType'] == "event":
            return data['Event'].lower(), data
        if data["MsgType"] in ["text", "image", "voice", "video", "location", "link"]:
            return data['MsgType'], data

    @classmethod
    def get_qrcode(cls, access_token, scene_str, type=None):
        '''
        :param type:type == "limit"永久性二维码
        :return:
        '''
        qr_api = " https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s"
        qr_api = qr_api % access_token
        headers = {'Content-Type': 'application/json'}
        if type == "limit":
            data = {"action_name": "QR_LIMIT_SCENE",
                    "action_info": {"scene": {"scene_str": "python-xp.com"}}
                    }
        else:
            data = {"action_name"   : "QR_STR_SCENE",
                    "action_info"   : {"scene": {"scene_str": scene_str}},
                    "expire_seconds": 604800,
                    }
        res = requests.post(qr_api, headers=headers, json=data)
        ticket = res.json().get('ticket')
        qr_url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s" % ticket
        try:
            img = requests.get(qr_url).content
            if img is None:
                raise RuntimeError("check token！！！！ ")
        except Exception as e:
            current_app.logger.error(e)
        return img


