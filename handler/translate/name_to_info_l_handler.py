# -*- coding: utf-8 -*-
# 此接口为名字转身份信息接口

from asyncio import events
import traceback

from auth import jwtauth
from database import SqlSet
from handler import BaseHandler
from log import LogBase
from route import app
logger = LogBase().get_logger("NameToInfoL")


@app.route(r'/translate/nameToInfoL')
@jwtauth
class NameToInfoLHandler(BaseHandler):
    """名字转身份信息 handler."""
    INFO = {"author": "zzccchen", "version": "2.0"}

    async def get(self, *args, **kwargs):
        name = self.get_argument('name', None)
        page = self.get_argument_page()
        pagesize = self.get_argument_pagesize()

        if not page or not pagesize:
            return self.finish()
        if not name:
            return self.write_error_f(40010)

        try:
            name = "%{}%".format(name)
            info_list, count = await SqlSet.get_student_info_like(
                ["*"], "name", name, page, pagesize)
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
