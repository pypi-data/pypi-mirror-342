# -*- coding=utf-8 -*-
import json
from uuid import uuid4
from datetime import datetime
from flask import request, session, render_template, \
    redirect, url_for, g, current_app
from flask import jsonify, flash
from flask_login import current_user
from .member_module import member_module
from xp_cms.models.article import Article, Category
from xp_cms.services.article_service import MemberDraftService
from xp_cms.extensions import db, csrf, nosql
from xp_cms.forms.article_form import MemberArticleForm, \
    ArticleSearchForm
from xp_cms.cores.html2bbcode import secure_html


@member_module.route("/article/publish/<article_id>", methods=['get', 'post'])
@member_module.route("/article/publish", methods=['get', "post"])
def article_publish(article_id=None):
    if request.headers.get("X-Requested-With"):
        ajax = True
    else:
        ajax = False

    form = MemberArticleForm()
    form.cate_id.choices = [(cate['cate_id'], cate['cate_name'])
                            for cate in nosql.get_file_cache("member_cates", type="json")]

    if article_id or form.article_id.data:
        return article_edit(article_id, form, ajax)
    else:
        return article_new(form, ajax)


def article_new(form, ajax=False):
    if form.validate_on_submit():
        draft_table = MemberDraftService()
        article = draft_table.get_all_by_author(current_user.username)
        if article.count() > 1:
            if ajax:
                return jsonify({"_id": None})
            else:
                flash("您还有尚未发布的 %s 篇文章草稿，请首先处理这些草稿" % article.count())
        else:
            data = form.data
            data['author'] = current_user.username
            data['title'] = secure_html(data['title'])[0:100]
            data['content'] = secure_html(data['content'])[0:5000]
            data['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data.pop("csrf_token")
            data.pop("article_id")

            id = draft_table.insert(data)
            if ajax and id:
                return jsonify({"_id": id})
            if id:
                flash("提交成功, 经过审核后正式发布")
            else:
                flash("发布失败, 请稍后尝试")
        return redirect(url_for(".draft_list"))
    elif form.errors:
        flash("数据提交错误")
    return render_template("member/{0}/article/article_post.html".format(g.client), form=form)


# 文章修改
def article_edit(article_id, form, ajax=False):
    draft_table = MemberDraftService()

    if form.validate_on_submit():
        data = form.data
        data['author'] = current_user.username
        data['title'] = secure_html(data['title'])[0:100]
        data['content'] = secure_html(data['content'])[0:5000]
        data.pop("csrf_token")
        article_id = data.pop("article_id")
        article_id = draft_table.update_one_by_author_and_id(current_user.username,
                                                             article_id,
                                                             data)

        if ajax and article_id:
            return jsonify({"_id": article_id})

        if article_id:
            flash("编辑成功")
        else:
            flash("不存在该文章或者无权编辑")
            return redirect(url_for(".draft_list"))
    article = draft_table.get_one_by_author_and_id(current_user.username, article_id)
    article['article_id'] = str(article['_id'])
    for key in ["article_id", "cate_id", "content", "title"]:
        getattr(form, key).data = article[key]
    return render_template("member/{0}/article/article_post.html".format(g.client), form=form)


#
# @member_module.route("/ckeditor", methods=['post'])
# def ckeditor_upload():
#
#     csrf.protect()
#     message = {
#         "uploaded": "0",
#         "fileName": "",
#         "url"     : "",
#         "error"   : {
#             "message": ""
#         }
#     }
#     if request.method == "POST":
#         file_storage = request.files.get("upload")
#         res = upload(file_storage)
#         if res['result']!="fail":
#             message['fileName'] =  res['result']
#             message['url'] = "/uploads/"+res['result']
#             message['uploaded'] = "1"
#         else:
#             message = {"uploaded":"0","error":str(res)}
#         return jsonify(message)

# @member_module.route("/ckeditor/browser", methods=['get'])
# def ckeditor_browser():
#     images = []
#     start_pos = len(current_app.config['BASEDIR'])
#     for dirpath, dirnames, filenames in os.walk(current_app.config['XPCMS_UPLOAD_PATH']):
#         for file in filenames:
#             file_info = os.path.splitext(file)
#             if file_info[0][-2:] not in ['_s', '_m']:
#                 images.append(os.path.join(dirpath[start_pos:], file))
#     return render_template("upload/browser.html", images=images)


# 获得文章列表
@member_module.route("/article/list/<int:page>", methods=['get', "post"])
@member_module.route("/article/list", defaults={"page": 1}, methods=['get', "post"])
def article_list(page):
    # 普通会员查看自己的文章
    # draft_table = MemberDraftService()
    res = Article.query.filter(Article.author == current_user.username).paginate(page, 10)

    # 无论搜索还是默认查看，都是翻页处理
    articles = res.items
    pageList = res.iter_pages()
    total = res.total

    return render_template("member/{0}/article/article_list.html".format(g.client), articles=articles,
                           pageList=pageList,
                           pages=res.pages,
                           total=total,

                           )


# 获得草稿列表
@member_module.route("/article/draft/<int:page>", methods=['get', "post"])
@member_module.route("/article/draft", defaults={"page": 1}, methods=['get', "post"])
def draft_list(page):
    #       普通会员只能在后台管理自己的文章
    draft_table = MemberDraftService()

    res = draft_table.get_all_by_author(current_user.username)
    status = {"0": "草稿", "1": "待审核", "2": "审核被拒"}
    # 无论搜索还是默认查看，都是翻页处理
    # {"items":res.items, "iter_pages":res.iter_pages(), "total":res.total,"pages":res.pages}
    # articles = res['items']
    # page_list = res['iter_pages']
    # pages = res['pages']
    # total = res['total']
    # for i in res:
    #     print(i)

    return render_template("member/{0}/article/draft_list.html".format(g.client),
                           articles=res, status=status
                           # pageList=page_list,
                           # pages=pages,
                           # total=total,
                           )


# 根据文章id删除文章
@member_module.route("/article/delete/<article_id>", methods=["POST"])
def article_delete(article_id):
    draft_table = MemberDraftService()
    res = draft_table.delete_one_by_author_and_id(current_user.username,
                                                  article_id)
    if res:
        return jsonify({"res": "success"})

# def set_article_form():
#     form = ArticleForm()
#     form.cate.choices = [(cateOption.cate_id, cateOption.name) for cateOption in Category.query.all()]
#     return form
