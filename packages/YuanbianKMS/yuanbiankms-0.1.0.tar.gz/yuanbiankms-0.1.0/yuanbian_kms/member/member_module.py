# -*- coding=utf-8 -*-
import re
from flask import request, session, redirect, url_for, \
    render_template, g
from flask import Blueprint
from flask_login import login_required
from .member_menus import Member_Menus

member_module = Blueprint("member", __name__)


@member_module.before_request
@login_required
def is_login():
    if g.client != "pc":
        g.client = "pc"
    #     return "<h1>为了给您带来更好的体验，会员中心手机端界面开发中，敬请期待</h1>" \
    #            "<p><a href=\"/\">返回首页</a>"
    # pass


@member_module.context_processor
def get_global_vars():

    regular_str = r"/member/([a-z0-9]+)/"
    # menu = {"profile": "我的资料",
    #         "account": "我的账户",
    #         "promotion": "我的推广",
    #         "": "安全设置",
    #         "article": "文章管理"
    #         }
    res = re.match(regular_str, request.path)
    if res:
        current_menu = res.groups()[0]
    else:
        current_menu = "profile"
    return {
        "Member_Menus": Member_Menus,
        "current_menu": current_menu}
