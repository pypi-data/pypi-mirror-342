# -*- coding=utf-8 -*-
import os, re
from datetime import date
from flask import render_template, flash, redirect, url_for, request, \
    current_app, Blueprint, send_from_directory, session
from flask_login import current_user, login_required
# from xp_cms.utils import redirect_back, allowed_file, rename_image, resize_image
from xp_cms.extensions import db
from xp_cms.forms.settings import SettingForm
from .admin_menu import Admin_Menus

admin_module = Blueprint('admin', __name__)

allowed_ips = ['192.168.3.1', '192.168.8.1']
@admin_module.before_request
@login_required
def is_admin():
    if request.access_route:
        client_ip = request.access_route[0]
    else:
        client_ip = request.remote_addr
    if request.host not in ['test.python-xp.com', 'debug.python-xp.com']:
    #if not current_user.is_admin or not client_ip in allowed_ips:
        return redirect(url_for("auth.login"))


@admin_module.route('/', methods=['GET'])
def index():
    return render_template("admin/admin_index.html")


@admin_module.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Setting updated.', 'success')
        return redirect(url_for('blog.index'))
    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about.data = current_user.about
    return render_template('admin/settings.html', form=form)


@admin_module.context_processor
def get_global_vars():
    regular_str = "\/admin\/([a-z0-9_]+)\/"
    res = re.match(regular_str, request.path)
    if res:
        current_menu = res.groups()[0]
    else:
        current_menu = "article"
    return {
        "Admin_Menus" : Admin_Menus,
        "current_menu": current_menu}
