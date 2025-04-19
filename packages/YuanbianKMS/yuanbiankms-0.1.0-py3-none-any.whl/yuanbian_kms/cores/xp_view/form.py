# -*- coding=utf-8 -*-
from flask_wtf import FlaskForm


class XPBaseForm(FlaskForm):
    edit_fields = ()
    def process(self, *args, **kwargs):
        super().process(*args, **kwargs)

    def data_to_dicts(self):
        pass
