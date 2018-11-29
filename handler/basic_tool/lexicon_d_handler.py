# -*- coding: utf-8 -*-
# 此接口为词库相关接口

from asyncio import events
import traceback

import tornado.web

from auth import jwtauth
from database import db_pool, SqlSet
from handler import BaseHandler
from log import LogBase
from route import app
logger = LogBase().get_logger("LexiconD")


@app.route(r'/basicTool/lexiconD')
@jwtauth
class LexiconDHandler(BaseHandler):
    """词库模块."""
    INFO = {"author": "zzccchen", "version": "2.0"}

    async def get(self, *args, **kwargs):
        """查询词库中对应的回复."""
        key = self.get_argument('key', None)
        try:
            reply = await SqlSet.get_dictionary(key)
            # 不开放secret标识为非0的key查询
            if not reply or reply.get("secret", 1) != 0:
                return self.write_error_f(4047)
            else:
                del reply["secret"]
                return self.write_json_f(reply)
        except Exception as e:
            logger.error(traceback.format_exc())
            return self.write_error_f(5001)
