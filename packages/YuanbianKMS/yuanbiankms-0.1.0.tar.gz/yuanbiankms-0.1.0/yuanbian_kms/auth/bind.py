# -*- coding=utf-8 -*-
from .auth_blueprint import AuthManage
from flask import request, render_template, redirect, url_for, \
    session, jsonify, flash
from flask_login import current_user, login_user
from xp_cms.forms.auth_form import *
from xp_cms.services.user_service import WechatOAuthService
from xp_cms.utils import redirect_back
from xp_cms.cores.xp_oauth.wechat.wechat_user_info import WechatUserInfo
from xp_cms.extensions import nosql
from xp_cms.cores.xp_oauth.account.account_login import LoginByAccount
from .login import LoginView
from .register import RegisterView


@AuthManage.route("/bind_select")
def bind_select():
    if session.get("wechat_oauth") is None:
        return redirect(url_for("auth.login"))
    nickname = session['wechat_oauth']['nickname']
    return render_template("auth/bind_select.html", nickname=nickname)


class WechatBindRegisterView(RegisterView):
    template = "auth/bind_register.html"

    def post(self):
        user = self._do_register()
        if user:
            user = WechatUserInfo.bind_user_to_unionid(user, session['wechat_oauth']['unionid'])
            if user:
                login_user(user)
                session.pop("wechat_oauth")
                return redirect_back()
            else:
                flash("绑定失败")
        return redirect(request.full_path)

    def _check_view(self):
        return session.get('wechat_oauth', None)


AuthManage.add_url_rule("/bind_register", view_func=WechatBindRegisterView.as_view("bind_register"))


# @AuthManage.route('/bind_register', methods=['GET', 'POST'])
# def bind_register():
#     """首先微信登录后才能注册
#     :return:
#     """
#     # 已经登陆用户跳转到首页
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#
#     if session.get('wechat_oauth') is None:
#         return redirect(url_for('auth.login'))
#
#     form = RegisterForm()
#     if form.validate_on_submit():
#         user = {
#             # "email": form.email.data.lower(),
#             "username": form.username.data,
#             "password_hash": form.password.data,
#             "vip_type": 0,
#             # "vip_type":form.vip_type.data,
#             "reg_ip": request.remote_addr,
#             # "realname": form.realname.data
#         }
#         user = WechatUserInfo.bind_user_to_unionid(user, session['wechat_oauth']['unionid'])
#         if user:
#             login_user(user)
#             session.pop("wechat_oauth")
#             return redirect_back()
#         else:
#             session['login_errors'] = nosql.incr("user_" + request.form.get("username") + "_login_error")
#             flash("账户密码不正确", category="'error'")
#     return render_template('auth/bind_register.html', form=form,
#                            nickname=session['wechat_oauth']['nickname']
#                            )

class WechatBindLoginView(LoginView):
    template = 'auth/bind_login.html'

    def post(self):
        user = self._do_login()
        if user:
            if self._bind(user):
                login_user(user)
                return redirect_back()

        return redirect(request.full_path)

    def _bind(self, user):
        user = WechatUserInfo.bind_user_to_unionid(user, session['wechat_oauth']['unionid'])
        if user:
            session.pop("wechat_oauth")
            return True
        else:
            flash("绑定失败，该微信号已经被绑定，请重新选择绑定账号")
            return False

    def _check_view(self):
        return session.get('wechat_oauth', None)


AuthManage.add_url_rule("/bind_login", view_func=WechatBindLoginView.as_view("bind_login"))
#
# @AuthManage.route('/bind_login', methods=['GET', 'POST'])
# def bind_login():
#     """
#     微信绑定已有会员
#     :return:
#     """
#     if current_user.is_authenticated:
#         return redirect(url_for("index"))
#
#     # 需要微信登陆oauth凭证
#     # 没有微信登陆的，跳转到登陆
#     if not session.get('wechat_oauth'):
#         return redirect(url_for("auth.login"))
#
#     if session.get('login_errors', 0) > 5:
#         flash("登录错误次数太多，需要完成扫码确认身份")
#         form = LoginFormCaptcha()
#     else:
#         form = LoginForm()
#
#     if form.validate_on_submit():
#         login_client = LoginByAccount()
#         user = login_client.login()
#         # 密码验证成功
#         if user:
#             user = WechatUserInfo.bind_user_to_unionid(user, session['wechat_oauth']['unionid'])
#             if user:
#                 login_user(user)
#                 session.pop("wechat_oauth")
#                 return redirect_back()
#             else:
#                 flash("绑定失败，该微信号已经被绑定，请重新选择绑定账号")
#         else:
#             session['login_errors'] = nosql.incr("user_" + request.form.get("username") + "_login_error")
#             flash("账户密码不正确", category="'error'")
#     return render_template("auth/bind_login.html", form=form)
