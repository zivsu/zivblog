#!/usr/bin/python
# coding:utf8

from pymongo import MongoClient

def init(app_conf):
    db_info = app_conf["db"]
    _db_name = db_info["db_name"]
    _db_host = db_info["db_host"]
    client = MongoClient(host=_db_host)
    db = client[_db_name]
    return db

