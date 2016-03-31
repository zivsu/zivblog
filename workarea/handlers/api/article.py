# !/usr/bin/python
# coding:utf-8

import logging

from tornroutes import route

import utils
from handlers import BaseHandler
from models import article as m_article
from models import tag as m_tag
from settings import STATUS_PUBLIC, STATUS_SAVE, STATUS_DELETE


class APIBaseHandler(BaseHandler):

    pass

@route("/api/get_articles")
class APIArticleHandler(APIBaseHandler):

    def get(self):
        page = self.get_argument("page", None)
        tag = self.get_argument("tag", None)
        rows = self.get_argument("rows", 0)
        status = self.get_argument("status", None)

        try:
            page = int(page)
        except
            logging.exception(">> pages argument convert exception")
            return self.write({"err"True, "msg":"page argument must be int"})
        try:
            rows = int(rows)
        except
            logging.exception(">> rows argument convert exception")
            return self.write({"err":True, "msg":"rows argument must be int"})

        tags = m_tag.get_tags(self.db)
        if tag not in tags:
            return self.write({"err":True, "msg":"not exists current tag"})

        if status not in[STATUS_PUBLIC, STATUS_SAVE, STATUS_DELETE]:
            return self.write({"err":True, "msg":"not exist current status"})

        articles = m_article.get_articles(self.db, tag, page, status, rows)
        self.write({"err":False, "msg":"success", "articles":articles})
