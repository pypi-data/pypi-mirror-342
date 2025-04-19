# -*- coding: utf-8 -*-
from datetime import datetime
from functools import wraps
# from flask_bootstrap import Bootstrap
from flask import redirect, url_for, current_app, request
from flask_ckeditor import CKEditor
from flask_login import LoginManager, current_user
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_whooshee import Whooshee
from flask_dropzone import Dropzone
from xp_cms.libs.sqlalchemy_cluster import RoutingSQLAlchemy
from flask_redis import FlaskRedis
from flask_nosql import FlaskNoSQL
from flask_elasticsearch import FlaskES
from xp_upload import XpUpload
from xp_pay.alipay.create_pay import Alipay
from xp_pay.wxpayv3.create_pay import Wxpay
from flask_mongoengine import MongoEngine
from xp_cms.cores.aliyun_sms import YuanbianSMS
from flask_jwt_extended import JWTManager
from xp_cms.cores.aliyun_check_robot import AliyunCaptchaRequest


db = RoutingSQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
# moment = Moment()
toolbar = DebugToolbarExtension()
migrate = Migrate(compare_type=True, compare_server_default=True)
whooshee = Whooshee()
dropzone = Dropzone()
redis = FlaskRedis()
nosql = FlaskNoSQL()
es = FlaskES()
mongodb = MongoEngine()
wechat_db = FlaskRedis(config_prefix="WECHAT_TOKEN_DB")
alipay = Alipay()
wxpay = Wxpay()
xp_upload = XpUpload()
yuanbian_sms_service = YuanbianSMS("LTAI5tLcfPx9Jbfvy1pRHH9t", "QeKAWmFMxvadIHFRNykYNPZF4SPxZW")
jwt = JWTManager()
aliyun_captcha_request = AliyunCaptchaRequest()

@login_manager.user_loader
def load_user(user_id):
    from xp_cms.services.user_service import UserService
    user = UserService.get_one_by_id(int(user_id))
    if user.vip_type > 0:
        if user.vip_expiration and user.vip_expiration < datetime.now():
            UserService.upgrade_vip_level(user, None, 0)

    return user

def is_vip(func):
    @wraps(func)
    def check_vip(*args, **kwargs):
        if current_user.is_anonymous:
            return redirect(url_for("auth.login"))
        if current_user.vip_type <= 0:
            return redirect(url_for("auth.upgrade2vip"))
        return func(*args, **kwargs)
    return check_vip


login_manager.login_view = 'auth.login'
login_manager.login_message = '您还没有登录，请先登录!'
login_manager.login_message_category = 'info'

RUN_TYPE = [("term", "term"),
            ("html", "html"),
            ("python", "python"),
            ("notebook", "notebook"),
            ("mysql", 'mysql'),
            ("mongodb", "mongodb"),
            ("redis", "redis"),
            ("python_mysql", "python_mysql"),
            ("python_mongodb", "python_mongodb"),
            ("python_redis", "python_redis")
            ]
