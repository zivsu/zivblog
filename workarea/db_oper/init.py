# !/usr/bin/python
# coding:utf-8

from pymongo import ASCENDING

from models.sessiom import COLL_SESSION

SESSION_EXPIRE_TIME = 3600 * 2

def ensure_indexes(db):
    try:
        db[COLL_SESSION].ensure_index([("created_at", ASCENDING)],
                                      expireAfterSeconds=SESSION_EXPIRE_TIME)
    except:
        pass

