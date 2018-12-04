# -*- coding: utf-8 -*-
# 此接口为用户签到相关接口

from route import app
import datetime
import requests
import time
import traceback

import json
import pymysql
from tornado import gen
import tornado.web

from auth import auth
from database import db_pool
from handler import BaseHandler
from log import LogBase
logger = LogBase().get_logger("Signin")


@app.route(r'/user/signin/signinD')
@auth.admin
class SigninHandler(BaseHandler):
    """签到模块.

    使用日出日落时间
    """
    INFO = {"author": "zzccchen&Polydick", "version": "2.0"}

    SCORE_BASE = 10  # 签到基础分
    SCORE_SUN_DOWN = 1  # 日落后补签加分
    CTN_SCORE_SCALER = 0.1  # 连续签到加成放大因子

    def _is_continue_signin(self, user):
        """"判段用户最后一次签到的日期是否是昨天."""
        one_day = datetime.timedelta(days=1)
        return True if datetime.date.today() - user["last_date"] == one_day else False

    @gen.coroutine
    def _get_sun_time(self):
        """获取日出日落时间."""

        SELECT_SQL = """
            SELECT 
                `sun_rise_time`,
                `sun_down_time`
            FROM
                testsmallwei.sunrisetime
            WHERE
                `date` = %s;"""

        with (yield db_pool.Connection()) as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                yield cursor.execute(SELECT_SQL, (datetime.date.today()))
                get_sun_time = cursor.fetchone()
                yield conn.commit()

                if get_sun_time:
                    raise gen.Return(
                        (str(get_sun_time["sun_rise_time"]), str(get_sun_time["sun_down_time"])))
                else:  # 如果数据库中没有今天的日出和日落时间
                    res_obj = json.loads(requests.get(
                        "http://aider.meizu.com/app/weather/listWeather?cityIds=101190101"
                    ).text)

                    INSERT_SQL = """
                        INSERT INTO testsmallwei.sunrisetime 
                            (`sun_rise_time`, `sun_down_time`, `date`) 
                        VALUES 
                            (%s, %s, %s);"""

                    param = [(iweather["sun_rise_time"],
                              iweather["sun_down_time"],
                              iweather["date"])
                             for iweather in res_obj["value"][0]["weathers"]]
                    yield cursor.executemany(INSERT_SQL, (param))
                    yield conn.commit()
                    iweather_0 = res_obj["value"][0]["weathers"][0]
                    raise gen.Return(
                        (iweather_0["sun_rise_time"], iweather_0["sun_down_time"]))

    @gen.coroutine
    def _get_signin_type(self):
        """判断当前时间对应的签到得分类型.

        Return:
            1: 当天日初时间到日落时间之内
            2: 当天日落时间到24时之内
            3: 当天0时到日初时间之内
        """
        (low, high) = yield self._get_sun_time()
        current_time = datetime.datetime.now()
        if current_time.hour < int(low[0:1]):
            return 3
        elif current_time.hour == int(low[0:1]) and current_time.minute < int(low[2:4]):
            return 3
        elif current_time.hour > int(high[0:2]):
            return 2
        elif current_time.hour == int(high[0:2]) and current_time.minute > int(high[3:5]):
            return 2
        else:
            return 1

    @gen.coroutine
    def _signin(self, user, qq, signin_type):
        """用户签到逻辑."""
        # 如果该用户本次是连续签到的
        if self._is_continue_signin(user) and signin_type == 1:
            # 基础分*(1+连续签到天数*放大因子)
            added_score = self.SCORE_BASE * \
                (1 + user["ctn_signin"] * self.CTN_SCORE_SCALER)
            user["ctn_signin"] += 1
        else:
            added_score = self.SCORE_SUN_DOWN
            user["ctn_signin"] = 10
        user["total_score"] += added_score  # 签到总积分+=added_score
        user["total_signin"] += 1  # 签到总次数+=1
        user["last_date"] = str(datetime.datetime.now().date())  # 更新该用户最后签到时间
        user["last_time"] = str(datetime.datetime.now().time())

        INSERT_SQL = """
            INSERT INTO testsmallwei.signin_records 
                (`date`, `personQQ`, `addedScore`, `time`) 
            VALUES 
                (%s, %s, %s, %s);"""

        UPDATE_SQL = """
            UPDATE testsmallwei.signin_user 
            SET 
                `totalScore` = %s,
                `totalSignIn` = %s,
                `ctnSignIn` = %s,
                `last_Date` = %s,
                `last_Time` = %s
            WHERE
                `personQQ` = %s;"""

        with (yield db_pool.Connection()) as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                yield cursor.execute(INSERT_SQL, (user["last_date"], qq,
                                                  added_score, user["last_time"]))
                yield conn.commit()
                yield cursor.execute(UPDATE_SQL, (user["total_score"], user["total_signin"],
                                                  user["ctn_signin"], user["last_date"],
                                                  user["last_time"], qq))
                yield conn.commit()
        raise gen.Return(user)

    @gen.coroutine
    def post(self, *args, **kwargs):
        """用户签到."""
        qq = self.get_argument_qq()
        if not qq:
            return self.finish()

        SELECT_SQL = """
            SELECT 
                `nickName` AS `nickname`,
                `totalScore` AS `total_score`,
                `totalSignIn` AS `total_signin`,
                `ctnSignIn` AS `ctn_signin`,
                `last_Date` AS `last_date`,
                `last_Time` AS `last_time`
            FROM
                testsmallwei.signin_user
            WHERE
                `personQQ` = %s;"""

        with (yield db_pool.Connection()) as conn:
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    yield cursor.execute(SELECT_SQL, (qq))
                    get_user = cursor.fetchone()
                    yield conn.commit()

                    if not get_user:
                        return self.write_error_f(4046)

                    if get_user["last_date"] == datetime.date.today():  # 已签到
                        return self.write_error_f(4008)

                    signin_type = yield self._get_signin_type()
                    if signin_type == 3:  # 还未日出
                        return self.write_error_f(4007)

                    get_user = yield self._signin(
                        get_user, qq, signin_type)

                    return self.write_json_f(get_user)

            except Exception as e:
                logger.error(traceback.format_exc())
                return self.write_error_f(5001)


@app.route(r'/user/signin/signinScoreD')
@auth.admin
class SigninScoreDHandler(BaseHandler):
    """
    查询用户签到分数等相关信息。
    """
    INFO = {"author": "zzccchen&Polydick", "version": "2.0"}

    @gen.coroutine
    def get(self, *args, **kwargs):
        qq = self.get_argument_qq()
        if not qq:
            return self.finish()

        SELECT_SQL = """
            SELECT 
                `nickName` AS `nickname`,
                `totalScore` AS `total_score`,
                `totalSignIn` AS `total_signin`,
                `ctnSignIn` AS `ctn_signin`,
                `last_Date` AS `last_date`,
                `last_Time` AS `last_time`
            FROM
                testsmallwei.signin_user
            WHERE
                `personQQ` = %s;"""

        with (yield db_pool.Connection()) as conn:
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    yield cursor.execute(SELECT_SQL, (qq))
                    get_user = cursor.fetchone()
                    yield conn.commit()

                    get_user["last_date"] = str(get_user["last_date"])
                    get_user["last_time"] = str(get_user["last_time"])
                    return self.write_json_f(get_user)

            except Exception as e:
                logger.error(traceback.format_exc())
                return self.write_error_f(5001)

    # @get(_path="/userInfo/signinScoreBoardL", _produces=mediatypes.APPLICATION_JSON)
    # TODO:
    # def signinD_query_score(self):
        """
        查询用户签到分数等相关信息。
        """
