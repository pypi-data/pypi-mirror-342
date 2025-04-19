# -*- coding=utf-8 -*-
from flask import request
from flask.views import View


class ListView(View):
    template = None
    fields = []
    methods = ["GET"]
    form = None
    def dispatch_request(self):

        meth = self.__getattribute__(request.method.lower())
    
    def get(self):
        pass
    
    def post(self):
        pass


