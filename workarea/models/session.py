# !/usr/bin/python
# coding:utf-8

import logging
import datetime

from bson.objectid import ObjectId

COLL_SESSION = "session"
COLL_VALIDATE_CODE = "session_validate_code"

def _transform_sid(db, sid):
    try:
        return ObjectId(sid)
    except:
        loging.exception("invalid sid:{}".format(sid))
        return None

def query_sid(db, sid):
    _id = _transform_sid(db, sid)
    if _id is None: return None
    # doc = db[COLL_SESSION].find_one({"_id":_id}, {"email":True})
    # if doc is None:
    #     return None
    # return doc.get("email", None)
    return db[COLL_SESSION].find_one({"_id":_id})

def add_to_session(db, email):
    create_at = datetime.datetime.utcnow()
    doc = db[COLL_SESSION].find_and_modify({"email":email}, update={"$set":
                                           {"create_at":create_at}}, upsert=True, new=True)
    return str(doc["_id"])

def remove_sid(db, sid):
    _id = _transform_sid(db, sid)
    if _id is not None:
        db[COLL_SESSION].remove({"_id":_id})

def add_validate_code(db, code):
    create_at = datetime.datetime.utcnow()
    spec_doc = {
        "create_at":create_at,
        "code":code,
    }
    return str(db[COLL_VALIDATE_CODE].insert(spec_doc, w=1))

def update_validate_code(db, sid, code):
    _id = _transform_sid(db, sid)
    if _id is not None:
        create_at = datetime.datetime.utcnow()
        doc = db[COLL_VALIDATE_CODE].find_and_modify({"_id":_id}, {"$set":{"code":code,
                                                     "create_at":create_at}}, new=True)
        if doc is None:
            # The session is expired or has removed.
            return add_validate_code(db, code)
        else:
            return sid
    else:
        return add_validate_code(db, code)

def query_code(db, sid):
    _id = _transform_sid(db, sid)
    if _id is None: return None
    return db[COLL_VALIDATE_CODE].find_one({"_id":_id})

def remove_code(db, sid):
    _id = _transform_sid(db, sid)
    if _id is not None:
        db[COLL_VALIDATE_CODE].remove({"_id":_id})