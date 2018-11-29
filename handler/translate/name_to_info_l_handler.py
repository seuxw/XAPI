# -*- coding: utf-8 -*-
# 此接口为名字转身份信息接口

import traceback

import pymysql
from tornado import gen
import tornado.web

from auth import jwtauth
from database import db_pool
from handler import BaseHandler
from log import LogBase
from route import app
logger = LogBase().get_logger("NameToInfoL")


@app.route(r'/translate/nameToInfoL')
@jwtauth
class NameToInfoLHandler(BaseHandler):
    """
    名字转身份信息 handler
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
            `name` LIKE %s
        LIMIT %s , %s;"""

    COUNT_SQL = """
        SELECT 
            COUNT(*) AS `count`
        FROM
            testsmallwei.student_info
        WHERE
            `name` LIKE %s;"""

    @gen.coroutine
    def get(self, *args, **kwargs):
        name = self.get_argument('name', None)
        page = self.get_argument_page()
        pagesize = self.get_argument_pagesize()

        if not page or not pagesize:
            return self.finish()
        if not name:
            return self.write_error_f(40010)

        with (yield db_pool.Connection()) as conn:
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    name = "%{}%".format(name)
                    yield cursor.execute(self.SELECT_SQL, (name, (page-1)*pagesize, pagesize))
                    info_list = cursor.fetchall()
                    yield conn.commit()

                    yield cursor.execute(self.COUNT_SQL, (name))
                    count = cursor.fetchone()
                    yield conn.commit()

                    if not info_list and not count:
                        return self.write_error_f(4044)

                    self.pagination = {
                        "page": page,
                        "pagesize": pagesize,
                        "total": count.get("count")
                    }
                    return self.write_json_f(info_list)

            except Exception as e:
                logger.error(traceback.format_exc())
                return self.write_error_f(5001)
