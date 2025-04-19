# -*- coding=utf-8 -*-

from flask import Blueprint


article_module = Blueprint("article", __name__)

from xp_cms.article.article import *
