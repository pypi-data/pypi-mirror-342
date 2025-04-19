# -*- coding=utf-8 -*-
from xp_cms.utils import redirect_back
from xp_cms.cores.xp_oauth.login_interface import AbstractLogin
from .wechat_login_api import WechatWebLogin, WechatOfficialLogin


class LoginByWechat(AbstractLogin):
    _login_type = {"pc": WechatWebLogin, "wechat": WechatOfficialLogin}
    def __init__(self, client_type):
        self.client = self._login_type[client_type]()

    def _get_login_qrcode(self, redirect_uri, state):
        return self.client.get_code(redirect_uri, state)

    def login(self, code=None, redirect_uri=None, state=None):
        if code is None:
            access_token, openid = self.client.check_access_token()
            if access_token is None:
                return {"jump_url": self._get_login_qrcode(redirect_uri, state)}
        else:
            access_token, openid = self.client.get_access_token(code)
        return self._do_login(access_token, openid)

    def _do_login(self, access_token, openid):
        user = self.client.get_wechat_user_info(access_token, openid)
        return user


