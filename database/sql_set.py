# -*- coding: utf-8 -*-
# 数据库指令集

from asyncio import events
import pymysql
from tornado import gen

from database import db_pool


class SqlSet():

    DB = "testsmallwei"
    GET_ALL = "SELECT {0} FROM {1}.{2} WHERE {3} = %s;"
    GET_ONE = "SELECT {0} FROM {1}.{2} WHERE {3} = %s LIMIT 1;"

    @staticmethod
    async def get(sql_dict, fetchone=True):
        """查询数据库."""
        async with await db_pool.Connection() as conn:
            async with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                if fetchone == True:
                    sql = SqlSet.GET_ONE.format(
                        sql_dict["names"], SqlSet.DB, sql_dict["table"],
                        sql_dict["key"])
                    await cursor.execute(sql, (sql_dict["value"]))
                    return cursor.fetchone()
                else:
                    sql = SqlSet.GET_ALL.format(
                        sql_dict["names"], SqlSet.DB, sql_dict["table"],
                        sql_dict["key"])
                    await cursor.execute(sql, (sql_dict["value"]))
                    return cursor.fetchall()

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

    # @staticmethod
    # async def get_student_info(key, value):
    #     """查询词库中对应的回复.
    #     Args:
    #         key: 查询的键名（基于模块变量名，与表无关）
    #         value: 查询的键值
    #     Returns:
    #         value, secret, remark, create_datetime
    #     """
    #     GET_DICTIONARY = """
    #         SELECT
    #             `value`, `secret`, `remark`, `create_datetime`
    #         FROM
    #             %s.dictionary
    #         WHERE
    #             `key` = %s;"""
    #     return await SqlSet.get(GET_DICTIONARY, key)
