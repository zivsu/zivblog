# !/usr/bin/python
# coding:utf-8

import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from pymongo import ASCENDING

import settings
from db_oper import db
from models.session import COLL_SESSION, COLL_VALIDATE_CODE

SESSION_EXPIRE_TIME = 3600 * 2
SESSION_CODE_EXPIRE_TIME = 2

def ensure_indexes(db):
    # try:
    #     db[COLL_SESSION].ensure_index([("create_at", ASCENDING)],
    #                                   expireAfterSeconds=SESSION_EXPIRE_TIME)
    # except:
    #     pass

    try:
        db[COLL_VALIDATE_CODE].ensure_index([("create_at", ASCENDING)],
                                    expireAfterSeconds=SESSION_CODE_EXPIRE_TIME)
    except:
        pass

if __name__ == '__main__':
    env = "local"
    app_conf = settings.CONF[env]
    _db = db.init(app_conf)
    ensure_indexes(_db)