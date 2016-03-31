#!/usr/bin/python
# coding:utf8

import base64
import uuid
import hashlib
import datetime
import calendar

FORMAT = "%Y-%m-%d"

def generate_cookie_secret():
    cookie_secret = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
    return cookie_secret

def salt_password(salt, password):
    m = hashlib.md5()
    try:
        m.update(password)
    except:
        raise Exception("invalid password")
    m.update(salt)
    return m.hexdigest()

def get_cur_utc_timestamp():
    return calendar.timegm(datetime.datetime.utcnow().utctimetuple())

def get_today_date():
    return datetime.date.today().strftime(FORMAT)

if __name__ == '__main__':
    cookie_secret = generate_cookie_secret()
    print cookie_secret

