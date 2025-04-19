# -*- coding=utf-8 -*-
from flask import request, render_template, current_app, \
    flash, url_for, jsonify, Blueprint
from flask_login import current_user, login_required
from xp_cms.utils import redirect_back, redirect
from xp_cms.services.course_service import CourseService, CourseLessonService, \
    CourseLearnLogService, CertificateLogService
from xp_cms.services.notebook_service import CourseNotebookService
from xp_cms.upload.upload_aliyun_video_module import UploadAliyunVideo
from .course_notes_data import notes_data
from xp_cms.extensions import is_vip

course_module = Blueprint("course", __name__)


# @course_module.before_request
# @login_required
# def is_vip():
#     if not current_user.vip_type and \
#             request.endpoint not in ["course.index",
#                                      "course.course_intro",
#                                      "course.course_notes"]:
#         return redirect(url_for("auth.upgrade2vip"))
#

@course_module.route('/')
def index():
    return render_template("index.html")
    return render_template("course/course_index.html")

@course_module.route("/course_intro/<course>")
def course_intro(course):
    course = course.lower()
    if course not in current_app.config.get("COURSE_ID").keys():
        return "抱歉， 您访问的课程目前还没上线， 敬请期待-猿变实验室", 404
    # course = CourseService.get_one_by_id(course_id)
    title = current_app.config.get("COURSE_ID").get(course).get("title")
    title = f"猿变{title}从入门到精通"
    course_ids = current_app.config.get("COURSE_ID").get(course).get("courses")
    course_intros = [(
                course_id,
                f"/static/img/course_banner/{course}-{i}_banner.png",
                f"./course/courses_intro/{course}_{i}_lessons.html")
               for i, course_id in enumerate(course_ids)]

    return render_template("course/course_intro.html",
                           title=title,
                           course_intros=course_intros)

#
@course_module.route("/course_notes/")
def course_notes():
    notes = notes_data
    return jsonify(notes)


@course_module.route('/<int:course_id>', methods=['GET'])
@is_vip
@login_required
def show_course(course_id):
    course = CourseService.get_one_by_id(course_id)
    user_notebook = CourseNotebookService.get_content(current_user.user_id, course_id)
    learn_log = None
    next_lesson = None
    if current_user.is_authenticated:
        learn_log = CourseLearnLogService.get_learn_log(user_id=current_user.user_id,
                                                        course_id=course_id)
        if learn_log:
            next_lesson = course.lessons[min(len(course.lessons) - 1, len(learn_log.log))]

    return render_template('course/course_detail.html', course=course,
                           learn_log=learn_log,
                           next_lesson=next_lesson,
                           notebook=user_notebook, course_id=course_id)


@course_module.route('/courses/<int:category_id>/', methods=["GET"])
@is_vip
@login_required
def category_course(category_id):
    return category_lists(category_id, "article")


@course_module.route('/lesson/<int:lesson_id>', methods=['GET', 'POST'])
@is_vip
@login_required
def show_lesson(lesson_id):

    lesson = CourseLessonService.get_one_by_id(lesson_id)
    learn_log = CourseLearnLogService.get_learn_log(user_id=current_user.user_id,
                                                    course_id=lesson.course.id)
    if not learn_log:
        return "", 403
    article_comment_id = lesson.comment_id or lesson.generate_comment_id()
    is_last_lesson = lesson_id == lesson.course.lessons[-1].id
    # if lesson.video:
    alivideo = UploadAliyunVideo()
    play_auth = None
    if lesson.video:
        # play_info = alivideo.get_play_info(video_id)
        play_auth = alivideo.get_video_play_auth(lesson.video[0].video_id)
        # play_url = play_info['PlayInfoList']['PlayInfo'][0]['PlayURL']
    return render_template('course/lesson/lesson_detail.html',
                           lesson=lesson,
                           # play_url=play_url,
                           play_auth=play_auth,
                           course_id=lesson.course_id,
                           course=lesson.course,
                           learn_log=learn_log, is_last_lesson=is_last_lesson,
                           article_comment_id=article_comment_id)


@course_module.route("/play/auth")
@is_vip
@login_required
def get_play_auth():
    video_id = request.args.get("video_id", "", type=str)
    if not video_id:
        return ""
    alivideo = UploadAliyunVideo()
    play_auth = alivideo.get_video_play_auth(video_id)
    return jsonify({"play_auth": play_auth})

@course_module.route('/finish/<int:course_id>', methods=['GET', 'POST'])
@is_vip
@login_required
def show_course_finish(course_id):
    course = CourseService.get_one_by_id(course_id)
    title = "猿变实验专业技能证书"
    user_id = current_user.user_id
    username = current_user.username
    incident = ""
    describe = f"完成{course.title}全部实验，已拥有该实验所必须全部技能"
    certificate_log = CertificateLogService.create_certificate(user_id,
                                                               course_id,
                                                               username,
                                                               title,
                                                               incident,
                                                               describe)
    return render_template("course/course_finish.html",
                           course=course, certificate_log=certificate_log, course_id=course_id)


@course_module.route('/passed/<int:course_id>/<int:lesson_id>/<int:order_id>', methods=['GET', 'POST'])
@is_vip
@login_required
def passed_lesson(course_id, lesson_id, order_id):
    CourseLearnLogService.update_log(
        user_id=current_user.user_id,
        course_id=course_id,
        lesson_id=lesson_id
    )
    return jsonify({
        "res"      : "success",
        "lesson_id": lesson_id
    })
    # next_lesson_id, = CourseLessonService.get_next_lesson(course_id, order_id)
    # if next_lesson_id:
    #     return redirect(url_for(".show_lesson", lesson_id=next_lesson_id))
    # else:
    #     return redirect(url_for(".show_course_finish", course_id=course_id))


@course_module.route('/notebook/<int:course_id>', methods=['POST'])
@is_vip
@login_required
def notebook(course_id):
    # notebook = CourseNotebookService.get_content(current_user.user_id, course_id)
    if request.method == "POST":
        new_content = request.form.get("note_content")
        res = CourseNotebookService.update_content(new_content, current_user.user_id, course_id)
        message = {"res": False}
        if res:
            message = {"res": True}
        return jsonify(message)
    # return render_template("course/yuanbian_notebook.html", notebook=notebook, course_id=course_id)


@course_module.route("/join/<int:course_id>")
@is_vip
@login_required
def join_course(course_id):
    if not current_user.vip_type:
        return redirect(url_for("auth.upgrade2vip"))
    learn_log = CourseLearnLogService.get_learn_log(user_id=current_user.user_id,
                                                    course_id=course_id)
    if not learn_log:
        course = CourseService.get_one_by_id(course_id)
        learn_log = CourseLearnLogService.create_log(
            user_id=current_user.user_id,
            course_id=course_id,
            course_title=course.title
        )

    return redirect(url_for(".show_course", course_id=course_id))


@course_module.route('/video/<video_id>')
@is_vip
@login_required
def play_video():
    pass
    return render_template()

@course_module.route('/certificate/<cert_id>')
def show_certificate(cert_id):
    certificate_log = CertificateLogService.get_one_by_id(cert_id)
    return render_template("course/certificate.html", certificate_log=certificate_log)


def category_lists(category_id, order_type=None):
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['XPCMS_ARTICLE_PER_PAGE']
    pagination = CourseService.get_many(None,
                                        order=order_type,
                                        page=page,
                                        pageSize=per_page)
    courses = pagination.items
    return render_template('course/lists.html',
                           pagination=pagination,
                           courses=courses
                           )


def get_pre_next(model, obj):
    # 前一条
    if obj.category.cate_type == "course":
        prev = model.query.filter(model.category_id == obj.category_id, model.order_id < obj.order_id). \
            order_by(model.order_id.desc()).first()
        _next = model.query.filter(model.category_id == obj.category_id, model.order_id > obj.order_id). \
            order_by(model.order_id.asc()).first()
    else:
        prev = model.query.filter(model.category_id == obj.category_id, model.id < obj.id). \
            order_by(model.id.desc()).first()
        _next = model.query.filter(model.category_id == obj.category_id, model.id > obj.id). \
            order_by(model.id.asc()).first()
    return prev, _next



