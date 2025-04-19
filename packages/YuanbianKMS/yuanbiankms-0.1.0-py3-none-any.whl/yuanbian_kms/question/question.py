# -*- coding=utf-8 -*-
import time
import requests
from quick_encrypt.quick_aes import encode_data
from flask import request, redirect,\
    url_for, render_template, jsonify, session, flash
from flask import current_app
from flask_login import current_user, login_required

import app
from xp_cms.question import question_module
from xp_cms.services.article_service import QuestionService
from xp_cms.services.question_service import QuestionDocumentService, \
    ExerciseLogDocumentService, TestingDocumentService, InternshipScoreLogService
from xp_cms.forms.article_form import QuestionSelectForm
from xp_cms.utils import queryObjToDicts
from xp_cms.extensions import redis


@question_module.route("/")
def index():
    """训练场首页"""
    return render_template("question/question_index.html")



@question_module.route("/testing/<testing_id>")
@question_module.route("/testing/<testing_id>/<int:page>")
def testing(testing_id, page=1):
    """测试试卷页面， 每一页是一道题"""

    if session.get("current_exercise", None) is None:
        # 查看有无未完成的练习
        exercise_log = ExerciseLogDocumentService.get_wait_finish_log(current_user.username, testing_id)
        if exercise_log is None:
            """创建练习记录"""
            try:
                testing_doc = TestingDocumentService.get_one_by_id(testing_id)
                if testing_doc.is_vip and not current_user.vip_type > 0:
                    return redirect(url_for("auth.upgrade2vip"))
                assert testing_doc is not None
            except Exception as e:
                print(e)
                return "", 404
            else:
                exercise_log = ExerciseLogDocumentService.add_new_log(current_user.username, testing_doc)

        session['current_exercise'] = {}
        session['current_exercise']['log_id'] = str(exercise_log.pk)
        session['current_exercise_current_page'] = 1
    else:
        session['current_exercise_current_page'] = page

        exercise_log = ExerciseLogDocumentService.get_one_by_id(session['current_exercise']['log_id'],
                                                                ("testing_id", "testing_title", "question_ids",
                                                                 "answer_log"))

        if exercise_log is None:
            session.pop("current_exercise")
            session.pop("current_exercise_current_page")
            return redirect(url_for(".testing", testing_id=testing_id))
        if testing_id != str(exercise_log.testing_id):
            # flash("您有尚未完成的练习，需要先完成此次练习")
            return render_template("question/reset_erercise_log.html",
                                   current_id=str(exercise_log.testing_id),
                                   testing_id=testing_id
                                   )
    q_index = session['current_exercise_current_page'] - 1
    question = QuestionDocumentService.get_one_by_id(exercise_log.question_ids[q_index])
    default_template = "question/testing.html"
    return render_template(default_template,
                           testing_id=testing_id,
                           question=question,
                           q_id=str(question.pk),
                           answer_log=exercise_log.answer_log,
                           question_ids=exercise_log.question_ids,
                           testing_title=exercise_log.testing_title,
                           page=page
                           )


# 验证答案是否正确
@question_module.route("/question/check/<int:page>", methods=["post"])
def check(page=1):
    """选择题答案验证"""
    if session.get("current_exercise", None) is None:
        return "", 404
    log_id = session['current_exercise']['log_id']
    current_page = page - 1

    # 加载记录
    exercise_log = ExerciseLogDocumentService.get_one_by_id(id=log_id)
    q_id = exercise_log.question_ids[current_page]
    #TODO 如果是考试模式禁止修改答复， 还需要增加刷题模式，允许反复重做
    if q_id in exercise_log.answer_log:
        return {"res": "error", "info": "已经回答过了"}
    question = QuestionDocumentService.get_one_by_id(q_id, ("q_option", "q_score", "q_answer", "is_run_code", "q_input_data", "q_output_data"))
    # exercise_log_question = exercise_log.questions[current_page]
    if question.is_run_code:
        answer_log, option_log, score, res = oj_check(q_id, question, exercise_log)
    else:
        answer_log, option_log, score, res =  select_question_check(q_id, question, exercise_log)
    exercise_log.update(answer_log=answer_log, option_log=option_log, inc__score=score)
    return res

def select_question_check(q_id, question, exercise_log):
    answer_option = request.form["option"]

    # 判断是否正确
    # correct_option = json.loads(exercise_log_question.correct_answers)
    # correct_option = [option.is_correct for option in question.q_option]
    res = {"res"          : "correct",
           "answer_option": answer_option,
           "answer"       : question.q_answer, # 答案解答
           # "correct"      : correct_option
           }
    # answer_log记录正确与否
    answer_log = exercise_log.answer_log
    # option_log记录用户选择
    option_log = exercise_log.option_log
    #TODO 只能记录单选题
    option_log.update({q_id: int(answer_option)})
    if question.q_option[int(answer_option)].is_correct:
        res['res'] = "correct"
        answer_log.update({q_id: True})
        score = question.q_score
    else:
        res['res'] = "error"
        res['info'] = "运行结果不正确"
        answer_log.update({q_id: False})
        score = 0
    return answer_log, option_log, score, jsonify(res)


def oj_check(q_id, question, exercise_log):
    code = request.form['code']
    q_input_data = question.q_input_data
    q_output_data = question.q_output_data
    res = {"res"          : "correct",
           "answer"       : question.q_answer,  # 答案解答
           "time": None,
           }
    answer_log = exercise_log.answer_log
    option_log = exercise_log.option_log
    # 发送请求
    t = encode_data({"username": current_user.username, "env_type": "python"}, current_app.config.get("API_SECRET_KEY"))
    run_result = requests.post(app.config['HOST_PATH']+"/python_oj?t="+t, data={"code":code, "input_data": q_input_data})
    if run_result.status_code == 200:
        run_result = run_result.json()
        # TODO 验证数据类型需要一致
        data_type, data = q_output_data.split(" ", 1)
        option_log.update({q_id: {"code": code, "time":run_result['total_time']} })
        output_data = run_result['exec_result'].strip()
        if data_type != "str":
            data = eval(data)
            output_data = eval(output_data)

        if data == output_data:
            res['res'] = "correct"
            res['time'] = run_result['total_time']
            answer_log.update({q_id: True})
            score = question.q_score
        else:
            res['res'] = "error"
            res['info'] = "运行结果不正确"
            answer_log.update({q_id: False})
            score = 0
    else:
        res['res'] = "error"
        res['info'] = "代码运行异常"
        score = 0
    return answer_log, option_log, score, jsonify(res)

@question_module.route("/reset_exercise_log", methods=["post"])
def reset_testing():

    # 加载记录
    try:
        log_id = session['current_exercise']['log_id']
    except:
        return jsonify({"res": "False"})
    exercise_log = ExerciseLogDocumentService.get_one_by_id(id=log_id)
    if not exercise_log:
        return jsonify({"res": "False"})
    finish_time = round(time.time() - exercise_log.start_time)
    exercise_log.update(score__=0, success__=False,
                        finish__=True, finish_time__=finish_time)
    session.pop("current_exercise")
    return jsonify({"res": "True"})



@question_module.route("/submit_testing")
def submit_testing():
    """提交试卷"""
    if session.get("current_exercise", None) is None:
        return "", 404
    log_id = session['current_exercise']['log_id']
    # 加载记录
    exercise_log = ExerciseLogDocumentService.get_one_by_id(id=log_id)
    # 检查是否跳过
    for index, q_id in enumerate(exercise_log.question_ids):
        if q_id not in exercise_log.answer_log:
            flash("尚未完全答完，需要继续完成！")
            return redirect(url_for(".testing",
                                    testing_id=exercise_log.testing_id,
                                    page=index + 1))

    # 正确数/总数
    score = round(list(exercise_log.answer_log.values()).count(True) / len(exercise_log.answer_log) * 100)
    success = False
    if score >= 85:
        success = True
    finish_time = round(time.time() - exercise_log.start_time)
    exercise_log.update(score__=score, success__=success,
                        finish__=True, finish_time__=finish_time)
    session.pop("current_exercise")
    if exercise_log.is_internship:
        return redirect(url_for(".reg_answer_info", log_id=log_id))

    return redirect(url_for(".exercise_log_detail", log_id=log_id))


@question_module.route("/exercise_log")
def exercise_log():
    """练习记录"""
    logs = ExerciseLogDocumentService.get_all_page(1, 10, conditions=({"username": current_user.username},))
    return render_template("question/exercise_log.html",
                           logs=logs.items,
                           total=len(logs.items))


@question_module.route("/exercise_log/<log_id>")
def exercise_log_detail(log_id):
    """测试记录"""
    exercise_log = ExerciseLogDocumentService.get_ownerlog_by_id(log_id=log_id, username=current_user.username)
    if exercise_log is None:
        return "", 404
    return render_template("question/exercise_log_detail.html",
                           project=exercise_log.testing_title,
                           score=exercise_log.score,
                           success=exercise_log.success,
                           question_ids=exercise_log.question_ids,
                           answer_log=exercise_log.answer_log,
                           exercise_log=exercise_log.pk,
                           finish_time=exercise_log.get_finish_time()
                           )


@question_module.route("/exercise_log/<question_id>/<exercise_log_id>")
def question_log(question_id, exercise_log_id):
    """答题回顾"""
    try:
        question = QuestionDocumentService.get_one_by_id(question_id)
        exercise_log = ExerciseLogDocumentService.get_one_by_id(exercise_log_id)
        assert question is not None
    except Exception:
        return "", 404

    return render_template("question/question_detail.html",
                           question=question,
                           option_log=exercise_log.option_log[question_id]
                           )


@question_module.route("reg_info/<log_id>", methods=["get", "post"])
def reg_answer_info(log_id):
    """校企合作成绩登记"""
    if request.method == "POST":
        try:
            exercise_log = ExerciseLogDocumentService.get_one_by_id(log_id)
            assert exercise_log is not None
            assert exercise_log.is_internship is True
            assert exercise_log.username == current_user.username
            assert exercise_log.is_save is not True
        except:
            return jsonify({"res": "fail"})
        else:
            log_data = {"college_name"  : exercise_log.college_name,
                        "student_number": request.form.get("student_number"),
                        "student_name"  : request.form.get("student_name"),
                        "username"      : current_user.username,
                        "student_score" : exercise_log.score,
                        "testing_name"  : exercise_log.testing_title}
            log = InternshipScoreLogService.add_by_dicts(log_data)
            if log:
                exercise_log.update(is_save=True)
                return jsonify({"res": "success"})
            else:
                return jsonify({"res": "fail"})

    return render_template("question/reg_answer_info.html", log_id=log_id)

# @question_module.route("/interview", defaults={"q_type": None})
# @question_module.route("/interview/<q_type>")
# def interview(q_type):
#     if not session.get('interview_key'):
#         session['interview_key'] = current_user.username + "_interview"
#         session['interview_key_answer'] = current_user.username + "_interview" + "_answer"
#     print(session['interview_key'])
#     if redis.llen(session['interview_key']) >= 20:
#         return ""
#     if not q_type:
#         q_type = "Python基础语法"
#     try:
#         questions = redis.srandmember(q_type, 20)
#     except Exception as e:
#         print(e)
#     else:
#         # redis.rpush(session['interview_key'], question)
#         # question = json.loads(question.decode())
#         # content = question['q_content']
#         # options = json.loads(question['q_options'])
#         # session['option'] = question['q_correct_option']
#         def load_question(question):
#             question = json.loads(question)
#             question.pop("q_answer")
#             # question.pop("q_correct_option")
#             question.pop("q_type")
#             return question
#
#         questions = [load_question(question) for question in questions]
#
#     return render_template("question/question_interview.html",
#                            questions=questions,
#                            )

# @question_module.route("/do_exercise", defaults={"q_type":None})
# @question_module.route("/do_exercise/<q_type>")
# def doExercise(q_type):
#     if not q_type:
#         q_type="Python基础语法"
#     try:
#         question = redis.srandmember(q_type,1)[0]
#     except Exception as e:
#         print(e)
#     else:
#         print(question)
#         question = json.loads(question.decode())
#         content = question['q_content']
#         options = json.loads(question['q_options'])
#         session['option'] = question['q_correct_option']
#
#     return render_template("question/question_doexercise.html",
#                            content=content,
#                            options=options)

