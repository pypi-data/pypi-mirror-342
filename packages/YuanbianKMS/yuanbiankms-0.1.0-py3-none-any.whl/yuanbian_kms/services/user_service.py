# -*- coding=utf-8 -*-
from datetime import datetime, timedelta
from flask import current_app
from xp_cms.services.base_service import XPService
from xp_cms.models.user import User, WechatOAuth
from xp_cms.models.account import Account
from xp_cms.models.user import ActiveCode, ActiveCodeUseLog
from xp_cms.services.account_service import AccountService
from xp_cms.models.user import ChatGPTAPIKey


class UserService(XPService):
    model = User

    @classmethod
    def get_user_by_id(cls, user_id):
        user = cls.get_one_by_id(user_id)
        return user

    @classmethod
    def get_user_by_username(cls, username):
        user = cls.get_one_by_field(("username", username))
        return user

    @classmethod
    def get_user_by_mobile(cls, mobile):
        user = cls.get_one_by_field(("mobile", mobile))
        return user

    @classmethod
    def login_check(cls, username, password):
        user = cls.get_one_by_field(("username", username))
        if user and user.validate_password(password):
            return user
        else:
            return False

    @classmethod
    def add(cls, obj):
        password = obj.pop("password_origin")
        user = cls.model(**obj)
        user.set_password(password)
        account = {
            "points" : 200,
            "balance": 0
        }
        user.account = Account(**account)
        return super().add(user)

    @classmethod
    def add_bind_wechat(cls, obj, oauth):
        user = cls.model(**obj)
        user.set_password(obj['password_hash'])
        user.oauth = oauth
        return super().add(user)

    @classmethod
    def update_bind_wechat(cls, user, oauth):
        user.oauth = oauth
        return super().update(user)

    @classmethod
    def update_login_info(cls, user, login_ip, login_time):
        return cls.update_columns(conditions={"user_id": user.user_id},
                                  fields={"last_login_ip"  : login_ip,
                                          "last_login_time": login_time})

    @classmethod
    def upgrade_vip_level(cls, user, expiration, vip_level=1):
        current_time = datetime.today()
        if user.vip_expiration:
            current_expiration = user.vip_expiration if user.vip_expiration > current_time else current_time
        else:
            current_expiration = current_time
        user.vip_type = vip_level
        if vip_level != 0:
            user.vip_expiration = current_expiration + timedelta(31 * expiration)
        else:
            user.vip_expiration = None
        return cls.update(user)


class WechatOAuthService(XPService):
    model = WechatOAuth

    @classmethod
    def get_one_by_unionid(cls, unionid):
        obj = cls.get_one_by_field(("unionid", unionid))
        return obj

    @classmethod
    def update_by_unionid(cls, data):
        obj = cls.get_one_by_field(("unionid", data['unionid']))

        for k, v in data.items():
            setattr(obj, k, v)
        try:
            cls.update(obj)
        except Exception as e:
            current_app.logger.error(e)
            return None

        return obj

    @classmethod
    def delete_by_unionid(cls, unionid):
        obj = cls.get_one_by_field(("unionid", unionid))
        try:
            cls.delete(obj)
        except Exception as e:
            current_app.logger.error(e)
            return False
        return True


class ActiveCodeService(XPService):
    model = ActiveCode


class ActiveCodeUseLogService(XPService):
    model = ActiveCodeUseLog


class ChatGPTAPIKeyService(XPService):
    model = ChatGPTAPIKey
