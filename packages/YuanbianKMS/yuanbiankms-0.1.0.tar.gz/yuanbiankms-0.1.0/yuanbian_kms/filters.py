# -*- coding=utf-8 -*-
import re, time, datetime
from uuid import uuid4
from xp_cms.services.article_service import ArticleService
from xp_cms.services.course_service import CourseLessonService

def substr_center(s, width):
    start = len(s)//2-width if len(s)//2 > width else 0
    end = len(s)//2+width if len(s)//2 > width else len(s)
    return s[start:end]

def pre_to_monaco(s):
    pre_pattern = '<pre\s*[class=\"prettyprint\"]*>(?P<code>[\s\S]*?)<\/pre>'
    def replace_pattern(res):
        dataId= uuid4()
        return """<pre style="display:none" id="%s">\n%s</pre>
        <iframe id="iframe_%s" scrolling=no src="/static/js/monaco/code_inline.html?language=python&theme=hc-black&fontSize=14px&dataId=%s"></iframe> """ %  (dataId,
                                                                 res.group("code"),
                                                                 dataId,
                                                                 dataId)
    return re.sub(pre_pattern, replace_pattern, s)

def pre_to_code(s, language="python"):
    pre_pattern = '<pre\s*[class=\"prettyprint\"]*>(?P<code>[\s\S]*?)<\/pre>'
    language = "python" if language == "notebook" else language
    if s is None:
        return ""
    s = s.replace("\n\n# %%\n\n", "")
    s = re.sub("&quot;&quot;&quot;[\s\S]*?&quot;&quot;&quot;\n", "", s)
    def replace_pattern(res):
        nonlocal language
        # language_pattern = "[\s*a-z\/\!#]+?(?P<language>python|html)"
        code = res.group("code")
        try:
            # language = "language-"+re.match(language_pattern, code).group("language")
            language_style = f"language-{language}"
        except Exception as e:
            language_style = "python"
        return """<pre><code class="%s">%s</code></pre>""" %  (language_style, code.strip())
    return re.sub(pre_pattern, replace_pattern, s)


def to_datetime(t=None, format=None):
    if t is None:
        t = time.time()
    if format is None:
        format = "%Y-%m-%d %H:%M:%S"
    if type(t) in (int, float):
        return datetime.datetime.fromtimestamp(t).strftime(format)
    return t.strftime(format)


def get_comment_topical(comment_id, page_type):
    title = intro = ""
    if page_type == "article":
        try:
            title, intro = ArticleService.get_summary_by_comment_id(comment_id)
        except Exception as e:
            pass
    if page_type == "lesson":
        try:
            title, intro = CourseLessonService.get_summary_by_lesson_id(comment_id)
        except Exception as e:
            pass
    if intro:
        return f"<h4>{title}</h4><q>{intro}</q>"
    else:
        return f"<h4>{title}</h4>"
