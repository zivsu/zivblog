#!/usr/bin/python
# coding:utf8

import os
import logging

import tornado.web
import tornado.ioloop
from tornado.options import define, options
from tornroutes import route

import urls
import settings
from db_oper import db

try:
    define("port", default="8000", help="run on the given port", type=int)
    define("env", default="local", help="run environment", type=str)
except:
    pass

class Application(tornado.web.Application):

    def __init__(self, db, env, handlers):
        app_settings = {
            "template_path":os.path.join(os.path.dirname(__file__), "templates"),
            "static_path":os.path.join(os.path.dirname(__file__), "static"),
            "cookie_secret":"KJM5DeTyTZOWCH+wyyDNVRlQ4SGwTUrIjbPXBcJRg3U=",
            "xsrf_cookies":True,
            "login_url":"/login"
        }
        if env == "local":
            app_settings["autoreload"] = True
            app_settings["debug"] = True
        logging.info("handlers:{}".format(handlers))
        super(Application, self).__init__(handlers, **app_settings)
        self.db = db
        self.env = env
        # self.app_conf = app_conf

if __name__ == '__main__':
    tornado.options.parse_command_line()
    env = options.env
    _app_conf = settings.CONF[env]
    _db = db.init(_app_conf)
    application = Application(_db, env, route.get_routes())
    application.listen(options.port, xheaders=True)
    logging.info("the app init env as {env} on {port}".format(env=env, port=options.port))
    tornado.ioloop.IOLoop.current().start()
