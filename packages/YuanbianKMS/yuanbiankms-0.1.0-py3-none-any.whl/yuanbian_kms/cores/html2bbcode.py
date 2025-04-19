# -*- coding=utf-8 -*-
from html.parser import HTMLParser
import re


class HTML2BBCODE(HTMLParser):
    pass


# def secure_html(html_code):
#     general_tag = {"pattern": "<(?P<tag>[a-z0-9]+)[\s\S]*?>(?P<html>[\s\S]+)</(?P=tag)>",
#                    "replace": "[{tag}]{html}[/{tag}]"
#                    }
#
#     def replace_pattern(res):
#         print(res.groups())
#         return general_tag['replace'].format(tag=res.group("tag"), html=res.group("html"))
#
#     res = re.sub(general_tag['pattern'], replace_pattern, html_code)
#     return res


# def secure_html(html_code):
#     general_tag = {"pattern": "<(?P<tag>)[\s\S]*?>(?P<html>[\s\S]+)</(?P=tag)(?P=level)>",
#            "replace": "[{tag}]%s[/{tag}]"
#            }
#
#     def replace_pattern(res):
#         return h_tag['replace'] % (res.group("level"), res.group("html"), res.group("level"))
#
#     res = re.sub(h_tag['pattern'], replace_pattern, html_code)


# general_tag = {"pattern": "<(?P<tag>[a-z0-9]+)[\s\S]*?>(?P<html>[\s\S]+)</(?P=tag)>",
#                "replace": "[{tag}]{html}[/{tag}]"
#                }

# 将<script>变成实体，并过滤各种添加的属性
def secure_html(html_code):
    general_tag = {"pattern": r"<(?P<tag>/{0,1}[a-z0-9]+)\s*([\s\S]*?)>",
                   "replace": "&lt;{tag}&gt;"
                   }

    def replace_pattern(res):
        tag = res.group("tag")
        if tag.lower() in ["script", "/script", "img", "video", "audio", "/video", "/audio"]:
            return general_tag['replace'].format(tag=res.group("tag"))
        else:
            return "<{tag}>".format(tag=res.group("tag"))
        # return general_tag['replace'].format(tag=res.group("tag"), html=res.group("html"))

    res = re.sub(general_tag['pattern'], replace_pattern, html_code)
    return res
