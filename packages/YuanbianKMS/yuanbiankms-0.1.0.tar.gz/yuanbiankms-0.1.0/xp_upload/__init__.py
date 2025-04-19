# -*- coding=utf-8 -*-
import os
import uuid
from PIL import Image
from datetime import date
from flask import session
from flask_login import current_user


class XpUpload:
    """文件上传对象
    需要在app.config中配置以下项：
    upload_allowed_type - 允许上传文件类型列表
    upload_file_maxsize - 允许上传文件最大尺寸
    """

    UploadTypeError = "上传文件类型不对, 允许类型 %s"
    SizeError = "文件尺寸超过上线"
    DirsError = "用户目录超过允许最大限制 %s"
    SaveError = "文件保存到 %s 失败"
    upload_allowed_type = ["image/jpg"]
    upload_file_maxsize = 30 * 1000

    upload_content_length_limit = 30 * 1000 * 10
    # 用户目录文件总字节数限制
    user_upload_dirs_limit = 10 * 1000 * 100

    def __init__(self, app=None):
        if app:
            self.init_app(app)
        else:
            self.app = None
            self.config = None

    def init_app(self, app):
        self.app = app
        self.config = app.config
        try:
            self.upload_allowed_type = app.config['XPCMS_ALLOWED_UPLOAD_TYPE']
        except KeyError:
            pass

        try:
            self.upload_file_maxsize = app.config['UPLOAD_FILE_MAXSIZE']
        except KeyError:
            pass

    def set_upload_option(self, upload_allowed_type=None, upload_file_maxsize=None):
        if upload_allowed_type:
            self.upload_allowed_type = upload_allowed_type
        if upload_file_maxsize:
            self.upload_file_maxsize = upload_file_maxsize

    def check_upload_type(self, f):
        if f.content_type not in \
                self.upload_allowed_type:
            return True

    def check_upload_content_length_limit(self, content_length):
        if content_length > self.upload_content_length_limit:
            return True

    def check_user_dir_limit(self):
        if session.get("user_upload_total_size") > self.user_upload_dirs_limit:
            return True

    def upload(self, f) -> object:
        """根据表单上传域上传文件
        :param f: 表单文件域
        :return:
        """
        # message = {"result": "", "error": "", "filepath_list": []}
        message = {"result": "", "filename": "", "error": ""}
        if self.check_upload_type(f):
            message.update({'result': False,
                            'error' : self.UploadTypeError % self.upload_allowed_type
                            })
            return message

        if self.check_user_dir_limit():
            message.update({'result': False,
                            'error' : self.DirsError % self.user_upload_dirs_limit
                            })
            return message
        # 使用新文件名保存
        # filename 用于前端显示,不需要绝对路径
        # file_path 用于实际文件保存操作绝对路径
        abs_path, path = self.generate_upload_file_path()
        if abs_path is None:
            message.update({'result': False,
                            'error' : "文件保存路径错误"
                            })
            return message
        new_file_name = self.generate_filename(f.filename)
        file_path = os.path.join(path, new_file_name)
        abs_file_path = os.path.join(abs_path, new_file_name)
        try:
            f.save(abs_file_path)
        except Exception as e:
            message.update({'result': False,
                            'error' : "文件保存错误 %s" % e
                            })
            self.app.logger.error(e)
            return message
        else:
            session['user_upload_total_size'] += os.path.getsize(abs_file_path)
        message.update({'result': file_path,
                        'filename': new_file_name})
        return message

    def upload_multiple(self, file_storage_list):
        """多文件上传操作
        :param file_storage_list: 上传文件对象列表
        :return: 上传成功文件列表
        """
        message = {"result": "", "error": "", "filepath_list": []}
        for file_storage in file_storage_list:
            res = self.upload(file_storage)
            if res['result'] != self.res_error:
                message['filepath_list'].append(res['result'])
        return message

    def ckeditor_upload(self, upload_file):
        """用于ckeditor上传"""
        message = {"uploaded": "0",
                   "fileName": "",
                   "url": "",
                   "error": {"message": ""}
                   }

        res = self.upload(upload_file)
        if res['result'] != self.res_error:
            message.update({'fileName': res['result'],
                            'url':  res['result'],
                            'uploaded': "1"})
        else:
            message = {"uploaded": "0", "error": str(res)}
        return message

    def generate_upload_file_path(self):
        upload_base_dir = self.config['XPCMS_UPLOAD_PATH']
        upload_dir = os.path.split(upload_base_dir)[1]
        # 根据上传的日期存放
        d = date.today()
        # 生成存储路径
        if not current_user.is_admin:
            path = os.path.join(current_user.username, str(d.year), str(d.month))
        else:
            path = os.path.join(str(d.year), str(d.month))
        abs_user_file_path = os.path.join(upload_base_dir, path)
        if not os.path.exists(abs_user_file_path):
            try:
                os.makedirs(abs_user_file_path)
            except Exception as e:
                self.app.logger.error(e)
                return None, None
        return abs_user_file_path, os.path.join("/", upload_dir, path)


    @staticmethod
    def generate_filename(filename):
        """生成随机文件名
        :param filename:
        :return:
        """
        ext = os.path.splitext(filename)[1]
        new_file_name = str(uuid.uuid4()) + ext
        return new_file_name

    def resize_image(self, image, filename, base_width):
        """缩略图生成
        :param image:
        :param filename:
        :param base_width:
        :return:
        """
        base_size = self.config['XPCMS_IMAGE_SIZE'].get(base_width)
        filename, ext = os.path.splitext(filename)
        img = Image.open(image).convert("RGB")
        filename += self.config['XPCMS_IMAGE_SUFFIX'].get(base_width) + ext
        upload_path = os.path.split(self.config['XPCMS_UPLOAD_PATH'])[0]
        file_full_path = os.path.join(upload_path, filename.lstrip("/"))
        if img.size[0] > base_size:
            w_percent = (base_size / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((base_size, h_size), resample=Image.LANCZOS)
            img.save(file_full_path, optimize=True, quality=85)
        else:
            img.save(file_full_path, optimize=True, quality=85)
        return filename

    def upload_thumb(self, f):
        """多尺寸缩略图生成"""
        # 上传原尺寸
        master_filename = self.upload(f)['result']
        # 生成 小尺寸、中等尺寸、原尺寸
        if master_filename != "fail":
            filename_s = self.resize_image(f, master_filename, 'small')
            filename_m = self.resize_image(f, master_filename, 'medium')

            return {"o": master_filename,
                    "s": filename_s,
                    "m": filename_m
                    }
        else:
            return "", 404
