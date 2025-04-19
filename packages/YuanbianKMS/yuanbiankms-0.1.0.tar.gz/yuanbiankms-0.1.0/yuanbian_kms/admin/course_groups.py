# -*- coding=utf-8 -*-
import os
import base64
from tempfile import mktemp
from flask import render_template, request, current_app, flash
from flask import jsonify, json
from flask_login import login_required

from xp_cms.admin import admin_module
from xp_cms.extensions import csrf
from xp_cms.forms.course_form import CourseGroupsForm
from xp_cms.services.course_service import CourseLessonService, \
    CourseLessonVideoService, CourseGroupsService


@admin_module.route('/course/groups/<int:course_id>/')
@login_required
def manage_groups(course_id):
    groups = CourseGroupsService.get_groups_by_course_id(course_id)
    return render_template('admin/course/groups/manage_group.html',
                           course_id=course_id,
                           groups=groups)


@admin_module.route('/course/groups/new/<int:course_id>', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def new_group(course_id):
    form = CourseGroupsForm()
    if form.validate_on_submit():
        data = {}
        for attr in ['group_name', 'group_order']:
            data[attr] = getattr(form, attr).data

        data['course_id'] = course_id
        group = CourseGroupsService.add_by_dicts(data)
        return jsonify({"group_id": group.group_id})
    elif form.errors:
        print(form.errors)

    return render_template('admin/course/groups/new_group.html', form=form, course_id=course_id)


@admin_module.route('/course/groups/<int:group_id>/edit', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def edit_group(group_id):
    form = CourseGroupsForm()
    group = CourseGroupsService.get_one_by_id(group_id)
    if not group:
        return "", 404
    if form.validate_on_submit():
        for attr in ['group_name', 'group_order']:
            setattr(group, attr, getattr(form, attr).data)
        CourseGroupsService.update(group)
    elif form.errors:
        print(form.errors)
    form.process(obj=group)

    return render_template('admin/course/groups/edit_group.html', form=form,
                           course_id=group.course_id,
                           group_id=group_id)


@admin_module.route('/course/groups/delete/<int:group_id>', methods=['POST'])
@login_required
def delete_group(group_id):
    if CourseGroupsService.delete_by_id(group_id):
        return "ok"
    else:
        return "fail"


