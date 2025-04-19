# -*- coding=utf-8 -*-

import json
from flask import request,session,render_template,\
                  redirect, url_for, jsonify

from xp_cms.admin import admin_module
from xp_cms.services.user_service import UserService
# from models import User
# from libs import db, csrf
from xp_cms.extensions import csrf
from xp_cms.forms.member import UserInfoEditForm, UserSearchForm
from xp_cms.constant import *

@admin_module.route("/user/list/<int:page>", methods=['get', "post"])
@admin_module.route("/user/list", defaults={"page":1},methods=['get', "post"])
def manage_member(page):
    form = UserSearchForm()
    if request.method == "POST":
        q = form.keyword.data
        conditions = [{'field':form.field.data,
                       "value":q,
                       "operator":"like"}]
        if form.order.data == "1":
            order = {"field": "user_id","type":"asc"}
        else:
            order = {"field": "user_id", "type": "desc"}
    else:
        conditions = {}
        order = None


    res = UserService.get_many(conditions, order, page)
    users = res['items']
    pageList = res['iter_pages']
    pages = res['pages']
    total = res['total']
    return render_template("admin/user/user_list.html", users=users,
                           pageList=pageList, pages=pages,
                           total=total, form=form,
                           vip_type=VIP_TYPE
                           )


# 根据用户id删除用户
@admin_module.route("/user/delete", methods=['post'])
def delete_user():
    csrf.protect()
    user_id = int(request.form.get("user_id"))
    message = {"result":"fail"}
    try:
        UserService.delete_by_id(user_id)
    except Exception as e:
        message['error'] = e
    else:
        message['result'] = "success"
    return jsonify(message)


# 用户信息修改
@admin_module.route("/user/edit/<int:user_id>", methods=['get', 'post'])
def edit_user(user_id):
    form = UserInfoEditForm()
    user = UserService.get_one_by_id(user_id)

    if form.validate_on_submit():
        message = {"res":"fail"}
        user.realname = form.data['name']
        user.sex = form.data['sex']
        user.mylike = "|".join(form.data['like'])
        user.city = form.data['city']
        user.intro = form.data['intro']
        try:
            UserService.update(user ,{})
        except Exception as e:
            print(e)
        else:
            message['res'] = "success"
        return jsonify(message)
    elif form.errors:
        print(form.errors)
    else:
        form.email.data = user.email
    return render_template("admin/user/user_edit.html", user_id=user_id, form=form)


# 用户认证审核
@admin_module.route("/user/user_approval", methods=["post"])
def approval_user():
    csrf.protect()
    user_id = int(request.form.get("user_id"))
    message = {"result":"fail"}
    user = UserService.get_one_by_id(user_id)
    if user is None:
        return jsonify(message)
    try:
        user.is_approve = 1
        UserService.update(user)
    except Exception as e:
        message['error'] = e
        return jsonify(message)
    else:
        message['result'] = "success"
        return jsonify(message)
