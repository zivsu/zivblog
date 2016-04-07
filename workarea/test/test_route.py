# !/usr/bin/env python
# coding=utf-8

import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from tornado.web import RequestHandler

from common.route import route

@route("/test")
def TestHandler(RequestHandler):

    def get(self):
        pass

def test_get_routes():
    print route.get_routes()

if __name__ == '__main__':
    test_get_routes()