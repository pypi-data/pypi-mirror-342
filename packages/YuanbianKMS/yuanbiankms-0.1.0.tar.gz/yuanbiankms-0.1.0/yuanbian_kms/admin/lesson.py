# -*- coding=utf-8 -*-
import os
import base64
from tempfile import mktemp
from flask import render_template, request, current_app, flash
from flask import jsonify, json
from flask_login import login_required

from xp_cms.admin import admin_module
from xp_cms.extensions import csrf
from xp_cms.forms.course_form import LessonForm
from xp_cms.services.course_service import CourseLessonService, \
    CourseLessonVideoService, CourseGroupsService
from xp_cms.upload.upload_aliyun_video_module import UploadAliyunVideo


@admin_module.route('/course/lesson/<int:course_id>/')
@admin_module.route('/course/lesson/<int:course_id>/<int:page>')
@login_required
def manage_lesson(course_id, page=1):

    pagination = CourseLessonService.get_course_lessons(
        course_id=course_id,
        page_index=page,
        per_page=current_app.config['XPCMS_MANAGE_ARTICLE_PER_PAGE']
    )

    lessons = pagination.items

    return render_template('admin/course/lesson/manage_lesson.html',
                           page=page, pagination=pagination,
                           course_id=course_id,
                           lessons=lessons)


@admin_module.route('/course/lesson/new/<int:course_id>', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def new_lesson(course_id):
    form = LessonForm()
    groups = CourseGroupsService.get_all_by_field(("course_id", course_id))
    form.group_id.choices = [(group.group_id, group.group_name) for group in groups]

    if form.validate_on_submit():
        data = {}
        for attr in ['title', 'order_id', 'intro', 'body',
                     'run_type', 'group_id', 'video_url']:
            data[attr] = getattr(form, attr).data

        data['course_id'] = course_id
        video_id = form.video_id.data
        if video_id:
            video = CourseLessonVideoService.get_one_by_id(video_id)
        else:
            video = None
        lesson = CourseLessonService.add_by_dicts(data)
        if video:
            video.lesson_id = lesson.id
            CourseLessonVideoService.update(video)

        if not lesson.comment_id:
            lesson.comment_id = lesson.generate_comment_id()
            CourseLessonService.update(lesson)

        return jsonify({"lesson_id": lesson.id})
    elif form.errors:
        print(form.errors)

    return render_template('admin/course/lesson/new_lesson.html', form=form, course_id=course_id)


@admin_module.route('/course/lesson/<int:lesson_id>/edit', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def edit_lesson(lesson_id):
    lesson = CourseLessonService.get_one_by_id(lesson_id)
    if not lesson:
        return "", 404
    form = LessonForm()
    groups = CourseGroupsService.get_all_by_field(("course_id", lesson.course_id))
    form.group_id.choices = [(group.group_id, group.group_name) for group in groups]
    if form.validate_on_submit():
        for attr in ['title', 'intro', 'order_id',
                     'body', 'video_url', 'trial',
                     'group_id', 'run_type']:
            setattr(lesson, attr, getattr(form, attr).data)
        video_id = form.video_id.data
        if video_id:
            video = CourseLessonVideoService.get_one_by_id(video_id)
        else:
            video = None
        if video:
            if lesson.video:
                lesson.video[0].lesson_id = None
            video.lesson_id = lesson.id
            CourseLessonVideoService.update(video)

        lesson.comment_id = lesson.generate_comment_id()
        CourseLessonService.update(lesson)
    elif form.errors:
        print(form.errors)
    form.process(obj=lesson)

    return render_template('admin/course/lesson/edit_lesson.html', form=form, course_id=lesson.course_id,
                           lesson_id=lesson_id)


@admin_module.route('/course/lesson/delete/<int:lesson_id>', methods=['POST'])
@login_required
def delete_lesson(lesson_id):
    lesson = CourseLessonService.delete_by_id(lesson_id)
    return "ok"


@admin_module.route("/course/lesson/delete", methods=['POST'])
@login_required
def batch_delete_lesson():
    ids = request.form.getlist("checkID[]")
    CourseLessonService.batch_lessons_delete(ids)
    return "ok"


@admin_module.route("/course/lesson/upload_video", methods=["POST"])
@login_required
def upload_video():
    upload_video_service = UploadAliyunVideo()
    file = request.files['video_file']
    temp_file = mktemp() + os.path.splitext(file.filename)[-1]
    file.save(temp_file)
    print(temp_file)
    video_id = upload_video_service.upload_video(
        file.filename,
        temp_file,
        "",
        ".",
        ""
    )
    os.unlink(temp_file)
    # video_url = json.loads(base64.urlsafe_b64decode(upload_info['UploadAddress']).decode())
    # video_id = upload_info['VideoId']
    CourseLessonVideoService.add_by_dicts({
        "video_id": video_id,
        "endpoint": "",
        "bucket"  : "",
        "filename": "",
    })

    return jsonify({"video_id": video_id})
