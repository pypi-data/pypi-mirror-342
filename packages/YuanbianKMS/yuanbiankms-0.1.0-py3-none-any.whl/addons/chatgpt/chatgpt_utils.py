# -*- coding=utf-8 -*-
from hashlib import md5, sha256
import hmac
import json
import time
import base64
from datetime import datetime
# import grpc
from flask import request, jsonify
from flask_login import current_user
from xp_cms.services.account_service import AccountService
from xp_cms.services.chatgpt_service import ChatGPTLogService
from xp_cms.services.user_service import ChatGPTAPIKeyService
from xp_cms.extensions import nosql

# import yuanbian_ai_pb2
# import yuanbian_ai_pb2_grpc


billing_reminder_message = "ChatGPT可用次数已经用完！，每天登录可以奖励5000GPT算力"
newchat_reminder_messsage = "请点击左上角创建新的对话"
prompt_reminder_message = "问的好才会答的好，请输入您的问题！"
sign_fail_reminder_message = "签名验证失败，请求非法"
ip_fail_reminder_message = "ip访问限制"


# 提醒信息
def billing_reminder():
    yield out_sse_data(billing_reminder_message)
    yield f"event:runout\ndata:close\n\n"
    yield f"event:close\ndata:close\n\n"


def newchat_reminder():
    yield out_sse_data(newchat_reminder_messsage)
    yield f"event:close\ndata:close\n\n"


def prompt_reminder():
    yield out_sse_data(prompt_reminder_message)
    yield f"event:close\ndata:close\nid:{time.monotonic_ns()}\n\n"


def sign_fail_reminder():
    yield out_sse_data(sign_fail_reminder_message)
    yield f"event:close\ndata:close\nid:{time.monotonic_ns()}\n\n"


def ip_fail_reminder():
    yield out_sse_data(ip_fail_reminder_message)
    yield f"event:close\ndata:close\nid:{time.monotonic_ns()}\n\n"


def out_sse_data(data):
    # data = base64.b64encode(data.encode()).decode("utf-8")
    data = json.dumps({"content": data}).replace("\n", "\\u000A")
    return f"event:message\ndata:{data}\nid:{time.monotonic_ns()}\n\n"

# #################################
# 对话记录处理
# #################################
# 加载用户对话记录
def load_user_chatlog(session_id, user_id=None):
    if not user_id:
        user_id = current_user.user_id
    try:
        chatlog = ChatGPTLogService.get_user_log_detail(session_id, user_id)
    except Exception as e:
        return
    else:
        return chatlog


def load_user_logs(user_id=None, keyword=None):
    if not user_id:
        user_id = current_user.user_id
    if keyword:
        logs = ChatGPTLogService.find_log_by_keyword(user_id, keyword)
    else:
        logs = ChatGPTLogService.get_user_logs(user_id)
    logs_list = []
    for log in logs.items[::-1]:
        chat_content = log.chat_content
        if chat_content:
            logs_list.append(
                {"log_id": str(log.id), "title": chat_content[0]['content'], "chatgpt": chat_content[1]['content']})
    return logs_list


# 创建新的对话
def create_new_chatlog(user_id):
    ChatGPTLogService.delete_empty_userlog(user_id)
    new_chat_log = ChatGPTLogService.add({"user_id"     : user_id,
                                          "chat_date"   : datetime.now(),
                                          "chat_content": []})
    return jsonify({"session_id": str(new_chat_log.pk)})


# 保存对话
def save_chat_data(session_id, user_id, prompt, openai_response_content):
    user_prompt = {"role": "user", "content": prompt}
    openai_response = {"role": "assistant", "content": openai_response_content}
    return ChatGPTLogService.add_new_chat(session_id, user_id, user_prompt, openai_response)


# 对话前检查
def check_prompt():
    prompt = request.args.get('user_prompt')
    keep = request.args.get('keep', "0")
    if not prompt:
        return True, prompt_reminder()

    if chat_billing():
        return True, billing_reminder()


# ###############################################
# 调用openai
# ##############################################
def make_chatgpt_messages(last_log, assistant, prompt, username, model):
    user = md5(username.encode()).hexdigest()
    messages = []
    messages.extend(last_log)
    messages.extend([{"role": "system", "content": "如无特殊说明，给出的程序代码示例需要明确标识语言类别"}])
    messages.extend([{"role": "user", "content": prompt}])
    if model.startswith("gpt"):
        messages.extend([{"role": "assistant", "content": assistant}])
    return user, messages


# def make_chatgpt_prompt(last_log, assistant, prompt, user_id=None):
#     if user_id:
#         user = md5(str(user_id).encode()).hexdigest()
#     else:
#         user = md5(current_user.username.encode()).hexdigest()
#     ai_prompt = yuanbian_ai_pb2.Prompt(
#         user=user,
#         prompt=json.dumps({"last_log": last_log, "assistant": assistant, "prompt": prompt})
#     )
#     return ai_prompt


# def call_openai_chatmodel(last_log, assistant, prompt, log_id=None, user_id=None):
#     if not user_id:
#         user_id = current_user.user_id
#     server_port = '47.89.253.20:10088'
#     openai_response_content = ""
#     ai_prompt = make_chatgpt_prompt(last_log, assistant, prompt, user_id)
#     try:
#         with grpc.insecure_channel(server_port) as channel:
#             stub = yuanbian_ai_pb2_grpc.YuanbianAIStub(channel)
#             for content in stub.CallOpenAI(ai_prompt):
#                 data = content.content
#                 openai_response_content += data
#                 yield out_sse_data(data)
#     except Exception as e:
#         with open("ai_run_error.log", "a+") as f:
#             f.write(str(e))
#     finally:
#         yield out_sse_data(" ")
#
#     yield f"event:close\ndata:close\n\n"
#     if log_id and openai_response_content:
#         save_chat_data(log_id, user_id, prompt, openai_response_content)


# def call_openai_imgmodel(prompt):
#     user = md5(current_user.username.encode()).hexdigest()
#     ai_prompt = yuanbian_ai_pb2.Prompt(
#         user=user,
#         prompt=prompt
#     )
#     with grpc.insecure_channel('47.89.210.173:10088') as channel:
#         stub = yuanbian_ai_pb2_grpc.YuanbianAIStub(channel)
#
#         for content in stub.CallOpenAICreateImage(ai_prompt):
#             yield out_sse_data(content.content)
#
#     yield f"event:close\ndata:close\n\n"


# #######################################
# 第三方接口验签
# #######################################

def gen_sign(params, api_secret):
    params_str = '&'.join([k + '=' + str(params[k]) for k in sorted(params.keys())])
    signature = hmac.new(api_secret.encode(), params_str.encode(), sha256).hexdigest()
    return signature


def get_api_key(api_key):
    api_secret_key = nosql.redis_client.hgetall("yuanbian_ai_" + api_key)
    if not api_secret_key:
        api_secret_key = ChatGPTAPIKeyService.get_one_by_field(("app_key", api_key))
        if api_secret_key:
            api_secret = api_secret_key.app_secret
            user_id = api_secret_key.user_id
            nosql.redis_client.hmset("yuanbian_ai_" + api_key,
                                     {"api_secret": api_secret, "user_id": user_id}, 24 * 3600)
            api_secret_key = {
                "user_id"   : api_secret_key.user_id,
                "api_secret": api_secret_key.api_secret,
                "api_key"   : api_secret_key.api_key
            }
    return api_secret_key


def verify_request_validity(params):
    api_key = params.get("api_key", "")
    # args = {
    #     "prompt"    : request.args.get("prompt"),
    #     "api_key"   : api_key,
    #     "t"         : request.args.get("t"),
    #     "session_id": request.args.get("session_id")
    # }
    api_secret = get_api_key(api_key)
    if not api_secret:
        return False
    _sign = gen_sign(params, api_secret['api_secret'])
    if _sign != request.args.get('sign'):
        return False
    return api_secret


# 一个补丁用于处理url中加密数据出现的=
def pad_base64(encoded_str):
    padding = ""
    padding_length = len(encoded_str) % 4

    if padding_length == 1:
        padding = "="
    elif padding_length == 2:
        padding = "=="
    else:
        padding = "==="

    return encoded_str + padding