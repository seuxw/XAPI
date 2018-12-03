# -*- coding: utf-8 -*-
# 此接口为跑操爬虫相关接口

from asyncio import events
import traceback

from auth import jwtauth, COMMON
from database import SqlSet
from handler import BaseHandler
from log import LogBase
from route import app
logger = LogBase().get_logger("PaocaoSpider")


@app.route(r'/basicTool/paocaoSpider')
@jwtauth(user=COMMON)
class PaocaoSpiderHandler(BaseHandler):
    INFO = {"author": "zzccchen", "version": "2.0"}

    async def update_paocao_use(self):
        """更新跑操调用次数，并返回."""

        INSERT_SQL = """
            INSERT INTO testsmallwei.s_paocao_use
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
                testsmallwei.s_paocao_use
            WHERE
                `use_date` = %s;"""

        with (yield db_pool.Connection()) as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                today = str(datetime.date.today())
                yield cursor.execute(INSERT_SQL, (today))
                yield conn.commit()
                yield cursor.execute(SELECT_SQL, (today))
                get_use_count = cursor.fetchone()
                yield conn.commit()
        raise gen.Return(get_use_count["use_count"])

    @gen.coroutine
    def get_rank(self, count):
        SELECT_SQL = """
            SELECT
                100 - COUNT(1) / 8007 * 100 AS `rank`
            FROM
                testsmallwei.s_paocao
            WHERE
                (`card_no` LIKE '21316%%'
                    OR `card_no` LIKE '21317%%')
                    AND `count_paocao` >= %s;"""

        with (yield db_pool.Connection()) as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                yield cursor.execute(SELECT_SQL, (count))
                rank = cursor.fetchone()["rank"]
                yield conn.commit()

        rank = str(decimal.Decimal(str(rank)).quantize(
            decimal.Decimal('0.000')))
        raise gen.Return(rank)

    @gen.coroutine
    def get(self, *args, **kwargs):
        cardno = self.get_argument_cardno()
        if not cardno:
            return self.finish()

        use = yield self.update_paocao_use()

        SELECT_SQL = """
            SELECT
                `count_paocao`,
                `modify_date`
            FROM
                testsmallwei.s_paocao
            WHERE
                `card_no` = %s;"""

        with (yield db_pool.Connection()) as conn:
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    yield cursor.execute(SELECT_SQL, (cardno))
                    get_paocao = cursor.fetchone()
                    yield conn.commit()

                    if not get_paocao:
                        return self.write_error_f(4041)

                    count = get_paocao["count_paocao"]
                    rank = yield self.get_rank(count)

                    data = {
                        "count": count,
                        "time": str(get_paocao["modify_date"]),
                        "rank": rank,
                        "use": use
                    }
                    return self.write_json_f(data)

            except Exception as e:
                logger.error(traceback.format_exc())
                return self.write_error_f(5001)
