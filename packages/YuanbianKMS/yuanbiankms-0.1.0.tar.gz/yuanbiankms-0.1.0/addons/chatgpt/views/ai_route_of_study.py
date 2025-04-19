# -*- coding=utf-8 -*-
from flask import render_template
from ..__main__ import chatgpt_app


@chatgpt_app.route("/route_of_study")
def route_of_study():
    return render_template("ai_route_of_study.html")
