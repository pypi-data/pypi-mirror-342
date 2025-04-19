# -*- coding=utf-8 -*-

import os
from datetime import date
from flask import render_template, flash, redirect, url_for, request,\
    current_app, Blueprint, send_from_directory, session
from flask_login import  current_user, login_required
# from xp_cms.utils import redirect_back, allowed_file, rename_image, resize_image
from xp_cms.extensions import db

question_module = Blueprint("question", __name__)

from xp_cms.question.question import *

@question_module.before_request
@login_required
def is_login():
    pass