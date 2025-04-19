# -*- coding=utf-8 -*-
from datetime import datetime, date
from flask import request, render_template, session, flash, current_app, \
    redirect, url_for, json, jsonify
from flask.views import View
from flask_login import login_user, logout_user, login_required, current_user
from .auth_blueprint import AuthManage, AuthView
from xp_cms.forms.auth_form import ApproveForm
from xp_cms.cores.xp_oauth.account import LoginByAccount, LoginByMobile
from xp_cms.extensions import nosql, csrf
from xp_cms.utils import show_username
from xp_cms.utils import redirect_back
from xp_cms.services.account_service import AccountService
from xp_cms.services.user_service import UserService
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_required, get_jwt_identity, verify_jwt_in_request


class LoginView(AuthView):
    template = 'auth/login.html'
    login_class = {"mobile": LoginByMobile, 'account': LoginByAccount}

    def get(self):
        self._check_next_link()
        form = LoginByAccount.create_form()
        return render_template(self.template, form=form)

    def post(self):
        user = self._do_login()
        if user:
            if request.form.get("is_jwt"):
                identity = {"user_id": user.user_id, "username": user.username}
                return jsonify(is_login=1,
                               access_token=create_access_token(identity=identity),
                               refresh_token=create_refresh_token(identity=identity)
                               )
            login_user(user)
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return json.jsonify({"is_login": 1, "is_approve": user.is_approve})
            return redirect_back()
        else:
            return redirect(request.full_path)

    def _do_login(self):

        user = None
        login_client = self.login_class.get(request.form.get("login_type", "account"), LoginByAccount)()
        user = login_client.login()
        if user:
            self._after_login(user)
            self._update_status(user)
        return user

    def _register_after_login_action(self):
        pass
    def _after_login(self, user):
        today = date.today()
        last_login_date = None
        if user.last_login_time:
            last_login_date = datetime.date(user.last_login_time)
        if today != last_login_date:
            AccountService.add_balance(user.user_id, 5000,"token_coin",
                                       "LOGIN", "每日登录奖励")


    def _update_status(self, user):
        login_ip = request.headers.get('X-Real-Ip') or request.remote_addr
        login_time = datetime.now()
        UserService.update_login_info(user, login_ip=login_ip, login_time=login_time)
        session.pop('login_errors', None)
        nosql.delete(f"user_{user.username}_login_error")


AuthManage.add_url_rule("/login", view_func=LoginView.as_view("login"))


@AuthManage.route('/logout')
@login_required
def logout():
    logout_user()
    if session.get('wechat_oauth'):
        session.pop('wechat_oauth')
    return redirect(url_for("index"))


# 登录状态
@AuthManage.route('/member_status')
def get_member_status():
    user_id = username = None
    if not current_user.is_anonymous:
        user_id = current_user.user_id
        username = current_user.username
    return _get_member_status(user_id, username)


@AuthManage.route('/member_status_by_jwt')
@jwt_required()
def get_member_status_jwt():
    _current_user = get_jwt_identity()
    return _get_member_status(_current_user['user_id'], _current_user['username'])


def _get_member_status(user_id, username=None):
    ai_power = 0
    account = AccountService.get_account(user_id)
    if account:
        ai_power = account.points
    if username:
        username = show_username(username)

    return render_template("member/member_status.html",
                           ai_power=ai_power,
                           username=username)


@AuthManage.route('/member_info')
@login_required
def get_member_info():
    """用于yuanbian_helper显示
    """
    return _get_member_info(current_user.user_id, current_user.username)


@AuthManage.route('/member_info_by_jwt')
@jwt_required()
def get_member_info_by_jwt():
    """用于yuanbian_helper显示
    """
    _current_user = get_jwt_identity()
    return _get_member_info(_current_user['user_id'], _current_user['username'])


def _get_member_info(user_id, username):
    token_coins = 0
    account = AccountService.get_account(user_id)
    if account:
        token_coins = account.token_coin
    username = show_username(username)
    return jsonify({"username": username, "token_coins": token_coins})


@AuthManage.route('/is_login')
def is_login():
    if current_user.is_anonymous:
        return "0"
    else:
        if not current_user.is_approve:
            return "1"
        else:
            account = AccountService.get_account(current_user.user_id)
            if account.points <= 0:
                return "2"
            else:
                return "3"


# ajax 登陆页面
@AuthManage.route("/inner_login")
def inner_login():
    template = 'auth/login_ajax.html'
    form = LoginByAccount.create_form()
    next = request.referrer
    return render_template(template, form=form, next=next)


# 等待认证页面
@AuthManage.route("/wait_approve", methods=['GET', 'POST'])
def wait_approve():
    approve_form = ApproveForm()
    if request.method == "POST":
        if approve_form.validate_on_submit():
            user = UserService.get_user_by_id(current_user.user_id)
            if user.is_approve:
                return jsonify({"res": "fail", "message": "您已认证过了"})
            if user.reg_openid:
                return jsonify({"res": "fail", "message": "您已关注过"})
            account = {
                "user_id": current_user.user_id,
                "amount" : 1000,
                "event"  : "approve",
                "type"   : "points",
                'detail' : 'approve'

            }
            try:
                account = AccountService.add_balance(**account)
            except Exception as e:
                current_app.logger.error(e)
                return jsonify({"res": "fail", "message": "服务器错误，后续重试"})
            else:
                user.is_approve = 1
                user.reg_openid = nosql.get(session['verify_code']['code_key'] + "_scan_openid")
                try:
                    user = UserService.update(user)
                    assert user != None
                except:
                    return jsonify({"res": "fail", "message": "此微信已被绑定过"})
                else:
                    return jsonify({"res": "success", "message": "获取成功"})
        else:

            return jsonify({"res": "fail", "message": "验证码不正确"})

    return render_template("auth/wait_approve.html", form=approve_form)


@AuthManage.route("/need_aipower", methods=['GET', 'POST'])
def need_aipower():
    return render_template("auth/need_aipower.html")


@AuthManage.route("/need_vip", methods=['GET'])
def need_vip():
    return render_template("auth/need_vip.html")


@AuthManage.route("/refresh_jwt_token", methods=["POST"])
@jwt_required(refresh=True)
def refresh_jwt_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)