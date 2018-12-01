# -*- coding: utf-8 -*-
# 数据库指令集

from asyncio import events
import datetime
import decimal

import pymysql

from database import db_pool


class SqlSet():

    DB = "testsmallwei"
    # 使用 %s 是为了使用 pymysql 自带的 execute 防注入
    GET_ONE = "SELECT {0} FROM {1}.{2} WHERE {3} = %s LIMIT 1;"
    # 禁用 GET_ALL，必须带 limit 限制
    GET_LIMIT = "SELECT {0} FROM {1}.{2} WHERE {3} {4} %s LIMIT %s, %s;"
    GET_COUNT = "SELECT COUNT(*) AS `count` FROM {0}.{1} WHERE {2} {3} %s;"

    @staticmethod
    async def get(sql_dict, fetch="one"):
        """查询数据库."""
        async def fetchone():
            await cursor.execute(sql, (sql_dict["value"]))
            return cursor.fetchone()

        async def fetchall(*sql_args):
            await cursor.execute(sql, (sql_args))
            return cursor.fetchall()

        async with await db_pool.Connection() as conn:
            async with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                if fetch == "one":
                    sql = SqlSet.GET_ONE.format(
                        sql_dict["names"], SqlSet.DB, sql_dict["table"],
                        sql_dict["key"])
                    return await fetchone()
                elif fetch == "count":
                    sql = SqlSet.GET_COUNT.format(
                        SqlSet.DB, sql_dict["table"],
                        sql_dict["key"], sql_dict["exp"])
                    return await fetchone()
                elif fetch == "limit":
                    sql = SqlSet.GET_LIMIT.format(
                        sql_dict["names"], SqlSet.DB, sql_dict["table"],
                        sql_dict["key"], sql_dict["exp"])
                    return await fetchall(sql_dict["value"],
                                          sql_dict["limit1"], sql_dict["limit2"])

    @staticmethod
    def names_join(names_dict, names):
        def as_format(names_dict, key):
            return "{0} AS `{1}`".format(names_dict[key], key)

        if names == ["*"]:
            names_list = [as_format(names_dict, key)
                          for key in names_dict.keys()
                          if key != "_others_"]
            names_list.append(names_dict["_others_"])
            return ", ".join(names_list)
        else:
            return ", ".join([as_format(names_dict, key)
                              if key in names_dict.keys()
                              else "`{}`".format(key)
                              for key in names])

    @staticmethod
    def page2limit(page, pagesize):
        return (page-1)*pagesize

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

    STUDENT_INFO_RENAME_DICT = {
        "stuid": "`stuNo`",
        "cardno": "`cardNo`",
        "qq": "`QQ`",
        "_others_": "`name`, `dept`, `major`, `grade`"
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
            "names": SqlSet.names_join(SqlSet.STUDENT_INFO_RENAME_DICT, names),
            "table": "student_info",
            "key": "`{}`".format(key),
            "value": value
        }
        return await SqlSet.get(sql_dict)

    @staticmethod
    async def get_student_info_like(names, key, value, page, pagesize):
        """模糊查询学生信息表.

        Args:
            names: 需要返回的列名(list)，当传入 ["*"] 时为全选
            key: 查询基于的键名（基于模块变量名，与表无关）
            value: 查询基于的键值
        Returns:
            由传入参数 names 决定，最多包括：
            `name`, `stuid`, `cardno`, `qq`, `dept`, `major`, `grade`
            和 {"count": 符合查询条件总个数统计}
        """
        sql_dict = {
            "names": SqlSet.names_join(SqlSet.STUDENT_INFO_RENAME_DICT, names),
            "table": "student_info",
            "key": "`{}`".format(key),
            "exp": "LIKE",
            "value": value,
            "limit1": SqlSet.page2limit(page, pagesize),
            "limit2": pagesize
        }
        return await SqlSet.get(sql_dict, "limit"), await SqlSet.get(sql_dict, "count")

    @staticmethod
    async def get_course_table_all(value):
        """查询词库中对应的回复.

        Args: 
            value: 对应 `stuid`
        Returns: 
            `id`, `course0`, ..., `course14`, `stuNo`
        """
        sql_dict = {
            "names": "*",
            "table": "coursetable",
            "key": "`stuNo`",
            "value": value
        }
        return await SqlSet.get(sql_dict)

    @staticmethod
    async def get_paocao(value):
        """查询词库中对应的回复.

        Args: 
            value: 对应 `cardno`
        Returns: 
            `count_paocao`, `modify_date`
        """
        async def update_paocao_use():
            """更新跑操调用次数，并返回."""
            INSERT_SQL = """
                INSERT INTO {0}.{1}
                    (`use_date`, `use_count`)
                VALUES
                    (%s, 1)
                ON DUPLICATE KEY
                UPDATE
                    `use_count` = `use_count` + 1;"""
            SELECT_SQL = """
                SELECT
                    `use_count`
                FROM
                    {0}.{1}
                WHERE
                    `use_date` = %s;"""
            INSERT_SQL = INSERT_SQL.format(SqlSet.DB, "s_paocao_use")
            SELECT_SQL = SELECT_SQL.format(SqlSet.DB, "s_paocao_use")
            async with await db_pool.Connection() as conn:
                async with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    today = str(datetime.date.today())
                    await cursor.execute(INSERT_SQL, (today))
                    await conn.commit()
                    await cursor.execute(SELECT_SQL, (today))
                    return cursor.fetchone()["use_count"]

        async def get_paocao_rank():
            SELECT_SQL = """
                SELECT
                    100 - COUNT(1) / 8007 * 100 AS `rank`
                FROM
                    {0}.{1}
                WHERE
                    (`card_no` LIKE '21316%%'
                        OR `card_no` LIKE '21317%%')
                        AND `count_paocao` >= %s;"""
            SELECT_SQL = SELECT_SQL.format(SqlSet.DB, sql_dict["table"])
            async with await db_pool.Connection() as conn:
                async with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    await cursor.execute(SELECT_SQL, (get_paocao["count_paocao"]))
                    rank = cursor.fetchone()["rank"]
            rank = str(decimal.Decimal(str(rank)).quantize(
                decimal.Decimal('0.000')))
            return rank

        sql_dict = {
            "names": "`count_paocao`, `modify_date`",
            "table": "s_paocao",
            "key": "`card_no`",
            "value": value
        }
        get_paocao = await SqlSet.get(sql_dict)
        return await update_paocao_use(), get_paocao, await get_paocao_rank()
