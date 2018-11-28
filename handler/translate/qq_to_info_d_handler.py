# -*- coding: utf-8 -*-
# 此接口为QQ转身份信息接口

import traceback

import pymysql
from tornado import gen
import tornado.web

from auth import jwtauth
from database import db_pool
from handler import BaseHandler
from log import LogBase
logger = LogBase().get_logger("QqToInfoD")
from route import app


@app.route(r'/translate/qqToInfoD')
@jwtauth
class QqToInfoDHandler(BaseHandler):
    """
    QQ转身份信息 handler
    """
    INFO = {"author": "zzccchen", "version": "2.0"}

    SELECT_SQL = """
        SELECT
            `name`,
            `stuNo` AS `stuid`,
            `cardNo` AS `cardno`,
            `QQ` AS `qq`,
            `dept`,
            `major`,
            `grade`
        FROM
            testsmallwei.student_info
        WHERE
            `qq` = %s;"""

    @gen.coroutine
    def get(self, *args, **kwargs):
        qq = self.get_argument_qq()
        if not qq:
            return self.finish()

        with (yield db_pool.Connection()) as conn:
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    yield cursor.execute(self.SELECT_SQL, (qq))
                    get_stu_info = cursor.fetchone()
                    yield conn.commit()

                    if not get_stu_info:
                        return self.write_error_f(4042)

                    return self.write_json_f(get_stu_info)

            except Exception as e:
                logger.error(traceback.format_exc())
                return self.write_error_f(5001)
