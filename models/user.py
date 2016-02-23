# !/usr/bin/python
# coding:utf-8

import logging

import utils

COLL_USER = "user"
COLL_LOG_LOGIN = "log_login"

def create_account(db, account):
    account["created_at"] = utils.get_cur_utc_timestamp()
    password = account["password"]
    salt = account["salt"]
    account["password"] = utils.salt_password(salt, password)
    db[COLL_USER].insert(account, w=1)

def validate_login(db, email, password):
    doc = db[COLL_USER].find_one({"email":email}, {"password":True,
                                 "salt":True})
    if doc is None:
        return {"err":True, "msg":u"当前邮箱不存在"}

    real_password = doc["password"]
    salt = doc["salt"]
    try:
        salted_password = utils.salt_password(salt, password)
    except:
        logging.warning("invalid password")
        timestamp = utils.get_cur_utc_timestamp()
        db[COLL_LOG_LOGIN].insert({"password":password, "email":email,
                                  "timestamp":timestamp})
        return {"err":True, "msg":"当前密码错误"}

    if salted_password != real_password:
        return {"err":True, "msg":"当前密码错误"}
    else:
        return {"err":False}

def get_user(db, email):
    doc = db[COLL_USER].find_one({"email":email}, {"name":True,
                                 "descript":True, "contact":True,
                                 "en_name":True})
    if doc is None:
        return None
    prepared = {
        "name": doc.get("name", ""),
        "en_name": doc.get("en_name", ""),
        "email": email,
        "descript": doc.get("descript", ""),
        "contact": doc.get("contact", {})
    }
    return prepared


def update_user(db, user):
    email = user["email"]
    name = user["name"]
    en_name = user["en_name"]
    descript = user["descript"]
    contact = user["contact"]
    return db[COLL_USER].find_and_modify({"email":email}, update={"$set":
                                         {"name":name, "en_name":en_name,
                                         "descript":descript,"contact":contact}},
                                         new=1)
