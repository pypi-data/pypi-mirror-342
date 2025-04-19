# -*- coding=utf-8 -*-
from bson.objectid import ObjectId
from datetime import datetime
from xp_cms.services.base_service import DocumentBaseService
from xp_cms.models.course import CourseNotebook



class CourseNotebookService(DocumentBaseService):
    model = CourseNotebook

    @classmethod
    def update_content(cls, new_content, user_id, course_id):
        update_data = {
            "user_id": user_id,
            "course_id": course_id,
            "content": new_content,
            "edit_time": datetime.now()
        }
        return cls.model.objects.upsert_one(**update_data)

    @classmethod
    def get_content(cls, user_id, course_id):
        return cls.model.objects(user_id=user_id, course_id=course_id).first()
