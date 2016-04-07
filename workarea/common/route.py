# coding=utf-8

from tornado.web import URLSpec

class Route(object):

    __routes = []

    def __init__(self, uri, name=None):
        self.__uri = uri
        self.__name = name

    def __call__(self, handler):
        name = self.__name or handler.__name__
        self.__routes.append(URLSpec(self.__uri, handler, name=name))

    @classmethod
    def get_routes(self):
        return self.__routes

route = Route