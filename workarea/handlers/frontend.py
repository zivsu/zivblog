# !/usr/bin/python
# coding:utf-8

import logging
from StringIO import StringIO
import base64

import markdown2
from tornado.web import HTTPError

import utils
from handlers import FrontEndHandler
from settings import EMAIL
from settings import STATUS_PUBLIC
from common.route import route

from models import user as m_user
from models import article as m_article
from models import comment as m_comment
from models import session as m_session

DEFAULT_HEADIMGURL = "/static/frontend/images/default-avatar.png"
HOME_TITLE = "ZivSu's Blog"
ARTICLES_TITLE = "Articles | ZivSu's Blog"
ABOUT_TITLE = "About Me | ZivSu's Blog"

@route("/articles")
class ArticlesHandler(FrontEndHandler):

    def get(self):
        page = self.get_argument("page", 1)
        tag = self.get_argument("tag", None)
        try:
            page = int(page)
        except:
            raise HTTPError(404)

        articles = m_article.get_articles(self.db, status=STATUS_PUBLIC,
                                          rows=5, page=page, tag=tag)
        page_amount = m_article.get_page_amount(self.db, status=STATUS_PUBLIC,
                                                rows=5)
        tags_stats = self.get_sidebar_tags_stats()
        hot_articles = self.get_hot_articles()
        visitor_num = self.get_visitor_num()

        self.render("frontend/articles.html",
                    articles=articles,
                    page_amount=page_amount,
                    cur_page=page,
                    tags_stats=tags_stats,
                    tag=tag,
                    hot_articles=hot_articles,
                    visitor_num=visitor_num,
                    title=ARTICLES_TITLE
                   )

@route("/article/(.*)")
class ArticleHandler(FrontEndHandler):

    def get(self, slug):
        article = m_article.get_article(self.db, slug)
        if article is None:
            raise HTTPError(404)

        m_article.add_pageview(self.db, slug)
        article["content"] = markdown2.markdown(article["content"])
        article_id = article["_id"]
        comments = m_comment.get_comments(self.db, article_id)

        # Sidebar data.
        tags_stats = self.get_sidebar_tags_stats()
        hot_articles = self.get_hot_articles()
        visitor_num = self.get_visitor_num()


        self.render("frontend/article.html",
                    article=article,
                    comments=comments,
                    tags_stats=tags_stats,
                    hot_articles=hot_articles,
                    visitor_num=visitor_num,
                    title=ARTICLES_TITLE
                   )

@route("/about")
class AboutHandler(FrontEndHandler):

    def get(self):
        user = m_user.get_user(self.db, EMAIL)
        if user is None:
            user = {
                "name": "",
                "en_name": "",
                "email": "",
                "descript": "",
                "wechat": "",
                "github": "",
                "address": "",
            }
        else:
            contact = user["contact"]
            user = {
                "name": user["name"],
                "en_name": user["en_name"],
                "descript": user["descript"],
                "email": contact.get("email", ""),
                "wechat": contact.get("wechat", ""),
                "github": contact.get("github", ""),
                "address": contact.get("address", ""),
            }
        visitor_num = self.get_visitor_num()
        self.render("frontend/about.html",
                    user=user,
                    visitor_num=visitor_num,
                    title=ABOUT_TITLE
                   )

@route("/add/comment")
class AddCommentHandler(FrontEndHandler):

    def post(self):
        slug = self.get_argument("slug", None)
        content = self.get_argument("content", "")
        username = self.get_argument("username", "")
        validate_code = self.get_argument("code", "")
        if username == "":
            return self.write({"err":True, "msg":u"用户名不能为空"})
        if content == "" :
            return self.write({"err":True, "msg":u"评论的内容不能为空"})
        if validate_code == "":
            return self.write({"err":True, "msg":u"验证码不能为空"})
        if slug is None:
            return self.write({"err":True, "msg":u"无效的请求"})

        code_id = self.get_secure_cookie("codeid", None)
        if code_id is None:
            return self.write({"err":True, "msg":u"无效的请求"})

        session = m_session.query_code(self.db, code_id)
        logging.info("session:{}".format(session))
        if session is None:
            logging.info("session expired")
            return self.write({"err":True, "msg":u"验证码过期", "refresh":True})

        if session["code"] != validate_code:
            return self.write({"err":True, "msg":u"验证码错误"})

        comment = {
            "content":content,
            "username":username,
            "headimgurl":DEFAULT_HEADIMGURL,
        }
        new_comment = m_comment.add_one_comment(self.db, slug, comment)
        if new_comment is not None:
            m_session.remove_code(self.db, code_id)
            self.write({"err":False, "comment":new_comment})
        else:
            self.write({"err":True, "msg":u"无效的请求"})

    # def get(self):
    #     self.post()

@route("/validae_code")
class ValidateCodeHnadler(FrontEndHandler):

    def get(self):
        validate_iamge, strs = utils.gen_validate_code(width=120, height=34)
        code_id = self.get_secure_cookie("codeid", None)
        if code_id is None:
            sid = m_session.add_validate_code(self.db, strs)
        else:
            sid = m_session.update_validate_code(self.db, code_id, strs)

        self.set_secure_cookie("codeid", sid)

        buf = StringIO()
        validate_iamge.save(buf, format="PNG")
        self.set_header("Content-type",  "image/png")
        encoded_image = base64.b64encode(buf.getvalue())
        self.write(encoded_image)


@route("/(.*)")
class HomeHandler(FrontEndHandler):

    def get(self, _):
        visitor_num = self.get_visitor_num()
        self.render("frontend/index.html",
                    visitor_num=visitor_num,
                    title=HOME_TITLE
                   )
