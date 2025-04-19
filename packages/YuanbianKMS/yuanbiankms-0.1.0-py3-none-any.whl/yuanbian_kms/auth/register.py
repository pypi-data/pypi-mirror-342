# -*- coding=utf-8 -*-
from datetime import datetime
from flask import request, render_template, session, \
    url_for, redirect, flash, jsonify, current_app
from xp_cms.extensions import nosql
from xp_cms.services.user_service import UserService

from xp_cms.forms.auth_form import RegisterForm
from .auth_blueprint import AuthManage, AuthView
from .utils import check_username, check_robot, add_user
from .sms_service import validator_sms_code


class RegisterView(AuthView):
    template = "auth/register.html"

    def get(self):
        self._check_next_link()
        form = self._create_form()
        return render_template(self.template, form=form)

    def post(self):
        user = self._do_register()
        if user:
            return redirect(url_for(".login"))
        return redirect(request.full_path)

    def _do_register(self):
        form = self._create_form()
        user = None

        if form.validate_on_submit():
            validator_code = request.form.get("sms_code", "")
            mobile = form.mobile.data
            if not validator_sms_code(mobile, validator_code):
                flash("短信验证码不正确或者已经失效")
                return None

            user = {
                "username"     : form.username.data,
                "password_origin"     : form.password.data,
                "mobile"       : mobile
            }

            user = add_user(**user)
            # if user:
            #     login_user(user)
            #     session.pop("verify_code")
            if not user:
                flash("注册失败，您可能已经注册过！")
        elif form.errors:
            for field, error in form.errors.items():
                flash(",".join(error))
        return user

    def _create_form(self):
        form = RegisterForm()
        return form


AuthManage.add_url_rule("/register", view_func=RegisterView.as_view("register"))


@AuthManage.route('/check_username_useful')
def check_username_useful():
    message = {"result": False, "errors": {}}
    user_fingerprint = request.args.get("user_fingerprint", "")
    sign = request.args.get("sign", "")
    t = request.args.get("t", "")
    message = check_robot(user_fingerprint, sign, t, "username")
    return jsonify(message)


@AuthManage.route('/check_mobile_useful')
def check_mobile_useful():
    message = {"result": False, "errors": {}}
    user_fingerprint = request.args.get("user_fingerprint", "")
    sign = request.args.get("sign", "")
    t = request.args.get("t", "")
    message = check_robot(user_fingerprint, sign, t, "mobile")
    return jsonify(message)
