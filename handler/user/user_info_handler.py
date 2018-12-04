# -*- coding: utf-8 -*-
# 此接口为用户信息相关接口

from route import app
import traceback

import pymysql
from tornado import gen
import tornado.web

from auth import auth
from database import db_pool
from handler import BaseHandler
from log import LogBase
logger = LogBase().get_logger("UserInfo")


@app.route(r'/user/userInfo/nicknameD')
@auth.admin
class NicknameDHandler(BaseHandler):
    """查询用户昵称."""
    INFO = {"author": "zzccchen", "version": "2.0"}

    SELECT_SQL = """
        SELECT 
            `nickName` AS `nickname`
        FROM
            testsmallwei.signin_user
        WHERE
            `personQQ` = %s;"""

    @gen.coroutine
    def get(self, *args, **kwargs):
        qq = self.get_argument_qq()
        if not qq:
            return self.finish()

        with (yield db_pool.Connection()) as conn:
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    yield cursor.execute(self.SELECT_SQL, (qq))
                    get_usr_nickname = cursor.fetchone()
                    yield conn.commit()

                    if not get_usr_nickname:
                        return self.write_error_f(4046)

                    return self.write_json_f(get_usr_nickname)

            except Exception as e:
                logger.error(traceback.format_exc())
                return self.write_error_f(5001)


@app.route(r'/user/userInfo/alterNicknameD')
@auth.admin
class AlterNicknameDHandler(BaseHandler):
    """修改用户昵称."""
    INFO = {"author": "zzccchen", "version": "2.0"}

    UPDATE_SQL = """
        UPDATE testsmallwei.signin_user 
        SET 
            `nickName` = %s
        WHERE
            `personQQ` = %s;"""

    @gen.coroutine
    def post(self, *args, **kwargs):
        qq = self.get_argument_qq()
        if not qq:
            return self.finish()

        nickname = self.get_argument("nickname", None)
        if not nickname or len(nickname) > 20:
            return self.write_error_f(40010)

        with (yield db_pool.Connection()) as conn:
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    yield cursor.execute(self.UPDATE_SQL, (nickname, qq))
                    get_status = cursor.fetchone()
                    yield conn.commit()

                    if get_status == 0:
                        return self.write_error_f(4046)

                    return self.write_json_f()

            except Exception as e:
                logger.error(traceback.format_exc())
                return self.write_error_f(5001)


@app.route(r'/user/userInfo/registD')
@auth.admin
class RegistDHandler(BaseHandler):
    """用户注册."""
    INFO = {"author": "zzccchen", "version": "2.0"}

    COUNT_SQL = """
        SELECT 
            COUNT(*)
        FROM
            testsmallwei.signin_user
        WHERE
            `personQQ` = %s;"""

    INSERT_SQL = """
        INSERT INTO testsmallwei.signin_user 
            (`personQQ`, `nickName`) 
        VALUES 
            (%s, %s);"""

    @gen.coroutine
    def post(self, *args, **kwargs):
        qq = self.get_argument_qq()
        if not qq:
            return self.finish()

        nickname = self.get_argument("nickname", None)
        if not nickname or len(nickname) > 20:
            return self.write_error_f(40010)

        with (yield db_pool.Connection()) as conn:
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    yield cursor.execute(self.COUNT_SQL, (qq))
                    get_status = cursor.fetchone()
                    yield conn.commit()

                    if get_status.get("COUNT(*)") != 0:
                        return self.write_error_f(4004)

                    yield cursor.execute(self.INSERT_SQL, (qq, nickname))
                    get_status = cursor.fetchone()
                    yield conn.commit()

                    if get_status == 0:
                        return self.write_error_f(5002)

                    return self.write_json_f()

            except Exception as e:
                logger.error(traceback.format_exc())
                return self.write_error_f(5001)
