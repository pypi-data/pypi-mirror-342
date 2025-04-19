# -*- coding=utf-8 -*-
from flask import request, jsonify
from flask_login import current_user, login_required
from ..__main__ import chatgpt_app
from quick_encrypt.quick_aes import encode_data, decode_data
from xp_cms.services.user_service import UserService, ChatGPTAPIKeyService
from xp_cms.extensions import nosql, csrf
# from xp_cms.member.api import do_generate_api_key
from xp_cms.auth.utils import add_user
from ..chatgpt_service import YuanbianChatAPI


REMOTE_CHANNEL_API_KEY = '2e5If2SBiXmnfsKe'


# @csrf.exempt
# @chatgpt_app.route("/create_user", methods=["POST"])
# def create_user():
#     message = ""
#     try:
#         data = decode_data(request.form['data'], REMOTE_CHANNEL_API_KEY)
#     except Exception as e:
#         message = "数据无法正确解析"
#         user = None
#     else:
#         try:
#             user_info = {
#                 "username": "_".join([data['channel'], data["username"]]),
#                 "password_origin": data["password"],
#                 "mobile": ""
#             }
#             user = add_user(**user_info)
#         except Exception as e:
#             message = "建立用户档案出错"
#             user = None
#     if user:
#         return jsonify({
#             "result": 1
#         })
#     else:
#         return jsonify({
#             "result" : 0,
#             "message": message
#         })
#

# @csrf.exempt
# @chatgpt_app.route("/refresh_user_api_key", methods=["POST"])
# def get_user_api_key():
#     try:
#         data = decode_data(request.form['data'], REMOTE_CHANNEL_API_KEY)
#     except Exception:
#         return "", 403
#     else:
#         user = UserService.get_user_by_username("_".join([data['channel'], data['username']]))
#         if not user:
#             return "", 403
#     api_secret_key = do_generate_api_key(user.user_id)
#     return jsonify({"app_key"   : api_secret_key.app_key,
#                     "app_secret": api_secret_key.app_secret})


