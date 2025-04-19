# -*- coding=utf-8 -*-
from bson.objectid import ObjectId
from xp_cms.services.base_service import DocumentBaseService
from xp_cms.services.article_service import ArticleService
from xp_cms.services.course_service import CourseLessonService
from xp_cms.models.comments import CommentsDocument
from mongoengine.errors import NotUniqueError


class CommentsDocumentService(DocumentBaseService):
    model = CommentsDocument

    @classmethod
    def add_comment(cls, comment_data):
        comment_document = cls.model(**comment_data)
        try:
            comment_document = comment_document.save()
        except NotUniqueError as e:
            return comment_document
        except Exception as e:
            raise e
        else:
            if comment_data['parent_id']:
                cls.model.objects(pk=comment_data['parent_id']). \
                    update(inc__replies=1)

        return comment_document

    @classmethod
    def get_page_comments(cls, page_type, page_id, parent_id=None, page_index=1, size=10):
        """
        根据页面的page_type, page_id查询第一级评论
        :param page_type:
        :param page_id:
        :param page_index:
        :param size:
        :return:
        """
        # cls.model.objects(page_type=page_type, page_id=page_id). \
        #     fields(slice__comments=[start, end]).first()
        comments = []
        pages = 0
        try:
            res = cls.model.objects(page_type=page_type, page_id=page_id). \
                filter(parent_id=parent_id).order_by("-pubdate", "-replies").\
                paginate(page_index, size)
        except Exception as e:
            raise e
        else:
            comments = res.items
            pages = res.pages
            has_next = res.has_next
            next_num = res.next_num

        return comments, pages, has_next, next_num


    @classmethod
    def get_user_comment_by_id(cls, comment_id, username):
        return cls.model.objects(id=comment_id, username=username).first()


    @classmethod
    def get_user_comments(cls, username, page_index=1, size=10):
        return cls.model.objects(username=username) \
            .order_by("-pubdate", "-replies").paginate(page_index, size)


    @classmethod
    def get_rel_content(cls, page_type, page_id):
        ref_content = ""
        if page_type == "article":
            ref_content = ArticleService.get_summary_by_comment_id(page_id)
        if page_type == "lesson":
            ref_content = CourseLessonService.get_summary_by_lesson_id(page_id)
        return ref_content

    @classmethod
    def delete_comment(cls, username, comment_id):
        res = cls.model.objects(pk=comment_id, username=username). \
                    update(is_deleted=True, content="原内容已经被删除")
        return res
