# -*- coding=utf-8 -*-
import json
import html
from flask import Flask, request, render_template, url_for, \
    jsonify, current_app, redirect

from flask_login import current_user

from xp_cms.member.member_module import member_module
from .member_menus import Member_Menus
from xp_cms.services.user_service import UserService
from xp_cms.services.account_service import AccountService
from xp_cms.services.question_service import ExerciseLogDocumentService
from xp_cms.services.course_service import CourseLearnLogService


# from xp_mall.models.goods import Goods
# from xp_mall.models.order import Order, OrderGoods, Cart
# from xp_mall.extensions import db
# from xp_mall.member import  member_module
# from xp_mall.forms.order  import SearchForm

@member_module.route("/")
def member_index():
    return render_template("member/pc/index.html")


@member_module.route("/welcome")
def welcome():
    ai_power = 0
    account = AccountService.get_account(current_user.user_id)
    if account:
        ai_power = account.points
        token_coin = account.token_coin

    exer_log_count = ExerciseLogDocumentService.count(current_user.username)
    exer_log_count_success = ExerciseLogDocumentService.count_success(current_user.username)
    exer_log_score_avg = ExerciseLogDocumentService.avg_score(current_user.username)
    # 挑战分组统计
    exer_log = ExerciseLogDocumentService.group_by_testing_id(current_user.username)
    exer_log = list(map(clear_field, exer_log))
    # 最近一周挑战记录
    week_exer_log = ExerciseLogDocumentService.last_week(current_user.username)

    # 实验记录
    last_10_course = CourseLearnLogService.get_last_10_log(current_user.user_id)

    return render_template("member/pc/welcome.html", ai_power=ai_power,
                           exer_log_count=exer_log_count,
                           exer_log_count_success=exer_log_count_success,
                           exer_log_score_avg=exer_log_score_avg,
                           exer_log=json.dumps(exer_log),
                           week_exer_log=week_exer_log,
                           last_10_course=last_10_course,
                           token_coin=token_coin
                           )


@member_module.route("/exercise_log")
def exercise_log():
    page = request.args.get("page", 1, int)
    page_size = 10
    logs = ExerciseLogDocumentService.get_all_page(page, page_size, conditions=({"username": current_user.username},))
    return render_template("member/pc/exercise/exercise_log.html",
                           logs=logs)



@member_module.route("/my_courses")
def my_courses():
    page = request.args.get("page", 1, int)
    page_size = 10
    my_courses = CourseLearnLogService.get_all_page(page, page_size,
                                                    conditions=({"user_id": current_user.user_id},))
    return render_template("member/pc/course/my_course.html",
                           my_courses=my_courses)

# @member_module.route("/cart")
# def cart_list():
#     cart_list = Cart.query.filter_by(user_id=current_user.user_id).all()
#     return render_template("member/cart/cart_list.html", cart_list=cart_list)


# @member_module.route('/myorders', defaults={'page': 1})
# @member_module.route('/myorders/<int:page>', methods=['GET'])
# def manage_orders(page):
#     form = SearchForm()
#     order_query =  Order.query.filter_by(buyer=current_user.user_id)
#     status = request.args.get("status", None)
#     if status:
#         form.status = status
#         order_query = order_query.filter_by(status=status)
#     #
#     keyword = request.args.get("keyword", None)
#     if keyword:
#         form.keyword.data = keyword
#         order_query = order_query.whooshee_search(keyword)
#
#     if request.args.get("order_type"):
#         order_type = request.args.get("order_type")
#         form.order_type.data = order_type
#         if order_type == "1":
#             order_type = Order.create_time.asc()
#         elif order_type == "2":
#             order_type = Order.create_time.desc()
#         elif order_type == "3":
#             order_type = Order.price.asc()
#         else:
#             order_type = Order.create_time.desc()
#         order_query = order_query.order_by(order_type)
#     print(order_query)
#     pagination = order_query.paginate(
#          page,current_app.config['XPMALL_MANAGE_GOODS_PER_PAGE'])
#     condition = request.query_string.decode()
#     return render_template('member/order/order_list.html', page=page,
#                            pagination=pagination, form=form,
#                            condition=condition)

def clear_field(item):
    item.pop("_id")
    return item



