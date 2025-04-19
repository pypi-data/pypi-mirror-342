# -*- coding=utf-8 -*-
from uuid import uuid4
import json
from urllib.parse import quote, urljoin, urlunparse
from flask import render_template, url_for, \
    request, g, session, redirect, current_app
from flask_login import login_user
from xp_cms.utils import redirect_back
from xp_cms.extensions import nosql, csrf, wechat_db
from xp_wechat.wechat_message_api import WechatMessageApi
from .utils import create_verify_code
from xp_cms.auth.auth_blueprint import AuthManage
from xp_wechat.wechat_official_api import WechatOfficialApi
from xp_cms.cores.xp_oauth.wechat.wechat_login import LoginByWechat
from xp_cms.cores.xp_oauth.wechat.wechat_user_info import WechatUserInfo


@AuthManage.route("/wx_verifier", methods=['get'])
def wx_verifier():
    if WechatOfficialApi.verier(request.args):
        return request.args.get('echostr')
    else:
        return ""

@csrf.exempt
@AuthManage.route("/wx_verifier", methods=['post'])
def wx_verifier_post():
    if WechatOfficialApi.verier(request.args):
        msg_type, data = WechatOfficialApi.wechat_verier_post(request.data.decode())
        return getattr(WechatMessageApi, msg_type)(data)
    else:
        return "..."


'''微信登录'''
@AuthManage.route("/wechat_login")
def wechat_login():
    session['redirect_url'] = request.args.get("next")
    direct_url = quote(urlunparse(("https", request.host, url_for("auth.wechat_login"), "", "", "")))
    code = request.args.get("code", None)
    state = request.args.get("state", None)
    if state != session.get("state", False):
        code = None
        state = session['state'] = uuid4().hex

    login_client = LoginByWechat(g.client)
    res = login_client.login(code, direct_url, state)
    if "jump_url" in res:
        return redirect(res['jump_url'])
    else:
        bind_user = WechatUserInfo.wechat_check_bind(res)
        if bind_user is None:
            session['wechat_oauth'] = {'unionid': res['unionid'],
                                       'nickname': res['nickname']}
            return redirect(url_for("auth.bind_select"))
        else:
            login_user(bind_user)
            return redirect_back()


# 微信公众号验证码服务
@AuthManage.route("/verify")
def official_verify():
    """微信公众号验证服务
    :return:
    """
    create_verify_code()
    return render_template("auth/subscribe.html",
                           code_number=session['verify_code']['code_number']
                           )


@AuthManage.route("/get_verify_code")
def get_verify_qrcode():
    # if session.get("register") is None:
    #     redirect(url_for(".official_verify"))
    create_verify_code()
    scene_str_id = session["wechat_scene_str_id"]
    try:
        token = wechat_db.get("wechat_access_token")
        assert token != None
    except Exception as e:
        current_app.logger.error(e)
        return "sorry，微信认证服务器出现故障，稍后再试", 404
    else:
        token = json.loads(token)['access_token']
    return WechatOfficialApi.get_qrcode(token, scene_str_id)



# 公众号扫码登录 discard
# @AuthManage.route("/check_subscribe")
# def check_subscribe():
#     # 必须有公众号扫码场景id session["wechat_scene_str_id"]
#     message = {"state": False, "jump_url": ""}
#     if not session.get("wechat_scene_str_id"):
#         message['jump_url'] = "404"
#         return message
#
#     scene_str_id = request.args.get("id")
#     # 检查场景id是否一致
#     if scene_str_id == session["wechat_scene_str_id"]:
#         # 根据id检查oauth信息，如果查询到，说明已经根据此id进行了扫码关注
#         # 第一次关注会写入oauth表
#         # 关注后重复扫码会更新oauth表的场景id
#         oauth = WechatOAuthService.get_one_by_field(("qr_scene_str", scene_str_id))
#         # 如果已经绑定会员号直接登陆
#         if oauth and oauth.user:
#             login_user(oauth.user)
#             message['state'] = True
#             message['jump_url'] = session.get('wechat_login_referrer') or url_for("index")
#             session.pop("wechat_scene_str_id")
#             session.pop("wechat_login_referrer")
#             return jsonify(message)
#         # 如果没有绑定会员号，跳转到绑定选择页面
#         if oauth:
#             session["oauth"] = {"openid": oauth.openid, "nickname": oauth.nickname}
#             message['state'] = True
#             message['jump_url'] = url_for("auth.bind_select")
#             return jsonify(message)
#     else:
#         message['state'] = True
#         message['jump_url'] = url_for("auth.check_subscribe")
#
#     return jsonify(message)