# -*- coding=utf-8 -*-
from bson import ObjectId
from flask import current_app
from xp_cms.services.base_service import XPService
from xp_cms.models.article import Article, Category, \
    Comment, Tags, QuestionType, Question, QuestionChoices, CategoryDetail, tags_articles
from xp_cms.extensions import db, nosql
from xp_cms.cores.xp_view.paginate import Paginate
# from sqlalchemy.sql.expression import update
from sqlalchemy import update


class ArticleService(XPService):
    model = Article

    @classmethod
    def batch_menu_article(cls, ids, is_menu):
        db.session.execute(
            update(cls.model).where(
                cls.model.id.in_(ids)
            ).values(is_menu=is_menu)
        )
        db.session.commit()

    @classmethod
    def batch_audit_article(cls, ids, status):
        # delete = tags_articles.delete().where(tags_articles.c.article_id.in_(ids))
        # db.get_engine().connect().execute(delete)
        # db.session.execute(delete)
        # Comment.query.filter(Comment.article_id.in_(ids)).delete(synchronize_session="fetch")
        # cls.model.query.filter(Article.id.in_(ids)).delete(synchronize_session="fetch")
        db.session.execute(
            update(cls.model).where(
                cls.model.id.in_(ids)
            ).values(status=status)
        )
        db.session.commit()
        # delete = tags_articles.delete().where(tags_articles.c.article_id.in_(ids))
        # db.get_engine().connect().execute(delete)
        # Article.query.filter(Article.id.in_(ids)).delete(synchronize_session="fetch")
        # Comment.query.filter(Comment.article_id.in_(ids)).delete(synchronize_session="fetch")
        # # print(dir(tags_articles))

    @classmethod
    def update_tags(cls, article):
        new_article_tags = TagsService.add_tags(article.tags_list)
        article.article_tags = []
        for tag in new_article_tags:
            article.article_tags.append(tag)

    @classmethod
    def update_order_id(cls, article_id, order_id):
        db.session.execute(update(cls.model).where(
            cls.model.id == int(article_id)
        ).values(order_id=int(order_id)))
        db.session.commit()

    @classmethod
    def get_summary_by_id(cls, id):
        return cls.model.query(cls.model.title, cls.model.intro).get(id)

    @classmethod
    def get_summary_by_comment_id(cls, comment_id):
        return cls.model.query.with_entities(cls.model.title, cls.model.intro).filter(
            cls.model.comment_id == comment_id
        ).first()

    @classmethod
    def get_url_by_comment_id(cls, comment_id):
        article = cls.model.query.filter(cls.model.comment_id == comment_id).first()
        return article.get_article_url()


class CategoryService(XPService):
    model = Category
    second_model = CategoryDetail

    def __init__(self, cate):
        if isinstance(cate, Category):
            self.cate = cate
        else:
            self.cate = self.get_one_by_id(cate)

    @classmethod
    def get_first_cate(cls):
        try:
            cate = cls.model.query.order_by(cls.model.order_id.asc()).first()
        except Exception as e:
            current_app.logger.error(e)
            return None
        else:
            return cate

    @classmethod
    def add_cate(cls, data):
        detail = data.pop('detail')
        cate = cls.model(**data)
        cate.detail = cls.second_model(detail=detail)
        return cls.add(cate)

    @classmethod
    def update_cate(cls, cate_obj, data):
        # detail = cls.model(detail=data.pop("detail"))
        detail = data.pop("detail")
        for key, val in data.items():
            setattr(cate_obj, key, val)
        cate_obj.detail = cls.second_model(detail=detail)
        return cls.update(cate_obj)

    def get_all_parent(self):
        if not self.cate.cate_parents:
            return []
        if self.cate.cate_parents[0] == ",":
            cate_parents = [int(cate) for cate in self.cate.cate_parents[1:].split(",")]
            all_parents = self.get_many([{"field"   : 'cate_id',
                                          "value"   : cate_parents,
                                          "operator": "in"}],
                                        order={"type": "field", "field": "cate_id", "order": (cate_parents)})
            return all_parents['items']
        else:
            return []

    @classmethod
    def get_children(cls, top_parent_id):
        return cls.model.query.filter(cls.model.cate_parents.like(f",{top_parent_id}%")).all()

    @classmethod
    def get_children_id(cls, top_parent_id):
        return cls.model.query.with_entities(cls.model.cate_id).filter(
            cls.model.cate_parents.like(f",{top_parent_id}%")).all()

    @classmethod
    def check_parent(cls, parent_id):
        if parent_id is not None:
            parent = cls.get_one_by_id(parent_id)
            return parent
        return None


class CategoryDetailService(XPService):
    model = CategoryDetail


class TagsService(XPService):
    model = Tags

    @classmethod
    def add_tags(cls, new_tags):
        tags_list = new_tags.split(",")
        tags_list_id = []
        for tag in tags_list:
            exit_tag = cls.get_one_by_field(("name", tag))
            if not exit_tag:
                new_tag = cls.model(name=tag)
                cls.add(new_tag)
                if new_tag.id:
                    tags_list_id.append(new_tag)
            else:
                tags_list_id.append(exit_tag)
        return tags_list_id


class QuestionService(XPService):
    model = Question
    # choice_model = QuestionChoices

    # @classmethod
    # def add_by_dicts(cls, dicts, choice_dicts):
    #     obj = cls.model(**dicts)
    #     for choice_dict in choice_dicts:
    #         obj.q_choices.append(
    #             cls.choice_model(**choice_dict)
    #         )
    #     return cls.add(obj)


class QuestionTypeService(XPService):
    model = QuestionType


class CommentService:
    model = Comment


class CommentService2(XPService):
    collection_name = "comment"

    def __init__(self):
        self.collection = nosql.mongo_client.select_collection(self.db_name, self.collection_name)
        self.page_size = current_app.config.get("XPCMS_MANAGE_ARTICLE_PER_PAGE")

    def pub_comment(self, data):
        """data结构

        article_id - 文章id
        username - 文章作者
        comment - 评论内容
        from-admin - 是否来自管理员
        createtime - 发表时间
        reviewed - 是否审核
        """
        res = self.collection.insert_one(data).inserted_id
        return str(res)

    def reply_comment(self, data):
        pass


class MemberDraftService(XPService):
    db_name = "member_center"
    collection_name = "draft"

    def __init__(self):
        self.collection = nosql.mongo_client.select_collection(self.db_name, self.collection_name)
        self.page_size = current_app.config.get("XPCMS_MANAGE_ARTICLE_PER_PAGE")

    # 获取某个用户的所有草稿
    def get_all_by_author(self, author):
        res = self.collection.find({"author": author})
        return res

    # 获取某个用户的一篇草稿
    def get_one_by_author(self, author):
        res = self.collection.find_one({"author": author})
        return res

    # 根据object_id获取篇草稿
    def get_one_by_id(self, article_id):
        res = self.collection.find_one({"_id": ObjectId(article_id)})
        return res

    # 根据用户名、文章id获取某篇草稿
    def get_one_by_author_and_id(self, author, article_id):
        res = self.collection.find_one({"_id": ObjectId(article_id), "author": author})
        return res

    # 根据用户、文章id修改
    def update_one_by_author_and_id(self, author, article_id, data):
        res = self.collection.update_one({"_id": ObjectId(article_id), "author": author},
                                         {"$set": data})
        if res.modified_count == 1:
            return article_id

    # 根据用户、文章id修改
    def update_one_by_and_id(self, article_id, data):
        res = self.collection.update_one({"_id": ObjectId(article_id)},
                                         {"$set": data})
        if res.modified_count == 1:
            return article_id

    def delete_one_by_author_and_id(self, author, article_id):
        res = self.collection.delete_one({"_id": ObjectId(article_id), "author": author})
        return res.deleted_count

    def delete_one_by_id(self, article_id):
        res = self.collection.delete_one({"_id": ObjectId(article_id)})
        return res.deleted_count

    def insert(self, data):
        res = self.collection.insert_one(data).inserted_id
        return str(res)

    def get_all_by_paginate(self, current_page):
        total_page = self.collection.estimated_document_count()
        paginate = Paginate(total_page, self.page_size).get_paginate(current_page)
        res = self.collection.find().limit(self.page_size).skip(
            (current_page - 1) * self.page_size)
        return {"items": res, "paginate": paginate}
