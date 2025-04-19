# -*- coding=utf-8 -*-
import os
from flask import render_template, flash, redirect, url_for, request,\
    current_app, Blueprint, send_from_directory, session, jsonify
from flask_login import current_user, login_required


upload_module = Blueprint("upload", __name__)


@upload_module.before_request
@login_required
def is_vip():
    if not current_user.vip_type:
        return jsonify({"uploaded": 0, "error":{"message": "非VIP用户不能上传"}})
    upload_base_dir = current_app.config['XPCMS_UPLOAD_PATH']
    # 管理员用户不限制上传
    if current_user.is_admin:
        session['user_upload_total_size'] = 0
        return
    user_upload_dir = os.path.join(upload_base_dir, current_user.username)
    if session.get('user_upload_total_size', None) is None:
        stat_user_upload_size(user_upload_dir)


def stat_user_upload_size(user_dir):
    amount = 0
    for dir, sub_dirs, files in os.walk(user_dir):
        for file in files:
            amount += os.path.getsize(os.path.join(dir, file))
    session['user_upload_total_size'] = amount



