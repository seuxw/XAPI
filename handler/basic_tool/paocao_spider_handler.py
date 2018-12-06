# -*- coding: utf-8 -*-
# 此接口为跑操爬虫相关接口

from asyncio import events
import traceback

from auth import auth
from database import SqlSet
from handler import BaseHandler
from log import LogBase
from route import app
logger = LogBase().get_logger("PaocaoSpider")


@app.route(r'/basicTool/paocaoSpider')
@auth.common
class PaocaoSpiderHandler(BaseHandler):
    INFO = {"author": "zzccchen", "version": "2.0"}

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
