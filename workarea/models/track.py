# coding=utf-8

COLL_PAGEVIEW = "pageview"

def save_pageview(db, view_info):
    db[COLL_PAGEVIEW].insert(view_info, w=1)