#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import os
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from handler import BaseHandler
from log import LogBase
from route import app
logger = LogBase().get_logger("Main")


@app.route(r'/')
class HelloHandler(BaseHandler):
    """hello world模块."""
    INFO = {"author": "zzccchen", "version": "2.0"}

    def get(self, *args, **kwargs):
        return self.write_json_f({"greet": "Hello Smallwei"})


def main():
    try:
        logger.info("Xapi start")

        # http_server = tornado.httpserver.HTTPServer(app, ssl_options={
        #     "certfile": os.path.join(os.path.abspath("."), "server.crt"),
        #     "keyfile": os.path.join(os.path.abspath("."), "server.key"),
        # }, xheaders=True)

        # http_server.listen(8895)
        app.listen(8895)
        IOLoop.current().start()

    except KeyboardInterrupt:
        logger.info("Xapi exit")


if __name__ == '__main__':
    main()
