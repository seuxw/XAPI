# -*- coding: utf-8 -*-

from pyrestful.rest import get
from pyrestful import mediatypes
from pyrestful.rest import RestHandler
from log import logger
import traceback
from database import make_mysql_session

DEVELOPMENG = True

class CoursetableHandler(RestHandler):
    """
    测试专用handler
    """

    @get(_path="/coursetable", _proeuces=mediatypes.APPLICATION_JSON)
    def query_course_table(self):
        """
        用户查询课表，返回课表上的所有课程。
        :return:
        """
        if DEVELOPMENG:
            self.set_secure_cookie("qq", str(2972822179))
        mysql_session = make_mysql_session()
        try:
            qq = self.get_secure_cookie("qq")
            if qq is None:
                return {"res": 1}
            feedbacks = mysql_session.query(FeedbackModal).filter(FeedbackModal.getPersonQQ == qq).all()
            result = []
            for feedback in feedbacks:
                result.append({
                    "id": feedback.id,
                    "getTime": feedback.getTime,
                    "getContent": feedback.getContent,
                    "getPersonQQ": feedback.getPersonQQ,
                    "state": feedback.subType,
                    "sendPersonQQ": feedback.sendPersonQQ,
                    "sendContent": feedback.sendContent,
                    "sendTime": feedback.sendTime
                })
            return {"res": 0, "feedbacks": result}
        except Exception as e:
            logger.error(traceback.format_exc())
            # logger.error(e.message)
            return {"res": 1}