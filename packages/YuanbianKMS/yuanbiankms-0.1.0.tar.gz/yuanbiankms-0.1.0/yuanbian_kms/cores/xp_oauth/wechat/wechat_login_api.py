# -*- coding=utf-8 -*-
from uuid import uuid4
import requests
from abc import ABC, abstractmethod
from flask import current_app, session


class WechatLoginApi(ABC):
    def __init__(self, app_id_name, app_secret_name, store_token_key):
        self.logger = current_app.logger
        self.app_id = current_app.config.get(app_id_name)
        self.app_secret = current_app.config.get(app_secret_name)
        self.session_storage = session
        self.nosql_storage = current_app.extensions['nosql']
        self.store_token_key = store_token_key

    @abstractmethod
    def get_code(self, *args, **kwargs):
        pass

    def get_access_token(self, code):
        access_token_api = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=" \
                           "%s&grant_type=authorization_code"
        data = requests.get(access_token_api % (self.app_id, self.app_secret, code)).json()
        if "access_token" in data:
            self._save_access_token(data)
            return data['access_token'], data['openid']
        return None, None

    def get_wechat_user_info(self, access_token, openid):
        unionid_api = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh-CN"
        try:
            user_info = requests.get(unionid_api % (access_token, openid)).json()
        except Exception as e:
            self.logger.error(e)
            user_info = None
        return user_info

    def check_access_token(self):
        refresh_token_url = "https://api.weixin.qq.com/sns/oauth2/refresh_token?" \
                            "appid={appid}" \
                            "&grant_type=refresh_token" \
                            "&refresh_token={refresh_token}"
        if self.session_storage.get(self.store_token_key):
            session_store_token_key = self.session_storage.get(self.store_token_key)
            access_token_key = session_store_token_key['access_token']
            openid_key = session_store_token_key['openid']
            access_token = self.nosql_storage.get(access_token_key)
            openid = self.nosql_storage.get(openid_key)
            if access_token is None:
                refresh_token = self.nosql_storage.get(session_store_token_key['refresh_token'])
                if refresh_token:
                    data = requests.get(refresh_token_url.format(appid=self.app_id, refresh_token=refresh_token)).json()
                    if data:
                        self._save_access_token(data)

            return access_token, openid
        return None, None

    def _save_access_token(self, access_token_data):
        if self.session_storage.get(self.store_token_key, None) is None:
            self.session_storage[self.store_token_key] = {
                'access_token': uuid4().hex,
                'refresh_token': uuid4().hex,
                'openid': uuid4().hex,
            }

        time_limit = {
            'access_token': 7200,
            'refresh_token': 29 * 24 * 3600,
            'openid': 29 * 24 * 3600,
        }
        for key, val in self.session_storage[self.store_token_key].items():
            self.nosql_storage.set(val, access_token_data[key], time_limit[key])


class WechatWebLogin(WechatLoginApi):
    def __init__(self):
        store_token_key = 'wechat_web_key'
        super().__init__("WX_WEB_APP_ID", "WX_WEB_APP_SECRET", store_token_key)

    def get_code(self, redirect_uri, state):
        """WEB页面扫码登录"""
        code_api = "https://open.weixin.qq.com/connect/qrconnect?appid=%s&redirect_uri=%s&response_type=code&" \
                   "scope=snsapi_login&state=%s#wechat_redirect"
        url = code_api % (self.app_id, redirect_uri, state)
        return url

    def get_wechat_user_info(self, access_token, openid):
        user = super().get_wechat_user_info(access_token, openid)
        if user:
            user['nickname'] = user['nickname'].encode("ISO-8859-1").decode()
            user['city'] = None  #user['city'].encode("ISO-8859-1").decode()
            user['province'] = None  #user['province'].encode("ISO-8859-1").decode()
            user['country'] = None  #user['country'].encode("ISO-8859-1").decode()

        return user


class WechatOfficialLogin(WechatLoginApi):
    def __init__(self):
        store_token_key = 'wechat_official_key'
        super().__init__("WX_APP_ID", "WX_APP_SECRET", store_token_key)

    def get_code(self, redirect_uri, state, scope="snsapi_userinfo"):
        """跳转到微信登录授权页面完成登录"""
        code_api = "https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&" \
                   "redirect_uri={redirect_uri}&" \
                   "response_type=code&scope={scope}&state={state}#wechat_redirect"
        return code_api.format(appid=self.app_id, redirect_uri=redirect_uri, state=state, scope=scope)
