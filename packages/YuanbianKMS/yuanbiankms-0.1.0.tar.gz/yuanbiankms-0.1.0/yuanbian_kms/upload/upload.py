# -*- coding=utf-8 -*-
import os, uuid
from PIL import Image
from flask import Blueprint, request, render_template
from flask import current_app
from flask_login import login_required, current_user
from flask import jsonify

from xp_cms.extensions import csrf
from xp_cms.upload import upload_module
from xp_cms.extensions import xp_upload


@upload_module.route("/upload_multiple", methods=['POST'])
def upload_multiple():
    """上传多张图片
    总的上传文件大小限制在 30 * 1000 * 1000 以下
    """
    message = {"result": "", "error": "", "filepath_list": []}
    if xp_upload.upload_content_length_limit(request.content_length):
        message.update({'result': "fail",
                        'error' : "上传文件太大"
                        })
        return jsonify(message)
    file_storage_list = request.files.getlist("file")
    for file_storage in file_storage_list:
        res = xp_upload.upload(file_storage)
        if res['result'] != "fail":
            message['filepath_list'].append(res['result'])
    return jsonify(message)


@upload_module.route("/ckeditor", methods=['POST'])
def ckeditor_upload():
    """CKEDITOR 上传接口

    """
    message = {
        "uploaded": "0",
        "fileName": "",
        "url"     : "",
        "error"   : {
            "message": ""
        }
    }

    file_storage = request.files.get("upload")
    res = xp_upload.upload(file_storage)
    if res['result']:
        # 返回键值由CKEditor API规定
        message['fileName'] = res['filename']
        message['url'] = res['result']
        message['uploaded'] = "1"
    else:
        message = {"uploaded": "0", "error": {"message": res['error']}}
    return jsonify(message)


@upload_module.route("/ckeditor/browser", methods=['get'])
def ckeditor_browser():
    images = []
    start_pos = len(current_app.config['BASEDIR'])
    for dirpath, dirnames, filenames in os.walk(current_app.config['XPCMS_UPLOAD_PATH'],
                                                current_user.username):
        for file in filenames:
            file_info = os.path.splitext(file)
            if file_info[0][-2:] not in ['_s', '_m']:
                images.append(os.path.join(dirpath[start_pos:], file))
    return render_template("upload/browser.html", images=images)


@upload_module.route("upload_thumb", methods=["POST"])
def upload_thumb():
    if 'upload' in request.files:
        f = request.files.get('upload')
        res = xp_upload.upload(f)
        if res['result']:
            filename_s = xp_upload.resize_image(f, res['result'], 'small')
            filename_m = xp_upload.resize_image(f, res['result'], 'medium')

            return jsonify({"o": res['result'],
                            "s": filename_s,
                            "m": filename_m
                            })
        else:
            return "", 404
