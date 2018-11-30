# -*- coding: utf-8 -*-
# 此接口为QQ转一卡通接口

from asyncio import events
import traceback

from auth import jwtauth
from database import SqlSet
from handler import BaseHandler
from log import LogBase
from route import app
logger = LogBase().get_logger("QqToCardnoD")


@app.route(r'/translate/qqToCardnoD')
@jwtauth
class QqToCardnoDHandler(BaseHandler):
    """ QQ转一卡通 handler."""
    INFO = {"author": "zzccchen", "version": "2.0"}

    async def get(self, *args, **kwargs):
        qq = self.get_argument_qq()
        if not qq:
            return self.finish()
        try:
            get_stu_cardno = await SqlSet.get_student_info(
                ["cardno"], "qq", qq)
            if not get_stu_cardno:
                return self.write_error_f(4042)
            return self.write_json_f(get_stu_cardno)
        except Exception as e:
            logger.error(traceback.format_exc())
            return self.write_error_f(5001)
