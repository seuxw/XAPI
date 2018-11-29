# -*- coding: utf-8 -*-
# 此接口为一卡通号转QQ接口

from asyncio import events
import traceback

from auth import jwtauth
from database import SqlSet
from handler import BaseHandler
from log import LogBase
from route import app
logger = LogBase().get_logger("CardnoToQqD")


@app.route(r'/translate/cardnoToQqD')
@jwtauth
class CardnoToQqDHandler(BaseHandler):
    """一卡通号转QQ handler."""
    INFO = {"author": "zzccchen", "version": "2.0"}

    async def get(self, *args, **kwargs):
        cardno = self.get_argument_cardno()
        if not cardno:
            return self.finish()
        try:
            get_stu_qq = await SqlSet.get_student_info(
                ["qq"], "cardno", cardno)
            if not get_stu_qq:
                return self.write_error_f(4041)
            if get_stu_qq.get("qq") == None:
                return self.write_error_f(4045)
            return self.write_json_f(get_stu_qq)
        except Exception as e:
            logger.error(traceback.format_exc())
            return self.write_error_f(5001)
