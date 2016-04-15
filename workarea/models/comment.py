# coding:utf-8

import logging

from bson.objectid import ObjectId

from models import article
import utils

COLL_COMMENTS = "comments"
FORMAT = utils.FORMAT

def add_one_comment(db, slug, comment):
    article_id = article.get_article_id(db, slug)
    if article_id is None:
        return None
    timestamp = utils.get_cur_utc_timestamp()
    hk_datetime = utils.utc_timestamp_to_hk_datetime(timestamp).strftime(FORMAT)
    comment.update({"timestamp":timestamp, "article_id":article_id,
                    "datetime":hk_datetime})
    # Insert `comment` copy because need return comment,
    # if not, `comment` will add {_id:ObjectId(...)}
    db[COLL_COMMENTS].insert(comment.copy(), w=1)
    return comment

def get_comments(db, article_id):
    article_id = str(article_id)
    cursor = db[COLL_COMMENTS].find({"article_id":article_id}, {"content":True,
                        "username":True, "headimgurl":True, "datetime":True})
    comments = []
    for doc in cursor:
        prepared = {
            "username":doc["username"],
            "headimgurl":doc["headimgurl"],
            "content":doc["content"],
            "datetime":doc["datetime"]
        }
        comments.append(prepared)
    return comments


