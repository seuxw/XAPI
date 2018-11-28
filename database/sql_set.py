# -*- coding: utf-8 -*-
# 数据库指令集

from asyncio import events
import pymysql
from tornado import gen

from database import db_pool


class SqlSet():

    @staticmethod
    async def get(SQL, arg, *args, fetchone=True):
        """查询数据库."""
        async with await db_pool.Connection() as conn:
            async with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                await cursor.execute(SQL, (arg))
                await conn.commit()
                if fetchone == True:
                    return cursor.fetchone()
                else:
                    return cursor.fetchall()

    GET_DICTIONARY = """
        SELECT
            `value`, `secret`, `remark`, `create_datetime`
        FROM
            testsmallwei.dictionary
        WHERE
            `key` = %s;"""

    @staticmethod
    async def get_dictionary(key):
        """查询词库中对应的回复.
        Args: 
            key
        Returns: 
            value, secret, remark, create_datetime
        """
        return await SqlSet.get(SqlSet.GET_DICTIONARY, key)
