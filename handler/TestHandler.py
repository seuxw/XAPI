# -*- coding: utf-8 -*-

from pyrestful.rest import get
from pyrestful import mediatypes
from pyrestful.rest import RestHandler


class TestHandler(RestHandler):
    """
    测试专用handler
    """

    @get(_path="/test/{name}", _types=[str], _produces=mediatypes.APPLICATION_JSON)
    def test(self, name):
        response = {
            "code": 200,
            "message": "OK",
            "data": {
                "type": "string",
                "hello": "name"
            },
            "pagination": {
                "page": 0,
                "pagesize": 0,
                "total": 0
            },
            "relationships": {
                "author": "Polydick"
            },
            "jsonapi": {
                "version": "1.0"
            }
        }
        return response
