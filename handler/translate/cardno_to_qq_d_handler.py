# -*- coding: utf-8 -*-
# 此接口为一卡通号转QQ接口

import traceback

import pymysql
from tornado import gen
import tornado.web

from auth import jwtauth
from database import db_pool
from handler import BaseHandler
from log import LogBase
logger = LogBase().get_logger("CardnoToQqD")
from route import app


@app.route(r'/translate/cardnoToQqD')
@jwtauth
class CardnoToQqDHandler(BaseHandler):
    """
    一卡通号转QQ handler
    """
    INFO = {"author": "zzccchen", "version": "2.0"}

    SELECT_SQL = """
        SELECT 
            `QQ` AS `qq`
        FROM
            testsmallwei.student_info
        WHERE
            `cardNo` = %s;"""

    @gen.coroutine
    def get(self, *args, **kwargs):
        cardno = self.get_argument_cardno()
        if not cardno:
            return self.finish()

        with (yield db_pool.Connection()) as conn:
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    yield cursor.execute(self.SELECT_SQL, (cardno))
                    get_stu_qq = cursor.fetchone()
                    yield conn.commit()

                    if not get_stu_qq:
                        return self.write_error_f(4041)

                    if get_stu_qq.get("qq") == None:
                        return self.write_error_f(4045)

                    return self.write_json_f(get_stu_qq)

            except Exception as e:
                logger.error(traceback.format_exc())
                return self.write_error_f(5001)
