# coding=utf8
# 此接口为学生信息查询接口

from asyncio import events
import traceback

from auth import jwtauth
from database import SqlSet
from handler import BaseHandler
from log import LogBase
from route import app
logger = LogBase().get_logger("CourseTable")


@app.route(r'/stu/stuInfo/courseTableAllL')
@jwtauth
class CourseTableAllLHandler(BaseHandler):
    """全部课表查询."""
    INFO = {"author": "zzccchen", "version": "2.0"}

    async def get(self, *args, **kwargs):
        cardno = self.get_argument_cardno()
        if not cardno:
            return self.finish()
        try:
            stuid = await SqlSet.get_student_info(
                ["stuid"], "cardno", cardno)
            if not stuid:
                return self.write_error_f(4041)

            get_course_table = await SqlSet.get_course_table_all(stuid["stuid"])
            if not get_course_table:
                return self.write_error_f(4043)

            data = {"w1": {}, "w2": {}, "w3": {}, "w4": {}, "w5": {}}
            for i in range(15):
                data["w{}".format(i % 5 + 1)]["{}".format(
                    i // 5 + 1)] = get_course_table["course{0}".format(i)]
            return self.write_json_f(data)

        except Exception as e:
            logger.error(traceback.format_exc())
            return self.write_error_f(5001)
