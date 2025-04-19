# -*- coding=utf-8 -*-
import json
from datetime import datetime
import html
from flask import request, session, render_template, \
    redirect, url_for, g, current_app, jsonify, flash
from flask_login import current_user
from .member_module import member_module
from xp_cms.models.user import User
from xp_cms.extensions import db
from xp_cms.forms.auth_form import EditInfoForm
from xp_cms.forms.acive_code_form import ActiveByCodeForm
from xp_cms.services.user_service import UserService, ActiveCodeService, ActiveCodeUseLogService
from xp_cms.extensions import nosql


# 用户信息修改
@member_module.route("/profile", methods=["get", "post"])
def profile():

    if request.method == "POST":
        if current_user.is_approve != 0:
            return jsonify({"res": False, "message": "您的认证已经提交过"})
        data = request.form.copy()
        data['mobile'] = html.escape(data['mobile'])[:20]
        data['email'] = html.escape(data['email'])[:20]
        data['realname'] = html.escape(data['realname'])[:10]
        # -1为等待认证
        data['is_approve'] = -1
        row = UserService.update_columns({"user_id": current_user.user_id},
                                         data)
        if row:
            return jsonify({"res": True, "message": "认证申请提交成功"})
    return render_template("member/pc/profile/profile.html")


@member_module.route("/change_password", methods=["get", "post"])
def change_password():
    if request.method == "POST":
        errors = nosql.incr("user_" + current_user.username + "_login_error")
        if errors >= 6:
            return jsonify(
                {"res": False, f"message": "修改错误次数超过限制，该账号在完成一次正确登陆之前，不再允许修改密码"})
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        user = User.query.filter_by(username=current_user.username).one()
        if user.validate_password(old_password):
            user.set_password(new_password)
            nosql.delete("user_" + current_user.username + "_login_error")
            return jsonify({"res": True, "message": "修改成功"})
        else:
            return jsonify({"res": False, "message": f"密码验证失败, 允许尝试次数剩余{5 - errors}次"})

    return render_template("member/pc/profile/password.html")


@member_module.route("/account_details")
def account_details():
    return ""


@member_module.route("/set_approve_email")
def set_approve_email():
    return ""


@member_module.route("/upgrade_level_by_code", methods=["get", "post"])
def upgrade_level_by_code():

    form = ActiveByCodeForm()
    if form.validate_on_submit():
        errors = nosql.incr("user_" + current_user.username + "_active_error")
        if errors >= 5:
            return jsonify(
                {"res": False, f"message": "激活码输入错误次数超过限制，账号已被限制激活操作，请联系客服人员"})
        active_code = request.form.get("active_code")
        code = ActiveCodeService.get_one_by_field(("code", active_code))
        user = UserService.get_user_by_username(current_user.username)
        if code:
            res = UserService.upgrade_vip_level(user, code.active_type)
            if res:
                ActiveCodeService.delete_by_id(code.code_id)
                active_log = {
                    "code": code.code,
                    "active_type": code.active_type,
                    "expiration": code.expiration,
                    "channel": code.channel,
                    "username": user.username,
                    "active_time": datetime.today()
                }
                ActiveCodeUseLogService.add_by_dicts(active_log)
                nosql.delete("user_" + current_user.username + "_active_error")
                return jsonify({"res": True, "message": f"升级成功，VIP有效期至: {res.vip_expiration}"})
            else:
                return jsonify({"res": False, "message": "升级失败，请联系客服人员微信:Yuanbian202201"})
        else:
            return jsonify({"res": False, "message": f"激活码不存在，请检查后重新输入， 剩余允许错误次数{5 - errors}"})
    else:
        return render_template("member/pc/profile/upgrade_vip_level.html")


