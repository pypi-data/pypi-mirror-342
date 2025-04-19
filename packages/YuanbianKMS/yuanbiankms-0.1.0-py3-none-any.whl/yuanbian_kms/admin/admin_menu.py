# -*- coding=utf-8 -*-
Admin_Menus = {
    'article': [
        "文章管理",
        ("文章列表", "manage_article"),
        ("文章发布", "new_article"),
        ("投稿审核", "member_draft"),
        ("刷新缓存", "update_all_cache")
        # ("评论管理", "manage_comment")
    ],
    'category': [
        "分类管理",
        ("分类管理", "manage_category"),
        ("添加分类", "new_category"),
    ],
    'user': [
        "会员管理",
        ("会员列表", "manage_member")
    ],
    'question': [
        "猿力测试",
        ("题库类型", "manage_question_type"),
        ("添加类型", "new_question_type"),
        ("题库管理", "manage_question"),
        ("添加题库", "new_question"),
        ("批量添加题库", "question_batch_loads"),
        ("管理试卷", "manage_testing"),
        ("添加试卷", "new_testing"),
        ("实训记录", "internship_log")

    ],
    'studios': [
        "工作台管理",
        ("添加宿主机", "new_host"),
        ("宿主机管理", "manage_host"),
        ("Stuio列表", "manage_studio"),

    ],
    'course': [
        "课程管理",
        ("课程列表", "manage_course"),
        ("添加课程", "new_course")

    ],
    'active_code': [
            "激活码",
            ("激活码生成", "active_code_generate"),
            ("激活码管理", "active_code_manage")
        ]


}
