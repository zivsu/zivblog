# !/usr/bin/python
# coding:utf-8

import logging

from tornado.web import authenticated
from tornado.web import HTTPError

import utils
from handlers import AdminHandler
from models import user as m_user
from models import article as m_article
from models import tag as m_tag
from settings import STATUS_PUBLIC, STATUS_SAVE, STATUS_DELETE,  DEFAULT_ROWS
from common.route import route


@route("/backend/index")
class AdminIndexHandler(AdminHandler):

    @authenticated
    def get(self):
        username = self.current_username
        self.render("backend/index.html", username=username)


@route("/backend/article_edit")
class AdminArticleEditHandler(AdminHandler):

    def get(self):
        slug = self.get_argument("slug", None)
        tags = m_tag.get_tags(self.db)
        default_tag = tags[0] if len(tags) >= 1 else "python"
        logging.info("default tag:{}".format(default_tag))
        default_article = {
            "title":"",
            "abstracts":"",
            "content":"",
            "slug":"",
            "tag":default_tag,
            "date":utils.get_today_date(),
        }
        article_id = ""
        if slug is not None:
            # Edit exists article
            default_article = m_article.get_article(self.db, slug)
            article_id = str(default_article["_id"])

        username = self.current_username
        self.render("backend/article_edit.html",
                    username=username,
                    article=default_article,
                    tags=tags,
                    article_id=article_id,
                    )

    def post(self):
        article_id = self.get_argument("id", "")
        title = self.get_argument("title", None)
        abstracts = self.get_argument("abstracts", "")
        content = self.get_argument("content", "")
        slug = self.get_argument("slug", None)
        tag = self.get_argument("tag", None)
        date = self.get_argument("date", None)
        status = self.get_argument("status", None)

        if title is None or title == "":
            return self.write({"err":True, "msg":u"标题不能为空"})

        if slug is None or slug == "":
            return self.write({"err":True, "msg":u"slug不能为空"})

        is_unique_slug = m_article.is_unique_slug(self.db, slug, article_id)
        logging.info("is unique slug:{}".format(is_unique_slug))
        if not is_unique_slug:
            return self.write({"err":True, "msg":u"当前slug已存在"})

        if tag is None or tag == "":
            return self.write({"err":True, "msg":u"标签不能为空"})

        if status not in [STATUS_PUBLIC, STATUS_SAVE]:
            return self.write({"err":True, "msg":u"文章status不正确"})

        if date is None:
            date = utils.get_today_date()

        article = {
            "title":title,
            "abstracts":abstracts,
            "content":content,
            "slug":slug,
            "tag":tag,
            "date":date,
            "status":status,
        }
        result = m_article.update_article(self.db, article)
        if result:
            self.write({"err":False, "msg":u"操作成功！"})
        else:
            self.write({"err":True, "msg":u"操作失败！稍后再试"})


@route("/backend/article_list")
class AdminArticleListHandler(AdminHandler):

    def get(self):
        page = self.get_argument("page", 1)
        try:
            page = int(page)
        except:
            logging.exception(">> page argument is not int")
            raise httperror(404)

        username = self.current_username
        articles = m_article.get_articles(self.db, page=page, rows=DEFAULT_ROWS)
        page_amount = m_article.get_page_amount(self.db, rows=DEFAULT_ROWS)
        self.render("backend/article_list.html",
                    username=username,
                    page_amount=page_amount,
                    cur_page=page,
                    articles=articles
                    )

@route("/backend/article_delete")
class AdminArticleDeleteHandler(AdminHandler):

    def get(self):
        slug = self.get_argument("slug", None)
        if slug is not None:
            m_article.delete_article(self.db, slug)
        self.redirect("/backend/article_list")

@route("/backend/article_trash")
class AdminArticleTrashHandler(AdminHandler):

    def get(self):
        page = self.get_argument("page", 1)
        try:
            page = int(page)
        except:
            logging.exception(">> page argument is not int")
            raise httperror(404)

        username = self.current_username
        articles = m_article.get_articles(self.db, page=page, rows=DEFAULT_ROWS, status=STATUS_DELETE)
        page_amount = m_article.get_page_amount(self.db, rows=DEFAULT_ROWS)
        self.render("backend/article_trash.html",
                    username=username,
                    page_amount=page_amount,
                    cur_page=page,
                    articles=articles
                    )

@route("/backend/article_detail/(.*)")
class AdminArticleDetailHandler(AdminHandler):

    def get(self, slug):
        logging.info("******** slug *********")
        logging.info("slug:{}".format(slug))
        article = m_article.get_article(self.db, slug)
        if article is None:
            raise HTTPError(404)

        username = self.current_username
        self.render("backend/article_detail.html",
                    username=username,
                    article=article
                    )

@route("/backend/profile")
class AdminProfileHandler(AdminHandler):

    @authenticated
    def get(self):
        user = self.current_user
        username = user.get("name", "")
        contact = user.get("contact", {})
        user_info = {
            "name":username,
            "en_name":user.get("en_name", ""),
            "descript":user.get("descript", ""),
            "wechat":contact.get("wechat", ""),
            "github":contact.get("github", ""),
            "email":contact.get("email", ""),
            "address":contact.get("address", ""),
        }
        logging.info("user info:{}".format(user_info))
        self.render("backend/profile.html",
                    username=username,
                    user=user_info)

    def post(self):
        name = self.get_argument("name", "")
        en_name = self.get_argument("en_name", "")
        wechat = self.get_argument("wechat", "")
        github = self.get_argument("github", "")
        contact_email = self.get_argument("email", "")
        address = self.get_argument("address", "")
        descript = self.get_argument("descript", "")

        user = self.current_user
        if user is None:
            return self.write({"msg":u"请重新登陆，当前用户已失效"})

        email = user.get("email", None)
        if email is None:
            return self.write({"msg":u"请重新登陆，当前用户已失效"})

        user_info = {
            "email":email,
            "name":name,
            "en_name":en_name,
            "descript":descript,
            "contact":{
                "wechat":wechat,
                "github":github,
                "email":contact_email,
                "address":address,
            }
        }
        logging.info("user info:{}".format(user_info))
        result = m_user.update_user(self.db, user_info)
        if result is None:
            self.write({"msg":u"更新失败，请稍后再试"})
        else:
            self.write({"msg":u"更新成功！"})

