# -*- coding=utf-8 -*-
import os
from flask import Blueprint
from flask_login import current_user, login_required

root_path = os.path.abspath("./")
template_folder = os.path.join(root_path, "addons/chatgpt/templates")
chatgpt_app = Blueprint("chatgpt_app", __name__, template_folder=template_folder)


# @chatgpt_app.before_request
# @login_required
# def is_approve():
#     return
