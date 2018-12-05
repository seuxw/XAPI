# -*- coding: utf-8 -*-
# 所有Handler基类

import copy

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """所有Handler基类.

    重载了输出方法，
    正确输出(200)使用write_rsp方法，错误输出使用write_error方法
    """

    # 输出模板
    RSP = {
        "code": "200",
        "message": "OK",
        "relationships": {
            "author": "null"
        },
        "jsonapi": {
            "version": "null"
        }}

    # 输出JSON
    rsp = dict

    pagination = None

    _ARG_DEFAULT = object()

    def get_argument_t(self, name, default=_ARG_DEFAULT, type=None, strip=True):
        """重载get_argument方法，并判断参数类型是否匹配.

        输出时如果满足参数类型要求，则按类型输出，否则输出None
        """
        arg = self.get_argument(name, default, strip)
        if type == int:
            if not isinstance(arg, int):
                arg = int(arg) if arg.isdigit() else None
        return arg

    def get_argument_cardno(self, default=0):
        """获取cardno参数，并校验."""
        cardno = self.get_argument_t('cardno', default, int)
        if not cardno or cardno < 213000000 or cardno > 213359999:
            return self.write_error(4001)
        return cardno

    def get_argument_qq(self, default=0):
        """获取qq参数，并校验."""
        qq = self.get_argument_t('qq', default, int)
        if not qq:
            return self.write_error(4002)
        return qq

    def get_argument_stuid(self, default=None):
        """获取stuid参数，并校验."""
        stuid = self.get_argument('stuid', default)
        if not stuid or len(stuid) != 8:
            return self.write_error(4003)
        return stuid

    def get_argument_page(self, default=1):
        """获取page参数，并校验."""
        page = self.get_argument_t('page', default, int)
        if not page or page <= 0:
            return self.write_error(4005)
        return page

    def get_argument_pagesize(self, default=10):
        """获取pagesize参数，并校验."""
        pagesize = self.get_argument_t('pagesize', default, int)
        if not pagesize or pagesize <= 0:
            return self.write_error(4006)
        return pagesize

    def write_json_f(self, data=None):
        """重载write方法，并finish.

        Args:
            data: 输出JSON的data字段，默认为空
        """
        self.write_json(data)
        self.finish()

    def write_json(self, data=None):
        """重载write方法.

        Args:
            data: 输出JSON的data字段，默认为空
        """
        self.rsp = copy.deepcopy(self.RSP)
        if self.pagination:
            self.rsp["pagination"] = self.pagination
        self._write_json(data)

    def _write_json(self, data=None):
        """输出准备."""
        if data:
            self.rsp["data"] = data
        self.rsp["relationships"]["author"] = self.INFO["author"]
        self.rsp["jsonapi"]["version"] = self.INFO["version"]
        self.write(self.rsp)

    def write_error_f(self, status_code):
        """重载write_error方法，并finish.

        Args:
            status_code: HTTP状态码
        """
        self.write_error(status_code)
        self.finish()

    def write_error(self, status_code, **kwargs):
        """重载write_error方法.

        Args:
            status_code: HTTP状态码
        """
        self.rsp = copy.deepcopy(self.RSP)
        self._transforms = []
        self._write_error(status_code)

    def _write_error(self, status_code):
        """write_error输出的准备.

        Args:
            status_code: HTTP状态码，根据此参数配置输出内容
        """
        status_code = str(status_code)
        status_code_b, status_code_s = status_code[:3], status_code[3:]

        self.rsp["code"] = status_code_b

        if status_code_b == "400":
            self.set_status(400)
            self.rsp["message"] = "Bad Request"

            if status_code_s == "1":
                self.rsp["errors"] = {"code": 4001,
                                      "message": "Wrong Type Of Cardno"}
            elif status_code_s == "2":
                self.rsp["errors"] = {"code": 4002,
                                      "message": "Wrong Type Of QQ"}
            elif status_code_s == "3":
                self.rsp["errors"] = {"code": 4003,
                                      "message": "Wrong Type Of Stuid"}
            elif status_code_s == "4":
                self.rsp["errors"] = {"code": 4004,
                                      "message": "This QQ Has Registered"}
            elif status_code_s == "5":
                self.rsp["errors"] = {"code": 4005,
                                      "message": "Wrong Type Of Page"}
            elif status_code_s == "6":
                self.rsp["errors"] = {"code": 4006,
                                      "message": "Wrong Type Of Pagesize"}
            elif status_code_s == "7":
                self.rsp["errors"] = {"code": 4007,
                                      "message": "Signin Before Sun Rise"}
            elif status_code_s == "8":
                self.rsp["errors"] = {"code": 4008,
                                      "message": "Has signed"}
            elif status_code_s == "9":
                self.rsp["errors"] = {"code": 4009,
                                      "message": "Wrong Type Of Week"}
            elif status_code_s == "10":
                self.rsp["errors"] = {"code": 40010,
                                      "message": "Wrong Type Of Nickname"}
            elif status_code_s == "11":
                self.rsp["errors"] = {"code": 40011,
                                      "message": "Wrong Type Of Name"}
            else:
                self.rsp["errors"] = {"code": status_code,
                                      "message": "Undefined Error"}

        elif status_code_b == "401":
            self.set_status(401)
            self.rsp["message"] = "Unauthorized"

            if status_code_s == "1":
                self.rsp["errors"] = {"code": 4011,
                                      "message": "Invalid Header Authorization"}
            elif status_code_s == "2":
                self.rsp["errors"] = {"code": 4012,
                                      "message": "Missing Authorization"}
            elif status_code_s == "3":
                self.rsp["errors"] = {"code": 4013,
                                      "message": "Wrong Authorization Level"}
            else:
                self.rsp["errors"] = {"code": status_code,
                                      "message": "Undefined Error"}

        elif status_code_b == "404":
            self.set_status(404)
            self.rsp["message"] = "Not Found"

            if status_code_s == "1":
                self.rsp["errors"] = {"code": 4041,
                                      "message": "Not Found This Cardno In MySQL Server"}
            elif status_code_s == "2":
                self.rsp["errors"] = {"code": 4042,
                                      "message": "This QQ Not Bound"}
            elif status_code_s == "3":
                self.rsp["errors"] = {"code": 4043,
                                      "message": "Not Found This Stuid In MySQL Server"}
            elif status_code_s == "4":
                self.rsp["errors"] = {"code": 4044,
                                      "message": "Not Found This Name In MySQL Server"}
            elif status_code_s == "5":
                self.rsp["errors"] = {"code": 4045,
                                      "message": "This Cardno Not Bound QQ"}
            elif status_code_s == "6":
                self.rsp["errors"] = {"code": 4046,
                                      "message": "This QQ Not Registered"}
            elif status_code_s == "7":
                self.rsp["errors"] = {"code": 4047,
                                      "message": "Not Found This Key In Word Dictionary"}
            else:
                self.rsp["errors"] = {"code": status_code,
                                      "message": "Undefined Error"}

        elif status_code_b == "405":
            self.set_status(405)
            self.rsp["message"] = "Method Not Allowed"
            self.rsp["errors"] = {"code": 405,
                                  "message": self._reason}

        elif status_code_b == "500":
            self.set_status(500)
            self.rsp["message"] = "Internal Server Error"

            if status_code_s == "1":
                self.rsp["errors"] = {"code": 5001,
                                      "message": "Unknown Server Error"}
            elif status_code_s == "2":
                self.rsp["errors"] = {"code": 5002,
                                      "message": "MySQL Server Error"}
            else:
                self.rsp["errors"] = {"code": status_code,
                                      "message": "Undefined Error"}

        else:
            self.rsp["message"] = "Undefined Error"
            self.rsp["errors"] = {"code": status_code,
                                  "message": "Undefined Error"}

        self._write_json()
