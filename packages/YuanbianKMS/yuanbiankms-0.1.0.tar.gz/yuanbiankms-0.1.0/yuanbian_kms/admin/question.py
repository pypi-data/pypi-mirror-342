# -*- coding=utf-8 -*-
from html import escape, unescape
import json
from io import StringIO
from tempfile import NamedTemporaryFile
from flask import request, session, render_template, \
    redirect, url_for, current_app, jsonify, make_response
from xp_cms.cores.xp_view.editview import EditAction
from xp_cms.admin import admin_module
from xp_cms.services.article_service import QuestionService, QuestionTypeService, CategoryService, \
    TagsService, CommentService
from xp_cms.services.question_service import QuestionDocumentService, TestingDocumentService, InternshipScoreLogService

from xp_cms.forms.article_form import  TestingSearchForm,  QuestionForm, \
    QuestionSearchForm, QuestionTypeForm, BatchLoadForm
from xp_cms.extensions import db, csrf, nosql

from xp_cms.utils import  queryObjToDicts
from openpyxl import Workbook

@admin_module.route('/question/manage_type', defaults={'page': 1})
@admin_module.route('/question/manage_type/<int:page>', methods=['GET'])
def manage_question_type(page):
    """题型管理"""
    q_types = QuestionTypeService.get_all()
    return render_template("admin/question/manage_question_type.html",
                           question_types=q_types)


@admin_module.route('/question/new_question_type', methods=['GET', 'POST'])
def new_question_type():
    """添加题库类型"""
    form = QuestionTypeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            q_type_title = form.q_type_title.data
            question_type = QuestionTypeService.add_by_dicts({"q_type_title": q_type_title})
            return jsonify({"q_type_id": question_type.q_type_id, 'errors': ""})
        else:
            return jsonify({"errors": form.errors})

    return render_template("admin/question/new_question_type.html", form=form)


@admin_module.route('/question_type/<int:q_type_id>/edit', methods=['GET', 'POST'])
def edit_question_type(q_type_id):
    """题库题型修改"""
    form = QuestionTypeForm()
    edit_fields = ['q_type_title']
    edit_action = EditAction(q_type_id, form, edit_fields, QuestionTypeService)
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                edit_action.update()
            except Exception as e:
                return jsonify({"errors": str(e)})
            return jsonify({"res": "success", 'q_type_id': q_type_id, "errors": ""})
        else:
            return jsonify({"errors": form.errors})
    return render_template("admin/question/edit_question_type.html",
                           form=edit_action.edit_form,
                           q_type_id=q_type_id
                           )


@admin_module.route('/question/manage', defaults={'page': 1})
@admin_module.route('/question/manage/<int:page>', methods=['GET'])
def manage_question(page):
    """题库管理
    题库数据库为mongodb
    """
    search_form = QuestionSearchForm()
    search_form.init_cate(QuestionTypeService.get_all())

    order = {"field": "q_id", "type": "asc"}
    per_page = current_app.config.get('XPCMS_MANAGE_ARTICLE_PER_PAGE', 25)
    conditions = []
    search_cate = request.args.get('q_type_id')

    if search_cate:
        conditions.append({"q_type_id": search_cate})
    q = request.args.get("q")

    if q:
        conditions.append({"q_content__icontains": q})
    q_status = True if request.args.get("q_status", False)=="True" else False
    conditions.append({'q_status': q_status})
    order_type = request.args.get("order")
    # if order_type == "1":
    #     order = {"field": "q_id", "type": "asc"}
    # elif order_type == "2":
    #     order = {"field": "q_id", "type": "desc"}
    # res = QuestionService.get_many(conditions, order, page, pageSize=per_page)
    res = QuestionDocumentService.get_all_page(page, per_page, conditions)
    query_string = request.query_string.decode()
    search_form.process(data={"q_type_id": search_cate,
                              "q": q,
                              "q_status": q_status,
                              "order": order_type})

    return render_template('admin/question/manage_question.html',
                           page=page,
                           questions=res.items,
                           iter_pages=res.iter_pages(),
                           total=res.total,
                           query_string=query_string,
                           pages=res.pages,
                           search_form=search_form)


@admin_module.route('/question/new', methods=['GET', 'POST'])
def new_question():
    """添加测试题"""
    form = QuestionForm()
    data = form.data_to_dicts()
    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data
            data.pop("csrf_token")
            data['q_correct_option'] = json.loads(data['q_correct_option'][0])
            data['q_type'] = QuestionTypeService.get_one_by_id(data['q_type_id']).q_type_title
            data['q_status'] = True if data['q_status']=="True" else False
            data['is_run_code'] = True if data['is_run_code'] == "True" else False
            data['q_course_url'] = data['q_course_url'] if data['q_course_url'] else None
            q_correct_option = data.pop("q_correct_option")
            q_option = []

            for i in range(0, 4):
                q_option.append({"q_option_text": escape(data.pop(f'q_option_{i + 1}')),
                                 "is_correct"   : str(i) in q_correct_option
                                 })
            question = QuestionDocumentService.add(data, q_option)
            return jsonify({"q_id": str(question.id)})
        else:
            print(form.errors)
    form.init_cate(QuestionTypeService.get_all())

    return render_template('admin/question/new_question.html', form=form)


@admin_module.route('/question/<q_id>/edit', methods=['GET', 'POST'])
def edit_question(q_id):
    form = QuestionForm()
    question = QuestionDocumentService.get_one_by_id(q_id)
    if request.method == "POST":
        if form.validate_on_submit():

            data = form.data
            data.pop("csrf_token")
            data['is_run_code'] = True if data['is_run_code'] == "True" else False
            data['q_status'] = True if data['q_status'] == "True" else False
            data['q_correct_option'] = json.loads(data['q_correct_option'][0])
            data['q_course_url'] = data['q_course_url'] if data['q_course_url'] else None
            for key, val in data.items():
                setattr(question, key, val)

            q_correct_option = data.pop("q_correct_option")
            q_options = []

            for i in range(0, 4):
                # 每题4项答案
                q_options.append({"q_option_text": escape(data.pop(f'q_option_{i + 1}')),
                                  "is_correct"   : str(i) in q_correct_option
                                  })
            question_document = QuestionDocumentService.update(question, data, q_options)

            return jsonify({"q_id"     : str(question.id),
                            "q_content": question.q_content,
                            "q_options": [
                                (option.q_option_text, option.is_correct) for option in question_document.q_option
                            ]})
        elif form.errors:
            print(form.errors)

    form.init_cate(QuestionTypeService.get_all())
    form.process(obj=question)
    form.is_run_code.id = "is_run_code"
    try:
        form.q_option_1.data = unescape(question.q_option[0].q_option_text)
        form.q_option_2.data = unescape(question.q_option[1].q_option_text)
        form.q_option_3.data = unescape(question.q_option[2].q_option_text)
        form.q_option_4.data = unescape(question.q_option[3].q_option_text)
    except:
        pass
    form.q_correct_option.data = [str(index) for index in range(len(question.q_option)) if question.q_option[index].is_correct]

    return render_template('admin/question/edit_question.html', form=form)

@admin_module.route("/question/batch_loads", methods=["get", "post"])
def question_batch_loads():
    if request.method == "POST":
        questions = request.files.get("files", None)
        questions = questions.stream.read().decode("utf-8")
        questions = questions.split("\n\n")
        success = ""
        for question in questions:
            lines = question.split("\n")
            q_content = lines[0]
            q_options = [{"q_option_text":escape(q),
                         "is_correct": False } for q in lines[1:]]

            data = {"q_content": escape(q_content),
                    "q_type_id": request.form.get("q_type_id"),
                    "q_score": request.form.get("q_score"),
                    "q_course_url": request.form.get("q_course_url"),
                    "q_status": True if request.form.get("q_status")=="True" else False}
            question = QuestionDocumentService.add(data, q_options)
            success += str(question.pk) + "<br>"
        return jsonify({"res": success})
    form = BatchLoadForm()
    form.process(data={"q_status": False})
    form.init_cate(QuestionTypeService.get_all())
    return render_template("admin/question/question_batch_loads.html", form=form)

@admin_module.route("/question/delete", methods=['post'])
def delete_question():
    q_id = request.args.get("q_id")
    message = {"res": "fail", "id": q_id, "type": "del"}
    if q_id:
        res = QuestionDocumentService.delete_by_id(q_id)
        if res:
            message['res'] = "success"
    return jsonify(message)


@admin_module.route("/question/flush")
def flush_question():
    questions = QuestionService.model.query.all()
    questions = queryObjToDicts(questions, ["q_content", "q_options", "q_type",
                                            "q_correct_option", "q_answer",
                                            "q_score"])
    question_types = QuestionService.model.query.with_entities(QuestionService.model.q_type). \
        group_by(QuestionService.model.q_type).all()

    for question_type in question_types:
        nosql.cache_db.delete(question_type[0])
    for question in questions:
        print(question)
        nosql.cache_db.sadd(question['q_type'], json.dumps(question))

    return "success"


@admin_module.route("/question/new_testing", methods=["GET", "POST"])
def new_testing():
    if request.method == "GET":
        question_types = QuestionTypeService.get_all()
        return render_template("admin/question/new_testing.html",
                               question_types=question_types)
    else:
        title = request.form.get("title")
        questions = json.loads(request.form.get("questions"))
        content = request.form.get("content")
        is_internship = bool(int(request.form.get("is_internship")))
        is_vip = bool(int(request.form.get("is_vip")))
        college_name = request.form.get("college_name")
        testing_doc = TestingDocumentService.add({"title": title,
                                                  "content": content,
                                                  "question_combination": questions,
                                                  "is_internship": is_internship,
                                                  "college_name": college_name,
                                                  "is_vip":  is_vip
                                                  })
        return jsonify({"res": "success", "_id": str(testing_doc.pk)})


@admin_module.route("/question/edit_testing", methods=["GET", "POST"])
def edit_testing():
    question_types = QuestionTypeService.get_all()
    testing_doc = TestingDocumentService.get_one_by_id(request.args.get("testing_id"))
    if request.method == "POST":
        testing_doc.update(**{"title": request.form.get("title"),
                            "content": request.form.get("content"),
                            "question_combination":json.loads(request.form.get("questions")),
                              "is_internship": bool(int(request.form.get("is_internship"))),
                              "college_name": request.form.get("college_name"),
                              "is_vip": bool(int(request.form.get("is_vip"))),
                              })
        testing_doc.reload()

        data = {
            "_id": str(testing_doc.pk),
            "title": testing_doc.title,
            "content": testing_doc.content,
            "question_combination": testing_doc.question_combination,
            "is_internship": testing_doc.is_internship,
            "college_name":  testing_doc.college_name,
            "is_vip": testing_doc.is_vip
        }
        return jsonify(data)
    return render_template("admin/question/edit_testing.html",
                           testing_doc=testing_doc,
                           question_types=question_types)

@admin_module.route("/question/delete_testing/<testing_id>", methods=["POST"])
def delete_testing(testing_id):
    TestingDocumentService.delete_by_id(testing_id)
    return jsonify({"res":"success", "_id": testing_id})

@admin_module.route("/question/manage_testing", defaults={"page": 1})
@admin_module.route("/question/manage_testing/<int:page>", defaults={"page": 1})
def manage_testing(page):
    search_form = TestingSearchForm()
    per_page = current_app.config.get('XPCMS_MANAGE_ARTICLE_PER_PAGE', 25)
    conditions = []
    q = request.args.get("q")
    search_form.q.data = q
    if q:
        conditions.append({"title__icontains": q})

    res = TestingDocumentService.get_all_page(page, per_page, conditions)

    return render_template("admin/question/manage_testing.html",
                           page=page,
                           testing_docs=res.items,
                           iter_pages=res.iter_pages(),
                           total=res.total,
                           query_string=request.query_string.decode(),
                           pages=res.pages,
                           search_form=search_form
                           )


@admin_module.route('/question/internship', defaults={'page': 1})
@admin_module.route('/question/internship/<int:page>', methods=['GET'])
def internship_log(page):
    # search_form = QuestionSearchForm()
    # search_form.init_cate(QuestionTypeService.get_all())

    # order = {"field": "q_id", "type": "asc"}
    per_page = current_app.config.get('XPCMS_MANAGE_ARTICLE_PER_PAGE', 25)
    conditions = []

    search_cate = request.args.get('q_type_id', None)
    if search_cate:
        conditions.append({"q_type_id": search_cate})

    q = request.args.get("q", None)
    if q:
        conditions.append({"college_name__icontains": q})

    log_id = request.args.get("log_id", None)
    if log_id:
        conditions.append({"score_log_id": log_id})
    # order_type = request.args.get("order")
    # if order_type == "1":
    #     order = {"field": "q_id", "type": "asc"}
    # elif order_type == "2":
    order = {"field": "score_log_id", "type": "desc"}
    res = InternshipScoreLogService.get_many(conditions, order, page, pageSize=per_page)

    query_string = request.query_string.decode()
    # search_form.process(data={"q_type_id": search_cate,
    #                           "q": q,
    #                           "q_status": q_status,
    #                           "order": order_type})

    return render_template('admin/question/internship_log.html',
                           page=page,
                           internship_logs=res['items'],
                           iter_pages=res['iter_pages'],
                           total=res['total'],
                           query_string=query_string,
                           pages=res['pages'],
                           search_form=None)


@admin_module.route('/question/export_internship/<testing_id>')
def export_internship_log(testing_id):
    testing = TestingDocumentService.get_one_by_id(id=testing_id, fields=("title",))
    res = InternshipScoreLogService.get_all_by_field(("testing_name", testing['title']))
    array = []

    wb = Workbook()
    ws = wb.active
    ws.title = "实训成绩"
    ws.sheet_properties.tabColor = "1072BA"
    for row, item in enumerate(res):
        for col, name in enumerate(['student_name', "student_number", "student_score"]):
            ws.cell(row=row+1, column=col+1, value=getattr(item, name))
    with NamedTemporaryFile() as f:
        wb.save(f.name)
        f.seek(0)
        response = make_response(f.read())
    response.headers['Content-Type'] = "application/vnd.ms-excel"
    response.headers['Content-Disposition'] = "attachment;filename=" + "test" + ".xls"
    return response