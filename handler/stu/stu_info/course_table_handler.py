# coding=utf8
# 此接口为学生信息查询接口

import traceback

import pymysql
from tornado import gen
import tornado.web

from auth import jwtauth
from database import db_pool
from handler import BaseHandler
from log import LogBase
logger = LogBase().get_logger("CourseTable")
from route import app


@gen.coroutine
def cardno_to_stuid(cardno):
    """一卡通转学号."""

    SELECT_SQL = """
        SELECT 
            `stuNo` AS `stuid`
        FROM
            testsmallwei.student_info
        WHERE
            `cardNo` = %s;"""

    with (yield db_pool.Connection()) as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            yield cursor.execute(SELECT_SQL, (cardno))
            stuid = cursor.fetchone().get("stuid")
            yield conn.commit()
            raise gen.Return(stuid)


@app.route(r'/stu/stuInfo/courseTableAllL')
@jwtauth
class CourseTableAllLHandler(BaseHandler):
    """全部课表查询."""
    INFO = {"author": "zzccchen", "version": "2.0"}

    SELECT_SQL = """
        SELECT 
            *
        FROM
            testsmallwei.coursetable
        WHERE
            `stuNo` = %s;"""

    @gen.coroutine
    def get(self, *args, **kwargs):
        cardno = self.get_argument_cardno()
        if not cardno:
            return self.finish()

        stuid = yield cardno_to_stuid(cardno)
        if not stuid:
            return self.write_error_f(4041)

        with (yield db_pool.Connection()) as conn:
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    yield cursor.execute(self.SELECT_SQL, (stuid))
                    get_course_table = cursor.fetchone()
                    yield conn.commit()

                    if not get_course_table:
                        return self.write_error_f(4043)

                    data = {"w1": {}, "w2": {}, "w3": {}, "w4": {}, "w5": {}}
                    for i in range(15):
                        data["w{}".format(
                            i % 5 + 1)]["{}".format(i // 5 + 1)] = get_course_table["course{0}".format(i)]
                    return self.write_json_f(data)

            except Exception as e:
                logger.error(traceback.format_exc())
                return self.write_error_f(5001)
