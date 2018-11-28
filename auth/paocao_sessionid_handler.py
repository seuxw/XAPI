# -*- coding: utf-8 -*-
# 此接口为跑操SESSIONID发放接口

import datetime

import jwt
import tornado.web

from handler import BaseHandler
from route import app


@app.route(r'/paocaoSessionid')
class PaocaoSessionidHandler(BaseHandler):
    """token发放模块."""
    INFO = {"author": "zzccchen", "version": "2.0"}
    TIMEOUT = 1200  # 20 分钟

    def get(self, *args, **kwargs):
        """获取sessionid"""
        # TODO: 临时密码
        SECRET_KEY_ = "f6545asdf56A5FS412/98*"
        if self.get_argument("pass") == "pass*" and self.get_argument("word") == "*word":
            token = jwt.encode(
                payload={
                    'iss': "xapi.seuxw.cn",
                    'iat': datetime.datetime.utcnow(),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=self.TIMEOUT)
                },
                key=SECRET_KEY_,
                algorithm='HS256'
            )
            response = {'sessionid': token.decode('ascii')}
            return self.write_json_f(response)
        else:
            return self.write_error_f(4012)
