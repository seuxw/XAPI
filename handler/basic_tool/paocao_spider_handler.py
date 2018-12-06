# -*- coding: utf-8 -*-
# 此接口为跑操爬虫相关接口

from asyncio import events
import traceback

from auth import auth
from database import SqlSet, redis_session
from handler import BaseHandler
from log import LogBase
from route import app
logger = LogBase().get_logger("PaocaoSpider")


@app.route(r'/basicTool/paocaoSpider')
@auth.common
class PaocaoSpiderHandler(BaseHandler):
    INFO = {"author": "zzccchen", "version": "2.0"}

    def get(self, *args, **kwargs):
        try:
            jsid = redis_session.get(redis_session.jsid)
            return self.write_json_f({"jsid": jsid})
        except Exception as e:
            logger.error(traceback.format_exc())
            return self.write_error_f(5001)
