# -*- coding: utf-8 -*-
# 此接口为词库相关接口

import traceback

import pymysql
from tornado import gen
import tornado.web

from auth import jwtauth
from database import db_pool
from handler import BaseHandler
from log import LogBase
logger = LogBase().get_logger("LexiconD")
from route import app


@app.route(r'/basicTool/lexiconD')
@jwtauth
class LexiconDHandler(BaseHandler):
    """词库模块."""
    INFO = {"author": "zzccchen", "version": "2.0"}

    SELECT_SQL = """
        SELECT
            `value`, `secret`, `remark`, `create_datetime`
        FROM
            testsmallwei.dictionary
        WHERE
            `key` = %s;"""

    @gen.coroutine
    def get(self, *args, **kwargs):
        """查询词库中对应的回复."""
        key = self.get_argument('key', None)

        with (yield db_pool.Connection()) as conn:
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:

                    yield cursor.execute(self.SELECT_SQL, (key))
                    reply = cursor.fetchone()
                    yield conn.commit()

                    # 不开放secret标识为非0的key查询
                    if not reply or reply.get("secret", 1) != 0:
                        return self.write_error_f(4047)
                    else:
                        del reply["secret"]
                        return self.write_json_f(reply)

            except Exception as e:
                logger.error(traceback.format_exc())
                return self.write_error_f(5001)
