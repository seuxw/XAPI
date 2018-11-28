# -*- coding: utf-8 -*-

import time
import traceback
from log import logger

from pyrestful.rest import get, post, delete
from pyrestful import mediatypes
from pyrestful.rest import RestHandler

from database import make_mysql_session
from modals.Feedback import FeedbackModal

DEVELOPMENG = True


class FeedbackHandler(RestHandler):
    """
    反馈处理
    get:查询反馈处理情况
    post:发送反馈
    delete:撤销反馈？
    """

    @get(_path="/api/feedback", _produces=mediatypes.APPLICATION_JSON)
    def query_feedback(self):
        """

        :return:
        """
        if DEVELOPMENG:
            self.set_secure_cookie("qq", str(2972822179))

        mysql_session = make_mysql_session()
        qq = self.get_secure_cookie("qq")
        if qq is None:
            return {"res": 1}
        logger.info(str(qq) + " query feedback")
        try:
            feedbacks = mysql_session.query(FeedbackModal).filter(FeedbackModal.getPersonQQ == qq).all()
        except Exception as e:
            # logger.error(e.message)
            logger.error(traceback.format_exc())
            mysql_session.rollback()
            return {"res": 1}
        else:
            result = []
            for feedback in feedbacks:
                result.append(feedback)
            return {"res": 0, "data": result}
        finally:
            mysql_session.close()

    # @get(_path="/api/feedback/{feedback_id}", _types=[int], _produces=mediatypes.APPLICATION_JSON)
    # def query_feedback(self, feedback_id):
    #     """
    #     查询反馈当前处理状态并返回给用户
    #     :param feedback_id:反馈id
    #     :return:
    #     """
    #     print "query_feedback"
    #     mysql_session = make_mysql_session()
    #     try:
    #         qq = self.get_secure_cookie("qq")
    #         if qq is None:
    #             return {"res": 1}
    #         feedback = mysql_session.query(FeedbackModal).filter(FeedbackModal.id == feedback_id).first()
    #         if feedback is None:
    #             return {"res": 1}
    #         return {"res": 0,
    #                 "feedback": {
    #                     "id": feedback.id,
    #                     "getTime": feedback.getTime,
    #                     "getContent": feedback.getContent,
    #                     "getPersonQQ": feedback.getPersonQQ,
    #                     "state": feedback.subType,
    #                     "sendPersonQQ": feedback.sendPersonQQ,
    #                     "sendContent": feedback.sendContent,
    #                     "sendTime": feedback.sendTime
    #                 }}
    #     except Exception as e:
    #         logger.error(traceback.format_exc())
    #         logger.error(e.message)
    #         return {"res": 1}

    class ReceivedFeedback:
        get_content = str

    @post(_path="/api/feedback", _types=[ReceivedFeedback], _consumes=mediatypes.APPLICATION_JSON,
          _produces=mediatypes.APPLICATION_JSON)
    def receive_feedback(self, received_feedback):
        """
        收到用户发送的反馈
        :var cookies和session中的qq，auth_session_id
        :param get_content:反馈内容
        :return:
        """
        get_content = received_feedback.get_content
        if DEVELOPMENG:
            self.set_secure_cookie("qq", str(2972822179))
        mysql_session = make_mysql_session()
        qq = self.get_secure_cookie("qq")
        if qq is None:
            return {"res": 1}
        logger.info(str(qq) + " send feedback")
        try:
            new_feedback = FeedbackModal(getContent=get_content,
                                         getPersonQQ=qq,
                                         getTime=int(time.time()),
                                         subType=0)
            mysql_session.add(new_feedback)
            mysql_session.commit()
            feedback = mysql_session.query(FeedbackModal).filter(
                FeedbackModal.getContent == get_content).first()
        except Exception as e:
            #logger.error(e.message)
            logger.error(traceback.format_exc())
            mysql_session.rollback()
            return {"res": 1}
        else:
            return {"res": 0, "data": feedback.make_response()}
        finally:
            mysql_session.close()

    @delete(_path="/api/feedback/{feedback_id}", _types=[int], _produces=mediatypes.APPLICATION_JSON)
    def undo_feedback(self, feedback_id):
        """
        用户提出撤销反馈
        :var cookies和session中的qq，auth_session_id
        :param feedback_id:反馈id
        :return:
        """
        if DEVELOPMENG:
            self.set_secure_cookie("qq", str(2972822179))
        mysql_session = make_mysql_session()
        qq = self.get_secure_cookie("qq")
        if qq is None:
            return {"res": 1}
        logger.info(str(qq) + " undo feedback")
        try:
            feedback = mysql_session.query(FeedbackModal).filter(
                FeedbackModal.id == feedback_id).first()
            mysql_session.delete(feedback)
            mysql_session.commit()
        except Exception as e:
            # logger.error(e.message)
            logger.error(traceback.format_exc())
            mysql_session.rollback()
            return {"res": 1}
        else:
            return {"res": 0}
        finally:
            mysql_session.close()
