# -*- coding=utf-8 -*-
import json
from xp_cms.services.base_service import DocumentBaseService
from xp_cms.models.chatgpt_log import ChatGPTLogDocument


class ChatGPTLogService(DocumentBaseService):
    model = ChatGPTLogDocument

    @classmethod
    def add_new_chat(cls, log_id, user_id, user_prompt, openai_response):
        try:
            cls.model.objects(id=log_id, user_id=user_id)\
                .update(push__chat_content=user_prompt)
        except Exception as e:
            return
        else:
            return cls.model.objects(id=log_id, user_id=user_id)\
                .update(push__chat_content=openai_response)

    @classmethod
    def get_user_logs(cls, user_id):
        return cls.model.objects(user_id=user_id).order_by("-chat_date").paginate(1, 100)

    @classmethod
    def get_user_log_detail(cls, log_id, user_id):
        return cls.model.objects(id=log_id, user_id=user_id).first()

    @classmethod
    def find_log_by_keyword(cls, user_id, keyword):
        return cls.model.objects(user_id=user_id, chat_content__content__contains=keyword).order_by("-chat_date").paginate(1, 100)

    @classmethod
    def delete_userlog_by_id(cls, user_id, document_id):
        return cls.model.objects(pk=document_id, user_id=user_id).delete()

    @classmethod
    def delete_empty_userlog(cls, user_id):
        return cls.model.objects(user_id=user_id, chat_content=[]).delete()