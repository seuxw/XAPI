# -*- coding: utf-8 -*-

from pyrestful.rest import get
from pyrestful import mediatypes
from pyrestful.rest import RestHandler
import datetime
from modals import ForecastWeather, RealtimeWeather, LifeSuggestion
from database import make_mysql_session, desc
from util import wrap_server_internal_error
import json
from log import logger
import time
import traceback

import threading
import requests

DEVELOPMENG = True


class WeatherServerThread(threading.Thread):
    ROOT_URL = "https://api.seniverse.com/v3"
    REALTIME_URL = "/weather/now.json"
    FORECAST_URL = "/weather/daily.json"
    SUGGESTION_URL = "/life/suggestion.json"

    payload = {
        "key": "cxsnhsknwszikccf",
        "location": "nanjing",
        "language": "zh-Hans",
        "unit": "c"
    }

    def __init__(self, time_interval):
        super(WeatherServerThread, self).__init__()
        self.time_interval = time_interval
        self.session = requests.session()

    def run(self):
        logger.info("Weather server thread start.")
        while True:
            time.sleep(self.time_interval)
            self.callback()

    def callback(self):
        try:
            logger.info("Weather server callback invoked.")
            realtime, forecasts, suggestion = self.fetch()
            self.store(realtime, forecasts, suggestion)
        except Exception as e:
            logger.error(traceback.format_exc())
            # logger.error(e.message)

    def store(self, realtime, forecasts, suggestion):
        session = make_mysql_session()
        if not session.query(RealtimeWeather).filter(RealtimeWeather.last_update == realtime.last_update).all():
            session.add(realtime)
            logger.info("GET {0}".format(realtime.make_response()))
        if not session.query(ForecastWeather).filter(ForecastWeather.last_update == forecasts[0].last_update).all():
            for f in forecasts:
                session.add(f)
                logger.info("GET {0}".format(f.make_response()))
        if not session.query(LifeSuggestion).filter(LifeSuggestion.last_update == suggestion.last_update).all():
            session.add(suggestion)
            logger.info("GET {0}".format(suggestion.make_response()))
        session.commit()

    def fetch(self):
        realtime, forecasts, suggestion = None, None, None
        resp = requests.get(self.ROOT_URL + self.REALTIME_URL, params=self.payload)
        if resp.status_code == 200:
            realtime = RealtimeWeather.make(json.loads(resp.text))
        resp = requests.get(self.ROOT_URL + self.FORECAST_URL, params=self.payload)
        if resp.status_code == 200:
            forecasts = ForecastWeather.make(json.loads(resp.text))
        resp = requests.get(self.ROOT_URL + self.SUGGESTION_URL, params=self.payload)
        if resp.status_code == 200:
            suggestion = LifeSuggestion.make(json.loads(resp.text))
        return realtime, forecasts, suggestion


class WeatherHandler(RestHandler):
    """
    天气查询handler
    """

    @staticmethod
    def get_day_range():
        today = datetime.datetime.today()
        return today - datetime.timedelta(days=1), today + datetime.timedelta(days=2)

    @get(_path="/api/weather/realtime", _produces=mediatypes.APPLICATION_JSON)
    def query_realtime_weather(self):
        """
        查询实时天气
        :return:
        """
        print ("realtime")
        mysql_session = make_mysql_session()
        try:
            weather = mysql_session.query(RealtimeWeather).order_by(desc(RealtimeWeather.last_update)).first()
        except Exception as e:
            # logger.error(e.message)
            logger.error(traceback.format_exc())
            mysql_session.rollback()
            return {"res": 1}
        else:
            return {"res": 0, "data": weather.make_response()}
        finally:
            mysql_session.close()

    @get(_path="/api/weather/forecast", _produces=mediatypes.APPLICATION_JSON)
    def query_weather_forecast(self):
        """
        查询天气预报
        :return:
        """
        print ("forecast")
        mysql_session = make_mysql_session()
        start_day, end_day = WeatherHandler.get_day_range()
        try:
            forecasts = mysql_session \
                .query(ForecastWeather) \
                .order_by(desc(ForecastWeather.last_update)) \
                .filter(ForecastWeather.date_.between(start_day, end_day)) \
                .limit(3).all()
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            mysql_session.rollback()
            return {"res": 1}
        else:
            resp = []
            for forecast in forecasts:
                resp.append(forecast.make_response())
            return {"res": 0, "data": resp}
        finally:
            mysql_session.close()

    @get(_path="/api/weather/suggestion", _produces=mediatypes.APPLICATION_JSON)
    def query_suggestion(self):
        """
        查询生活指数
        :return:
        """
        print ("suggestion")
        mysql_session = make_mysql_session()
        try:
            suggestion = mysql_session \
                .query(LifeSuggestion) \
                .order_by(desc(LifeSuggestion.last_update)) \
                .first()
        except Exception as e:
            # logger.error(e.message)
            logger.error(traceback.format_exc())
            mysql_session.rollback()
            return {"res": 1}
        else:
            return {"res": 0, "data": suggestion.make_response()}
        finally:
            mysql_session.close()
