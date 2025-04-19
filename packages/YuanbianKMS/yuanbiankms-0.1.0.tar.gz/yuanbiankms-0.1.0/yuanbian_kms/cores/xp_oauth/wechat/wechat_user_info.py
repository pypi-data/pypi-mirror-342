# -*- coding=utf-8 -*-
import json
from flask import current_app
from  xp_cms.services.user_service import UserService, WechatOAuthService


class WechatUserInfo:
    @classmethod
    def bind_user_to_unionid(cls, user, unionid):
        oauth = WechatOAuthService.get_one_by_field(("unionid", unionid))
        # 新注册的会员，user为表单数据
        if type(user) == dict:
            sex = oauth.sex
            country = oauth.country
            province = oauth.province
            city = oauth.city
            user.update({
                    "sex"          : sex,
                    "country"      : country,
                    "province"     : province,
                    "city"         : city,
                    })

            user = UserService.add_bind_wechat(user, oauth)
        # 登录绑定会员，数据为会员数据对象
        else:
            user.sex = oauth.sex
            user.country = oauth.country
            user.province = oauth.province
            user.city = oauth.city
            user = UserService.update_bind_wechat(user, oauth)
        return user

    @classmethod
    def save_wechat_info(cls, wechat_info):
        """:arg"""

        if "language" in wechat_info:
            wechat_info.pop('language')
        if "subscribe_time" in wechat_info:
            wechat_info.pop('subscribe_time')
        if "subscribe_scene" in wechat_info:
            wechat_info.pop('subscribe_scene')
        if "qr_scene" in wechat_info:
            wechat_info.pop('qr_scene')
        if "privilege" in wechat_info:
            wechat_info.pop('privilege')
        if "tagid_list" in wechat_info:
            wechat_info['tagid_list'] = json.dumps(wechat_info['tagid_list'])

        try:
            wechat_oauth = WechatOAuthService.add_by_dicts(wechat_info)
        except Exception as e:
            current_app.logger.error(e)
            return None
        return wechat_oauth

    @classmethod
    def wechat_check_bind(cls, data):
        oauth = WechatOAuthService.get_one_by_field(("unionid", data['unionid']))
        if oauth is None:
            oauth = cls.save_wechat_info(data)
        else:
            oauth = WechatOAuthService.update_by_unionid(data)

        return oauth.user

