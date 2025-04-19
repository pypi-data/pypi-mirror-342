# -*- coding=utf-8 -*-
import json
import base64
import traceback
from aliyunsdkcore.client import AcsClient
from aliyunsdkvod.request.v20170321 import CreateUploadVideoRequest
from aliyunsdkvod.request.v20170321 import GetPlayInfoRequest
from voduploadsdk.AliyunVodUtils import *
from voduploadsdk.AliyunVodUploader import AliyunVodUploader
from voduploadsdk.UploadVideoRequest import UploadVideoRequest
from aliyunsdkvod.request.v20170321 import GetVideoPlayAuthRequest
from flask import current_app


class UploadAliyunVideo:
    client = None

    def __init__(self):
        aliyun_video_option = current_app.config.get('ALIYUN_VIDEO')
        if not aliyun_video_option:
            raise "缺少Aliyun Video配置"
        self.accessKeyId = aliyun_video_option['accessKeyId']
        self.accessKeySecret = aliyun_video_option['accessKeySecret']
        self.regionId = aliyun_video_option['regionId']
        self.auto_retry = aliyun_video_option['AutoRetry']
        self.max_retry_time = aliyun_video_option['maxRetryTime']
        self.connectTimeout = aliyun_video_option['connectTimeout']
        self.init_vod_client()

    def init_vod_client(self):
        self.client = AcsClient(self.accessKeyId,
                                self.accessKeySecret,
                                self.regionId,
                                self.auto_retry,
                                self.max_retry_time,
                                self.connectTimeout)

    def create_upload_video(self, title, file_path, video_desc, cover_url, tags):
        # request = CreateUploadVideoRequest.CreateUploadVideoRequest()
        # request.set_Title(title)
        # request.set_FileName(file_path)
        # request.set_Description(video_desc)
        # CoverURL示例："http://192.168.0.1/16/tps/TB1qnJ1PVXXXXXCXXXXXXXXXXXX-700-700.png"
        # request.set_CoverURL(cover_url)
        # request.set_Tags(tags)
        # request.set_CateId(0)

        # request.set_accept_format('JSON')
        upload_video_request = UploadVideoRequest(file_path, title)
        try:
            uploader = AliyunVodUploader(self.accessKeyId, self.accessKeySecret)
            video_id = uploader.uploadLocalVideo(upload_video_request)
            print("video_id=", video_id)
            # response = json.loads(self.client.do_action_with_exception(request))
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        else:
            return video_id['VideoId']

    def upload_video(self, title, video_file, video_desc, cover_url, tags):
        try:
            video_id = self.create_upload_video(title, video_file, video_desc, cover_url, tags)
            # print(uploadInfo['UploadAuth'])
            # print(json.dumps(uploadInfo, ensure_ascii=False, indent=4))

        except Exception as e:
            print(e)
            print(traceback.format_exc())
        else:
            return video_id

    def get_play_info(self, video_id):
        request = GetPlayInfoRequest.GetPlayInfoRequest()
        request.set_accept_format('JSON')
        request.set_VideoId(video_id)
        request.set_Formats("m3u8")
        request.set_ResultType("Multiple")
        request.set_AuthTimeout(3600 * 5)
        try:
            response = json.loads(self.client.do_action_with_exception(request))
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        return response

    def upload_video_file(self, file_path, title, storageLocation=None):
        try:
            # 可以指定上传脚本部署的ECS区域。如果ECS区域和视频点播存储区域相同，则自动使用内网上传，上传更快且更省公网流量。
            # ecsRegionId ="cn-shanghai"
            # uploader = AliyunVodUploader(accessKeyId, accessKeySecret, ecsRegionId)
            # 不指定上传脚本部署的ECS区域。
            uploader = AliyunVodUploader(self.accessKeyId, self.accessKeySecret)
            upload_video_request = UploadVideoRequest(file_path, title)
            # 可以设置视频封面，如果是本地或网络图片可使用UploadImageRequest上传图片到视频点播，获取到ImageURL
            # ImageURL示例：https://example.com/sample-****.jpg
            # uploadVideoRequest.setCoverURL('<your Image URL>')
            # 标签
            # uploadVideoRequest.setTags('tag1,tag2')
            if storageLocation:
                upload_video_request.setStorageLocation(storageLocation)
            video_id = uploader.uploadLocalVideo(upload_video_request)
            print("file: %s, videoId: %s" % (upload_video_request.filePath, video_id))

        except AliyunVodException as e:
            print(e)

    def get_video_play_auth(self, video_id):
        request = GetVideoPlayAuthRequest.GetVideoPlayAuthRequest()
        request.set_accept_format('JSON')
        request.set_VideoId(video_id)
        request.set_AuthInfoTimeout(3000)
        play_auth = ""
        try:
            play_auth = json.loads(self.client.do_action_with_exception(request))
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        else:
            # play_auth = base64.urlsafe_b64decode(play_auth["PlayAuth"]).decode()
            play_auth = play_auth['PlayAuth']
        return play_auth





