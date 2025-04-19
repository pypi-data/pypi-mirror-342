# -*- coding=utf-8 -*-
import xmltodict
import json
from xp_cms.extensions import nosql


def to_xml(params, cdata=True, encoding='utf-8'):
    """ dict转xml """
    tag = '<{0}><![CDATA[{1}]]></{0}>' if cdata else '<{0}>{1}</{0}>'
    s = ''.join(tag.format(k, v) for k, v in params.items())
    return '<xml>{}</xml>'.format(s).encode(encoding)


def to_dict(content):
    """ xml转dict """
    data = xmltodict.parse(content).get('xml')
    if '#text' in data:
        del data['#text']
    return data


def get_access_token():
    token_data = nosql.get("wechat_access_token")
    token = json.loads(token_data)
    return token['access_token']


# def delete_wechat_info():
#     try:
#         WechatOAuthService.delete_by_openid(request.args.get("openid"))
#     except Exception as e:
#         print(e)
#         return False
#     else:
#         return True

# def update_wechat_info(data):
#     try:
#         if data.get('qr_sence_str'):
#             qr_sence_str = None
#         user_info = WechatOAuthService.update_by_unionid(data)
#     except Exception as e:
#         current_app.logger.error(e)
#         return None
#     else:
#         return user_info

# def get_oauth_info(unionid):
#     return WechatOAuthService.get_one_by_unionid(unionid)

# def help_bind(data):
#     user_info = update_wechat_info(data['FromUserName'], data['EventKey'])
#     if user_info is None:
#         # 需要记录扫描场景
#         user_info = save_wechat_info(get_wechat_info(eventkey=data['EventKey']))
#         if user_info is None:
#             message = "服务器故障，注册失败，请等待管理员修复！"
#         else:
#             message = "已经关注，请按照PC端提示继续完成微信号与会员账号的绑定，绑定后可以直接扫码登录"
#     elif user_info.user:
#         message = user_info.user.username + ", 欢迎您回到Python-XP.com"
#     else:
#         message = "需要继续完成绑定"
#     return message

def get_verify_code(key, openid):
    code_info = nosql.get(key)
    nosql.set(key + "_scan_openid", openid)
    if code_info is None:
        return "二维码已过期，请刷新页面！"
    code_info = code_info.split()
    message = "验证码ID:" + code_info[0] + "\r\n" + "验证码:" + code_info[1]
    return message
