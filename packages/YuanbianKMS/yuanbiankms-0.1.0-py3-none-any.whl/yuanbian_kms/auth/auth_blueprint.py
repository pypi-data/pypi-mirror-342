# -*- coding=utf-8 -*-
from urllib.parse import urlparse
from flask import Blueprint, current_app, request, redirect, url_for, session
from flask_login import current_user
from flask.views import View
from xp_cms.extensions import csrf

AuthManage = Blueprint("auth", __name__)
csrf.exempt(AuthManage)


class AuthView(View):
    methods = ["GET", "POST"]
    _check_list = []

    def dispatch_request(self, *args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        meth = getattr(self, request.method.lower(), None)
        if meth is None:
            meth = getattr(self, "get", None)
        if self._check_view() is None:
            return redirect(url_for(".login"))
        assert meth is not None, "Unimplemented method %r" % request.method
        return meth(*args, **kwargs)

    def _check_view(self):
        return True

    def _check_next_link(self):
        next_url = request.args.get("next", None)
        if next_url:
            if next_url not in ["/mall/fast_pay"]:
                session['redirect_url'] = next_url
            else:
                session['redirect_url'] = "/upgrade2vip"
        elif request.referrer is None:
            session['redirect_url'] = url_for("index")
        elif urlparse(request.referrer).path not in [url_for('.register'), url_for('.login')]:
            session['redirect_url'] = request.referrer
