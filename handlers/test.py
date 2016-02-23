#!/usr/bin/python
# coding:utf8

import tornado.web
from tornroutes import route

@route("/test")
class TestHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Hello, world")
