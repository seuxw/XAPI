# -*- coding: utf-8 -*-
# 此接口为QQ转身份信息接口

from asyncio import events
import traceback

from auth import auth
from database import SqlSet
from handler import BaseHandler
from log import LogBase
from route import app
logger = LogBase().get_logger("QqToInfoD")


@app.route(r'/translate/qqToInfoD')
@auth.admin
class QqToInfoDHandler(BaseHandler):
    """
    QQ转身份信息 handler
    """
    INFO = {"author": "zzccchen", "version": "2.0"}

    async def get(self, *args, **kwargs):
        qq = self.get_argument_qq()
        if not qq:
            return self.finish()
        try:
            get_stu_info = await SqlSet.get_student_info(
                ["*"], "qq", qq)
            if not get_stu_info:
                return self.write_error_f(4042)
            return self.write_json_f(get_stu_info)
        except Exception as e:
            logger.error(traceback.format_exc())
            return self.write_error_f(5001)
