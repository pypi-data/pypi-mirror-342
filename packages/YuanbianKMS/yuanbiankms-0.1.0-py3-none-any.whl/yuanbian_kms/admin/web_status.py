# -*- coding=utf-8 -*-
from flask import make_response
from xp_cms.admin.__main__ import admin_module


@admin_module.route("/web_status/list_status")
def list_status():
    pass
    # hosts_status = get_hosts_status
    # mongodb_status = get_mongodb_status()
    # mysql_status = get_mysql_status()
    # redis_status = get_redis_status()
    return make_response("ok")


def get_host_status():
    pass
    return make_response("ok")