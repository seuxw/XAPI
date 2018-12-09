# -*- coding: utf-8 -*-
# 此接口为跑操爬虫相关接口

import base64
import codecs
import json
import traceback
import zlib
from asyncio import events

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from auth import auth
from database import SqlSet, redis_session
from handler import BaseHandler
from log import LogBase
from route import app

logger = LogBase().get_logger("PaocaoSpider")


@app.route(r'/basicTool/paocaoSpider')
@auth.common
class PaocaoSpiderHandler(BaseHandler):
    INFO = {"author": "zzccchen", "version": "2.0"}

    def decrypt(self, raw_data):
        key = b'1234123412ABCDEF'
        iv = b'ABCDEF1234123412'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64decode(unpad(cipher.decrypt(codecs.decode(raw_data, 'hex')),
                                      AES.block_size))

    def decompress(self, gzip_data):
        return json.loads(zlib.decompress(gzip_data, zlib.MAX_WBITS | 32))

    def get(self, *args, **kwargs):
        try:
            jsid = redis_session.get(redis_session.jsid)
            return self.write_json_f({"jsid": jsid})
        except Exception as e:
            logger.error(traceback.format_exc())
            return self.write_error_f(5001)

    def post(self, *args, **kwargs):
        try:
            raw_data = json.loads(self.request.body).get("data")
            gzip_data = self.decrypt(raw_data)
            print(gzip_data)
            json_data = self.decompress(gzip_data)
            print(json_data)
            # return self.write_json_f({"cardno": cardno})
        except Exception as e:
            logger.error(traceback.format_exc())
            return self.write_error_f(5001)
