# -*- coding=utf-8 -*-
import json
from datetime import datetime
from html import escape
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from xp_cms.extensions import csrf
from xp_cms.utils import show_username
from xp_cms.services.comments_service import CommentsDocumentService
from xp_cms.forms.article_form import CommentForm


comments_module = Blueprint("comments", __name__)

@comments_module.route("/load_comments")
# @nosql.cache_view_page()
def load_comments():
    # 评论列表
    page_id = request.args.get('article_comment_id')
    page_type = request.args.get("type")
    parent_id = request.args.get("parent_id", None)
    if not parent_id:
        parent_id = None
    page = request.args.get('page', 1, int)
    out_data = {"comments": None, "total_pages": 1, "res": "success"}

    if page_id:
            # res = CommentsDocumentService.filter_by(page_id=article_id, replied_id=None).order_by(Comment.timestamp.desc()).paginate(page,10)
        res = CommentsDocumentService.\
            get_page_comments(page_type=page_type, page_id=page_id,
                              parent_id=parent_id, page_index=page)

        if res:
            out_data.update(comments_to_dict(res[0]))
            out_data.update({"total_pages": res[1]})
            out_data.update({"has_next": res[2]})
            out_data.update({"next_page": res[3]})


        return jsonify(out_data)
        #     page_info, comments = CommentsDocumentService.get_first_page_comments(page_type, article_id)
        #     if page_info:
        #         out_data.update({"replies"    : page_info.replies,
        #                          "total_pages": comments.pages,
        #                          "next_page"  : comments.next_num
        #                          })
        #         out_data.update(comments_to_dict(comments.items))
        #     else:
        #         comments = CommentsDocumentService.get_main_comments(page_type, article_id, page)
        #         if comments:
        #             out_data.update({
        #                 "total_pages": comments.pages,
        #                 "next_page"  : comments.next_num
        #             })
        #             out_data.update(comments_to_dict(comments.items))
        #




# 发表评论
@csrf.exempt
@comments_module.route("/publish", methods=["post"])
@login_required
def publish():
    message = {"res": "fail", "message":""}
    if not current_user.is_approve:
        return jsonify({"res": "wait_approve", "url": "/wait_approve"})
    form = CommentForm(meta={'csrf': False})

    if form.validate_on_submit():
        page_type = escape(str(form.data['type']))
        page_id = escape(str(form.data['article_comment_id']))
        comment_data = escape(form.data['comment'])
        parent_id = escape(str(form.data['parent_id'])) if form.data['parent_id'] else None
        # comment_id = escape(form.data['comment_id']) if form.data['comment_id'] else None
        ref = escape(str(form.data['ref'])) if form.data['ref'] else None
        #
        comment = {
            "page_type": page_type,
            "page_id": page_id,
            "content" : comment_data,
            "ref": ref,
            "parent_id": parent_id,
            "username": current_user.username,
        }

        try:
            CommentsDocumentService.add_comment(comment)
        except Exception as e:
            current_app.logger.error(e)
        else:
            message['res'] = "success"
    else:
        message['res'] = "fail"
        message['message'] = "表单数据验证不通过"

    return jsonify(message)

def comments_to_dict(comments):
    return {
        "comments": [
            {"comment_id": str(comment.pk),
             "parent_id" : comment.parent_id,
             "replies"   : comment.replies,
             "content"   : comment.content,
             "username"  : show_username(comment.username),
             "pub_date"  : datetime.strftime(comment.pubdate,"%Y-%m-%d %H:%M:%S"),
             "ref" : comment.ref if hasattr(comment, "ref") else "",
             } for comment in comments
        ]
    }