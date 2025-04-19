# -*- coding=utf-8 -*-
import os
from html import escape
from bson.objectid import ObjectId
import json
import math
from datetime import datetime
from flask import request, redirect, url_for, render_template, \
    jsonify, current_app, send_from_directory, send_file, g
from flask_login import login_required, current_user
from xp_cms.article import article_module
from xp_cms.models.article import Article, Comment
from xp_cms.forms.article_form import CommentForm
from xp_cms.services.article_service import ArticleService, CategoryService, CategoryDetailService
from xp_cms.services.comments_service import CommentsDocumentService

from xp_cms.utils import queryObjToDicts, queryObjToDicts_deep
from xp_cms.filters import pre_to_code
from xp_cms.extensions import nosql, es, csrf
from xp_cms.extensions import is_vip

html_404 = "页面不见了<a href=\"/\">返回首页</a>"


@article_module.route("/")
def index():
    return render_template("article/manual_index.html")

    # category = CategoryService.get_first_cate()
    # return redirect(url_for("article.getArticleList", path=category.get_cate_url()))


# 分类访问
# 1. 如果设置了cate_url 访问cate_url article/cate_url
# 2. 如果没有设置cate_url, 访问 cate_url = cate_id_md5
# 3. article/cate_id 跳转 article/cate_url

# 文章访问
# 1. 如果设置 aricle_url, 访问 article/cate_dir/article_url
# 2. 没有设置 article_url, 访问article/view/id/id_md5

# 如果是id，进行跳转
# 举例 /article/152
@article_module.route("/<int:cate_id>")
def old_getArticleList(cate_id):
    jump_url = nosql.cache_db.get(f"cate_{cate_id}_url")
    if jump_url:
        return redirect(jump_url, code=301)
    return html_404, 404


@article_module.route("/view/<int:article_id>")
def view(article_id):
    try:
        jump_url = os.path.join("../" + nosql.get(f"article_{article_id}_url"))
    except Exception:
        return html_404, 404
    else:
        return redirect(jump_url, code=302)


# VIP限制类文章
# 路径开头包括/training-ground
@article_module.route("/training-ground/<path:cate_url>/<article_url>")
@is_vip
def exercise(cate_url, article_url):
    url = os.path.join("training-ground", cate_url, article_url)
    return nosql.read_cache_page(url)

# 显示文章列表
# # @login_required
# @nosql.cache_page()
@article_module.route("/<path>")
def getArticleList(path):
    # url = path
    return nosql.read_cache_page(path)


#     if not cate_id:
#         return "", 404
#     current_cate, breadcrumb = get_cates(cate_id)
#     if current_cate is None or breadcrumb is None:
#         return "", 404
#     return render_template("article/manual.html",
#                             current_cate=current_cate,
#                             breadcrumb=breadcrumb,
#                             content_type="cate",
#                             title=current_cate.name,
#                             cate_name=current_cate.name
#                            )


# 面向SEO的访问路径
@article_module.route("/<path:cate_url>/<path:article_url>")
# @nosql.get_cache_page()
def get_manual(cate_url, article_url="index.html"):
    url = os.path.join(cate_url, article_url)
    return nosql.read_cache_page(url)


# 根据文章id阅读文章 - id 经过md5
@article_module.route("/view/id/<path>")
def view_by_path(path):
    url = g.client + "/" + path
    return nosql.read_cache_page(url)


# ajax加载
@article_module.route("/ajax_view/<cate_url>/<article_url>")
def ajax_view(cate_url, article_url):
    url = "ajax_view/" + cate_url + "/" + article_url
    return nosql.read_cache_page(url)

@article_module.route("/ajax_view_exercise/<cate_url>/<article_url>")
def ajax_view_exercise(cate_url, article_url):
    """动态加载excersi
    :param cate_url:
    :param article_url:
    :return:
    """
    url = "ajax_view_exercise/" + cate_url + "/" + article_url
    return nosql.read_cache_page(url)


def get_run_type(run_type):
    # if run_type == "html":
    #     run_url = "/run_code/run_html"
    # elif run_type == "python":
    #     run_url = "/run_code/run_python"
    # elif run_type == "notebook":
    #     run_url = "/run_code/run_lab"
    # else:
    #     run_url = "/run_code/run_python"
    run_url = "/run_code/run_{run_type}"
    return run_url


def get_cates(cate_id):
    cate_obj = CategoryService(cate_id)
    current_cate = cate_obj.cate
    if current_cate is None:
        return None, None
    breadcrumb = cate_obj.get_all_parent()
    breadcrumb.append(current_cate)
    return current_cate, breadcrumb


@article_module.route("/yuanbian")
def yuanbian():
    return render_template("article/yuanbian.html")


@article_module.route("/search")
@article_module.route("/search/<int:page_index>")
@nosql.cache_page()
def search(page_index=1):
    keyword = request.args.get("keyword", None)
    if not keyword:
        return redirect(url_for(".index"))
    index = current_app.config['ARTICLE_INDEX']
    query = {'bool': {'should': [], 'must': []}}
    kws = keyword.split()
    page_size = 30
    _from = (page_index - 1) * page_size
    for kw in kws:
        query['bool']['should'].append({'match_phrase': {'title': kw}})
        query['bool']['should'].append({'match_phrase': {'content': kw}})
    highlight = {"fields": {"content": {}}}
    res = es.client.async_search.submit(index=index, query=query, highlight=highlight, from_=_from, size=page_size)
    total_page = math.ceil(res['response']['hits']['total']['value'] / page_size)
    articles = res['response']['hits']['hits']
    page_navigation_start = page_index - 5 if page_index > 5 else 1
    page_navigation_end = page_index + 5 if page_index < total_page - 5 else total_page + 1
    page_navigation = [page for page in range(page_navigation_start, page_navigation_end)]
    return render_template("article/search.html",
                           articles=articles,
                           total_page=total_page,
                           keyword=keyword,
                           page_navigation=page_navigation)


# # 评论列表
# @article_module.route("/comments", methods=["GET"])
# # @login_required
# # @nosql.cache_view_page()
# def getComments():
#     article_id = request.args.get('article_comment_id')
#     page_type = request.args.get("type")
#
#     try:
#         page = int(request.args.get('page', 1))
#         assert page >= 1
#     except Exception as e:
#         return ""
#
#     out_data = {"replies": None, "comments": None, "total_pages": 1, "res": "success"}
#     if article_id:
#         # res = CommentsDocumentService.filter_by(article_id=article_id, replied_id=None).order_by(Comment.timestamp.desc()).paginate(page,10)
#         if page == 1:
#             page_info, comments = CommentsDocumentService.get_first_page_comments(page_type, article_id)
#             if page_info:
#                 out_data.update({"replies"    : page_info.replies,
#                                  "total_pages": comments.pages,
#                                  "next_page": comments.next_num
#                                  })
#                 out_data.update(comments_to_dict(comments.items))
#         else:
#             comments = CommentsDocumentService.get_main_comments(page_type, article_id, page)
#             if comments:
#                 out_data.update({
#                                  "total_pages": comments.pages,
#                                  "next_page"  : comments.next_num
#                                  })
#                 out_data.update(comments_to_dict(comments.items))
#
#         return json.dumps(out_data)



# # 发表评论
# @csrf.exempt
# @article_module.route("/comment/publish", methods=["post"])
# @login_required
# def publish():
#     message = {"res": "fail"}
#     if not current_user.is_approve:
#         return jsonify({"res": "wait_approve", "url": "/wait_approve"})
#     form = CommentForm(meta={'csrf': False})
#
#     if form.validate_on_submit():
#         comment_data = escape(form.data['comment'])
#         article_id = escape(str(form.data['article_comment_id']))
#         page_type = escape(str(form.data['type']))
#         reply_id = escape(str(form.data['reply_id'])) if form.data['reply_id'] else None
#         comment_id = escape(form.data['comment_id']) if form.data['comment_id'] else None
#         ref = escape(str(form.data['ref'])) if form.data['ref'] else None
#
#         #
#         comment = {
#             "content" : comment_data,
#             "username": current_user.username,
#         }
#
#         try:
#             CommentsDocumentService.add_comment(article_id, page_type, comment, reply_id, comment_id, ref)
#         except Exception as e:
#             current_app.logger.error(e)
#         else:
#             message['res'] = "success"
#     else:
#         print(form.errors)
#
#     return jsonify(message)



