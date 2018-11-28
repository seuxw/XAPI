# -*- coding: utf-8 -*-

from log import logger
import traceback

from pyrestful.rest import get, post, delete
from pyrestful import mediatypes
from pyrestful.rest import RestHandler

from database import make_mysql_session
from modals.QQToken import QQToken
from auth import *


class RedirectHandler(RestHandler):

    @get(_path="/api/entry/{token}", _type=[str], _produces=mediatypes.APPLICATION_JSON)
    def entry(self, token):
        """

        :param token:
        :return:
        """
        print ("redirect")
        mysql_session = make_mysql_session()
        try:
            qq_token = mysql_session.query(QQToken).filter(QQToken.token == token).first()
            if qq_token is None:
                return
            elif qq_token.cardnum != 0:
                self.set_secure_cookie("cardnum", qq_token.cardnum, 7)
            self.set_secure_cookie("token", token, 7)
            self.set_secure_cookie("qq", str(qq_token.qq), 7)
            self.redirect("http://localhost:8100")
        except Exception as e:
            # logger.error(e.message)
            logger.error(traceback.format_exc())
            return
