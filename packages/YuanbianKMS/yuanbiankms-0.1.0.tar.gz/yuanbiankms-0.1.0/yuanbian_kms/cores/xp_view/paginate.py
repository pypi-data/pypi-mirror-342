# -*- coding=utf-8 -*-
import math


class Paginate:

    def __init__(self, total_size, page_size):
        self.total_page = math.ceil(total_size / page_size)
        self.page_size = page_size

    def get_paginate(self, current_page):
        min_page = max(1, current_page-5)
        max_page = min(self.total_page, current_page+5)
        paginate = list(range(min_page, max_page+1))
        return paginate
