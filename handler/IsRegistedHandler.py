# -*- coding: utf-8 -*-

from pyrestful.rest import get
from pyrestful import mediatypes
from pyrestful.rest import RestHandler
from log import logger
from modals.QQToken import QQToken
import traceback
from database import make_mysql_session
from modals import *


class IsRegistedHandler(RestHandler):
    """
    判断用户是否已注册 handler
    """

    @get(_path="/IsRegisted/{qq}", _types=[str], _produces=mediatypes.APPLICATION_JSON)
    def IsRegisted(self, qq):
        try:
            mysql_session=make_mysql_session()
            queryans=mysql_session.query(QQToken).filter(QQToken.qq==qq).first()
            if not queryans:
                response={
                        "code":200,
                        "mesage":"OK",
                        "data":{
                            "type":bool,
                            "ans":False
                            },
                        "relationships":{
                            "author":"MLT"
                            },
                        "jsonapi":{
                            "version":"1.0"
                            }
                        }
                mysql_session.close()
                return response
            response={
                    "code":200,
                    "message":"OK",
                    "data":{
                        "type":"bool",
                        "ans":True
                        },
                    "pagination":{
                        "page":0,
                        "pagesize":0,
                        "total":0
                        },
                    "relationships":{
                        "author":"MLT"
                        },
                    "jsonapi":{
                        "version":"1.0"
                        }
                    }
            mysql_session.close()
            return response
        except Exception as e:
            logger.error(traceback.format_exc())
            # logger.error(e.message)
            response = {
                "code": 500,
                "message": "Internal Server Error",
                "errors": {
                    "code": 5001,
                    "message": "MySQL Server Error"
                },
                "relationships": {
                    "author": "MLT"
                },
                "jsonapi": {
                    "version": "1.0"
                }
            }
            return response
