# -*- coding: utf-8 -*-
# 数据库指令集

from asyncio import events

import pymysql
from tornado import gen

from database import db_pool


class SqlSet():

    DB = "testsmallwei"
    # 使用 %s 是为了使用 pymysql 自带的 execute 防注入
    GET_ALL = "SELECT {0} FROM {1}.{2} WHERE {3} = %s;"
    GET_ONE = "SELECT {0} FROM {1}.{2} WHERE {3} = %s LIMIT 1;"
    GET_LIKE = "SELECT {0} FROM {1}.{2} WHERE {3} LIKE %s LIMIT %s, %s;"

    @staticmethod
    async def get(sql_dict, fetch="one"):
        """查询数据库."""
        async with await db_pool.Connection() as conn:
            async with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                if fetch == "one":
                    sql = SqlSet.GET_ONE.format(
                        sql_dict["names"], SqlSet.DB, sql_dict["table"],
                        sql_dict["key"])
                    await cursor.execute(sql, (sql_dict["value"]))
                    return cursor.fetchone()
                elif fetch == "all":
                    sql = SqlSet.GET_ALL.format(
                        sql_dict["names"], SqlSet.DB, sql_dict["table"],
                        sql_dict["key"])
                elif fetch == "like":
                    sql = SqlSet.GET_LIKE.format(
                        sql_dict["names"], SqlSet.DB, sql_dict["table"],
                        sql_dict["key"])
                await cursor.execute(sql, (sql_dict["value"]))
                return cursor.fetchall()

    @staticmethod
    def names_join(names_dict, names):
        if names == ["*"]:
            return ", ".join([value for value in names_dict.values()])
        else:
            return ", ".join([names_dict.get(key) for key in names])

    @staticmethod
    async def get_dictionary(value):
        """查询词库中对应的回复.

        Args: 
            value: 对应 `key`
        Returns: 
            `key`, `value`, `secret`
        """
        sql_dict = {
            "names": "`key`, `value`, `secret`",
            "table": "dictionary",
            "key": "`key`",
            "value": value
        }
        return await SqlSet.get(sql_dict)

    STUDENT_INFO_NAME_DICT = {
        "name": "`name`",
        "stuid": "`stuNo` AS `stuid`",
        "cardno": "`cardNo` AS `cardno`",
        "qq": "`QQ` AS `qq`",
        "dept": "dept",
        "major": "major",
        "grade": "grade"
    }

    @staticmethod
    async def get_student_info(names, key, value):
        """查询学生信息表.

        Args:
            names: 需要返回的列名(list)，当传入 ["*"] 时为全选
            key: 查询基于的键名（基于模块变量名，与表无关）
            value: 查询基于的键值
        Returns:
            由传入参数 names 决定，最多包括：
            `name`, `stuid`, `cardno`, `qq`, `dept`, `major`, `grade`
        """
        sql_dict = {
            "names": SqlSet.names_join(SqlSet.STUDENT_INFO_NAME_DICT, names),
            "table": "student_info",
            "key": "`{}`".format(key),
            "value": value
        }
        return await SqlSet.get(sql_dict)

    # @staticmethod
    # async def get_student_info_like(names, key, value, page, pagesize):
    #     """模糊查询学生信息表.

    #     Args:
    #         names: 需要返回的列名(list)，当传入 ["*"] 时为全选
    #         key: 查询基于的键名（基于模块变量名，与表无关）
    #         value: 查询基于的键值
    #     Returns:
    #         由传入参数 names 决定，最多包括：
    #         `name`, `stuid`, `cardno`, `qq`, `dept`, `major`, `grade`
    #     """
    #     sql_dict = {
    #         "names": SqlSet.names_join(SqlSet.STUDENT_INFO_NAME_DICT, names),
    #         "table": "student_info",
    #         "key": "`{}`".format(key),
    #         "value": value
    #     }
    #     return await SqlSet.get(sql_dict)
