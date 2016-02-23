# coding:utf-8

import datetime
import logging

import tornado.web
from tornado import httputil

from models import session
from models import user

class BaseHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        sid = self.get_secure_cookie("sid")
        if not sid: return None
        # return session.query_sid(self.db, sid)
        session_doc = session.query_sid(self.db, sid)
        if not isinstance(session_doc, dict):
            # Not found user by the sid.
            return None
        email = session_doc.get("email", None)
        if email is None: return None
        return user.get_user(self.db, email)

    def set_secure_cookie(self, name, value, expires_second=None):
        if expires_second is None:
            expires_second = 3600 * 2
        expires = datetime.datetime.now() + datetime.timedelta(seconds=expires_second)
        super(BaseHandler,self).set_secure_cookie(name, value, expires=expires)

class AdminHandler(BaseHandler):

    @property
    def current_username(self):
        return self.get_current_username()

    def get_current_username(self):
        user = self.get_current_user()
        if user is None: return ""
        return user.get("name", "")


