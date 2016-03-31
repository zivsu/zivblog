# !/usr/bin/python
# coding:utf-8

COLL_TAG = "tag"


def add_tags(db, tags):
    spec_doc = {"name":tags}
    db[COLL_TAG].insert(spec_doc, w=1)

def get_tags(db):
    doc = db[COLL_TAG].find_one({"name":{"$exists":True}}, {"name":True})
    return doc["name"]