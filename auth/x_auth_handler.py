# -*- coding: utf-8 -*-
# 此接口为token发放接口

import datetime

import jwt
import tornado.web

from .auth import auth
from handler import BaseHandler
from route import app


@app.route(r'/xAuth')
class XAuthHandler(BaseHandler):
    """token发放模块."""
    INFO = {"author": "zzccchen", "version": "2.0"}

    def post(self, *args, **kwargs):
        """获取token"""
        if isinstance(self.get_argument("tk"), str):
            token = jwt.encode(
                payload={
                    'iss': "xapi.seuxw.cn",
                    'aud': self.get_argument("tk"),
                    'iat': datetime.datetime.utcnow(),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=auth.TIMEOUT)
                },
                key=auth.SECRET_KEY,
                algorithm=auth.ALGORITHMS
            )
            response = {'token': token.decode('ascii')}
            print(response)
            return self.write_json_f(response)
        else:
            return self.write_error_f(4012)
