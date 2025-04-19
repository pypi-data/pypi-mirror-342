# -*- coding=utf-8 -*-
import re, json, hashlib
from functools import wraps
from xp_cms.extensions import nosql


try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin
from flask import current_app, session, request, redirect,  url_for
from xp_cms.models.article import Category
from xp_cms.services.user_service import UserService, WechatOAuthService
from xp_cms.services.article_service import CategoryService
from xp_cms.extensions import db, nosql
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from itsdangerous import BadSignature, SignatureExpired


def queryObjToDicts(obj, keys):
    lists = [{key: getattr(item, key) for key in keys} for item in obj]
    return lists

def queryObjToDicts_deep(obj_list, keys, deep_keys):
    lists = []
    for obj in obj_list:
        item = {}
        for key in keys:

            if key in deep_keys:

                item[key] = queryObjToDicts_deep(getattr(obj,key), keys, deep_keys)
            else:
                item[key] = getattr(obj,key)
        lists.append(item)
    return lists

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def redirect_back(default='index', **kwargs):
    for target in (session.get('redirect_url', None), request.args.get('next')):
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))




def get_all_subcate(cate_id):
    category = CategoryService.get_one_by_id(cate_id)
    all_subcates = CategoryService.get_many([{"field": 'cate_parents',
                                             "value": category.cate_parents + "," + category.cate_id+",%",
                                             "operator": "in"}])
    return all_subcates.items()



def get_all_parent(cate_id):
    '''
    获得某个分类的所有父类
    :param id:
    :return:
    '''
    try:
        # category = db.session.query(Category).get(cate_id)
        category = CategoryService.get_one_by_id(cate_id)
    except Exception as e:
        db.session.commit()
        current_app.logger.error(e)
        return None
    if category is None:
        return None
    if category.parent_id:
        return [(category.name, category.cate_id, category.sub_cates)]+get_all_parent(category.parent_id)
    else:
        return [(category.name, category.cate_id, category.sub_cates)]

# def get_all_subcate(cate_id):
#     # redis all_subcate_cateid为缓存key名
#     key = "all_subcate_cate_%s" % cate_id
#     print(key)
#     sub_cates = redis.get(key)
#     if sub_cates:
#         return json.loads(sub_cates)
#
#     all_cate_id = get_all_subcate_id(cate_id, [])
#
#     nosql.set(key, str(all_cate_id))




def get_all_cates(current_cate_id):
    """多级菜单数据结构
    [[{cate1},{cate2},{cate3}],[{subcate1},{subcate2}, {subcate3}],...[{current_cate}]]
    ,最后的包含当前current_cate_id
    """
    category = CategoryService.get_one_by_id(current_cate_id)
    all_parents =  CategoryService.get_many([{"field": "cate_id",
                                              "value": category.cate_parents[1:].split(","),
                                              "operator": "in"}]
                                            )
    top_cates = CategoryService.get_many([{
        'field': 'parent_id',
        'value': None,
        'operator': "eq"
    }])
    cates = list()
    # 最顶层一级分类，当前类别所属的祖先分类选中
    cates.append(top_cates.items)
    # 祖先分类的子分类，当前类别所属的祖先分类选中
    # print(all_parents.items)
    # print(type(all_parents.items))
    # for parents in all_parents.items:
    #     print(parents)
        # cates.append(parents.sub_cates)
    # print(cates)
    return cates

#
# def generate_token(user, operation, expire_in=None, **kwargs):
#     s = Serializer(current_app.config['SECRET_KEY'], expire_in)
#     data = {'id': user.id, 'operation': operation }
#     data.update(**kwargs)
#     return s.dumps(data)

# def validate_token(user, token, operation):
#     s = Serializer(current_app.config['SECRET_KEY'])
#     try:
#         data = s.loads(token)
#     except (SignatureExpired, BadSignature):
#         return False
#
#     if operation != data.get('operation') or user.id != data.get('id'):
#         return False
#
#     if operation == Operations.CONFIRM:
#         user.confirmed = True
#     else:
#         return False
#
#     db.session.commit()
#     return True


def show_username(username):
    if username.startswith("yuanbian"):
        return username[:12] + "******" + username[-3:]
    else:
        return username
