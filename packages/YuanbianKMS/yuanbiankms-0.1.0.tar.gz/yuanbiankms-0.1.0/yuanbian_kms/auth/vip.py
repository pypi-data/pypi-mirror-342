# -*- coding=utf-8 -*-

from flask import render_template

from .auth_blueprint import AuthManage


@AuthManage.route("/upgrade2vip")
def upgrade2vip():
    return render_template("auth/upgrade2vip.html")


@AuthManage.route("/upgrade2vvip")
def upgrade2vvip():
    return render_template("auth/upgrade2vvip.html")
