# -*- coding=utf-8 -*-
from hashlib import md5
import re
from datetime import datetime
from uuid import uuid4
from random import choices
from flask import session, request, flash

from xp_cms.services.user_service import UserService
from xp_cms.extensions import nosql


def check_username(username):
    if not re.match("^[a-z][a-z0-9_]{4,19}$", username):
        return {"usable": False, "error": "用户名必须由字母开始，只能包含6～20个字母、数字、_字符"}
    user = UserService.get_one_by_field(("username", username))
    if user:
        return {"usable": False, "error": "真遗憾，该用户名已经被占用"}
    return {"usable": True}


def check_mobile(mobile):
    if not re.match(r"^1[345789]\d{9}$", mobile):
        return {"usable": False, "error": "手机号必须是13*, 15*, 17*, 18*, 19*等号端11位手机号"}
    user = UserService.get_one_by_field(("mobile", mobile))
    if user:
        return {"usable": False, "error": "手机号已经被注册，可以使用手机号直接登陆"}
    return {"usable": True}


def check_code(code):
    if session.get('verify_code') is None or code != session['verify_code']['code']:
        return False
    return True


def create_verify_code():
    if session.get('verify_code') is None:
        session['verify_code'] = {
            'code_key'   : uuid4().hex,
            'code'       : "".join(choices("abcdefghijklmnopqrstuvwxyz123456890", k=6)),
            'code_number': 0
        }
    session['verify_code'].update({
        'code_key'   : uuid4().hex,
        'code'       : "".join(choices("abcdefghijklmnopqrstuvwxyz123456890", k=6)),
        'code_number': session['verify_code']['code_number'] + 1,
    })

    nosql.set(session['verify_code']['code_key'],
              str(session['verify_code']['code_number']) + " " + session['verify_code']['code'])
    nosql.set(session['verify_code']['code_key'] + "_scan_openid", "")
    session["wechat_scene_str_id"] = "verify_" + session['verify_code']['code_key']


def check_robot_sign(user_fingerprint, sign, t):
    if md5("".join(["yuanbian-lab", user_fingerprint, t]).encode()).hexdigest() != sign:
        return False
    return True


def check_robot(user_fingerprint, sign, t, check_item):
    message = {"result": False, "errors": {}}
    check_call = {"username": check_username, "mobile": check_mobile}
    user_fingerprint = request.args.get("user_fingerprint", "")
    sign = request.args.get("sign", "")
    t = request.args.get("t", "")
    if not check_robot_sign(user_fingerprint, sign, t):
        message['errors'][check_item] = "没能通过人机认证，拒绝爬虫访问"
    if not request.args.get(check_item, ""):
        message['errors'][check_item] = "此项为必填项"
    else:
        res = check_call[check_item](request.args.get("mobile"))
        if not res.get('usable', False):
            message['errors'][check_item] = res['error']
    if not message.get('errors', False):
        message['result'] = True
    return message


def add_user(username, password_origin, mobile):
    user = {
        "username"        : username,
        "password_origin" : password_origin,
        "mobile"          : mobile,
        "vip_type"        : 0,
        "reg_ip"          : request.headers.get('X-Real-Ip') or request.remote_addr,
        "reg_date"        : datetime.now()
        # "reg_openid"   : nosql.get(session['verify_code']['code_key'] + "_scan_openid")
    }
    res = check_username(user['username'])
    if res['usable'] is False:
        flash(res['error'])
        return None
    return UserService.add(user)
