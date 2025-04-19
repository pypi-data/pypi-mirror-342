# -*- coding=utf-8 -*-
from flask import request, render_template
from flask_login import login_required, current_user
from ..__main__ import chatgpt_app


@chatgpt_app.route("/manual")
def ai_manual():
    is_login = True
    if current_user.is_anonymous:
        is_login = False
    ai_type = {"option": "我是Python资料搜集者，你想查询什么",
               "type": "Python中文指南"}
    return render_template("playground.html", ai_type=ai_type, is_login=is_login)