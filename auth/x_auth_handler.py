# -*- coding: utf-8 -*-
# 此接口为token发放接口

from asyncio import events
import datetime
import json
import traceback

import jwt
import requests

from .auth import auth
from database import SqlSet
from handler import BaseHandler
from log import LogBase
from route import app
logger = LogBase().get_logger("XAuth")


@app.route(r'/xAuth')
class XAuthHandler(BaseHandler):
    """token发放模块."""
    INFO = {"author": "zzccchen", "version": "2.0"}
    GET_OPEN_ID_URL = "https://graph.qq.com/oauth2.0/me"

    def get_openid(self, tk):
        access_token = str(tk)[3:]
        res = requests.get(self.GET_OPEN_ID_URL, params={
            "access_token": access_token}, timeout=60)
        res_json = json.loads(res.text[10:-3])

        if res_json.get("client_id") != auth.CLIENT_ID:
            self.write_error_f(4014)
            return None

        openid = res_json.get("openid")
        if not openid:
            self.write_error_f(4015)
            return None
        return openid

    def token_prepare(self, cardno):
        token = jwt.encode(
            payload={
                'iss': "xapi.seuxw.cn",
                'cnb': cardno,
                'iat': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=auth.TIMEOUT)
            },
            key=auth.SECRET_KEY,
            algorithm=auth.ALGORITHMS
        )
        response = {'token': token.decode('ascii')}
        return self.write_json_f(response)

    async def cardno_match(self):
        tk = self.get_argument("tk")
        if not tk:
            return self.write_error_f(4012), None
        openid = self.get_openid(tk)
        if not openid:
            return None, None
        return await SqlSet.get_student_info(["cardno"], "openid", openid), openid

    async def get(self, *args, **kwargs):
        """重新获取token"""
        try:
            cardno, openid = await self.cardno_match()
            if not openid:
                return
            if not cardno:
                return self.write_error_f(4048)
            self.token_prepare(cardno["cardno"])
        except Exception as e:
            logger.error(traceback.format_exc())
            return self.write_error_f(5001)

    async def post(self, *args, **kwargs):
        """获取token"""
        try:
            cardno, openid = await self.cardno_match()
            if not openid:  # 用以接受调用函数内的 return None
                return
            if cardno:
                return self.write_error_f(4004)

            cardno = self.get_argument_cardno()
            if not cardno:
                return self.finish()
            await SqlSet.update_student_openid(cardno, openid)
            self.token_prepare(cardno)
        except Exception as e:
            logger.error(traceback.format_exc())
            return self.write_error_f(5001)
