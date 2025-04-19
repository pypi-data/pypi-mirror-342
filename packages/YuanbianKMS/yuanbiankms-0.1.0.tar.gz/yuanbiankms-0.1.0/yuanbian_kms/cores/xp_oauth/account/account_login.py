# -*- coding=utf-8 -*-
from flask import request, flash, session, current_app
from xp_cms.cores.xp_oauth.login_interface import AbstractLogin
from xp_cms.services.user_service import UserService
from xp_cms.forms.auth_form import LoginForm
from xp_cms.extensions import nosql
from xp_cms.forms.auth_form import LoginForm, LoginFormCaptcha


class LoginByAccount(AbstractLogin):

    def __init__(self):
        self.form = self.create_form()

    def login(self):
        user = self._check_login()
        if user:
            return user
            # if user is False:
            #     flash("账户密码不正确", category="'error'")
                # return redirect(url_for("login", next=request.args.get('next')))
            # 登录用户必须绑定微信公众号
            # elif user.oauth:
            #     return user
                # login_user(user)
                # return redirect_back()
            # else:
            #     session['login_user'] = user.user_id
            #     if g.client == "wechat":
            #         return redirect(url_for("auth.wechat_inner_login"))
            #     else:
            #         return redirect(url_for("auth.wechat_sns_login_step1"))
        else:
            return None

    def _check_login(self):
        if self.form.validate_on_submit():
            username = self.form.username.data
            password = self.form.password.data
            remember = self.form.remember.data
            user = UserService.login_check(username, password)
            if user:
                return user
            else:
                session['login_errors'] = nosql.incr(f"user_{username}_login_error")
                flash("账户密码不正确", category="'error'")
                return None

    @staticmethod
    def create_form():
        if session.get('login_errors', 0) > current_app.config.get('SHOW_CAPTCHA_ERRORS', 5):
            flash("登录错误次数太多，需要完成扫码确认身份")
            form = LoginFormCaptcha()
        else:
            form = LoginForm()
        return form



