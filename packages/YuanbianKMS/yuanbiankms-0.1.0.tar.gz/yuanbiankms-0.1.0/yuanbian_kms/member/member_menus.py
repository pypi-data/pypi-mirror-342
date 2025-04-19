# -*- coding=utf-8 -*-

Member_Menus = {
    'profile':[
        "我的资料",
        ("统计报表","member_index"),
        ("资料修改","edit_profile"),
    ],
    'account':[
        "我的账户",
        ("账户明细", "account_details"),
        ("推广链接", "get_promotion_link")
    ],
    'security':[
        "安全设置",
        ("认证邮箱", "set_approve_email"),
        ("修改密码", "reset_password")
    ],
    # 'article':[
    #     "文章管理",
    #     ("文章发布", "article_publish"),
    #     ("已发布文章", "article_list"),
    #     ("待审核文章", "draft_list"),
    # ],
    'studio':[
        "实验台",
        ("运行状况", "mystudio"),
        ("实验中心", "jupyterlab")
    ]
    # 'study':[
    #     "我的学习",
    #     ("文章发布", "article_post"),
    #     ("文章列表", "article_list")
    # ],
    # 'courseware':[
    #     "我的课件",
    #     ("文章发布", "article_post"),
    #     ("文章列表", "article_list")
    # ]
}

