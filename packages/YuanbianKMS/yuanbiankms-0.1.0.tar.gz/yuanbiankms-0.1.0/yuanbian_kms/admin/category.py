# -*- coding=utf-8 -*-
import json
from os import path
from flask import render_template, g, request, \
    jsonify, current_app, redirect, flash, url_for
from flask_login import login_required
from xp_cms.admin import admin_module
from xp_cms.extensions import db
from xp_cms.forms.article_form import CategoryForm
from xp_cms.models.article import Article, Category
from xp_cms.services import ArticleService, CategoryService, CategoryDetailService
from xp_cms.extensions import nosql
from xp_cms.utils import queryObjToDicts

"""
Category
"""


@admin_module.route('/category/manage/', defaults={"parent_id": 0}, methods=["GET"])
@admin_module.route('/category/manage/<int:parent_id>', methods=["GET"])
@login_required
def manage_category(parent_id):
    conditions = [{"field": "parent_id", "value": None, "operator": "eq"}]
    order = {"field": "order_id", "type": "asc"}
    res = CategoryService.get_many(conditions, order)
    return render_template('admin/category/category_list.html', categories=res['items'])


@admin_module.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm(meta={'csrf': False})
    if form.validate_on_submit():

        data = form.data
        try:
            data['parent_id'] = int(data['parent_id'])
            assert data['parent_id'] != 0
        except:
            data['parent_id'] = None

        parent = CategoryService.get_one_by_id(data['parent_id'])
        if parent and parent.cate_parents is not None:
            data['cate_parents'] = parent.cate_parents + "," + str(data['parent_id'])
        elif parent:
            data['cate_parents'] = "," + str(data['parent_id'])
        else:
            data['cate_parents'] = ""

        flush_cate_dir(parent, data)

        category = CategoryService.add_cate(data)
        if category:
            create_category_cache()
            return jsonify({"res": "success", "message": category.cate_id})
        else:
            return jsonify({"res": "fail", "errors": {"_": ["添加失败"]}})
    elif form.errors:
        return jsonify({"res": "fail", "errors": form.errors})
    return render_template('admin/category/category_add.html', form=form)


@admin_module.route('/category/<int:cate_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(cate_id):
    message = None
    form = CategoryForm()
    category = Category.query.get_or_404(cate_id)
    g.category_id = category.cate_id
    g.category_name = category.name
    category.open_contribute = str(category.open_contribute)

    if form.validate_on_submit():
        if cate_id == int(form.parent_id.data):
            return jsonify({"res": "fail", "errors": {" ": ["父类不能设定为自身"]}})
        data = form.data
        data.pop("csrf_token")
        try:
            data['parent_id'] = form.parent_id.data if int(form.parent_id.data) else None
        except Exception:
            data['parent_id'] = None

        parent = None
        if data['parent_id']:
            parent = CategoryService.check_parent(data['parent_id'])
            if parent is None:
                return jsonify({"res": "fail", "errors": {"_": ["父类不存在"]}})
            else:
                if parent.cate_parents is None:
                    parent.cate_parents = ""

        flush_cate_dir(parent, data)
        data['is_menu'] = int(data['is_menu'])
        data['is_vip'] = int(data['is_vip'])
        category = CategoryService.update_cate(category, data)
        if category:
            flush_category_parents(category)
            return jsonify({"res": "success", "message": category.cate_id})
        else:
            return jsonify({"res": "fail", "errors": {"_": ['fail']}})

    elif form.errors:
        return jsonify({"res": "fail", "errors": form.errors})
    else:
        data = None
        if category.parent_id is None:
            data = {"parent_id": 0}
        form.edit_field(category, data=data)

    return render_template('admin/category/category_edit.html', form=form, cate_id=cate_id, cate=category)


@admin_module.route('/category/menu', methods=['GET', 'POST'])
@login_required
def update_category_menu():
    cate_id = request.args.get("cate_id", 0)
    cate = CategoryService.get_one_by_id(cate_id)
    if cate.is_menu == 0:
        cate.is_menu = 1
    else:
        cate.is_menu = 0
    CategoryService.update(cate)
    return jsonify({"res": cate.is_menu})


@admin_module.route('/category/delete', methods=['POST'])
@login_required
def delete_category():
    cate_id = int(request.form['cate_id'])
    try:
        cate = CategoryService.get_one_by_id(cate_id)
        assert cate.sub_cates == []
        assert cate.articles == []
        CategoryService.delete_by_id(cate_id)
    except Exception as e:
        current_app.logger.error(e)
        return "fail"
    return "ok"


@admin_module.route('/category', methods=['get'])
@login_required
def get_cate():
    parent_id = request.args.get("parent_id", 0, type=int)
    parent_id = parent_id if parent_id else None
    sub_cates = CategoryService.get_many([{"field"   : "parent_id",
                                           "value"   : parent_id,
                                           "operator": "eq"}])['items']

    cate_dicts = [(sub_cate.name, sub_cate.cate_id) for sub_cate in sub_cates]
    return jsonify(cate_dicts)


@admin_module.route("/flush_categroy_articles", methods=['post'])
@login_required
def flush_category_articles():
    cate_id = int(request.form['cate_id'])
    cate = CategoryService.get_one_by_id(cate_id)
    nosql.clean_page_cache(url_for("article.getArticleList", cate_id=cate_id))
    for article in cate.articles:
        nosql.clean_page_cache(url_for("article.view", article_id=article.id))
        nosql.clean_page_cache(url_for("article.ajax_view", article_id=article.id))
    return "ok"


@admin_module.route("/flush_categroy", methods=['post'])
@login_required
def flush_category():
    cate_id = int(request.form['cate_id'])
    cate = CategoryService.get_one_by_id(cate_id)
    nosql.clean_page_cache(url_for("article.getArticleList", cate_id=cate_id))
    return "ok"


#
@admin_module.route('/category/create_parents', methods=['GET'])
def create_parents():
    all_top_cates = CategoryService.get_all_by_field(("parent_id", None))
    for item in all_top_cates:
        do_create_parents(item)
    return str(all_top_cates)


@admin_module.route('/category/get_parents/<cate_parent>', methods=['GET'])
def get_parents(cate_parent):
    cate_data = []
    cate_parents = cate_parent.split(",")
    cates = CategoryService.get_all_by_field(("parent_id", None))
    cate_data.append([(cate.name, cate.cate_id) for cate in cates])
    for i in cate_parents[1:]:
        cates = CategoryService.get_all_by_field(("parent_id", i))
        cate_data.append([(cate.name, cate.cate_id) for cate in cates])
    return jsonify(cate_data)


def do_create_parents(cate):
    if cate.parent_id is not None:
        print(cate.parent_id)
        cate.cate_parents = cate.parent.cate_parents + "," + str(cate.parent_id)
    else:
        cate.cate_parents = ""

    CategoryService.update(cate)

    if cate.sub_cates is not None:
        for sub_cate in cate.sub_cates:
            do_create_parents(sub_cate)


def create_category_cache():
    member_cates = CategoryService.get_all_by_field(("open_contribute", 1))
    member_cates = [{"cate_name": cate.name, "cate_id": cate.cate_id} for cate in member_cates]
    nosql.save_file_cache("member_cates", json.dumps(member_cates))


def flush_category_parents(category):
    for sub_cate in category.sub_cates:
        sub_cate.cate_parents = (category.cate_parents or "") + "," + str(sub_cate.parent_id)
        if not CategoryService.update(sub_cate):
            pass
        flush_category_parents(sub_cate)


def flush_cate_dir(parent, data):
    if parent:
        parent_cate_full_dir = parent.cate_full_dir or parent.cate_dir or ""
        parent_cate_parents = parent.cate_parents or ""
        data['cate_parents'] = parent_cate_parents + "," + str(data['parent_id'])
        data['cate_full_dir'] = path.join(parent_cate_full_dir, data['cate_dir'])
    else:
        data['cate_parents'] = None
        data['cate_full_dir'] = data['cate_dir']
