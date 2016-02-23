# !/usr/bin/python
# coding:utf-8

import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__)))

import settings
from db_oper import db
from models import user
from models import tag

env = "local"
# env = "prod"
app_conf = settings.CONF[env]
_db = db.init(app_conf)

def create_login_account():
    user.create_account(_db, settings.ACCOUNT)

def init_tags():
    tags = settings.INIT_TAGS
    tag.add_tags(_db, tags)

if __name__ == '__main__':
    # create_login_account()
    init_tags()