# !/usr/bin/python
# coding:utf-8

import logging

from models import user
from models import session
from handlers import BaseHandler
from common.route import route

@route("/login")
class LoginHandler(BaseHandler):

    def get(self):
        self.render("backend/login.html")

    def post(self):
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        remember = self.get_argument("remember", False)

        if email is None or email == "":
            return self.write({"err":True, "msg":u"邮箱不能为空"})

        if password is None or password == "":
            return self.write({"err":True, "msg":u"邮箱不能为空"})

        result = user.validate_login(self.db, email, password)
        logging.info("login result:{}".format(result))
        err = result["err"]
        if err:
            self.write({"err":True, "msg":result["msg"]})
        else:
            # Add to session. TODO remember me.
            sid = session.add_to_session(self.db, email)
            self.set_secure_cookie("sid", sid)
            self.write({"err":False})

@route("/logout")
class LogoutHandler(BaseHandler):

    def get(self):
        sid = self.get_secure_cookie("sid")
        if sid is not None:
            session.remove_sid(self.db, sid)
            self.clear_cookie("sid")
        self.redirect("/login")
