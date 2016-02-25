# !/usr/bin/python
# coding:utf-8

import logging

from settings import STATUS_SAVE, STATUS_PUBLIC, STATUS_DELETE

COLL_ARTICLE = "article"

def is_unique_slug(db, slug, article_id):
    doc = db[COLL_ARTICLE].find_one({"slug":slug}, {"_id":True})
    if doc is None: return True
    if str(doc["_id"]) == article_id: return True
    return False

def update_article(db, article):
    slug = article["slug"]
    return db[COLL_ARTICLE].find_and_modify({"slug":slug}, {"$set":article},
                                            upsert=True, new=True)

def get_article(db, slug):
    return db[COLL_ARTICLE].find_one({"slug":slug})

def get_articles(db, tag=None, page=None, status=None, rows=0):
    filter_doc = {}
    if status is not None:
        filter_doc ["status"] = status
    if tag is not None:
        filter_doc ["tag"] = tag
    skip = rows * (page - 1) if page is not None else 0
    kwargs = {"limit":rows, "skip":skip, "sort":[("date", -1)]}
    articles_cursor = db[COLL_ARTICLE].find(filter_doc, {"_id":False}, **kwargs)
    articles = []
    article_status = {
        STATUS_SAVE: "save",
        STATUS_PUBLIC: "publish",
        STATUS_DELETE: "delete",
    }
    for article in articles_cursor:
        article["status"] = article_status.get(article["status"], "")
        articles.append(article)
    return articles

def get_page_amount(db, rows, tag=None, status=None):
    article_amount = len(get_articles(db, tag=tag, status=status))
    if not isinstance(rows, int): return 0
    if rows == 0: return 0
    page_amount = article_amount % rows
    if page_amount == 0:
        # 0 / 5, 10 / 5
        page_amount = article_amount / rows
    else:
        # 1 / 5, 6 / 5
        page_amount = article_amount / rows + 1
    return page_amount