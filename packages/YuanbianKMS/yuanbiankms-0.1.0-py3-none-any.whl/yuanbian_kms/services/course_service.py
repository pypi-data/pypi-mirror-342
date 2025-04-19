# -*- coding=utf-8 -*-
from datetime import datetime
from xp_cms.services.base_service import XPService, DocumentBaseService
from xp_cms.extensions import db, nosql
from xp_cms.models.course import Course, CourseLesson, CourseTags, \
    CourseLearnLog, CertificateLog, LessonVideo
from xp_cms.models.course import CourseGroups
from xp_cms.models.course import OrderCourse


class CourseService(XPService):
    model = Course

    @classmethod
    def get_all_courses(cls, page, page_size=25):
        return cls.model.query.order_by(cls.model.timestamp.desc()).paginate(page=page, per_page=page_size)

    @classmethod
    def get_courses_by_cate(cls, cate_id, page, page_size=25):
        return cls.model.query.filter_by(category_id=cate_id). \
            order_by(cls.model.timestamp.desc()).paginate(page=page, per_page=page_size)

    @classmethod
    def get_course_tags(cls, tag):
        return db.session.query(CourseTags).filter_by(name=tag).one_or_none()

    @classmethod
    def create_tag(cls, tag):
        new_tag = CourseTags(name=tag)
        db.session.add(new_tag)
        db.session.commit()


class CourseGroupsService(XPService):
    model = CourseGroups
    @classmethod
    def get_groups_by_course_id(cls, course_id):
        return cls.model.query.filter_by(course_id=course_id). \
            order_by(cls.model.group_order.asc()).all()



class CourseLessonService(XPService):
    model = CourseLesson

    @classmethod
    def get_summary_by_lesson_id(cls, comment_id):
        return cls.model.query.with_entities(cls.model.title, cls.model.intro).filter(
            cls.model.comment_id == comment_id
        ).first()

    @classmethod
    def get_one_by_comment_id(cls, comment_id):
        return cls.model.query.with_entities(cls.model.course_id).filter(
            cls.model.comment_id == comment_id
        ).first()

    @classmethod
    def get_next_lesson(cls, course_id, order_id):
        next_order_id = order_id + 1
        return cls.model.query.with_entities(cls.model.id).filter(
            cls.model.course_id == course_id,
            cls.model.order_id == next_order_id
        ).first()

    @classmethod
    def get_course_lessons(cls, course_id, page_index, per_page):
        return cls.model.query.join(CourseGroups, CourseLesson.group_id==CourseGroups.group_id). \
                filter_by(course_id=course_id).\
                order_by(CourseGroups.group_order.asc(), CourseLesson.order_id.asc()).paginate(
                page=page_index, per_page=per_page
        )

    @classmethod
    def batch_lessons_delete(cls, ids):
        CourseLesson.query.filter(CourseLesson.id.in_(ids)).delete(synchronize_session="fetch")
        db.session.commit()


class OrderCourseService(XPService):
    model = OrderCourse


class CourseLearnLogService(DocumentBaseService):
    model = CourseLearnLog

    @classmethod
    def get_learn_log(cls, user_id, course_id):
        return cls.model.objects(user_id=user_id, course_id=course_id).first()

    @classmethod
    def update_log(cls, user_id, course_id, lesson_id):
        return cls.model.objects(user_id=user_id, course_id=course_id). \
            update_one(add_to_set__log=lesson_id)

    @classmethod
    def create_log(cls, user_id, course_id, course_title):
        log_data = {
            "user_id"     : user_id,
            "course_id"   : course_id,
            "course_title": course_title,
            "log"         : [],
            "start_date"  : datetime.now()
        }
        return cls.model(**log_data).save()

    @classmethod
    def get_last_10_log(cls, user_id):
        return cls.model.objects(user_id=user_id).only("course_title", "log", "start_date").order_by(
            "-start_date").limit(10)


class CertificateLogService(DocumentBaseService):
    model = CertificateLog

    @classmethod
    def create_certificate(cls, user_id, course_id, username, title, incident, describe):
        cert_log = cls.model.objects(user_id=user_id, course_id=course_id).first()
        if cert_log is None:
            cert_log = cls.add(
                {"user_id"   : user_id,
                 "course_id" : course_id,
                 "username"  : username,
                 "title"     : title,
                 "incident"  : incident,
                 "describe"  : describe,
                 "issue_date": datetime.now()}
            )
        return cert_log


class CourseLessonVideoService(XPService):
    model = LessonVideo
