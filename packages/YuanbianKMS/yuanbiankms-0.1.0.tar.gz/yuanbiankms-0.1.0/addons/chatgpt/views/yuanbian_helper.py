# -*- coding=utf-8 -*-
import json
import time
from flask import request, render_template, Response, \
    current_app, stream_with_context, jsonify
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from quick_encrypt.quick_aes import encode_data, decode_data
from ..__main__ import chatgpt_app
from ..chatgpt_service import YuanbianChatAPI
from ..chatgpt_utils import prompt_reminder_message, create_new_chatlog, \
    newchat_reminder_messsage, make_chatgpt_messages, pad_base64
from ..chatgpt_utils import load_user_chatlog, load_user_logs, create_new_chatlog
from .chat_common.chat_stream import _gen_chat
from xp_cms.services.user_service import ChatGPTAPIKeyService
from xp_cms.extensions import csrf



# ##############################
# 插件内置页面                   #
# 认证方式基于jwt方式             #
# ##############################

@chatgpt_app.route("yuanbian_helper/")
def helper_index():
    """插件页面"""
    my_key = None
    if current_user.is_authenticated:
        my_key = ChatGPTAPIKeyService.get_one_by_field(("user_id", current_user.user_id))
    return render_template("yuanbian_helper/chat.html", my_key=my_key)


@chatgpt_app.route("yuanbian_helper/new_session", methods=["GET"])
@jwt_required()
def create_new_session_by_jwt():
    """创建新的对话"""
    _current_user = get_jwt_identity()
    return create_new_chatlog(_current_user['user_id'])


@chatgpt_app.route("yuanbian_helper/chat_logs", methods=["GET"])
@jwt_required()
def load_chat_logs_by_jwt():
    """加载对话记录"""
    _current_user = get_jwt_identity()
    return jsonify(load_user_logs(_current_user['user_id']))


@csrf.exempt
@chatgpt_app.route("yuanbian_helper/search_logs", methods=["POST"])
@jwt_required()
def search_chat_logs_by_jwt():
    """对话记录搜索"""
    _current_user = get_jwt_identity()
    keyword = request.form.get("keyword", "")
    return jsonify(load_user_logs(_current_user['user_id'], keyword))


@chatgpt_app.route("yuanbian_helper/load_log_detail", methods=["GET"])
@login_required
def load_log_detail_by_jwt():
    """对话记录详细"""
    log_id = request.args.get("log_id", None)
    _current_user = get_jwt_identity()
    if log_id:
        return jsonify(load_user_chatlog(log_id, _current_user.user_id).chat_content)
    return jsonify({})


@chatgpt_app.route("yuanbian_helper/sse_token")
@jwt_required()
def get_sse_token():
    """插件端sse发送的认证信息"""
    _current_user = get_jwt_identity()
    data = {
        "t"       : time.time_ns(),
        "user_id" : _current_user['user_id'],
        "username": _current_user['username'],
        "time"    : time.time_ns()
    }
    data = encode_data(data, current_app.config.get("SSO_SECRET_KEY")).rstrip("=")
    return jsonify({"token": data})


@stream_with_context
def exec_chatgpt(model, assistant, prompt, keep, session_id, _current_user):
    if not prompt:
        yield YuanbianChatAPI.out_sse_data(event="message", data=prompt_reminder_message)
        yield YuanbianChatAPI.out_sse_data(event="close")
        return

    chat_log = YuanbianChatAPI.load_chat_log(session_id, _current_user['user_id'])
    if not chat_log:
        yield YuanbianChatAPI.out_sse_data(event="message", data=newchat_reminder_messsage)
        yield YuanbianChatAPI.out_sse_data(event="close")
        return

    if keep == "1":
        last_log = YuanbianChatAPI.get_last_log(chat_log, is_dumps=False)
    else:
        last_log = []
    messages = []
    messages.extend(last_log)
    ai_user, ai_messages = make_chatgpt_messages(last_log, assistant, prompt, _current_user['username'])
    api_key = ChatGPTAPIKeyService.get_one_by_field(("user_id", _current_user['user_id']))
    openai_key = api_key.app_key if api_key else None
    yuanbian_chat_api = YuanbianChatAPI(_current_user, model, key=openai_key, log_id=session_id)
    try:
        for content in yuanbian_chat_api.call_openai_chat(ai_user, ai_messages):
            yield content
    except Exception as e:
        with open("ai_run_error.log", "a+") as f:
            f.write(str(e))
    finally:
        yield YuanbianChatAPI.out_sse_data(event="close")


# @chatgpt_app.route("yuanbian_helper/chat", methods=["get"])
# @login_required
# def helper_chat():
#     return _help_chat(current_user.user_id, current_user.username)


@chatgpt_app.route("yuanbian_helper/chat", methods=["get"])
def helper_chat():
    """基于token完成对话认证"""
    try:
        data = request.args.get("token", "")
        data = decode_data(pad_base64(data), current_app.config.get("SSO_SECRET_KEY"))
    except Exception as e:
        return "", 403
    else:
        if time.time() > data['time'] + 5:
            return "", 403

        return _gen_chat(data['user_id'], data['username'])

# def _help_chat(user_id, username):
#     session_id = request.args.get("session_id", 0)
#     assistant = request.args.get("assistant")
#     prompt = request.args.get('user_prompt', None)
#     keep = request.args.get('keep', "0")
#     model = request.args.get('model', "gpt3.5")
#     user = {"user_id": user_id, "username": username}
#     if model not in ["gpt3.5", "gpt4.0"]:
#         model = "gpt3.5"
#     model = {"gpt3.5": "gpt-3.5-turbo", "gpt4.0": "gpt-4"}[model]
#
#     return Response(exec_chatgpt(model, assistant, prompt, keep, session_id, user), mimetype='text/event-stream')
