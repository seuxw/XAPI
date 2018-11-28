# -*- coding: utf-8 -*-
# 此接口为QQ转一卡通接口

import traceback

import pymysql
from tornado import gen
import tornado.web

from auth import jwtauth
from database import db_pool
from handler import BaseHandler
from log import LogBase
logger = LogBase().get_logger("QqToCardnoD")
from route import app


@app.route(r'/translate/qqToCardnoD')
@jwtauth
class QqToCardnoDHandler(BaseHandler):
    """
    QQ转一卡通 handler
    """
    INFO = {"author": "zzccchen", "version": "2.0"}

    SELECT_SQL = """
        SELECT 
            `cardNo` AS `cardno`
        FROM
            testsmallwei.student_info
        WHERE
            `QQ` = %s;"""

    @gen.coroutine
    def get(self, *args, **kwargs):
        qq = self.get_argument_qq()
        if not qq:
            return self.finish()

        with (yield db_pool.Connection()) as conn:
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    yield cursor.execute(self.SELECT_SQL, (qq))
                    get_stu_cardno = cursor.fetchone()
                    yield conn.commit()

                    if not get_stu_cardno:
                        return self.write_error_f(4042)

                    return self.write_json_f(get_stu_cardno)

            except Exception as e:
                logger.error(traceback.format_exc())
                return self.write_error_f(5001)
