#!/usr/bin/python
# coding:utf8

ENV_LOCAL = "local"
ENV_PROD = "prod"

CONF = {
    ENV_LOCAL:{
        "db":{
            "db_name":"blog",
            "db_host":"localhost"
        },
    },
    ENV_PROD:{
        "db":{
            "db_name":"blog",
            "db_host":"localhost"
        },
    }
}

ACCOUNT = {
    "email":"test@test.com",
    "password":"test",
    "salt":"1t/77alWSIarPAWV27iROF/AcGgIHU/AjGHjj1nHcAs="
}

# Article status
STATUS_SAVE = "0"
STATUS_PUBLIC = "1"
STATUS_DELETE = "2"

INIT_TAGS = ["python", "java"]

DEFAULT_ROWS = 10

test = 1
