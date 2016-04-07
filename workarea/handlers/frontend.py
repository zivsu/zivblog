# !/usr/bin/python
# coding:utf-8

import logging

import markdown2
from tornado.web import HTTPError

from handlers import FrontEndHandler
from settings import EMAIL
from models import user as m_user
from models import article as m_article
from settings import STATUS_PUBLIC
from common.route import route

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

        self.render("frontend/articles.html",
                    web_page="articles",
                    articles=articles,
                    page_amount=page_amount,
                    cur_page=page,
                    tags_stats=tags_stats,
                    tag=tag,
                    hot_articles=hot_articles
                   )

@route("/article/(.*)")
class ArticleHandler(FrontEndHandler):

    def get(self, slug):
        article = m_article.get_article(self.db, slug)
        if article is None:
            raise HTTPError(404)

        m_article.add_pageview(self.db, slug)
        article["content"] = markdown2.markdown(article["content"])
        tags_stats = self.get_sidebar_tags_stats()
        hot_articles = self.get_hot_articles()

        self.render("frontend/article.html",
                    web_page="articles",
                    article=article,
                    tags_stats=tags_stats,
                    hot_articles=hot_articles
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
        self.render("frontend/about.html",
                    web_page="about",
                    user=user
                   )

@route("/(.*)")
class HomeHandler(FrontEndHandler):

    def get(self, _):
        self.render("frontend/index.html",
                    web_page="home"
                   )
