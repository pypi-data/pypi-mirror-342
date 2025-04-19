# -*- coding=utf-8 -*-

from flask import request,session,render_template,\
                  redirect, url_for
from flask import jsonify
from flask_login import current_user
from xp_cms.member.member_module import member_module
# from models import Article,Category, Comment
# from xp_cms.extensions import db
from xp_cms.services.comments_service import CommentsDocumentService
from xp_cms.services.article_service import ArticleService
from xp_cms.services.course_service import CourseLessonService
from xp_cms.forms.article_form import CommentForm


@member_module.route("/comments")
def my_comments():
    page_index = request.args.get("page", 1, type=int)
    comments = CommentsDocumentService.get_user_comments(current_user.username, page_index)
    comments_data = []

    return render_template("member/pc/comments/comments.html",
                           comments=comments,
                           types={"article": "技术文章区域", "lesson": "实验区域"})

@member_module.route("/comment/reply/<reply_id>")
def reply_comment(reply_id):

    return render_template("member/pc/reply_comment.html")



@member_module.route("/comments/<page_type>/<page_id>")
def view_page(page_type, page_id):
    types = {"article": {"__class__":ArticleService},
             "lesson": CourseLessonService}
    if page_type == "article":
        url = types[page_type]["__class__"].get_url_by_comment_id(page_id)
        return redirect("/article/"+url)

    if page_type == "lesson":
        course_id = types['lesson'].get_one_by_comment_id(page_id)[0]
        return redirect(url_for("course.show_course", course_id=course_id))

@member_module.route("/load_comments/<page_type>/<page_id>/<parent_id>")
def load_comments(page_type, page_id, parent_id):
    return render_template("member/pc/comments/comment_detail.html",
                           page_type=page_type,
                           page_id=page_id,
                           parent_id=parent_id)


@member_module.route("/del_comment")
def delete_comment():
    message = {"res": False, "message": "修改失败"}
    username = current_user.username
    comment_id = request.args.get("comment_id", None)
    if comment_id is None:
        return jsonify(message)

    res = CommentsDocumentService.delete_comment(username, comment_id)
    if res:
        message.update({
            "res": True,
            "message": "已经删除"
        })
    return jsonify(message)




