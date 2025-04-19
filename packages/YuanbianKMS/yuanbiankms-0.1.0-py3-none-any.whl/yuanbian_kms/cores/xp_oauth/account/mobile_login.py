# -*- coding=utf-8 -*-
from flask import request, flash
from xp_cms.cores.xp_oauth.login_interface import AbstractLogin
from xp_cms.services.user_service import UserService
from xp_cms.forms.auth_form import LoginForm
from xp_cms.auth.sms_service import validator_sms_code
from xp_cms.auth.utils import add_user


class LoginByMobile(AbstractLogin):
    def __init__(self):
        self.mobile = None

    def login(self):
        self.mobile = request.form.get("mobile")
        validator_code = request.form.get("sms_code")
        if not validator_sms_code(self.mobile, validator_code):
            return None
        user = self._check_login()
        if user:
            return user
        else:
            user_info = {
                "username"       : f"yuanbian_{self.mobile}",
                "mobile"         : self.mobile,
                "password_origin": ""
            }

            return add_user(**user_info)

    def _check_login(self):
        return UserService.get_user_by_mobile(self.mobile)
