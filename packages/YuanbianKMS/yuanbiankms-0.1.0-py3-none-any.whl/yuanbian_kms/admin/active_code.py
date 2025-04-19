# -*- coding=utf-8 -*-
import random
from flask import render_template, jsonify
from xp_cms.admin.__main__ import admin_module
from xp_cms.forms.acive_code_form import ActiveCodeForm, ActiveCodeSearchForm
from xp_cms.services.user_service import ActiveCodeService, ActiveCodeUseLogService


@admin_module.route("/active_code/generate", methods=["GET", "POST"])
def active_code_generate():
    form = ActiveCodeForm()
    if form.validate_on_submit():
        active_type = form.data.get("active_type")
        code_numbers = form.data.get('code_numbers')
        expiration = form.data.get("expiration")
        channel = form.data.get("channel")
        n = 0
        for code in generate_codes(active_type, code_numbers):
            result = ActiveCodeService.add_by_dicts({
                "code"       : code,
                "active_type": active_type,
                "expiration" : expiration,
                "channel"    : channel
            })
            if result:
                n += 1
        return jsonify({"code_numbers": code_numbers, "success_numbers": n})
    elif form.errors:
        print(form.errors)

    return render_template("admin/active_code/generate.html",
                           form=form)


@admin_module.route("/active_code/manage", methods=["GET", "POST"])
def active_code_manage():
    form = ActiveCodeSearchForm()
    res = None
    search_type = "0"
    if form.validate_on_submit():
        search_type = "1" if form.data.get("search_type") == "1" else "0"
        if search_type == "1":
            res = load_active_log(form)
        else:
            res = load_active_code(form)

        if form.data.get(""):
            pass
    form.search_type.data = search_type

    return render_template("admin/active_code/manage.html",
                           form=form,
                           res=res)


def generate_codes(type, number):
    code_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    start_char = {1: "Y", 3: "U", 6: "A", 12: "N", 24: "B", 1200: "I"}
    for i in range(number):
        yield start_char.get(type) + "".join(random.choices(code_string, k=7))


def load_active_code(form):
    code = form.data.get("code")
    if code:
        res = ActiveCodeService.get_many([{"field": "code", "value": code, "operator": "eq"}])
    else:
        channel = form.data.get("channel")
        active_type = form.data.get("active_type")
        res = ActiveCodeService.get_many([{"field"   : "active_type",
                                           "value"   : active_type,
                                           "operator": "eq"},
                                          {"field"   : "channel",
                                           "value"   : channel,
                                           "operator": "eq"},
                                          ])
    return res


def load_active_log(form):
    channel = form.data.get("channel")
    active_type = form.data.get("active_type")
    res = ActiveCodeUseLogService.get_many([{"field"   : "active_type",
                                             "value"   : active_type,
                                             "operator": "eq"},
                                            {"field"   : "channel",
                                             "value"   : channel,
                                             "operator": "eq"},
                                            ])

    return res
