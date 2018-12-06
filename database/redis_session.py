# -*- coding: utf-8 -*-
# redis模块

import configparser
import redis

from database.connect_database import Database
from log import LogBase
logger = LogBase().get_logger("RedisSession")


class RedisSession(object):
    """Redis 相关类."""
    __instance = None

    def __new__(cls, *args, **kwargs):
        """单例模式实现."""
        if cls.__instance is None:
            cls.__instance = super(
                RedisSession, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("./database/redis.cfg")
        self.host = conf["REDIS_INFO"]["host"]
        self.port = conf["REDIS_INFO"]["port"]
        self.db = conf["REDIS_INFO"]["db"]
        self.jsid = "jsid"

    def connect_redis(self):
        """连接到 Redis 数据库.

        Return:
            返回一个连接
        """
        pool = redis.ConnectionPool(
            host=self.host, port=self.port, db=self.db)
        conn = redis.StrictRedis(connection_pool=pool)
        logger.info("Connect to Redis server")
        return conn


# 创建 Redis 连接
redis_session = RedisSession().connect_redis()
