# -*- coding: utf-8 -*-
# 此接口为token发放接口

import datetime

import jwt
import tornado.web

from .auth import SECRET_KEY
from handler import BaseHandler
from route import app


@app.route(r'/xAuth')
class XAuthHandler(BaseHandler):
    """token发放模块."""
    INFO = {"author": "zzccchen", "version": "2.0"}
    TIMEOUT = 15552000  # 180 天

    def post(self, *args, **kwargs):
        """获取token"""
        if self.get_argument("pass") == "pass*" and self.get_argument("word") == "*word":
            token = jwt.encode(
                payload={
                    'iss': "xapi.seuxw.cn",
                    'iat': datetime.datetime.utcnow(),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=self.TIMEOUT)
                },
                key=SECRET_KEY,
                algorithm='HS256'
            )
            response = {'token': token.decode('ascii')}
            return self.write_json_f(response)
        else:
            return self.write_error_f(4012)
