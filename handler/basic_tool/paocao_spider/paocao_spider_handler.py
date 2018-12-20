# -*- coding: utf-8 -*-
# 此接口为跑操爬虫相关接口

import base64
import codecs
import hashlib
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

MD5_SET = "MD5_SET"
MD5_COUNT = "count"


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
        return zlib.decompress(gzip_data, zlib.MAX_WBITS | 32).decode('UTF-8')

    def data_push(self, data_md5, data):
        if not redis_session.sismember(MD5_SET, data_md5):
            redis_session.sadd(MD5_SET, data_md5)
            redis_session.hset(data_md5, "data", data)
        redis_session.hincrby(data_md5, MD5_COUNT, 1)
        # print(redis_session.hget(data_md5, MD5_COUNT))

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
            # print(gzip_data)
            data = self.decompress(gzip_data)
            # print(data)
            data_md5 = hashlib.md5(
                data.encode('UTF-8')).hexdigest()
            print(data_md5)
            self.data_push(data_md5, data)
            return self.write_json_f()
        except Exception as e:
            logger.error(traceback.format_exc())
            return self.write_error_f(5001)
