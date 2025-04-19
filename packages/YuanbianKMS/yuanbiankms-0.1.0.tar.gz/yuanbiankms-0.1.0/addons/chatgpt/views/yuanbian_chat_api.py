# -*- coding=utf-8 -*-
# ##########################################
# 向第三方开放接口， 比如猿变学员自己编写接口     #
# ##########################################
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


@csrf.exempt
@chatgpt_app.route("add_openai_key", methods=["POST"])
@login_required
def add_openai_key():
    openai_key = request.form.get("new_key", "")
    organization_id = request.form.get("org_id")
    message = {"status": False}
    if len(openai_key) >= 51:
        try:
            result = YuanbianChatAPI.test_openai_key(openai_key)
        except Exception as e:
            pass
        else:

            api_key = ChatGPTAPIKeyService.get_one_by_field(("user_id", current_user.user_id))
            if api_key:
                api_key.app_key = openai_key
                ChatGPTAPIKeyService.update(api_key)
            else:
                openai_api_key = {
                    "user_id"     : current_user.user_id,
                    "app_key"     : openai_key,
                    "app_secret"  : "",
                    "organization": organization_id
                }
                api_key = ChatGPTAPIKeyService.add_by_dicts(openai_api_key, replace=True)
            if api_key:
                message = {"status": True, "key": api_key.app_key[:4] + "..." + api_key.app_key[-4:]}
    return jsonify(message)


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

# @chatgpt_app.route("/yuanbian_new_chat")
# def yuanbian_new_chat():
#     params = {
#         "api_key": request.args.get("api_key"),
#         "t"      : request.args.get("t")
#     }
#     app_secret = verify_request_validity(params)
#     if not app_secret:
#         return jsonify({})
#     new_chat_log = create_new_chatlog(app_secret['user_id'])
#     return jsonify({"session_id": str(new_chat_log.pk)})

# @chatgpt_app.route("yuanbian_chat_logs", methods=["GET"])
# def yuanbian_chat_logs():
#     params = {
#         "api_key": request.args.get("api_key"),
#         "t"      : request.args.get("t")
#     }
#     app_secret = verify_request_validity(params)
#     if not app_secret:
#         return jsonify({})
#     return jsonify(_load_chat_logs(app_secret.get("user_id")))


# @chatgpt_app.route("yuanbian_log_detail", methods=["GET"])
# def yuanbian_log_detail():
#     params = {
#         "api_key": request.args.get("api_key"),
#         "t"      : request.args.get("t"),
#         "log_id" : request.args.get("log_id")
#     }
#     app_secret = verify_request_validity(params)
#     if not app_secret:
#         return jsonify({})
#     log_id = request.args.get("log_id", None)
#     if log_id:
#         return _load_log_detail(log_id, app_secret.get("user_id"))
#     return jsonify({})

# @chatgpt_app.route("/yuanbian_chatgpt")
# def yuanbian_chatgpt():
#     params = {
#         "api_key"   : request.args.get("api_key"),
#         "t"         : request.args.get("t"),
#         "session_id": request.args.get("session_id")
#     }
#     return Response(flush_text_content(remote=True, params=params), mimetype='text/event-stream')
