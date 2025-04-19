# -*- coding=utf-8 -*-

from flask import render_template, request, current_app, flash
from flask import jsonify, json
from flask_login import login_required

from xp_cms.admin import admin_module
from xp_cms.extensions import db
from xp_cms.utils import redirect_back

from xp_cms.forms.course_form import CourseForm, COURSE_CATEGORY
from xp_cms.models.course import Course, CourseTags, tags_courses
from xp_cms.services.course_service import CourseService


@admin_module.route('/course/manage', defaults={'category_id': None})
@admin_module.route('/course/manage/<int:category_id>', methods=['GET'])
def manage_course(category_id=None):
    page = request.args.get('page', 1, type=int)
    page_size = current_app.config['XPCMS_MANAGE_ARTICLE_PER_PAGE']
    if not category_id:
        pagination = CourseService.get_all_courses(page, page_size)
    else:
        pagination = CourseService.get_courses_by_cate(category_id, page, page_size)
    courses = pagination.items

    return render_template('admin/course/manage_course.html',
                           page=page,
                           pagination=pagination,
                           courses=courses,
                           course_category=COURSE_CATEGORY)


@admin_module.route('/course/new', methods=['GET', 'POST'])
@login_required
def new_course():
    form = CourseForm()
    if form.validate_on_submit():
        new_course_dict = form.data
        new_course_dict.pop('csrf_token')
        new_course_dict["tags_list"] = new_course_dict["tags_list"].replace("，", ",")
        tags = add_tags(new_course_dict["tags_list"])
        new_course_dict.update({"tags": tags})
        course = CourseService.add_by_dicts(new_course_dict)
        return jsonify({"course_id": course.id})
    elif request.method == 'POST' and form.errors:
        return jsonify(form.errors)

    return render_template('admin/course/new_course.html', form=form)


@admin_module.route('/course/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    form = CourseForm()
    course = Course.query.get_or_404(course_id)
    if form.validate_on_submit():
        for field in ["title", "intro", "order_id",
                      "video_url", "category_id",
                      "thumb", "total_price"]:
            setattr(course, field, getattr(form, field).data)

        tags_list = form.tags_list.data.replace(" ", "").replace("，", ",")
        course.tags_list = tags_list
        tags = add_tags(tags_list)
        for item in course.tags:
            if tags_list.find(item.name) == -1:
                course.tags.remove(item)

        course.tags = tags

        CourseService.update(course)

    elif form.errors:
        print("************")
        print(form.errors)
    form.process(obj=course)

    return render_template('admin/course/edit_course.html', form=form,
                           thumb=course.thumb, course_id=course_id)


@admin_module.route('/manage/course/delete/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    CourseService.delete_by_id(course_id)
    return "ok"


@admin_module.route("/manage/course/delete", methods=['POST'])
def batch_delete_course():
    pass


#     ids = request.form.getlist("checkID[]")
#     print(list(request.form.lists()))
#     print(ids)
#     delete = tags_courses.delete().where(tags_courses.c.course_id.in_(ids))
#     db.get_engine().connect().execute(delete)
#     Course.query.filter(Course.id.in_(ids)).delete(synchronize_session="fetch")
#     CourseComment.query.filter(CourseComment.course_id.in_(ids)).delete(synchronize_session="fetch")
#     # print(dir(tags_articles))
#     db.session.commit()
#
#     return "ok"


@admin_module.route('/manage/commment/set/<int:course_id>', methods=['POST'])
def set_comment(course_id):
    course = CourseService.get_one_by_id(course_id)
    if course.can_comment:
        course.can_comment = False
        flash('Comment disabled.', 'success')
    else:
        course.can_comment = True
        flash('Comment enabled.', 'success')
    CourseService.update(course)
    return "ok"


# @course_module.route('/manage/comment/')
# @login_required
# def manage_comment():
#     filter_rule = request.args.get('filter', 'all')  # 'all', 'unreviewed', 'admin'
#     page = request.args.get('page', 1, type=int)
#     per_page = current_app.config['XPCMS_COMMENT_PER_PAGE']
#     if filter_rule == 'unread':
#         filtered_comments = CourseComment.query.filter_by(reviewed=False)
#     elif filter_rule == 'admin':
#         filtered_comments = CourseComment.query.filter_by(from_admin=True)
#     else:
#         filtered_comments = CourseComment.query
#
#     pagination = filtered_comments.order_by(CourseComment.timestamp.desc()).paginate(page, per_page=per_page)
#     comments = pagination.items
#     return render_template('article/admin/article/manage_comment.html', comments=comments, pagination=pagination)


# @admin_module.route('/manage/comment/approve/<int:comment_id>', methods=['POST'])
# def approve_comment(comment_id):
#     comment = CourseComment.query.get_or_404(comment_id)
#     comment.reviewed = True
#     db.session.commit()
#     flash('Comment published.', 'success')
#     return redirect_back()


# @admin_module.route('/manage/comment/delete/<int:comment_id>', methods=['POST'])
# @login_required
# def delete_comment(comment_id):
#     comment = CourseComment.query.get_or_404(comment_id)
#     db.session.delete(comment)
#     db.session.commit()
#     flash('Comment deleted.', 'success')
#     # return redirect_back()
#     return "ok"

# @admin_module.route("/manage/comment/delete", methods=['POST'])
# @login_required
# def batch_delete_comment():
#     print("------"*10)
#     ids = request.form.getlist("checkID[]")
#     print(ids)
#     CourseComment.query.filter(CourseComment.id.in_(ids)).delete(synchronize_session="fetch")
#     db.session.commit()
#     return "ok"

def add_tags(tags_list):
    tags = []
    for tag in tags_list.split(","):
        exits_tag = CourseService.get_course_tags(tag)
        if not exits_tag:
            new_tag = CourseService.create_tag(tag)
            if new_tag and new_tag.id:
                tags.append(new_tag)
        else:
            tags.append(exits_tag)
    return tags
