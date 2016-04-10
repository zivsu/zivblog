# coding:utf-8

import datetime
import logging

import tornado.web
from tornado import httputil

from models import session
from models import user
from models import article
from models import track
import utils

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

    # def write_error(self, status_code, **kwargs):
    #     # TODO.
    #     pass


class AdminHandler(BaseHandler):

    @property
    def current_username(self):
        return self.get_current_username()

    def get_current_username(self):
        user = self.get_current_user()
        if user is None: return ""
        return user.get("name", "")


class FrontEndHandler(BaseHandler):

    def get_sidebar_tags_stats(self):
        return article.get_tags_stats(self.db)

    def get_hot_articles(self, limit=5):
        return article.get_hot_articles(self.db, limit)

    def get_visitor_num(self):
        return track.get_visitor_num(self.db)

    def track_pageview(self):
        user_agent = self.request.headers.get("User-Agent", None)
        uri = self.request.uri
        view_info = {
            "ip":self.request.remote_ip,
            "useragent":user_agent,
            "timestamp":utils.get_cur_utc_timestamp(),
            "uri":uri
        }
        track.save_pageview(self.db, view_info)

    def prepare(self):
        # track pageview
        self.track_pageview()