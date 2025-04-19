# -*- coding=utf-8 -*-
import json
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..__main__ import chatgpt_app
from ..chatgpt_utils import load_user_chatlog, load_user_logs, create_new_chatlog
from .chat_common.chat_stream import _gen_chat
from xp_cms.extensions import csrf


# ################################
# pc端对话 - 依靠cookie完成身份认证  #
# ################################
AI_TYPES = [
    {"type": "资深编程工程师", "option": "您的角色是一名资深的软件工程师， 将帮助回答编程领域的任何问题，凡是回答中，涉及到代码示例的，务必标注对应的编程语言"},
    {"type": "资深职场导师", "option": "您的角色是一名资深的职场发展导师， 将帮助回答职业的发展方向，人事关系处理等等问题"},
    {"type": "论文助手", "option": "您的角色是研究生导师， 以研究生导师的眼光给出论文的建议，或者具体的一些编写内容，以及论文可参考的数据与来源"},
    {"type": "文档助手", "option": "您的角色是一个内容丰富的知识库， 需要您帮助获取相关文档的资料"}
]
@chatgpt_app.route("/playground")
def chatgpt():
    """ChatGPT PlayGround界面"""
    is_login = True
    if current_user.is_anonymous:
        is_login = False
    ai_type = request.args.get("ai_type", "0")
    try:
        ai_type_idx = int(ai_type)
        assert ai_type_idx in [0, 1, 2, 3]
    except:
        ai_type_idx = 0
    ai_type = AI_TYPES[ai_type_idx]
    return render_template("playground.html", is_login=is_login, ai_type=ai_type)

@chatgpt_app.route("/")
def chat_page_index():
    is_login = True
    if current_user.is_anonymous:
        is_login = False
    return render_template("chatgpt_index.html", is_login=is_login)


@chatgpt_app.route("/chat_code")
@login_required
def chat_code():
    """在线coding 辅助AI界面
    :return:
    """
    is_login = True
    if current_user.is_anonymous:
        is_login = False
    return render_template("yuanbian_ai.html", is_login=is_login)


@chatgpt_app.route("new_session", methods=["POST"])
@login_required
def create_new_session():
    """创建新对话
    :return: 新对话的log_id
    """
    return create_new_chatlog(current_user.user_id)


@chatgpt_app.route("chat_logs", methods=["GET"])
@login_required
def load_chat_logs():
    """加载对话记录"""
    return jsonify(load_user_logs(current_user.user_id))


@csrf.exempt
@chatgpt_app.route("search_logs", methods=["POST"])
@login_required
def search_chat_logs():
    """对话记录搜索"""
    keyword = request.form.get("keyword", "")
    return jsonify(load_user_logs(current_user.user_id, keyword))


@chatgpt_app.route("load_log_detail", methods=["GET"])
@login_required
def load_log_detail():
    """对话记录详细"""
    log_id = request.args.get("log_id", None)
    if log_id:
        return jsonify(load_user_chatlog(log_id, current_user.user_id).chat_content)
    return jsonify({})


@chatgpt_app.route("/chat", methods=["get"])
@login_required
def chat():
    """ChatGPT SSE 接口"""
    return _gen_chat(current_user.user_id, current_user.username)



# @stream_with_context
# def flush_img_content():
#     """ChatGPT AI Image"""
#     prompt = request.args.get('prompt')
#     if not prompt:
#         for reminder in prompt_reminder():
#             yield reminder
#         return
#     if chat_billing():
#         for reminder in billing_reminder():
#             yield reminder
#         return
#
#     for content in call_openai_imgmodel(prompt):
#         yield content


# @chatgpt_app.route("/generate_image", methods=["get"])
# @login_required
# def generate_image():
#     """生成图片 SSE 接口"""
#     return Response(flush_img_content(), mimetype='text/event-stream')





