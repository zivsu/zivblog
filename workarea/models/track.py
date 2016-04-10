# coding=utf-8

COLL_PAGEVIEW = "pageview"

def save_pageview(db, view_info):
    db[COLL_PAGEVIEW].insert(view_info, w=1)


def get_visitor_num(db):
    pipline = [
        {"$project":{"ip":1}},
        {"$group":{"_id":"$ip"}},
        {"$group":{"_id":None, "amount":{"$sum":1}}}
    ]
    cursor = db[COLL_PAGEVIEW].aggregate(pipline)
    visitor_num = 0
    for doc in cursor: visitor_num += doc["amount"]
    return visitor_num
