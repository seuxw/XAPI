# -*- coding: utf-8 -*-
# 此接口为token发放接口

import datetime
import json

import jwt
import requests

from .auth import auth
from handler import BaseHandler
from route import app


@app.route(r'/xAuth')
class XAuthHandler(BaseHandler):
    """token发放模块."""
    INFO = {"author": "zzccchen", "version": "2.0"}
    GET_OPEN_ID_URL = "https://graph.qq.com/oauth2.0/me"

    def post(self, *args, **kwargs):
        """获取token"""
        cardno = self.get_argument_cardno()
        tk = self.get_argument("tk")

        if isinstance(tk, str) and cardno:
            access_token = tk[3:]
            res = requests.get(self.GET_OPEN_ID_URL, params={
                "access_token": access_token}, timeout=60)
            res_json = json.loads(res.text[10:-3])

            if res_json.get("client_id") != auth.CLIENT_ID:
                return self.write_error_f(4014)

            openid = res_json.get("openid")
            if not openid:
                return self.write_error_f(4015)

            print(openid)
            token = jwt.encode(
                payload={
                    'iss': "xapi.seuxw.cn",
                    'cnb': "str(openid)",
                    'iat': datetime.datetime.utcnow(),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=auth.TIMEOUT)
                },
                key=auth.SECRET_KEY,
                algorithm=auth.ALGORITHMS
            )
            response = {'token': token.decode('ascii')}
            return self.write_json_f(response)
        else:
            return self.write_error_f(4012)
