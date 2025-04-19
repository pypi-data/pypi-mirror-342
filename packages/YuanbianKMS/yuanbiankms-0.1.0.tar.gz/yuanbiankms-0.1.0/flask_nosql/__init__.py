# -*- coding=utf-8 -*-
import decimal, hashlib
import os, json
from functools import wraps
from flask import request, g
from .redis import Redis
from .mongodb import Mongo


class FlaskNoSQL:
    """
    flask NoSQl缓存对象
    """
    app = None
    redis_client = None
    cache_db = None
    ex = 300
    page_ex = 7200
    file_cache_path = "./"
    mongo_client = None

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.ex = app.config.get("CACHE_EX_TIME", 300)
        self.page_ex = app.config.get("PAGE_CACHE_EX_TIME", 2 * 3600)
        self.file_cache_path = app.config.get("FILE_CACHE_PATH", "./")
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions['nosql'] = self
        # if self.app.config.get('OPEN_CACHE'):
        if self.app.config.get("REDIS_URL"):
            self.redis_client = Redis(self.app)

        if self.app.config.get("MONGODB_URL"):
            self.mongo_client = Mongo(self.app)

        if self.app.config.get('CACHE_DB') is None:
            raise RuntimeError("没有配置缓存数据库")
        if self.app.config.get('CACHE_DB') == "redis":
            self.cache_db = self.redis_client

    def set_cache_page(self, url, page):
        print(f"url='{url}'")
        key = hashlib.md5(url.encode()).hexdigest()
        self.cache_db.set(key, page, None)

    def read_cache_page(self, url):
        key = hashlib.md5(url.encode()).hexdigest()
        page = self.cache_db.get(key)
        if page is None:
            return "访问的页面不存在，返回首页<a href=/>猿变手册</a>", 404
        return page

    def delete_page_cache(self, url):
        key = hashlib.md5(url.encode()).hexdigest()
        self.delete(key)

    def get_cache_page(self, cache=True):
        def decorated_function(func):
            @wraps(func)
            def inner_func(*args, **kwargs):
                try:
                    url = os.path.join(kwargs['cate_url'], kwargs['article_url'])
                except Exception:
                    return ""
                return self.read_cache_page(url)

            if cache:
                return inner_func
            else:
                return func

        return decorated_function

    def cache_page(self):
        def decorated_function(func):
            @wraps(func)
            def inner_func(*args, **kwargs):
                # self.app.logger.error(g.client + request.path)
                key = hashlib.md5((request.path + request.args.get('keyword', "")).encode()).hexdigest()
                try:
                    page = self.cache_db.get(key)
                except Exception:
                    page = "页面不存在"
                if page:
                    return page
                page = func(*args, **kwargs)
                if type(page) is tuple:
                    ex = 30
                    page = "页面不存在"
                else:
                    ex = self.page_ex
                self.cache_db.set(key, page, ex)
                return page

            if self.app.config['OPEN_CACHE']:

                return inner_func
            else:
                return func

        return decorated_function

    def cache_view_page(self, cache_time=300):
        def decorated_function(func):
            @wraps(func)
            def inner_func(*args, **kwargs):
                key = hashlib.md5(request.full_path.encode()).hexdigest()
                page = self.cache_db.get(key)
                if page:
                    return page
                page = func(*args, **kwargs)
                if type(page) is tuple:
                    ex = cache_time
                    page = "页面不存在"
                else:
                    ex = cache_time
                self.cache_db.set(key, page, ex)
                return page

            if self.app.config['OPEN_CACHE']:
                return inner_func
            else:
                return func

        return decorated_function

    def clean_page_cache(self, url):
        for client in ("pc", "mobile", "wechat"):
            page_url = client + url
            key = hashlib.md5(page_url.encode()).hexdigest()
            try:
                self.delete(key)
            except Exception as e:
                self.app.logger.error(e)

    def get(self, key):
        return self.cache_db.get(key)

    def set(self, key, value, time=None):
        # if time is None:
        #     time = self.ex
        return self.cache_db.set(key, value, time)

    def incr(self, key):
        return self.cache_db.client.incr(key)

    def exists(self, key):
        return self.cache_db.client.exists(key)

    def expire(self, key, time):
        return self.cache_db.client.expire(key, time)

    def ttl(self, key):
        return self.cache_db.client.ttl(key)

    def delete(self, key):
        return self.cache_db.client.delete(key)

    def save_file_cache(self, file_name, string):
        try:
            file_name = os.path.join(self.file_cache_path, file_name)
            with open(file_name, "w") as f:
                f.write(string)
                f.close()
        except RuntimeError as e:
            self.app.logger.error(e)
            return False
        else:
            return True

    def get_file_cache(self, file_name, type="string"):
        try:
            file_name = os.path.join(self.file_cache_path, file_name)
            with open(file_name, "r") as f:
                data = f.read()
                if type == "string":
                    return data
                elif type == "json":
                    return json.loads(data)
        except RuntimeError as e:
            self.app.logger.error(e)

    # #####################################################
    # 先进先出队列
    # #####################################################
    def push_fifo_queue(self, queue_key, data):
        data = json.dumps(data)
        self.cache_db.client.rpush(queue_key, data)

    def pop_fifo_queue(self, queue_key, data):
        data = self.cache_db.client.blpop(queue_key)
        return json.loads(data)

# #######################################################
# 文档更新
# #######################################################
