# -*- coding=utf-8 -*-
import random
import string
import secrets
from flask import request, jsonify, render_template
from flask_login import current_user
from .member_module import member_module
from quick_encrypt.quick_aes import encode_data, decode_data
from xp_cms.extensions import nosql, csrf
from xp_cms.services.user_service import ChatGPTAPIKeyService



# @member_module.route("generate_api_key", methods=["POST"])
# def generate_api_key():
#     user_id = current_user.user_id
#     api_secret_key = do_generate_api_key(user_id)
#     return jsonify({"user_id"   : api_secret_key.user_id,
#                     "app_key"   : api_secret_key.app_key,
#                     "app_secret": api_secret_key.app_secret})


# @member_module.route("manage_api_key")
# def manage_api_key():
#     api_key = ChatGPTAPIKeyService.get_one_by_field(("user_id", current_user.user_id))
#     return render_template("member/pc/api_key/manage_api_key.html", api_key=api_key)


# def do_generate_api_key(user_id):
#     api_secret_key = ChatGPTAPIKeyService.get_one_by_field(("user_id", user_id))
#
#     def _gen_secret():
#         return "".join(random.choices(string.digits + string.ascii_letters, k=16))
#
#     if api_secret_key:
#         api_secret_key.app_secret = _gen_secret()
#         ChatGPTAPIKeyService.update(api_secret_key)
#     else:
#         api_secret_key = {
#             "user_id"   : user_id,
#             "app_key"   : secrets.token_hex(8).upper(),
#             "app_secret": _gen_secret()
#         }
#
#         api_secret_key = ChatGPTAPIKeyService.add_by_dicts(api_secret_key)
#     return api_secret_key






