# !/usr/bin/python
# coding:utf-8

import logging

from settings import DEFAULT_ROWS, STATUS_PUBLIC

DEFAULT_STATUS = STATUS_PUBLIC

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

def get_articles(db, tag=None, page=None, status=DEFAULT_STATUS,
                rows=DEFAULT_STATUS):
    pass
