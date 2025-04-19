# -*- coding=utf-8 -*-
import json
from hashlib import md5
import random
import time
import xml.etree.ElementTree as ET

from flask import request, session, jsonify, current_app
from aliyunsdkcore import client
from aliyunsdkafs.request.v20180112 import AuthenticateSigRequest
from aliyunsdkcore.profile import region_provider

from xp_cms.extensions import nosql, csrf, yuanbian_sms_service
from .auth_blueprint import AuthManage
from .utils import check_robot_sign
from xp_cms.extensions import aliyun_captcha_request


@AuthManage.route("/send_login_sms_code", methods=["POST"])
def send_login_sms_code():
    return _do_send_login_sms_code()


@csrf.exempt
@AuthManage.route("/send_login_sms_code_by_token", methods=["POST"])
def send_login_sms_code_by_token():
    return _do_send_login_sms_code()


def _do_send_login_sms_code():
    template_code = "SMS_276382202"
    if not send_sms_code(template_code):
        return jsonify({"result": False, "info": "请求过于频繁或者判断为非法请求，可以与管理员联系"})
    return jsonify({"result": True, "message": ""})


def send_sms_code(template_code):
    sign_name = "猿变实验室"
    ip = request.headers.get('X-Real-Ip') or request.remote_addr
    user_fingerprint = request.form.get("user_fingerprint", "")
    sign = request.form.get("sign", "")
    t = session['t']
    mobile = request.form.get("mobile")
    if not check_robot_sign(user_fingerprint, sign, t):
        return False
    if not check_sms_fq(user_fingerprint, ip, mobile):
        return False
    code = generate_sms_code(mobile)
    if not code:
        return False
    template_param = '{"code": "%s"}' % "".join(code)
    try:
        yuanbian_sms_service.main(sign_name, template_code, mobile, template_param)
    except Exception as e:
        current_app.logger.error(f"{mobile}发送验证码错误：{str(e)}")
        return False
    return True


def check_sms_fq(user_fingerprint, ip, mobile):
    redis_client = nosql.redis_client
    # 限制每个客户端每小时调用次数 =2
    # key = user_fingerprint_ip_hour
    fq_hour_key = "%s_%s_per_hour" % (user_fingerprint, ip)
    if not redis_client.get(fq_hour_key):
        redis_client.incr(fq_hour_key, 1)
        redis_client.expire(fq_hour_key, 3600)
    elif redis_client.get(fq_hour_key, type="int") > 2:
        return False
    else:
        redis_client.incr(fq_hour_key, 1)

    # 限制每个客户端24小时调用次数 10
    fq_24hour_key = "%s_%s_per_24hour" % (user_fingerprint, ip)
    if not redis_client.get(fq_24hour_key):
        redis_client.incr(fq_24hour_key, 1)
        redis_client.expire(fq_24hour_key, 3600 * 24)
    elif redis_client.get(fq_24hour_key, type="int") > 10:
        return False
    else:
        redis_client.incr(fq_24hour_key, 1)

    # 限制每个客户端手机变化
    sms_mobile_key = "%s_%s_mobile" % (user_fingerprint, ip)
    if not redis_client.smembers(sms_mobile_key):
        redis_client.sadd(sms_mobile_key, mobile)
        redis_client.expire(sms_mobile_key, 3600 * 24)
    elif redis_client.scard(sms_mobile_key) > 2 and not redis_client.sismember(sms_mobile_key, mobile):
        return False
    else:
        redis_client.sadd(sms_mobile_key, mobile)

    return True


@csrf.exempt
# @yuanbian_token
@AuthManage.route("/check_is_robot_by_token", methods=["POST"])
def check_is_robot_by_token():
    """插件终端无法通过csrf_token识别"""
    return _do_check_is_robot()


# @csrf.exempt
@AuthManage.route("/check_is_robot", methods=["POST"])
def check_is_robot():
    """基于csrf_token"""
    return _do_check_is_robot()

def _do_check_is_robot():
    user_fingerprint = request.form.get("user_fingerprint")
    session['user_fingerprint'] = user_fingerprint
    biz_result = {"bizResult": {"signal": None}}
    result = aliyun_captcha_request.request("1jna4zfy",
                                            request.form.get("captchaVerifyParam"))
    if result['captcha_verify_result']:
        t = "".join(random.choices("1234567890abcdefghijklmnopqrstuvwxyz", k=6))
        signal = md5("".join(["yuanbian-lab", user_fingerprint, t]).encode()).hexdigest()
        biz_result = {"bizResult":{"signal": signal}}
        session['t'] = t
    result.update(biz_result)
    return result

def _do_check_is_robot_1():
    region_provider.modify_point('afs', 'cn-hangzhou', 'afs.aliyuncs.com')
    clt = client.AcsClient('LTAI5tGSm2YGojY3NsJ9r51N', 'DKsF73qvm0Hq99dF4P539Wd2RMZsjQ', 'cn-hangzhou')
    acs_request = AuthenticateSigRequest.AuthenticateSigRequest()
    session_id = request.form.get('session_id')
    sig = request.form.get("sig")
    token = request.form.get("token")
    scene = request.form.get("scene")
    user_fingerprint = request.form.get("user_fingerprint")
    acs_request.set_SessionId(session_id)
    acs_request.set_Sig(sig)
    acs_request.set_Token(token)
    acs_request.set_Scene(scene)
    # 必填参数：后端填写
    acs_request.set_AppKey('FFFF0N0000000000B4F8')
    # 必填参数：后端填写
    acs_request.set_RemoteIp(request.headers.get('X-Real-Ip') or request.remote_addr)

    result = clt.do_action_with_exception(acs_request).decode()  # 返回code 100表示验签通过，900表示验签失败
    result = json.loads(result)
    message = {"success": False}
    if result.get("Code") == 100:
        t = "".join(random.choices("1234567890abcdefghijklmnopqrstuvwxyz", k=6))
        signal = md5("".join(["yuanbian-lab", user_fingerprint, t]).encode()).hexdigest()
        message = {"success": True, "signal": signal, "t": t}
    return jsonify(message)


def mobile_exists(mobile):
    pass


def generate_sms_code(mobile):
    code = "".join(random.choices("1234567890", k=6))
    # 验证码存入redis
    try:
        nosql.redis_client.set("mobile_%s" % mobile, code, 600)
    except Exception as e:
        current_app.logger.error(f"{mobile} 请求生成code失败：{str(e)}")
        return False
    return code


def validator_sms_code(mobile, validator_code):
    try:
        code = nosql.redis_client.get("mobile_%s" % mobile)
    except Exception as e:
        current_app.logger.error(f"{mobile}验证code失败:{str(e)}")
        return False
    if code == validator_code:
        nosql.redis_client.delete("mobile_%s" % mobile)
        return True
    return False
