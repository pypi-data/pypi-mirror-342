# -*- coding=utf-8 -*-
import time
from .utils import to_xml,  get_verify_code


class WechatMessageApi:
    """微信公众号消息接口
    subscribe - 公众号订阅事件
    unsubscribe - 公众号取消订阅事件
    scan - 扫描事件
    view - view事件
    """

    @classmethod
    def subscribe(cls, data, message=None):
        # 如果是扫码注册(包含场景参数)
        if data['EventKey'][8:21] == "register_bind":
            message = "欢迎你来到Python-XP手册"
        elif data['EventKey'][8:18] == "login_bind":
            data['EventKey'] = data['EventKey'][8:]
            # message = help_bind(data)
        elif data['EventKey'][8:15] == "verify_":
            message = get_verify_code(data['EventKey'][15:])
        return WechatMessage.create_text_message(message, data['FromUserName'], data['ToUserName'])

    @classmethod
    def unsubscribe(cls, data, message=None):
        # if delete_wechat_info():
        #     message = "已取消关注，您的微信绑定信息已删除，下次登陆需要重新绑定"
        # else:
        if message is None:
            message = "您已取消关注Python-XP手册，下次访问Python-XP.COM需要重新关注"
        return WechatMessage.create_text_message(message, data['FromUserName'], data['ToUserName'])

    @classmethod
    def scan(cls, data, message=None):
        """
        已关注, 扫描公众号事件，根据场景值处理

        :param data: data包含了openid
        :param message:
        :return:
        """
        if message is None:
            message = "我们将为您带来更多更好的学习服务"
        if data['EventKey'] is None:
            message = "谢谢关注"
        elif data['EventKey'][:13] == "register_bind":
            message = "您已经完成关注，请选择登录"
        # elif data['EventKey'][:10] == "login_bind":
        #     # 检测是否已经绑定
        #     message = help_bind(data)
        elif data['EventKey'][:7] == "verify_":
            message = get_verify_code(data['EventKey'][7:], data['FromUserName'])
        else:
            message = "没有找到对应的业务"
        return WechatMessage.create_text_message(message, data['FromUserName'], data['ToUserName'])

    @classmethod
    def view(cls, data):
        print(data)
        return " "


class WechatMessage:
    """消息回复
    create_text_message - 创建文本类型回复消息
    create_news_message - 创建多条新闻列表回复消息
    """
    @staticmethod
    def create_text_message(content, to_user_name, from_user_name):
        response_data = {"ToUserName": to_user_name,
                         "FromUserName": from_user_name,
                         "CreateTime": round(time.time()),
                         "MsgType": "text",
                         "Content": content,
                         "MsgId": round(time.time() * 10 ** 6)
                         }
        return to_xml(response_data)

    @staticmethod
    def create_news_message(content, to_user_name, from_user_name):
        response_data = {"ToUserName": to_user_name,
                         "FromUserName": from_user_name,
                         "CreateTime": round(time.time()),
                         "MsgType": "news",
                         'ArticleCount': content['count'],
                         "Articles": content['items'],
                         "MsgId": round(time.time() * 10 ** 6)
                         }

        return to_xml(response_data)

