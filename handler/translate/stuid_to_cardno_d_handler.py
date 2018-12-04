# -*- coding: utf-8 -*-
# 此接口为学号转一卡通接口

from asyncio import events
import traceback

from auth import auth
from database import SqlSet
from handler import BaseHandler
from log import LogBase
from route import app
logger = LogBase().get_logger("StuidToCardnoD")


@app.route(r'/translate/stuidToCardnoD')
@auth.admin
class StuidToCardnoDHandler(BaseHandler):
    """
    学号转一卡通 handler
    """
    INFO = {"author": "zzccchen", "version": "2.0"}

    SELECT_SQL = """
        SELECT 
            `cardNo` AS `cardno`
        FROM
            testsmallwei.student_info
        WHERE
            `stuNo` = %s;"""

    async def get(self, *args, **kwargs):
        stuid = self.get_argument_stuid()
        if not stuid:
            return self.finish()
        try:
            get_stu_cardno = await SqlSet.get_student_info(
                ["cardno"], "stuno", stuid)
            if not get_stu_cardno:
                return self.write_error_f(4043)
            return self.write_json_f(get_stu_cardno)
        except Exception as e:
            logger.error(traceback.format_exc())
            return self.write_error_f(5001)
