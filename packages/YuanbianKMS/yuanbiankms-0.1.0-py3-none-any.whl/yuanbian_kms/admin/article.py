# -*- coding=utf-8 -*-
import hashlib
from html.parser import HTMLParser
from flask import request, session, render_template, g, \
    redirect, url_for, current_app, jsonify, \
    Response, stream_with_context
from flask_login import login_required
from xp_cms.admin import admin_module
from xp_cms.models.article import Article, Category
from xp_cms.services.article_service import ArticleService, CategoryService, \
    TagsService, CommentService, MemberDraftService
from xp_cms.services.comments_service import CommentsDocumentService
from xp_cms.forms.article_form import ArticleForm, ArticleSearchForm
from xp_cms.extensions import db, es
from xp_cms.utils import get_all_parent, get_all_cates
from xp_cms.extensions import nosql
from .libs.__cache_lib import generate_cate_page, \
    generate_article_page, generate_article_ajax_page, html_parser, \
    generate_comment_id


@admin_module.route('/article/manage/', defaults={'page': 1})
@admin_module.route('/article/manage/<int:page>', methods=['GET'])
def manage_article(page):
    search_form = ArticleSearchForm()
    order = {"field": "order_id", "type": "asc"}
    per_page = current_app.config.get('XPCMS_MANAGE_ARTICLE_PER_PAGE', 25)
    conditions = []
    cate_parent = None
    search_cate_id = request.args.get('search_cate_id')
    if search_cate_id:
        cate = CategoryService.get_one_by_id(search_cate_id)
        cate_parent = cate.cate_parents + "," + str(cate.cate_id) if cate.cate_parents \
            else "," + str(cate.cate_id)
        search_cate = [res[0] for res in CategoryService.get_children_id(search_cate_id)]
        search_cate.insert(0, search_cate_id)
        conditions.append({"field": "cate_id",
                           "value": search_cate, "operator": "in"}
                          )
    q = request.args.get("q", "")
    q_field = request.args.get('field', "id")
    if q:
        conditions.append({"field": q_field,
                           "value": q, "operator": "like"
                           })

    status = request.args.get("status", "3")
    if status != "3":
        conditions.append({"field": "status",
                           "value": status, "operator": "eq"})

    is_menu = request.args.get("is_menu", "3")
    if is_menu != "3":
        conditions.append({"field": "is_menu",
                           "value": is_menu, "operator": "eq"})

    order = request.args.get("order", "1")
    asc_or_desc = {"1": "asc", "2": "desc"}[order]
    order = {"fields": (("cate_id", asc_or_desc), ("order_id", asc_or_desc)), "type": "multi_fields"}

    res = ArticleService.get_many(conditions, order, page, pageSize=per_page)
    articles = res['items']
    iter_pages = res['iter_pages']
    query_string = request.query_string.decode()
    form_data = {
        "q"             : q,
        "search_cate_id": request.args.get("search_cate_id", None),
        "order"         : order,
        "field"         : q_field,
        "status"        : status,
        "is_menu"       : is_menu,
    }
    search_form.process(data=form_data)
    return render_template('admin/article/manage_article.html', page=page,
                           iter_pages=iter_pages, total=res['total'],
                           query_string=query_string, current_page=page,
                           pages=res['pages'], articles=articles,
                           search_form=search_form, cate_parent=cate_parent)


@admin_module.route('/article/new', methods=['GET', 'POST'])
def new_article():
    form = ArticleForm()
    if form.validate_on_submit():
        form_fields = ("title", "title2", "order_id", "thumb", "intro",
                       "content", "cate_id", "video_url", "status",
                       "run_code", "run_type", "article_url", "is_menu")
        new_article = {}
        for key in form_fields:
            new_article[key] = getattr(form, key).data

        tags_list_id = TagsService.add_tags(form.tags.data.replace("，", ","))
        new_article['article_tags'] = tags_list_id
        article = ArticleService.add_by_dicts(new_article)
        # 页面写入缓存
        if article.status == 1:
            save_article_cache(article)
        return jsonify({"res": "success", "article_id": article.id})
    elif form.errors:
        current_app.logger.error(form.errors)
        return jsonify({"res": "fail", "message": form.errors})

    return render_template('admin/article/new_article.html', form=form)


@admin_module.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    form = ArticleForm()
    article = ArticleService.get_one_by_id(article_id)
    if form.validate_on_submit():
        form.populate_obj(article)
        article.tags_list = form.clean_tags()
        ArticleService.update_tags(article)
        ArticleService.update(article)
        if article.status == 1:
            save_article_cache(article)
    elif form.errors:
        current_app.logger.error(form.errors)
    if article.is_menu is None:
        article.is_menu = "0"
    form.process(obj=article, data={"tags": article.tags_list})
    thumb = article.thumb
    if article.category:
        cate_parent = (article.category.cate_parents or "") + "," + str(article.cate_id)
    else:
        cate_parent = 0
    return render_template('admin/article/edit_article.html', form=form,
                           thumb=thumb, cate_parent=cate_parent)


@admin_module.route("/article/preview/<int:article_id>")
def preview_article(article_id):
    article = ArticleService.get_one_by_id(article_id)
    return generate_article_page(article)


@admin_module.route("/article/batch_update_order", methods=['POST'])
def batch_update_order():
    for data in request.form.items():
        ArticleService.update_order_id(*data)
    return jsonify({"res": "success"})


# 根据文章id删除文章
@admin_module.route("/article/delete", methods=['post'])
def delete_article():
    article_id = request.args.get("article_id")
    message = {"res": "fail", "id": article_id, "type": "del"}
    if article_id:
        res = ArticleService.delete_by_id(article_id)
        if res:
            message['res'] = "success"
    return jsonify(message)


@admin_module.route("/article/batch_menu", methods=['POST'])
def batch_menu_article():
    ids = [int(id) for id in request.form.getlist("checkID[]")]
    status = int(request.form.get("status"))
    ArticleService.batch_menu_article(ids, status)
    return jsonify({"res": "success"})


@admin_module.route('/article/menu', methods=['GET', 'POST'])
@login_required
def update_article_menu():
    article_id = request.args.get("article_id", 0)
    article = ArticleService.get_one_by_id(article_id)
    if article.is_menu == 0:
        article.is_menu = 1
    else:
        article.is_menu = 0
    ArticleService.update(article)
    return jsonify({"res": article.is_menu})


@admin_module.route("/article/batch_audit", methods=['POST'])
def batch_audit_article():
    ids = [int(id) for id in request.form.getlist("checkID[]")]
    status = int(request.form.get("status"))
    ArticleService.batch_audit_article(ids, status)
    return jsonify({"res": "success"})


@admin_module.route("/article/audit/<int:article_id>", methods=["post"])
def audit_article(article_id):
    article = ArticleService.get_one_by_id(article_id)
    if article.status:
        article.status = 0
    else:
        article.status = 1
    ArticleService.update(article)
    return jsonify({"res": article.status})


# 文章推荐
@admin_module.route("/article/recommend", methods=["post"])
def article_recommend():
    article_id = int(request.form.get("article_id"))
    message = {"res": "fail", "id": article_id, "type": "recommend"}
    if article_id:
        article = Article.query.get(article_id)
        if article:
            article.is_recommend = 1
            try:
                db.session.commit()
            except Exception as e:
                print(e)
            else:
                message['res'] = "success"
    return jsonify(message)


# 会员投稿列表
@admin_module.route("article/member_draft/", defaults={"page": 1}, methods=["get"])
@admin_module.route("article/member_draft/<int:page>", methods=["get"])
def member_draft(page):
    member_draft = MemberDraftService()
    res = member_draft.get_all_by_paginate(page)
    return render_template('admin/article/manage_draft.html',
                           draft_list=res['items'],
                           paginate=res['paginate'])


# 预览
@admin_module.route("article/member_draft/view/<object_id>", methods=["GET"])
def member_draft_view(object_id):
    if object_id:
        member_draft = MemberDraftService()
        draft = member_draft.get_one_by_id(object_id)
        return render_template("article/detail.html", article=draft)


# 审核通过
@admin_module.route("article/member_draft/check/", methods=["POST"])
def member_draft_check():
    object_id = request.form.get('object_id')
    if object_id:
        member_draft = MemberDraftService()
        draft = member_draft.get_one_by_id(object_id)
        if request.form.get('type') == "pass":
            article = Article(title=draft['title'],
                              content=draft['content'],
                              cate_id=draft['cate_id'],
                              author=draft['author'])
            if ArticleService.add(article):
                member_draft.delete_one_by_id(object_id)
        else:
            member_draft.update_one_by_and_id(object_id, {"status": "2"})
        return jsonify({"object_id": object_id})


@admin_module.route("article/update_all_cache", methods=["GET"])
def update_all_cache():
    cate_id = request.args.get('cate_id', None)
    return render_template("admin/article/update_cache.html", cate_id=cate_id)


@admin_module.route("article/update_cache", methods=["GET"])
def do_update_cache():
    event_id = request.headers.get('LAST_EVENT_ID', None)
    cate_id = request.args.get('cate_id', None)

    @stream_with_context
    def flush_content():
        import time
        if cate_id is None or cate_id == "None":
            cates = CategoryService.get_all()
        else:
            cate = CategoryService.get_one_by_id(cate_id)
            cates = [cate]
            cates.extend(CategoryService.get_children(cate.cate_id))
        tree_symbol = "-"

        for cate in cates:
            if cate.cate_parents is None:
                tree = ""
            else:
                tree = len(cate.cate_parents.split(",")) * tree_symbol
            yield f"data:{tree}{cate.name}\nid:{time.monotonic_ns()}\n\n"

            # 写入缓存数据库
            if cate.cate_template != "exercise":
                save_cate_cache(cate)
            time.sleep(0.05)

            for index, article in enumerate(cate.articles):

                if index > 0:
                    front_article = cate.articles[index-1]
                    setattr(article, "front_article_url", front_article.get_article_url())
                if index < len(cate.articles)-1:
                    next_article = cate.articles[index+1]
                    setattr(article, "next_article_url", next_article.get_article_url())

                save_article_cache(article)
                yield f"data:{tree} - /{article.title}\n\n"

        yield f"event:close\ndata:close\n\n"

    return Response(flush_content(), mimetype='text/event-stream')


def save_cate_cache(cate):
    """将分类页面缓存到缓存数据库
    1. 缓存 cate_id_url: cate_url (cate_url or cate_id_md5)
    1. 如果cate_url设置， 使用cate_url生成 cache_key
    2. 如果cate_url无设置，使用cate_id 生成 cache_key

    """
    # 生成页面缓存
    f = open("cache_log", "a+")
    cate_page = generate_cate_page(cate)
    # 生成cate_url
    cate_url = cate.get_cate_url()
    nosql.set_cache_page(cate_url, cate_page)
    print("cate_url", cate_url)
    f.write(f"cate_{cate.cate_id}_url=" + cate_url + "\r\n")
    f.close()
    nosql.set(f"cate_{cate.cate_id}_url", cate_url)
    return True


def save_article_cache(article):
    """将分类页面缓存到缓存数据库
    1. 缓存 article_id_url: article_url (cate_dir/article_url or cate_dir/article_id_md5)
    1. 如果article_url设置， 使用article_url生成 cache_key
    2. 如果article_url无设置，使用article_id 生成 cache_key

    """
    # 生成页面
    article_page = generate_article_page(article)
    #
    article_url = article.get_article_url()
    nosql.set_cache_page(article_url, article_page)
    print("article_url", article_url)
    nosql.set(f"article_{article.id}_url", article_url)
    f = open("cache_log", "a+")
    f.write(f"article_{article.id}_url=" + article_url + "\r\n")
    # 生成ajax缓存
    print(f"ajax_url='ajax_view/{article_url}'")
    nosql.set_cache_page("ajax_view/" + article_url,
                         generate_article_ajax_page(article))

    # es 索引
    if article.status:
        doc = {
            'title'    : article.title,
            'content'  : html_parser.strip_tags(article.content),
            'url'      : article_url,
            'cate_name': article.category.name
        }
        doc_id = article.id
        es.client.index(index=current_app.config['ARTICLE_INDEX'], id=doc_id, document=doc)

    # # 临时 - 生成comment_id
    # comments_data = {
    #     "page_id": generate_comment_id(article),
    #     "page_type": "article"
    # }
    # CommentsDocumentService.add_comments(comments_data)
    return True
