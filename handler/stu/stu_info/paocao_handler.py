# coding=utf8
# 此接口为学生信息查询接口

from asyncio import events
import traceback

from auth import auth
from database import SqlSet
from handler import BaseHandler
from log import LogBase
from route import app
logger = LogBase().get_logger("Paocao")


@app.route(r'/stu/stuInfo/paocaoD')
@auth.admin
class PaocaoDHandler(BaseHandler):
    """获取最后一次打卡的次数和打卡时间."""
    INFO = {"author": "zzccchen", "version": "2.0"}

    async def get(self, *args, **kwargs):
        cardno = self.get_argument_cardno()
        if not cardno:
            return self.finish()
        try:
            use, get_paocao, rank = await SqlSet.get_paocao(cardno)
            if not get_paocao:
                return self.write_error_f(4041)
            data = {
                "count": get_paocao["count_paocao"],
                "time": str(get_paocao["modify_date"]),
                "rank": rank,
                "use": use
            }
            return self.write_json_f(data)
        except Exception as e:
            logger.error(traceback.format_exc())
            return self.write_error_f(5001)
