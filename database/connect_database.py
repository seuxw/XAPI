# -*- coding: utf-8 -*-
# 创建数据库连接

import configparser

import tormysql

from log import LogBase
logger = LogBase().get_logger("Database")


class Database(object):
    """数据库类."""
    __instance = None

    def __new__(cls, *args, **kwargs):
        """单例模式实现."""
        if cls.__instance is None:
            cls.__instance = super(
                Database, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        """数据库配置."""
        conf = configparser.ConfigParser()
        conf.read("./database/database.cfg")
        self.host = conf["DATABASE_INFO"]["host"]
        self.port = int(conf["DATABASE_INFO"]["port"])
        self.user = conf["DATABASE_INFO"]["user"]
        self.passwd = conf["DATABASE_INFO"]["passwd"]
        self.db = conf["DATABASE_INFO"]["db"]
        self.charset = conf["DATABASE_INFO"]["charset"]
        self.max_connections = conf["DATABASE_INFO"]["max_connections"]
        self.idle_seconds = conf["DATABASE_INFO"]["idle_seconds"]
        self.wait_connection_timeout = conf["DATABASE_INFO"]["wait_connection_timeout"]

    def connect_database(self):
        """数据库连接方法.

        return:
            pool: 返回连接池
        """
        logger.info("Connect to MySQL server")
        pool = tormysql.ConnectionPool(
            host=self.host, port=int(self.port), user=self.user,
            passwd=self.passwd, db=self.db, charset=self.charset,
            max_connections=int(self.max_connections), idle_seconds=int(self.idle_seconds),
            wait_connection_timeout=int(self.wait_connection_timeout))
        return pool


# 创建数据库连接池
db_pool = Database().connect_database()
