# -*- coding: utf-8 -*-

from pyrestful.rest import get
from pyrestful import mediatypes
from pyrestful.rest import RestHandler
from log import logger
from modals.Student import StudentModal
import traceback
from database import make_mysql_session
from modals import *
from .StatusCode import error_response


class CardStatusHandler(RestHandler):
    """
    检查一卡通状态 handler
    4041    | Not Found This CardNo In MySQL Server
    "exist":0 一卡通存在
    "exist":-1 一卡通丢失中
    """   
    info = {"author": "zzccchen","version": "1.0"}

    @get(_path="/cardStatus/{cardNo}", _types=[str], _produces=mediatypes.APPLICATION_JSON)
    def CardStatus(self, cardNo):
        try:
            if len(cardNo) != 9:
                return error_response("e4001",self.info)

            mysql_session=make_mysql_session()
            queryans=mysql_session.query(StudentModal).filter(StudentModal.cardNo==cardNo).first()
            if not queryans:
                mysql_session.close()
                return error_response("e4041",self.info)
            response={
                    "code":200,
                    "message":"OK",
                    "data":{
                        "type":"int",
                        "exist":0
                        },
                    "pagination":{
                        "page":1,
                        "pagesize":1,
                        "total":1
                        },
                    "relationships":{
                        "author":self.info["author"]
                        },
                    "jsonapi":{
                        "version":self.info["version"]
                        }
                    }
            mysql_session.close()
            return response
        except Exception as e:
            logger.error(traceback.format_exc())
            # logger.error(e.message)
            return error_response("e5001",self.info)
