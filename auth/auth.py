# -*- coding: utf-8 -*-
# JWT 身份验证模块

import configparser

import jwt

INFO = {"author": "smallwei", "version": "2.1"}


class JwtAuth(object):
    """JWT 身份验证类."""
    __instance = None

    def __new__(cls, *args, **kwargs):
        """单例模式实现."""
        if cls.__instance is None:
            cls.__instance = super(
                JwtAuth, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        """身份验证类配置."""
        conf = configparser.ConfigParser()
        conf.read("./auth/auth.cfg")
        self.AUTHORIZATION_HEADER = conf["AUTH_CFG"]["AUTHORIZATION_HEADER"]
        self.AUTHORIZATION_METHOD = conf["AUTH_CFG"]["AUTHORIZATION_METHOD"]
        self.SECRET_KEY = conf["AUTH_CFG"]["SECRET_KEY"]
        self.ALGORITHMS = conf["AUTH_CFG"]["ALGORITHMS"]
        self.JWT_OPTIONS = {
            'verify_signature': True,
            'verify_exp': True,
            'verify_nbf': False,
            'verify_iat': True,
            'verify_iss': True,
            'verify_aud': True
        }
        self.TIMEOUT = 15552000  # 180 天
        # 用户类别 0-普通 10-VIP 20-管理 30-超级管理
        self.common = self._jwt(0)
        self.vip = self._jwt(10)
        self.admin = self._jwt(20)
        self.master = self._jwt(30)

    def _is_valid_header(self, parts):
        """header 验证."""
        return True if parts[0] == self.AUTHORIZATION_METHOD and len(parts) == 2 else False

    def _jwt(self, user):
        """JWT 身份验证.

        Args:
            user: 用户类别：0-普通 10-VIP 20-管理 30-超级管理
        """
        def decorator(handler_class):
            def wrap_execute(handler_execute):
                def require_auth(handler, kwargs):
                    get_auth = handler.request.headers.get(
                        self.AUTHORIZATION_HEADER)
                    if not get_auth:
                        handler.INFO = INFO
                        return handler.write_error_f(4012)

                    auth_parts = get_auth.split()
                    if not self._is_valid_header(auth_parts):
                        handler.INFO = INFO
                        return handler.write_error_f(4011)

                    token = auth_parts[1]
                    try:
                        jwt.decode(
                            token,
                            self.SECRET_KEY,
                            options=self.JWT_OPTIONS,
                            algorithms=self.ALGORITHMS)
                    except Exception as err:
                        handler.INFO = INFO
                        return handler.write_error_f(4011)
                    # TODO:
                    print(user)
                    return True

                def _execute(self, transforms, *args, **kwargs):
                    try:
                        require_auth(self, kwargs)
                    except Exception:
                        return False
                    return handler_execute(self, transforms, *args, **kwargs)
                return _execute

            handler_class._execute = wrap_execute(handler_class._execute)
            return handler_class
        return decorator


# 创建身份验证对象
auth = JwtAuth()
